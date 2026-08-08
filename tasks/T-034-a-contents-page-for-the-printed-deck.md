---
id: T-034
title: Add a contents page to the printed deck
type: deliverable
status: review
phase: review
parent: null
blocked_by: []
related: [T-032, T-018, T-005, T-035]
work_package: WP2
owner: maintainer
created: 2026-08-08
updated: 2026-08-08
deliverables:
  - examples/reference-deck.html
  - tools/deck/contents_bound.py
  - docs/DESIGN-SYSTEM.md
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

**The rule this amends — raised rather than taken, and taken by the owner 2026-08-08** (**L-37**)
[`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §5.4 opens *"the printable mode is the paginated
stage — one slide per page"*. A contents page is **a printed page that is not a slide**, so the
sentence becomes *"the paginated stage, preceded by a generated contents page"*. **The owner took
that wording unchanged**, so the amendment is now this task's to make rather than to assume — it is
plan step 5, and it is not done until the ruleset says it. It also lands on
[T-005](T-005-build-check-the-gate-the-deck-must-pass.md)'s print row: the gate stops counting
*n* pages for *n* slides and counts *n* + 1.

**What the mark should be, and why "thumbnail" is probably the wrong answer**
Thumbnails were floated as an option. At twelve boxes on one 1920 × 1080 page each box is roughly
480 × 360 design units, so a live scaled clone of a slide renders at about **0.22 scale — 24-unit
body text becomes 5 units**. On paper that is a grey texture, not information, and it cannot be
made readable without dropping to four or six boxes. **A texture that looks like content is worse
than no mark**, because it invites a reader to squint at it. The deck already draws line icons
(the cost slide, the comparison header), so a per-stage or per-archetype **icon** is the cheaper
mark and the honest one. **The owner ruled for the icon on 2026-08-08**, so this is settled rather
than recommended: seven line icons, one per stage, keyed to `data-stage`.

**Scope**
- In: a print-only contents page, generated from the slides at print time.
- In: **seven line icons, one per stage**, drawn in the deck's existing icon vocabulary.
- In: **the compression behaviour past twelve slides** — 4 columns, growing rows, a stated type
  floor — and the measurement of where it stops holding.
- In: the amendment to `DESIGN-SYSTEM.md` §5.4, which the owner has now taken.
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

### What the deck already does — measured 2026-08-08, so the specify pass need not re-derive it

Read this before writing the detailed spec. It is the state of
[`examples/reference-deck.html`](../examples/reference-deck.html) as it stands, not a proposal.

**The data the page needs already exists, and here is where it lives.**

| Field | Where | Note |
| :--- | :--- | :--- |
| Slide title | `data-name` on `<section class="slide">` | Also drives `document.title` (DS-135) |
| Bottom line | `<p class="bottom-line rise">` | One per slide, all twelve present |
| Stage | `data-stage` on the section | 0–6, so **seven stages** |
| Number | The slide's index | Printed in the eyebrow as `01 · WHY NOW` |

**Geometry, so the box arithmetic can be done on paper.** The printed page is `@page{size:1920px
1080px;margin:0}` — 1440 × 810 pt, exactly 1920 × 1080 px at 96 dpi. `--pad-x` is **96 design
units** and **`--pad-y` is 72**, so a contents page has **1728 × 936 usable units** inside the
padding. Twelve boxes on a 4 × 3 grid, gapped at `--sp-3` (26 du), gives columns of
**(1728 − 3 × 26) / 4 = 412 units**; the row height falls out of whatever the page header is
allowed, which is not designed yet and is therefore measured at plan step 4 rather than asserted
here.

> *Corrected 2026-08-08.* The row above previously read **1728 × 1080**, which subtracted `--pad-x`
> on both sides but never subtracted `--pad-y` at all. The usable height is **936**, not 1080, and
> the per-box estimate of "~432 × 360" was built on the wrong number. Recorded rather than silently
> fixed because the erroneous figure is exactly the kind that gets quoted onward (**L-08** — one
> home per fact, and this is the home).

**A design unit is not a point, and on paper it is worth less than half of one — which is the
conversion every type-size decision on this page depends on.** The stage is authored in design
units, but the reader meets **points on A4 landscape**, and [`R7`](../docs/research/R7-printable-mode.md)
records that A4 landscape is what this deck is printed on with the dialog's *fit to page* doing the
only scaling. Fitting the 1440 × 810 pt page box into A4 landscape's 841.9 × 595.3 pt is
**width-bound at 0.5847**, so:

**1 design unit = 0.75 pt × 0.5847 = 0.4385 pt printed** (and 1 pt ≈ 2.28 du).

| Design units | Printed, A4 landscape | What it is today |
| ---: | ---: | :--- |
| 14 | **6.1 pt** | — |
| 18 | 7.9 pt | `--fs-mono` — the smallest type the deck currently ships |
| 21 | 9.2 pt | — |
| 26 | 11.4 pt | `--fs-body` |
| 32 | **14.0 pt** | — |
| 40 | 17.5 pt | `--fs-bottom` |

**The slides are not uniform, and one of them is the odd one.** Stage membership runs
**1 · 1 · 2 · 2 · 3 · 2 · 1** across the seven stages. **Slide 1 carries no disclosure panel at
all**; the other eleven carry exactly one each. Any per-box mark derived from slide content has to
survive that.

### The compression rule — the owner's scaling condition, evaluated and adjusted

The owner attached this to the *one box per slide* ruling on 2026-08-08, **explicitly as suggestions
to evaluate rather than as instructions to transcribe**. Each is recorded with what it was checked
against and what it became.

| Suggested | Verdict | Why |
| :--- | :--- | :--- |
| Past twelve slides, reduce box height as much as needed | **Adopted** | Rows are the only axis with give once columns are pinned. It is also the right yielding order: a shorter box loses whitespace before it loses information. |
| No more than 4 columns | **Adopted unchanged** | Checked, and 4 is right at the boundary. A fifth column gives (1728 − 4 × 26) / 5 = **324 du ≈ 142 pt ≈ 2.0 in**, and a title that is a claim (**DS-210**) is 4–7 words — it would set at three or more lines and the box would grow taller than the row it was meant to shorten. Widening past 4 defeats the compression it was supposed to serve. |
| Text no smaller than the minimum readable | **Adopted, restated in printed points** | "Minimum readable" is a property of the reader's eye, so it has to be fixed in **points on paper**; design units convert at a rate that depends on the paper (the table above). The floor is **9 pt printed = 21 du**, which sits just above `--fs-mono`'s 7.9 pt — i.e. the contents page is not permitted to go as small as the deck's existing smallest type, because that type is a label glanced at, not a sentence read. |
| Page number 14 or bigger | **Adopted as 14 pt printed = 32 du** | **The unit was the whole question.** Read as design units, "14" prints at **6.1 pt** — below the floor in the row above and smaller than anything the deck ships, so as a *minimum* it would license exactly what the previous row forbids. Read as points it is a real floor, and it makes the number the largest mandated element in the box. That is correct here and follows from the ruling: the number is the handle a paper reader navigates by, and it is the one thing on the box that the ribbon never had to provide. |

**What yields, in order, and what never does.** Gaps first, then the bottom line's size down to the
9 pt floor, then the bottom line clamps to a line count. **A slide is never dropped from the page
and never truncated out of it** — a contents page that silently omits a slide is worse than no
contents page, because it is confidently wrong about the shape of the argument. Clamping a bottom
line is acceptable where dropping a box is not: the page is a map, and the unclamped sentence is
still on the slide's own page a few sheets later.

**Where this stops, and what happens then, is measured and not guessed.** When the bottom line has
reached the floor and clamped to one line and the rows still do not fit, the single-page bound is
exceeded. Plan step 6 measures the slide count at which that happens. The presumptive answer beyond
it is **a second contents page**, not truncation — but it is presumptive, it is not specified here,
and if the measurement puts the bound comfortably beyond any deck this plugin targets then the
question costs nothing and is closed by the number.

#### The bound, measured 2026-08-08

Measured by [`tools/deck/contents_bound.py`](../tools/deck/contents_bound.py), which drives the same
real, offline Chrome `render.py` uses and self-tests before reporting. It lifts the deck's own
`@media print` rules onto screen **through the CSSOM** — the rules themselves, not a copy, because
the copy is what drifts — then grows the grid and reads the geometry back out of the DOM. The grid
gets **780.3 du** of the page's 936 usable units, the rest going to the head and the screen-only
line. Because rows are `ceil(n / 4)`, the result is a **step function, not a curve**:

| Rows | Slides | Box height | Description visible | Verdict |
| ---: | :--- | ---: | ---: | :--- |
| 3 | 9–12 | 242.8 du (106 pt) | 3 lines | Comfortable — the reference deck sits here |
| 4 | 13–**16** | 175.6 du (77 pt) | 1.55 lines | **Holds.** Number, title and a readable description |
| 5 | 17–20 | 135.3 du (59 pt) | 0.19 lines | Number and title intact, **description gone** |
| 6 | 21–24 | 108.4 du (48 pt) | 0 | Number and title intact, description gone |
| 7+ | **25+** | 89.2 du (39 pt) | 0 | **Breaks — the title itself clips** |

**So there are two numbers, and conflating them would be the mistake.**

- **16 slides is the bound** — the largest deck for which the page still does its whole job. Past
  it the description disappears and the page degrades to a numbered title list, which is still a
  usable map but is no longer what was specified.
- **24 slides is the hard limit.** At 25 the box is physically too small for the padding, the number
  row and one line of title — **96 du of content in an 89 du box** — and no compression resolves
  that. This is arithmetic, not a stylesheet defect.

**A defect was found and fixed by this measurement.** The flex column originally shrank every child
alike, so past 24 slides the **title** was squeezed rather than the description — breaking
**DS-226**'s invariant that a box may lose its description but never its entry. `flex:none` on the
number row and the title confines all compression to the description. It does not raise the hard
limit, and it was not expected to: it makes the failure **sharp and predictable** — the title is
either fully rendered or the box is genuinely too small — instead of the entry quietly eroding
across a range of deck sizes.

**What this settles, and what it leaves open.** The target case is twelve slides and the bound is
sixteen, so **the second contents page is not built** and the reference deck conforms with room to
spare. It is not dismissed either: a deck of 25 or more slides cannot satisfy DS-226 by compression
alone, and that gap is [T-036](T-036-the-second-contents-page-for-long-decks.md) rather than a
silence.

*This is a layout measurement, taken in a real browser at the true page-box geometry. It is not a
printed measurement, and it does not discharge the print-and-look criterion below.*

### Two traps in the print block, both of which have already cost a round

1. **Where the contents section goes in the DOM is load-bearing, and putting it last reintroduces
   the blank thirteenth page.** The stage is `<main class="stage">` containing exactly twelve
   `<section class="slide">`, and the print block cancels the last slide's page break with
   **`section.slide:last-of-type`**. That selector matches the last `<section>` **among its
   siblings by element type** — so adding a `<section class="contents">` *after* slide 12 makes the
   twelfth slide no longer the last section, the selector matches **nothing**, and the empty
   thirteenth page T-018 spent a printed round finding comes straight back. **Put the contents
   section first**, which is also where it belongs, or use a non-`<section>` element, or fix the
   selector — but decide it deliberately. This is DS-222's corollary, live.
2. **Do not disturb two strings the tooling anchors on.**
   [`tools/deck/print_variants.py`](../tools/deck/print_variants.py) finds the block to replace with
   a regex starting at the comment `/* printing is a mode the user forces on`, and its self-test
   asserts `[hidden]{display:block!important` is present. Both must survive any restructuring of the
   print CSS, or the script fails its own test — which is exactly how it failed when
   [T-032](T-032-adopt-the-paginated-print-mode-in-the-reference-deck.md) adopted the block.

**One more thing print already does to the clones.** `.rise` is forced to `opacity:1` with
`animation:none` in print, so bottom lines cloned into a contents page inherit a resolved state
rather than a pre-animation one. Nothing to do — stated so it is not re-discovered.

**Acceptance criteria**
- [ ] The printed deck is *n* + 1 pages: a contents page, then one page per slide, still with no
      blank page at either end
- [ ] **One box per slide** — twelve boxes for the reference deck, never one per stage
- [ ] Every box carries the slide's number, its title and its bottom line, **read from the slide**
      rather than authored — changing a slide's bottom line changes the contents page
- [ ] Every box carries a **line icon keyed to `data-stage`** — seven icons, drawn in the deck's
      existing icon vocabulary, no raster and no scaled slide clone (**DS-110**)
- [ ] The fields are read through a **slide manifest** that the on-screen overlay index can consume
      unchanged, so the two renderings cannot derive the same fact twice (**L-08**)
- [ ] The page states in one line that detail behind disclosure is screen-only
- [ ] **The grid is at most 4 columns at any slide count**, and rows are what grow
- [ ] **No text on the page prints below 9 pt on A4 landscape (21 du)**, and the **page number
      prints at 14 pt or larger (32 du)** — both verified by measurement on the printed page, not by
      reading the stylesheet
- [ ] **No slide is ever absent from the page.** Under compression a bottom line may clamp; a box
      may not disappear
- [ ] The whole thing fits one page at twelve slides, and **the number of slides at which it stops
      fitting is measured and written down**
- [ ] Screen rendering is byte-identical in behaviour — the page exists only under `@media print`
- [ ] Printed from a double-clicked file and **looked at** (**L-01**), not headless (**L-35**)
- [ ] `audit.py`, both variant suites and `print_variants.py` still pass

**Open questions — all three answered by the owner 2026-08-08. None is open.**

- ~~One box per slide, or one per stage?~~ **One box per slide.** The reason for differing from
  [T-035](T-035-the-ruler-navigator.md), should it tick per stage, is stated and is not
  arbitrary: **paper is navigated by page number and the ribbon is not**, so the rendering that
  reaches a paper reader is the one that must carry a per-page handle. The owner attached a
  scaling condition to this answer, which is written up as *The compression rule* below.
- ~~Icon, or nothing at all?~~ **A line icon per stage** — seven icons, keyed to `data-stage`,
  drawn in the vocabulary the deck already uses on the cost slide and the comparison header.
  Keying the mark to the **stage** rather than to slide content also disposes of the non-uniformity
  recorded above: it no longer matters that slide 1 carries no disclosure panel where the other
  eleven carry one, because no mark is derived from panel content.
- ~~The `DESIGN-SYSTEM.md` §5.4 amendment.~~ **Taken as worded**, below.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | ~~Take the two open questions, and the §5.4 amendment~~ — **done 2026-08-08** | the three rulings, written into §1 |
| 2 | Build the **slide manifest** — number, title, bottom line, stage, mark — derived from the slides, generalising the existing `firstSlideOfStage()`. **This is the step [T-035](T-035-the-ruler-navigator.md) consumes**, so it is built to be consumed and not inlined into the page | a manifest function in the deck |
| 3 | Draw **seven line icons**, one per stage, in the deck's existing icon vocabulary | inline SVG, one symbol per stage |
| 4 | Build the contents page from the manifest, print-only, with the section placed **first** in the DOM — trap 1 | edited deck |
| 5 | Implement the compression rule — 4 columns, growing rows, the 9 pt / 21 du floor, the 14 pt / 32 du number | the print CSS |
| 6 | Measure the slide count at which one page stops holding, on a deck longer than twelve, and **write the number into §1** | the bound |
| 7 | Amend `DESIGN-SYSTEM.md` §5.4 and [T-005](T-005-build-check-the-gate-the-deck-must-pass.md)'s print row | ruleset, gate |
| 8 | Re-run `audit.py`, both variant suites and `print_variants.py` | green gates, or a named failure |
| 9 | Print from a double-click and **look at every page** (**L-01**, **L-35**) | printed artefact, and the §4 verdicts |

**Approach decisions**

- **The manifest is built before the page, and as a separate thing, even though only one consumer
  exists today.** Building the page first and factoring the manifest out later is the same amount of
  work done in the order that permits drift in between (**L-08**), and
  [T-035](T-035-the-ruler-navigator.md) is specified against a manifest that this task is the one
  scheduled to produce.
- **The icons are drawn before the page rather than stubbed.** A placeholder mark makes the box
  arithmetic in steps 5 and 6 measure a box that is not the one shipping, which would put the
  measured bound at step 6 in question.
- **The bound (step 6) is measured on a longer deck built for the purpose, not on the reference
  deck.** The reference deck is twelve slides and is not being lengthened to answer this; the
  measurement needs a deck that is deliberately too long, and that deck is a scratch input, not a
  repository artefact.
- **Steps 7 and 8 come before step 9, and step 9 is last on purpose.** Printing is the expensive,
  manual, non-scriptable check (**L-35**), so everything mechanical is green before a sheet is
  looked at.

## 3. Implement

**Decisions & assumptions**

- **Six of the seven stage marks reuse symbols already in the sprite; only one was drawn.** —
  The plan said "draw seven line icons". On reading the sprite, nine symbols were already declared
  and **only five were used** — `i-corridor`, `i-growth`, `i-gate` and `i-ask` were dead. The stage
  set is structural (Claim · Why now · The problem · The choice · The evidence · The cost · The
  ask), and six of the seven had an apt structural glyph already present: flag, calendar-with-clock,
  clock, trend, warning triangle, check-circle. Only **The choice** had none, so `i-choice`
  (a split/fork) was added. Seven new icons would have been a second vocabulary beside the deck's
  own for no gain. — 2026-08-08
- **Topical glyphs were deliberately *not* used as stage marks.** `i-bike`, `i-bus` and
  `i-corridor` are about this deck's subject, and a stage mark is about deck *structure*. Keying a
  structural mark to a topical glyph would bake one deck's topic into the theme layer, which is
  what CLAUDE.md rule 4 exists to prevent. `i-corridor` therefore stays unused. — 2026-08-08
- **Each box repeats the slide's own eyebrow string (`01 · WHY NOW`) rather than the number
  alone.** An unlabelled glyph on paper is decoration — there is no legend to consult and nothing
  to hover — and the stage name makes the icon mean something. It costs one line and it makes the
  box and its page carry the identical string, so matching one to the other is exact. — 2026-08-08
- **The contents rules live inside the deck's existing print block, not in a second one.** —
  [`print_variants.py`](../tools/deck/print_variants.py) replaces that whole block when it builds
  the T-018 variants, so putting the rules inside it strips them from both variants **by
  construction**: the paginated-vs-reflow comparison keeps measuring a pagination strategy rather
  than silently acquiring a feature on one side. The script's docstring claimed the paginated
  variant *was* the deck's print stylesheet; that claim is now false, so it was amended to state
  the divergence and the reason. — 2026-08-08
- **`flex:none` on the number row and the title.** Found by measurement, not by review: the flex
  column shrank every child alike, so past 24 slides the **title** eroded rather than the
  description — breaking **DS-226**'s invariant that a box may lose its description but never its
  entry. It does not raise the hard limit and was not expected to; it makes the boundary sharp
  instead of letting entries decay across a range of deck sizes. — 2026-08-08
- **The second contents page was not built, and was raised as
  [T-036](T-036-the-second-contents-page-for-long-decks.md) instead.** §1 made it presumptive and
  said the measurement decides. The measurement puts the bound at 16 against a target of 12, so
  building it now would be building for a deck size this project does not produce — but DS-226
  states an invariant that is unimplementable past 24 slides, and a rule with a known
  unimplementable range needs a task rather than a silence. — 2026-08-08
- **The description clamp is four lines, not three, and only looking at the page found it.** —
  Every gate passed and every measurement was green while **four of the twelve descriptions were
  ellipsised mid-word** — "…the only meeting that can commi…", "…spending money on that…", "…16 Old
  Quarter stations if the…", "…measured by someone outsid…". The box had room: ~131 du below the
  title at twelve slides, and a line costs 29.7, so 4.4 lines fit while a 3-line clamp left that
  room empty. Truncating a bottom line at the size the deck actually ships is the map misstating
  the argument (**DS-211**), and no gate here can see it. Raising the clamp to 4 completes all
  twelve and **does not move the bound**, since past twelve the box rather than the clamp is the
  binding constraint — re-measured to confirm, 16 and 24 unchanged. **This is L-01 paying for
  itself**: a rendering-level defect invisible to `audit.py`, to both variant suites and to the
  geometry measurement, found in the first minute of looking at the page. — 2026-08-08
- **The bound was re-measured on the sanctioned instrument after being taken in a preview pane.**
  The pane reported `window.innerWidth` as **0** — L-06/L-15's failure exactly. Its numbers for
  this element happened to be right, because the contents page is a fixed 1920 × 1080 box and its
  geometry is viewport-independent, but *right by luck on one element* is not an instrument. Both
  runs agree to the decimal. — 2026-08-08

**Outputs produced**
- [`examples/reference-deck.html`](../examples/reference-deck.html) — the manifest, the generated
  contents page, the `i-choice` symbol, and the print CSS
- [`tools/deck/contents_bound.py`](../tools/deck/contents_bound.py) — the bound, re-measurable
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — §5.4 amended, DS-225 and DS-226 added
- [`tools/deck/print_variants.py`](../tools/deck/print_variants.py) — docstring corrected
- [`T-005`](T-005-build-check-the-gate-the-deck-must-pass.md) — the print row now says `n` + 1

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| *n* + 1 pages, no blank page at either end | **not yet** | The mechanism is verified, the paper is not. `section.slide:last-of-type` was checked **at runtime in the browser, not by reading the selector**: with the contents section inserted first it still matches slide 12 (`matchesRule: true`), which is the condition that keeps the trailing blank page away. The page *count* is only provable on paper — see the print row below |
| One box per slide, never one per stage | **met** | 12 boxes for 12 slides |
| Number, title and bottom line read from the slide | **met** | `manifest()` reads `data-name` and `.bottom-line` off each section; box 1 came back as `01 / Claim / "Buy frequency before bikes" / "Spend the $5.6M grant on bus frequency…"`. Nothing is authored, so changing a bottom line changes the page. **All twelve descriptions render complete** — four were being ellipsised mid-word until the clamp was corrected, which only looking found (§3) |
| A line icon keyed to `data-stage`, no raster, no slide clone | **met** | `STAGE_ICON` is indexed by stage; box 1 resolves to `#i-gate`. Six symbols were already in the sprite, one (`i-choice`) was drawn — see §3 |
| Fields read through a manifest the overlay index can consume unchanged | **met** | `manifest()` returns number, title, bottom line, stage, stage name and mark, and is a separate function from the renderer that consumes it. [T-035](T-035-the-ruler-navigator.md) consumes it without change |
| One line stating detail is screen-only | **met** | `.contents-foot`, generated onto the page — the first surface in this project that states R7 §5's loss to the person **holding** the pages rather than to whoever was about to print |
| At most 4 columns at any slide count | **met** | Pinned in CSS; the measurement asserts `columns == 4` before reporting, so a change to the grid fails the instrument rather than skewing it |
| No text below 9 pt / 21 du; page number ≥ 14 pt / 32 du | **partly** | Set correctly in the stylesheet — nothing on the page is authored below 21 du and `.cnum` is 32 du — and the arithmetic behind the conversion is written up in §1. **Verified as CSS, not on paper**; the criterion asks for measurement on the printed page, which is the print row below |
| No slide ever absent from the page | **met, within the implemented range** | Number and title survive every compression to 24 slides. Past 24 the box is physically too small (89 du for 96 du of content) and an entry clips — the limit is measured, stated in DS-226, and raised as [T-036](T-036-the-second-contents-page-for-long-decks.md) rather than left to be found |
| Fits one page at twelve, **and the count where it stops fitting is measured and written down** | **met** | [`contents_bound.py`](../tools/deck/contents_bound.py), real offline Chrome, self-testing. **Bound 16, hard limit 24**, full table in §1. At twelve the box is 242.8 du with three full lines of description — comfortable, not marginal |
| Screen rendering unchanged; the page exists only under `@media print` | **met** | One screen rule, `.contents{display:none}`; everything else is inside `@media print`. Confirmed in the browser: computed `display` is `none`, and no console errors |
| Printed from a double-clicked file and looked at (**L-01**, **L-35**) | **not done** | **Owed, and it is the owner's to do** — I cannot double-click a file, and synthesising the gesture would be the L-35 failure in miniature. This is what holds the task at `review` |
| `audit.py`, both variant suites and `print_variants.py` still pass | **met** | `audit.py` 0 mechanical failures · `deliverable_variants.py` 7/7 · `contract_variants.py` 7/7 · `check_scaffold.py` OK · `print_variants.py` self-test ok, both anchor strings intact |

**Child fix tasks raised**
- [T-036](T-036-the-second-contents-page-for-long-decks.md) — continue the contents page onto a
  second sheet past the measured hard limit.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-08 | → review | **Built, gated and measured; one criterion is owed and it is the owner's.** The deck gained a `manifest()` — number, title, bottom line, stage and mark, read off the slides — and the contents page is a *rendering* of it, so [T-035](T-035-the-ruler-navigator.md) consumes the same derivation rather than making a second one (**L-08**). Three findings changed the work as specified. **The icons were mostly already there**: the sprite declared nine symbols and used five, and six of the seven structural stages had an apt glyph already present, so one (`i-choice`) was drawn instead of seven — and the topical glyphs were deliberately left out of a structural mark. **A defect surfaced only under measurement**: the flex column shrank every child alike, so past 24 slides the *title* eroded rather than the description, breaking DS-226's invariant; `flex:none` confines compression to the description and makes the boundary sharp. **And the bound came out at 16 with a hard limit of 24**, against a target deck of 12 — so the second contents page is not built and is raised as [T-036](T-036-the-second-contents-page-for-long-decks.md), because a rule with a known unimplementable range needs a task, not a silence. The bound was first taken in a preview pane, which reported `window.innerWidth` as **0** (**L-06**/**L-15**); it was re-measured on real offline Chrome through the new [`contents_bound.py`](../tools/deck/contents_bound.py), and the two agree to the decimal. `DESIGN-SYSTEM.md` §5.4 was amended as the owner took it and gained **DS-225** and **DS-226**; T-005's print row now says `n` + 1; `print_variants.py`'s docstring claimed to be byte-identical to the deck's print block and no longer is, so it was corrected rather than left to drift. All five gates pass. **What is not done is the one thing no script can do**: the deck has not been printed from a double-click and looked at (**L-01**, **L-35**), which is why this is `review` and not `done`. |
