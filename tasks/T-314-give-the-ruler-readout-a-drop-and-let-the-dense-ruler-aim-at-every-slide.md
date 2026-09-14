---
id: T-314
title: Give the ruler readout a drop, and let the dense ruler aim at every slide
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-307]
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-09-14
updated: 2026-09-14
deliverables: []
---

# T-314 — Give the ruler readout a drop, and let the dense ruler aim at every slide

## 1. Specify

**Outcome**
The slide number over a ruler mark sits in an upside-down drop whose point is on the mark and whose
round end holds the number. Past the dense bound, the small marks can be aimed at: the strip reads the
pointer as an analogue control, the drop shows the nearest slide's number, and a press goes there.

**Ruled by the owner** at [`OWED-LOOKS.md`](../docs/OWED-LOOKS.md) row 14, 2026-09-14. That ruling
reopens Nextep adopter record
[`16`](../docs/adopter-reports/nextep/2026-09-08-the-condensed-ruler-drops-the-small-dots-as-targets.md),
which [T-307](T-307-give-the-chrome-first-and-last-page-controls-and-a-ruler-whose-marks-a-reader-can-aim-at.md)
deferred because a dense mark is an 8 du cell and DS-168 is `hard`.

**Scope**
- In: the drop shape, in both ruler modes
- In: the dense strip as one analogue control, without making an 8 du cell a target under DS-168
- In: DS-217 and the component contract, amended to say what the ruler does
- In: a 25-slide splice the owner can open, named in the owed look
- Out: the undegraded ruler's targets, which T-307 settled

**Acceptance criteria**
- [ ] measured in Chrome on 13 and 25 slides: the drop's point sits on the mark, and on the dense
      strip a pointer over a small mark shows that slide's number and a press goes to it
- [ ] DS-168's target count does not change
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None: the owner ruled the behaviour.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |

## 3. Implement

**Decisions & assumptions**
- <what was decided>: <why, in one sentence>. <Reversible | Not reversible>. — YYYY-MM-DD

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
| 2026-09-14 | -> proposed | Raised from the owner's look at row 14, which asks for the drop and for the dense strip to aim. `PH3`: new behaviour. Batched into B28 first by the owner's ruling. |
