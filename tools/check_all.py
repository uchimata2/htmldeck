#!/usr/bin/env python3
"""Every checker in this repository, run in one command, with a stated reason for each one it skips.

    python tools/check_all.py            # the partition, and the verdict
    python tools/check_all.py --list     # the manifest, without running anything
    python tools/check_all.py --verbose  # let every child write to the console

**This exists because `docs/PUBLISHING.md` §8's gate list was an enumeration, and said so.** It was
written on 2026-08-10 after four releases had each re-derived the sequence from the last one's
commits, and **it had already missed three red checks the day it was written** (T-083, T-084, and a
stale shell on `examples/sort-window/`). Writing the list down did not stop it being a list: `0.2.1`
was cut on 2026-08-11 by running sixteen commands by hand and reading sixteen exit codes, which is
the same failure mode one step slower. That section's own excusal names this file as what closes it.

**The partition is the point, not the convenience.** Every tool under `tools/` ends the run in
exactly one of **ran**, **skipped with a reason**, or **failed** - the account `check.py` keeps over
rules and `figures.py` over fences, one altitude up, over checkers. A tool in none of the three is
`UNCLASSIFIED` and **fails the run**.

**What stops this being another list** is that the manifest below is checked against the filesystem
in both directions, against what `git ls-files` says a clone receives:

  - a tracked `tools/**/*.py` that no entry names is `UNCLASSIFIED`;
  - an entry naming a file that is gone is `STALE`.

Both fail, and **both directions are needed** - the first catches the tool nobody wired, the second
the entry nobody deleted, and a list that catches one of them is trusted for catching neither
(**L-74**). *Is this file a checker?* has no mechanical answer, which is why the answer is written
down at all: every script here has a `__main__`, and the four that break rules on purpose look
exactly like the one the release runs. **L-08** says derive a fact rather than store it; where it
cannot be derived, this is what makes the stored copy fail loudly instead of quietly.

**It does not stop at the first failure, and that is the opposite of `tools/tasks/lint.py`.** That
tool chains three checks and stops, because a task edit that fails the first check has nothing to
learn from the third. Here the whole set is the deliverable: a release run needs every verdict, not
the first red one, or the next run finds the second defect after fixing the first.

Runs from anywhere: the project root is derived from this file, not from the working directory.
Pure standard library (**L-07**), plus `git`, which decides what a clone receives.
"""

import os
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable


# --- the manifest ---------------------------------------------------------------------------
#
# Four tables, and between them they name every tracked `tools/**/*.py` exactly once. Adding a
# tool and wiring nothing goes red; deleting one an entry names goes red.

# Repository-wide gates: `path -> argv tail`. Run once, in this order.
WIDE = [
    ("tools/tasks/lint.py", []),
    ("tools/docs/lessons.py", []),
    ("tools/docs/figures.py", []),
    ("tools/deck/ruleset.py", ["--counts"]),
    ("tools/plugin/check_scaffold.py", []),
    ("tools/deck/static_variants.py", []),
    ("tools/deck/deliverable_variants.py", []),
    ("tools/deck/contract_variants.py", []),
    ("tools/deck/content_variants.py", []),
    ("tools/examples/seed_defects.py", ["--check"]),
    ("tools/deck/contents_bound.py", []),
]

# Per-deck gates: `path -> builder`. The builder takes `(deck, sources)` - both repo-relative -
# and returns the argv tail, or a string, which is a refusal with its reason.
PER_DECK = [
    ("tools/deck/shell.py", lambda deck, src: ["check", deck]),
    ("tools/deck/component.py", lambda deck, src: ["check", deck]),
    ("tools/deck/theme.py", lambda deck, src: ["check", deck]),
    ("tools/deck/check.py", lambda deck, src: [deck, "--sources", src, "--print-pages"]),
    ("tools/deck/spec.py", lambda deck, src: _spec_args(deck)),
]

# A per-deck gate that does not apply to one deck, and why. `(tool, deck) -> reason`.
DECK_EXEMPT = {
    ("tools/deck/spec.py", "examples/reference-deck.html"):
        "PERMANENT. That deck was built by hand before the specification pair existed, so there is "
        "no .foundation.md to hand it. T-087 rejected retrofitting one on 2026-08-11: it would make "
        "a hand-built deck claim to be a build-mode output. The argument is docs/PUBLISHING.md "
        "section 8; this is not a deck awaiting a pair",
}

