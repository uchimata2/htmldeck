---
id: T-113
title: Evaluate an embeddable chart library against hand-authored SVG, and settle where each is used
type: research
status: in_progress
phase: implement
parent: null
blocked_by: []
related: [T-057, T-112, T-187]
work_package: PH3
owner: the project owner
business_value: high
effort: l
created: 2026-08-12
updated: 2026-08-21
deliverables: [docs/research/R9-embeddable-chart-library-versus-hand-authored-svg.md, examples/portfolio-review/portfolio-review.html]
---

# T-113 — Evaluate an embeddable chart library against hand-authored SVG, and settle where each is used

## 1. Specify

**Outcome**
A recommendation with a number behind it: build charts from an embeddable library, from hand-authored
SVG, or from both with a stated rule for which is used when. Whatever the answer, the threshold that
decides it is written down so the next chart does not re-argue it.

**The premise the request came with is false, and correcting it is the first finding**
The feedback asked to *"compare it with your built-in capabilities."* There are none:

```
grep -c -i "chart" shell/components.css        →  0
grep -i  "chart" docs/COMPONENT-CONTRACT.md    →  1 hit, incidental prose inside another rule
```

**DS-146** and **DS-147** both legislate chart behaviour — draw in once, never re-animate on
back-navigation, count up on headline statistics, one emphasis pulse. ~~The component they govern was
never built.~~ **Corrected 2026-08-17 by
[T-119](T-119-audit-the-ruleset-for-rules-that-cost-more-than-they-return.md), which was raised on
this same reading and withdrew it.** Both rules are implemented by name in `shell/deck.js` — 410 for
DS-146, 825 for DS-147 — and `examples/reference-deck.html` draws a line chart in hand-authored SVG.
The greps above are right and they are pointed at a stylesheet and a contract, where behaviour is
not (**L-115**). **What is true is that no chart *component* exists, and DS-122 already says one
must not**: *no chart library, hand-written SVG, borrowing scale arithmetic as a few lines.* So the
comparison is not blocked for want of a subject — **it is mostly already decided, against the
library**, and the live remainder is narrower than this task was scoped for: whether *borrowing
scale arithmetic* has a form worth writing down, and what the reference deck's chart already shows
about it. **Re-specify before planning; the honest shape of the question has moved twice.**

**The owner's steer, recorded 2026-08-12**
*"In the recent days I spent too much time on implementing htmldeck's new features, and I learned how
costly the development of a single feature is. So, it's very likely we use some existing embeddable
lib than we start implementing from the scratch. Still, where a single SVG + a little highlight or
anim can be used, we don't need to use a more costly, rich library."*

That is a two-part instruction and both parts are the deliverable: **default to an existing library**,
and **name the threshold below which SVG wins**. A recommendation that answers only the first half
would leave every future chart an argument.

**The owner's steer, restated 2026-08-19 — and the two halves swap places**
Put to the owner as a straight conflict between the 2026-08-12 steer and DS-122, the answer keeps
both and reorders them:

> *"To be researched. There's no chart intensive deck been created so far. Need one, with full of
> financial figures, meaningful charts and visualization. I believe a dedicated chart-only library
> could boost the content with animations and interactions adapted for the best visualization. The
> current presentations are awesome, I have no intention to replace their content, but if you have a
> glance at some lightweight library (I mentioned one in the tasks), that could be a great
> future-proof feature for financial reports, trading / investment presentations, scientific
> explanations, UI demos and many more. Only free, reliable, robust, simple, recently and
> continuously updated libs can be considered. By default, simple SVGs do a great job. This feature
> is not crucial, but keep it scheduled."*

Four things changed, and each moves the task rather than confirming it:

1. **SVG is the default and DS-122 stands for the ordinary chart.** *"By default, simple SVGs do a
   great job."* The 2026-08-12 reading — default to a library — was about the cost of building
   features from scratch, not about charts specifically, and the owner has now scoped it.
2. **A library is wanted for a case this repository has never built.** Chart-heavy decks: financial
   reports, trading and investment, scientific explanation, UI demos. That is the threshold, stated
   as a class of deck rather than as a property of one chart — which is a **better** threshold than
   the one this task set out to write, and the acceptance criteria should say so.
