#!/usr/bin/env python3
"""Check that every reference in this repository's documents resolves in a fresh clone.

    python tools/docs/refcheck.py

Four checks, all mechanical:

  1. **BROKEN LINK** - a markdown `[text](target)` whose target does not exist.
  2. **DEAD POINTER** - a repo-relative `.md` path written in **prose**, or printed by a tool into
     a fenced block. As much a promise as a link, and nothing else checks it.
  3. **DEAD SECTION** - a `<named document> §n` whose number is not a heading in that document.
  4. **LYING LABEL** - a link whose **label** names one `.md` file and whose target opens another.
     Checks 1 to 3 all resolve a *target*; this is the first that reads what the reader is told.

**Check 4 is the one defect class no pointer-resolver can reach.** A link whose target is right and
whose words are wrong passes every other check here and every check taskmd has, because all of them
ask *does this file exist* and none asks *is the sentence beside it true*. It was found twice, both
times by a person, and the second time inside a pass raised to catch exactly this (T-146, T-159).
The label and the target sit in one string, which is what makes this member of the class arithmetic
while the rest of it is not - the refusal to gate the others, and the numbers behind it, are
`tasks/TOOLING.md` §2.

**Why this file exists.** It is the reference half of the retired `task.py`, kept when taskmd
replaced the task half (T-062). taskmd's own `check` validates markdown links and is the
authority on tasks; it does not see checks 2 or 3, and reports `OK` on a repository carrying both.
Measured, not assumed - the seeded-defect comparison is in T-062 §1. The rule behind check 3 is
`tasks/TASK-WORKFLOW.md` §6.1, and this implements it.

**Why it is still here after upstream ruled.** taskmd decided in 2026-08-10 that its `check` resolves
Markdown link syntax and nothing else - no bare path, in prose or in a fence - and said so in its
README so the next project retiring its own checker knows what it gives up. The measurement behind that
decision included this repository's corpus and reported 31 dead bare pointers here, which reads as an
argument for deleting this file. It is not: those 31 come from a rule that resolves a path of **any**
extension, and check 2 above matches `.md` only. On this tree this file reports 0 broken. T-073 §3.

Keep it even if it ever stops running: taskmd's T-093, whether `check` resolves a **section**
reference, is still open, and this is the offered reference implementation - adjacency decision and
all (check 3).

**What this file deliberately does not check: a table row carrying more cells than its header.**
Markdown drops the excess, so the text is in the file and renders nowhere. Declined 2026-08-15
(T-161), for the second time and on different evidence: taskmd shipped exactly this rule as a
**problem that moves `check`'s exit status**, and a second instrument for a class that gate covers is
the checker-that-outlives-the-fault argument pointing at itself. Measured when the decision was taken:
**307 files, 0 wide rows, 0 unescaped pipes inside a code span.**

**The cover is not in place yet, and the refusal does not rest on it being.** Their gate is on upstream
master and unreleased: the installed skill is `0.5.0`, that is their latest release, and a seeded
three-cell row under a two-column header goes unreported by it - measured 2026-08-15 (T-163). So the
class is ungated here today, over a tree with nothing in it to catch, because T-139 swept the only two
rows this repository has ever had.

**What would reverse it, so it is not re-asked from scratch a third time:** `python tools/tasks/lint.py`
ceasing to run `taskmd check`. That is the whole of this repository's cover for the class, and losing it
is the reason to build the narrow thing here.

**The coverage gap this file claimed on 2026-08-15 does not exist.** `check` reads every Markdown
document a clone would receive - `skills/` and `examples/` included, nested taskmd projects and
untracked-and-ignored files excluded. taskmd corrected it on the report thread and it was reproduced
here with a seeded probe in each tree (T-163). **A trigger that cannot fire is worse than none**: it
reads as a decision made permanent rather than one taken on evidence. A wide row appearing in either
tree is therefore upstream's alarm, not a blind spot in both tools.

If the narrow thing is ever built, the trap is that GFM splits a row into cells **before** parsing
inline spans, so a backtick does not protect a pipe: blanking code spans first - which every other
text check here does - makes the rule silent on a row that is broken twice over. What to prove about
the fixture before believing its zeros is **L-103**.

Run it from the repository root. Task validation is `taskmd check`, not this.
"""

