#!/usr/bin/env python3
"""Which audit finding is which task, and what state is it in - derived, never kept by hand.

    python tools/docs/findings.py           # the listing
    python tools/docs/findings.py --check   # the verdict, and nothing else on a green run

**Why this file exists.** Answering that question once, on 2026-08-14, meant reading
`docs/CONTEXT-AUDIT.md` §6's ranking table, its §6.1 statements, `R8` §8, the §9 candidate table, the
three documents under `docs/upstream/`, and every task file naming a `CE-nn` - **325,695 bytes across
six sources** - and what it produced was one more copy of facts that already existed, correct that day
and stale at the next closure. This is that answer computed instead of written down (T-151).

**Nothing here is a new home for anything.** The findings stay in §6's table, where each row carries
the argument that is the reason it survives a re-read; the tasks stay in the tracker. What was missing
was the *link*, and it now lives in one place: a `finding: CE-nn` field in the task's front matter.
`.taskmd/config.md` carries a field it does not name without interpreting it, which is the same
mechanism `shipped_in` has been running on since 2026-08-12, so the schema needed no vocabulary row.

**Two structural markers do the work, and neither was invented for this file:**

  - **a struck-through rank cell** (`~~10~~`) in §6 means the finding is closed;
  - **an Effort cell ending in `each`** means the band is **per item**, so a closed row is not a
    finished subject. `CE-04` is banded `xs each` and had a second task raised against it after its
    row closed. `docs/CONTEXT-AUDIT.md` §9 said nothing in the table marked per-item bands; the cell
    already did, and this file is what reads it.

**It fails in both directions** (**L-74**), which is the whole point of writing it rather than
eyeballing: a finding whose row reads closed while open work names it, a finding whose row still reads
open when every task on it is finished, and a task naming a finding that does not exist all stop the
run. A check that catches one direction is trusted for catching neither.

**The execution order is the same defect in a different shape.** `docs/RELEASE-PHASES.md` numbers its
rows and five of its notes used to cite those numbers, so an insertion cascaded into the prose - four
hand renumbering passes in two days. The notes cite task ids now, and what is left is checked here:
the open rows are a consecutive `1..n`, every id resolves to a task, and a row's form agrees with its
task's status.

**A finding with no task is reported, not failed.** Every one has a task today, and a finding raised
before its task exists is a legal state rather than drift.

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

AUDIT = os.path.join(ROOT, "docs", "CONTEXT-AUDIT.md")
PHASES = os.path.join(ROOT, "docs", "RELEASE-PHASES.md")
CONFIG = os.path.join(ROOT, ".taskmd", "config.md")
TASKS = os.path.join(ROOT, "tasks")

# Where each table starts. **Anchored on a sentence, and a missing anchor is an error** - a checker
# that quietly found no table would report a green run over nothing, which is the failure mode every
# gate in this repository is written against.
FINDINGS_ANCHOR = "## 6. The ranked findings"
ORDER_ANCHOR = "**The execution order"

STRUCK = re.compile(r"^~~(.*)~~$")
PER_ITEM = re.compile(r"\beach\b")
SEPARATOR = re.compile(r"^:?-+:?$")
TASK_ID = re.compile(r"\bT-\d{3}\b")
FINDING_ID = re.compile(r"\bCE-\d\d\b")
# A rank cell is a number, a `A-B` span (en dash in the document, hyphen tolerated), or neither.
RANK = re.compile(r"^(\d+)(?:[–-](\d+))?$")


# --- reading --------------------------------------------------------------------------------

def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def rows_after(text, anchor, path):
    """Every row of the first Markdown table following `anchor`, as lists of stripped cells.

    Separator rows are dropped and the header is left in - callers key on the cells they need
    rather than on a column count, so a column added to either table does not break this.
    """
    start = text.find(anchor)
    if start < 0:
        sys.exit("%s: no table anchored at %r. This file locates both tables by a sentence in the\n"
                 "  document; if that sentence was reworded, reword the anchor here in the same\n"
                 "  commit. A checker that found no table would report success over nothing."
                 % (os.path.relpath(path, ROOT), anchor))
    found, seen_table = [], False
    for line in text[start:].splitlines():
        line = line.strip()
        if not line.startswith("|"):
            if seen_table:
                break
            continue
        seen_table = True
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(SEPARATOR.match(c) for c in cells if c):
            continue
        found.append(cells)
    return found


def open_statuses():
    """The open half of the status vocabulary, read from the schema rather than copied here.

    `.taskmd/config.md` is the authority on the fields (**L-08**); a second copy of this list would
    disagree with it the first time somebody added a status to one of them.
    """
    match = re.search(r"^open_statuses:\s*\[(.+?)\]", read(CONFIG), re.M)
    if not match:
        sys.exit(".taskmd/config.md: no `open_statuses` key. That file is the authority on the "
                 "status vocabulary and this tool reads it rather than keeping a second copy.")
    return set(v.strip() for v in match.group(1).split(","))


def tasks():
    """`{task id: (status, finding or None)}` over every task file."""
    found = {}
    for name in sorted(os.listdir(TASKS)):
        if not (name.startswith("T-") and name.endswith(".md")):
            continue
        head = read(os.path.join(TASKS, name)).split("\n---", 1)[0]
        fields = dict(re.findall(r"^(\w+):[ \t]*(.*)$", head, re.M))
        found[name[:5]] = (fields.get("status", ""), fields.get("finding") or None)
    return found


def findings(text):
    """`[(id, closed, per_item, family, gain, effort, title)]` from §6's ranking table."""
    found = []
    for cells in rows_after(text, FINDINGS_ANCHOR, AUDIT):
        if len(cells) < 6:
            continue
        ident = FINDING_ID.search(cells[1])
        if not ident:
            continue
        found.append((ident.group(0),
                      bool(STRUCK.match(cells[0])),
                      bool(PER_ITEM.search(cells[5])),
                      cells[2],
                      cells[4],
                      cells[5],
                      title(cells[3])))
    return found


