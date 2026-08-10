#!/usr/bin/env python3
"""Check that every figure in `README.md` still matches the command that produced it.

    python tools/docs/figures.py            # the partition, and the verdict
    python tools/docs/figures.py --values   # what to paste when something has drifted

**Why this file exists.** `docs/PUBLISHING.md` §6 says every figure in the README is pasted from a
run, and instructs a person to run five commands and diff each by eye. That instruction was in
writing and unchecked, and **six figures were already stale** when T-056 went looking - the ruleset
had grown and nothing re-derived the page (**L-52**). This is that instruction, executed. It does
not add a command to the release pass; it replaces the manual half of one.

**A figure is bound to the field that produced it.** Occurring somewhere in a command's output was
never a comparison: `12 slides` was covered twice by `8-12` inside a `DS-082` rule note, and a
figure moved into a sentence about something else stayed green. Each output line is `<label>
<value>`, so a prose numeral is `compared` only when its sentence names that label - and the report
prints which field each one bound to, because a binding nobody can read is a claim (**L-63**).

**Five documents beside the README are read the same way, by a different rule.** They paste no
output and describe the account in their own words, where a gate's labels - `checked`, `owned`,
`rules` - are ordinary English; binding those by vocabulary produced 30 false alarms against 5 true
ones. What binds there is the claim's construction: *part* of *whole*, plus the remainder. That
figure drifted to three different values across those five pages while the README's stayed correct.

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
# A figure ends in a digit: `1,218` keeps its thousands separator and `the other 31, with a reason`
# does not take the comma with it.
PROSE_NUMERAL = re.compile(r"(?<![\w.$-])(\d[\d,]*\d|\d)(?![\w.%-])")

# The same numeral rule applied to a command's output. `DS-082` is not the number 82 in either
# direction, which is what the boundaries are for.
CORPUS_NUMERAL = re.compile(r"(?<![\w.-])(\d[\d,]*\d|\d)(?![\w.%-])")

# A label ends at the numeral it introduces and starts after the previous one - but also after a
# sentence break, so a numeral buried in a gate's prose gets `*past` rather than the whole rule
# note as its label. `.` counts as a break only before whitespace, or `reference-deck.html` would
# label itself `html` and stop binding to the sentence that names the file.
LABEL_CUT = re.compile(r"[.;:]\s|[.;:]$")

# Prose splits on sentence ends, blank lines and table-cell walls - and **not** on `:` or `;`,
# because "holds *Move the window, not the fleet*: 12 slides, **220 KB**" is one claim and cutting
# it would separate the figure from the file it is about.
SENTENCE_END = re.compile(r"(?<=[.!?])\s")

# A backlog row whose task is struck through and dated is a **record of what was true then**, not a
# claim the page is making now: `BRIEF.md` says "161 rows were 163" and "113 rules owned, 81
# checked" in two such rows, both correct, both about numbers no command prints today. Skipping
# them is a rule about the row's own shape - the same reasoning `TASK-WORKFLOW.md` §6 gives for
# leaving a task record's mention of a retired tool alone.
DONE_ROW = re.compile(r"~~.*~~\s*\*\*done \d{4}-\d{2}-\d{2}\*\*")

# Words with no binding force. A label survives this filter or it binds nothing, which is what
# disqualifies `-12 band is measured and reported by the DS-081 row's count; *past` from claiming
# the README's slide count.
STOPWORDS = set("""a an and are as at be been but by for from had has have here in into is it its
not of on or over per that the their them then there these they this to under was were what when
which with""".split())

# Documents that state a figure some command here derives, each with why it is read. **They are not
# accounts of command output**, so their numerals are not a partition: a sentence that speaks an
# account's vocabulary is held to that account's numbers, and one that does not is skipped and
# counted. The list is which documents, never which sentences - the binding stays derived.
#
# `docs/DESIGN-RATIONALE.md` is deliberately absent: it states the coverage account as history in
# ordinary prose - "took the gate to 78 of the 111 rules owned at the time", "checked 80 -> 81" -
# with no marker distinguishing it from a live claim. Every one of those is correct and every one
# would be flagged, which is an alarm that is wrong every time.
DECLARED_DOCS = {
    "CLAUDE.md": "states the coverage split in its own summary of what the gate decides",
    "docs/BRIEF.md": "the specification; states the split under *Decisions taken*",
    "docs/EVALUATION.md": "states what the mechanical half decides before scoring the rest",
    "skills/htmldeck/references/pipeline.md": "the shipped skill tells a build what the gate covers",
    "examples/README.md": "states the split twice, for the reference deck and the built one",
}

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

# Prose numerals that no command prints, each with what would close the exclusion. An entry whose
# numeral has left the page is reported STALE and fails the run - see `stale_exclusions`. Four sat
# here when that check was written (`1.1`, `0.1`, `0.2`, `106`) and were deleted rather than
# rephrased: an excusal is re-earned by the numeral coming back, and a red run is how it asks.
#
# **It is empty, and that is the result rather than the starting state.** Its last entry was `31`,
# excused as *"113 - 82, stated as the remainder in the same sentence"*, with the closing condition
# *"the gate printing the unchecked count as a row of its own"*. `claimed()` closed it a better
# way: the sentence states the subtraction, so the figure is derived and checked instead of
# excused, and no row had to be added to the gate to do it.
EXCLUDED_PROSE = {}

# The shape of a claim about an account: a part, of a whole, and sometimes the remainder. **The
# shape is the binding** - "82 of the 113 rules a gate owns ... the other 31" says which figure it
# quotes in the only way a page of prose can, and five documents state exactly this one. Bold
# markers are stepped over because `**82** of the 113` is the same sentence.
CLAIM = re.compile(r"(?<![\w.$-])(\d[\d,]*\d|\d)\*{0,2}\s+of\s+(?:the\s+)?\*{0,2}"
                   r"(\d[\d,]*\d|\d)(?![\w.%-])")
REMAINDER = re.compile(r"other\s+\*{0,2}(\d[\d,]*\d|\d)(?![\w.%-])")


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


def stem(word):
    """Crude suffix strip, so `checks` and `checked` reach the label `checked` from either side.

    **The trailing `e` goes last and unconditionally**, because stripping the plural is what makes
    it necessary: `rules` -> `rule` and `rule` -> `rule` look equal and are not once `gates` ->
    `gate` has to meet `gated`. Taking both to `rul` and `gat` is ugly and it is symmetric, which is
    the only property a stem needs here. `ss` is exempt or `class` and `classes` diverge.
    """
    for suffix in ("ing", "ed"):
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            word = word[:-len(suffix)]
            break
    if word.endswith("s") and not word.endswith("ss") and len(word) > 3:
        word = word[:-1]
    if word.endswith("e") and len(word) > 3:
        word = word[:-1]
    return word


def words(text):
    """The stems of `text` worth binding on - four letters or more, and not a stopword.

    Path separators split, so the label `examples/sort-window/sort-window.html` reaches a sentence
    that names `examples/sort-window`. Four letters is where the noise starts: `KB`, `of` and `to`
    bind everything to everything.
    """
    raw = re.findall(r"[A-Za-z]{4,}", re.sub(r"[/_.-]", " ", text))
    return set(stem(w.lower()) for w in raw if w.lower() not in STOPWORDS)


def sentences(text):
    """`[(sentence, is_dated_record)]` over prose - the unit a figure is bound inside.

    Table cells are their own sentences: a row states one claim per cell, and a wrapped markdown
    paragraph states one across several lines, so newlines join and `|` splits.
    """
    out = []
    for block in re.split(r"\n\s*\n", text):
        dated = bool(DONE_ROW.search(block))
        for cell in block.split("|"):
            for s in SENTENCE_END.split(" ".join(cell.split("\n"))):
                if s.strip():
                    out.append((s, dated))
    return out


def fields(outputs):
    """`[(value, label, command)]` - every figure a command printed, with the words beside it.

    **This is the binding the tool did not have.** A pasted numeral used to be checked against the
    union of every command's output, so `81` was covered by `checked 81` no matter what sentence it
    sat in. A value's label is the text between it and the previous numeral on its line, which is
    where a report puts the name of the thing it is counting.
    """
    out = []
    for cmd, text in outputs.items():
        for line in text.split("\n"):
            at = 0
            for m in CORPUS_NUMERAL.finditer(line):
                label = line[at:m.start()]
                at = m.end()
                cuts = list(LABEL_CUT.finditer(label))
                if cuts:
                    label = label[cuts[-1].end():]
                out.append((m.group(1), label.strip(), cmd))
    return out


def bound(numeral, said, table):
    """`[(label, command)]` - every field carrying `numeral` whose label `said` names.

    A field whose label keeps no distinctive word cannot bind anything, which is how `12` stops
    being covered by the `DS-082` triage note that happens to contain it.
    """
    hits = []
    for value, label, cmd in table:
        if value != numeral:
            continue
        lw = words(label)
        if lw and (lw & said):
            hits.append((label, cmd))
    return hits


def claimed(sentence, table, outputs):
    """`{numeral: (verdict, why)}` for the figures a sentence's own arithmetic accounts for.

    **Why a shape and not a label.** Binding by label works on the README, where a figure sits
    beside the word the command printed next to it. It does not survive paraphrase: `EVALUATION.md`
    says *"decides 82"* where the gate prints `checked`, and the words a gate prints - `checked`,
    `owned`, `rules`, `gate` - are ordinary English that five documents use in their ordinary
    sense. Anchoring a whole sentence on one such word was tried and produced **30 false alarms
    against 5 true ones**, on prose about external references, SVG counts and effect sizes. So the
    claim is bound by its construction instead: *part* of *whole*, where the whole is a figure a
    command prints under a label this sentence does name. Then the part must be a figure of that
    same account, and any *"other N"* must be the subtraction. That is exact, it is derived from
    the sentence and the command rather than from a list, and it is what drifted - the coverage
    split reached three different values across five documents while the README's stayed correct.
    """
    out = {}
    said = words(sentence)
    for m in CLAIM.finditer(sentence):
        part, whole = m.group(1), m.group(2)
        hits = bound(whole, said, table)
        if not hits:
            continue
        where = "; ".join(sorted(set(c for _l, c in hits)))
        account = "\n".join(outputs[c] for _l, c in hits)
        if re.search(r"(?<![\w.-])%s(?![\w.%%-])" % re.escape(part), account):
            out[part] = ("compared", "%s of %s, both figures of %s" % (part, whole, where))
        else:
            out[part] = ("STALE", "claimed as %s of %s, and %s prints no %s"
                                  % (part, whole, where, part))
        rest = int(whole.replace(",", "")) - int(part.replace(",", ""))
        for r in REMAINDER.finditer(sentence[m.end():]):
            got = int(r.group(1).replace(",", ""))
            out[r.group(1)] = (("compared", "the remainder, %s - %s, which this sentence states"
                                            % (whole, part))
                               if got == rest else
                               ("STALE", "stated as the rest of %s after %s, which is %s"
                                         % (whole, part, rest)))
    return out


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


# The decks are a source of figures like any command, and are named like one so a report can say
# where a value came from.
DECK_FACTS = "the deck files themselves"

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
    """Sizes and slide counts the prose states, so each is a figure rather than a recollection.

    **One fact per line, because the line is what carries the label.** `221 KB` and `12 slides` on
    one line would leave the second labelled ` KB `, binding nothing. The slide count is here
    because the page states it twice and no command printed it: both numerals were reported
    `compared` against `8-12` inside a `DS-082` triage note - a coincidence, in the one place this
    tool exists to refuse them. Counted from the markup; the reference deck's colophon carries
    `slide close` and is not one of the twelve, which is why the page says "and a colophon".
    """
    out = []
    for rel in ("examples/reference-deck.html", "examples/sort-window/sort-window.html"):
        path = os.path.join(ROOT, rel.replace("/", os.sep))
        if os.path.exists(path):
            out.append("%s %d KB" % (rel, int(round(os.path.getsize(path) / 1024.0))))
            html = io.open(path, encoding="utf-8").read()
            out.append("%s %d slides" % (rel, len(re.findall(r'class="slide"', html))))
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

    outputs[DECK_FACTS] = deck_facts()
    corpus.append(outputs[DECK_FACTS])
    seen = "\n".join(corpus)
    table = fields(outputs)

    # **Occurring in the corpus was never a comparison.** Tightening the word boundary stopped
    # `163` being covered by `DS-163`, `113` by `DS-113` and `221` by `DS-221` - but only that
    # coincidence, and a numeral still passed by turning up anywhere in the union of every
    # command's output. So `12` was covered by `8-12` inside a `DS-082` triage note, twice, and a
    # `25` moved onto a sentence about a different figure would have been covered by `checked 25`.
    # A figure is now bound to **the field it claims to be**: the sentence has to name the label
    # the command printed beside the value. A check that says `compared` when it compared a
    # coincidence is worse than one that says nothing (**L-36**, **L-44**).
    prose_rows = []
    for sentence, _dated in sentences(prose(text)):
        said = words(sentence)
        claims = claimed(sentence, table, outputs)
        for m in PROSE_NUMERAL.finditer(sentence):
            n = m.group(1)
            if n in EXCLUDED_PROSE:
                prose_rows.append(("excluded", n, EXCLUDED_PROSE[n]))
                continue
            hits = bound(n, said, table)
            if hits:
                prose_rows.append(("compared", n, "%r, printed by %s" % (hits[0][0], hits[0][1])))
            elif n in claims:
                prose_rows.append((claims[n][0], n, claims[n][1]))
            else:
                prose_rows.append(("UNDECLARED", n, "no command prints it under a label this "
                                                    "sentence names, and it is excused nowhere"))
    return rows, prose_rows, seen, table, outputs


def declared(table, outputs, docs=None):
    """`(rows, skipped)` - the same figures, stated in documents that paste no command output.

    **The other half of the binding question, one scope out.** The coverage split lives in five
    documents beside the README and drifted to three different values while the README's own figure
    stayed bound and correct; correcting it by hand in five places is what T-045 already did once.
    These pages are not accounts of a run, so their numerals are not a partition and most are not
    figures at all - **the great majority of a number written here is not a figure this tool could
    ever check**, and saying which is which is the whole difficulty. `claimed()` carries that
    judgement: a numeral is judged when the sentence states it as part of a whole the command
    prints, and is skipped and counted otherwise. Nothing is guessed at, and a page is never held
    to a partition it was not written as.
    """
    rows, skipped = [], 0
    for rel in sorted(DECLARED_DOCS):
        if docs and rel in docs:
            text = docs[rel]
        else:
            text = io.open(os.path.join(ROOT, rel.replace("/", os.sep)), encoding="utf-8").read()
        for sentence, dated in sentences(prose(text)):
            nums = [m.group(1) for m in PROSE_NUMERAL.finditer(sentence)]
            if not nums:
                continue
            claims = {} if dated else claimed(sentence, table, outputs)
            for n in nums:
                if n in claims:
                    rows.append((claims[n][0], rel, n, claims[n][1]))
                else:
                    skipped += 1
    return rows, skipped


def stale_exclusions(text):
    """`[(table, key, why)]` - every exclusion whose subject is no longer on the page.

    **The other direction of the same question.** `audit` asks *is every figure on the page
    accounted for?* and nothing asked *is every account still about a figure on the page?* - so an
    excusal outlives its subject silently, and its stated reason goes false with it. That is how this
    tool came to be red on `master`: the coverage split moved from 81/32 to 82/31, `EXCLUDED_PROSE`
    still declared `32` with the reason *"113 - 81"*, and the run failed on the new numeral while
    the dead excusal for the old one sat there saying nothing (T-077). `audit.py` has reported this
    shape since T-066 and calls it `stale`; this is the same discipline in the second file that
    needed it (**L-54**).
    """
    fenced = [" ".join(l.strip() for l in body if l.strip()) for _s, _l, body in fences(text)]
    numerals = set(m.group(1) for m in PROSE_NUMERAL.finditer(prose(text)))
    out = []
    for prefix, why in EXCLUDED_FENCES.items():
        if not any(cmd.startswith(prefix) for cmd in fenced):
            out.append(("EXCLUDED_FENCES", prefix, why))
    for n, why in EXCLUDED_PROSE.items():
        if n not in numerals:
            out.append(("EXCLUDED_PROSE", n, why))
    return out


def self_test():
    """Four staled copies, one per failure mode. **A check only ever seen passing is not a check**
    (**L-36**), and reading the assertion is not enough - each fixture is judged by the *message*
    it produces, because an assertion that cannot run still exits non-zero (**L-55**)."""
    base = io.open(README, encoding="utf-8").read()

    rows, prose_rows, _seen, table, outputs = audit(base)
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

    # 6. **An exclusion whose subject has left the page.** Seeded by taking the subject off the
    # page rather than by adding a table entry: a fabricated entry would test the loop, and what
    # has to be tested is that a live declaration goes stale when the page moves underneath it -
    # which is what actually happened. It seeds a **fence** exclusion because `EXCLUDED_PROSE` is
    # now empty, `claimed()` having derived its last entry instead of excusing it. Emptied by
    # deriving, not by deleting: the same fixture on the other table is the check surviving that.
    victim, emptied = None, base
    for prefix in sorted(EXCLUDED_FENCES):
        for start, _lang, body in fences(base):
            cmd = " ".join(l.strip() for l in body if l.strip())
            if cmd.startswith(prefix):
                lines = base.split("\n")
                victim = prefix
                emptied = "\n".join(lines[:start - 1] + lines[start + len(body) + 1:])
                break
        if victim:
            break
    if victim is None or emptied == base:
        sys.exit("SELF-TEST FAILED: no declared fence exclusion names a block the page carries, so "
                 "the live README already carries the defect this fixture seeds")
    got = [k for _t, k, _w in stale_exclusions(emptied)]
    if victim not in got:
        sys.exit("SELF-TEST FAILED: the %r block was taken off the page and its exclusion was not "
                 "reported stale. An excusal for a block nobody prints is a false statement "
                 "sitting in the tool, which is the state T-077 was raised from" % victim)
    if stale_exclusions(base):
        sys.exit("SELF-TEST FAILED: the live README already carries a stale exclusion (%s), so a "
                 "green run below would mean nothing"
                 % ", ".join("%s %s" % (t, k) for t, k, _w in stale_exclusions(base)))

    # 7. **A figure moved onto a sentence about a different field.** The case T-060's review named
    # and this tool could not see: the numeral is real, the corpus prints it, and the sentence it
    # now sits in is about something else. Derived rather than written down - a compared numeral is
    # swapped for the value of a field whose label this sentence does not name, so the fixture
    # cannot go stale when the figures move (**L-54**).
    swapped = None
    for kind, n, why in prose_rows:
        if kind != "compared":
            continue
        mine = set(l for v, l, _c in table if v == n)
        for value, label, _cmd in table:
            if value != n and words(label) and label not in mine and value not in EXCLUDED_PROSE:
                pat = re.compile(r"(?<![\w.$-])%s(?![\w.%%-])" % re.escape(n))
                cand = pat.sub(value, base, count=1)
                if cand != base and not [r for r in audit(cand)[1]
                                         if r[0] == "compared" and r[1] == value]:
                    swapped = (n, value, label)
                    break
        if swapped:
            break
    if swapped is None:
        sys.exit("SELF-TEST FAILED: no compared prose figure could be swapped for another field's "
                 "value, so nothing here tests the wrong-field case this check exists for")

    # 8. **A declared document quoting a figure its own account does not print.** The drift the
    # coverage split actually took, seeded the way it happened: one live sentence, one number.
    live = [r for r in declared(table, outputs)[0] if r[0] == "compared"]
    if not live:
        sys.exit("SELF-TEST FAILED: no sentence in any declared document states a figure as part "
                 "of a whole a command prints, so the half of this check that watches the other "
                 "documents is inert")
    staled = None
    for _kind, rel, n, _why in live:
        src = io.open(os.path.join(ROOT, rel.replace("/", os.sep)), encoding="utf-8").read()
        pat = re.compile(r"(?<![\w.$-])%s(?![\w.%%-])" % re.escape(n))
        for hit in range(len(pat.findall(src))):
            seen_n = [0]

            def once(m, k=hit):
                seen_n[0] += 1
                return str(int(m.group(0).replace(",", "")) + 7) if seen_n[0] == k + 1 \
                    else m.group(0)

            moved = pat.sub(once, src)
            if [r for r in declared(table, outputs, {rel: moved})[0] if r[0] == "STALE"]:
                staled = (rel, n)
                break
        if staled:
            break
    if staled is None:
        sys.exit("SELF-TEST FAILED: every figure a declared document states as part of a whole was "
                 "moved off its own account and the run stayed green. That is the 80/81/82 drift, "
                 "undetected in the five documents it drifted in")
    return True


def report(values):
    text = io.open(README, encoding="utf-8").read()
    rows, prose_rows, _seen, table, outputs = audit(text)
    doc_rows, unanchored = declared(table, outputs)
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
        if kind in ("UNDECLARED", "STALE"):
            print("  %-10s prose numeral %s - %s" % (kind, n, why))
    dead = stale_exclusions(text)
    for where, key, why in dead:
        print("  %-10s %s declares %r and the page no longer carries it - %s"
              % ("STALE", where, key, why))
    dc = {}
    for kind, rel, n, why in doc_rows:
        dc[kind] = dc.get(kind, 0) + 1
        if kind == "STALE":
            print("  %-10s %s states %s - %s" % (kind, rel, n, why))

    # **What was compared, not just how many.** A binding nobody can read is a claim to be taken on
    # trust, which is the thing this file was written to stop doing.
    print("\n  prose figures, and the field each is bound to")
    for kind, n, why in prose_rows:
        if kind == "compared":
            print("    %-6s %s" % (n, why))

    print("\n  fenced blocks")
    for k in ("command", "compared", "volatile", "excluded", "UNDECLARED", "FAILING"):
        if counts.get(k):
            print("    %-12s %3d" % (k, counts[k]))
    print("    %-12s %3d   = every fence, so the account is a partition" % ("total", len(rows)))
    print("\n  prose numerals")
    for k in ("compared", "excluded", "UNDECLARED", "STALE"):
        if pc.get(k):
            print("    %-12s %3d" % (k, pc[k]))
    print("    %-12s %3d" % ("total", len(prose_rows)))
    print("\n  the same figures in %d document(s) that paste no output" % len(DECLARED_DOCS))
    for k in ("compared", "excluded", "STALE"):
        if dc.get(k):
            print("    %-12s %3d" % (k, dc[k]))
    print("    %-12s %3d   = in a sentence that names no field, so not judged"
          % ("unanchored", unanchored))
    print("\n  exclusions")
    print("    %-12s %3d" % ("declared", len(EXCLUDED_FENCES) + len(EXCLUDED_PROSE)))
    print("    %-12s %3d   = an excusal whose subject has left the page" % ("STALE", len(dead)))

    drift = [r for r in rows if r[0] == "volatile" and r[3]]
    if values and drift:
        print("\n  paste these:")
        for _k, _s, _w, extra in drift:
            for _was, now in extra:
                print("    %s" % now)

    # **A stale exclusion fails the run**, decided 2026-08-10 with reporting-only as the rival: it is
    # a written claim the page contradicts, which is the same kind of thing as a stale figure, and
    # `audit.py` exits on its equivalent. Reporting it would keep the run green while a false
    # statement sits in the tool - the state this check was written from (T-077).
    fails = (counts.get("FAILING", 0) + counts.get("UNDECLARED", 0)
             + pc.get("UNDECLARED", 0) + pc.get("STALE", 0) + len(dead) + dc.get("STALE", 0))
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
