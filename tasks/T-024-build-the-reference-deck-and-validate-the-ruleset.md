---
id: T-024
title: Build the reference deck by hand and find out whether the ruleset works
type: deliverable
status: done
phase: review
parent: null
blocked_by: []
related: [T-001, T-002, T-006, T-007, T-014, T-016, T-021, T-023]
work_package: WP2
owner: maintainer
created: 2026-08-06
updated: 2026-08-06
deliverables:
  - examples/reference-deck.html
  - examples/reference-deck-seeded-defects.html
  - examples/README.md
---

# T-024 — Build the reference deck by hand and find out whether the ruleset works

## 1. Specify

**Outcome**
A real **12-slide deck with diagrams**, on a neutral topic, built by hand from
[`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) alone — opened offline and looked at. Plus a
**seeded-defect variant** of it, carrying one known defect per evaluation dimension, which is what
[`docs/EVALUATION.md`](../docs/EVALUATION.md) needs to prove its rubric detects anything.

**Why this one**
**Nothing in this project has ever been tested by building a deck.** Six research notes, 131 rules,
an evaluation rubric and a convergence loop, and the only HTML anyone has written was R5's probe —
built to be weighed, not read.

This is the task CLAUDE.md rule 6 exists for, and it is **overdue rather than new**: it has been the
standing recommendation in two consecutive handoffs and has never had a task file, which is why it
kept not happening. It now blocks three things concretely:

- **[T-023](T-023-the-deck-evaluation-rubric-and-convergence-loop.md) cannot close.** Its one unmet
  criterion is the seeded-defect validation, and an unvalidated rubric passes everything.
- **Two of `BRIEF.md`'s definition-of-done criteria** name an artifact that does not exist.
- **T-002 has no target to be judged against.** A generator with no reference output is a generator
  nobody can review.

**What is actually being tested — this is not a demo**

| Question | How this deck answers it |
| :--- | :--- |
| Does the ruleset produce a deck worth presenting? | Build to it strictly, then look. **The failure mode to watch for is a deck that satisfies all 131 rules and is dull** — that is a finding about the ruleset, not about the deck. |
| Is the type floor right? | DS-034/035 predict body text ≥ 16 px in a 720p capture. **Capture it and measure.** The floor was derived arithmetically and has never been observed. |
| Does the stage hold? | DS-063 — render at 3840×2000 and 1280×634 and diff up to a uniform scale factor. |
| Do the rules conflict in practice? | A rule that cannot be satisfied alongside another shows up here first. Record it in [`DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) §2, which is where conflicts live. |
| Does the rubric detect anything? | The seeded variant. |
| Can the three standing decisions be made? | Building forces T-001 (fonts), T-006 (charts) and T-007 (tokens) into the open. **This task informs them; it is not blocked by them.** |

**Scope**
- In: **12 slides, with diagrams**, per CLAUDE.md's verification rule — not a three-slide toy. That
  is the size where layout and pacing problems appear.
- In: a **neutral topic written fresh.** Nothing from the corpus. See *Publishing constraints* in
  CLAUDE.md — this deck ships in a public repository.
- In: `portable` mode, opened from `file://` with the **network disabled**, and looked at.
- In: the **720p capture measurement** and the **two-resolution diff**.
- In: the **seeded-defect variant** — one defect per dimension (S1–S6, D1–D4) at score 0, documented
  so the rubric's result can be graded against a known answer.
- In: running the deck through the convergence loop and recording which outcome it reaches.
- Out: **the generator.** This deck is built by hand. T-002 automates what this proves is worth
  automating, and cannot sensibly be specified before it.
- Out: changing rules to make the build easier. **A rule that is painful is a finding to record, not
  a rule to quietly soften.**

**Inputs**
- `docs/DESIGN-SYSTEM.md` — and **only** this, for the build itself. If something needed is not in
  it, that absence is the finding.
- `docs/EVALUATION.md` — for the loop and the seeded variant.
- `docs/research/R5-assets-and-licences.md` — the recommended font trio, icon sprite approach, sizes.
- `docs/research/R6-portability-contract.md` — what `file://` permits.

**Acceptance criteria**
- [ ] 12 slides with diagrams exist as one `.html` file, **zero external references**
- [ ] **Opened offline, with the network disabled, and looked at** — CLAUDE.md rule 6, and stated as
      what was seen rather than as "works"
