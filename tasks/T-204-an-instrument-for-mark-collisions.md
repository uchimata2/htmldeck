---
id: T-204
title: An instrument for mark collisions, so a person is not the only thing that can see one
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-113, T-203, T-205]
work_package: PH3
owner: the project owner
business_value: high
effort: m
created: 2026-08-21
updated: 2026-08-21
deliverables: []
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

*Not started.*

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
-

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-21 | → proposed | Raised from the owner's review of the portfolio-review deck. The deck passed every gate this repository owns while carrying thirteen chart defects, nine found by one look and four by a second — so the instrument for a mark overlapping a mark is a person, and a person missed four including a whole slide. Ranked `high` because it is the cheaper of the two answers on the table: R9 §6 reads the same evidence as an argument for a chart library, and a detector costs a fraction of one. |
| 2026-08-21 | (no change) | **Two more subjects and a starting sketch, from T-203's closing look.** The count in §1 goes thirteen to fifteen: slides 4 and 10 carry the same class of defect and had been passed by two earlier looks (T-207). T-203 also left five working geometry identities and their SVG readers in the portfolio generator, proven against seeded defects — narrow on purpose, but the arithmetic this task needs, so it starts from a sketch rather than a blank page. |
