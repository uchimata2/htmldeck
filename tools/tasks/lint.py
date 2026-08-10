#!/usr/bin/env python3
"""Run the three checks a task edit owes, in order, stopping at the first failure.

`tasks/TASK-WORKFLOW.md` §7 *Closing a task* requires `taskmd index`, then `taskmd check`, then
`tools/docs/refcheck.py`, chained with `&&` rather than `;` so a failure stops the chain (**L-40**).
This is that chain as one command.

**It exists because the chain could not be written as one.** The bare `taskmd` command does not
resolve in an agent shell, so every written copy of the chain carried a `PYTHONPATH` incantation to
find the installed skill - and the incantation had two homes the moment it had one, in this project's
task workflow and in the handoff config's `tracker_lint`. Both now name this file (**L-13**).

    python tools/tasks/lint.py

Runs from anywhere: the project root is derived from this file, not from the working directory.
Pure standard library (**L-07**).
"""

import glob
import os
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Where the installed taskmd plugin keeps its skill. Globbed rather than pinned: the version
# directory changes on every plugin update, and a pinned one would break silently at the next.
TASKMD = os.path.join(os.path.expanduser("~"), ".claude", "plugins", "cache",
                      "taskmd", "taskmd", "*", "skills", "taskmd")


def find_taskmd():
    """The newest installed taskmd skill directory, or `None`."""
    found = sorted(p for p in glob.glob(TASKMD) if os.path.isdir(p))
    return found[-1] if found else None


def run(steps, quiet=False):
    """Run each step until one fails. `(exit code, label)` - `label` is `None` when all passed.

    A step is `(label, argv, env)`. Output is inherited rather than captured: these three tools
    report what they found, and swallowing that to reprint a summary would be a second copy of
    their own output.

    **The flush is not a tidiness fix.** This module's `print` is buffered and a child writes to the
    console directly, so without it every heading arrives after the output it introduces - which is
    worse than no heading, because it labels the wrong run.
    """
    for label, argv, env in steps:
        if not quiet:
            print("\n=== %s" % label)
            sys.stdout.flush()
        result = subprocess.run(argv, cwd=ROOT, env=env)
        if result.returncode:
            return result.returncode, label
    return 0, None


def steps():
    skill = find_taskmd()
    if not skill:
        sys.exit("no installed taskmd skill under %s\n"
                 "  Install the taskmd plugin, or run the three checks separately - "
                 "tasks/TASK-WORKFLOW.md section 6 lists them." % TASKMD)
    with_taskmd = dict(os.environ, PYTHONPATH=skill)
    return [
        ("taskmd index", [sys.executable, "-m", "taskmd", "index"], with_taskmd),
        ("taskmd check", [sys.executable, "-m", "taskmd", "check"], with_taskmd),
        ("refcheck", [sys.executable, os.path.join("tools", "docs", "refcheck.py")],
         dict(os.environ)),
    ]


def self_test():
    """A chain that does not stop is not a chain (**L-04**), and the exit status is the whole
    contract `tracker_lint` is called under - so both halves are asserted, not read."""
    def step(label, code):
        return (label, [sys.executable, "-c", "raise SystemExit(%d)" % code], dict(os.environ))

    code, label = run([step("first", 0), step("second", 3), step("third", 4)], quiet=True)
    if (code, label) != (3, "second"):
        sys.exit("SELF-TEST FAILED: a failing step reported %r, wanted (3, 'second'). Either the "
                 "chain ran past a failure - the `;` behaviour L-40 is about - or it lost the "
                 "exit code the caller gates on" % ((code, label),))
    if run([step("first", 0), step("second", 0)], quiet=True) != (0, None):
        sys.exit("SELF-TEST FAILED: an all-passing chain did not report success, so a green run "
                 "here would mean nothing")
    return True


def main():
    self_test()
    code, label = run(steps())
    if code:
        print("\nFAILED at `%s` (exit %d). The chain stopped there; the steps after it did not "
              "run." % (label, code))
    else:
        print("\nAll three passed: the task record, its references, and every pointer in every "
              "document.\n"
              "This validates structure and references. It cannot tell you a specification is "
              "wrong or a deliverable is bad.")
    return code


if __name__ == "__main__":
    sys.exit(main())
