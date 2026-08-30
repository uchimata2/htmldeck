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

**Two kinds of number, and one rule cannot hold both.** A figure that describes a *decision* - 165
rule rows, 119 hard rules, 25 that need a person - moves when somebody changes the ruleset, which is
rare and deliberate. A figure that counts the *repository* moves on every documentation commit,
**including the commit that corrects it**, which is why re-deriving it has never converged (T-067
§4). So a figure is `compared` and fails the run on any drift, or it is a `floor`, declared below
with the reason: **the run may print more and never redden, and a pasted `0` is exact**, because
zero as a lower bound asserts nothing. Every one of T-056's six was a ruleset count, so nothing is
weakened by treating the three that count documents as bounds.

*Until T-154 the second kind was `volatile` - masked digit by digit and reported rather than
enforced. That excused the wrong half: `0 broken` and `0 dead` carry the whole evidence of the block
they sit in and were the two figures in it nothing could ever fail on.*

Runs its own self-test first and refuses to report if it fails (**L-04**). Pure standard library
(**L-07**).
"""

import io
import os
import re
import shlex
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
#
# **It stays narrow, and T-154 widened it for a day before measuring what that would suppress.**
# `pipeline.md` writes `| 6 - per-batch automatic checks | ~~The build check~~ - **built
# 2026-08-09.** ... gates 84 of the 115 rules ... |`, which matches *strike, then a bolded date* and
# is **not** a record: that table's columns are `Stage | Owned by | Until then`, the strike is on the
# name of the **gap**, and the sentence after it describes what an adopter's plugin does now. Marking
# it would have taken a stale figure out of the watched set inside the shipped skill - defect One
# again, self-inflicted, by the task written to end it. Read the row before trusting its shape.
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

# Blocks whose counts move on every documentation commit - including the one that corrects them -
# so an exact comparison has never converged (T-067 §4). **They are compared as floors, not
# excused.**
#
# **`volatile` was here until T-154, and it excused the wrong half.** Under it every digit run in
# the block was masked before comparison, so `0 broken` and `0 dead` - the two figures in it that
# never drift and carry all of its evidence - were unenforceable alongside the three counts that
# drift constantly. Seeded and measured: a README announcing `3 broken`, or `9 dead` section
# references, passed the run and was reported as drift, mixed into the pointer-count drift a reader
# has been taught to skip. A category that has never failed and never can is not a second opinion,
# so it is retired rather than kept beside this one.
#
# What a floor asserts is in `floor_breaches`. The reason below is still the excusal for not
# comparing exactly, and what would close it is a figure that does not count its own source.
FLOOR = {
    "python tools/docs/refcheck.py":
        "every count is of documents in this repository, so it is stale in the very commit that "
        "corrects it - re-derived three times in one session and wrong again each time (T-067 §4)",
}

# Fenced blocks that are not a command's output, each with the reason. An unlisted unbound fence
# fails the run: the partition is the point, and a silent third category is how six figures went
# stale under a rule that was already in writing.
# **How far after a command an output fence may open, in lines, counting from the command's own
# closing fence** (T-246, `PR-67`). Two is the minimum a closing fence plus one blank line allows and
# is what every genuine pair in the tree measures; the two false ones measured 73 and 113. Derived,
# not chosen - the census is in `bind()`'s docstring.
GAP = 2

EXCLUDED_FENCES = {
    "/plugin marketplace add": "typed into Claude Code; there is no local command to run",
    "git clone https://": "clones this repository; running it would fetch the network every check",
    "claude plugin update": "upgrades an installed plugin on the reader's machine",
    "taskmd check": "belongs to another project's tool, and no output is pasted under it",
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

# ------------------------------------------------------------------- the account a claim is about
# **The binding was anchored on the value that drifts, so a claim left the watched set precisely
# because it went wrong** (T-154). `claimed()` found the account by asking which field carried the
# *whole* as its value; nothing printed `113` any more, so *"82 of the 113 rules a gate owns"* bound
# to nothing and fell into `unanchored` with 420 numerals that are not figures at all. Three live
# documents and the shipped skill held that sentence with every gate green. It is `self_test`
# fixture 9's own rule - *a fixture may assert what the page's wording binds; it may not require the
# page to be right first* - broken in the production path.
#
# So the whole gets a second chance: an **account**, declared here, naming the command and the two
# labels that carry the part and the whole. A sentence with the *part of whole* shape whose words
# name the **whole's label** is held to that account, whatever value it states.
#
# **This is a hand-kept list and it is allowed on `ARTIFACTS`' condition, not on convenience**: an
# account whose label no command prints fails the run (`missing_accounts`), so it cannot quietly
# cover nothing. It names *which account*, never which sentence and never which numeral - what binds
# stays derived from the page.
#
# **Why the sentence still has to earn it.** Binding a whole sentence on one of a gate's words was
# tried and produced 30 false alarms against 5 true ones (T-068), which is why the shape came first.
# The shape stays the trigger; the account only decides *which* numbers a triggered sentence is held
# to. Measured over the six documents this tool reads, the shape fires 8 times and the account
# claims 4 of them - the four that were the drifted split.
ACCOUNTS = {
    "the gate's coverage of the ruleset": {
        "command": "python tools/deck/check.py examples/reference-deck.html",
        "part": "checked",
        "whole": "owned by a gate",
    },
}

# ---------------------------------------------------------------- a property of a named artifact
# **The third binding, and the narrowest of the three** (T-088). `bound()` needs the sentence to name
# the field's label and `claimed()` needs the *part of whole* shape; a page that says *"it is 220 KB
# in one file, 12 slides"* has neither, and two figures of exactly that shape went stale inside the
# `unanchored` bucket while the front README's bound copies of the same properties stayed correct.
#
# Three conditions together, and each is doing work:
#   1. the **block** links the artifact - not names it, links it. `sentences()` splits *"It is 220 KB"*
#      off from the sentence that says what *it* is, so a sentence-level test cannot see the subject.
#      A link is the one reference a paragraph makes that cannot be a coincidence of vocabulary,
#      which is the whole objection T-068 sustained against binding by words;
#   2. the numeral is followed by a **unit** naming a property this tool computes, within three
#      words and with no other numeral between - so `97 KB of it as base64` binds to `KB` and is
#      then judged, while `slides 1, 5, 8` binds to nothing;
#   3. the artifact is in `ARTIFACTS`, so what may be claimed is declared rather than inferred.
#
# A spelled-out number counts here and nowhere else in this file. `EXCLUDED_PROSE`'s rule - a figure
# is a numeral - holds over free prose, where "two days" outnumbers measurements six to one. Inside
# these three conditions the noun has already said it is a count: *"six hand-written SVG figures"* is
# the figure `v0.2.0` corrected, and it was written as a word both before and after.
# Keyed by `stem()`'s output, not by the word: `stem` strips the plural and then a trailing `e`
# unconditionally, so `bytes` arrives as `byt` and `slides` as `slid`. Written out because keying
# this by the readable form silently matched two of the four units and nothing said so - the run
# went green having judged half of what it claims to judge.
ARTIFACT_UNITS = {"kb": "KB", "byt": "bytes", "slid": "slides", "figur": "figures"}

WORD_NUMBERS = dict((w, i) for i, w in enumerate(
    "one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen "
    "sixteen seventeen eighteen nineteen twenty".split(), 1))

# A digit run may carry spaces as thousands separators - `225 639 bytes` is one figure, and
# `PROSE_NUMERAL` reads it as two. The unit is what says where the number ends.
ARTIFACT_NUMERAL = re.compile(r"(?<![\w.$-])(\d[\d ,]*\d|\d|[A-Za-z]+)")
LINK_TARGET = re.compile(r"\]\(([^)#\s]+)")


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


def blocks(text):
    """`[(block, [(sentence, is_dated_record)])]` - prose split twice, and both units are needed.

    A figure is bound inside a **sentence** by every rule here but one: a property of a named
    artifact is bound inside the **block**, because *"It is 220 KB in one file"* is a sentence whose
    subject is in the sentence before it (T-088).

    Table cells are their own sentences: a row states one claim per cell, and a wrapped markdown
    paragraph states one across several lines, so newlines join and `|` splits.

    **A record dates its own row and nothing else** (T-155). `dated` was computed once per block, so a
    single `~~...~~ **done 2026-08-10**` row switched `claimed()` off for every live claim sharing its
    table - the value that excuses a figure taken from a scope wider than the figure. The split is
    `claim_scopes()`, which T-088 and T-129 had already settled for the same question about a link's
    subject; using a second rule here would be two answers to one question (**L-13**).
    """
    out = []
    for block in re.split(r"\n\s*\n", text):
        sents = []
        for scope in claim_scopes(block):
            dated = bool(DONE_ROW.search(scope))
            for cell in scope.split("|"):
                for s in SENTENCE_END.split(" ".join(cell.split("\n"))):
                    if s.strip():
                        sents.append((s, dated))
        out.append((block, sents))
    return out


def sentences(text):
    """`[(sentence, is_dated_record)]` over prose - the unit a figure is bound inside."""
    return [s for _block, sents in blocks(text) for s in sents]


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


def near_miss(numeral, said, table):
    """`[(value, label, command)]` - fields this sentence NAMES that carry a different value,
    nearest first.

    **This is a message, not a verdict** (T-173). `bound` needs the value and the label to agree, so
    a figure that has gone stale fails both halves at once and the report could only reach for the
    weaker sentence: *no command prints it under a label this sentence names*. True, and it describes
    a numeral nothing watches - where what happened is that a watched numeral went wrong. The same
    drift on the same property of the same file reads `STALE ... which is 263` two lines below, on
    the path that binds through a link.

    **The cost was measured.** [T-172] was specified against that message and planned to bind a
    figure that was already bound; correcting the value was the whole fix. A report that names the
    wrong failure buys a wrong plan from whoever reads it.

    It stays out of the verdict on purpose. Nothing here knows the sentence means this field rather
    than an unrelated number sitting near it, and a kind that claimed to would be the
    coincidence-matching **L-36** and **L-44** refused - which is why `bound` needs both halves in
    the first place.
    """
    hits = []
    for value, label, cmd in table:
        if value == numeral:
            continue
        lw = words(label)
        if lw and (lw & said):
            hits.append((value, label, cmd))

    def distance(hit):
        try:
            return abs(int(hit[0].replace(" ", "").replace(",", ""))
                       - int(numeral.replace(" ", "").replace(",", "")))
        except ValueError:
            return float("inf")

    return sorted(hits, key=distance)


def unbound_why(numeral, said, table):
    """The one line an `UNDECLARED` prose numeral carries - the near miss when there is one."""
    near = near_miss(numeral, said, table)
    if not near:
        return ("no command prints it under a label this sentence names, and it is excused nowhere")
    value, label, cmd = near[0]
    return ("no command prints %s under a label this sentence names. The sentence DOES name %r, "
            "whose nearest value is %s, printed by %s - if that is this figure it is STALE rather "
            "than unwatched, and correcting it binds it" % (numeral, label, value, cmd))


def account_values(table, accounts=None):
    """`{name: {"part": v, "whole": v, "command": cmd}}` for every account both labels resolve for.

    An account is resolved only from a field printed by **its own declared command**, so a label as
    ordinary as `checked` cannot pick up another tool's line.
    """
    out = {}
    for name, spec in sorted((ACCOUNTS if accounts is None else accounts).items()):
        got = {}
        for value, label, cmd in table:
            if cmd != spec["command"]:
                continue
            for role in ("part", "whole"):
                if label == spec[role] and role not in got:
                    got[role] = value
        if len(got) == 2:
            got["command"] = spec["command"]
            out[name] = got
    return out


def missing_accounts(table, accounts=None):
    """`[(name, role, label, command)]` for every declared label its command does not print.

    **This is what buys `ACCOUNTS` its place**, on exactly the terms `missing_artifacts` won for the
    artifact manifest: a hand-kept list is acceptable where it cannot cover nothing in silence. A
    renamed output label would otherwise switch this binding off and leave the count reading as
    though the split were still watched.
    """
    have = account_values(table, accounts)
    out = []
    for name, spec in sorted((ACCOUNTS if accounts is None else accounts).items()):
        if name in have:
            continue
        printed = set(l for _v, l, c in table if c == spec["command"])
        for role in ("part", "whole"):
            if spec[role] not in printed:
                out.append((name, role, spec[role], spec["command"]))
    return out


def account_for(said, table, accounts=None):
    """The account whose **whole** label this sentence names, or `None`.

    The whole is what the shape puts the claim's subject on - *"of the 115 **rules a gate owns**"* -
    and holding the sentence to the part's label as well would demand the page use the gate's own
    word for both halves, which is the paraphrase `claimed()` exists to survive.
    """
    for name, got in sorted(account_values(table, accounts).items()):
        spec = (ACCOUNTS if accounts is None else accounts)[name]
        lw = words(spec["whole"])
        if lw and (lw & said):
            return name, got
    return None


def claimed(sentence, table, outputs, accounts=None):
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
            # **The whole has drifted, or this is not a claim about an account at all.** Only a
            # declared account can tell those apart, and it does it from the sentence's words
            # rather than from its numbers - which is the whole repair (T-154).
            got = account_for(said, table, accounts)
            if got is None:
                continue
            name, acc = got
            if whole != acc["whole"] or part != acc["part"]:
                out[whole] = ("STALE", "claimed as the whole of %s, which is %s"
                                       % (name, acc["whole"]))
                out[part] = ("STALE", "claimed as %s of %s, and %s prints %s of %s"
                                      % (part, whole, acc["command"], acc["part"], acc["whole"]))
                # **The remainder is judged against the account, not against the sentence.** Both
                # halves of `82 of 113` were stale and `113 - 82` is still 31, which is also
                # `115 - 84`; calling that numeral stale would put a figure that needs no edit in
                # the list of figures to fix, in a message saying it is 31.
                rest = int(acc["whole"]) - int(acc["part"])
                for r in REMAINDER.finditer(sentence[m.end():]):
                    got_rest = int(r.group(1).replace(",", ""))
                    out[r.group(1)] = (
                        ("compared", "the remainder of %s, %s - %s, which this sentence states"
                                     % (name, acc["whole"], acc["part"]))
                        if got_rest == rest else
                        ("STALE", "stated as the rest of %s after %s, and %s leaves %s"
                                  % (whole, part, name, rest)))
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

    **`directly after` is measured, and until T-261's batch it was not** (`PR-67`). The loop carried
    `pending` forward to whatever fence came next, however much prose and however many headings lay
    between - so *adjacency* named the docstring's intent and the code implemented *eventually*. Two
    pairs in the tree were bound across 73 and 113 lines and both were being compared: a command
    shown in a plain fence in `PUBLISHING.md`, and a `check.py` account in `examples/README.md`. The
    threshold is **derived rather than chosen**: across every tracked document the gaps were 2, 2, 2,
    2, 2, 73, 113 - five genuine pairs at the minimum a closing fence and a blank line allow, then
    nothing at all until the two false ones. `GAP` is that measurement, and a pair further apart is
    `UNDECLARED`, which fails the run rather than passing quietly.
    """
    out, pending = [], None
    close = {}
    for start, lang, body in blocks:
        close[start] = start + len(body) + 1
    for start, lang, body in blocks:
        cmd = " ".join(l.strip() for l in body if l.strip())
        if pending is not None and start - close[pending[1]] > GAP:
            pending = None
        if lang == "bash" or (lang == "" and not pending and not RUNNABLE.match(cmd)):
            reason = None
            for prefix, why in EXCLUDED_FENCES.items():
                if cmd.startswith(prefix):
                    reason = why
                    break
            if lang == "bash" and RUNNABLE.match(cmd) and reason is None:
                pending = (cmd, start)
                out.append(("command", start, cmd, body))
            else:
                pending = None
                out.append(("excluded" if reason else "UNDECLARED", start,
                            reason or "a fenced block bound to nothing and declared nowhere", body))
        elif pending:
            out.append(("output", start, pending[0], body))
            pending = None
        else:
            out.append(("UNDECLARED", start,
                        "an output block with no command above it", body))
    return out


