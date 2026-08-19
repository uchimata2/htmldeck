---
id: T-182
title: The shipped example deck's specification carries three false claims about the deck it briefed
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-115, T-117, T-128, T-184]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-18
updated: 2026-08-19
deliverables: [examples/measure-first/measure-first.slides.md]
---

# T-182 — The shipped example deck's specification carries three false claims about the deck it briefed

## 1. Specify

**Outcome**
`examples/measure-first/measure-first.slides.md` describes the deck this repository ships. Where it
describes it wrongly, it is corrected — so the worked example a reader copies is not teaching them
to assert layouts the shell does not produce.

**The three, each measured**
Found by running [T-115](T-115-the-specification-can-assert-a-layout-the-shell-cannot-honour.md)'s
new specification-conformance pass against the deck it was written for. Measured in real Chrome at
1920×1234, offline.

| # | Slide, field | The claim | What the deck does |
| :-- | :--- | :--- | :--- |
| 1 | 1, `Structure` | the bottom line *sits below both, spanning the full width* | 1500 du inside a 1726 du content column. `--bottom-measure` caps it, so it cannot span on **any** slide of any deck |
| 2 | 1, `Visuals` | *the three figures set at display weight* | two per side reach display size (84 px): `€18.6m` and `45%` left, `87%` and `310` right. `1.4×` and `58%` do not |
| 3 | 2, `Visuals` | *The diamond is sized from its own label so the outline never crosses the text* | ~~there is no label slot on the diamond at all~~ — **resolved 2026-08-18 by [T-117](T-117-the-decision-diamond-has-no-label-slot-and-diagrams-sit-off-the-text-grid.md)**, which built `.decision` and re-cut this exact node. The label is inside the outline and the shape is sized from it at `w/A + h/B = 0.74`, so **the sentence is now true** and this row has nothing to correct |

**The direction of repair differs per row, and that is the point.** Rows 1 and 2 are *fix the
specification*: the deck is right, and the measure capping the bottom line is doing its job — a
review that assumed the deck was wrong would have argued for removing it. Row 3 was *fix the deck*,
and T-117 landed first — **so row 3 is already spent and this task is now two sentences, not
three.** That is the branch this paragraph anticipated, taken.

**Why it is worth a record.** This specification is **published as a worked example**
([T-128](T-128-publish-the-adopter-deck-as-a-worked-example.md)), so its sentences are a template
someone copies. A false layout claim damages nothing in the deck, which is exactly why all three
survived a build, four gates, a render and a presentation — DS-234, and **L-118**'s shape in a
different artifact.

**Scope**
- In: the three sentences above, corrected against what the deck does, in the specification's own
  register.
- In: re-running T-115's pass afterwards, so the correction is verified rather than asserted.
- Out: changing the deck. Row 3's repair is T-117's and is not duplicated here.
- Out: `sort-window`'s specification, which the same pass found clean — its *full-width* claim is
  true, measured at 100% of the content column.

**Inputs**
- [`examples/measure-first/measure-first.slides.md`](../examples/measure-first/measure-first.slides.md)
- [`skills/htmldeck/references/critique.md`](../skills/htmldeck/references/critique.md) §3.3 — the pass.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-234, the obligation.

**Acceptance criteria**
- [ ] Each of the three sentences is either corrected, or recorded as already true, with a reason
      — row 3 is the second case and needs verifying rather than editing
- [ ] The corrected sentences describe what the deck measurably does, at the container the element
      sits in
- [ ] T-115's pass, re-run on the pair, reports no remaining mismatch it can decide
- [ ] `python tools/deck/spec.py` and the full gate stay green

**Open questions**
- None. The measurements are taken and the direction of repair is settled per row.

## 2. Plan

**Re-measure first, then edit.** §1's figures were taken on 2026-08-18 and
[T-184](T-184-re-cut-the-shipped-diagrams-onto-the-text-column-and-gate-it.md) changed this deck on
2026-08-19 — every viewBox, and slide 8's decision node. A correction written from a stale
measurement is the defect this task exists to remove.

**Then sweep the whole document, not only the three rows.** §1's list is what T-115's pass found on
one run; the Outcome is *where it describes the deck wrongly, it is corrected*. Every sentence
asserting a measurable layout gets judged against the container the element actually sits in, which
is DS-234's own calibration.

**Steps**
1. Re-measure slide 1's bottom line and its six figures, and slide 8's decision node, in real Chrome
   at 1920×1234 offline.
2. Grep the specification for every phrase asserting geometry — *full width*, *spanning*, *two
   thirds*, *a third*, *different heights*, *display size* — and measure each against its own
   container.
3. Correct what is false, in the specification's register. The deck is not touched: this task's
   direction of repair is the specification (§1), and row 3's deck-side repair was T-117's.
4. Verify row 3 rather than edit it.
5. `python tools/deck/spec.py` on the pair, then the full gate.

## 3. Implement

