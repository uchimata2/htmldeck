---
id: T-316
title: Give the reference deck's sources quick views
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-070, T-233]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-09-14
updated: 2026-09-14
deliverables: []
---

# T-316 — Give the reference deck's sources quick views

## 1. Specify

**Outcome**
Every source the reference deck names opens its document in the quick view. Today its provenance
marks list `Cost model`, `Ridership model` and the programme timetable as plain text:
`quickview.py list examples/reference-deck.html` reports 0 quick views, while `examples/sources/`
holds all three documents.

**Why it was passive.** Not a token saving. The deck was built by hand before the quick view existed
([T-070](T-070-the-quick-view-for-a-source-document.md)), and no later task attached them;
the three decks built afterwards all carry them.

**Raised by** the owner's observation beside the B27 looks, 2026-09-14: sources should almost never be
passive text.

**Scope**
- In: attach the three sources with `quickview.py add`, and whatever the addition costs the gates and
  the fixture derived from this deck
- Out: a rule that a source with a file must open it, which is a wider question than one deck

**Acceptance criteria**
- [ ] `quickview.py list` names three quick views, and `quickview.py check` passes against
      `examples/sources/`
- [ ] the look is recorded as owed
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |

## 3. Implement

**Decisions & assumptions**
- <what was decided>: <why, in one sentence>. <Reversible | Not reversible>. — YYYY-MM-DD

**Outputs produced**
- `deliverables/...`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- <T-NNN or "none">

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-14 | -> proposed | Raised from the owner's observation beside the B27 looks. `PH3`. Batched into B28 first by the owner's ruling. |
