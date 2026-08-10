#!/usr/bin/env python3
"""Measure how many slides the printed contents page holds, in REAL Chrome, offline.

T-034 added a generated contents page to the printable mode, and DS-226 states a rule about how it
compresses. A rule with a number in it needs the number measured, and re-measurable when the layout
changes - otherwise the first edit to the box padding silently invalidates the ruleset.

**Why this is not done in a preview pane.** The pane reports `window.innerWidth` as 0, which is
L-06/L-15's failure exactly. The contents page happens to be a fixed 1920x1080 box, so its geometry
is viewport-independent and the pane's numbers for it were in fact right - but "right by luck on
this element" is not an instrument. This drives the same real Chrome, offline, that `render.py`
uses, and reads the numbers back out of the DOM.

**What it measures.** The deck's own `@media print` rules are lifted onto screen through the CSSOM -
not a copy of them, the rules themselves - and the grid is then grown a box at a time. Because rows
are `ceil(n / 4)`, the answer is a step function, and two different numbers fall out of it:

    the bound       the largest deck where every box still shows a readable description
    the hard limit  the largest deck where the number and title render at all

Past the hard limit the page must continue onto a second sheet (T-036); no compression resolves it.

Pure standard library, by L-07. Reuses `render.py` rather than re-launching Chrome its own way.

    python tools/deck/contents_bound.py
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths                                                        # noqa: E402
import render  # noqa: E402  - the real-Chrome harness, deliberately shared

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = render.ROOT
DECK = os.path.join(ROOT, "examples", "reference-deck.html")

# A4 landscape is the paper this deck is printed on (R7). The 1920x1080 page box is 1440x810 pt and
# fit-to-page is width-bound, so a design unit is worth well under half a point on paper - which is
# why DS-226 states its floor in points and not in design units.
PT_PER_DU = 0.75 * (841.89 / 1440.0)

# The low end is here because it was missed the first time. The task framed compression as a
# question about long decks, so the first sweep ran upward from twelve and never looked below it -
# and a seven-slide page turned out to be the worse-looking of the two ends.
COUNTS = [4, 6, 7, 8, 9, 10, 12, 13, 16, 17, 20, 21, 24, 25, 28, 32, 40]

PROBE = r"""
<script>
(function(){
  function run(){
    /* Lift the deck's OWN print rules onto screen. Copying them into this probe would measure the
       copy, and the copy is what drifts. */
    var lifted = 0, css = [];
    for (var i=0;i<document.styleSheets.length;i++){
      var ss = document.styleSheets[i], rules;
      try { rules = ss.cssRules; } catch(e){ continue; }
      for (var j=0;j<rules.length;j++){
        var r = rules[j];
        if (r.type === CSSRule.MEDIA_RULE && /print/.test(r.conditionText || r.media.mediaText)){
          for (var k=0;k<r.cssRules.length;k++){ css.push(r.cssRules[k].cssText); lifted++; }
        }
      }
    }
    var st = document.createElement('style');
    st.textContent = css.join('\n');
    document.head.appendChild(st);

    var contents = document.querySelector('.contents');
    var grid = contents ? contents.querySelector('.contents-grid') : null;
    var out = { lifted: lifted, vw: window.innerWidth, vh: window.innerHeight, rows: [] };
    if (!grid){ out.error = 'no contents grid - the deck does not build one'; }
    else {
      var originals = Array.prototype.slice.call(grid.children).map(function(b){
        return b.cloneNode(true);
      });
      out.authored = originals.length;
      out.columns = getComputedStyle(grid).gridTemplateColumns.split(/\s+/).length;
      out.contentsBox = [contents.getBoundingClientRect().width,
                         contents.getBoundingClientRect().height];
      out.gridH = +grid.getBoundingClientRect().height.toFixed(2);

      function lines(el){
        return el.getBoundingClientRect().height / parseFloat(getComputedStyle(el).lineHeight);
      }
      /* The deck decides its own columns and its own density, and this asks it rather than
         repeating the rule - a second copy here is what would silently stop measuring what
         ships (L-08). */
      var layout = window.htmldeckContentsLayout;
      if (typeof layout !== 'function'){
        out.error = 'the deck exports no htmldeckContentsLayout - this tool would be measuring '
                  + 'its own copy of the layout rule instead of the deck\'s';
        document.title = 'RESULT' + JSON.stringify(out) + 'ENDRESULT';
        return;
      }
      COUNTS.forEach(function(n){
        var lay = layout(n);
        contents.style.setProperty('--ccols', lay.cols);
        contents.dataset.rows = lay.rows;
        if (lay.dense) contents.dataset.dense = ''; else delete contents.dataset.dense;
        grid.innerHTML = '';
        for (var i=0;i<n;i++) grid.appendChild(originals[i % originals.length].cloneNode(true));
        grid.offsetHeight;
        var boxes = Array.prototype.slice.call(grid.children);
        var minBot = 99, cutTitle = 0, cutNum = 0;
        boxes.forEach(function(b){
          var br = b.getBoundingClientRect();
          minBot = Math.min(minBot, lines(b.querySelector('.cbox-bottom')));
          if (b.querySelector('.cbox-title').getBoundingClientRect().bottom > br.bottom + 0.5) cutTitle++;
          if (b.querySelector('.cnum').getBoundingClientRect().bottom > br.bottom + 0.5) cutNum++;
        });
        out.rows.push({ n:n, cols:lay.cols, gridRows:lay.rows, dense:!!lay.dense,
                        boxH:+boxes[0].getBoundingClientRect().height.toFixed(2),
                        descLines:+minBot.toFixed(2), cutTitle:cutTitle, cutNum:cutNum });
      });
      /* leave the deck as it shipped */
      grid.innerHTML = '';
      originals.forEach(function(b){ grid.appendChild(b); });
    }
    document.title = 'RESULT' + JSON.stringify(out) + 'ENDRESULT';
    document.documentElement.setAttribute('data-probe-done','');
  }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function(){ setTimeout(run,120); });
  else window.addEventListener('load', run);
})();
</script>
"""


def self_test(data):
    """L-04: the checks are arithmetic done by hand first, so a wrong instrument fails loudly.

    Each one guards a way this measurement could be quietly meaningless rather than absent."""
    failures = []

    if data.get("error"):
        failures.append(data["error"])
        return failures

    # A real browser, not a pane. The pane reports 0 and would make every ratio below nonsense.
    if not data.get("vw"):
        failures.append("viewport reported as %r - this is not a real browser viewport (L-06)"
                        % data.get("vw"))
    # If no print rules were found, the page measured is the SCREEN one, which is display:none.
    if data.get("lifted", 0) < 10:
        failures.append("only %d print rule(s) lifted - the print block was not found, so what "
                        "was measured is not the printed layout" % data.get("lifted", 0))
    if data.get("columns") != 4:
        failures.append("grid reports %r columns, DS-226's arithmetic assumes 4"
                        % data.get("columns"))
    if data.get("contentsBox") != [1920.0, 1080.0]:
        failures.append("contents page is %r, expected the 1920x1080 page box"
                        % (data.get("contentsBox"),))

    by_n = dict((r["n"], r) for r in data["rows"])

    # The row arithmetic, by hand: three rows of boxes plus two gaps must fill the grid height.
    # gap is --sp-3 = 26 du. 3*boxH + 2*26 == gridH, within a rounding unit.
    if 12 in by_n:
        predicted = 3 * by_n[12]["boxH"] + 2 * 26
        if abs(predicted - data["gridH"]) > 2:
            failures.append("row arithmetic does not close at 12 slides: 3 boxes + 2 gaps = %.1f "
                            "but the grid is %.1f du - the gap is not --sp-3, or the rows are not "
                            "1fr" % (predicted, data["gridH"]))
    # Boxes must shrink as the deck grows. If they do not, `grid-auto-rows:1fr` is not in force and
    # the page is overflowing instead of compressing - which would make every number below a lie.
    heights = [by_n[n]["boxH"] for n in sorted(by_n) if n in by_n]
    if any(b - a > 0.5 for a, b in zip(heights, heights[1:])):
        failures.append("box height does not fall monotonically as the deck grows - the grid is "
                        "not compressing, so the 'bound' measured here is not a bound")
    # The sliver: a description showing part of a line. Either a full line fits or the row is
    # dense and the description is dropped outright - a few units of clipped letterform reads as a
    # rendering fault. This is the check that would have caught it at 17 slides.
    slivers = [r["n"] for r in data["rows"]
               if not r["dense"] and 0 < r["descLines"] < 1]
    if slivers:
        failures.append("part-line description at %s slide(s) - neither a full line nor dropped"
                        % ", ".join(str(n) for n in slivers))
    # The cap. A box stretched far past its content reads as content that failed to load.
    over = [(r["n"], r["boxH"]) for r in data["rows"] if r["boxH"] > 268.5]
    if over:
        failures.append("box taller than the 268 du cap at %s - the cap is not in force"
                        % ", ".join("%d slides (%.1f du)" % t for t in over))
    # The deck must be measured at the size it actually ships, or the reference case is unproven.
    #
    # **13, not 12, and the difference is a section rather than a slide.** `examples/reference-deck.html`
    # is a twelve-slide deck plus the colophon T-069 added after the close under a named DS-085
    # exemption, and the contents page is derived from the manifest, so it builds a box per section -
    # thirteen. The number was 12 and stopped being true on the day that colophon landed, which took
    # this tool from measuring to refusing and left it that way until T-084 (2026-08-10).
    #
    # **Deliberately not derived.** This assertion exists to trip when the deck moves under the
    # measurement, so a value read from the deck would agree with every deck and catch nothing. What
    # a re-baseline owes instead is saying which deck the number describes, so the next trip is
    # readable rather than mysterious - and that is what the paragraph above is.
    AUTHORED = 13
    if data.get("authored") != AUTHORED:
        failures.append("the deck built %r contents boxes, expected %d (twelve slides and the "
                        "colophon) - the reference deck changed and these numbers describe a "
                        "different deck" % (data.get("authored"), AUTHORED))
    return failures


def main():
    if render.CHROME is None:
        print("No Chrome or Edge found - this measurement needs a real browser (L-15).")
        return 3
    if not os.path.exists(DECK):
        print("Deck not found: %s" % paths.display_path(DECK, ROOT))
        return 1

    probe_src = PROBE.replace("COUNTS", json.dumps(COUNTS))
    probe = render.make_probe(DECK, name="contents-bound-probe.html", extra=probe_src)
    data, err = render.read_result(render.file_url(probe), 1920, 1200)
    if not data:
        print("No result from Chrome.\n%s" % err[:600])
        return 2

    failures = self_test(data)
    if failures:
        print("SELF-TEST FAILED")
        for f in failures:
            print("  - " + f)
        return 4
    print("self-test ok  (real viewport %dx%d, %d print rules lifted, 4 columns, "
          "row arithmetic closes)" % (data["vw"], data["vh"], data["lifted"]))

    print("\nCONTENTS PAGE - how many slides one printed sheet holds")
    print("-" * 78)
    print("  grid height %.1f du of the page's 936 usable, at %d columns"
          % (data["gridH"], data["columns"]))
    print("  1 design unit = %.4f pt printed on A4 landscape\n" % PT_PER_DU)
    print("  %-7s %-5s %-5s %-20s %-14s %s"
          % ("slides", "cols", "rows", "box height", "description", "verdict"))
    bound = hard = None
    for r in data["rows"]:
        if r["cutTitle"] or r["cutNum"]:
            verdict = "BREAKS - entry clipped"
        elif r["dense"]:
            verdict = "compact - description dropped by design"
        elif r["descLines"] < 1:
            verdict = "SLIVER - a part-line is showing, which should not happen"
        else:
            verdict = "holds"
            bound = r["n"]
        if not (r["cutTitle"] or r["cutNum"]):
            hard = r["n"]
        print("  %-7d %-5d %-5d %8.1f du (%3.0f pt) %8.2f lines   %s"
              % (r["n"], r["cols"], r["gridRows"], r["boxH"], r["boxH"] * PT_PER_DU,
                 r["descLines"], verdict))
    print("-" * 78)
    print("  THE BOUND      %s slides - the largest deck that still shows a description" % bound)
    print("  THE HARD LIMIT %s slides - the largest deck whose number and title render at all"
          % hard)
    print("\n  Past the hard limit the page must continue onto a second sheet (T-036). This is a")
    print("  LAYOUT measurement in a real browser; it does not discharge printing and looking.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
