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
    python tools/deck/render.py shots   examples/reference-deck.html 1,5,7
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
# **The motion pin, in one place, applied to every probe that is not about motion** (T-209).
#
# T-206 put this pin into `PROBE` and proved what it is worth: on a page read at frame zero, 27 of
# 132 elements sat exactly 18.00 design units from where they settle - the entrance animation's full
# travel, to the digit. But `make_probe` composes the page as `extra or PROBE`, so **`extra`
# replaces the shared probe rather than joining it**, and every one of the eight probe sources that
# passes an `extra` lost the pin. The fix belongs here rather than copied into eight files, which is
# T-206's own argument one level up.
#
# **The exception is not a flag a caller passes; it is a declaration the probe carries.** A
# `pin=False` parameter would make this a guarantee any caller can decline, which is not a guarantee
# (**L-128**). A probe whose *subject* is motion declares `MEASURES_MOTION` in its own source and is
# left alone - the same idiom as DS-217's `data-scale` and DS-230's `data-disc`, where the artifact
# states the claim and the tool reads it back.
#
# **There are three such probes and only one of them was obvious**, which is the finding this task
# produced rather than the one it was raised for. `MOTION_PROBE` announces itself (T-185). The other
# two do not: `audit.PROBE` decides DS-140, DS-142 and DS-218 by reading
# `getComputedStyle(el).animationIterationCount` for `infinite`, and `audit.REDUCED_PROBE` asks what
# the *deck* does under `prefers-reduced-motion`. **`animation:none!important` erases exactly the
# property both of them read.** Pinned unconditionally, the seeded-variant suite went from 8 of 8 and
# 2 of 2 caught to 7 of 8 and 1 of 2: a deck that hides its stop control inside a shut menu passed
# DS-218, and a deck that leaves a slide blank under reduced motion passed DS-143 - both because the
# rule had no subject left to fail on. **A pin that silences a rule is worse than a probe that reads
# an unsettled page**, and this is the absent-subject defect this repository has now met eight times
# (**L-57**).
MEASURES_MOTION = "htmldeck:measures-motion"
#
# `*` DOES NOT MATCH PSEUDO-ELEMENTS, so the selector names them: the ruler's tick marks are
# `::before`, and a capture taken while one was mid-transition read its animated height and colour
# instead of its settled ones. Found 2026-08-08 building the ruler's dot variant.
# **The console trap, in `<head>`, ahead of the deck's own script** (T-041, GF-2).
#
# R6 section 8's condition 2 is *no console errors and no unhandled rejections, collected over the
# full load and one pass through every slide*. A listener appended at `</body>` cannot satisfy the
# first half: the deck's own script has already run and thrown by then, and a load-time error is
# exactly the class this condition exists for. So `make_probe` gained a second injection point and
# this is what goes through it.
#
# **Unconditional, on `MOTION_PIN`'s argument and for `MOTION_PIN`'s reason.** Eight probe sources
# pass an `extra`; anything a caller has to remember is a thing eight callers will forget, which is
# how the pin came to be in `PROBE` and nowhere else (**L-57**, T-206, T-209). It differs from the
# pin in the one way that decides whether an exemption is needed: **the pin changes the page and
# this only listens**, so no probe's subject can be erased by it and there is no counterpart to
# `MEASURES_MOTION` here.
#
# The one thing it does change is `console.error`, which it wraps and calls through. A wrapper that
# forwards is not a silenced console, and the alternative - reading Chrome's stderr - cannot say
# which slide an error came from, which is the half of the condition that needs the walk.
#
# `capture: true` on `error` is what catches a **resource** failure. Those do not bubble, and under
# `--host-resolver-rules=MAP * ~NOTFOUND` they are how an external reference announces itself at run
# time. DS-001 decides the same thing from the markup; this sees what the browser actually did.
ERROR_TRAP = r"""
<script>
(function(){
  var E = [];
  window.__htmldeckErr = E;
  function rec(kind, text){
    if (E.length < 50) E.push(kind + ': ' + String(text).slice(0, 300));
  }
  window.addEventListener('error', function(e){
    var t = e && e.target;
    if (t && t !== window && t.tagName) rec('resource', t.tagName + ' ' + (t.src || t.href || ''));
    else rec('error', (e && e.message) || 'error');
  }, true);
  window.addEventListener('unhandledrejection', function(e){
    var r = e && e.reason;
    rec('rejection', (r && (r.message || r)) || 'rejection');
  });
  var ce = console.error;
  console.error = function(){
    rec('console.error', Array.prototype.join.call(arguments, ' '));
    return ce.apply(console, arguments);
  };
})();
</script>
"""


