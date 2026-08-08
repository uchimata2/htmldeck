#!/usr/bin/env python3
"""Measure the chrome row the ruler navigator has to move into, in REAL Chrome, offline.

T-035 replaces the stage-name ribbon with a ruler, and two numbers decide whether that fits. Both
are currently arithmetic on paper, and this measures them instead:

    the target bound   how many 48 x 48 du targets (DS-168) fit in what the row has LEFT once the
                       right-hand controls have taken their share. T-035 derives "around 30" from
                       1728 / 48 = 36 and then subtracts the controls by eye. The controls have
                       never been measured.
    the mark floor     the stage bottoms out at 0.5 scale (DS-071), so a mark of n design units
                       renders at n/2 CSS px. This reports the rendered size of candidate marks at
                       that floor; whether one SURVIVES there is a question for the eye, and this
                       tool says so rather than pretending to answer it.

It also re-measures the ribbon itself. T-035 cites "~1450 of 1728" from a comment in the deck's own
source, and a number read out of a comment is a quotation, not a measurement (L-36, L-38).

Pure standard library, by L-07. Reuses `render.py` rather than launching Chrome its own way.

    python tools/deck/chrome_row.py
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render  # noqa: E402  - the real-Chrome harness, deliberately shared

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = render.ROOT
DECK = os.path.join(ROOT, "examples", "reference-deck.html")

# DS-168: >= 24 x 24 CSS px, which inside the stage is >= 48 x 48 design units, because a design
# unit is worth half a CSS pixel at the 0.5 scale floor.
TARGET_FLOOR_DU = 48
# What the ruler declares as its pitch, in `TICK_PITCH_DU`. It is `--disc-hit` (52), not the bare
# floor, so a tick is the same size as every other hit target in the deck.
DECLARED_PITCH_DU = 52
# The row, from --pad-x on both sides of a 1920 stage. Asserted rather than assumed.
ROW_DU = 1920 - 2 * 96
# Candidate mark sizes for the degraded mode, in design units.
MARKS = [2, 3, 4, 5, 6, 8, 10]

PROBE = r"""
<script>
(function(){
  function run(){
    var stage = document.getElementById('stage');
    var k = parseFloat(getComputedStyle(stage).getPropertyValue('--k')) || 0;
    function du(el){
      var r = el.getBoundingClientRect();
      return { w:+(r.width/k).toFixed(2), h:+(r.height/k).toFixed(2),
               l:+(r.left/k).toFixed(2), r:+(r.right/k).toFixed(2) };
    }
    var chrome   = document.querySelector('.chrome');
    /* The indicator: the ruler since T-035, the ribbon before it. Both are measured the same way -
       what the left-hand block costs and what the row has left - so the numbers stay comparable
       across the replacement rather than restarting at it. */
    var ribbon   = document.getElementById('rulerTicks') || document.getElementById('ribbon');
    var controls = document.querySelector('.controls');
    var out = { k:+k.toFixed(6), vw:window.innerWidth, vh:window.innerHeight };
    if (!chrome || !ribbon || !controls){
      out.error = 'chrome row not found - the deck has changed shape';
    } else {
      out.chrome   = du(chrome);
      out.ribbon   = du(ribbon);
      out.controls = du(controls);
      /* every child of the controls block, priced individually - T-035 says there are five and
         that the ruler must share the row with them, but never measured what they cost */
      out.controlItems = [];
      Array.prototype.forEach.call(controls.children, function(c){
        var d = du(c);
        out.controlItems.push({ id:c.id || c.className || c.tagName.toLowerCase(),
                                w:d.w, h:d.h });
      });
      /* The gap is read from the ROW's own `gap`, not inferred from the distance between the two
         boxes. Those agreed while the ribbon filled its space, and stopped agreeing the moment the
         ruler's flexible label took the slack instead - at which point the inferred figure was
         596 du of "gap" and the free space collapsed to the ticks' own width. Correct by accident
         is not correct. */
      var gapCss = parseFloat(getComputedStyle(chrome).gap) / k;
      out.gapDu = +(isFinite(gapCss) ? gapCss : 0).toFixed(2);
      /* what the indicator actually gets: the row minus the controls minus that gap */
      out.freeDu = +(out.chrome.w - out.controls.w - out.gapDu).toFixed(2);
      /* the current ribbon's real footprint, against the number quoted from the source comment */
      out.ribbonPct = +((out.ribbon.w / out.chrome.w) * 100).toFixed(1);
      /* The ribbon's BOX is not its CONTENT. It is a flex child that stretches to the space it is
         given, so measuring the <ul> reports what is available, not what is used - and T-035's
         premise is a claim about what is USED ("~1450 of 1728, 84%", quoted from a source
         comment). Measure the content extent and the overflow directly. */
      var items = Array.prototype.slice.call(ribbon.children);
      out.ribbonItems = items.length;
      if (items.length){
        var first = items[0].getBoundingClientRect();
        var last  = items[items.length-1].getBoundingClientRect();
        out.ribbonContentDu = +(((last.right - first.left)/k)).toFixed(2);
      }
      /* Split the ribbon's children. The stage items carry the names; the `link` items are the
         connector dashes between them, and being flexible they are what absorbs compression -
         so the row can be AT capacity while still rendering cleanly, which is not something the
         overflow figure alone can tell you. */
      var named = [], links = [];
      items.forEach(function(li){
        var w = +(li.getBoundingClientRect().width/k).toFixed(2);
        (li.className.indexOf('link') >= 0 ? links : named).push(w);
      });
      out.namedItems = named;
      out.linkItems = links;
      out.namedTotal = +named.reduce(function(a,b){ return a+b; }, 0).toFixed(2);
      out.linkTotal  = +links.reduce(function(a,b){ return a+b; }, 0).toFixed(2);
      out.linkMin    = links.length ? Math.min.apply(null, links) : 0;
      out.linkMax    = links.length ? Math.max.apply(null, links) : 0;

      out.ribbonScrollDu = +(ribbon.scrollWidth/k).toFixed(2);
      out.ribbonOverflowDu = +((ribbon.scrollWidth - ribbon.getBoundingClientRect().width)/k).toFixed(2);
      /* Wrapping is the failure DS-217 exists to prevent, so ask the box rather than infer it:
         a wrapped ribbon is taller than one of its own items. */
      out.ribbonHeightDu = +(ribbon.getBoundingClientRect().height/k).toFixed(2);
      out.itemHeightDu = items.length
        ? +(items[0].getBoundingClientRect().height/k).toFixed(2) : 0;

      /* the lit mark, which is the idiom the degraded mode reuses */
      var lit = document.querySelector('[data-lit]');
      if (lit) out.litDot = du(lit);

      /* The capacity the deck itself computes, asked of the deck rather than recomputed here -
         a second copy of the rule is what stops the tool measuring what ships (L-08). */
      if (window.htmldeckRulerLayout){
        var lay = window.htmldeckRulerLayout(document.querySelectorAll('.slide').length, out.freeDu);
        out.rulerCapacity = lay.capacity;
        out.rulerDense = !!lay.dense;
        out.rulerTicks = ribbon.children.length;
        /* the rendered pitch, so the deck's declared TICK_PITCH_DU cannot drift from the cell it
           actually draws - the capacity arithmetic is built on the two agreeing */
        var t0 = ribbon.firstElementChild;
        out.rulerPitchDu = t0 ? +(t0.getBoundingClientRect().width/k).toFixed(2) : 0;
        var lbl = document.querySelector('.ruler-label');
        out.rulerLabelDu = lbl ? +(lbl.getBoundingClientRect().width/k).toFixed(2) : 0;
      }
    }
    document.title = 'RESULT' + JSON.stringify(out) + 'ENDRESULT';
    document.documentElement.setAttribute('data-probe-done','');
  }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function(){ setTimeout(run,150); });
  else window.addEventListener('load', run);
})();
</script>
"""


def self_test(wide, floor):
    """L-04: hand-computed checks, so a wrong instrument fails loudly instead of quietly."""
    failures = []
    for name, d in (("1920", wide), ("0.5 floor", floor)):
        if d.get("error"):
            failures.append("%s: %s" % (name, d["error"]))
            continue
        if not d.get("vw"):
            failures.append("%s: viewport reported as %r - not a real browser (L-06)"
                            % (name, d.get("vw")))
        if not d.get("k"):
            failures.append("%s: stage scale --k came back as %r" % (name, d.get("k")))
    if failures:
        return failures

    # The floor run must still be showing the stage. Below 0.5 the deck hands over to the reflow
    # view (DS-071) and hides the stage, so every element measures zero - which is not a small row,
    # it is no row, and it would silently report a free-space bound of zero targets.
    if not floor.get("chrome", {}).get("w"):
        failures.append("the stage is hidden at scale %.4f - DS-071 has handed over to the reflow "
                        "view, so nothing in the chrome row has a size to measure" % floor["k"])
    # The row is --pad-x off each side of a 1920 stage, less the stage's own border. A couple of
    # units off the paper figure is that border; a large drift means the row was re-laid out and
    # every number below is measured against the wrong denominator.
    if abs(wide["chrome"]["w"] - ROW_DU) > 8:
        failures.append("chrome row is %.1f du against a paper figure of %d - that is too far to "
                        "be the stage border, so the row has been re-laid out and T-035's "
                        "arithmetic is stale" % (wide["chrome"]["w"], ROW_DU))
    # T-035 states the controls block holds five elements and prices the ruler against that.
    if len(wide["controlItems"]) != 5:
        failures.append("controls block holds %d element(s), T-035 says five - the row this task "
                        "was specified against has changed"
                        % len(wide["controlItems"]))
    # Design units must not depend on the stage scale. Measuring the same row at two scales and
    # getting two answers would mean the du conversion is wrong, and every bound with it.
    drift = abs(wide["chrome"]["w"] - floor["chrome"]["w"])
    if drift > 2:
        failures.append("the row measures %.1f du at scale %.3f and %.1f du at %.3f - a design "
                        "unit is supposed to be scale-independent, so one of these is wrong"
                        % (wide["chrome"]["w"], wide["k"], floor["chrome"]["w"], floor["k"]))
    # The floor run has to actually be at the floor, or the mark sizes below describe nothing.
    if not (0.45 <= floor["k"] <= 0.62):
        failures.append("the 'floor' run is at scale %.3f, not near the 0.5 hand-over (DS-071) - "
                        "the mark sizes are being reported for the wrong scale" % floor["k"])
    # Blocks must not already overlap, or "free space" is a negative fiction.
    if wide["gapDu"] < 0:
        failures.append("the indicator and the controls already overlap by %.1f du"
                        % -wide["gapDu"])
    # The pitch the deck DECLARES and the cell it DRAWS have to be the same number, because the
    # capacity below is arithmetic on the declared one. They were 48 and 52 on the first build.
    pitch = wide.get("rulerPitchDu")
    if pitch and abs(pitch - DECLARED_PITCH_DU) > 0.6:
        failures.append("the ruler draws a %.1f du cell but the capacity arithmetic assumes %d - "
                        "TICK_PITCH_DU in the deck and the rendered tick have drifted apart"
                        % (pitch, DECLARED_PITCH_DU))
    return failures


def main():
    if render.CHROME is None:
        print("No Chrome or Edge found - this measurement needs a real browser (L-15).")
        return 3
    if not os.path.exists(DECK):
        print("Deck not found: %s" % os.path.relpath(DECK, ROOT))
        return 1

    probe = render.make_probe(DECK, name="chrome-row-probe.html", extra=PROBE)
    url = render.file_url(probe)
    wide, err1 = render.read_result(url, 1920, 1180)
    # 1120x700 is the smallest of the sizes tried that lands ABOVE the 0.5 hand-over: measured,
    # the stage is hidden at k=0.4685 and shown at k=0.5056, so DS-071's threshold behaves exactly
    # as it is written. Going smaller does not measure a smaller stage, it measures no stage.
    floor, err2 = render.read_result(url, 1120, 700)
    if not wide or not floor:
        print("No result from Chrome.\n%s\n%s" % (err1[:400], err2[:400]))
        return 2

    failures = self_test(wide, floor)
    if failures:
        print("SELF-TEST FAILED")
        for f in failures:
            print("  - " + f)
        return 4
    print("self-test ok  (row %.0f du at both scales, five controls, floor run at k=%.3f)"
          % (wide["chrome"]["w"], floor["k"]))

    print("\nTHE CHROME ROW - what the ruler has to fit into")
    print("-" * 74)
    print("  row (.chrome)            %8.1f du   measured; T-035 quotes %d, and the %.0f du "
          "difference is the stage's own border"
          % (wide["chrome"]["w"], ROW_DU, ROW_DU - wide["chrome"]["w"]))
    print("  indicator                %8.1f du   %.1f%% of the row, across %d item(s)"
          % (wide["ribbon"]["w"], wide["ribbonPct"], wide.get("ribbonItems", 0)))
    if wide.get("linkItems"):
        # the ribbon shape: named labels separated by flexible connectors
        print("      %d stage name(s)   %7.1f du total" % (len(wide.get("namedItems", [])),
                                                           wide.get("namedTotal", 0)))
        print("      %d connector(s)    %7.1f du total, each %.1f-%.1f du"
              % (len(wide.get("linkItems", [])), wide.get("linkTotal", 0),
                 wide.get("linkMin", 0), wide.get("linkMax", 0)))
        if wide.get("ribbonOverflowDu", 0) > 1:
            print("      content wants %.1f du more than the box gives it - absorbed by the"
                  % wide["ribbonOverflowDu"])
            print("      connectors, which is why the row still renders cleanly")
    if wide.get("rulerLabelDu"):
        print("  ruler label              %8.1f du   flexible; it takes the slack the ticks leave"
              % wide["rulerLabelDu"])
    if wide.get("itemHeightDu") and wide.get("ribbonHeightDu", 0) > wide["itemHeightDu"] * 1.4:
        print("      WRAPPED - %.1f du tall against a %.1f du item"
              % (wide["ribbonHeightDu"], wide["itemHeightDu"]))
    print("  gap between the blocks   %8.1f du" % wide["gapDu"])
    print("  controls block           %8.1f du" % wide["controls"]["w"])
    for c in wide["controlItems"]:
        print("      %-10s %10.1f du" % (c["id"], c["w"]))
    print("  " + "-" * 44)
    print("  LEFT FOR THE RULER       %8.1f du" % wide["freeDu"])

    fits = int(wide["freeDu"] // TARGET_FLOOR_DU)
    paper = int(ROW_DU // TARGET_FLOOR_DU)
    print("\nTHE TARGET BOUND - DS-168's 48 du floor against what is actually free")
    print("-" * 74)
    print("  on paper, whole row      %8d targets   (%d / %d, ignoring the controls)"
          % (paper, ROW_DU, TARGET_FLOOR_DU))
    print("  T-035 estimated          %8s targets   derived from that, then eyeballed down" % "~30")
    print("  MEASURED, free space     %8d targets   (%.1f / %d, ticks alone)"
          % (fits, wide["freeDu"], TARGET_FLOOR_DU))
    if wide.get("rulerCapacity") is not None:
        print("  AS BUILT, label included %8d targets   the label shares the row, and the deck's"
              % wide["rulerCapacity"])
        print("                                        own htmldeckRulerLayout() says so")
        print("      %d tick(s) drawn, dense mode %s"
              % (wide.get("rulerTicks", 0), "ON" if wide.get("rulerDense") else "off"))
    print("\n  The ruler shares the row, so the whole-row figure was never the bound. What the")
    print("  controls cost had not been measured, and it is %.1f du - %.0f%% of the row."
          % (wide["chrome"]["w"] - wide["freeDu"],
             100.0 * (wide["chrome"]["w"] - wide["freeDu"]) / wide["chrome"]["w"]))

    print("\nTHE MARK FLOOR - rendered size at the 0.5 scale hand-over (DS-071)")
    print("-" * 74)
    print("  measured at k = %.3f, so a design unit is %.3f CSS px here"
          % (floor["k"], floor["k"]))
    if floor.get("litDot"):
        print("  the lit dot that ships   %.1f du  ->  %.2f CSS px"
              % (floor["litDot"]["w"], floor["litDot"]["w"] * floor["k"]))
    for m in MARKS:
        px = m * floor["k"]
        note = "sub-pixel - will alias" if px < 1 else ("exactly one device pixel at 1x"
                                                        if px < 1.5 else "")
        print("  %2d du  ->  %5.2f CSS px   %s" % (m, px, note))
    print("-" * 74)
    print("  Which of these SURVIVES is a question for the eye, not for this tool (L-01).")
    print("  It reports the size; a person looks at the strip and says which is still a mark.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
