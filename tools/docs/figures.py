#!/usr/bin/env python3
"""Check that every figure in `README.md` still matches the command that produced it.

    python tools/docs/figures.py            # the partition, and the verdict
    python tools/docs/figures.py --values   # what to paste when something has drifted

**Why this file exists.** `docs/PUBLISHING.md` §6 says every figure in the README is pasted from a
run, and instructs a person to run five commands and diff each by eye. That instruction was in
writing and unchecked, and **six figures were already stale** when T-056 went looking - the ruleset
had grown and nothing re-derived the page (**L-52**). This is that instruction, executed. It does
not add a command to the release pass; it replaces the manual half of one.

**Two kinds of number, and one rule cannot hold both.** A figure that describes a *decision* - 163
rule rows, 117 hard rules, 25 that need a person - moves when somebody changes the ruleset, which is
rare and deliberate. A figure that counts the *repository* moves on every documentation commit,
**including the commit that corrects it**, which is why re-deriving it has never converged (T-067
§4). So a figure is `compared` and fails the run on any drift, or it is `volatile`, declared below
with the reason, and **reported** rather than enforced. Every one of T-056's six was a ruleset
count, so nothing is weakened by excusing the three that count documents.

Runs its own self-test first and refuses to report if it fails (**L-04**). Pure standard library
(**L-07**).
"""

import io
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
README = os.path.join(ROOT, "README.md")

FENCE = re.compile(r"^```(\w*)\s*$")

# A numeral written in prose is a measurement; a spelled-out number almost always is not - of the
# 60 numbers in this page's prose, 50 are words like "one project" and "two days". **Every one of
# T-056's stale prose figures was a numeral**, so this is where the defect class lives. The
# spelled-out ones are excluded in writing rather than silently: see EXCLUDED_PROSE.
PROSE_NUMERAL = re.compile(r"(?<![\w.$-])(\d[\d,]*)(?![\w.%-])")

# Commands this tool is willing to execute. **An allowlist, not a convenience.** The page also
# prints `git clone`, `/plugin install` and `claude plugin update`, and a tool that ran whatever a
# document told it to would execute those the first time somebody edited the README.
RUNNABLE = re.compile(r"^python tools/[\w/]+\.py(?: [\w.=/-]+)*$")

# Figures whose value counts this repository, so any documentation commit moves them - including
# the one that corrects them. Reported as drift, never failed on. The reason is the excusal, and
# what would close it is a figure that does not count its own source.
VOLATILE = {
    "python tools/docs/refcheck.py":
        "every number counts documents in this repository, so it is stale in the very commit that "
        "corrects it - re-derived three times in one session and wrong again each time (T-067 §4)",
}

# Fenced blocks that are not a command's output, each with the reason. An unlisted unbound fence
# fails the run: the partition is the point, and a silent third category is how six figures went
# stale under a rule that was already in writing.
EXCLUDED_FENCES = {
    "/plugin marketplace add": "typed into Claude Code; there is no local command to run",
    "git clone https://": "clones this repository; running it would fetch the network every check",
    "claude plugin update": "upgrades an installed plugin on the reader's machine",
    "taskmd check": "belongs to another project's tool, and no output is pasted under it",
    "python tools/deck/check.py examples/sort-window": "invoked for its side effect in the text; "
        "no output is pasted under it",
    "python tools/deck/critique.py": "shows the calling form with placeholder arguments, not a run",
}

# Prose numerals that no command prints, each with what would close the exclusion.
EXCLUDED_PROSE = {
    "31": "113 - 82, stated as the remainder in the same sentence; it would be closed by the gate "
          "printing the unchecked count as a row of its own",
    "1.1": "a section number in `EVALUATION.md 1.1`, not a measurement",
    "0.1": "a release name",
    "0.2": "a release name",
    "106": "a rule ID (DS-106) written without its prefix in prose",
}


# ---------------------------------------------------------------------------- the document


def fences(text):
    """`[(line_no, lang, [body lines])]` for every fenced block, in document order."""
    out, lang, body, start = [], None, None, 0
    for i, line in enumerate(text.split("\n"), 1):
        m = FENCE.match(line)
        if m and body is None:
            lang, body, start = m.group(1), [], i
        elif m:
            out.append((start, lang, body))
            lang, body = None, None
        elif body is not None:
            body.append(line)
    return out


