---
id: T-155
title: Date a record by its own row, not by the table it sits in
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-154, T-129, T-088]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-14
updated: 2026-08-14
deliverables: []
---

# T-155 — Date a record by its own row, not by the table it sits in

## 1. Specify

**Outcome**
A struck-through, dated row in [`figures.py`](../tools/docs/figures.py) excuses **itself** from
checking, not every live claim sharing its table or its paragraph.

**Raised 2026-08-14 by
[T-154](T-154-bind-the-measurements-that-five-live-documents-state-in-prose.md)**, which wrote the
fix, measured it, and **did not ship it**. `blocks()` computes `dated` from `DONE_ROW.search(block)`,
where a block is anything between blank lines — so one `~~…~~ **done 2026-08-10**` row silently turns
off `claimed()` and the artifact binding for every other row in that table. `claim_scopes()` already
splits a block at table rows and list items, and is the split T-088 and T-129 settled for exactly this
question about a link's subject.

**Why it is a task and not an edit.** Measured over all six documents `figures.py` reads, the
per-scope and per-block versions **decide no verdict differently today**. Shipping an unmeasured
behaviour change inside a task about unmeasured claims was the wrong shape, and a latent defect
written into a code comment is one nobody schedules.

**Scope**
- In: `blocks()`, `declared()`'s block-level `DONE_ROW` guard, and `artifact_claims()`.
- In: a fixture that fails when a live claim beside a dated row goes unjudged — the defect has no
  instance today, so the fixture must build its own (**L-78**, **L-85**).
- Out: what marks a record. `DONE_ROW` stays `~~…~~ **done <date>**`; T-154 widened it, read
  `pipeline.md` 190, and reverted — the strike there is on the name of a **gap** and the sentence
  after it is a live claim in the shipped skill.

**Inputs**
- [T-154](T-154-bind-the-measurements-that-five-live-documents-state-in-prose.md) §3 — the
  measurement, and why it was reverted
- **L-97** — a check anchored on the value that drifts goes blind exactly when it is needed
- [T-129](T-129-the-reference-decks-figures-in-examples-readme-are-unwatched-and-two-are-wrong.md) —
  the same block-versus-scope question, decided for the artifact binding

**Acceptance criteria**
- [ ] A live claim in a table that also holds a dated record is judged
- [ ] A dated record is still not judged, in the row it is written in
- [ ] The fixture fails when the guard is put back to block scope
- [ ] `python tools/docs/figures.py` and `python tools/check_all.py` green, with the `compared`
      count not falling

**Open questions**
- **Does the same scope error exist in `stale_exclusions` or `audit`'s prose loop?** Neither reads
  `DONE_ROW`, so probably not — worth one search rather than an assumption. — the implementer, at
  `specify`.

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
| 2026-08-14 | → proposed | Raised by T-154, which wrote the fix and measured it as changing no verdict in any of the six documents `figures.py` reads. `PH3` because PH2 has shipped and this is not a defect in the published plugin — `figures.py` is a repository tool. |
