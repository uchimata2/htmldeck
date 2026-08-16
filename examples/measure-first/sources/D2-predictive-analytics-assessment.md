# Deliverable 2 — Predictive Analytics & Data Readiness

**Client:** Larkfield Dental Group · **Process analysed:** Demand Planning
**Work package:** WP2
**Date:** 2026-08-05

---

## About this document

The Larkfield case is fictional. Every figure here is invented to be realistic and marked
`[example]`. Figures carried over from [D1](D1-current-business-process-analysis.md) are marked
`[D1]` and are reused unchanged. Systems are named generically, because we are showing the
approach and not a product. These are worked examples, not a full inventory.

**The question for WP2 is not "which model should we buy?" but "could we train one on what we have
today?"** D1 found a feedback problem, not a forecasting software problem. `[D1]`

---

## 1. What we would predict

*Predictive analytics answers "what will happen?". It uses past patterns to estimate something that
has not happened yet.*

Three examples, each tied to a root cause D1 documented.

| # | Prediction question | Root cause it attacks `[D1 §5.1]` | What it predicts |
| :-- | :--- | :--- | :--- |
| **P1** | **How much will each product family sell next quarter?** | Sales optimism on the expensive families is never corrected; the everyday families get no analytical attention | Units sold, per family per month, three months ahead |
| **P2** | **Which suppliers are likely to deliver late next month?** | Supplier delays are absorbed by re-planning instead of being anticipated | Probability of a late delivery, per supplier per month |
| **P3** | **Will this month's agreed forecast be too high or too low?** | The monthly meeting overrides the calculation with no recorded reason | Forecast error and its direction, per family per month |

**We stay at product-family level** — the eight portfolio families, not thousands of articles.
`[D1]` Two years of history is too thin per article, and the families are the level at which
management decides.

### The one that cannot be built yet

**P3 is impossible today.** That is the most useful finding in this document. To learn whether the
meeting helps you need both numbers: the forecast the calculation produced and the forecast the
meeting agreed. Today the second overwrites the first. `[D1]`

> **Save one extra file each month.** Keep the draft forecast next to the agreed one. No system, no
> licence, no project. From that month on, Larkfield can measure something it has never measured —
> and after a year it holds a dataset nobody else in its market has.

---

## 2. What data we would need

Examples rather than a full catalogue, chosen to show the spread: what exists, what is
half-there, and what is missing. **Internal data says what Larkfield did. External data says what
the market did to it.** A forecast built only on internal history can see its own past and nothing
of the world that moved it, which is why the split below is a column and not an afterthought.

| Data | Internal / External | Why it is needed | Exists today? |
| :--- | :---: | :--- | :--- |
| Order and sales history, two years | Internal | The backbone of P1 — past demand is the strongest predictor of future demand | ✅ In the ERP |
| Stock levels and movements | Internal | Turns a demand forecast into an availability warning | ✅ In the ERP |
| Purchase orders: date promised vs. date delivered | Internal | The basis of P2 — you cannot predict lateness without a record of past lateness | ⚠️ Dates exist, but are overwritten when a delivery is rescheduled |
| **The original draft forecast, kept** | Internal | Without it no forecast can ever be scored, including a future model's | ❌ Overwritten monthly |
| **The reason for each regional adjustment** | Internal | Turns eight managers' judgement from noise into something learnable | ❌ Never written down |
| Number and growth of dental practices per market | **External** | The size of the market, which internal sales figures cannot show | ❌ Would need to be bought |
| **Supplier lead times and upstream stock** | **External** | The other half of P2. Our purchase orders show when a supplier was late; only the supplier's own data shows when they are *about to be* | ❌ Not requested from suppliers today |
| **Economic indicators per market** | **External** | Practice equipment is an investment decision. Treatment units and CAD/CAM move with credit conditions, not with last year's sales | ❌ Free from public sources, never used |
| Public dental health and insurance statistics | **External** | Reimbursement rule changes move consumable volumes across a whole market at once | ❌ Free, never used |

**One reclassification, and it changes a finding.** Purchase-order dates were treated throughout as
internal data. They are the *record of a supplier's past behaviour*, not the supplier's own data —
so P2 today predicts lateness from our own paperwork and nothing else. Asking the two problem
suppliers for lead-time and upstream stock data is an external source, it costs a conversation
rather than a licence, and it is the single cheapest improvement to P2 available.

**The rest of the external list is free.** Economic indicators and public health statistics cost
nothing but the work of pulling them in. Only the practice-count data has to be bought. That order
matters: start with the free sources, and buy nothing until a model has shown it can use them.

