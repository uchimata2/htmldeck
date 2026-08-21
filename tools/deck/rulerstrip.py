#!/usr/bin/env python3
"""Render candidate treatments for the dense-mode position mark, side by side, for a person to pick.

T-178: past the ruler's capacity bound the ring is dropped and the lit dot is left at 7 du against
14 du section marks, so the mark that *changes* is the smallest thing on the ruler. Which treatment
replaces it is a question for the eye, and this tool exists to put the eye in front of the real
thing rather than in front of a description of it - the same refusal `chrome_row.py` makes about the
mark floor.

    python tools/deck/rulerstrip.py
    python tools/deck/rulerstrip.py --slides 43 --at 20
    python tools/deck/rulerstrip.py --ticks bar
    python tools/deck/rulerstrip.py --self-test

**What it produces.** One `ruler-strip.png`: every candidate, in both themes, cropped to the
navigation container, stacked and labelled. Plus a table of what each mark actually measures, read
out of the DOM in the same run - because *which is biggest* has to be a number, while *which reads
best* must not be.

**Three things here are deliberate.**

- **The crop is Chrome's, not a simulation.** There is no image library here (**L-07**) and
  `--screenshot` captures the whole window with no clip, so the strip is assembled by loading the
  real PNGs into a contact sheet and screenshotting that. Every pixel in the strip came off a real
  render of a real deck.
- **Every candidate reuses `.ruler-ring`.** It is already in every deck, `placeRing()` already puts
  it where the current tick is *by measuring the tick*, and it already translates between positions
  instead of being redrawn. A candidate that added an element would be answering a different
  question - §1's constraint is a treatment, not a new part.
- **The dot never grows.** Size on the ruler means section-versus-slide and DS-216 forbids a third
  encoding of position, so no candidate touches the lit mark's size. They differ only in what is
  drawn *around* it.

Pure standard library (**L-07**). Output goes to the deck's own project (T-074), via `paths`.
"""

import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths                                                        # noqa: E402
import render                                                       # noqa: E402
import longdeck                                                     # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = render.ROOT
DECK = os.path.join(ROOT, "examples", "reference-deck.html")

# --- the candidates ---------------------------------------------------------------------------
# Each is scoped to `.ruler[data-dense] .ruler-ring` and NOT to a tick style, so one rule serves
# `dot` and `bar` alike. That is CLAUDE.md rule 4 as a constraint on the candidate rather than as a
# check applied to it afterwards: the shipped ring is defined only under `[data-ticks="dot"]`, so a
# dense rule written the same way would silently leave `bar` with the defect it has today.
#
# `--rx` is the current tick's centre, in design units, written by `placeRing()`. Each candidate
# subtracts its own half-width, because `left:0` puts the element's LEFT edge at the ruler's origin.
BASELINE = ""

CAPSULE = """
.ruler[data-dense] .ruler-ring{
  display:block;position:absolute;left:0;top:50%;
  width:calc(10*var(--du));height:calc(30*var(--du));
  margin-top:calc(-15*var(--du));
  border:var(--rule) solid var(--accent);border-radius:calc(5*var(--du));
  background:none;
  transform:translateX(calc(var(--rx,0px) - 5*var(--du)));
  transition:transform var(--scale-dur) var(--scale-ease);
  --motion-kind:affordance;
  pointer-events:none;
}
"""

CARET = """
.ruler[data-dense] .ruler-ring{
  display:block;position:absolute;left:0;top:50%;
  width:0;height:0;
  margin-top:calc(-22*var(--du));
  border:0;border-radius:0;background:none;
  border-left:calc(5*var(--du)) solid transparent;
  border-right:calc(5*var(--du)) solid transparent;
  border-top:calc(7*var(--du)) solid var(--accent);
  transform:translateX(calc(var(--rx,0px) - 5*var(--du)));
  transition:transform var(--scale-dur) var(--scale-ease);
  --motion-kind:affordance;
  pointer-events:none;
}
"""

