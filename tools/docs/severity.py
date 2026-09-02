#!/usr/bin/env python3
"""Hold the pre-release audit's severity table to the register's own rows.

    python tools/docs/severity.py            # the verdict, and one line when it is green
    python tools/docs/severity.py --report   # the partition even when piped; --quiet is the reverse

**A green run prints one line when stdout is not a terminal** (T-286): an agent pays a tool's output
again on every later turn, and a green partition is a report nobody acts on. `--report` restores it,
`--quiet` forces the line at a terminal, and a red run prints everything in every mode.

**Why this file exists.** `T-219` section 3 states `High`, `Medium` and `Low` against `Raised`,
`Tasked`, `Accepted` and `Open`, and every one of those twelve cells is a fold over rows the register
already holds. Nothing connected the two. Measured 2026-08-29 by `PR-110`: the table read
`High 8, Medium 63, Low 34` where the register held `High 8, Medium 64, Low 35` - and **the error was
already there before the cycle that last reconciled it**, so a cycle that added its own findings
accurately is exactly what carried it forward. That is **L-136** turned on the run's own findings
table: a count with no membership cannot be audited, and its errors cancel instead of showing.

**The one judgement a script cannot take is what a struck rank means**, which `PR-110` says out loud.
It is taken here, once, and stated rather than inferred:

  - a **withdrawn** row was never a finding - its id is spent and its statement stands as a record -
    so it is not `Raised`. Two rows are withdrawn and the run's own log counts them out the same way;
  - a **closed** row was raised and answered, so it is `Raised` and not `Open`. Its rank cell is
    struck through, which is the only marker section 3 defines;
  - an **accepted** row is `Raised`, `Accepted` and not `Open`, and section 4 carries it. The two
    counts are compared against each other here, which is the second binding and costs nothing.

**Three rows struck their id instead of their rank** until 2026-09-02 - a second convention the
document never declared, and one no count over this table could read. They were normalised in the
same batch; the parser refuses a struck id rather than tolerating it, so it cannot fork again.

Runs its own self-test first and refuses to report if it fails (**L-04**). Runs from anywhere: the
project root is derived from this file, not from the working directory. Pure standard library
(**L-07**).
"""

import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REGISTER = os.path.join(ROOT, "docs", "PRE-RELEASE-AUDIT.md")
RECORD = os.path.join(ROOT, "tasks",
                      "T-219-pre-release-audit-of-the-whole-repository.md")

BANDS = ("High", "Med", "Low")
# What the record's table calls each band. The register writes `Med`; the table writes `Medium`.
LABEL = {"High": "High", "Med": "Medium", "Low": "Low"}
COLUMNS = ("Raised", "Tasked", "Accepted", "Open")

# **Anchored on a sentence, not on a line number** - a missing anchor is an error rather than an
# empty result, which is the failure `findings.py` names in its own header.
FINDINGS_ANCHOR = "## 3. The ranked findings"
ACCEPTED_ANCHOR = "## 4. Accepted without action"
COUNTS_ANCHOR = "**Findings raised**"

ROW = re.compile(r"^\|\s*(~~)?`(PR-\d+)`(~~)?\s*\|")