# ---------------------------------------------------------------------------- the commands


# The decks are a source of figures like any command, and are named like one so a report can say
# where a value came from.
DECK_FACTS = "the deck files themselves"

# **The artifacts whose properties a document may state as a figure**, each with why it is here.
# A manifest kept by hand, which `PUBLISHING.md` §2 is an argument against - so it is allowed one
# thing only: it names *which files*, never which sentences or which numerals, so what binds stays
# derived from the document and the file.
#
# **What makes a hand-kept list acceptable here is that it cannot go stale in silence.** An entry
# naming a file that has moved or gone fails the run (`missing_artifacts`), rather than emitting no
# fields and covering nothing - the shape T-051 settled for a check with no subject, and the
# condition the owner's 2026-08-11 answer rests on (T-088). The old code skipped a missing path with
# `if os.path.exists`, which is exactly the silence.
ARTIFACTS = {
    "examples/reference-deck.html":
        "the hand-built reference deck; README.md and examples/README.md both state its size and "
        "slide count",
    "examples/sort-window/sort-window.html":
        "the deck nobody authored by hand, which is what README.md points at as the generated "
        "example - and the file both of v0.2.0's stale figures were about",
    "examples/measure-first/measure-first.html":
        "the deck an adopter built, published by T-128; examples/README.md states its size and "
        "slide count, and it is the one deck here whose size moves for a reason nobody in this "
        "repository decided - an upstream author's edit, arriving through a copy rather than "
        "through a commit",
    "examples/portfolio-review/portfolio-review.html":
        "the chart-first deck T-113 built to cost hand-authored SVG against a library; "
        "examples/README.md states its size, slide count and figure count, and the figure count is "
        "the one this manifest watches that the others do not - it is what the deck is FOR, so a "
        "figure added or lost is the claim moving. Added by T-226, which found the deck in neither "
        "human-facing document a release after it shipped",
}