UNDERLINE = """
.ruler[data-dense] .ruler-ring{
  display:block;position:absolute;left:0;top:50%;
  width:calc(12*var(--du));height:calc(3*var(--du));
  margin-top:calc(11*var(--du));
  border:0;border-radius:var(--radius-xs);
  background:var(--accent);
  transform:translateX(calc(var(--rx,0px) - 6*var(--du)));
  transition:transform var(--scale-dur) var(--scale-ease);
  --motion-kind:affordance;
  pointer-events:none;
}
"""

CANDIDATES = [
    ("baseline", "what ships today - the ring is dropped and the lit dot stands alone", BASELINE),
    ("capsule", "the ring, reshaped to the dense cell: a tall outline around the current tick",
     CAPSULE),
    ("caret", "an accent arrow above the current tick, pointing at it", CARET),
    ("underline", "a short accent rule under the current tick", UNDERLINE),
]

THEMES = ("light", "dark")

# --- measurement ------------------------------------------------------------------------------
# `next.click()` then a settle, exactly as `render.PROBE` navigates. Copied rather than shared
# because that probe reports slide typography and this one reports ruler geometry, and a probe that
# returned both would be read by two tools with different reasons to change it.
PROBE = r"""
<script>
(function(){
  var P = new URLSearchParams(location.search);
  var want = parseInt(P.get('s') || '0', 10);
  function run(){
    var stage = document.getElementById('stage');
    var next  = document.getElementById('next');
    /* Pinned by `render.MOTION_PIN`, injected for every probe by
       `make_probe` (T-209). This file carried its own copy until then. */
    if (want > 0){
      if (!next) { document.title = 'PROBE-ERROR no next control'; return; }
      for (var n = 0; n < want; n++) next.click();
    }
    setTimeout(function(){
      var k = parseFloat(getComputedStyle(stage).getPropertyValue('--k')) || 1;
      var ruler = document.getElementById('ruler');
      var ticks = document.getElementById('rulerTicks');
      var ring  = document.getElementById('rulerRing');
      var box   = document.querySelector('.navbox') || ruler;
      function du(el){
        if (!el) return null;
        var r = el.getBoundingClientRect();
        if (!r.width && !r.height) return null;
        return {w:+(r.width/k).toFixed(2), h:+(r.height/k).toFixed(2)};
      }
      /* The MARK is the ::before, not the cell. The cell is the hit area and is the same width for
         every small tick; what a reader sees - and what T-178 measured at 7 px against 14 - is the
         painted pseudo-element.

         **`getComputedStyle` is NOT divided by k, and `getBoundingClientRect` is.** The stage is
         scaled with a CSS transform, and a transform does not change computed style: inside the
         stage a design unit is one CSS pixel BEFORE the transform, so the computed width already
         IS the design unit. Dividing it by k reported 7 du as 14 at the 0.5 hand-over - which is
         indistinguishable from a correct reading at the wide size, where k is 0.99 and the error
         is a rounding difference. The rendered size is the multiplication, and it is reported
         separately because that is the number DS-071 is about. */
      function mark(li){
        if (!li) return null;
        var b = li.querySelector('button');
        if (!b) return null;
        var cs = getComputedStyle(b, '::before');
        var w = parseFloat(cs.width), h = parseFloat(cs.height);
        return {w:+w.toFixed(2), h:+h.toFixed(2), px:+(w*k).toFixed(2)};
      }
      var lit = ticks.querySelector('li[data-lit]');
      var sect = ticks.querySelector('li[data-section]:not([data-lit])');
      var plain = ticks.querySelector('li:not([data-section]):not([data-lit])');
      var br = box.getBoundingClientRect();
      var out = {
        vw: window.innerWidth, vh: window.innerHeight, k: +k.toFixed(6),
        dense: ruler.hasAttribute('data-dense'),
        ticks: ticks.children.length,
        /* CSS pixels in the VIEWPORT, which is what the screenshot is, so the contact sheet can
           crop with these numbers directly. --force-device-scale-factor=1 makes the two equal. */
        boxpx: {x:+br.left.toFixed(1), y:+br.top.toFixed(1),
                w:+br.width.toFixed(1), h:+br.height.toFixed(1)},
        litMark: mark(lit), sectionMark: mark(sect), plainMark: mark(plain),
        ring: du(ring)
      };
      document.title = 'RESULT' + JSON.stringify(out) + 'ENDRESULT';
      document.documentElement.setAttribute('data-probe-done','');
    }, 250);
  }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function(){ setTimeout(run,150); });
  else window.addEventListener('load', run);
})();
</script>
"""