3. **The evaluation has no subject yet.** *"There's no chart intensive deck been created so far. Need
   one."* Comparing candidates against the reference deck's single line chart measures the easy case,
   which is exactly the case SVG already wins. **A chart-intensive deck is now an input to this task,
   not an output of it**, and it is the first thing to build.
4. **A seventh gate, and it is about the project rather than the code:** *free, reliable, robust,
   simple, recently and continuously updated*. Maintenance health is a gate the six below do not
   cover — a dead library passes every one of them.

**Priority, in the owner's words: *"not crucial, but keep it scheduled."*** So this is neither
withdrawn nor next.

**A fifth change, found on re-specification 2026-08-21: the rule that forbids the outcome is
`hard`, `auto` and owned, and its check is a list of five names**

DS-122 reads *no chart library; hand-written SVG, borrowing scale arithmetic as a few lines*, and the
ruleset marks it `hard` / `auto` / owned — the strongest triple the design system has. What enforces
it is one row in [`tools/deck/audit.py`](../tools/deck/audit.py)'s `STATIC` table, and that row is a
substring blocklist of five vendor names: `chart.js`, `d3.min`, `plotly`, `highcharts`, `echarts`.
Probed directly against the row rather than read off the table:

| Probe handed to DS-122's check | Verdict |
| :--- | :--- |
| `uPlot` | **passes** |
| `tanstack charts` | **passes** |
| `apexcharts` | **passes** |
| `frappe-charts` | **passes** |
| `chart.js` | fails |

Two consequences, and both are this task's rather than a successor's:

1. **Amending DS-122 is in scope now**, where this section previously put it out on the reading that
   the comparison was *"mostly already decided, against the library."* The owner's 2026-08-19 steer
   asks for a library in chart-heavy decks and DS-122 forbids exactly that, so a recommendation that
   does not say what becomes of DS-122 recommends something the gate refuses.
2. **Whatever is decided, DS-122's check has to bind on structure rather than on vendor names.** A
   rule enforced by a blocklist admits every library nobody thought of, which is the opposite of what
   `hard` claims — **L-125**'s shape one step short of vacuous, and the reason the four passes above
   are a finding rather than a curiosity.

**The gates a candidate has to clear**
Not preferences — each is an existing rule of this project, and a candidate failing any one is out
with a reason rather than a score:

1. **Inlines with zero external references** and keeps the deck inside the measured size bound
   (rule 1, DS-001). 192 KB is what a full 12-slide deck costs today; a library is measured against
   what is left, not against nothing.
2. **A licence that permits redistribution**, recorded next to it — CLAUDE.md, *Publishing
   constraints*.
3. **Drags no framework in.** A charting layer that needs React needs React embedded in every deck.
   This is the gate most likely to decide the answer and it is checked first.
4. **Driven by the theme tokens**, not by its own palette. Rule 4 makes every layer parametric, and a
   chart that themes itself is a second design system inside the deck.
5. **Can be pinned off for capture and honours reduced motion** — DS-221, DS-224, DS-143.
6. **Executes nothing it was not given.** Same posture as T-070's admission tests.
7. **Maintained.** Free, and released recently and continuously — the owner's gate of 2026-08-19, and
   the only one here that is about the project rather than the code. A dead library passes all six
   above. Read it off the release history and the commit record, with dates, not off a badge.

**Scope**
- In: **TanStack Charts**, named in the request. Its documentation, its own comparison page and its
  catalogue are the starting points, and **nothing about it is asserted from memory** — it postdates
  or barely predates the assistant's knowledge cutoff and a recalled fact about it would be a guess.
  <https://tanstack.com/charts/latest> · <https://tanstack.com/charts/latest/docs/comparison> ·
  <https://tanstack.com/charts/catalog>
- In: at least two alternatives, so the recommendation is a comparison rather than a verdict on one
  candidate.
- In: hand-authored SVG as a full candidate, costed honestly — including the interaction the reporter
  actually wants, which is *values appearing on hover*.
