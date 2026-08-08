---
id: T-034
title: Add a contents page to the printed deck
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-032, T-018, T-005, T-035]
work_package: WP2
owner: maintainer
created: 2026-08-08
updated: 2026-08-08
deliverables: []
---

# T-034 — Add a contents page to the printed deck

## 1. Specify

**Outcome**
The printed deck opens with a **generated contents page** — one box per slide carrying its number,
its title, a one-sentence description and a mark — laid out to fit a single page, so a reader
holding the paper can see the shape of the argument before reading it. Screen rendering is
unchanged.

**Why this one**
Raised by the owner 2026-08-08 on reading the printed deck produced by
[T-032](T-032-adopt-the-paginated-print-mode-in-the-reference-deck.md). Twelve pages of slides
arrive with no map: on screen the spine ribbon shows where you are in the argument at all times, and
**the paginated print stylesheet hides the chrome**, so the printed artifact loses the one element
that carried the structure. A contents page is the paper equivalent of the ribbon.

**Two arguments for it the request did not make, and they are the stronger ones.**

1. **The content already exists, so the page is generated rather than authored.** Every slide
   carries a title that is a claim (DS-210) and a **bottom line** that states the one thing it
   delivers (DS-211, gated since [T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md)).
   The one-sentence description **is** the bottom line — it needs no writing, and because it is
   read from the slide it cannot drift from it. A contents page that had to be authored separately
   would be a second copy of the argument and would rot; this one cannot.
