---
id: T-108
title: A deck has no back-matter stage, so the colophon is labelled with the last argument stage
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-034, T-035, T-036, T-109]
work_package: PH1
owner: the project owner
business_value: high
effort: m
created: 2026-08-12
updated: 2026-08-12
deliverables:
  - shell/deck.js
  - docs/COMPONENT-CONTRACT.md
  - docs/DESIGN-SYSTEM.md
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
-

**Outputs produced**
-

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :--- | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-12 | → proposed | Created. Reported against published `0.2.2` by the first adopting project and filed as theirs; re-derived here as this repository's, and as a missing vocabulary value rather than a label bug. The reporter's reading — "the title of the previous page" — is not what the code does; the resting label is the stage name. |
| 2026-08-12 | (no change) | **Confirmed in a render**, offline with motion pinned: slide 13 of 13 shows `DECISION` beside the ruler while the slide's own name is *What this deck rests on*. Also visible is the second half nobody reported — the colophon holds the last **section tick**'s stage, so the Decision stage's census reads one slide longer than the argument is. |
| 2026-08-13 | (no change) | **Step 1 done — the blast radius, and one defect it found in this repository's own deck.** Consumers of `m.stage` / `m.stageName` / `m.icon` in [`shell/deck.js`](../shell/deck.js): `firstSlideOfStage`, `buildRuler` (`isSection`, `aria-label`, `dataset.label`), `restoreLabel`, and `buildContents`'s `.cstage` and `.cico`. Five, in four functions, from one manifest. **`examples/reference-deck.html` worked around this by inventing an eighth stage**: `STAGES` ends `…,'The ask','Colophon']` — 8 entries — while `STAGE_ICON` has **7**, so the colophon's `data-stage="7"` subscripts `STAGE_ICON[7]` to `undefined` and its contents box prints with **no mark** where the other twelve carry one. Visible on the printed contents page and shipped that way. So this repository is not a bystander to the adopter's report; it has the same defect in a worse form, because a fake argument stage also miscounts the census the ruler draws from. `Colophon` in `STAGES` is additionally a second copy of the slide's own authored eyebrow, *13 · Colophon* (**L-08**). |
| 2026-08-13 | (no change) | **Where step 2 has to decide something §1 left open.** With `data-stage="back"` the slide has no stage, and four of the five consumers need nothing more — the ruler names the slide, the tick is not a section, the census skips it. Only the printed contents box wants a word and a mark for a slide that has no stage to supply either, and the shell's own CSS says why it cannot simply be left blank: *"the stage name gives the icon a label — an unlabelled glyph on paper is decoration"*. Decide between a shell-owned constant plus a shell-owned icon (costs a sprite entry, so every deck's `ICONS` slot and `shell.py icons`), and omitting `.cico` for back matter (costs nothing, but one card among thirteen then carries no mark, which is what it looks like today and was read as a bug). Not decided here — it is step 2's, and it wants the printed page in front of it. |
