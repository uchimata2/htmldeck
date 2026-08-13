#!/usr/bin/env python3
"""The two questions a session asks the tracker, answered without reading the board.

    python tools/tasks/query.py list --open --limit 1   # what to work on next
    python tools/tasks/query.py context T-131           # everything one task needs

**It exists because the board is generated for people and read by agents.** `tasks/README.md` is
33,676 bytes and answers *what next* only by being read whole; `list --open` answers it in 1,901 and
`context` answers one task in 790 - 17.7x and 42x, measured 2026-08-13. The tracker shipped both
commands all along. What stopped them being used is that the bare `taskmd` command does not resolve
in an agent shell, which is the obstacle `tools/tasks/lint.py` was written for; this is a second
entry point through the same door (`CE-02`).

**It refuses `index` and `check` by name.** `lint.py` chains those two with `refcheck.py` and stops
at the first failure. A second way to run half of that chain is exactly the duplicate this tool
exists to avoid (**L-13**), so the refusal names the tool that owns them rather than being silent.

**The locator is imported, not copied.** Finding the installed skill, and refusing when there is
none, both live in `lint.py` and are called from here - so a plugin update that moves the skill
breaks neither tool, and the assertion that a version bump sorts correctly is in that file's
self-test, which runs on every invocation of it.

`list` and `context` are taskmd's own commands. Every argument after the command name is passed
through untouched, which is why this file does not describe them and cannot go stale about them.

Runs from anywhere: the project root comes from `lint.py`, not from the working directory.
Pure standard library (**L-07**).
"""

import os
import subprocess
import sys

# The script's own directory is on `sys.path`, which is how the locator keeps one home.
import lint

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

QUERIES = ("list", "context")

# Commands this deliberately does not offer, and the tool that owns each.
ELSEWHERE = {
    "index": "python tools/tasks/lint.py",
    "check": "python tools/tasks/lint.py",
}

USAGE = """usage: python tools/tasks/query.py {list,context} [args...]

  list [--<field> V] [--open|--closed] [--limit N] [--json]
  context T-NNN

Arguments after the command go to taskmd unchanged. `index` and `check` are run by
`python tools/tasks/lint.py`, which chains them with the reference check."""


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
    if command in ELSEWHERE:
        print("`%s` is not run from here - use `%s`, which chains it with the checks a task edit "
              "owes and stops at the first failure.\n\n%s" % (command, ELSEWHERE[command], USAGE))
        return 2
    if command not in QUERIES:
        print("unknown command `%s`. This tool answers %s.\n\n%s"
              % (command, " and ".join("`%s`" % q for q in QUERIES), USAGE))
        return 2
    return query(argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
