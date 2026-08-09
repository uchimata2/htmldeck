---
id: T-028
title: Retrofit the reference deck to the deliverable contract and thin its chrome
type: fix
status: done
phase: review
parent: T-027
blocked_by: []
related: [T-002, T-005, T-021, T-024, T-025, T-033]
work_package: WP2
owner: maintainer
created: 2026-08-06
updated: 2026-08-07
deliverables:
  - examples/reference-deck.html
  - examples/reference-deck-seeded-defects.html
  - tools/deck/deliverable_variants.py
---

# T-028 — Retrofit the reference deck to the deliverable contract and thin its chrome

> **This task gates the first published version of the plugin** — owner, 2026-08-06.
> [`BRIEF.md`](../docs/BRIEF.md) *Decisions taken* → **Release gate**, and its definition of done
> carries the criterion. Nothing else is blocked by it; publishing is.

## 1. Specify

**Outcome**
[`examples/reference-deck.html`](../examples/reference-deck.html) carries a **bottom line on every
slide** per DS-201 to DS-209, and its navigation obeys DS-216 and DS-217. It becomes an example of
the ruleset as it now stands, rather than of the ruleset as it stood before the owner reviewed it.

**Why this is separate from T-027**
T-027 wrote the rules and repaired the two defects that broke **hard** rules — the stage clipping
(DS-200) and 28 dead `fill=` attributes, one of which rendered at 2.17:1 (DS-214, DS-215). What is
left is not a defect list. **Every slide needs a sentence it does not currently have**, and adding a
bottom line to a slide that was composed without one changes its layout, its emphasis and often its
headline. That is a rewrite, and it should be looked at rather than patched.

**The deck's current state against the new rules**

| Rule | Now | Needed |
| :--- | :--- | :--- |
| DS-202 bottom line on every slide | **absent on all 12** | one factual sentence per slide, no reasoning |
| DS-203 second-most-prominent element | n/a | a defined slot in the slide template, not a per-slide invention |
| DS-209 one emphasis, and it is the deliverable | several slides emphasise two or three things | one |
| DS-216 one encoding of position | **three** — spine ribbon, 12 dots, progress bar | one primary, plus at most one encoding a *different* fact |
| DS-217 chrome budget | **23 labelled items, 96 design units** | ~12 items; per-slide dots stop scaling near ten slides |

**The owner's words on the chrome, which are the acceptance test:** *"The bottom navigation area with
the subtitles above it are extremely noisy with that many dots."*

**Scope**
- In: a bottom line per slide, written before the layout changes — the outline contract (DS-210,
  DS-211) applied to a deck that already exists.
- In: a slot for it in the shared slide template, so it is one component reused, not twelve inventions.
- In: thinning the chrome to one position encoding within the DS-217 budget, keeping click-to-jump.
- In: re-running the gate and **looking at every slide** afterwards.
- Out: changing the deck's topic, argument or figures. The spine survived review; only the
  presentation of each slide's point changes.
- Out: any further rule change. If a rule proves unbuildable here, it is a finding for T-025, not an
  edit to `DESIGN-SYSTEM.md`.

**Inputs**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §3.4, §3.5, and DS-216/DS-217
- [`T-027`](T-027-specify-the-slide-deliverable-and-the-outline-contract.md) — the rules and why they exist
- [`T-024`](T-024-build-the-reference-deck-and-validate-the-ruleset.md) §3.1 — the deck's spine, which stands

**Acceptance criteria**
- [ ] Every slide has a bottom line: one sentence, factual, no reasoning, not the headline restated
- [ ] The bottom line is the second-most-prominent text on the slide, verified by rendered measurement
- [ ] No slide emphasises more than one thing
- [ ] Exactly one primary encoding of position; chrome within DS-217's budget
- [ ] `python tools/deck/audit.py` reports zero mechanical failures
- [ ] Every slide opened offline and looked at, and the result stated as what was seen

