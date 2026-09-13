---
id: T-301
title: Decide whether task, register, lesson and handoff records get shorter, since writing them is a quarter of a session's spend
type: decision
status: proposed
phase: specify
parent: T-287
blocked_by: []
related: [T-290]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
finding: CE-22
created: 2026-09-13
updated: 2026-09-13
deliverables: []
---

# T-301 — Decide whether task, register, lesson and handoff records get shorter, since writing them is a quarter of a session's spend

## 1. Specify

**Outcome**
Each record form `CE-22` measured has a decided budget, or the owner declines one and the reason is
written where the next session writing that form meets it. The forms are a task's implement
section, a register row, a lesson and a handoff.

**Where it came from**
[`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.3, `CE-22`. An output token weighs five
input tokens. By its fourteenth call the audit session had written 22,020 of them, 25% of its
weighted spend, and the record forms were what it wrote. The next session reads each of them again.
The audit proposed no change, because the forms are settled policy. The owner ruled on 2026-09-13
that it becomes a decision.

**Scope**
- In: one decision per form, from four levers: a length limit, a shape change, the resume-side lever
  alone (a session reads the section a pointer names, not the whole file), or no change
- In: writing each decision into the document a session already reads when it writes that form
- Out: shortening existing records. A decision binds new writing; a closed record keeps what it says
- Out: the session rhythm, which is [T-290](T-290-measure-one-batch-run-as-one-session-against-the-session-per-task-rhythm.md)'s

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.3 `CE-22`, and §11 for the instrument

**Acceptance criteria**
- [ ] each of the four forms has a decision and its reason
- [ ] each adopted limit or shape is measured on one real record first: bytes before and after, and
      whether any fact lost its only home, which is `CE-22`'s stated risk
- [ ] each decision is written where a session writing that form reads it
- [ ] `python tools/tasks/lint.py` green

**Open questions**
- Which lever for each form. The owner decides, because `CE-22`'s controller is policy. The
  recommendation comes with the measurement.

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
| 2026-09-13 | → proposed | Raised from `CE-22` on the owner's ruling of the same day. The audit had reported it with no task because it collides with settled record policy. Child of [T-287](T-287-audit-what-a-session-pays-per-turn-and-why-it-grows.md). `PH3`. |
