---
id: T-051
title: A check whose subject is absent must not report a pass
type: fix
status: proposed
phase: specify
parent: T-044
blocked_by: []
related: [T-005, T-038, T-043]
work_package: none
owner: the project owner
created: 2026-08-09
updated: 2026-08-09
deliverables: []
---

# T-051 — A check whose subject is absent must not report a pass

## 1. Specify

**Outcome**
No verdict in `tools/deck/` reports `pass` for a rule whose subject the deck does not contain. A
check that finds nothing to judge reports that it found nothing, and the run treats it the way it
treats any other rule nothing decided.

**Why this one**
Found by [T-044](T-044-restore-the-seeded-defect-fixture-and-its-claims.md) while re-measuring the
seeded fixture, in the one place it could be found — a deck deliberately missing something:

```
good deck     DS-140  `Current` renders dashed: 7px, 6px            pass
seeded deck   DS-140  `Current` renders dashed: no dashed flow      pass
```

The S3 seed replaces the deck's only dashed flow with a card row, so DS-140's subject stops
existing — and `data.get("currentDasharray") != "none"` is `True` for `None`, so the rule passes on
its own absence.

**This is L-36 inside the instrument**, and the repository already treats the pattern as a defect
everywhere else: `check.py` excuses DS-087 in writing precisely because *"no deck in the repository
has an appendix, so the check would have no subject to run against and would pass on nothing"*, and
[T-038](T-038-the-gate-emits-verdicts-for-judge-rules-and-one-wrong-id.md) fixed exactly this shape
for DS-130, which landed on a slide with no disclosure control, reported `null`, and passed. So the
question is not whether DS-140 should be fixed but **why the same fault keeps being found one
instance at a time** — three now — when the gate is otherwise built around the principle that a
rule nothing decided fails the run.

**Scope**
- In: an audit of every verdict in `tools/deck/` for the same shape — a truthy-by-absence
  comparison, a `.get()` defaulting to something that passes, a filter over an empty list.
- In: deciding what a subjectless check reports. It is **not** obviously a failure: a deck with no
  flows is legitimate, and DS-140 does not require one. The candidate is a third state the account
  already has room for — the rule is *not decided by this run*, which is what `SILENT` means.
- In: whatever prevents the fourth instance, which is the point of the task.
- Out: adding subjects to the reference deck so the checks have something to bite on. That
  reverses the dependency — the instrument would be shaping the artifact.
- Out: `judge` rules, which no check decides by definition.

**Inputs**
- [`tools/deck/audit.py`](../tools/deck/audit.py) — `render_verdicts()`, and the DS-130 comment
  recording the same fault
- [`tools/deck/check.py`](../tools/deck/check.py) — the account, and DS-087's excusal wording
- [`docs/LESSONS.md`](../docs/LESSONS.md) — **L-36**
- [T-044](T-044-restore-the-seeded-defect-fixture-and-its-claims.md) §4 — where this was found

**Acceptance criteria**
- [ ] Every verdict that can be reached with its subject absent is identified, and the list is in
      the task rather than only in the fix
- [ ] A deck with no dashed flow does not produce a DS-140 `pass`
- [ ] Whatever the subjectless state is, the coverage account still partitions
- [ ] Demonstrated against the seeded fixture, which is the deck that exposed it (**L-04**)
- [ ] Something makes the fourth instance loud rather than requiring another audit to find it

**Open questions**
- none — the reporting question above is the implementer's, decided from what `SILENT` already
  means in the account.

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
| 2026-08-09 | → proposed | Raised by [T-044](T-044-restore-the-seeded-defect-fixture-and-its-claims.md), which found it by running the gate over a deck built to be missing things — the only kind of deck that can expose it. DS-140 passes on a deck with no dashed flow because `None != "none"`. **The reason this is worth its own task rather than a one-line fix is that it is the third instance**: DS-130 was the same fault and was fixed in place by T-038, DS-087 is excused in `check.py` for exactly this reason, and nothing generalised either. The gate's whole design is that a rule nothing decided fails the run; a rule decided *vacuously* is the same claim wearing a pass. |
