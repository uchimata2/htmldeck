# Meridian Infrastructure Fund — 2026 portfolio review

**Governing idea.** The fund's returns now come from the one sector that is also its largest
concentration breach, so the next allocation decision should buy diversification rather than yield.

**Audience and occasion.** The fund's investment committee, at the meeting that approves or defers
the FY27 rebalancing programme. A decision is taken in the room; nothing here is for information.

**Built as T-113's evaluation subject.** This deck exists because
[T-113](../../tasks/T-113-evaluate-an-embeddable-chart-library-against-hand-authored-svg.md) needs a
chart-intensive deck to measure chart candidates against, and the repository had none — every deck it
ships carries at most one chart, which is the case hand-authored SVG already wins. It is a real deck
with a real argument first and an instrument second; a chart gallery would have measured the wrong
thing. **The fund is illustrative and named in no market.**

## Narrative spine

The deck opens on the two figures that are the whole argument — a 52% sector share against a 65%
share of the return — and spends the next three slides showing that neither was chosen: the drift
was passive, the return was concentrated, and the year's gain is mostly an unrealised mark. Having
established that the position arrived rather than being taken, it turns to whether the position is
worth keeping, and finds two limits breached and a risk-return ranking that does not reward the
concentration. Only then does it price the fix, in the deck's own voice and before the committee
asks. The close is one tranche and one gate, because the argument earns a first step, not a
programme.

The order is risk-retirement, not chronology. Each slide kills the objection the previous one
provokes: *it was a decision* → *it was one good year* → *the gain is real* → *the limits are
advisory* → *diversifying is free*. The uncomfortable slide sits at nine because that is where the
committee would raise it.

## Selections

| Layer | This deck uses | Catalogue |
| :--- | :--- | :--- |
| Archetypes | A-01, A-03, A-04, A-05, A-06, A-09, A-10, A-11, A-12, A-14 | DESIGN-SYSTEM §3.2 |
| Disclosure | Tier two on slides 4, 5, 6, 7 and 9, each a `derivation` — how a plotted figure was produced. Nothing the argument needs sits behind a click. | DESIGN-SYSTEM §5.3 |
| Motion | `Rise` for every chart's marks, staggered, encoding reading order; `Pulse-once` on the one headline figure per slide; no `Current`, because the deck carries no flow diagram; no looping motion anywhere, so DS-218's stop control has no subject. | DESIGN-SYSTEM §5.2 |
| Visuals | Seven charts, all hand-authored SVG: a stacked area (4), a diverging contribution bar (5), a waterfall (6), a risk-return scatter (7), a stacked share bar (8), a drawdown line (10), and a gated timeline (11). Two single-number slides carry no chart. **As built: ten, and slide 4 is not stacked.** The reviewed wording stands as the record of what was reviewed; what shipped is `FIGURES` in `tools/examples/portfolio_charts.py`, which the self-test counts and prints — a truncated curve (2), a limit bar (3), **five lines rather than a stacked area** (4), a diverging contribution bar (5), a waterfall (6), a risk-return scatter (7), a top-three bar (8), a drawdown line and tranche bars (10, one each side), and a gated timeline (11). The three the row omitted are the curve, the limit bar and the tranche bars; the deviation on slide 4 is `PR-71` and its reason is beside that slide in `portfolio-review.slides.md`. Raised as `PR-71` and `PR-72`, written by [T-247](../../tasks/T-247-the-portfolio-generators-documents-against-the-deck.md). | DESIGN-SYSTEM §4 |

**Why every chart is hand-authored, in the deck that exists to question that.** DS-122 requires it
today, and T-113 has not reported yet. Building the subject under the incumbent rule is also what
makes the comparison honest: step 7 of that task costs hand-authored SVG *from what this deck
actually took*, which is a number no estimate would have produced.

## Quality bar — additions only

Two, both consequences of this being a financial deck rather than of it being an instrument:

- **Every plotted value appears somewhere as a number.** A committee reads figures, not shapes. A
  chart whose values can only be estimated off an axis fails this deck's bar even where it passes
  the standing one.
- **Every total that is stated is checkable against its parts on the same slide.** The allocation
  columns sum to 100, the contributions sum to 12.4, and the waterfall closes on 2,400. A reader who
  adds them up must not find a gap.

## Sources and the figure ledger

Read from `sources/` beside this file.

| Slug | Source | What it carries |
| :--- | :--- | :--- |
| portfolio-model | Portfolio model | NAV, the five-year allocation, FY26 contribution by sector, IRR and volatility, the NAV waterfall, both concentration limits, the cost of rebalancing, the drawdown, and the tranche sequence |
| market-outlook | Market outlook | The 2026–2030 forward curve, the contracted supply behind it, and how much of the fund's renewable revenue is exposed to it |