import contextlib
import fnmatch
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# The documents this repository's tooling, templates and prose send a reader to. Each one is a
# promise that the file is there, and this repository has to be clone-and-run (CLAUDE.md), so they
# are required by name. Named here so the pointer that gets printed and the pointer that gets
# checked cannot drift apart - the retired tool once reported "0 broken links" while two of these
# did not exist at all, because it only looked at markdown links between task files (L-09).
PROJECT_DOCS = {
    "CLAUDE.md": "the working conventions every task inherits",
    "docs/BRIEF.md": "what to build and why",
    "docs/LESSONS.md": "the carried lessons, cited as L-nn",
    "tasks/TASK-WORKFLOW.md": "the task standard, cited by the task template",
    "tasks/README.md": "the generated task index",
}

LINK = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(?:#[^)\s]*)?\)")

# Check 4 needs the label as well as the target; check 1 discards it, because resolving a target
# never had a use for it.
LABELLED_LINK = re.compile(r"\[([^\]]*)\]\(([^)#\s]+)(?:#[^)\s]*)?\)")

# A pointer written as prose - `docs/LESSONS.md` in a sentence, in a template comment, or in a
# string a tool prints - is as much a promise as a markdown link, and nothing checked those.
# Requires a slash, so a bare "README.md" in prose is not mistaken for a path to somewhere;
# a glob such as docs/research/R1-*.md cannot match, which is deliberate.
POINTER = re.compile(r"(?<![\w./-])((?:\w|\.\.?)[\w.-]*(?:/[\w.-]+)+\.md)\b")

# ---------------------------------------------------------------- section references (§6.1)
# Both halves exist so the number a reference cites is PRINTED in the document it points at.
DOC_STEMS = "DESIGN-SYSTEM|DESIGN-RATIONALE|EVALUATION|BRIEF|TASK-WORKFLOW|LESSONS|PUBLISHING"

# **Adjacency is the whole of the binding.** A document named earlier in the paragraph is not the
# target: tried against the corpus, "nearest document mentioned" picked the wrong file for a third
# of the misses it reported - `R4-prior-art.md` for a §2.1 that meant the citing document's own.
# So the name and the mark may be separated only by markdown punctuation and at most one space.
SECTION_REF = re.compile(
    r"(?P<doc>[A-Za-z0-9_./-]+\.md|\bR[1-9]\b|\bT-\d{3}\b|\b(?:%s)\b)"
    r"[`*\]\)_,]{0,4}[ ]?[`*\]\)_]{0,3}[ ]?§(?P<sec>\d+(?:\.\d+)*)" % DOC_STEMS)
SECTION_ANY = re.compile(r"§\d+(?:\.\d+)*")

# A numbered heading: `## 3.` or `### 2.1 ` - the trailing dot is optional because both forms are
# in use.
NUM_HEADING = re.compile(r"^#{1,6}\s+(\d+(?:\.\d+)*)\.?\s", re.M)
ANY_HEADING = re.compile(r"^#{1,6}\s", re.M)
ORDINAL = re.compile(r"^\s{0,3}(\d+)\.\s", re.M)

# Code is literal text, not a pointer. This is what lets a document quote a reference that is
# WRONG - the audit that found this family wrote `DESIGN-SYSTEM.md §11` a dozen times to say it
# never existed, and under any other rule the record of a dead pointer is itself one.
FENCE = re.compile(r"^```.*?^```", re.M | re.S)
CODE_SPAN = re.compile(r"`[^`\n]*`")


def strip_code(text):
    """Blank out fenced blocks and code spans, preserving offsets and line structure."""
    blank = lambda m: re.sub(r"[^\n]", " ", m.group(0))     # noqa: E731
    return CODE_SPAN.sub(blank, FENCE.sub(blank, text))


def links_in(text):
    """Every markdown link check 1 is entitled to resolve - the ones a reader can follow.

    **Link syntax inside code is a picture of a link.** It renders as the characters that were
    typed: nobody can follow it, so nothing can break it. Resolving it does not find a defect, it
    edits the evidence - this repository states results as what was actually produced, `taskmd
    index` prints one markdown link per row, and quoting a board row with an abridged filename
    therefore turned the run red until a *resolvable* target was substituted. A quotation adjusted
    to satisfy a link checker is no longer a quotation, and the adjustment is invisible afterwards
    (T-080).

    So the same `strip_code` the section scan already relied on governs check 1. The two scans
    disagree about **bare paths** on purpose - see `pointers_in`.
    """
    return LINK.finditer(strip_code(text))


def labelled_links_in(text):
    """Every link check 4 may read, as `(label, target)` - the label taken from the **raw** text.

    Two rules meet here and they pull opposite ways. A link inside code is a picture of a link and
    check 1 does not resolve it, so `strip_code` still decides which links are read at all. But the
    house convention writes the path in a label **inside a code span** - ``[`docs/BRIEF.md`](…)`` -
    and stripping code blanks the very string this check compares. Reading the label from the
    stripped text would leave check 4 silent on nearly every link it exists for, while reporting a
    confident zero.

    So the stripped copy is used only to ask *is this link followable*, and the label is then read
    where it was written.
    """
    stripped = strip_code(text)
    for m in LABELLED_LINK.finditer(text):
        if not stripped[m.start():m.end()].strip():
            continue                        # the whole link is inside code - see `links_in`
        yield m.group(1), m.group(2)


def label_disagrees(label, target, base):
    """`(what the label claims, what the link opens)` when they are not the same file, else `None`.

    **Both conventions in this repository are honest**, and accepting only one would turn a house
    style into 700 failures: a label may be written from the citing document's own directory, the
    way the target is, or from the repository root, the way a tool prints one. Either resolving to
    the target is a label that tells the truth. A third answer is a label that does not - which is
    exactly the shape found twice: a one-level path beside a target carrying the new two-level one.

    `POINTER` decides what counts as path-shaped, so check 2 and check 4 cannot drift apart about
    what a path is (**L-13**). A label with no path in it makes no claim and is not this check's
    business.
    """
    m = POINTER.search(label)
    if not m:
        return None
    claim = m.group(1)
    norm = lambda p: os.path.normpath(p).replace("\\", "/")     # noqa: E731
    opens = norm(os.path.join(base, target))
    if any(norm(c) == opens for c in (os.path.join(base, claim), claim)):
        return None
    return claim, opens


def pointers_in(text):
    """Every prose or printed pointer check 2 is entitled to resolve.

    **Fences are read here on purpose**, and that is the boundary rather than an oversight: a tool
    printing `docs/LESSONS.md` into a block makes the same promise a sentence does, and check 2 has
    caught real defects that way. It is also why blanket fence-skipping was the wrong ask upstream
    (T-080 §1). Front-matter is not prose, so it is not scanned - `strip_front_matter`.
    """
    return POINTER.finditer(strip_front_matter(text))


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def doc_aliases(paths):
    """Every name a document can be cited by -> its path.

    `DESIGN-SYSTEM.md`, `DESIGN-SYSTEM`, `R7`, `T-042`. Derived from the filenames present, so a
    renamed document changes what resolves without anything here being edited (**L-08**).
    """
    alias = {}
    for p in paths:
        if not p.endswith(".md"):
            continue
        base = os.path.basename(p)
        alias.setdefault(base.upper(), p)
        alias.setdefault(base[:-3].upper(), p)
        for pat in (r"^(R[1-9])-", r"^(T-\d{3})-"):
            m = re.match(pat, base[:-3])
            if m:
                alias.setdefault(m.group(1).upper(), p)
    return alias


def section_index(path):
    """(numbered headings, {heading: ordinals printed in a numbered list under it})."""
    return section_index_of(read(path))


def section_index_of(text):
    heads, ordinals = set(), {}
    starts = [m.start() for m in ANY_HEADING.finditer(text)]
    for m in NUM_HEADING.finditer(text):
        heads.add(m.group(1))
        nxt = next((s for s in starts if s > m.start()), len(text))
        found = {o.group(1) for o in ORDINAL.finditer(text[m.start():nxt])}
        ordinals.setdefault(m.group(1), set()).update(found)
    return heads, ordinals


def section_resolves(index, ref):
    """TASK-WORKFLOW.md §6.1: a heading, or a heading plus an ordinal printed under it."""
    heads, ordinals = index
    if ref in heads:
        return True
    if "." in ref:
        n, m = ref.rsplit(".", 1)
        return n in heads and m in ordinals.get(n, set())
    return False


def project_files(exts=(".md",)):
    """Every file with one of `exts`, including dot-directories that glob's ** skips."""
    for base, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "__pycache__")]
        for f in files:
            if f.endswith(exts):
                yield os.path.normpath(os.path.join(base, f))


