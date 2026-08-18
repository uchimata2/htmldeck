---
id: T-184
title: Re-cut the shipped diagrams onto the text column, and turn the measurement into a gate
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-117, T-115, T-182]
work_package: PH3
owner: the project owner
business_value: medium
effort: l
created: 2026-08-18
updated: 2026-08-18
deliverables:
  - examples/reference-deck.html
  - examples/sort-window/sort-window.html
  - docs/DESIGN-SYSTEM.md
---

# T-184 — Re-cut the shipped diagrams onto the text column, and turn the measurement into a gate

## 1. Specify

**Outcome**
Every diagram in every deck this repository ships starts its ink on the same column as the slide's
text, and the measurement that says so is a gated rule rather than a tool somebody has to remember
to run.

**The finding this starts from**
[T-117](T-117-the-decision-diamond-has-no-label-slot-and-diagrams-sit-off-the-text-grid.md) landed
the rule for what a build writes from now on, and the measurement that decides it —
`python tools/deck/figgrid.py <deck>`. Its first run, 2026-08-18:

| Deck | Diagrams | Off the column by more than 4 du |
| :--- | :---: | :---: |
| `examples/reference-deck.html` | 8 | 7 |
| `examples/sort-window/sort-window.html` | 6 | 6 |
| `examples/measure-first/measure-first.html` | 7 | 5 |
| **total** | **21** | **18** |

Offsets run from +22.7 to +217.9 design units. **The `<svg>` element is not the problem** — it sits
at 96 du on every slide of every deck, exactly where the headline and the bottom line sit. Each
diagram declares its own viewBox, the element is scaled to the 1726 du content column, and the
drawing starts wherever the author left it inside that box.

**Why this was split off rather than done in T-117.** Shifting every `x` in a viewBox is mechanical,
but a re-cut diagram is then owed a look (`CLAUDE.md` rule 6), and 18 looks is the cost — not the
arithmetic. T-117 was `m` and this is not. The split is [T-054](T-054-record-which-clauses-of-a-rule-the-gate-decides.md)'s
precedent: make the hole visible and countable first, close it as its own work.

**Scope**
- In: re-cutting the 18 diagrams so their ink starts on the text column, deck by deck, each one
  looked at offline after the change.
- In: promoting `figgrid.py` from a reporting tool to a gated rule — a `DS-nnn` row, a verdict
  reached by `check.py`, and its entry moving out of `check_all.py`'s `NOT_RUN` table.
- In: the two slides that already measure +1.3 and +2.2 du. They are inside the tolerance and are
  the accident rather than the rule; leaving them is correct, and saying so is part of the record.
- In: `measure-first` slide 8's decision node, the second of the two T-117 found. T-117 re-cut
  slide 2 as its demonstration and left this one, and it is the same surgery.
- Out: changing what a diagram *says*. This is placement, not redrawing.
- Out: the tolerance. 4 du is `figgrid.py`'s and it is not this task's to move; if it turns out to
  be wrong, that is a finding with a measurement behind it, not an adjustment.

**Inputs**
- [`tools/deck/figgrid.py`](../tools/deck/figgrid.py) — the measurement, and the tolerance.
- [`skills/htmldeck/references/build.md`](../skills/htmldeck/references/build.md) §2 — the rule as a
  build must now follow it.
- [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) §3.6 — `.decision` and its parts.
- [T-117](T-117-the-decision-diamond-has-no-label-slot-and-diagrams-sit-off-the-text-grid.md) §3 —
  the worked re-cut of one node, with the arithmetic that sized it.

**Acceptance criteria**
- [ ] `python tools/deck/figgrid.py` reports 0 diagrams off the column across all three decks
- [ ] Every re-cut diagram has been opened and looked at offline; the record says which and at what
      length
- [ ] The rule is gated — a `DS-nnn` row, decided by `check.py`, with the full gate green
- [ ] `figgrid.py` no longer sits in `check_all.py`'s `NOT_RUN`, and the partition still holds
- [ ] `measure-first` slide 8's decision node carries its label inside itself
- [ ] No diagram's meaning changed; the re-cut is placement only

**Open questions**
- Whether a diagram genuinely wider than the text column spans it or is inset deliberately. T-117's
  §1 answered the principle — a wide diagram spans whole columns rather than ignoring them — and
  the first deck that has one decides the practice.

## 2. Plan

<not started>

## 3. Implement

**Decisions & assumptions**
- <none yet>

**Outputs produced**
- <none yet>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :--- | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-18 | → proposed | Split out of [T-117](T-117-the-decision-diamond-has-no-label-slot-and-diagrams-sit-off-the-text-grid.md) on the owner's ruling, once measuring turned *one deck's diagrams* into 18 across three decks. `l` rather than `m` because the arithmetic is mechanical and the looking is not. `PH3` by [`../CLAUDE.md`](../CLAUDE.md)'s rule: the decks render correctly and no adopter is affected, so it does not reopen `PH1`. |