_RUNS = {}


def run(cmd):
    """The command's combined output, run at most once per process.

    **The cache is not an optimisation.** `check.py` drives real headless Chrome, and the self-test
    audits the document six times over - once clean and once per staled fixture. Without this the
    fixtures cost six browser launches and the tool times out before it reports anything, which is
    a check nobody waits for (**L-40**).
    """
    if cmd not in _RUNS:
        # **`shlex`, not `str.split`.** Every command in the README is bare words, so the two agreed
        # and the weaker one was never wrong. A measurement fence is not: `python -c "import
        # pathlib;[print(...)]"` is three arguments, and `.split()` shreds the third into fourteen.
        argv = shlex.split(cmd)
        if argv[0] == "python":
            argv[0] = sys.executable
        p = subprocess.Popen(argv, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        _RUNS[cmd] = p.communicate()[0].decode("utf-8", "replace").replace("\r\n", "\n")
    return _RUNS[cmd]


def artifact_path(rel):
    return os.path.join(ROOT, rel.replace("/", os.sep))


def missing_artifacts(manifest=None):
    """`[(rel, why)]` - every manifest entry whose file is not there.

    **This is what buys the manifest its place.** A hand-kept list is acceptable only where it
    cannot cover nothing quietly, so an entry that has moved is a failure of this tool and not a
    property of the documents it reads (T-088). Takes the manifest as an argument so the fixture can
    hand it a missing file without mutating the module.
    """
    return [(rel, why) for rel, why in sorted((ARTIFACTS if manifest is None else manifest).items())
            if not os.path.exists(artifact_path(rel))]


def artifact_facts():
    """`{rel: {property: value}}` for every manifest artifact that is on disk.

    **Four properties, and each is a claim some document already makes.** `KB` and `bytes` are the
    same size stated two ways, because `examples/README.md` states it both ways in one sentence and
    only the rounded half was ever derivable here - so the exact figure sat unwatched beside a
    watched one, and at `v0.2.0` both were wrong.
    """
    out = {}
    for rel in sorted(ARTIFACTS):
        path = artifact_path(rel)
        if not os.path.exists(path):
            continue
        html = io.open(path, encoding="utf-8").read()
        out[rel] = {"KB": int(round(os.path.getsize(path) / 1024.0)),
                    "bytes": os.path.getsize(path),
                    "slides": len(re.findall(r'class="slide"', html)),
                    "figures": len(re.findall(r'class="[^"]*\bfig\b', html))}
    return out


def deck_facts():
    """Sizes and slide counts the prose states, so each is a figure rather than a recollection.

    **One fact per line, because the line is what carries the label.** `221 KB` and `12 slides` on
    one line would leave the second labelled ` KB `, binding nothing. The slide count is here
    because the page states it twice and no command printed it: both numerals were reported
    `compared` against `8-12` inside a `DS-082` triage note - a coincidence, in the one place this
    tool exists to refuse them. Counted from the markup; the reference deck's colophon carries
    `slide close` and is not one of the twelve, which is why the page says "and a colophon".

    **The byte count is a field of its own, beside the rounded KB.** `examples/README.md` states
    both - *"212 KB in one file - 217 050 bytes"* - and only one of them was ever derivable here, so
    the exact figure was unwatched while the rounded one beside it was not. Both were wrong at
    `v0.2.0`.

    A path missing from disk emits nothing here and is reported by `missing_artifacts`; skipping it
    silently is what this function used to do.
    """
    out = []
    for rel, props in sorted(artifact_facts().items()):
        for prop in ("KB", "bytes", "slides", "figures"):
            out.append("%s %d %s" % (rel, props[prop], prop))
    return "\n".join(out)


# ------------------------------------------------------- a figure the document measures but pastes
# **The fourth binding, and the first that runs a command no output is pasted under** (T-158).
#
# `CLAUDE.md` states the two figures that govern what every session of this project pays, carries the
# command that produces them in a fence, and pastes nothing under it. So `bind()` saw a command and
# never ran it, `fields()` got no labels from it, and both figures sat in `unanchored` among 413.
# Measured: the pair drifted 15,034 -> 15,208 with nothing reporting it, and the page's own debt note
# records that the statement *has now been wrong in both terms twice*.
#
# **The comparison runs the other way round from every other rule here, and the page is why.**
# Elsewhere a written numeral must be printed by a command. Held to that, this page fails twice over:
# its live sentence says *"15,208 bytes against `tasks/TASK-WORKFLOW.md`'s 11,925"* and never writes
# `CLAUDE.md`, so the first term binds nothing; and the record sentence beside it says *"it read
# 18,807 against `.taskmd/config.md`'s 14,087"*, which names a label the command does print and would
# be reported STALE for stating what was true in the past. One term unwatched, one false alarm - T-068's
# measured result, on a page that deliberately keeps its own history.
#
# So: **every measured term must be written**, and a numeral the page states that nothing measures is
# a record and is not judged. It is the only direction that can be right about this page.
#
# **A per-document grant, and `RUNNABLE` is deliberately untouched.** That allowlist refuses to run
# what a document tells it to; widening its *shape* to admit `python -c` would let any fence in any
# scanned page run arbitrary code, which is the opposite of what it is for. An entry here authorises
# one command prefix in one named document instead. Hand-kept, on `ARTIFACTS`' and `ACCOUNTS`'
# condition: a declared fence the document no longer carries fails the run (`missing_measurements`),
# so it cannot come to cover nothing in silence.
MEASURED = {
    "CLAUDE.md": {
        "fence": 'python -c "import pathlib;',
        "subject": "CLAUDE.md",
        "why": "the tier-1 bound - the size of the file every session loads unasked, against the "
               "smallest document it defers to. Both figures are stated in prose and the command "
               "that produces them is fenced directly above with no output under it",
    },
}


def doc_text(rel, docs=None):
    """The declared document's text, from the fixture map when one supplies it."""
    if docs and rel in docs:
        return docs[rel]
    return io.open(os.path.join(ROOT, rel.replace("/", os.sep)), encoding="utf-8").read()


def measurement_fence(text, prefix):
    """The one fenced command in `text` that `prefix` authorises, or `None`."""
    for _start, _lang, body in fences(text):
        cmd = " ".join(l.strip() for l in body if l.strip())
        if cmd.startswith(prefix):
            return cmd
    return None


def missing_measurements(docs=None, entries=None):
    """`[(rel, prefix, why)]` - every declared measurement whose document no longer carries the fence.

    **This is what buys the entry its place**, the same way `missing_artifacts` buys the manifest its
    own: the page can be edited from under a declaration, and a grant that quietly stops matching
    would leave the two figures unwatched with every count in the report reading as though they were
    judged. That is the state T-158 was raised out of.
    """
    out = []
    for rel, spec in sorted((MEASURED if entries is None else entries).items()):
        if measurement_fence(doc_text(rel, docs), spec["fence"]) is None:
            out.append((rel, spec["fence"], spec["why"]))
    return out


def measurement(cmd):
    """`{path: size}` from a measurement's `<size> <path>` lines, separators normalised.

    `pathlib` renders a path with the platform's separator, so the same fence prints `docs\\BRIEF.md`
    here and `docs/BRIEF.md` elsewhere. Normalising is what keeps the subject resolvable on both.
    """
    out = {}
    for line in run(cmd).split("\n"):
        parts = line.split()
        if len(parts) == 2 and parts[0].isdigit():
            out[parts[1].replace("\\", "/")] = int(parts[0])
    return out


def measured_pair(sizes, subject):
    """`[(path, value)]` - the subject's own size, and the smallest of the rest.

    **The page's bound, restated as arithmetic over the same output**: *this file stays smaller than
    the smallest document it defers to*. Only the subject is declared; which document is the other
    term is derived, and it has already changed hands twice - which is precisely why naming it
    anywhere would be a third copy waiting to go wrong.

    Note what this does **not** compute: whether the subject is in fact smaller. The bound is
    knowingly unmet, and a check that failed on it would block every release until a debt this
    project has chosen to carry is paid. What is checked is the pair's *figures*.
    """
    rest = sorted((v, k) for k, v in sizes.items() if k != subject)
    if subject not in sizes or not rest:
        return []
    return [(subject, sizes[subject]), (rest[0][1], rest[0][0])]


def measured_rows(rel, text, spec):
    """`[(verdict, rel, value, why)]` - each measured term, and whether the document states it."""
    cmd = measurement_fence(text, spec["fence"])
    if cmd is None:
        return []
    pair = measured_pair(measurement(cmd), spec["subject"])
    if not pair:
        return [("STALE", rel, "-", "the fence this page carries printed no size for %r, so the "
                                    "pair cannot be formed and neither figure is watched"
                 % spec["subject"])]
    stated = set(m.group(1).replace(",", "") for m in PROSE_NUMERAL.finditer(prose(text)))
    rows = []
    for path, value in pair:
        if str(value) in stated:
            rows.append(("compared", rel, str(value),
                         "%s, measured by the fence this page carries" % path))
        else:
            rows.append(("STALE", rel, str(value),
                         "the fence measures %s at %s and the page states no such figure"
                         % (path, value)))
    return rows


def mask(line):
    """`line` with every run of digits replaced, so a floor block is paired on its shape."""
    return re.sub(r"\d+", "#", line)


def floor_breaches(pasted, actual):
    """`[complaint]` - every floor the run has fallen below, for a block compared as one.

    Two rules, and the second is the one the block exists for:

      * **a pasted count is a lower bound.** The run may print more and the page never reddens on
        growth, which is the only reason a figure counting this repository can be enforced at all;
      * **a pasted `0` is exact**, because zero as a lower bound asserts nothing. It is the one
        value where a floor and an exact claim cannot differ, so reading it as a floor is reading it
        as no claim - and `0 broken` and `0 dead` are the whole evidence of the block they sit in.

    Lines are paired by their masked shape, the way `drifted` pairs them, so a moved count is
    compared with the line it is a version of rather than with the line at the same index.
    """
    have = actual.split("\n")
    out = []
    for line in pasted:
        if not line.strip() or not re.search(r"\d", line):
            continue
        cand = next((c for c in have if mask(c).strip() == mask(line).strip()), None)
        if cand is None:
            continue
        was = [int(m.group(1).replace(",", "")) for m in CORPUS_NUMERAL.finditer(line)]
        now = [int(m.group(1).replace(",", "")) for m in CORPUS_NUMERAL.finditer(cand)]
        for w, n in zip(was, now):
            if w == 0 and n != 0:
                out.append("the page states 0 and the run prints %d - a floor of zero asserts "
                           "none, so this one is exact: %r" % (n, cand.strip()))
            elif w and n < w:
                out.append("the run has fallen below a stated floor, %d -> %d: %r"
                           % (w, n, cand.strip()))
    return out


def excerpt(pasted, actual, floor):
    """`(ok, [complaint])` - every pasted line must appear in `actual`, in order.

    **The blocks are excerpts and have to be compared as such.** `ruleset.py --counts` prints
    twenty-odd lines and the README pastes three of them; a whole-output equality test would fail
    on every block in the page and would prove nothing about any of them.

    For a **floor** block this decides only that the line is still there, in its shape - what the
    numbers on it are allowed to do is `floor_breaches`. The two were one test until T-154, and the
    masking that let a count grow also let `0 broken` become `3 broken`.
    """
    want = [l for l in pasted if l.strip()]
    have = actual.split("\n")
    if floor:
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
    """`[(pasted_line, actual_line)]` for floor lines whose digits have moved."""
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
        flo = what in FLOOR
        ok, bad = excerpt(body, actual, flo)
        if not ok:
            rows.append(("FAILING", start, "%s: %d line(s) absent from the run: %s"
                         % (what, len(bad), "; ".join(bad[:2])), None))
        elif flo:
            breach = floor_breaches(body, actual)
            if breach:
                rows.append(("FAILING", start, "%s: %s" % (what, "; ".join(breach)), None))
            else:
                rows.append(("floor", start, what, drifted(body, actual)))
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
                prose_rows.append(("UNDECLARED", n, unbound_why(n, said, table)))
    return rows, prose_rows, seen, table, outputs


def declared(table, outputs, docs=None, facts=None):
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
    facts = artifact_facts() if facts is None else facts
    rows, skipped, watched = [], 0, {}
    for rel in sorted(DECLARED_DOCS):
        text = doc_text(rel, docs)
        # **The document's own measurement runs first, and it is judged in the other direction** -
        # every term the fence measures must be written here, rather than every numeral written here
        # being printed by a command. Why that inverts for these pages is on `MEASURED`.
        judged = set()
        if rel in MEASURED:
            got = measured_rows(rel, text, MEASURED[rel])
            rows.extend(got)
            judged = set(n for _v, _r, n, _y in got)
        for block, sents in blocks(prose(text)):
            # **The block's own rule runs first, and it takes numerals out of the remainder.** A
            # figure it judged is judged; leaving it in `unanchored` as well would report the same
            # numeral in two buckets and make the count mean nothing.
            art = artifact_claims(block, rel, facts)
            for written, verdict, why, prop, art_rel in art:
                rows.append((verdict, rel, written, why))
                watched[(art_rel, prop)] = watched.get((art_rel, prop), 0) + 1
            spoken = sum(len(PROSE_NUMERAL.findall(w)) for w, _v, _y, _p, _a in art)
            for sentence, dated in sents:
                nums = [m.group(1) for m in PROSE_NUMERAL.finditer(sentence)]
                if not nums:
                    continue
                claims = {} if dated else claimed(sentence, table, outputs)
                for n in nums:
                    if n in claims:
                        rows.append((claims[n][0], rel, n, claims[n][1]))
                    elif spoken:
                        spoken -= 1
                    elif n.replace(",", "") in judged:
                        # Judged by the measurement above. Counting it as unanchored as well would
                        # report one numeral in two buckets, which is the rule the block's own claims
                        # already follow through `spoken`. A figure stated twice is one figure.
                        continue
                    else:
                        skipped += 1
    return rows, skipped, watched


def linked_artifacts(block, rel_doc):
    """Which manifest artifacts this block links to, resolved against the linking document.

    A link to the artifact's **directory** counts - `examples/README.md` writes
    ``[`sort-window/`](sort-window)`` and then describes the deck inside it, which is the paragraph
    both of `v0.2.0`'s stale figures were in.
    """
    here = os.path.dirname(rel_doc)
    out = []
    for m in LINK_TARGET.finditer(block):
        target = os.path.normpath(os.path.join(here, m.group(1))).replace(os.sep, "/")
        for rel in ARTIFACTS:
            if target in (rel, os.path.dirname(rel)) and rel not in out:
                out.append(rel)
    return out


LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+\.)\s")