def prose(text):
    """The document with every fenced block removed, so prose scans cannot see pasted output."""
    keep, inside = [], False
    for line in text.split("\n"):
        if FENCE.match(line):
            inside = not inside
            continue
        keep.append("" if inside else line)
    return "\n".join(keep)


def bind(blocks):
    """`[(kind, line_no, command_or_reason, body)]` - the partition over every fence.

    **Adjacency is the whole of the binding**, and it is the document's own shape rather than a
    list kept beside it: an unlabelled fence directly after a ```bash fence is that command's
    output. A list of which block goes with which command would be a second copy of a fact the
    page already states by layout, and it would drift the first time a section moved (**L-13**).
    """
    out, pending = [], None
    for start, lang, body in blocks:
        cmd = " ".join(l.strip() for l in body if l.strip())
        if lang == "bash" or (lang == "" and not pending and not RUNNABLE.match(cmd)):
            reason = None
            for prefix, why in EXCLUDED_FENCES.items():
                if cmd.startswith(prefix):
                    reason = why
                    break
            if lang == "bash" and RUNNABLE.match(cmd) and reason is None:
                pending = cmd
                out.append(("command", start, cmd, body))
            else:
                pending = None
                out.append(("excluded" if reason else "UNDECLARED", start,
                            reason or "a fenced block bound to nothing and declared nowhere", body))
        elif pending:
            out.append(("output", start, pending, body))
            pending = None
        else:
            out.append(("UNDECLARED", start,
                        "an output block with no command above it", body))
    return out


# ---------------------------------------------------------------------------- the commands


_RUNS = {}


