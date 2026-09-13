---
id: T-306
title: Wire an icon-first source item in quickview.py, and make shell.py sync name a stale chrome tail
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-299, T-269]
work_package: PH1
owner: the project owner
business_value: medium
effort: s
created: 2026-09-13
updated: 2026-09-13
deliverables: []
---

# T-306 — Wire an icon-first source item in quickview.py, and make shell.py sync name a stale chrome tail

## 1. Specify

**Outcome**
Two build-path tools stop reporting a state that is false. Today `quickview.py`'s item pattern fixes
the id before the icon, so a `.sources-item` whose icon comes first is invisible to `wire` and `plan`
and is reported as uncited. And `shell.py sync` ends by counting regions (`tools/deck/shell.py`
`:1265`) and never runs or names `tail` (`:198`), so a deck whose chrome tail is a release behind is
reported fully up to date.

**From the adopter report** [`03`](../docs/adopter-reports/nextep/2026-09-06-quickview-cannot-wire-an-icon-first-source-item.md), [`15`](../docs/adopter-reports/nextep/2026-09-08-shell-sync-is-silent-about-a-stale-chrome-tail.md).

**Re-run in triage, 2026-09-13, on this tree.** `item_pattern()` matched the id-first ordering and
returned no match for the icon-first one. `15` was confirmed from source.

**Scope**
- In: the two optional groups of the item pattern made order-independent, the record's own alternation
- In: one line at the end of `sync` naming `shell.py tail <deck>`, the way `sync` already names
  `shell.py tokens --write` for undeclared tokens
- Out: anything the records above do not name. The report is a closed one-way hand-over, so a
  question this task cannot answer is settled here rather than asked

**Inputs**
- the two records above, each with its command, its version and its own proposed fix
- [T-299](T-299-triage-the-nextep-adopter-report.md) section 3

**Acceptance criteria**
- [ ] records `03` and `15` are each closed with the remedy measured, or deferred with the reason
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
| 2026-09-13 | -> proposed | Raised by T-299 from Nextep records `03` and `15`. `PH1`: an adopter met both in the published `0.7.0`. `15` arrived as `friction` and is ruled a defect, because the tool reports a deck up to date when it is not. |