**Weather data is deliberately excluded.** It is the standard external source in demand
forecasting, and dental practices do not buy fewer implants because it rained. Naming an
irrelevant source and leaving it out is part of the assessment.

**The data Larkfield has describes what it sold. The data it is missing describes how well it
decided — and what the market was doing while it decided.** That is D1's feedback problem,
appearing again as a data problem.

---

## 3. Is the data good enough? The six quality dimensions

**We score each dimension on a five-point scale — Poor, Fair, Good, Very Good, Excellent — against
one management audit question.** A traffic light would say *amber* six times and tell management
nothing about where to spend. Five points force a ranking, and the ranking is what turns an
assessment into a plan.

| Dimension | The audit question | Rating | Why that rating |
| :--- | :--- | :---: | :--- |
| **Accuracy** | Is the data historically correct and factually reliable? | **Good** | Sales and stock come from invoices and are reliable. Only delivery punctuality is counted by hand, so the 87% OTIF figure carries an unknown error `[D1]` |
| **Completeness** | Are all required attributes and records populated? | **Poor** | The two fields that matter most for prediction — the original forecast and the reason for each adjustment — do not exist at all (§2) |
| **Consistency** | Is the data identical across ERP, CRM and the planning sheets? | **Poor** | Eight markets submit eight spreadsheets in different layouts `[example]` |
| **Validity** | Does the data follow business rules and schema boundaries? | **Fair** | ERP fields are validated; the spreadsheets are not. Units vs. cases, and three date formats across the eight markets `[example]` |
| **Timeliness** | Is data refreshed at the frequency needed to act? | **Fair** | The cycle consumes three of the four weeks, so a forecast is released with about one week left to act on it `[D1]` |
| **Uniqueness** | Is the dataset free of duplicate records? | **Good** | One known duplication pattern: practices buying both directly and through a distributor appear twice `[example]`. It is understood and fixable, not pervasive |

**Two Poor, two Fair, two Good, and nothing above Good.** That shape is the finding. Larkfield has
no excellent data and no catastrophic data — it has a solid transactional core and two specific
holes, both of which are records it chooses not to keep rather than systems it does not own.

**The two Poor dimensions are not equally hard.** Consistency is fixed by removing the eight
spreadsheets, which the redesign does anyway. Completeness is fixed by saving two fields, starting
this month. Neither needs a purchase.

**What Larkfield records, it records reasonably well. The most important things are not recorded at
all.** Everything that passes through a spreadsheet also loses its shape.

---

## 4. The data problems, and the one that matters most

| Problem | What it looks like here |
| :--- | :--- |
| Missing values | ~12% of order lines have no requested delivery date, mostly from the distributor channel `[example]` |
| Duplicate records | The same practice held twice — direct customer and distributor `[example]` |
| Outliers | Three large clinic-chain tenders in two years, each several times a normal month `[example]` |
| Wrong formats | Units vs. cases, and three date formats, across the eight regional sheets `[example]` |
| **Bias** | Two years of history covers a growing market only, and the regional adjustments are systematically optimistic on the expensive families `[D1]` |
| Missing history | Two years is two seasonal cycles — and for P3 there is no history at all, because the draft forecast is never kept |

**Bias is the one to watch.** The other five are visible: you can look at the data and see a gap or a
duplicate. Bias is invisible. The data looks complete and clean while being wrong in one consistent
direction. A model trained on it repeats that error confidently, which is worse than being obviously
broken. D1 found this and could not prove it. `[D1]`

---

## 5. AI readiness checklist

*These are the six standard readiness criteria — the checks a data asset must pass before anyone
builds a model on it. A tick would be worthless, so each item gets a verdict and the reason behind
it. Readiness is a different question from quality (§3): quality asks whether the data is right,
readiness asks whether there is enough of it, and whether we are allowed to use it.*

| Question | Verdict | Reasoning |
| :--- | :---: | :--- |
| **Enough history?** | 🟠 Just barely | Two years is two seasonal cycles — the minimum for spotting a season, not enough to be sure of one |
| **Enough records?** | 🟠 Depends what you count | Order lines run to tens of thousands. But the monthly forecast decision, the thing we most want to learn from, has 24 records per family, and the meeting overrides have none `[example]` |
| **Representative?** | 🔴 No | The history covers a growing market only, so nothing in it shows what a downturn looks like |
| **Accessible?** | 🟠 Partly | ERP data comes out through standard reports. The regional spreadsheets sit in eight separate places and are overwritten monthly |
| **Legal and compliant?** | 🟢 Yes, with care | Demand at family level is commercial data, not personal, so GDPR barely applies. Keep customer records aggregated to the practice, and supplier risk scores internal `[case]` |
| **Documented?** | 🔴 No | No data dictionary: no agreed definition of a "unit", no owner per field. Two people producing the same report get two answers |