def run(cmd):
    """The command's combined output, run at most once per process.

    **The cache is not an optimisation.** `check.py` drives real headless Chrome, and the self-test
    audits the document six times over - once clean and once per staled fixture. Without this the
    fixtures cost six browser launches and the tool times out before it reports anything, which is
    a check nobody waits for (**L-40**).
    """
    if cmd not in _RUNS:
        argv = cmd.split()
        if argv[0] == "python":
            argv[0] = sys.executable
        p = subprocess.Popen(argv, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        _RUNS[cmd] = p.communicate()[0].decode("utf-8", "replace").replace("\r\n", "\n")
    return _RUNS[cmd]


def deck_facts():
    """Sizes the prose states directly, so `221 KB` is a figure rather than a recollection."""
    out = []
    for rel in ("examples/reference-deck.html", "examples/sort-window/sort-window.html"):
        path = os.path.join(ROOT, rel.replace("/", os.sep))
        if os.path.exists(path):
            out.append("%s %d KB" % (rel, int(round(os.path.getsize(path) / 1024.0))))
    return "\n".join(out)


def mask(line):
    """`line` with every run of digits replaced, so a volatile block compares on its shape."""
    return re.sub(r"\d+", "#", line)


def excerpt(pasted, actual, volatile):
    """`(ok, [complaint])` - every pasted line must appear in `actual`, in order.

    **The blocks are excerpts and have to be compared as such.** `ruleset.py --counts` prints
    twenty-odd lines and the README pastes three of them; a whole-output equality test would fail
    on every block in the page and would prove nothing about any of them.
    """
    want = [l for l in pasted if l.strip()]
    have = actual.split("\n")
    if volatile:
        want, have = [mask(l) for l in want], [mask(l) for l in have]
    bad, at = [], 0
    for line in want:
        for j in range(at, len(have)):
            if have[j].strip() == line.strip():
                at = j + 1
                break
        else:
            bad.append(line.strip())
    return (not bad), bad


def drifted(pasted, actual):
    """`[(pasted_line, actual_line)]` for volatile lines whose digits have moved."""
    have = actual.split("\n")
    out = []
    for line in pasted:
        if not line.strip() or not re.search(r"\d", line):
            continue
        for cand in have:
            if mask(cand).strip() == mask(line).strip() and cand.strip() != line.strip():
                out.append((line.strip(), cand.strip()))
                break
    return out


# ---------------------------------------------------------------------------- the run


def audit(text):
    """`(rows, prose_rows, corpus)` - every verdict this tool reaches, decided nowhere else."""
    rows, corpus, outputs = [], [], {}
    for kind, start, what, body in bind(fences(text)):
        if kind != "output":
            rows.append((kind, start, what, None))
            continue
        if what not in outputs:
            outputs[what] = run(what)
        actual = outputs[what]
        corpus.append(actual)
        vol = what in VOLATILE
        ok, bad = excerpt(body, actual, vol)
        if not ok:
            rows.append(("FAILING", start, "%s: %d line(s) absent from the run: %s"
                         % (what, len(bad), "; ".join(bad[:2])), None))
        elif vol:
            moved = drifted(body, actual)
            rows.append(("volatile", start, what, moved))
        else:
            rows.append(("compared", start, what, None))

    corpus.append(deck_facts())
    seen = "\n".join(corpus)
    prose_rows = []
    for m in PROSE_NUMERAL.finditer(prose(text)):
        n = m.group(1)
        if n in EXCLUDED_PROSE:
            prose_rows.append(("excluded", n, EXCLUDED_PROSE[n]))
        # **The boundary has to reject a letter, not just a digit.** Without the `\w`, `163` in
        # prose matched `DS-163` in a gate's output, `113` matched `DS-113` and `221` matched
        # `DS-221` - three of eight prose figures reported as covered by a rule ID that has nothing
        # to do with them. A check that says `compared` when it compared a coincidence is worse
        # than one that says nothing (**L-36**, **L-44**).
        elif re.search(r"(?<![\w.-])%s(?![\w.%%-])" % re.escape(n), seen):
            prose_rows.append(("compared", n, "printed by a bound command"))
        else:
            prose_rows.append(("UNDECLARED", n, "no bound command prints it and it is excused "
                                                "nowhere"))
    return rows, prose_rows, seen


def self_test():
    """Four staled copies, one per failure mode. **A check only ever seen passing is not a check**
    (**L-36**), and reading the assertion is not enough - each fixture is judged by the *message*
    it produces, because an assertion that cannot run still exits non-zero (**L-55**)."""
    base = io.open(README, encoding="utf-8").read()

    rows, prose_rows, _seen = audit(base)
    if [r for r in rows if r[0] in ("FAILING", "UNDECLARED")]:
        bad = [r for r in rows if r[0] in ("FAILING", "UNDECLARED")][0]
        sys.exit("SELF-TEST FAILED: the live README does not pass its own check - line %d, %s"
                 % (bad[1], bad[2]))
    if not [r for r in rows if r[0] == "compared"]:
        sys.exit("SELF-TEST FAILED: no block was compared, so a clean run means nothing")
    if not [r for r in rows if r[0] == "volatile"]:
        sys.exit("SELF-TEST FAILED: no block is volatile, so the split this tool exists for is "
                 "not exercised and the refcheck block must have stopped being bound")

    # **Both fixtures are derived from the document, never quoted from it.** A hardcoded figure
    # here goes stale exactly like the ones this tool is watching, and a `replace` that matches
    # nothing stales nothing and passes - a fixture that tests nothing, reporting success
    # (**L-54**, **L-55**). So the line is found, its first number is moved, and the fixture
    # refuses to run if it could not find one.
    def stale_a(kind_wanted):
        for kind, _start, what, body in bind(fences(base)):
            if kind != "output":
                continue
            if (what in VOLATILE) != (kind_wanted == "volatile"):
                continue
            for line in body:
                if re.search(r"\d", line):
                    moved = re.sub(r"\d+", lambda m: str(int(m.group(0)) + 7), line, count=1)
                    return line, base.replace(line, moved)
        return None, base

    # 1. A stale *compared* figure has to fail. This is the defect class T-056 found six of.
    line, staled = stale_a("compared")
    if line is None or staled == base:
        sys.exit("SELF-TEST FAILED: no compared block carries a number, so nothing here tests the "
                 "stale-figure case at all")
    if not [r for r in audit(staled)[0] if r[0] == "FAILING"]:
        sys.exit("SELF-TEST FAILED: a compared figure was moved (%r) and the run stayed green. "
                 "That is exactly the six-stale-figures state this tool exists to end"
                 % line.strip())

    # 2. A stale *volatile* figure must NOT fail - and must still be reported, or it rots quietly.
    line, vol = stale_a("volatile")
    if line is None or vol == base:
        sys.exit("SELF-TEST FAILED: no volatile block carries a number, so the half of the split "
                 "that must NOT fail is unexercised")
    rows2 = audit(vol)[0]
    if [r for r in rows2 if r[0] == "FAILING"]:
        sys.exit("SELF-TEST FAILED: a moved pointer count failed the run. It moves on every "
                 "documentation commit, so this check would be switched off within a week")
    if not [r for r in rows2 if r[0] == "volatile" and r[3]]:
        sys.exit("SELF-TEST FAILED: a moved pointer count was neither failed nor reported, so "
                 "nothing can tell anyone it drifted")

    # 3. An undeclared fence is a gap, not a silence.
    added = base + "\n\n```\nsomething nobody bound to anything\n```\n"
    if not [r for r in audit(added)[0] if r[0] == "UNDECLARED"]:
        sys.exit("SELF-TEST FAILED: a fenced block bound to nothing passed. The partition is the "
                 "whole point - a third category nobody sees is how the last six got through")

    # 4. So is an undeclared prose numeral.
    added = base + "\n\nThe gate owns 4242 rules.\n"
    if not [r for r in audit(added)[1] if r[0] == "UNDECLARED"]:
        sys.exit("SELF-TEST FAILED: a prose numeral no command prints was accepted")

    # 5. **A numeral that appears only inside a rule ID is not covered by it.** `107` occurs in the
    # gate's output solely as `DS-107`. Reported as `compared` it would be a false pass, which is
    # the failure this repository treats hardest - and three real figures were passing that way
    # before the word boundary was tightened.
    added = base + "\n\nThe ruleset carries 107 rules of that kind.\n"
    if not [r for r in audit(added)[1] if r[0] == "UNDECLARED" and r[1] == "107"]:
        sys.exit("SELF-TEST FAILED: a prose numeral matched only by a rule ID (DS-107) was "
                 "reported as compared. A check that compares a coincidence is worse than one "
                 "that says nothing")
    return True


def report(values):
    text = io.open(README, encoding="utf-8").read()
    rows, prose_rows, _seen = audit(text)
    print("README figures - %s\n" % os.path.basename(README))

    counts = {}
    for kind, start, what, extra in rows:
        counts[kind] = counts.get(kind, 0) + 1
        if kind in ("FAILING", "UNDECLARED"):
            print("  %-10s line %-4d %s" % (kind, start, what))
        elif kind == "volatile" and extra:
            print("  %-10s line %-4d %s" % ("drifted", start, what))
            for was, now in extra:
                print("               was  %s" % was)
                print("               now  %s" % now)
    pc = {}
    for kind, n, why in prose_rows:
        pc[kind] = pc.get(kind, 0) + 1
        if kind == "UNDECLARED":
            print("  %-10s prose numeral %s - %s" % (kind, n, why))

    print("\n  fenced blocks")
    for k in ("command", "compared", "volatile", "excluded", "UNDECLARED", "FAILING"):
        if counts.get(k):
            print("    %-12s %3d" % (k, counts[k]))
    print("    %-12s %3d   = every fence, so the account is a partition" % ("total", len(rows)))
    print("\n  prose numerals")
    for k in ("compared", "excluded", "UNDECLARED"):
        if pc.get(k):
            print("    %-12s %3d" % (k, pc[k]))
    print("    %-12s %3d" % ("total", len(prose_rows)))

    drift = [r for r in rows if r[0] == "volatile" and r[3]]
    if values and drift:
        print("\n  paste these:")
        for _k, _s, _w, extra in drift:
            for _was, now in extra:
                print("    %s" % now)

    fails = counts.get("FAILING", 0) + counts.get("UNDECLARED", 0) + pc.get("UNDECLARED", 0)
    print("\n%s" % ("%d figure(s) to fix" % fails if fails else
                    "0 stale figure(s)%s" % (" - %d volatile block(s) drifted, which is reported "
                                             "rather than failed (see --values)" % len(drift)
                                             if drift else "")))
    print("\nThis checks that a pasted figure matches its command. It cannot tell you the sentence\n"
          "around it is still true - the README's \"all three are fixed\" went false with every\n"
          "figure on the page correct, and no gate here would have seen it (L-05).")
    return 1 if fails else 0


if __name__ == "__main__":
    self_test()
    sys.exit(report("--values" in sys.argv[1:]))
