---
id: T-146
title: One file per lesson, with a generated index
type: deliverable
status: proposed
phase: specify
parent: T-130
blocked_by: []
related: [T-130, T-145, T-147]
work_package: PH3
owner: the project owner
business_value: medium
effort: l
created: 2026-08-14
updated: 2026-08-14
deliverables: []
---

# T-146 — One file per lesson, with a generated index

## 1. Specify

**Outcome**
A lesson is fetched one at a time instead of by loading every lesson this project has learned.
**The finding is `CE-06`**, stated in
[`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
§8; it is not restated here.

**[`../docs/LESSONS.md`](../docs/LESSONS.md) is 162,403 bytes over 2,371 lines** — the largest
read-path document in the repository, and it is consulted one entry at a time. Lessons are cited as
`L-nn` from task records, tool output and the working rules, so **the citation is the interface** and
whatever this becomes must keep resolving.

**The pattern already exists in this repository**, in the tracker: one file per unit, an index
generated from them, and a checker that fails when the index and the files disagree. That is the
comparison to argue against, not a new invention.

**Scope**
- In: the storage shape, the generated index, and the checker that keeps them honest.
- In: every `L-nn` citation continuing to resolve, which `refcheck.py` decides.
- Out: rewriting a lesson's text. A restructure that also edits is two changes nobody can review.
- Out: deciding this project's general splitting policy alone — see below.

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.2 — read before starting
- `R8` §8 — `CE-06` in full
- **L-74** in [`../docs/LESSONS.md`](../docs/LESSONS.md) — when a fact cannot be derived, make the
  stored copy fail loudly in both directions. It is the rule a generated index lives or dies by

**What specifying must settle**
- **The shared policy question**, with [T-145](T-145-move-brief-mds-release-phases-to-its-own-document.md)
  and [T-147](T-147-one-workflow-file-per-lifecycle-phase.md): does this project split large documents
  by unit, with a generated index? **The first of the three specified settles it**; the other two
  adopt it or argue explicitly.
- Whether the gain is real for an agent that already greps a single file cheaply, or whether the cost
  is paid mostly by whole-file reads nobody performs.
- What generates the index, what checks it, and where that runs in the gate chain.

**Acceptance criteria**
- Written at `specify`. `../docs/CONTEXT-AUDIT.md` §6.2 owns what an audit task owes beyond them.

**Open questions**
- **Is it worth doing at all?** Banded `m`–`l` and taken as `l` here, which under this project's size
  rule is PH3 work by definition. It is the largest of the six raised together and the most likely to
  be `cancelled` at plan — the honest close, with the file kept.

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
| 2026-08-14 | → proposed | Raised at the owner's direction with the rest of the unraised findings; it was the sixth of T-130's seven candidates. **Scheduled to `plan` and no further** — the next session decides whether it is worth implementing. Its own band is the argument for stopping there: `l` on a document whose read cost is real but paid in greps rather than in whole-file loads. |
