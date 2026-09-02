#!/usr/bin/env python3
"""Check that no blank line splits a Markdown table in a tracked document.

    python tools/docs/tables.py

Markdown ends a table at a blank line. So one empty line between two data rows does not break
anything visibly - it **splits the table in two**, and the first row after the gap is drawn as the
**column headings** of the second, its cells promoted out of the body and the row itself gone from
the rendering. The rows below it are then listed under headings that are prose about something else.

**Nothing here could see it, and that is the point of a separate tool.** Every other checker over
these documents counts cells *inside* a table or resolves what a cell says; a blank line simply ends
the table, so the rows on either side of it stay well-formed and every count still adds up.
`refcheck.py` still resolves the links in the orphaned rows. `figures.py` still binds their numerals.
The defect lives in the boundary between two tables, which is the one place none of them looks.

**Raised as `PR-16`**, against `docs/PUBLISHING.md` section 8.1 - the release-requirements table an
adopter reads before upgrading and step 7 copies into a release note verbatim, where a single empty
line put nine of twelve rows under a heading made out of the `0.2.3` row. The register's remedy asked
whether the durable half was worth a tool; **it is, and the measurement is why**: the same defect was
sitting in three more places nobody had looked, two of them in `docs/RELEASE-PHASES.md`'s own phase
tables. One reported instance was four (T-237, 2026-09-02).

**A blank line between two tables is legal and common**, so the check is not *a blank line between
two rows*. What separates the two cases is what follows: a table that genuinely starts after the gap
opens with a header **and its delimiter row**, `| :--- | :--- |`. Where that delimiter is there, this
is two tables and the file is right. Where it is absent, the rows below the gap have no headings of
their own and are being drawn under a promoted data row.

Runs its own self-test first and refuses to report if it fails (**L-04**). Pure standard library
(**L-07**).
"""

import os
import re
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ROW = re.compile(r"^\s*\|.*\|\s*$")
DELIM = re.compile(r"^\s*\|[\s:|-]+\|\s*$")


def tracked():
    """Every tracked Markdown file, from git rather than a walk - untracked scratch is not ours."""
    out = subprocess.run(["git", "ls-files", "*.md"], cwd=ROOT,
                         capture_output=True, text=True, check=True).stdout
    return [p for p in out.split("\n") if p.strip()]


def splits(lines):
    """Line numbers (1-based) of blank lines that split one table rather than separating two."""
    found = []
    for i, line in enumerate(lines):
        if line.strip():
            continue
        before, after = i - 1, i + 1
        if before < 0 or after >= len(lines):
            continue
        if not (ROW.match(lines[before]) and ROW.match(lines[after])):
            continue
        # A genuinely new table opens with a header and then its delimiter row. Where the line
        # after the gap is followed by one, this is two tables and the blank line belongs there.
        if after + 1 < len(lines) and DELIM.match(lines[after + 1]):
            continue
        found.append(i + 1)
    return found


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as handle:
        return handle.read().split("\n")


def self_test():
    intact = ["| A | B |", "| :-- | :-- |", "| 1 | 2 |", "| 3 | 4 |", "", "prose"]
    if splits(intact):
        sys.exit("SELF-TEST FAILED: a blank line after the last row of a table was reported. That "
                 "is where a table is supposed to end")

    broken = ["| A | B |", "| :-- | :-- |", "| 1 | 2 |", "", "| 3 | 4 |", "| 5 | 6 |"]
    if splits(broken) != [4]:
        sys.exit("SELF-TEST FAILED: a blank line between two data rows raised %r, not [4]. This is "
                 "the defect the tool exists for - the `| 3 | 4 |` row becomes column headings"
                 % (splits(broken), ))

    adjacent = ["| A | B |", "| :-- | :-- |", "| 1 | 2 |", "", "| C | D |", "| :-- | :-- |",
                "| 3 | 4 |"]
    if splits(adjacent):
        sys.exit("SELF-TEST FAILED: two tables separated by a blank line were reported as one "
                 "broken table. The delimiter row under the second header is what tells them apart")

    header_gap = ["| A | B |", "", "| :-- | :-- |", "| 1 | 2 |"]
    if splits(header_gap) != [2]:
        sys.exit("SELF-TEST FAILED: a blank line between a header and its delimiter raised %r, not "
                 "[2]. The table renders as prose from there down" % (splits(header_gap), ))
    return True


def report():
    bad = []
    for path in tracked():
        for line in splits(read(path)):
            bad.append((path, line))

    print("Split tables - a blank line inside a Markdown table, over every tracked *.md\n")
    for path, line in bad:
        print("  SPLIT      %s:%d   the row below this blank line renders as column headings"
              % (path, line))

    print("\n  %d tracked Markdown file(s) read" % len(tracked()))
    print("\n%s" % ("%d split table(s) to fix - delete the blank line" % len(bad) if bad else
                    "0 split tables - no blank line interrupts a table in a tracked document"))
    print("\nThis reads table boundaries and nothing inside one. A table whose cells are wrong, or\n"
          "whose row belongs to another release, is every other checker's subject and not this.")
    return 1 if bad else 0


if __name__ == "__main__":
    self_test()
    sys.exit(report())