def title(cell):
    """The finding's one-line name: the What cell up to where its status commentary starts.

    ` - **` is where every closed row turns from what the finding is into what became of it, and
    that is a construction rather than a word - the same reasoning `figures.py` gives for binding on
    a claim's shape instead of its vocabulary.
    """
    head = re.split(r"\s[—-]\s\*\*", cell)[0]
    head = re.sub(r"[`*~]", "", head).strip()
    return head if len(head) <= 62 else head[:59].rsplit(" ", 1)[0] + "..."


def order(text):
    """`[(low, high, [task ids], done_row)]` for the execution order, in document order.

    `low`/`high` are `None` on a row that carries no number - the `-` rows above the table's live
    part, and the `**next**` row.
    """
    found = []
    for cells in rows_after(text, ORDER_ANCHOR, PHASES):
        if len(cells) < 2:
            continue
        ids = TASK_ID.findall(cells[1])
        if not ids:
            continue
        span = RANK.match(re.sub(r"[`*~ ]", "", cells[0]))
        low = int(span.group(1)) if span else None
        high = int(span.group(2)) if span and span.group(2) else low
        found.append((low, high, ids, "done" in cells[1] or "cancelled" in cells[1]))
    return found


# --- the checks -----------------------------------------------------------------------------

def link(register, task_map, opens):
    """`(rows, problems)` - the finding listing, and everything wrong with it.

    `rows` is one tuple per finding: id, closed, per_item, family, gain, effort, title, and the
    tasks naming it as `[(id, status, open)]`.
    """
    serving = {}
    problems = []
    known = set(ident for ident, _, _, _, _, _, _ in register)

    for task, (status, finding) in sorted(task_map.items()):
        if not finding:
            continue
        if finding not in known:
            problems.append("%s names finding %s, which is not in CONTEXT-AUDIT.md section 6. "
                            "Either the id is wrong or the row was removed without its task."
                            % (task, finding))
            continue
        serving.setdefault(finding, []).append((task, status, status in opens))

    rows = []
    for ident, closed, per_item, family, gain, effort, name in register:
        served = serving.get(ident, [])
        rows.append((ident, closed, per_item, family, gain, effort, name, served))
        if not served:
            continue
        still_open = [t for t, _, is_open in served if is_open]
        if closed and still_open and not per_item:
            problems.append("%s reads closed in section 6 and %s is still open. Strike the rank "
                            "cell only when the work is finished, or band the finding per item if "
                            "it closes per instance." % (ident, ", ".join(still_open)))
        if not closed and not still_open:
            problems.append("%s reads open in section 6 and every task on it is finished (%s). "
                            "Strike its rank cell." % (ident, ", ".join(t for t, _, _ in served)))
    return rows, problems


