---
id: T-305
title: Let render.py see an SVG paint change, a scripted hover, and a figure painting over its neighbour
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-299, T-267]
work_package: PH1
owner: the project owner
business_value: medium
effort: m
created: 2026-09-13
updated: 2026-09-13
deliverables: []
---

# T-305 — Let render.py see an SVG paint change, a scripted hover, and a figure painting over its neighbour

## 1. Specify

**Outcome**
`render.py` reports a difference where one was painted, or says plainly what it did not exercise.
Today it reports confidently on three states it never reached:

- `state` compares `STATE_DEEP` (`tools/deck/render.py` `:1280`-`:1281`), which holds `color`,
  `background`, `borderColor`, `transform`, `boxShadow`, `outline` and `filter` and no SVG paint
  property. So a `fill` or `stroke` change reports that nothing measured differs.
- `state --hover` substitutes the `:hover` rule onto an attribute (`tools/deck/render.py`
  `:1262`-`:1274`) and dispatches no event, so an effect a script runs on `mouseenter` never runs.
- `measure` checks a figure only against the stage (`tools/deck/render.py` `:325`, `:350`-`:354`), and
  never against its own track. So a figure painting over the prose beneath it reports zero overflow.

**From the adopter report** [`06`](../docs/adopter-reports/nextep/2026-09-07-measure-reports-no-overflow-while-a-figure-paints-over-the-prose.md), [`08`](../docs/adopter-reports/nextep/2026-09-07-render-state-cannot-see-an-svg-fill-change.md), [`09`](../docs/adopter-reports/nextep/2026-09-07-render-state-hover-fires-css-hover-but-no-mouseenter.md).

**Re-run in triage, 2026-09-13, on this tree.** `state --hover ".ruler-ticks button"` on a copy of the
reference deck printed the record's message for `08`, and the tick's `mouseenter` label write did not
run for `09`. `06` was confirmed from source.

**`09` re-opens a choice, not an oversight.** T-267 chose substitution on purpose and prints
*substituted trigger*. The remedy is a decision recorded here: dispatch pointer events at the
element's centre, or keep substitution and say in the report that script handlers were not exercised.

**Scope**
- In: `fill`, `fillOpacity`, `stroke`, `strokeWidth` and `strokeDasharray` in `STATE_DEEP`
- In: the hover decision above, measured on a deck whose hover effect is scripted
- In: a figure's box compared against its own container, from the geometry `measure` already collects
- Out: anything the records above do not name. The report is a closed one-way hand-over, so a
  question this task cannot answer is settled here rather than asked

**Inputs**
- the three records above, each with its command, its version and its own proposed fix
- [T-299](T-299-triage-the-nextep-adopter-report.md) section 3, where the three were ruled together

**Acceptance criteria**
- [ ] records `06`, `08` and `09` are each closed with the remedy measured, or deferred with the reason
      recorded in this task
- [ ] each fix is proved by seeding the defect and watching it fire, in both directions (**L-125**)
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None. Each record carries its evidence and a proposed fix; the proposal is a hypothesis to measure
  before committing to it.

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
| 2026-09-13 | -> proposed | Raised by T-299 from Nextep records `06`, `08` and `09`, which share `render.py`. `PH1`: an adopter met all three in the published `0.7.0`. `06` arrived as a `gap` and is ruled a defect, because `measure` reports zero overflow over a real overlap. |
