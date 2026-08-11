---
id: T-021
title: Build the reflow view and enforce the resolution contract
type: deliverable
status: done
phase: review
parent: null
blocked_by: []
related: [T-002, T-005, T-007, T-014, T-016, T-018]
work_package: WP2
shipped_in: 0.1.0
owner: maintainer
created: 2026-08-06
updated: 2026-08-12
deliverables:
  - tools/deck/contract.py
  - tools/deck/contract_variants.py
---

# T-021 — Build the reflow view and enforce the resolution contract

## 1. Specify

> **Rewritten 2026-08-07**, in the specify phase, because the specification had gone stale in three
> ways at once: it referenced a section numbering that no longer exists, it carried an open question
> [R7](../docs/research/R7-printable-mode.md) had already answered, and it read as though nothing
> were built when a working reflow view had been in the repository for a day. The original text is
> in git; what changed and why is the log's top row. **Nothing was reworded to match an output** —
> the nine original acceptance criteria are carried through unedited, and the four added below are
> about the enforcement half, which has not been started.

**Outcome**
The **resolution contract** and the **reflow view** — [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md)
§2.4 (DS-060–DS-065, DS-200) and §2.5 (DS-070–DS-076) — are **enforced by a check that has been seen
to fail**, and the half of §2.5 that currently exists only as one hand-built instance is **verified
rather than assumed**.

**The view is not the deliverable; the enforcement is.** A conforming reflow view already exists in
[`examples/reference-deck.html`](../examples/reference-deck.html), built by
[T-024](T-024-build-the-reference-deck-and-validate-the-ruleset.md) because the deck failed its own
hard rules without one, and [`tools/deck/audit.py`](../tools/deck/audit.py) already checks four of
the seven §2.5 rules (DS-070, DS-073, DS-075, DS-076). That is **L-32** — building one artifact by
hand does the first pass of every task downstream of it — and it makes this task extraction and
enforcement, not authorship.

**Why this one**
Two failures the owner has actually hit, and neither is hypothetical:

1. **A deck built for small screens breaks when opened on a 4K display.** Breakpoints land in a
   bucket nobody designed, `max-width` containers leave dead gutters, absolutely-positioned
   decoration drifts.
2. **A deck presented from a high-resolution monitor arrives illegible**, because Zoom, Meet and
   Discord re-encode the shared screen at 1080p or 720p and the text goes down with the frame.

§2.4 shows the second has an arithmetic answer: **under a uniformly scaled stage the presenter's
viewport cancels out**, so stream legibility depends only on the design size and the call's
resolution. That is why the stage is `hard` and why no responsive presentation layout is acceptable.
**This task is the other half** — the floor is met by a view the presenter never sees.

And a third reason the rewrite makes explicit: **one deck complying by hand is not a contract.**
Six of the twelve rules across §2.4 and §2.5 have no executable check, so the next deck can regress
every one of them silently. DS-063 in particular is the cheapest test in the ruleset and catches the
whole "it broke on my monitor" class.

**Scope**

- In: the **resolution-contract and reflow checks**, as executable gates in `tools/deck/audit.py`'s
  stage 2 — **DS-063 first**: render at 3840×2000 and at 1280×634 and diff up to a uniform scale
  factor, against the tolerance §2.4 already states (non-text geometry ≤ 0.25 design units, text
  runs ≤ 2 design units).
- In: **DS-071's boundary, measured** — auto-engage below 960 CSS px and *not* at 1280.
- In: **DS-072 demonstrated** — the switch cannot fire in fullscreen or while a presentation control
  is active.
- In: **DS-064 measured** — body text ≥ 16 px in a 720p capture, or the design-unit floor revised
  with the measurement that showed why.
- In: confirming the conformance wording the deck ships with — *AA via a conforming alternate
  version reachable by a persistent control* (§7, DS-070), never a bare "this deck is AA".
- In: settling the two open questions still open below, against a real deck rather than in the
  abstract.