**Open questions**
- ~~**Does the bottom line replace the standfirst, or sit below the body?**~~ **Answered
  2026-08-07, against rendered slides: neither wholly.** It sits in its own slot at the foot of the
  body, and the standfirst stays but is demoted. Two rendered facts decided it. **Slide 5 already
  has the slot** — `.ledger-foot`'s note, accent-weighted at the foot of the body, is a bottom line
  in everything but name, and it is the only slide whose point is legible without the presenter.
  **Slide 4's standfirst is already the deliverable** ("Standing still takes 15 of the 34 minutes"),
  which is why the answer cannot be "keep the standfirst as it is": on the slides where it does the
  job, it does it in the wrong place, and on the rest it sets the scene. Demoting it and adding the
  slot separates the two jobs the one element was doing.

**Verified against the deck before planning, 2026-08-07** — the §1 table above was written
2026-08-06 and the deck has been committed to twice since (`8cafa46`, `b3cca1f`). Re-checked
rather than assumed, because the last two tasks resumed from a handoff both had stale
specifications:

- **DS-202 — holds.** No bottom-line element exists in the file, under any name.
- **DS-216 — holds.** All three encodings are live in the markup and visible together in every
  capture: `.ribbon` (7 stages), `.dots` (12), `.progress`.
- **DS-217 — holds.** 23 labelled or interactive items: 7 ribbon stages, 12 dots, prev, next,
  `Read`, `Motion on`.
- **T-021 and T-032 changed the deck's behaviour, not its chrome or its slide bodies**, which is
  why the table survived them.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Write the twelve bottom lines first, as an outline, with no HTML open | the outline |
| 2 | Add one bottom-line slot to the slide template and place it | the component |
| 3 | Reduce each slide to a single emphasis, the deliverable | the slides |
| 4 | Thin the chrome to one position encoding inside the budget | the navigation |
| 5 | Gate, measure, and look at all twelve offline | the verdicts |

## 3. Implement

### 3.1 The outline — twelve bottom lines, written before the HTML was opened

DS-211: *archetype · title · bottom line*, and the sentence here is the sentence that ships.
Written from the slide content, with the file closed, so the layout could not talk the sentence
into being easier to place.

| # | Archetype | Title | Bottom line |
| :-- | :--- | :--- | :--- |
| 1 | Title / claim | Buy frequency before bikes | Spend the $5.6M grant on bus frequency, and hold $1.5M for bike-share until month 18. |
| 2 | Timeline | The window shuts in March | The grant closes on 31 March 2027, and the 12 March budget vote is the only meeting that can commit it. |
| 3 | Single number | Eleven minutes decides this | A Riverbend rider waits 11 minutes on average, and both proposals are ways of spending money on that number. |
| 4 | Mechanism | Waiting is the trip | Eleven of the 34 minutes are the wait, and the wait is half the headway. |
| 5 | Two-column ledger | Both options are real | Operating cost decides it: the grant pays for no staff in either column. |
| 6 | Small multiple | Bikes win three corridors | The three corridors bike-share wins carry 12,200 weekday trips; the three frequency wins carry 36,000. |
| 7 | Projection | Frequency compounds, bikes plateau | Bike-share stops growing when its docks fill in 2029, and frequency is still adding trips in 2031. |
| 8 | Network diagram | One transfer disappears | A timed connection at Centre removes one change for North Line and Market Cross riders. |
| 9 | Decision gate | Month eighteen stays reversible | Nothing before month 18 is irreversible, and the $1.5M reserve buys 16 Old Quarter stations if the gate fails. |
| 10 | Cost / concession | Frequency has no ribbon | Three corridors wait until month 18, and the general fund carries $6.8M every year after. |
| 11 | Tripwires | Three things would change this | Three thresholds are fixed before approval, and each is measured on a stated date by someone outside this team. |
| 12 | The ask | Approve the frequency package | On 12 March: $4.1M of the grant, $6.8M a year from the general fund, $1.5M held for the gate. |

