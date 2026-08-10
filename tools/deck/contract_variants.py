#!/usr/bin/env python3
"""Break the resolution contract on purpose, one rule at a time, and require the gate to notice.

**A check that has only ever passed is not evidence that it checks anything.** `contract.py` went
green on the reference deck the first time it ran every rule but one, which is exactly the state a
check has when it is silently measuring nothing - and this project has already shipped a tolerance
that was cited, sourced and covering zero values (**L-36**). So each rule gets a deck that violates
it, and the run fails if the gate does not object.

The one that was never seeded is the one that matters most: **DS-071 was caught on a real
divergence**, not a synthetic one. The deck's auto-engage was width-based while the rule had become
scale-based, the check failed on 1280 x 400 before anything here existed, and the fix turned it
green. That is recorded in T-021 §3; the variant below reproduces it so it stays covered.

    python tools/deck/contract_variants.py

Each variant derives from `examples/reference-deck.html` so everything except the seeded break is
held constant, and every edit asserts that it matched - a seeding script that silently no-ops
produces a variant that proves the opposite of what it claims (**L-04**, and seed_defects.py's
reason for the same rule).

Output goes to `.assets-cache/deck/variants/` (gitignored). Pure standard library (**L-07**).
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths                                                        # noqa: E402
import render                                                        # noqa: E402
import contract                                                      # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = render.ROOT
SRC = os.path.join(ROOT, "examples", "reference-deck.html")
OUT = os.path.join(render.OUT, "variants")

# (name, rule it must break, which pass to run, [(old, new), ...])
#
# `pass` is "sweep" for the rules four viewports decide, "scale" for the two that need the
# two-resolution comparison. Running only the pass a variant can affect keeps the suite at a few
# minutes instead of half an hour.
VARIANTS = [
    ("non-uniform-scale", "DS-062", "sweep", [
        # scaleX/scaleY instead of scale(): the stage stretches to the window instead of
        # letterboxing, which is the failure DS-062 exists for and the one that makes a deck
        # "look fine on my monitor".
        ("transform:translate(-50%,-50%) scale(var(--k,1));",
         "transform:translate(-50%,-50%) scaleX(calc(var(--k,1)*1.15)) scaleY(var(--k,1));")]),

    ("stage-not-centred", "DS-200", "sweep", [
        # DS-200's own text: centring that does not survive the transform positions the UNSCALED
        # 1920x1080 box, so the scaled stage lands off-centre and clips at the far edge. The rule
        # says the bug is invisible at full size; reintroduce exactly it.
        ("  position:absolute;left:50%;top:50%;\n"
         "  width:calc(1920*var(--du));height:calc(1080*var(--du));",
         "  position:absolute;left:0;top:0;\n"
         "  width:calc(1920*var(--du));height:calc(1080*var(--du));"),
        ("transform:translate(-50%,-50%) scale(var(--k,1));",
         "transform:scale(var(--k,1));")]),

    ("width-keyed-reflow", "DS-071", "sweep", [
        # The real defect this task found, kept as a regression: a width test cannot see a short
        # wide window, so 1280 x 400 stays on a stage scaled to 0.37.
        ("var k = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);\n"
         "    if (!isFinite(k) || k <= 0) return;\n"
         "    if (k < 0.5 && !inDoc) setView(true);\n"
         "    if (k >= 0.5 && inDoc) setView(false);",
         "var narrow = window.matchMedia('(max-width: 959px)').matches;\n"
         "    if (narrow && !inDoc) setView(true);\n"
         "    if (!narrow && inDoc) setView(false);")]),

    ("no-fullscreen-guard", "DS-072", "sweep", [
        ("    if (document.fullscreenElement) return;\n", "")]),

    ("reading-view-in-px", "DS-074", "sweep", [
        # Type that ignores the user's font size. WCAG 1.4.4 is the criterion; a reading view
        # that does this is not a conforming alternate version, it just looks like one.
        # The anchors read the deck's tokens since T-007 made the reading view derive from them;
        # the seeded break is unchanged, and it is still the point - a `px` here is a `px`
        # however it got there.
        (".doc-head .t{font-family:var(--font-display);font-size:var(--doc-fs-title)",
         ".doc-head .t{font-family:var(--font-display);font-size:38px"),
        (".doc .headline{font-size:var(--doc-fs-head)", ".doc .headline{font-size:30px"),
        (".doc .standfirst{font-size:var(--doc-fs)", ".doc .standfirst{font-size:17px"),
        (".doc-inner{max-width:var(--doc-measure)", ".doc-inner{max-width:736px")]),

    ("viewport-units-in-stage", "DS-063", "scale", [
        # A length that does not ride the transform. At 3840x2000 and 1280x634 `vw` resolves to
        # different design-unit values, so the two renderings stop being the same stage - the
        # "broken on my monitor" class, in one declaration. DS-033 bans this statically too;
        # here it is the non-text geometry probe that has to see it.
        (".fig{width:100%;height:100%}", ".fig{width:calc(100% - 4vw);height:100%}")]),

    ("body-type-under-the-floor", "DS-064", "scale", [
        # 20 design units renders at 13.3 CSS px in a 720p share. Legible on the presenter's
        # monitor, gone in the stream - the failure the whole stage arithmetic exists to prevent.
        # Both roles the body probe can land on, so the variant does not depend on which slide
        # the sample happens to hit.
        # Since T-007 both roles derive from `--fs-base`, so **one** edit moves both and the
        # variant no longer has to seed each. That is the token layer doing its job, and it is
        # why the second anchor went rather than being repaired.
        ("--fs-base:26;", "--fs-base:20;")]),

    ("body-prose-under-a-foreign-class", "DS-064", "scale", [
        # **The deck an outside project built, in the one respect that mattered** (T-075). Its
        # supporting prose was conformant and classed with names of its own, and DS-064's probe
        # looked for `.standfirst, .cost-p, .title-note` - two of which are this deck's composition
        # and appear in no contract. So the rule reported `no body run measured` and FAILED a deck
        # measuring 17.3 px against a 16 px floor, with no remedy but to adopt a class name no
        # document states.
        #
        # Nothing here is illegal: `.body` still holds the prose, the prose is still a paragraph,
        # and it is still set at `--fs-body`. The only change is the name. **This is the one
        # variant that must make its rule PASS** - a seeded defect would be caught by the broken
        # probe as readily as by the fixed one, and would prove nothing.
        ('class="standfirst rise"', 'class="lede rise"', 11),
        (".standfirst{", ".lede{", 2),
        ('class="title-note"', 'class="note-run"', 1),
        (".title-note{max-width:calc(1100*var(--du));color:var(--ink-soft);font-size:var(--fs-small)",
         ".note-run{max-width:calc(1100*var(--du));color:var(--ink-soft);font-size:var(--fs-body)",
         1)]),
]

# Variants whose rule must PASS rather than fail, with the reason. Named here rather than as a
# fifth tuple field so that the default stays explicit: everything not in this set is a seeded
# defect the gate has to catch, which is what the suite is for.
MUST_PASS = {
    "body-prose-under-a-foreign-class":
        "a conforming deck under class names no contract states. Before T-075 the probe found no "
        "body run and DS-064 failed it; a variant that expected a failure would have passed "
        "against the defect it exists to catch",
}


def build(name, edits):
    html = open(SRC, "r", encoding="utf-8").read()
    for edit in edits:
        # A third element declares how many occurrences the edit expects. **Declared, never
        # defaulted to "all"**: a rename that silently hit a different number of elements than the
        # variant's author believed would make the variant test something nobody wrote down.
        old, new, want = edit if len(edit) == 3 else (edit[0], edit[1], 1)
        n = html.count(old)
        if n != want:
            sys.exit("VARIANT %s: expected %d occurrence(s), found %d\n  %.140s"
                     % (name, want, n, old))
        html = html.replace(old, new)
    os.makedirs(OUT, exist_ok=True)
    dest = os.path.join(OUT, name + ".html")
    with open(dest, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html)
    return dest


def failed_rules(deck, which_pass):
    if which_pass == "sweep":
        rows = contract.verdicts(contract.sweep(deck, quiet=True))
    else:
        # The default sample, not one slide. A single slide missed the `vw` variant outright,
        # because the slide it happened to pick carries no figure - the probe measured nothing
        # and reported a pass (**L-36**, again, inside the suite written to prevent it).
        rows = contract.scale_verdicts(deck)
    # `good is False`, not `not good`: an undecided row is `None` and reporting it as caught would
    # let a variant claim a gate found a defect the gate declined to judge (T-065's third state,
    # reaching this suite in T-075).
    return {rule for rule, _what, good in rows if good is False}, rows


def self_test():
    """The suite must be able to distinguish a broken deck from a good one (L-04)."""
    if not os.path.exists(SRC):
        sys.exit("SELF-TEST FAILED: no reference deck at %s" % SRC)
    src = open(SRC, "r", encoding="utf-8").read()
    for name, _rule, _p, edits in VARIANTS:
        for edit in edits:
            old, want = edit[0], (edit[2] if len(edit) == 3 else 1)
            if src.count(old) != want:
                sys.exit("SELF-TEST FAILED: variant %r no longer matches the deck.\n"
                         "  The deck changed under the suite; fix the variant, do not delete it.\n"
                         "  wanted %d occurrence(s), found %d\n  %.140s"
                         % (name, want, src.count(old), old))
    covered = {v[1] for v in VARIANTS}
    if "DS-071" not in covered:
        sys.exit("SELF-TEST FAILED: DS-071 is the rule this suite exists to keep honest")
    names = {v[0] for v in VARIANTS}
    orphan = sorted(MUST_PASS) if not (set(MUST_PASS) <= names) else []
    if orphan:
        sys.exit("SELF-TEST FAILED: MUST_PASS names %s and no variant is called that - the "
                 "expectation outlived the variant it was written for" % ", ".join(orphan))
    return True


def main():
    self_test()
    render.self_test()
    contract.self_test()
    print("browser: %s" % render.CHROME)
    print("source:  %s\n" % paths.display_path(SRC, ROOT))
    bad = []
    for name, rule, which_pass, edits in VARIANTS:
        deck = build(name, edits)
        caught, rows = failed_rules(deck, which_pass)
        must_pass = name in MUST_PASS
        # A must-pass variant is not satisfied by the rule merely staying off the failure list: an
        # undecided row is off it too, and `no body run measured` is exactly what this is testing
        # for. The row has to have been decided, and decided in the deck's favour.
        decided = [ok for r, _w, ok in rows if r == rule and ok is not None]
        good = (bool(decided) and all(decided)) if must_pass else rule in caught
        if not good:
            bad.append((name, rule, caught))
        print("  %-34s %s %-7s -> %s"
              % (name, "keeps  " if must_pass else "breaks ", rule,
                 ("PASSED" if good else "WRONGLY REPORTED") if must_pass
                 else ("CAUGHT" if good else "MISSED")))
        for r, what, ok_ in rows:
            if ok_ is not True:
                print("      %-8s %-6s %s" % (r, "FAIL" if ok_ is False else "undec", what))
    print("\n%d of %d variants behaved as specified." % (len(VARIANTS) - len(bad), len(VARIANTS)))
    for name, rule, caught in bad:
        print("  WRONG   %-34s expected %s %s, gate reported %s"
              % (name, rule, "to pass" if name in MUST_PASS else "to fail",
                 ", ".join(sorted(caught)) or "no failure at all"))
    print("\nVariants are written to %s and are not committed - the suite regenerates them."
          % paths.display_path(OUT, ROOT))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
