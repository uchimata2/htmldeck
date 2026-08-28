---
id: T-265
title: Decide whether DS-110 narrows by where a raster sits
type: decision
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-225]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-29
updated: 2026-08-29
deliverables: []
---

# T-265 — Decide whether DS-110 narrows by where a raster sits

## 1. Specify

**Outcome**
**A decision, not a fix.** `DS-110` bans every raster the deck produces. The adopter's presenter supplied a pencil drawing for the lobby — front matter, which `DS-242` already defines as carrying nothing from the argument — and the deck now ships a permanent failure to do something the rule was never written to prevent. Every alternative was worse: no tracer installed, the drawn emblem already rejected, and the reading view is where nobody is sitting.

**From the adopter report** [`011`](../docs/adopter-reports/claimai/011-ds-110-cannot-tell-a-rasterised-diagram-from-a-drawing.md).

**Scope**
- In: the decision, argued both ways, with `DS-000`'s stated reason either way
- In: **the rule row saying what it protects.** *No raster the deck produces, ever* reads as a portability rule and is really a legibility and consistency rule about diagrams — that is the half worth doing whichever way the decision goes
- Out: anything the records above do not name. The report is a closed one-way hand-over — there is no
  channel back and none is expected, so a question this task cannot answer is settled here rather
  than asked.

**Inputs**
- the record above, [`011`](../docs/adopter-reports/claimai/011-ds-110-cannot-tell-a-rasterised-diagram-from-a-drawing.md) — each carries its evidence, its version and its own proposed fix
- **My recommendation is the record's own weaker form, not its primary.** Allowing any raster in a `front`/`back` section is broader than the argument supports; allowing one that is not inside `.body` and carries no `role="img"` label naming data is closer to the real test. It is harder to explain, which is a cost worth paying for a rule this load-bearing
- `CLAUDE.md` rule 3 — *still never raster images* — which this would amend and which is why the owner decides it

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
| 2026-08-29 | → proposed | Raised by [T-225](T-225-triage-the-claimai-adopter-report.md), the triage of the ClaimAI adopter report. **`PH3`**: not a defect in the published plugin's behaviour, so `CLAUDE.md`'s rule puts it in the main line rather than reopening a shipped phase. |
