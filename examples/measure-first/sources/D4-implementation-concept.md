# Deliverable 4 — Business Value & Implementation Concept

**Client:** Larkfield Dental Group · **Process:** Demand Planning
**Work package:** WP4
**Date:** 2026-08-05

---

## About the numbers

The Larkfield case is fictional. Every euro figure here is invented to be realistic and marked
`[example]`. Figures taken from [D1](D1-current-business-process-analysis.md),
[D2](D2-predictive-analytics-assessment.md) and [D3](D3-future-business-process.md) are marked
`[D1]`, `[D2]` or `[D3]` and are reused unchanged. No number here is a measurement.

**One new figure carries the rest: annual revenue of €95m** `[example]`. D1 never states it, and
every value row needs it. It fits D1's own baseline. €18.6m of stock turning 3.2 times a year is
€59.5m of goods sold. That is 63% of €95m, a normal cost ratio for a manufacturer.

These are worked examples, not a full inventory.

---

## 1. Business value assessment matrix

*All six categories, with the reference framework's benefit level and the euro effect underneath it.*

| Value category | Benefit level | Effect on profit per year `[example]` | Why |
| :--- | :---: | :--- | :--- |
| **Revenue growth** | **High** | **+€0.2m** | Fewer stockouts on the fast families. Sales that are lost today are captured |
| **Cost reduction** | **High** | **+€0.4m** *(plus €1.3m of cash released once)* | Less money parked in slow-moving stock, and less express freight to cover shortages |
| **Customer satisfaction** | **High** | **+€0.15m** | On-time delivery to more than 5,500 practices `[case]`. Fewer credits, fewer accounts lost |
| **Productivity** | Medium | **+€0.1m** | Eight regional spreadsheets and the manual merge disappear `[D3 §2]` |
| **Risk reduction** | **High** | **+€0.3m** | Supplier lateness is seen a month early instead of absorbed afterwards |
| **Sustainability** | Medium | **+€0.05m** | Fewer air-freight shipments and less stock written off unsold |
| **Total** | | **+€1.2m per year** | About 1.3% of revenue |

### Where each figure comes from

| Category | The arithmetic `[example]` |
| :--- | :--- |
| Revenue growth | Stockouts cost about 1.5% of revenue, €1.4m. The plan recovers a third of it, €0.5m of sales, worth €0.2m at a 37% margin |
| Cost reduction | Slow families hold €8.4m of the €18.6m stock `[D1 §4]`. A 15% cut releases €1.3m and saves €0.23m of holding cost at 18% a year. Express freight runs at €0.6m a year and falls by a quarter, €0.15m |
| Customer satisfaction | 310 complaints a quarter, 58% about delivery `[D1 §4]` — 720 delivery complaints a year. A third fewer, plus a third of the practices lost to late delivery retained |
| Productivity | 264 days a year returned: eight regional managers at two days a month, the demand planner at six. At €400 a day |
| Risk reduction | Suppliers deliver on time 78% of the time, and two of them cause more than half the delay `[D1 §4]`. Predicting the delay removes half the rush production and expediting it causes |
| Sustainability | Air freight follows express freight down. Write-offs on slow-moving families fall by a quarter |

### Three things to read carefully

**The €1.3m is cash, not profit.** It is released once, when slow-moving stock comes down. It does
not repeat, and it is kept out of the €1.2m total and out of the payback in §2.

**Two categories score Medium, and that is the honest answer.** Productivity improves because
spreadsheet work disappears, not because anyone leaves — the days go back into the work. The
sustainability gain is real and small; a demand planning project is not an environmental
programme.

**None of this arrives on day one.** The value above is the steady state, with all eight families
running in the new process. §2 shows what is realised when.

---

## 2. The four-phase roadmap

```
[Phase 1: Improve Data]              months 1–4     €120k
  ├── Audit the two years of sales and stock history, per family
  ├── Stop overwriting the promised delivery date when an order is rescheduled
  └── Save the draft forecast and a reason code for every adjustment
         │
         ▼
[Phase 2: Implement Analytics]       months 5–8     €180k
  ├── Build the accuracy report and the deviation explanation
  ├── Train the demand forecast (P1) and the supplier risk model (P2)
  └── Back-test both against the same two years the planners worked from
         │
         ▼
[Phase 3: Integrate into Process]    months 9–12    €150k
  ├── Put the recommendation and its tolerance band into the planning tool
  ├── Train Sales, Demand Planning, Finance and Procurement on the new cycle
  └── Run implants and consumables through a full cycle, end to end
         │
         ▼
[Phase 4: Continuous Improvement]    month 13 on    €90k a year
  ├── Watch forecast accuracy and bias for drift; review the bands each quarter
  ├── Add the remaining six families as their history passes the Phase 1 checks
  └── Build P3 once twelve months of draft-versus-agreed forecasts exist
```

