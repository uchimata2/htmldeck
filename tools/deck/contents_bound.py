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

    the bound       the largest SHEET where every box still shows a readable description
    the hard limit  the largest sheet where the number and title render at all

**Since T-036 those are sheet numbers, not deck numbers, and the deck can no longer reach either.**
Past 16 entries the page continues onto further sheets, so the compression bands past the bound are
what a sheet *would* do if a cap moved rather than what any deck prints. They are still measured
here, because they are the only instrument DS-226's numbers have. What is asserted instead is the
cap: the split rule the deck ships is exercised on stage shapes that stress it, and a sheet that
came back over its cap - or an entry that came back missing, reordered or duplicated - fails the
run.

**And since T-125 there are two caps, so which one applies depends on whether the page split.** One
sheet holds up to 16; once the page continues, every sheet holds at most 12, because 13 crosses into
the four-row band and that band clamps a description to one line. Both are asserted below, on the
same eight shapes.

**Both numbers are entry counts, and an entry's height is not constant - so the fixture pins the
height.** Every cloned box gets the same three-line description (`BOTTOM`), which is what a real
deck writes and what the reference deck happens not to. Until T-116 the clones carried the
reference deck's own shorter bottom lines, and a bound measured on entries of one height is not a
bound: the first adopting project collided at 13 against a stated limit of 24. The clones keep
their real titles, so the box with the tallest title is the one the description is measured in.

**What this tool cannot see, stated because it already cost a release.** It measures a SCREEN
simulation of print. T-116 was a print-only divergence: Chrome's paged layout gave a grid item its
own content height instead of its track, so cards printed 200.2 pt tall in a 151 pt pitch and rows
overlapped - while the numbers below, measured the same day on the same deck, were correct and
clean. **Nothing here decides whether a printed sheet is clean, and this tool must not be read as
saying so** - that is `printgeom.py`, which reads the card rectangles out of the printed PDF and
asserts that none intersects and none reaches the footnote (T-123). What is measured here is the
bands and the two caps - the *inputs* to the split rule - which the printed reading does not measure
and which are worth having in seconds rather than in a minute of Chrome. The two are not
alternatives; the screen tool sizes the rule and the printed one decides the page.

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

# The tallest realistic entry, and the reason the numbers below are believable (T-116). DS-211
# wants the map to state the argument rather than label it, so three lines is what a deck writes
# when the slide has one; the self-test measures this string rather than trusting the sentence.
BOTTOM = ("Frequency compounds where bike-share plateaus, and the gap is already visible in the "
          "2029 figures rather than in the forecast that follows them.")


