---
id: T-307
title: Give the chrome first and last page controls, and a ruler whose marks a reader can aim at
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-299, T-178]
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-09-13
updated: 2026-09-13
deliverables: []
---

# T-307 — Give the chrome first and last page controls, and a ruler whose marks a reader can aim at

## 1. Specify

**Outcome**
A reader with a pointer can reach the first and the last page, and can tell which slide a ruler mark
is before clicking it, in both ruler modes. Today:

- the pager wires only previous and next (`shell/shell.html` `:77`-`:78`, `shell/deck.js`
  `:618`-`:619`), and Home and End are keyboard-only;
- hovering or focusing a tick writes the one shared `#rulerLabel` beside the ticks
  (`shell/deck.js` `:209`-`:211`, `:233`-`:235`), not a readout at the mark the pointer is on;
- past the dense-mode bound the small ticks are `disabled` with `tabIndex = -1`
  (`shell/deck.js` `:257`-`:259`), and `DS-217` states that as intended.

**From the adopter report** [`01`](../docs/adopter-reports/nextep/2026-09-01-nav-chrome-has-no-first-last-page-control.md), [`11`](../docs/adopter-reports/nextep/2026-09-07-the-ruler-gives-no-slide-number-on-hover.md), [`16`](../docs/adopter-reports/nextep/2026-09-08-the-condensed-ruler-drops-the-small-dots-as-targets.md).

**`01` was measured on `0.6.0`.** Triage checked it against this tree on 2026-09-13, and the pager is
unchanged.

**Why the three are one task.** `16` asks for the small ticks back as targets, and a target is only
aimable once `11`'s readout exists, so `16` depends on `11`. `01` is the same chrome row and the same
question: what a pointer can reach.

**Scope**
- In: first and last page controls, wired to the existing `go(0)` and `go(slides.length-1)`
- In: a readout at the hovered or focused mark, from `dataset.label`. `DS-163` permits hover as a
  supplement, and `DS-217` bars a per-item label only at rest
- In: whether the small ticks become targets again in dense mode once the readout exists, decided from
  `DS-217`'s own reason, with `DS-217` and the component contract amended in the same change if so
- Out: anything the records above do not name. The report is a closed one-way hand-over, so a
  question this task cannot answer is settled here rather than asked

**Inputs**
- the three records above
- `DS-217`, `DS-163` and `DS-131` in `docs/DESIGN-SYSTEM.md`, and the ruler rows of
  `docs/COMPONENT-CONTRACT.md`

**Acceptance criteria**
- [ ] records `01`, `11` and `16` are each closed with the change looked at in a rendered deck of 12
      slides and in one past the dense-mode bound, or deferred with the reason recorded in this task
- [ ] `DS-217` and the component contract say what the ruler does in both modes
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None for the owner. `16` reverses a behaviour `DS-217` states on purpose, and that is settled here
  from the rule's own reason rather than asked.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

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
| 2026-09-13 | -> proposed | Raised by T-299 from Nextep records `01`, `11` and `16`. `PH3`: all three ask for behaviour the chrome was not built to have, and none is a defect. |