- Out: **authoring the reflow view.** It exists and it measures clean on three criteria; this task
  extracts the rules from it and enforces them. Where the instance and the ruleset disagree, the
  ruleset is what a check enforces and the instance is what gets fixed.
- Out: the stage itself. That is T-002's, built to §2.4.
- Out: **printing — settled, no longer an open question.**
  [R7 §4](../docs/research/R7-printable-mode.md) measured the reading view as a print target and
  **rejected it**: it is a document made of slide-sized chunks with atomic figures, so it strands
  headings and leaves interior pages up to 29% empty after three rounds of fixes. The printable mode
  is the paginated stage. The two renderings share nothing, and reshaping the reflow view to
  paginate better is exactly what CLAUDE.md rule 5 forbids.
- Out: mobile as a first-class target. The Portability decision keeps mobile secondary; auto-engage
  is what a phone gets, and that is deliberate.

**Inputs**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §2.4 and §2.5 — the twelve rules this task
  enforces; §7 — the conformance claim; §8 — DS-190, DS-191, DS-220 and DS-221, which are claims
  about what a check may assert and bind the enforcement work directly.
- [`docs/research/R6-portability-contract.md`](../docs/research/R6-portability-contract.md) — what
  `file://` permits, including view transitions.
- [`docs/research/R7-printable-mode.md`](../docs/research/R7-printable-mode.md) §4 — the measurement
  that closed the shared-rendering question; §3 — that **a deck adapting to viewport width will
  adapt during printing**, which is the auto-engage threshold behaving correctly and looking like a
  defect.
- [`examples/reference-deck.html`](../examples/reference-deck.html) and
  [`examples/reference-deck-seeded-defects.html`](../examples/reference-deck-seeded-defects.html) —
  the conforming instance and the fixture a check must be seen to fail on.
- [`tools/deck/audit.py`](../tools/deck/audit.py) and [`tools/deck/render.py`](../tools/deck/render.py) —
  the existing gate and the real-Chrome-offline instrument this extends. `render.py` already carries
  the two measurements that make DS-063 and DS-064 tractable: `--window-size` is the outer window,
  not the viewport, so 720p is not 720p until the shortfall is calibrated; and an infinite animation
  stops a headless render ever settling.
- [`docs/LESSONS.md`](../docs/LESSONS.md) — **L-35** above all: this is a measurement task, and an
  instrument scoped out for being a different code path will eventually prove it. Also **L-32**
  (why this is extraction) and **L-01** (looking is not optional).
- [`docs/BRIEF.md`](../docs/BRIEF.md) open question 7 — **already answered** by the owner
  2026-08-06; this task builds what that answer promised, it does not close the question.

**Acceptance criteria**

*The nine written 2026-08-06, unedited. Three of them already have evidence on the reference deck —
that is a verdict for §4 to record, not a reason to drop a criterion.*

- [ ] The reflow view renders every slide's tier-one **and tier-two** content, verified by counting
      elements against the stage rendering — not by reading
- [ ] No two-dimensional scrolling at 320 CSS px equivalent
- [ ] The switch is keyboard-operable, visible without hover, and preserves position both ways
- [ ] The switch **cannot** fire in fullscreen, demonstrated
- [ ] Auto-engage triggers below 960 CSS px and **not** at 1280 CSS px — the 150%-scaled FullHD
      laptop stays on the stage
- [ ] **DS-063 demonstrated** *(the rule the original text called "condition 17")*: the same deck
      rendered at 3840×2000 and 1280×634 is identical up to a uniform scale factor, within §2.4's
      stated tolerance
- [ ] **A real 12-slide deck opened offline on a large display and on a 1080p display**, and looked
      at in both — CLAUDE.md rule 6, and the whole point of this task
- [ ] Body text measured at ≥ 16 px in a 720p capture of the presented deck, or the design-unit floor
      revised with the measurement that showed why
- [ ] The shipped conformance wording states the alternate-version route explicitly

*Four added 2026-08-07, for the enforcement half. None of this work has been started, so these are
still criteria written before the work.*

