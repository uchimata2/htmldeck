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

import io
import os
import re
import subprocess
import sys
import time

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
    ("tools/docs/screening.py", []),
    ("tools/deck/ruleset.py", ["--counts"]),
    ("tools/plugin/check_scaffold.py", []),
    ("tools/deck/static_variants.py", []),
    ("tools/deck/deliverable_variants.py", []),
    ("tools/deck/contract_variants.py", []),
    ("tools/deck/content_variants.py", []),
    ("tools/examples/seed_defects.py", ["--check"]),
    ("tools/examples/portfolio_charts.py", ["selftest"]),
    ("tools/deck/contents_bound.py", []),
    ("tools/deck/slidefacts.py", ["--self-test"]),
    ("tools/deck/readability.py", ["--self-test"]),
]

# Per-theme gates: `path -> builder`, the builder taking the theme's repo-relative path.
#
# **The themes are discovered, never listed** (T-228). `theme.py check <deck>` was in PER_DECK from
# the start and asks whether a DECK declares what it uses; nothing asked whether a THEME declares
# what the contract requires, so `themes/lattice.css` sat fifteen tokens behind for as long as it
# took anyone to run `validate` by hand - every one of them a token that arrived after the file did.
# A hand-kept list would have gone stale at exactly the same moment, which is why this globs.
PER_THEME = [
    ("tools/deck/theme.py", lambda theme: ["validate", theme]),
]


def themes_tracked():
    """Every tracked theme, discovered.

    **A theme is a `.css` directly in `themes/`; anything deeper is a resource a theme uses.**
    `themes/faces/` holds the three embedded font faces, which have no contract to validate
    against and would fail on every token in it.

    The depth filter is explicit because `tracked()` takes a **git pathspec**, not a shell glob,
    and `themes/*.css` matches across directories there - it returned the three faces, and the
    self-test below is what said so rather than a failing run three steps later.
    """
    return [t for t in tracked("themes/*.css") if t.count("/") == 1]

