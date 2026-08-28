---
id: T-268
title: Guard the single-letter shortcuts, dismiss the sources box, and land data-played on arrival
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

# T-268 — Guard the single-letter shortcuts, dismiss the sources box, and land data-played on arrival

## 1. Specify

**Outcome**
The shell's chrome behaves the way its own comments say. Today **every browser chord built on one of six letters is captured** — Ctrl-R enters the reading view and cancels the reload, Ctrl-F goes fullscreen instead of opening find, and `grep -n "ctrlKey|metaKey|altKey" shell/deck.js` returns nothing; the **sources box does not dismiss on an outside click** though the More menu beside it does, with the More menu's own comment arguing the case; and **`data-played` lands at `t = 0` of the transition**, so an entrance gated on it — the gate `DS-146` tells authors to use — begins under the outgoing slide.

**From the adopter report** [`008`](../docs/adopter-reports/claimai/008-single-letter-shortcuts-swallow-ctrl-r-and-every-other-browser-chord.md), [`009`](../docs/adopter-reports/claimai/009-the-sources-box-does-not-dismiss-on-an-outside-click.md), [`010`](../docs/adopter-reports/claimai/010-data-played-lands-at-transition-start-so-an-entrance-plays-under-the-outgoing-slide.md).

**Scope**
- In: the modifier guard, one line, with Shift deliberately excluded because the handler already accepts `R` as well as `r`
- In: the same three-line document listener for the sources root, keyed to `.sources` rather than to the button so the toggle does not close what the click just opened
- In: **a second attribute, `data-arrived`, rather than moving `data-played`** — the record's own safer option, because nothing already in the field changes behaviour
- In: the rule rows: the keyboard section saying the shortcuts are unmodified only, and `DS-146` saying *when* `data-played` lands
- Out: anything the records above do not name. The report is a closed one-way hand-over — there is no
  channel back and none is expected, so a question this task cannot answer is settled here rather
  than asked.

**Inputs**
- the records above, [`008`](../docs/adopter-reports/claimai/008-single-letter-shortcuts-swallow-ctrl-r-and-every-other-browser-chord.md), [`009`](../docs/adopter-reports/claimai/009-the-sources-box-does-not-dismiss-on-an-outside-click.md), [`010`](../docs/adopter-reports/claimai/010-data-played-lands-at-transition-start-so-an-entrance-plays-under-the-outgoing-slide.md) — each carries its evidence, its version and its own proposed fix
- all three were reported by the presenter using the deck, which is the one instrument this repository cannot run
- `010`'s own note that the reviewer's original report was the **deck's** defect and not htmldeck's; what is left is the narrower thing underneath

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
