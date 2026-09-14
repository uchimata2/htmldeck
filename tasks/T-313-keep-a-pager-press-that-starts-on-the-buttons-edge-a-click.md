---
id: T-313
title: Keep a pager press that starts on the button's edge a click
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-307, T-199]
work_package: PH1
shipped_in: unreleased
owner: the project owner
business_value: medium
effort: s
created: 2026-09-14
updated: 2026-09-14
deliverables: [shell/components.css]
---

# T-313 — Keep a pager press that starts on the button's edge a click

## 1. Specify

**Outcome**
A press anywhere on a pager button pages. Today a press that starts near the button's edge animates
and does not page. The hypothesis is the pinch: `.btn.btn--pager:active` scales the button to
`--pager-pinch` while it is held, so the release lands outside the shrunken box and the browser fires
no click.

**Found by** the owner's look at [`OWED-LOOKS.md`](../docs/OWED-LOOKS.md) row 14, 2026-09-14, on all
four pager buttons.

**Scope**
- In: measure the mechanism, then keep the press a click without removing the pinch
- Out: the pinch's look and its tokens

**Acceptance criteria**
- [x] measured in Chrome: a point just inside the edge falls outside the pinched button before the
      change and inside it after (**L-125**)
- [x] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Measure where a point inside the edge lands on a pinched button | §3 |
| 2 | Give the pager a hit margin that survives the pinch | `shell/components.css` |
| 3 | Sync, measure again, record the look, lint, gate | §3 |

## 3. Implement

**Decisions & assumptions**
- The hypothesis holds: the pinch is the mechanism. A click needs the press and the release on the
  same element, and a release on the edge of a shrunken button lands on the box around it.
  Reversible. — 2026-09-14
- Each pager button carries an invisible `::after` reaching `--sp-1` past its edge. A pseudo-element
  is part of its element for hit-testing and shrinks with it, and 8 units covers the pinch's 6% of
  the widest pager button, 66 units, several times over. Two neighbours' margins meet in the
  16-unit gap between them without overlapping. Reversible. — 2026-09-14
- Rejected: dropping the pinch, which is the press acknowledgement the owner asked for in T-199.
  Rejected: moving the transform onto the button's children, which restyles the filled surface and
  changes what the contrast check reads. Rejected: paging on `pointerdown`, which pages before the
  release and splits the pointer's route from the keyboard's. Reversible. — 2026-09-14

On the reference deck in headless Chrome, each pager button scaled to `.94` as `:active` does, and a
point 1.5 px inside its right edge:

| Button | Before | After |
| :--- | :--- | :--- |
| `#first` | the navbox `DIV` | `#first` |
| `#prev` | the navbox `DIV` | `#prev` |
| `#next` | the navbox `DIV` | `#next` |
| `#last` | the navbox `DIV` | `#last` |

§1.14 after the shell edit: four decks synced, the fixture regenerated, `density.py check` `0 wrong`
on each, and the size figures corrected.

**The look is owed**: [`../docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md) row 18.

**Outputs produced**
- `shell/components.css`: the pager's hit margin

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| a point inside the edge falls outside the pinched button before and inside after | **pass** | §3's table |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | **pass** | Lint, then the full gate on the finished tree |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-14 | - | The owner's look at row 18: an edge press still animates and does not page. Not reproduced here: in the in-app browser, real clicks 1 px inside `#next`'s right and top edges, one of them held, each paged, and every edge of all four buttons hit-tests as the button at rest, pinched and tilted. Dropped by the owner's ruling as not critical. |
| 2026-09-14 | -> done | The pinch was the mechanism, measured on all four buttons. An invisible hit margin keeps the press a click. The look is owed as `OWED-LOOKS.md` row 18. |
| 2026-09-14 | -> proposed | Raised from the owner's look at row 14. `PH1`: the published pager animates a press and does not page. Batched into B28 first by the owner's ruling. |