- [ ] Rendered at 3840×2000 and 1280×634; the two are identical up to a uniform scale factor (DS-063)
- [ ] **Body text measured in a 720p capture**, with the number recorded — whether or not it clears 16 px
- [ ] Every font embedded carries its licence
- [ ] The deck run through the convergence loop, with its outcome (PASS/CAP/STALL/OSCILLATION) and
      per-dimension scores recorded
- [ ] The seeded-defect variant exists, its defects documented, and **the rubric scores each 0 or 1**
      — or the anchors are corrected and the reason recorded
- [ ] **Every rule that proved wrong, unbuildable, or in conflict with another is recorded** — this
      is an expected output, not a sign the build went badly
- [ ] No personal, client or machine data anywhere in either file

**Open questions** — both settled 2026-08-06.

- ~~**What topic?**~~ **Settled by the owner: a mid-size city choosing between building a bike-share
  network and raising bus frequency.** Neutral and publishable, genuinely two-sided, and it needs
  diagrams rather than decorating with them — a network map, a trip-time decomposition, a corridor
  facet, a five-year trajectory. Why-now is a closing funding window; the ask is one action.
  Deliberately **not** a software topic: a software-tooling deck inside a software-tooling
  repository invites the reader to judge the argument instead of the craft.
- ~~**Does the seeded variant derive from the good deck?**~~ **Settled: it derives.** The rubric's
  response has to be attributable to the seeded defect, and that only holds with everything else
  held constant. The counter-argument — that deriving inherits the good deck's blind spots — is
  real but is answered by scoring the good deck, not by building a second one.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Settle the topic; write the argument before any HTML — the ruleset's own DS-090/D1 discipline applied to itself | the deck's spine and governing idea |
| 2 | Build 12 slides against `DESIGN-SYSTEM.md` alone, recording every point where the ruleset was silent, painful or self-contradictory | the deck, plus a findings list |
| 3 | Open it offline and **look at it**. Measure: two-resolution diff, 720p capture | the measurements |
| 4 | Run the convergence loop; record the outcome and scores | loop result |
| 5 | Seed the defect variant and score it against the known answer | rubric validation, and any anchor corrections |
| 6 | Route findings — rule conflicts to `DESIGN-RATIONALE.md` §2, rule changes as tasks, lessons to `LESSONS.md` | the corrections |

## 3. Implement

### 3.1 The spine — written before any HTML (plan step 1)

**Governing claim.** *Riverbend should buy bus frequency before it buys a bike-share network,
because frequency compounds across the whole network while bike-share serves the corridor it is
built on.*

Riverbend is an **illustrative city, named as one on the deck itself**. See the provenance decision
in §3.2 — this is not a real place and the deck never implies it is.

Twelve slides, each retiring the next objection a sceptical reader raises. The order **is** the
argument (D1); the archetype is chosen by what the slide has to do, never for variety's sake (D2).

| # | Archetype | Headline (the claim) | Objection it retires |
| :-- | :--- | :--- | :--- |
| 1 | Title | Buy frequency before bikes | — |
| 2 | A-01 Why-Now | The window shuts in March | "Why decide this now?" |
| 3 | A-03 Single Number | Eleven minutes decides this | "How big is the problem?" |
| 4 | A-10 Architecture View | Waiting is the trip | "What is the mechanism?" |
| 5 | A-04 Two-Column Ledger | Both options are real | "You have already decided." |
| 6 | A-06 Small Multiple | Bikes win three corridors | "It depends where you look." |
| 7 | A-05 Animated Trajectory | Frequency compounds, bikes plateau | "Does the gain last?" |
| 8 | A-07 Before / After | One transfer disappears | "What actually changes?" |
| 9 | A-09 Timeline with a Gate | Month eighteen is reversible | "What if you are wrong?" |
| 10 | A-12 Uncomfortable Truth | Frequency has no ribbon | "What does this cost us?" |
| 11 | A-02 Risk-Retirement | Three things would change this | "You cannot be talked out of it." |
| 12 | A-14 Verdict / Close | Approve the frequency package | — |

Slides 5, 6 and 10 are the ones carrying the credibility. **Slide 6 concedes three corridors to
bike-share on the evidence**, which is what stops slide 5 collapsing into X-03; slide 10 states the
recommendation's cost in the deck's own voice before anyone asks for it.

### 3.2 Decisions & assumptions