**Two of the twelve were already written and in the wrong place**, which is the finding this step
produced. Slide 5's is `.ledger-note`, and slide 12's is `.close-sub` — both already say the right
sentence. Slide 4's standfirst says its bottom line. The deck was not silent on its deliverables;
it stated three of them subordinately and the other nine not at all.

### 3.2 What the work found

**The gate was calling chrome that a design rule required deleting.** Removing the twelve dots
broke `render.py` and `audit.py` at once: both drove the deck by clicking `#dots.children[i]`.
`audit.py` then printed **stage 3 render gate: NO RESULT** and `render.py measure` reported
`no result` for slides 1–11 while happily printing a DS-063 verdict computed from **16 values, all
from slide 1** — a tolerance line that read as a pass. Both now walk with the next/previous
controls, which are controls rather than position encodings, and `deliverable_variants.py` treats a
deck that will not render as *not caught* rather than counting a crash as a pass.

**Five rules labelled `auto` and `render` had no implementation.** DS-202, DS-203, DS-205, DS-216
and DS-217 were written by T-027 as machine-checkable and nothing checked them, which is how a deck
with a bottom line on **none** of its twelve slides and three simultaneous position encodings
passed a 43-check gate. They are gated now, and `tools/deck/deliverable_variants.py` breaks each on
purpose. This is L-36 in a second place: the first was a tolerance covering no values, this is five
rules covering no deck.

**Two of the new checks were wrong when first written, and the variants are what showed it.**
DS-217's item count scored every ribbon stage twice — once as the `li`, once as the `button` inside
it — and reported **24 items for an 11-item chrome**. The chrome-height check then failed the
redesign at 125 du against a 90 du budget, correctly: the two-row chrome cost 48 du to solve a
collision that only existed because of the dots. One row fixed it. Neither error would have
surfaced from a suite that only ever ran against a passing deck.

**Three seeded defects were anchored to markup this task deleted.** `seed_defects.py` asserted its
edits matched and stopped, rather than writing a fixture that silently no longer carried S4, S6 or
D3 (**L-04**, and the reason that assertion exists). All three were retargeted. Worth recording:
S4's retargeted defect **passes** DS-202 and DS-205 — a bottom line is present and is not behind a
disclosure, and only a reader can see that *"Two options, six rows."* decides nothing. That is S4
being one of the five dimensions the gate cannot judge, working as documented.

**The slide-2 label collision is on screen, not only in print.** Confirmed in a 1920×1080 capture
before anything was changed; the markers sit 140 units apart in a 1728-unit viewBox with both
labels `text-anchor="middle"`, so it was geometric and scale-independent. Fixed by anchoring the
pair away from each other.

**Decisions & assumptions**
- **The bottom line is its own slot at the foot of the body; the standfirst stays and is demoted**
  from `--fs-lead` (30 du) to `--fs-body` (26 du) — the two elements were doing two jobs under one
  name, and DS-203 reserves second place for the deliverable — 2026-08-07
- **One component, twelve uses, including the closing slide.** Slide 12's ask moved out of
  `.close-sub` into the same `.bottom-line`, centred by a modifier. The task asked for a slot in the
  shared template rather than twelve inventions, and an exception on the one slide that most needs
  the deliverable to look like every other deliverable would have been the wrong place to start —
  2026-08-07
- **The accent is carried by the rule above the sentence, not by the sentence.** Accent-coloured
  prose is the weaker pair against paper; ink at 40 du with an accent rule above it is unambiguous
  in rank and never near the contrast floor (DS-215) — 2026-08-07
- **Kept two encodings of position, not one.** DS-216 permits a second when it encodes a different
  fact; the ribbon says which stage, the `05 / 12` counter says how far through, and the counter
  also satisfies DS-133. The progress bar was the third and was removed — 2026-08-07
- **Slide 10's pull-quote aside was deleted, not demoted.** It was the loudest element on the slide
  (DS-209) and it was a metaphor (DS-207). The honest framing survives in the headline, where wit
  is allowed — 2026-08-07
