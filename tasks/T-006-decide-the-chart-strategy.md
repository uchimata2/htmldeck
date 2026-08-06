---
id: T-006
title: Decide the chart strategy
type: decision
status: done
phase: review
parent: null
blocked_by: [T-013]
related: [T-002, T-016, T-017]
work_package: WP2
owner: maintainer
created: 2026-08-04
updated: 2026-08-06
deliverables: []
---

# T-006 — Decide the chart strategy

## 1. Specify

**Outcome**
A decision on how data becomes a diagram.

**Why this one**
Hand-authored inline SVG scales badly to real data; a charting library is an external dependency and breaks self-containment. The corpus used both, and the library-based decks are the ones that will not render offline.

**Reopened 2026-08-06.** That framing assumed a JavaScript budget. There is none — a charting
library is no longer disqualified by being a library, only by being *external*. A vendored,
inlined library that initialises from `file://` is now a live option, and so is an animated or
interactive chart. This widens the decision rather than settling it; the size and licence cost
comes from T-013, the `file://` envelope from T-017.

**Acceptance criteria**
- [x] Approach chosen, with the reason — hand-authored SVG, generated SVG, or a vendored library
- [x] The three or four chart types a business deck actually needs identified from the corpus
- [x] If a library: licence permits redistribution, it runs from `file://`, and its inlined size
      is measured on a real deck
- [x] Interaction and animation position stated — charts that reveal on interaction fit the
      disclosure layer (T-016), and that is a reason to prefer one approach over another
- [x] A chart produced by the chosen approach rendered and looked at

**Open questions**
- ~~Does a minimal built-in SVG chart generator cover enough cases?~~ **Answered 2026-08-06: yes,
  at four types.** Built and rendered — see §3. The four cover every chart in the corpus's own
  layout archetypes.
- ~~Does chart interaction belong to the chart or to the disclosure layer?~~ **Answered
  2026-08-06: the disclosure layer (T-016).** A chart that owns its own interaction is a second
  interaction model competing with the deck's, and R1 records "two interactions with undefined
  precedence" as a corpus defect that failed live under presentation pressure. The chart renders
  static and complete; revealing part of it is the disclosure layer's job. **This removes the last
  argument for a library** — interactivity was the one thing a library offered that static SVG
  does not, and it turns out to belong somewhere else.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Identify the chart types from the corpus archetypes | the four types below |
| 2 | Build each as hand-computed SVG with the corpus's defect classes guarded | `tools/assets/chart_probe.py` |
| 3 | Render, measure and look at the result | §4 |

## 3. Implement

**Decisions & assumptions**
- **Hand-computed inline SVG, generated. No charting library — decided 2026-08-06.** Size is the
  weak argument (Chart.js 203.6 KB, d3 273.2 KB, against 4.5 KB for a page carrying all four
  types). **The strong argument is that a library would not have prevented any of the corpus's
  chart defects.** R1 names three: a chart 558 px tall that pushed its own title off screen, a bar
  rendering at 1.4 px that reads as a rendering fault, and an SVG label clipped by its own
  viewBox. Every one is a constraint *between the chart and the slide it sits on* — which is
  precisely the part a library cannot own, because it does not know the slide exists.
- **Four types, and the fourth is not a chart** — 2026-08-06:

  | Type | Question it answers | Corpus archetype |
  | :--- | :--- | :--- |
  | **Bar** | how do these compare? | Data / L5 Chart focus |
  | **Line** | which way is it going? | Data / L5 Chart focus |
  | **Share** | how much of the whole? | Data — one callout |
  | **Stat** | one number, stated | **L2 Stat focus**, named explicitly |

  **Honest limitation:** the corpus names *slide* archetypes, not chart types — it does not
  enumerate bar/line/pie anywhere. Only "Stat focus" is named as such. The other three are
  inferred from the archetypes plus ordinary business-deck practice, and that inference is stated
  here rather than presented as a corpus finding.
- **"Stat" exists to stop charts being drawn** — 2026-08-06. One number beats a chart of one
  number, and the generator should say so rather than draw something. A pie with two slices is a
  bar; a bar with one value is a stat.
- **The three defect guards are the deliverable, not the drawing code** — 2026-08-06. Each is
  named after the corpus defect it prevents and is self-tested against the input that produced it:
  a height budget (refuses a chart that would push its slide's title off), a bar floor (draws at
  3 px and labels the value rather than rendering a sliver), and a label-clip check. Drawing a bar
  is easy; refusing to draw a misleading one is the part worth building.
- **Charts fail loudly, not quietly** — 2026-08-06. A chart that will not fit raises rather than
  silently shrinking. Whether a chart fits its slide is a design decision, and R1's "missing
  content rather than error" is listed as the failure mode a self-review most easily misses.
- **A defect found by measuring the rendered output, and worth recording** — 2026-08-06. The line
  chart's x-axis labels were drawn on a *band* scale while its vertices sat on a *point* scale,
  putting "Q5" **76 px** from the point it named. It survived looking at the screenshot; measuring
  the DOM made it unambiguous. Fixed, and both scales now carry a self-test. This is **L-06**'s
  visual case in action, one commit after that lesson was written.

**Outputs produced**
- `tools/assets/chart_probe.py` — the four types, the three guards, and a 12-check self-test.
  Renders to gitignored `.assets-cache/chart-probe.html`; the repository keeps the generator.
- The decision itself, recorded here and carried into `docs/DESIGN-SYSTEM.md` by T-014. The
  chart generator proper is built by T-002; this establishes what it must do.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Approach chosen, with the reason — hand-authored SVG, generated SVG, or a vendored library | **Met** | **Generated SVG.** The reason is the defect argument in §3, not the size argument |
| The three or four chart types a business deck actually needs identified from the corpus | **Met, with a stated limitation** | Four: bar, line, share, stat. Only "Stat focus" is named as such by the corpus, which names slide archetypes rather than chart types; the other three are inferred and §3 says so rather than dressing the inference as evidence |
| If a library: licence permits redistribution, runs from `file://`, inlined size measured | **n/a** | No library. Licences and sizes were measured anyway in R5 §3, which is what ruled them out |
| Interaction and animation position stated | **Met** | Interaction belongs to the disclosure layer (T-016), not the chart. R1 records competing interaction models as a corpus defect that failed live. This also removed the last argument for a library |
| A chart produced by the chosen approach rendered and looked at | **Met** | All four rendered from `file://` and looked at. Measured too, which is what caught the axis-scale defect a screenshot had passed — labels now sit at delta 0.00 from their data points, and the near-zero bar draws at exactly the 3 px floor |

**Child fix tasks raised**
- none. Two obligations are handed on rather than raised as tasks:
  - **T-002** builds the generator proper; this task fixes what it must do, and
    `tools/assets/chart_probe.py` is the working reference for the guards.
  - **T-016** owns chart interaction, per the open question resolved above.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-04 | → proposed | Seeded from `docs/BRIEF.md` when the project folder was prepared. |
| 2026-08-06 | (no change) | Reopened and widened: a vendored charting library is back on the table now that the minimal-JavaScript constraint is gone. |
| 2026-08-06 | → done | Unblocked by T-013 and decided the same session. **Generated inline SVG, no library** — and the widening that reopened this task did not change the answer, it sharpened the reason. Once chart interaction was assigned to the disclosure layer, the only thing a library offered over static SVG was gone, and what remained was three corpus defects a library could not have prevented because it cannot see the slide. Four types built, guarded, self-tested and looked at. |