def even(n, stages):
    """`n` entries dealt into `stages` stages as evenly as they divide - the shape a real argument
    has. Returned as one stage key per entry, in slide order."""
    out = []
    for s in range(stages):
        take = -(-(n - len(out)) // (stages - s))
        out += [s] * take
    return out


# The split rule's input is the stage SHAPE, not the entry count, because the cut falls at a stage
# boundary (T-036). Each case is one stage key per entry in slide order, `-1` for back matter, plus
# the number of sheets it should take - written out rather than computed, so the expectation is a
# number a reader can check by hand rather than a second copy of the rule.
#
# **`ceil(n / 12)` is a floor, not the answer.** The 43-entry deck whose argument is one stage of 40
# splits into runs of 10 · 10 · 10 · 10, then a stage of 2 and a colophon: four sheets are full
# before the last three entries are placed, so it takes FIVE where the arithmetic says four. That is
# the answered question working as specified - the boundary is preferred to the sheet count. Under
# the single cap of 16 the same sentence was true of the seven-even-stages case at 43, which now
# lands exactly on its floor of four; the demonstration moved, the rule did not.
#
# The last two are the cases with no boundary to cut at, where DS-226's never-drop invariant forces
# the split inside a stage. They are the reason `splitLongRuns` exists.
#
# **Two of these moved on 2026-08-13 with T-125's second cap**, and they are the whole reason it was
# taken: the 25-entry deck went from 12 · 13 to three sheets, and the 40-entry stage from three
# sheets to five. Both bought their old sheet count by printing one-line fragments. Nothing else
# here moved, because the balancing search already reached below 12 for the other six.
SPLIT_CASES = [
    ("13 entries, the reference deck's length", even(13, 7), 1),
    ("16 entries, exactly the bound", even(16, 7), 1),
    ("17 entries, one past it", even(17, 7), 2),
    ("25 entries, past the old hard limit", even(25, 7), 3),
    ("43 entries, the longest deck anyone reports", even(43, 7), 4),
    ("17 entries, a stage of 12 then a stage of 5", [0] * 12 + [1] * 5, 2),
    ("20 entries, one stage throughout", [0] * 20, 2),
    ("43 entries, a stage of 40 and a colophon", [0] * 40 + [1, 1] + [-1], 5),
]

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
      /* what the description WOULD set to with nothing clamping it - the fixture's entry height,
         measured rather than asserted (T-116) */
      function fullLines(el){
        return el.scrollHeight / parseFloat(getComputedStyle(el).lineHeight);
      }
      /* The deck decides its own columns and its own density, and this asks it rather than
         repeating the rule - a second copy here is what would silently stop measuring what
         ships (L-08). */
      var layout = window.htmldeckContentsLayout;
      var split = window.htmldeckContentsSheets;
      if (typeof layout !== 'function' || typeof split !== 'function'){
        out.error = 'the deck exports no htmldeckContentsLayout/htmldeckContentsSheets - this '
                  + 'tool would be measuring its own copy of the rules instead of the deck\'s';
        document.title = 'RESULT' + JSON.stringify(out) + 'ENDRESULT';
        return;
      }

      /* The shipped split rule (T-036), run on the stage shapes that stress it. The entries are
         synthetic because the input that matters is the SHAPE - where one stage ends and the next
         begins - and no single deck carries eight of them. `idx` rides along so the flattened
         result proves every entry survived, once, in order. */
      out.splits = SPLITS.map(function(c){
        var man = c[1].map(function(st, i){
          return { idx: i, back: st < 0, stage: st < 0 ? null : st };
        });
        var sheets = split(man);
        return { name: c[0], want: c[2],
                 sizes: sheets.map(function(s){ return s.length; }),
                 order: [].concat.apply([], sheets).map(function(m){ return m.idx; }) };
      });

      COUNTS.forEach(function(n){
        var lay = layout(n);
        contents.style.setProperty('--ccols', lay.cols);
        contents.style.setProperty('--crows', lay.rows);
        contents.dataset.rows = lay.rows;
        if (lay.dense) contents.dataset.dense = ''; else delete contents.dataset.dense;
        grid.innerHTML = '';
        for (var i=0;i<n;i++){
          var clone = originals[i % originals.length].cloneNode(true);
          /* the fixture's one pinned variable: every entry carries the SAME three-line
             description, so the bound is measured on the entry that breaks it (T-116) */
          clone.querySelector('.cbox-bottom').textContent = BOTTOM;
          grid.appendChild(clone);
        }
        grid.offsetHeight;
        var boxes = Array.prototype.slice.call(grid.children);
        var minBot = 99, maxFull = 0, cutTitle = 0, cutNum = 0;
        boxes.forEach(function(b){
          var br = b.getBoundingClientRect();
          minBot = Math.min(minBot, lines(b.querySelector('.cbox-bottom')));
          maxFull = Math.max(maxFull, fullLines(b.querySelector('.cbox-bottom')));
          if (b.querySelector('.cbox-title').getBoundingClientRect().bottom > br.bottom + 0.5) cutTitle++;
          if (b.querySelector('.cnum').getBoundingClientRect().bottom > br.bottom + 0.5) cutNum++;
        });
        out.rows.push({ n:n, cols:lay.cols, gridRows:lay.rows, dense:!!lay.dense,
                        boxH:+boxes[0].getBoundingClientRect().height.toFixed(2),
                        descLines:+minBot.toFixed(2), fixtureLines:+maxFull.toFixed(2),
                        cutTitle:cutTitle, cutNum:cutNum });
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

    # The fixture's own claim, measured rather than trusted. A "three-line description" that
    # quietly sets to two makes every number below describe a shorter entry than the one that
    # broke the page - which is the exact way the old fixture was wrong (T-116).
    # A dense row hides the description outright, so it has no height to measure - excluded here
    # rather than special-cased below, because "0.00 lines" there means dropped, not short.
    thin = [(r["n"], r["fixtureLines"]) for r in data["rows"]
            if r["cols"] == 4 and not r["dense"] and r["fixtureLines"] < 3]
    if thin:
        failures.append("the fixture's description sets to fewer than three lines at %s - the "
                        "bound below describes a shorter entry than the one that broke the page"
                        % ", ".join("%d slides (%.2f lines)" % t for t in thin))

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
    # ---- the split rule (T-036). Three invariants, and the first is the one DS-226 states.
    #
    # Checked here rather than trusted because the split is the only thing now standing between a
    # long deck and the compression bands below: every band past the bound is unreachable if and
    # only if no sheet ever exceeds the bound.
    if len(data.get("splits") or []) != len(SPLIT_CASES):
        failures.append("the probe returned %d split results for %d cases - the sheet rule was "
                        "not exercised, so nothing here says the bound is respected"
                        % (len(data.get("splits") or []), len(SPLIT_CASES)))
    for s in data.get("splits") or []:
        n = sum(s["sizes"])
        # DS-226, the whole of it: every entry, exactly once, in slide order. A contents page that
        # silently omits or reorders a slide is confidently wrong about the shape of the argument.
        if s["order"] != list(range(n)):
            failures.append("%s: the sheets do not carry every entry once in order" % s["name"])
        # Which cap applies is decided by whether the page split at all (T-125): a lone sheet holds
        # 16, every sheet of a continued page holds 12. Read off the result rather than off the
        # entry count, so a rule that split when it should not have is still measured against the
        # cap it actually used.
        cap = 16 if len(s["sizes"]) == 1 else 12
        over = [z for z in s["sizes"] if z > cap]
        if over:
            why = ("the compression bands past the bound are reachable again" if cap == 16 else
                   "a split sheet in the four-row band clamps every description to one line, "
                   "which is what T-125 ruled out")
            failures.append("%s: sheet of %s entries, over the cap of %d - %s"
                            % (s["name"], ", ".join(str(z) for z in over), cap, why))
        if 0 in s["sizes"]:
            failures.append("%s: an empty sheet" % s["name"])
        if len(s["sizes"]) != s["want"]:
            failures.append("%s: %d sheets, expected %d"
                            % (s["name"], len(s["sizes"]), s["want"]))

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

    probe_src = (PROBE.replace("COUNTS", json.dumps(COUNTS))
                      .replace("SPLITS", json.dumps(SPLIT_CASES))
                      .replace("BOTTOM", json.dumps(BOTTOM)))
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
    print("  1 design unit = %.4f pt printed on A4 landscape" % PT_PER_DU)
    fixture = max(r["fixtureLines"] for r in data["rows"] if not r["dense"])
    print("  every entry carries the same description, which sets to %.2f lines at 4 columns\n"
          % fixture)
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
    print("  THE BOUND      %s slides - the largest sheet that still shows a description," % bound)
    print("                 measured where every entry wants %.2f lines of one. A deck whose"
          % fixture)
    print("                 descriptions are shorter does not earn a higher bound; it gets")
    print("                 emptier boxes, because the clamp is per row band and the band is")
    print("                 decided by the slide count alone.")
    print("  THE HARD LIMIT %s slides - the largest sheet whose number and title render at all"
          % hard)
    print("\n  Both are SHEET numbers since T-036, and there are two caps since T-125: a lone")
    print("  sheet holds 16, a sheet of a continued page holds 12 - so the four-row band is")
    print("  reached only by a deck of 13 to 16, and the bands past the bound by no deck at all.")

    print("\nTHE SPLIT - how a deck past the bound divides across sheets")
    print("-" * 78)
    print("  %-46s %-7s %s" % ("stage shape", "sheets", "entries per sheet"))
    for s in data["splits"]:
        print("  %-46s %-7d %s"
              % (s["name"], len(s["sizes"]), " · ".join(str(z) for z in s["sizes"])))
    print("-" * 78)
    print("  The cut falls at a stage boundary, and the sheets are balanced rather than filled")
    print("  and spilled - 17 entries print 9 and 8, not 12 and 5. The last two shapes have no")
    print("  boundary to cut at, so the boundary yields and the entry does not (DS-226).")

    print("\n  This is a SCREEN measurement of the bands and the caps. It says nothing about")
    print("  whether a printed sheet is clean - T-116 was a print-only fault that these numbers")
    print("  were clean throughout. `printgeom.py` decides the printed page; this sizes the rule.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
