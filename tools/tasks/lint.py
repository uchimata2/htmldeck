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


def version_key(path):
    """Sort key for one match, on the version directory in the middle of it.

    **Sorted as text, `0.10.0` comes before `0.5.0`** - so the newest install would be the one this
    picks last, and a plugin update past `0.9` would silently start running the older skill. A name
    that is not all digits and dots sorts below every numbered one rather than being guessed at.
    """
    name = os.path.basename(os.path.dirname(os.path.dirname(path)))
    parts = name.split(".")
    if parts and all(p.isdigit() for p in parts):
        return (1, [int(p) for p in parts], name)
    return (0, [], name)


def find_taskmd():
    """The newest installed taskmd skill directory, or `None`."""
    found = sorted((p for p in glob.glob(TASKMD) if os.path.isdir(p)), key=version_key)
    return found[-1] if found else None


def require_taskmd():
    """The same directory, but exiting rather than returning `None`.

    Both entry points in this folder need the installed skill and neither can do anything without
    it, so the locating and the refusal have one home between them (**L-13**) - this one.
    """
    skill = find_taskmd()
    if not skill:
        sys.exit("no installed taskmd skill under %s\n"
                 "  Install the taskmd plugin. tasks/TASK-WORKFLOW.md section 6 names every "
                 "command that needs it, and what each one is for." % TASKMD)
    return skill


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
    with_taskmd = dict(os.environ, PYTHONPATH=require_taskmd())
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

    # The locator serves this file and `query.py`, and the ordering defect it guards against
    # arrives with a plugin update rather than with an edit here - so it is asserted, not read.
    installs = ["/c/taskmd/0.5.0/skills/taskmd", "/c/taskmd/0.10.0/skills/taskmd",
                "/c/taskmd/0.9.1/skills/taskmd"]
    newest = sorted(installs, key=version_key)[-1]
    if newest != "/c/taskmd/0.10.0/skills/taskmd":
        sys.exit("SELF-TEST FAILED: the newest of %r was read as %r. Sorted as text 0.10.0 loses "
                 "to 0.5.0, and both tools here would then run an older installed skill than the "
                 "one present, with nothing to say so" % (installs, newest))
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
