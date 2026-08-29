# Larkfield Dental Group — Demand Planning — slide-by-slide specification

Expanded from the outline in `measure-first.foundation.md`, page by page. Nine
fields per slide.

**Version 2**, built on htmldeck 0.2.2 in a rebuild against consolidated requirements.
Three things changed against v1: a **colophon** follows the close, every provenance mark carries the
file glyph and **opens its source in a quick view**, and slide 10 carries the reference framework's own limit on a
forecast. Twelve of the thirteen sections are the argument; the colophon is not (DS-085).

**Every figure on every slide is illustrative.** The Larkfield case is fictional and the source
deliverables mark each value `[example]`, `[case]` or `[D-n]`. The deck says so on its own surface.

---

## Slide 1 — Two opposite problems, one cause

- **Archetype.** A-04 Two-Column Ledger.
- **Title.** Two opposite problems, one cause
- **Bottom line.** Too much stock and too little stock come from the same forecast.
- **Structure.** Two equal columns on one grid, both genuinely argued — the failure mode of A-04 is a
  weaker side, and here the two sides carry three figures each. Left column *Too much stock*, right
  column *Too little stock*. The bottom line sits below both, starting on the same left edge as the
  columns and running to the measure the shell caps it at — 1500 of the content column's 1726
  design units — so the reader's eye lands on the join rather than on either column. **Nothing
  spans the content column here**: `--bottom-measure` holds a bottom line to a readable line length
  on every slide of every deck, so *full width* is not a layout this shell offers. Tier one is everything except the
  scope panel.
- **Text.** Left, under the heading *Too much stock*: `€18.6m held in stock` · `45% of it in two slow
  families` · `turning 1.4× a year`. Right, under *Too little stock*: `87% of orders arrive on time`
  · `~310 complaints a quarter` · `58% of them about delivery`. One standfirst above the columns:
  *Demand for dental products keeps growing. Both of these are getting worse.*
- **Visuals.** No diagram. The two columns are the visual: a shared baseline grid track, one accent
  rule under each heading, and **two figures per side set at display weight** — `€18.6m` and
  `45%` left, `87%` and `310` right — so the symmetry reads at a glance from four marks rather
  than six. The third figure on each side sits inside the note under the second, where it qualifies
  the number above it rather than competing with it. A diagram here would assert a relationship the slide has not yet earned (X-04).
- **Animations.** Rise, staggered, left column then right, so the two halves arrive as a pair rather
  than as one list.
- **Interactive elements.** One `.disc`, `data-disc="scope"`, labelled *What "on time" counts*. It
  says that Larkfield counts on-time delivery by hand and does not count *in full* at all, so the 87%
  is narrower than the industry's OTIF measure. Tier one reads without it.
- **Sources.** `D1-current-business-process-analysis`

---

## Slide 2 — The plan is negotiated, not calculated

- **Archetype.** A-08 Process / Flow.
- **Title.** The plan is negotiated, not calculated
- **Bottom line.** A rejected plan goes back to the meeting, never back to the data.
- **Structure.** The diagram occupies the upper two thirds at full width. Three supporting fragments
  sit in a row beneath it. The bottom line is last and carries the slide's one accent emphasis.
- **Text.** Fragments: `3 of every 4 weeks spent producing the plan` · `8 regional spreadsheets,
  8 layouts` · `no reason recorded for any change`. Standfirst: *The monthly demand plan, as it runs
  today.*
- **Visuals.** Inline SVG, the As-Is process reduced to five boxes on one row: `Calculate draft` →
  `8 regions adjust` → `Merge and compare` → `Monthly meeting` → `Finance checks budget`, then a
  decision diamond `Fits the budget?` and a terminal `Release plan`. **The rejection loop is the
  picture**: from the diamond, a labelled edge *no — renegotiate* runs backwards **above** the row
  and re-enters `Monthly meeting`, not `Calculate draft`. That backward edge carries the accent; every
  other stroke is the neutral UI-line role. The diamond is sized from its own label so the outline
  never crosses the text, and the backward edge's label sits clear of both the edge and the boxes it
  passes over.
- **Animations.** Current on the forward connectors and on the backward edge — dashed, looping — so
  the direction of the loop is visible with nobody talking. A persistent motion-stop control is
  required by the deck because this motion loops.
- **Interactive elements.** None. The point is the shape of the loop and it is entirely on the face.
- **Sources.** `D1-current-business-process-analysis`

---

## Slide 3 — Nothing here measures the forecast

