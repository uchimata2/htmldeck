---
id: T-054
title: Record which clauses of a rule the gate decides, not only which rules it reaches
type: fix
status: proposed
phase: specify
parent: T-053
blocked_by: []
related: [T-037, T-043, T-051, T-005]
work_package: none
owner: the project owner
created: 2026-08-09
updated: 2026-08-09
deliverables: []
---

# T-054 — Record which clauses of a rule the gate decides, not only which rules it reaches

## 1. Specify

**Outcome**
The coverage account can say that a rule is **partly** decided, and where the rest of it went. A
clause no check reaches is recorded the way an unreached *rule* already is — with a reason and what
would close it — instead of disappearing inside a rule the account reports as `checked`.

**Why this one**
The account is per rule, and several rules are conjunctions. DS-091 is the case that exposed it:

> Per slide: one headline ≤ 6 words plus ≤ 3 supporting fragments.

Three clauses. [T-053](T-053-enforce-the-headline-ds-091-requires.md) closed the first and the
second is long-standing; **the third cannot be reached and the account still counts DS-091 as
`checked`**, because one satisfied row is enough to move a rule into that bucket. The excusal for
the fragment clause is a comment in `audit.py` — the one place `check.py`'s own rule says an excusal
must not live, since `DEFERRED` is keyed by rule and cannot express *clause 3 of DS-091*.

**This is L-43's shape one level down.** T-037 recorded which *rules* no check can reach; the same
argument applies to clauses, and the device that guarantees rule-level coverage is what stops the
clause-level question being asked. `render_verdicts`' docstring already sanctions partial checks —
*"a row deciding one clause of its rule is a partial check and belongs here"* — so the design admits
them and nothing counts them.

**How many there are is not known, and finding out is most of the task.** DS-091 is one. DS-092
(*sentence under 20 words · paragraph 3–4 sentences · table cell one line*) is a likely second — the
cell clause is not measured. DS-100 and DS-105 are candidates.

**Scope**
- In: a sweep for `hard` rules whose text is a conjunction, and which clauses each gate decides.
- In: somewhere for a clause-level excusal to live, that `check.py` can report and a self-test can
  hold to the same standard as `DEFERRED` — a reason, and what would close it.
- Out: building the missing checks. This task makes the hole visible; closing each is its own work.
- Out: rewriting rules into one clause each. Splitting DS-091 into three IDs is a ruleset change
  with a renumbering cost, and it is the owner's call, not a consequence of this task.

**Inputs**
- [`tools/deck/check.py`](../tools/deck/check.py) — `DEFERRED`, `account()`
- [`tools/deck/audit.py`](../tools/deck/audit.py) — the DS-091 rows and their excusal comment
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §3.3
- [`docs/LESSONS.md`](../docs/LESSONS.md) — **L-43**, **L-36**
- [T-037](T-037-record-in-the-ruleset-which-rules-no-check-can-reach.md) — the same move at rule level

**Acceptance criteria**
- [ ] Every `hard` rule with more than one checkable clause is listed, with which clauses are decided
- [ ] A clause no check reaches is excused where `check.py` reports it, not only in a code comment
- [ ] The run says how many rules are partly decided, so the number cannot sit at zero unnoticed
- [ ] The reference deck's account still partitions

**Open questions**
- none yet — the sweep decides the shape.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <path>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-09 | → proposed | Raised by [T-053](T-053-enforce-the-headline-ds-091-requires.md), which could close two of DS-091's three clauses and had nowhere to record the third except a comment. Deliberately not absorbed there: DS-091 is one instance and the question is general, which is the mistake the same file made three times before [T-051](T-051-a-check-with-no-subject-must-not-report-a-pass.md). |