- **Three slides' supporting copy was tightened to pay for the new slot.** Slide 10's three
  paragraphs went from two rendered lines each to one, and slide 5's ledger padding halved. Both
  slides overflowed their body track when the bottom line was added; the alternative was a smaller
  bottom line, which would have broken the rule the task exists to satisfy — 2026-08-07
- **No rule was changed.** Where the deck and a rule disagreed, the deck moved. Scope said any
  unbuildable rule is a finding for T-025, and none proved unbuildable — 2026-08-07

**Outputs produced**
- `examples/reference-deck.html` — twelve bottom lines, one-row chrome, slide-2 collision fixed
- `examples/reference-deck-seeded-defects.html` — regenerated against the rewritten deck
- `tools/deck/deliverable_variants.py` — new; breaks DS-202/203/205/216/217 on purpose
- `tools/deck/audit.py` — seven new checks, `render_data` / `render_verdicts` split out so a
  variant suite can call the same code that gates the deck
- `tools/deck/render.py` — drives with next/previous; probes the bottom line
- `tools/examples/seed_defects.py` — S4, S6 and D3 retargeted
- `examples/README.md` — chrome, bottom line and measurements brought current

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every slide has a bottom line: one sentence, factual, no reasoning, not the headline restated | **met** | 12 of 12. Gated by two DS-202 checks — presence, and a sentence count that ignores decimal points so `$4.1M` is not read as a sentence end. *Not the headline restated* is judgement, and it is where slide 6 was corrected: its first draft opened *"Bike-share wins three corridors"*, which is the headline. It now leads with the magnitude |
| The bottom line is the second-most-prominent text on the slide, verified by rendered measurement | **met** | DS-203, measured not asserted: every prose run of four words or more on the current slide, computed font size, SVG runs corrected through `getScreenCTM`. 0 runs outrank the bottom line's 40 du. The word-count floor is what keeps a stat figure (`11`) and a chart label (`Bus`) out of a comparison about sentences |
| No slide emphasises more than one thing | **met**, by judgement | Not mechanically decidable, so recorded as what was changed: slide 10's boxed pull-quote deleted, slide 6's two chart captions reduced to one that no longer states the comparison, and the standfirsts on slides 4, 6, 7, 9 and 10 rewritten from claim to setup. **Slides 7 and 9 were caught only by looking** — both standfirsts still restated their own bottom line after the gate was green |
| Exactly one primary encoding of position; chrome within DS-217's budget | **met** | 2 encodings, and DS-216 permits the second only because they answer different questions: ribbon = stage, `05 / 12` = position in the deck. Progress bar removed. **11 labelled or interactive items** (was 23) and **52 du tall** (was 96, budget ~90). Click-to-jump kept, moved from twelve dots to seven stage buttons |
| `python tools/deck/audit.py` reports zero mechanical failures | **met** | 0 of 50 checks failing, including the seven added here. `contract_variants.py` 7/7, `deliverable_variants.py` 7/7, `task.py check --closing` 466 pointers 0 broken, `check_scaffold.py` OK |
| Every slide opened offline and looked at, and the result stated as what was seen | **met** | All twelve rendered in real Chrome from `file://` with DNS black-holed, and looked at. Four defects were found this way and by no check: the slide-2 label collision, `Motion on` wrapping to two lines inside its button, the ribbon squeezed until its connector dashes collapsed, and the slides 7 and 9 standfirsts above. The gate was reporting zero failures throughout |

**What this task did not do**

- **No rule changed.** Scope said an unbuildable rule is a finding for T-025; none proved unbuildable.
- **The deck's spine, topic and figures are untouched**, as scope required. Three supporting
  paragraphs on slide 10 were shortened and five standfirsts rewritten — presentation of each
  slide's point, which scope put in.
- **DS-201, DS-204, DS-206, DS-207, DS-208 are still `judge`-only** and are not gated. They are
  judgement rules and adding a machine check for them would be the L-36 failure in a new place.