- **Archetype.** A-03 Single Number.
- **Title.** Nothing here measures the forecast
- **Bottom line.** Larkfield measures its results carefully and its forecast not at all.
- **Structure.** The figure **0** at display size on the left third, with its one line of
  interpretation directly under it — *measurements of forecast quality*. The right two thirds carry
  two short stacked lists under mono labels `MEASURED` and `NOT MEASURED`. The interpretation is the
  slide: the number alone means nothing.
- **Text.** `MEASURED`: revenue against budget · stock value · delivery punctuality · complaint
  numbers. `NOT MEASURED`: forecast accuracy · forecast bias · stockout rate. Standfirst: *This is
  descriptive analytics — what happened. It is the first question and Larkfield answers it well.*
  One note at the side of the `MEASURED` list: *delivery punctuality is counted by hand.*
- **Visuals.** No diagram. Two lists and one number, aligned on a shared grid track so the four
  measured items and the three missing ones read as one set split in two.
- **Animations.** Rise on the two lists. One Pulse-once on the figure 0, and nowhere else on the
  slide.
- **Interactive elements.** None. Seven items is not enough to need a second tier.
- **Sources.** `D1-current-business-process-analysis`

---

## Slide 4 — The loop that never closes

- **Archetype.** A-10 Architecture View.
- **Title.** The loop that never closes
- **Bottom line.** Nobody owns forecast quality, so the same error repeats every month.
- **Structure.** The mechanism drawn across the upper two thirds, three fragments below it, bottom
  line last. Only the parts the argument turns on are drawn — four nodes and the edge that is
  missing.
- **Text.** Fragments: `two suppliers cause more than half the late deliveries` · `expensive families
  forecast high, consumables low` · `4½ of the 5 standard failure modes`. Standfirst: *This is
  diagnostic analytics — why did it happen.*
- **Visuals.** Inline SVG. Four nodes in a cycle: `Forecast` → `A manager adjusts it` → `The plan
  ships` → `What sold`. Three edges are solid, labelled and directional, with arrowheads
  meeting their targets. **The fourth edge, from `What sold` back to `Forecast`, is drawn
  dashed and quiet, with no arrowhead and the label *never happens*** — an absent edge asserts no
  direction, and drawing it as an arrow would claim the loop closes. A small annotation on the second
  node reads *reason not recorded*. The gap in the ring is the whole slide.
- **Animations.** Rise on the nodes, clockwise. Current on the three real edges only; the missing
  edge does not animate, which is the encoding.
- **Interactive elements.** One `.disc`, `data-disc="instances"`, labelled *The five failure modes*.
  It names all five — poor data quality, missing data, data silos, no ownership, lack of governance —
  with Larkfield's verdict on each, because the face states the count and the reference framework expects the full
  list. No ownership is marked as the root one.
- **Sources.** `D1-current-business-process-analysis`

---

## Slide 5 — Poor exactly where we decide

- **Archetype.** A-06 Small Multiple.
- **Title.** Poor exactly where we decide
- **Bottom line.** The data is partially ready: strong sales history, and two records we choose not
  to keep.
- **Structure.** Two panels side by side, each a repeated facet with a positional encoding. Left:
  the six data quality dimensions, each a row with a five-position scale and one filled mark. Right:
  the six AI readiness items, each a row with one of three verdict marks. Every comparison is
  positional, which is what makes the shape readable in two seconds: the left block's marks cluster
  low, the right block's show two at the bottom.
- **Text.** Left panel heading `DATA QUALITY — SIX DIMENSIONS`, scale labels `Poor` to `Excellent`,
  rows: Accuracy · Completeness · Consistency · Validity · Timeliness · Uniqueness. Right panel
  heading `AI READINESS — SIX CHECKS`, rows: Enough history · Enough records · Representative ·
  Accessible · Legal · Documented. Two fragments under the panels: `2 Poor, 2 Fair, 2 Good — nothing
  above Good` · `2 red, 3 amber, 1 green`.
- **Visuals.** Inline SVG for both panels. The rating marks are drawn, not typed, so position carries
  the value rather than a word. A legend is required and visible: green, amber and red each named
  once. The two panels share a vertical grid so the twelve rows align across the slide.
- **Animations.** Rise, staggered down the rows, left panel then right.
- **Interactive elements.** One `.disc`, `data-disc="instances"`, labelled *Why each rating*. One
  line per row, twelve lines, giving the reason behind each mark — the completeness row names the two
  missing records, the representative row names the growing-market-only history. The face carries
  every name and every mark; the panel carries only the reasons.
- **Sources.** `D2-predictive-analytics-assessment`

---

## Slide 6 — Fix the data worth fixing first

