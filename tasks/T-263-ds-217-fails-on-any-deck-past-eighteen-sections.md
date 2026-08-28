---
id: T-263
title: Give regularScale a tolerance, so a long deck can satisfy DS-217
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-225]
work_package: PH1
owner: the project owner
business_value: high
effort: s
created: 2026-08-29
updated: 2026-08-29
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
| 2026-08-29 | → proposed | Raised by [T-225](T-225-triage-the-claimai-adopter-report.md), the triage of the ClaimAI adopter report. **`PH1`**: a defect an adopter met in the published `0.6.0`, which is `CLAUDE.md`'s one condition for reopening the phase. Verified against this tree before the record was actioned — the report's `Version seen` was stamped rather than re-run on fourteen of the twenty-seven. |