**Child fix tasks raised**
- none. One **finding** was raised as a sibling rather than a child:
  [T-033](T-033-reconcile-ds-131-with-the-chrome-budget.md) — obeying DS-216 and DS-217 meant
  deleting the twelve dots that **DS-131 lists as required navigation**, so the reference deck now
  departs from a rule in the ruleset it exists to demonstrate. All three are `default`, so the
  departure is legitimate; the ruleset contradicting itself is not. Not fixed here because scope
  put rule changes out, and not appended to T-025 — T-028's stated route for such findings —
  because T-025 is `done`.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-07 | → done | All six acceptance criteria met; see §4. **The release gate is clear** — `BRIEF.md`'s seventh criterion is satisfied and nothing now blocks [T-008](T-008-package-document-and-publish.md) but T-008 itself. The finding worth carrying out of this task is not the deck: **five rules written as machine-checkable went a whole task with nothing checking them**, and the two checks that finally did were themselves wrong until a variant broke them. L-36 has now happened twice, in different parts of the system, which makes it a property of how rules get written here rather than one bad afternoon. |
| 2026-08-07 | → in_progress | Specify closed and the plan approach settled. **The slide-2 label collision is not print-only — it is on screen too**, which the entry below correctly refused to assume. In the 1920x1080 capture *"Budget vote"* and *"Grant closes"* touch with no gap between them, and the dates below read as a single run, *"12 Mar 20271 Mar 2027"*. The markers sit at x=820 and x=960 in a 1728-unit viewBox, both `text-anchor="middle"`, so the labels overlap at any scale — the collision is in the geometry, not in the rendering. Fixed here rather than raised as a child task: it is one of the twelve slides being rewritten anyway, and DS-215's lesson is that a defect you can see is cheaper than the one you argue about. |
| 2026-08-07 | (no change) | **A label collision on slide 2's timeline, found while looking at [T-018](T-018-measure-the-printable-mode-what-printing-from-fi.md)'s printed output** and recorded here because it is a deck defect, not a print defect. Two markers sit close enough that their labels overlap and read as one word — *"Budget vote"* against *"Grant closes"*, and *"12 Mar 2027"* against *"31 Mar 2027"*. **Whether it also occurs on screen was not checked**, so treat that as the first question rather than an assumption; the print rendering uses the same 1920×1080 stage geometry, which makes it likely. Noted rather than fixed: T-018 was measuring the printable mode, and quietly editing the deck it was measuring would have invalidated its own run. |
| 2026-08-07 | (no change) | [R7](../docs/research/R7-printable-mode.md) ruled the printable mode is the **paginated stage**, so this deck's committed `@media print` block — which prints the reading view — is now the rejected rendering. Adoption is [T-032](T-032-adopt-the-paginated-print-mode-in-the-reference-deck.md), split out rather than folded in here because it carries an owner decision about tier two with a page-count consequence. |
| 2026-08-06 | (no change) | **Made a release gate by the owner: this lands before the first published version.** Recorded in `BRIEF.md` *Decisions taken* and added to its definition of done as a seventh criterion. The reasoning is that the example deck is the plugin's argument for itself, so shipping one that fails the deliverable contract argues against the ruleset it is meant to demonstrate. No `blocked_by` edge exists for it — nothing else in the backlog is gated, only publishing. |
| 2026-08-06 | (no change) | Confirmed still open by [T-025](T-025-reconcile-the-thirteen-ruleset-findings-from-the-reference-deck.md): the three simultaneous position encodings (DS-216/DS-217) are visible in every capture taken during its re-check, and no rule change there touched them. |
| 2026-08-06 | → proposed | Raised by [T-027](T-027-specify-the-slide-deliverable-and-the-outline-contract.md). The owner's review produced two hard-rule defects, fixed there, and one change that is a rewrite rather than a fix: **no slide in the deck states its deliverable**, because the rule requiring it did not exist when the deck was built. Chrome density comes with it — three encodings of position, which the owner called *"extremely noisy"*. |