# Per-deck gates: `path -> builder`. The builder takes `(deck, sources)` - both repo-relative -
# and returns the argv tail, or a string, which is a refusal with its reason.
PER_DECK = [
    ("tools/deck/shell.py", lambda deck, src: ["check", deck]),
    ("tools/deck/component.py", lambda deck, src: ["check", deck]),
    ("tools/deck/theme.py", lambda deck, src: ["check", deck]),
    ("tools/deck/check.py", lambda deck, src: [deck, "--sources", src, "--print-pages"]),
    ("tools/deck/spec.py", lambda deck, src: _spec_args(deck)),
    ("tools/deck/quickview.py", lambda deck, src: _quickview_args(deck, src)),
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
    "tools/deck/density.py":
        "runs inside tools/deck/check.py, the per-deck gate, which is where its exit code is read. "
        "Its verdicts() is DS-239's row and kind_verdicts() carries DS-237 and DS-238. Runnable "
        "alone, and then it prints the rank of every content motion in the deck rather than one "
        "verdict: python tools/deck/density.py list <deck>",
    "tools/deck/figgrid.py":
        "runs inside tools/deck/check.py, the per-deck gate, which is where its exit code is read. "
        "Its verdicts() is DS-236's row and check.py gathers it on every deck. It was a "
        "measurement rather than a checker until 2026-08-19, because every deck this repository "
        "shipped failed the rule it measures - 18 of 21 diagrams - and T-184 re-cut those first, "
        "which is what made gating it honest. Still runnable alone, and then it prints the offset "
        "per diagram rather than one verdict: python tools/deck/figgrid.py <deck>",
    "tools/deck/glitchfree.py":
        "runs inside tools/deck/check.py, the per-deck gate, which is where its exit code "
        "is read. Its verdicts() are GF-2 to GF-8 - R6 section 8's conditions 2 to 8, the "
        "decomposition of CLAUDE.md rule 2 - and check.py gathers all seven on every deck. "
        "Condition 1 is DS-001 and condition 9 is a person, which check.py's closing text "
        "names rather than this table. Still runnable alone, and then it prints all seven "
        "rows per deck with the counts behind them rather than one verdict: python "
        "tools/deck/glitchfree.py <deck>",
    "tools/deck/markhits.py":
        "runs inside tools/deck/check.py, the per-deck gate, which is where its exit code is read. "
        "Its verdicts() is DS-244's row and check.py gathers it on every deck. Half of what it "
        "measures gates and half reports: a label over another label fails a deck, and a label set "
        "on a line does not, because across these four decks that fires 16 times for one real "
        "defect and the two are geometrically identical (T-204). Still runnable alone, and then it "
        "prints every collision and every placement rather than one verdict: python "
        "tools/deck/markhits.py <deck>",
    "tools/docs/refcheck.py":
        "runs inside tools/tasks/lint.py, the first gate, which is where its exit code is read",
    "tools/docs/findings.py":
        "runs inside tools/tasks/lint.py, the first gate, as --check. The drift it catches - a "
        "finding whose row and whose task disagree - is created at a task closure, and lint.py is "
        "what a closure runs. Catching it here instead would report it at the next release, which "
        "is days after the edit that caused it. Its listing mode is a question, not a check: it "
        "answers which finding is which task in 1,317 bytes against the 325,695 the same answer "
        "cost by hand (T-151)",
    "tools/docs/cycles.py":
        "the pre-release audit's coverage partition, and deliberately not a gate here. It fails "
        "when a tracked file belongs to no audit cycle - which is a defect in T-219's coverage, not "
        "in the release - and docs/AUDIT-METHOD.md section 1 says no audit is a release step. "
        "Wiring it in would block a release over a document that had not been assigned a reader. "
        "Its failing half rides on the command a cycle already runs: python tools/docs/cycles.py "
        "--cycle <n> answers which files that cycle reads, and reports the whole partition's "
        "verdict before it answers. Cycle 42 decides whether it outlives the audit",
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
    "tools/deck/presenter.py":
        "a derivation, not a gate. It writes <slug>-presenter.html beside a deck - the same deck "
        "plus the speaker notes its specification authors - and that artifact FAILS DS-088 by "
        "design, which is T-211 section 3's safety property rather than a defect. It decides "
        "nothing about the deck it reads and never modifies it. Run it by hand: python "
        "tools/deck/presenter.py <deck> <slug>.slides.md",
    "tools/deck/fps.py":
        "an instrument a PERSON runs, and the only one here that cannot be automated at all. "
        "Headless produces no frames, so a frame rate cannot be measured by anything in this file "
        "(T-185, L-26); it prepares a deck and a real browser window supplies the frames. It "
        "decides nothing and fails no deck - a frame-rate threshold would be a claim about hardware "
        "this project has no corpus for (L-05). Run it by hand: python tools/deck/fps.py <deck>",
    "tools/deck/preflight.py":
        "a builder. It writes the capability preflight into a deck; shell.py check gates the result",
    "tools/deck/print_variants.py":
        "a builder. It emits the two print variants T-018 measures, for a person to print and look "
        "at - CLAUDE.md rule 5 keeps printing optional and rule 6 keeps the looking manual",
    "tools/deck/chrome_row.py":
        "a measurement for T-035, taken once against a real browser. It answers whether the ruler "
        "fits the chrome row; it has no pass or fail to report on a shipped deck",
    "tools/deck/longdeck.py":
        "a fixture builder for T-178 - it splices a deck to any slide count so a long-deck question "
        "can be asked twice. It produces a deck to look at, and decides nothing about one",
    "tools/deck/rulerstrip.py":
        "an instrument for T-178. It renders candidate treatments for the dense-mode position mark "
        "side by side, for a person to choose between; which one reads best is the judgement it "
        "exists to put in front of the eye rather than to make",

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
    "examples/measure-first/measure-first.html": "examples/measure-first/sources",
    "examples/portfolio-review/portfolio-review.html": "examples/portfolio-review/sources",
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


def _quickview_args(deck, sources):
    """`quickview.py check`'s arguments, or a refusal. T-181.

    **The tool takes `--source <title>=<path>` and this is what derives the list.** The owner ruled
    on 2026-08-19 that the check stays per-deck on the argument shape every other verb here uses,
    rather than teaching the build to record a source path in the deck - which would have reached
    every deck this plugin ever emits, for a detection that can ship without it. What makes the
    derivation possible is already in the markup: a wired control carries `data-qv`, the title, and
    `data-file`, the source's base name (T-109), and `DECKS` above maps the deck to the directory
    those base names sit in.

    A deck carrying no quick view is refused with that as its reason. It is not a gap in coverage:
    there is nothing embedded, so there is nothing that can have drifted.
    """
    html = io.open(os.path.join(ROOT, deck), encoding="utf-8").read()
    pairs, seen = [], set()
    for m in re.finditer(r'data-qv="([^"]*)" data-file="([^"]*)"', html):
        title, base = m.group(1), m.group(2)
        if title in seen or not base:
            continue
        seen.add(title)
        pairs.append((title, "%s/%s" % (sources, base)))
    if not pairs:
        return ("the deck carries no quick view, so there is no embedded rendering that can have "
                "drifted from a source. `quickview.py list %s` says so in one line" % deck)
    missing = [p for _t, p in pairs if not os.path.exists(os.path.join(ROOT, p))]
    if missing:
        return ("the deck names %d source file(s) that are not in %s (%s). A quick view whose "
                "source is gone cannot be compared, and that is a defect rather than an exemption"
                % (len(missing), sources, ", ".join(missing)))
    args = ["check", deck]
    for title, path in pairs:
        args += ["--source", "%s=%s" % (title, path)]
    return args


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

    def __init__(self, label, state, code=None, output="", why="", seconds=None):
        self.label, self.state, self.code, self.output, self.why = label, state, code, output, why
        # `None` for a skipped command, and that is the distinction (T-279): a command that did not
        # run took no time in a different sense from one that ran fast, and `0.0s` says the wrong
        # one. The report prints `-` rather than a number.
        self.seconds = seconds


def run_one(path, argv_tail, verbose):
    """Run one checker and return its `Result`.

    Output is captured rather than inherited, and printed only for a failure. Sixteen tools each
    printing their full account is thousands of lines, and a wall of green is where the three red
    checks of 2026-08-10 hid. `--verbose` restores the inherited stream when the account itself is
    what you came for.
    """
    label = "python %s%s" % (path, "".join(" " + a for a in argv_tail))
    argv = [PY, path] + list(argv_tail)
    # Timed here because this is the one place every command goes through, so the durations are a
    # partition of the run by construction rather than by anybody remembering to add one (T-279).
    started_one = time.time()
    if verbose:
        print("\n=== %s" % label)
        sys.stdout.flush()
        code = subprocess.run(argv, cwd=ROOT).returncode
        return Result(label, "ran" if code == 0 else "failed", code,
                      seconds=time.time() - started_one)
    done = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True,
                          errors="replace")
    out = (done.stdout or "") + (done.stderr or "")
    return Result(label, "ran" if done.returncode == 0 else "failed", done.returncode, out,
                  seconds=time.time() - started_one)