def markdown_files():
    return project_files((".md",))


def gitignore_patterns():
    """What .gitignore excludes. Those paths are absent from a fresh clone by design - the
    corpus knowledgebase carries private data, the live handoff state is machine-local - so a
    pointer to one is not a pointer that fails for the reader."""
    patterns = []
    if os.path.exists(".gitignore"):
        for ln in read(".gitignore").splitlines():
            ln = ln.strip()
            if ln and not ln.startswith("#"):
                patterns.append(ln.strip("/"))
    return patterns


def is_ignored(rel, patterns):
    rel = rel.replace("\\", "/")
    for pat in patterns:
        if "/" in pat:
            if fnmatch.fnmatch(rel, pat) or fnmatch.fnmatch(rel, pat + "/*"):
                return True
        elif any(fnmatch.fnmatch(part, pat) for part in rel.split("/")):
            return True
    return False


def strip_front_matter(text):
    """The pointer scan reads prose, and front-matter is not prose - it is the structured record
    taskmd parses and validates by other means. `deliverables:` is the case that forces the
    distinction: it names outputs a task has not produced yet, so scanning it would make declaring
    one impossible. Replaced with blank lines rather than removed, so nothing downstream shifts."""
    m = re.match(r"---\r?\n.*?\r?\n---\r?\n", text, re.S)
    return "\n" * text[:m.end()].count("\n") + text[m.end():] if m else text


