---
id: T-312
title: Start a slide's one-time content motions when the slide has arrived
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-268, T-304]
work_package: PH1
shipped_in: 1.0.0
owner: the project owner
business_value: medium
effort: s
created: 2026-09-14
updated: 2026-09-14
deliverables: [shell/components.css]
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
- [x] measured in Chrome: before arrival each motion has not started, and after arrival it plays,
      in both directions of the change (**L-125**)
- [x] the look is recorded as owed on the slides that showed it
- [x] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Measure the three motions' state before the slide has arrived | §3 |
| 2 | Hold each on its first frame until `data-arrived`, and settle it where a slide never arrives | `shell/components.css` |
| 3 | Sync, measure again, record the look, lint, gate | §3 |

## 3. Implement

**Decisions & assumptions**
- Each one-time content motion keeps its rule and is held with `animation-play-state:paused`, and
  `.slide[data-arrived]` sets it running. A held motion rests on its first frame, which is scale 1
  for the pulse and scale 0 for the arrowheads and dots, so nothing flashes during the crossfade,
  and its delay counts from arrival. Reversible. — 2026-09-14
- Rejected: moving each motion under `.slide[data-arrived]` as `.turn` is. The contract's motion
  table and the motion checks read one rule per motion by its selector, and a reveal gated that way
  shows its end state under the crossfade and then snaps to nothing. Rejected: a delay equal to the
  page transition, which copies `--slide-dur` into three rules and drifts when a theme changes it.
  Reversible. — 2026-09-14
- The reading view and the degraded state now settle the arrowheads and dots, because a copied or
  degraded slide never arrives. Motion off, reduced motion and print already settled all three.
  Reversible. — 2026-09-14

In headless Chrome on the reference deck, after paging to slide 3. The virtual clock does not advance
CSS animations, so the measurement is the play state, not elapsed time:

| Element | Before, not yet arrived | After, not yet arrived | After, `data-arrived` set |
| :--- | :--- | :--- | :--- |
| slide 3's `.pulse` | `running` | `paused`, over 1400 ms of samples | `running` |
| an arrowhead on a slide not yet reached | `running` | `paused` | `running` |

§1.14 after the shell edit: four decks synced, the fixture regenerated, `density.py check` `0 wrong`
on each, and the size figures corrected.

**The look is owed**: [`../docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md) row 19.

**Outputs produced**
- `shell/components.css`: the three held motions, the rule that releases them, and two settling rules

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| before arrival each motion has not started, and after arrival it plays | **pass** | §3's table, both directions |
| the look is recorded as owed | **pass**, look owed | `OWED-LOOKS.md` row 19 |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | **pass** | Lint, then the full gate on the finished tree |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-14 | -> done | The three one-time content motions are held on their first frame until the slide has arrived. Measured both ways by play state. The look is owed as `OWED-LOOKS.md` row 19. |
| 2026-09-14 | -> proposed | Raised from the owner's look at row 13. `PH1`: the published shell plays a one-time motion under the transition DS-146 says an entrance waits for. Batched into B28 first by the owner's ruling. |
