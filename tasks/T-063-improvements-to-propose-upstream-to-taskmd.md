---
id: T-063
title: Improvements to propose upstream to taskmd
type: analysis
status: done
phase: review
parent: null
blocked_by: []
related: [T-062]
work_package: PH2
shipped_in: 0.1.2
owner: the project owner
business_value: medium
effort: s
created: 2026-08-09
updated: 2026-08-12
deliverables: []
---

# T-063 — Improvements to propose upstream to taskmd

**This task is a hand-off document, not work to do here.** It exists so that what
[T-062](T-062-retire-the-pre-split-task-tool-and-repoint-what-points-at-it.md) learned about taskmd
is written down in a form the owner can copy into the taskmd project. **Nothing below should be
implemented in htmldeck.**

## 1. Specify

**Outcome**
A list of proposals, each with the evidence that produced it, at a size someone can paste into
taskmd's own backlog without rewriting.

**How these were found**
By migrating a real 61-task project off a mature bespoke tool. Every item is something that tool did
and taskmd does not, or something the migration tripped over. They are ordered by how much they cost
the migrating project.

---

### 1. `check` does not see references outside markdown-link syntax

**The evidence.** Seeded into a throwaway clone of this project, taskmd 0.1.1 reported
`OK - 61 task(s), vocabulary valid, references resolve, no broken links` with two live defects
present:

- a dead **bare path in prose**: a `.md` under a real directory of the project, written without
  markdown-link syntax;
- a dead **section reference**: a sibling document cited at a section number it has no heading for.

*Both are described rather than written out, because writing either here would make this file carry
the defect it reports.*

`check_links` matches `LINK = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(?:#[^)\s]*)?\)")`, so a path written
as prose, or **printed by a tool into a fenced block**, is not a reference as far as the check is
concerned. In this project that is not an edge case: 1005 document pointers are validated and a large
share are bare paths, because tools print them.

**Why it matters more than it looks.** A project adopting taskmd and retiring its own checker loses
this without being told. The adoption path actively encourages that, since the two tools' command
lists look equivalent.

**Proposal.** An opt-in prose-pointer check: a path-shaped token whose first segment is a real
directory in the project is a pointer and must resolve. The false-positive class is other projects'
layouts quoted in prose, and the fix that worked here is exactly that directory test, kept in
`points_into_repo`.

---

### 2. No notion of a section reference

**The evidence.** `§` appears in taskmd's own source only in comments citing `METHOD §4` and
`T-011 §1` — the tool uses the convention in its own documentation and cannot check it.

**What it costs.** This project cites 497 of them and had 1394 unchecked before it built the rule.
A `§n` is a pointer whose target is a number **printed in the document it points at**, so it can be
resolved mechanically, and it goes stale exactly like a link: renumber a section and every citation
of it lies.

**Proposal.** Resolve `<document> §n` where the document is named **adjacent** to the mark. Adjacency
is the whole of it — this project measured "nearest document mentioned in the paragraph" and it
picked the wrong target for a third of the misses it reported. `§n` resolves when `n` is a heading;
`§n.m` when `n.m` is a heading **or** `n` is a heading and `m` is an ordinal in a numbered list under
it. Marks the form does not bind are **counted and reported as skipped**, never silently dropped.
A `§` inside a code span or fence is literal text, which is what lets a document quote a reference
that is wrong.

Working implementation, MIT, in this repository at `tools/docs/refcheck.py`, with the self-test that
proves the resolver rejects `§9.4` and `§0.9` while accepting `§5.1` and `§0.8`.

---

### 3. `.gitignore` is not consulted, so the question the check answers is ambiguous

**The evidence.** taskmd's `markdown_files` walks everything except `SKIP_DIRS` and nested projects.
This project's checker excludes gitignored documents deliberately, and states why: the question is
*"would a reader who just cloned this find the file?"*, so an excluded path is not a broken pointer
and an excluded **document** is not scanned, because neither is in the clone.

Without it, a machine-local file — a live handoff, a private knowledgebase — is link-checked as
though a fresh clone contained it, and a project keeping either gets failures it cannot fix. This
project hit exactly that and recorded it.

**Proposal.** Consult `.gitignore` on both sides, and **print how many documents were skipped**, so
the exclusion cannot quietly grow.

---

### 4. `check` says what passed, not what was checked

**The evidence.** taskmd prints one line:

```
OK - 61 task(s), vocabulary valid, references resolve, no broken links
```

