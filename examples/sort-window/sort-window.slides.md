# Move the window, not the fleet — slide-by-slide specification

Expanded from the outline in `sort-window.foundation.md`, page by page. Nine fields per slide.

Stages, in order: **Claim · Why now · The failure · The cause · The evidence · The cost · The ask.**

**Titles and bottom lines were rewritten at the specification review**, before any HTML: nine of the
twelve headlines ran past DS-091's six words and four bottom lines past DS-092's twenty. The
outline in `sort-window.foundation.md` carries the rewritten sentences, because DS-211 requires the
bottom line in the outline to be the one that ships.

---

## Slide 1 — Move the window, not the fleet

- **Archetype.** A-11 Manifesto Line.
- **Title.** Move the window, not the fleet
- **Bottom line.** The parcels that miss the day are the ones the sorter never released.
- **Structure.** Title slide. Eyebrow, the headline at display size, and a foot block holding the
  illustrative-subject note. Tier one is the whole slide; no tier two.
- **Text.** Eyebrow *Marnfield network · operations board · 4 September*. Standfirst names the
  window, because the headline uses the word as a term: *One depot, one sorter line, and a nightly
  window that closes at 01:00.*
- **Visuals.** None. A manifesto line that shares the stage is not one.
- **Animations.** Rise, five steps.
- **Interactive elements.** None.
- **Sources.** none

## Slide 2 — The slot closes on 19 September

- **Archetype.** A-01 Why-Now.
- **Title.** The slot closes on 19 September
- **Bottom line.** Eight weeks' notice before the 14 November review means this is decided in a
  fortnight or not this season.
- **Structure.** Headline, standfirst, then a horizontal date rail: *4 September today* →
  *19 September decide* → *14 November contract review* → *18 November peak opens*. The decision
  mark is the only accented one.
- **Text.** Standfirst: *The linehaul slot needs eight weeks' notice, and peak opens on
  18 November.*
- **Visuals.** SVG date rail, four marks on one axis, the decision mark accented and larger.
- **Animations.** Rise on the rail. Pulse-once on the decision mark.
- **Interactive elements.** Disclosure, `data-disc="scope"` — *What the eight weeks covers*: the
  slot request and the carrier's confirmation window, and what is not in it — the crew hire, which
  runs on a six-week lead and is not on the critical path.
- **Sources.** service-calendar

## Slide 3 — One parcel in eight arrives late

- **Archetype.** A-03 Single Number.
- **Title.** One parcel in eight arrives late
- **Bottom line.** At peak we move 27,600 parcels a day and 12.4% of them arrive late.
- **Structure.** Two columns. Left: **12.4%** at display size with one line of interpretation.
  Right: an icon and the volume the percentage is a percentage of.
- **Text.** Left unit: *of peak parcels miss next-day delivery.* Right: *27,600 parcels a day, from
  18 November to 23 December.*
- **Visuals.** One icon (`i-late`, Lucide `clock`). The number is the visual.
- **Animations.** Rise, two steps. Pulse-once on the figure.
- **Interactive elements.** Disclosure, `data-disc="derivation"` — *How the rate is measured*:
  numerator, denominator, the 31 working days, and the three exclusions.
- **Sources.** throughput-model

## Slide 4 — The failure is seasonal, not structural

- **Archetype.** A-05 Animated Trajectory.
- **Title.** The failure is seasonal, not structural
- **Bottom line.** Four months sit at or under 3.4%, then November reaches 9.8% and December 15.2%.
- **Structure.** Headline, standfirst, then a full-width line chart: July to December across the
  x-axis, miss rate up the y-axis, the 4% contractual threshold as a horizontal rule.
- **Text.** Standfirst: *The same depot, the same fleet, the same sorter, six months apart.* Value
  labels on November and December, and a quiet annotation over July to October reading **3.4% or
  under**, because the bottom line cites that figure.
- **Visuals.** SVG line chart. The threshold rule is quiet, the series is accented, the two
  above-threshold points carry their values.
- **Animations.** Current on the series path, which draws the trajectory's own mechanism. Rise on
  the frame and labels.
- **Interactive elements.** Disclosure, `data-disc="scope"` — *What this line includes*: working
  days only, the excluded fortnight, and why January is not on it yet.
- **Sources.** throughput-model, service-calendar

## Slide 5 — Sorting ends an hour late

- **Archetype.** A-08 Process / Flow.
- **Title.** Sorting ends an hour late
- **Bottom line.** 7,200 parcels land at 23:40 and clear the sorter at 01:59, an hour past the 01:00
  cut-off.
