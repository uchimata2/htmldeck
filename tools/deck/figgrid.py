#!/usr/bin/env python3
"""Measure how far each diagram's **ink** sits from the slide's text column.

    python tools/deck/figgrid.py <deck> [<deck> ...]

**This reports; it does not gate, and that is deliberate rather than unfinished.** Every deck this
repository ships violates the rule it measures, so a gated version would be red on three correct-
looking decks from the moment it landed. T-117 landed the rule for what a build *writes from now
on*; [T-184] re-cuts the diagrams already shipped and promotes this to a gated `DS-nnn` once the
decks can pass it. Until then the number is a finding somebody can re-derive in one command, which
is worth more than a comment saying the same thing.

**What it measures, and why not the `<svg>` element.** The element is already on the column - 96 du
on every slide of every deck, exactly where the headline, the body and the bottom line sit. What is
inset is the drawing *inside* the viewBox: a diagram declares its own (`0 0 1900 430`), the element
is scaled to the content column, and the leftmost drawn thing lands wherever the author left it. So
the measurement is the leftmost **ink** against the slide's text left edge, both read from the laid
out page - not from the markup, which cannot know the scale factor.

Real Chrome, offline, through `render.py`'s runner, so the flags and the viewport calibration are
the shipped ones. Pure standard library (**L-07**).
"""

import json
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import paths                                                            # noqa: E402
import render                                                           # noqa: E402

ROOT = render.ROOT

# What counts as on the column. A diagram whose ink starts within this of the text edge is placed,
# not merely near - the two slides that already come out at +1 and +2 du are inside it, and they
# are the accident this rule turns into the rule.
TOLERANCE_DU = 4.0

PROBE = r"""
<script>
window.addEventListener('load', function () {
  setTimeout(function () {
    var vw = document.documentElement.clientWidth, vh = document.documentElement.clientHeight;
    var out = [];
    var slides = document.querySelectorAll('.slide');
    for (var i = 0; i < slides.length; i++) {
      var s = slides[i], st = s.getBoundingClientRect();
      if (st.width < 2) { continue; }
      var svg = s.querySelector('.body svg.fig') || s.querySelector('.body svg');
      if (!svg) { continue; }
      var box = svg.getBoundingClientRect();
      if (box.width < st.width / 4) { continue; }   /* an icon, not a diagram */
      var text = s.querySelector('.headline') || s.querySelector('.body');
      if (!text) { continue; }
      var tl = text.getBoundingClientRect().left - st.left;
      var min = null;
      var kids = svg.querySelectorAll('rect,path,polygon,circle,ellipse,line,text,image,use');
      for (var k = 0; k < kids.length; k++) {
        var r = kids[k].getBoundingClientRect();
        if (r.width <= 0.5 && r.height <= 0.5) { continue; }
        var left = r.left - st.left;
        if (min === null || left < min) { min = left; }
      }
      if (min === null) { continue; }
      out.push({slide: s.dataset.name || ('slide ' + (i + 1)),
                i: i + 1,
                textL: Math.round(tl * 100) / 100,
                inkL: Math.round(min * 100) / 100,
                svgL: Math.round((box.left - st.left) * 100) / 100});
    }
    var el = document.createElement('div');
    el.textContent = 'RESULT' + JSON.stringify({vw: vw, vh: vh, figs: out}) + 'ENDRESULT';
    document.body.appendChild(el);
  }, 700);
});
</script>
"""


def measure(deck):
    """`[{slide, i, textL, inkL, svgL, off}]` - one row per diagram, or `None` if nothing rendered."""
    probe = render.make_probe(deck, name="figgrid.html", extra=PROBE, out=render.out_dir(deck))
    cw, ch = render.calibrate(probe, 1920, 1234)
    data, err = render.read_result(render.file_url(probe), cw, ch)
    if not data:
        print("  !! no result for %s\n%s" % (deck, err[:300]))
        return None
    for row in data["figs"]:
        row["off"] = round(row["inkL"] - row["textL"], 2)
    return data["figs"]


def report(deck, rows):
    """One deck's rows, and the count that is the finding. Returns `(off_grid, total)`."""
    name = paths.display_path(deck, ROOT).replace("\\", "/")
    if rows is None:
        print("%s - no result" % name)
        return (0, 0)
    if not rows:
        print("%s - no diagram measured" % name)
        return (0, 0)
    off = [r for r in rows if abs(r["off"]) > TOLERANCE_DU]
    print("%s - %d diagram(s), %d off the text column by more than %.0f du"
          % (name, len(rows), len(off), TOLERANCE_DU))
    for r in rows:
        print("   slide %-3d %-42s text %6.1f  ink %6.1f  %+7.1f%s"
              % (r["i"], r["slide"][:42], r["textL"], r["inkL"], r["off"],
                 "" if abs(r["off"]) <= TOLERANCE_DU else "   OFF"))
    return (len(off), len(rows))


def self_test():
    """The arithmetic, and the two ways of reading it wrongly (**L-04**)."""
    rows = [{"slide": "a", "i": 1, "textL": 96.0, "inkL": 98.0, "svgL": 96.0, "off": 2.0},
            {"slide": "b", "i": 2, "textL": 96.0, "inkL": 282.0, "svgL": 96.0, "off": 186.0}]
    off = [r for r in rows if abs(r["off"]) > TOLERANCE_DU]
    if len(off) != 1 or off[0]["slide"] != "b":
        sys.exit("SELF-TEST FAILED: the tolerance did not split a placed diagram from an inset one")
    # **The svg element being on the column is not the question.** Both rows above have svgL == 96,
    # and one of them is 186 du off. A check that read the element would report this deck clean,
    # which is what every gate did before T-117 measured it.
    if any(r["svgL"] != r["textL"] for r in rows):
        sys.exit("SELF-TEST FAILED: the fixture no longer models the case - the svg element sits "
                 "on the column in both rows, and that is the point")
    # A negative offset is off the column too: ink left of the text is not alignment.
    if not [r for r in [{"off": -90.0}] if abs(r["off"]) > TOLERANCE_DU]:
        sys.exit("SELF-TEST FAILED: ink to the LEFT of the text column was read as placed")
    return True


def main(argv):
    if not argv:
        print(__doc__.strip())
        return 2
    self_test()
    total_off = total = 0
    for deck in argv:
        if deck.startswith("-"):
            continue
        o, n = report(deck, measure(deck))
        total_off += o
        total += n
        print("")
    print("%d of %d diagram(s) sit off the slide's text column by more than %.0f du."
          % (total_off, total, TOLERANCE_DU))
    print("This reports and does not gate: T-184 re-cuts the diagrams and promotes it to a rule.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
