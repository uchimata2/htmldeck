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


def output_root(target):
    """The project **`target` belongs to** — not the project the tool belongs to.

    Every tool here anchored its working output at `ROOT`, derived from its own `__file__`. Run
    from a clone that is right; run as an installed plugin, `${CLAUDE_PLUGIN_ROOT}/tools/...`, it
    means an adopter's screenshots, PDFs, themed decks **and a full copy of their deck** are
    written into the package cache — a directory that is not theirs, is not in their repository,
    and a reinstall erases (T-074, reported from a real project on 2026-08-10).

    The rule: walk up from the target to the nearest ancestor holding a `.git`, and fall back to
    the target's own directory. A deck inside this repository resolves to this repository, so
    nothing that worked before moves; a deck in someone else's project resolves to theirs.
    """
    here = os.path.dirname(os.path.abspath(target)) if target else os.path.abspath(os.getcwd())
    probe = here
    while True:
        if os.path.isdir(os.path.join(probe, ".git")):
            return probe
        parent = os.path.dirname(probe)
        if parent == probe:
            # No repository above it. The target's own directory is the honest answer: it is
            # where the person is working, and it is somewhere they can find.
            return here
        probe = parent


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

    # **The output root must follow the deck, not this file.** A deck in this repository has to
    # resolve to this repository - that is what keeps every existing path unmoved - and the fixture
    # asserts it against the tool's own location rather than against a literal, so it still means
    # something in a clone somewhere else.
    repo = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    got = output_root(os.path.join(repo, "examples", "reference-deck.html"))
    if os.path.normcase(got) != os.path.normcase(repo):
        sys.exit("SELF-TEST FAILED: a deck in this repository resolved its output root to %r, "
                 "not to the repository %r" % (got, repo))
    # A deck with no repository above it falls back to its own directory, never to the tool's.
    orphan = os.path.join(os.path.abspath(os.sep), "no-such-place-%d" % os.getpid())
    fell_back = output_root(os.path.join(orphan, "deck.html"))
    if os.path.normcase(fell_back) != os.path.normcase(orphan):
        sys.exit("SELF-TEST FAILED: a deck outside any repository resolved to %r rather than to "
                 "its own directory - an adopter's output would land somewhere they did not "
                 "choose" % fell_back)
    return True


if __name__ == "__main__":
    self_test()
    print("OK - display_path degrades to an absolute path across drives, and is unchanged "
          "on one.")
