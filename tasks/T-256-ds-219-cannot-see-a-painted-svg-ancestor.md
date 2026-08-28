---
id: T-256
title: Walk the full ancestor chain for DS-219's ground, and settle the doubt the rationale records
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-225]
work_package: PH1
owner: the project owner
business_value: critical
effort: m
created: 2026-08-29
updated: 2026-08-29
deliverables: []
---

# T-256 — Walk the full ancestor chain for DS-219's ground, and settle the doubt the rationale records

## 1. Specify

**Outcome**
`DS-219` measures a label against the ground a reader actually sees. Today it walks to the nearest painted background and **stops at the mark**, so a pale label on a pale card resting on a filled panel is measured against the card alone and can never reach 3:1. The adopter's deck fails **40 of 46 labels** and has since the build; every attempt to fix it made the slide worse.

**From the adopter report** [`019`](../docs/adopter-reports/claimai/019-ds-219-cannot-see-a-painted-svg-ancestor.md).

**Scope**
- In: compositing painted ancestors rather than stopping at the first
- In: **saying so where the walk cannot resolve a ground** — an unmeasurable pair and a failing pair are different findings
- In: **settling the `never`**: [`DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) section 5.7 is headed *two rules that said more than they meant* and says of this one that *the prohibition outran its own argument*. This is independent evidence for a doubt this repository already recorded, from a deck built without knowing the section existed
- Out: anything the records above do not name. The report is a closed one-way hand-over — there is no
  channel back and none is expected, so a question this task cannot answer is settled here rather
  than asked.

**Inputs**
- the record above, [`019`](../docs/adopter-reports/claimai/019-ds-219-cannot-see-a-painted-svg-ancestor.md) — each carries its evidence, its version and its own proposed fix
- [T-241](T-241-the-design-system-and-the-rationale-against-what-shipped.md), which closes `PR-97` — the rationale recording conflicts as unresolved. **This task supplies the evidence that one of them can now be settled**
- the second face in the record: seven unfilled `rect`s are black, `DS-215` reported fourteen runs under 4.5:1 and `DS-219`'s count rose by the same fourteen — the rule sees a painted *sibling* it was never meant to measure and misses the *ancestor* that is the real ground

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
