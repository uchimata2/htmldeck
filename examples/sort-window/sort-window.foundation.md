# Move the window, not the fleet

**Governing idea.** The parcels that miss the day are the ones the sorter never released, so the fix
is the schedule and not the fleet.

**Audience and occasion.** The Marnfield network operations board, 4 September. They are holding a
fleet proposal and a capital line for it. What happens after is a decision that must be taken by
19 September, because the linehaul slot needs eight weeks' notice before the 14 November contract
review.

**Marnfield is an illustrative parcel network. It does not exist.** Every figure in this deck is an
output of the assumptions stated in `sources/`, and nothing is attributed to any real operator,
study or place.

## Narrative spine

The deck opens on the claim and immediately spends its most expensive asset — a date — because the
board's real question is not *which option* but *why now*. It then establishes the failure as a
number, shows that the number is seasonal rather than structural, and only then goes looking for the
cause. The cause slide is the hinge: it follows one night's parcels and shows the second trunk
finishing an hour after the outbound door has closed. Everything after that is retirement of
objections in the order the board will raise them — *is it really the sequence?* (the districts),
*would moving the slot actually reach it?* (the before/after), *at what cost?* (the ledger), *what
does this cost us that nobody has said?* (the truth slide) — and then the gate that lets a sceptic
say yes without conceding the fleet case forever.

**The counter-intuitive finding is the whole deck**, so it is not saved for the end. It arrives on
slide 5 of 12, which leaves seven slides to survive it.

## Selections

| Layer | This deck uses | Catalogue |
| :--- | :--- | :--- |
| Archetypes | A-11, A-01, A-03, A-05, A-08, A-06, A-07, A-03, A-04, A-12, A-09, A-14 | DESIGN-SYSTEM §3.2 |
| Disclosure | Ten panels, slides 2–11. `derivation` on every figure the board will challenge; `scope` where a boundary is doing work; `condition` where the recommendation depends on something outside our control; `instances` once, for the four districts | DESIGN-SYSTEM §5.3 |
| Motion | Rise for entrances; Current on the flow's live path; Pulse-once on the cut-off marker; Open and Turn on the disclosure. No fifth | DESIGN-SYSTEM §5.2 |
| Visuals | Six hand-written SVG figures — a date rail, a trajectory, a night-flow, a small multiple, a before/after, a gated timeline — plus one ledger built in the composition block. No charts library | DESIGN-SYSTEM §4 |

**A-03 is used twice and that is deliberate.** Slide 3 is 12.4% and slide 8 is 2.4%: the same
measure, before and after, in the same form, so the comparison needs no chart. Repeating an
archetype to repeat a measure is the case DS-082's *recorded reason* exists for.

## Quality bar — additions only

One, and it binds slide 9 hardest: **every cost figure names the thing it buys.** A ledger row
reading `$310k` and nothing else is the row a board argues about for ten minutes.

## Sources and the figure ledger

Three source documents, in `sources/`. This is not a presentation-only run. Each file is its slug
plus `.md` inside that directory, so no row below repeats the path.

| Slug | Source | What it carries |
| :--- | :--- | :--- |
| throughput-model | Throughput model | Volumes, miss rates, the sorter's rate, both trunks' nights, and the districts with the order they are loaded in |
| fleet-and-cost-model | Fleet and cost model | Both proposals costed, the vans, the twilight crew's shift, and the slot movement they are compared against |
| service-calendar | Service calendar | Dates, notice and hire lead times, and the contractual service level |

**What earns a row.** Every value the deck states as a fact, tier one and tier two alike, including
the ones a reader only reaches by clicking. The single exclusion is arithmetic the deck performs on
screen from figures that already have rows: slide 5's derivation panel shows 7,200 ÷ 3,100 = 2h 19m,
and 2h 19m is the panel working rather than a figure the panel asserts. Its two operands have rows,
its result — 01:59 — has a row, and the step between them does not.

