---
id: T-238
title: Fix the board header that routes work into a shipped phase, and two silent closures
type: fix
status: proposed
phase: specify
parent: T-219
blocked_by: []
related: []
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-29
updated: 2026-08-29
deliverables: []
---

# T-238 — Fix the board header that routes work into a shipped phase, and two silent closures

## 1. Specify

**Outcome**
The tracker's own documents agree with `CLAUDE.md`'s phase rule and with themselves. Today the board's hand-written header routes a new task into a shipped phase; the opening checklist's first step names a command an agent cannot run and the substitute refuses it; and [T-221](T-221-answer-the-three-defects-taskmd-0-6-0s-wider-check-set-found.md) and [T-222](T-222-derive-the-reconcile-sweeps-membership-instead-of-enumerating-it.md) are `done` with `shipped_in` **absent** - the third recurrence of a defect written down twice, which nothing gates because the field is deliberately outside the schema's vocabularies.

**Closes** `PR-19`, `PR-20`, `PR-27` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: `tasks/README.md`'s hand-written header, `TASK-WORKFLOW.md` sections 1 and 7, `tools/tasks/query.py`, and the two task records
- In: **nothing else** - every finding this task closes is named above, and each statement stays in the register rather than being restated here (the method's umbrella condition 2)
- Out: any finding not in the list above
- Out: committing to a remedy before measuring it. A remedy is a hypothesis (the method's section 5); a fix that the measurement refuses is reported here and its finding stays open

**Inputs**
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3 - the rows for `PR-19`, `PR-20`, `PR-27`
- `CLAUDE.md`'s phase rule, which the header contradicts
- [T-187](T-187-open-the-motion-vocabulary-into-a-style-guide.md)'s log, which records this same correction being made once already

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