**Decisions & assumptions**
- **Re-measured on 2026-08-19 rather than trusting §1's figures** — T-184 changed this deck the
  same morning. Slide 1 was unaffected and both its numbers reproduce exactly: the bottom line is
  1500 du wide at left 96 in a 1726 du column, capped by `--bottom-measure: 1500px`; and exactly four
  text runs carry `.lfig` at 84 px.
- **The sweep found two more, both in slide 8, and both were fixed** — 2026-08-19. §1's list
  is what one run of T-115's pass reported, and the Outcome is the broader claim. Leaving a sentence
  known to be false in a document published as a template is the failure this task exists to remove,
  so the boundary that held was *the specification only, never the deck* — not *these three
  sentences only*.
- **Row 3 was verified, not edited** — 2026-08-19, as §1 required. Slide 2's `.decision`
  carries its label inside the outline, the label's centre sits on the shape's centre to within 0.0
  du in both axes, and `w/A + h/B = 40.2/106 + 30.4/96 = 0.696`. The sentence is a true description
  of the deck.
- **`the diagram occupies the upper two thirds` was measured and deliberately left** —
  2026-08-19. On slides 2, 4, 6 and 7 the figure occupies 83%, 79%, 79% and 89% of the body's height,
  not 67%. It is loose prose about proportion rather than a layout the shell cannot honour, which is
  what separates it from the four corrected here: no reader copying it is led to assert something
  impossible. Recorded with the numbers so the judgement is re-openable rather than rediscovered.

**The four sentences, and what each now says**

| Slide, field | Was | Measured | Now |
| :--- | :--- | :--- | :--- |
| 1, `Structure` | the bottom line *spans the full width* | 1500 du at left 96, in a 1726 du column | runs to the measure the shell caps it at, and says *full width is not a layout this shell offers* |
| 1, `Visuals` | *the three figures set at display weight* | four `.lfig` runs at 84 px, two per side | two per side named, and where the third one goes |
| 8, `Visuals` | the diamond `Inside the band?` | the deck's label is `within the band` | named as the deck sets it |
| 8, `Visuals` | *the two outcome boxes sit at different heights* | both at y 246, height 72 — level | level, and what actually keeps the edge labels apart |

The third and fourth were found by the §2 sweep rather than by T-115's pass, and the fourth was
false before T-184 and after it: the boxes were level the whole time, and the sentence explained a
collision that a different mechanism prevents.

**Outputs produced**
- [`examples/measure-first/measure-first.slides.md`](../examples/measure-first/measure-first.slides.md)
  — four sentences, slides 1 and 8.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Each of the three sentences is corrected, or recorded as already true with a reason | **pass** | Rows 1 and 2 corrected; row 3 verified true against the rebuilt node at `w/A + h/B = 0.696` and left alone. Two more of the same kind were found and corrected — §3 |
| The corrected sentences describe what the deck measurably does, at the container the element sits in | **pass** | Every figure in §3's table is a reading taken in real Chrome at 1920×1234 offline on 2026-08-19, against the content column rather than the stage — DS-234's calibration |
| T-115's pass, re-run on the pair, reports no remaining mismatch it can decide | **pass** | Re-run as §2's sweep: every phrase in the document asserting geometry, measured against its own container. One survives and is recorded rather than corrected — *the upper two thirds*, at a measured 79–89%, which §3 argues is prose and not an impossible layout |
| `python tools/deck/spec.py` and the full gate stay green | **pass** | SPEC-1 to SPEC-5 pass on the pair; `python tools/check_all.py` green |

**Child fix tasks raised**
- none. The two extra corrections were four lines in the same document.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-18 | → proposed | Raised by [T-115](T-115-the-specification-can-assert-a-layout-the-shell-cannot-honour.md), whose scope books fixing a reference deck's own specification as a child rather than as part of building the pass. Three claims, each measured rather than read; two are the specification's fault and one is the deck's. `PH3` by [`../CLAUDE.md`](../CLAUDE.md)'s rule — a wrong sentence in an example specification does not break the published plugin, so it does not reopen `PH1`. |
| 2026-08-18 | (no change) | **Row 3 is spent before the task starts.** [T-117](T-117-the-decision-diamond-has-no-label-slot-and-diagrams-sit-off-the-text-grid.md) closed the same day and re-cut slide 2's decision node as its demonstration, so the sentence *the diamond is sized from its own label so the outline never crosses the text* is now a true description of the deck — verified against the rebuilt node: label inside the outline, `w/A + h/B = 0.74`. Two sentences remain, both *fix the specification*. Recorded here rather than left for the next session to rediscover. |
| 2026-08-19 | → done | Four sentences, not two. Both remaining rows corrected against readings taken the same day — T-184 had changed this deck that morning, so §1's figures were re-measured rather than trusted, and slide 1's reproduce exactly. Row 3 verified true and left. A sweep of every geometry claim in the document then found two more in slide 8: the diamond named by a label the deck does not carry, and *the two outcome boxes sit at different heights*, which they never did. One loose claim — *the upper two thirds*, measured at 79–89% — recorded with its numbers and deliberately left. |