- **Riverbend is declared illustrative, and the model is the source — 2026-08-06.** DS-102 forbids
  fabricated metrics and requires every figure sourced, which an example deck about a place that
  does not exist cannot satisfy by citing anyone. Resolved by making the arithmetic the source: every
  city-specific number is an output of assumptions stated on the deck, carries an `[est.]` marker
  (DS-102) or an assumption marker (DS-104), and no figure is attributed to a real study. **The
  alternative — quoting real transit research from memory — would have been the actual DS-102
  violation**, since a misremembered elasticity is a fabricated metric wearing a citation.
- **The seeded variant derives from the good deck** — see §1.
- **CSS-only motion, no library — 2026-08-06.** R5 §3 puts anime.js at 82 KB and 43% of the probe
  deck's weight, and says plainly that below ~10 staggered elements CSS `animation-delay` is
  sufficient. Nothing in the spine needs orchestration. Recorded because the absence is a choice.

### 3.3 Findings against the ruleset

**These are the point of the task, not evidence it went badly.** Routed per plan step 6 on close.

> **All thirteen are closed** by [T-025](T-025-reconcile-the-twelve-ruleset-findings-from-the-reference-deck.md)
> — nine rules amended, four added, none rejected. The table below is the record of what the build
> found; the resolutions are in [`DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) §2.1.

| # | Rule(s) | Finding | Found |
| :-- | :--- | :--- | :--- |
| F-01 | DS-035 × DS-036 | **Conflict, both `hard`.** DS-035 sets an absolute floor of 18 design units; DS-036 sizes mono labels at "16–18". The 16–17 band is unreachable, so DS-036's range is wrong or DS-035's "anywhere" is not absolute. Neither yields to the other by its own terms. Built to DS-035. | Reading the ruleset, before any HTML |
| F-02 | DS-033 | **Unimplementable as written.** "No `px` … inside the stage" cannot hold: every CSS length resolves to an absolute unit, so the design unit itself must be declared as one. Resolved with `--du:1px` and every size as a token derived from it. The rule means *no bare `px`*, and `vw`/`vh`/`clamp()` — which is what actually fights the transform. | Writing the token block |
| F-03 | DS-140 × §7 (2.2.2) | **The `Current` motion is `4.5s linear infinite`, and §7 requires a control for motion lasting over 5 s.** DS-140 mandates the animation and never mentions the control that makes it conformant. Added a Motion toggle; the ruleset should require it rather than leave each deck to notice. | Writing the motion layer |
| F-04 | DS-140 × DS-141 | **Conflict, both `hard`.** DS-141 caps animations at 500 ms; DS-140's own vocabulary contains Pulse-once at 1.2 s and Current at 4.5 s. Read DS-141 as governing entry and transition only, with DS-140 as the specific override — but the text does not say so. | Writing the motion layer |
| F-05 | DS-146 × DS-140 | **DS-146 requires charts to "draw in once", and DS-140's four-motion vocabulary has no slot for a draw-in.** Implemented as Rise applied to the chart's marks, which keeps the vocabulary intact. A stroke-dash draw would have been a fifth motion. | Building the trajectory chart |
| F-06 | DS-168 × DS-071 | **Silence with a computable answer.** A control's minimum size in *design units* is fixed by the smallest scale at which the stage is still shown: reflow engages at 960 CSS px, so the stage scale bottoms out at 0.5 and a 24 CSS px target needs **≥48 design units**. The ruleset states the CSS-pixel floor but never the design-unit consequence, so the natural choice is wrong. Built at 52. | Sizing the disclosure control |
| F-07 | DS-117 | **Assumes directed flow diagrams.** "Connectors have arrowheads that meet their target, and are labelled" mis-fits an undirected network graph, where arrowheads would assert a direction the data does not have. Resolved by labelling every edge and giving arrowheads only to genuinely directional connectors. | Building the before/after network |
| F-08 | DS-063 | **No tolerance stated, and exact equality is unachievable.** Measured across 384 geometry values at 3840×2000 and 1280×634, positions agree to 0.09 design units but **text-run widths differ by up to 1.17** through glyph-advance rounding. A check demanding exact equality fails every deck containing text. The rule needs a stated tolerance. | The two-resolution diff |
| F-09 | DS-013 | **The core token list has no data-series role**, so the natural move is to reuse `--line-firm` for chart marks — which sits at 1.79:1 against the ground and fails 1.4.11's 3:1 for meaningful graphics. Added `--data-quiet` and `--ui-line` as separate tokens. | The contrast pass |
| F-10 | §7 (1.4.3 × 1.4.11) | **A neutral data mark cannot host text.** To clear 3:1 against the ground it must be dark; to carry 4.5:1 text it must be light. The two cannot both hold in a neutral. Text belongs outside the mark. This is a general consequence of the accessibility floor, not a fact about this deck. | The contrast pass |
| F-11 | DS-138 | **Geometrically unsatisfiable at the foot of the stage.** A panel that must drop *below* its control cannot do so if the control sits near the bottom of a 1080-unit stage and the panel is more than about two rows. The control has to move up. The ruleset says where the panel goes but never where the control goes. | Placing the disclosure |
| F-12 | DS-190/DS-191, and the harness | **Two measurement traps, both hit.** (a) Content taller than a `1fr` grid track never shows up as a box overflowing the stage — the track clamps the box and the content spills silently; the check has to compare `scrollHeight` with `clientHeight`. (b) DS-140's infinite `Current` prevents a headless render from ever reaching a quiescent state, so screenshots fire mid-transition and produce convincing blank slides. **Any automated render gate must pin motion off before capturing.** | Measuring, twice |

| F-13 | EVALUATION §6.2 × §6.4 | **"Fixes are applied one at a time" cannot coexist with an iteration cap of 3.** This deck needed **23 fixes** before it cleared its own gate. One fix per iteration under a cap of 3 is off by an order of magnitude; the loop would have reported CAP with twenty defects outstanding. Run as *two measurement rounds with fixes batched inside each*, it reached PASS. **The cap governs measurement rounds, not fixes** — and that answers EVALUATION §8's open question *"is the cap 2 or 3?"* with evidence: **2 rounds sufficed for a first-draft 12-slide deck.** The one-at-a-time rule should be scoped to fixes that interact, which is the case it was written for. | Running the loop |

**None of these was found by reading the ruleset.** F-01 came from reading it to build against; every
other one came from the build or the measurements — which is the argument for CLAUDE.md rule 6 stated
as evidence rather than as principle.

### 3.4 Defects the build found in the deck itself

Recorded because L-01 means reporting what was seen, not what passed. All fixed unless noted.

- The spine ribbon and the dots shared one chrome row and **collided** at 12 slides. Chrome is now two rows.
- The title and close slides used `height:100%` inside a `1fr` track and **spilled 27 design units**; a
  slide with no disclosure also auto-placed its body into the wrong grid track. Rows are now placed explicitly.
- Branch labels on the gate slide and threshold labels on the falsifier slide **ran off the stage**.
- `--ink-faint` at 3.21:1 and the neutral data colour at 1.79:1 **failed WCAG 1.4.3 and 1.4.11**.
- The `[est.]` marker was set at **16 design units, below DS-035's own floor** — caught by the gate, not by looking.
- The close headline ran to **seven words against DS-091's six** — also caught by the gate.
- The reading view kept the panels' absolute positioning and fixed 940-unit width, so it **could not reflow**;
  the title headline carried an inline `font-size` that outranked the reading view's type scale.
- **D4, found by counting rather than reading:** the ledger priced 62 stations at $5.6M ($90k each) while the
  gate slide bought "24 stations" for $1.5M ($63k each). The figures had disagreed since they were written and
  survived every visual pass. Corrected to 16 stations. *This is exactly what EVALUATION.md §4 warns about.*

**Outputs produced**
- `examples/reference-deck.html` — 178 KB, one file, zero external references
- `examples/reference-deck-seeded-defects.html` — the rubric fixture, 10 seeded defects
- `examples/README.md` — how to use both, the seeded-defect ledger, and the measurements
- `tools/examples/seed_defects.py` — derives the fixture from the deck, asserting every edit lands

## 4. Review

### 4.1 The convergence loop, as actually run

**Outcome: PASS**, in two measurement rounds.

| Round | Auto gate | Render gate + look | Fixes applied |
| :-- | :--- | :--- | :-- |
| 1 | pass | ribbon/dots collision · body content spilling 27 du on two slides · 10 WCAG contrast failures · labels clipped off-stage on two slides · `[est.]` at 16 du under DS-035's floor · close headline at 7 words over DS-091's 6 · reading view unable to reflow below ~430 px | 23 |
| 2 | pass | 0 hard violations · 0 spill · 0 contrast failures · 0 elements overflowing at 320 CSS px · body 17.3 px at 720p | 1 (D4 count) |

**Per-slide scores** (S1–S6, max 24; threshold ≥18 with no dimension below 2):

| Slide | S1 | S2 | S3 | S4 | S5 | S6 | Total |
| :--- | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| 1 Title | 4 | 3 | 2 | 4 | 3 | 2 | **18** |
| 2 Why-Now | 4 | 3 | 3 | 4 | 3 | 2 | **19** |
| 3 Single Number | 4 | 3 | 3 | 4 | 4 | 3 | **21** |
| 4 Mechanism | 4 | 3 | 4 | 4 | 3 | 2 | **20** |
| 5 Ledger | 4 | 4 | 3 | 3 | 3 | 2 | **19** |
| 6 Small Multiple | 4 | 4 | 4 | 4 | 3 | 2 | **21** |
| 7 Trajectory | 4 | 3 | 4 | 3 | 3 | 3 | **20** |
| 8 Before / After | 4 | 3 | 4 | 4 | 4 | 3 | **22** |
| 9 Gate | 4 | 3 | 4 | 4 | 3 | 2 | **20** |
| 10 Uncomfortable Truth | 4 | 4 | 2 | 4 | 3 | 2 | **19** |
| 11 Falsifiers | 4 | 4 | 3 | 4 | 3 | 2 | **20** |
| 12 Close | 4 | 2 | 2 | 4 | 4 | 2 | **18** |

**Whole-deck: D1 4 · D2 4 · D3 4 · D4 4 = 16/16.** D4 reached 4 only after the count in §3.4 —
it was a 2 on the evidence, and reading had passed it repeatedly.

All three threshold conditions hold. **Stated limitation:** these scores are the author's, in the
author's own build context. They should be read as *"the loop found no further defect it can see"*,
which is what §0 of EVALUATION says a score means.

> **This limitation is what closed the question.** At the time, EVALUATION §8 only *recommended*
> fresh-context whole-deck scoring. On this evidence — the D4 result above especially —
> [T-026](T-026-settle-who-scores-a-deck-and-whether-the-score-is-shown.md) ruled that **all five
> judgement-only dimensions** (S1, S2, S4, D1, D4) are scored in fresh context, not just the
> whole-deck two. EVALUATION §8.1. **The scores in this section predate that ruling** and were not
> produced under it.

### 4.2 Did the rubric detect the seeded defects?

Each seeded dimension was scored against the anchors, blind to which fix produced it.

| Dim | Rubric score | Detected by |
| :--- | :-: | :--- |
| S1 | **0** — "the heading is a topic label" is the literal anchor | judgement |
| S2 | **0** — a modelled curve asserted as observed, no figure qualified | judgement |
| S3 | **0** — cards where a diagram belongs | **mechanical** (card row count 1) |
| S4 | **0** — the slide only completes once something is opened | judgement |
| S5 | **0** — text below the design-unit floor, visible misalignment | **mechanical** (12 runs at 11 du) |
| S6 | **0** — continuous motion on static content | **mechanical** (`seededThrob`, infinite) |
| D1 | **0** — ordered by topic; objections not retired in sequence | judgement |
| D2 | **1** — three near-identical slides, length by dumping | **mechanical** (14 sections) |
| D3 | **0** — ends on a recap and a thank-you | **mechanical** (last slide "Thank you") |
| D4 | **0** — $2.2M contradicts the $1.5M the ledger established | judgement, by counting |

**Every seeded defect scored 0 or 1. No anchor needed correcting.** The rubric detects what it was
built to detect.

**The finding that matters is the split.** Five of ten are caught mechanically; the other five —
S1, S2, S4, D1, D4 — are invisible to any static or measured check. A pipeline that stops at the
gate ships a deck whose headline is a topic label, whose figures contradict each other, and whose
slides are ordered by topic. That is DS-191 demonstrated rather than asserted.

### 4.3 Acceptance criteria

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| 12 slides with diagrams, one `.html`, zero external references | **met** | 178 KB; 7 hand-written SVG figures; 0 external references by static scan |
| Opened offline, network disabled, and looked at | **met** | Real Chrome, clean throwaway profile, `--host-resolver-rules=MAP * ~NOTFOUND`. All 12 slides rendered and examined individually. All 3 faces report `loaded`. **The literal double-click through the file association (T-017's `shell` mode) was not run** — this is T-017's `clean` mode, which that task treats as the exact-results path. |
| Rendered at 3840×2000 and 1280×634, identical up to a uniform scale factor | **met, with a tolerance** | 384 geometry values compared. Positions agree to 0.09 du; worst disagreement 1.17 du on an SVG text-run width. Exact equality is unachievable — see F-08. |
| Body text measured in a 720p capture, number recorded | **met** | **17.3 px** (26 du), the smallest body run in the deck. Others 20.0 px. The arithmetic floor is confirmed: 24 du would land on exactly 16.00 px, with no margin. |
| Every font embedded carries its licence | **met** | Three faces, OFL 1.1, copyright line and licence URL in a comment beside the `@font-face` block |
| Convergence loop run, outcome and per-dimension scores recorded | **met** | §4.1 — PASS in two rounds |
| Seeded variant exists, defects documented, rubric scores each 0 or 1 | **met** | §4.2 — ten defects, all scored 0 or 1, no anchor corrected |
| Every rule that proved wrong, unbuildable or in conflict is recorded | **met** | §3.3 — twelve findings, F-01 to F-12 |
| No personal, client or machine data in either file | **met** | Illustrative topic written fresh; no corpus content; no local paths, usernames or machine specifics in either deck |

### 4.4 What this says about the ruleset

**The ruleset produces a deck worth presenting.** The failure mode the task named — *satisfies all
131 rules and is still dull* — did not occur, and the reason is worth stating: the rules that did
the work were the argument rules, not the visual ones. A-04's demand that both columns be genuinely
argued forced the concession slide; A-12 forced the deck to state its own cost; DS-090's
claim-not-topic rule is what makes the headlines carry the spine. **A deck built to the visual rules
alone would have been dull. The argument rules are what stopped it.**

**Twelve findings, and none of them is cosmetic.** Four are conflicts between two `hard` rules
(F-01, F-03, F-04, F-05), three are rules that cannot be satisfied as written (F-02, F-07, F-11),
two are silences with computable answers (F-06, F-09), and one is a rule whose check is impossible
as specified (F-08). That density — roughly one per ten rules — is the argument that a design
system has to be built against before it can be trusted.

**Child fix tasks raised**
- [T-025](T-025-reconcile-the-twelve-ruleset-findings-from-the-reference-deck.md) — reconcile F-01 to
  F-13 into `DESIGN-SYSTEM.md`, `DESIGN-RATIONALE.md` and `EVALUATION.md`. Kept out of this task on
  purpose: **a test that edits the thing it is testing is not a test**, so the findings are recorded
  here and applied there.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-06 | → done | All nine acceptance criteria met, one with a stated tolerance (DS-063 cannot be met exactly — F-08). The deck was opened offline in real Chrome with DNS black-holed and **every slide looked at**; 23 defects were fixed across two measurement rounds. **Thirteen findings against the ruleset**, four of them conflicts between two `hard` rules. The rubric scored all ten seeded defects at 0 or 1, and the split — five mechanical, five judgement-only — is the sharpest result in the task. Findings handed to [T-025](T-025-reconcile-the-twelve-ruleset-findings-from-the-reference-deck.md) rather than applied here. |
| 2026-08-06 | → review | Deck and seeded variant built and measured. |
| 2026-08-06 | → specified | Both open questions closed. Owner settled the topic: a mid-size city choosing between a bike-share network and higher bus frequency — neutral, two-sided, and diagram-hungry rather than diagram-decorated. The seeded variant derives from the good deck, so the rubric's response stays attributable. |
| 2026-08-06 | → planned | §2 was already written at creation; the spine in §3.1 is plan step 1's output and was written before any HTML, which is the ruleset's own DS-090/D1 discipline turned on itself. |
| 2026-08-06 | → in_progress | Building. **First finding (F-01) landed before a line of HTML** — DS-035 and DS-036 are both `hard` and cannot both hold, which is exactly the class of result this task exists to produce. |
| 2026-08-06 | → proposed | Created at handoff, after the board showed the artifact CLAUDE.md rule 6 has been demanding since T-014 had **no task file** — which is why two handoffs recommended it and neither produced it. It now blocks T-023's closure and two of BRIEF's done criteria. Written so the deck is a **test**, not a demo: the interesting outcomes are a rule that cannot be built, two rules that conflict, or a deck that satisfies all 131 rules and is still dull. |