def resolves(target, base):
    """A pointer may be written from the repository root - the form a tool prints - or
    relative to the file it appears in. Either is fine; neither existing is not."""
    for candidate in (target, os.path.join(base, target)):
        if os.path.exists(os.path.normpath(candidate)):
            return True
    return False


def points_into_repo(target, base):
    """Whether a path-shaped string is a promise about *this* repository at all.

    Research notes quote other projects' layouts - `references/libraries.md` inside the deck
    skill - and those are citations, not pointers a reader is meant to follow here. The test that
    separates them: the directory the path names has to exist, from the root or beside the citing
    file. A missing file under `docs/` is still caught, because that directory is real.

    The hole this leaves is a typo in the directory itself - `doc/BRIEF.md` reads as somebody
    else's tree and is skipped. `PROJECT_DOCS` covers the documents that matter most by name,
    which is why that list exists separately."""
    head = target.replace("\\", "/").split("/")[0]
    if head in ("", ".", ".."):
        return True
    return any(os.path.isdir(os.path.normpath(c)) for c in (head, os.path.join(base, head)))


def cmd_check():
    problems = []

    # glob's ** skips dot-directories, which hid .handoff/ and .claude/. Walk instead.
    # `.gitignore` governs here too: an archived, machine-local handoff was once link-checked as
    # though a fresh clone contained it, which is the opposite of the question both scans answer.
    ignore = gitignore_patterns()
    labels = 0
    for md in sorted(markdown_files()):
        if is_ignored(os.path.relpath(md, "."), ignore):
            continue
        base = os.path.dirname(md)
        text = read(md)
        for m in links_in(text):
            target = m.group(1)
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            if not os.path.exists(os.path.normpath(os.path.join(base, target))):
                problems.append("BROKEN LINK  %s -> %s" % (md, target))

        # Check 4. Same documents, same links, and the one question the three others cannot ask:
        # not whether the target is there, but whether the words beside it are true.
        for label, target in labelled_links_in(text):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            lie = label_disagrees(label, target, base)
            if lie is None:
                if POINTER.search(label):
                    labels += 1
                continue
            labels += 1
            problems.append("LYING LABEL  %s -> the label says %s, the link opens %s"
                            % (md, lie[0], lie[1]))

    for doc in sorted(PROJECT_DOCS):
        if not os.path.exists(os.path.normpath(doc)):
            problems.append("MISSING DOC  %s is pointed at but does not exist - %s"
                            % (doc, PROJECT_DOCS[doc]))

    # Prose and printed pointers. The question this answers is narrow - would a reader who just
    # cloned this repository find the file? So .gitignore decides on both sides: an excluded path
    # is not a broken pointer, and an excluded *document* is not scanned at all, because it is not
    # in the clone either.
    #
    # There used to be a third exemption: any path some task declared as a deliverable was skipped,
    # on the grounds that it was a promise about the future. It was deleted (T-029), because it
    # exempted the path *everywhere in the repository, forever*, including files that already
    # existed - declaring `docs/LESSONS.md` silently dropped six live pointers out of validation
    # and the summary still printed "0 broken" (L-05). What replaces it is narrower by
    # construction: front-matter is not prose, so it is not scanned.
    pointers, seen_pointers, skipped = 0, set(), 0
    for src in sorted(project_files((".md", ".py"))):
        if is_ignored(os.path.relpath(src, "."), ignore):
            skipped += 1
            continue
        base = os.path.dirname(src)
        for m in pointers_in(read(src)):
            target = m.group(1)
            if is_ignored(target, ignore):
                continue
            if not points_into_repo(target, base):
                continue
            pointers += 1
            if (src, target) in seen_pointers:
                continue          # one report per document per target, not one per mention
            seen_pointers.add((src, target))
            if not resolves(target, base):
                problems.append("DEAD POINTER %s -> %s does not exist" % (src, target))

    # ---- section references (TASK-WORKFLOW.md §6.1)
    scanned = [s for s in sorted(project_files((".md", ".py")))
               if not is_ignored(os.path.relpath(s, "."), ignore)]
    alias = doc_aliases(scanned)
    sec_index, sections, sec_skipped, seen_sections = {}, 0, 0, set()
    for src in scanned:
        text = strip_code(strip_front_matter(read(src)))
        bound = set()
        for m in SECTION_REF.finditer(text):
            bound.add(m.start("sec"))
            tok, ref = m.group("doc"), m.group("sec")
            target = None
            if "/" in tok:
                cand = os.path.normpath(os.path.join(os.path.dirname(src), tok))
                target = cand if os.path.exists(cand) else None
            target = target or alias.get(os.path.basename(tok).upper())
            if not target:
                sec_skipped += 1              # a name this repository does not carry
                continue
            sections += 1
            if target not in sec_index:
                sec_index[target] = section_index(target)
            if section_resolves(sec_index[target], ref):
                continue
            key = (src, target, ref)
            if key in seen_sections:
                continue                      # one report per document per target section
            seen_sections.add(key)
            problems.append("DEAD SECTION %s -> %s has no §%s"
                            % (src, os.path.relpath(target, "."), ref))
        # Every mark the citation form does not bind to a document. Counted, never dropped: a
        # scan that silently ignores what it cannot bind is the report this tool exists not to be.
        sec_skipped += len([m for m in SECTION_ANY.finditer(text)
                            if m.start() + 1 not in bound])

    if problems:
        print("\nFAIL - %d problem(s):\n" % len(problems))
        for p in problems:
            print("  " + p)
        return 1, "refcheck: %d problem(s)" % len(problems)
    # Say what was checked, not just that it passed: this line used to read "0 broken links"
    # while two documents the tool itself points at were missing (L-05).
    print("OK - %d document pointer(s) checked, 0 broken" % pointers)
    print("     %d section reference(s) resolved, 0 dead; %d not bound to a document and skipped."
          % (sections, sec_skipped))
    print("     %d link label(s) name a path, 0 disagree with the file the link opens." % labels)
    print("     %d document(s) not scanned (.gitignore); front-matter is not scanned."
          % skipped)
    print("     references only - it cannot tell you a document is any good. Tasks are `taskmd`.")
    return 0, ("refcheck: %d pointer(s), %d section reference(s), %d label(s), 0 broken"
               % (pointers, sections, labels))


