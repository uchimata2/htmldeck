---
id: T-204
title: An instrument for mark collisions, so a person is not the only thing that can see one
type: deliverable
status: done
phase: review
parent: null
blocked_by: []
related: [T-113, T-203, T-205, T-206, T-207]
work_package: PH3
owner: the project owner
business_value: high
effort: m
created: 2026-08-21
updated: 2026-08-21
shipped_in: unreleased
deliverables: [tools/deck/markhits.py, docs/DESIGN-SYSTEM.md]
---

# T-204 — An instrument for mark collisions, so a person is not the only thing that can see one

## 1. Specify

**Outcome**
A checker that fails a deck when two things that should not overlap do. Three of
[T-203](T-203-four-chart-defects-the-decks-look-missed.md)'s four defects are inside its reach, and
so is the fourth if it also measures a slide's content against its own bottom line.

**Six subjects now, not four — added 2026-08-21 when T-203 closed.** Its closing look covered all
twelve slides and found **two more of this class**, on slides 4 and 10, both of which two earlier
human looks had passed:
[T-207](T-207-two-more-mark-collisions-the-twelve-slide-look-found.md). That strengthens the
argument here rather than changing it — a label over a line and two labels over each other are
exactly what this checker is for, and the seed corpus is now six.

**And T-203 left a working sketch to start from, not a blank page.** Five geometry identities now
live above `selftest()` in
[`tools/examples/portfolio_charts.py`](../tools/examples/portfolio_charts.py), with readers that
take marks back off the emitted SVG (`read_lines`, `read_labels`, `read_nodes`, `seg_hits_box`,
`box_hits_disc`). They are deliberately narrow — one deck, no vocabulary — but the segment-versus-box
and box-versus-disc arithmetic is the same arithmetic this task needs, and it is proven against
seeded defects. **Read it before writing a second copy** (**L-13**); what is missing is generality,
not geometry.

**The gap, stated as a measurement rather than as a worry**
On 2026-08-21 the portfolio-review deck passed `check.py` (0 failures across 91 decided rules),
`check_all.py` (35 commands, 0 failures) and `printgeom.py` (PRINT-2, PRINT-3) while carrying
**fifteen** chart defects. Nine were found by looking; four more by the owner looking at the same
deck afterwards; **two more by a third look, over all twelve slides, after those four were fixed**
(T-207). **Nothing in this repository can see a mark overlap another mark**, so the only instrument
is a person — and three separate people-looks each missed some, which is a stronger statement than
the one this paragraph originally made. *Thirteen until 2026-08-21; the number is the count of
defects found, so it rises whenever anyone looks again, and that is the point.*

**Why this is the cheaper answer than the one it competes with**
[R9](../docs/research/R9-embeddable-chart-library-versus-hand-authored-svg.md) §6 offers the same
evidence as the strongest argument *for* adopting a chart library: connector attachment, label
placement and axis breaks are what a library owns for free. But every one of the four was fixable by
hand in minutes once seen, and `spread()` — the label separator this repository already has — is
twelve lines. **The gap is detection, not capability**, and a detector is a fraction of the
165,077 bytes the library costs. That argument is this task's premise and R9 §7 should be re-read
after it ships, which is [T-205](T-205-correct-r9s-gate-7-scoring-and-its-account-of-looking.md).

**What it has to decide**
- **Mark against mark.** Two filled marks intersecting where neither is a stack segment and neither
  declares an overlap.
- **Text against line.** A text run whose box crosses a drawn line or path — slide 7's labels over
  the reference diagonal, slide 11's axis through the gate's second label.
- **Connector against its own bar.** A line that claims to join two marks and touches neither at the
  edge it names — slide 6. This one may be out of reach generically; if so, say so and excuse it
  with a reason rather than approximating it.
- **Content against the frame.** A slide's body reaching the bottom line or the chrome — slide 9.
  This is not a mark collision and may want its own row.

**The calibration rule this project already has, and why it applies here**
[T-115](T-115-the-specification-can-assert-a-layout-the-shell-cannot-honour.md) shipped **no checker**
because its candidate produced two false alarms against one hit, and
[T-118](T-118-a-style-must-mean-the-same-thing-in-the-reading-view.md)
shipped one only after a second count took its false alarms to zero. **Count this one's false alarms
against its true hits on all four shipped decks before deciding it ships**, and be willing to
report rather than gate. A nagging geometry check teaches the next reader to re-run until green —
the failure [T-183](T-183-ds-063-failed-once-in-four-full-gate-runs-on-an-unchanged-tree.md) is named for, in a new place.

