# Deliverable 5 — Management Decision Matrix & Executive Recommendation

**Client:** Larkfield Dental Group · **Process:** Demand Planning
**Work package:** WP5
**Date:** 2026-08-05

---

## About this document

**D5 invents no numbers.** Every figure comes from [D1](D1-current-business-process-analysis.md),
[D2](D2-predictive-analytics-assessment.md), [D3](D3-future-business-process.md) or
[D4](D4-implementation-concept.md) and is marked with its source. The Larkfield case is fictional
and its figures are illustrative, as those documents say.

This is the decision the Executive Board is being asked to take.

---

## 1. Management decision matrix

| Matrix element | Our answer | Source |
| :--- | :--- | :--- |
| **Business Goal** | Cut delivery delays, release the money parked in slow-moving stock, and stop the margin decline | `[case]`, `[D1 §4]` |
| **Business Question** | How much will each product family sell next quarter, and which suppliers will deliver late? | `[D2 §1]` |
| **Selected Analytics Type(s)** | All four, in order: **descriptive → diagnostic → predictive → prescriptive**. Descriptive first, because an unscored forecast cannot be trusted | `[D3 §2, §4]` |
| **Required Data** | Two years of sales and stock history (**exists**); promised versus actual delivery dates (**overwritten today**); the original draft forecast and a reason code per adjustment (**never kept**) | `[D2 §2]` |
| **Is the Data AI Ready?** | ☐ Yes ☑ **Partially** ☐ No — two of six readiness items are red, three more amber | `[D2 §5]` |
| **Expected Business Value** | ☑ **High** ☐ Medium ☐ Low — **€1.2m a year** at steady state, plus €1.3m of cash released once. Payback in month 19 | `[D4 §1, §2]` |
| **Biggest Risk** | **Bias in the two years of history.** It is the one data problem you cannot see, and automation repeats it at machine speed | `[D2 §4]` |
| **Final Recommendation** | **Start with a pilot project** — implants and consumables, with the data work as its first phase | `[D4 §2]` |

### The five decision stages, and where each one is answered

The matrix above has eight rows because that is what WP5 asks for. Underneath it are the five
stages a management decision on an AI project has to pass through, and every one is answered:

| Stage | The question it asks | Answered in the row |
| :--- | :--- | :--- |
| **1. Business Goal** | What problem are we solving, and what is the target? | *Business Goal* |
| **2. Required Data** | What data, features and history would we need? | *Required Data* |
| **3. Available Data** | What exists today, and can we get at it? | *Required Data* — each item is marked **exists**, **overwritten** or **never kept** |
| **4. Quality Audit** | Is it accurate, complete, consistent, valid and current? | *Is the Data AI Ready?* — scored against the six quality dimensions in `[D2 §3]` and the six readiness criteria in `[D2 §5]` |
| **5. Recommendation** | Proceed, remediate, or pivot? | *Final Recommendation* — remediate first, then proceed |

**Stages 2 and 3 share a row on purpose.** Splitting *required* from *available* into two rows would
hide the only thing that matters about them: the gap between them. Marking each required item with
whether it exists puts the gap on one line, and that gap is the recommendation.

### 1.1 Which data earns the investment first

**Not all data is worth fixing.** Two things decide: what a data asset is worth to the business, and
how good it is today. Plotting Larkfield's assets against both is what produced the phased roadmap
rather than a general clean-up.

```
                 High │  REMEDIATE FIRST              START HERE
                      │  · Supplier delivery dates    · Sales & stock history
              BUSINESS│  · Draft forecast + reasons     (2 years, from invoices)
                VALUE │  · Practice counts (buy)
                      ├──────────────────────────────────────────────────
                      │  DEPRIORITISE                 CHEAP QUICK WIN
                  Low │  · Free-text order notes      · Economic indicators
                      │                                 (public, clean, free)
                      └──────────────────────────────────────────────────
                         Low            DATA QUALITY            High
```

