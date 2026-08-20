---
id: T-190
title: critique.py reports a NO SUBJECT rule as a gate failure the reviewer must cite
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-051]
work_package: PH1
owner: the project owner
business_value: high
effort: s
created: 2026-08-20
updated: 2026-08-20
deliverables: []
---

# T-190 - critique.py reports a NO SUBJECT rule as a gate failure the reviewer must cite

## 1. Specify

**Outcome**
`critique.py` reports what the gate decided, not the opposite of it. Today a rule the gate could not
judge is printed as `FAIL`, under a heading that instructs the reviewer to cite it.

**The defect**
[`../tools/deck/critique.py`](../tools/deck/critique.py) line 143:

    failing = [r for r in rows if not r.get("ok")]

A verdict row carries three states, and `check.py` knows it -
[`../tools/deck/check.py`](../tools/deck/check.py) line 870 reads
`"NO SUBJECT" if row["ok"] is None else "pass" if row["ok"] else "FAIL"`. `critique.py` tests
falsiness, so `None` joins the failing list. It then prints those rows under **WHAT THE GATE ALREADY
DECIDED - cite these, do not re-find them**.

**Reproduced 2026-08-20** on a 16-slide deck built by an outside adopter. `check.py` prints
`DS-140  `Current` renders dashed: no dashed flow in this deck    NO SUBJECT` and passes the deck
with `0 failing`. `critique.py`, on the same file in the same minute, prints
`FAIL  DS-140   `Current` renders dashed: no dashed flow in this deck`.

So the review pass tells a reviewer to cite a failure that does not exist, on a deck the gate passed.
The reviewer either fixes a non-problem or learns to distrust the section.

**This is T-051's fault reflected.** T-051 was absence read as conformance; this is absence read as
failure. Both come from a two-state test over a three-state verdict.
[`../tools/deck/spec.py`](../tools/deck/spec.py) records a third instance of the same family in its
own header.

**Scope**
- In: the failing filter in `critique.py`, and any other `not r.get("ok")` over a verdict row.
- In: what the spine prints for a `NO SUBJECT` row - silence, or a third list. Argued, not assumed.
- In: a self-test fixture that drives a `None` row through the spine and asserts it is not called a
  failure.
- Out: `check.py`, which is already right.

**Acceptance criteria**
- [ ] On the adopter deck above, `critique.py` and `check.py` agree about DS-140.
- [ ] A fixture holds a `NO SUBJECT` row to whatever the spine decides to print, and it is watched
      failing before it is watched passing.
- [ ] Every other three-state verdict read in this repository is swept for the same test, and the
      sweep result is recorded even where it is clean.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision - rationale - date>

**Outputs produced**
- <path>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-20 | -> proposed | Created. |