def fixture(deck, slides, css, theme, ticks, out_dir, stem):
    """One spliced, themed, candidate-carrying deck on disk."""
    html = longdeck.build(open(deck, encoding="utf-8").read(), slides)
    if css:
        html = longdeck.inject_css(html, css)
    if theme != "light":
        html = html.replace('data-theme="light"', 'data-theme="%s"' % theme, 1)
    if ticks != "dot":
        html = html.replace('class="ruler" id="ruler" data-ticks="dot"',
                            'class="ruler" id="ruler" data-ticks="%s"' % ticks, 1)
    dest = os.path.join(out_dir, "%s.html" % stem)
    with open(dest, "wb") as fh:
        fh.write(html.encode("utf-8"))
    return dest


SHEET_HEAD = """<!doctype html><meta charset="utf-8"><title>ruler strip</title>
<style>
 :root{color-scheme:light}
 body{margin:0;background:#f2f2f4;font:13px/1.4 -apple-system,Segoe UI,system-ui,sans-serif;color:#111}
 h1{font-size:15px;margin:16px 20px 4px}
 p.sub{margin:0 20px 14px;color:#555}
 .cand{margin:0 20px 16px;background:#fff;border:1px solid #d8d8de;border-radius:6px;overflow:hidden}
 .cand>h2{font-size:13px;margin:0;padding:8px 12px;background:#ececf1;border-bottom:1px solid #d8d8de}
 .cand>h2 span{font-weight:400;color:#555}
 .pair{display:flex;flex-direction:column}
 .shot{display:flex;align-items:center;gap:10px;padding:8px 12px;border-top:1px solid #eee}
 .shot:first-child{border-top:0}
 .tag{width:44px;flex:none;color:#666;text-transform:uppercase;letter-spacing:.06em;font-size:10px}
 .crop{position:relative;overflow:hidden;flex:none;border:1px solid #e2e2e8}
 .crop img{position:absolute;display:block;max-width:none}
</style>
<h1>T-178 &mdash; the current-position mark past the ruler's capacity bound</h1>
<p class="sub">%(sub)s</p>
"""


# --- finding the ruler in the picture ----------------------------------------------------------
# **A DOM coordinate cannot crop a screenshot here, and that is measured rather than assumed.**
# Chrome reports `innerHeight` 546 for a 1120x700 window and then paints a capture in which the deck
# occupies ~648 px - so the layout the capture used is not the layout the DOM described, even inside
# a single invocation. Two offsets fitted the wide window and neither fitted the small one, which is
# what a wrong model looks like when the first test happens to be forgiving.
#
# So the ruler is found in the image: one throwaway render outlines the navigation container in a
# colour nothing in the theme uses, and one scan reports where that colour landed. The offset is
# then a measurement of this window size, not a constant anyone has to keep true.
MARKER_CSS = ".navbox{outline:3px solid #ff00ff !important;outline-offset:0 !important}"