def self_test():
    """Refuse to run if the checks cannot tell a good reference from a bad one (**L-04**).

    The retired tool had no self-test until T-046, which is why three of its reports could not
    fail. Each assertion below **constructs the failure** and requires it to be reported - an
    assertion that only ever sees the passing case is the same defect one level up.
    """
    # A miniature of the two documents that decide the rule: a §0 whose numbered list runs to 8,
    # a §5 with three items and a real §5.1 subsection, and a §9 with no list under it.
    idx = section_index_of(
        "# T\n\n## 0. Preamble\n\n" + "".join("%d. item\n" % i for i in range(9)) +
        "\n## 5. Five\n\n1. first\n2. second\n3. third\n\n### 5.1 Sub\n\n## 9. Nine\n\nprose\n")

    # The four cases that decide the rule (TASK-WORKFLOW.md §6.1), plus the two shapes each side.
    # Two must pass and two must fail; a resolver that says yes to everything satisfies only the
    # first pair, which is why the second is here.
    for ref in ("5", "5.1", "5.3", "0.8"):
        if not section_resolves(idx, ref):
            sys.exit("SELF-TEST FAILED: §%s should resolve - a heading, or an ordinal under one"
                     % ref)
    for ref in ("9.4", "0.9", "11"):
        if section_resolves(idx, ref):
            sys.exit("SELF-TEST FAILED: §%s does not exist and was reported as resolving" % ref)

    # Adjacency binds a reference to a document; proximity does not. Both halves are asserted,
    # because the loose version passed the first and produced wrong targets on the second.
    # The fixtures name documents this repository does not carry, so the scan over this file does
    # not read its own test data as live pointers - which it did, and reported two.
    if not SECTION_REF.search("see [EXAMPLE.md](EXAMPLE.md) §2 for the rest"):
        sys.exit("SELF-TEST FAILED: a linked document followed by a section mark did not bind")
    if not SECTION_REF.search("EXAMPLE.md §5.3 covers it"):
        sys.exit("SELF-TEST FAILED: a bare document name beside a section mark did not bind")
    if SECTION_REF.search("EXAMPLE.md is the source, and the reasoning is in §2.1"):
        sys.exit("SELF-TEST FAILED: a document named earlier in the sentence was bound to a "
                 "later section mark - that is the heuristic T-046 rejected")

    # Code is literal text. Without this a document cannot record that a pointer is dead.
    if "§11" in strip_code("the note cites `DESIGN-SYSTEM.md §11`, which never existed"):
        sys.exit("SELF-TEST FAILED: a section mark inside a code span was not treated as literal")
    if "§9" not in strip_code("cites DESIGN-SYSTEM.md §9 in prose"):
        sys.exit("SELF-TEST FAILED: stripping code removed a mark that was not in code")

    # A prose pointer is the check taskmd does not have, so it is asserted here rather than
    # assumed: the shape that must match, and the bare filename that must not (T-062).
    if not POINTER.search("the reasoning is in docs/BRIEF.md and nowhere else"):
        sys.exit("SELF-TEST FAILED: a repo-relative path in prose was not seen as a pointer")
    if POINTER.search("see README.md for the rest"):
        sys.exit("SELF-TEST FAILED: a bare filename with no directory was read as a path")

    # Where the two scans part company (T-080). Four fixtures, the same four the task measured, and
    # they assert the functions `cmd_check` actually calls rather than the patterns underneath them
    # - a regex that happens to be used the right way today is not the shipped behaviour.
    #
    # The target names a directory this repository does not have, so the live scan over this file
    # reads none of it as a promise: `points_into_repo` skips it, and check 1 no longer sees it at
    # all. That trap is not hypothetical - the fixtures above are worded the way they are because an
    # earlier self-test's data was scanned as live pointers and reported two.
    link = "[T-041](no-such-dir/T-041-implement-the-nine-glitch-free-conditions.md)"
    fenced = "before\n```\n%s\n```\nafter\n" % link
    if any(links_in(fenced)):
        sys.exit("SELF-TEST FAILED: link syntax inside a fence was resolved - it renders as the "
                 "characters typed, so nobody can follow it and nothing can break it")
    if any(links_in("the row reads `%s` verbatim" % link)):
        sys.exit("SELF-TEST FAILED: link syntax inside an inline code span was resolved - a span "
                 "is code for the same reason a fence is")
    # Both halves, because a scan that reports nothing satisfies the two above on its own.
    if not any(links_in("see [the brief](docs/BRIEF.md) for the rest")):
        sys.exit("SELF-TEST FAILED: a real markdown link outside code was not seen at all, so the "
                 "two assertions above prove nothing")
    # The behaviour that has to survive them: check 2 reads inside fences deliberately.
    if not any(pointers_in("```\nWrote no-such-dir/T-041-implement-the-nine-"
                           "glitch-free-conditions.md - 8 active\n```\n")):
        sys.exit("SELF-TEST FAILED: a bare path printed into a fence was skipped - that is a "
                 "tool's own output and check 2 exists to hold it")

    # ---- check 4, the label beside the target (T-159)
    # Every fixture names `no-such-dir/`, for the reason two paragraphs up: a path-shaped string
    # anywhere in this file is a promise check 2 reads, and test data must not make one. **And not
    # one of them opens with a parent-directory hop**, which is the same trap one step further in:
    # `points_into_repo` answers yes to a relative path unconditionally, so no `no-such-dir` can
    # excuse it. Two of these did, and check 2 reported both - then reported the comment written to
    # explain it, because check 2 reads code spans in prose on purpose (`pointers_in`). Check 3 can
    # quote a dead reference and this check cannot, which is the boundary between them.
    #
    # They compare strings and touch no filesystem, so the directory never needs to exist.
    #
    # The honest set comes first and is not decoration: a rule that fires on the house style would
    # report 700 failures on this tree, and only the negative cases can show that it does not.
    if label_disagrees("no-such-dir/a.md", "no-such-dir/a.md", ""):
        sys.exit("SELF-TEST FAILED: a label written from the repository root, beside the target it "
                 "names, was called a lie")
    if label_disagrees("sub/a.md", "sub/a.md", "no-such-dir"):
        sys.exit("SELF-TEST FAILED: a label written the same way as its target was called a lie")
    if label_disagrees("no-such-dir/sub/a.md", "sub/a.md", "no-such-dir"):
        sys.exit("SELF-TEST FAILED: the two conventions were required to be the same one - a "
                 "root-written label beside a file-relative target opens the same file")
    if label_disagrees("the brief", "no-such-dir/a.md", ""):
        sys.exit("SELF-TEST FAILED: a label naming no path was treated as claiming one")

    # The defect itself, in the shape it was found in twice: a one-level label left beside a target
    # that gained a level. Without this the four above are satisfied by a check that never fires.
    if not label_disagrees("no-such-dir/a.md", "no-such-dir/deep/a.md", ""):
        sys.exit("SELF-TEST FAILED: a label one directory level out of date was not reported, "
                 "which is the whole reason check 4 exists")

    # The trap that would disable check 4 while it reported a confident zero. This repository
    # writes the path inside a code span, so a label read from the stripped text is blank - and a
    # blank label claims nothing and can never lie.
    labelled = list(labelled_links_in("see [`no-such-dir/a.md`](no-such-dir/b.md) for the rest"))
    if not labelled or "no-such-dir/a.md" not in labelled[0][0]:
        sys.exit("SELF-TEST FAILED: a label written inside a code span was not read - check 4 "
                 "would then be silent on the convention this repository actually uses")
    if any(labelled_links_in("```\n[`no-such-dir/a.md`](no-such-dir/b.md)\n```\n")):
        sys.exit("SELF-TEST FAILED: a link inside a fence was read by check 4 - it renders as the "
                 "characters typed, so its label tells nobody anything")
    return True


