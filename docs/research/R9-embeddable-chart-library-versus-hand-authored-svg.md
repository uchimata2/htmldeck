# R9 — An embeddable chart library against hand-authored SVG

**[T-113](../../tasks/T-113-evaluate-an-embeddable-chart-library-against-hand-authored-svg.md), 2026-08-21.** Four candidates and hand-authored SVG, against
seven gates, measured on a chart-intensive deck built for the purpose.

---

## The recommendation, first

**Hand-authored SVG stays the default and DS-122 stands for the ordinary chart.** Not on size, and
not on principle: on what a library actually replaces. In a twelve-slide financial deck carrying ten
figures, the scale arithmetic a chart library exists to supply is **69 of 1,036 lines**. Everything
else the same file spends — the model, the slide markup, the disclosure panels, the provenance
marks, the composition CSS — a library replaces none of.

**A library is admissible for one class of deck, and the trigger is capability rather than count:
a deck whose charts the reader is expected to interrogate.** Hover a continuous series for its
value, brush a range, zoom a time axis, cross-filter linked views. That is the financial, trading,
scientific and UI-demo class the owner named on 2026-08-19, and it is the one thing this repository
cannot reach by hand — not because SVG cannot draw it, but because its disclosure component is
authored per slide and interrogation is per data point.

**When that trigger fires, the candidate is TanStack Charts — and not yet.** It is the only
candidate that passes gates 1 to 6, and it fails gate 7 on one thing that time fixes by itself: it
was 23 days old when this was written. Revisit at 1.0, when there is a release history to read.

**Until then, a chart-intensive deck is still hand-authored**, and
[`examples/portfolio-review/`](../../examples/portfolio-review/portfolio-review.foundation.md) is the
evidence that it can be.

**Number of charts is never the trigger.** Ten of them cost 310 lines. The eleventh costs 31 more.

---

## 1. Two premise findings

**The request assumed a built-in chart capability to compare against.** There is none as a
*component*, and there never was: DS-146 and DS-147 are implemented by name in `shell/deck.js`, and
`examples/reference-deck.html` draws its line chart in hand-authored SVG. Recorded, not silently
corrected, and already corrected once by
[T-119](../../tasks/T-119-audit-the-ruleset-for-rules-that-cost-more-than-they-return.md).

**DS-122 is `hard`, `auto` and owned, and its check is a list of five vendor names.** The rule reads
*no chart library. Hand-written SVG, borrowing scale arithmetic as a few lines.* What enforces it is
one row in [`tools/deck/audit.py`](../../tools/deck/audit.py)'s `STATIC` table, matching the
substrings `chart.js`, `d3.min`, `plotly`, `highcharts` and `echarts`. Probed against the row itself:

| Probe handed to DS-122's check | Verdict |
| :--- | :--- |
| `uPlot` | **passes** |
| `tanstack charts` | **passes** |
| `apexcharts` | **passes** |
| `frappe-charts` | **passes** |
| `chart.js` | fails |

Four things a reader would call chart libraries pass a rule that forbids chart libraries. This is
one step short of **L-125**'s vacuous check, and §6 below says what to do about it.

---

## 2. The candidates, and why these four

**TanStack Charts** because the request named it. **Chart.js** as the framework-neutral incumbent.
**Apache ECharts** as the rich end, because the owner's cases are financial, trading and scientific
and ECharts is where candlesticks and linked views come from. **uPlot** as the small end. One named
candidate and three alternatives, against the task's floor of two.

---

## 3. Gates 3 and 7 — framework, and maintenance

Read from the npm registry and the GitHub API on 2026-08-21.

| Candidate | Version | Runtime deps | Gate 3 — framework | First release | Last release | Last commit | Stars |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | ---: |
| TanStack Charts | 0.14.0 | 18 `d3-*` + `tslib` at the root; **none on the narrow scale subpaths** | **passes** | 2026-07-29 | 2026-08-15 | 2026-08-15 | 671 |
| Chart.js | 4.5.1 | `@kurkle/color` | **passes** | 2014-07-08 | 2025-10-13 | 2026-05-27 | 67,653 |
| Apache ECharts | 6.1.0 | `tslib`, `zrender` | **passes** | 2015-07-08 | 2026-05-19 | 2026-08-04 | 67,104 |
| uPlot | 1.6.32 | **none** | **passes** | 2020-03-10 | 2025-03-14 | 2026-04-22 | 10,431 |