**What earns a row.** Every value the deck states as a fact, tier one and tier two alike. The one
exclusion is arithmetic the deck performs on screen from figures that already carry rows.

**This ledger is written from the outline and is completed from the built deck** — the figures that
reach a slide through a disclosure or as a diagram label arrive at build time and are the ones that
go missing (**L-62**).

| Figure | Value | Origin | Used on |
| :--- | :--- | :--- | :--- |
| Renewables share of NAV, 2026 | 52% | portfolio-model | 1, 3, 4 |
| Renewables contribution to FY26 return | +8.1 points | portfolio-model | 5 |
| Net asset value | $2.40B | portfolio-model | 3 |
| Single-sector policy limit | 45% | portfolio-model | 3, 11 |
| Forward curve, 2026 | $78 | market-outlook | 2 |
| Forward curve, 2030 | $61 | market-outlook | 2 |
| Curve decline to 2030 | 22% | market-outlook | 2 |
| Renewables revenue exposed to the curve | 39% | market-outlook | 2 |
| Renewables allocation rise, five years | 21 points | portfolio-model | 4 |
| FY26 total return | 12.4% | portfolio-model | 5 |
| Renewables contribution | +8.1 pp | portfolio-model | 5 |
| Transport contribution | −0.7 pp | portfolio-model | 5 |
| Unrealised revaluation | $172M | portfolio-model | 6 |
| Revaluation sitting in renewables | $102M | portfolio-model | 6 |
| Closing NAV | 2,400 | portfolio-model | 6 |
| Transport net IRR | 5.9% | portfolio-model | 7 |
| Transport volatility | 9.6% | portfolio-model | 7 |
| Water net IRR | 7.4% | portfolio-model | 7 |
| Water volatility | 4.8% | portfolio-model | 7 |
| Top-three asset concentration | 34% | portfolio-model | 8 |
| Top-three policy limit | 30% | portfolio-model | 8 |
| NAV to move out of renewables | $170M | portfolio-model | 9 |
| Value forgone on sale | $7.7M | portfolio-model | 9 |
| Redeployment drag | $14.8M | portfolio-model | 9 |
| Total cost of rebalancing | $22.5M | portfolio-model | 9, 10 |
| Cost as a share of NAV | 0.9% | portfolio-model | 9 |
| Worst FY26 drawdown | −6.8% | portfolio-model | 10 |
| Drawdown carried by renewables | 5.1 points | portfolio-model | 10 |
| Tranche one | $70M | portfolio-model | 11, 12 |

## Outline

Titles are inside DS-091's six words and bottom lines inside DS-092's twenty. The sentences below
are the ones that ship (DS-211).

| # | Archetype | Title — a claim, not a topic | Bottom line |
| :-- | :--- | :--- | :--- |
| 1 | A-11 | Concentration, not performance | Renewables is 52% of the fund and produced 65% of the year's return. |
| 2 | A-01 | The curve falls 22% by 2030 | Our largest sector's uncontracted revenue basis falls a fifth while its NAV share peaks. |
| 3 | A-03 | Renewables reached 52% of NAV | The policy limit is 45%, and no purchase caused the breach. |
| 4 | A-05 | Five years of quiet drift | Renewables rose 21 points in five years without a single allocation decision. |
| 5 | A-06 | Two sectors carried the year | Renewables and digital produced 92% of FY26's 12.4% return, and transport subtracted. |
| 6 | A-10 | The best year is a mark | Unrealised revaluation is $172M of the movement, and $102M of it is renewables. |
| 7 | A-06 | Return does not track risk | Transport returns 5.9% at 9.6% volatility; water returns 7.4% at 4.8%. |
| 8 | A-03 | Top three assets hold 34% | The second limit is breached as well, against a 30% policy ceiling. |
| 9 | A-12 | Rebalancing costs $22.5M | Selling $170M forgoes $7.7M on discount and $14.8M idle, 0.9% of NAV. |
| 10 | A-04 | Holding is not the cheap option | Holding risks 5.1 points of renewables drawdown against a $22.5M one-off cost. |
| 11 | A-09 | Three tranches, one gate | Tranche one is $70M in Q1 2027, and the committee reviews the realised discount. |
| 12 | A-14 | Approve tranche one | Approve $70M in Q1 2027 and the gate that follows it. |

**Gate 1 — outline sign-off: not asked.** This deck is built inside T-113 as that task's evaluation
subject, and the owner's steer of 2026-08-19 set its brief. The pipeline's *Declined* branch applies:
the foundation spec is written either way and stage 4 proceeds. Recorded here rather than left
silent, because a gate nobody was offered is not a gate somebody passed.
