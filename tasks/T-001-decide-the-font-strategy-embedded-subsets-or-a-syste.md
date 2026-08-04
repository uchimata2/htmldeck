---
id: T-001
title: Decide the font strategy: embedded subsets or a system stack
type: decision
status: proposed
phase: specify
parent: null
blocked_by: []
related: []
work_package: none
owner: maintainer
created: 2026-08-04
updated: 2026-08-04
deliverables: []
---

# T-001 — Decide the font strategy: embedded subsets or a system stack

## 1. Specify

**Outcome**
A decided approach to typography that keeps decks self-contained.

**Why this one**
**This decides how the decks look and blocks the build mode.** Every deck in the source corpus carries 2–7 external references, mostly web fonts — none renders correctly offline. Typography is also what makes those decks look designed rather than generated, so the trade-off is identity against self-containment.

**Acceptance criteria**
- [ ] Option chosen with the reason recorded
- [ ] If embedding: licences permit redistribution, and each is recorded next to its font
- [ ] A deck built with the chosen approach renders correctly **with the network disabled**
- [ ] File size of a 12-slide deck measured and stated

**Open questions**
- Is a curated system-font stack distinctive enough to avoid the template look?

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
| 2026-08-04 | → proposed | Seeded from `docs/BRIEF.md` when the project folder was prepared. |