**Gate 3 eliminates nobody, and that is the finding.** T-113 called it *"the gate most likely to
decide the answer"*, on the reading that a modern charting layer drags React in. All four ship a
framework-free entry point — TanStack Charts included, whose 13 framework peers are every one of
them `optional: true` and whose `@tanstack/charts/dom` exposes `mountChart(container, options)`. Its
React-only appearance is a fact about its documentation and its 188 catalogue examples, not about
its packaging.

**Gate 7 splits the field three ways**, against the owner's wording — *free, reliable, robust,
simple, recently and continuously updated*:

- **ECharts passes outright.** Eleven years, releases three months old, commits seventeen days old.
- **Chart.js and uPlot are reliable and robust but thin on *recent*.** Chart.js last released about
  ten months before this note; uPlot **seventeen months, with no release at all in the last twelve**.
  Both repositories are active and unarchived. Neither is *continuously* released.
- **TanStack Charts is the only candidate that fails a gate**, and not for want of activity — 28
  releases in the 23 days since its first, the most active of the four. It fails because *reliable*
  and *robust* are claims about a track record that does not exist yet. **This is a wait, not a
  refusal.**

---

## 4. Gate 1 — size, in the units a deck actually pays

**A deck is opened from `file://`. No transfer encoding applies, so the deck pays the raw column.**
Every published comparison quotes the other one, and the gap is between two and five times.

| Candidate and route | Raw bytes — what a deck pays | gzip — what a vendor quotes |
| :--- | ---: | ---: |
| uPlot 1.6.32, `uPlot.iife.min.js` + `uPlot.min.css` | **52,938** | 21,991 + css |
| TanStack Charts, minimal line chart, root import | **74,300** | 26,084 |
| TanStack Charts, minimal line chart, narrow subpaths | **78,196** | 27,584 |
| TanStack Charts, the financial slide's feature set | **165,077** | 55,830 |
| Chart.js 4.5.1, `chart.umd.min.js` | **208,522** | 70,506 |
| ECharts 6.1.0, `echarts.simple.min.js` | **500,315** | 169,097 |
| ECharts 6.1.0, `echarts.min.js` | **1,121,883** | 368,202 |

*The financial feature set is stacked bars, a margin line, a zero rule, value labels, a crosshair, an
interactive legend, a tooltip and motion — built through the routes TanStack's own bundle-size guide
documents, with `esbuild 0.28.2 --bundle --minify --format=iife`, because the package publishes no
browser build at all: `"type": "module"`, an exports map carrying only `import` conditions, no
`unpkg` or `jsdelivr` field, no UMD.*

Four things this table says that a vendor comparison cannot:

1. **The vendors' figures are gzipped.** TanStack's comparison page states 37.60–43.56 KiB for
   itself; the financial bundle measures **55,830** gzipped and **165,077** raw. Chart.js is quoted
   there at 44.70–58.21 KiB and ships **208,522** raw.
2. **R5's 2026-08-06 measurement reproduces to the byte.** It records Chart.js at 203.6 KB;
   `chart.umd.min.js` is 208,522 B — 203.6 KiB — two releases later.
3. **Narrow subpaths did not make the minimal chart smaller**: 78,196 against the root import's
   74,300. They pay for themselves once the feature set grows, and cost bytes below that.
4. **Measured against the deck, not against nothing.** `portfolio-review.html` is 396,062 B and
   `reference-deck.html` 313,926 B. So ECharts-simple adds **1.26×** a whole deck, Chart.js **53%**,
   TanStack's financial bundle **42%**, and uPlot **13%**.

---

## 5. Gates 2, 4, 5 and 6

**Gate 2 — licence, read out of the file that carries it.**