def read(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def section(text, anchor, path):
    """Everything from `anchor` to the next `## ` heading."""
    i = text.find(anchor)
    if i < 0:
        sys.exit("%s no longer contains %r - this file's anchor is stale, not the document"
                 % (os.path.basename(path), anchor))
    j = text.find("\n## ", i + len(anchor))
    return text[i: j if j > 0 else len(text)]


def rows(text):
    """`(id, band, tasked, state)` for every finding row in section 3."""
    out = []
    for line in section(text, FINDINGS_ANCHOR, REGISTER).splitlines():
        m = ROW.match(line)
        if not m:
            continue
        if m.group(1) or m.group(3):
            sys.exit("%s strikes the ID of %s. Section 3 strikes the RANK cell and nothing else; a "
                     "struck id reads as open to every count over this table"
                     % (os.path.basename(REGISTER), m.group(2)))
        cells = [c.strip() for c in line.split("|")]
        band = cells[3].replace("~", "").replace("*", "").strip()
        if band not in BANDS:
            sys.exit("%s: %s has rank %r, which is not one of %s"
                     % (os.path.basename(REGISTER), m.group(2), band, ", ".join(BANDS)))
        task, status = cells[-3], cells[-2]
        low = status.lower().lstrip("*")
        state = ("withdrawn" if low.startswith("withdrawn") else
                 "accepted" if low.startswith("accepted") else
                 "open" if low == "open" else "closed")
        out.append((m.group(2), band, "](../tasks/T-" in task, state))
    if not out:
        sys.exit("%s: section 3 holds no finding row - the parser and the document disagree"
                 % os.path.basename(REGISTER))
    return out


def derived(found):
    """`{band: (raised, tasked, accepted, open)}`, and the ids the rows mark accepted."""
    table, accepted = {}, []
    for band in BANDS:
        live = [r for r in found if r[1] == band and r[3] != "withdrawn"]
        table[band] = (len(live),
                       len([r for r in live if r[2]]),
                       len([r for r in live if r[3] == "accepted"]),
                       len([r for r in live if r[3] == "open"]))
        accepted += [r[0] for r in live if r[3] == "accepted"]
    return table, accepted


def accepted_rows(text):
    """The ids section 4 carries. `*none*` is a legal empty state, not a parse failure."""
    out = []
    for line in section(text, ACCEPTED_ANCHOR, REGISTER).splitlines():
        m = re.match(r"^\|\s*`?(PR-\d+)`?\s*\|", line)
        if m:
            out.append(m.group(1))
    return out


def stated(text):
    """`{band: (raised, tasked, accepted, open)}` as the task record's table states it."""
    out = {}
    for line in section(text, COUNTS_ANCHOR, RECORD).splitlines():
        m = re.match(r"^\|\s*(High|Medium|Low)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|"
                     r"\s*(\d+)\s*\|", line)
        if m:
            band = [b for b in BANDS if LABEL[b] == m.group(1)][0]
            out[band] = tuple(int(m.group(i)) for i in (2, 3, 4, 5))
    if sorted(out) != sorted(BANDS):
        sys.exit("%s: the counts table under %r does not carry one row per band - found %s"
                 % (os.path.basename(RECORD), COUNTS_ANCHOR, ", ".join(sorted(out)) or "none"))
    return out


def self_test():
    """Refuse to run if the parser has stopped agreeing with the documents (**L-04**)."""
    # **The fixture's task cells are assembled rather than written out**, and that is not fussiness:
    # `refcheck.py` resolves every `](path)` in a tracked file, so a plausible link spelled in full
    # here is a dead pointer in the repository and fails the first gate. A self-test may not mint a
    # reference - learned on this file's own first lint.
    link = "[T-%d](.." + "/tasks/T-%d.md)"
    fixture = FINDINGS_ANCHOR + "\n\n| # | Sev |\n| :-- | :--- |\n" + "\n".join([
        "| `PR-01` | a | **Med** | f | e | w | r | s | " + link % (1, 1) + " | **closed** x |",
        "| `PR-02` | a | ~~**High**~~ | f | e | w | r | s | " + link % (2, 2) + " | open |",
        "| `PR-03` | a | ~~**Low**~~ | f | e | w | r | s | - withdrawn, no task | **withdrawn** y |",
        "| `PR-04` | a | **Low** | f | e | w | r | s | - batched | **accepted 2026-09-02** z |",
        "| `PR-05` | a | **Low** | f | e | w | r | s | - none yet | open |",
    ]) + "\n\n## 4. next\n"
    got = rows(fixture)
    if [g[0] for g in got] != ["PR-0%d" % n for n in range(1, 6)]:
        sys.exit("SELF-TEST FAILED: the row parser did not find all five fixture rows: %r" % (got,))
    table, acc = derived(got)
    if table["Med"] != (1, 1, 0, 0):
        sys.exit("SELF-TEST FAILED: a closed row must be raised and tasked and not open: %r"
                 % (table["Med"],))
    if table["High"] != (1, 1, 0, 1):
        sys.exit("SELF-TEST FAILED: a struck rank must not change what a row counts as: %r"
                 % (table["High"],))
    if table["Low"] != (2, 0, 1, 1):
        sys.exit("SELF-TEST FAILED: a withdrawn row must not be raised, and an accepted row must be "
                 "raised and not open: %r" % (table["Low"],))
    if acc != ["PR-04"]:
        sys.exit("SELF-TEST FAILED: the accepted ids came back as %r" % (acc,))
    empty = (ACCEPTED_ANCHOR + "\n\n| # | Reason | Date |\n| :-- | :--- | :--- |\n"
             "| | *none* | |\n\n## 5. next\n")
    if accepted_rows(empty):
        sys.exit("SELF-TEST FAILED: an empty section 4 must read as no accepted row")
    one = ACCEPTED_ANCHOR + "\n\n| `PR-04` | because | 2026-09-02 |\n\n## 5. x\n"
    if accepted_rows(one) != ["PR-04"]:
        sys.exit("SELF-TEST FAILED: section 4's own rows did not parse")
    counts = (COUNTS_ANCHOR + "\n\n| Severity | Raised | Tasked | Accepted | Open |\n"
              "| :--- | ---: | ---: | ---: | ---: |\n| High | 1 | 1 | 0 | 1 |\n"
              "| Medium | 2 | 2 | 0 | 0 |\n| Low | 3 | 0 | 1 | 2 |\n")
    if stated(counts)["Low"] != (3, 0, 1, 2):
        sys.exit("SELF-TEST FAILED: the record's counts table did not parse")


def main(argv):
    self_test()
    found = rows(read(REGISTER))
    table, acc_ids = derived(found)
    says = stated(read(RECORD))
    section4 = accepted_rows(read(REGISTER))

    problems = []
    for band in BANDS:
        for k, column in enumerate(COLUMNS):
            if table[band][k] != says[band][k]:
                problems.append("%s %s: the register holds %d, T-219 section 3 states %d"
                                % (LABEL[band], column, table[band][k], says[band][k]))
    if sorted(acc_ids) != sorted(section4):
        problems.append("section 4 carries %s and the rows marked accepted are %s"
                        % (", ".join(sorted(section4)) or "nothing",
                           ", ".join(sorted(acc_ids)) or "nothing"))

    loud = bool(problems) or "--report" in argv or (sys.stdout.isatty() and "--quiet" not in argv)
    if loud:
        print("%-9s %8s %8s %9s %6s" % (("Severity",) + COLUMNS))
        for band in BANDS:
            print("%-9s %8d %8d %9d %6d" % ((LABEL[band],) + table[band]))
        print("\n  %d finding row(s); %d withdrawn and counted out of Raised"
              % (len(found), len([r for r in found if r[3] == "withdrawn"])))
        print("")
    if problems:
        for p in problems:
            print("  %s" % p)
        print("\nThe register is the count's one home and T-219 section 3 is a view of it. "
              "Re-derive the cells; never increment them.")
        return 1
    print("OK - T-219 section 3's twelve cells agree with the register's %d rows, and section 4 "
          "carries every accepted one." % len(found))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