SCANNER = """<!doctype html><meta charset="utf-8"><title>scanning</title>
<script>
window.addEventListener('load', function(){
  var img = new Image();
  img.onload = function(){
    var c = document.createElement('canvas');
    c.width = img.naturalWidth; c.height = img.naturalHeight;
    var g = c.getContext('2d'); g.drawImage(img, 0, 0);
    var d;
    try { d = g.getImageData(0, 0, c.width, c.height).data; }
    catch (e) { document.title = 'RESULT{"err":"canvas tainted"}ENDRESULT'; return; }
    var minx = 1e9, miny = 1e9, maxx = -1, maxy = -1, hits = 0;
    for (var y = 0; y < c.height; y++){
      for (var x = 0; x < c.width; x++){
        var i = (y * c.width + x) * 4;
        /* magenta and nothing else: the themes are warm neutrals and one accent, and no deck pixel
           is simultaneously high in red and blue and low in green. */
        if (d[i] > 200 && d[i+1] < 90 && d[i+2] > 200){
          hits++;
          if (x < minx) minx = x; if (x > maxx) maxx = x;
          if (y < miny) miny = y; if (y > maxy) maxy = y;
        }
      }
    }
    document.title = 'RESULT' + JSON.stringify(
      {hits:hits, x:minx, y:miny, w:maxx-minx+1, h:maxy-miny+1, iw:c.width, ih:c.height}
    ) + 'ENDRESULT';
  };
  img.onerror = function(){ document.title = 'RESULT{"err":"image did not load"}ENDRESULT'; };
  img.src = 'MARKED';
});
</script>
"""


def locate(deck, slides, ticks, at, out_dir, w, h):
    """Where the navigation container is **in the capture**, in capture pixels.

    Two renders: one that paints a magenta outline round the box, one that reads the pixels back.
    The reading needs `--allow-file-access-from-files`, because a canvas that drew a `file://` image
    is otherwise tainted and `getImageData` throws - acceptable in an instrument, and stated here so
    nobody copies it into a gate.

    Done once per run rather than per candidate: the box does not move between candidates, because
    no candidate changes layout - they all draw inside a ring that is already absolutely positioned.
    """
    fx = fixture(deck, slides, MARKER_CSS, "light", ticks, out_dir, "t178-marker")
    probe = render.make_probe(fx, name="t178-marker-probe.html", extra=PROBE, out=out_dir)
    marked = os.path.join(out_dir, "t178-marker.png")
    render.chrome_run(render.file_url(probe) + "?s=%d" % at, w, h, ["--screenshot=" + marked])
    if not (os.path.isfile(marked) and os.path.getsize(marked)):
        raise ValueError("the marker render produced no image at %s" % marked)
    scan = os.path.join(out_dir, "t178-scan.html")
    with open(scan, "wb") as fh:
        fh.write(SCANNER.replace("MARKED", os.path.basename(marked)).encode("utf-8"))
    res, err = render.read_result(render.file_url(scan), 900, 600,
                                  extra=["--allow-file-access-from-files"])
    if not res:
        raise ValueError("the scanner returned nothing\n%s" % err[:300])
    if res.get("err"):
        raise ValueError("the scanner could not read the capture: %s" % res["err"])
    if res["hits"] < 100:
        raise ValueError("only %d marker pixel(s) in the capture - the outline did not render, so "
                         "the crop would be a guess" % res["hits"])
    return res


def png_size(path):
    """`(width, height)` from the IHDR, which is the first chunk and always at a fixed offset.

    Twelve bytes of struct rather than an image library, because there is none here (**L-07**) and
    this needs the dimensions, not the pixels.
    """
    with open(path, "rb") as fh:
        head = fh.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("%s is not a PNG" % path)
    return struct.unpack(">II", head[16:24])


def sheet(rows, out_dir, sub):
    """The contact sheet: real screenshots, cropped by the browser to the navigation container."""
    parts = [SHEET_HEAD % {"sub": sub}]
    for name, why, shots in rows:
        parts.append('<div class="cand"><h2>%s &nbsp;<span>%s</span></h2><div class="pair">'
                     % (name, why))
        for theme, png, box in shots:
            pad = 10
            x, y = max(0, box["x"] - pad), max(0, box["y"] - pad)
            w, h = box["w"] + pad * 2, box["h"] + pad * 2
            parts.append('<div class="shot"><span class="tag">%s</span>'
                         '<div class="crop" style="width:%.0fpx;height:%.0fpx">'
                         '<img src="%s" style="left:%.0fpx;top:%.0fpx"></div></div>'
                         % (theme, w, h, os.path.basename(png), -x, -y))
        parts.append("</div></div>")
    dest = os.path.join(out_dir, "ruler-strip-sheet.html")
    with open(dest, "wb") as fh:
        fh.write("".join(parts).encode("utf-8"))
    # The capture window is derived from the crops, never guessed. A fixed size silently clips the
    # last candidate off the bottom and the pager off the right - and a strip that is missing an
    # option is worse than no strip, because nothing in the picture says an option is missing.
    pad = 10
    cw = max(box["w"] + pad * 2 for _n, _w, shots in rows for _t, _p, box in shots)
    ch = max(box["h"] + pad * 2 for _n, _w, shots in rows for _t, _p, box in shots)
    width = int(cw + 44 + 24 + 26 + 40)          # tag column, gaps, card padding, page margins
    height = int(90 + len(rows) * (34 + 2 * (ch + 18) + 16) + 30)
    return dest, width, height


