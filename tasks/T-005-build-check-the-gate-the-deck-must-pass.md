---
id: T-005
title: Build check — the gate the deck must pass
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: [T-002]
related: [T-001]
work_package: none
owner: maintainer
created: 2026-08-04
updated: 2026-08-04
deliverables: []
---

# T-005 — Build check — the gate the deck must pass

## 1. Specify

**Outcome**
An automated check run on every generated deck.

**Why this one**
Cheap to build, and it converts several house rules from hopes into failures.

**Acceptance criteria**
- [ ] Fails on any external reference
- [ ] Fails on banned terminology
- [ ] Fails on a `<section>` with no heading
- [ ] Checks contrast against WCAG AA
- [ ] Proven **failing** on each class before being trusted

**Open questions**
- Is the check a separate command, or always part of build?

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
