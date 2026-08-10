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
| Visuals | Five hand-written SVG figures — a trajectory, a night-flow, a small multiple, a before/after, a gated timeline — plus one ledger built in the composition block. No charts library | DESIGN-SYSTEM §4 |

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
| throughput-model | Throughput model | Volumes, miss rates, the sorter's rate, and the night the second trunk lands |
| fleet-and-cost-model | Fleet and cost model | Both proposals costed, the vans, and the slot movement they are compared against |
| service-calendar | Service calendar | Dates, notice periods and the contractual miss threshold |

| Figure | Value | Origin | Used on |
| :--- | :--- | :--- | :--- |
| Peak miss rate | 12.4% | throughput-model | 3, 4, 8, 9 |
| Off-peak miss rate | 3.1% | throughput-model | 4 |
| Misses never sorted | 84% | throughput-model | 5, 7 |
| Misses sorted, not loaded | 16% | throughput-model | 5, 9 |
| Second trunk arrival | 23:40 | throughput-model | 5, 7 |
| Second trunk sort finishes | 01:59 | throughput-model | 5, 7 |
| Outbound cut-off | 01:00 | throughput-model | 5, 7 |
| Second trunk parcels | 7,200 | throughput-model | 5 |
| Sort rate | 3,100 | throughput-model | 5, 10 |
| Peak daily volume | 27,600 | throughput-model | 3 |
| District miss rates | 4.1 / 11.2 / 15.9 / 18.7% | throughput-model | 6 |
| District distances | 9 / 14 / 6 / 11 miles | throughput-model | 6 |
| Slot movement | 110 minutes | fleet-and-cost-model | 7 |
| Sort finish after the move | 00:09 | fleet-and-cost-model | 7, 8 |
| Monthly miss rate | 2.9 / 3.0 / 3.4 / 3.1 / 9.8 / 15.2% | throughput-model | 4 |
| Vans in service | 34 | fleet-and-cost-model | 9 |
| Peak round utilisation | 88% | fleet-and-cost-model | 9 |
| Fleet option capital | $522k | fleet-and-cost-model | 9 |
| Fleet option annual | $468k | fleet-and-cost-model | 9 |
| Window option annual | $310k | fleet-and-cost-model | 9, 11, 12 |
| Projected peak miss rate | 2.4% | fleet-and-cost-model | 8, 11, 12 |
| Carrier reliability floor | 95% | fleet-and-cost-model | 7, 10 |
| Proposed trunk arrival | 21:50 | fleet-and-cost-model | 7, 12 |
| Proposed second cut-off | 02:30 | fleet-and-cost-model | 7, 10, 12 |
| Held to the January review | $120k | fleet-and-cost-model | 11 |
| Contractual miss threshold | 4% | service-calendar | 11 |
| Decision date | 19 September | service-calendar | 2, 12 |
| Contract review | 14 November | service-calendar | 2 |
| Slot notice | 8 weeks | service-calendar | 2 |

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
