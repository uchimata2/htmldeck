---
id: T-147
title: One workflow file per lifecycle phase
type: deliverable
status: proposed
phase: specify
parent: T-130
blocked_by: []
related: [T-130, T-145, T-146]
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-08-14
updated: 2026-08-14
deliverables: []
---

# T-147 — One workflow file per lifecycle phase

## 1. Specify

**Outcome**
A session at one phase of the lifecycle reads that phase's rules, not the history of which checker
resolved what. **The finding is `CE-09`**, stated in
[`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.1; it is not restated here.

**Measured at the audit: [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) is 22,190 bytes and §6 *The tooling*
is 11,842 of them — 53%.** A session at `plan` needs §2, which is 1,291 bytes. The file is 22,483
bytes now, because §6 grows with every tooling change, which is the finding describing itself.

**Section numbers must survive.** A dozen task records cite this document at §2 through §6.2, and
`refcheck.py` resolves them — a split that keeps the numbers keeps the citations, and one that does
not falsifies twelve records at once.

**Scope**
- In: the split, the numbering that survives it, and the entry point that says which file to open.
- Out: rewriting a rule while moving it.
- Out: deleting the tooling history. It is the record of why each check exists; it moves.

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.2 — read before starting; §6.1 — `CE-09`
- `R8` §9, P2 — the four-part shape this finding proposes: preflight, do, do-not, close
- [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §6.1 — the section-reference rule this task is bound by

**What specifying must settle**
- ~~**The shared policy question**, with [T-145](T-145-move-brief-mds-release-phases-to-its-own-document.md)
  and [T-146](T-146-one-file-per-lesson-with-a-generated-index.md): does this project split large
  documents by unit? **The first of the three specified settles it**; the other two adopt or argue.~~
  **Settled 2026-08-14 by T-145 as `L-89`.** Both limbs bear on this task and they point different
  ways, which is the second bullet below: `§n` is an address and a planner wants one phase at a time,
  which argues the by-unit limb; but the weight is in one section, which argues the by-kind limb and
  a single extraction. **`L-89`'s rule 2 decides it — move the part that grows.** Adopt that or argue
  against it; do not re-decide the policy.
- Whether the four-part shape fits a document whose weight is in one section, or whether extracting
  that one section is the whole change and the rest is churn.
- How `§n` citations survive a split — the constraint that decides the shape.

**Acceptance criteria**
- Written at `specify`. §6.2 owns what an audit task owes beyond them.

**Open questions**
- **Is it worth doing at all?** `m`, and the cheaper alternative — move §6 out and leave the rest —
  may capture most of the gain. Deciding that is what `specify → plan` is for here.

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
| 2026-08-14 | → proposed | Raised at the owner's direction with the rest of the unraised findings. It was **never a candidate** — it ranked ninth in T-130's §6 and was not put up — so this is the cut-off moving, not a proposal accepted. **Scheduled to `plan` and no further.** |
