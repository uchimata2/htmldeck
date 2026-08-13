---
id: T-145
title: Move BRIEF.md's Release phases to its own document
type: deliverable
status: proposed
phase: specify
parent: T-130
blocked_by: []
related: [T-130, T-146, T-147]
work_package: PH3
owner: the project owner
business_value: high
effort: m
created: 2026-08-14
updated: 2026-08-14
deliverables: []
---

# T-145 — Move BRIEF.md's Release phases to its own document

## 1. Specify

**Outcome**
[`../docs/BRIEF.md`](../docs/BRIEF.md) is the size of a specification again, and the per-task decision
record it grew lives in its own document. **The finding is `CE-05`**, stated in
[`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
§8; it is not restated here.

**Measured at the audit, 2026-08-13: 66,461 of 108,163 bytes — 61% — in one section, 112 rows of
which 68 were struck through.** The document is larger now and every PH3 closure adds to that
section, so re-measure before claiming anything
([`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.2, rule 1).

**One collision is already ruled**: `TASK-WORKFLOW.md` §6 excuses the `DUPLICATE INDEX` advisory **by
file name**, so the excusal moves with the content **inside this task**. Splitting the two would
leave the advisory firing correctly against a document no rule covers.

**Scope**
- In: the split, the excusal's move, and every pointer into the moved rows.
- Out: rewriting a row while moving it.
- Out: the execution-order table's placement decisions, which are the owner's and move unchanged.

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.2 — read before starting
- `R8` §8 — `CE-05` in full, including the collision it names
- [`../tasks/TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §6 — the excusal that moves

**What specifying must settle**
- **Whether this project splits large documents by unit at all.** It is the same question as
  [T-146](T-146-one-file-per-lesson-with-a-generated-index.md) and
  [T-147](T-147-one-workflow-file-per-lifecycle-phase.md) — three tasks, one policy. **The first of
  the three specified settles it for all three**, and the other two adopt or argue against it
  explicitly rather than answering it again.
- Where completed rows go, and whether a closed phase stays readable in place.
- What still points into the moved section, and how the pointers survive.

**Acceptance criteria**
- Written at `specify`, with the measurement re-taken first. The criteria this project owes are in
  `../docs/CONTEXT-AUDIT.md` §6.2 and are not repeated per task.

**Open questions**
- **Is it worth doing at all?** `m`, and the document it shrinks is one a session is told to read
  first. Specify and plan decide this; `cancelled` is a legitimate outcome and keeps the file.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <none yet>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-14 | → proposed | Raised at the owner's direction with the rest of the unraised findings. It was the fifth of T-130's seven candidates and stood as a candidate for a day. **Scheduled to `plan` and no further**: the next session takes it through `specify → plan` to decide whether it is worth implementing, which is the owner's instruction and not this task's judgement. |