This project's checker prints what it actually did, and the reason is written in its source: the
summary *"used to read 0 broken links while two documents the tool itself points at were missing"*.

```
OK - 61 tasks, vocabulary valid, task references resolve, 1005 document pointer(s) checked, 0 broken
     494 section reference(s) resolved, 0 dead; 1149 not bound to a document and skipped.
     28 document(s) not scanned (.gitignore); front-matter is not scanned.
     structure and references only - it cannot tell you a spec or a deliverable is any good.
```

A count that silently shrinks is undetectable against a pass/fail line. This project has a lesson for
it (**L-05**) raised after a scoping change dropped six pointers out of validation while the summary
still read `0 broken`.

**Proposal.** Report the denominators, and one line naming what the check cannot decide.

---

### 5. Smaller things

- **`bin/` is dropped from `PATH`** in agent shells built from the shell snapshot, so the bare
  `taskmd` command does not resolve and every invocation needs
  `PYTHONPATH=<skill> python -m taskmd`. Worth either documenting or shipping a shim.
- **The shipped template's `work_package` placeholder reads `WP<n> | final | none`**, which does not
  match a config that enumerates its own values. A template generated from the config would not drift.
- **`STALE INDEX` is reported and not fixed.** Correct for a checker, but `check` and `index` are then
  always run as a pair, which invites a `--fix`.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Owner copies the items above into taskmd's backlog | Tasks in that project |

## 3. Implement

**Decisions & assumptions**
- **Nothing here is implemented in htmldeck — 2026-08-09.** The proposals are about taskmd's code,
  which this repository does not own. `refcheck.py` is offered as a working reference, not as a patch.

**Outputs produced**
- this document

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A list of proposals, each with the evidence that produced it | **met** | Five items. Each carries the run, the source line or the measurement behind it rather than an assertion |
| At a size someone can paste into taskmd's backlog without rewriting | **met** | Confirmed by use: the owner copied it on 2026-08-09 and is processing it upstream |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-10 | (no change) | **§5's first smaller thing is answered locally, and the proposal upstream stands.** *Worth either documenting or shipping a shim* — this project has now done both: `tasks/TASK-WORKFLOW.md` §6 says the bare command does not resolve in an agent shell, and `tools/tasks/lint.py` is the shim, finding the installed skill by glob and running the three checks a task edit owes. It was written because the incantation had reached two documents, which is one more than a fact may have (**L-13**). Local, so it does not weaken the case for taskmd shipping its own: every adopting project writing this shim independently is the argument. |
| 2026-08-10 | (no change) | **Upstream answered, and item 1 came back *out*:** taskmd's `check` will not resolve a path written as prose or inside a fenced block. Decided by measurement and shipped in v0.2.0, with the gap documented adopter-facing so the next project retiring its own checker is told. The measurement included **this project's corpus** — 481 bare pointers, 31 dead, 19 of them naming `tools/tasks/task.py`, which [T-062](T-062-retire-the-pre-split-task-tool-and-repoint-what-points-at-it.md) retired — so the coverage this task argued was being lost is, here too, 31 alarms and no defects. That does not make the proposal wrong: upstream's own reasoning before it measured agreed with it, and this project's report is what caused the measurement to happen at all. What it forces is a decision about `tools/docs/refcheck.py`, raised as [T-073](T-073-decide-whether-to-keep-refcheck-now-that-upstream-has-ruled.md) rather than settled here. Item 2, the section-reference rule, is **still open upstream** and this project's implementation is still its reference, so the file should outlive the decision either way. This record is not amended — it was correct when written, and the outcome is a later fact rather than a correction. |
| 2026-08-10 | → done | **Copied upstream by the owner and now being processed there, which is this task's exit criterion rather than a status change made on its behalf.** Nothing was implemented in htmldeck and nothing should be: the proposals are about taskmd's own code. The one item with a working implementation behind it is the section-reference rule, and that implementation is public at `tools/docs/refcheck.py` under MIT, so taskmd can take it without re-deriving the adjacency decision. Closed rather than cancelled: the deliverable was the document, it exists, and it has been used for the thing it was written for. |
| 2026-08-09 | → proposed | Raised at the owner's request while [T-062](T-062-retire-the-pre-split-task-tool-and-repoint-what-points-at-it.md) migrated this project onto taskmd. Findings are from a real migration of a 61-task project off a mature bespoke tool, which is why items 1 and 2 are framed as adoption hazards rather than missing features: both are things a project silently loses when it retires its own checker on the strength of the two command lists matching. |
