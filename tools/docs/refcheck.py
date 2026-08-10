#!/usr/bin/env python3
"""Check that every reference in this repository's documents resolves in a fresh clone.

    python tools/docs/refcheck.py

Three checks, all mechanical:

  1. **BROKEN LINK** - a markdown `[text](target)` whose target does not exist.
  2. **DEAD POINTER** - a repo-relative `.md` path written in **prose**, or printed by a tool into
     a fenced block. As much a promise as a link, and nothing else checks it.
  3. **DEAD SECTION** - a `<named document> §n` whose number is not a heading in that document.

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

Run it from the repository root. Task validation is `taskmd check`, not this.
"""

import fnmatch
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
    for md in sorted(markdown_files()):
        if is_ignored(os.path.relpath(md, "."), ignore):
            continue
        base = os.path.dirname(md)
        for m in LINK.finditer(read(md)):
            target = m.group(1)
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            if not os.path.exists(os.path.normpath(os.path.join(base, target))):
                problems.append("BROKEN LINK  %s -> %s" % (md, target))

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
        for m in POINTER.finditer(strip_front_matter(read(src))):
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
        return 1
    # Say what was checked, not just that it passed: this line used to read "0 broken links"
    # while two documents the tool itself points at were missing (L-05).
    print("OK - %d document pointer(s) checked, 0 broken" % pointers)
    print("     %d section reference(s) resolved, 0 dead; %d not bound to a document and skipped."
          % (sections, sec_skipped))
    print("     %d document(s) not scanned (.gitignore); front-matter is not scanned."
          % skipped)
    print("     references only - it cannot tell you a document is any good. Tasks are `taskmd`.")
    return 0


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
    return True


def main():
    argv = sys.argv[1:]
    if argv and argv[0] not in ("check", "--self-test"):
        print(__doc__)
        return 1
    os.chdir(ROOT)
    self_test()
    if argv and argv[0] == "--self-test":
        print("OK - self-test passed; the resolver rejects what it should.")
        return 0
    return cmd_check()


if __name__ == "__main__":
    sys.exit(main())
