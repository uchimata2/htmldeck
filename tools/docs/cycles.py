#!/usr/bin/env python3
"""The pre-release audit's coverage partition, derived from the tree instead of tabulated by hand.

    python tools/docs/cycles.py            # the partition, the grade table, and the verdict
    python tools/docs/cycles.py --cycle 7  # one cycle's membership - what that session reads
    python tools/docs/cycles.py --list     # every tracked path with the cycle that owns it
    python tools/docs/cycles.py --plan     # section 2's Files and Bytes columns, ready to paste

**This exists because `PR-06` found the audit's own coverage short by one file and 17,028 bytes,
and the plan could not say where.** `T-219` section 1 gave the tree as 492 files; section 2's
thirty-seven sized cycles summed to 491. Neither number was wrong on purpose - they were measured
at different moments and reconciled by nobody, which is what two hand-kept tables of one fact do.
The sharper half of that finding is why this file exists rather than a corrected table: section 2
stated a **count** per cycle and never a **membership**, so the missing file could not be located
from the document at all. A count is an answer with no working shown.

**So the membership is the rule and the count is derived from it.** Each cycle below carries the
patterns that define its subject; every tracked path falls to the first cycle that claims it, and a
path no cycle claims is `UNASSIGNED` and **fails the run**. That is `tools/check_all.py`'s partition
one subject over - it is a tool no table names that fails that run, and a file no cycle reads that
fails this one - and it is **L-135** applied to the audit's own boundaries: derive the membership,
never enumerate it.

**Three ways to fail, because a list that catches one is trusted for catching neither** (**L-74**):

  - a tracked path no cycle's rules match is `UNASSIGNED`;
  - a **path claim** - a written-out filename or glob - that matches nothing in the tree is `STALE`;
  - a cycle that owns no tracked file **and gives no reason for owning none** is `UNSTATED`.

**A query is not a path claim, and cannot go stale.** `Task(shipped_in="unreleased")` is a question
about the tree's state, and an empty answer is a correct one - it is empty the day after a release
and full the day a task closes. Failing on that would teach a reader to ignore the verdict, which
costs more than the case it catches. What the check was standing in for is the empty *cycle*, and
`UNSTATED` catches that directly.

A pattern whose every match was already claimed by an earlier cycle is **not** stale either - that is
the design. Cycle 13 is *the rest of `tools/deck/`* and is written as the whole directory, after
cycles 10 to 12 have taken theirs. Precedence is what lets a broad rule stay broad.

**Six cycles hold no tracked file and that is not a gap.** Cycles 25 and 26 examine surfaces outside
git, and 39 to 42 are synthesis over material other cycles have already read. Each is declared with
an empty rule list and an explicit reason, so *no files* is a stated answer rather than an omission -
which is exactly what `UNSTATED` distinguishes it from.

**When the audit closes, this gate has done its job.** Cycle 42 is the place to decide whether it
keeps running: a partition over cycles nobody will run again costs every later file a decision it
does not need. Deleting it then is a smaller mistake than carrying it by inertia - which is the one
thing this docstring is here to prevent.

Runs from anywhere: the project root is derived from this file, not from the working directory.
Pure standard library (**L-07**), plus `git`, which decides what a clone receives.
"""

import fnmatch
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONFIG = os.path.join(ROOT, ".taskmd", "config.md")
TASK = re.compile(r"^tasks/T-(\d+)-")

# A cycle is sized to about 300 KB of source - what one session can read *and still judge* - and
# this is where that stops being true rather than where it stops being exact. An **advisory**, never
# a failure: a cycle 15% over is a long sitting, and a cycle 50% over is a boundary that needs
# cutting before anyone starts. Grade C is exempt, because those files are rendered and measured
# rather than read (`CLAUDE.md` rule 6), so their bytes say nothing about the sitting.
SIZING = 350000


# --- the rules ------------------------------------------------------------------------------

