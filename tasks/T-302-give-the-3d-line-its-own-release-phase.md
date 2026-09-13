---
id: T-302
title: Give the 3D line its own release phase, so the 1.0.0 backlog can be empty while T-057 stays open
type: admin
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-057]
work_package: PH3
owner: the project owner
business_value: high
effort: s
created: 2026-09-13
updated: 2026-09-13
deliverables: []
---

# T-302 - Give the 3D line its own release phase, so the 1.0.0 backlog can be empty while T-057 stays open

## 1. Specify

**Outcome**
The board separates what 1.0.0 needs from the 3D line the owner scheduled for 1.1.0, so *the backlog
is empty* is answered by a query rather than by judgement. [T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md)
stays open as the first task of that line and is not counted against 1.0.0.

**Where it came from**
The owner, 2026-09-13: 1.0.0 ships with the community marketplace submission once the backlog is
empty, and it is not to wait for 3D. 3D is 1.1.0, and needs thorough testing, more examples, fixes,
and features that use a 3D library; T-057 is only its beginning. Today T-057 sits in `PH3` beside the
1.0.0 work, and `CLAUDE.md` names three phases.

**Scope**
- In: a phase value for the 3D line in `.taskmd/config.md`'s vocabulary and the task template's menu
- In: `docs/RELEASE-PHASES.md`, and the sentences in `CLAUDE.md` and `tasks/TASK-WORKFLOW.md`
  section 3 that enumerate the phases
- In: moving T-057 into the new phase
- Out: raising the rest of the 1.1.0 work. Those tasks are raised when that line starts
- Out: `shipped_in`, which stays a version and is set at close

**Inputs**
- `docs/RELEASE-PHASES.md`, `.taskmd/config.md`, `tasks/_task-template.md`

**Acceptance criteria**
- [ ] `python tools/tasks/query.py list --open --work_package PH3` lists no 3D task, and the new phase
      lists T-057
- [ ] every document that enumerates the phases names the new one; if `CLAUDE.md` changes size, its
      measured pair is re-measured in the same edit
- [ ] `python tools/tasks/lint.py` green

**Open questions**
- The mechanism - the owner. Recommended: a fourth phase, `PH4`, because this repository already groups
  work by release phase and a phase is what the index divides on. The alternative, a log note on
  T-057, leaves every open-task query counting it toward 1.0.0.
  **Answered by the owner 2026-09-13: `PH4`.**

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision - rationale - date>

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
| 2026-09-13 | -> proposed | Raised on the owner's direction of the same day: 3D is 1.1.0 and must not hold 1.0.0. `PH3`, since it is neither a published defect nor `l`. |
| 2026-09-13 | (no change) | The owner chose `PH4`. Still `proposed`. |
