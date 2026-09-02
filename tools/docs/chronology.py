#!/usr/bin/env python3
"""Hold `docs/RELEASE-HISTORY.md`'s two derived columns to the commands the document says derive them.

    python tools/docs/chronology.py          # the verdict, and the partition behind it
    python tools/docs/chronology.py --report # the partition even when piped; --quiet is the reverse

**A green run prints one line when stdout is not a terminal** (T-286): an agent pays a tool's output
again on every later turn, and a green partition is a report nobody acts on. `--report` restores it,
`--quiet` forces the line at a terminal, and a red run prints everything in every mode.

**Why this file exists.** Section 1 of the chronology names two commands in a fence - the tag list
with each tag's date, and `shipped_in` counted over the task records - and says the *Date* and
*Tasks* columns are derived from them rather than kept by hand. Nothing connected the two. Measured
2026-08-22 while cutting `0.6.0`: `0.5.0` read **14** where the command answered **22**, `0.2.4` read
**1** against **2**, both wrong for days with every gate green and `figures.py` reporting `0 stale`.
Half of the shortfall was task records carrying no `shipped_in` at all, back-filled that day; the
other half was the row simply never being recounted, which is the half no back-fill fixes (T-220).

**Why `figures.py` does not reach it.** That tool watches a fence holding what a command printed,
and holds a prose numeral to a label the command prints beside it. This column is a number lifted
out of a command's output and typed into a table cell - the same claim in a shape no fence holds -
and the commands are `git` and a shell pipeline, which `figures.py`'s `RUNNABLE` allowlist refuses
by design. So this is a checker of its own, on the precedent of `cycles.py` and `findings.py`: one
subject, one verdict.

**The commands are implemented here, not executed.** The second is a pipeline and the tools in this
repository run without a shell (**L-07**). So the tag dates come from `git for-each-ref` with the
document's own format, and the counts from every `shipped_in:` line in `tasks/*.md`, which is what
`grep -h` reads - and **the fence is asserted**: a document that stops naming these two commands
fails the run, because then the check would be enforcing a derivation the document no longer claims.
If the owner wants the date column to mean something else, that is an edit to the fence and to this
file together.

**It fails in both directions** (**L-74**). A row whose date or count disagrees fails. A tag with no
row fails, and a version the task records carry with no row fails - a release that forgot step 8 of
`PUBLISHING.md` section 8 is caught here rather than at the next session's sweep. A row with no tag
fails rather than passing quietly. The comparison is against `%(creatordate:short)` and nothing
better: the tag set is mixed, annotated and lightweight, and `creatordate` means the tag's date for
one and the commit's for the other. Binding to the command the document names tests the claim the
document makes; binding to anything better would move a near-midnight release by a day the first
time a timezone differs.

**What it does not decide.** The fourth column, *what it is remembered for*, is prose. And whether
a row *should* exist for a version is the release sequence's question; this only says the table and
the commands disagree.

Runs its own self-test first and refuses to report if it fails (**L-04**). Runs from anywhere: the
project root is derived from this file, not from the working directory. Pure standard library.
"""

import contextlib
import io
import os
import re
import subprocess
import sys
from collections import Counter

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HISTORY = os.path.join(ROOT, "docs", "RELEASE-HISTORY.md")
TASKS = os.path.join(ROOT, "tasks")

# The two commands the document names, verbatim. A fence that carries neither, or only one, fails.
TAG_COMMAND = ("git for-each-ref --sort=creatordate "
               "--format='%(refname:short) %(creatordate:short)' refs/tags")
COUNT_COMMAND = 'grep -h "^shipped_in:" tasks/*.md | sort | uniq -c'

FENCE = re.compile(r"^```(\w*)\s*$")
# A release row: a code-spanned `x.y.z`, then the date cell, then the count cell.
ROW = re.compile(r"^\|\s*`(\d+\.\d+\.\d+)`\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|")
SHIPPED = re.compile(r"^shipped_in:[ \t]*(.*?)[ \t]*$")
VERSION = re.compile(r"^\d+\.\d+\.\d+$")


def fenced_lines(text):
    """Every non-blank line inside a fenced block, stripped."""
    out, inside = [], False
    for line in text.split("\n"):
        if FENCE.match(line):
            inside = not inside
            continue
        if inside and line.strip():
            out.append(line.strip())
    return out


def stated_commands(text):
    """`(tag_named, count_named)` - whether the document's fences carry each command verbatim."""
    lines = fenced_lines(text)
    return TAG_COMMAND in lines, COUNT_COMMAND in lines


def rows(text):
    """`[(line_no, version, date_cell, count_cell)]` for every release row, in document order."""
    out = []
    for i, line in enumerate(text.split("\n"), 1):
        m = ROW.match(line)
        if m:
            out.append((i, m.group(1), m.group(2), m.group(3)))
    return out