class Task(object):
    """A rule over task records: a work package, an open/closed state, and an id ceiling.

    Written as three conditions rather than as a file list because that is what the cycle's own
    subject says - *`PH3` closed, `T-113`-`T-130`* is a query, and a query re-answers itself when a
    task closes or a new one is filed. The id ceiling is inclusive and `None` means *onward*, which
    is how section 2 words the last band of every run.
    """

    def __init__(self, work_package=None, state=None, id_max=None, shipped_in=None):
        self.work_package = work_package     # a tuple of values, or None for any
        self.state = state                   # "open", "closed", or None for either
        self.id_max = id_max                 # inclusive; None for no ceiling
        self.shipped_in = shipped_in         # a tuple of versions, or None for any

    def __repr__(self):
        bits = []
        if self.work_package:
            bits.append("/".join(str(w) for w in self.work_package))
        if self.state:
            bits.append(self.state)
        if self.shipped_in:
            bits.append("shipped_in " + "/".join(str(v) for v in self.shipped_in))
        bits.append("T-%03d and below" % self.id_max if self.id_max else "no ceiling")
        return "task record: " + ", ".join(bits)

    def matches(self, path, meta):
        m = TASK.match(path)
        if not m or meta is None:
            return False
        if self.work_package is not None and meta["work_package"] not in self.work_package:
            return False
        if self.state is not None and meta["state"] != self.state:
            return False
        if self.shipped_in is not None and meta["shipped_in"] not in self.shipped_in:
            return False
        if self.id_max is not None and int(m.group(1)) > self.id_max:
            return False
        return True


class Lesson(object):
    """A rule over the lesson files in `docs/lessons/`, by number band, inclusive at both ends."""

    def __init__(self, low, high=None):
        self.low, self.high = low, high

    def __repr__(self):
        return "lesson L-%02d to %s" % (self.low, "L-%02d" % self.high if self.high else "the end")

    def matches(self, path, meta):
        m = re.match(r"^docs/lessons/L-(\d+)\.md$", path)
        if not m:
            return False
        n = int(m.group(1))
        return n >= self.low and (self.high is None or n <= self.high)


