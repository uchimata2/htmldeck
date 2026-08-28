---
id: T-260
title: Decide what DS-244 measures, from the two findings that contradict each other
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

# T-260 — Decide what DS-244 measures, from the two findings that contradict each other

## 1. Specify

**Outcome**
`DS-244` decides whether anything is actually obscured. Today it compares text against text and nothing else, which makes it **wrong in both directions at once** — the pair of findings is why this is one task. It **misses** a label crossing the rectangle it labels, the commonest way a hand-built figure goes wrong, three instances in one evening on slides it called clean. It **refuses** a cross-fade in place, because it does not read `opacity` and cannot see that only one of the pair is ever visible — three constructions rejected in a row on one slide.

**From the adopter report** [`013`](../docs/adopter-reports/claimai/013-ds-244-sees-label-over-label-but-not-label-over-shape.md), [`022`](../docs/adopter-reports/claimai/022-ds-244-refuses-a-cross-fade-in-place.md).

**Scope**
- In: reading the computed `opacity` before pairing two labels
- In: comparing a text rect against `rect`, `path` and `line` in the same `svg.fig` — and the test has to be *crosses a shape edge*, never *touches a shape*, because a label centred in its own box is legitimate
- In: **saying which frame was measured** where opacity is animated
- In: **at minimum, saying in the rule row what the measurement does not do**, so nobody reads a pass as *the labels are placed correctly*
- Out: anything the records above do not name. The report is a closed one-way hand-over — there is no
  channel back and none is expected, so a question this task cannot answer is settled here rather
  than asked.

**Inputs**
- the records above, [`013`](../docs/adopter-reports/claimai/013-ds-244-sees-label-over-label-but-not-label-over-shape.md), [`022`](../docs/adopter-reports/claimai/022-ds-244-refuses-a-cross-fade-in-place.md) — each carries its evidence, its version and its own proposed fix
- **Read the two records together or neither makes the point.** `013` says the rule is too blind and `022` says it is too strict; together they say it tests proximity of two text runs where it means obstruction
- [T-204](T-204-an-instrument-for-mark-collisions.md), which built `DS-244` and recorded text-against-line as *reports, never gates* after measuring 16 firings for 1 real defect. **That calibration is a term in this decision** and must not be quietly reversed
- `022` records that the rule improved the slide three times while being wrong — it is a report, not a complaint

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