| Candidate | Licence | File | Redistribution |
| :--- | :--- | :--- | :--- |
| TanStack Charts | MIT — *Copyright (c) 2026-present Tanner Linsley* | `LICENSE`, 1,079 B | permitted; the notice travels |
| Chart.js | MIT — *Copyright (c) 2014-2024 Chart.js Contributors* | `LICENSE.md`, 1,093 B | permitted; the notice travels |
| uPlot | MIT — *Copyright (c) 2022 Leon Sorokin* | `LICENSE`, 1,078 B | permitted; the notice travels |
| Apache ECharts | Apache-2.0 | `LICENSE`, 11,990 B + `NOTICE`, 168 B | permitted, **and §4(d) requires the NOTICE to travel too** |

All four permit redistribution. ECharts is the only one whose licence obliges a second file, and in
a single-file deck that means carrying both texts inline — about 12 KB on top of 500.

**Gate 5 — pinned off for capture, and reduced motion.** Counted in the shipped bytes rather than
read off documentation:

| Candidate | `prefers-reduced-motion` in the bundle | Animation |
| :--- | ---: | :--- |
| TanStack Charts | **6** | opt-in (`svgAnimation`, `@tanstack/charts/motion`) |
| Chart.js | 0 | on by default |
| Apache ECharts | 0 | on by default |
| uPlot | 0 | **none at all** |

**TanStack Charts is the only candidate that honours reduced motion itself.** For the other three the
deck has to disable animation on their behalf, which is a shim this repository would own and DS-143
would gate. uPlot passes DS-221 and DS-224 trivially by never animating — and for the same reason
cannot satisfy DS-146's staggered draw-in, which is a `default`-severity deviation a deck using it
would have to declare.

**Gate 6 — executes nothing it was not given.** `eval(` and `new Function` both count **zero** in
every one of the four shipped bundles. All four pass.

**Gate 4 — driven by the theme tokens.** All four fail as shipped, and equally: each carries its own
palette and none reads CSS custom properties natively. Adopting any of them means a shim that reads
the theme region through `getComputedStyle` and hands the values in as configuration. That shim is
this repository's to write and maintain, and it is the same size whichever candidate wins — so gate
4 ranks nobody, and its finding is that **the cost it names is real and is not in any size table
above.**

**One route was probed and is unsettled.** `renderChartSvg(scene, options)` renders to SVG at build
time, so the deck would ship no library at all; the build-time entry bundles to 24,133 B, which never
reaches a deck. Three attempts to construct a scene failed on *Chart scale "x" requires a configured
scale when a mark materializes its channel*, before the package's own concept documentation showed
that scales are constructors under `x` and `y` keys inside `defineChart`. **Recorded as unsettled
rather than as a failure.** If it works it is the most interesting answer available, because it is
DS-122's *hand-written SVG, borrowing scale arithmetic* at industrial strength — the library in the
build, and nothing but marks in the deck.

---

## 6. What hand-authored SVG costs, measured rather than estimated

The whole point of building
[`examples/portfolio-review/`](../../examples/portfolio-review/portfolio-review.foundation.md) first
was to answer this with a number.
[`tools/examples/portfolio_charts.py`](../../tools/examples/portfolio_charts.py) computes ten figures
— a slope chart, a diverging contribution bar, a waterfall, a risk-return scatter, two limit bands, a
truncated-axis line, a drawdown line, a tranche bar and a gated timeline — and composes twelve
slides. It is 1,036 lines:

| What the lines are for | Lines | Would a chart library replace them? |
| :--- | ---: | :--- |
| **Scale arithmetic and helpers** | **69** | **yes** — this is the whole of what a library supplies |
| The ten figures' mark geometry | 310 | partly |
| The twelve slides' markup | 200 | no |
| Composition CSS | 110 | no |
| Rendering the sources into the quick view | 126 | no |
| The model — the deck's own figures | 56 | no |
| Self-test | 62 | no |
| Docstring, imports, the plot box | 58 | no |
| Composing the deck | 45 | no |

**DS-122's claim is literally true.** *Borrowing scale arithmetic as a few lines* is 69 lines: four
functions — a linear map, its inverted twin for the y axis, band centres, and a label spreader — plus
three guards imported from `tools/assets/chart_probe.py` rather than rewritten. A library replaces at
most 379 of 1,036 lines, and the strict arithmetic is **6.7%** of the file.