| Where it sits | The assets | What we do about it |
| :--- | :--- | :--- |
| **High value, high quality** | Two years of sales and stock history, straight from invoices `[D2 §3]` | **Start here.** This is the only quadrant ready for a model today, and it is what P1 and P2 are built on |
| **High value, low quality** | Supplier delivery dates (overwritten), the draft forecast and reason codes (never kept), practice counts (not owned) `[D2 §2]` | **Remediate.** This quadrant *is* Phase 1 of the roadmap `[D4 §2]`. High value and unusable is the definition of work worth funding |
| **Low value, high quality** | Public economic indicators `[D2 §2]` | **Quick win.** Free, clean, and worth adding once a model exists to use them. Not a reason to delay anything |
| **Low value, low quality** | Free-text notes on orders `[D2 §6]` | **Leave it.** Written in several languages by eight markets, with almost no signal. Cleaning it would cost real money and change no decision |

**The matrix explains the roadmap's shape.** Four months of data work before any model looks slow
until you see that three of Larkfield's four most valuable data assets sit in the *remediate*
quadrant. Phase 1 is not preparation for the project — it is the project's highest-value quadrant
being worked first.

### Two cells where we did not take the obvious answer

**The business question names two predictions, not "can we use AI?"** A board question has to be
answerable. *How much will each family sell* and *which suppliers will deliver late* are the two
questions D2 showed are buildable on data Larkfield already has. `[D2 §1]`

**The biggest risk is bias, not poor data quality.** Poor data quality is the expected answer and
it is too broad to act on. D2 listed six data problems, and five of them are visible: you can look
at the data and see a gap, a duplicate, an outlier, a wrong format, a short history. **Bias is
invisible.** Larkfield's history covers a growing market only, and the regional adjustments lean
optimistic on the expensive families. `[D2 §4]` The data looks clean while being wrong in one
consistent direction, and a model trained on it repeats that error confidently. That is worse than
a model that is obviously broken.

---

## 2. The five options

*The Board is choosing one of five. Here is what each would mean at Larkfield.*

| Option | Verdict | Why |
| :--- | :---: | :--- |
| Start the project immediately | **No** | Two of six readiness items are red `[D2 §5]`. A full rollout on undocumented, unrepresentative data would produce confident recommendations nobody can check `[D3 §4]` |
| **Start with a pilot project** | ✅ **Chosen** | The sales and stock foundation is sound, so two families can start now. The scope is small enough that being wrong is cheap, and large enough to produce real evidence `[D2 §5]`, `[D4 §2]` |
| Improve data quality first | **No — but it is half right** | This is Phase 1 of the pilot, not an alternative to it. Run as a separate project it has no business outcome, no owner in the process, and no date at which anyone decides anything |
| Collect additional data | **No** | The valuable missing data is not bought, it is *thrown away every month*: the draft forecast and the reason for each adjustment `[D2 §6]`. Collecting more of what we already have adds nothing |
| Postpone the project | **No** | The cost of waiting is a year of decisions not recorded, and no later investment recovers it `[D2 §6]` |

### The close call, and how it was settled

**"Improve data quality first" and "start with a pilot" are not really opposites here.** Our
roadmap does the data work first — Phase 1 is four months of exactly that. `[D4 §2]`

The difference is what management approves today. A data quality project is approved on faith and
reports on data. A pilot is approved on a business case. Its first phase happens to be data
work, with a stop-or-go gate at the end. The second one is easier to fund, easier to stop, and
puts the missing records into the hands of the people who will use them.

**We reach the same option the reference framework suggests, for reasons of our own.** The evidence
that decided it is Larkfield's, not the template's. It is sound sales history, two red readiness
items, and missing fields that cost nothing to start capturing.

---

## 3. Executive recommendation

> ☐ Start the project immediately
> ☑ **Start with a pilot project**
> ☐ Improve data quality first
> ☐ Collect additional data
> ☐ Postpone the project

### Executive justification

> We recommend a pilot on two product families — implants and consumables — beginning with four
> months of data work. Larkfield's sales and stock records are sound and two years deep, but the
> two facts that matter most are thrown away every month: the forecast our own calculation
> produced, and the reason a manager changed it. Capturing them costs a change of habit, not a
> budget, and until they exist we cannot tell whether our forecasts are getting better or worse.
> The pilot costs €450,000 over twelve months and returns about €1.2m a year once all eight
> families are running, paying for itself in month 19. `[D4 §2]` We ask the Board to approve
> Phase 1 now, and to judge the whole programme on the evidence it produces in month 4.

---

## 4. What management is being asked to approve