# Ordered, and the order is the precedence. `grade` is `AUDIT-METHOD.md` section 2's reading
# depth: A wide, B narrow, C instrument-only. `rules` is a list of fnmatch patterns and rule
# objects; `reason` is required where the list is empty, so that no files is stated rather than
# missing.
CYCLES = [
    (0, "Instruments and baseline", "A", [
        "tools/check_all.py",
        "tools/docs/findings.py",
        "tools/tasks/lint.py",
        "tools/tasks/query.py",
    ], None),
    (1, "The human-facing set", "A", [
        "README.md",
        "LICENSE",
        "examples/README.md",
        "examples/sources/README.md",
        "shell/README.md",
        ".claude-plugin/*.json",
    ], None),
    (2, "The skill and the prompt", "A", [
        "skills/htmldeck/*",
        "skills/htmldeck/references/*",
        "reference/*",
    ], None),
    (3, "Tier 1 and the brief", "A", [
        "CLAUDE.md",
        "docs/BRIEF.md",
    ], None),
    (4, "The release machinery", "A", [
        "docs/PUBLISHING.md",
        "docs/RELEASE-HISTORY.md",
        ".gitignore",
        ".gitattributes",
    ], None),
    (5, "The tracker's own rules", "A", [
        "tasks/README.md",
        "tasks/TASK-WORKFLOW.md",
        "tasks/TOOLING.md",
        "tasks/_*.md",
        ".taskmd/config.md",
        ".handoff/config.md",
    ], None),
    (6, "The release plan", "A", [
        "docs/RELEASE-PHASES.md",
    ], None),
    (7, "The unreleased work, and this audit's own record", "A", [
        "docs/AUDIT-METHOD.md",
        "docs/PRE-RELEASE-AUDIT.md",
        Task(state="open"),
        # *Every `shipped_in: unreleased` record*, which is the cycle's own words. A task can close
        # and stay unreleased for days, and the closed-record bands are stage 7 - the LEAST current
        # subject. Without this a remedy raised by this very audit would be read as history the week
        # it was written. No record carries the value today; the first one to close after `0.6.0`
        # will, which is why the rule is here before it is needed.
        Task(state="closed", shipped_in=("unreleased",)),
    ], None),
    (8, "The design system and the evaluation", "A", [
        "docs/DESIGN-SYSTEM.md",
        "docs/EVALUATION.md",
    ], None),
    (9, "The three contracts", "A", [
        "docs/COMPONENT-CONTRACT.md",
        "docs/THEME-CONTRACT.md",
        "docs/MOTION-GUIDE.md",
    ], None),
    (10, "The gate's code", "A", [
        "tools/deck/check.py",
        "tools/deck/contract.py",
        "tools/deck/content.py",
        "tools/deck/contrast.py",
        "tools/deck/density.py",
        "tools/deck/figgrid.py",
        "tools/deck/glitchfree.py",
        "tools/deck/markhits.py",
        "tools/deck/ruleset.py",
    ], None),
    (11, "audit.py and critique.py", "A", [
        "tools/deck/audit.py",
        "tools/deck/critique.py",
    ], None),
    (12, "The build path", "A", [
        "tools/deck/spec.py",
        "tools/deck/shell.py",
        "tools/deck/component.py",
        "tools/deck/theme.py",
        "tools/deck/preflight.py",
        "tools/deck/presenter.py",
        "tools/deck/render.py",
    ], None),
    (13, "The rest of tools/deck/", "A", [
        "tools/deck/*",
    ], None),
    (14, "tools/docs/", "A", [
        "tools/docs/*",
    ], None),
    (15, "The remaining tools", "A", [
        "tools/assets/*",
        "tools/examples/*",
        "tools/kb/*",
        "tools/plugin/*",
        "tools/portability/*",
        "tools/*",
    ], None),
    (16, "The shell and the themes", "A", [
        "shell/*",
        "themes/*",
        "themes/faces/*",
    ], None),
    (17, "The shipped decks and the blindness fixture", "C", [
        "examples/*.html",
        "examples/*/*.html",
    ], None),
    (18, "The deck specifications and sources", "A", [
        "examples/*",
        "examples/*/*",
        "examples/*/*/*",
    ], None),
    (19, "The prior audits", "B", [
        "docs/CONTEXT-AUDIT.md",
        "docs/RULESET-AUDIT.md",
    ], None),
    (20, "The design rationale", "B", [
        "docs/DESIGN-RATIONALE.md",
    ], None),
    (21, "Lessons L-01 to L-77, and the index", "B", [
        "docs/LESSONS.md",
        Lesson(1, 77),
    ], None),
    (22, "Lessons L-78 onward", "B", [
        Lesson(78),
    ], None),
    (23, "Research R1 to R4", "B", [
        "docs/research/R1*",
        "docs/research/R2*",
        "docs/research/R3*",
        "docs/research/R4*",
    ], None),
    (24, "Research R5 to R9, upstream, sketches", "B", [
        "docs/research/*",
        "docs/upstream/*",
        "docs/sketches/*",
    ], None),
    (25, "Memory and the handoff record", "-", [],
     "outside git. The agent memory store and the handoff archive are not tracked paths; the one "
     "tracked file of that machinery is .handoff/config.md, which cycle 5 reads with the tracker's "
     "other configuration"),
    (26, "The untracked surface", "-", [],
     "outside git by definition - what .gitignore hides. A tracked path here would be a "
     "contradiction in the cycle's own subject"),
    (27, "PH1 closed, T-002 to T-085", "B", [
        Task(work_package=("PH1",), state="closed", id_max=85),
    ], None),
    (28, "PH1 closed, T-086 onward", "B", [
        Task(work_package=("PH1",), state="closed"),
    ], None),
    (29, "PH2 closed", "B", [
        Task(work_package=("PH2",), state="closed"),
    ], None),
    # The five PH3 bands were re-cut on 2026-08-23, and the boundaries moved rather than the rule.
    # `0.6.0` shipped that morning and closed eighteen PH3 tasks, all of them above T-164; under the
    # plan's old ceilings they landed in one cycle of 39 files and 465,531 bytes, against the ~300 KB
    # a cycle is sized to. **Derived membership does not mean derived boundaries.** A ceiling that
    # rebalanced itself would move a finished cycle's membership under it, and a coverage-ledger row
    # would stop describing what that session read - so the ceilings are declared, sized once, and
    # `--sizing` reports when one has drifted far enough to need cutting again. None of the five had
    # run when they moved.
    (30, "PH3 closed, up to T-113", "B", [
        Task(work_package=("PH3",), state="closed", id_max=113),
    ], None),
    (31, "PH3 closed, T-114 to T-135", "B", [
        Task(work_package=("PH3",), state="closed", id_max=135),
    ], None),
    (32, "PH3 closed, T-136 to T-153", "B", [
        Task(work_package=("PH3",), state="closed", id_max=153),
    ], None),
    (33, "PH3 closed, T-154 to T-186", "B", [
        Task(work_package=("PH3",), state="closed", id_max=186),
    ], None),
    (34, "PH3 closed, T-187 onward", "B", [
        Task(work_package=("PH3",), state="closed"),
    ], None),
    (35, "WP2 closed, up to T-032", "B", [
        Task(work_package=("WP2",), state="closed", id_max=32),
    ], None),
    (36, "WP2 closed, T-033 onward", "B", [
        Task(work_package=("WP2",), state="closed"),
    ], None),
    (37, "WP1 closed", "B", [
        Task(work_package=("WP1",), state="closed"),
    ], None),
    (38, "WP3, final, none, and the cancelled stubs", "B", [
        Task(state="closed"),
    ], None),
    (39, "The figure and version sweep", "-", [],
     "synthesis. Every number in the tree, over material cycles 0 to 38 have already read - a file "
     "assigned here would be read twice and counted twice"),
    (40, "Triage, rank, raise the tasks", "-", [], "synthesis over the register, not over the tree"),
    (41, "Re-read what the remedies changed", "-", [],
     "synthesis. It re-runs cycles that already own their files; the second reading is a repeat of "
     "an assignment, not a new one"),
    (42, "Phase 2", "-", [], "synthesis over the register, not over the tree"),
]