# **A table row is a scope for the same reason a bullet is**, and for one more: a row states one
# claim about one thing, and the row under it states another about another, so a table that indexes
# several files links several artifacts in a single block. `examples/README.md` opens with exactly
# that table - three decks, three rows - and as one block it linked two manifest artifacts, which
# `scope_claims` declines to judge at all. Two true figures sat unbound in it for that reason and no
# other, and splitting the rows binds both with no new alarm anywhere (T-129).
TABLE_ROW = re.compile(r"^\s*\|")


def claim_scopes(block):
    """A block, split again at list-item and table-row boundaries - the scope a link's subject
    reaches over.

    **Measured, not assumed.** With the whole block as the scope, `BRIEF.md`'s *Definition of done*
    list bound *"all twelve slides carry a bottom line"* to a link thirty lines above it in another
    bullet. The verdict was right and the binding was luck, and a rule that is right by luck is the
    one T-068 rejected. A bullet is where a subject stops carrying (T-088).
    """
    out, cur = [], []
    for line in block.split("\n"):
        if (LIST_ITEM.match(line) or TABLE_ROW.match(line)) and cur:
            out.append("\n".join(cur))
            cur = []
        cur.append(line)
    if cur:
        out.append("\n".join(cur))
    return out


def artifact_claims(block, rel_doc, facts):
    """`[(figure_as_written, verdict, why, property, artifact)]` per claim scope, in document order.

    **A list, because two scopes can state the same numeral about different files.** This merged the
    scopes into a dict keyed by the written figure until T-129, and the day the index table split
    into rows both decks claimed `12 slides` - so the second row's verdict replaced the first row's
    and one of the two decks went unwatched while the count read as though both were judged. Nothing
    had triggered it before only because no two bullets of one block had ever linked different files.
    """
    out = []
    for scope in claim_scopes(block):
        # **The record excuses its own row** (T-155). This guard sat in `declared()` and read the
        # whole block, so an index table holding one struck-through deck stopped every live row in it
        # from being judged - and the count read as though they had been.
        if DONE_ROW.search(scope):
            continue
        out.extend(scope_claims(scope, rel_doc, facts))
    return out


