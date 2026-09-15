---
id: T-317
title: Fill the ruler readout's drop in the softer ink
type: deliverable
status: done
phase: review
parent: null
blocked_by: []
related: [T-314]
work_package: PH3
shipped_in: 1.0.0
owner: the project owner
business_value: low
effort: s
created: 2026-09-14
updated: 2026-09-14
deliverables: [shell/components.css]
---

# T-317 — Fill the ruler readout's drop in the softer ink

## 1. Specify

**Outcome**
The drop over a ruler mark is filled in the theme's dark warm brown with the number in the cream
ground colour, where it was filled in `--ink`.

**Ruled by the owner** at [`OWED-LOOKS.md`](../docs/OWED-LOOKS.md) row 20, 2026-09-14: the drop reads
well, and black is too much contrast, so dark coffee with the cream colour. The owner asked for the
change without a full rebuild, and for a test that it works.

**Scope**
- In: the drop's fill
- Out: the drop's shape and placement, which [T-314](T-314-give-the-ruler-readout-a-drop-and-let-the-dense-ruler-aim-at-every-slide.md) settled
- Out: the pager's fill, which the owner did not name

**Acceptance criteria**
- [x] on the synced reference deck, a hovered mark shows the drop in `--ink-soft` with a `--paper` number
- [x] `python tools/deck/check.py examples/reference-deck.html` and `python tools/tasks/lint.py` green

**Open questions**
- None.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Fill the drop in `--ink-soft` | `shell/components.css` |
| 2 | Sync, check the rendered drop, record the look, lint | §3 |

## 3. Implement

**Decisions & assumptions**
- The fill is `--ink-soft`, an existing token: `#5F594E` in `quarto`'s light band and `#ADA69A` in
  its dark band. A new theme token would pay the theme contract in both themes for one value that an
  existing token already carries per theme. Reversible. — 2026-09-14
- The number stays `--paper`. By the WCAG formula the pair is 6.1:1 in the light band and 7.1:1 in
  the dark band. Reversible. — 2026-09-14
- The full gate is not run for this task, by the owner's instruction. B28's gate before its pull
  request covers it. Reversible. — 2026-09-14

In the in-app browser at 1026x1258, on the synced reference deck: a real hover on mark 4 showed the
drop with the text `4`, the fill computed `rgb(95, 89, 78)` and the number `rgb(243, 240, 232)`.

§1.14 after the shell edit: four decks synced, the fixture regenerated, `density.py check` `0 wrong`
on each, and `README.md`'s `sort-window` figure corrected from 330 KB to 331 KB.

**The look is owed**: [`../docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md) row 23.

**Outputs produced**
- `shell/components.css`: the drop's fill

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| a hovered mark shows the drop in `--ink-soft` with a `--paper` number | **pass**, look owed | §3. The look is `OWED-LOOKS.md` row 23 |
| `check.py` on the reference deck and `lint.py` green | **pass** | `122 owned`, `0 failing` |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-14 | -> done | The drop is filled in `--ink-soft` under a `--paper` number. The look is owed as `OWED-LOOKS.md` row 23. |
| 2026-09-14 | -> proposed | Raised from the owner's look at row 20. `PH3`: a change to shipped styling, not a defect. Joined B28 by the owner's instruction in the same session. |
