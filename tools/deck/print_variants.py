#!/usr/bin/env python3
"""Build the two print-rendering variants T-018 measures, from one deck.

The task's owner ruled that the printable mode is decided by printed evidence rather than by
assertion, so the same twelve-slide deck is emitted twice with different `@media print` rules:

    paginated   the STAGE printed one slide per page. Slides are absolutely stacked and scaled by
                a transform on screen; print undoes both, sizes the page to the slide, and breaks
                after each. Tier-two disclosure panels stay hidden - they are absolutely
                positioned overlays, and unhiding them onto a fixed 1920x1080 box overlaps the
                content it explains. That loss is a measurement, not an oversight.
    reflow      the READING view printed as a continuous document. `buildDoc()` already clones
                every slide and opens every disclosure panel (DS-073), so tier two travels into
                this rendering by construction. This is what the deck does today.

Both are written to `.assets-cache/print/`, gitignored, because they are artefacts: the repository
keeps the script and the numbers, never the output (R6's rule).

Neither variant is proposed for the reference deck. Which stylesheet - if either - lands there for
good is T-021's and T-028's business.

Pure standard library, by L-07. Writes LF (L-11) and UTF-8 (L-10).

    python tools/deck/print_variants.py
"""

import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DECK = os.path.join(ROOT, "examples", "reference-deck.html")
OUT = os.path.join(ROOT, ".assets-cache", "print")

# The block already in the deck. Both variants replace it, so neither run inherits half of it.
EXISTING = re.compile(
    r"/\* printing is a mode the user forces on.*?\n@media print\{.*?\n\}\n",
    re.S)


PAGINATED = """/* T-018 variant: PAGINATED STAGE - one slide per printed page. */
@media print{
  /* The page is sized to the slide rather than the slide to the page. A4 would letterbox a
     16:9 stage and leave the print dialog to scale it anyway; this way the dialog's "fit to
     page" does the only scaling, and it does it to a page of the right shape. */
  @page{ size:1920px 1080px; margin:0 }

  html,body{background:#fff;overflow:visible;height:auto}
  .viewswitch,.chrome,.progress,.controls{display:none!important}
  .doc{display:none!important}

  /* THE RULE THIS RENDERING LIVES OR DIES BY, and the one whose absence printed blank pages twice.
     The deck switches itself to the reading view below 960px and sets `viewport.hidden` when it
     does - and PRINTING IS WHAT MAKES IT SWITCH, because printing changes the layout viewport.
     `.viewport[hidden]{display:none}` then hides the stage, and overriding `position` does not
     touch `display`. So the stage was never in the output at all: the first run hid the reading
     view too and printed nothing; the second left the reading view visible and printed THAT,
     which looked like a fix and was not.
     Forcing `display` on both the element and its [hidden] state is what makes this rendering
     print the stage regardless of which view the deck has decided it is in. */
  .viewport,.viewport[hidden]{display:block!important;
            position:static!important;inset:auto!important;overflow:visible!important;
            height:auto!important;background:#fff!important}
  .stage{
    position:static!important;transform:none!important;
    width:1920px!important;height:auto!important;
    border:0!important;box-shadow:none!important;overflow:visible!important;
  }

  /* Slides are absolutely stacked with only [data-current] visible. Un-stack them, make every
     one visible, and give each its own page. */
  /* `relative`, not `static`. A slide is the containing block for its own absolutely positioned
     descendants - the disclosure panels and the provenance line - and making it static hands them
     to the page instead, which scatters them across breaks. Relative keeps it in normal flow AND
     keeps it a containing block. */
  .slide{
    position:relative!important;
    width:1920px!important;height:1080px!important;
    opacity:1!important;visibility:visible!important;
    transition:none!important;
    break-after:page;break-inside:avoid;
  }
  /* :last-child does not match - the stage ends with the nav and the progress bar, not with a
     slide - so the twelfth slide kept its page break and produced a thirteenth, empty page. */
  section.slide:last-of-type{break-after:auto}

  /* Entrance animations hold their pre-animation state until played, so an unplayed slide
     prints blank or half-risen. */
  .rise{opacity:1!important;transform:none!important;animation:none!important}

  /* Backgrounds and rules are most of this design; without this they print as white. */
  *{print-color-adjust:exact!important;-webkit-print-color-adjust:exact!important}
}
"""


REFLOW = """/* T-018 variant: REFLOW DOCUMENT - the reading view, printed as continuous prose. */
@media print{
  /* Margin only, and deliberately NO `size` descriptor. Pinning `size:A4 portrait` here did work,
     but it also greyed out the print dialog's orientation control - the reader could not choose
     landscape even though this rendering reads perfectly well in it. A print stylesheet that
     dictates paper takes a decision away from the person holding the printer. */
  @page{ margin:14mm }

  html,body{background:#fff;overflow:visible;height:auto}
  .viewport,.viewswitch,.chrome,.progress,.controls{display:none!important}

  /* buildDoc() has already run and has already opened every disclosure panel (DS-073), so tier
     two is in this rendering whether or not the reader ever switched views. */
  .doc{display:block!important;height:auto!important;overflow:visible!important}
  .doc-inner{max-width:none;padding:0}

  /* `break-inside:avoid` on the SECTION is what produced half-empty pages: a section is a slide's
     worth of content, often most of a page tall, so any section that will not fit is pushed whole
     to the next one and leaves the remainder blank. Measured on a 22-page export where nine pages
     carried a third of the text of their neighbours.
     Sections are therefore allowed to break. Only the things that are unreadable when split -
     a figure, a table, a disclosure panel - are kept whole, and headings are tied to what follows
     so a break cannot orphan one at the foot of a page. */
  .doc section{padding:1.2rem 0}
  .doc .eyebrow,.doc .headline{break-after:avoid}
  .doc .standfirst,.doc .disc-lead{break-before:avoid}
  .doc .figwrap,.doc .fig,.doc table,.doc .disc-panel,
  .doc .stat,.doc .ledger,.doc .cost-aside{break-inside:avoid}
  .doc p,.doc li{orphans:3;widows:3}

  .rise{opacity:1!important;transform:none!important;animation:none!important}
  *{print-color-adjust:exact!important;-webkit-print-color-adjust:exact!important}
}
"""


