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
- **An infinite animation stops a headless render from ever settling.** DS-140's `Current` loops
  forever, so the virtual-time budget never reaches a quiescent state and `--screenshot` fires
  mid-transition, producing convincingly blank slides. Captures pin motion off first.

    python tools/deck/render.py measure examples/reference-deck.html
    python tools/deck/render.py shots   examples/reference-deck.html
    python tools/deck/render.py shots   examples/reference-deck.html 0,4,6

Output goes to `.assets-cache/deck/` (gitignored). Pure standard library (**L-07**).
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

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, ".assets-cache", "deck")

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
      s.textContent = '*{transition:none!important;animation:none!important}' +
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
        body:      cur.querySelector('.standfirst, .cost-p, .title-note'),
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


def make_probe(deck, name="probe.html", extra=""):
    html = open(deck, "r", encoding="utf-8").read()
    if "</body>" not in html:
        sys.exit("%s has no </body> - not a deck" % deck)
    html = html.replace("</body>", (PROBE if not extra else extra) + "\n</body>")
    os.makedirs(OUT, exist_ok=True)
    dest = os.path.join(OUT, name)
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

def measure(deck, which, quiet=False):
    """Collect the per-slide geometry at every resolution. `quiet` suppresses the per-row log so
    a gate can call this without burying its own verdicts."""
    probe = make_probe(deck)
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
    with open(os.path.join(OUT, "measurements.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1)
    return results


def cmd_measure(deck, which):
    results = measure(deck, which)
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
        print("        worst text-run disagreement %.2f du  (%s)  tolerance %.2f - %s"
              % (g["text"][0], g["text"][1], contract.TEXT_TOLERANCE_DU,
                 "within" if g["text_ok"] else "OVER"))
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


def cmd_shots(deck, which, w=1920, h=1234):
    """Uncalibrated on purpose: --screenshot captures the WINDOW, so asking for a window a little
    larger than the stage puts the whole stage inside the PNG instead of clipping its edge."""
    probe = make_probe(deck)
    for s in which:
        dest = os.path.join(OUT, "slide-%02d.png" % (s + 1))
        chrome_run(file_url(probe) + "?s=%d&quiet=1" % s, w, h, ["--screenshot=" + dest])
        ok = os.path.exists(dest)
        print("  %s  %s" % (os.path.basename(dest),
                            "%.0f KB" % (os.path.getsize(dest) / 1024) if ok else "FAILED"))
    print("\n%s" % OUT)


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
    return True


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    self_test()
    cmd, deck = argv[0], os.path.abspath(argv[1])
    if not os.path.exists(deck):
        sys.exit("no such deck: %s" % deck)
    which = [int(x) for x in argv[2].split(",")] if len(argv) > 2 else list(range(12))
    print("browser: %s" % CHROME)
    print("deck:    %s\n" % os.path.relpath(deck, ROOT))
    if cmd == "measure":
        cmd_measure(deck, which)
    elif cmd == "shots":
        cmd_shots(deck, which)
    else:
        sys.exit("unknown command %r - use measure or shots" % cmd)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
