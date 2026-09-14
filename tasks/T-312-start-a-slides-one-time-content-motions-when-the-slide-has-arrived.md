---
id: T-312
title: Start a slide's one-time content motions when the slide has arrived
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-268, T-304]
work_package: PH1
owner: the project owner
business_value: medium
effort: s
created: 2026-09-14
updated: 2026-09-14
deliverables: []
---

# T-312 — Start a slide's one-time content motions when the slide has arrived

## 1. Specify

**Outcome**
A one-time content motion plays after its slide has arrived, not under the page crossfade. Today
`.pulse`, `.arrow-pop marker path` and `.dot-pop circle` carry no slide state in `shell/components.css`,
so they start with the transition and are almost over when the reader can see them. `.turn` is gated
on `data-arrived` and reads correctly, which is DS-146's rule for an entrance.

**Found by** the owner's look at [`OWED-LOOKS.md`](../docs/OWED-LOOKS.md) row 13, 2026-09-14: slide 3's
pulse and slide 9's arrowheads on the reference deck were barely visible; slide 12's turn was right.
Continuous motions, such as the dashed flow, need no change.

**Scope**
- In: gate the three one-time content motions on `data-arrived`, with no flash of their end state
  during the crossfade
- In: every context that settles them: motion off, reduced motion, print, the reading view, the
  degraded state
- Out: `.rise`, which is an affordance entrance on `data-played` and was not reported

**Acceptance criteria**
- [ ] measured in Chrome: before arrival each motion has not started, and after arrival it plays,
      in both directions of the change (**L-125**)
- [ ] the look is recorded as owed on the slides that showed it
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None.

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
| 2026-09-14 | -> proposed | Raised from the owner's look at row 13. `PH1`: the published shell plays a one-time motion under the transition DS-146 says an entrance waits for. Batched into B28 first by the owner's ruling. |