def plan(decks, themes=()):
    """Every command this run will issue, in order, as `(section, path, argv-tail-or-reason)`."""
    steps = [("repository-wide", path, tail) for path, tail in WIDE]
    # Themes before decks: a deck is built against a theme, so a theme that does not conform is
    # the more useful failure to read first.
    for theme in themes:
        for path, builder in PER_THEME:
            steps.append((theme, path, builder(theme)))
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
            print("\n  %s" % ("gates" if sect == "repository-wide"
                              else ("per theme - " if sect.startswith("themes/")
                                    else "per deck - ") + sect))
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

    # The theme glob's one distinction is depth, and depth is not self-evident (T-228). Assert
    # both directions: it reaches the themes, and it does not reach the font faces one level
    # down - a face has no contract to validate against and would fail every token in it.
    found = themes_tracked()
    if "themes/lattice.css" not in found or "themes/quarto.css" not in found:
        sys.exit("SELF-TEST FAILED: the theme glob found %r - it must reach every theme, or a "
                 "theme falls out of the gate silently, which is the defect T-228 closed" % (found,))
    if any(f.startswith("themes/faces/") for f in found):
        sys.exit("SELF-TEST FAILED: the theme glob reached %r - `themes/faces/` holds font faces, "
                 "which have no contract to validate and would fail on every token"
                 % ([f for f in found if f.startswith("themes/faces/")],))

    if "examples/reference-deck.html" not in DECKS:
        sys.exit("SELF-TEST FAILED: no --sources declared for the reference deck. Guessing it "
                 "wrong does not error, it reports a content failure that reads like a defect in "
                 "the deck")
    return True