# --- discovery ------------------------------------------------------------------------------

def tracked():
    """Every tracked path - what a fresh clone receives, and nothing else.

    `git` rather than a walk, and for `tools/check_all.py`'s reason: `control/`, `dist/` and `.kb/`
    are machine-local by design, and a file discovered there would be a file no adopter has. An
    audit that read them would be auditing this machine.
    """
    try:
        out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True)
    except OSError:
        sys.exit("git is not on PATH, so this cannot tell a tracked file from a local scratch one "
                 "- and that distinction is the whole partition. Install git.")
    if out.returncode:
        sys.exit("git ls-files failed (exit %d): %s" % (out.returncode, out.stderr.strip()))
    return sorted(p.strip() for p in out.stdout.splitlines() if p.strip())


def open_statuses():
    """The statuses that count as open, read from `.taskmd/config.md` rather than copied here.

    The schema is that file's (`TASK-WORKFLOW.md` section 3), and a second copy of a vocabulary
    disagrees with the first the day either changes - **L-13**. Cycle 7 is *the unreleased work*,
    which is a question about status, so this rule has to ask the schema what open means.
    """
    try:
        text = open(CONFIG, encoding="utf-8").read()
    except IOError:
        sys.exit("cannot read %s, which is where the open/closed vocabulary lives. Cycle 7's rule "
                 "is a question about status and has no answer without it." % CONFIG)
    m = re.search(r"^open_statuses:\s*\[([^\]]*)\]", text, re.M)
    if not m:
        sys.exit("no open_statuses key in %s. The schema names which statuses are open and this "
                 "file will not guess a vocabulary it does not own." % CONFIG)
    return set(v.strip() for v in m.group(1).split(",") if v.strip())