def decls(css):
    """The declarations only, with comments removed.

    Both of the checks below name the defect they guard against, so the phrase they look for also
    appears in the comment explaining why it is absent. Reading the commented source would fail on
    its own documentation - which it did, the first time this ran."""
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S).replace(" ", "")


def self_test(source):
    """L-04: worked out by hand first - if the anchor has moved, both variants are built on sand."""
    failures = []

    hits = EXISTING.findall(source)
    if len(hits) != 1:
        failures.append("expected exactly 1 existing @media print block, found %d - the deck has "
                        "changed and the replacement anchor is wrong" % len(hits))
    if ".doc section{break-inside:avoid}" not in source:
        failures.append("the deck's current print block is not the one this script was written "
                        "against")

    # Both variants must survive substitution intact, and must differ. A copy-paste that left
    # them identical would produce two files and one measurement.
    if PAGINATED == REFLOW:
        failures.append("the two variants are identical")
    for name, css in (("paginated", PAGINATED), ("reflow", REFLOW)):
        if "@media print" not in css:
            failures.append("%s variant has no @media print block" % name)
        if css.count("{") != css.count("}"):
            failures.append("%s variant has unbalanced braces (%d open, %d close)"
                            % (name, css.count("{"), css.count("}")))

    # The distinguishing rule of each. If these ever coincide the two runs stop being a comparison.
    if "break-after:page" not in PAGINATED:
        failures.append("paginated variant does not break after each slide")
    if "break-after:page" in REFLOW:
        failures.append("reflow variant paginates - it is meant to be continuous")
    # The regression that cost this task a run: hiding `.doc` with `!important` blanks the whole
    # printed output in Chrome and Edge. Measured on the real thing, then reproduced headlessly.
    # It reads like a harmless tidy-up, which is exactly why it needs a check rather than a memory.
    # The regression that cost this task two runs. The deck hides the stage itself when it decides
    # it is in the reading view, and printing is what makes it decide that. Overriding `position`
    # does not touch `display`, so the stage silently never reached the page.
    if "[hidden]{display:block!important" not in decls(PAGINATED):
        failures.append("paginated variant does not force .viewport[hidden] back to display:block "
                        "- the deck hides the stage when print narrows the viewport, and this "
                        "rendering then prints nothing, or prints the reading view instead")
    if ".doc{display:none!important}" not in decls(PAGINATED):
        failures.append("paginated variant does not hide the reading view - with the stage forced "
                        "visible both would print, one after the other")
    # A slide is the containing block for its own absolutely positioned descendants.
    if "position:relative!important" not in decls(PAGINATED):
        failures.append("paginated variant un-positions the slide, which hands its disclosure "
                        "panels and provenance line to the page and scatters them across breaks")
    if ".docsection{break-inside:avoid" in decls(REFLOW):
        failures.append("reflow variant keeps whole sections unbreakable - a section is most of a "
                        "page, so any that will not fit is pushed whole and leaves the rest blank")
    if ":last-child{break-after:auto}" in decls(REFLOW) + decls(PAGINATED):
        failures.append("break-after is being suppressed with :last-child, which does not match - "
                        "the stage ends with the nav, so the last slide keeps its break and emits "
                        "an empty final page. Use section.slide:last-of-type")
    if re.search(r"@page\{[^}]*size:", decls(REFLOW)):
        failures.append("reflow variant pins @page size, which greys out the dialog's orientation "
                        "control and takes the choice away from the reader")

    if failures:
        print("SELF-TEST FAILED")
        for f in failures:
            print("  - " + f)
        return False
    print("self-test ok  (anchor found once, variants differ, braces balanced, break rules right)")
    return True


def build():
    if not os.path.exists(DECK):
        print("Deck not found: %s" % os.path.relpath(DECK, ROOT))
        return 1
    with open(DECK, encoding="utf-8") as fh:
        source = fh.read()

    if not self_test(source):
        return 2

    os.makedirs(OUT, exist_ok=True)
    written = []
    for name, css in (("paginated", PAGINATED), ("reflow", REFLOW)):
        variant = EXISTING.sub(lambda _m, c=css: c, source, count=1)
        path = os.path.join(OUT, "reference-deck-%s.html" % name)
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(variant)
        written.append((name, path, os.path.getsize(path), len(css.encode("utf-8"))))

    base = os.path.getsize(DECK)
    print("\nPRINT VARIANTS BUILT - %s" % os.path.relpath(OUT, ROOT))
    print("-" * 72)
    print("  %-28s %9.1f KB   (deck as committed)" % ("reference-deck.html", base / 1024.0))
    for name, path, size, csslen in written:
        print("  %-28s %9.1f KB   print CSS %5d B   delta %+.1f KB"
              % (os.path.basename(path), size / 1024.0, csslen, (size - base) / 1024.0))
    print("-" * 72)
    print("  The delta is the size cost of the print stylesheet, measured not estimated.")
    print("\n  Do NOT open these in any preview pane (L-15). Open each by double-clicking it,")
    print("  print to a file through the browser's own dialog, and look at the result.")
    return 0


if __name__ == "__main__":
    sys.exit(build())