**Two findings the building produced that no comparison would have.**

**The repository's existing borrowed arithmetic covers four chart kinds and a financial deck needs
seven.** `chart_probe.py` has bar, line, share and stat. Stacked area, waterfall and scatter did not
exist and were written here. That gap is the honest shape of what a library supplies, and it is
narrower than *charting*: it is three mark geometries and a label spreader.

**A green gate is not a good chart, and the margin is nine defects.** `check.py`, `check_all.py` and
`printgeom.py` were all green on this deck before a person looked at it. Looking found nine, two of
them fatal to the slide they were on: a five-series stacked area that rendered as two shapes, because
DS-020 allows one accent hue and four bands therefore shared a fill; and a waterfall that was
arithmetically correct and unreadable, because five movements of 52 to 180 on a 0–2,500 axis are one
flat band. **Neither is a rule violation.** Both are the failure CLAUDE.md rule 6 exists to catch,
and both would have been a library's problem to solve rather than ours — which is the strongest
argument in this note *for* a library, and it is an argument about defaults, not about capability.

---

## 7. The threshold rule

Stated as the owner stated it — a class of deck, not a property of one chart.

| The deck | What it uses | Why |
| :--- | :--- | :--- |
| **Every deck this repository has shipped, and this one** | **Hand-authored SVG** | The charts are static marks with labelled values. The reader reads them; they do not interrogate them. 69 lines of arithmetic and 0 bytes. |
| **A deck whose charts the reader interrogates** — hover a continuous series, brush a range, zoom a time axis, cross-filter linked views | **A library** | A disclosure is authored per slide; interrogation is per data point. This is the only thing hand-authored SVG plus this repository's components cannot reach. |
| **A deck with a lot of charts** | **Hand-authored SVG** | Count is not the trigger. Ten figures cost 310 lines; the eleventh costs 31. |

**And one constraint that decides *which* library the day the middle row fires: the output has to be
SVG.** The stage is scaled by a transform (DS-060, DS-062) and the deck is printed (DS-224). A canvas
chart at fixed pixel dimensions blurs under the first and prints badly under the second, which is
CLAUDE.md rule 3's *when SVG is as good, prefer it* applied to a case where SVG is better. Chart.js
and uPlot are canvas-only. ECharts defaults to canvas. **TanStack Charts is SVG by default and canvas
by opt-in**, on its own documentation — which, with reduced motion and the framework-free `dom`
entry, is why it wins a race it currently cannot enter.

---

## 8. DS-122's disposition

**Amend it, and re-bind its check on structure.**

The rule today is a flat ban with a name-matching check. It should become the threshold in §7 with a
check that cannot be walked around by picking a library nobody listed:

- **The rule.** *Charts are hand-written SVG, borrowing scale arithmetic as a few lines. A deck whose
  charts the reader is expected to interrogate may carry a chart engine, declared, and its output
  must be SVG.*
- **The check.** Not a vendor blocklist. A deck carrying a chart engine **declares** it — engine,
  version and licence — in one block, and the check asserts two things it can actually see: that no
  chart-drawing code sits outside a declared block, and that a declared block names a licence
  permitting redistribution. A deck that declares nothing is held to the hand-authored default, which
  is where every deck stands today.

That change is not made here. It needs a child task, because it touches the ruleset, `audit.py`'s
`STATIC` table and the component contract at once, and because nothing should be admitted through the
new door until the middle row of §7 actually fires.

---

## 9. What this does not settle

- **The build-time SVG route** (§5). Unsettled, with the shape of the fix now known.
- **The theme shim's real cost** (gate 4). Estimated as equal across candidates and never built.
- **Whether TanStack Charts is any good.** This note measures its packaging, its licence, its size
  and its reduced-motion handling. It has not been used to draw a chart in a deck, because gate 7
  says not yet.
- **The chart component itself.** Still this task's expected child, and its shape now depends on
  which row of §7 the next deck lands in.
