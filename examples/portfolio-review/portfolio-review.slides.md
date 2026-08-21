# Meridian Infrastructure Fund — 2026 portfolio review — slide-by-slide specification

Expanded from the outline in `portfolio-review.foundation.md`, page by page (DS-212). Nine fields
per slide.

**Motion, stated once so no slide repeats it.** Every chart's marks enter with `Rise`, staggered in
reading order, once, and never on back-navigation (DS-146). One `Pulse-once` per slide, on the
headline figure and on nothing else (DS-147). No motion in this deck loops, so DS-218's stop control
has no subject here. Under `prefers-reduced-motion` every entrance resolves to its final state and
the count-ups print their final value (DS-143); for print they hold nothing back (DS-224).

---

## Slide 1 — Concentration, not performance

- **Archetype.** A-11 — Manifesto Line.
- **Title.** Concentration, not performance
- **Bottom line.** Renewables is 52% of the fund and produced 65% of the year's return.
- **Structure.** One declarative line set at display size, upper two thirds. Below it, two figures
  side by side on the content column — `52%` and `65%` — each with a four-word label beneath. No body
  copy. Both figures are tier one.
- **Text.** Title as above. Figure labels: `share of the fund` and `share of the return`. Bottom
  line as above, on the bottom line rail.
- **Visuals.** None. The two figures are the visual, and a chart here would ask the reader to
  compare two numbers they can already see.
- **Animations.** The two figures count up from zero, staggered 60 ms apart, encoding that the
  second is read after the first. `Pulse-once` on `65%`, because that is the figure the deck is
  about and the one a reader would otherwise skip past on the way to the larger number.
- **Interactive elements.** None. The opening slide reads with everything closed because there is
  nothing to open.
- **Sources.** portfolio-model

## Slide 2 — The curve falls 22% by 2030

- **Archetype.** A-01 — Why-Now.
- **Title.** The curve falls 22% by 2030
- **Bottom line.** Our largest sector's uncontracted revenue basis falls a fifth while its NAV share
  peaks.
- **Structure.** A short line chart on the left two thirds — five points, 2026 to 2030 — and on the
  right a stacked pair of figures: `39%` exposed to the curve, `$310M` re-contracting before 2030.
  The chart's y-axis starts at 55, not zero, and the slide says so on the axis label rather than in a
  footnote, because a truncated axis a reader has to discover is the chart lying.
- **Text.** Axis label: `$/MWh — axis starts at 55`. Point labels `78` and `61` on the first and
  last points only. Right-hand labels: `of renewable revenue is uncontracted` and `of NAV
  re-contracts before 2030`.
- **Visuals.** Line chart, five points, one series. The two endpoint values are labelled directly on
  the marks; the three interior points are not, because the shape carries them and the endpoints are
  the claim.
- **Animations.** The line's five points `Rise` in date order, 60 ms apart — the stagger encodes
  time, which is the one thing this chart is about. The line itself does **not** draw itself in
  along its length: that is the stroke-dash draw DS-146 refuses, and it would make the reader watch
  the drawing instead of read the fall. `Pulse-once` on `22%` in the title area.
- **Interactive elements.** One `derivation` disclosure under the chart: *how the 22% was produced*
  — the 14.2 GW contracted against 3.1 GW of demand growth. Tier one reads without it.
- **Sources.** market-outlook

## Slide 3 — Renewables reached 52% of NAV

- **Archetype.** A-03 — Single Number.
- **Title.** Renewables reached 52% of NAV
- **Bottom line.** The policy limit is 45%, and no purchase caused the breach.
- **Structure.** `52%` at display size on the content column, one line of interpretation beneath it,
  and a single horizontal rule marking 45% with the seven-point overshoot shaded. NAV `$2.40B` sits
  small, above the figure, as scale rather than as a claim.
- **Text.** Interpretation line: `Seven points above the single-sector limit, on a position nobody
  bought.` Rule label: `policy limit 45%`.
- **Visuals.** A single horizontal bar, full content width, with the 45% mark drawn as a rule across
  it and the overshoot beyond the mark filled in the accent. It is the smallest chart that can show
  a breach as a breach rather than as two numbers.
- **Animations.** The bar `Rise`s from the left to 45%, pauses one frame at the limit, then
  continues to 52% — the pause is the encoding, and it is the only place in this deck where a motion
  carries a boundary. `Pulse-once` on `52%`.