All four costs are `[example]`. They total €450k to reach a running pilot, then €90k a year.

### What each phase must prove before the next one starts

| Phase | Exit criterion | Resources |
| :--- | :--- | :--- |
| **1 — Improve data** | The draft forecast and a reason code are recorded for three consecutive months, and a data dictionary exists for the fields the model needs | Demand planner (half time), one ERP analyst, external data-quality review |
| **2 — Implement analytics** | P1 and P2 beat today's spreadsheet on the same history, measured by forecast accuracy | One data scientist (part time), analytics platform subscription, the ERP analyst |
| **3 — Integrate into process** | Two families complete a full cycle in the new process, with Finance's bands set up front and every change carrying a reason | Demand planner (full time), process lead, trainer, IT integration |
| **4 — Continuous improvement** | Reviewed each quarter, not exited. A family joins only when its history passes the Phase 1 checks | Demand planner, quarterly model review, Finance for the band review |

**Phase 1 starts this month and needs no system.** Saving the draft forecast and picking a reason
code are habits, not software. `[D2 §6]` Every month without them is a month of learning thrown
away, and no later investment recovers it.

**Phase 2 cannot start early.** A forecast that cannot be scored cannot be trusted. `[D3 §4]`
Phase 1 is what makes the score possible.

**Phase 3 pilots on two families, not eight.** D2 rated the data *partially ready*, with two of
six readiness items red. `[D2 §5]` Implants and consumables have the strongest sales history of the
eight families. They are also the two families D3 §1 already works through. `[D3 §1]` The pilot
tests recommendations that are written down, not new ones.

### Investment against benefit

| | Year 1 | Year 2 | Year 3 |
| :--- | ---: | ---: | ---: |
| Spend `[example]` | €450k | €90k | €90k |
| Benefit realised `[example]` | €90k | €1.0m | €1.2m |
| Cumulative position | −€360k | +€550k | +€1.66m |

**The project pays for itself in month 19** `[example]` — nine months after the pilot goes live.
Year 1 shows almost no benefit because nothing is running until month 10, and then only two
families. Year 2 is the scale-up. The benefit builds through the year as families join, not evenly;
an even split would show payback around month 17. Year 3 is the steady state from §1.

A roadmap showing €1.2m from month one would be easier to sell and would not be credible.

---

## 3. Change management plan

### Affected departments

| Department | What changes for them | Effort |
| :--- | :--- | :---: |
| **Sales** — 8 regional managers | The monthly spreadsheet is gone. They review exceptions and give a reason for every change `[D3 §5]` | **High** |
| **Demand Planning** | Stops assembling numbers, starts managing exceptions and owning the decision log `[D3 §5]` | **High** |
| **Supply Chain & Procurement** | Acts on a supplier risk figure before the delay, with about two weeks more lead time `[D3 §5]` | **High** |
| **Production Planning** | Receives a steadier plan with fewer late changes. Fewer rushed batches | Medium |
| **Finance** | Sets the budget limits and the bands at the start of the cycle instead of reviewing a finished plan `[D3 §5]` | Medium |
| **IT** | Runs the analytics platform and the ERP integration. New data to keep, none to delete | Medium |
| **Customer Support** | Sees fewer delivery complaints and gets a delivery date it can trust | Low |

### Who owns the data — the missing accountability

**D1 found that nobody owns forecast quality, and named it the root cause.** `[D1 §5.4]` A roadmap
that fixes the process without fixing that would rebuild the same problem on better software. Five
roles have to exist by name before Phase 1 records its first reason code.