- **Archetype.** A-10 Architecture View.
- **Title.** Fix the data worth fixing first
- **Bottom line.** Three of the four most valuable data assets need work, and that work is Phase 1.
- **Structure.** A 2×2 matrix filling the centre of the slide, business value on the vertical axis
  and data quality on the horizontal. Each quadrant is a labelled region holding the assets that sit
  in it, and the *remediate* quadrant carries the accent. One fragment sits under the matrix.
- **Text.** Quadrant labels: `START HERE` (high value, high quality) · `REMEDIATE FIRST` (high value,
  low quality) · `CHEAP QUICK WIN` (low value, high quality) · `LEAVE IT` (low value, low quality).
  Contents — **`REMEDIATE FIRST` holds exactly three, and they are the three the bottom line
  counts**: supplier delivery dates · the draft forecast and its reason codes · practice counts per
  market. `START HERE`: two years of sales and stock history. `CHEAP QUICK WIN`: public economic
  indicators. `LEAVE IT`: free-text notes on orders. Fragment: *the remediate quadrant is Phase 1 of
  the roadmap.*
- **Visuals.** Inline SVG. Axis lines in the UI-line role, quadrant dividers quieter than the axes,
  the *remediate* region tinted with the accent at low opacity. Axis labels sit outside the plot area
  so no label crosses a divider. Asset names are set in the body face, never in mono inside the SVG.
- **Animations.** Rise on the four quadrants, then one Pulse-once on the remediate region. Nothing
  loops.
- **Interactive elements.** One `.disc`, `data-disc="scope"`, labelled *What each quadrant means*.
  Four lines, one per quadrant, saying what is done about the assets in it and why. The face already
  names every asset, so the panel adds the action rather than the list.
- **Sources.** `D5-management-decision-matrix`, `D2-predictive-analytics-assessment`

---

## Slide 7 — Two of eight steps need AI

- **Archetype.** A-08 Process / Flow.
- **Title.** Two of eight steps need AI
- **Bottom line.** Six of the eight steps improve with no AI at all.
- **Structure.** The redesigned process across the upper two thirds, in two rows of four so no box
  falls below the type floor. Two fragments below. The two AI steps carry the accent and a small
  marked badge; the other six are neutral.
- **Text.** The eight steps, **in the order they run**: **1 `Finance sets the limits`** · 2 `Report
  last month's accuracy` · 3 `Explain the biggest deviations` · 4 `Forecast demand and supplier
  risk` · 5 `Recommend an action per family` · 6 `Screen the exceptions` · 7 `Approve or change, and
  record why` · 8 `Order and schedule`. Steps 4 and 5 are the two marked as needing a trained model.
  Fragments: `the 8 regional spreadsheets are gone` · `no rejection loop at the end`. Standfirst:
  *The same process, redesigned.*
- **Visuals.** Inline SVG, two rows of four boxes with labelled connectors, and a return connector
  from step 7 to step 4 labelled *decision log feeds next month's forecast* — the loop that was
  missing on slide 4, now drawn as a real directional edge with an arrowhead meeting its target.
  **Finance's box is first and is drawn first**, because Finance now sets the limits before the plan
  is built rather than checking a finished plan at the end. The two AI steps are marked by a badge
  and the accent, and the badge is explained by a visible legend rather than by the presenter.
- **Animations.** Rise along the process order, so the sequence is the stagger. Current on the return
  connector only — it is the one edge whose direction is the argument.
- **Interactive elements.** One `.disc`, `data-disc="condition"`, labelled *What has to be true
  first*. Three lines: the draft forecast is kept, a reason code is recorded on every change, and the
  bands are set before the cycle starts. Without those three the two AI steps cannot be trusted, and
  the panel says where each one fails if it is skipped.
- **Sources.** `D3-future-business-process`, `D1-current-business-process-analysis`

---

## Slide 8 — Each answer needs the one before

- **Archetype.** A-08 Process / Flow.
- **Title.** Each answer needs the one before
- **Bottom line.** Analytics recommends and a person approves, inside limits Finance sets first.
- **Structure.** A zoom into step 4 of the previous slide's diagram — the analytics platform — so the
  reader sees the same process closer rather than a second one. Four stages left to right, then a
  branch. The branch is where the slide's information is.
- **Text.** The four types, each with its question and one Larkfield example, one line each:
  **Descriptive** *what happened?* — 87% of orders on time · **Diagnostic** *why did it happen?* —
  two suppliers cause more than half the delay · **Predictive** *what will happen?* — Supplier B has
  a 72% chance of delivering late next month · **Prescriptive** *what should we do?* — bring the
  order forward or split it with the second source. Branch labels: *inside the band* → `system acts`
  and *outside the band* → `a person approves`. Fragment: `bands: 10% of plan, €25,000 of order
  value`.