# Every other tracked tool, with what it is. A checker whose checks are wholly reached by a gate
# above says which gate; anything else says what it is instead of a checker.
NOT_RUN = {
    "tools/docs/refcheck.py":
        "runs inside tools/tasks/lint.py, the first gate, which is where its exit code is read",
    "tools/tasks/query.py":
        "a question, not a check. It asks the tracker what to work on next and what one task "
        "points at, so a session pays 1,901 bytes instead of reading the 33,676-byte board "
        "(CE-02, T-131). It has no verdict to give: every answer it can return is a correct one. "
        "The locator it shares with lint.py is asserted in that file's self-test, which is the "
        "first gate above",

    "tools/deck/audit.py":
        "runs inside tools/deck/check.py, which imports it - the whole auto gate and the "
        "measurable half of the render gate",
    "tools/deck/contrast.py":
        "runs inside tools/deck/check.py, which imports it",
    "tools/deck/contract.py":
        "runs inside tools/deck/check.py, which imports it",
    "tools/deck/content.py":
        "runs inside tools/deck/check.py under --sources, which is why that argument is declared "
        "per deck in DECKS rather than guessed",
    "tools/deck/printpages.py":
        "runs inside tools/deck/check.py under --print-pages, which the per-deck line above passes "
        "- the old gate list never did, so DS-222's page count was checked by nothing. Its own "
        "entry point now derives the slide count from the deck instead of defaulting to a hardcoded "
        "12 and agrees with that caller on both shipped decks (T-120), so running it here would "
        "print the same verdict from a second Chrome launch",
    "tools/deck/printgeom.py":
        "runs inside tools/deck/check.py under the same --print-pages the per-deck line above "
        "passes. It is the printed GEOMETRY - no two contents cards intersect, no card reaches the "
        "footnote - which is the one fault class no screen measurement reaches and which shipped in "
        "three decks with every gate green (T-123, T-116, **L-76**). Its own entry point takes any "
        "deck it is pointed at, which is what an adopter runs; here it would be a second Chrome "
        "print of a verdict check.py already has",

    "tools/deck/critique.py":
        "the review mode, not a gate. It assembles the half of a critique a program can assemble "
        "so a reviewer can spend on the half it cannot; its output is prose for a person",
    "tools/deck/paths.py":
        "a library - one function that formats a path for display on any drive. Its main is a "
        "self-test, not a check of anything in the repository",
    "tools/deck/render.py":
        "an instrument, not a gate. It renders a deck in real Chrome offline and reports what came "
        "out; the gates that need a render call it",
    "tools/deck/preflight.py":
        "a builder. It writes the capability preflight into a deck; shell.py check gates the result",
    "tools/deck/quickview.py":
        "a builder. It carries a source document into a deck so a provenance mark can be opened",
    "tools/deck/print_variants.py":
        "a builder. It emits the two print variants T-018 measures, for a person to print and look "
        "at - CLAUDE.md rule 5 keeps printing optional and rule 6 keeps the looking manual",
    "tools/deck/chrome_row.py":
        "a measurement for T-035, taken once against a real browser. It answers whether the ruler "
        "fits the chrome row; it has no pass or fail to report on a shipped deck",

    "tools/assets/measure.py":
        "a research instrument for T-013 - what one embeddable asset costs inside one HTML file",
    "tools/assets/build_probe_deck.py":
        "a research instrument for T-013 - it builds a probe deck to weigh, not a deck this "
        "repository ships",
    "tools/assets/chart_probe.py":
        "a research instrument for T-006 - it generates the four chart types as hand-computed SVG "
        "to settle whether a charting library is needed",
    "tools/portability/build_probes.py":
        "a research instrument for T-017 - it builds the file:// probe pages",
    "tools/portability/run_probes.py":
        "a research instrument for T-017 - it runs those probes in a real browser and collects "
        "what they report",
    "tools/kb/extract.py":
        "extracts the deck corpus into .kb/, which .gitignore excludes because it holds client and "
        "personal data. There is nothing here for it to read and nothing it produces may publish",

    "tools/check_all.py":
        "this file. Its own self-test runs first, on every invocation",
}

