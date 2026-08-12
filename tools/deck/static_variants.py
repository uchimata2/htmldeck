#!/usr/bin/env python3
"""Break the rules T-005 closed, one at a time, and require the gate to notice.

Fourth sibling of `deliverable_variants.py`, `contract_variants.py` and `content_variants.py`, and
the reason has not changed: **a check that has never been seen to fail is a claim about the
instrument, not about the deck** (**L-36**). T-005 took the gate from 44 checked rules to 77, which
is 33 checks nobody had watched fail — and T-038 had just finished proving that a green row can
mean the check cannot fire at all.

Two halves, because they cost different amounts:

- **static** — a string edit and a predicate, no browser. Every one of these runs in milliseconds,
  so there is no reason to sample rather than cover.
- **rendered** — one real Chrome render each, so this half covers the rules where the measurement
  itself was the new thing rather than the threshold.

    python tools/deck/static_variants.py
    python tools/deck/static_variants.py --static-only

Each variant derives from `examples/reference-deck.html`, so everything except the seeded break is
held constant, and every edit asserts that it matched (**L-04**). Pure standard library (**L-07**).
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths                                                        # noqa: E402
import render                                                        # noqa: E402
import audit                                                         # noqa: E402
import contrast                                                      # noqa: E402
import theme                                                         # noqa: E402
import component                                                     # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = render.ROOT
SRC = os.path.join(ROOT, "examples", "reference-deck.html")
OUT = os.path.join(render.OUT, "variants")

# (name, rule it must break, [(old, new), ...]) - the edit is the smallest one that breaks the
# rule and nothing else, because a variant that breaks three rules proves nothing about any of them.
STATIC_VARIANTS = [
    ("cdn-reference", "DS-002", [
        ('<meta charset="utf-8">',
         '<meta charset="utf-8"><link rel="stylesheet" href="https://cdn.example.com/x.css">')]),
    ("script-reads-a-file", "DS-005", [
        ("var DECK = 'Buy frequency before bikes';",
         "var DECK = 'Buy frequency before bikes';\n  fetch('data.json');")]),
    ("colour-outside-the-tokens", "DS-010", [
        (".legend i{width:var(--swatch)",
         ".legend i{background:#C43B2A;width:var(--swatch)")]),
    # ---- added by T-007, which made the theme a region and the token set a contract
    ("type-scale-outside-the-region", "DS-010", [
        # A slide setting its own type size is the defect the composition/look line exists to
        # catch: the geometry around it may be this deck's, the type scale never is.
        (".close-h{font-size:var(--fs-display-lg)", ".close-h{font-size:calc(81*var(--du))")]),
    ("derived-token-pinned-to-a-literal", "DS-013", [
        # The whole point of `derived`: a theme may set the dial, never the step. Pinned, the
        # family silently stops moving with `--type-ratio` and every individual value still
        # looks like a token.
        ("--fs-lead:calc(var(--fs-base)*var(--type-ratio)*var(--du));",
         "--fs-lead:calc(30*var(--du));")]),
    ("two-theme-regions", "DS-011", [
        ('<style id="slides">',
         '<style id="theme">:root{--accent:#1E7A4C}</style>\n<style id="slides">')]),
    ("motion-outside-its-band", "DS-140", [
        # 2.4 s is neither a reveal under DS-141's cap nor inside either long motion's band. It
        # breaks **DS-140**, not DS-141: DS-141 yields to the vocabulary by name (F-04), so the
        # rule that still has something to say is the one that states the band.
        ("--pulse-dur:1.2s;", "--pulse-dur:2.4s;")]),
    ("a-second-accent", "DS-020", [
        ("--accent-wash:#EBE7F5;", "--accent-wash:#EBE7F5;\n  --accent-two:#1E7A4C;")]),
    ("pure-white-ground", "DS-023", [
        ("--paper:#F3F0E8;", "--paper:#FFFFFF;")]),
    ("body-type-off-the-band", "DS-034", [
        # The dial, not the step. Since T-007 `--fs-body` derives from `--fs-base`, so seeding
        # the derived token would break the contract as well as the band and prove neither.
        ("--fs-base:26;", "--fs-base:21;")]),
    ("viewport-unit-decoration", "DS-065", [
        (".legend{display:flex", ".legend{margin-top:2vh;display:flex")]),
    ("hard-coded-svg-colour", "DS-118", [
        ('<line class="axis" x1="150" y1="420" x2="1660" y2="420"/>',
         '<line class="axis" x1="150" y1="420" x2="1660" y2="420" stroke="#8D8572"/>')]),
    ("animation-over-the-cap", "DS-141", [
        ("--slide-dur:420ms;", "--slide-dur:900ms;")]),
    ("styled-bare-b", "DS-045", [
        # The narrow reading, which is the rule as clarified 2026-08-09: a rule on the ELEMENT
        # reaches every `<b>` in the deck, so the deliverable's weight becomes a global default.
        # `.bottom-line b` is deliberately NOT this, and the deck keeps four such selectors.
        # No length in the seeded rule: a `letter-spacing` literal here would break DS-010's
        # region check as well, and a variant that breaks two rules proves nothing about either.
        ("</nav>\n", "</nav>\n<style>b{font-weight:800}</style>\n")]),
    ("hover-only-reveal", "DS-163", [
        (".disc-btn:hover{border-color:var(--accent);color:var(--ink)}",
         ".disc-btn:hover{border-color:var(--accent);color:var(--ink)}\n"
         ".disc:hover .disc-panel{display:block}")]),
    # ---- added by T-069, which stopped excusing *never a dead link*
    ("provenance-link-into-the-authors-disk", "DS-105", [
        # The defect the rule has always named and nothing has ever caught: a link that resolves
        # perfectly on the machine the deck was written on and is dead the moment it is emailed.
        # `file://` is the honest form of it; a relative path is the same defect wearing a shorter
        # string, and the check treats them alike for that reason.
        # *Re-anchored 2026-08-12 by T-103*: a one-source mark is the `.sources--one` shape now,
        # so the link is seeded where a link actually goes - inside the item.
        ('<span class="sources-box" id="src20"><span class="sources-item">Ridership model</span>',
         '<span class="sources-box" id="src20"><span class="sources-item">'
         '<a class="sources-link" href="file:///C:/sources/ridership-model.md">Ridership '
         'model</a></span>')]),
    ("provenance-link-to-a-fragment-that-is-not-there", "DS-105", [
        # The other half, and the one a person cannot see by reading: an in-document anchor whose
        # target was renamed. It looks like a working link and behaves like a dead one.
        # *Re-anchored 2026-08-12 by T-103*, for the reason above.
        ('<span class="sources-box" id="src25"><span class="sources-item">Cost model</span>',
         '<span class="sources-box" id="src25"><span class="sources-item">'
         '<a class="sources-link" href="#src-cost-model">Cost model</a></span>')]),
    # ---- added by T-016, which made the markup a contract
    ("control-with-no-aria-controls", "DS-229", [
        # The defect a generator produces and a person does not: the tenth disclosure looks
        # identical to the other nine and its panel is wired to nothing. Nothing in the render
        # gate sees it either - the panel still opens, because the script pairs them by DOM
        # position, and only a reader on a screen reader loses the association.
        ('<button class="disc-btn" aria-expanded="false" aria-controls="p11">',
         '<button class="disc-btn" aria-expanded="false">')]),
    ("panel-outside-its-disclosure", "DS-229", [
        # The place half. The panel is still in the slide and still styled, so it renders where it
        # always did; what it has stopped being is part of a component.
        ('<div class="disc" data-disc="instances">\n    <button class="disc-btn" '
         'aria-expanded="false" aria-controls="p10">',
         '<div class="disc" data-disc="instances"></div>\n  <div>\n    <button class="disc-btn" '
         'aria-expanded="false" aria-controls="p10">')]),
    ("component-nobody-contracted", "DS-229", [
        # A shared component added the way components are actually added - by writing a rule in
        # the shared block. The contract cannot know about it, which is the whole point: the row
        # is what makes it emittable, and the gate is what makes the row get written.
        (".icon{width:var(--icon)", ".callout{color:var(--accent)}\n.icon{width:var(--icon)")]),
    ("motion-that-stopped-reading-its-token", "DS-229", [
        # **The half `theme.py`'s literal scan cannot state, and the seed has to avoid writing a
        # literal or it proves the wrong thing.** Turn reads the slide transition's dials instead
        # of its own: every token is still declared, still inside its band, and there is no literal
        # anywhere for the scan to find. What has gone is the tokenisation itself - a theme moving
        # Turn now moves everything except the disclosure mark.
        (".disc-mark::after{width:var(--disc-mark-stroke);height:var(--disc-mark-bar);\n"
         "  transition:transform var(--turn-dur) var(--turn-ease)}",
         ".disc-mark::after{width:var(--disc-mark-stroke);height:var(--disc-mark-bar);\n"
         "  transition:transform var(--slide-dur) var(--slide-ease)}")]),
    ("easing-curve-in-a-component", "DS-010", [
        # §5's line, and the one the scan could not see until T-016: a curve is a choice about how
        # a motion FEELS, so a component writing one has taken a decision the theme owns.
        #
        # **It seeds a NEW transition rather than rewriting a tokenised one**, and that is the
        # point rather than convenience: rewriting an existing motion would also drop the token
        # its contract row names, so DS-229 would fail as well and the variant would prove nothing
        # about either rule. The duration is a token here for the same reason - a literal would be
        # caught by the length half of the same scan.
        (".legend{display:flex;gap:var(--sp-3);align-items:center}",
         ".legend{display:flex;gap:var(--sp-3);align-items:center;"
         "transition:opacity var(--scale-dur) cubic-bezier(.34,1.56,.64,1)}")]),
    # ---- added by T-016 step 4, which made the editorial split a rule
    ("a-fifth-editorial-kind", "DS-229", [
        # DS-230's vocabulary is closed, and `appendix` is the exact value the closure exists to
        # refuse - the name a generator reaches for when the content did not fit anywhere else.
        # The markup is otherwise untouched: the panel opens, reads and closes as it always did,
        # which is why nothing but the contract can see this.
        ('<div class="disc" data-disc="condition">\n    <button class="disc-btn" '
         'aria-expanded="false" aria-controls="p8">',
         '<div class="disc" data-disc="appendix">\n    <button class="disc-btn" '
         'aria-expanded="false" aria-controls="p8">')]),
    ("marker-defined-in-another-slide", "DS-232", [
        # **The defect that shipped four blank arrowheads** (T-104). The reference deck defines a
        # marker per slide, correctly; this points one slide's arrow at another slide's marker.
        # Nothing else moves - the connector is still directional, still labelled, still meets its
        # target - and it draws no arrowhead anywhere but the slide holding the definition.
        ("url(#ar4)", "url(#ar9)")]),
    ("bottom-line-supported-only-behind-the-click", "DS-231", [
        # **The failure a generator writes and a reader meets closed.** The deliverable is rewritten
        # to quote the gate's 26%, which lives in the panel and nowhere on the slide - so the slide
        # asserts a figure it does not show, and looks entirely fine until someone asks where the
        # number came from. The face is untouched, so no other row moves.
        ("<b>Nothing before month 18 is irreversible, and the\n"
         "    $1.5M reserve buys 16 Old Quarter stations if the gate fails.</b>",
         "<b>The gate clears at 26%, so nothing before month 18 is irreversible.</b>")]),
]

# One render each. These are the rules where T-005 added the MEASUREMENT and not just a threshold,
# so a string edit alone would prove nothing about whether the probe can see the defect.
# The one-source provenance mark, written once: two anchors below quote it (T-103).
MARK21 = ('<p class="provenance"><span class="sources sources--one"><svg class="sources-mark" aria-hidden="true"><use href="#i-source"/></svg><span class="sources-box" id="src21"><span class="sources-item">Ridership model</span></span></span></p>')

RENDER_VARIANTS = [
    ("slide-is-not-a-section", "DS-080", [
        ('<section class="slide" data-name="Waiting is the trip"',
         '<div class="slide" data-name="Waiting is the trip"'),
        # **The closing tag, which this variant left behind until T-055.** Without it the document
        # is malformed, Chrome repairs it, and what the run measures is the repair rather than the
        # rule - the same variant failed DS-091, DS-130 and DS-075 as collateral, reporting a slide
        # with no headline whose headline the parser had lifted out of it. The anchor is the
        # slide's own bottom line: `</section>` is not unique and neither is the provenance mark
        # above it.
        # *Re-anchored 2026-08-12 by T-103*: the mark this anchors past is the one-source
        # shape now. Still the slide's own bottom line plus its mark, for the reason above.
        ('is half the headway.</b></p>\n  ' + MARK21 + '\n</section>',
         'is half the headway.</b></p>\n  ' + MARK21 + '\n</div>')]),
    ("sentence-over-twenty-words", "DS-092", [
        ("<b>Spend the $5.6M grant on bus frequency, and hold",
         "<b>Spend the whole of the $5.6M state corridor grant on bus frequency across the six "
         "trunk routes, and hold")]),
    ("icon-nobody-uses", "DS-113", [
        ('<symbol id="i-ask"',
         '<symbol id="i-unused" viewBox="0 0 24 24"><path d="M4 4h16v16H4z"/></symbol>\n '
         '<symbol id="i-ask"')]),
    ("a-third-tier", "DS-160", [
        ('<div class="disc-panel" id="p2" hidden>',
         '<div class="disc-panel" id="p2" hidden><button class="disc-btn" '
         'aria-expanded="false">More still</button>')]),
    ("mark-too-pale-to-clear-the-ground", "DS-219", [
        # **The half the old blanket ban never looked at.** The mark is washed out until it fails
        # 1.4.11 against the paper, and the label is darkened so it still reads perfectly well on
        # it - so DS-215 passes, the slide looks fine in a screenshot, and the chart's bars have
        # stopped being distinguishable from the page. Only DS-219 has anything to say about it.
        ("</nav>\n",
         "</nav>\n<style>svg.fig rect.accent{fill:#EBE7F5}\n"
         "svg.fig text.t-paper{fill:#23211D}</style>\n")]),
    ("slide-with-no-headline", "DS-091", [
        # The class is what carries the rule's subject, so dropping it is how one slide loses its
        # headline without losing its text - which is the shape that used to pass. Until T-053 the
        # word-count check ran over an empty set and reported 0 headlines over six words.
        ('<h2 class="headline rise" style="--i:1">The window shuts in March</h2>',
         '<h2 class="was-headline rise" style="--i:1">The window shuts in March</h2>')]),
    ("chevron-with-no-label", "DS-164", [
        ('<button class="disc-btn" aria-expanded="false" aria-controls="p2">',
         '<button class="disc-btn" aria-expanded="false" aria-controls="p2"><i></i></button>'
         '<button class="disc-btn" aria-expanded="false" hidden aria-controls="p2x">')]),
]


# One render each, with `prefers-reduced-motion` forced. Separate from RENDER_VARIANTS because the
# measurement is a different render, not a different threshold - and because a check nobody has
# watched fail is a claim about the instrument (**L-36**), which is exactly what DS-143 was while
# it sat excused.
REDUCED_VARIANTS = [
    ("reduced-motion-leaves-the-slide-blank", "DS-143", [
        # **The failure the second clause exists to see.** Stopping the animation is not enough:
        # `.rise` holds opacity 0 until it plays, so a deck that only sets `animation:none` shows
        # the reader an empty slide and reports motion dutifully disabled. Same shape as DS-224
        # on paper.
        #
        # **Both paths have to be seeded, and finding that out is what this variant was for.**
        # The deck disables motion twice over: an `@media (prefers-reduced-motion:reduce)` block
        # that applies at parse time, and `:root[data-motion="off"]`, which the script sets from
        # `matchMedia` on load. Seeding only the media query changed nothing measurable - the
        # attribute rules carry higher specificity and put the opacity back. A variant that
        # breaks one of two redundant paths proves the check cannot see the OTHER path.
        (":root[data-motion=\"off\"] .opening{animation:none;opacity:1;transform:none}",
         ":root[data-motion=\"off\"] .opening{animation:none}"),
        (".rise,.pulse,.opening{animation:none;opacity:1;transform:none}",
         ".rise,.pulse,.opening{animation:none}")]),
    ("reduced-motion-solidifies-the-flow", "DS-143", [
        # The semantics half. The arrows stop moving AND stop being dashed, so the diagram no
        # longer says *flow* - motion removed, and meaning with it.
        (".current{animation:none}",
         ".current{animation:none;stroke-dasharray:none}")]),
]


def build(name, edits):
    html = open(SRC, "r", encoding="utf-8").read()
    for old, new in edits:
        if html.count(old) < 1:
            sys.exit("VARIANT %s: anchor not found\n  %.160s" % (name, old))
        html = html.replace(old, new, 1)
    os.makedirs(OUT, exist_ok=True)
    dest = os.path.join(OUT, name + ".html")
    with open(dest, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html)
    return dest


def static_failures(path):
    html = open(path, "r", encoding="utf-8").read()
    # `fetch_verdicts` joined the list when T-093 moved DS-005 out of `STATIC`, and this suite is
    # what noticed: the variant that seeds a file read reported MISSED the moment the rule left the
    # static list, because the producer it moved to was not being run here. A gate's static half is
    # whatever `check.py` gathers without a browser, not whatever happens to be in one table.
    rows = ([(r, w, bool(fn(html))) for r, w, fn in audit.STATIC]
            + audit.split_verdicts(html) + audit.provenance_verdicts(html)
            + audit.marker_verdicts(html)
            + audit.fetch_verdicts(html)
            + contrast.verdicts(html) + theme.verdicts(html) + component.verdicts(html))
    return {r for r, _w, ok in rows if not ok}, rows


def render_failures(path):
    data, err = render.read_result(
        render.file_url(render.make_probe(path, name="variant.html", extra=audit.PROBE)),
        1622, 1054)
    if not data:
        return None, [("PROBE", (err or "")[:120], False)]
    rows = audit.render_verdicts(data)
    # `is False`: a row reporting `None` decided nothing, and counting that as a catch would let a
    # variant look caught because the seed removed the rule's subject rather than broke it (T-051).
    return {r for r, _w, ok in rows if ok is False}, rows


def reduced_failures(path):
    """The same shape as `render_failures`, from the reduced-motion render."""
    data, err = audit.reduced_motion_data(path)
    if not data:
        return None, [("PROBE", (err or "")[:120], False)]
    rows = audit.reduced_verdicts(data)
    return {r for r, _w, ok in rows if ok is False}, rows


def self_test():
    """The suite must be able to tell a broken deck from a good one (**L-04**), and the baseline
    must be green or a caught variant proves nothing."""
    if not os.path.exists(SRC):
        sys.exit("SELF-TEST FAILED: no reference deck at %s" % SRC)
    src = open(SRC, "r", encoding="utf-8").read()
    for name, _rule, edits in STATIC_VARIANTS + RENDER_VARIANTS + REDUCED_VARIANTS:
        for old, _new in edits:
            if src.count(old) < 1:
                sys.exit("SELF-TEST FAILED: variant %r no longer matches the deck.\n"
                         "  The deck changed under the suite; fix the variant, do not delete it.\n"
                         "  %.160s" % (name, old))
    base, _rows = static_failures(SRC)
    if base:
        sys.exit("SELF-TEST FAILED: the UNBROKEN deck already fails %s - a seeded break cannot be "
                 "shown caught against a red baseline" % sorted(base))
    return True


def run(variants, failures_of, label):
    bad = []
    for name, rule, edits in variants:
        deck = build(name, edits)
        caught, rows = failures_of(deck)
        good = caught is not None and rule in caught
        if not good:
            bad.append((name, rule, caught))
        print("  %-28s breaks %-7s -> %s" % (name, rule, "CAUGHT" if good else "MISSED"))
        for r, what, ok in rows:
            if ok is not True:
                print("      %-8s %-58s %s"
                      % (r, what[:58], "NO SUBJECT" if ok is None else "FAIL"))
    print("  %d of %d %s variants caught.\n" % (len(variants) - len(bad), len(variants), label))
    return bad


def main(argv):
    self_test()
    print("source:  %s\n" % paths.display_path(SRC, ROOT))
    print("=== static (no browser)")
    bad = run(STATIC_VARIANTS, static_failures, "static")
    if "--static-only" not in argv:
        render.self_test()
        print("=== rendered (one real Chrome render each)")
        bad += run(RENDER_VARIANTS, render_failures, "rendered")
        print("=== rendered with prefers-reduced-motion forced")
        bad += run(REDUCED_VARIANTS, reduced_failures, "reduced-motion")
    if bad:
        print("MISSED - the gate does not check what it says it checks:")
        for name, rule, caught in bad:
            print("  %-28s %s not among %s" % (name, rule, sorted(caught or [])))
        return 1
    print("Variants are written to %s and are not committed - the suite regenerates them."
          % paths.display_path(OUT, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