- **Interactive elements.** None. A breach is not something to put behind a click.
- **Sources.** portfolio-model

## Slide 4 — Five years of quiet drift

- **Archetype.** A-05 — Animated Trajectory.
- **Title.** Five years of quiet drift
- **Bottom line.** Renewables rose 21 points in five years without a single allocation decision.
- **Structure.** A stacked area chart across the full content column, five years on the x-axis and
  five sectors stacked to 100%. Renewables is the bottom band so its growth reads against the
  baseline rather than against a moving edge. A right-hand key names the five bands in stacking
  order; no legend floats over the plot.
- **Text.** Axis ticks `2022`–`2026`. Band labels in the key, with each band's 2022 and 2026 value:
  `Renewables 31 → 52`, `Transmission 22 → 18`, `Digital 14 → 20`, `Water 18 → 7`, `Transport 15 →
  3`. Annotation on the renewables band: `+21 points`.
- **Visuals.** Stacked area, five series, five points each, summing to 100 at every point. This is
  the deck's densest chart and the one that most nearly needs a library.
- **Animations.** The five bands `Rise` in stacking order, 60 ms apart, encoding that they are read
  bottom to top. `Pulse-once` on the `+21 points` annotation.
- **Interactive elements.** One `derivation` disclosure: *what moved the share* — that revaluation,
  not purchases, produced the drift, with the sector's own revaluation line. Tier one already says
  no decision moved it; the disclosure says what did.
- **Sources.** portfolio-model

## Slide 5 — Two sectors carried the year

- **Archetype.** A-06 — Small Multiple.
- **Title.** Two sectors carried the year
- **Bottom line.** Renewables and digital produced 92% of FY26's 12.4% return, and transport
  subtracted.
- **Structure.** Five horizontal bars, one per sector, ordered by contribution and sharing one
  x-axis with a zero rule. Transport's bar crosses the zero rule to the left. Every bar carries its
  value at its end. The total `12.4%` sits at the axis foot, so the parts and the total are on the
  same slide.
- **Text.** Bar labels: `Renewables +8.1`, `Digital infrastructure +3.4`, `Transmission +1.4`,
  `Water +0.2`, `Transport −0.7`. Axis label `percentage points of FY26 return`. Foot: `total
  +12.4`.
- **Visuals.** Diverging bar chart, five bars, one negative. Positional comparison against a shared
  axis, which is the whole reason the archetype is A-06 and not a pie.
- **Animations.** Bars `Rise` in ranked order, 60 ms apart — the stagger encodes the ranking, which
  is the slide's argument. `Pulse-once` on `+8.1`.
- **Interactive elements.** One `derivation` disclosure: *how a contribution is computed* — sector
  return weighted by average share of NAV over the year, with renewables' arithmetic shown.
- **Sources.** portfolio-model

## Slide 6 — The best year is a mark

- **Archetype.** A-10 — Architecture View, applied to a movement rather than a system: the parts the
  argument turns on and no others.
- **Title.** The best year is a mark
- **Bottom line.** Unrealised revaluation is $172M of the movement, and $131M of it is renewables.
- **Structure.** A waterfall across the content column: opening NAV, five movement bars, closing
  NAV. The two NAV bars sit on the baseline; the five movements float. The revaluation bar is the
  only one in the accent; the rest are neutral, because the slide is about one of the six.
- **Text.** Bar labels `2,150`, `+180`, `−145`, `+95`, `+172`, `−52`, `2,400` with names beneath:
  `opening`, `contributions`, `distributions`, `realised`, `revaluation`, `fees and carry`,
  `closing`. Axis label `$M`. An annotation on the revaluation bar: `$131M of it renewables`.
- **Visuals.** Waterfall, seven bars, two grounded and five floating, with connectors between
  consecutive tops. The connectors are what make it a waterfall rather than seven bars, and they are
  drawn thin and neutral so they never read as data.
- **Animations.** The seven bars `Rise` left to right, 60 ms apart, encoding the order the movement
  happened in. `Pulse-once` on `+172`.
- **Interactive elements.** One `derivation` disclosure: *what the $131M is* — the three renewable
  assets carrying the revaluation and the valuation basis each moved on.
- **Sources.** portfolio-model

## Slide 7 — Return does not track risk