# The decks this repository ships, and the one argument that cannot be guessed from a deck's path.
# **Guessing it wrong does not error** - check.py reports `FIG-0 ... source files this reader cannot
# open` and fails, which reads exactly like a defect in the deck. So it is declared, and a deck with
# no declaration is refused rather than run against a guess.
DECKS = {
    "examples/reference-deck.html": "examples/sources",
    "examples/sort-window/sort-window.html": "examples/sort-window/sources",
}

# Tracked `.html` that is not a deck, and what it is.
NOT_A_DECK = {
    "examples/reference-deck-seeded-defects.html":
        "the blindness fixture. It carries one known defect per evaluation dimension on purpose, "
        "at score 0, so the rubric's answer can be graded against a known answer. Its gate is "
        "seed_defects.py --check, which proves it is still derived from the reference deck rather "
        "than edited",
    "shell/shell.html":
        "the shared shell, not a deck. It is the half of a deck that cannot be authored per run; "
        "shell.py check compares a deck against it",
}


def _spec_args(deck):
    """`spec.py`'s three arguments, or a refusal. The pair sits beside the deck under its slug."""
    stem = deck[:-len(".html")]
    foundation, slides = stem + ".foundation.md", stem + ".slides.md"
    missing = [p for p in (foundation, slides) if not os.path.exists(os.path.join(ROOT, p))]
    if missing:
        return ("the specification pair is missing (%s) and no exemption in DECK_EXEMPT says why. "
                "A deck built by this plugin has one; declare the exemption or produce the pair"
                % ", ".join(missing))
    return [foundation, slides, deck]


# --- discovery ------------------------------------------------------------------------------

def tracked(pattern):
    """Every tracked path matching `pattern` - what a fresh clone receives, and nothing else.

    `git` rather than a walk, for the same reason `refcheck.py` reads `.gitignore`: `control/`,
    `dist/` and `.kb/` are machine-local by design, and a checker discovered there would be a
    checker no adopter has.
    """
    try:
        out = subprocess.run(["git", "ls-files", "--", pattern], cwd=ROOT,
                             capture_output=True, text=True)
    except OSError:
        sys.exit("git is not on PATH, so this cannot tell a tracked tool from a local scratch "
                 "file - and that distinction is the whole discovery rule. Install git, or run "
                 "the gates named in docs/PUBLISHING.md section 8 separately.")
    if out.returncode:
        sys.exit("git ls-files failed (exit %d): %s" % (out.returncode, out.stderr.strip()))
    return sorted(p.strip() for p in out.stdout.splitlines() if p.strip())


def classify(tools, wide, per_deck, not_run):
    """`(classified, unclassified, stale)` over the tool set.

    `classified` maps a path to `"gate"`, `"per-deck gate"` or `"not run"`. `unclassified` is every
    tracked tool no table names - the state that fails the run, because it is what a new checker
    nobody wired looks like. `stale` is the mirror: an entry naming a file that is gone.
    """
    named = {}
    for path, _ in wide:
        named[path] = "gate"
    for path, _ in per_deck:
        named[path] = "per-deck gate"
    for path in not_run:
        named[path] = "not run"
    have = set(tools)
    classified = {p: k for p, k in named.items() if p in have}
    return (classified,
            sorted(have - set(named)),
            sorted(set(named) - have))


# --- running --------------------------------------------------------------------------------

class Result(object):
    """One row of the report: a command that ran, was skipped, or failed."""

    def __init__(self, label, state, code=None, output="", why=""):
        self.label, self.state, self.code, self.output, self.why = label, state, code, output, why


def run_one(path, argv_tail, verbose):
    """Run one checker and return its `Result`.

    Output is captured rather than inherited, and printed only for a failure. Sixteen tools each
    printing their full account is thousands of lines, and a wall of green is where the three red
    checks of 2026-08-10 hid. `--verbose` restores the inherited stream when the account itself is
    what you came for.
    """
    label = "python %s%s" % (path, "".join(" " + a for a in argv_tail))
    argv = [PY, path] + list(argv_tail)
    if verbose:
        print("\n=== %s" % label)
        sys.stdout.flush()
        code = subprocess.run(argv, cwd=ROOT).returncode
        return Result(label, "ran" if code == 0 else "failed", code)
    done = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True,
                          errors="replace")
    out = (done.stdout or "") + (done.stderr or "")
    return Result(label, "ran" if done.returncode == 0 else "failed", done.returncode, out)


