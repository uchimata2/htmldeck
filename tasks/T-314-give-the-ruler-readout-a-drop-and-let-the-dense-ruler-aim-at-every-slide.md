---
id: T-314
title: Give the ruler readout a drop, and let the dense ruler aim at every slide
type: deliverable
status: done
phase: review
parent: null
blocked_by: []
related: [T-307]
work_package: PH3
shipped_in: unreleased
owner: the project owner
business_value: medium
effort: m
created: 2026-09-14
updated: 2026-09-14
deliverables: [shell/components.css, shell/deck.js, docs/DESIGN-SYSTEM.md, docs/COMPONENT-CONTRACT.md]
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
- [x] measured in Chrome on 13 and 25 slides: the drop's point sits on the mark, and on the dense
      strip a pointer over a small mark shows that slide's number and a press goes to it
- [x] DS-168's target count does not change
- [x] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None: the owner ruled the behaviour.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Measure the readout and the dense strip before the change | §3 |
| 2 | Draw the readout as a drop, and read the pointer against the dense strip | `shell/components.css`, `shell/deck.js` |
| 3 | Amend DS-217 and the contract | `docs/DESIGN-SYSTEM.md`, `docs/COMPONENT-CONTRACT.md` |
| 4 | Sync, splice 25 slides, measure both decks, record the look, lint, gate | §3 |

## 3. Implement

**Decisions & assumptions**
- The drop is the readout's own box with a `::before` square that has one sharp corner and is turned
  45 degrees, so the corner points down and the number stays upright. The box is raised 7 of its 34
  units above the mark's centre, which is where the turned corner lands. Reversible. — 2026-09-14
- The drop is `--ink` with the number in `--paper`, the pager's filled pair, so the one filled shape
  on the ruler reads as belonging to the controls beside it. Reversible. — 2026-09-14
- Past the bound the small marks stay disabled cells, and the strip reads the pointer: `mousemove`
  shows the nearest slide in the drop and the label, and a click goes there. A section tick keeps its
  own button. So no target under DS-168's floor is added, and record `16` is met without amending a
  `hard` rule. Reversible. — 2026-09-14
- Rejected: enabling the small marks as buttons, which is the change T-307 deferred, because an
  8 du cell fails DS-168's probe on every deck past the bound. Reversible. — 2026-09-14

In headless Chrome at 1920x1080, on the reference deck and on its 25-slide splice from
`python tools/deck/longdeck.py examples/reference-deck.html 25`:

| Deck | Mode | Drop over a section tick | A small mark | Enabled chrome buttons under 24 px |
| :--- | :--- | :--- | :--- | :--- |
| before, 13 slides | not dense | plain text 17.3 px above the mark's centre, no fill | a button; a press pages | 0 |
| after, 13 slides | not dense | 29.2 px drop, point 0.0 px from the mark's centre across and down, ink fill | a button; a press pages | 0 |
| after, 25 slides | dense | the same drop, point 0.0 px from the centre | hit-tests as its `LI`; the pointer shows `13`; a press goes to slide index 12, its own | 0 |

§1.14 after the shell edit: four decks synced, the fixture regenerated, `density.py check` `0 wrong`
on each, and the size figures corrected.

**Record `16` closed** by the owner's ruling and this change. **The look is owed**:
[`../docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md) row 20.

**Outputs produced**
- `shell/components.css`: the drop, and the strip's cursor
- `shell/deck.js`: `nearestTick`, and the strip's pointer handlers
- `docs/DESIGN-SYSTEM.md`: DS-217's readout and dense strip
- `docs/COMPONENT-CONTRACT.md`: `.ruler-tip`'s paragraph and state row

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| the drop's point sits on the mark, and the dense strip aims and pages | **pass**, look owed | §3's table. The look is `OWED-LOOKS.md` row 20 |
| DS-168's target count does not change | **pass** | 0 undersized enabled buttons before and after, on both decks |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | **pass** | Lint, then the full gate on the finished tree |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-14 | -> done | The readout is a drop pointing at its mark, and the dense strip reads the pointer, so record `16` is met with no new target under DS-168. The look is owed as `OWED-LOOKS.md` row 20. |
| 2026-09-14 | -> proposed | Raised from the owner's look at row 14, which asks for the drop and for the dense strip to aim. `PH3`: new behaviour. Batched into B28 first by the owner's ruling. |
