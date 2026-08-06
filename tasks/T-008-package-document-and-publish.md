---
id: T-008
title: Package, document and publish
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: [T-002, T-004, T-005, T-028]
related: []
work_package: final
owner: maintainer
created: 2026-08-04
updated: 2026-08-07
deliverables: []
---

# T-008 — Package, document and publish

## 1. Specify

**Outcome**
An installable plugin with an honest README and a fresh example deck.

**Why this one**
The example deck must be written new on a neutral topic — the corpus is real training work for named scenarios and none of its content may be copied here.

**Acceptance criteria**
- [ ] Install instructions end with a command that proves it runs
- [ ] Example deck written fresh, on a neutral topic
- [ ] Renders offline
- [ ] No personal, client or machine data anywhere
- [ ] Installs from a clean clone

**Open questions**
- Marketplace plugin, plain skill package, or both?

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <path>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-07 | (no change) | **Two blockers added by [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md), both taken from [`BRIEF.md`](../docs/BRIEF.md)'s own definition of done.** [T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) is the *Release gate*, settled by the owner 2026-08-06 and until now recorded **in prose with no edge representing it** — the precise drift `blocked_by` exists to prevent, and the strongest finding of the audit. [T-005](T-005-build-check-the-gate-the-deck-must-pass.md) is criterion 2 on the same list, equally open and equally a gate on shipping; it was `related`, which does not gate. Both bind publishing and nothing else, which is what this task is. `related` is now empty because its only entry became a blocker. |
| 2026-08-04 | → proposed | Seeded from `docs/BRIEF.md` when the project folder was prepared. |
