#!/usr/bin/env python3
"""Format a path for display, on any drive.

    import paths
    print("deck:    %s" % paths.display_path(deck, ROOT))

**Why this exists.** Every tool here printed a heading with
`os.path.relpath(deck, ROOT)`, where `ROOT` is the *plugin's own directory*. On Windows
`relpath` cannot express a path across drives and raises:

    ValueError: path is on mount 'N:', start on mount 'C:'

A project on `N:` therefore could not run the gate at all, reported from a real one on
2026-08-10 (T-064). Every crashing call was **display-only**: the tool completed its analysis
and then died formatting its own output, which throws away sound work rather than degrading it.

So the rule is: a shorter path is a courtesy, and a courtesy may never fail. When a relative
path cannot be expressed, print the absolute one and carry on.

Pure standard library (**L-07**).
"""

import os
import sys


def display_path(path, start):
    """`path` relative to `start` when that is expressible, else `path` itself.

    Forward slashes either way, so output is identical on every platform (**L-11**) and a
    caller never needs its own `.replace("\\\\", "/")`.
    """
    try:
        shown = os.path.relpath(path, start)
    except ValueError:
        # Different drives on Windows. Not an error - the absolute path is a fine heading,
        # and the alternative is losing the whole run over a cosmetic choice.
        shown = os.path.abspath(path)
    return shown.replace("\\", "/")


def self_test():
    """A scan that has not been shown to fail is not evidence (**L-04**).

    The cross-drive case is asserted directly rather than through a tool, because it cannot be
    reached on a single-drive machine and would otherwise be covered by nothing anywhere.
    """
    # The defect, constructed. `relpath` must raise here, or this fixture is testing nothing.
    try:
        os.path.relpath(r"N:\proj\deck.html", r"C:\plugin")
        raised = False
    except ValueError:
        raised = True
    if os.name == "nt" and not raised:
        sys.exit("SELF-TEST FAILED: relpath across drives did not raise, so this module's "
                 "reason for existing is unverified on this platform")
    if raised and display_path(r"N:\proj\deck.html", r"C:\plugin") != "N:/proj/deck.html":
        sys.exit("SELF-TEST FAILED: a cross-drive path did not fall back to the absolute path")

    # The ordinary case must be unchanged, or the fix has broken every heading it touched.
    same = display_path(os.path.join("a", "b", "deck.html"), "a")
    if same != "b/deck.html":
        sys.exit("SELF-TEST FAILED: a same-drive path is no longer shown relative: %r" % same)
    if "\\" in display_path(os.path.join("a", "b", "deck.html"), "a"):
        sys.exit("SELF-TEST FAILED: a backslash survived into a displayed path (L-11)")
    return True


if __name__ == "__main__":
    self_test()
    print("OK - display_path degrades to an absolute path across drives, and is unchanged "
          "on one.")