def front_matter(path, opens):
    """`{work_package, state}` for a task record, or `None` for a file that is not one.

    Only the two fields the rules ask about are read. A record missing `work_package` carries
    `None` for it, which cycle 38's rule accepts on purpose - the two cancelled stubs predate the
    field and are still tracked files somebody has to read.
    """
    if not TASK.match(path):
        return None
    try:
        text = open(os.path.join(ROOT, path), encoding="utf-8").read()
    except IOError:
        return None
    if not text.startswith("---"):
        return {"work_package": None, "shipped_in": None, "state": "closed"}
    body = text.split("---", 2)
    head = body[1] if len(body) > 2 else ""
    def field(name):
        m = re.search(r"^%s:\s*(.*)$" % name, head, re.M)
        if not m:
            return None
        v = m.group(1).strip()
        return v or None
    status = field("status")
    return {"work_package": field("work_package"),
            "shipped_in": field("shipped_in"),
            "state": "open" if status in opens else "closed"}


# --- the partition --------------------------------------------------------------------------

def matched(rule, path, meta):
    if isinstance(rule, str):
        return fnmatch.fnmatchcase(path, rule)
    return rule.matches(path, meta)


def partition(paths, opens):
    """`(assignment, unassigned, stale)`.

    `assignment` maps a path to its cycle number - the first cycle whose rules claim it, which is
    what makes *exactly one* structural rather than checked afterwards. `unassigned` is every
    tracked path no cycle claims, the state that fails the run. `stale` is the mirror: a rule that
    matches nothing anywhere in the tree, ignoring precedence, which is a rule written for a file
    that has since moved or gone.
    """
    meta = {p: front_matter(p, opens) for p in paths}
    assignment, hit = {}, set()
    for number, _subject, _grade, rules, _reason in CYCLES:
        for rule in rules:
            for path in paths:
                if matched(rule, path, meta[path]):
                    hit.add((number, repr(rule)))
                    if path not in assignment:
                        assignment[path] = number
    stale = []
    for number, _subject, _grade, rules, _reason in CYCLES:
        for rule in rules:
            # **Only a path claim can go stale; a query cannot.** A string names a file, or a shape
            # of filename, so matching nothing means the file moved or the name was mistyped - the
            # hand-kept half failing silently, which is the whole reason this direction is checked.
            # A `Task` or `Lesson` rule is a *question* about the tree, and an empty answer is a
            # legitimate one: *every unreleased record* is empty the day after a release and full
            # the day a task closes. Failing on that would teach a reader to ignore the verdict,
            # which costs more than the case it catches. The empty **cycle** is still caught, by
            # `unstated` below - which is the failure that question was standing in for.
            if isinstance(rule, str) and (number, repr(rule)) not in hit:
                stale.append((number, rule))
    return assignment, sorted(p for p in paths if p not in assignment), stale


def unstated(assignment):
    """Cycles that own no tracked file and give no reason for owning none.

    Six own none and say why - two examine surfaces outside git, four are synthesis over material
    other cycles have already read. That is a stated answer. A cycle that empties out *without* a
    reason is the other thing entirely: a subject nobody is reading and nobody decided not to read.
    """
    out = []
    for number, subject, _grade, _rules, reason in CYCLES:
        if not [p for p, c in assignment.items() if c == number] and not reason:
            out.append((number, subject))
    return out


def sizes(paths):
    total = {}
    for p in paths:
        try:
            total[p] = os.path.getsize(os.path.join(ROOT, p))
        except OSError:
            total[p] = 0
    return total


# --- reporting ------------------------------------------------------------------------------

