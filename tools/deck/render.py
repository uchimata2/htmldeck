#!/usr/bin/env python3
"""Render a deck in REAL Chrome, offline, and measure what came out.

**Why not a preview pane.** It reports the stage as zero-size with `transform: none` while the
custom property resolves correctly, and it has given this project a confident wrong answer four
times (**L-06**, **L-15**). So: a clean throwaway profile, every DNS lookup black-holed, and the
numbers read back out of the DOM.

Two things here are not obvious and both cost time to discover (**L-26**):

- **`--window-size` sets the outer window, not the viewport.** The viewport comes back short by a
  constant, so "1280x720" is not 720p unless the shortfall is measured and corrected. `calibrate`
  does that, and asserts the corrected size actually landed.
- **Headless never produces a frame, so an animation's own clock never starts.** Measured
  2026-08-19 (T-185): under this invocation `document.timeline.currentTime` stays at 0, no
  `animationstart` or `animationend` fires, and a 420 ms animation reads `currentTime: 0` after
  900 ms of real timers - on a compositor property and on a main-thread one alike. Adding
  `--disable-gpu` makes the *document* timeline advance (0, 200, 900) and changes nothing about the
  animation, which is the sharp version of the finding: **the clock a CSS animation runs on is
  frame production, not time.** So `motion` **seeks** rather than waits. See its own docstring for
  what that proves and what it does not.
- **An infinite animation stops a headless render from ever settling.** DS-140's `Current` loops
  forever, so the virtual-time budget never reaches a quiescent state and `--screenshot` fires
  mid-transition, producing convincingly blank slides. Captures pin motion off first.

    python tools/deck/render.py measure examples/reference-deck.html
    python tools/deck/render.py shots   examples/reference-deck.html
    python tools/deck/render.py shots   examples/reference-deck.html 0,4,6
    python tools/deck/render.py shots   examples/reference-deck.html --out shots/
    python tools/deck/render.py motion  examples/reference-deck.html
    python tools/deck/render.py motion  examples/reference-deck.html --into 4 --at 0,25,50,75,100
    python tools/deck/render.py motion  examples/reference-deck.html --into 4 --shots
    python tools/deck/render.py motion  examples/reference-deck.html --into 4 --back

Output goes to `<the deck's project>/.assets-cache/deck/`, or to `--out`. **The deck's project, not
this tool's** - installed as a plugin those are different directories, and writing to the second put
an adopter's screenshots and a copy of their deck inside the package cache (T-074).
Pure standard library (**L-07**).
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths                                                        # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# This repository's own working directory, and the default for the development suites, which only
# ever run from a clone. **It is not where a deck's output goes** - `out_dir` decides that from the
# deck, because `ROOT` is the *plugin's* directory once the plugin is installed (T-074).
OUT = os.path.join(ROOT, ".assets-cache", "deck")


def out_dir(deck, override=None):
    """Where this deck's shots, probes and measurements belong, always as an absolute path.

    **`--out` is resolved here and nowhere else**, and that is T-094. Three call sites wrote
    `out = out or out_dir(deck)`, which reads as resolution and is not: the `or` takes the override
    verbatim, and only the *default* ever reached the function where `abspath` lives. A relative
    `--out` then arrived at Chrome as `--screenshot=.assets-cache/...`, which Chrome resolved
    against its own working directory - so the run printed `FAILED` for two shots that were never
    where the tool looked, and named the file rather than the cause. Everything downstream now takes
    its directory from the probe `make_probe` returns, so there is one resolution to keep right.
    """
    if override:
        return os.path.abspath(override)
    return os.path.join(paths.output_root(deck), ".assets-cache", "deck")

BROWSERS = [
    r"%ProgramFiles%\Google\Chrome\Application\chrome.exe",
    r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe",
    r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe",
    r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe",
    r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe",
]


def find_browser():
    for pattern in BROWSERS:
        path = os.path.expandvars(pattern)
        if os.path.exists(path):
            return path
    for name in ("google-chrome", "chromium", "chromium-browser", "microsoft-edge"):
        path = shutil.which(name)
        if path:
            return path
    return None


CHROME = find_browser()

# The resolutions DS-063 and DS-064 name, plus the one used for looking at slides.
RESOLUTIONS = [(3840, 2000, "3840x2000"), (1280, 634, "1280x634"), (1280, 720, "720p")]

# Injected into a COPY of the deck. It drives the deck through its own public controls - never by
# writing internal state, which would measure something the audience never sees.
#
# It advances with the NEXT button rather than by jumping to a per-slide target. T-028 removed the
# twelve dots this used to click (DS-216: three encodings of position where one was wanted), and
# every slide after the first went unmeasured with no error - the gate reported "NO RESULT", not a
# failure. A measurement tool must not depend on a piece of chrome a design rule can delete. Next
# and previous are controls, not position encodings, so they survive a chrome redesign; if they
# ever do not, the assertion below fails loudly instead of silently measuring slide 1 twelve times.
PROBE = r"""
<script>
(function(){
  var P = new URLSearchParams(location.search);
  var want = parseInt(P.get('s') || '0', 10);
  var quiet = P.get('quiet') === '1';
  function local(el, srect, k){
    var r = el.getBoundingClientRect();
    return [ +(((r.left - srect.left)/k).toFixed(2)), +(((r.top - srect.top)/k).toFixed(2)),
             +((r.width/k).toFixed(2)), +((r.height/k).toFixed(2)) ];
  }
  function run(){
    var stage = document.getElementById('stage');
    var next  = document.getElementById('next');
    if (quiet){
      document.documentElement.setAttribute('data-motion','off');
      var s = document.createElement('style');
      /* `*` DOES NOT MATCH PSEUDO-ELEMENTS, so this pinned motion on every element and on none of
         the ::before marks - and the ruler's tick marks are ::before. A capture taken while one of
         them was mid-transition read its animated height and colour instead of its settled ones,
         which is DS-221's failure in the instrument rather than in the deck: it does not look like
         a broken capture, it looks like broken CSS, and it cost a round of chasing specificity
         that was never wrong. Found 2026-08-08 building the ruler's dot variant. */
      s.textContent = '*,*::before,*::after{transition:none!important;animation:none!important}' +
                      '.rise,.pulse,.opening{opacity:1!important;transform:none!important}';
      document.head.appendChild(s);
    }
    if (want > 0){
      if (!next) { document.title = 'PROBE-ERROR no next control'; return; }
      for (var n = 0; n < want; n++) next.click();
    }
    setTimeout(function(){
      var k = parseFloat(getComputedStyle(stage).getPropertyValue('--k')) || 0;
      var srect = stage.getBoundingClientRect();
      var cur = document.querySelector('.slide[data-current]');
      var out = { vw:window.innerWidth, vh:window.innerHeight, k:+k.toFixed(6),
                  stage:[+srect.width.toFixed(2), +srect.height.toFixed(2)],
                  slide: cur ? cur.dataset.name : null,
                  fonts: document.fonts.size + '/' + document.fonts.status,
                  geom:{}, type:{}, overflow:[] };
      var probes = {
        headline:  cur.querySelector('.headline'),
        standfirst:cur.querySelector('.standfirst'),
        /* the deliverable, on every slide since T-028. Probed by name because DS-203 is a claim
           about RANK - it has to be comparable against the headline and the body, not just present. */
        bottomLine:cur.querySelector('.bottom-line b'),
        /* **By contract, not by the reference deck's composition.** This read
           `.standfirst, .cost-p, .title-note` until T-075, and two of those three are class names
           belonging to one deck - `COMPONENT-CONTRACT.md` names neither. A conforming deck whose
           prose is classed anything else reported `no body run measured` and FAILED DS-064 for a
           rule it satisfies, with no remedy but to adopt a class name no document states. That
           inverts the contract: the selector becomes the specification. `.standfirst` is
           contracted at 0-1 per slide and `.body` at 1, so the run is the standfirst where the
           slide has one and the first paragraph of the body where it does not. */
        body:      cur.querySelector('.standfirst') || cur.querySelector('.body p'),
        eyebrow:   cur.querySelector('.eyebrow'),
        discLabel: cur.querySelector('.disc-label'),
        monoLab:   cur.querySelector('.mono, .lab, .col-c'),
        svgLab:    cur.querySelector('svg .lab'),
        svgVal:    cur.querySelector('svg .val'),
        svgName:   cur.querySelector('svg .name'),
        /* NON-TEXT boxes. Everything above is a text run, and until 2026-08-07 that was the
           whole probe - so DS-063's *non-text* tolerance had a stated number and no coverage
           at all. A rect that is laid out rather than glyph-derived is the only thing that can
           test it (DS-191: a measurement cannot find a defect nobody thought to measure). */
        figBox:    cur.querySelector('svg.fig'),
        discBox:   cur.querySelector('.disc'),
        btnBox:    cur.querySelector('.disc-btn'),
        rowBox:    cur.querySelector('.ledger-row, .col-a, .card, .stat-right')
      };
      for (var key in probes){
        var el = probes[key];
        if (!el) continue;
        var fs = parseFloat(getComputedStyle(el).fontSize);
        if (el.namespaceURI === 'http://www.w3.org/2000/svg'){
          var m = el.getScreenCTM();
          var sc = m ? Math.sqrt(Math.abs(m.a*m.d - m.b*m.c)) : k;
          out.type[key] = { du:+(fs*(sc/k)).toFixed(2), css:+(fs*sc).toFixed(2) };
        } else {
          out.type[key] = { du:+fs.toFixed(2), css:+(fs*k).toFixed(2) };
        }
        out.geom[key] = local(el, srect, k);
      }
      // Content taller than its grid track never shows up as a box overflowing the stage - the
      // track clamps the box and the content spills silently. Measure the content (L-26).
      var bodyEl = cur.querySelector('.body');
      if (bodyEl){
        var spill = bodyEl.scrollHeight - bodyEl.clientHeight;
        if (spill > 2) out.overflow.push('body content spills ' + Math.round(spill/k) + ' du');
      }
      var watch = cur.querySelectorAll('.headline,.standfirst,.body,.disc,.provenance,.eyebrow,svg.fig');
      for (var i=0;i<watch.length;i++){
        var g = local(watch[i], srect, k);
        if (g[0] < -1 || g[1] < -1 || g[0]+g[2] > 1921 || g[1]+g[3] > 1081)
          out.overflow.push('element outside the stage: ' + JSON.stringify(g));
      }
      var db = cur.querySelector('.disc-btn');
      if (db){ var dr = db.getBoundingClientRect();
               out.discHitCssPx = [+dr.width.toFixed(2), +dr.height.toFixed(2)]; }
      if (!quiet) document.title = 'RESULT' + JSON.stringify(out) + 'ENDRESULT';
      document.documentElement.setAttribute('data-probe-done','');
    }, 700);
  }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function(){ setTimeout(run,120); });
  else window.addEventListener('load', run);
})();
</script>
"""


def make_probe(deck, name="probe.html", extra="", out=None):
    html = open(deck, "r", encoding="utf-8").read()
    if "</body>" not in html:
        sys.exit("%s has no </body> - not a deck" % deck)
    html = html.replace("</body>", (PROBE if not extra else extra) + "\n</body>")
    # The probe is a **whole copy of the deck**. Writing it under the tool put an adopter's
    # content inside the installed package; it goes with the deck now (T-074).
    out = out_dir(deck, out)
    os.makedirs(out, exist_ok=True)
    dest = os.path.join(out, name)
    with open(dest, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html)
    return dest


def chrome_run(url, w, h, extra=None, timeout=120):
    profile = tempfile.mkdtemp(prefix="htmldeck-")
    args = [CHROME, "--headless=new", "--no-first-run", "--no-default-browser-check",
            "--disable-extensions", "--user-data-dir=" + profile,
            "--host-resolver-rules=MAP * ~NOTFOUND",     # offline, for real
            "--force-device-scale-factor=1", "--hide-scrollbars",
            "--window-size=%d,%d" % (w, h), "--virtual-time-budget=4000"]
    args += (extra or []) + [url]
    try:
        r = subprocess.run(args, capture_output=True, timeout=timeout)
        return r.stdout.decode("utf-8", "replace"), r.stderr.decode("utf-8", "replace")
    finally:
        shutil.rmtree(profile, ignore_errors=True)


def read_result(url, w, h, extra=None):
    out, err = chrome_run(url, w, h, ["--dump-dom"] + (extra or []))
    m = re.search(r"RESULT(\{.*?\})ENDRESULT", out, re.S)
    if not m:
        return None, err
    return json.loads(m.group(1).replace("&quot;", '"').replace("&amp;", "&")), err


def file_url(path):
    return "file:///" + os.path.abspath(path).replace("\\", "/")


def calibrate(probe, w, h):
    """--window-size is the OUTER window; the viewport comes back short by a constant. Measure
    the shortfall once, correct it, and confirm the corrected size actually landed."""
    url = file_url(probe) + "?s=0"
    first, err = read_result(url, w, h)
    if not first:
        sys.exit("calibration failed at %dx%d\n%s" % (w, h, err[:400]))
    dw, dh = w - first["vw"], h - first["vh"]
    if (dw, dh) == (0, 0):
        return w, h
    w2, h2 = w + dw, h + dh
    second, _ = read_result(url, w2, h2)
    got = (second["vw"], second["vh"]) if second else (None, None)
    if got != (w, h):
        print("  ! calibration for %dx%d landed on %sx%s" % (w, h, got[0], got[1]))
    return w2, h2


# ---------------------------------------------------------------------------- commands

def measure(deck, which, quiet=False, out=None):
    """Collect the per-slide geometry at every resolution. `quiet` suppresses the per-row log so
    a gate can call this without burying its own verdicts."""
    # The directory comes back off the probe rather than being resolved a second time (T-094).
    probe = make_probe(deck, out=out)
    out = os.path.dirname(probe)
    results = {}
    for (w, h, label) in RESOLUTIONS:
        cw, ch = calibrate(probe, w, h)
        results[label] = []
        for s in which:
            data, err = read_result(file_url(probe) + "?s=%d" % s, cw, ch)
            if not data:
                print("  !! no result for %s slide %d" % (label, s))
                continue
            results[label].append(data)
            if not quiet:
                print("  %-10s slide %2d  vp=%dx%d k=%.4f stage=%sx%s body=%.1fpx hit=%s %s"
                      % (label, s, data["vw"], data["vh"], data["k"],
                         data["stage"][0], data["stage"][1],
                         data["type"].get("body", {}).get("css", -1),
                         data.get("discHitCssPx"), data["fonts"]))
            for o in data["overflow"]:
                print("     OVERFLOW: %s" % o)
    with open(os.path.join(out, "measurements.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1)
    return results


def cmd_measure(deck, which, out=None):
    results = measure(deck, which, out=out)
    report(results)
    return results


def report(results):
    """DS-063: identical up to a uniform scale factor. DS-064: body >= 16px in a 720p capture.

    **The thresholds are not here.** They live in `contract.py`, which is what gates on them, and
    this prints the same verdict rather than a second opinion (L-08). Imported at call time
    because `contract` imports this module.
    """
    import contract                                                  # noqa: E402

    g = contract.geometry(results)
    if g:
        print("\nDS-063  %d geometry values across 3840x2000 and 1280x634" % g["counted"])
        print("        worst non-text disagreement %.2f du  (%s)  tolerance %.2f - %s"
              % (g["geom"][0], g["geom"][1], contract.GEOM_TOLERANCE_DU,
                 "within" if g["geom_ok"] else "OVER"))
        print("        worst text-run disagreement %.2f du = %.2f device px  (%s)  "
              "tolerance %.1f px = %.2f du - %s"
              % (g["text"][0], g["text_px"], g["text"][1], contract.TEXT_TOLERANCE_PX,
                 g["text_tol_du"], "within" if g["text_ok"] else "OVER"))
        print("        k ratio %.4f" % g["k_ratio"])

    b = contract.body_floor(results)
    if b:
        print("\nDS-064  smallest body run in a 720p capture: %.1f px (%.0f du) on %r  (%d sampled)"
              % (b["css"], b["du"], b["slide"], b["n"]))
        print("        floor is %.0f px - %s"
              % (contract.BODY_FLOOR_CSS_PX, "clears it" if b["ok"] else "FAILS"))

    spills = [(lbl, r["slide"], o) for lbl, rows in results.items()
              for r in rows for o in r["overflow"]]
    print("\noverflow findings: %d" % len(spills))
    for lbl, slide, o in spills[:10]:
        print("  %-10s %-34s %s" % (lbl, slide[:34], o))


def cmd_shots(deck, which, out=None, w=1920, h=1234):
    """Uncalibrated on purpose: --screenshot captures the WINDOW, so asking for a window a little
    larger than the stage puts the whole stage inside the PNG instead of clipping its edge."""
    probe = make_probe(deck, out=out)
    out = os.path.dirname(probe)
    for s in which:
        dest = os.path.join(out, "slide-%02d.png" % (s + 1))
        chrome_run(file_url(probe) + "?s=%d&quiet=1" % s, w, h, ["--screenshot=" + dest])
        # `isfile` and a size, not `exists`: a DIRECTORY at the destination satisfies `exists` and
        # reported as a successful `0 KB` shot, and an empty file is not a picture either.
        if os.path.isfile(dest) and os.path.getsize(dest):
            print("  %s  %.0f KB" % (os.path.basename(dest), os.path.getsize(dest) / 1024))
        else:
            # The path, not just the verdict. A bare FAILED sent T-094 looking at the deck for a
            # defect that was in the argument handling, and a shot missing from a path the tool
            # chose is a different problem from a shot Chrome could not take.
            print("  %s  FAILED - no image at %s" % (os.path.basename(dest), dest))
    print("\n%s" % out)


# **The opposite of `PROBE`'s `quiet` half, and a separate probe rather than a flag on that one.**
# `quiet` exists to pin motion OFF so a capture measures a settled page (DS-221); weakening it with
# a flag would put the guarantee and its exception in one place, where the next edit reaches both.
# T-185's scope says the exception gets its own name, and this is it.
MOTION_PROBE = r"""
<script>
(function(){
  var P = new URLSearchParams(location.search);
  var into = parseInt(P.get('into') || '1', 10);
  var back = P.get('back') === '1';
  /* **A capture is one moment on one clock, and that is the whole difference between a frame and
     a picture of nothing.** This page's animations are staggered - `rise` at delays 0, 60, 120,
     180, 240 - and run for 340, 420, 1200 and 4500 ms. Seeking each to the same FRACTION of its
     own duration composites five moments that never co-occur, and the result looks exactly like a
     frame, which is **L-110**'s failure with a new face. So the capture takes an absolute
     millisecond `t` and puts each animation at `t - delay`, clamped to its own duration - which is
     where it would be if the page had been photographed at `t`. */
  var seek = P.get('seekms');
  var offs = (P.get('at') || '0,25,50,75,100').split(',');
  function css(el){
    var c = getComputedStyle(el);
    return {transform: c.transform, opacity: c.opacity, filter: c.filter,
            visibility: c.visibility, boxShadow: c.boxShadow.slice(0, 60)};
  }
  function who(el){
    var name = el.tagName.toLowerCase();
    if (el.id) { name += '#' + el.id; }
    var cls = el.getAttribute('class');
    if (cls) { name += '.' + cls.trim().split(/\s+/).slice(0, 3).join('.'); }
    var sl = el.closest ? el.closest('.slide') : null;
    return {sel: name, slide: sl ? (sl.dataset.name || '') : ''};
  }
  function run(){
    var next = document.getElementById('next');
    if (!next) { document.title = 'PROBE-ERROR no next control'; return; }
    /* **What was already running is not part of this navigation, and telling them apart is the
       whole of whether a capture is a frame.** The slide being left finished its own entrance
       animations long ago; they carry `fill: both`, so they are still in `getAnimations()` and a
       seek to t=0 rewinds them to their invisible start - which produced a capture of a page in a
       state that never exists (**L-110**: the instrument, not the deck). Nothing in a frozen
       headless clock distinguishes them, because every animation reads `currentTime: 0`. So take
       the set BEFORE the click: what is new belongs to the navigation and rides its clock; what
       was there is finished and is put at its end. */
    /* **The backward transition is a different keyframe and needs a different arrival.**
       DS-235 names `--slide-leave-fwd` and `--slide-leave-back`, and direction follows the
       navigation rather than the slide numbers - so the only way to reach the second one is to
       arrive at the slide by going back to it. Advance one further, then take Previous, and the
       set-difference below picks up the leave-back exactly as it picks up the leave-fwd. */
    var prev = document.getElementById('prev');
    if (back) {
      if (!prev) { document.title = 'PROBE-ERROR no prev control'; return; }
      for (var m = 0; m <= into; m++) { next.click(); }
    }
    var before = new Set(document.getAnimations());
    /* Drive the deck through its own control, exactly as `PROBE` does and for the same reason:
       writing internal state would measure a transition the audience never triggers. */
    if (back) { prev.click(); }
    else { for (var n = 0; n < into; n++) { next.click(); } }
    var settled = 0;
    document.getAnimations().forEach(function(a){
      if (before.has(a)) { try { a.finish(); } catch (e) { a.pause(); } settled++; }
    });
    var anims = document.getAnimations().filter(function(a){
      return a.effect && a.effect.target && !before.has(a);
    });
    /* **Which slides this navigation involves.** The current one, and the one being left - the
       latter identified by carrying the leave animation rather than by index, so a deck whose
       transition is named differently still resolves. Everything outside a slide is chrome and
       counts: the ruler moves as part of the same navigation. */
    var cur = document.querySelector('.slide[data-current]');
    var leaving = null;
    anims.forEach(function(a){
      var n = a.animationName || '';
      if (n.indexOf('slide-leave') === 0 && a.effect.target.classList &&
          a.effect.target.classList.contains('slide')) {
        leaving = a.effect.target;
      }
    });
    var out = {into: into, count: anims.length, settled: settled, anims: []};
    anims.forEach(function(a){
      var el = a.effect.target, tm = a.effect.getTiming();
      var dur = (typeof tm.duration === 'number') ? tm.duration : 0;
      var sl = el.closest ? el.closest('.slide') : null;
      var row = {name: a.animationName || (a.effect.getKeyframes ? '(effect)' : ''),
                 target: who(el), duration: dur, easing: tm.easing, fill: tm.fill,
                 delay: tm.delay, iterations: tm.iterations,
                 /* finite, and on a slide this navigation is moving between, or on the chrome */
                 inNav: (tm.iterations === 1) && (!sl || sl === cur || sl === leaving),
                 stateBefore: a.playState, at: []};
      a.pause();
      var want;
      if (seek !== null && seek !== undefined) {
        var at = parseFloat(seek) - (tm.delay || 0);
        want = [Math.max(0, Math.min(dur, at))];
      } else {
        /* The report is per animation and stays a fraction of each one's own duration: it
           describes one animation's lifecycle, where a fraction is the right unit. */
        want = offs.map(function(p){ return dur * (parseFloat(p) / 100); });
      }
      want.forEach(function(ms){
        a.currentTime = ms;
        row.at.push({ms: Math.round(ms * 100) / 100, read: a.currentTime,
                     state: a.playState, css: css(el)});
      });
      out.anims.push(row);
    });
    if (seek === null || seek === undefined) {
      var el = document.createElement('div');
      el.textContent = 'RESULT' + JSON.stringify(out) + 'ENDRESULT';
      document.body.appendChild(el);
    }
  }
  if (document.readyState === 'complete') { setTimeout(run, 60); }
  else { window.addEventListener('load', function(){ setTimeout(run, 60); }); }
})();
</script>
"""


def motion_span(anims):
    """How long the navigation's clock runs, in ms - `delay + duration`, over the animations it
    started. Returns `None` when none of them belongs to it.

    **Pure, so the fixtures can reach it without a browser** (**L-07**), and it is worth reaching:
    a span taken over the wrong set is a capture of five settled pages that looks exactly like a
    capture of a transition.
    """
    innav = [a for a in anims if a.get("inNav")]
    if not innav:
        return None
    return max(a["delay"] + a["duration"] for a in innav)


def cmd_motion(deck, into=1, at=None, shots=False, back=False, out=None, w=1920, h=1234):
    """Report what the animations a navigation produces are, and what they look like part way.

    **This seeks; it does not watch.** Headless Chrome produces no frames, so no animation's own
    clock ever starts - measured 2026-08-19 across four invocations, on a compositor property and a
    main-thread one alike (T-185, and the module docstring above carries the numbers). What the Web
    Animations API still offers is a **settable `currentTime`**, and the computed style follows it
    exactly: a 420 ms linear fade reads opacity 0, 0.25, 0.5, 0.75, 1 at the five offsets, and an
    eased width reads its own curve rather than a straight line.

    **So be exact about what a green run here means.** It proves the animation exists on the
    element the CSS names, with the duration, easing, fill and iteration count the CSS intends, and
    that every intermediate state interpolates to what the keyframes say - which is what
    `CLAUDE.md` rule 6 needs to look at a transition, and it is more than anything here could
    answer before. It does **not** prove the animation plays: frame rate, dropped frames and
    compositor behaviour are all downstream of frame production, and this instrument has none.
    A frame-rate figure is T-057's and needs a real browser.
    """
    at = at or [0, 25, 50, 75, 100]
    probe = make_probe(deck, name="motion.html", extra=MOTION_PROBE, out=out)
    where = os.path.dirname(probe)
    url = (file_url(probe) + "?into=%d&at=%s%s"
           % (into, ",".join(str(x) for x in at), "&back=1" if back else ""))
    data, err = read_result(url, w, h)
    if not data:
        print("no result - the navigation produced nothing to read\n%s" % err[:300])
        return 1
    print("%s slide %d by the deck's own %s control - %d animation(s) this navigation "
          "started, %d already-finished one(s) put at their end"
          % ("back into" if back else "into", data["into"] + 1,
             "Previous" if back else "Next", data["count"], data.get("settled", 0)))
    if not data["count"]:
        print("\nNothing is animating. Either the transition is `immediate` for this deck, or the "
              "navigation did not happen - and those are different, so check which.")
        return 1
    for a in data["anims"]:
        print("\n  %s on %s%s" % (a["name"] or "(unnamed effect)", a["target"]["sel"],
                                  ("  [slide %s]" % a["target"]["slide"]) if a["target"]["slide"] else ""))
        print("    %s ms, %s, fill %s, delay %s, iterations %s"
              % (a["duration"], a["easing"], a["fill"], a["delay"], a["iterations"]))
        print("    %8s %8s %-10s %-9s %s" % ("seek", "read", "state", "opacity", "transform"))
        for s in a["at"]:
            print("    %8s %8s %-10s %-9s %s"
                  % (s["ms"], s["read"], s["state"], s["css"]["opacity"],
                     s["css"]["transform"][:44]))
        moved = len(set(json.dumps(s["css"]) for s in a["at"])) > 1
        print("    the computed style %s across the offsets"
              % ("MOVES" if moved else "DOES NOT MOVE - the seek reached nothing"))
    if shots:
        # **One clock, and its span is stated rather than assumed.** The span runs to the last
        # moment anything this navigation started is still moving - `delay + duration`, over the
        # finite animations on the two slides involved and on the chrome. An animation looping on
        # a slide nobody is looking at (DS-140's `Current`, 4500 ms) would otherwise stretch every
        # offset past the end of the transition and photograph five settled pages.
        span = motion_span(data["anims"])
        if span is None:
            print("\nNo finite animation belongs to this navigation, so there is no clock to "
                  "sample. Nothing captured.")
            return 1
        innav = [a for a in data["anims"] if a.get("inNav")]
        print("\nclock: 0 to %g ms - the last moment anything this navigation started is still "
              "moving, over %d of %d animation(s)" % (span, len(innav), len(data["anims"])))
        for pct in at:
            ms = span * (float(pct) / 100)
            dest = os.path.join(where, "motion-%s%03d.png" % ("back-" if back else "", int(pct)))
            chrome_run(file_url(probe) + "?into=%d&seekms=%s%s"
                       % (into, ms, "&back=1" if back else ""), w, h,
                       ["--screenshot=" + dest])
            if os.path.isfile(dest) and os.path.getsize(dest):
                print("  %s  %.0f KB  the page at %.0f ms"
                      % (os.path.basename(dest), os.path.getsize(dest) / 1024, ms))
            else:
                print("  %s  FAILED - no image at %s" % (os.path.basename(dest), dest))
        print("\n%s" % where)
    return 0


SECTION_CLASS = re.compile(r'<section[^>]*\sclass="([^"]*)"', re.I)


def slide_count(deck):
    """How many slides the deck has, read from the file rather than assumed.

    Counts `<section>` whose class list holds `slide`, which is what `.slide` selects and what the
    stage iterates. A deck this cannot read is a deck this tool should not silently render a guess
    at, so zero is fatal rather than empty.

    **Matched as a class TOKEN, not as a prefix** (T-120). This is the file-side half of a number
    whose other half is counted in the DOM by `audit.py` and handed to `printpages.verdicts` by
    `check.py`, so the two have to mean the same thing: `class="close slide"` is a slide and the old
    prefix match missed it, while `class="slide-note"` is not one and the old match took it. Splitting
    the attribute is what `.slide` does, so it cannot disagree by construction.
    """
    html = open(deck, "r", encoding="utf-8").read()
    n = sum(1 for m in SECTION_CLASS.finditer(html) if "slide" in m.group(1).split())
    if not n:
        sys.exit("no `<section class=\"slide\">` found in %s - refusing to guess a slide count"
                 % paths.display_path(deck, ROOT))
    return n


def self_test():
    """Refuse to measure if the harness itself is broken (L-04)."""
    if not CHROME:
        sys.exit("no Chrome or Edge found - this harness measures in a real browser on purpose")
    probe_marker = "data-probe-done"
    if probe_marker not in PROBE:
        sys.exit("SELF-TEST FAILED: the probe no longer signals completion")
    if "--host-resolver-rules=MAP * ~NOTFOUND" not in " ".join(
            ["--host-resolver-rules=MAP * ~NOTFOUND"]):
        sys.exit("SELF-TEST FAILED: offline flag missing")
    u = file_url(os.path.join("a", "b.html"))
    if not u.startswith("file:///") or "\\" in u:
        sys.exit("SELF-TEST FAILED: file_url built a path Chrome will not open: %s" % u)

    # T-094, and the fixture is deliberately over the RELATIVE case: every path this tool was ever
    # tested with was absolute, which is why a bug in the one branch that is not survived a task
    # about the same flag. `make_probe` is the only thing that resolves a directory now, so proving
    # what it returns proves what `shots` and `measure` write into - no browser needed.
    if not os.path.isabs(out_dir("deck.html", os.path.join("rel", "ative"))):
        sys.exit("SELF-TEST FAILED: a relative --out came back relative; Chrome would resolve it "
                 "against its own working directory and the shots would land nowhere the caller "
                 "looks")
    fixture = tempfile.mkdtemp(prefix="htmldeck-selftest-")
    try:
        deck = os.path.join(fixture, "d.html")
        with open(deck, "w", encoding="utf-8") as fh:
            fh.write("<html><body><section class=\"slide\"></section></body></html>")
        here = os.getcwd()
        os.chdir(fixture)
        try:
            probe = make_probe(deck, out=os.path.join("out", "shots"))
        finally:
            os.chdir(here)
        if not os.path.isabs(probe) or not os.path.exists(probe):
            sys.exit("SELF-TEST FAILED: make_probe with a relative --out returned %r, which is "
                     "what every caller joins its output paths onto" % probe)
    finally:
        shutil.rmtree(fixture, ignore_errors=True)

    # `slide_count` has to mean what `.slide` means, because `printpages` compares its answer with
    # a DOM count taken by `audit.py` through `check.py` (T-120). Both the cases the old prefix
    # match got wrong are here, and so is one it got right, or the fixture only proves the change.
    counted = _count_classes(['<section class="slide">',
                              '<section class="slide close">',
                              '<section class="close slide">',
                              '<section id="x" class="slide">',
                              '<section class="slide-note">',
                              '<section class="contents">'])
    if counted != 4:
        sys.exit("SELF-TEST FAILED: slide_count read %d slides out of a fixture holding 4 - it no "
                 "longer matches `slide` as a class token, so it and the DOM count disagree" % counted)
    # ---- `motion`'s clock (T-185) ------------------------------------------------------------
    # **The span is taken over the navigation's own animations and nothing else.** A deck carries
    # DS-140's `Current` looping at 4500 ms on a slide nobody is looking at; letting it into the
    # span puts every requested offset past the end of a 420 ms transition, and five captures of a
    # settled page look exactly like five captures of a transition that does not move.
    fixture = [
        {"delay": 0, "duration": 420, "inNav": True},      # the slide transition
        {"delay": 240, "duration": 340, "inNav": True},     # the last staggered rise
        {"delay": 0, "duration": 4500, "inNav": False},     # `Current`, looping, another slide
    ]
    if motion_span(fixture) != 580:
        sys.exit("SELF-TEST FAILED: the motion clock ran to %s ms, not 580. It is `delay + "
                 "duration` over the navigation's own animations - a looping one on a slide "
                 "nobody is looking at must not stretch it" % motion_span(fixture))
    if motion_span([{"delay": 0, "duration": 4500, "inNav": False}]) is not None:
        sys.exit("SELF-TEST FAILED: a navigation that started nothing returned a clock. There is "
                 "no moment to sample, and a span invented here is a capture of nothing")
    if "before" not in MOTION_PROBE or "getAnimations" not in MOTION_PROBE:
        sys.exit("SELF-TEST FAILED: the motion probe no longer takes the animation set BEFORE the "
                 "click. Without it, animations that finished long ago are rewound to their start "
                 "and the capture is of a page that never exists")
    if "animation:none" in MOTION_PROBE:
        sys.exit("SELF-TEST FAILED: the motion probe pins motion off. It is the one path that must "
                 "not - DS-221's default lives in PROBE and this is its named exception")
    return True


def _count_classes(sections):
    """`slide_count`'s matching, over fixture markup rather than a file."""
    return sum(1 for m in SECTION_CLASS.finditer("".join(sections))
               if "slide" in m.group(1).split())


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    self_test()
    cmd, deck = argv[0], os.path.abspath(argv[1])
    if not os.path.exists(deck):
        sys.exit("no such deck: %s" % deck)

    # **`--out` is pulled out before the slide list is read, and that is the whole of T-074's first
    # half.** `build.md` documented this flag from the day the per-batch loop was written; nothing
    # implemented it, and the third argument was parsed as a comma-separated slide list, so a build
    # following the documented command hit `ValueError: invalid literal for int() with base 10:
    # '--out'` at exactly the step that closes the *visual* gate. Reported from a real project on
    # 2026-08-10, which found seven geometry defects by working around it.
    rest, out = list(argv[2:]), None

    # **`motion` takes its own options and is parsed before the shared ones**, because the shared
    # path below rejects every unknown flag by design - which is what stops a documented flag going
    # unimplemented for a second time (T-074, and the note under `--out`).
    if cmd == "motion":
        into, at, shots = 1, [0, 25, 50, 75, 100], False
        if "--into" in rest:
            i = rest.index("--into")
            if i + 1 >= len(rest):
                sys.exit("--into needs a slide number")
            into = int(rest[i + 1])
            del rest[i:i + 2]
        if "--at" in rest:
            i = rest.index("--at")
            if i + 1 >= len(rest):
                sys.exit("--at needs a comma-separated list of percentages")
            at = [float(x) for x in rest[i + 1].split(",")]
            del rest[i:i + 2]
        if "--shots" in rest:
            shots = True
            rest.remove("--shots")
        back = "--back" in rest
        if back:
            rest.remove("--back")
        if "--out" in rest:
            i = rest.index("--out")
            if i + 1 >= len(rest):
                sys.exit("--out needs a directory")
            out = rest[i + 1]
            del rest[i:i + 2]
        if rest:
            sys.exit("unknown option %r - `motion` takes [--into N] [--at a,b,c] [--back] "
                     "[--shots] [--out <dir>]" % rest[0])
        print("browser: %s" % CHROME)
        print("deck:    %s\n" % paths.display_path(deck, ROOT))
        return cmd_motion(deck, into=into, at=at, shots=shots, back=back, out=out)

    if "--out" in rest:
        i = rest.index("--out")
        if i + 1 >= len(rest):
            sys.exit("--out needs a directory")
        out = rest[i + 1]
        del rest[i:i + 2]
    for a in rest:
        if a.startswith("-"):
            sys.exit("unknown option %r - this command takes [<slides>] [--out <dir>]" % a)

    # **Derived from the deck, never assumed.** This read `range(12)` until T-044, which is the
    # reference deck's length and not any deck's: the 14-slide seeded fixture rendered 12 shots and
    # said nothing about the two it dropped, so "look at the rendered deck" (CLAUDE.md rule 6) was
    # being satisfied against an artifact two slides short (**L-05**).
    which = [int(x) for x in rest[0].split(",")] if rest else list(range(slide_count(deck)))
    print("browser: %s" % CHROME)
    print("deck:    %s\n" % paths.display_path(deck, ROOT))
    if cmd == "measure":
        cmd_measure(deck, which, out=out)
    elif cmd == "shots":
        cmd_shots(deck, which, out=out)
    else:
        sys.exit("unknown command %r - use measure, shots or motion" % cmd)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