| Role | Who at Larkfield | What they are accountable for |
| :--- | :--- | :--- |
| **Business Owner** | Head of Supply Chain | Why the data is worth having. Sets the targets the forecast is judged against and approves what the data may be used for |
| **Data Owner** | Head of Demand Planning | The forecast data domain: what a "unit" means, what may not be overwritten, who gets access. Answers for quality targets being met |
| **Data Steward** | The demand planner | The day-to-day guardian. Owns the decision log's completeness, watches the quality score, and is the person to ask what a field means |
| **IT / Data Engineering** | IT | The pipelines, the ERP integration and the security around them. Builds it and keeps it running; does not decide what the numbers mean |
| **Executive Management** | The Executive Board | Funding, the stop-or-go gates, and the decision-log safeguard. Owns the strategy, not the data |

**The split that matters is Data Owner from IT.** Today, when two reports disagree, the question
goes to IT — who can say what the system did and cannot say which number is correct. That is the
governance gap D1 found `[D1 §5.4]`, and it is closed by naming a Data Owner, not by buying
anything.

**None of these is a new job.** All five are people already in post, taking on a named
accountability they do not have today. The Data Steward role is the only one that changes how
somebody spends their week, and it is the same shift D3 already describes for the demand planner:
from assembling numbers to owning the exceptions. `[D3 §5]`

### Anticipated resistance

| Who | What they fear | Whether the fear is fair |
| :--- | :--- | :--- |
| **Regional sales managers** | The decision log exposes judgement that is private today, and will be used to rank them | **Fair, and the biggest risk in the project.** See the safeguard below |
| **Demand planner** | The role disappears with the spreadsheets | Not fair. The role grows — it moves from clerical work to owning the exceptions |
| **Procurement** | A "72% chance of late" is not a fact, and acting on it will look wrong when the delivery arrives on time | Fair. A probability is right on average and wrong in individual months. Training has to cover this |
| **Finance** | Setting bands up front gives up the final veto `[D3 §2]` | Partly. The authority is the same, exercised three weeks earlier |
| **Everyone** | The algorithm decides and people carry the blame | Not fair by design. Analytics recommends, a person approves `[D-004]` |

#### The safeguard the whole design depends on

**The decision log is never used in an individual performance review.** That rule is permanent. For
the first year, reason codes are also reported by code only, never by manager.

D3 named this as the change most likely to fail. `[D3 §5]` The first time the log is used to make a
point about a person, it fills with whichever code is safest. The data then becomes worthless. The
question the log exists to answer — *which kinds of reasoning turn out to be right?* — can only be
answered while people answer it honestly.

Write the rule down before Phase 1 records its first reason code. A safeguard introduced after the
first performance conversation arrives too late.

### Communication

| Group | The message | The message to avoid |
| :--- | :--- | :--- |
| Regional sales managers | "Your judgement stops being invisible and starts being evidence" | "The system will check your numbers" |
| Demand Planning | "You stop chasing eight spreadsheets and start managing the exceptions" | "The forecast is automated now" |
| Supply Chain & Procurement | "You hear about a late supplier a month early instead of on the day" | "The model will tell you what to order" |
| Finance | "Your limits shape the plan before it is built, not after" | "Approval moves into the system" |
| Executive Board | "Six of the eight steps improve with no AI at all" `[D3 §2]` | "This is our AI project" |

One message runs through all of them: **this replaces spreadsheet work, not judgement.**

### Training

| Who | What | When | How long |
| :--- | :--- | :--- | :--- |
| Everyone in the seven departments | Data literacy: what a forecast error is, what bias is, what a probability means | Phase 2 | Half a day |
| Regional sales managers | Working the exception list; choosing a reason code and what each one means | Phase 3, before the pilot | Half a day |
| Demand planner | The full cycle, the decision log, and how to spot a model drifting | Phase 3 | Two days |
| Finance | Setting and reviewing the tolerance bands | Phase 3 | Half a day |
| Executive Board and department heads | Reading a probability, and what "partially ready" data can and cannot support | Phase 3 | Half a day |

The heaviest training is half a day for most people. **Nobody has to become a data scientist.**
`[D3 §5]`

### Success KPIs

| KPI | Today | Target | First measurable |
| :--- | :--- | :--- | :--- |
| **Forecast accuracy** (MAPE) | Not measured `[D1 §3]` | 5 points better than the first baseline `[example]` | Month 4 — Phase 1 creates the baseline |
| **Forecast bias**, per family | Not measured `[D1 §3]` | Within ±2% `[example]` | Month 4 |
| **Reason codes captured** on adjustments | 0% `[D1 §2]` | 95% `[example]` | Month 6 |
| **Recommendations accepted unchanged** | No recommendation exists | 60% by month 18 `[example]` | Month 12 |
| **Delivery punctuality** (OTIF) | 87% `[D1 §4]` | 92% by month 24 `[example]` | Month 1 — but counted by hand, so fix the count first `[D2 §3]` |
| **Stock turnover** | 3.2× a year `[D1 §4]` | 3.6× by month 24 `[example]` | Month 1 |
| **Delivery complaints** | ~180 a quarter — 58% of 310 `[from D1 §4]` | 120 a quarter `[example]` | Month 1 |