def plan(decks):
    """Every command this run will issue, in order, as `(section, path, argv-tail-or-reason)`."""
    steps = [("repository-wide", path, tail) for path, tail in WIDE]
    for deck in decks:
        src = DECKS[deck]
        for path, builder in PER_DECK:
            exempt = DECK_EXEMPT.get((path, deck))
            steps.append((deck, path, exempt if exempt else builder(deck, src)))
    return steps


# --- the report -----------------------------------------------------------------------------

def field(name, value, note=""):
    return "    %-14s %4s%s" % (name, value, "   = " + note if note else "")


def wrap(text, indent):
    """Fold `text` to 96 columns at `indent` spaces. The reasons are sentences, not labels."""
    words, lines, line = text.split(), [], ""
    for w in words:
        if line and len(line) + 1 + len(w) > 96 - indent:
            lines.append(line)
            line = w
        else:
            line = (line + " " + w) if line else w
    if line:
        lines.append(line)
        return ("\n" + " " * indent).join(lines)
    return ""


def report(results, classified, unclassified, stale, tools, decks, not_a_deck):
    print("Every checker under tools/ - %d tool(s), %d deck(s)\n" % (len(tools), len(decks)))

    section = None
    for sect, res in results:
        if sect != section:
            section = sect
            print("\n  %s" % ("gates" if sect == "repository-wide" else "per deck - " + sect))
        mark = {"ran": "pass", "failed": "FAIL", "skipped": "skip"}[res.state]
        print("    %-4s %s" % (mark, res.label))
        if res.why:
            print("         %s" % wrap(res.why, 9))

    print("\n  not run, and what each one is instead")
    for path in sorted(NOT_RUN):
        if path in classified:
            print("    %s" % path)
            print("        %s" % wrap(NOT_RUN[path], 8))

    print("\n  tracked .html that is not a deck")
    for path in sorted(not_a_deck):
        print("    %s" % path)
        print("        %s" % wrap(not_a_deck[path], 8))

    ran = sum(1 for _, r in results if r.state == "ran")
    failed = sum(1 for _, r in results if r.state == "failed")
    skipped = sum(1 for _, r in results if r.state == "skipped")

    print("\n  commands")
    print(field("ran", ran))
    print(field("skipped", skipped, "each with its reason printed above"))
    print(field("FAILED", failed, "a checker that ran and said no"))
    print(field("total", ran + skipped + failed, "so the account is a partition"))

    print("\n  the tools those commands come from")
    kinds = {}
    for kind in classified.values():
        kinds[kind] = kinds.get(kind, 0) + 1
    print(field("gate", kinds.get("gate", 0)))
    print(field("per-deck gate", kinds.get("per-deck gate", 0)))
    print(field("not run", kinds.get("not run", 0), "each with what it is instead"))
    print(field("UNCLASSIFIED", len(unclassified),
                "a tracked tool no table names, which fails the run"))
    print(field("STALE", len(stale), "an entry naming a file that is gone, which fails the run"))
    print(field("total", len(tools), "every tracked tools/**/*.py, so the account is a partition"))

    for path in unclassified:
        print("\n  UNCLASSIFIED  %s" % path)
        print("        %s" % wrap("Nothing says whether this is a checker. Add it to WIDE or "
                                  "PER_DECK if it is one, or to NOT_RUN with what it is instead. "
                                  "This is the state a new checker nobody wired is in, and it is "
                                  "why this command is not a list.", 8))
    for path in stale:
        print("\n  STALE         %s" % path)
        print("        %s" % wrap("An entry names this and the file is not tracked. Delete the "
                                  "entry, or restore the file.", 8))

    return failed, len(unclassified), len(stale)


def failures(results):
    """Print the captured output of every failure, after the report, in run order."""
    for sect, res in results:
        if res.state == "failed" and res.output:
            print("\n" + "=" * 96)
            print("FAILED (exit %d): %s" % (res.code, res.label))
            print("=" * 96)
            print(res.output.rstrip())


# --- the self-test --------------------------------------------------------------------------

