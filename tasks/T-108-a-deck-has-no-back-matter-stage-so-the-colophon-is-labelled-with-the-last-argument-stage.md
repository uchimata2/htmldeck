---
id: T-108
title: A deck has no back-matter stage, so the colophon is labelled with the last argument stage
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-034, T-035, T-036, T-109]
work_package: PH1
owner: the project owner
business_value: high
effort: m
created: 2026-08-12
updated: 2026-08-13
shipped_in: 0.2.3
deliverables:
  - shell/deck.js
  - docs/COMPONENT-CONTRACT.md
  - docs/DESIGN-SYSTEM.md
  - tools/deck/component.py
  - tools/deck/shell.py
  - examples/reference-deck.html
  - examples/sort-window/sort-window.html
  - examples/reference-deck-seeded-defects.html
---

# T-108 — A deck has no back-matter stage, so the colophon is labelled with the last argument stage

## 1. Specify

**Outcome**
A slide that is not part of the argument says so, and every renderer that reads the stage census
gets an answer that is true. Today the colophon is forced to declare an argument stage it is not in,
and the ruler reports that stage as the reader's location.

**The mechanism, measured**
Reported as *"the navigator dot shows the title correctly on hover ('Sources'), but when selected it
is the title of the previous page ('Decision')"*, and filed against the adopting project. **It is
this repository's, and it is not the previous page's title.**

[`shell/deck.js`](../shell/deck.js) builds two labels from one manifest:

```
b.dataset.label = isSection ? m.stageName : m.title;   // hover and focus
rulerLabel.textContent = m ? m.stageName : '';         // at rest
```

Hover shows the slide title; **at rest the ruler shows the stage name, always.** The reporting deck
declares `STAGES = ['Problem','Evidence','Redesign','Case','Decision']` and gives its colophon
`data-stage="4"`, so at rest the ruler correctly reports stage 4 — *Decision* — for a slide that is
not in the Decision stage or in any other.

**The label is the symptom.** `data-stage` is mandatory and its vocabulary contains only argument
stages, so back matter has nowhere to go and is pushed into the nearest one. Every consumer of the
census inherits that: `firstSlideOfStage`, the ruler's section ticks, the printed contents page
(T-034) and the on-screen index (T-035) are all renderings of one manifest, so a colophon counted
into *Decision* is a colophon counted into *Decision* four times. Fixing `restoreLabel` alone would
hide the miscount and leave it.

