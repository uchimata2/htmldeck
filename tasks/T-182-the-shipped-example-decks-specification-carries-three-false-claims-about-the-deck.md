---
id: T-182
title: The shipped example deck's specification carries three false claims about the deck it briefed
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-115, T-117, T-128]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-18
updated: 2026-08-18
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
| 3 | 2, `Visuals` | *The diamond is sized from its own label so the outline never crosses the text* | there is no label slot on the diamond at all — which is [T-117](T-117-the-decision-diamond-has-no-label-slot-and-diagrams-sit-off-the-text-grid.md)'s subject |

**The direction of repair differs per row, and that is the point.** Rows 1 and 2 are *fix the
specification*: the deck is right, and the measure capping the bottom line is doing its job — a
review that assumed the deck was wrong would have argued for removing it. Row 3 is *fix the deck*,
and T-117 is already open to do it, so this task corrects the sentence only if T-117 does not land
first; if it does, the sentence becomes true and this row closes with nothing to do.

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
- [ ] Each of the three sentences is either corrected or recorded as waiting on T-117, with a reason
- [ ] The corrected sentences describe what the deck measurably does, at the container the element
      sits in
- [ ] T-115's pass, re-run on the pair, reports no remaining mismatch it can decide
- [ ] `python tools/deck/spec.py` and the full gate stay green

**Open questions**
- None. The measurements are taken and the direction of repair is settled per row.

## 2. Plan

<not started>

## 3. Implement

**Decisions & assumptions**
- <none yet>

**Outputs produced**
- <none yet>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-18 | → proposed | Raised by [T-115](T-115-the-specification-can-assert-a-layout-the-shell-cannot-honour.md), whose scope books fixing a reference deck's own specification as a child rather than as part of building the pass. Three claims, each measured rather than read; two are the specification's fault and one is the deck's. `PH3` by [`../CLAUDE.md`](../CLAUDE.md)'s rule — a wrong sentence in an example specification does not break the published plugin, so it does not reopen `PH1`. |