**Scope**
- In: the checker, its self-test, and its wiring into `check.py` or `check_all.py` per the
  calibration outcome.
- In: a seeded-defect run in **both** directions (**L-125**) — the four known defects trip it, and a
  deck with none does not.
- In: the four shipped decks as the false-alarm corpus.
- Out: fixing the four defects. That is [T-203](T-203-four-chart-defects-the-decks-look-missed.md),
  and it should land **first** so this task has four real subjects to seed from and a clean deck to
  measure false alarms against.
- Out: a new design-system rule, unless the calibration says the check should gate — in which case
  it owes one, because a gate with no rule behind it is a preference.

**Inputs**
- [`tools/deck/figgrid.py`](../tools/deck/figgrid.py) — the nearest existing instrument: it measures
  a diagram's ink against the text column and **reports rather than gates**. The precedent for both
  the geometry and the disposition.
- [`tools/deck/render.py`](../tools/deck/render.py) — `getScreenCTM` and box geometry in real Chrome;
  **L-123** warns that a number read from the DOM is in a coordinate system you have not
  established.
- [`tools/deck/audit.py`](../tools/deck/audit.py) — DS-219's existing on-mark label test, which is
  the one overlap this project already permits and the check must not report.

**Acceptance criteria**
- [ ] The four defects in T-203 are each either **caught** or **excused with a reason**, and the
      partition is stated — no defect is silently out of scope.
- [ ] False alarms counted against true hits across all four shipped decks, with the numbers in the
      record, and the ship-or-report decision taken from that count rather than from preference.
- [ ] The seeded run passes in both directions.
- [ ] `python tools/check_all.py` green, with the new tool classified — an unclassified tool fails
      the run by design.
- [ ] Whatever it decides is written where a rule lives, not only in the tool.

**Open questions**
- Whether it renders or reads the markup. Rendering catches what CSS does and costs a Chrome run;
  reading the SVG catches what the generator emitted and cannot see the composition. The four
  defects split across both, which suggests rendering — and **L-123** says that is the expensive
  answer to get right.
- Whether *content against the frame* is this tool's or a second one's.

## 2. Plan

**The open question is answered first, because everything else follows from it: it renders.**
§1 offers reading the markup or rendering, and says the defects split across both. They do, but not
evenly — a label's box is *glyph* geometry, and only a browser with the real face loaded knows how
wide a string is. The sketch estimates it as `len(text) * font_px * 0.62`, which is honest for one
generator's output and cannot be the basis of a check run against decks it did not write. **L-123**
is the cost, and the answer to it is to take every number out of one coordinate system: the slide's
own rect, via `getScreenCTM` for SVG geometry and `getBoundingClientRect` for boxes.

1. **Reuse the predicates, replace the readers.** `seg_hits_box` (Liang-Barsky) and `box_hits_disc`
   are proven against seeded defects and are the arithmetic this needs. The *readers* are what has
   to go: regexes over one generator's attribute order cannot read a deck it did not emit. So the
   new tool owns the geometry, and [`tools/examples/portfolio_charts.py`](../tools/examples/portfolio_charts.py)
   **imports it and deletes its copies** — the general owning the arithmetic and the specific
   borrowing it, rather than two homes (**L-13**). The generator already puts `tools/assets` on its
   path, so the direction is established.
2. **Extract typed geometry, not boxes.** A diagonal line's bounding box is mostly empty, so
   box-versus-box would report every label near a sloping axis. Lines come back as **segments**,
   text as **boxes**, circles as **discs**, and each pair is decided by the predicate that fits it.
   That is the difference between an instrument and a nuisance.
3. **Decide two classes and excuse the rest, explicitly.** *Text against text* and *text against
   line* are decidable and cover four of the six subjects. Slide 6's connector-against-its-own-bar
   needs to know which bar a line *claims* to join, which is authoring intent and not in the
   markup — §1 already allows excusing it with a reason. Slide 9's content-against-the-frame is not
   a mark collision and belongs to whatever owns the frame. The partition gets stated, not implied.
4. **Do not report the overlaps this project permits.** DS-219's on-mark label is deliberate, so
   text over a *filled* mark is out of the checker's reach by construction rather than by a special
   case — the tool only ever compares text to text and text to line.
