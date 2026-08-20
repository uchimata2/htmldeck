---
id: T-190
title: critique.py reports a NO SUBJECT rule as a gate failure the reviewer must cite
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-051]
work_package: PH1
shipped_in: unreleased
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
| 1 | Split the three-state verdict properly | `critique.py` line 143 |
| 2 | Decide what a NO SUBJECT row prints | a third list |
| 3 | Fixture it, seeded failing first | `self_test` |

## 3. Implement

**Decisions & assumptions**
- **NO SUBJECT is printed, in its own list, not silenced** - 2026-08-20. Silence hands the reviewer the same wrong picture one direction over: a rule the gate could not judge is not a rule it cleared, and which rules had no subject is exactly what a reviewer needs before deciding what the review must cover itself.
- **The fixture passed against the restored bug on its first version.** The row prints as `FAIL  DS-140`, two spaces, and the assertion looked for five. Caught only by putting the defect back and running (**L-04**); the corrected assertion is watched failing.

**Outputs produced**
- `tools/deck/critique.py`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| critique and check agree about DS-140 on the adopter deck | **pass** | `DS-140` now appears under *WHAT THE GATE COULD NOT JUDGE*, and the gate passes the deck |
| A fixture holds a NO SUBJECT row and is watched failing first | **pass** | 13 of 14 with the bug restored, 14 of 14 fixed |
| Every other three-state read is swept | **pass** | `not r.get("ok")` over a verdict row appears nowhere else in the repository |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-20 | -> proposed | Created. |
| 2026-08-20 | -> in_progress | One line, and a fixture that took two attempts. |
| 2026-08-20 | -> done | Three criteria met. |
