#!/usr/bin/env python3
"""Check that every closed task carries `shipped_in`.

    python tools/tasks/shipped.py

`tasks/TASK-WORKFLOW.md` section 3: *`shipped_in` is set at close*, and holds `unreleased` until
there is a version. **Nothing asked for it.** `shipped_in` is a carried field by this project's own
`.taskmd/config.md` - deliberately outside the schema's vocabularies, because the values are version
strings and no enumeration can hold them - so `taskmd check` validates every enumerated field and
never this one. A task could close without it and every gate stayed green.

**The consequence is not cosmetic, and it is not about the record being tidy.** A task with no
`shipped_in` is selected by nothing: the chronology counts by version, the audit's cycle 7 selects
the unreleased work by open status or `shipped_in: unreleased`, and a record carrying neither falls
into the band the method calls *the settled record*. Work closed yesterday gets scheduled to be read
as history.

**Raised as `PR-27`**, which named two records - and the project had already written the same defect
down twice before that, in `RELEASE-HISTORY.md` section 1: eight tasks closed 2026-08-19 *carrying no
`shipped_in` at all*, and `T-187` in `0.6.0`, *which is how it nearly missed the set*. Back-filling
was the fix all three times and the defect came back all three times, because nothing new was
watching. On the day this was written the two reported records were **44** (T-238, 2026-09-02).

Runs as the fifth step of `tools/tasks/lint.py`, which is what a closure runs. Its own self-test
first (**L-04**). Pure standard library (**L-07**).
"""

import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TASKS = os.path.join(ROOT, "tasks")

CLOSED = ("done", "cancelled")
STATUS = re.compile(r"^status:\s*(\S+)\s*$", re.M)
SHIPPED = re.compile(r"^shipped_in:\s*(\S.*?)\s*$", re.M)


def missing(records):
    """The ids of closed records carrying no `shipped_in`, in file order.

    `records` is an iterable of `(id, front-matter text)`. An open task is not asked for the field:
    the rule is *set at close*, so demanding it earlier would make every new task fail.
    """
    bad = []
    for name, text in records:
        status = STATUS.search(text)
        if not status or status.group(1) not in CLOSED:
            continue
        if not SHIPPED.search(text):
            bad.append(name)
    return bad


def records():
    for name in sorted(os.listdir(TASKS)):
        if not re.match(r"^T-\d+.*\.md$", name):
            continue
        with open(os.path.join(TASKS, name), encoding="utf-8") as handle:
            # The front matter is the whole subject; a `status:` line in the body is prose.
            head = handle.read().split("\n---", 2)
            yield name.split("-")[0] + "-" + name.split("-")[1], head[0]


def self_test():
    if missing([("T-001", "status: done\nshipped_in: 0.6.0")]):
        sys.exit("SELF-TEST FAILED: a closed task carrying the field was reported")
    if missing([("T-001", "status: in_progress")]) or missing([("T-001", "status: proposed")]):
        sys.exit("SELF-TEST FAILED: an open task was asked for `shipped_in`. The rule is *set at "
                 "close* - asking earlier would fail every task the moment it is created")
    if missing([("T-001", "status: done")]) != ["T-001"]:
        sys.exit("SELF-TEST FAILED: a closed task with no `shipped_in` raised nothing. That is the "
                 "whole defect - it has recurred three times because nothing asked")
    if missing([("T-001", "status: cancelled")]) != ["T-001"]:
        sys.exit("SELF-TEST FAILED: `cancelled` was treated as open. A cancelled task is closed and "
                 "is counted by the same selections a done one is")
    if missing([("T-001", "status: done\nshipped_in: unreleased")]):
        sys.exit("SELF-TEST FAILED: `unreleased` was not accepted. It is what the field holds until "
                 "there is a version, which is most of the tree between releases")
    return True


def report():
    bad = missing(records())
    print("shipped_in - every closed task carries it (`PR-27`)\n")
    for name in bad:
        print("  MISSING    %s   closed with no `shipped_in`; set the version, or `unreleased`"
              % name)
    print("\n%s" % ("%d closed task(s) missing the field" % len(bad) if bad else
                    "0 missing - every closed task carries `shipped_in`"))
    return 1 if bad else 0


if __name__ == "__main__":
    self_test()
    sys.exit(report())
