#!/usr/bin/env python3
"""Break the content half on purpose, one class at a time, and require the gate to notice.

Third sibling of `deliverable_variants.py` and `contract_variants.py`, same reason and same method.
The reason is the one this project keeps re-learning: **a check that has never been seen to fail is
a claim about the instrument, not about the deck** (**L-36**). The content half is the half with no
prior art in this repository at all, so it gets the same treatment before anyone trusts a green
`FIG-1`.

One variant per acceptance criterion, and the criteria are the task's own words:

- a figure on a slide that appears in **no source**
- a figure that **disagrees with the source it came from**
- the **same figure twice in the deck with different values**

    python tools/deck/content_variants.py

Each variant derives from `examples/reference-deck.html` against `examples/sources/`, so everything
except the seeded break is held constant, and every edit asserts that it matched: a seeding script
that silently no-ops produces a variant proving the opposite of what it claims (**L-04**).

Output goes to `.assets-cache/deck/variants/` (gitignored). Pure standard library (**L-07**).
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths                                                        # noqa: E402
import render                                                        # noqa: E402
import content                                                       # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = render.ROOT
SRC = os.path.join(ROOT, "examples", "reference-deck.html")
SOURCES = os.path.join(ROOT, "examples", "sources")
OUT = os.path.join(render.OUT, "variants")

VARIANTS = [
    ("figure-in-no-source", "FIG-1", [
        # A quantity with a subject no source document mentions. This is the shape the corpus
        # failure actually had: not a wrong number, an *unattributable* one that nobody could
        # trace back and everybody assumed someone had.
        ("<b>Spend the $5.6M grant on bus frequency, and hold",
         "<b>Funded by 47,000 parking permits. Spend the $5.6M grant on bus frequency, and hold")]),

    ("figure-disagrees-with-source", "FIG-2", [
        # The dangerous one. The subject is right, the sentence is right, the number is not - and
        # every presentation check in the gate passes it, because $5.9M is a perfectly good figure.
        ("$5.6M capital, available once. Nineteen days between the vote and the deadline.",
         "$5.9M capital, available once. Nineteen days between the vote and the deadline.")]),

    ("same-figure-two-values", "FIG-3", [
        # One figure, two slides, two values. Restated rather than moved, because restating is how
        # it happens: a number is repeated on the closing slide from memory instead of from the
        # model, and the two slides are never read side by side again.
        ('<p class="provenance">Illustrative model</p>\n</section>\n\n'
         '<!-- ==================================================',
         '<p class="cost-p">The general fund carries $7.2M a year.</p>\n'
         '  <p class="provenance">Illustrative model</p>\n</section>\n\n'
         '<!-- ==================================================')]),
]


def build(name, edits):
    html = open(SRC, "r", encoding="utf-8").read()
    for old, new in edits:
        n = html.count(old)
        if n < 1:
            sys.exit("VARIANT %s: anchor not found\n  %.160s" % (name, old))
        html = html.replace(old, new, 1)
    os.makedirs(OUT, exist_ok=True)
    dest = os.path.join(OUT, name + ".html")
    with open(dest, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html)
    return dest


def self_test():
    """The suite must be able to tell a broken deck from a good one (**L-04**)."""
    if not os.path.exists(SRC):
        sys.exit("SELF-TEST FAILED: no reference deck at %s" % SRC)
    if not os.path.isdir(SOURCES):
        sys.exit("SELF-TEST FAILED: no source set at %s - the content half has nothing to "
                 "reconcile against and would report every figure unsourced" % SOURCES)
    src = open(SRC, "r", encoding="utf-8").read()
    for name, _rule, edits in VARIANTS:
        for old, _new in edits:
            if src.count(old) < 1:
                sys.exit("SELF-TEST FAILED: variant %r no longer matches the deck.\n"
                         "  The deck changed under the suite; fix the variant, do not delete it.\n"
                         "  %.160s" % (name, old))
    _L, rows = content.audit(SRC, SOURCES)
    if not all(ok for _r, _w, ok in rows):
        sys.exit("SELF-TEST FAILED: the UNBROKEN deck already fails the content half - a suite "
                 "cannot show a seeded break was caught if the baseline is red:\n  %s"
                 % "\n  ".join("%s %s" % (r, w) for r, w, ok in rows if not ok))
    return True


def main():
    self_test()
    content.self_test()
    print("source:  %s" % paths.display_path(SRC, ROOT))
    print("sources: %s\n" % paths.display_path(SOURCES, ROOT))
    bad = []
    for name, rule, edits in VARIANTS:
        deck = build(name, edits)
        _L, rows = content.audit(deck, SOURCES)
        caught = {r for r, _w, ok in rows if not ok}
        good = rule in caught
        if not good:
            bad.append((name, rule, caught))
        print("  %-30s breaks %-6s -> %s" % (name, rule, "CAUGHT" if good else "MISSED"))
        for r, what, ok in rows:
            if not ok:
                print("      %-6s %s" % (r, what))

    print("\n%d of %d variants caught." % (len(VARIANTS) - len(bad), len(VARIANTS)))
    if bad:
        print("\nMISSED - the content half does not check what it says it checks:")
        for name, rule, caught in bad:
            print("  %-30s %s not among %s" % (name, rule, sorted(caught)))
        return 1
    print("\nVariants are written to %s and are not committed - the suite regenerates them."
          % paths.display_path(OUT, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