def run(deck=DECK, slides=25, at=8, ticks="dot", out=None, w=1920, h=1234):
    if not render.CHROME:
        print("No Chrome or Edge found - this needs a real browser (L-15).")
        return 3
    # **Absolute, here and nowhere else.** `--screenshot=` is handed straight to Chrome, which
    # resolves a relative path against its OWN working directory - so a relative `--out` writes the
    # picture somewhere the tool then reports as missing. That is T-094 exactly, and T-186 after it;
    # both were found the same way, by a tool that looked correct and produced nothing.
    out_dir = os.path.abspath(out or os.path.join(paths.output_root(deck),
                                                  ".assets-cache", "deck", "t178"))
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    try:
        crop = locate(deck, slides, ticks, at, out_dir, w, h)
    except ValueError as e:
        print("could not find the ruler in the capture: %s" % e)
        return 2

    rows, table = [], []
    for name, why, css in CANDIDATES:
        shots = []
        for theme in THEMES:
            stem = "t178-%s-%s" % (name, theme)
            fx = fixture(deck, slides, css, theme, ticks, out_dir, stem)
            probe = render.make_probe(fx, name=stem + "-probe.html", extra=PROBE, out=out_dir)
            url = render.file_url(probe)
            png = os.path.join(out_dir, stem + ".png")
            # One run for both. See `inset` - the two flags lay out at different viewports, so the
            # measurement and the picture have to come out of the same invocation.
            res, err = render.read_result(url + "?s=%d" % at, w, h,
                                          extra=["--screenshot=" + png])
            if not res:
                print("  %-10s %-5s  NO RESULT from Chrome\n%s" % (name, theme, err[:300]))
                return 2
            if not (os.path.isfile(png) and os.path.getsize(png)):
                print("  %-10s %-5s  no image at %s" % (name, theme, png))
                return 2
            if png_size(png) != (crop["iw"], crop["ih"]):
                print("  %-10s %-5s  capture is %dx%d but the located crop came off a %dx%d "
                      "image" % ((name, theme) + png_size(png) + (crop["iw"], crop["ih"])))
                return 2
            shots.append((theme, png, crop))
            if theme == "light":
                table.append((name, res))
        rows.append((name, why, shots))

    sub = ("%d slides, tick style <b>%s</b>, viewing slide %d, rendered at %dx%d in real Chrome, "
           "offline. Every candidate reuses the existing ring element and none changes the size of "
           "the lit mark." % (slides, ticks, at + 1, w, h))
    sheet_path, sw, sh = sheet(rows, out_dir, sub)
    strip = os.path.join(out_dir, "ruler-strip.png")
    render.chrome_run(render.file_url(sheet_path), sw, sh, ["--screenshot=" + strip])

    print("\nDENSE-MODE MARKS - design units, read out of the DOM (light theme)\n")
    print("  %-11s %-6s %-11s %-11s %-11s %-13s %s"
          % ("candidate", "dense", "lit mark", "section mark", "plain mark", "treatment",
             "lit, rendered"))
    for name, res in table:
        def fmt(m):
            return "-" if not m else "%.0fx%.0f" % (m["w"], m["h"])
        ring = res.get("ring")
        print("  %-11s %-6s %-11s %-11s %-11s %-13s %s"
              % (name, "yes" if res["dense"] else "NO", fmt(res["litMark"]),
                 fmt(res["sectionMark"]), fmt(res["plainMark"]),
                 "none" if not ring else "%.0fx%.0f du" % (ring["w"], ring["h"]),
                 "-" if not res["litMark"] else "%.2f px" % res["litMark"]["px"]))
    k = table[0][1]["k"]
    print("\n  %d ticks, stage scale k=%.3f, so a design unit renders at %.3f CSS px here."
          % (table[0][1]["ticks"], k, k))
    print("  The treatment column is design units; multiply by %.3f for what the screen got."
          % k)
    print("\n%s" % paths.display_path(strip, ROOT))
    return strip