### Overall verdict: **partially ready**

Not "no": the sales and stock foundation is sound. P1 and P2 could start on it, with the limits
above stated openly.

Not "yes" either. **Two of six items are red, and both decide whether a result can be *trusted*:**
the history is not representative, and nothing is documented. Three more are amber.

The third weakness is not in this table. The most valuable records do not exist at all. That is
**Completeness** in §3, and it is why P3 cannot be built.

**So: a pilot on the strongest data, while the missing fields start being recorded in parallel.**
Not an enterprise rollout. WP4 and WP5 pick this up.

---

## 6. Which data actually helps — feature examples

*A **feature** is one piece of information a model is allowed to look at. Choosing them well matters
more than choosing the model.*

**Every candidate feature falls into one of four categories, and each category has a different
action.** *Relevant* — keep it. *Irrelevant* — filter it out, because noise dilutes accuracy.
*Redundant* — remove the duplicate, because two columns carrying the same information make a model
confident for the wrong reason. *Missing* — build something to capture it. Sorting Larkfield's
candidates this way is what produced the recommendation in this document:

| Feature | Category | Why |
| :--- | :---: | :--- |
| Past monthly sales per family | **Relevant** | The strongest signal for P1 — demand repeats before it changes |
| Working days in the month, per market | **Relevant** | Separates "a weak month" from "a short month". Free, external, and it removes a lot of false noise |
| Supplier lead-time variance | **Relevant** | For P2, *inconsistency* predicts lateness better than the average lead time does |
| Free-text notes on orders | *Irrelevant* | Written differently by every market, in several languages. High effort, almost no signal |
| Revenue in euros per family | *Redundant* | Quantity × price, which the model already has — and it hides which of the two moved |
| **The original draft forecast** | **Missing** | Without it, P3 is impossible and no forecast can ever be scored |
| **Reason code per regional adjustment** | **Missing** | Would turn eight managers' experience from unusable noise into a learnable signal |

**Both missing rows are decisions Larkfield makes and then throws away.** Neither needs new
software. That is D1's conclusion, reached from the data side. It is also why WP5 recommends
a pilot rather than a full programme.

---

## What management should take from this

1. **The foundation is sound.** Sales and stock data is real, reliable and two years deep. This is
   not a company starting from nothing.
2. **The gaps are decisions, not systems.** What is missing are records of choices already being
   made. Capturing them costs a change of habit, not a budget.
3. **Start recording now, model later.** The first year of kept forecasts is the asset. Every month
   without it is a month of learning thrown away, and no later investment can recover it.

---

## Terms used here

| Term | Plain meaning |
| :--- | :--- |
| **Predictive analytics** | Using past patterns to estimate something that has not happened yet |
| **Feature** | One piece of information a model is allowed to look at when making its estimate |
| **Granularity** | How fine the detail is. Here: product family and month, not article and day |
| **Lead-time variance** | How much a supplier's delivery time swings. One that is always 20 days late is easier to plan for than one varying between 5 and 30 |
| **Bias** *(in data)* | Error leaning consistently one way, so the data looks clean while being systematically wrong |
| **Data dictionary** | A written definition of every field: what it means, who owns it, what counts as valid |
| **OTIF** | "On time, in full" — the share of orders arriving when promised *and* complete |

---

## Check against the requirements

| Requirement | Status |
| :--- | :--- |
| 2–4 prediction questions, each traced to a D1 root cause | ✅ §1 |
| Required data inventory, internal/external, with justification | ✅ §2 |
| All six data quality dimensions, with a verdict and a reason | ✅ §3 — rated on the five-point scale, two Poor, two Fair, two Good |
| Internal and external sources both assessed, with exclusions named | ✅ §2 — four external sources, three of them free; weather excluded with a reason |
| Data problems identified | ✅ §4 |
| AI readiness checklist, a verdict per item | ✅ §5 — overall *partially ready* |
| Feature matrix across the four categories | ✅ §6 |
| Every figure marked `[example]`, `[case]` or `[D1]`; consistent with D1 | ✅ throughout |