- **Structure.** The hinge slide. One night on a horizontal time axis from 19:00 to 03:00, two trunk
  lanes with a sort bar in each, the 01:00 cut-off as a vertical rule, and two labelled exits: *made
  the day* and *missed — 84% of these were still on the belt*.
- **Text.** Connector labels *unload*, *sort at 3,100/hr*, *load*. The second lane carries **7,200
  parcels**, because the bottom line cites it and DS-231 will not have a bottom line resting on a
  figure that lives behind the click. The rule is labelled **01:00 cut-off**.
- **Visuals.** SVG night-flow. Two lanes, labelled connectors, one accented vertical rule.
- **Animations.** Current on the second lane's sort bar, the path that runs past the rule. Rise on
  the lanes. Pulse-once on the cut-off rule.
- **Interactive elements.** Disclosure, `data-disc="derivation"` — *Where 01:59 comes from*: 7,200
  parcels at 3,100 an hour is 2h 19m, sorting cannot start before the trunk is unloaded, and 23:40
  plus 2h 19m is 01:59.
- **Sources.** throughput-model

## Slide 6 — Loading order, not distance

- **Archetype.** A-06 Small Multiple.
- **Title.** Loading order, not distance
- **Bottom line.** The last district loaded misses 18.7%, and the district furthest away is loaded
  second and misses 11.2%.
- **Structure.** Four panels in one row, one per district, in loading order. Each panel carries the
  district name, one bar for miss rate on a scale shared across all four, and the distance under it.
  The shared scale is the point: every comparison positional.
- **Text.** Ashgrove 4.1% · 9 miles · first. Cranleigh 11.2% · 14 miles · second. Dellow 15.9% ·
  6 miles · third. Beacon Hill 18.7% · 11 miles · last.
- **Visuals.** SVG small multiple, four facets, one shared axis.
- **Animations.** Rise, staggered left to right, which is the loading order the slide is about.
- **Interactive elements.** Disclosure, `data-disc="instances"` — the four districts in full: round
  count, departure time, and the round that leaves last on 27 of 31 peak nights.
- **Sources.** throughput-model

## Slide 7 — One edge moves: the arrival

- **Archetype.** A-07 Before / After.
- **Title.** One edge moves: the arrival
- **Bottom line.** Landing the second trunk 110 minutes earlier clears it at 00:09, inside the
  existing cut-off.
- **Structure.** Slide 5's diagram twice, stacked: *now* above, *proposed* below. Exactly one edge
  differs — the second trunk's arrival — and it is marked. The cut-off rule sits in the same place
  in both.
- **Text.** Marks *now 23:40, clears 01:59* and *proposed 21:50, clears 00:09*. The delta label
  reads **−110 minutes**.
- **Visuals.** SVG before/after, deliberately the same geometry as slide 5, so the reader is not
  learning a new diagram at the moment of the argument.
- **Animations.** Rise on the two panels. No motion on the delta: the mark is the message, and a
  moving one reads as decoration.
- **Interactive elements.** Disclosure, `data-disc="condition"` — *What has to hold*: the carrier
  meets the earlier slot on 95% of nights, which is its own contractual floor, and the 02:30 second
  cut-off covers the other 5%.
- **Sources.** throughput-model, fleet-and-cost-model

## Slide 8 — The same measure after: 2.4%

- **Archetype.** A-03 Single Number.
- **Title.** The same measure after: 2.4%
- **Bottom line.** Moving the window reaches the 84% of misses a van cannot, and takes 12.4% to
  2.4%.
- **Structure.** Deliberately slide 3's layout, so the two figures read as one comparison. Left:
  **2.4%** at display size, with 12.4% struck through above it. Right: the icon and one line naming
  what closes the gap.
- **Text.** Right: *the 84% of misses still on the belt at 01:00.*
- **Visuals.** One icon (`i-after`, Lucide `trending-down`). Not `circle-check`: slide 12's ask owns
  that glyph, and DS-114 reads a repeated icon as a repeated idea.
- **Animations.** Rise, two steps.
- **Interactive elements.** Disclosure, `data-disc="derivation"` — *How 2.4% is projected*: the sort
  finish moves to 00:09, the 84% band closes, the 16% loading band is unchanged, and volume, sort
  rate and district sequence are held constant.
- **Sources.** throughput-model, fleet-and-cost-model

## Slide 9 — Nine vans reach one sixth

- **Archetype.** A-04 Two-Column Ledger.
- **Title.** Nine vans reach one sixth
- **Bottom line.** The fleet costs $522k of capital to reach a sixth; the window costs $310k a year
  and reaches the rest.