def decks_not_in_examples_readme():
    """`[(deck, why)]` - every deck in `DECKS` that `examples/README.md` does not link.

    **The page opens with a count, and a count is the one thing about a folder that goes stale
    without anybody editing it.** `examples/portfolio-review/` was tracked with its specification
    pair, its sources and a line in `DECKS`, and `0.6.0` shipped with `examples/README.md` saying
    *Four decks* over a table listing three and the seeded-defects fixture - so the number was right
    about the table and the table was wrong about the tree (`PR-02`, T-226).

    **What this asserts is membership, not the numeral**, and that is deliberate. Parsing the count
    out of the prose would bind this gate to one sentence's wording; asking whether each deck is
    reachable from the page binds it to the property the reader cares about. A deck added to `DECKS`
    and not written up fails here, which is the direction the defect travelled.
    """
    text = io.open(os.path.join(ROOT, "examples", "README.md"), encoding="utf-8").read()
    out = []
    for deck in sorted(DECKS):
        rel = deck[len("examples/"):]
        if rel not in text:
            out.append((deck, "`examples/README.md` does not link it. It is a deck this repository "
                              "ships - it is in DECKS and it is gated on every run - so the page "
                              "the front README sends a reader to for *every shipped deck* has to "
                              "reach it. Add its row and its section, and its entry to "
                              "`figures.py`'s ARTIFACTS if the section states its size."))
    return out


# --- entry point ----------------------------------------------------------------------------

def main(argv):
    verbose = "--verbose" in argv
    listing = "--list" in argv
    started = time.time()
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

    unlisted = decks_not_in_examples_readme()
    if unlisted:
        for h, why in unlisted:
            print("UNLISTED DECK     %s" % h)
            print("        %s" % wrap(why, 8))
        return 2

    decks = [d for d in html if d in DECKS]
    themes = themes_tracked()

    steps = plan(decks, themes)
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

    # **How long this took, printed rather than written down anywhere** (T-148, `CE-08`). Five
    # successive handoffs carried a run time for this command that no committed document stated, so
    # nothing could check it and it drifted freely - it was quoted as 7-11 minutes against a real
    # 154 seconds (`BP-2`). A figure with no home cannot be stale and cannot be corrected either.
    # The number belongs to the run, not to a document: **L-95**.
    # **Where that time went, ranked** (T-279). The line above was the whole account of cost until
    # 2026-08-29, and one number over 37 commands cannot answer *what is slow* - the first person to
    # ask had to write a harness outside the repository to rank them. Printed on every run, at any
    # size, for the reason everything else here is: a figure that appears only when somebody is
    # already suspicious is a figure nobody checks (**L-36**).
    wall = time.time() - started
    timed_rows = sorted(((r.seconds, r.label) for _s, r in results if r.seconds is not None),
                        reverse=True)
    measured = sum(sec for sec, _l in timed_rows)
    if timed_rows:
        print("\n  where the time went")
        shown, cum = 0, 0.0
        for sec, label in timed_rows:
            cum += sec
            shown += 1
            print("    %7.1fs  %5.1f%%  cum %5.1f%%  %s"
                  % (sec, 100 * sec / measured, 100 * cum / measured, label))
            # The tail is a long list of sub-second commands and naming each buys nothing; the cut
            # is at the share, so what prints is *the commands that dominate* rather than a fixed
            # count that would flatter a faster machine. **The row that crosses the line is shown
            # before breaking**: cutting above it put a 41 s command into a bucket whose own label
            # says none of them is the reason a run is slow, which was a lie the first time it ran.
            if cum / measured > 0.95:
                break
        rest = timed_rows[shown:]
        if rest:
            tail = sum(s for s, _l in rest)
            print("    %7.1fs  %5.1f%%              the other %d command(s), none of them the "
                  "reason a run is slow" % (tail, 100 * tail / measured, len(rest)))
        # The commands are a partition of the run, so their times must reconcile with the clock.
        # The difference is this file's own work - discovery, classification, the report - and it
        # is printed rather than absorbed, because an unexplained gap is where a slow step hides.
        print("    ------------------------")
        print("    %7.1fs  in commands, against %.1fs on the clock - %.1fs is this file's own "
              "discovery and report" % (measured, wall, wall - measured))
    print("\n%d failure(s), %d unclassified, %d stale  -  %.0f s"
          % (failed, un, st, wall))
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