5. **Calibrate before deciding disposition, per T-115 and T-118.** Run all four shipped decks, count
   false alarms against true hits, and take the ship-or-report decision from that count.
   [`figgrid.py`](../tools/deck/figgrid.py) is the precedent in both directions: it reported until
   the decks were clean, then gated.
6. **The live true positives are better than seeded ones, and they already exist.** T-207's two
   defects are unfixed in the shipped deck, so a correct instrument finds them **without anything
   being seeded** — an independent instrument reproducing what a third human look found. Seeding
   covers the other direction (**L-125**): a clean fixture must stay clean.
7. **Born with the motion pin.** T-206 closed hours before this, and **L-128** is why: a probe that
   measures an unsettled page can agree with itself and be wrong. This probe pins motion in its own
   source rather than waiting for [T-209](T-209-six-more-probes-measure-a-page-whose-entrance-never-ran.md)
   to sweep the six that do not.

## 3. Implement

**Decisions & assumptions**
- **It renders, and it extracts typed geometry** — 2026-08-21. Lines come back as segments through
  `getScreenCTM()`, text as boxes through `getBoundingClientRect()`, curves sampled with
  `getPointAtLength()`. A diagonal's bounding box is mostly empty; box-versus-box would report every
  label near a sloping axis, which is a nuisance rather than an instrument.
- **The predicates moved rather than being copied** — 2026-08-21. `seg_hits_box` and `box_hits_disc`
  now live in `markhits.py` and [`portfolio_charts.py`](../tools/examples/portfolio_charts.py)
  imports them. The general tool owns the arithmetic; the deck-specific caller borrows it
  (**L-13**). The generator's identities pass unchanged and the deck rebuilds byte-identical, which
  is what makes the move a refactor rather than a change.
- **Both thresholds are fractions of the mark, never design units** — 2026-08-21. An absolute figure
  states one face at one size and has to be re-tuned for every deck that sets labels larger, which
  is how a tolerance stops meaning anything.
- **Only text-against-text gates. Text-against-line reports** — 2026-08-21, from the count below and
  T-115's rule, not from caution.
- **The tool was born with the motion pin** ([T-206](T-206-ds-063-gives-a-different-verdict-on-identical-input.md),
  **L-128**) rather than waiting for [T-209](T-209-six-more-probes-measure-a-page-whose-entrance-never-ran.md)
  to sweep the six probes that lack one.

**Outputs produced**
- [`tools/deck/markhits.py`](../tools/deck/markhits.py) — the checker, its probe, its predicates and
  a browser-free self-test running both directions.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — **DS-244**, the rule. DS-242 and DS-243 were
  already taken; the tool was written against DS-242 and renumbered before anything shipped.
- [`tools/deck/check.py`](../tools/deck/check.py), [`tools/deck/audit.py`](../tools/deck/audit.py),
  [`tools/check_all.py`](../tools/check_all.py) — gathered on every deck, exercised by the
  absent-subject fixture, and classified.

**The calibration, which is the finding and not a formality.**

Run on all four shipped decks, 30 slides carrying a diagram, 2026-08-21:

| Comparison | Fires | Real defects | Disposition |
| :--- | ---: | ---: | :--- |
| **text against text** | 1 | **1** | **gates** |
| text against line | 16 | 1 | **reports, never fails a deck** |

**The one text-against-text hit was real, and nobody had told the tool about it.** Pointed at the
shipped deck it named slide 4 — `Renewables 31 → 52` over `+21 points`, at 39% of the smaller box —
which is exactly what a third human look had found and filed as
[T-207](T-207-two-more-mark-collisions-the-twelve-slide-look-found.md). Unseeded, independent, and
the strongest evidence this task could produce for itself.

**The text-against-line half fails T-115's bar, and the obvious rescue inverts.** Fifteen of its
sixteen firings are a deck setting a label on the line it names — eight route names along their own
edges on one reference-deck slide alone — which is ordinary chart vocabulary and reads perfectly.
The rescue everyone reaches for is *only count it if the line crosses the middle of the label*. It
was implemented, measured, and **it is backwards**: the smallest core fraction at which each
crossing still registers is **0.951** for the one real defect and **0.001** for the deliberate
placements. A label set on its own line is geometrically indistinguishable from a label a line ran
over, because what separates them is intent, and intent is not in the drawing. T-115 shipped no
checker at two false alarms against one hit; this would have been fifteen.

**Two defects in the instrument, both found by running it rather than by reading it.**

- A **nested `<svg>` was collected twice**, so one slide reported eight collisions where it has
  four. `querySelectorAll('svg')` returns the outer element and the inner one.
