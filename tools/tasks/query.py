#!/usr/bin/env python3
"""The three questions a session asks the tracker, answered without reading the board.

    python tools/tasks/query.py list --open --limit 1   # what to work on next
    python tools/tasks/query.py context T-131           # everything one task needs
    python tools/tasks/query.py next                    # the id the next task takes

**It exists because the board is generated for people and read by agents.** `tasks/README.md` is
33,676 bytes and answers *what next* only by being read whole; `list --open` answers it in 1,901 and
`context` answers one task in 790 - 17.7x and 42x, measured 2026-08-13. The tracker shipped both
commands all along. What stopped them being used is that the bare `taskmd` command does not resolve
in an agent shell, which is the obstacle `tools/tasks/lint.py` was written for; this is a second
entry point through the same door (`CE-02`).

**That is the harness, not the plugin** - taskmd ships `bin/taskmd` and it runs when invoked
directly, but the shell snapshot's `PATH` line is truncated mid-value and loses every plugin's
`bin/` (T-140, **L-87**). Locating the skill ourselves is the right answer either way, because it
does not depend on a `PATH` that cannot be relied on.

**It refuses `index` and `check` by name.** `lint.py` chains those two with `refcheck.py` and stops
at the first failure. A second way to run half of that chain is exactly the duplicate this tool
exists to avoid (**L-13**), so the refusal names the tool that owns them rather than being silent.

**`next` is here because the refusal was standing where the question gets asked** (`PR-20`). The
opening checklist's first step is *take the next ID from `taskmd index`*, and the substitute pair
drops exactly that line: `lint.py` runs the index and prints `Wrote tasks/README.md - N active, M
closed`, with no id in it. So an agent opening a task took the number from a directory listing
instead - demonstrated, not argued, by the session that took `T-223` that way. It is computed here
rather than passed to taskmd for two reasons that both matter: the answer is needed **before** the
task file exists, and `taskmd index` earns its number by **rewriting the board**, which is a write in
the middle of a read-only question.

**The locator is imported, not copied.** Finding the installed skill, and refusing when there is
none, both live in `lint.py` and are called from here - so a plugin update that moves the skill
breaks neither tool, and the assertion that a version bump sorts correctly is in that file's
self-test, which runs on every invocation of it.

`list` and `context` are taskmd's own commands. Every argument after the command name is passed
through untouched, which is why this file does not describe them and cannot go stale about them.
`next` is the exception and is answered here, from the task directory.

Runs from anywhere: the project root comes from `lint.py`, not from the working directory.
Pure standard library (**L-07**).
"""

import os
import re
import subprocess
import sys

# The script's own directory is on `sys.path`, which is how the locator keeps one home.
import lint

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

QUERIES = ("list", "context")
LOCAL = ("next", )

# Commands this deliberately does not offer, and the tool that owns each.
ELSEWHERE = {
    "index": "python tools/tasks/lint.py",
    "check": "python tools/tasks/lint.py",
}

USAGE = """usage: python tools/tasks/query.py {list,context,next} [args...]

  list [--<field> V] [--open|--closed] [--limit N] [--json]
  context T-NNN
  next

Arguments after `list` and `context` go to taskmd unchanged. `next` is answered here.
`index` and `check` are run by `python tools/tasks/lint.py`, which chains them with the
reference check."""

ID = re.compile(r"^T-(\d+)", re.M)


def next_id(names=None):
    """The id the next task takes: one past the highest in `tasks/`, never a gap refilled.

    From the file names rather than from the front-matter, because both are held to each other by
    `taskmd check` and one of them can be read without opening 250 files.
    """
    if names is None:
        names = os.listdir(os.path.join(lint.ROOT, "tasks"))
    seen = [int(m.group(1)) for m in (ID.match(n) for n in names) if m]
    return "T-%03d" % (max(seen) + 1) if seen else "T-001"


def self_test():
    if next_id(["T-001-a.md", "T-009-b.md", "T-010-c.md"]) != "T-011":
        sys.exit("SELF-TEST FAILED: the next id is not one past the highest")
    if next_id(["T-001-a.md", "T-003-c.md"]) != "T-004":
        sys.exit("SELF-TEST FAILED: a gap was refilled. An id is never reused - 872 citations across "
                 "this tree resolve by number, and a second T-002 would answer for the first")
    if next_id(["README.md", "TOOLING.md", "_task-template.md"]) != "T-001":
        sys.exit("SELF-TEST FAILED: the directory's non-task files were counted, or an empty "
                 "tracker did not start at T-001")
    if next_id(["T-9-short.md", "T-100-long.md"]) != "T-101":
        sys.exit("SELF-TEST FAILED: ids were compared as text rather than as numbers")
    return True


def query(argv):
    """Run one taskmd query with the installed skill on `PYTHONPATH`. Its exit code, its output.

    Output is inherited rather than captured: the answer *is* what the child prints, and this tool's
    whole purpose is that a session reads that instead of a 33,676-byte file.
    """
    env = dict(os.environ, PYTHONPATH=lint.require_taskmd())
    return subprocess.run([sys.executable, "-m", "taskmd"] + list(argv),
                          cwd=lint.ROOT, env=env).returncode


def main(argv):
    if argv and argv[0] in ("-h", "--help"):
        print(USAGE)
        return 0
    if not argv:
        print(USAGE)
        return 2
    command = argv[0]
    if command in LOCAL:
        print(next_id())
        return 0
    if command in ELSEWHERE:
        print("`%s` is not run from here - use `%s`, which chains it with the checks a task edit "
              "owes and stops at the first failure." % (command, ELSEWHERE[command]))
        # The one thing `index` prints that the substitute drops is the next id, and this
        # refusal is where somebody asking for it is standing (`PR-20`).
        if command == "index":
            print("\nIf the next task id is what you wanted, `python tools/tasks/query.py next` "
                  "answers it without rewriting the board.")
        print("\n%s" % USAGE)
        return 2
    if command not in QUERIES:
        print("unknown command `%s`. This tool answers %s.\n\n%s"
              % (command, " and ".join("`%s`" % q for q in QUERIES), USAGE))
        return 2
    return query(argv)


if __name__ == "__main__":
    self_test()
    sys.exit(main(sys.argv[1:]))