def check_order(rows, task_map, opens):
    """Everything wrong with the execution order: the numbering, the ids, and each row's form."""
    problems = []
    seen = []
    for low, high, ids, done_row in rows:
        for task in ids:
            if task not in task_map:
                problems.append("the execution order names %s, which has no task file." % task)
                continue
            is_open = task_map[task][0] in opens
            # **Every live row, not only the numbered ones.** The `next` row carries no number and
            # a finished task sitting in it is the same drift - it was the state T-151 itself was
            # in the moment it closed, and a rule keyed on the number would have missed it.
            if not done_row and not is_open:
                problems.append("%s holds a live row in the execution order and its status is "
                                "%s. A finished task's row folds to two cells."
                                % (task, task_map[task][0]))
            if done_row and is_open:
                problems.append("%s is struck through in the execution order and its status is %s."
                                % (task, task_map[task][0]))
        if low is None:
            continue
        # **A single number holding several tasks is a shared cell and is legal** - it is what the
        # document reaches for instead of a renumbering pass, and it is why T-148 and T-152 share
        # position 2. A *span* is the other thing: `10-12` claims three positions and owes three
        # tasks, or the numbering after it is wrong by the difference.
        if low != high and high - low + 1 != len(ids):
            problems.append("the execution order's row %d-%d spans %d positions and names %d "
                            "task(s)." % (low, high, high - low + 1, len(ids)))
        seen.extend(range(low, high + 1))

    want = list(range(1, len(seen) + 1))
    if seen != want:
        problems.append("the execution order's numbers read %s, wanted a consecutive 1..%d. The "
                        "numbers are position and nothing else - no note cites them."
                        % (compress(seen), len(seen)))
    return problems


def compress(numbers):
    """`[1,2,3,5]` as `1-3, 5`, so a numbering complaint is readable at any length."""
    if not numbers:
        return "(none)"
    spans, start, last = [], numbers[0], numbers[0]
    for value in numbers[1:]:
        if value == last + 1:
            last = value
            continue
        spans.append((start, last))
        start = last = value
    spans.append((start, last))
    return ", ".join(str(a) if a == b else "%d-%d" % (a, b) for a, b in spans)


# --- the report -----------------------------------------------------------------------------

def report(rows):
    closed = sum(1 for r in rows if r[1])
    per_item = [r[0] for r in rows if r[2]]
    unlinked = [r[0] for r in rows if not r[7]]

    print("%d findings: %d closed, %d open" % (len(rows), closed, len(rows) - closed))
    for ident, is_closed, is_per_item, family, gain, effort, name, served in rows:
        served_text = ", ".join("%s %s" % (t, s) for t, s, _ in served) or "no task"
        print("  %s %-6s %-9s %-25s %s" % (ident,
                                           "closed" if is_closed else "open",
                                           "%s/%s" % (strip(gain), strip(effort)),
                                           served_text, name))
    if per_item:
        print("\nper-item bands (a closed row is not a finished subject): %s" % ", ".join(per_item))
    if unlinked:
        print("unlinked (reported, not a failure): %s" % ", ".join(unlinked))


def strip(cell):
    """A band cell as its current value.

    **A corrected band keeps its old value struck through** - `CE-07` reads `~~L~~ **S**` and
    `CE-12` reads `~~M~~ **none**` - because §6.2 requires a correction to stay legible in the row.
    Dropping the markup without dropping the struck text would print both, which is a listing that
    says the band is `L S`. The struck span goes first, then the markup. What is left of `CE-06`'s
    is a sentence, so the band is its first clause and the argument stays in the table.
    """
    cell = re.sub(r"~~.*?~~", "", cell)
    cell = re.sub(r"[`*~]", "", cell).split(",")[0]
    return cell.replace(" each", "*").strip() or "-"


# --- the self-test --------------------------------------------------------------------------

