#!/usr/bin/env python3
"""Measure how far each diagram's **ink** sits from the slide's text column.

    python tools/deck/figgrid.py <deck> [<deck> ...]

**This gates, from 2026-08-19.** `verdicts()` is DS-236's row and `check.py` reads it, so the
measurement is decided on every run rather than when somebody remembers to type the command. It
reported and did not gate until T-184, on the accurate ground that every deck this repository
shipped failed it - 18 of 21 diagrams - and a gate that is red on three correct-looking decks from
the moment it lands teaches people to ignore it. T-117 landed the rule for what a build *writes
from now on*; T-184 re-cut what was already shipped, which is what made gating it honest.

**Two causes, and only one of them is the author's.** An **aspect letterbox** - `.fig` is
`width:100%;height:100%`, so a viewBox taller in proportion than its wrapper is fitted by height and
the default `preserveAspectRatio` (`xMidYMid`) centres the slack, inset with nobody involved; and the
drawing's own **left margin** inside the viewBox. The fixes are `preserveAspectRatio="xMinYMid meet"`
and a `min-x` set to where the ink begins. This measures the outcome and does not care which caused
it.

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

RULE = "DS-236"

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


def verdicts(deck):
    """DS-236's row - `[(rule, what, ok)]`, the shape `check.py` gathers.

    **A prohibition, and the denominator is what makes it one.** *No diagram starts its ink off the
    column* has the deck's diagrams as its subject, so a deck that draws none has nothing off the
    column and passes honestly - but *0 off, of 0* and *0 off, of 8* are the same boolean and not
    the same fact (**L-36**), so the count travels in the text. That is DS-231's and DS-232's shape
    and it is here for their reason.

    **A measurement that did not happen is a failure, never a pass.** A render that produced nothing
    leaves every diagram unmeasured, which is the case T-028 found where a stage printed NO RESULT
    and the run stayed green.
    """
    if not deck:
        return [(RULE, "no deck to measure - the diagram grid gate has no subject", False)]
    return [_verdict_from(measure(deck))]


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
    # The absence discipline, in the module that owns the rule (`audit.ABSENCE_IS_A_PASS` is the
    # same fixture for the rows `audit` produces). Two cases, and they must not read alike.
    rid, what, ok = _verdict_from(rows=[])
    if not ok:
        sys.exit("SELF-TEST FAILED: a deck that draws no diagram has none off the column, so the "
                 "row is a pass. Failing it would fail every deck without a diagram")
    if "of 0" not in what:
        sys.exit("SELF-TEST FAILED: the row for a deck with no diagram does not print its own "
                 "denominator, so *0 off of 0* reads exactly like *0 off of 8* (**L-36**)")
    rid, what, ok = _verdict_from(rows=None)
    if ok:
        sys.exit("SELF-TEST FAILED: a render that produced nothing was reported as a pass. An "
                 "unmeasured diagram is not a placed one (T-028)")
    rid, what, ok = _verdict_from(rows=[{"i": 4, "off": 186.2}, {"i": 5, "off": 1.3}])
    if ok or "1 of 2" not in what or "slide 4" not in what:
        sys.exit("SELF-TEST FAILED: a deck with one diagram off the column and one inside the "
                 "tolerance did not report exactly that")
    return True


def _verdict_from(rows):
    """`verdicts` over a measurement supplied directly - what `self_test` holds the row to.

    The browser is the only reason `verdicts` takes a deck rather than rows, and the self-test has
    no browser (**L-07**). So the row's logic lives here and both callers reach it.
    """
    if rows is None:
        return (RULE, "no render result - every diagram's placement is unmeasured, not passing",
                False)
    off = [r for r in rows if abs(r["off"]) > TOLERANCE_DU]
    detail = "" if not off else " - " + "; ".join(
        "slide %d %+.1f du" % (r["i"], r["off"]) for r in off[:4])
    return (RULE, "diagrams starting their ink off the slide's text column by more than %.0f du: "
                  "%d of %d%s" % (TOLERANCE_DU, len(off), len(rows), detail), not off)


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
    print("%s: the same measurement check.py gates on, run here on its own." % RULE)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