2. **It is the only surface that reaches the person holding the paper.** T-032 put the statement of
   what print does not preserve into the plugin's handover text — which is read by the person
   *about to* print, and never by whoever is handed the pages. The disclosure loss (38.6% of the
   deck's text, [R7](../docs/research/R7-printable-mode.md) §5) currently reaches a paper reader
   **nowhere**. One line on the contents page fixes that, and there is no other candidate location:
   [T-032](T-032-adopt-the-paginated-print-mode-in-the-reference-deck.md) ruled out print-only
   chrome on the slides.

**One content source, two renderings — and the manifest is the shared part, not the page**
*Owner's question, 2026-08-08: does the on-screen overlay index show the same thing as this?*
**The fields are the same and must be derived once; the renderings are not the same and should not
be forced to be.** Both need each slide's **number, title, bottom line, stage and mark** — and
`buildDoc()` already sets the precedent by cloning slides for the reading view rather than
re-authoring them. Two independent derivations of one fact is how they drift (**L-08**), so
whichever of this task and [T-035](T-035-the-ruler-navigator.md) lands first builds a **slide
manifest** and the other consumes it.

What legitimately differs, and why forcing them to match would be the wrong economy:

| | Printed contents page | On-screen overlay index |
| :--- | :--- | :--- |
| Constraint | **Must fit one page.** Length forces the layout. | Scrolls. Length costs nothing. |
| Read to | **Orient** before reading, once. | **Jump**, repeatedly. |
| Needs | The line stating that detail is screen-only. | Current-position highlight; nothing about print. |
| Mark | A slide clone is a texture at 0.22 scale — icon or nothing. | A live clone **can** work: no paper resolution limit, and it can enlarge on hover. |

So: **do not generate the content twice, and do not render it once.**

**The rule this amends, raised rather than taken** (**L-37**)
[`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §5.4 opens *"the printable mode is the paginated
stage — one slide per page"*. A contents page is **a printed page that is not a slide**, so the
sentence becomes *"the paginated stage, preceded by a generated contents page"*. That is a small
amendment and it is the owner's to make, not this task's to assume. It also lands on
[T-005](T-005-build-check-the-gate-the-deck-must-pass.md)'s print row: the gate stops counting
*n* pages for *n* slides.

**What the mark should be, and why "thumbnail" is probably the wrong answer**
Thumbnails were floated as an option. At twelve boxes on one 1920 × 1080 page each box is roughly
480 × 360 design units, so a live scaled clone of a slide renders at about **0.22 scale — 24-unit
body text becomes 5 units**. On paper that is a grey texture, not information, and it cannot be
made readable without dropping to four or six boxes. **A texture that looks like content is worse
than no mark**, because it invites a reader to squint at it. The deck already draws line icons
(the cost slide, the comparison header), so a per-stage or per-archetype **icon** is the cheaper
mark and the honest one. This is a recommendation, not a ruling — see the open question.

**Scope**
- In: a print-only contents page, generated from the slides at print time.
- In: the amendment to `DESIGN-SYSTEM.md` §5.4, once the owner takes it.
- In: the statement of what print does not preserve, placed on the page.
- In: the single-page bound — **measured on a deck longer than twelve slides**, not asserted.
- Out: a contents page on screen. The ribbon already carries structure there, and an on-demand
  slide index is [T-035](T-035-the-ruler-navigator.md)'s and
  [T-016](T-016-the-interaction-and-motion-layer.md)'s question, not this one.
- Out: authored descriptions. If the bottom line is not a good description, that is a defect in the
  bottom line and DS-211 already owns it.
- Out: raster thumbnails in any form — DS-110.

**Inputs**
- [`docs/research/R7-printable-mode.md`](../docs/research/R7-printable-mode.md) §5 — the list of
  what print does not preserve, which this page has to state in one line.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §5.4 and DS-210 · DS-211 · DS-110.
- [`examples/reference-deck.html`](../examples/reference-deck.html) — `buildDoc()` already clones
  every slide for the reading view, so the mechanism for reading titles and bottom lines at runtime
  exists and should not be written twice.

**Acceptance criteria**
- [ ] The printed deck is *n* + 1 pages: a contents page, then one page per slide, still with no
      blank page at either end
- [ ] Every box carries the slide's number, its title and its bottom line, **read from the slide**
      rather than authored — changing a slide's bottom line changes the contents page
- [ ] The fields are read through a **slide manifest** that the on-screen overlay index can consume
      unchanged, so the two renderings cannot derive the same fact twice (**L-08**)
- [ ] The page states in one line that detail behind disclosure is screen-only
- [ ] The whole thing fits one page at twelve slides, and **the number of slides at which it stops
      fitting is measured and written down**
- [ ] Screen rendering is byte-identical in behaviour — the page exists only under `@media print`
- [ ] Printed from a double-clicked file and **looked at** (**L-01**), not headless (**L-35**)
- [ ] `audit.py`, both variant suites and `print_variants.py` still pass

**Open questions**
- **One box per slide, or one per stage?** Twelve boxes give a 4 × 3 grid at ~480 × 360 du each,
  which is comfortable; seven stage boxes are roomier but lose the page numbers a reader needs to
  navigate paper. **This is the same question [T-035](T-035-the-ruler-navigator.md) asks about
  ticks**, and answering the two differently would be defensible only with a reason. — owner
  decides.
- **Icon, or nothing at all?** The analysis above argues thumbnails are a texture at this size. A
  contents page with no mark is also a legitimate answer and is the cheapest. — owner decides.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Take the two open questions, and the §5.4 amendment | the rulings |
| 2 | Measure a scaled slide clone at 12-up and record why the mark is what it is | the measurement |
| 3 | Build the contents page from the existing slide-cloning code, print-only | edited deck |
| 4 | Measure the slide count at which one page stops holding, on a longer deck | the bound |
| 5 | Amend `DESIGN-SYSTEM.md` §5.4 and T-005's print row | ruleset, gate |
| 6 | Print from a double-click and look at every page | printed artefact |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <path>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-08 | (no change) | **Answered the owner's question — the on-screen overlay index and this page share their content but not their rendering, and the shared part is a slide manifest rather than a page.** Both need each slide's number, title, bottom line, stage and mark, and deriving that twice is how the two drift (**L-08**); `buildDoc()` already sets the precedent of cloning slides instead of re-authoring them. What differs is real and should not be flattened: this page **must fit one page** and is read once to orient, the overlay scrolls and is read repeatedly to jump; this page owes the screen-only line, the overlay owes a current-position highlight; and **the mark can legitimately differ** — a slide clone is a texture at 0.22 scale on paper, but on screen it has no resolution limit and can enlarge on hover. So whichever of this and [T-035](T-035-the-ruler-navigator.md) lands first builds the manifest and the other consumes it. |
| 2026-08-08 | → proposed | Raised by the owner on reading the printed deck from [T-032](T-032-adopt-the-paginated-print-mode-in-the-reference-deck.md). Recorded with two arguments the request did not make — **the description is free**, because DS-211's bottom line already exists on every slide and reading it means the page cannot drift from the deck; and **it is the only surface that reaches a paper reader**, so the disclosure loss finally has somewhere to be stated to the person actually holding the pages. One amendment is owed and is raised rather than taken (**L-37**): §5.4 says the printable mode *is* the paginated stage, and a contents page is a printed page that is not a slide. The thumbnail option is argued against rather than dropped: at twelve boxes a slide clone renders at ~0.22 scale, which puts body text at five design units — a texture that looks like content. |