**The ledger is grouped by source and it is complete.** Grouping is not cosmetic: it is what makes
the completeness claim checkable by a reader, who can hold one source document beside one block.

| Figure | Value | Origin | Used on |
| :--- | :--- | :--- | :--- |
| Peak daily volume | 27,600 | throughput-model | 3 |
| Peak window, volume basis | 18 November to 23 December | throughput-model | 3 |
| Peak volume uplift | 50% | throughput-model | 4 |
| Busiest single day | 31,900 | throughput-model | 10 |
| Peak working days | 31 | throughput-model | 3, 11 |
| Off-peak working days | 22 | throughput-model | 3 |
| Peak miss rate | 12.4% | throughput-model | 3, 8 |
| Off-peak miss rate | 3.1% | throughput-model | 3 |
| Monthly miss rate | 2.9 / 3.0 / 3.4 / 3.1 / 9.8 / 15.2% | throughput-model | 4 |
| Misses never sorted | 84% | throughput-model | 5, 8, 9 |
| Misses sorted, not loaded | 16% | throughput-model | 8, 9 |
| Sort rate | 3,100 | throughput-model | 5, 10 |
| Sort rate tolerance | 4% across a shift | throughput-model | 5 |
| First trunk arrival | 19:40 | throughput-model | 5 |
| First trunk parcels | 20,400 | throughput-model | 5 |
| First trunk sort finishes | 22:57 | throughput-model | 5 |
| Sort rate, both lines | 6,200 | throughput-model | 5 |
| Second trunk arrival | 23:40 | throughput-model | 5, 7 |
| Second trunk parcels | 7,200 | throughput-model | 5 |
| Second trunk sort finishes | 01:59 | throughput-model | 5, 7 |
| Outbound cut-off | 01:00 | throughput-model | 5, 7, 8 |
| Overrun past the cut-off | 59 minutes | throughput-model | 5, 7 |
| District miss rates | 4.1 / 11.2 / 15.9 / 18.7% | throughput-model | 6 |
| District distances | 9 / 14 / 6 / 11 miles | throughput-model | 6 |
| District loading order | first / second / third / last | throughput-model | 6 |
| District rounds | 6 / 5 / 4 / 7 | throughput-model | 6 |
| District first departure | 04:10 / 04:35 / 05:05 / 05:30 | throughput-model | 6 |
| Nights Beacon Hill loaded last | 27 of 31 | throughput-model | 6 |
| Vans in service | 34 | fleet-and-cost-model | 9 |
| Peak round utilisation | 88% | fleet-and-cost-model | 9 |
| Fleet option vans | 9 | fleet-and-cost-model | 9 |
| Fleet option capital | $522k | fleet-and-cost-model | 9 |
| Fleet option annual | $468k | fleet-and-cost-model | 9 |
| Fleet option first benefit | 5 months | fleet-and-cost-model | 9 |
| Slot premium | $140k | fleet-and-cost-model | 9 |
| Twilight crew cost | $170k | fleet-and-cost-model | 9, 10 |
| Twilight crew | 6 people | fleet-and-cost-model | 9, 10 |
| Crew shift | 22:00 to 02:30 | fleet-and-cost-model | 10 |
| Crew nights a week | 5 | fleet-and-cost-model | 10 |
| Window option annual | $310k | fleet-and-cost-model | 9, 11, 12 |
| Window option first benefit | 6 weeks | fleet-and-cost-model | 9 |
| Slot movement | 110 minutes | fleet-and-cost-model | 7 |
| Proposed trunk arrival | 21:50 | fleet-and-cost-model | 7, 10, 12 |
| Sort finish after the move | 00:09 | fleet-and-cost-model | 7, 8 |
| Margin inside the cut-off | 51 minutes | fleet-and-cost-model | 7 |
| Proposed second cut-off | 02:30 | fleet-and-cost-model | 7, 10, 12 |
| Carrier reliability floor | 95% | fleet-and-cost-model | 7, 8, 9, 10 |
| Nights the slot is missed | 5% | fleet-and-cost-model | 7, 10 |
| Projected peak miss rate | 2.4% | fleet-and-cost-model | 8 |
| Held to the January review | $120k | fleet-and-cost-model | 11, 12 |
| Board meeting | 4 September | service-calendar | 2 |
| Decision date | 19 September | service-calendar | 2, 11, 12 |
| Contract review | 14 November | service-calendar | 2, 11 |
| Peak opens | 18 November | service-calendar | 2, 11 |
| Slot notice | 8 weeks | service-calendar | 2 |
| Crew hire lead | 6 weeks | service-calendar | 2 |
| Contractual service level | 96% | service-calendar | 11 |
| Contractual miss threshold | 4% | service-calendar | 4, 11 |
| January review | first working week of January | service-calendar | 11 |

