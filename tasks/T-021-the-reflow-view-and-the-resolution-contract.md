---
id: T-021
title: Build the reflow view and enforce the resolution contract
type: deliverable
status: specified
phase: plan
parent: null
blocked_by: []
related: [T-002, T-005, T-007, T-014, T-016, T-018]
work_package: WP2
owner: maintainer
created: 2026-08-06
updated: 2026-08-07
deliverables: []
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

*Not yet worked — the phase is `specify`. Steps 1–4 predate the 2026-08-07 rewrite of §1 and are
carried with their stale rule references corrected; step 2 in particular no longer describes the
work, since the rendering and the switch exist.*

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Settle the two remaining open questions above against a real deck, not in the abstract | decisions recorded in §3 |
| 2 | ~~Build the document rendering and the switch~~ — **exists**. Reconcile the instance against §2.5 instead, and fix whichever side is wrong | the instance and the ruleset agreeing |
| 3 | Implement DS-060–DS-065, DS-200 and DS-070–DS-076 as checks, **DS-063 first** — it is the cheapest and catches the whole "broken on my monitor" class | checks in `tools/deck/audit.py`, handed to T-005 |
| 4 | Verify on a real 12-slide deck at both resolutions, offline, and in a 720p capture | measurements in §4 |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <path>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-07 | → specified | **Both remaining open questions answered by the owner, and each produced a rule amendment rather than only a decision row.** *Tier two is inlined* — **DS-073** now states it (panels open in normal flow, control not rendered), ratifying what the reference deck already shipped and matching R7 §5's ruling for print; T-016's disclosure component therefore has one context, not two. *Auto-engage keys off the scale factor, not width* — **DS-071** now reads `min(vw/1920, vh/1080) < 0.5`, with 960 CSS px kept as the quotable equivalent for a 16:9-or-taller viewport. The second amendment **closes a caveat that was already written down and unactioned**: F-06 in `DESIGN-RATIONALE.md` noted that the 0.5 floor assumed width binds, which is what made DS-168's ≥ 48-design-unit floor an assumption; it is now true by construction. `DESIGN-RATIONALE.md`'s viewer-scale table gains the short-and-wide row — 1280 × 400, scale 0.37, body at **8.9 px** — because the case a rule misses belongs next to the rule. **The reference deck now diverges from the ruleset on DS-071** and that is deliberate: plan step 2 reconciles the instance to the rule, not the other way round. |
| 2026-08-07 | (no change) | **§1 rewritten, which is the specify phase's work** — [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md) §4 flagged this specification as stale and left the rewrite to the owner. Three staleness classes, all fixed: **(a)** it cited *"§11 conditions 13–19"* and *"condition 17"*, a numbering [T-022](T-022-split-the-design-system-from-its-rationale.md) removed when it split the design system — the rules are DS-060–DS-065, DS-200 and DS-070–DS-076, and *condition 17* is **DS-063**; **(b)** its shared-rendering open question was answered `no` by [R7](../docs/research/R7-printable-mode.md) §4 and is struck; **(c)** it read as greenfield while a conforming reflow view and four of the seven §2.5 checks already existed. **The outcome statement changed as a result** — the deliverable is the enforcement, not the view, and the scope now says so. Two questions remain open and **both are the owner's**: whether the ruleset adopts the inlined tier two the instance already ships, and whether DS-071 should key off the computed scale factor rather than 960 CSS px — the arithmetic for the second is in §1 and it says width is a lossy proxy. Four acceptance criteria added for the enforcement half, none of which is started; the original nine are carried unedited, because a criterion reworded after the fact is a description of what happened. |
| 2026-08-07 | (no change) | `related` gains [T-018](T-018-measure-the-printable-mode-what-printing-from-fi.md), the measurement that answers this task's shared-rendering open question. [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md) also **flags this specification as partly satisfied**: the row below records a reflow view already carrying all tier-two content, `scrollWidth` 320 at 320 CSS px and position preserved both ways, so three of the acceptance criteria are demonstrated on one deck. What remains is the fullscreen suppression, the auto-engage threshold, condition 17, the 720p body-text measurement, the conformance wording — and the **enforcement**, which is the half the title names and the half that does not exist. Flagged, not rewritten; the rewrite is the owner's call. |
| 2026-08-06 | (no change) | **A working reflow view now exists** in [`examples/reference-deck.html`](../examples/reference-deck.html), built by [T-024](T-024-build-the-reference-deck-and-validate-the-ruleset.md) because without it the deck fails its own hard rules and the convergence loop is meaningless. Measured: 12 sections carrying all tier-two content, `scrollWidth` **320** at 320 CSS px with zero elements overflowing, position preserved in both directions, panels open and their controls removed. **This task now specifies against a real implementation rather than in the abstract** — and two defects it already surfaced are worth carrying: the stage's absolutely-positioned, fixed-width disclosure panel cannot reflow until both are undone, and an inline `font-size` on a headline outranks the reading view's own type scale. |
| 2026-08-06 | → proposed | Raised out of [T-014](T-014-synthesise-research-into-the-design-system-reference.md) §9.1, which the owner settled the same day: keep the fixed stage, add a reflow view. Created because a mode is built, not asserted. **The owner's reason for the stage reshaped the design system rather than only answering the question** — the screen-share arithmetic in §2.4 produced a type floor (body ≥ 24 design units) that no research note had, tightened D5's 18–24 range to 24–28, and demoted the corpus's mono labels to decoration because they are illegible at 720p. |
