# Larkfield Dental Group — Demand Planning: what Business Analytics can do first

**Governing idea.** Larkfield can fix demand planning with measurement and discipline before it buys
any AI, because the two facts that would make a forecast trustworthy are already produced every month
and thrown away.

**Audience and occasion.** The Larkfield Executive Board, at the meeting where they approve or refuse
Phase 1. Afterwards the CEO's question — *how can Business Analytics help us improve one of our core
business processes before investing in Artificial Intelligence?* — has an answer with a price, a date
and an owner.

## Narrative spine

The deck opens on the contradiction the Board already feels: too much stock and too little stock at
the same time. It shows that both come from one decision nobody measures, then walks the evidence —
what is measured, why the error repeats, whether the data could carry a model, and which data is
worth fixing. Only then does it show the redesigned process, and the redesign's own headline is that
six of its eight steps need no AI at all. The last third prices the work, names the one change that
will be resisted, and puts five options on the table with four of them refused. The close is a single
ask.

**The order is an argument, not a work-package tour.** Every slide answers the objection the slide
before it raises: *why is this our problem* → *because nothing measures it* → *could we measure it*
→ *is the data good enough* → *which data first* → *what would the process look like* → *what does
it cost* → *what will go wrong* → *what else could we do* → *approve this*.

## Selections

| Layer | This deck uses | Catalogue |
| :--- | :--- | :--- |
| Archetypes | A-03, A-04, A-06, A-08, A-09, A-10, A-12, A-14 | DESIGN-SYSTEM §3.2 |
| Disclosure | Tier two on six slides, all four kinds used: `instances` for the fixed checklists the reference framework requires in full (S4, S5, S9), `scope` for what a figure includes (S1), `condition` for what a claim needs to hold (S7), `derivation` for how the recommendation was reached (S11) | DESIGN-SYSTEM §5.3 |
| Motion | Rise on slide entry, staggered. Current on the two process flows, so the direction of the flow is visible without narration. Pulse-once on the bottom line of S3 and S9, the two slides carrying a single number. No Open/Turn/Scale beyond the disclosure panels' own reveal. | DESIGN-SYSTEM §5.2 |
| Visuals | Hand-drawn inline SVG on eight slides: two process flows, one broken-loop mechanism, one 2×2 priority matrix, one five-point rating scale repeated across six dimensions, one phased timeline with a marked gate. No charts with continuous axes — the deck has no time series it can source. | DESIGN-SYSTEM §4 |

## Quality bar — additions only

Four, and each comes from something this project has already paid for.

1. **No figure appears beside a picture that contradicts it.** A count true of the full process map is
   false beside a simplified drawing of it. The deck therefore quotes **no element counts at all**
   for the two process maps, although both source documents state them.
2. **Delivery punctuality is stated as *on time*, never as OTIF — in the deck's own copy.** Larkfield
   counts on-time delivery by hand and does not count *in full*, so the industry term claims a
   measurement that does not exist (D1 §3). **The bar does not reach the five sources the deck
   carries**, and two of them use the term: `D2` §3 and `D4` §3 both label the same 87% figure OTIF
   where `D1` §3 caveats it. A source is evidence, and editing one on the way in stops it being
   the thing the deck was built from - so a reader who opens a provenance mark does meet the term
   the bar avoids, and this sentence is where that is said rather than a silence (`PR-88`).
3. **Each of the six geometry classes listed in the outline's note is checked against the rendered
   slides by name before the deck ships.** Every one passed all four automatic checks the last time.
4. **The reference framework is read, not substituted for by D1–D5.** v1 was authored from the five
   deliverables alone and the owner reversed that. What the re-read returned that no deliverable
   carried is the reference framework's **limitations** frame — a forecast is a probability and not a guarantee,
   and human judgement stays essential — and it ships on slide 10.

## Sources and the figure ledger