- **Only `<line>` was read**, so the drawdown — a `<path>` — was invisible, and T-207's slide 10
  went unfound on the first run. Curves are sampled now, and a line is decided by *paint* (stroked,
  unfilled) rather than by tag name, which keeps DS-219's permitted on-mark label out of reach by
  construction instead of by a list of element names that would go stale.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :--- | :--- |
| The four defects in T-203 are each **caught** or **excused with a reason**, and the partition is stated | met | Stated in the tool's docstring and in DS-244. **Caught:** label over label (slide 4's class) and label over line (slides 7 and 11's class) — the second measured and reported rather than gated, for the count above. **Excused with a reason:** slide 6's connector-against-its-own-bar needs to know which bar a line *claims* to join, which is authoring intent and is not in the markup; slide 9's content-against-the-frame is not a mark collision and belongs to whatever owns the frame. Text over a *filled* mark is DS-219's permitted on-mark label, and the tool never forms that pair |
| False alarms counted against true hits across all four shipped decks, numbers in the record, disposition taken from the count | met | Section 3's table, over 30 slides with a diagram. Gating half **1 hit, 0 false alarms**; reporting half **16 firings, 1 real**. Both dispositions follow from those rows and T-115's precedent, and the depth measurement that refuted the obvious rescue is recorded with its numbers |
| The seeded run passes in both directions (**L-125**) | met | `markhits.self_test()`, browser-free, both ways: a clean slide reports nothing; two labels on top of each other are caught; a label crossed by its line is measured and does **not** reach the gate; a paragraph inside a figure is not read as a label; a diagonal's bounding box covering a distant label is **not** a hit, which is the false alarm the design exists to avoid. Plus the absence discipline — no deck declines, no diagram passes with its denominator, a failed render is never a pass |
| `python tools/check_all.py` green, with the new tool classified | met | See the log row. `markhits.py` is classified in `check_all.py` as running inside `check.py`, and registered in `audit.py`'s absent-subject fixture — which **refused the first attempt to wire it in** until it was, which is that fixture working |
| Whatever it decides is written where a rule lives, not only in the tool | met | **DS-244** in [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) section 4, carrying the threshold, why it is a fraction, the explicit statement that a label on a line is deliberately not this rule, and the calibration counts |

**Child fix tasks raised**
- none of this task's own. It **raised the gate on a defect that already had a task**:
  [T-207](T-207-two-more-mark-collisions-the-twelve-slide-look-found.md), fixed immediately after so
  DS-244 could land green rather than red. That ordering is
  [`figgrid.py`](../tools/deck/figgrid.py)'s precedent exactly — T-184 re-cut the shipped decks
  first, *which is what made gating it honest*.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-21 | → proposed | Raised from the owner's review of the portfolio-review deck. The deck passed every gate this repository owns while carrying thirteen chart defects, nine found by one look and four by a second — so the instrument for a mark overlapping a mark is a person, and a person missed four including a whole slide. Ranked `high` because it is the cheaper of the two answers on the table: R9 §6 reads the same evidence as an argument for a chart library, and a detector costs a fraction of one. |
| 2026-08-21 | (no change) | **Two more subjects and a starting sketch, from T-203's closing look.** The count in §1 goes thirteen to fifteen: slides 4 and 10 carry the same class of defect and had been passed by two earlier looks (T-207). T-203 also left five working geometry identities and their SVG readers in the portfolio generator, proven against seeded defects — narrow on purpose, but the arithmetic this task needs, so it starts from a sketch rather than a blank page. |
| 2026-08-21 | → done, review | Built as `tools/deck/markhits.py` and landed as **DS-244**, gathered by `check.py` on every deck. It renders and extracts typed geometry - segments through `getScreenCTM`, curves sampled with `getPointAtLength`, text as real glyph boxes - because a label's width is a fact about the face and only a browser with that face loaded knows it. **Calibrated on all four shipped decks, 30 slides**: text-against-text is 1 hit and 0 false alarms and gates; text-against-line is 16 firings for 1 real defect and reports. The obvious rescue for the second - *only count a crossing through the middle* - was implemented and **inverts**, at depth 0.951 for the real defect against 0.001 for the deliberate placements, so a label on its own line is not separable from a label a line ran over. **The one gating hit was real and unseeded**: pointed at the shipped deck it independently named T-207's slide 4, which is the argument this task was raised to make. T-207 was then fixed so the rule lands green, on `figgrid`/T-184's precedent. |