def quiet_wanted(argv, stdout=None):
    """Whether a green run prints one line (**L-153**). `--report` says no and `--quiet` says yes,
    outright; otherwise a terminal gets the account and anything else gets the line."""
    if "--report" in argv:
        return False
    if "--quiet" in argv:
        return True
    stdout = sys.stdout if stdout is None else stdout
    return not (hasattr(stdout, "isatty") and stdout.isatty())


def emit(full, code, line, quiet):
    """The text a run prints: the whole account on a red run or a watched one, the line otherwise.
    `code` is consulted before `quiet` - a quiet mode that hid a failure would be worse than the
    account it replaces."""
    return full if code or not quiet else line + "\n"


def main():
    argv = sys.argv[1:]
    # `--report` and `--quiet` decide how a *green* run reads (**L-153**) and are not commands.
    # Filtering them here rather than widening the guard keeps the guard's job intact: a mistyped
    # command still prints the docstring and exits 1, which is what it is for.
    words = [a for a in argv if a not in ("--report", "--quiet")]
    if words and words[0] not in ("check", "--self-test"):
        print(__doc__)
        return 1
    os.chdir(ROOT)
    self_test()
    if words and words[0] == "--self-test":
        print("OK - self-test passed; the resolver rejects what it should.")
        return 0
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code, line = cmd_check()
    sys.stdout.write(emit(buf.getvalue(), code, line, quiet_wanted(argv)))
    return code


if __name__ == "__main__":
    sys.exit(main())