**Each of the five is carried inside the deck as a quick view** and opens from the provenance mark of
any slide that cites it, which is `DS-105`'s answer where a `file://` link would be a defect. Read
from `sources/`, the project's own five work-package deliverables. The deck introduces no
figure of its own: every value below already exists in one of them, with its own `[example]`,
`[case]` or `[D-n]` mark. **The subject is fictional and every figure illustrative**, which the deck
states on its own surface.

| Slug | Source | What it carries |
| :--- | :--- | :--- |
| `D1-current-business-process-analysis` | Current business process analysis | The As-Is process, what is and is not measured, the descriptive and diagnostic findings, the five failure modes |
| `D2-predictive-analytics-assessment` | Predictive analytics and data readiness | The three predictions, the data inventory, the six quality dimensions and the six readiness items |
| `D3-future-business-process` | Future business process | The To-Be process, the four analytics types, the tolerance bands and the approval rule |
| `D4-implementation-concept` | Business value and implementation concept | The six value categories, the four-phase roadmap, payback, the governance roles and the change plan |
| `D5-management-decision-matrix` | Management decision matrix | The eight-row decision matrix, the five options, the recommendation and the risk |

### Figure ledger

**Written from the built deck, not from the outline.** The first block is tier one, drafted with the
outline; the second is what only the built artefact could show — the values that reach a slide
through a disclosure or as a label inside a diagram. Thirteen rows are in the second block, and they are
what a ledger drafted at outline time would have missed.

| Figure | Value | Origin | Used on |
| :--- | :--- | :--- | :--- |
| Stock held | €18.6m | `D1-current-business-process-analysis` | S1 |
| Stock turnover | 3.2× a year | `D1-current-business-process-analysis` | S3 |
| Share of stock in the two slow families | 45% | `D1-current-business-process-analysis` | S1 |
| Turnover of the slow families | 1.4× a year | `D1-current-business-process-analysis` | S1 |
| Orders delivered on time | 87% | `D1-current-business-process-analysis` | S1, S3 |
| Complaints per quarter | 310 | `D1-current-business-process-analysis` | S1 |
| Share of complaints about delivery | 58% | `D1-current-business-process-analysis` | S1 |
| Weeks of the month the cycle consumes | 3 of 4 | `D1-current-business-process-analysis` | S2 |
| Regional spreadsheets merged by hand | 8 | `D1-current-business-process-analysis` | S2, S7 |
| Measurements of forecast quality | 0 | `D1-current-business-process-analysis` | S3 |
| Standard failure modes Larkfield has | Four and a half of the five | `D1-current-business-process-analysis` | S4 |
| Data quality dimensions, by rating | 2 Poor, 2 Fair, 2 Good | `D2-predictive-analytics-assessment` | S5 |
| AI readiness items, by verdict | 2 red, 3 amber, 1 green | `D2-predictive-analytics-assessment` | S5 |
| Most valuable data assets needing remediation | 3 of 4 | `D5-management-decision-matrix` | S6 |
| Steps in the redesigned process needing AI | 2 of 8 | `D3-future-business-process` | S7, S12 |
| Automatic action band, share of plan | 10% | `D3-future-business-process` | S8 |
| Automatic action band, order value | €25,000 | `D3-future-business-process` | S8 |
| Benefit at steady state | €1.2m a year | `D4-implementation-concept` | S9 |
| Cash released once | €1.3m | `D4-implementation-concept` | S9 |
| Cost to a running pilot | €450k | `D4-implementation-concept` | S9 |
| Phase 1 cost | €120k | `D4-implementation-concept` | S9, S12 |
| Payback | month 19 | `D4-implementation-concept` | S9 |
| The stop-or-go gate | month 4 | `D5-management-decision-matrix` | S9, S12 |
| Adjustments that must carry a reason code | 95% | `D4-implementation-concept` | S10 |
| Dental practices served | 5,500 | `D4-implementation-concept` | S9 |

**Behind a disclosure, or a label inside a diagram.** Found by sweeping the built deck.

