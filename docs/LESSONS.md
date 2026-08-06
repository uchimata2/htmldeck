# Lessons

Things this project has already paid for once. Each is **generic** — it survives the task that
produced it and applies to the next one — and each is stated so it can be *acted on*, not
admired.

Cite them by ID. `L-07` and `L-11` are cited from `tools/tasks/task.py`, so **IDs are stable**:
add at the end of a section, never renumber.

Seeded from the "Carried lessons" table in [`BRIEF.md`](BRIEF.md), which keeps the corpus
evidence behind several of them, and from `docs/research/R4-prior-art.md` §1. Project-specific
findings stay in the task file or the research note that produced them; only what generalises
comes here.

---

## Evidence and verification

### L-01 — Look at the output

Every automated check can pass on something visibly broken. A deck that validates is not a deck
that reads well; a report that renders is not a report that makes sense.

**How to apply.** Open the artefact the way its audience will — for a deck, from `file://` with
the network off — and look at it before writing "done". This is rule 6 in
[`../CLAUDE.md`](../CLAUDE.md) and part of the definition of done in
[`../tasks/TASK-WORKFLOW.md`](../tasks/TASK-WORKFLOW.md) §2.

### L-02 — Verify on the real case, not a toy

Layout, pacing and performance problems appear at real size and nowhere else. A three-slide
example proves the generator runs; it proves nothing about what it produces.

**How to apply.** Pick the smallest case that is genuinely representative — for this project, a
12-slide deck with diagrams — and make that the acceptance case, not the demo.

### L-03 — Count, don't read

Defects that span documents are invisible to reading and obvious to counting. A figure that is
right where it is stated and wrong where it is quoted survives every careful read of each
document on its own.

**How to apply.** Tally the table's own verdict column. Count the nodes in the model the sentence
describes. Build the one boring table that lists every figure, its origin, and every place it is
reused — then compare. Cheap, and it finds what review does not.

### L-04 — Verify the checker on a known case

A measurement is believed in proportion to how little it looks like a tool. One scan in the
corpus split sentences line by line against hard-wrapped Markdown and under-reported by 15×; it
was trusted because it printed numbers.

**How to apply.** Every check ships with a self-test on a case whose answer was worked out by
hand. Run it before believing the check, and again whenever the check changes.

### L-05 — Say which half you checked

A check that *looks* complete is worse than no check, because a partial pass gets read as a
verdict on the whole.

**How to apply.** State in the output what was **not** examined. `task.py check` reporting "0
broken links" was true and misleading in the same breath: it validated links between task files
while two documents the tooling itself pointed at did not exist. Name the scope in the success
line, not only in the failure.

### L-06 — Ask the authoritative source, not the convenient one

The convenient source answers confidently and wrongly. Two versions of this cost time in one
sitting:

- **A sandboxed shell reports "denied" as "does not exist".** `Get-ChildItem` on a directory
  outside the sandbox returns *cannot find path*, and a recursive search returns nothing at all,
  with no error. Bash and the file-reading tools read the same path without trouble. A session
  that trusts the shell here concludes the files are not on disk, which is false.
- **A skill's own body is half of it.** `SKILL.md` is a routing table; the substance sits in
  `references/` and `templates/`, several times longer, and that is where nearly everything
  worth finding was found.

**How to apply.** When a source says "nothing here", confirm with a second tool before recording
it as a finding. Absence claimed by a restricted reader is not evidence of absence. Two
acceptance criteria on T-009 were reported unmet on this exact mistake and were both wrong — the
material existed in documents that had not been read.

---

## Tooling

### L-07 — Standard library only

Project tooling is run by whoever clones the repository, on a machine nobody configured for it.
A dependency is a thing that can be missing.

**How to apply.** Scripts in `tools/` use the standard library and nothing else. If that makes a
script longer, it is still the right trade — the same reasoning that bans external libraries from
the decks themselves (rule 1 in [`../CLAUDE.md`](../CLAUDE.md)).

### L-08 — Store one edge; derive the rest

Write a fact in exactly one place and compute every view of it. Facts that are computed cannot
drift from facts that are stored; two hand-maintained copies of the same relationship disagree
within a week.

**How to apply.** In the task system, the forward edge lives in the front-matter and the child
list, the "blocks" list and the index are all derived. The same rule governs prose: if another
document owns a fact, point at it (**L-13**).

### L-09 — Every pointer must resolve in a fresh clone

A path in prose, in a template comment, or in a tool's output is a promise that the file is
there. This repository publishes, and CLAUDE.md requires clone-and-run, so a dangling pointer is
a defect and not a cosmetic one.

**How to apply.** Check pointers mechanically, including the ones hard-coded in tools, not only
markdown links between documents. Where a pointer is legitimately unresolvable — a machine-local
path, a deliverable not produced yet — make that explicit rather than letting the checker learn
to ignore it.

### L-10 — Declare the encoding; the console will not

The Windows console defaults to cp1252 and mangles the typographic punctuation this project's
prose is full of. The failure looks like corrupt data rather than a display setting.

**How to apply.** Open files as UTF-8 explicitly, reconfigure `stdout` where the runtime allows
it, and keep console output ASCII when the alternative is a garbled em-dash.

### L-11 — Write LF, everywhere, from every tool

Generated files get compared byte for byte. If line endings depend on who checked the repository
out, every comparison is noise and every regeneration is a diff.

**How to apply.** `.gitattributes` pins `eol=lf`; anything that writes a file passes
`newline="\n"` so the output is identical on every platform.

---

## Writing

### L-12 — What is read every time must be short

Anything loaded on every run competes with the work for attention and for context. Length there
is a recurring cost, not a one-off one.

**How to apply.** The always-loaded body stays short and routes; the detail lives in a reference
loaded on demand. This is why the design system will be a separate file the skill points at
rather than prose inside the skill.

### L-13 — Point at the source; do not restate it

A paraphrase is a second copy that starts drifting immediately, and the reader cannot tell which
copy is current.

**How to apply.** One document owns each fact. Everything else links to it. If a restatement is
genuinely needed for flow, keep it to a sentence and link the owner in the same breath —
`../CLAUDE.md` owns the rules, [`BRIEF.md`](BRIEF.md) owns what to build,
[`../tasks/TASK-WORKFLOW.md`](../tasks/TASK-WORKFLOW.md) owns the task mechanics, and this file
owns the lessons.
