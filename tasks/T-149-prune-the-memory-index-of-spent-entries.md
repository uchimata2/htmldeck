---
id: T-149
title: Prune the memory index of spent entries
type: admin
status: proposed
phase: specify
parent: T-130
blocked_by: []
related: [T-130, T-134]
work_package: PH3
owner: the project owner
business_value: low
effort: xs
created: 2026-08-14
updated: 2026-08-14
deliverables: []
---

# T-149 — Prune the memory index of spent entries

## 1. Specify

**Outcome**
The agent memory index stops paying, on every turn of every session, for entries that tell the reader
in their own text not to use them. **The finding is `CE-10`**, stated in
[`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.1; it is not restated here.

**It is tier 1 and it is not this repository's.** The index measured **6,134 bytes over 39 lines, 35
entries**, and it is one of the three files [`../CLAUDE.md`](../CLAUDE.md) records as loaded on every
turn. The bound written there deliberately covers only the file this repository owns, because a
repository cannot edit the other two — **so this task is the owner acting on their own store, and the
repository's part is the check, not the edit.**

**Scope**
- In: which entries are spent, and which are project-shaped and belong in this repository instead,
  where they are shared rather than private.
- In: the check each removal owes — is this fact recorded in [`../docs/LESSONS.md`](../docs/LESSONS.md)
  or elsewhere in the tree?
- Out: any change this repository can make on its own. The store is the owner's.
- Out: memories from other projects. This is scoped to the index this project's sessions load.

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.2 — read before starting; §6.1 — `CE-10`
- [`../CLAUDE.md`](../CLAUDE.md) — *What loads every turn, and what bounds it*, which names this file
  as tier 1 and says why it is outside the bound
- [`../docs/LESSONS.md`](../docs/LESSONS.md) — what the repository already records, and therefore what
  a memory need not

**What specifying must settle**
- What *spent* means as a test somebody can apply twice and get the same answer, rather than as a
  judgement per entry.
- What happens to a memory that is still true but project-shaped: promoted into the repository, or
  left private.
- Who runs it, and how the result is recorded here when the artifact edited is not in this tree.

**Acceptance criteria**
- Written at `specify`. §6.2 owns what an audit task owes beyond them.

**Open questions**
- **Whether a task in this tracker is the right instrument at all**, given the deliverable is outside
  the repository. The precedent says yes:
  [T-135](T-135-cut-the-load-path-this-project-cannot-use.md) was the same shape, closed here, and its
  correction is the most cited thing it produced.

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
| 2026-08-14 | → proposed | Raised at the owner's direction with the rest of the unraised findings; it ranked twelfth and was never a candidate. Scheduled to `plan` and no further. The one row of the six whose work is not a repository change, which is why its specification is mostly about the test for *spent* and about where the result is recorded. |
| 2026-08-14 | (unchanged) | **Removed from the decision batch the same day, with [T-148](T-148-give-a-measured-figure-a-durable-home.md), by the same argument**: `xs`, the instance already measured, and the entries that call themselves spent are named in `CE-10` — so a pass to decide whether it is worth doing costs what doing it costs. It takes the ordinary lifecycle in its turn. **The work itself is still the owner's**, because the store is not in this tree; what this repository owes is the test and the record. |