| Figure | Value | Origin | Used on | Reaches the slide by |
| :--- | :--- | :--- | :--- | :--- |
| Revenue growth | €0.2m | `D4-implementation-concept` | S9 | disclosure |
| Cost reduction | €0.4m | `D4-implementation-concept` | S9 | disclosure |
| Customer satisfaction | €0.15m | `D4-implementation-concept` | S9 | disclosure |
| Productivity | €0.1m | `D4-implementation-concept` | S9 | disclosure |
| Risk reduction | €0.3m | `D4-implementation-concept` | S9 | disclosure |
| Sustainability | €0.05m | `D4-implementation-concept` | S9 | disclosure |
| Phase 2 cost | €180k | `D4-implementation-concept` | S9 | diagram label |
| Phase 3 cost | €150k | `D4-implementation-concept` | S9 | diagram label |
| Phase 4 cost, per year | €90k | `D4-implementation-concept` | S9 | diagram label |
| End of the timeline axis | month 12 | `D4-implementation-concept` | S9 | diagram label |
| End of the timeline axis | month 24 | `D4-implementation-concept` | S9 | diagram label |
| Supplier B's chance of being late | 72% | `D3-future-business-process` | S8 | diagram label |
| The cut that is small and still needs approval | 12% | `D3-future-business-process` | S8 | disclosure |

## Outline

Twelve slides, and a colophon after the close that is **not** one of them (`DS-085`), so the deck
holds thirteen sections. **Six geometry classes are carried as a build-time checklist**, because each one
passed every automatic check on the previous build and was found only by looking: a connector label
overlapping an adjacent box · text overflowing its box · a fragment set in mono inside an SVG · an
edge label overlapping the edge it names · the same label overlapping the node beside it · a decision
diamond narrower than its own label.

| # | Archetype | Title — a claim, not a topic | Bottom line |
| :-- | :--- | :--- | :--- |
| 1 | A-04 | Two opposite problems, one cause | Too much stock and too little stock come from the same forecast. |
| 2 | A-08 | The plan is negotiated, not calculated | A rejected plan goes back to the meeting, never back to the data. |
| 3 | A-03 | Nothing here measures the forecast | Larkfield measures its results carefully and its forecast not at all. |
| 4 | A-10 | The loop that never closes | Nobody owns forecast quality, so the same error repeats every month. |
| 5 | A-06 | Poor exactly where we decide | The data is partially ready: strong sales history, and two records we choose not to keep. |
| 6 | A-10 | Fix the data worth fixing first | Three of the four most valuable data assets need work, and that work is Phase 1. |
| 7 | A-08 | Two of eight steps need AI | Six of the eight steps improve with no AI at all. |
| 8 | A-08 | Each answer needs the one before | Analytics recommends and a person approves, inside limits Finance sets first. |
| 9 | A-09 | €450k in, €1.2m a year out | The pilot costs €450k over twelve months and pays for itself in month 19. |
| 10 | A-12 | The reason code is the change | Eight managers record why they changed a number, and the Board protects them for doing it. |
| 11 | A-04 | One option survives the evidence | Start with a pilot on two families, beginning with four months of data work. |
| 12 | A-14 | Approve Phase 1 this month | Approve €120k for Phase 1, and judge the programme on what month 4 shows. |
| — | — | **Colophon — What this deck rests on** *(follows the close; not one of the twelve)* | Open any of the five from the mark in the corner of the slide that cites it. |

### Stages

Five, for the ruler and the printed contents page.

| Stage | Slides | What it settles |
| :--- | :--- | :--- |
| Problem | 1–2 | What the Board is feeling, and where it comes from |
| Evidence | 3–6 | What is measured, why it repeats, and what the data can carry |
| Redesign | 7–8 | What the process becomes, and who decides in it |
| Case | 9–10 | What it costs, what it returns, and what will resist it |
| Decision | 11–12, colophon | The options, and the ask. The colophon sits in this stage rather than adding a sixth, which would break the five stage names |