def scope_claims(block, rel_doc, facts):
    """`[(figure_as_written, verdict, why, property, artifact)]` for properties this block states
    about a linked file.

    Returns nothing at all unless the block links **exactly one** manifest artifact: a paragraph
    comparing both decks states two figures the same way and there is no honest way to say which
    file each belongs to. Silence there is the point - an unanchored figure is a figure this tool
    declines to judge, and it stays a declared bucket.
    """
    linked = [rel for rel in linked_artifacts(block, rel_doc) if rel in facts]
    if len(linked) != 1:
        return []
    have = facts[linked[0]]
    out = []
    tokens = [(m.group(1), m.start()) for m in ARTIFACT_NUMERAL.finditer(block)]
    for i, (tok, _at) in enumerate(tokens):
        value = None
        if tok[0].isdigit():
            value = int(tok.replace(" ", "").replace(",", ""))
        elif tok.lower() in WORD_NUMBERS:
            value = WORD_NUMBERS[tok.lower()]
        if value is None:
            continue
        for k in range(i + 1, min(i + 5, len(tokens))):
            word = tokens[k][0]
            if word[0].isdigit() or word.lower() in WORD_NUMBERS:
                break
            prop = ARTIFACT_UNITS.get(stem(word.lower()))
            if not prop:
                continue
            # **A part of the file is not the file.** *"97 KB of it as base64"* states the size of
            # the three embedded typefaces, in the same sentence as the deck's own size and in the
            # same shape, and judging it against the whole would report the true sentence as STALE.
            # `of` directly after the unit is the whole of the signal, and it is the construction
            # rather than the vocabulary - which is what `claimed()` binds on for the same reason.
            if k + 1 < len(tokens) and tokens[k + 1][0].lower() == "of":
                break
            actual = have[prop]
            out.append((tok, "compared", "%s %s of %s" % (tok, prop, linked[0]), prop, linked[0])
                       if value == actual else
                       (tok, "STALE", "claims %s %s of %s, which is %d"
                        % (tok, prop, linked[0], actual), prop, linked[0]))
            break
    return out


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

    # **Adjacency, asserted on a page written here** (T-246, `PR-67`). The docstring said *directly
    # after* and the loop carried `pending` to whatever fence came next, however far. The fixture is
    # the register's own evidence: a command fence, prose and headings, then an unlabelled fence far
    # below. Both directions, because a threshold that never pairs is as wrong as one that always
    # does - and the near case is what stops the fix being "bind nothing".
    far = "\n".join(["```bash", "python tools/docs/cycles.py --list", "```"]
                     + ["", "## a heading", ""] + ["filler paragraph."] * 12
                     + ["", "```", "  7  docs/AUDIT-METHOD.md", "```"])
    kinds = [k for k, _l, _w, _b in bind(fences(far))]
    if "output" in kinds:
        sys.exit("SELF-TEST FAILED: a fence %d lines below a command was still bound to it as its "
                 "output. `bind()` says *directly after* and GAP is what makes that true (PR-67)"
                 % (len(far.split(chr(10))) - 4))
    near = "\n".join(["```bash", "python tools/docs/cycles.py --list", "```", "", "```", "  7  docs/AUDIT-METHOD.md", "```"])
    if [k for k, _l, _w, _b in bind(fences(near))] != ["command", "output"]:
        sys.exit("SELF-TEST FAILED: an output fence directly under its command was not bound to it "
                 "(%r). A threshold that pairs nothing passes every page by deciding nothing"
                 % ([k for k, _l, _w, _b in bind(fences(near))],))
    if not [r for r in rows if r[0] == "floor"]:
        sys.exit("SELF-TEST FAILED: no block is compared as a floor, so the split this tool exists "
                 "for is not exercised and the refcheck block must have stopped being bound")
    # **The grant has to still match a fence, and that is asserted here rather than only reported.**
    # Whether the two figures are *current* is `report()`'s to say - a real drift must redden the run,
    # not crash the self-test. Whether anything is watching them at all is this file's own contract.
    if missing_measurements():
        sys.exit("SELF-TEST FAILED: %s"
                 % "; ".join("%s no longer carries a fence starting %r, so nothing measures %s" % row
                             for row in missing_measurements()))
    if missing_accounts(table):
        sys.exit("SELF-TEST FAILED: %s"
                 % "; ".join("the account %r declares its %s as %r and %s prints no such label"
                             % row for row in missing_accounts(table)))

    # **Both fixtures are derived from the document, never quoted from it.** A hardcoded figure
    # here goes stale exactly like the ones this tool is watching, and a `replace` that matches
    # nothing stales nothing and passes - a fixture that tests nothing, reporting success
    # (**L-54**, **L-55**). So the line is found, its first number is moved, and the fixture
    # refuses to run if it could not find one.
    def stale_a(kind_wanted, delta=7, only_nonzero=True):
        for kind, _start, what, body in bind(fences(base)):
            if kind != "output":
                continue
            if (what in FLOOR) != (kind_wanted == "floor"):
                continue
            for line in body:
                nums = [m for m in re.finditer(r"\d+", line)
                        if not only_nonzero or int(m.group(0)) != 0]
                if nums:
                    at = nums[0]
                    moved = line[:at.start()] + str(int(at.group(0)) + delta) + line[at.end():]
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

    # 2. **A floor block, in all three of its directions** (T-154). It replaced a `volatile` block
    # that asserted one thing - *this must not fail* - and therefore could not fail at all, which
    # is how `0 broken` came to be unenforceable inside the check that exists to enforce figures.
    #
    # 2a. Growth is green, and still reported. The half that must NOT fail, or the check is
    # switched off within a week of the first documentation commit.
    line, grew = stale_a("floor", delta=-7)
    if line is None or grew == base:
        sys.exit("SELF-TEST FAILED: no floor block carries a non-zero number, so the half of the "
                 "split that must NOT fail is unexercised")
    rows2 = audit(grew)[0]
    if [r for r in rows2 if r[0] == "FAILING"]:
        sys.exit("SELF-TEST FAILED: a pointer count the run has grown past failed the run. It "
                 "grows on every documentation commit, and that is what the floor is for")
    if not [r for r in rows2 if r[0] == "floor" and r[3]]:
        sys.exit("SELF-TEST FAILED: a moved pointer count was neither failed nor reported, so "
                 "nothing can tell anyone it drifted")

    # 2b. **Falling below a stated floor is red.** The direction `volatile` could not express: a
    # count that goes down means documents or references have gone, which is news.
    line, sank = stale_a("floor", delta=10 ** 6)
    if line is None or sank == base:
        sys.exit("SELF-TEST FAILED: no floor line could be raised above the run, so the direction "
                 "that must fail is unexercised")
    if not [r for r in audit(sank)[0] if r[0] == "FAILING"]:
        sys.exit("SELF-TEST FAILED: the page was seeded with a floor the run does not reach (%r) "
                 "and stayed green. A floor nothing can fall below is the `volatile` category "
                 "again, under a new name" % line.strip())

    # 2c. **A pasted zero is exact**, asserted on the function rather than through the page,
    # because the page cannot be made to say the run found broken pointers - only the run can, and
    # a fixture may not wait for a real regression to prove it works (**L-78**, **L-85**). This is
    # the seeded defect T-154 measured: under digit-masking, `3 broken` against a pasted `0 broken`
    # passed and was reported as drift.
    if not floor_breaches(["OK - 100 pointer(s) checked, 0 broken"],
                          "OK - 120 pointer(s) checked, 3 broken"):
        sys.exit("SELF-TEST FAILED: a run reporting 3 broken pointers against a pasted `0 broken` "
                 "raised nothing. Zero as a lower bound asserts nothing, so it has to be read as "
                 "exact - that figure is the entire evidence of the block it sits in")
    if floor_breaches(["OK - 100 pointer(s) checked, 0 broken"],
                      "OK - 120 pointer(s) checked, 0 broken"):
        sys.exit("SELF-TEST FAILED: a clean run above a stated floor was reported as a breach, so "
                 "the rule fires on the ordinary case and would be switched off")

    # 3. An undeclared fence is a gap, not a silence.
    added = base + "\n\n```\nsomething nobody bound to anything\n```\n"
    if not [r for r in audit(added)[0] if r[0] == "UNDECLARED"]:
        sys.exit("SELF-TEST FAILED: a fenced block bound to nothing passed. The partition is the "
                 "whole point - a third category nobody sees is how the last six got through")

    # 4. So is an undeclared prose numeral.
    added = base + "\n\nThe gate owns 4242 rules.\n"
    if not [r for r in audit(added)[1] if r[0] == "UNDECLARED"]:
        sys.exit("SELF-TEST FAILED: a prose numeral no command prints was accepted")

    # 4a. **And the two reasons a numeral can be undeclared read differently** (T-173). Both rows
    # stay `UNDECLARED` - the verdict is right and only the sentence was wrong - but a figure whose
    # own subject is measured has to say so, because the message that could not led T-172 to plan a
    # binding the figure already had. Fixtures build their own table rather than reading the live
    # one (**L-78**).
    deck_table = [("263", "examples/reference-deck.html", "the deck files themselves"),
                  ("269083", "examples/reference-deck.html", "the deck files themselves")]
    named = words("the reference deck at examples/reference-deck.html is 262 KB")
    stale_line = unbound_why("262", named, deck_table)
    if "263" not in stale_line or "STALE" not in stale_line:
        sys.exit("SELF-TEST FAILED: a prose numeral whose own subject is measured did not say which "
                 "value that subject carries, so a stale figure still reads as an unwatched one: %s"
                 % stale_line)
    unwatched = unbound_why("4242", words("the gate owns 4242 rules"), deck_table)
    if "STALE" in unwatched or "263" in unwatched:
        sys.exit("SELF-TEST FAILED: a numeral nothing measures was offered a near miss, which is "
                 "the sharper message fired on the case it is not about: %s" % unwatched)
    if near_miss("262", named, deck_table)[0][0] != "263":
        sys.exit("SELF-TEST FAILED: the near miss is not ordered by distance, so a byte count can "
                 "be offered ahead of the rounded size the sentence actually got wrong")

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

    # 9. **The two claim shapes `v0.2.0` corrected** (T-088). Seeded from the real wording rather
    # than from a constructed sentence, because what has to be tested is that *this page's* way of
    # stating a property binds - the sentence says "It is", and the file it is about is named a
    # sentence earlier, which is why nothing caught these two the first time.
    #
    # **Found by the sentence's SHAPE, never by what the deck measures today** (T-127, **L-78**).
    # This built its seed from `artifact_facts()` and `replace`d the page's *correct* sentence until
    # 2026-08-13. On the one day that matters - the day the page has drifted - the replace matched
    # nothing, the seed was empty, and the fixture took the whole tool down saying `the tool itself
    # is wrong`, while the drift it exists to report sat in its own failure message. A fixture may
    # assert what the page's wording binds. It may not require the page to be right first, which is
    # the same substitution `shell.py` made in T-126.
    #
    # It also stopped being the *two* figures and became every claim of either shape the page binds.
    # Naming the deck's own two was what tied the fixture to the deck's own numbers.
    rel = "examples/README.md"
    src = io.open(os.path.join(ROOT, rel.replace("/", os.sep)), encoding="utf-8").read()
    NUMBER_WORDS = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
                    "eleven", "twelve")
    SIZE = re.compile(r"\*\*(\d[\d  ]*) KB in one file\*\*, (\d[\d  ]*) bytes")
    COUNT = re.compile(r"\b(%s)\b(?= hand-written SVG figures)" % "|".join(NUMBER_WORDS))

    # Every value any account prints. A seed has to avoid all of them, or the fixture can "stale" a
    # figure onto another correct number and then fail because nothing reported it - which is what
    # the first drifted page tried did: the page said 252, the seed added 8, and 260 is the right
    # answer. **A fixed delta is not a wrong value; not being in this set is** (**L-79**).
    # Renamed from `account_values` by T-154, which added a module function of that name; the local
    # shadowed it and fixture 12 called a set.
    printed_values = set(v for v, _label, _cmd in table)

    def moved_numeral(text):
        """The same figure, wrong, in the notation the page wrote it in - so the row that reports
        it is the row a reader would see, separators and all. `None` when no candidate is actually
        wrong, which the caller reports rather than seeding a figure that is secretly correct."""
        digits = int(re.sub(r"\D", "", text))
        sep = next((s for s in (" ", " ") if s in text), "")
        for delta in (8, 17, 33, 71, 137):
            n = digits + delta
            out = "{:,}".format(n).replace(",", sep) if sep else str(n)
            if out != text and out not in printed_values:
                return out
        return None

    def moved_word(text):
        """A different count word, and one no account prints - the same rule as the numerals."""
        return next((w for w in NUMBER_WORDS if w != text and w not in printed_values), None)

    # **`compared` OR `STALE` - binding is the question, not correctness.** A figure that has
    # drifted reports as `STALE`, which is *proof* it binds; counting only `compared` would drop it
    # out of its own shape on exactly the day it went wrong, and the fixture would then refuse for
    # want of a shape the page still carries. That is T-127's own defect one level further in, and
    # it was caught by seeding a real drift rather than by reading the code.
    bound = set(r[2] for r in declared(table, outputs)[0]
                if r[0] in ("compared", "STALE") and r[1] == rel)

    # **Every claim of these shapes must bind, not one of each shape** (T-129). The weaker form let
    # this page state one deck's size in a paragraph linking nothing while the other deck's identical
    # sentence bound: both shapes were exercised, the fixture was satisfied, and two figures drifted
    # 12 KB inside the `unanchored` bucket for a whole release. Requiring all of them is the
    # assertion that fails on the day the defect appears rather than at the next reading of the page.
    #
    # **It asserts what the page's wording BINDS, never that the page is right** - which is the line
    # T-127 drew and the reason a drifted figure counts as bound above. The one edit that trips it
    # honestly is a size sentence about a file outside `ARTIFACTS`, so the message names both
    # remedies; a fixture that fires without saying what to do is the one nobody can act on.
    claims, unbound = [], []
    for m in SIZE.finditer(src):
        for g in (1, 2):
            (claims if m.group(g) in bound else unbound).append(
                (m.start(g), m.group(g), moved_numeral(m.group(g)), "a size figure"))
    for m in COUNT.finditer(src):
        (claims if m.group(1) in bound else unbound).append(
            (m.start(1), m.group(1), moved_word(m.group(1)),
             "a figure count, which the page writes as a word"))
    if unbound:
        sys.exit("SELF-TEST FAILED: %s states %s (%s) and it binds to nothing, so no run can ever "
                 "report it stale - which is the state T-129 was raised from. Either link the file "
                 "inside that paragraph, row or bullet, the way the other decks' claims are linked, "
                 "or add it to ARTIFACTS if the manifest should carry it"
                 % (rel, unbound[0][3], unbound[0][1]))
    for _at, text, wrong, what in claims:
        if wrong is None:
            sys.exit("SELF-TEST FAILED: no wrong value could be built for %s (%r) - every candidate "
                     "is a value some account prints, so seeding it would test nothing"
                     % (what, text))
    numeral_claims = [c for c in claims if c[3] == "a size figure"]
    word_claims = [c for c in claims if c[3] != "a size figure"]
    if not numeral_claims or not word_claims:
        sys.exit("SELF-TEST FAILED: %s no longer binds both of the claim shapes T-088 was raised "
                 "for - '**N KB in one file**, N bytes' and 'N hand-written SVG figures'. Bound "
                 "values found: %r. One shape is now unexercised, which is how the two figures got "
                 "through the first time" % (rel, sorted(bound)))
    for at, text, wrong, what in claims:
        was = src[:at] + wrong + src[at + len(text):]
        if not [r for r in declared(table, outputs, {rel: was})[0]
                if r[0] == "STALE" and r[2] == wrong]:
            sys.exit("SELF-TEST FAILED: %s was re-seeded as %s and no row reported it. That is the "
                     "state this task was raised from - a figure about a named file, inside the "
                     "unanchored bucket, wrong and unwatched" % (what, wrong))

    # 10. **A manifest entry whose artifact is gone fails**, which is the condition the manifest was
    # allowed on. `PUBLISHING.md` §2 is an argument against hand-kept lists because they go stale in
    # silence; this one cannot, and the assertion is what makes that a property rather than a claim.
    if not missing_artifacts({"examples/no-such-deck.html": "a fixture entry, never on disk"}):
        sys.exit("SELF-TEST FAILED: a manifest entry naming a file that does not exist was not "
                 "reported. An entry that covers nothing in silence is this tool's own defect "
                 "(T-088), in the shape T-051 settled for a check with no subject")
    if missing_artifacts():
        sys.exit("SELF-TEST FAILED: the live manifest names %s, which is not on disk"
                 % ", ".join(rel for rel, _why in missing_artifacts()))

    # 11. **An account whose label no command prints fails**, which is the condition `ACCOUNTS` was
    # allowed on and the same one `ARTIFACTS` won (fixture 10). A renamed output label would
    # otherwise switch the coverage binding off and leave the counts reading as though four
    # documents were still held to it.
    if not missing_accounts(table, {"a fixture account": {
            "command": "python tools/deck/check.py examples/reference-deck.html",
            "part": "no command prints this label",
            "whole": "nor this one"}}):
        sys.exit("SELF-TEST FAILED: an account declaring labels no command prints was not "
                 "reported. A declaration that covers nothing in silence is this tool's own "
                 "defect, not a property of the documents it reads")

    # 12. **A claim whose whole has drifted off its account reports STALE rather than vanishing.**
    # This is T-154's defect One, and the fixture has to seed the *whole*: while the part alone
    # moves, `bound()` still finds the whole and the old path handles it. Derived from whatever a
    # declared document actually writes, so it cannot go stale when the ruleset grows - and the
    # replacement is a value no account prints, or the seed would be secretly correct (**L-79**).
    acc = account_values(table)
    if not acc:
        sys.exit("SELF-TEST FAILED: no declared account resolves, so the binding T-154 added is "
                 "inert and four documents are unwatched again")
    _name, got = sorted(acc.items())[0]
    printed = set(v for v, _l, _c in table)
    wrong = next((str(int(got["whole"]) + d) for d in (7, 19, 41, 83)
                  if str(int(got["whole"]) + d) not in printed), None)
    seeded = None
    for rel in sorted(DECLARED_DOCS):
        src = io.open(os.path.join(ROOT, rel.replace("/", os.sep)), encoding="utf-8").read()
        for m in CLAIM.finditer(prose(src)):
            if m.group(2) != got["whole"] or wrong is None:
                continue
            at = src.find(m.group(0))
            if at < 0:
                continue
            moved = (src[:at] + m.group(0).replace(got["whole"], wrong, 1)
                     + src[at + len(m.group(0)):])
            if [r for r in declared(table, outputs, {rel: moved})[0]
                    if r[0] == "STALE" and r[2] == wrong]:
                seeded = (rel, wrong)
            break
        if seeded:
            break
    if seeded is None:
        sys.exit("SELF-TEST FAILED: no declared document states this account as a part of a whole, "
                 "or moving the whole off the account reported nothing. That is the exact state "
                 "T-154 was raised from - the claim leaves the watched set BECAUSE it went wrong, "
                 "and four documents held the stale split with every gate green")

    # 13. **A record dates its own row, not the table it sits in** (T-155).
    #
    # **The defect has no instance in the tree**, which is exactly why it needs a fixture rather than a
    # code comment: T-154 wrote this fix, measured it as changing no verdict in any of the six
    # documents, and correctly declined to ship an unmeasured behaviour change. So the fixture builds
    # its own instance (**L-78**, **L-85**) - a two-row table, one row a dated record and one a live
    # claim about the same file. Under the block-scoped guard the record's date reaches the live row
    # and **both** go unjudged, with every count in the report reading as though they had been.
    fix_facts = {"examples/reference-deck.html":
                 {"KB": 1, "bytes": 2, "slides": 7, "figures": 3}}
    two_rows = ("| ~~[the deck](reference-deck.html) had 4 slides~~ **done 2026-08-10** | a record |\n"
                "| [the deck](reference-deck.html) has 7 slides | a live claim |")
    judged = artifact_claims(two_rows, "examples/README.md", fix_facts)
    if not [r for r in judged if r[0] == "7" and r[1] == "compared"]:
        sys.exit("SELF-TEST FAILED: a live claim sharing a table with a dated record went unjudged, "
                 "reported %r. That is the block-scoped guard T-155 removed - one struck-through row "
                 "switches off every live row beside it, and the count says nothing is missing"
                 % (judged, ))
    if [r for r in judged if r[0] == "4"]:
        sys.exit("SELF-TEST FAILED: the dated record itself was judged, reported %r. A record states "
                 "what was true then; holding it to today's figure reports a true sentence as stale"
                 % (judged, ))

    # The same split, one layer down, where `claimed()` reads it. `blocks()` marks a sentence dated
    # from the scope it sits in, so the two rows must disagree - and under block scope they cannot.
    marks = dict((s.strip(), d) for s, d in sentences(two_rows) if "slides" in s)
    if sorted(marks.values()) != [False, True]:
        sys.exit("SELF-TEST FAILED: a dated record and a live claim in one table were marked the "
                 "same way (%r), so `claimed()` is switched on or off for both together - which is "
                 "the scope error, whichever way it happens to land" % (marks, ))

    # 14. **A document that measures itself, in both terms and both directions** (T-158).
    #
    # **Built out of a synthetic page and a synthetic fence, never the live `CLAUDE.md`** (**L-78**,
    # **L-85**). That rule matters more than usual here: the subject of this check *is* a tracked
    # file whose size the task changed, so a fixture reading it would assert today's bytes and go red
    # on the next edit to the page - the drift it exists to report, reported as a broken test.
    #
    # The pair is stated with thousands separators and printed without, because the page this serves
    # writes `15,208` and the fence prints `15208`, and a check that missed the comma would pass by
    # never matching anything.
    fix_cmd = "python -c \"print('  1300  a.md');print('  1100  b.md');print('  2000  c.md')\""
    fix_spec = {"fence": "python -c \"print(", "subject": "a.md", "why": "a fixture"}

    def fixture(subject, other):
        return ("# Fixture\n\nA bound, measured by the fence below.\n\n"
                "```bash\n%s\n```\n\nThis file is %s bytes against `b.md`'s %s, measured today.\n"
                % (fix_cmd, subject, other))

    clean = measured_rows("fixture.md", fixture("1,300", "1,100"), fix_spec)
    if len(clean) != 2 or [r for r in clean if r[0] != "compared"]:
        sys.exit("SELF-TEST FAILED: a page stating both measured terms was not read as two compared "
                 "figures, it reported %r. The ordinary case has to be green or the check is "
                 "switched off the week it lands" % (clean, ))

    # Both terms, both directions. **Four seeds rather than two**: a figure goes stale by the file
    # growing or by the page being edited wrong, and only one of those moves the number downward.
    for term, subject, other, moved in (("the subject's own size", "1,301", "1,100", "1300"),
                                        ("the subject's own size", "1,299", "1,100", "1300"),
                                        ("the smallest of the rest", "1,300", "1,101", "1100"),
                                        ("the smallest of the rest", "1,300", "1,099", "1100")):
        got = measured_rows("fixture.md", fixture(subject, other), fix_spec)
        if not [r for r in got if r[0] == "STALE" and r[2] == moved]:
            sys.exit("SELF-TEST FAILED: %s was measured at %s and the page was seeded to say "
                     "something else (%s / %s), and the run reported %r. A pair nothing can fail on "
                     "is the state T-158 was raised from - 174 bytes drifted with nothing to say so"
                     % (term, moved, subject, other, got))

    # **A declared fence the page no longer carries fails**, which is the condition this grant is
    # allowed on at all. Without it the entry stops matching in silence and both figures go back to
    # being watched by nobody, with every count in the report reading as though they were judged.
    no_fence = "# Fixture\n\nThis file is 1,300 bytes against `b.md`'s 1,100, measured today.\n"
    if not missing_measurements({"fixture.md": no_fence}, {"fixture.md": fix_spec}):
        sys.exit("SELF-TEST FAILED: a declared measurement whose page carries no such fence was "
                 "accepted. A hand-kept grant is allowed here only because it cannot come to cover "
                 "nothing quietly, and that is the property just found missing")
    if missing_measurements({"fixture.md": fixture("1,300", "1,100")}, {"fixture.md": fix_spec}):
        sys.exit("SELF-TEST FAILED: a page that does carry its declared fence was reported as "
                 "missing it, so the rule fires on the ordinary case")

    return True