def tag_dates(root=ROOT):
    """`{version: date}` from the document's own tag command, the leading `v` dropped."""
    argv = ["git", "for-each-ref", "--sort=creatordate",
            "--format=%(refname:short) %(creatordate:short)", "refs/tags"]
    p = subprocess.Popen(argv, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if p.returncode:
        sys.exit("git for-each-ref failed (%d): %s" % (p.returncode, err.decode("utf-8", "replace")))
    dates = {}
    for line in out.decode("utf-8", "replace").split("\n"):
        parts = line.split()
        if len(parts) == 2:
            dates[parts[0][1:] if parts[0].startswith("v") else parts[0]] = parts[1]
    return dates


def shipped_counts(tasks_dir=TASKS):
    """`Counter` over every `shipped_in:` line in `tasks/*.md` - what `grep -h | uniq -c` counts."""
    counts = Counter()
    for name in sorted(os.listdir(tasks_dir)):
        if not name.endswith(".md"):
            continue
        with io.open(os.path.join(tasks_dir, name), encoding="utf-8") as f:
            for line in f:
                m = SHIPPED.match(line.rstrip("\r\n"))
                if m:
                    counts[m.group(1)] += 1
    return counts


def version_key(v):
    return tuple(int(x) for x in v.split("."))


def compare(table, tags, counts):
    """`[complaint]` - every disagreement between the table and the two commands, both directions."""
    bad = []
    listed = set()
    for line_no, version, date, count in table:
        listed.add(version)
        if version not in tags:
            bad.append("line %d: `%s` has no tag `v%s`, so its date derives from nothing"
                       % (line_no, version, version))
        elif date != tags[version]:
            bad.append("line %d: `%s` is dated %s and the tag's creatordate is %s"
                       % (line_no, version, date, tags[version]))
        expected = counts.get(version, 0)
        if not count.isdigit() or int(count) != expected:
            bad.append("line %d: `%s` counts %s task(s) and `shipped_in:` on the task records answers %d"
                       % (line_no, version, count or "no", expected))
    for version in sorted(tags, key=version_key):
        if version not in listed:
            bad.append("tag `v%s` (%s) has no row in the table" % (version, tags[version]))
    for version in sorted((v for v in counts if VERSION.match(v)), key=version_key):
        if version not in listed:
            bad.append("%d task record(s) carry `shipped_in: %s` and the table has no row for it"
                       % (counts[version], version))
    return bad


def self_test():
    """Every direction asserted on a fixture, judged by the message it produces (**L-55**) - and the
    two 2026-08-22 errors seeded back, which is the proof the task asked for."""
    doc = "\n".join(["# fixture", "", "```bash", TAG_COMMAND, COUNT_COMMAND, "```", "",
                     "| Version | Date | Tasks | What it is remembered for |",
                     "| :--- | :--- | ---: | :--- |",
                     "| `0.2.4` | 2026-08-14 | 2 | nothing an adopter loads |",
                     "| `0.5.0` | 2026-08-20 | 30 | the release an outside build wrote |", ""])
    tags = {"0.2.4": "2026-08-14", "0.5.0": "2026-08-20"}
    counts = Counter({"0.2.4": 2, "0.5.0": 30, "unreleased": 8})

    def fail(msg):
        sys.exit("SELF-TEST FAILED: " + msg)

    if stated_commands(doc) != (True, True):
        fail("the fixture's fence names both commands and they were not both found")
    if stated_commands(doc.replace(COUNT_COMMAND, "wc -l tasks/*.md")) != (True, False):
        fail("a fence naming a different count command was still read as naming the document's")
    table = rows(doc)
    if [r[1:] for r in table] != [("0.2.4", "2026-08-14", "2"), ("0.5.0", "2026-08-20", "30")]:
        fail("the two release rows were read as %r" % (table,))
    if compare(table, tags, counts):
        fail("a table that agrees with both commands produced %r" % (compare(table, tags, counts),))

    # The two errors of 2026-08-22, seeded back one at a time.
    got = compare(rows(doc.replace("| 30 |", "| 14 |")), tags, counts)
    if len(got) != 1 or "`0.5.0` counts 14" not in got[0] or "answers 30" not in got[0]:
        fail("0.5.0 seeded to 14 against 30 produced %r - the eight-short row of 2026-08-22" % (got,))
    got = compare(rows(doc.replace("| 2 |", "| 1 |")), tags, counts)
    if len(got) != 1 or "`0.2.4` counts 1" not in got[0]:
        fail("0.2.4 seeded to 1 against 2 produced %r" % (got,))

    got = compare(rows(doc.replace("2026-08-20", "2026-08-21")), tags, counts)
    if len(got) != 1 or "dated 2026-08-21" not in got[0] or "creatordate is 2026-08-20" not in got[0]:
        fail("a date one day off its tag produced %r" % (got,))
    got = compare(table, {"0.2.4": "2026-08-14"}, counts)
    if len(got) != 1 or "no tag `v0.5.0`" not in got[0]:
        fail("a row with no tag produced %r - it must fail rather than pass quietly" % (got,))
    got = compare(table, dict(tags, **{"0.6.0": "2026-08-22"}), counts)
    if len(got) != 1 or "tag `v0.6.0`" not in got[0] or "no row" not in got[0]:
        fail("a tag with no row produced %r" % (got,))
    got = compare(table, tags, Counter(counts, **{"0.6.0": 20}))
    if len(got) != 1 or "`shipped_in: 0.6.0`" not in got[0] or "20 task" not in got[0]:
        fail("a version the records carry with no row produced %r" % (got,))
    if compare(table, tags, Counter(counts, **{"unreleased": 9})):
        fail("`unreleased` was read as a version owing a row")

    # Quiet never hides a failure (T-286). The decision is one function so it can be asserted
    # without a red history to run against.
    if emit("FULL", 1, "line", True) != "FULL":
        fail("a red run under --quiet printed the one-line form; quiet decides how a GREEN run "
             "reads and nothing else")
    if emit("FULL", 0, "line", True) != "line\n" or emit("FULL", 0, "line", False) != "FULL":
        fail("the green form did not follow the quiet flag")

    class _Stream(object):
        def __init__(self, tty):
            self._tty = tty

        def isatty(self):
            return self._tty
    if (quiet_wanted([], _Stream(False)) is not True or quiet_wanted([], _Stream(True)) is not False
            or quiet_wanted(["--report"], _Stream(False)) is not False
            or quiet_wanted(["--quiet"], _Stream(True)) is not True):
        fail("the quiet default did not follow the terminal, --report and --quiet as documented")
    return True


def quiet_wanted(argv, stdout=None):
    """Whether a green run prints one line (T-286). `--report` says no and `--quiet` says yes,
    outright; otherwise a terminal gets the account and anything else gets the line."""
    if "--report" in argv:
        return False
    if "--quiet" in argv:
        return True
    stdout = sys.stdout if stdout is None else stdout
    return not (hasattr(stdout, "isatty") and stdout.isatty())


def emit(full, code, line, quiet):
    """The text a run prints: the whole account on a red run or a watched one, the line otherwise.
    `code` is consulted before `quiet` - a quiet mode that hid a failure would be worse than the
    report it replaces."""
    return full if code or not quiet else line + "\n"


def main(argv):
    self_test()
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code, line = account()
    sys.stdout.write(emit(buf.getvalue(), code, line, quiet_wanted(argv)))
    return code


def account():
    """Print the whole partition; `(exit code, the one-line form of it)`."""
    text = io.open(HISTORY, encoding="utf-8").read()
    rel = os.path.relpath(HISTORY, ROOT).replace(os.sep, "/")
    print("Release chronology - %s\n" % rel)

    bad = []
    tag_named, count_named = stated_commands(text)
    if not tag_named:
        bad.append("the document no longer names %r in a fence, so the date column's derivation "
                   "is not the one this checker implements" % TAG_COMMAND)
    if not count_named:
        bad.append("the document no longer names %r in a fence, so the task column's derivation "
                   "is not the one this checker implements" % COUNT_COMMAND)
    table = rows(text)
    if not table:
        bad.append("no release row found - a table with nothing to compare is not a pass")

    tags, counts = tag_dates(ROOT), shipped_counts(TASKS)
    unreleased = sum(n for v, n in counts.items() if not VERSION.match(v))
    bad.extend(compare(table, tags, counts))

    print("  %-18s %3d   = every `x.y.z` row of the table" % ("rows compared", len(table)))
    print("  %-18s %3d   from %s" % ("tags", len(tags), TAG_COMMAND))
    print("  %-18s %3d   from %s, plus %d record(s) not shipped in any"
          % ("versions in tasks", sum(1 for v in counts if VERSION.match(v)), COUNT_COMMAND, unreleased))
    print("  %-18s %3d" % ("FAILING", len(bad)))
    for line in bad:
        print("    FAILING  %s" % line)
    line = ("chronology: %d row(s) agree with both commands, %d tag(s), %d version(s) in tasks, "
            "%d FAILING" % (len(table), len(tags), sum(1 for v in counts if VERSION.match(v)),
                            len(bad)))
    if bad:
        print("\n%d disagreement(s) between the table and the commands the document names." % len(bad))
        return 1, line
    print("\nOK - %d row(s) agree with both commands, in both directions.\n"
          "     this checks that the two derived columns match what derives them. It cannot tell you\n"
          "     a release should have been cut, or what a row is remembered for." % len(table))
    return 0, line


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
