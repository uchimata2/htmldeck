---
id: T-271
title: Decide whether a slide can open a quick view scoped to the section it argues from
type: decision
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-225]
work_package: PH3
owner: the project owner
business_value: low
effort: m
created: 2026-08-29
updated: 2026-08-29
deliverables: []
---

# T-271 — Decide whether a slide can open a quick view scoped to the section it argues from

## 1. Specify

**Outcome**
**Accepted and deferred.** A slide citing one risk row, one finding or one clause makes the reader open the whole source and scroll to find it. The whole-file view is right on the colophon, where a reader is browsing sources, and wrong on an argument slide, where they are checking one claim. The adopter built any per-section panel by hand on the slide that needed it.

**From the adopter report** [`001`](../docs/adopter-reports/claimai/001-per-section-quick-view.md).

**Scope**
- In: the decision, which the record explicitly leaves to this repository: a new component, an anchor into the existing sheet, or a `data-` attribute selecting a range
- In: **deferred rather than rejected**, and the reason is scheduling: it is the only record in the set that asks for a new component, and it competes with nothing else here
- Out: anything the records above do not name. The report is a closed one-way hand-over — there is no
  channel back and none is expected, so a question this task cannot answer is settled here rather
  than asked.

**Inputs**
- the record above, [`001`](../docs/adopter-reports/claimai/001-per-section-quick-view.md) — each carries its evidence, its version and its own proposed fix
- `COMPONENT-CONTRACT.md` section 3 — `.qv-src` as a `template` whose parent is `.sources-item`
- `DS-085`, which names the colophon as the one thing allowed to follow the closing slide

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