- **Structure.** Two argued columns with a centre gutter naming each row. Rows: capital, annual
  cost, share of misses reached, first benefit, what it assumes. **Both columns are argued** — the
  fleet column is not a straw man, and its *what it assumes* row is the honest one.
- **Text.** Fleet: $522k · $468k a year · 16% of misses · 5 months · assumes vans are the
  constraint, at 88% peak utilisation across 34 vans. Window: no capital · $310k a year · 84% of
  misses · 6 weeks · assumes the carrier meets 95% of slots.
- **Visuals.** No SVG. The ledger is composition, a three-track grid in `<style id="slides">`.
- **Animations.** Rise, row by row.
- **Interactive elements.** Disclosure, `data-disc="derivation"` — the cost build-up on both sides:
  nine vans at capital and running cost, and the $140k slot premium plus the $170k six-person crew
  that make $310k.
- **Sources.** throughput-model, fleet-and-cost-model

## Slide 10 — Six people work at 02:30

- **Archetype.** A-12 Uncomfortable Truth.
- **Title.** Six people work at 02:30
- **Bottom line.** The window costs less because six people work at 02:30, and it needs the carrier
  to meet 95% of slots.
- **Structure.** Headline, then two stated costs in the deck's own voice, before anyone asks. No
  diagram: a slide that softens this with a picture does the opposite of what the archetype is for.
- **Text.** Cost one — *A six-person crew, 22:00 to 02:30, five nights a week through peak. That is
  a shift pattern, not a line item.* Cost two — *The saving rests on a slot the carrier has never
  had to meet. The 02:30 cut-off is the hedge, and it is why the crew exists.*
- **Visuals.** None.
- **Animations.** Rise, two steps. Nothing else: this is the slide where ambient motion reads as
  evasion.
- **Interactive elements.** Disclosure, `data-disc="condition"` — *When this goes wrong*: the slot
  is missed on more than 5% of nights, peak volume passes 31,900, or the sorter drops below 3,100 an
  hour.
- **Sources.** throughput-model, fleet-and-cost-model

## Slide 11 — $120k waits for January

- **Archetype.** A-09 Timeline with a Gate.
- **Title.** $120k waits for January
- **Bottom line.** We hold $120k until January, and the fleet case reopens if peak misses stay above
  4%.
- **Structure.** A left-to-right timeline: *19 September decide* → *14 November review* →
  *18 November peak opens* → **January gate** → two branches, *under 4%: release the $120k* and *4%
  or above: the fleet case reopens*. The gate is the only marked point.
- **Text.** Standfirst: *The change costs $310k a year. We are not asking for all of it now.* The
  gate label reads **January review · 4% threshold**.
- **Visuals.** SVG gated timeline. One accented decision mark, two labelled branches.
- **Animations.** Rise on the timeline. Pulse-once on the gate.
- **Interactive elements.** Disclosure, `data-disc="condition"` — *What the gate measures*: peak
  miss rate over the 31 peak working days, on slide 3's definition, read at the January board.
- **Sources.** fleet-and-cost-model, service-calendar, throughput-model

## Slide 12 — Approve the slot by 19 September

- **Archetype.** A-14 Verdict / Close.
- **Title.** Approve the slot by 19 September
- **Bottom line.** Approve the 21:50 slot and the 02:30 cut-off at $310k a year, and hold $120k for
  January.
- **Structure.** The ask set large and centred as one action. Under it, three lines naming exactly
  what approval authorises. No disclosure: a close that hides half of itself is not a close.
- **Text.** Three lines — *the 21:50 linehaul slot, requested this month* · *the 02:30 second
  cut-off and the crew that runs it* · *$310k a year, with $120k held to January*.
- **Visuals.** One icon (`i-ask`, Lucide `circle-check`), the same concept the seventh stage is
  marked with, so it is one idea and not two.
- **Animations.** Rise, two steps.
- **Interactive elements.** None.

---

## Open — needs a decision

| # | The question | Why it matters | Proposed |
| :-- | :--- | :--- | :--- |
| 1 | Slide 8 sets 12.4% struck through above 2.4%. | DS-045 forbids an unscoped rule on a bare element, so `<s>` or a bare `<del>` fails the gate; a class is composition and passes. | Draw it as a class in `<style id="slides">`. Taken at build time if unanswered. |
| 2 | Slide 9's fleet column states its assumption in the board's own words. | A ledger with one straw-man column fails A-04 the way X-03 records, and the fix is editorial rather than structural. | Keep the wording. Revisit only if the build review scores D1 below 3. |
- **Sources.** fleet-and-cost-model, service-calendar