| 2026-08-08 | → planned | **§2 filled, and three approach decisions recorded with it.** The manifest is step 2 rather than a by-product of the page, because building the page first and factoring the manifest out afterwards is the same work in the order that lets the two derivations drift (**L-08**) and [T-035](T-035-the-ruler-navigator.md) is already specified against it. The icons are drawn before the page rather than stubbed, so the box arithmetic at steps 5–6 measures the box that ships. The bound at step 6 is measured on a **scratch deck built deliberately too long**, not by lengthening the reference deck. Printing is last because it is the expensive manual check (**L-35**) and everything mechanical is green before a sheet is looked at. |
| 2026-08-08 | → specified | **All three open questions answered by the owner, and §1 gained a measurement correction plus a conversion the task cannot be built without.** The rulings: **one box per slide** (the differing answer from a possible per-stage [T-035](T-035-the-ruler-navigator.md) is defended rather than assumed — paper is navigated by page number, the ribbon is not); **a line icon per stage**, which as a side effect disposes of the slide-1-has-no-disclosure-panel non-uniformity, since no mark now derives from panel content; and **the §5.4 amendment taken as worded**. **A wrong number was corrected**: §1 said the usable area was 1728 × 1080, having subtracted `--pad-x` on both sides but never `--pad-y` — it is **1728 × 936**, and the "~432 × 360" per-box estimate rested on it. **And the conversion the type-size ruling turns on was missing entirely**: the stage is authored in design units but the reader meets points on A4 landscape, where fit-to-page is width-bound at 0.5847, so **1 du = 0.4385 pt printed**. That is what settled the owner's "page number 14 or bigger" — as design units it prints at **6.1 pt**, below any readable floor and smaller than `--fs-mono`, so it would have licensed the opposite of what it was asked for; taken as **points** it is a real floor at 32 du. The owner offered the scaling conditions as suggestions to evaluate; all four are recorded in *The compression rule* with what each was checked against, three adopted and one restated in different units. |
| 2026-08-08 | (no change) | **§1 gained what the raising session had measured but never written down** — where each field the page needs actually lives in the markup, the printed geometry (**1728 × 1080 usable design units** inside `--pad-x`, on a page that is 1440 × 810 pt), the uneven stage membership **1 · 1 · 2 · 2 · 3 · 2 · 1**, and the fact that **slide 1 carries no disclosure panel** where the other eleven carry one, so any mark derived from slide content meets a non-uniform set. **Two traps are recorded because both have already cost a printed round elsewhere**: `section.slide:last-of-type` matches by *element type*, so a `<section>` placed after slide 12 makes it match nothing and silently reinstates T-018's blank thirteenth page — DS-222's corollary, live; and [`print_variants.py`](../tools/deck/print_variants.py) anchors on two strings inside the print block, which is exactly how it broke when [T-032](T-032-adopt-the-paginated-print-mode-in-the-reference-deck.md) adopted that block. **None of this changes the specification** — it takes the measurements off the next session's critical path so the detailed spec starts from facts rather than from a re-derivation. |
| 2026-08-08 | (no change) | **Answered the owner's question — the on-screen overlay index and this page share their content but not their rendering, and the shared part is a slide manifest rather than a page.** Both need each slide's number, title, bottom line, stage and mark, and deriving that twice is how the two drift (**L-08**); `buildDoc()` already sets the precedent of cloning slides instead of re-authoring them. What differs is real and should not be flattened: this page **must fit one page** and is read once to orient, the overlay scrolls and is read repeatedly to jump; this page owes the screen-only line, the overlay owes a current-position highlight; and **the mark can legitimately differ** — a slide clone is a texture at 0.22 scale on paper, but on screen it has no resolution limit and can enlarge on hover. So whichever of this and [T-035](T-035-the-ruler-navigator.md) lands first builds the manifest and the other consumes it. |
| 2026-08-08 | → proposed | Raised by the owner on reading the printed deck from [T-032](T-032-adopt-the-paginated-print-mode-in-the-reference-deck.md). Recorded with two arguments the request did not make — **the description is free**, because DS-211's bottom line already exists on every slide and reading it means the page cannot drift from the deck; and **it is the only surface that reaches a paper reader**, so the disclosure loss finally has somewhere to be stated to the person actually holding the pages. One amendment is owed and is raised rather than taken (**L-37**): §5.4 says the printable mode *is* the paginated stage, and a contents page is a printed page that is not a slide. The thumbnail option is argued against rather than dropped: at twelve boxes a slide clone renders at ~0.22 scale, which puts body text at five design units — a texture that looks like content. |