MOTION_PIN = r"""
<script>
(function(){
  document.documentElement.setAttribute('data-motion','off');
  var s = document.createElement('style');
  s.textContent = '*,*::before,*::after{transition:none!important;animation:none!important}' +
                  '.rise,.pulse,.opening{opacity:1!important;transform:none!important}';
  (document.head || document.documentElement).appendChild(s);
})();
</script>
"""


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
    /* **Unconditional, and never behind `quiet` again (T-206).** It sat inside `if (quiet)` until
       2026-08-21, so `shots` measured a settled page and `measure` - the one that produces a
       VERDICT - measured whatever the entrance animation happened to be showing. Measured on the
       portfolio-review deck that day: 27 of 132 readings at EVERY resolution sat exactly 18.00 du
       from settled, which is `--rise-dist` to the digit. Not part-way through the entrance: frame
       zero of it, because under `--virtual-time-budget` a CSS animation's clock is frame
       production rather than time (**L-26**, T-185) and the 700 ms wait below is virtual.
       DS-063 still PASSED, because all three resolutions were frozen equally and agreeing about
       the wrong page reads exactly like agreeing about the right one. The moment one pass
       produced a frame the other did not, the same comparison reported anything from 0 to 18.00
       du of disagreement against a 0.25 du bound - which is the intermittency T-206 was raised
       for, and the five magnitudes recorded there all fall inside that range.
       So the guarantee has no exception in this probe at all; the exception has its own name and
       its own probe, `MOTION_PROBE` below. `quiet` now controls the title and nothing else. */
    /* The pin itself is `MOTION_PIN`, injected by `make_probe` ahead of this script and ahead of
       every other probe body (T-209). It was inline here until then, which is why the eight
       sources that pass an `extra` never had it. */
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


def inject_head(html, snippet):
    """Put `snippet` as early in the document as the markup allows.

    **Earliest, not merely inside `<head>`** - the point of the seam is to sit ahead of the deck's
    own script, and a deck declares that script in `<head>` like everything else. Three fallbacks,
    because the last of them is what `self_test`'s fixture is: a page with no `<head>` at all still
    parses a leading `<script>` into an implied one, so the guarantee survives markup that never
    wrote the tag.
    """
    m = re.search(r"<head\b[^>]*>", html, re.I)
    if m:
        return html[:m.end()] + snippet + html[m.end():]
    m = re.search(r"<html\b[^>]*>", html, re.I)
    if m:
        return html[:m.end()] + snippet + html[m.end():]
    return snippet + html