- [ ] **Every `hard` rule in §2.4 and §2.5 is either an executable check or is named in §3 with the
      reason it cannot be one.** A rule silently left unenforced is the failure mode this task
      exists to end; a rule stated as unenforceable is an honest close (**L-05**)
- [ ] **Each new check has been seen to fail**, on the seeded-defect fixture or on a variant built
      for it. A check that has only ever passed is not evidence that it checks anything
- [ ] Each check reports the **rule ID and the measured value**, not a boolean — DS-191 is why: a
      measurement confirms geometry you suspect, so the number has to be readable
- [ ] The checks run offline from `file://` in real Chrome, and the run is reproducible from a clean
      clone by one documented command

**Open questions**

*Answered, kept for the record:*

- ~~**Do the reflow view and the print stylesheet share one document rendering?**~~ **Answered `no`,
  measured** — [R7 §4](../docs/research/R7-printable-mode.md). Do not reopen it; the scope line
  above carries the consequence.

- ~~**Does the reflow view need the interaction layer at all, or does it inline tier two?**~~
  **Answered 2026-08-07 by the owner: inline it.** The reference deck had already taken that
  position unratified — it hides `.disc-btn` in the reading view and renders every panel open — and
  [R7 §5](../docs/research/R7-printable-mode.md) decided the same question the same way for print.
  **DS-073 amended** to state it: panels open in normal flow, the control not rendered at all. The
  two-tier reading rhythm is the stage's, and §5.3 stays written for the stage. Consequence for
  [T-016](T-016-the-interaction-and-motion-layer.md): the disclosure component has one context, not
  two.
