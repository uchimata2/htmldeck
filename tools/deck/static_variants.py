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
import render                                                        # noqa: E402
import audit                                                         # noqa: E402
import contrast                                                      # noqa: E402

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
        (".legend i{width:calc(14*var(--du))",
         ".legend i{background:#C43B2A;width:calc(14*var(--du))")]),
    ("a-second-accent", "DS-020", [
        ("--accent-wash:#EBE7F5;", "--accent-wash:#EBE7F5;\n  --accent-two:#1E7A4C;")]),
    ("pure-white-ground", "DS-023", [
        ("--paper:#F3F0E8;", "--paper:#FFFFFF;")]),
    ("body-type-off-the-band", "DS-034", [
        ("--fs-body:calc(26*var(--du));", "--fs-body:calc(21*var(--du));")]),
    ("viewport-unit-decoration", "DS-065", [
        (".legend{display:flex", ".legend{margin-top:2vh;display:flex")]),
    ("hard-coded-svg-colour", "DS-118", [
        ('<line class="axis" x1="150" y1="420" x2="1660" y2="420"/>',
         '<line class="axis" x1="150" y1="420" x2="1660" y2="420" stroke="#8D8572"/>')]),
    ("animation-over-the-cap", "DS-141", [
        ("--slide-dur:420ms;", "--slide-dur:900ms;")]),
    ("hover-only-reveal", "DS-163", [
        (".disc-btn:hover{border-color:var(--accent);color:var(--ink)}",
         ".disc-btn:hover{border-color:var(--accent);color:var(--ink)}\n"
         ".disc:hover .disc-panel{display:block}")]),
]

# One render each. These are the rules where T-005 added the MEASUREMENT and not just a threshold,
# so a string edit alone would prove nothing about whether the probe can see the defect.
RENDER_VARIANTS = [
    ("slide-is-not-a-section", "DS-080", [
        ('<section class="slide" data-name="Waiting is the trip"',
         '<div class="slide" data-name="Waiting is the trip"')]),
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
    ("chevron-with-no-label", "DS-164", [
        ('<button class="disc-btn" aria-expanded="false" aria-controls="p2">',
         '<button class="disc-btn" aria-expanded="false" aria-controls="p2"><i></i></button>'
         '<button class="disc-btn" aria-expanded="false" hidden aria-controls="p2x">')]),
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
    rows = [(r, w, bool(fn(html))) for r, w, fn in audit.STATIC] + contrast.verdicts(html)
    return {r for r, _w, ok in rows if not ok}, rows


def render_failures(path):
    data, err = render.read_result(
        render.file_url(render.make_probe(path, name="variant.html", extra=audit.PROBE)),
        1622, 1054)
    if not data:
        return None, [("PROBE", (err or "")[:120], False)]
    rows = audit.render_verdicts(data)
    return {r for r, _w, ok in rows if not ok}, rows


def self_test():
    """The suite must be able to tell a broken deck from a good one (**L-04**), and the baseline
    must be green or a caught variant proves nothing."""
    if not os.path.exists(SRC):
        sys.exit("SELF-TEST FAILED: no reference deck at %s" % SRC)
    src = open(SRC, "r", encoding="utf-8").read()
    for name, _rule, edits in STATIC_VARIANTS + RENDER_VARIANTS:
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
            if not ok:
                print("      %-8s %s" % (r, what))
    print("  %d of %d %s variants caught.\n" % (len(variants) - len(bad), len(variants), label))
    return bad


def main(argv):
    self_test()
    print("source:  %s\n" % os.path.relpath(SRC, ROOT))
    print("=== static (no browser)")
    bad = run(STATIC_VARIANTS, static_failures, "static")
    if "--static-only" not in argv:
        render.self_test()
        print("=== rendered (one real Chrome render each)")
        bad += run(RENDER_VARIANTS, render_failures, "rendered")
    if bad:
        print("MISSED - the gate does not check what it says it checks:")
        for name, rule, caught in bad:
            print("  %-28s %s not among %s" % (name, rule, sorted(caught or [])))
        return 1
    print("Variants are written to %s and are not committed - the suite regenerates them."
          % os.path.relpath(OUT, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