def make_probe(deck, name="probe.html", extra="", out=None):
    html = open(deck, "r", encoding="utf-8").read()
    if "</body>" not in html:
        sys.exit("%s has no </body> - not a deck" % deck)
    # **Every probe is pinned except the one whose subject is motion** (T-209). The pin goes in
    # ahead of the probe body, so it is a property of `make_probe` rather than of any caller.
    body = PROBE if not extra else extra
    pin = "" if MEASURES_MOTION in body else MOTION_PIN
    html = html.replace("</body>", pin + body + "\n</body>")
    # **And every probe carries the console trap, with no exemption at all** (T-041). It goes in
    # after the pin so the two seams never contend for one anchor, and lands first in the document.
    html = inject_head(html, ERROR_TRAP)
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
                      % (label, s + 1, data["vw"], data["vh"], data["k"],
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


# **The opposite of `PROBE`'s motion pin, and a separate probe rather than a flag on that one.**
# `PROBE` pins motion OFF unconditionally so that everything it reports - a capture (DS-221) and a
# measurement alike - is taken on a settled page; weakening that with a flag would put the
# guarantee and its exception in one place, where the next edit reaches both. T-185's scope says
# the exception gets its own name, and this is it.
#
# **That pin was behind `quiet` until T-206**, which is the same "one place" fault seen from the
# inside: `shots` asked for the guarantee and `measure` did not, so the only consumer that issues a
# verdict was the one measuring an unsettled page. A guarantee a caller can decline is an exception
# without a name.
MOTION_PROBE = r"""
<!-- htmldeck:measures-motion - this probe's declared subject is the animation itself, so
     `make_probe` leaves it unpinned (T-209). -->
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
     millisecond `t` and puts each animation at `t`, clamped to its own `delay + duration` - which
     is where it would be if the page had been photographed at `t`.

     **`currentTime` is that absolute clock already** (T-255). It is measured from the start of the
     delay, not from the start of the active phase, so `t - delay` is an active-phase offset
     written to a property that is not one - and this comment said `t - delay` while stating the
     right goal in the same sentence, which is why the arithmetic below read as correct for as
     long as it did. */
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
      var want, dly = tm.delay || 0;
      if (seek !== null && seek !== undefined) {
        /* **The clock arrives absolute and stays absolute.** `motion_span` runs the capture to
           `delay + duration` over the navigation's own animations, so the moment handed in here
           is already on `currentTime`'s scale. Subtracting the delay from it - which this branch
           did until T-255 - moves every frame a delay too early, and with `fill: both` all five
           photograph the FROM keyframe. */
        want = [Math.max(0, Math.min(dly + dur, parseFloat(seek)))];
      } else {
        /* The report is per animation and stays a fraction of each one's own duration: it
           describes one animation's lifecycle, where a fraction is the right unit. **The delay is
           where that life starts.** `currentTime` is measured from the start of the delay, so a
           bare fraction of duration samples the delay instead of the animation (T-255). */
        want = offs.map(function(p){ return dly + dur * (parseFloat(p) / 100); });
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


def report_seeks(delay, duration, offs):
    """Where the report samples one animation, on `currentTime`'s scale - `delay + duration*p/100`.

    **The same rule the probe applies, stated where it can be seeded** (**L-07**). The seek lives
    in a JavaScript string that only a browser can run, so without this there is nothing to drive
    in the failing direction and the fix would rest on one green run. `cmd_motion` checks the reads
    the browser sent back against this, which is what keeps the two statements from drifting apart.

    **`currentTime` is measured from the start of the delay, not from the start of the active
    phase.** Dropping the `delay` term - which the probe did until T-255 - samples the delay rather
    than the animation, and with `fill: both` every offset then reads the FROM keyframe. On this
    repository's own reference deck that was 12 of 17 animations.
    """
    return [delay + duration * (float(p) / 100) for p in offs]


def animation_set(anims):
    """`{label: how many}` over one read's animations - the thing two reads have to agree on."""
    counts = {}
    for a in anims:
        label = "%s on %s" % (a.get("name") or "(effect)", a["target"]["sel"])
        counts[label] = counts.get(label, 0) + 1
    return counts


def set_disagreement(first, second):
    """`[(label, in the first read, in the second)]` where two reads of one page disagree.

    **One read cannot say what it could not promise** (T-272). A CSS transition is created only
    when the browser recomputes style, and whether a load-time one is still live when the probe
    takes its `before` set is a race with the page rather than a fact about the deck. Measured on
    `examples/reference-deck.html --into 3`: the ruler ring's 200 ms transition appeared in **one
    run of ten**, then **two of twelve**, so the same command reported seventeen animations or
    eighteen with nothing changed.

    **Two hypotheses were tried and the measurement refused both.** Settling the page before the
    snapshot made the ruler ring no more stable and silently added a second `button` transition to
    every report; forcing a style flush after each click looked clean over ten runs and was not
    over twenty. So the tool stops claiming determinism it does not have and reports the
    uncertainty instead, which is the honest half of this task's own acceptance criterion.
    """
    out = []
    for label in sorted(set(first) | set(second)):
        if first.get(label, 0) != second.get(label, 0):
            out.append((label, first.get(label, 0), second.get(label, 0)))
    return out


def motion_verdict(moved, delay, reads):
    """What the report says about one animation - and **whose finding it is**.

    Three answers, not two (record `017` item 3). An animation that interpolates to nothing is a
    finding about the deck. One whose sampled range never left its delay is a finding about this
    tool, and until T-255 both printed the same sentence: *the computed style DOES NOT MOVE*. That
    sentence sent a reviewer to the deck for a fault in the seek, and the delay was printed two
    lines above it.
    """
    if moved:
        return "MOVES"
    if delay and reads and max(reads) <= delay:
        return ("DOES NOT MOVE - but every offset fell inside the %s ms delay, so this is the "
                "seek's reading and not the deck's" % delay)
    return "DOES NOT MOVE - the seek reached nothing"


def capture_seek(delay, duration, at):
    """Where `--shots` photographs one animation, given a moment on the navigation's clock.

    The moment arrives absolute, from `motion_span`, so it is clamped to the animation's own span
    and nothing is subtracted from it (T-255).
    """
    return max(0.0, min(float(delay) + float(duration), float(at)))


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
    # **The page is read twice and the two reads are compared** (T-272). Membership is object
    # identity: an animation already live when `before` was taken counts as the page's, and
    # whether a load-time transition is still live at that moment is a race. A single read cannot
    # see it, so this one asks the same question twice and says where the answers differ. It costs
    # a second Chrome invocation on a tool `check_all.py` classifies as an instrument rather than
    # a gate, which is the right place to spend it.
    again, _again_err = read_result(url, w, h)
    differ = (set_disagreement(animation_set(data["anims"]), animation_set(again["anims"]))
              if again else None)
    if differ is None:
        print("    the second read produced nothing, so this set is UNCONFIRMED")
    elif differ:
        print("    NOT PROMISED - a second read of the same page disagreed on %d animation(s):"
              % len(differ))
        for label, one, two in differ:
            print("      %-46s %d in the first read, %d in the second" % (label[:46], one, two))
        print("      Object identity decides membership, so a transition already live when the "
              "set\n      was taken counts as the page's. Rerun to see which answer you get.")
    else:
        print("    a second read of the same page agreed, animation for animation")
    if not data["count"]:
        print("\nNothing is animating. Either the transition is `immediate` for this deck, or the "
              "navigation did not happen - and those are different, so check which.")
        return 1
    for a in data["anims"]:
        print("\n  %s on %s%s" % (a["name"] or "(unnamed effect)", a["target"]["sel"],
                                  ("  [slide %s]" % a["target"]["slide"]) if a["target"]["slide"] else ""))
        delay, dur = a["delay"], a["duration"]
        # **The window is stated, not left to be inferred from the seek column** - the same reason
        # `motion_span` prints its clock. A reader who cannot see where the sampling started cannot
        # tell a dead animation from one measured in the wrong place (T-255).
        want = report_seeks(delay, dur, at)
        print("    %s ms, %s, fill %s, delay %s, iterations %s, sampled %g-%g ms"
              % (dur, a["easing"], a["fill"], delay, a["iterations"], want[0], want[-1]))
        print("    %8s %8s %-10s %-9s %s" % ("seek", "read", "state", "opacity", "transform"))
        for s in a["at"]:
            print("    %8s %8s %-10s %-9s %s"
                  % (s["ms"], s["read"], s["state"], s["css"]["opacity"],
                     s["css"]["transform"][:44]))
        moved = len(set(json.dumps(s["css"]) for s in a["at"])) > 1
        reads = [s["read"] for s in a["at"] if isinstance(s["read"], (int, float))]
        print("    the computed style %s across the offsets"
              % motion_verdict(moved, delay, reads))
        # **The probe's arithmetic against this module's, on every run.** They are two statements
        # of one rule in two languages, and nothing but a run can tell whether they still agree.
        drift = [(w, s["ms"]) for w, s in zip(want, a["at"]) if abs(w - s["ms"]) > 0.5]
        if drift:
            print("    SEEK DISAGREES with `report_seeks` at %d of %d offset(s) - wanted %s, the "
                  "probe sought %s. The rows above are this tool's reading, not the deck's"
                  % (len(drift), len(want), [round(w, 2) for w, _g in drift],
                     [g for _w, g in drift]))
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
            # **How much of the navigation this frame actually shows.** An animation still inside
            # its delay contributes its FROM keyframe, which photographs as a page that has not
            # started - indistinguishable from a broken one unless the count is said out loud.
            started = sum(1 for a in innav
                          if capture_seek(a["delay"], a["duration"], ms) > a["delay"])
            dest = os.path.join(where, "motion-%s%03d.png" % ("back-" if back else "", int(pct)))
            chrome_run(file_url(probe) + "?into=%d&seekms=%s%s"
                       % (into, ms, "&back=1" if back else ""), w, h,
                       ["--screenshot=" + dest])
            if os.path.isfile(dest) and os.path.getsize(dest):
                print("  %s  %.0f KB  the page at %.0f ms, %d of %d animation(s) past their delay"
                      % (os.path.basename(dest), os.path.getsize(dest) / 1024, ms,
                         started, len(innav)))
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

    # **T-206's guard, and it is structural on purpose.** The fault it watches for is not a wrong
    # number, it is the motion pin going back behind a caller's flag - at which point `measure`
    # silently returns to reading a page mid-entrance and DS-063's verdict stops being a function
    # of the deck's bytes. Nothing about that is visible in a value: the gate stayed GREEN through
    # it for as long as the two resolutions were unsettled by the same amount. So the assertion is
    # on the shape of the probe, which is what actually changed, and it needs no browser - which
    # matters, because a ten-run measurement is minutes of Chrome and would never run here.
    #
    # **T-209 moved what it asserts, because T-206's version asserted the wrong thing.** It read
    # `"data-motion" not in PROBE` - true of the shared probe and true of nothing else, while eight
    # probe sources passed an `extra` that replaced `PROBE` entirely and took no pin with it. A
    # guard on one probe's text cannot see a guarantee that belongs to `make_probe`. So the
    # assertion is now on what `make_probe` writes, which is the thing every caller actually gets.
    if "data-motion" not in MOTION_PIN:
        sys.exit("SELF-TEST FAILED: MOTION_PIN no longer pins motion off, so every measurement "
                 "every probe takes is of whatever the entrance animation was showing (T-206)")
    # Matched as CODE, not as prose: the brace is the difference. The first version of this guard
    # looked for `if (quiet)` and was tripped by the comment above it explaining the fault - a
    # self-test that fails on its own documentation teaches the next reader to delete the
    # documentation.
    if re.search(r"if\s*\(\s*quiet\s*\)\s*\{", PROBE + MOTION_PIN):
        sys.exit("SELF-TEST FAILED: the motion pin is behind `quiet` again - that is the T-206 "
                 "fault exactly, and it fails the gate green rather than red")
    # **The trap's two listeners and its store, asserted as text** (T-041). GF-2 is decided from
    # `window.__htmldeckErr`, and a trap that stopped installing either listener would report an
    # empty array - a clean console is exactly what a broken collector looks like, which is the
    # optimistic-direction failure R6 section 8 raised conditions 3 and 7 for. Structural, and it
    # needs no browser, for the same reason the pin's guard is.
    for _needle, _why in (("__htmldeckErr", "the store GF-2 reads"),
                          ("'error'", "the error listener"),
                          ("'unhandledrejection'", "the rejection listener"),
                          ("console.error", "the console wrapper")):
        if _needle not in ERROR_TRAP:
            sys.exit("SELF-TEST FAILED: ERROR_TRAP no longer installs %s (%s), so GF-2 reports a "
                     "clean console for every deck whatever it logged (T-041)" % (_why, _needle))

    # **And no probe source may carry a copy of it** (T-209). Two did, and a third would have been
    # written the next time somebody needed one - which is how the pin came to be in `PROBE` and
    # nowhere else in the first place. Read off the package directory rather than a list kept here,
    # so a module added tomorrow is covered (**L-57**).
    # T-041 put the console trap through the same sweep rather than writing a second one: both are
    # single-home guarantees `make_probe` owns, and the sweep's whole point is that it is read off
    # the directory rather than off a list somebody has to extend.
    _seams = [("the motion pin", "transition:none!important;animation:none!important", "T-209"),
              ("the console trap", "__htmldeckErr", "T-041")]
    for _what, _marker, _task in _seams:
        _copies = []
        for _name in sorted(os.listdir(os.path.dirname(os.path.abspath(__file__)))):
            if not _name.endswith(".py") or _name == "render.py":
                continue
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), _name),
                      "r", encoding="utf-8") as _fh:
                _text = _fh.read()
            # A module that READS the store is not a module that installs one. `glitchfree.py`
            # names `__htmldeckErr` because reading it is its subject; what is forbidden is a
            # second copy of the installer, which is the assignment rather than the name.
            if _marker in _text and ("window.__htmldeckErr =" in _text
                                     or _marker != "__htmldeckErr"):
                _copies.append(_name)
        if _copies:
            sys.exit("SELF-TEST FAILED: %s carr%s its own copy of %s. There is one and `make_probe` "
                     "injects it; a copy is a second home that goes stale silently (%s)"
                     % (", ".join(_copies), "ies" if len(_copies) == 1 else "y", _what, _task))
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

        # **The pin, proved on the page `make_probe` writes rather than on a constant** (T-209).
        # Three cases, because two of them are the ones that were broken: a probe built with no
        # `extra`, a probe built with a foreign `extra` - the case all eight sources are - and
        # `MOTION_PROBE`, which must NOT be pinned because measuring motion is its subject.
        with open(probe, "r", encoding="utf-8") as _fh:
            _plain = _fh.read()
        if "data-motion" not in _plain:
            sys.exit("SELF-TEST FAILED: make_probe wrote a probe with no motion pin")
        _foreign = make_probe(deck, name="foreign.html", extra="<script>/*caller*/</script>",
                              out=os.path.join(fixture, "out"))
        with open(_foreign, "r", encoding="utf-8") as _fh:
            _ftext = _fh.read()
        if "data-motion" not in _ftext or "/*caller*/" not in _ftext:
            sys.exit("SELF-TEST FAILED: a probe built with a caller's own `extra` lost the motion "
                     "pin - that is the T-209 fault exactly, and it is invisible in every value "
                     "the probe reports")
        _motion = make_probe(deck, name="motion.html", extra=MOTION_PROBE,
                             out=os.path.join(fixture, "out"))
        with open(_motion, "r", encoding="utf-8") as _fh:
            _mtext = _fh.read()
        if "data-motion" in _mtext:
            sys.exit("SELF-TEST FAILED: MOTION_PROBE was pinned. Measuring motion is its "
                     "declared subject; pinning it makes it report a page with none (T-185)")

        # **The trap, proved on the written page and in all three cases** (T-041). The pin has one
        # declared exemption and the trap has none, so `MOTION_PROBE` is here as a case that must
        # carry it rather than as one that must not - the two seams differ exactly here, and a
        # reader who assumes they match would be wrong in the direction that loses the guarantee.
        # The fixture also has no `<head>`, so this is `inject_head`'s last fallback under test.
        for _label, _text in (("no extra", _plain), ("a caller's extra", _ftext),
                              ("MOTION_PROBE", _mtext)):
            if "__htmldeckErr" not in _text:
                sys.exit("SELF-TEST FAILED: the probe built with %s carries no console trap, so "
                         "GF-2 reads an absent store and reports a clean console (T-041)" % _label)
            # Ahead of the deck, not merely present. A trap after the deck's own script cannot see
            # the load-time error that is the whole reason condition 2 needs a `<head>` seam.
            if _text.index("__htmldeckErr") > _text.lower().index("<body"):
                sys.exit("SELF-TEST FAILED: the console trap in the probe built with %s sits after "
                         "<body>, so a load-time throw happens before it listens (T-041)" % _label)
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
    # **Where the report samples, and where the capture does** (T-255). Both seeks were off by the
    # delay: the report never added it, the capture subtracted it from a clock that already had
    # it, and with `fill: both` every offset then read the FROM keyframe. The tool printed *the
    # computed style DOES NOT MOVE* - a sentence about the deck, produced by the seek. On this
    # repository's own `examples/reference-deck.html`, 12 of 17 animations were sampled that way.
    _last_rise = report_seeks(240, 340, [0, 25, 50, 75, 100])
    if _last_rise != [240, 325, 410, 495, 580]:
        sys.exit("SELF-TEST FAILED: the report samples %s, not 240-580. `currentTime` is measured "
                 "from the start of the DELAY, so a bare fraction of duration lands a delay early "
                 "- for the reference stagger's last rise, three of five offsets inside it"
                 % (_last_rise,))
    if min(_last_rise) < 240 or max(_last_rise) != 580:
        sys.exit("SELF-TEST FAILED: the sampled window is not the animation's own life. It starts "
                 "at the delay and ends at delay + duration; %s does neither" % (_last_rise,))
    # The failing direction (**L-125**): the arithmetic this fix replaced, stated so the guard can
    # be seen to fail rather than merely to exist.
    _before = [340 * (p / 100.0) for p in [0, 25, 50, 75, 100]]
    if sum(1 for s in _before if s < 240) != 3:
        sys.exit("SELF-TEST FAILED: the fixture no longer reproduces the defect, so the assertion "
                 "above proves nothing about it")
    if capture_seek(600, 300, 675) != 675:
        sys.exit("SELF-TEST FAILED: the capture moved a moment that arrived on the navigation's "
                 "own clock. `motion_span` runs it to delay + duration, so subtracting the delay "
                 "here puts every frame a delay too early - 675 ms became %s"
                 % capture_seek(600, 300, 675))
    if capture_seek(600, 300, 1200) != 900 or capture_seek(600, 300, -5) != 0:
        sys.exit("SELF-TEST FAILED: the capture no longer clamps to the animation's own span")
    # **Two reads of one page, compared** (T-272). The comparison is what the tool says instead of
    # a promise it cannot keep, so it has to be right about agreement and disagreement alike - a
    # comparator that never disagrees is the same silence in a new place.
    _one = animation_set([{"name": "rise", "target": {"sel": "p.a"}},
                          {"name": "rise", "target": {"sel": "p.a"}},
                          {"name": None, "target": {"sel": "i#rulerRing"}}])
    if _one != {"rise on p.a": 2, "(effect) on i#rulerRing": 1}:
        sys.exit("SELF-TEST FAILED: the animation set lost a duplicate or misnamed a transition: "
                 "%r. Two rises on one selector are two animations, and an unnamed effect is a "
                 "transition rather than a missing name" % (_one,))
    if set_disagreement(_one, dict(_one)):
        sys.exit("SELF-TEST FAILED: two identical reads were reported as disagreeing, so every "
                 "run would carry a NOT PROMISED it has not earned")
    _two = dict(_one)
    del _two["(effect) on i#rulerRing"]
    if set_disagreement(_one, _two) != [("(effect) on i#rulerRing", 1, 0)]:
        sys.exit("SELF-TEST FAILED: an animation present in one read and absent from the other "
                 "was not reported. That is the exact shape T-272 measured - one run of ten, then "
                 "two of twelve - and a comparator that misses it says nothing at all")
    # **The verdict names whose finding it is**, which is the half of T-255 that costs a reviewer
    # a session rather than a wrong number. The adopter's case is delay 600 against duration 300:
    # every offset inside the delay, `fill: both` holding the FROM keyframe, and a sentence about
    # the deck printed for a fault in the seek.
    if motion_verdict(True, 600, [600, 675, 750, 825, 900]) != "MOVES":
        sys.exit("SELF-TEST FAILED: an animation that moves was reported as dead")
    _theirs = motion_verdict(False, 600, [0, 75, 150, 225, 300])
    if "delay" not in _theirs or "not the deck's" not in _theirs:
        sys.exit("SELF-TEST FAILED: an animation sampled entirely inside its own delay was "
                 "reported as a finding about the deck: %r. That is the sentence that sent the "
                 "adopter looking for a race in their own motion (T-255)" % _theirs)
    _real = motion_verdict(False, 0, [0, 50, 100, 150, 200])
    if "delay" in _real:
        sys.exit("SELF-TEST FAILED: an animation with no delay that genuinely interpolates to "
                 "nothing was excused as the tool's own fault: %r. That direction loses a real "
                 "finding, which is worse than the one this task fixed" % _real)
    if "parseFloat(seek) - (tm.delay" in MOTION_PROBE:
        sys.exit("SELF-TEST FAILED: the capture branch subtracts the delay again. That is T-255's "
                 "fault exactly, and it photographs five FROM keyframes without saying so")
    if "dly + dur * (parseFloat(p) / 100)" not in MOTION_PROBE:
        sys.exit("SELF-TEST FAILED: the report branch no longer adds the delay, so it samples the "
                 "delay instead of the animation (T-255)")
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
    # **The argument counts from one, and it did not until 2026-08-20 (T-196).** The index was the
    # internal one and the filename was `slide-%02d % (s + 1)`, so `shots <deck> 1,12,14` wrote
    # `slide-02`, `slide-13`, `slide-15` - a caller reading the shots back, which is the entire
    # point of the command, read a different numbering from the one they typed. The ruler, the
    # eyebrow, the filename and every conversation about a deck count from one; the argument was
    # the only thing that did not. Internally it stays zero-based, which is what `?s=` wants.
    count = slide_count(deck)
    if rest:
        asked = [int(x) for x in rest[0].split(",")]
        bad = [n for n in asked if not 1 <= n <= count]
        if bad:
            sys.exit("slide %s - this deck has %d, numbered 1 to %d"
                     % (", ".join(str(n) for n in bad), count, count))
        which = [n - 1 for n in asked]
    else:
        which = list(range(count))
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
