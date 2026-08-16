---
id: T-170
title: The reference deck states four evaluation dates no source carries
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-169]
work_package: PH1
owner: the project owner
business_value: high
effort: s
created: 2026-08-16
updated: 2026-08-16
deliverables:
  - examples/sources/programme-timetable.md
---

# T-170 — The reference deck states four evaluation dates no source carries

## 1. Specify

**Outcome**
`python tools/deck/check.py examples/reference-deck.html examples/sources` reports `FIG-1` pass
again, because the four dates the deck states are either in a source or off the slides — decided as
a content question and not by loosening the gate.

**What was found.** [T-169](T-169-the-figure-binder-cannot-bind-a-value-split-across-table-cells.md)
taught the ledger to read a time word before its numeral. The reference deck gained eleven figures
of kind `month`; seven bind to `programme-timetable.md` and **four appear in no source**:

| Figure | Slide | The run |
| :--- | :--- | :--- |
| `months 13` | Month eighteen stays reversible | Boardings on the six trunk routes, months 13 to 18 |
| `month-9` | Month eighteen stays reversible | Service holds at month-9 levels |
| `month 12` | Three things would change this | Measured month 12 · by the annual household survey |
| `month 12` | Three things would change this | Measured month 12 · by the city auditor |

**The sources say none of it.** `examples/sources` states a gate at month 18, 14 months to first
benefit for bike-share and 4 months for bus frequency. There is no month 9, no month 12, and no
measurement window. The deck's evaluation plan invented its own timetable.

**This is FIG-1 doing its job, on the deck this repository ships to demonstrate it.** The figures
were unreadable before T-169, so the row was green on a check that could not see them — the same
shape as **L-105**, one layer along. It is not collateral damage from T-169 and must not be fixed by
narrowing the binder.

**Scope**
- In: decide, per figure, whether the **source** is incomplete or the **deck copy** is unsupported.
- In: whichever of the two is wrong, correct it — and rebuild the deck if it is the deck.
- Out: changing `FIG-1`, `FIGURE` or the binder. T-169 owns those and they are not at fault here.
- Out: `examples/reference-deck-seeded-defects.html`, which is derived from the reference deck by
  `seed_defects.py` and follows it.

**The decision this needs, and why it is not mine to take alone.** Adding the dates to
`programme-timetable.md` turns the gate green in one edit — and *making the source say what the
slide says* is precisely the move FIG-1 exists to catch. It is right only if a real programme
timetable would carry an evaluation schedule, which is a judgement about the fixture's content.
The alternative is to cut the unsupported dates from the deck copy, which costs a rebuild.

**Acceptance criteria**
- [ ] Each of the four figures has a recorded verdict: source incomplete, or deck copy unsupported
- [ ] `FIG-1` passes on `examples/reference-deck.html` with no change to `content.py`
- [ ] `examples/reference-deck-seeded-defects.html` still derives from the deck — `seed_defects.py --check`
- [ ] No other row on any shipped deck moves

**Open questions**
- Is the fixture's source corpus meant to carry an evaluation timetable — the project owner.

## 2. Plan

_Not planned._

## 3. Implement

_Not started._

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-16 | → proposed | Raised out of [T-169](T-169-the-figure-binder-cannot-bind-a-value-split-across-table-cells.md)'s review, which recorded *no shipped deck moves* as **not met** against exactly these four figures. The gate is red on the reference deck from that commit until this closes. |