- In: the threshold rule. What makes a chart simple enough that SVG wins.
- In: a measured size figure per candidate, inlined, against a real chart — not the vendor's number.
- Out: **building the chart component.** That is this task's expected child, and its shape depends on
  the answer.
- Out: amending DS-146 or DS-147 **as motion rules**. What changed instead is how they are applied:
  **DS-146 was re-derived on 2026-08-21 by
  [T-187](T-187-open-the-motion-vocabulary-into-a-style-guide.md)** and no longer refuses a
  stroke-dash chart draw on a motion count — it refuses it on **DS-243**, *the page is not designed
  around its own animation* — while **DS-140** became a suggested starter set with an admission test
  rather than a closed vocabulary. So *may a candidate keep its own draw-in?* is now answered by that
  test — it encodes something, it does not drive the page's design, it declares its kind, it sits
  inside DS-141's band or declares a licence to leave it, and it survives reduced motion, print and
  the stop control — and not by whether the motion has one of four names. Gate 5 below is applied
  that way.
- **In: amending DS-122**, per the fifth change above. It is this task's last section, not a child.

**Inputs**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-001, DS-110, DS-143, DS-146, DS-147,
  DS-221, DS-224.
- [`docs/research/R5-assets-and-licences.md`](../docs/research/R5-assets-and-licences.md) — the
  192 KB measurement and the licence method this reuses.
- [`tools/assets/chart_probe.py`](../tools/assets/chart_probe.py) — an existing probe; establish what
  it measures before writing a second one.
- [`CLAUDE.md`](../CLAUDE.md) rule 3 — *"When SVG is as good, prefer it: it scales, themes and
  diffs."* The threshold rule is that sentence made operable.

**Acceptance criteria**
- [ ] **A chart-intensive deck exists first** — real financial figures, several meaningful charts, and
      the interactions a reader of such a deck expects. It is the evaluation's subject; without it
      every candidate is measured on the case SVG already wins.
- [ ] Every candidate has a verdict against all seven gates, with the failing gate named where it
      fails.
- [ ] A measured inlined size for each surviving candidate, against the same real chart **from that
      deck**, not against the reference deck's single line chart.
- [ ] A recommendation, and the threshold rule stated so a future chart can be decided without
      reopening this — expressed as the owner expressed it, a class of deck rather than a property of
      one chart.
- [ ] The false premise is recorded as a finding, not silently corrected.
- [ ] Nothing about any candidate is stated without a source that was actually fetched.
- [ ] **DS-122's disposition is stated** — amended, or kept with its reason restated — and either
      way what its check binds on is named, since today it binds on five vendor names.
