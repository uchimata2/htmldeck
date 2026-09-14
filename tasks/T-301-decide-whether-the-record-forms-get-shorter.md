---
id: T-301
title: Decide whether task, register, lesson and handoff records get shorter, since writing them is a quarter of a session's spend
type: decision
status: done
phase: review
parent: T-287
blocked_by: []
related: [T-290]
work_package: PH3
shipped_in: unreleased
owner: the project owner
business_value: medium
effort: s
finding: CE-22
created: 2026-09-13
updated: 2026-09-14
deliverables: [tasks/_task-template.md, docs/PRE-RELEASE-AUDIT.md, docs/LESSONS.md, .handoff/config.md]
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
  recommendation comes with the measurement. **Answered by the owner 2026-09-14**, in §3's ruling
  table.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Measure each form over its real records | the table in §3 |
| 2 | Find where a session writing each form reads its rules | the *written in* column |
| 3 | Put one question per form to the owner, with the measurement and a recommendation | the ruling |
| 4 | Measure each adopted limit or shape on one real record: bytes before and after, and any fact left with no home | a row per form |
| 5 | Write each decision where its writer reads it | the four homes |

## 3. Implement

**Measured 2026-09-14** over every record in the tree, UTF-8 bytes. The script read the files and
wrote nothing. Tasks are `status: done`, and *recent* means created on or after 2026-09-01.

| Form | Records | Median | p90 | Max | Written in, when a session writes one |
| :--- | ---: | ---: | ---: | ---: | :--- |
| Task §3 (implement) | 290 | 2,932 | 5,881 | 15,130 | [`_task-template.md`](_task-template.md) |
| Task §3, recent | 14 | 2,952 | 6,425 | 10,367 | the same. The recent whole file has a median of 8,330, and §4 1,136 and the log 921 of that |
| Register row, `PR-nn` | 143 | 2,439 | 3,365 | 5,732 | [`../docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) §3, where rows are written |
| Lesson | 164 | 2,347 | 3,404 | 4,426 | [`../docs/LESSONS.md`](../docs/LESSONS.md), *To add a lesson* |
| Lesson, L-150 and later | 15 | 2,239 | 3,342 | 3,561 | the same |
| Handoff, archived | 130 | 4,800 | 6,386 | 7,608 | the handoff skill, and [`../.handoff/config.md`](../.handoff/config.md) |

**The handoff has already moved.** The last six archived handoffs are 3,227, 2,444, 2,871, 2,394,
1,850 and 1,348 bytes, the last being B25's own. Wave 8's handoff points and does not store, which is
what the handoff skill's core §2 already required.

**Frequency differs by a wide margin.** A batch writes one to five task §3s, about one lesson, and one
handoff. It writes a register row only during an audit cycle, and no audit is scheduled before 1.0.0
([`../docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) wave 8).

**Ruled by the owner 2026-09-14**, each form on the recommendation put to them:

| Form | Lever | Reason | Written in |
| :--- | :--- | :--- | :--- |
| Task §3 | shape | one bullet per decision and measurements in a table, with no cap, so no reason is cut to fit | [`_task-template.md`](_task-template.md) §3 |
| Register row | no change for now | no audit runs before 1.0.0, so a limit could not be tested on a real cycle | [`../docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) §3 |
| Lesson | a 1,500-byte limit | a lesson is opened on every citation, and its evidence keeps its home in the task | [`../docs/LESSONS.md`](../docs/LESSONS.md), *To add a lesson* |
| Handoff | no change | the skill's core §2 already requires pointers, and wave 8 follows it | [`../.handoff/config.md`](../.handoff/config.md) |

**Each adopted form, tried on one real record in scratch.** The records themselves are unchanged, as
§1's scope says.

| Record | Before | After | Facts left with no home |
| :--- | ---: | ---: | :--- |
| [T-306](T-306-wire-an-icon-first-source-item-in-quickview-py-and-make-shell-py-sync-name-a-stale-chrome-tail.md) §3, shaped | 2,132 | 1,887 | none. Its decisions block fell from 1,009 to 764. Dropped: an analogy to `tokens --write`, and a narrative the evidence table's second row already shows |
| [L-164](../docs/lessons/L-164.md), limited | 2,438 | 1,062 | none. Every dropped detail (the twelve days, the inline array, the five-line partial read, taskmd's `T-169`) is in [T-295](T-295-complete-t-288s-observation-and-decide-the-move.md) §3, which the shorter lesson links |

**Decisions & assumptions**
- The register decision goes in `PRE-RELEASE-AUDIT.md` §3, not `AUDIT-METHOD.md`: the second is a term of `../CLAUDE.md`'s size bound, and growing it would falsify that file's debt figure. Reversible. — 2026-09-14
- The shape saves 11% of T-306's §3 and no more: that record was below the median and already close to the shape, and the owner chose shape over a cap to protect reasons, not for bytes. Not a reversal trigger. — 2026-09-14
- No gate enforces the lesson limit: it is written where a lesson writer reads it, and `lessons.py` can check L-165 and later if the rule is ignored. Reversible. — 2026-09-14

**Outputs produced**
- `tasks/_task-template.md` §3, `docs/PRE-RELEASE-AUDIT.md` §3, `docs/LESSONS.md` and `.handoff/config.md`
- `docs/CONTEXT-AUDIT.md`, where `CE-22` is closed

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| each of the four forms has a decision and its reason | met | §3's ruling table |
| each adopted limit or shape is measured on one real record first: bytes before and after, and whether any fact lost its only home | met | §3's trial table. Both trials ran before their home was edited, and neither left a fact without a home |
| each decision is written where a session writing that form reads it | met | the *Written in* column. The register's home moved from `AUDIT-METHOD.md` to the register itself, for the reason in §3 |
| `python tools/tasks/lint.py` green | met | run before the batch's full gate |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-13 | → proposed | Raised from `CE-22` on the owner's ruling of the same day. The audit had reported it with no task because it collides with settled record policy. Child of [T-287](T-287-audit-what-a-session-pays-per-turn-and-why-it-grows.md). `PH3`. |
| 2026-09-14 | → specified | B25. §1 was complete. Deliverables name the four homes a decision is written in, because a declined form still gets its reason there. |
| 2026-09-14 | → planned | §2 written: measure, find each form's home, survey, then measure an adopted form on one real record before writing it. |
| 2026-09-14 | → in_progress | Steps 1 and 2 done, with the table in §3. The handoff had already fallen from 3,227 to 1,348 bytes over wave 8's last six. Stopped at the owner's survey. |
| 2026-09-14 | → done | The owner took all four recommendations. Shape and limit were each tried on one real record first: T-306 §3 went from 2,132 to 1,887 bytes, and L-164 from 2,438 to 1,062. Each decision is written in its home, and `CE-22` is closed. |
