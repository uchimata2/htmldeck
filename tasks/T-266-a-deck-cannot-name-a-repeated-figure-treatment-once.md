---
id: T-266
title: Say what to do when a class fails DS-229, and decide whether a deck gets a local prefix
type: fix
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

# T-266 — Say what to do when a class fails DS-229, and decide whether a deck gets a local prefix

## 1. Specify

**Outcome**
A deck can name a repeated figure treatment once, or is told plainly that it cannot. Today `DS-229` reports `.ico` as *uncontracted* — and the contract lives in the plugin, so a builder reads *not yet in the contract*, goes looking for where to add the row, and the search ends nowhere. Eleven marks then repeat three presentation attributes each.

**From the adopter report** [`014`](../docs/adopter-reports/claimai/014-a-deck-cannot-name-a-repeated-figure-treatment-once.md).

**Scope**
- In: **the message, which is a string change and removes the whole dead-end search**: a deck may not add a class; carry the properties as presentation attributes on the element
- In: **a reserved deck-local prefix** — the record's second proposal and the real gap. `DS-229` keeps its job of stopping a deck redefining a *component* and stops policing a deck's own figure internals, which no component contract can anticipate
- Out: anything the records above do not name. The report is a closed one-way hand-over — there is no
  channel back and none is expected, so a question this task cannot answer is settled here rather
  than asked.

**Inputs**
- the record above, [`014`](../docs/adopter-reports/claimai/014-a-deck-cannot-name-a-repeated-figure-treatment-once.md) — each carries its evidence, its version and its own proposed fix
- the record explicitly does **not** ask to weaken `DS-229` over components — holding `.slide` or `.sources-box` to a contract is the rule earning its keep
- its third proposal, a figure-internals contract section, which the record itself calls probably wrong because the set of treatments a hand-built figure needs is open

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