- [ ] Written to a new research note under `docs/research/` — **R9**, the next free number — and
      referenced from the brief if it changes direction. *This task claimed **R8** on 2026-08-12;
      `R8-context-economy-for-coding-agents.md` took it on 2026-08-18, which is what a number
      reserved in prose is worth.* Declared in `deliverables:` at `specified`, per
      [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §6.2.
- [ ] `python tools/docs/refcheck.py` green.

**Open questions**
- Whether the answer changes the brief. If a library is adopted, rule 3's *"never an external
  library"* needs its inline-versus-external distinction restated explicitly, because it currently
  reads as a flat ban and is not one. Surfaced to the owner if it happens.

## 2. Plan

**Re-planned 2026-08-21.** The 2026-08-12 table was written before the deck became an input and
before DS-122's check was probed, and it put the measurement before the elimination. Two ordering
rules carry the new one:

- **The cheap gates run before the expensive subject is built.** Gates 3 and 7 — *drags no framework
  in*, *maintained* — are answered from fetched sources in minutes and each is disqualifying on its
  own. A candidate eliminated there is never inlined, never measured, and never needs a chart drawn
  for it.
- **Nothing is measured against the reference deck's line chart.** That is the case SVG already wins,
  and measuring it again would answer the question this task was re-specified away from.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Record both premise findings — that no chart *component* exists, and that DS-122's `hard`/`auto` check is a five-name blocklist — each with the command behind it | findings 1–2 |
| 2 | Fetch the sources for every candidate and apply **gate 3** and **gate 7** to all of them, before anything is built | the shortlist, with the failing gate named per elimination |
| 3 | Build the chart-intensive deck the evaluation needs — `examples/portfolio-review/`, its `sources/` model and spec pair first, then the deck through the ordinary build path | the evaluation's subject |
| 4 | Inline each survivor against **one real chart from that deck** and measure the bytes it adds | size table, gate 1 |
| 5 | Read each survivor's licence out of the file that carries it, not off a badge | licence table, gate 2 |
| 6 | Apply gates 4, 5 and 6 against the built deck — theme tokens, pinned-off capture and reduced motion, and what the candidate executes | the remaining verdicts |
| 7 | Cost hand-authored SVG for the same chart with hover values, honestly, from what step 3 actually took | the last candidate |
| 8 | The recommendation, the threshold rule as a **class of deck**, and DS-122's disposition | the R9 note |

**Step 3 is the long pole and it is not optional** — the acceptance criteria make the deck the
subject, and CLAUDE.md's verification rule makes 12 slides the floor. If a session runs out before
step 8, it stops at a step boundary and hands the shortlist forward; it does not measure against a
smaller subject to finish sooner.

## 3. Implement

**Decisions & assumptions**
- 2026-08-12 — owner: default to an existing embeddable library over building from scratch, but keep
  SVG where a chart is simple. Both halves are deliverables.
- 2026-08-21 — **the candidate set is four libraries and hand-authored SVG.** TanStack Charts because
  the request named it; **Chart.js** as the framework-neutral incumbent; **Apache ECharts** as the
  rich end, because the owner's cases are financial, trading and scientific and ECharts is where
  candlesticks and linked views come from; **uPlot** as the small end. That is one named candidate
  and three alternatives, against a floor of two.
- 2026-08-21 — **size is measured in raw bytes, and the gzip column is reported only to explain the
  vendors' numbers.** A deck is opened from `file://`. No transfer encoding applies, so the deck pays
  the raw column. This is the most decision-relevant fact in the evaluation, and every published
  comparison states the other one.

### Step 1 — the premise findings

**Finding 1 (2026-08-12, unchanged).** The request asked to compare a library against *"your built-in
capabilities"*. There is no chart **component**; DS-146 and DS-147 are implemented by name in
`shell/deck.js`, and `examples/reference-deck.html` draws a line chart in hand-authored SVG. Recorded
in §1 with the greps behind it, and corrected there once already by
[T-119](T-119-audit-the-ruleset-for-rules-that-cost-more-than-they-return.md).

**Finding 2 (2026-08-21, new).** **DS-122 is `hard` / `auto` / owned and its check is a five-name
substring blocklist.** Probed against the row itself in
[`tools/deck/audit.py`](../tools/deck/audit.py)'s `STATIC` table: `uPlot`, `tanstack charts`,
`apexcharts` and `frappe-charts` all **pass** a rule reading *no chart library*; only `chart.js`
fails. Written up in §1.

### Step 2 — gates 3 and 7, applied before anything was built

Read from the npm registry and the GitHub API on 2026-08-21, not from memory and not off a badge.

| Candidate | Version | Licence | Runtime deps | Gate 3 — framework | First release | Last release | Last commit |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TanStack Charts | 0.14.0 | MIT | 18 `d3-*` plus `tslib` at the root; **none on the narrow scale subpaths** | **passes** — all 13 framework peers are `optional: true`, and `@tanstack/charts/dom` exposes `mountChart(container, options)` | 2026-07-29 | 2026-08-15 | 2026-08-15 |
| Chart.js | 4.5.1 | MIT | `@kurkle/color` | **passes** — UMD build, no peer | 2014-07-08 | 2025-10-13 | 2026-05-27 |
| Apache ECharts | 6.1.0 | Apache-2.0 | `tslib`, `zrender` | **passes** — UMD build, no peer | 2015-07-08 | 2026-05-19 | 2026-08-04 |
| uPlot | 1.6.32 | MIT | **none** | **passes** — IIFE build, no peer | 2020-03-10 | 2025-03-14 | 2026-04-22 |

**Gate 3 eliminates nobody, and that is a finding.** §1 called it *"the gate most likely to decide
the answer"*, on the reading that a modern charting layer drags React in. Measured, all four ship a
framework-free entry point — including the one whose documentation and all 188 catalogue examples
are React. The React-only appearance of TanStack Charts is a documentation fact, not a packaging
one.

**Gate 7 splits the field three ways**, against the owner's wording — *free, reliable, robust,
simple, recently and continuously updated*:

- **ECharts passes outright.** 67,104 stars, releases 3 months old, commits 17 days old, eleven
  years of history, Apache-2.0.
- **Chart.js and uPlot pass on *reliable* and *robust* and are thin on *recent*.** Chart.js last
  released 2025-10-13, about 10 months ago, with commits 86 days old; uPlot last released
  2025-03-14 — **17 months, and no release at all in the last 12** — with commits 121 days old.
  Neither is dead; both repositories are active and unarchived. Neither is *continuously* released.
- **TanStack Charts fails *reliable* and *robust*, and it is the only candidate that fails a gate.**
  Not for want of activity: 28 releases in the 23 days since its first, the most active of the four.
  It fails because it is **23 days old at 0.14.0**, and *reliable* and *robust* are claims about a
  track record that does not exist yet. 671 stars against 67,653 and 67,104 measures the same thing.
  **This is a wait, not a refusal** — it is the one gate here that time closes on its own.

### Step 4 — gate 1, measured

Every figure below is bytes of the file that would be inlined, measured locally on 2026-08-21. The
library builds came from unpkg at pinned versions. The TanStack figures are `esbuild 0.28.2
--bundle --minify --format=iife` over the routes its own
published guide *Bundle Size and Performance* documents (shipped inside the npm package, under its
docs tree), because **it publishes no browser build at
all**: `"type": "module"`, an exports map carrying only `import` conditions, no `unpkg` or
`jsdelivr` field, no UMD.

| Candidate and route | Raw bytes — what a deck pays | gzip — what a vendor quotes |
| :--- | ---: | ---: |
| uPlot 1.6.32, `uPlot.iife.min.js` + `uPlot.min.css` | **52,938** | 21,991 + css |
| TanStack Charts, minimal line chart, root import | **74,300** | 26,084 |
| TanStack Charts, minimal line chart, narrow subpaths | **78,196** | 27,584 |
| TanStack Charts, financial slide: stacked bars, margin line, zero rule, value labels, crosshair, interactive legend, tooltip, motion | **165,077** | 55,830 |
| Chart.js 4.5.1, `chart.umd.min.js` | **208,522** | 70,506 |
| ECharts 6.1.0, `echarts.simple.min.js` | **500,315** | 169,097 |
| ECharts 6.1.0, `echarts.min.js` | **1,121,883** | 368,202 |

Four things this table says that a vendor comparison cannot:

1. **The vendors' figures are gzipped, and a `file://` deck gets none of it.** TanStack's own
   comparison page states 37.60–43.56 KiB for itself; the financial bundle measures **55,830**
   gzipped and **165,077** raw. Chart.js is quoted there at 44.70–58.21 KiB and ships **208,522**
   raw. The task asked for *"not the vendor's number"*, and this is what that clause was protecting.
2. **R5's 2026-08-06 measurement reproduces to the byte.** `tools/assets/chart_probe.py` records
   Chart.js at 203.6 KB; `chart.umd.min.js` is 208,522 B, which is 203.6 KiB, at a version two
   releases later. The old number was right and is still right.
3. **Narrow subpaths did not make the minimal chart smaller** — 78,196 against the root import's
   74,300. They pay for themselves once the feature set grows; below that, following the guidance
   costs bytes instead of saving them.
4. **Measured against the deck, not against nothing.** `examples/reference-deck.html` is 313,926 B
   and R5 measured a full 12-slide deck at 192 KB. So ECharts-simple adds **1.6×** a whole deck,
   Chart.js two thirds of one, TanStack's financial bundle **53%**, and uPlot **17%**.

**One route was probed and is not settled: rendering to SVG at build time, so the deck ships no
library at all.** `renderChartSvg(scene, options)` is exported from the root, and a build-time entry
using it bundles to **24,133 B** — bytes that never reach the deck, because they run in the build.
Three attempts to construct a scene failed on `Chart scale "x" requires a configured scale when a
mark materializes its channel`; the package's own published concept page *Chart Definitions* documents
scales as constructors under `x` and `y` keys inside `defineChart`, which none of the three
attempts used. **Recorded as unsettled rather than as a failure** — the correct shape is now known,
and it is the first thing step 6 retries. If it works it is the most interesting answer available,
because it is DS-122's *hand-written SVG, borrowing scale arithmetic* at industrial strength.

### Step 3 — the chart-intensive deck, in progress

The subject exists and does not yet pass. What is built:

| Artefact | State |
| :--- | :--- |
| `examples/portfolio-review/sources/` — two illustrative models | written |
| `portfolio-review.foundation.md` — governing idea, spine, selections, 29-row ledger, 12-slide outline | written; `spec.py` SPEC-1 to SPEC-4 green |
| `portfolio-review.slides.md` — nine fields per slide, three open decisions recorded | written |
| `tools/examples/portfolio_charts.py` — the scale arithmetic and the composer | written; its 22 self-test checks pass |
| `portfolio-review.html` — 12 slides, 359,269 bytes | **built, 13 gate failures open** |

**The deck is deliberately not committed while it is red.** `tools/check_all.py` fails on any tracked
`.html` that its deck map does not declare, and declaring a deck that fails `check.py` would leave
the release gate red in the tree. The generator rebuilds it from the two specifications in one
command, so nothing is lost by leaving the artefact untracked until it is green.

**What the gate names, in the order it will be worked:**

| Class | Rules | What it is |
| :--- | :--- | :--- |
| Sourcing | `FIG-1` 13 of 95, `FIG-2` 8, `FIG-3` 1 | Figures in the disclosures that the two source models do not carry, plus a format mismatch — the deck writes `$78` where the model's table writes `78` under a `$/MWh` head. The invented ones are the disclosure detail on slides 5, 6, 7, 8 and 9, and the honest fix is to put them in the model, which is where a figure lives. |
| Layout | three slides overflow by 141, 446 and 393 du; `DS-075` reflow overflows 24 px at 320 | The stat-plus-chart slides ask for a figure and a statistic in one body. |
| Contrast | `DS-215` 3 text runs, `DS-219` data-mark labels | `t-soft` and `t-faint` used on marks that need 4.5:1. |
| Motion | `DS-239` 5 content motions whose `--m-rank` is not what the rule derives | The rank was written by hand rather than derived. |
| Grid | `DS-236` diagrams starting their ink off the text column | Four figures carry a viewBox whose x-origin is not 120. |
| Copy | `DS-241` slide 12's eyebrow names the stage; `DS-203` its ask outranks its bottom line; `DS-092` one sentence over 20 words; `DS-035` one text run under 16 du | Ordinary first-build copy defects. |
| Preflight | `DS-009` holds rows this deck has no subject for | One `shell.py` command. |

**Two findings for R9 are already in hand from building it**, and neither would have come from an
estimate:

1. **The repository's existing borrowed arithmetic covers four chart kinds and a financial deck needs
   seven.** `tools/assets/chart_probe.py` has bar, line, share and stat. Stacked area, waterfall and
   scatter did not exist and had to be written. That gap is the honest shape of what a library
   supplies, and it is narrower than *charting* — it is three mark geometries.
2. **The cost of hand-authored SVG is not the drawing, it is everything around it.** The scale
   arithmetic — `linear`, `y_of`, `band` and the guards imported from the probe — is a few dozen
   lines, exactly as DS-122 claims. What the same file spends on top of that is the slide markup,
   the disclosure panels, the provenance marks and the source quick views. **A chart library replaces
   the few dozen lines and none of the rest**, which is the comparison the recommendation has to make
   and is not the comparison the request assumed.

**Outputs produced**
- Gate verdicts for gates 1, 2, 3 and 7 across four candidates, above. They are R9's input tables.
- `examples/portfolio-review/` — two source models, both specifications, and a composed 12-slide
  deck that does not yet pass the gate.
- `tools/examples/portfolio_charts.py` — the scale arithmetic, ten figures, and 22 self-test checks
  asserting the identities the deck's own quality bar promises.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :--- | :--- |
|  |  |  |

**Child fix tasks raised**
- expected: the chart component itself, raised from this task's recommendation

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-12 | → proposed | Created from the first adopting project's feedback on published `0.2.2`. The request assumed a built-in chart capability to compare against; there is none, and the correction is scoped as the first finding rather than as a footnote. |
| 2026-08-19 | (no change) | **Re-specified from the owner's restated steer**, recorded in §1. The task keeps both halves of the 2026-08-12 instruction and swaps which is the default: hand-authored SVG wins the ordinary chart and DS-122 stands, while a library is wanted for chart-heavy decks the repository has never built — financial, trading, scientific, UI demo. Three consequences: the threshold is now a **class of deck** rather than a property of one chart; **a chart-intensive deck becomes an input** to this task rather than its child, because evaluating candidates against the reference deck's one line chart measures the case SVG already wins; and a **seventh gate** is added for maintenance health, which the six existing gates do not cover. Priority set by the owner: *"not crucial, but keep it scheduled."* |
| 2026-08-21 | proposed → specified | **Re-specified and re-planned in one session.** Four changes. (a) A fifth premise finding: **DS-122**, the `hard`/`auto`/owned rule that forbids the outcome the owner asked for, is enforced by a five-name substring blocklist in `audit.py`'s `STATIC` table — `uPlot`, `tanstack charts`, `apexcharts` and `frappe-charts` all pass a rule reading *no chart library*, probed against the row itself. **Amending DS-122 therefore moves into scope**, where §1 had put it out. (b) **DS-146's re-derivation of the same day** by T-187 changes how gate 5 is applied: a candidate's own draw-in is now measured against DS-140's admission test rather than against a closed four-name vocabulary. (c) The note's number moves **R8 → R9**; R8 was taken on 2026-08-18 while this task held it in prose. (d) `effort` **m → l**, because the 2026-08-19 restatement made a chart-intensive deck an input rather than a child, and a 12-slide deck is not an `m`. |
| 2026-08-21 | specified → planned | The plan is re-ordered so the two disqualifying gates — framework and maintenance — run before the deck is built, and re-scoped so nothing is measured against the reference deck's single line chart. Eight steps; step 3 named as the long pole and as a stop boundary rather than something to shrink. |
| 2026-08-21 | planned -> in_progress | Steps 1, 2 and 4 done, out of order and deliberately: the two disqualifying gates ran first as planned, and gate 1 followed because the library builds were already downloaded to answer gate 3. **Gate 3 eliminated nobody** — all four candidates ship a framework-free entry, TanStack Charts included, whose React-only appearance is a documentation fact rather than a packaging one and whose 13 framework peers are every one of them optional. **Gate 7 eliminated one**: TanStack Charts is 23 days old at 0.14.0 and cannot evidence *reliable* or *robust*, which is a wait rather than a refusal. **Gate 1 was measured in raw bytes**, and the finding that will carry the recommendation is that every published comparison quotes gzip while a `file://` deck pays raw — TanStack's own page says 37.60–43.56 KiB against a measured 165,077 B. Steps 3 and 5-8 remain; step 3, the chart-intensive deck, is the long pole and has not started. |
| 2026-08-21 | (no change) | **Step 3 started and not finished.** The chart-intensive deck is specified, its two illustrative source models are written, and `tools/examples/portfolio_charts.py` composes 12 slides carrying ten hand-authored SVG figures — a stacked area, a diverging contribution bar, a waterfall, a risk-return scatter, two limit bars, a drawdown line, a tranche bar and a gated timeline. `spec.py` is green on SPEC-1 to SPEC-4 and the generator's 22 arithmetic checks pass. **`check.py` names 13 failures**, listed in §3 by class; the largest is sourcing, where 13 of 95 figures on a slide appear in no source because the disclosure detail was written into the deck rather than into the model. The deck is left untracked while it is red, because `check_all.py` fails on an undeclared tracked `.html` and declaring a red deck would leave the release gate red. Steps 5 to 8 are unstarted. |
