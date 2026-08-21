---
id: T-202
title: Amend DS-122 into a threshold, and bind its check on structure rather than on five vendor names
type: decision
status: proposed
phase: specify
parent: T-113
blocked_by: []
related: [T-113, T-119]
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-08-21
updated: 2026-08-21
deliverables: []
---

# T-202 — Amend DS-122 into a threshold, and bind its check on structure rather than on five vendor names

## 1. Specify

**Outcome**
DS-122 states the threshold [R9](../docs/research/R9-embeddable-chart-library-versus-hand-authored-svg.md)
§7 settled, and its check tests something a library nobody listed cannot walk past.

**Why this is not part of its parent**
[T-113](T-113-evaluate-an-embeddable-chart-library-against-hand-authored-svg.md) recommends that no
library be adopted yet: the one candidate that passes six gates fails the seventh on age. So the
door this task builds should not open until something needs to walk through it, and R9 §8 says so.
Raising it now records the decision while the reasoning is in one place; working it is a later
choice.

**The two findings it acts on**

**DS-122 is `hard`, `auto` and owned, and its check is a substring blocklist of five vendor names** —
`chart.js`, `d3.min`, `plotly`, `highcharts`, `echarts` — in
[`tools/deck/audit.py`](../tools/deck/audit.py)'s `STATIC` table. Probed against the row itself,
`uPlot`, `tanstack charts`, `apexcharts` and `frappe-charts` all pass a rule reading *no chart
library*. That is **L-125**'s shape one step short of vacuous: the column still reads `auto` and the account
still counts DS-122 among the rules a machine decides, while what the machine decides is whether five
strings appear.

**The rule's text is now known to be too flat.** R9 §7 gives the threshold as a class of deck: hand
authored by default, a library only where the reader is expected to *interrogate* the chart, and
never on chart count. DS-122 currently reads as a flat ban, which is not what the owner's steer of
2026-08-19 asks for and not what the evidence supports.

**Scope**
- In: DS-122's text, as R9 §8 drafts it.
- In: its check, re-bound on a **declared chart engine** rather than on vendor names — a deck
  carrying one declares engine, version and licence in a single block, and the check asserts that no
  chart-drawing code sits outside a declared block and that a declared block names a licence
  permitting redistribution.
- In: whatever the component contract owes the declaration block, since a new authorable region is
  a component.
- In: a seeded-defect run in **both** directions, per **L-125** — the undeclared case fails and the
  declared case passes. One direction proves half of it.
- Out: adopting a library. That is R9 §7's middle row firing, and it has not.
- Out: the chart component itself, which is still T-113's expected child.

**Inputs**
- [R9](../docs/research/R9-embeddable-chart-library-versus-hand-authored-svg.md) §6, §7 and §8 — the
  measured cost of hand-authored SVG, the threshold, and the draft rule and check.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-122, and DS-002 and DS-006, which a
  declared engine has to satisfy at the same time.
- [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) — where the declaration block's row
  goes.

**Acceptance criteria**
- [ ] DS-122's text states the threshold as a class of deck, not as a flat ban and not as a chart
      count.
- [ ] Its check binds on a declared engine and names no vendor. Probed with a library invented for
      the probe, the check still fails it.
- [ ] The seeded-defect run passes in both directions.
- [ ] `python tools/check_all.py` green, including every deck this repository already ships, none of
      which declares an engine and all of which must stay passing.
- [ ] The ruleset's own account still counts DS-122 among the `auto` rules honestly.

**Open questions**
- Whether the declaration belongs in the deck's `<head>` or beside the chart it governs. Beside it
  is more local and harder to check; in the head is one block and easier to forget.

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
| 2026-08-21 | → proposed | Raised from [T-113](T-113-evaluate-an-embeddable-chart-library-against-hand-authored-svg.md)'s R9 §8. The parent found DS-122 enforced by a five-name substring blocklist that four real chart libraries walk past, and re-derived the rule's text as a threshold rather than a ban. Both changes are recorded here rather than made there, because the parent's recommendation is *no library yet* and a door nobody needs should not be opened first. |
