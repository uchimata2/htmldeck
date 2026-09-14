---
id: T-307
title: Give the chrome first and last page controls, and a ruler whose marks a reader can aim at
type: deliverable
status: done
phase: review
parent: null
blocked_by: []
related: [T-299, T-178]
work_package: PH3
shipped_in: unreleased
owner: the project owner
business_value: medium
effort: m
created: 2026-09-13
updated: 2026-09-14
deliverables: [shell/shell.html, shell/deck.js, shell/components.css, docs/COMPONENT-CONTRACT.md, docs/DESIGN-SYSTEM.md, tools/deck/chrome_row.py]
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

**From the adopter report** `01`, `11`, `16`.

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
- [x] records `01`, `11` and `16` are each closed with the change looked at in a rendered deck of 12
      slides and in one past the dense-mode bound, or deferred with the reason recorded in this task
- [x] `DS-217` and the component contract say what the ruler does in both modes
- [x] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None for the owner. `16` reverses a behaviour `DS-217` states on purpose, and that is settled here
  from the rule's own reason rather than asked. **Settled in §3: the marks stay marks.**

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Add first and last to the pager, and a readout element to the ruler | `shell/shell.html`, `shell/deck.js`, `shell/components.css` |
| 2 | Decide `16` from DS-217's reason and DS-168 | §3 |
| 3 | Sync the decks, then re-measure the chrome row and DS-217's bound | `tools/deck/chrome_row.py`, `docs/DESIGN-SYSTEM.md` |
| 4 | Amend the contract rows and prose | `docs/COMPONENT-CONTRACT.md` |
| 5 | Measure the readout and the buttons in Chrome on 13 and 25 slides, record the look, lint, gate | §3 |

## 3. Implement

**Decisions & assumptions**
- First and last are two more `.btn--pager` buttons in `.navbox`, each drawn with two chevrons: they
  are navigation, and the contract admits only navigation to that box. They cost the ruler three
  targets, and DS-217 records the re-measured bound. Reversible. — 2026-09-14
- The readout is a `.ruler-tip` over the tick, showing the slide number, placed by measurement like
  the ring so it takes no width. The slide's name stays in `.ruler-label`, which already names the
  hovered tick. Reversible. — 2026-09-14
- Record `16` is deferred: the small ticks past the bound stay marks. A readout answers the aiming
  half of DS-217's reason, and not the other half: DS-168 is `hard`, its probe fails any enabled
  target under 24 CSS px, and a dense small tick is 8 du. Reversing it needs DS-168 to admit WCAG
  2.5.8's exception for a function another control provides, which is an amendment to a `hard` rule
  and the owner's. Reversible. — 2026-09-14
- `chrome_row.py` asserted five controls beside the ruler, and the unchanged tree measured four:
  T-277 had moved `Motion` into the menu. The assertion is now a constant of six, with the reason.
  Reversible. — 2026-09-14
- DS-217's bound was 16 on paper and 20 as built before this task, for the same reason. It is 17 now,
  measured. `.claude/rules/decks.md` names the tool and the date instead of a bare number.
  `DESIGN-SYSTEM.md`'s DS-226 rationale, which says the ruler goes dense past 16, is a dated argument
  and is left as written. Reversible. — 2026-09-14

`python tools/deck/chrome_row.py`, on the reference deck after the sync:

| Figure | Before | After |
| :--- | :--- | :--- |
| controls beside the ruler | 4 | 6: count 85.4, first 66.0, prev 52.0, next 52.0, last 66.0, more 82.8 du |
| left for the ruler | 1324.8 du, derived | 1160.8 du |
| capacity | 20 | 17 |

In headless Chrome at 1920x1080, through `render.chrome_run` with a probe appended to a copy:

| Deck | Mode | Rest | Hover a section tick | First, last |
| :--- | :--- | :--- | :--- | :--- |
| reference, 13 slides | not dense | readout hidden | shows `3`, centred on the tick at x 335, directly above it; hidden after leave | slide 0, slide 12 |
| `longdeck.py` splice, 25 slides | dense | readout hidden, small ticks disabled | shows `7`, centred at x 363; hidden after leave | slide 0, slide 24 |

§1.14 after the shell edit: four decks synced, the fixture regenerated, `density.py check` `0 wrong`
on each, and the seven size figures corrected in `README.md`, `examples/README.md` and
`docs/BRIEF.md`.

**Records:** `01` closed by the first and last buttons, `11` closed by the readout, `16` deferred for
the reason above.

**The look is owed**: [`../docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md) row 14.

**Outputs produced**
- `shell/shell.html`: `#first`, `#last` and `#rulerTip`
- `shell/deck.js`: `showTip`, `hideTip`, and the two click handlers
- `shell/components.css`: `.ruler-tip`, and the double chevron
- `tools/deck/chrome_row.py`: the controls constant
- `docs/COMPONENT-CONTRACT.md`: the `.ruler-tip` row and state, the pager counts and prose
- `docs/DESIGN-SYSTEM.md`: DS-217's bound, and what the ruler does in both modes

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| records `01`, `11` and `16` closed or deferred, looked at on 12 slides and past the bound | **pass**, look owed | `01` and `11` measured on 13 and 25 slides; `16` deferred with the reason. The look is `OWED-LOOKS.md` row 14 |
| `DS-217` and the contract say what the ruler does in both modes | **pass** | DS-217's row and the contract's `.ruler-tip` paragraph |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | **pass** | Lint, then the full gate on the finished tree |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-14 | -> done | First and last join the pager, and a target tick shows its number over the mark. Record `16` is deferred: DS-168 still binds the dense marks. DS-217's bound re-measured at 17. The look is owed as `OWED-LOOKS.md` row 14. |
| 2026-09-13 | -> proposed | Raised by T-299 from the third adopter's records `01`, `11` and `16`. `PH3`: all three ask for behaviour the chrome was not built to have, and none is a defect. |