**Two slides had to be corrected rather than the ledger**, which is SPEC-4's rule running in the
direction it names. Slide 4 draws the 4% contractual threshold across its chart and declared only
the throughput model; slide 11 reads its gate over the 31 peak working days and declared only the
fleet and calendar. Both now name the source the figure came from, and the deck's provenance marks
say the same. Neither was visible before, because a figure with no row is a figure SPEC-4 has
nothing to compare.

**One row had to be corrected rather than a slide**, and it took a gate to find it. `Off-peak miss
rate` — 3.1% — claimed slides 3 and 4. Slide 4's chart labels its maximum and prints *3.4% or under*
for the four months beneath it, so 3.1% appears nowhere on it; the cell now reads 3 alone. It is the
fifth over-claim of this kind in this ledger and the first that no hand sweep caught, which is the
argument for `SPEC-5` existing (T-086).

**Slide 1 carries no row, and that is a judgement rather than an omission.** Its eyebrow prints the
occasion and its standfirst introduces the term — *a nightly window that closes at 01:00* — and
neither presents a measurement. The slide declares `Sources: none` and the deck gives it no
provenance mark, which is the same judgement written twice.

## Outline

**Rewritten at the specification review.** Nine of the twelve headlines ran past DS-091's six words
and four bottom lines past DS-092's twenty. The sentences below are the ones that ship, which is
what DS-211 requires of an outline.

| # | Archetype | Title — a claim, not a topic | Bottom line |
| :-- | :--- | :--- | :--- |
| 1 | A-11 | Move the window, not the fleet | The parcels that miss the day are the ones the sorter never released. |
| 2 | A-01 | The slot closes on 19 September | Eight weeks' notice before the 14 November review means this is decided in a fortnight or not this season. |
| 3 | A-03 | One parcel in eight arrives late | At peak we move 27,600 parcels a day and 12.4% of them arrive late. |
| 4 | A-05 | The failure is seasonal, not structural | Four months sit at or under 3.4%, then November reaches 9.8% and December 15.2%. |
| 5 | A-08 | Sorting ends an hour late | 7,200 parcels land at 23:40 and clear the sorter at 01:59, an hour past the 01:00 cut-off. |
| 6 | A-06 | Loading order, not distance | The last district loaded misses 18.7%, and the district furthest away is loaded second and misses 11.2%. |
| 7 | A-07 | One edge moves: the arrival | Landing the second trunk 110 minutes earlier clears it at 00:09, inside the existing cut-off. |
| 8 | A-03 | The same measure after: 2.4% | Moving the window reaches the 84% of misses a van cannot, and takes 12.4% to 2.4%. |
| 9 | A-04 | Nine vans reach one sixth | The fleet costs $522k of capital to reach a sixth; the window costs $310k a year and reaches the rest. |
| 10 | A-12 | Six people work at 02:30 | The window costs less because six people work at 02:30, and it needs the carrier to meet 95% of slots. |
| 11 | A-09 | $120k waits for January | We hold $120k until January, and the fleet case reopens if peak misses stay above 4%. |
| 12 | A-14 | Approve the slot by 19 September | Approve the 21:50 slot and the 02:30 cut-off at $310k a year, and hold $120k for January. |
