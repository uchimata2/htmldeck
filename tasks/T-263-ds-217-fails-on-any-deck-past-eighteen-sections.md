---
id: T-263
title: Give regularScale a tolerance, so a long deck can satisfy DS-217
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-225]
work_package: PH1
owner: the project owner
business_value: high
effort: s
created: 2026-08-29
updated: 2026-08-29
shipped_in: unreleased
deliverables: []
---

# T-263 — Give regularScale a tolerance, so a long deck can satisfy DS-217

## 1. Specify

**Outcome**
A deck of any legal length can satisfy `DS-217`. Today `regularScale()` refuses the ruler's `data-scale` claim past about eighteen sections — sub-pixel layout rounding across many flex items produces a third cluster of pitch — and every tick is then counted as its own chrome item against a budget of about twelve. **The failure is one no slide edit can move**, measured by truncation: 18 sections pass, 19 fails at 24 items, 25 fails at 30.

**From the adopter report** [`002`](../docs/adopter-reports/claimai/002-ruler-scale-claim-breaks-past-eighteen-sections.md).

**Scope**
- In: clustering gaps and widths to the nearest whole design unit rather than the nearest half CSS pixel, or accepting a spread under one unit
- In: or letting the ruler's own `data-dense` carry the claim — the shell already sets it past the measured capacity, so the check could test the two clusters it declares rather than discovering them
- Out: anything the records above do not name. The report is a closed one-way hand-over — there is no
  channel back and none is expected, so a question this task cannot answer is settled here rather
  than asked.

**Inputs**
- the record above, [`002`](../docs/adopter-reports/claimai/002-ruler-scale-claim-breaks-past-eighteen-sections.md) — each carries its evidence, its version and its own proposed fix
- `DS-082` already requires a recorded reason past twelve slides and the adopter's deck has one, so *make the deck shorter* is not an answer available to them
- `CLAUDE.md`'s verifying section and [T-178](T-178-dense-mode-drops-the-position-mark-below-the-section-marks.md) — the ruler is already known to degrade past 16, and this is the second thing that does

**Acceptance criteria**
- [ ] every record named above is **closed with its remedy measured**, or explicitly deferred with the
      reason recorded in this task
- [ ] each fix is proved by seeding the defect and watching the check fire, in both directions where
      the record's own evidence is a verdict (**L-125**)
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None yet. Every record carries its own evidence and its own proposed fix; the proposal is a
  hypothesis and whoever implements it measures before committing to it.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Reproduce on this repository's own deck before touching the check. `longdeck.py` splices the reference deck to any length, so the question can be asked at 19, 25 and 43 | 19, 25 and 43 all **pass**. The record's threshold does not reproduce on length alone, so the stated cause is wrong or incomplete |
| 2 | Measure what `regularScale()` actually sees, rather than reasoning about it — a throwaway probe dumping every tick's width and centre | At 43 ticks the widths differ by **1e-4 CSS px**. The old test rounded to half a pixel, so sub-pixel rounding never reached the bucket. **Cause refused** |
| 3 | Find what does produce a third cluster. Two mark sizes give three centre-to-centre distances; the third appears only where two **major** marks are adjacent | Confirmed: a fixture whose stage 5 holds one slide fails at **30 items**, the record's own 25-section row to the digit |
| 4 | Re-bind the check on what a scale claims — a repeating lattice — instead of on a cluster count | `regularScale()` in `audit.py`: at most two mark sizes, and either evenly spaced centres **or** evenly spaced edges |
| 5 | Make the fixture a command, for the reason `longdeck.py` itself exists | `--solo-stage`, plus a self-test asserting the adjacency it produces and that a plain splice does not |
| 6 | Seed the three irregularities the rule still forbids, and watch each fire | Irregular spacing, a third mark size and a label at rest all FAIL, each naming its own cause |
| 7 | Amend the `DS-217` row to say what *uniform pitch* means where two mark sizes exist | The row carries both lattices, the refusal of the report's cause, and `DS-000` reversibility |

## 3. Implement

**Decisions & assumptions**
- **Both of the record's proposed remedies are refused, and so is its account of the cause** — measured, 2026-08-29. Candidate 1, *give `regularScale()` a tolerance*, would have changed nothing: the rounding it blames is 1e-4 CSS px across 43 ticks, four orders of magnitude below the half-pixel bucket. Candidate 2, *let `data-dense` carry the claim*, would have made the ruler's own mode attribute the thing that decides whether the ruler is regular — trusting exactly what `DS-217` says is verified and never trusted. The finding itself is real and is fixed.
- **The defect is adjacency, not length.** Two mark sizes produce three centre-to-centre distances — minor/minor, minor/major, major/major — and the third exists only where two section marks sit side by side, which is a stage holding a single slide. Length is what turns the small ticks into a second size (dense mode) and is therefore a precondition, which is why the record read the threshold as a length. Kept as [L-141](../docs/lessons/L-141.md), because the shape generalises past this rule: a threshold found by varying one thing names that thing only if nothing else changes with it.
- **A scale is a repeating lattice, and there are two of them** — evenly spaced centres, or evenly spaced edges. Accepting either is what admits both a classic ruler and this deck's flush-packed cells. It **tightens** as much as it opens: the old test allowed any two gap values, including two nothing about the marks explained. 2026-08-29.
- **The tolerance is half a design unit, applied by clustering rather than by rounding**, and each value is compared with its cluster's first member so that a slow drift across forty marks cannot pass as one cluster. Fixed-width buckets were the old mechanism and they split two values that straddle a boundary however close they are. 2026-08-29.
- **No look is owed.** Nothing this task changed renders: the checker's verdict moved, no deck did. The five tracked decks are byte-identical.

**Outputs produced**
- [`tools/deck/audit.py`](../tools/deck/audit.py) — `regularScale()` re-bound on the lattice, and its verdict now names why it refused
- [`tools/deck/longdeck.py`](../tools/deck/longdeck.py) — `--solo-stage`, its docstring paragraph, and the self-test assertion
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — the `DS-217` row's *uniform pitch* clause
- [`docs/adopter-reports/claimai/002-ruler-scale-claim-breaks-past-eighteen-sections.md`](../docs/adopter-reports/claimai/002-ruler-scale-claim-breaks-past-eighteen-sections.md) — closed, with the refusals stated

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Record [`002`](../docs/adopter-reports/claimai/002-ruler-scale-claim-breaks-past-eighteen-sections.md) closed with its remedy measured | pass | Closed. The finding is fixed; its cause and both its candidate remedies are refused, each with the measurement that refused it |
| Each fix proved by seeding the defect and watching the check fire, in both directions (**L-125**) | pass | `--solo-stage` at 25 slides: **30 items, FAIL** before, **6 items, pass** after. Three seeded irregularities still fail — irregular spacing, a third mark size, a label at rest — each with its own reason in the verdict |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | pass | Both run at the end of B5, after T-262 and T-264, on a tree nothing was editing |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → proposed | Raised by [T-225](T-225-triage-the-claimai-adopter-report.md), the triage of the ClaimAI adopter report. **`PH1`**: a defect an adopter met in the published `0.6.0`, which is `CLAUDE.md`'s one condition for reopening the phase. Verified against this tree before the record was actioned — the report's `Version seen` was stamped rather than re-run on fourteen of the twenty-seven. |
| 2026-08-29 | → done | Batch **B5**. The record's cause and both its candidate remedies refused by measurement; the finding fixed by re-binding `regularScale()` on the lattice a scale claims. `--solo-stage` makes the fixture a command, so the 30-items-to-6 proof can be re-run rather than believed. |