def report(assignment, unassigned, stale, byte):
    print("The audit's coverage partition - %d tracked files, %s bytes\n"
          % (len(assignment) + len(unassigned), "{:,}".format(sum(byte.values()))))
    print("  %-3s %-4s %-46s %6s %12s" % ("#", "Grd", "Subject", "Files", "Bytes"))
    print("  " + "-" * 74)
    grades = {}
    for number, subject, grade, _rules, reason in CYCLES:
        own = [p for p, c in assignment.items() if c == number]
        n, b = len(own), sum(byte[p] for p in own)
        grades.setdefault(grade, [0, 0])
        grades[grade][0] += n
        grades[grade][1] += b
        print("  %-3d %-4s %-46s %6d %12s"
              % (number, grade, subject[:46], n, "{:,}".format(b)))
        if not own and reason:
            print("      %s" % reason[:100])
    print("  " + "-" * 74)
    print("  %-54s %6d %12s"
          % ("total", sum(g[0] for g in grades.values()),
             "{:,}".format(sum(g[1] for g in grades.values()))))

    print("\nCoverage grades - AUDIT-METHOD.md section 2\n")
    print("  %-4s %-40s %6s %12s" % ("Grd", "Reading depth", "Files", "Bytes"))
    print("  " + "-" * 64)
    labels = {"A": "wide", "B": "narrow", "C": "instrument only", "-": "no tracked file"}
    for grade in ("A", "B", "C", "-"):
        if grade in grades:
            print("  %-4s %-40s %6d %12s"
                  % (grade, labels[grade], grades[grade][0], "{:,}".format(grades[grade][1])))
    read_n = sum(grades.get(g, [0, 0])[0] for g in ("A", "B"))
    read_b = sum(grades.get(g, [0, 0])[1] for g in ("A", "B"))
    print("  " + "-" * 64)
    print("  %-45s %6d %12s" % ("read (A + B)", read_n, "{:,}".format(read_b)))
    print("  %-45s %6d %12s"
          % ("the tree", len(assignment) + len(unassigned), "{:,}".format(sum(byte.values()))))

    print("")
    for number, subject, grade, _rules, _reason in CYCLES:
        own = [p for p, c in assignment.items() if c == number]
        b = sum(byte[p] for p in own)
        if grade != "C" and b > SIZING:
            print("  OVERSIZED   cycle %d, %s - %s bytes against the ~300 KB a cycle is sized to"
                  % (number, subject, "{:,}".format(b)))
    code = complaint(unassigned, stale, unstated(assignment))
    if unassigned:
        print("\nEvery one of those is a hole in the acceptance criterion *every tracked file is "
              "read,\nskipped with a stated reason, or produced a finding* - the claim cycle 40 has "
              "to make,\nand cannot make over a file no cycle reads. Assign each, or declare a "
              "cycle that does.")
    if stale:
        print("\nA rule written for a file that has since moved is how a partition goes quietly "
              "short.\nThat is PR-06, and it is why this checks both directions rather than one "
              "(**L-74**).")
    if not code:
        print("Every tracked file belongs to exactly one cycle, and every rule earns its place.")
    return code


def plan_rows(assignment, byte):
    """Section 2's Files and Bytes columns, ready to paste over the hand-kept ones."""
    for number, subject, grade, _rules, _reason in CYCLES:
        own = [p for p, c in assignment.items() if c == number]
        if own:
            print("| %d | %s | %d | %s |"
                  % (number, subject, len(own), "{:,}".format(sum(byte[p] for p in own))))
        else:
            print("| %d | %s | - | - |" % (number, subject))


# --- the self-test --------------------------------------------------------------------------

def self_test():
    """**A partition that has never been seen to fail is a claim about the instrument** (**L-04**,
    **L-36**). Five states are asserted rather than read: precedence deciding a contested path, an
    unassigned file, a stale path claim, a query whose empty answer must **not** read as stale, and
    an empty cycle that states its reason against one that does not. The fixture is written here and
    never taken from the tree - a self-test built out of repository state blocks the commit that
    changes it."""
    cycles = [(1, "first", "A", ["a/*"], None),
              (2, "second", "A", ["a/x.md"], None),
              (3, "third", "A", ["gone/*"], None),
              (4, "fourth", "A", [Task(work_package=("NONESUCH",))], None),
              (5, "fifth", "A", [], "declared empty, and this is the reason")]
    real, CYCLES[:] = list(CYCLES), cycles
    try:
        assign, un, stale = partition(["a/x.md", "a/y.md", "b/z.md"], set())
        if [n for n, _s in unstated(assign)] != [2, 3, 4]:
            sys.exit("SELF-TEST FAILED: the empty cycles reported %r, wanted 2, 3 and 4. Cycle 5 "
                     "states why it is empty and the other three do not - and cycle 2 is the case "
                     "worth having: it is empty because precedence took its only file, which is a "
                     "subject nobody reads and looks like nothing at all in the table"
                     % (unstated(assign),))
        if any(not isinstance(r, str) for _n, r in stale):
            sys.exit("SELF-TEST FAILED: a query reported stale (%r). A question with an empty "
                     "answer is answered, not broken, and failing on it trains a reader to ignore "
                     "every verdict this file prints" % (stale,))
        if assign.get("a/x.md") != 1:
            sys.exit("SELF-TEST FAILED: a path two cycles claim went to %r, wanted cycle 1. First "
                     "match wins is what makes *exactly one cycle* structural; without it a file "
                     "is counted twice and the totals still look right" % (assign.get("a/x.md"),))
        if un != ["b/z.md"]:
            sys.exit("SELF-TEST FAILED: a path no cycle claims reported %r, wanted ['b/z.md']. A "
                     "file falling through every rule in silence is PR-06 itself" % (un,))
        if [n for n, _r in stale] != [3]:
            sys.exit("SELF-TEST FAILED: a rule matching nothing reported %r, wanted cycle 3 - the "
                     "hand-kept half going stale without a word" % (stale,))
    finally:
        CYCLES[:] = real
    return True