#### Why "fewer manual overrides" is the wrong KPI

**A human override is the design, not a defect.** `[D-004]` Analytics recommends and a person
approves, so a falling override count would mean people had stopped looking. Chasing that number
would push the process back toward the unrecorded judgement D1 found. `[D1 §5.3]`

Measure two things instead:

1. **The share of overrides that carry a reason code.** Target 95%. An override is not a failure;
   an override nobody can explain later is.
2. **Which reason codes turn out to be right,** reviewed after four quarters. That is the question
   the decision log was built to answer. It needs a year of data before it can be asked.

**Adoption is measured by the first KPI, not the fourth.** If 95% of changes carry a reason, the
process is being used as designed — whether the number was overridden or not.

---

## What management should do next

1. **Approve Phase 1 and start it this month.** €120k over four months, and the two habits that
   cost nothing: save the draft forecast, record a reason for every adjustment. `[D2 §6]`
2. **Write the decision-log safeguard down now,** before the first reason code is recorded. One
   sentence, signed by the Board: the log is not used in individual performance reviews.
3. **Set the pilot scope to implants and consumables,** and hold it there until Phase 3's exit
   criterion is met. The remaining six families join in Phase 4, one at a time.
4. **Expect nothing in year 1.** The value case is €1.2m a year from year 3, and the project pays
   for itself in month 19 `[example, §2]`. Budget against that shape, not against an early return.

---

## Terms used here

| Term | Plain meaning |
| :--- | :--- |
| **Payback** | The month when the money the project has earned catches up with the money it has cost |
| **Working capital** | Cash tied up in stock. Releasing it is a one-off gain, not a yearly profit |
| **Holding cost** | What it costs to keep stock for a year: storage, insurance, and the cash that could have been used elsewhere. Taken as 18% a year here `[example]` |
| **Expediting** | Paying extra to make a late order arrive sooner: express freight, an unplanned production changeover |
| **Model drift** | A model getting worse over time because the world it learned from has moved on |
| **MAPE** | Forecast accuracy: the average percentage by which forecasts miss reality `[D1]` |
| **OTIF** | "On time, in full" — the share of orders arriving when promised *and* complete `[D1]` |
| **Reason code** | A short fixed label chosen when a number is changed: *promotion*, *tender*, *known supplier issue*, *disagree with the model* `[D3]` |
| **Tolerance band** | An agreed limit, in percent or euros. Inside it the system may act alone; outside it a person must approve `[D3]` |

---

## Check against the requirements

| Requirement | Status |
| :--- | :--- |
| Business value assessment matrix, all six categories | ✅ §1 — benefit level and euro effect per row |
| A business justification tied to Demand Planning per row | ✅ §1 — the mechanism in the matrix, the arithmetic below it |
| 4-phase predictive analytics roadmap | ✅ §2 — the reference framework's four phases, rewritten against this process |
| Concrete activities and an exit criterion per phase | ✅ §2 — three activities and one exit criterion each |
| Indicative timeline and resources | ✅ §2 — months 1–12 plus ongoing, with the roles each phase assumes |
| Investment against benefit, with payback | ✅ §2 — three years, payback in month 19 |
| Change management: affected departments | ✅ §3 — seven departments, with the effort each carries |
| Data governance roles named and assigned | ✅ §3 — all five roles, mapped to people already in post; closes the governance gap D1 §5.4 found |
| Change management: anticipated resistance | ✅ §3 — five, each judged fair or not, plus the safeguard |
| Change management: communication strategy | ✅ §3 — per group, including the message to avoid |
| Change management: training requirements | ✅ §3 — five audiences, timed to the phases |
| Change management: success KPIs | ✅ §3 — seven KPIs with baseline, target and first measurable date |
| Consistent with D1, D2 and D3; every figure marked | ✅ throughout — the bands and predictions from D3 §1 are unchanged |
| The board recommendation | ⬜ Out of scope by design — WP5 |
