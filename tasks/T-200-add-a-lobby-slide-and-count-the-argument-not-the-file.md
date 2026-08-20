---
id: T-200
title: Add a lobby slide, and count the argument rather than the file
type: decision
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-036, T-108, T-175, T-178]
work_package: PH3
owner: the project owner
business_value: high
effort: l
created: 2026-08-20
updated: 2026-08-20
deliverables: []
---

# T-200 - Add a lobby slide, and count the argument rather than the file

## 1. Specify

**Outcome**
A deck can open on a slide the audience looks at while the room fills, and the position counter
counts the argument rather than the file.

**What the owner asked for, 2026-08-20**
A starting page - *an audience waiter page, a kinda appetizer, a lobby* - showing the topic, the
presenter and the context (an expo, a training exam), and nothing from the results. And: *when the
number of slides is calculated, the colophon and the lobby page should be excluded, these are just
cover pages of the topic, not content.*

**Contradiction check - three rules are near this and none is broken**

- **DS-085** - the last slide is a close, with one named exemption for a colophon. A lobby is front
  matter, so DS-085 is untouched. But DS-085's wording is deliberately narrow to stop an appendix
  growing behind the close, and **front matter invites exactly the same creep**: agenda, about-me,
  thank-you. The lobby rule has to be written as narrowly as DS-085's exemption, or it becomes the
  door. The owner's own framing already is narrow - topic, presenter, context, nothing from the
  results - and it should be written that way rather than as *a title slide*.
- **DS-225** - *the contents page is generated from the deck, never authored, and it is placed
  first.* Measured 2026-08-20: the contents page is **print-only** - `deck.js` builds it inside the
  print path. So *first* is a statement about sheet order, and its stated reason is mechanical: a
  `<section>` placed after the final slide breaks `section.slide:last-of-type`. A lobby placed
  before it breaks neither the reason nor the mechanism. The wording still needs amending, because
  it will no longer be literally true.
- **DS-108's back-matter stage** already exists - `data-stage="back"`, a slide outside the argument,
  which DS-225 gives a box with no mark. A `front` stage is that rule's mirror and should be built
  as one rather than as a new idea.

**The cost nobody has stated yet, and it decides part of the design**
DS-226 bounds the printed contents page at **16 entries on one sheet, then sheets of at most 12**.
The adopter deck is 16. Add a lobby and it is 17 - so a deck that printed one contents sheet prints
two, and DS-226's own discontinuity note says a 17-entry deck gets *better* rows than a 16-entry one.
Separately, `CLAUDE.md`'s verifying section records that the ruler degrades to dense mode past 16
([T-178](T-178-dense-mode-drops-the-position-mark-below-the-section-marks.md)). **Adding one slide to
the front of a 16-slide deck therefore crosses two thresholds at once.** That is an argument for the
lobby being excluded from the counter *and* the ruler marks - which is what the owner asked for - and
it is the strongest argument for it, stronger than tidiness.

**Where I disagree, on one point**
Excluding the covers from the **counter** is right. Excluding them from the **printed contents page**
is not, and the owner did not ask for it - but the two will be conflated unless the task says so.
The counter answers *where am I in the argument*; the contents page is a map of the physical
artifact a reader is holding, and a map that omits two of the sheets in the pile is wrong about the
pile. My recommendation: front and back matter keep their contents boxes, marked as matter rather
than as argument, and lose their counter position and their ruler mark. That keeps DS-225's
stage-keyed marks working exactly as T-108 built them.

**Scope**
- In: a `front` stage mirroring `back`, and what a lobby slide may carry - stated as narrowly as
  DS-085's colophon exemption.
- In: the counter and the ruler counting argument slides only.
- In: DS-225's *placed first* clause, amended to say first among what.
- In: the contents page's treatment of front matter - decided explicitly, per the paragraph above.
- In: the three shipped decks, which gain a lobby or state why they do not.
- Out: a template or a theme for the lobby's look. That follows the rule; it is not this decision.

**Inputs**
- [`../docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) DS-085, DS-105, DS-225, DS-226.
- [T-108](T-108-a-deck-has-no-back-matter-stage-so-the-colophon-is-labelled-with-the-last-argument-stage.md)
  - the back-matter stage this mirrors.
- [T-036](T-036-the-second-contents-page-for-long-decks.md) - the sheet bounds the count interacts with.

**Acceptance criteria**
- [ ] A deck with a lobby and a colophon reports `n / N` over its argument slides only.
- [ ] The lobby rule names what may appear on it, and a second front-matter slide fails the gate.
- [ ] A 16-argument deck with both covers still prints **one** contents sheet, or the task records
      why that was given up.
- [ ] Printed and looked at, per `CLAUDE.md` rule 6 - the covers are where a numbering change shows
      up on paper first.

**Open questions**
- Do front and back matter keep a contents box? My recommendation is yes, marked as matter.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision - rationale - date>

**Outputs produced**
- <path>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-20 | -> proposed | Created. |
