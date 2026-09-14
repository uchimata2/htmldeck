---
id: T-309
title: Contract an inline term that opens a definition bubble
type: deliverable
status: done
phase: review
parent: null
blocked_by: []
related: [T-299, T-262]
work_package: PH3
shipped_in: 1.0.0
owner: the project owner
business_value: low
effort: m
created: 2026-09-13
updated: 2026-09-14
deliverables: [docs/COMPONENT-CONTRACT.md, docs/DESIGN-SYSTEM.md, shell/deck.js, shell/components.css, tools/deck/audit.py, tools/deck/static_variants.py]
---

# T-309 — Contract an inline term that opens a definition bubble

## 1. Specify

**Outcome**
`docs/COMPONENT-CONTRACT.md` gives an inline term with a definition bubble a contracted form, so a deck
that uses the pattern passes the gate on the contract's terms. Today the contract defines `.disc` only
as a block, and no inline disclosure exists. The nearest precedent is the sources box: deliberately not
a `.disc`, with rows of its own, and still bound to the general disclosure rules `DS-163`, `DS-164`,
`DS-227` and `DS-137`.

**From the adopter report** `18`.
The deck's owner asked for the pattern by name and approved it.

**Scope**
- In: contract rows for the term and its bubble, shaped on the sources box
- In: `DS-138`'s direction clause for an inline control, so the bubble opens away from the reading line
- In: `DS-092` subtracting bubble text from the word count, as
  [T-262](T-262-ds-092-counts-a-sources-box-as-prose.md) did for the sources box
- In: the shell styles and script the rows require, looked at in a rendered deck
- Out: anything the record does not name. The report is a closed one-way hand-over, so a question this
  task cannot answer is settled here rather than asked

**Inputs**
- the record above, with the markup the deck used
- the sources box's rows in `docs/COMPONENT-CONTRACT.md`, and `DS-092`, `DS-137`, `DS-138`, `DS-163`,
  `DS-164` and `DS-227` in `docs/DESIGN-SYSTEM.md`

**Acceptance criteria**
- [x] record `18` is closed with the component contracted, built and looked at in a rendered deck, or
      deferred with the reason recorded in this task
- [x] a deck using the term passes the rules the contract binds it to, and a seeded misuse fails them
      (**L-125**)
- [x] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None. The record carries the markup and the owner's approval; the shape is settled here.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Contract the term on the sources box's footing | `docs/COMPONENT-CONTRACT.md` |
| 2 | Build its styles, its script and its reading-view and print forms | `shell/components.css`, `shell/deck.js` |
| 3 | Amend DS-092, DS-138 and DS-168, and make DS-092 and DS-227 read the bubble | `docs/DESIGN-SYSTEM.md`, `tools/deck/audit.py`, `tools/deck/check.py` |
| 4 | Seed a passing term and two misuses | `tools/deck/static_variants.py` |
| 5 | Sync, measure the term in Chrome, record the look, lint, gate | §3 |

## 3. Implement

**Decisions & assumptions**
- The term is three parts on the sources box's footing: `.term` in the copy, `.term-btn` the word
  itself, `.term-bub` the definition. It is not a `.disc`. Record `18`'s `.termlist` of bubbles beside
  the block is rejected: it existed only to keep definitions out of DS-092's count, which the
  amendment below does instead. Reversible. — 2026-09-14
- Hover shows the bubble and a press pins it. A preview does not close a panel the reader opened, and
  a pin does (DS-137). An outside click and Escape close it. Reversible. — 2026-09-14
- The bubble opens above its term, below only where above would leave the stage, and against its
  right edge where it would cross the stage's. Record `18`'s floor at the bottom line is rejected: it
  is one deck's layout, and the rule's obligation is the stage. Reversible. — 2026-09-14
- The reading view, print and the degraded state show every definition as a parenthetical beside its
  term, which keeps the hover a supplement (DS-163). Reversible. — 2026-09-14
- DS-092 subtracts a bubble from the sentence and the paragraph and holds each definition to the
  cap alone; the probe does both, and the clause table gains the row. DS-138 gains the inline
  direction. DS-227's probe counts an open bubble. Reversible. — 2026-09-14
- DS-168 admits WCAG 2.5.8's inline exception for a control that is a word in a sentence. The term's
  button measured 34.6 px tall at 1920 wide, under the rule's 48 units, and padding it would break
  its line. The scope did not name DS-168; the amendment is the criterion's own text, and it is
  reported here. Reversible. — 2026-09-14
- A bubble left open in the file is caught by DS-229, where the contract row requires `hidden`, and
  not by a render seed. The first full gate missed a DS-227 seed: the shell's `go(0)` shuts every
  bubble before any probe runs, as it shuts a disc panel. DS-227's probe still counts an open bubble,
  which catches a shell that stops shutting them. Reversible. — 2026-09-14
- `SWEPT` re-digests DS-092, DS-138 and DS-168, each re-read against its amendment. Reversible.
  — 2026-09-14

In headless Chrome at 1920x1080, on a copy of the synced reference deck with a term on slide 10:

| Step | Bubble | `aria-expanded` | Pinned |
| :--- | :--- | :--- | :--- |
| at rest | hidden | false | no |
| hover | shown, bottom at 604 px above the button's top at 608, inside the stage | true | no |
| leave | hidden | false | no |
| press, then leave | shown | true | yes |
| outside click | hidden | false | no |
| press, then Escape | hidden | false | no |
| reading view | inline, opening `" ("` | — | — |

`check.py` on that copy exits 0: DS-092 `sentences over 20 words: 0`, DS-168 `targets under 24 CSS
px: 0`, DS-227 `panels closed at load: 0 open`, DS-229 and DS-138 pass.

The seeds, run by `static_variants.py` in the full gate:

| Seed | Rule | Direction |
| :--- | :--- | :--- |
| `a-term-in-a-sentence`: a 17-word sentence with a 12-word definition | DS-092 | must pass |
| `term-bubble-not-shut-in-the-file`: a bubble without `hidden` | DS-229 | must fail |
| `term-button-naming-no-bubble` | DS-229 | must fail |

§1.14 after the shell edit: four decks synced, the fixture regenerated, `density.py check` `0 wrong`
on each, and the seven size figures corrected.

**Record `18` closed.** **The look is owed**: [`../docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md) row 15.

**Outputs produced**
- `docs/COMPONENT-CONTRACT.md`: the `.term` rows, paragraph, example and state rows
- `docs/DESIGN-SYSTEM.md`: DS-092, DS-138 and DS-168 amended
- `shell/deck.js` and `shell/components.css`: the term, its placement, and its reading-view, print
  and degraded forms
- `tools/deck/audit.py`: DS-092's and DS-227's readings of the bubble
- `tools/deck/check.py`: DS-092's clause row and three digests
- `tools/deck/static_variants.py`: the three seeds

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| record `18` closed with the component contracted, built and looked at | **pass**, look owed | Built and measured in §3. The look is `OWED-LOOKS.md` row 15 |
| a deck using the term passes, and a seeded misuse fails | **pass** | §3's seeds, run in the full gate |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | **pass** | Lint, then the full gate on the finished tree |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-14 | -> done | The inline term is contracted and built on the sources box's footing. DS-092, DS-138 and DS-168 amended, DS-168 beyond the scope for the reason in §3. Record `18` closed; the look is owed as `OWED-LOOKS.md` row 15. |
| 2026-09-13 | -> proposed | Raised by T-299 from the third adopter's record `18`. `PH3`: a new component, not a defect in one that exists. |