- **Archetype.** A-06 — Small Multiple.
- **Title.** Return does not track risk
- **Bottom line.** Transport returns 5.9% at 9.6% volatility; water returns 7.4% at 4.8%.
- **Structure.** A scatter on the content column: volatility on x, net IRR on y, one point per
  sector, each labelled beside its point rather than in a legend. A faint diagonal marks equal
  return-per-unit-risk so the two sectors that sit below it read as below something.
- **Text.** Point labels with both values, e.g. `Digital 16.8 / 15.4`, `Renewables 14.2 / 12.1`,
  `Transmission 9.1 / 6.2`, `Water 7.4 / 4.8`, `Transport 5.9 / 9.6`. Axis labels `volatility %`
  and `net IRR %`. Diagonal label: `equal return per unit of risk`.
- **Visuals.** Scatter, five points, two axes and one reference line. Five points is few enough that
  every one is labelled, which is this deck's added quality bar working.
- **Animations.** The five points `Rise` in descending IRR order, 60 ms apart. `Pulse-once` on the
  transport point, which is the one the slide is about.
- **Interactive elements.** One `derivation` disclosure: *how volatility is measured* — the standard
  deviation of quarterly valuation movements, and over what window.
- **Sources.** portfolio-model

## Slide 8 — Top three assets hold 34%

- **Archetype.** A-03 — Single Number.
- **Title.** Top three assets hold 34%
- **Bottom line.** The second limit is breached as well, against a 30% policy ceiling.
- **Structure.** `34%` at display size, and beneath it a single stacked bar splitting the 34 into
  its three assets, with the 30% policy mark drawn across it. The three segments are named but not
  valued individually on the face — the total is the claim.
- **Text.** Interpretation line: `Two limits, both breached, and neither by a decision.` Segment
  names on the bar. Rule label `policy limit 30%`.
- **Visuals.** One stacked bar with a limit rule — deliberately the same visual grammar as slide 3,
  because it is the same kind of fact and a second grammar would imply a second kind.
- **Animations.** The three segments `Rise` left to right, 60 ms apart. `Pulse-once` on `34%`.
- **Interactive elements.** One `instances` disclosure: *which three assets* — named, with each
  one's share. It is `instances` and not `derivation` because the face states a total and the
  disclosure names its members (DS-230).
- **Sources.** portfolio-model

## Slide 9 — Rebalancing costs $22.5M

- **Archetype.** A-12 — Uncomfortable Truth.
- **Title.** Rebalancing costs $22.5M
- **Bottom line.** Selling $170M forgoes $7.7M on discount and $14.8M idle, 0.9% of NAV.
- **Structure.** Two figures stacked on the content column — `$7.7M` and `$14.8M` — with a rule
  beneath and `$22.5M` under it, so the arithmetic is the layout. `0.9% of NAV` sits small beside
  the total. No chart: three numbers that add up do not need one.
- **Text.** Labels `value forgone on sale`, `redeployment drag`, `total`. A single line of the
  deck's own voice above the figures: `This is what the recommendation costs, before anyone asks.`
- **Visuals.** None. The sum is the visual.
- **Animations.** The two components count up, then the total, staggered so the sum reads as a sum.
  `Pulse-once` on `$22.5M`.
- **Interactive elements.** One `condition` disclosure: *what the total needs in order to hold* —
  the 4.5% discount and the nine-month redeployment assumption, and what the number becomes if
  either moves. It is `condition` and not `derivation` because the face already shows the
  arithmetic; what it does not show is where the arithmetic fails (DS-230).
- **Sources.** portfolio-model

## Slide 10 — Holding is not the cheap option

- **Archetype.** A-04 — Two-Column Ledger.
- **Title.** Holding is not the cheap option
- **Bottom line.** Holding risks 5.1 points of renewables drawdown against a $22.5M one-off cost.
- **Structure.** Two columns, both genuinely argued. Left, `Hold`: the FY26 drawdown line chart with
  the −6.8% trough marked and the 5.1 points attributed to renewables shaded within it. Right,
  `Rebalance`: the $22.5M as a single figure with the three tranches beneath it as a small bar. The
  columns share a horizontal rule so neither reads as the conclusion.
- **Text.** Column heads `Hold` and `Rebalance`. Left annotations: `−6.8% trough`, `11 weeks to
  recover`, `5.1 points renewables`. Right: `$22.5M one-off`, `spread over three tranches`.
