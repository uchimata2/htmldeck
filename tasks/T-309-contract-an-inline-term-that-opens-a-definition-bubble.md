---
id: T-309
title: Contract an inline term that opens a definition bubble
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-299, T-262]
work_package: PH3
owner: the project owner
business_value: low
effort: m
created: 2026-09-13
updated: 2026-09-13
deliverables: []
---

# T-309 — Contract an inline term that opens a definition bubble

## 1. Specify

**Outcome**
`docs/COMPONENT-CONTRACT.md` gives an inline term with a definition bubble a contracted form, so a deck
that uses the pattern passes the gate on the contract's terms. Today the contract defines `.disc` only
as a block, and no inline disclosure exists. The nearest precedent is the sources box: deliberately not
a `.disc`, with rows of its own, and still bound to the general disclosure rules `DS-163`, `DS-164`,
`DS-227` and `DS-137`.

**From the adopter report** [`18`](../docs/adopter-reports/nextep/2026-09-08-an-inline-term-tag-with-a-definition-bubble-has-no-contracted-form.md).
The deck's owner asked for the pattern by name and approved it.

**Scope**
- In: contract rows for the term and its bubble, shaped on the sources box
- In: `DS-138`'s direction clause for an inline control, so the bubble opens away from the reading line
- In: `DS-092` subtracting bubble text from the word count, as
  [T-262](T-262-ds-092-counts-a-sources-box-as-prose.md) did for the sources box
- In: the shell styles and script the rows require, looked at in a rendered deck
- Out: anything the record does not name. The report is a closed one-way hand-over, so a question this
  task cannot answer is settled here rather than asked

**Inputs**
- the record above, with the markup the deck used
- the sources box's rows in `docs/COMPONENT-CONTRACT.md`, and `DS-092`, `DS-137`, `DS-138`, `DS-163`,
  `DS-164` and `DS-227` in `docs/DESIGN-SYSTEM.md`

**Acceptance criteria**
- [ ] record `18` is closed with the component contracted, built and looked at in a rendered deck, or
      deferred with the reason recorded in this task
- [ ] a deck using the term passes the rules the contract binds it to, and a seeded misuse fails them
      (**L-125**)
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None. The record carries the markup and the owner's approval; the shape is settled here.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

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
| 2026-09-13 | -> proposed | Raised by T-299 from Nextep record `18`. `PH3`: a new component, not a defect in one that exists. |