**Scope**
- In: a back-matter value in the stage vocabulary, declared in
  [`COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md), with what it means and what may carry it.
- In: `manifest()` and `firstSlideOfStage` treating it as outside the argument — not a section start,
  not counted in any stage's total.
- In: `restoreLabel` falling back to the slide's own title for a back-matter slide, because there is
  no stage to name.
- In: the two contents renderings (T-034, T-035) checked against the change rather than assumed
  unaffected — they read the same manifest.
- In: `check.py` deciding whatever part of this a gate can decide, or naming why it cannot.
- Out: **what the colophon slide contains.** That is
  [T-109](T-109-one-source-reference-component-rendered-in-three-places.md).
- Out: a second contents page for long decks — [T-036](T-036-the-second-contents-page-for-long-decks.md),
  parked by the owner and not unparked by this.

**Inputs**
- [`shell/deck.js`](../shell/deck.js) — `manifest()`, `buildRuler()`, `restoreLabel()`,
  `firstSlideOfStage()`.
- [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) — where `data-stage` is specified.
- [T-035](T-035-the-ruler-navigator.md) — the ruler, and the derivation rule (**L-08**) that makes
  this one change reach four renderings.
- [T-034](T-034-a-contents-page-for-the-printed-deck.md) — the second rendering of the same manifest.

**Acceptance criteria**
- [ ] A slide marked as back matter is not a section start and appears in no stage's total.
- [ ] At rest, the ruler on a back-matter slide names the slide, not a stage.
- [ ] On hover, the behaviour is unchanged for every other slide.
- [ ] The printed contents page and the on-screen index both place back matter correctly, verified by
      rendering both.
- [ ] The stage vocabulary's new value has a contract row.
- [ ] A deck with no back matter renders byte-identically to before, or the difference is explained.
- [ ] `python tools/deck/check.py` green on the reference deck; `chrome_row.py` green.
- [ ] Opened and looked at, offline, in both renderings.

**Open questions**
- The owner has taken the design: a back-matter stage, not a label fallback. The value's *name* is an
  implementation decision.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Enumerate every consumer of `data-stage` and of the manifest's `stage` field | the blast radius, written down |
| 2 | Add the vocabulary value and its contract row | contract |
| 3 | Teach `manifest()` and `firstSlideOfStage` the exclusion | `deck.js` |
| 4 | Fall the resting label back to the title for back matter | `deck.js` |
| 5 | Render the ruler, the on-screen index and the printed contents page | three renderings compared |
| 6 | Decide what `check.py` can gate here, and write the reason where it cannot | `check.py`, ruleset |

## 3. Implement

**Decisions & assumptions**

- **The value is `data-stage="back"`** — the owner's design, a value in the stage vocabulary rather
  than a label fallback. `manifest()` returns `stage: null`, `back: true`, and a `stageName` of
  `Back matter`; the other four consumers branch on `back`.
- **The label is a shell constant, not a deck-supplied word, and that was forced.** A slide with no
  stage has no stage entry to read a word from, and supplying one would mean a fourth per-deck
  script declaration. `Back matter` is also true of every thing that may carry the value — a
  colophon, an appendix, a sources page, a glossary — where `Colophon` is true of one.
- **Back matter carries no mark, and this was decided from the ruleset rather than from taste.**
  DS-113/114 key the mark to the stage; a slide with no stage therefore has none, and the absence is
  the rule holding. This is what the open decision in the log of 2026-08-13 was, and it did not need
  the printed page after all — it needed DS-113 read back.
- **`firstSlideOfStage(null)` returns 0**, so `isSection` had to be guarded rather than left to the
  lookup. Without the guard a back-matter slide silently re-declares slide 1 a section start. Found
  by reading, then confirmed in the census: 7 section ticks, not 8 and not 9.
- **DESIGN-SYSTEM.md changed after all, and not where §1 expected.** No new rule was needed — the
  behaviour follows from DS-113/114 — but **DS-225 had become false**: it says the mark is keyed to
  the stage "so an uneven deck cannot produce an uneven set of marks", and back matter makes exactly
  one box markless. The clause is amended to say which unevenness is forbidden (the one derived from
  slide content) and which is the rule working.
- **The reference deck's colophon eyebrow now reads `13 · Back matter`.** `buildContents` states as
  a property that a box's number and stage name render *exactly* as the slide's own eyebrow does, so
  a reader can match card to page — and `13 BACK MATTER` against `13 · COLOPHON` broke it. Changing
  the deck's authored word was the cheaper of the two repairs, and the honest one: `Colophon` was
  the name of the invented stage this task retires.
- **`shell.py check` gained a gate for the defect step 1 found.** `STAGES` and `STAGE_ICON` are one
  table subscripted by one attribute, so a deck whose two halves differ in length is wrong;
  `new()` builds them together and cannot get it wrong, a hand-edited deck can, and one had.
  Seeded in both directions.

**Outputs produced**
- [`shell/deck.js`](../shell/deck.js) — `manifest()`'s back-matter branch, the `isSection` guard,
  `restoreLabel`'s fallback, and `buildContents` emitting no mark rather than an empty one.
- [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) — the vocabulary value, what may
  carry it, and a six-row table of what it changes in every rendering at once.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-225's mark clause corrected.
- [`tools/deck/component.py`](../tools/deck/component.py) — `NOT_AN_INDEX`, so `back` is legal where
  an `#ARRAY` attribute is otherwise a subscript; fixtures in both directions.
- [`tools/deck/shell.py`](../tools/deck/shell.py) — the `STAGE TABLE` gate and its two fixtures.
- The three tracked decks, carrying the shell byte for byte; the reference deck also drops its
  eighth stage and marks its colophon.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A slide marked as back matter is not a section start and appears in no stage's total | met | Read out of the live DOM, offline: 13 ticks, section ticks at slides **1, 2, 3, 5, 7, 10, 12** — seven, where the invented eighth stage previously made it eight and put one on slide 13. |
| At rest, the ruler on a back-matter slide names the slide, not a stage | met | `SOURCES`, the slide's own `data-name`. Was `Colophon` here and `Decision` in the deck that reported it. Looked at in a screenshot as well as read from the DOM. |
| On hover, the behaviour is unchanged for every other slide | met | Slide 1 rests on `Claim` and slide 13 hovers to `Sources`; the aria name is the non-section form, `Go to slide 13: Sources`. On the deck with no back matter (`sort-window`) the whole census is unchanged: 12 ticks, sections at 1, 2, 3, 5, 7, 9, 11, resting `The ask`, hovering `Approve the slot by 19 September`. |
| The printed contents page and the on-screen index both place back matter correctly, verified by rendering both | met | Contents box 13 reads `Back matter` with no `.cico` element; boxes 1–12 keep their stage names and marks. The ruler is the on-screen rendering and is the row above. Both rendered, not reasoned about. |
| The stage vocabulary's new value has a contract row | met | `COMPONENT-CONTRACT.md`, with what may carry it, what may not, and the per-rendering table. |
| A deck with no back matter renders byte-identically to before, or the difference is explained | met, with the difference explained | Not byte-identical: `sort-window.html` grew 1 941 bytes because the shared script block is in it. Its **rendering** is unchanged, verified above — no deck without `data-stage="back"` can reach any new branch, since all four are guarded on a flag that is false. |
| `python tools/deck/check.py` green on the reference deck; `chrome_row.py` green | met | `0 failure(s): none`. `chrome_row.py`: `self-test ok (row 1726 du at both scales, five controls, floor run at k=0.506)`. |
| Opened and looked at, offline, in both renderings | met | The printed contents page as a PDF, and the deck on screen resting on slide 13. The first screenshot came back with a blank slide body; that was my own animation-pinning style holding the `rise` elements at opacity 0, confirmed by re-shooting without it rather than assumed. |
| *(added)* `STAGES` and `STAGE_ICON` cannot differ in length | met | `shell.py check` gains `STAGE TABLE`, seeded both ways: `a stage with no icon is caught`, `an icon table shorter than the stages is caught`. 30 of 30 fixtures. |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-12 | → proposed | Created. Reported against published `0.2.2` by the first adopting project and filed as theirs; re-derived here as this repository's, and as a missing vocabulary value rather than a label bug. The reporter's reading — "the title of the previous page" — is not what the code does; the resting label is the stage name. |
| 2026-08-12 | (no change) | **Confirmed in a render**, offline with motion pinned: slide 13 of 13 shows `DECISION` beside the ruler while the slide's own name is *What this deck rests on*. Also visible is the second half nobody reported — the colophon holds the last **section tick**'s stage, so the Decision stage's census reads one slide longer than the argument is. |
| 2026-08-13 | (no change) | **Step 1 done — the blast radius, and one defect it found in this repository's own deck.** Consumers of `m.stage` / `m.stageName` / `m.icon` in [`shell/deck.js`](../shell/deck.js): `firstSlideOfStage`, `buildRuler` (`isSection`, `aria-label`, `dataset.label`), `restoreLabel`, and `buildContents`'s `.cstage` and `.cico`. Five, in four functions, from one manifest. **`examples/reference-deck.html` worked around this by inventing an eighth stage**: `STAGES` ends `…,'The ask','Colophon']` — 8 entries — while `STAGE_ICON` has **7**, so the colophon's `data-stage="7"` subscripts `STAGE_ICON[7]` to `undefined` and its contents box prints with **no mark** where the other twelve carry one. Visible on the printed contents page and shipped that way. So this repository is not a bystander to the adopter's report; it has the same defect in a worse form, because a fake argument stage also miscounts the census the ruler draws from. `Colophon` in `STAGES` is additionally a second copy of the slide's own authored eyebrow, *13 · Colophon* (**L-08**). |
| 2026-08-13 | (no change) | **Where step 2 has to decide something §1 left open.** With `data-stage="back"` the slide has no stage, and four of the five consumers need nothing more — the ruler names the slide, the tick is not a section, the census skips it. Only the printed contents box wants a word and a mark for a slide that has no stage to supply either, and the shell's own CSS says why it cannot simply be left blank: *"the stage name gives the icon a label — an unlabelled glyph on paper is decoration"*. Decide between a shell-owned constant plus a shell-owned icon (costs a sprite entry, so every deck's `ICONS` slot and `shell.py icons`), and omitting `.cico` for back matter (costs nothing, but one card among thirteen then carries no mark, which is what it looks like today and was read as a bug). Not decided here — it is step 2's, and it wants the printed page in front of it. |
| 2026-08-13 | → specified | §1 was already complete; the two rows above are step 1's findings. |
| 2026-08-13 | → planned | §2 was already complete and unchanged. |
| 2026-08-13 | → in_progress | Built as the owner specified — `data-stage="back"`, a value in the stage vocabulary. Four consumers branch on it and the fifth, `firstSlideOfStage`, needed a guard rather than a branch. |
| 2026-08-13 | (no change) | **The open decision resolved from the ruleset, not from the printed page.** DS-113/114 key the mark to the stage, so a slide with no stage carries none and the absence is the rule holding. That also made DS-225 false where it said the marks cannot be uneven, so the ruleset took a correction. The knock-on nobody predicted: the contents box's label then disagreed with the slide's own eyebrow, which `buildContents` states as a property a reader relies on — repaired by changing the deck's authored word to the vocabulary's. |
| 2026-08-13 | → done | Eight §1 criteria met and one added. The census reads 7 section ticks where it read 8, the ruler rests on `SOURCES`, and the contents box carries a label and no empty mark. `check.py` and `chrome_row.py` green; both renderings looked at offline. |
| 2026-08-13 | (no change) | **Shipped in `0.2.3`**, tagged `v0.2.3`. `python tools/check_all.py` green on the tagged tree: 19 ran, 1 skipped with its reason, 0 failed. |