def report(values):
    text = io.open(README, encoding="utf-8").read()
    rows, prose_rows, _seen, table, outputs = audit(text)
    doc_rows, unanchored, watched = declared(table, outputs)
    print("README figures - %s\n" % os.path.basename(README))

    counts = {}
    for kind, start, what, extra in rows:
        counts[kind] = counts.get(kind, 0) + 1
        if kind in ("FAILING", "UNDECLARED"):
            print("  %-10s line %-4d %s" % (kind, start, what))
        elif kind == "floor" and extra:
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
    gone = missing_artifacts()
    for rel, why in gone:
        print("  %-10s the artifact manifest names %s and it is not there - %s"
              % ("MISSING", rel, why))
    unresolved = missing_accounts(table)
    for name, role, label, cmd in unresolved:
        print("  %-10s the account %r declares its %s as %r and %s prints no such label"
              % ("MISSING", name, role, label, cmd))
    unfenced = missing_measurements()
    for rel, prefix, why in unfenced:
        print("  %-10s %s no longer carries a fence starting %r, so nothing measures %s"
              % ("MISSING", rel, prefix, why))

    # **What was compared, not just how many.** A binding nobody can read is a claim to be taken on
    # trust, which is the thing this file was written to stop doing.
    print("\n  prose figures, and the field each is bound to")
    for kind, n, why in prose_rows:
        if kind == "compared":
            print("    %-6s %s" % (n, why))

    print("\n  fenced blocks")
    for k in ("command", "compared", "floor", "excluded", "UNDECLARED", "FAILING"):
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
    print("    %-12s %3d   = in a sentence naming no field and in no block linking an artifact, "
          "so not judged" % ("unanchored", unanchored))

    # **The accounts, and what each resolves to today.** A claim's *whole* is held to these, so a
    # reader can see which numbers four documents are being measured against without running the
    # gate - and a `MISSING` row above says the binding is off rather than merely quiet.
    print("\n  the declared accounts - a part-of-whole claim naming one is held to it")
    have = account_values(table)
    for name in sorted(ACCOUNTS):
        got = have.get(name)
        print("    %-42s %s" % (name, "UNRESOLVED" if got is None else
                                "%s of %s, from %s" % (got["part"], got["whole"], got["command"])))

    # **The measured pair, spelled out.** The same reason the accounts are printed above: a reader
    # can see the two numbers this page is held to without running the fence themselves, and a
    # `STALE` row says which term moved rather than that something did.
    print("\n  what a document measures itself - every term must be written on the page")
    for rel in sorted(MEASURED):
        pair = [r for r in doc_rows if r[1] == rel and r[3].endswith("this page carries")]
        stale = [r for r in doc_rows if r[1] == rel and r[0] == "STALE"]
        print("    %-42s %s" % (rel, "NO FENCE" if (rel, ) in [(m[0], ) for m in unfenced] else
                                ", ".join("%s %s" % (r[2], r[3].split(",")[0]) for r in pair + stale)
                                or "nothing measured"))

    print("\n  the artifact manifest - a property of one of these, in a block that links it, is a "
          "figure")
    facts = artifact_facts()
    for rel in sorted(ARTIFACTS):
        props = facts.get(rel)
        print("    %-42s %s" % (rel, "NOT ON DISK" if props is None else
                                ", ".join("%s %s" % (props[p], p)
                                          for p in ("KB", "bytes", "slides", "figures"))))

    # **How many documents each property is watched in, because a zero is the shape of this defect.**
    # The reference deck's size was stated on a published page and bound nowhere, and every count in
    # this report was of things the tool *did* judge - so nothing anywhere read as missing. A zero
    # here is not a failure on its own: a property no document states is correctly watched by nobody.
    # It is the one number that would have made T-129 visible without reading the page.
    print("\n    where each property is watched - a zero means no declared document binds a claim "
          "to it")
    for rel in sorted(ARTIFACTS):
        print("    %-42s %s" % (rel, ", ".join("%s %d" % (p, watched.get((rel, p), 0))
                                               for p in ("KB", "bytes", "slides", "figures"))))
    print("    %-12s %3d   = an entry whose file is not there, which fails the run"
          % ("MISSING", len(gone)))

    print("\n  exclusions")
    print("    %-12s %3d" % ("declared", len(EXCLUDED_FENCES) + len(EXCLUDED_PROSE)))
    print("    %-12s %3d   = an excusal whose subject has left the page" % ("STALE", len(dead)))

    drift = [r for r in rows if r[0] == "floor" and r[3]]
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
             + pc.get("UNDECLARED", 0) + pc.get("STALE", 0) + len(dead) + dc.get("STALE", 0)
             + len(gone) + len(unresolved) + len(unfenced))
    print("\n%s" % ("%d figure(s) to fix" % fails if fails else
                    "0 stale figure(s)%s" % (" - %d floor block(s) grew above what is pasted, "
                                             "which is reported rather than failed (see --values)"
                                             % len(drift) if drift else "")))
    print("\nThis checks that a pasted figure matches its command. It cannot tell you the sentence\n"
          "around it is still true - the README's \"all three are fixed\" went false with every\n"
          "figure on the page correct, and no gate here would have seen it (L-05).")
    return 1 if fails else 0


if __name__ == "__main__":
    self_test()
    sys.exit(report("--values" in sys.argv[1:]))