# --- entry point ----------------------------------------------------------------------------

def complaint(unassigned, stale, empty=()):
    """The partition's verdict, printed by **every** mode rather than only by the default one.

    **This is where the failing half lives, and it is deliberately not `tools/check_all.py`'s.**
    Wiring it into the release gate would make an audit's coverage a release step, and
    `AUDIT-METHOD.md` section 1 says no audit is one - a new document with no cycle would block a
    release it has nothing to do with. So the check rides on the command a cycle already runs at
    step 2 of `T-219` section 2: ask this file which files a cycle reads, and it answers only after
    saying whether the partition still holds. Forty-one cycles remain, so the question gets asked
    forty-one more times, which is the coverage this needed and the release gate could not give it.
    """
    for path in unassigned:
        print("  UNASSIGNED  %s" % path)
    for number, rule in stale:
        print("  STALE       cycle %d: %s" % (number, rule))
    for number, subject in empty:
        print("  UNSTATED    cycle %d, %s - no tracked file, and no reason for having none"
              % (number, subject))
    if unassigned or stale or empty:
        print("The partition no longer holds: %d file(s) in no cycle, %d rule(s) matching nothing, "
              "%d cycle(s) empty without saying why. Run `python tools/docs/cycles.py` for the "
              "whole account before reading anything."
              % (len(unassigned), len(stale), len(empty)))
        return 1
    return 0


def main(argv):
    self_test()
    paths = tracked()
    opens = open_statuses()
    assignment, unassigned, stale = partition(paths, opens)
    byte = sizes(paths)

    if "--cycle" in argv:
        try:
            want = int(argv[argv.index("--cycle") + 1])
        except (IndexError, ValueError):
            sys.exit("--cycle takes a cycle number, 0 to %d" % CYCLES[-1][0])
        row = [c for c in CYCLES if c[0] == want]
        if not row:
            sys.exit("no cycle %d. The programme is 0 to %d." % (want, CYCLES[-1][0]))
        number, subject, grade, _rules, reason = row[0]
        own = sorted(p for p, c in assignment.items() if c == number)
        print("Cycle %d - %s  (grade %s)\n" % (number, subject, grade))
        for p in own:
            print("  %10s  %s" % ("{:,}".format(byte[p]), p))
        if own:
            print("\n  %d file(s), %s bytes" % (len(own), "{:,}".format(sum(byte[p] for p in own))))
        else:
            print("  no tracked file: %s" % (reason or "no reason recorded, which is a defect"))
        print("")
        return complaint(unassigned, stale, unstated(assignment))

    if "--list" in argv:
        for p in sorted(paths):
            print("%3s  %s" % (assignment.get(p, "--"), p))
        print("")
        return complaint(unassigned, stale, unstated(assignment))

    if "--plan" in argv:
        plan_rows(assignment, byte)
        print("")
        return complaint(unassigned, stale, unstated(assignment))

    return report(assignment, unassigned, stale, byte)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
