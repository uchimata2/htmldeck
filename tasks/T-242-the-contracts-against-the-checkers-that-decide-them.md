---
id: T-242
title: Reconcile the component and theme contracts with what their checkers read
type: fix
status: proposed
phase: specify
parent: T-219
blocked_by: []
related: []
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-08-29
updated: 2026-08-29
deliverables: []
---

# T-242 — Reconcile the component and theme contracts with what their checkers read

## 1. Specify

**Outcome**
A contract row states what a checker decides. Today section 2.1 states a check for two of its four sources; the motion-rule table has no completeness half and two rules animate with no row in it; two theme-contract motion tokens are read by nothing tracked and a third names a rule that does not govern it; section 3.2 calls `data-stage` back the one value outside the argument where a second now exists; and `--accent-ink` is four hand-chosen colours across two themes with nothing deriving them.

**Closes** `PR-34`, `PR-35`, `PR-36`, `PR-39`, `PR-77` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: `COMPONENT-CONTRACT.md` sections 2.1, 3.2 and 3.8, `THEME-CONTRACT.md` section 3.6 and its `--accent-ink` row, `tools/deck/component.py`, and the two theme files
- In: **nothing else** - every finding this task closes is named above, and each statement stays in the register rather than being restated here (the method's umbrella condition 2)
- Out: any finding not in the list above
- Out: committing to a remedy before measuring it. A remedy is a hypothesis (the method's section 5); a fix that the measurement refuses is reported here and its finding stays open

**Inputs**
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3 - the rows for `PR-34`, `PR-35`, `PR-36`, `PR-39`, `PR-77`
- `motion_gaps` in [`tools/deck/component.py`](../tools/deck/component.py)
- [T-200](T-200-add-a-lobby-slide-and-count-the-argument-not-the-file.md), which added the second stage value section 3.2 has not caught up with

**Acceptance criteria**
- [ ] every finding above is **closed with its remedy measured**, or explicitly deferred with the reason recorded on its register row - the method's obligation for `Med`
- [ ] each register row's `Task` cell names this task and its `Status` cell says what happened
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None yet. The register's `Remedy` column carries a hypothesis for each finding, and the method's
  section 5 says it is a hypothesis: whoever implements this measures before committing to it, and
  records what the measurement said.

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
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`Med`**, grouped: the owner ruled on 2026-08-29 that a severity obliges a disposition before the release rather than a file count, on the precedent that the method already accepts many findings to one task at `Low`. Every finding keeps its id and its statement in the register. |
