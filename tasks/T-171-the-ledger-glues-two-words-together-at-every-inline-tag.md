---
id: T-171
title: The ledger glues two words together at every inline tag it deletes
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-169]
work_package: PH1
owner: the project owner
business_value: medium
effort: s
created: 2026-08-16
updated: 2026-08-16
deliverables:
  - tools/deck/content.py
---

# T-171 — The ledger glues two words together at every inline tag it deletes

## 1. Specify

**What is wrong.** `runs()` in [`tools/deck/content.py`](../tools/deck/content.py) deletes an inline
tag — `INLINE.sub("", frag)` — instead of replacing it with a boundary. Where two inline elements
butt together with no whitespace between them, which is how a deck's key/value rows are written,
the last word of one and the first word of the next arrive as **one word**:

| In the deck | In the run | In the label |
| :--- | :--- | :--- |
| `<span class="k">The other 5%</span><span>The 02:30 …` | `5%The 02:30 …` | — |
| `<span class="k">If it fails</span><span>Service holds …` | `failsService holds …` | `failsservice` |
| `<span class="k">Measure</span><span>Boardings on …` | `MeasureBoardings on …` | `measureboardings` |
| `<span class="k">What they get</span><span>Nothing until …` | `getNothing until …` | `getnothing` |

**Why it matters.** `label_of` is a set of significant words, and a glued word matches nothing. Two
documents describing one figure in the same words fail to bind because one of them wrote the words
inside adjacent tags — and the failure is invisible, because a label full of `customershigh` and
`getnothing` looks like the approximate matching the module documents.

**It cost a real figure once already.** T-169's first cut guarded the unit branch of `FIGURE` with
`(?![-\w])`, so a unit word could not run on into a compound. `5%The` read as a compound and
`sort-window`'s `5%` left the ledger. The guard was narrowed to `(?!-)` rather than the gluing
fixed, because the two are different defects and the wider guard is the one that is actually right.

**Scope**
- In: replace a deleted inline tag with a space, and prove no figure is split by it.
- In: restore the `(?![-\w])` guard on `FIGURE`'s unit branch once the gluing is gone, so
  `4 stopover` stops minting `4 stop`.
- Out: the non-inline split, which is correct and load-bearing — see the comment above `INLINE`.

**The risk is the reverse direction.** A space where a tag was could split a figure written across
one: `$<b>5.6M</b>` becomes `$ 5.6M`, and `<b>5.6</b>M` becomes `5.6 M`. Both patterns already
allow one `\s?`, so both should survive — that is a prediction, and the before/after ledger
comparison is what tests it.

**Acceptance criteria**
- [ ] A deleted inline tag leaves a word boundary, asserted in `self_test` on strings
- [ ] Every ledger this repository can build is compared before and after; every change is a glued
      word coming apart, and none is a figure lost or a verdict moved
- [ ] `FIGURE`'s unit branch carries the `(?![-\w])` guard, with `4 stopover` asserted
- [ ] No shipped deck moves

## 2. Plan

_Not planned._

## 3. Implement

_Not started._

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-16 | → proposed | Raised out of [T-169](T-169-the-figure-binder-cannot-bind-a-value-split-across-table-cells.md)'s implementation, which hit it as a regression and narrowed its own guard rather than widen its scope. |
