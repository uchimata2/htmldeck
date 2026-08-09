
(function(){
  "use strict";
  var root = document.documentElement;
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

  function manifest(){
    return slides.map(function(s, i){
      var b = s.querySelector('.bottom-line');
      var st = parseInt(s.dataset.stage, 10);
      if (isNaN(st) || st < 0 || st >= STAGES.length) st = 0;
      return {
        n:         i + 1,
        title:     s.dataset.name || '',
        bottom:    b ? b.textContent.replace(/\s+/g, ' ').trim() : '',
        stage:     st,
        stageName: STAGES[st],
        icon:      STAGE_ICON[st]
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

  /* What the ruler actually has: the row, less the controls, less the gap between them. Measured
     rather than derived, because the controls cost 32% of the row and that was the number T-035's
     paper estimate of "~30 targets" got wrong. */
  function rulerAvailableDu(){
    var kk = parseFloat(getComputedStyle(stage).getPropertyValue('--k')) || 1;
    var chromeEl = document.querySelector('.chrome');
    var ctrlEl = document.querySelector('.controls');
    if (!chromeEl || !ctrlEl || !kk) return 0;
    var cw = chromeEl.getBoundingClientRect().width / kk;
    var ow = ctrlEl.getBoundingClientRect().width / kk;
    var gap = parseFloat(getComputedStyle(chromeEl).gap) / kk || 0;
    return cw - ow - gap;
  }

  var MAN = manifest();

  function buildRuler(){
    MAN.forEach(function(m, i){
      var isSection = firstSlideOfStage(m.stage) === i;
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
  function restoreLabel(){
    rulerLabel.removeAttribute('data-preview');
    var m = MAN[idx];
    rulerLabel.textContent = m ? m.stageName : '';
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
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    panel.hidden = !open;
    if (open) panel.classList.add('opening');
  }

  /* ---------------------------------------------------------- navigation */
  function go(i, opts){
    i = Math.max(0, Math.min(slides.length - 1, i));
    idx = i;
    closeAllDiscs(null);
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
    else if (k === 'Escape')                                      { closeAllDiscs(null); }
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
     this one must fit a single page and is read once to orient, that one scrolls and is read
     repeatedly to jump.

     Built at start-up rather than on `beforeprint`, because the page has to exist for a print
     triggered any way at all - the dialog, the menu, a capture - and twelve boxes of DOM is not
     a cost worth deferring.

     Each box's number and stage name are formatted exactly as the slide's own eyebrow renders
     them (`01 · WHY NOW`), so a reader matching a box to its page finds the identical string,
     and the per-stage icon has a label rather than being a glyph to decode. */
  /* How many columns, and whether the page is too dense to carry descriptions. Pure arithmetic on
     the slide count - no DOM, no measurement - so it gives the same answer on screen, in print and
     to the measuring tool.

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
  /* The one export, and it exists for a reason: tools/deck/contents_bound.py has to measure the
     layout rule the deck SHIPS rather than a copy of it kept in step by hand (L-08). Nothing in
     the deck reads this back, and it carries no DOM. */
  window.htmldeckContentsLayout = contentsLayout;

  function buildContents(){
    var sec = document.createElement('section');
    sec.className = 'contents';
    sec.setAttribute('aria-label', 'Contents');

    var lay = contentsLayout(slides.length);
    sec.style.setProperty('--ccols', lay.cols);
    sec.dataset.rows = lay.rows;
    if (lay.dense) sec.dataset.dense = '';

    var head = document.createElement('div');
    head.className = 'contents-head';
    var eyebrow = document.createElement('span');
    eyebrow.className = 'contents-eyebrow';
    eyebrow.textContent = 'Contents';
    var title = document.createElement('h2');
    title.className = 'contents-title';
    title.textContent = DECK;
    head.appendChild(eyebrow);
    head.appendChild(title);
    sec.appendChild(head);

    var grid = document.createElement('div');
    grid.className = 'contents-grid';

    manifest().forEach(function(m){
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
      var ico = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      ico.setAttribute('class', 'cico');
      ico.setAttribute('aria-hidden', 'true');
      var use = document.createElementNS('http://www.w3.org/2000/svg', 'use');
      use.setAttribute('href', '#' + m.icon);
      ico.appendChild(use);
      top.appendChild(num);
      top.appendChild(st);
      top.appendChild(ico);

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
       print and never by whoever is handed the pages (R7 §5). */
    var foot = document.createElement('p');
    foot.className = 'contents-foot';
    foot.textContent = 'Detail behind the disclosure panels is on screen only — '
                     + 'it is not on these pages.';
    sec.appendChild(foot);

    /* FIRST, and that is load-bearing: `section.slide:last-of-type` matches by element type, so
       a <section> appended after slide 12 would make it match nothing and bring back the empty
       thirteenth page (DS-222's corollary). */
    stage.insertBefore(sec, stage.firstChild);
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
})();