- ~~**Is 960 CSS px the right threshold, or should it key off the computed scale factor instead?**~~
  **Answered 2026-08-07 by the owner: key off the scale factor.** The arithmetic said width is a
  lossy proxy and said by how much — the stage scales by `k = min(vw/1920, vh/1080)`, so 960 px of
  width is the threshold *only when height does not bind*; 1280 × 400 gives `k = 0.37` and body text
  at 8.9 px while a width test keeps the deck on the stage. **DS-071 amended** to `k < 0.5`, with
  960 CSS px kept as the number to quote for a 16:9-or-taller viewport. Two consequences: the
  reference deck's width-based auto-engage now diverges from the ruleset and is plan step 2's
  reconciliation, and **DS-168's ≥ 48-design-unit target floor stops resting on an assumption about
  which dimension binds** — the caveat under F-06 in
  [`DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) is closed by this.

*Still open:* none. Both remaining questions were settled by the owner on 2026-08-07, and the two
rule amendments they produced are in the ruleset rather than only here.

## 2. Plan

**What a baseline run showed, and it changes the plan.** `python tools/deck/audit.py
examples/reference-deck.html` reports **0 mechanical failures over 32 checks** — and **not one of
them is a §2.4 rule** beyond the static DS-061. Meanwhile
[`tools/deck/render.py`](../tools/deck/render.py) already renders at 3840×2000, 1280×634 and 720p
and already computes DS-063's geometry diff and DS-064's smallest body run. **So DS-063 and DS-064
are measured but not gated**: the numbers print, nothing fails, and a regression is a line of output
nobody is obliged to read. That is a third instance of **L-32**, and it makes step 3 mostly wiring
rather than authorship.

**Order, and why this order.** The DS-071 amendment goes first, because it is the one step whose
check is *expected to fail before it* — the deck's auto-engage is width-based and the rule is now
scale-based. Writing the check first and watching it fail on a real divergence is worth more than
any seeded defect, and it is the acceptance criterion *each new check has been seen to fail* earned
honestly rather than staged.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | **Write the DS-071 check first and watch it fail.** Three viewports: `k < 0.5` must engage, `k > 0.5` must not, and **1280 × 400** — short and wide, `k = 0.37` — must engage, which is the case a width test cannot see | a failing check, recorded in §3 |
| 2 | **Reconcile the instance to the rule.** Auto-engage keys off `min(vw/1920, vh/1080) < 0.5`; the check goes green on the same three viewports | `examples/reference-deck.html` |
| 3 | **Gate what is already measured.** Lift DS-063's tolerance test and DS-064's 720p floor out of `render.py`'s report into a shared function, and give `audit.py` a stage that fails on them | `tools/deck/render.py`, `tools/deck/audit.py` |
| 4 | **Close the rest of §2.4 and §2.5.** DS-060 (fixed design space, uniform scale), DS-062 (letterbox, never reflow), DS-065 (no absolute-pixel decoration), DS-200 (the scaled stage is centred — measured against the viewport at several widths, as the rule itself instructs), DS-072 (no engage in fullscreen), DS-074 (one column, `rem`, normal flow). **Any rule that cannot honestly be automated is named in §3 with the reason** rather than quietly dropped | checks, and a stated list of what is not checkable |
| 5 | **Verify on the real 12-slide deck**: `measure` at all three resolutions, the seeded-defect fixture for the failure direction, and the deck **opened offline and looked at** on a large display and at 1080p (**L-01**, CLAUDE.md rule 6) | measurements in §4 |

## 3. Implement

**Decisions & assumptions**

- **The two open questions, settled by the owner 2026-08-07**, each producing a rule amendment
  rather than a decision row: **DS-073** — the reflow view inlines tier two, panels open in normal
  flow, control not rendered; **DS-071** — auto-engage keys off `min(vw/1920, vh/1080) < 0.5`, with
  960 CSS px kept as the quotable equivalent for a 16:9-or-taller viewport. §1's open-questions
  block carries the reasoning.
- **The DS-071 check was written before the fix, and failed.** 1280 × 400, k = 0.370, the deck
  stayed on the stage because its auto-engage was a `max-width: 959px` media query. That failure is
  the honest version of the *seen to fail* criterion — a real divergence, not a staged one. The
  media query is also why it listened on the wrong event: a media query never fires on a height
  change, so the handler now listens for `resize` and `orientationchange`.
- **DS-063's tolerance is split by element kind, not by axis** — and this was a correction, not a
  design choice. Implementing the rule as written failed the reference deck on 27 of 336 values
  while its layout was provably identical: glyph rounding moves a text run's position and height,
  not only its width. Amended in the ruleset with the measurement behind it.
- **DS-063's non-text tolerance had never been measured.** The probe carried nine keys and all nine
  are text runs, so the 0.25 du figure had a citation and zero coverage. Four non-text boxes added
  to the probe; 116 values, **worst disagreement 0.000 du**. Generalised as **L-36** and it is the
  finding of this task, not the checks.
- **DS-065 was reworded rather than checked.** Inside the stage a design unit *is* one CSS pixel
  before the transform, so *"absolute pixels rather than design units"* could not be false. The
  rule now names units that do not ride the transform, which DS-033 decides statically.
- **DS-072 is verified against doubles and says so.** A faked `fullscreenElement` and a faked
  viewport height, never a real fullscreen — headless has no gesture to request one with. The first
  version of this check passed a deck with the guard deleted, because it asserted "nothing changed"
  while the deck was already in the right state; it now forces a state where the guard has to act.
- **Assumption, stated:** everything mechanical was measured in headless Chrome 151 from `file://`
  with DNS black-holed. Per **L-35** that is a different code path from a double-clicked file, so
  the rendered captures were **looked at** rather than trusted from the numbers, and the checks
  report values rather than verdicts so a wrong one is visible.

**Outputs produced**
- [`tools/deck/contract.py`](../tools/deck/contract.py) — the §2.4 / §2.5 gate: a four-viewport
  sweep, the two-resolution comparison, and the list of what it does *not* check with the reason.
- [`tools/deck/contract_variants.py`](../tools/deck/contract_variants.py) — seven decks that each
  break one rule, and the requirement that the gate notice.
- [`tools/deck/audit.py`](../tools/deck/audit.py) — stage 4 added; 43 checks, from 33.
- [`tools/deck/render.py`](../tools/deck/render.py) — four non-text probes added; thresholds moved
  out to `contract.py` so the report and the gate cannot disagree.
- [`examples/reference-deck.html`](../examples/reference-deck.html) — auto-engage reconciled to
  DS-071, and [`examples/reference-deck-seeded-defects.html`](../examples/reference-deck-seeded-defects.html)
  regenerated from it.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-063, DS-065, DS-071, DS-073 amended.
- [`docs/DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) — F-06's caveat closed, F-08 corrected,
  and a new section on what the first tolerance measurement did not measure.
- [`docs/LESSONS.md`](../docs/LESSONS.md) — **L-36**.
- [`examples/README.md`](../examples/README.md) — the corrected measurements and the conformance
  claim written out in full.

## 4. Review

*Reproduce with `python tools/deck/audit.py examples/reference-deck.html` (43 checks, stage 4 is
this task's) and `python tools/deck/contract_variants.py` (the failure direction).*

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Reflow renders tier-one **and tier-two**, counted not read | **met** | `audit.py` DS-073: 10/10 panels open in the reading view, and no section carrying less text than its slide, compared character by character across all 12 |
| No two-dimensional scrolling at 320 CSS px | **met** | DS-075: `scrollWidth` **320**, zero elements over 321 px |
| Switch keyboard-operable, visible without hover, position preserved both ways | **met** | DS-076 returns on *Frequency compounds, bikes plateau* — the slide it left from. `r` toggles; the control is a persistent button, not a hover affordance |
| The switch **cannot** fire in fullscreen, demonstrated | **met, against a double** | DS-072, and the honest half is the qualifier. Faked `fullscreenElement` + faked short viewport, then a `resize`: the deck holds. The `no-fullscreen-guard` variant fails it. **Never tested against a real fullscreen** — headless has no gesture to request one, and the check prints that caveat every run rather than implying otherwise (**L-35**) |
| Auto-engage below 960 CSS px and **not** at 1280 | **met, and the rule moved under it** | The criterion as written passes: 800 × 700 engages, 1280 × 720 and 1600 × 900 do not. It is also now the weaker claim — **1280 × 400 must engage too** (k = 0.370) and did not until DS-071 was amended and the deck reconciled |
| **DS-063 demonstrated** — identical up to a uniform scale factor | **met, after correcting the rule** | Full 12-slide run at 3840 × 2000 vs 1280 × 634, k ratio 3.1546: **116 non-text values, worst 0.000 du**; 336 text values, worst 1.17 du. The tolerance split had to be corrected from per-axis to per-element-kind first, and the non-text half had never been measured at all (**L-36**) |
| **A real 12-slide deck opened offline on a large display and on a 1080p display, looked at in both** | **met, with the instrument stated** | Captured at 3840 × 2000, 1920 × 1080, 1280 × 720 and 1280 × 400, offline with DNS black-holed, and **looked at** — the 4K stage letterboxes and centres, the 720p ledger slide is legible row by row, and the short-wide viewport now hands over to a readable document. Real Chrome, but headless: not a physical monitor, and **L-35** says that distinction stays written down |
| Body text ≥ 16 px in a 720p capture | **met** | DS-064: smallest body run **17.3 px** (26 du) on *Eleven minutes decides this*, over 11 slides carrying a body probe. The `body-type-under-the-floor` variant lands at 13.3 px and fails |
| Conformance wording states the alternate-version route | **met** | Was an HTML comment and a half-sentence. [`examples/README.md`](../examples/README.md) now states it in full — *AA via a conforming alternate version reachable by a persistent control* — and says why the presentation view does not carry it alone |
| Every `hard` rule in §2.4 / §2.5 is a check **or** named with the reason | **met** | Gated: DS-060, DS-062, DS-063, DS-064, DS-070, DS-071, DS-072, DS-073, DS-074, DS-075, DS-076, DS-200. Named unenforceable and printed on every run: DS-061 (static, in `audit.py`), DS-065 (**not checkable — the rule was reworded**), DS-072's real-fullscreen half |
| Each new check **seen to fail** | **met** | Seven variants, seven caught. **Three of them were not caught on the first run** — DS-072 asserted stability in a state that could not change, DS-074 sampled one reading-view role while the variant broke three others, and DS-063 sampled a slide with no figure and measured nothing. All three would have shipped as checks that check nothing |
| Checks report the rule ID and the measured value, not a boolean | **met** | Every row prints its number — `worst 0.00 du of 0.25 allowed over 24 values`, `k=0.370 gave doc=False`. A count of zero values is visible rather than silent, which is the specific defect **L-36** is about |
| Runs offline from `file://` in real Chrome, reproducible by one documented command | **met** | `--host-resolver-rules=MAP * ~NOTFOUND`, a throwaway profile, `file:///…`. One command each, documented in [`examples/README.md`](../examples/README.md); both self-test before measuring |

**What this task did not settle, stated rather than implied**

- **One deck.** Every number is the reference deck. DS-063's tolerances are now covered rather than
  asserted, but a second deck would be expected to move the text figure and might move the non-text
  one off zero.
- **Chrome 151 and Edge 151 on Windows, headless, from `file://`.** No Firefox, no Safari, no
  mobile, no physical display.
- **DS-071's threshold is `default`.** A deck that moves it moves DS-168's ≥ 48-design-unit target
  floor with it, and nothing checks that pairing.

**Child fix tasks raised**
- none. Two rule amendments and one rewording went into the ruleset directly, because a `hard` rule
  that a gate proves wrong is not a separate task — it is this task's output.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-07 | → done | **Twelve of the fourteen §2.4 / §2.5 rules are now gated; the two that are not are printed on every run with the reason.** Worked plan steps 1–5 in one pass. The order paid for itself immediately: writing DS-071's check *before* reconciling the deck caught the divergence on 1280 × 400 — k = 0.370 with the deck still on the stage — which is *seen to fail* earned on a real defect rather than a staged one. **The task's real output is not the checks, it is what building them found.** DS-063's non-text tolerance, stated as *measured rather than guessed* and cited to 384 values, turned out to have **zero values in it**: every key in the probe behind those numbers is a text run. Measuring it for the first time gave 116 values at **0.000 du** — the rule was right and its evidence was not there (**L-36**). Two further corrections came with it: the tolerance splits by element kind, not by axis, because glyph rounding moves a text run's position and height as well as its width — implementing the rule as written failed a provably-identical layout on 27 values — and **DS-065 could not be false at all**, since inside the stage a design unit *is* one CSS pixel, so it was reworded to name units that do not ride the transform. The variant suite then caught **three of its own checks measuring nothing**: DS-072 asserted stability in a state that could not change, DS-074 sampled one reading-view role while the variant broke three others, DS-063 sampled a slide with no figure. All three would have shipped green. Deck opened offline and looked at at 3840 × 2000, 1920 × 1080, 1280 × 720 and 1280 × 400 — headless real Chrome, which **L-35** says is not the same as a double-clicked file, and §4 says so too. |
| 2026-08-07 | → specified | **Both remaining open questions answered by the owner, and each produced a rule amendment rather than only a decision row.** *Tier two is inlined* — **DS-073** now states it (panels open in normal flow, control not rendered), ratifying what the reference deck already shipped and matching R7 §5's ruling for print; T-016's disclosure component therefore has one context, not two. *Auto-engage keys off the scale factor, not width* — **DS-071** now reads `min(vw/1920, vh/1080) < 0.5`, with 960 CSS px kept as the quotable equivalent for a 16:9-or-taller viewport. The second amendment **closes a caveat that was already written down and unactioned**: F-06 in `DESIGN-RATIONALE.md` noted that the 0.5 floor assumed width binds, which is what made DS-168's ≥ 48-design-unit floor an assumption; it is now true by construction. `DESIGN-RATIONALE.md`'s viewer-scale table gains the short-and-wide row — 1280 × 400, scale 0.37, body at **8.9 px** — because the case a rule misses belongs next to the rule. **The reference deck now diverges from the ruleset on DS-071** and that is deliberate: plan step 2 reconciles the instance to the rule, not the other way round. |
| 2026-08-07 | (no change) | **§1 rewritten, which is the specify phase's work** — [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md) §4 flagged this specification as stale and left the rewrite to the owner. Three staleness classes, all fixed: **(a)** it cited *"§11 conditions 13–19"* and *"condition 17"*, a numbering [T-022](T-022-split-the-design-system-from-its-rationale.md) removed when it split the design system *(**corrected 2026-08-09 by [T-037](T-037-record-in-the-ruleset-which-rules-no-check-can-reach.md): nothing was removed.** `DESIGN-SYSTEM.md` has ended at §9 in every commit of its life — §11 was recorded as delivered and never written. This row's **fix** was right and its **cause** was wrong, which matters because the wrong cause sends the next reader hunting for a deletion in the history. This task's own translation of *"condition 17"* → DS-063 is the only one anyone made, and it is what later proved the numbering unrecoverable: DS-063 is the 31st hard rule, not the 17th)* — the rules are DS-060–DS-065, DS-200 and DS-070–DS-076, and *condition 17* is **DS-063**; **(b)** its shared-rendering open question was answered `no` by [R7](../docs/research/R7-printable-mode.md) §4 and is struck; **(c)** it read as greenfield while a conforming reflow view and four of the seven §2.5 checks already existed. **The outcome statement changed as a result** — the deliverable is the enforcement, not the view, and the scope now says so. Two questions remain open and **both are the owner's**: whether the ruleset adopts the inlined tier two the instance already ships, and whether DS-071 should key off the computed scale factor rather than 960 CSS px — the arithmetic for the second is in §1 and it says width is a lossy proxy. Four acceptance criteria added for the enforcement half, none of which is started; the original nine are carried unedited, because a criterion reworded after the fact is a description of what happened. |
| 2026-08-07 | (no change) | `related` gains [T-018](T-018-measure-the-printable-mode-what-printing-from-fi.md), the measurement that answers this task's shared-rendering open question. [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md) also **flags this specification as partly satisfied**: the row below records a reflow view already carrying all tier-two content, `scrollWidth` 320 at 320 CSS px and position preserved both ways, so three of the acceptance criteria are demonstrated on one deck. What remains is the fullscreen suppression, the auto-engage threshold, condition 17, the 720p body-text measurement, the conformance wording — and the **enforcement**, which is the half the title names and the half that does not exist. Flagged, not rewritten; the rewrite is the owner's call. |
| 2026-08-06 | (no change) | **A working reflow view now exists** in [`examples/reference-deck.html`](../examples/reference-deck.html), built by [T-024](T-024-build-the-reference-deck-and-validate-the-ruleset.md) because without it the deck fails its own hard rules and the convergence loop is meaningless. Measured: 12 sections carrying all tier-two content, `scrollWidth` **320** at 320 CSS px with zero elements overflowing, position preserved in both directions, panels open and their controls removed. **This task now specifies against a real implementation rather than in the abstract** — and two defects it already surfaced are worth carrying: the stage's absolutely-positioned, fixed-width disclosure panel cannot reflow until both are undone, and an inline `font-size` on a headline outranks the reading view's own type scale. |
| 2026-08-06 | → proposed | Raised out of [T-014](T-014-synthesise-research-into-the-design-system-reference.md) `§9.1`, which the owner settled the same day: keep the fixed stage, add a reflow view. Created because a mode is built, not asserted. **The owner's reason for the stage reshaped the design system rather than only answering the question** — the screen-share arithmetic in §2.4 produced a type floor (body ≥ 24 design units) that no research note had, tightened D5's 18–24 range to 24–28, and demoted the corpus's mono labels to decoration because they are illegible at 720p. |