def self_test():
    """**Both failing directions and the per-item exception are asserted, not read** (**L-74**,
    **L-78**, **L-85**). The fixtures are synthetic: a test built out of the repository's current
    state would go red on the commit that changes it, and would be asserting today's data rather
    than this file's rules."""
    opens = set(["proposed", "in_progress"])
    register = [("CE-90", True, False, "A", "`L`", "`xs`", "a closed finding"),
                ("CE-91", False, False, "A", "`L`", "`xs`", "an open finding"),
                ("CE-92", True, True, "A", "`M`", "`xs` each", "a per-item finding")]

    good = {"T-901": ("done", "CE-90"), "T-902": ("proposed", "CE-91"),
            "T-903": ("done", "CE-92"), "T-904": ("proposed", "CE-92")}
    _, problems = link(register, good, opens)
    if problems:
        sys.exit("SELF-TEST FAILED: a consistent register reported %r. A green run here would mean "
                 "nothing, and the per-item row is the one CE-04 really is in." % problems)

    _, problems = link(register, {"T-901": ("proposed", "CE-90")}, opens)
    if len(problems) != 1 or "still open" not in problems[0]:
        sys.exit("SELF-TEST FAILED: a closed row with open work reported %r. That is the direction "
                 "this file was written for." % problems)

    _, problems = link(register, {"T-902": ("done", "CE-91")}, opens)
    if len(problems) != 1 or "reads open" not in problems[0]:
        sys.exit("SELF-TEST FAILED: finished work under an open row reported %r. Catching one "
                 "direction and not the other is what L-74 is about." % problems)

    _, problems = link(register, {"T-905": ("proposed", "CE-99")}, opens)
    if len(problems) != 1 or "not in CONTEXT-AUDIT" not in problems[0]:
        sys.exit("SELF-TEST FAILED: a task naming a finding that does not exist reported %r."
                 % problems)

    task_map = {"T-901": ("done", None), "T-902": ("proposed", None), "T-903": ("proposed", None)}
    if check_order([(None, None, ["T-901"], True), (None, None, ["T-902"], False),
                    (1, 1, ["T-903"], False)], task_map, opens):
        sys.exit("SELF-TEST FAILED: a well-formed execution order was reported as broken. The "
                 "unnumbered rows are the `-` history and the `next` row, and both are legal.")

    problems = check_order([(None, None, ["T-901"], False)], task_map, opens)
    if len(problems) != 1 or "live row" not in problems[0]:
        sys.exit("SELF-TEST FAILED: a finished task in the unnumbered `next` row reported %r. That "
                 "row carries no number, so a rule keyed on the number would never see it."
                 % problems)

    problems = check_order([(1, 1, ["T-902"], False), (3, 3, ["T-903"], False)], task_map, opens)
    if len(problems) != 1 or "consecutive" not in problems[0]:
        sys.exit("SELF-TEST FAILED: a gap in the numbering reported %r. The gap is what a hand "
                 "renumbering leaves behind." % problems)

    problems = check_order([(1, 2, ["T-902"], False)], task_map, opens)
    if not any("spans 2 positions" in p for p in problems):
        sys.exit("SELF-TEST FAILED: a span wider than the tasks it names reported %r." % problems)

    if compress([1, 2, 3, 5]) != "1-3, 5":
        sys.exit("SELF-TEST FAILED: the numbering complaint is unreadable, so nobody would act on "
                 "it: %r" % compress([1, 2, 3, 5]))
    return True


# --- entry point ----------------------------------------------------------------------------

def main(argv):
    self_test()
    checking = "--check" in argv

    opens = open_statuses()
    task_map = tasks()
    rows, problems = link(findings(read(AUDIT)), task_map, opens)
    problems += check_order(order(read(PHASES)), task_map, opens)

    if not checking:
        report(rows)
        if not problems:
            return 0
        print()

    if problems:
        for problem in problems:
            print("FAIL  %s" % problem)
        print("\n%d problem(s). The register, the execution order and the tracker disagree; the "
              "most recent verified fact wins." % len(problems))
        return 1
    if checking:
        print("findings: %d linked, %d task(s), execution order consecutive"
              % (len(rows), sum(len(r[7]) for r in rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
