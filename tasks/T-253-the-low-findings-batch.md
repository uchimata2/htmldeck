---
id: T-253
title: Correct the audit's forty-nine Low findings, or accept each with a reason and a date
type: fix
status: proposed
phase: specify
parent: T-219
blocked_by: []
related: []
work_package: PH3
owner: the project owner
business_value: low
effort: l
created: 2026-08-29
updated: 2026-08-29
deliverables: []
---

# T-253 — Correct the audit's forty-nine Low findings, or accept each with a reason and a date

## 1. Specify

**Outcome**
Every `Low` finding in the register is corrected, or carries an accepted row with a reason and a date. **Batching is the method's own rule for this level** and not a convenience: forty-nine task records for forty-nine one-line corrections is a cost the tracker pays and nobody recovers, and batching keeps every finding in the record while stopping the tracker from becoming the audit's byproduct.

**Closes** the whole `Low` band in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: the whole band, worked in register order, each finding either fixed or moved to the register's section 4 with a reason and a date
- In: **stating how many were accepted rather than fixed**, because a batch that accepts most of its band is evidence the severity threshold was set too low - which the method says is the thing to fix, not the batch
- Out: any `High` or `Med` finding - each of those has its own task
- Out: re-ranking. A finding that turns out worse than `Low` is said so on its row and raised as its own task; it is not quietly fixed at this level

**Inputs**
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3, the `Low` rows
- the method's section 4, served by the installed taskmd plugin - *severity has to oblige something*
- section 4 of the register, *Accepted without action*, where an accepted row goes

**Acceptance criteria**
- [ ] every `Low` row is fixed, or has an accepted row carrying a reason and a date
- [ ] the fixed-to-accepted split is stated as two numbers
- [ ] no `Low` row is left `open` with neither disposition
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None yet. The register's `Remedy` column carries a hypothesis for each finding, and the method's
  section 5 says it is a hypothesis: whoever implements this measures before committing to it, and
  records what the measurement said.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <the files this task changed>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- <T-NNN or "none">

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`Low`**, batched, which is the method's own rule for the level rather than a convenience — its reason is that the tracker must not become the audit's byproduct. |