def self_test():
    """Structure only. Whether a candidate READS best is the question this tool refuses to answer."""
    fail = []
    names = [n for n, _, _ in CANDIDATES]
    if len(set(names)) != len(names):
        fail.append("two candidates share a name, so their fixtures would overwrite each other")
    if names[0] != "baseline":
        fail.append("the first candidate must be the baseline - a strip with nothing to compare "
                    "against is a picture of one option")
    for name, _why, css in CANDIDATES[1:]:
        if ".ruler[data-dense] .ruler-ring" not in css:
            fail.append("%s does not target `.ruler[data-dense] .ruler-ring`; it either adds an "
                        "element or misses dense mode" % name)
        if "data-ticks" in css:
            fail.append("%s scopes itself to a tick style, which forks the component "
                        "(CLAUDE.md rule 4)" % name)
        if "li[data-lit]" in css or "button::before" in css:
            fail.append("%s touches the lit mark itself; size on the ruler means section-versus-"
                        "slide and DS-216 forbids a third encoding of position" % name)
        if "--rx" not in css:
            fail.append("%s does not read --rx, so it would not follow the current tick" % name)
    # The measurement probe has to report the two numbers the whole task is about.
    for needed in ("litMark", "sectionMark", "dense", "boxpx"):
        if needed not in PROBE:
            fail.append("the probe does not report %r" % needed)
    if fail:
        sys.exit("SELF-TEST FAILED:\n  - " + "\n  - ".join(fail))
    print("self-test OK - %d candidates, each on the shared ring, none scoped to a tick style, "
          "none touching the lit mark, and the probe reports the marks and the crop box"
          % len(CANDIDATES))


def main(argv):
    if "--self-test" in argv:
        return self_test()
    opts = {"slides": 25, "at": 8, "ticks": "dot", "out": None, "window": "1920x1234"}
    rest = list(argv)
    while rest:
        a = rest.pop(0)
        if a in ("--slides", "--at"):
            if not rest:
                sys.exit("%s needs a number" % a)
            opts[a.lstrip("-")] = int(rest.pop(0))
        elif a in ("--ticks", "--out", "--window"):
            if not rest:
                sys.exit("%s needs a value" % a)
            opts[a.lstrip("-")] = rest.pop(0)
        else:
            sys.exit("unknown option %r - this takes [--slides n] [--at n] [--ticks dot|bar] "
                     "[--window WxH] [--out dir] [--self-test]" % a)
    if opts["ticks"] not in ("dot", "bar"):
        sys.exit("--ticks is dot or bar, got %r" % opts["ticks"])
    # `--window` exists for one question: DS-071 bottoms the stage out at 0.5 scale, and a mark
    # that reads at k=0.99 may not exist at k=0.51. 1120x700 is the smallest size `chrome_row.py`
    # found that still lands ABOVE the hand-over, so it is the floor to look at rather than a
    # smaller number that measures no stage at all.
    try:
        w, h = (int(v) for v in opts["window"].lower().split("x"))
    except ValueError:
        sys.exit("--window takes WxH, got %r" % opts["window"])
    return run(slides=opts["slides"], at=opts["at"], ticks=opts["ticks"], out=opts["out"],
               w=w, h=h)


if __name__ == "__main__":
    main(sys.argv[1:])
