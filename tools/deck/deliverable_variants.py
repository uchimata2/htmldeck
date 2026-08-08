#!/usr/bin/env python3
"""Break the deliverable and chrome rules on purpose, one at a time, and require the gate to notice.

Sibling of `contract_variants.py`, same reason and same method, different rules: that suite covers
the resolution contract (DS-060..064, DS-071..074, DS-200), this one covers what T-027 added and
T-028 first enforced - DS-202, DS-203, DS-205, DS-216 and DS-217.

**These five rules are exactly the case the project has already been bitten by.** They were written
with `auto` and `render` labels, meaning "a machine decides this", and then nothing decided them:
the reference deck carried a bottom line on none of its twelve slides and three simultaneous
encodings of position while a 43-check gate reported zero failures. A stated check that runs
against nothing is a claim about the instrument, not about the deck (**L-36**).

So each rule gets a deck that violates it, and the run fails if the gate does not object. Two of
the five checks below were themselves wrong when first written and this suite is how that was
found - see T-028 §3.

    python tools/deck/deliverable_variants.py

Each variant derives from `examples/reference-deck.html`, so everything except the seeded break is
held constant, and every edit asserts that it matched: a seeding script that silently no-ops
produces a variant proving the opposite of what it claims (**L-04**).

Output goes to `.assets-cache/deck/variants/` (gitignored). Pure standard library (**L-07**).
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render                                                        # noqa: E402
import audit                                                         # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = render.ROOT
SRC = os.path.join(ROOT, "examples", "reference-deck.html")
OUT = os.path.join(render.OUT, "variants")

# (name, rule it must break, [(old, new), ...])
VARIANTS = [
    ("no-bottom-line", "DS-202", [
        # The state the deck was actually in before T-028, reduced to one slide: the slot is
        # simply absent. This is the variant that matters most, because "absent" is the failure
        # mode a presence check is most likely to mis-handle by measuring nothing and passing.
        ('<p class="bottom-line rise" style="--i:4"><b>Eleven of the 34 minutes are the wait, and '
         'the wait\n    is half the headway.</b></p>\n', "")]),

    ("bottom-line-is-a-paragraph", "DS-202", [
        # DS-202 says one sentence, factual, no reasoning. Reasoning arrives as a second sentence
        # far more often than as a longer one, so sentence count is the cheap proxy the rule needs.
        ("<b>Operating cost decides it: the grant pays for no\n    staff in either column.</b>",
         "<b>Operating cost decides it: the grant pays for no staff in either column. That is why "
         "the frequency package needs the general fund, and why the capital comparison above is "
         "the wrong row to read.</b>")]),

    ("bottom-line-behind-a-disclosure", "DS-205", [
        # DS-205's exact failure: the point of the slide is one click away, so a closed slide does
        # not make it. Moved into the tier-two panel rather than deleted, which is the realistic
        # version - an author tidying a full slide by hiding the thing that matters.
        ('  <p class="bottom-line rise" style="--i:4"><b>A timed connection at Centre removes one '
         'change for\n    North Line and Market Cross riders.</b></p>\n',
         ""),
        ('<div class="row"><span class="k">Bike-share</span><span>Cannot produce this edge. '
         'A dock at Centre still leaves the rider waiting for Route 7.</span></div>',
         '<div class="row"><span class="k">Bike-share</span><span>Cannot produce this edge. '
         'A dock at Centre still leaves the rider waiting for Route 7.</span></div>\n'
         '      <p class="bottom-line"><b>A timed connection at Centre removes one change for '
         'North Line and Market Cross riders.</b></p>')]),

    ("bottom-line-outranked", "DS-203", [
        # Rank, not presence. The bottom line is still there and still says the right thing; the
        # standfirst is simply louder, which is the state every slide in the deck was in before
        # T-028 demoted it. A check that only asks "is it present" scores this a pass.
        ("  font-size:var(--fs-body);color:var(--ink-soft);max-width:var(--measure);",
         "  font-size:calc(52*var(--du));color:var(--ink-soft);max-width:var(--measure);")]),

    ("three-position-encodings", "DS-216", [
        # The deck's own committed state until T-028: ribbon, counter AND a progress bar. Restored
        # verbatim rather than invented, so the variant is a regression test for a real defect.
        # Re-anchored 2026-08-08 when T-035 replaced the ribbon with the ruler. The defect is
        # unchanged and so is the rule it breaks - a progress bar beside the ruler and the counter
        # is a THIRD encoding, and DS-216's amended cap forbids a third however well it is argued.
        # This is the variant that proves the cap is enforced rather than merely written down.
        # ONE anchor, and it is structural. This variant broke twice in a single session while it
        # anchored on a CSS declaration line - first when the ribbon became the ruler, then when
        # the ruler gained `position:relative`. Both times the suite refused to run, which is the
        # designed behaviour and still two interruptions that bought nothing. The stylesheet now
        # travels with the markup, so the only thing that can move is `</nav>`.
        ("</nav>\n",
         '</nav>\n'
         '<style>.progress{position:absolute;left:0;right:0;bottom:0;'
         'height:calc(5*var(--du));background:var(--line)}\n'
         '.progress i{display:block;height:100%;background:var(--accent);width:0}</style>\n'
         '<div class="progress" role="presentation"><i id="bar"></i></div>\n')]),

    ("chrome-over-budget", "DS-217", [
        # Twelve per-slide targets back in the controls row - the exact thing the owner called
        # "extremely noisy", and the reason DS-217 names a number instead of a preference.
        ('<p class="count" id="count" aria-hidden="true"></p>',
         '<p class="count" id="count" aria-hidden="true"></p>\n'
         '    <button class="btn" aria-label="1. Slide">1</button>'
         '<button class="btn" aria-label="2. Slide">2</button>'
         '<button class="btn" aria-label="3. Slide">3</button>'
         '<button class="btn" aria-label="4. Slide">4</button>'
         '<button class="btn" aria-label="5. Slide">5</button>'
         '<button class="btn" aria-label="6. Slide">6</button>'
         '<button class="btn" aria-label="7. Slide">7</button>'
         '<button class="btn" aria-label="8. Slide">8</button>'
         '<button class="btn" aria-label="9. Slide">9</button>')]),

    ("chrome-too-tall", "DS-217", [
        # Height, not item count: the same eleven items stacked into two rows. The chrome that
        # shipped before T-028 failed on exactly this and passed the item count on its own.
        ("  display:flex;align-items:center;gap:var(--sp-4);z-index:8;",
         "  display:grid;grid-template-rows:auto auto;gap:var(--sp-4);z-index:8;")]),
]


def build(name, edits):
    html = open(SRC, "r", encoding="utf-8").read()
    for old, new in edits:
        n = html.count(old)
        if n != 1:
            sys.exit("VARIANT %s: expected 1 occurrence, found %d\n  %.160s" % (name, n, old))
        html = html.replace(old, new)
    os.makedirs(OUT, exist_ok=True)
    dest = os.path.join(OUT, name + ".html")
    with open(dest, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html)
    return dest


def failed_rules(deck):
    data, err = audit.render_data(deck)
    if not data:
        # A variant that will not render is not a caught variant - say so rather than counting a
        # crash as a pass, which is how the dots removal read as "NO RESULT" for a whole run.
        return None, [("PROBE", (err or "")[:120], False)]
    rows = audit.render_verdicts(data)
    return {rule for rule, _what, good in rows if not good}, rows


def self_test():
    """The suite must be able to tell a broken deck from a good one (L-04)."""
    if not os.path.exists(SRC):
        sys.exit("SELF-TEST FAILED: no reference deck at %s" % SRC)
    src = open(SRC, "r", encoding="utf-8").read()
    for name, _rule, edits in VARIANTS:
        for old, _new in edits:
            if src.count(old) != 1:
                sys.exit("SELF-TEST FAILED: variant %r no longer matches the deck.\n"
                         "  The deck changed under the suite; fix the variant, do not delete it.\n"
                         "  %.160s" % (name, old))
    covered = {v[1] for v in VARIANTS}
    for must in ("DS-202", "DS-203", "DS-205", "DS-216", "DS-217"):
        if must not in covered:
            sys.exit("SELF-TEST FAILED: %s is one of the rules this suite exists to keep honest"
                     % must)
    return True


def main():
    self_test()
    render.self_test()
    print("browser: %s" % render.CHROME)
    print("source:  %s\n" % os.path.relpath(SRC, ROOT))
    bad = []
    for name, rule, edits in VARIANTS:
        deck = build(name, edits)
        caught, rows = failed_rules(deck)
        good = caught is not None and rule in caught
        if not good:
            bad.append((name, rule, caught))
        print("  %-32s breaks %-7s -> %s" % (name, rule, "CAUGHT" if good else "MISSED"))
        for r, what, ok_ in rows:
            if not ok_:
                print("      %-8s %s" % (r, what))

    print("\n%d of %d variants caught." % (len(VARIANTS) - len(bad), len(VARIANTS)))
    if bad:
        print("\nMISSED - the gate does not check what it says it checks:")
        for name, rule, caught in bad:
            print("  %-32s %s not among %s" % (name, rule, sorted(caught or [])))
        return 1
    print("\nVariants are written to %s and are not committed - the suite regenerates them."
          % os.path.relpath(OUT, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
