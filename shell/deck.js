
(function(){
  "use strict";
  var root = document.documentElement;

  /* ---------------------------------------------------------- the preflight's other half (DS-009) */
  /* The preflight ran before this file was parsed. If its marker survived, this browser cannot
     present the deck: the flowed document is already on screen and the chrome that would drive it
     is hidden, so booting would rebuild a reading view nobody can reach and re-hide eleven slides
     out of twelve. Stand down and leave the reader with the document. */
  if (root.hasAttribute('data-preflight')) return;

  /* And the net under it, for the capability nobody enumerated. A check set cannot be complete, so
     a boot that throws puts the marker back and the recipient reads the deck rather than a blank
     stage. Scoped to BOOT deliberately - `booted` is set on the last line of this function - because
     a chart that throws on slide nine must not collapse a deck somebody is already reading. */
  var booted = false;
  window.addEventListener('error', function(e){
    if (booted) return;
    root.setAttribute('data-preflight','fail');
    var say = document.getElementById('preflightSay');
    if (say) say.textContent = 'This deck could not start in this browser'
      + ((e && e.message) ? ' (' + e.message + ')' : '')
      + ". Every slide's content is below instead, in order.";
  });

  var stage = document.getElementById('stage');
  var viewport = document.getElementById('viewport');
  var slides = Array.prototype.slice.call(stage.querySelectorAll('.slide'));
  var countBox = document.getElementById('count');
  var rulerEl = document.getElementById('ruler');
  var rulerTicks = document.getElementById('rulerTicks');
  var rulerLabel = document.getElementById('rulerLabel');
  var rulerRing = document.getElementById('rulerRing');
  var doc = document.getElementById('doc');
  var docBody = document.getElementById('docBody');
  var toDoc = document.getElementById('toDoc');
  var toStage = document.getElementById('toStage');
  var motionBtn = document.getElementById('motion');
  var moreBtn = document.getElementById('moreBtn');
  var moreMenu = document.getElementById('moreMenu');
  var DECK = '{{DECK_NAME}}';

  /* the deck's argument, lit stage by stage (DS-134) */
  var STAGES = [{{STAGES}}];
  var idx = 0, played = {}, inDoc = false;

  /* ---------------------------------------------------------- stage scaling (DS-060/062) */
  function fit(){
    var k = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
    /* a viewport reported as zero during start-up would otherwise scale the stage to nothing */
    if (!isFinite(k) || k <= 0) k = 1;
    stage.style.setProperty('--k', k);
  }

  /* ---------------------------------------------------------- chrome, built from the slides */
  /* where each stage starts, read from the slides rather than declared twice (L-08) */
  function firstSlideOfStage(st){
    for (var n = 0; n < slides.length; n++){
      if (parseInt(slides[n].dataset.stage, 10) === st) return n;
    }
    return 0;
  }

  /* ------------------------------------------------------------------ the slide manifest */
  /* Number, title, bottom line, stage and mark for every slide, read off the slides rather
     than authored a second time. This is the ONE derivation: the printed contents page
     (T-034) and the on-screen index (T-035) are two RENDERINGS of it, not two readings of
     the deck - which is how the two would drift (L-08). Same principle as firstSlideOfStage
     above and as buildDoc() cloning slides instead of re-authoring them.

     Add a field here rather than reading a slide directly from a renderer. */
  /* the mark is keyed to the STAGE, never to slide content - so it does not matter that
     slide 1 carries no disclosure panel where the other eleven carry one */
  var STAGE_ICON = [{{STAGE_ICON}}];

  /* Back matter is a slide that is not part of the argument - a colophon, an appendix, a sources
     page - and `data-stage="back"` is how it says so (T-108). Before this it had nowhere to go:
     `data-stage` is mandatory and held only argument stages, so back matter was pushed into the
     nearest one and every rendering of the census inherited the miscount.

     Two consequences follow from rules already written, rather than from taste. It carries NO MARK,
     because DS-113/114 key the mark to the stage and this slide has no stage - so the absence is
     the rule holding. And its label is a constant here rather than a deck-supplied word, because
     there is no stage entry to read one from; `Back matter` is also true of all three of the things
     it names, where `Colophon` is true of one. */
  var BACK_MATTER = 'Back matter';

  function manifest(){
    return slides.map(function(s, i){
      var b = s.querySelector('.bottom-line');
      var raw = (s.dataset.stage || '').trim();
      var back = raw === 'back';
      var st = parseInt(raw, 10);
      if (isNaN(st) || st < 0 || st >= STAGES.length) st = 0;
      return {
        n:         i + 1,
        title:     s.dataset.name || '',
        bottom:    b ? b.textContent.replace(/\s+/g, ' ').trim() : '',
        back:      back,
        stage:     back ? null : st,
        stageName: back ? BACK_MATTER : STAGES[st],
        icon:      back ? null : STAGE_ICON[st]
      };
    });
  }

  /* ------------------------------------------------------------------------ the ruler (T-035) */
  /* Built from manifest(), the same derivation the printed contents page renders (T-034). The two
     are renderings of one source rather than two readings of the deck (L-08).

     48 du is the pitch, not a minimum bolted on afterwards: DS-168's target floor inside the stage
     is 48 x 48, because the stage bottoms out at 0.5 scale. The label needs room on the same row,
     so capacity is what is left after it - measured below rather than assumed. */
  /* The pitch is `--disc-hit` = 52 du, the deck's existing target-size token, not DS-168's bare 48
     floor - the token already sits above the floor on purpose and reusing it keeps a tick the same
     size as every other hit target in the deck. Written here as a number because the arithmetic
     needs one; tools/deck/chrome_row.py measures the rendered tick and fails if the two disagree. */
  var TICK_PITCH_DU = 52;
  var LABEL_MIN_DU = 260;

  function rulerLayout(n, availDu){
    var capacity = Math.floor((availDu - LABEL_MIN_DU) / TICK_PITCH_DU);
    return { capacity: capacity, dense: n > capacity };
  }
  /* exported for tools/deck/chrome_row.py, so the bound it reports is the rule the deck SHIPS
     rather than a copy kept in step by hand (L-08) */
  window.htmldeckRulerLayout = rulerLayout;

  /* What the ruler actually has: the NAVIGATION CONTAINER, less its other children and the gaps
     between them. Measured rather than derived, because the controls cost 32% of the row and that
     was the number T-035's paper estimate of "~30 targets" got wrong.
     The subject moved from the row to the box in T-114, and the change is not cosmetic: `More` and
     `Motion` now sit outside the container, so a row-wide measurement would hand the ruler width
     that belongs to controls it does not share a box with. Every non-ruler child is subtracted by
     measurement rather than by name, so a deck whose tail form differs - `Motion` in the menu or
     beside it - does not change what this function has to know. */
  function rulerAvailableDu(){
    var kk = parseFloat(getComputedStyle(stage).getPropertyValue('--k')) || 1;
    var boxEl = document.querySelector('.navbox');
    if (!boxEl || !rulerEl || !kk) return 0;
    /* The CONTENT box, not the border box. The container is drawn (T-114) - a hairline and a
       horizontal pad - and those are width the ruler cannot have. Measuring the outer rectangle
       reported 34 du the ticks were never going to get, which is the same shape of error as the
       paper estimate this function replaced. */
    var cs = getComputedStyle(boxEl);
    function px(v){ var n = parseFloat(v); return isFinite(n) ? n / kk : 0; }
    var bw = boxEl.getBoundingClientRect().width / kk
             - px(cs.paddingLeft) - px(cs.paddingRight)
             - px(cs.borderLeftWidth) - px(cs.borderRightWidth);
    var gap = px(cs.gap);
    var taken = 0, n = 0;
    Array.prototype.forEach.call(boxEl.children, function(el){
      n++;
      if (el !== rulerEl) taken += el.getBoundingClientRect().width / kk;
    });
    return bw - taken - gap * (n - 1);
  }

  var MAN = manifest();

  function buildRuler(){
    MAN.forEach(function(m, i){
      /* Back matter starts no section, and the guard is load-bearing rather than tidy:
         `firstSlideOfStage(null)` matches nothing and returns 0, so without it the deck's FIRST
         slide would be re-declared a section every time a back-matter slide was drawn (T-108). */
      var isSection = !m.back && firstSlideOfStage(m.stage) === i;
      var li = document.createElement('li');
      li.dataset.slide = i;
      if (isSection) li.dataset.section = '';

      var b = document.createElement('button');
      b.type = 'button';
      b.tabIndex = -1;                 /* roving: only the current tick is in the tab order */
      /* The accessible name is independent of the visible swap, because the swap is for the eye
         (DS-163). A section tick names its stage AND its slide; a small tick names its own slide,
         never its section - twelve targets carrying seven labels would be exactly the unnamed
         targets DS-131 forbids. */
      b.setAttribute('aria-label', isSection
        ? 'Go to ' + m.stageName + ': ' + m.title
        : 'Go to slide ' + m.n + ': ' + m.title);
      b.dataset.label = isSection ? m.stageName : m.title;
      b.addEventListener('click', function(){ go(i); countIfSeen(); });
      b.addEventListener('mouseenter', function(){ previewLabel(b.dataset.label); });
      b.addEventListener('mouseleave', restoreLabel);
      b.addEventListener('focus', function(){ previewLabel(b.dataset.label); });
      b.addEventListener('blur', restoreLabel);
      li.appendChild(b);
      rulerTicks.appendChild(li);
    });
  }

  /* Where the ring sits, MEASURED off the current tick rather than computed from the pitch. The
     pitch is only uniform while the ruler is undegraded, and a ring that assumed it would drift
     the moment the small ticks collapsed - so it is read from the box instead. Inside the stage a
     design unit is one CSS pixel before the transform, which is why dividing by --k gives units. */
  function placeRing(){
    if (!rulerRing) return;
    var li = rulerTicks.children[idx];
    if (!li) return;
    var kk = parseFloat(getComputedStyle(stage).getPropertyValue('--k')) || 1;
    var lr = rulerEl.getBoundingClientRect();
    var tr = li.getBoundingClientRect();
    if (!tr.width) return;                      /* hidden, e.g. in the reading view */
    rulerEl.style.setProperty('--rx', ((tr.left + tr.width / 2 - lr.left) / kk) + 'px');
  }

  function previewLabel(text){
    rulerLabel.textContent = text;
    rulerLabel.setAttribute('data-preview','');
  }
  /* At rest the ruler names the STAGE, where hover names the slide (DS-163). Back matter has no
     stage to name, so it falls back to its own title - which is also what the reporter of T-108 saw
     the lack of: a colophon captioned `Decision`, the stage it had been forced into. */
  function restoreLabel(){
    rulerLabel.removeAttribute('data-preview');
    var m = MAN[idx];
    rulerLabel.textContent = m ? (m.back ? m.title : m.stageName) : '';
  }

  /* Sized after layout, and again on resize - the controls' width is what decides capacity, and a
     label can change it. */
  function fitRuler(){
    var lay = rulerLayout(MAN.length, rulerAvailableDu());
    if (lay.dense) rulerEl.setAttribute('data-dense',''); else rulerEl.removeAttribute('data-dense');
    placeRing();
    /* Past the bound the small ticks are marks, not targets, so they leave the tab order and stop
       being clickable. Section ticks stay targets at full pitch. */
    Array.prototype.forEach.call(rulerTicks.children, function(li){
      var b = li.querySelector('button');
      if (!b) return;
      var isMark = lay.dense && li.dataset.section === undefined;
      b.disabled = isMark;
      if (isMark) b.tabIndex = -1;
    });
    return lay;
  }

  /* DS-137: the precedence rule, decided rather than left to whichever listener runs first.
     Arrow keys already advance the deck from a document-level listener, and the conventional idiom
     for a tick group is arrow-to-move-within-it. Both cannot own the arrows.
     RULE: while focus is inside the ruler, the arrows move between ticks and do NOT advance; Enter
     or Space jumps. Everywhere else they advance the deck, unchanged. Same shape as DS-166, where
     arrows advance and a separate key toggles disclosure - the two never interact. */
  function tickButtons(){
    return Array.prototype.slice.call(rulerTicks.querySelectorAll('button:not([disabled])'));
  }
  rulerTicks.addEventListener('keydown', function(e){
    var bs = tickButtons();
    var cur = bs.indexOf(document.activeElement);
    if (cur < 0) return;
    var to = -1;
    if      (e.key === 'ArrowRight') to = Math.min(bs.length - 1, cur + 1);
    else if (e.key === 'ArrowLeft')  to = Math.max(0, cur - 1);
    else if (e.key === 'Home')       to = 0;
    else if (e.key === 'End')        to = bs.length - 1;
    else return;
    e.preventDefault();
    e.stopPropagation();      /* belt; the document handler also checks, so neither relies on order */
    bs[cur].tabIndex = -1;
    bs[to].tabIndex = 0;
    bs[to].focus();
  });

  /* ---------------------------------------------------------- disclosure (one open at a time) */
  var discs = Array.prototype.slice.call(stage.querySelectorAll('[data-disc]'));
  discs.forEach(function(d){
    var btn = d.querySelector('.disc-btn');
    var panel = d.querySelector('.disc-panel');
    btn.addEventListener('click', function(){ toggleDisc(d, null); });
    panel.addEventListener('animationend', function(){ panel.classList.remove('opening'); });
  });

  function closeAllDiscs(except){
    discs.forEach(function(d){
      if (d === except) return;
      d.querySelector('.disc-btn').setAttribute('aria-expanded','false');
      d.querySelector('.disc-panel').hidden = true;
    });
  }
  /* precedence: opening any panel closes the other (DS-137) */
  function toggleDisc(d, force){
    var btn = d.querySelector('.disc-btn');
    var panel = d.querySelector('.disc-panel');
    var open = force === null ? btn.getAttribute('aria-expanded') !== 'true' : force;
    closeAllDiscs(d);
    closeAllSources(null);
    closeMore();
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    panel.hidden = !open;
    if (open) panel.classList.add('opening');
  }

  /* ------------------------------------------------ sources (DS-105, one open at a time) */
  /* Its own component and not a .disc - provenance is what the argument rests on rather than tier
     two (DS-230) - which is why it has its own list and its own toggle. It shares the precedence
     rule with the disclosure because a reader has one attention whatever the content is (DS-137). */
  /* A one-source mark has no button and its box never closes (T-103), so it is not one of these:
     there is nothing to toggle and nothing to close it for. Selecting on the button rather than on
     `.sources` is what keeps that true - the list below is *the disclosures*, not the marks. */
  var srcs = Array.prototype.slice.call(stage.querySelectorAll('.sources')).filter(function(s){
    return !!s.querySelector('.sources-btn');
  });
  srcs.forEach(function(s){
    var box = s.querySelector('.sources-box');
    s.querySelector('.sources-btn').addEventListener('click', function(){ toggleSources(s, null); });
    box.addEventListener('animationend', function(){ box.classList.remove('opening'); });
  });

  function closeAllSources(except){
    srcs.forEach(function(s){
      if (s === except) return;
      s.querySelector('.sources-btn').setAttribute('aria-expanded','false');
      s.querySelector('.sources-box').hidden = true;
    });
  }
  function toggleSources(s, force){
    var btn = s.querySelector('.sources-btn');
    var box = s.querySelector('.sources-box');
    var open = force === null ? btn.getAttribute('aria-expanded') !== 'true' : force;
    closeAllDiscs(null);
    closeAllSources(s);
    closeMore();
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    box.hidden = !open;
    if (open) box.classList.add('opening');
  }

  /* ------------------------------------------------ the quick view (DS-105, T-070) */
  /* One surface for the whole deck; what it shows is cloned from the cited slide's own
     <template class="qv-src">. The template is why nothing here has to be trusted: its content is
     inert to the parser, so a source loads, renders and runs nothing until this clone - and a
     <script> that arrived inside it does not execute when cloned either.

     Precedence is the disclosure's rule (DS-137): opening a source closes the panels, and the
     quick view closes both. Dismissal is Escape or the button, and advancing the deck closes it -
     a reader who moves on has already dismissed it. */
  var qv = document.getElementById('qv');
  var qvBody = document.getElementById('qvBody');
  var qvTitle = document.getElementById('qvTitle');
  var qvFile = document.getElementById('qvFile');
  var qvOpener = null;

  /* One document, however many slides cite it: the control is on every mark, the <template> is on
     the first, and this map is what joins them. Six copies of one source would be the size cost
     this feature has to justify, spent on nothing. */
  var qvSrc = {};
  Array.prototype.forEach.call(stage.querySelectorAll('template.qv-src'), function(tpl){
    qvSrc[tpl.getAttribute('data-qv')] = tpl;
  });
  /* Delegated, and that is not a style preference: buildDoc() clones every slide into the reading
     view, so the controls exist twice and the clones are made after this runs. Bound per element,
     the reading view's copies would be buttons that do nothing - and the reading view is where the
     deck is read alone, which is exactly the reader who wants the source. The map stays keyed off
     the STAGE's templates, so the clones show the same one document rather than their own copy. */
  document.addEventListener('click', function(e){
    var btn = e.target.closest && e.target.closest('.sources-open');
    if (!btn) return;
    var tpl = qvSrc[btn.getAttribute('data-qv')];
    if (!tpl) return;
    /* Whitespace-collapsed, because the title comes out of MARKUP: an author who wraps a long
       source title across two lines gets the newline and its indentation inside textContent, and
       the header then paints a line break and ten spaces where the deck's own name for the source
       should be. HTML already collapses it on the slide, so nothing looked wrong there (T-109). */
    openQuick(btn, btn.textContent.replace(/\s+/g, ' ').trim(), tpl,
              btn.getAttribute('data-file') || '');
  });
  document.getElementById('qvClose').addEventListener('click', function(){ closeQuick(); });
  /* The scrim dismisses; the sheet does not, or every scroll inside it would close the view. */
  qv.addEventListener('click', function(e){ if (e.target === qv) closeQuick(); });

  function openQuick(btn, title, tpl, file){
    closeAllDiscs(null);
    closeAllSources(null);
    closeMore();
    qvBody.textContent = '';
    /* The contracted container, not a wrapper for its own sake: COMPONENT-CONTRACT.md gives
       `.qv-doc` as an <article> this script creates inside `.qv-body`, and every rule that styles
       a source - headings, lists, tables, quotes, fences, rules - is written against it. Without
       it those 17 rules match nothing and a quoted source renders at slide scale (T-122). */
    var article = document.createElement('article');
    article.className = 'qv-doc';
    article.appendChild(tpl.content.cloneNode(true));
    qvBody.appendChild(article);
    qvTitle.textContent = title;
    /* The title is the deck's name for the source; this is the file it was rendered from, so a
       reader who wants the original knows what to look for. Cleared rather than left behind: the
       surface is shared, and a stale file name under a new title is worse than none (T-109). */
    qvFile.textContent = file || '';
    qv.hidden = false;
    /* Every opening starts at the top of ITS document, and the clear in closeQuick() is not enough
       to get that - it was measured doing its job and the offset came back anyway. Emptying the
       container really does take scrollTop to 0, because there is nothing left to scroll; the
       browser then RESTORES the offset the moment this function puts content back into the same
       element, which is a feature everywhere except here. So the reset belongs on the way in,
       after the content and after `hidden` clears, because a hidden element has no scroll height
       to assign against. Without it a reader who scrolled through one source and asked for the
       next one landed 82% of the way down a document they had never seen (T-174).

       Nothing here fights the focus call below: `qvClose` is in the header, a sibling of this
       container rather than a descendant, so focusing it cannot scroll the body. */
    qvBody.scrollTop = 0;
    qvOpener = btn;
    document.getElementById('qvClose').focus();
  }
  function closeQuick(){
    if (qv.hidden) return;
    qv.hidden = true;
    qvFile.textContent = '';
    qvBody.textContent = '';       /* the surface holds nothing between openings - but see the
                                      reset in openQuick(): emptying it does not decide where the
                                      NEXT document starts (T-174) */
    if (qvOpener) qvOpener.focus();
    qvOpener = null;
  }

  /* ---------------------------------------------------------- navigation */
  function go(i, opts){
    i = Math.max(0, Math.min(slides.length - 1, i));
    idx = i;
    closeQuick();
    closeAllDiscs(null);
    closeAllSources(null);
    closeMore();
    slides.forEach(function(s, n){
      var cur = n === i;
      if (cur) { s.setAttribute('data-current',''); } else { s.removeAttribute('data-current'); }
      /* off-screen slides leave the tab order (DS-132) */
      if (cur) { s.removeAttribute('inert'); s.removeAttribute('aria-hidden'); }
      else     { s.setAttribute('inert',''); s.setAttribute('aria-hidden','true'); }
    });
    /* charts and entrances draw in once, never on the way back (DS-146) */
    if (!played[i]) { played[i] = true; slides[i].setAttribute('data-played',''); }

    countBox.innerHTML = '';
    var strong = document.createElement('b');
    strong.textContent = (i + 1) < 10 ? '0' + (i + 1) : String(i + 1);
    countBox.appendChild(strong);
    countBox.appendChild(document.createTextNode(' / ' + slides.length));

    /* The ruler lights the SLIDE, where the ribbon lit the stage - the tick is per slide now, and
       the section ticks show the stage boundaries graphically. `aria-current` moves with it, as it
       did on the ribbon. Roving tabindex follows too, so tabbing into the ruler lands on where you
       actually are rather than on slide one. */
    Array.prototype.forEach.call(rulerTicks.children, function(li, n){
      var lit = n === i;
      if (lit) li.setAttribute('data-lit',''); else li.removeAttribute('data-lit');
      var b = li.querySelector('button');
      if (!b) return;
      if (lit) b.setAttribute('aria-current','true'); else b.removeAttribute('aria-current');
      if (!b.disabled) b.tabIndex = lit ? 0 : -1;
    });
    if (rulerLabel && !rulerLabel.hasAttribute('data-preview')) restoreLabel();
    placeRing();
    var name = slides[i].dataset.name;
    document.title = (name === DECK) ? DECK : name + ' — ' + DECK;
    if (opts && opts.focus) slides[i].focus();
  }

  document.addEventListener('keydown', function(e){
    if (e.target.matches('input,textarea')) return;
    var k = e.key;
    /* DS-137, the stated half of the precedence rule. The ruler's own handler already stops these
       propagating, and this says the same thing again on purpose: the rule is that the ruler owns
       the arrows while it holds focus, and a rule that depends on which listener was registered
       first is not a rule. */
    if (e.target.closest && e.target.closest('.ruler-ticks') &&
        (k === 'ArrowRight' || k === 'ArrowLeft' || k === 'Home' || k === 'End')) return;
    if (inDoc){
      if (k === 'Escape' || k === 'r' || k === 'R'){ setView(false); e.preventDefault(); }
      return;
    }
    if (k === 'ArrowRight' || k === 'PageDown' || k === ' ')      { go(idx+1); e.preventDefault(); }
    else if (k === 'ArrowLeft' || k === 'PageUp')                 { go(idx-1); e.preventDefault(); }
    else if (k === 'Home')                                        { go(0); e.preventDefault(); }
    else if (k === 'End')                                         { go(slides.length-1); e.preventDefault(); }
    else if (k === 'd' || k === 'D'){        /* disclosure never interacts with advancing (DS-166) */
      var d = slides[idx].querySelector('[data-disc]');
      if (d) { toggleDisc(d, null); e.preventDefault(); }
    }
    else if (k === 'Escape')     { closeQuick(); closeAllDiscs(null); closeAllSources(null); closeMore(); }
    else if (k === 'r' || k === 'R')                              { setView(true); e.preventDefault(); }
    else if (k === 'm' || k === 'M')                              { setMotion(root.dataset.motion === 'off'); }
    else if (k === 't' || k === 'T')                              { setTheme(root.dataset.theme === 'light' ? 'dark' : 'light'); }
    else if (k === 'f' || k === 'F'){
      if (document.fullscreenElement) document.exitFullscreen();
      else if (document.documentElement.requestFullscreen) document.documentElement.requestFullscreen();
    }
  });

  document.getElementById('prev').addEventListener('click', function(){ go(idx-1); });
  document.getElementById('next').addEventListener('click', function(){ go(idx+1); });

  var wheelLock = 0;
  viewport.addEventListener('wheel', function(e){
    var now = Date.now();
    if (now - wheelLock < 700) return;
    if (Math.abs(e.deltaY) < 20) return;
    wheelLock = now;
    go(idx + (e.deltaY > 0 ? 1 : -1));
  }, {passive:true});

  var tx = 0, ty = 0;
  viewport.addEventListener('touchstart', function(e){
    tx = e.changedTouches[0].clientX; ty = e.changedTouches[0].clientY;
  }, {passive:true});
  viewport.addEventListener('touchend', function(e){
    var dx = e.changedTouches[0].clientX - tx, dy = e.changedTouches[0].clientY - ty;
    if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy)) go(idx + (dx < 0 ? 1 : -1));
  }, {passive:true});

  /* ---------------------------------------------------------- motion and theme toggles */
  function setMotion(on){
    root.dataset.motion = on ? 'on' : 'off';
    motionBtn.textContent = on ? 'Motion on' : 'Motion off';
    motionBtn.setAttribute('aria-pressed', on ? 'false' : 'true');
  }
  motionBtn.addEventListener('click', function(){ setMotion(root.dataset.motion === 'off'); });
  function setTheme(t){ root.dataset.theme = t; }
  setMotion(!window.matchMedia('(prefers-reduced-motion: reduce)').matches);

  /* ---------------------------------------------------------- the More menu (T-114) */
  /* Chrome, not tier two. DS-230's four-kind vocabulary is closed and this is not content the
     face provokes a question about, so `More` is its own component rather than a `.disc` - the
     same footing DS-105 gives `.sources`. It obeys the disclosure INTERACTION rules regardless,
     because a reader has one attention whatever the content is: a real label (DS-164), click
     rather than hover (DS-163), shut at load (DS-227), and one thing open at a time (DS-137) -
     which is why `closeMore()` is called at each of the four sites that already close the other
     two, and why opening the menu closes them.
     WHAT IS IN THE MENU IS NOT THIS SCRIPT'S BUSINESS. `Motion` leaves it when the deck loops
     (DS-218, step 7a) and the markup decides that at build time, so nothing here addresses a menu
     item by name - `motionBtn` is found by id and works from either parent. */
  function closeMore(){
    if (!moreMenu) return;
    moreMenu.hidden = true;
    moreBtn.setAttribute('aria-expanded', 'false');
  }
  function toggleMore(force){
    if (!moreMenu) return;
    var open = force === null || force === undefined
      ? moreBtn.getAttribute('aria-expanded') !== 'true' : force;
    closeAllDiscs(null);
    closeAllSources(null);
    moreMenu.hidden = !open;
    moreBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    /* Opening moves focus into the menu, because the control that opened it is the last thing a
       keyboard reader touched and the menu is what they asked for. Escape puts it back: a menu
       dismissed while still holding focus leaves the keyboard nowhere. */
    if (open){ var first = moreMenu.querySelector('.btn'); if (first) first.focus(); }
  }
  if (moreBtn && moreMenu){
    moreBtn.addEventListener('click', function(){ toggleMore(null); });
    moreMenu.addEventListener('keydown', function(e){
      if (e.key === 'Escape'){ closeMore(); moreBtn.focus(); e.preventDefault(); e.stopPropagation(); }
    });
    /* Choosing an item shuts the menu. `Read` switches view and hides the chrome anyway; `Motion`
       does not, and a menu left standing open over the deck after a toggle is the state DS-227
       exists to prevent. */
    moreMenu.addEventListener('click', function(){ closeMore(); });
    /* A click anywhere else dismisses. Bound on the document rather than on a scrim, because a
       two-item chrome menu that laid a scrim over the deck would block the stage to close itself. */
    document.addEventListener('click', function(e){
      if (!e.target.closest || !e.target.closest('.more')) closeMore();
    });
  }

  /* ---------------------------------------------------------- the reflow view (DS-070..076) */
  function buildDoc(){
    slides.forEach(function(s, i){
      var c = s.cloneNode(true);
      c.removeAttribute('style'); c.removeAttribute('inert'); c.removeAttribute('aria-hidden');
      c.className = 'docslide';
      /* tier two travels with it, opened (DS-073) */
      Array.prototype.forEach.call(c.querySelectorAll('.disc-panel'), function(p){
        p.hidden = false;
        var lead = document.createElement('p');
        lead.className = 'disc-lead';
        var src = s.querySelector('.disc-label');
        lead.textContent = src ? src.textContent : 'Detail';
        p.parentNode.insertBefore(lead, p);
      });
      /* the source list travels opened too - same rule, same reason (DS-073) */
      Array.prototype.forEach.call(c.querySelectorAll('.sources-box'), function(b){
        b.hidden = false;
      });
      Array.prototype.forEach.call(c.querySelectorAll('[id]'), function(n){ n.id = 'doc-' + n.id; });
      Array.prototype.forEach.call(c.querySelectorAll('[aria-controls]'), function(n){
        n.setAttribute('aria-controls', 'doc-' + n.getAttribute('aria-controls'));
      });
      Array.prototype.forEach.call(c.querySelectorAll('svg.fig'), function(f){
        var vb = (f.getAttribute('viewBox') || '0 0 1 1').split(/\s+/);
        f.removeAttribute('height');
        f.setAttribute('width','100%');
        f.style.aspectRatio = vb[2] + ' / ' + vb[3];
        f.style.height = 'auto';
      });
      var sec = document.createElement('section');
      sec.setAttribute('aria-label', (i+1) + '. ' + s.dataset.name);
      while (c.firstChild) sec.appendChild(c.firstChild);
      docBody.appendChild(sec);
    });
  }

  /* ------------------------------------------------------------ the printed contents page */
  /* A RENDERING of manifest(), not a second reading of the deck (T-034). The on-screen index
     T-035 builds is the other rendering of the same manifest, and the two legitimately differ:
     this one is bounded by the sheet and is read once to orient, that one scrolls and is read
     repeatedly to jump.

     Built at start-up rather than on `beforeprint`, because the page has to exist for a print
     triggered any way at all - the dialog, the menu, a capture - and twelve boxes of DOM is not
     a cost worth deferring.

     Each box's number and stage name are formatted exactly as the slide's own eyebrow renders
     them (`01 · WHY NOW`), so a reader matching a box to its page finds the identical string,
     and the per-stage icon has a label rather than being a glyph to decode. */
  /* How many columns ONE SHEET uses, and whether it is too dense to carry descriptions. Pure
     arithmetic on an entry count - no DOM, no measurement - so it gives the same answer on screen,
     in print and to the measuring tool.

     Its argument is a SHEET's entry count, not the deck's: since T-036 the caps below keep that at
     16 or under, and since T-125 at 12 or under wherever the page splits. So the four-row band is
     reached only by a deck of 13 to 16 that prints one sheet, and the dense band and the hard limit
     past it are unreachable through the shipped rule. They are kept, not dead: they are what a
     sheet would do if a cap ever moved, and DS-226's numbers would otherwise have no instrument
     left measuring them.

     THREE columns below ten slides, four above. Columns are what decide the row count, and the row
     count is what decides how tall a box gets stretched: seven slides at four columns is two rows
     of 377 du boxes holding 150 du of content, while at three columns it is three rows of 243 -
     the same height as the twelve-slide page, in wider boxes. The owner's rule was "no MORE than
     four", so going narrower is available and this is what it is for. */
  function contentsLayout(n){
    var cols = n <= 9 ? 3 : 4;
    var rows = Math.ceil(n / cols);
    return { cols: cols, rows: rows, dense: rows >= 5 };
  }

  /* ---- WHEN THE PAGE BECOMES SHEETS (T-036)
     16 is the largest number of entries one sheet carries with a description on every box - T-034
     measured it, T-116 re-measured it against a three-line description in every entry and it did
     not move. Past it the page CONTINUES rather than degrading: the alternative was to let the
     layout above compress, which drops the description at 17 and clips the entry itself at 25, and
     DS-226 forbids the second outright. */
  var CONTENTS_CAP = 16;

  /* ---- AND HOW FULL A SHEET GETS ONCE IT DOES (T-125)
     TWO NUMBERS, deliberately: one sheet up to 16, then sheets of at most 12. 16 is where the page
     splits; 12 is the largest sheet that still shows a THREE-LINE description, because 13 crosses
     into the four-row band and that band clamps every description to one line. Printed at 25
     entries the old single number split 12 / 13, put both sheets in the four-row band and printed
     thirteen fragments - `Spend the $5.6M grant on bus...` - while 17 entries, one band down,
     printed full sentences. A longer deck got a better map than a shorter one.

     The owner ruled on 2026-08-13 and accepted the three costs: a second number; a discontinuity at
     17, where a 16-entry deck prints fragments on one sheet and a 17-entry deck prints sentences on
     two; and five sheets rather than three for a 43-entry deck whose argument is one stage of 40.
     The argument that carried it is T-036's own, one band deeper - the description is what makes a
     contents page more than a list of titles, and a page that degrades by growing must not buy a
     sheet back by dropping to fragments.

     The trigger is untouched. A deck at or under 16 still prints the single sheet T-034 measured
     and T-116 fixed; what moves is the capacity of a sheet once the page is already continuing. */
  var SHEET_CAP = 12;

  /* Runs of one stage, in slide order. Back matter has no stage (T-108) and forms its own run, so
     a colophon lands on a sheet boundary rather than in the middle of the last argument stage. */
  function stageRuns(man){
    var runs = [], last;
    man.forEach(function(m){
      var key = m.back ? 'back' : m.stage;
      if (!runs.length || key !== last){ runs.push([]); last = key; }
      runs[runs.length - 1].push(m);
    });
    return runs;
  }

  /* A stage longer than a whole sheet has no boundary inside it, so THE BOUNDARY IS WHAT YIELDS -
     never the entry. DS-226: a box may lose its description, the page may never lose the box. Cut
     into even pieces rather than cap-sized ones, so the overflow is a short piece rather than a
     one-box remainder. */
  function splitLongRuns(runs, cap){
    var out = [];
    runs.forEach(function(r){
      if (r.length <= cap){ out.push(r); return; }
      var parts = Math.ceil(r.length / cap), at = 0;
      for (var p = 0; p < parts; p++){
        var take = Math.ceil((r.length - at) / (parts - p));
        out.push(r.slice(at, at + take));
        at += take;
      }
    });
    return out;
  }

  /* How many sheets a capacity needs, packing runs left to right. Greedy is exact here: the runs
     keep their order, so the first sheet taking as much as it can never costs a later one. */
  function sheetsNeeded(runs, cap){
    var sheets = 1, used = 0;
    for (var i = 0; i < runs.length; i++){
      if (used && used + runs[i].length > cap){ sheets++; used = 0; }
      used += runs[i].length;
    }
    return sheets;
  }

  /* The sheets, as arrays of manifest entries.
     Two objectives in order: the FEWEST sheets, then the SMALLEST largest sheet. The second is
     what stops 17 slides printing twelve boxes and then five - a near-empty sheet is the
     stretched-empty-box fault T-034 already paid to fix at the short end. Binary search the
     capacity down to the tightest one that still fits in the same number of sheets, which is
     exact for that objective and needs no scoring heuristic to defend. */
  function contentsSheets(man){
    if (man.length <= CONTENTS_CAP) return [man];
    var runs = splitLongRuns(stageRuns(man), SHEET_CAP);
    var k = sheetsNeeded(runs, SHEET_CAP);
    var lo = 1, hi = SHEET_CAP;
    runs.forEach(function(r){ if (r.length > lo) lo = r.length; });
    while (lo < hi){
      var mid = Math.floor((lo + hi) / 2);
      if (sheetsNeeded(runs, mid) <= k) hi = mid; else lo = mid + 1;
    }
    var sheets = [], cur = [];
    runs.forEach(function(r){
      if (cur.length && cur.length + r.length > lo){ sheets.push(cur); cur = []; }
      cur = cur.concat(r);
    });
    if (cur.length) sheets.push(cur);
    return sheets;
  }

  /* The two exports, and they exist for a reason: tools/deck/contents_bound.py has to measure the
     rules the deck SHIPS rather than copies of them kept in step by hand (L-08). Nothing in the
     deck reads these back, and they carry no DOM. */
  window.htmldeckContentsLayout = contentsLayout;
  window.htmldeckContentsSheets = contentsSheets;

  /* One <section class="contents"> per sheet, and EVERY SHEET GETS THE SAME GRID - taken from the
     largest, not from its own entry count. Sheets that each sized themselves would print boxes of
     different heights, and two sheets of one page that disagree about box height read as a
     rendering fault rather than as a continuation. */
  function buildContentsSheet(entries, lay, index, total){
    var sec = document.createElement('section');
    sec.className = 'contents';
    sec.setAttribute('aria-label', total > 1
      ? 'Contents, sheet ' + index + ' of ' + total : 'Contents');

    sec.style.setProperty('--ccols', lay.cols);
    sec.style.setProperty('--crows', lay.rows);
    sec.dataset.rows = lay.rows;
    if (lay.dense) sec.dataset.dense = '';

    var head = document.createElement('div');
    head.className = 'contents-head';
    var eyebrow = document.createElement('span');
    eyebrow.className = 'contents-eyebrow';
    /* The marker goes on EVERY sheet including the first, which is the one that needs it: a reader
       holding sheet one has no other way to know the map is not finished. */
    eyebrow.textContent = total > 1 ? 'Contents · ' + index + ' of ' + total : 'Contents';
    var title = document.createElement('h2');
    title.className = 'contents-title';
    title.textContent = DECK;
    head.appendChild(eyebrow);
    head.appendChild(title);
    sec.appendChild(head);

    var grid = document.createElement('div');
    grid.className = 'contents-grid';

    entries.forEach(function(m){
      var box = document.createElement('div');
      box.className = 'cbox';

      var top = document.createElement('div');
      top.className = 'cbox-top';
      var num = document.createElement('span');
      num.className = 'cnum';
      num.textContent = (m.n < 10 ? '0' : '') + m.n;
      var st = document.createElement('span');
      st.className = 'cstage';
      st.textContent = m.stageName;
      top.appendChild(num);
      top.appendChild(st);
      /* No stage, no mark (DS-113/114) - and no EMPTY mark either. Back matter used to reach here
         with `m.icon` undefined and get a `<use href="#undefined">`, which draws nothing and leaves
         a box that looks like a glyph that failed to load rather than one that has none (T-108). */
      if (m.icon){
        var ico = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        ico.setAttribute('class', 'cico');
        ico.setAttribute('aria-hidden', 'true');
        var use = document.createElementNS('http://www.w3.org/2000/svg', 'use');
        use.setAttribute('href', '#' + m.icon);
        ico.appendChild(use);
        top.appendChild(ico);
      }

      var t = document.createElement('h3');
      t.className = 'cbox-title';
      t.textContent = m.title;

      var b = document.createElement('p');
      b.className = 'cbox-bottom';
      b.textContent = m.bottom;

      box.appendChild(top);
      box.appendChild(t);
      box.appendChild(b);
      grid.appendChild(box);
    });
    sec.appendChild(grid);

    /* The one line that reaches the person holding the paper. T-032 put the statement of what
       print does not preserve into the handover text, which is read by whoever is ABOUT to
       print and never by whoever is handed the pages (R7 §5).

       On EVERY sheet, for two reasons that agree. Paper gets separated, so a sheet read alone
       still owes the reader the statement; and the line takes height, so a sheet without it would
       hand its grid more room than the others and print taller boxes - which is the thing the
       shared grid above exists to prevent. */
    var foot = document.createElement('p');
    foot.className = 'contents-foot';
    foot.textContent = 'Detail behind the disclosure panels is on screen only — '
                     + 'it is not on these pages.';
    sec.appendChild(foot);
    return sec;
  }

  function buildContents(){
    var sheets = contentsSheets(manifest());
    var largest = 0;
    sheets.forEach(function(s){ if (s.length > largest) largest = s.length; });
    var lay = contentsLayout(largest);

    var frag = document.createDocumentFragment();
    sheets.forEach(function(s, i){
      frag.appendChild(buildContentsSheet(s, lay, i + 1, sheets.length));
    });

    /* FIRST, and that is load-bearing: `section.slide:last-of-type` matches by element type, so
       a <section> appended after slide 12 would make it match nothing and bring back the empty
       thirteenth page (DS-222's corollary). The sheets go in as one fragment so they stay in
       order ahead of slide 1. */
    stage.insertBefore(frag, stage.firstChild);
  }

  function setView(toDocView){
    if (toDocView === inDoc) return;
    inDoc = toDocView;
    if (inDoc){
      doc.setAttribute('data-on','');
      viewport.hidden = true;
      document.body.style.overflow = 'auto';
      toStage.setAttribute('data-on','');   /* the return control exists only in the reading view */
      /* position is preserved in both directions (DS-076) */
      var target = docBody.children[idx];
      if (target) target.scrollIntoView({block:'start'});
      doc.focus();
    } else {
      /* read the position back out of the reading view before leaving it */
      var best = 0, top = doc.scrollTop;
      Array.prototype.forEach.call(docBody.children, function(sec, n){
        if (sec.offsetTop - 80 <= top) best = n;
      });
      doc.removeAttribute('data-on');
      viewport.hidden = false;
      document.body.style.overflow = 'hidden';
      toStage.removeAttribute('data-on');
      go(best);
      fit();
    }
  }
  toDoc.addEventListener('click', function(){ setView(true); });
  toStage.addEventListener('click', function(){ setView(!inDoc ? true : false); });

  /* Auto-engage when the stage scales below 0.5 - the point where 24-unit body text renders
     under 12 CSS px - and never in fullscreen (DS-071/072).

     Keyed off the scale factor, not viewport width. 960 CSS px is the same threshold only when
     height does not bind: 1280 x 400 scales to 0.37 and puts body text at 8.9 px, and a
     `max-width: 959px` query keeps that on the stage. So the trigger is the number the rule is
     actually about, and it listens for resize - a media query never fires on a height change. */
  function autoView(){
    if (document.fullscreenElement) return;
    var k = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
    if (!isFinite(k) || k <= 0) return;
    if (k < 0.5 && !inDoc) setView(true);
    if (k >= 0.5 && inDoc) setView(false);
  }
  window.addEventListener('resize', autoView);
  window.addEventListener('orientationchange', autoView);

  /* ---------------------------------------------------------- count-up (DS-147) */
  function countUp(el){
    var target = parseInt(el.dataset.count, 10);
    if (root.dataset.motion === 'off' ||
        window.matchMedia('(prefers-reduced-motion: reduce)').matches){ el.textContent = target; return; }
    var t0 = null, dur = 480;
    function step(t){
      if (t0 === null) t0 = t;
      var p = Math.min(1, (t - t0) / dur);
      el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  /* A function declaration, not a var: the ribbon's click handlers are wired during boot, before
     the line that would have assigned it. Runs once, the first time its slide is the current one. */
  var counter = stage.querySelector('[data-count]'), counted = false;
  function countIfSeen(){
    if (!counter || counted || !slides[idx].contains(counter)) return;
    counted = true;
    countUp(counter);
  }

  /* ---------------------------------------------------------- boot */
  window.addEventListener('resize', fit);
  window.addEventListener('orientationchange', fit);
  document.addEventListener('fullscreenchange', fit);
  fit();
  buildRuler();
  buildDoc();
  buildContents();
  /* after fit(), because capacity is measured off the laid-out row rather than derived */
  fitRuler();
  window.addEventListener('resize', fitRuler);
  /* the ring is placed for the first time without a transition, or it flies in from the left */
  rulerEl.setAttribute('data-noanim','');
  go(0);
  requestAnimationFrame(function(){ rulerEl.removeAttribute('data-noanim'); });
  autoView();
  document.addEventListener('keyup', countIfSeen);
  document.getElementById('next').addEventListener('click', countIfSeen);
  document.getElementById('prev').addEventListener('click', countIfSeen);
  /* Boot survived. From here an error is a defect in one slide, not a reason to take the deck
     away from the reader (DS-009). */
  booted = true;
})();