- **Visuals.** Inline SVG. Four boxes in sequence with labelled connectors, then a decision diamond
  labelled `within the band` with two labelled outgoing edges — **this is where the process branches
  and the diagram branches with it**. The diamond is drawn from the measured width of its own label
  so the outline cannot cut the text. The two outcome boxes sit level with each other, one on each
  side; what keeps the edge labels apart is the length of the connectors, sized from the labels
  themselves rather than from the diamond.
- **Animations.** Rise across the four stages in order. Current on the two branch edges, so both
  outcomes read as live.
- **Interactive elements.** One `.disc`, `data-disc="condition"`, labelled *When the system may act
  alone*. Two tests, both of which must pass: the action is easy to undo, and it is inside the agreed
  band. One worked line showing a 12% cut failing the first test despite being a small number.
- **Sources.** `D3-future-business-process`, `D1-current-business-process-analysis`

---

## Slide 9 — €450k in, €1.2m a year out

- **Archetype.** A-09 Timeline with a Gate.
- **Title.** €450k in, €1.2m a year out
- **Bottom line.** The pilot costs €450k over twelve months and pays for itself in month 19.
- **Structure.** One horizontal time axis across the slide, months 1 to 24. Four phase bands sit on
  it, and two marks stand above it: the **month-4 stop-or-go gate** and the **month-19 payback**. The
  gate is the information — everything before it is €120k and everything after it is a decision the
  Board takes later.
- **Text.** Phase bands: `1 Improve data · months 1–4 · €120k` · `2 Implement analytics · months 5–8
  · €180k` · `3 Integrate into process · months 9–12 · €150k` · `4 Continuous improvement · month 13
  on · €90k a year`. **The month-4 gate mark reads, in full: *three consecutive months of draft
  forecasts and reason codes, and a data dictionary for the fields the model needs*.** The month-19
  mark reads `payback`. Fragment: `€1.3m of cash released once, and kept out of the €1.2m`.
- **Visuals.** Inline SVG. A single axis with four bands, the gate drawn as a vertical rule with a
  labelled flag and the payback as a second, quieter mark. The two labels sit on opposite sides of
  the axis so neither can collide with the other. Band labels sit inside their bands where they fit
  and above them where they do not, measured rather than assumed.
- **Animations.** Rise on the four bands, left to right, so the phases arrive in time order. One
  Pulse-once on the month-4 gate.
- **Interactive elements.** One `.disc`, `data-disc="instances"`, labelled *The six value
  categories*. All six with their benefit level and euro effect: revenue growth High +€0.2m · cost
  reduction High +€0.4m · customer satisfaction High +€0.15m · productivity Medium +€0.1m · risk
  reduction High +€0.3m · sustainability Medium +€0.05m. The face states the €1.2m total, so the
  panel names the members of it.
- **Sources.** `D4-implementation-concept`, `D5-management-decision-matrix`
- **Notes.** They will argue about the €1.2m, and it is not what is being approved today. Bring them back to the month-4 gate: €120k, three months of draft forecasts and reason codes, and a data dictionary - then this committee decides again. If the payback month is challenged, concede month 19 is a model output and hold that the gate is not.

---

## Slide 10 — The reason code is the change

- **Archetype.** A-12 Uncomfortable Truth.
- **Title.** The reason code is the change
- **Bottom line.** Eight managers record why they changed a number, and the Board protects them for
  doing it.
- **Structure.** The cost of the recommendation, stated in the deck's own voice before anyone asks.
  A short statement block at the top carries the uncomfortable half; below it, one line naming the
  safeguard, set apart and carrying the slide's emphasis. No diagram — this slide is an argument
  about people and a picture would soften it.
- **Text.** The statement opens on the reason the override exists at all — *the model gives a
  probability, and a person still decides* — which is the reference framework's own limit on predictive analytics
  and reached this deck from there rather than from D1–D5. Then: *For eight regional
  managers this redesign is less work and more exposure.
  Their judgement is private today. From now on the reason sits next to the number and can be scored
  next quarter.* Then the safeguard, set as the slide's one emphasised line: **the decision log is
  never used in an individual performance review.** Two fragments: `target: 95% of changes carry a
  reason` · `sign the safeguard before the first code is recorded`.
- **Visuals.** None. Stated plainly, because the slide's subject is a promise the Board makes.
- **Animations.** Rise on the statement, then the safeguard line, in that order. One Pulse-once on
  the safeguard.
