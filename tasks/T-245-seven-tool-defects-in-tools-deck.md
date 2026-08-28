---
id: T-245
title: Fix seven defects in the deck tools, each with its own seeded proof
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

# T-245 — Fix seven defects in the deck tools, each with its own seeded proof

## 1. Specify

**Outcome**
Seven tools behave as their own documents say. Today `theme.py swap`'s refusal path crashes instead of reporting and had never run; the diagram-placement gate measures one diagram per slide where a shipped deck has two; `shell.py` states its region count three ways and prints one of them; the browser search names five Windows paths, four Linux binaries and no macOS install; `rulerstrip.py` and `longdeck.py` build an exit code and throw it away; `quickview.py` escapes a title in three places and not in two; and `deck.js` dereferences `toDoc` and `motionBtn` unguarded.

**Closes** `PR-38`, `PR-42`, `PR-55`, `PR-56`, `PR-58`, `PR-59`, `PR-78` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: the seven sites the register names, one per finding
- In: **nothing else** - every finding this task closes is named above, and each statement stays in the register rather than being restated here (the method's umbrella condition 2)
- Out: any finding not in the list above
- Out: committing to a remedy before measuring it. A remedy is a hypothesis (the method's section 5); a fix that the measurement refuses is reported here and its finding stays open

**Inputs**
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3 - the rows for `PR-38`, `PR-42`, `PR-55`, `PR-56`, `PR-58`, `PR-59`, `PR-78`
- each finding's own evidence column, which carries the command that reproduces it

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