def self_test():
    """**A partition that has never been seen to fail is a claim about the instrument** (**L-04**,
    **L-36**). Three states have to be asserted rather than read: an unwired tool, a stale entry,
    and a deck with no declared `--sources`."""
    wide = [("tools/a.py", [])]
    per_deck = [("tools/b.py", lambda deck, src: [deck])]
    not_run = {"tools/c.py": "a library"}

    ok, un, stale = classify(["tools/a.py", "tools/b.py", "tools/c.py"], wide, per_deck, not_run)
    if (un, stale) != ([], []):
        sys.exit("SELF-TEST FAILED: a fully wired tool set reported %r unclassified and %r stale, "
                 "so a green run here would mean nothing" % (un, stale))

    _, un, _ = classify(["tools/a.py", "tools/b.py", "tools/c.py", "tools/new_check.py"],
                        wide, per_deck, not_run)
    if un != ["tools/new_check.py"]:
        sys.exit("SELF-TEST FAILED: a tool no table names reported %r, wanted "
                 "['tools/new_check.py']. An unwired checker passing is the exact failure this "
                 "command was written to stop" % (un,))

    _, _, stale = classify(["tools/a.py", "tools/b.py"], wide, per_deck, not_run)
    if stale != ["tools/c.py"]:
        sys.exit("SELF-TEST FAILED: an entry naming a deleted file reported %r, wanted "
                 "['tools/c.py'] - the hand-kept list going stale silently" % (stale,))

    if "examples/reference-deck.html" not in DECKS:
        sys.exit("SELF-TEST FAILED: no --sources declared for the reference deck. Guessing it "
                 "wrong does not error, it reports a content failure that reads like a defect in "
                 "the deck")
    return True


# --- entry point ----------------------------------------------------------------------------

def main(argv):
    verbose = "--verbose" in argv
    listing = "--list" in argv
    self_test()

    tools = tracked("tools/*.py") + tracked("tools/**/*.py")
    tools = sorted(set(tools))
    html = tracked("*.html")

    classified, unclassified, stale = classify(tools, WIDE, PER_DECK, NOT_RUN)

    undeclared = [h for h in html if h not in DECKS and h not in NOT_A_DECK]
    gone = [d for d in list(DECKS) + list(NOT_A_DECK) if d not in html]
    if undeclared or gone:
        for h in undeclared:
            print("UNDECLARED .html  %s" % h)
            print("        %s" % wrap("Nothing says whether this is a deck this repository ships. "
                                      "Add it to DECKS with the --sources directory it needs, or "
                                      "to NOT_A_DECK with what it is. A deck run against a guessed "
                                      "--sources fails in a way that reads like a defect in the "
                                      "deck.", 8))
        for h in gone:
            print("STALE .html       %s  - declared and not tracked" % h)
        return 2

    decks = [d for d in html if d in DECKS]

    steps = plan(decks)
    if listing:
        for sect, path, tail in steps:
            if isinstance(tail, str):
                print("skip  %-14s python %s" % (sect if sect != "repository-wide" else "", path))
                print("      %s" % wrap(tail, 6))
            else:
                print("run   python %s%s" % (path, "".join(" " + a for a in tail)))
        # The partition is reported here too, and fails here too. `--list` is what someone runs
        # after adding a tool, and a listing that stayed green while the tool was unclassified
        # would be the silent-staleness this command exists to end.
        print("\n%d tool(s): %d unclassified, %d stale"
              % (len(tools), len(unclassified), len(stale)))
        for path in unclassified:
            print("  UNCLASSIFIED  %s" % path)
        for path in stale:
            print("  STALE         %s" % path)
        return 1 if unclassified or stale else 0

    results = []
    for sect, path, tail in steps:
        if isinstance(tail, str):
            label = "python %s <%s>" % (path, sect)
            results.append((sect, Result(label, "skipped", why=tail)))
            continue
        if not verbose:
            print("  %s ..." % path, end="\r")
            sys.stdout.flush()
        results.append((sect, run_one(path, tail, verbose)))

    if not verbose:
        print(" " * 78, end="\r")
    print()
    failed, un, st = report(results, classified, unclassified, stale, tools, decks, NOT_A_DECK)
    failures(results)

    print("\n%d failure(s), %d unclassified, %d stale" % (failed, un, st))
    if failed or un or st:
        print("\nThis is step 1 of docs/PUBLISHING.md section 8, and it is red. Nothing after it "
              "runs until it is green.")
        return 1
    print("\n**A green run here is the whole gate set, and it is still not a good deck.** Every "
          "one of these\nvalidates structure, references or a stated rule. None can tell you a "
          "specification is wrong, a\nplan is thin, or a deck reads as machine-written - and the "
          "rules a person asserts by looking are\nnamed, with reasons, in check.py's own account "
          "(L-05, CLAUDE.md rule 6).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