- **Interactive elements.** One `.disc`, `data-disc="condition"`, labelled *What makes this fail*.
  Three lines: the first time the log is used to make a point about a person it fills with whichever
  code is safest; reason codes are reported by code and never by manager for the first year; the
  question the log exists to answer needs a year of honest data. A fourth line names why the override
  exists: a forecast is a probability and not a guarantee, which is the reference framework's own limitation and
  the reason human judgement stays in the process.
- **Sources.** `D4-implementation-concept`, `D3-future-business-process`

---

## Slide 11 — One option survives the evidence

- **Archetype.** A-04 Two-Column Ledger.
- **Title.** One option survives the evidence
- **Bottom line.** Start with a pilot on two families, beginning with four months of data work.
- **Structure.** The chosen option on the left at full weight with its reason; the four refused
  options on the right, each one line with its reason. Both columns are argued — the four refusals
  are reasons, not dismissals, which is what keeps this out of the lopsided-comparison failure.
- **Text.** Chosen: **Start with a pilot project** — *the sales and stock foundation is sound, the
  scope is small enough that being wrong is cheap, and large enough to produce real evidence.*
  Refused: `Start immediately` — two of six readiness items are red · `Improve data quality first` —
  half right, and it is Phase 1 rather than an alternative · `Collect additional data` — the valuable
  data is not bought, it is thrown away each month · `Postpone` — a year of decisions not recorded,
  and no later investment recovers it.
- **Visuals.** No diagram. The asymmetry of weight between one chosen option and four refused ones
  is the visual, and it is built from the grid rather than drawn.
- **Animations.** Rise, the chosen option first and the four refusals after it as one staggered
  group.
- **Interactive elements.** One `.disc`, `data-disc="derivation"`, labelled *How we reached this*.
  The eight-row management decision matrix — business goal, business question, analytics types,
  required data, readiness, expected value, biggest risk, recommendation — each with its answer in
  one line. It is how the option on the face was produced, and every row of it has already appeared
  on an earlier slide.
- **Sources.** `D5-management-decision-matrix`, `D2-predictive-analytics-assessment`

---

## Slide 12 — Approve Phase 1 this month

- **Archetype.** A-14 Verdict / Close.
- **Title.** Approve Phase 1 this month
- **Bottom line.** Approve €120k for Phase 1, and judge the programme on what month 4 shows.
- **Structure.** The ask as one action, set large, with one subtle supporting line beneath it and
  nothing else. The last slide is a close and not a recap.
- **Text.** The ask: **Approve €120k for Phase 1 — four months of data work, starting this month.**
  The supporting line: *Six of the eight steps improve with no AI at all, and month 4 tells you
  whether the other two are worth building.*
- **Visuals.** None.
- **Animations.** Rise on the ask, then the supporting line. No pulse — the slide is already the
  emphasis.
- **Interactive elements.** None. A close that needs a click is not a close.
- **Sources.** `D5-management-decision-matrix`, `D4-implementation-concept`, `D3-future-business-process`

---

## Colophon — What this deck rests on

**Not one of the twelve.** `DS-085` allows exactly one thing to follow the close — a colophon
carrying the deck's sources — and it stays outside the argument, so the ask is still the last thing
the Board is asked to act on.

- **Archetype.** None of the thirteen. A register, not an argument.
- **Title.** What this deck rests on
- **Bottom line.** Open any of the five from the mark in the corner of the slide that cites it.
- **Structure.** Five numbered rows, one per source deliverable, on the same grid track the stat
  rows use. Nothing else on the slide — the scope of `DS-085` is sources and nothing else, so no
  second ask, no summary and no thank-you.
- **Text.** `D1 Current business process analysis` · `D2 Predictive analytics and data readiness` ·
  `D3 Future business process` · `D4 Business value and implementation concept` · `D5 Management
  decision matrix`. Standfirst: *Five documents. Every figure on every slide comes from one of them.*
- **Visuals.** None. The list is the slide.
- **Animations.** Rise, staggered down the five rows.
- **Interactive elements.** None. **Deliberate:** the five sources are already visible here, so a
  disclosure repeating them would be a second copy of the list on the slide whose whole subject is
  the list. Opening a source is done from the twelve slides that cite it, where the reader is when
  the question arises.
- **Sources.** `D1-current-business-process-analysis`, `D2-predictive-analytics-assessment`,
  `D3-future-business-process`, `D4-implementation-concept`, `D5-management-decision-matrix`

---

## Open — needs a decision

| # | The question | Why it matters | Proposed |
| :-- | :--- | :--- | :--- |
| — | _none outstanding._ Every question this specification raised was settled during the run and recorded in that rebuild's own record, because the run was authorised to decide in the owner's place. | | |
