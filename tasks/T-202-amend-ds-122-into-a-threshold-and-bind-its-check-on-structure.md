---
id: T-202
title: Amend DS-122 into a threshold, and bind its check on structure rather than on five vendor names
type: decision
status: done
phase: review
parent: T-113
blocked_by: []
related: [T-113, T-119]
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-08-21
updated: 2026-08-21
shipped_in: 0.6.0
deliverables: [docs/DESIGN-SYSTEM.md, docs/COMPONENT-CONTRACT.md, tools/deck/audit.py, tools/deck/static_variants.py]
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
- ~~Whether the declaration belongs in the deck's `<head>` or beside the chart it governs.~~
  **The head.** Beside the chart loses on two counts, and the second is the one that decided it: it
  multiplies the places a deck can forget one, and **a check reading per-chart declarations would
  first have to decide which chart each governs before it could say anything at all**. One block is
  one thing to find and one licence to read — the shape DS-009's preflight already uses for a
  whole-deck capability.
## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Find a structural signal that separates a chart engine from this repository's figures, and **calibrate it against every deck already shipped** before writing a rule around it | a signal with a measured false-alarm count |
| 2 | Amend DS-122's text to R9 §7's threshold | the ruleset |
| 3 | Re-bind the check on that signal plus a declaration; name no vendor | `audit.py` |
| 4 | Give the declaration a component-contract row | the contract |
| 5 | Seed in **both** directions, per **L-125** — undeclared fails, declared passes | fixtures in `audit.self_test` and two variants in `static_variants` |
| 6 | Seed regressions in the check itself and prove the fixtures are not blind | evidence |
| 7 | `python tools/check_all.py` | every shipped deck still passing |

## 3. Implement

**Decisions & assumptions**
- **The signal is *when the marks exist*, not who wrote them.** Every figure this repository ships is
  literal SVG in the file, written by the generator at build time; an engine draws at run time, and a
  browser offers three ways to do that — SVG shape elements built from script, a canvas drawing
  context, or a `<canvas>` element. That is a property no library can rename its way out of. —
  2026-08-21
- **Step 1 came before step 2, and it changed the signal.** Bound on `createElementNS` alone the
  check fails **all five** decks it must pass: the shell makes two such calls, building `svg` and
  `use` for one icon reference into the sprite. So the signal is the **shape argument** — `path`,
  `rect`, `circle`, `ellipse`, `line`, `polyline`, `polygon`, `g`, `text` — on which all five score
  zero. **A check calibrated after the rule was written would have shipped that false alarm**; this
  is **L-125** from the side nobody looks at. — 2026-08-21
- **The limit is stated in the code rather than left to be discovered.** An engine that writes marks
  by assigning `innerHTML` from a string of `<path …>` is not seen, because a deck's own literal
  figures carry the same bytes and no structural reading separates them. The rule catches the three
  mechanisms a real engine uses and says so. — 2026-08-21
- **The licence set is the one DS-032 already applies to an embedded face**, one artifact along: an
  SPDX identifier whose terms permit redistribution inside a single file. A deck *is* a single file,
  so the test is the same test. — 2026-08-21
- **The fixtures run through `check.py`, not through `audit.py <deck>`.** Found by seeding: the first
  regression run reported *blind* three times, because `audit.self_test()` is called by
  [`check.py`](../tools/deck/check.py) `:659` and `audit.main` runs `render`'s, `contrast`'s and
  `contract`'s but not its own. Re-run against `audit.self_test()` directly, all three regressions
  are caught. **The fixture was never blind; the way I invoked it was** — worth recording because the
  first reading of that output was that the fixtures did not work. — 2026-08-21

**Outputs produced**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-122 amended to the threshold.
- [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) §3.6 — the declaration's row, its
  four required fields, and why it sits in the head.
- [`tools/deck/audit.py`](../tools/deck/audit.py) — `ds122_charts`, the three signals, the
  declaration parser, and nine fixtures in `self_test`.
- [`tools/deck/static_variants.py`](../tools/deck/static_variants.py) — two seeded DS-122 defects.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| DS-122's text states the threshold as a class of deck, not a flat ban and not a chart count | **met** | The row now carries R9 §7's threshold verbatim in force: hand-written SVG by default; an engine permitted where the reader is expected to *interrogate* the chart; **the number of charts is never the trigger**. |
| Its check binds on a declared engine and names no vendor. Probed with a library invented for the probe, the check still fails it | **met** | `ds122_charts` names no library. The fixture's engine is called `nobody-has-heard-of-this` and is refused undeclared, accepted declared. |
| The seeded-defect run passes in both directions | **met** | **9 of 9** fixtures in `audit.self_test`: three undeclared run-time mechanisms fail, four bad declarations fail, and two correct decks pass — including **prose naming a real library**, which the old blocklist failed and which is not a defect. Plus **2 new static variants**, both CAUGHT, taking that suite to **29 of 29**. |
| `python tools/check_all.py` green, including every deck this repository already ships | **met** | **0 failure(s), 0 unclassified, 0 stale — 35 ran, 2 skipped with reasons, 362 s.** All five shipped decks pass DS-122 with *hand-authored: no marks are built at run time*. |
| The ruleset's own account still counts DS-122 among the `auto` rules honestly | **met** | It stays `hard`/`auto`, and what the machine decides is now a property of the deck rather than whether five strings appear. |
| *(evidence, not a criterion)* | — | Three regressions seeded **into the check itself** — reverting to a blocklist, dropping the licence test, dropping the SVG-output test — each caught by the right fixture. Restored and verified byte-identical. |
| *(closing checklist step 3)* | **n/a** | Nothing rendered changed. The five shipped decks are byte-identical; this task added a rule and a check. |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-22 | (shipped) | **Shipped in `0.6.0`.** The release note carries `docs/PUBLISHING.md` §8.1's row for this version, which names what an adopter must change and the smallest edit that satisfies it. |
| 2026-08-21 | → proposed | Raised from [T-113](T-113-evaluate-an-embeddable-chart-library-against-hand-authored-svg.md)'s R9 §8. The parent found DS-122 enforced by a five-name substring blocklist that four real chart libraries walk past, and re-derived the rule's text as a threshold rather than a ban. Both changes are recorded here rather than made there, because the parent's recommendation is *no library yet* and a door nobody needs should not be opened first. |
| 2026-08-21 | proposed → done | DS-122 is the threshold and its check binds on **when the marks exist** rather than on who wrote them — SVG shapes built from script, a canvas context, or a `<canvas>`. **Calibrating before writing the rule is what saved it**: bound on `createElementNS` alone it fails all five shipped decks, because the shell makes two such calls to build one icon reference, so the signal is the shape argument. Both directions seeded — 9 fixtures in `audit.self_test`, 2 new static variants taking that suite to 29 of 29 — and three regressions seeded into the check itself, each caught. `check_all.py` green at 0 failures, 0 unclassified, 0 stale. The open question is answered for the head, because a per-chart declaration would make the check decide which chart each one governs before it could say anything. |