| The ask | Detail | When |
| :--- | :--- | :--- |
| **Approve Phase 1** | €120k, four months of data work `[D4 §2]` | This month |
| **Sign the decision-log safeguard** | One sentence: the log is never used in an individual performance review `[D4 §3]` | Before the first reason code is recorded |
| **Name the two pilot families** | Implants and consumables `[D4 §2]` | With Phase 1 |
| **Set the stop-or-go gate** | Phase 2 starts only if the draft forecast and reason codes have been recorded for three consecutive months **and a data dictionary exists for the fields the model needs** `[D4 §2]` | Month 4 |
| **Fund Phases 2 and 3** | €330k, subject to the month-4 gate | Month 5 |

**The first evidence arrives in month 4.** That is when Larkfield can answer a question it has
never been able to answer: how accurate is our forecast, and does it lean high or low? `[D1 §3]`

**Nothing here commits the company to an AI programme.** Six of the eight steps in the redesigned
process improve with no AI at all. `[D3 §2]` The two that need a model are the last to be built.
They come only after the other six have produced the data they would learn from.

---

## 5. The risk, and what we do about it

**Bias is the biggest risk, and it cannot be removed — only watched.**

| What we do | Why it works |
| :--- | :--- |
| Measure forecast bias per family from month 4, and hold it within ±2% `[D4 §3]` | Bias is invisible in the data and visible in the score. Measuring it is the only way to see it |
| Keep a person on every decision that is large or hard to undo `[D-004]` | A biased recommendation that a person rejects costs nothing. One that a system executes costs a quarter |
| Pilot two families, not eight | If the history misleads us, it misleads us on two of the eight families `[D4 §2]` |
| Record the reason for every change | After four quarters the company can ask which kinds of reasoning proved right `[D4 §3]` |

**The honest limit:** Larkfield's history contains no downturn. `[D2 §5]` If the dental market
turns, the forecasts will be wrong in the same direction at the same time. The human approval
step is the only thing standing behind them. That is not a reason to wait. It is a reason to keep
the bands narrow until the models have been through a bad quarter.

---

## Terms used here

| Term | Plain meaning |
| :--- | :--- |
| **Bias** *(in data)* | Error leaning consistently one way, so the data looks clean while being systematically wrong `[D2]` |
| **AI readiness** | Whether the data can support a trustworthy model: enough history, enough records, representative, accessible, legal, documented `[D2]` |
| **Stop-or-go gate** | A date and a test agreed in advance. The next phase is funded only if the test passes |
| **Payback** | The month when the money the project has earned catches up with what it has cost `[D4]` |
| **Tolerance band** | An agreed limit. Inside it the system may act alone; outside it a person must approve `[D3]` |

### Decisions referenced by mark

`[D-004]` is cited in D3, D4 and in the to-be process diagram, and this is where it is recorded.

| Mark | The decision | Taken |
| :--- | :--- | :--- |
| `[D-004]` | **Analytics recommends; a person approves.** No forecast, order or replenishment is executed by the system alone where the decision is large or hard to undo. Inside an agreed tolerance band the system may act; outside it, a named person approves and the reason is recorded | With the future process, D3 §1 |

---

## Check against the requirements

| Requirement | Status |
| :--- | :--- |
| Matrix filled for all eight elements | ✅ §1 — each cell sourced to D1–D4 |
| All five management decision stages answered | ✅ §1 — mapped onto the eight rows; stages 2 and 3 share a row so the gap between them is visible |
| Data prioritised by business value against data quality | ✅ §1.1 — four quadrants, and it is what gives the roadmap its shape |
| AI readiness verdict consistent with WP2 | ✅ §1 — *Partially*, two of six red, unchanged from D2 §5 |
| Exactly one of the five options selected | ✅ §3 — *Start with a pilot project* |
| All five options shown, with a rejection reason | ✅ §2 |
| Justification of 3–5 sentences, no data vocabulary | ✅ §3 — five sentences |
| What management must approve, and when they see results | ✅ §4 — five asks, first evidence in month 4 |
| The recommendation derived from our evidence, not inherited | ✅ §2 — same option as the reference framework, reached from Larkfield's own findings; the biggest risk differs from the template's |
| No new figures invented; every figure marked and sourced | ✅ throughout |
| The decision-log safeguard stays in D4 | ✅ §4 references it; it is not restated |
| Slide production | ⬜ Out of scope by design — the presentation work package |