- **Visuals.** A line chart with a marked trough and a shaded attribution band, against a small bar
  triple. Two different chart kinds side by side is deliberate: the columns are not the same kind of
  claim, and drawing them alike would say they were.
- **Animations.** Left column's line points `Rise` in date order; right column's bars `Rise` after
  it, so the comparison is read left then right. `Pulse-once` on `−6.8%`.
- **Interactive elements.** None. A two-column ledger with a disclosure in one column weights that
  column, and X-03 already says this archetype fails more often than it works.
- **Sources.** portfolio-model

## Slide 11 — Three tranches, one gate

- **Archetype.** A-09 — Timeline with a Gate.
- **Title.** Three tranches, one gate
- **Bottom line.** Tranche one is $70M in Q1 2027, and the committee reviews the realised discount.
- **Structure.** A horizontal timeline across the content column with three tranche markers and one
  gate marker between the first and second. Beneath each tranche, its size and the renewables share
  it reaches. The gate carries its own label and is drawn differently from the tranches — it is the
  information, so it must not look like a fourth tranche.
- **Text.** Markers `Q1 2027 · $70M · to 49%`, `Q3 2027 · $60M · to 47%`, `Q1 2028 · $40M · to 45%`.
  Gate label: `committee reviews realised discount against 4.5%`.
- **Visuals.** Timeline with three step markers and one gate node. The gate node carries its label
  inside itself, per the component contract's decision-node rule.
- **Animations.** The three tranches `Rise` in date order, 60 ms apart, then the gate node after
  them — the stagger encodes sequence and the gate arriving last encodes that it follows tranche
  one. `Pulse-once` on the gate node.
- **Interactive elements.** One `condition` disclosure on the gate: *what reopens the programme* —
  the realised discount running above 4.5%, and what the committee decides if it does.
- **Sources.** portfolio-model

## Slide 12 — Approve tranche one

- **Archetype.** A-14 — Verdict / Close.
- **Title.** Approve tranche one
- **Bottom line.** Approve $70M in Q1 2027 and the gate that follows it.
- **Structure.** One ask, set large, on the content column. Beneath it, three short lines naming
  what approval covers and, separately, one line naming what it does not. Nothing else on the slide.
- **Text.** Ask: `Approve tranche one — $70M, Q1 2027.` Covered: `the $70M`, `the 4.5% discount
  assumption`, `the committee gate that follows`. Not covered: `tranches two and three, which return
  to this committee.`
- **Visuals.** None.
- **Animations.** The ask arrives with `Rise`; the four lines follow, staggered. `Pulse-once` on the
  ask. No count-up — there is no statistic on this slide, and animating an ask would make it look
  like a result.
- **Interactive elements.** None. A close with something behind a click is a close that is not
  finished.
- **Sources.** portfolio-model

  *The template says a close usually rests on nothing external, and this one does not: the ask
  states $70M and Q1 2027, both of which are the model's. `spec.py` caught the mismatch against
  the ledger (SPEC-4) rather than a reader catching it later, which is the check working.*

## Open — needs a decision

| # | The question | Why it matters | Proposed |
| :-- | :--- | :--- | :--- |
| 1 | Slide 2's y-axis starts at 55 rather than zero. | A truncated axis exaggerates the fall, which is the slide's claim. Starting at zero flattens a 22% decline into something a reader will not act on. | Keep the truncation and label it on the axis, as specified. The alternative is a chart nobody can read making a point nobody disputes. Recorded as decided by this specification, not deferred. |
| 2 | Slide 6 shades one waterfall bar in the accent and leaves five neutral. | Colour is doing argument here, not category. A reader could take the accent for a data property. | Keep it, and say so in the bar's own label rather than in a legend. |
| 3 | Whether tranches two and three should appear at all, given the ask is tranche one. | Showing a three-tranche programme while asking for one invites the committee to approve or refuse all three. | Keep them, because slide 12 names explicitly what approval does not cover. This is the one item a reviewer might overturn and it is left visible rather than settled quietly. |

**Gate 2 — detailed-spec sign-off: not asked**, on the same ground as gate 1 and recorded the same
way. The three items above are therefore this specification's own decisions rather than the owner's,
and item 3 is flagged as the one most worth overturning.
