---
id: T-023
title: Define the deck evaluation rubric and the convergence loop that uses it
type: deliverable
status: done
phase: review
parent: null
blocked_by: []
related: [T-002, T-004, T-005, T-014, T-020, T-024]
work_package: WP1
owner: maintainer
created: 2026-08-06
updated: 2026-08-06
deliverables: [docs/EVALUATION.md]
---

# T-023 — Define the deck evaluation rubric and the convergence loop that uses it

## 1. Specify

**Outcome**
A stated method for **scoring a deck against the design system** — per slide and whole-deck — and a
**convergence loop** that evaluates, reports, fixes and re-evaluates until a stated threshold is met
or the loop stops honestly and says why. Deliverable: `docs/EVALUATION.md`.

**Why this one**
Raised by the owner, 2026-08-06: *a design system without an effective and efficient pipeline is
just decoration.* The project has 120-odd rules, six research notes and no way to answer *"is this
deck good enough yet?"* — which is the only question that matters at build time.

**The gap is specific.** `docs/BRIEF.md` names a check (pass/fail) and a critique mode (prose
findings). Neither produces a **score**, so neither can drive a loop: pass/fail cannot show
progress, and prose cannot show convergence. **Nothing in the repository states what "good enough"
means**, which means today the loop terminates when the agent feels finished.

**Scope**

- In: the **gate/score split.** `hard` rules are **gates, not score contributors** — a hard violation
  fails the deck outright and no quality elsewhere compensates. Only `default` and `guidance` rules
  and the judgement dimensions are scored.
- In: the **dimensions**, per slide and whole-deck, each with **anchor descriptions at 0, 2 and 4**
  rather than bare numbers — an unanchored scale scored by the same agent that wrote the deck drifts
  to the middle.
- In: the **threshold**, stated as three conditions that must hold together, including a **floor per
  dimension** so a slide cannot be carried to passing by craft while its claim is absent.
- In: the **loop's termination rules** — an iteration cap, a required minimum improvement per
  iteration, oscillation detection, and what happens when it stops short.
- In: **regression sweep.** Each iteration re-runs the checks that *passed*, not only those that
  failed. A fix that breaks something previously fine is the failure mode a fix loop is most prone
  to and least likely to notice.
- In: **ordering, for cost.** Cheap automatic gates before any judgement pass; per-slide before
  whole-deck; re-score only touched slides plus a full whole-deck pass.
- In: **the whole-deck pass is not optional, and the report says which passes ran.** Defects that
  span slides are invisible to per-slide review — this project has the evidence twice over.
- In: **validating the rubric itself** against a deck with seeded, known defects.
- Out: implementing the loop. This defines it; [T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md)
  places it in the pipeline, [T-004](T-004-critique-mode-blunt-section-by-section-review.md) reports
  it, [T-005](T-005-build-check-the-gate-the-deck-must-pass.md) runs its automatic half.
- Out: any new design rule. The rubric scores the rules that exist; it does not invent standards.

**Inputs**
- `docs/DESIGN-SYSTEM.md` after T-022 — the `DS-nnn` IDs and the `Check` column are what the rubric
  binds to. **This is why T-022 is a hard blocker: a rubric cannot cite rules that have no IDs.**
- `docs/research/R1-corpus-conventions.md` §14 — the two proven critique formats and the severity
  scheme, which the rubric reuses rather than replacing.
- `docs/research/R3-exemplar-decks.md` §6 — the twelve anti-patterns, already scoring-shaped.
- `docs/LESSONS.md` — **L-05** (a check cannot tell you a deliverable is good) and the
  verify-the-checker lesson are direct constraints on what this rubric may claim.

**Acceptance criteria**
- [ ] Every dimension has anchor text at 0, 2 and 4 — not just a numeric scale
- [ ] Every dimension traces to `DS-nnn` rules or to a named anti-pattern; **no dimension is invented
      for the rubric's convenience**
- [ ] The threshold is stated as conditions that can be evaluated without judgement about the
      threshold itself
- [ ] The loop terminates in **all** of: threshold met · iteration cap reached · improvement below
      the minimum delta · oscillation detected — each with a stated, different output
- [ ] The regression sweep is specified, including what it re-runs and when
- [ ] **The rubric is run against a deck with seeded known defects and finds them** — the
      verify-the-checker lesson, and already in BRIEF's definition of done
- [ ] The document states plainly that **the score is a stopping rule, not a quality claim**
- [ ] Cost is bounded and stated: what runs per iteration, and what the cap implies

**Open questions**
- **Who scores?** The same agent that wrote the deck, a fresh-context evaluator, or both? A
  self-scoring author is the cheap option and the one most likely to pass its own work — M9 names
  this as the failure a self-review most easily misses. A fresh evaluator costs a full context.
  **This is the decision that most affects whether the loop is worth having.** — owner
- **Does the score ever reach the user?** A visible number invites gaming and implies a precision the
  rubric does not have; hiding it makes the loop opaque. — owner
- ~~**Is the iteration cap 2 or 3?**~~ **Answered against a real deck, 2026-08-06 — and the question
  turned out to be the wrong one.** T-024 finding F-13: the reference deck needed **23 fixes** before
  it cleared its own gate. Under §6.2's "fixes are applied one at a time", a cap of 3 permits three
  fixes and the loop would have reported CAP with twenty defects outstanding. Run as **two
  measurement rounds with fixes batched inside each**, it reached PASS. So **the cap governs
  measurement rounds, not fixes**, and 2 rounds sufficed for a first draft. The one-at-a-time rule
  should be scoped to fixes that interact — the case it was written for. Applying this to
  `EVALUATION.md` is [T-025](T-025-reconcile-the-thirteen-ruleset-findings-from-the-reference-deck.md).

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Derive the dimensions from the `DS-nnn` rules and the anti-patterns, discarding any that do not trace | dimension list with traces |
| 2 | Write anchors at 0/2/4 for each, in language that describes an artifact rather than a feeling | the rubric |
| 3 | Set the threshold and the loop's four termination rules | `docs/EVALUATION.md` |
| 4 | Seed a deck with known defects, one per dimension, and run the rubric against it | the validation result, and whatever it changes |

## 3. Implement

**Decisions & assumptions**
- **Hard rules are gates and are never scored — 2026-08-06.** Averaging a hard failure into a total
  is how a deck ships with a wrong number on the title slide and a respectable percentage.
- **A per-dimension floor of 2, not just a total — 2026-08-06.** Without it a slide reaches 18/24 on
  craft and motion while scoring 1 on Claim: a beautiful slide that says nothing, which is the exact
  failure the design system exists to prevent.
- **Anchors at 0/2/4, described as artifacts rather than feelings — 2026-08-06.** The likely scorer
  is the agent that wrote the deck. An unanchored 0–10 scale drifts to the middle and produces
  false precision on top of it.
- **A slide with no motion scores S6 `n/a`, prorated — not 4 — 2026-08-06.** Scoring absence as
  perfection rewards doing nothing.
- **Four distinct stop outcomes, not one — 2026-08-06.** PASS, CAP, STALL and OSCILLATION mean
  different things and need different reports. **OSCILLATION is a finding about the ruleset**: two
  rules that cannot both hold on one slide belong in `DESIGN-RATIONALE.md` §2, not papered over with
  a third fix.
- **The regression sweep re-scores slides sharing a component with a touched slide — 2026-08-06.**
  DS-136 requires interaction patterns to be built once and reused, so a component fix silently
  touches every slide using it. This is where regressions actually hide, and no obvious sweep design
  catches it.

**Outputs produced**
- [`docs/EVALUATION.md`](../docs/EVALUATION.md) — 8 sections

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Anchors at 0, 2 and 4 for every dimension | **met** | 10 dimensions — S1–S6, D1–D4 — each with three anchors |
| Every dimension traces to `DS-nnn` or a named anti-pattern | **met** | Traces are on each dimension heading; none invented for the rubric |
| The threshold is evaluable without judging the threshold | **met** | §5 — three conditions, each mechanical given the scores |
| Four termination outcomes, each with a different output | **met** | §6.1 |
| The regression sweep is specified | **met** | §6.3, four re-run classes |
| **The rubric finds seeded known defects** | **met** | Closed by [T-024](T-024-build-the-reference-deck-and-validate-the-ruleset.md) §4.2. Ten defects seeded, one per dimension, derived from the reference deck so everything else stayed constant. **All ten scored 0 or 1; no anchor needed correcting.** The fixture is [`examples/reference-deck-seeded-defects.html`](../examples/reference-deck-seeded-defects.html), regenerated by `python tools/examples/seed_defects.py`. |
| States that the score is a stopping rule, not a quality claim | **met** | §0 preamble, repeated in §7 |
| Cost bounded and stated | **met** | §6.4 |

**Why this task is `review` and not `done`.** Nine of ten criteria are met and the tenth is the one
that matters most: **an unvalidated rubric passes everything.** This project has already paid for
that — a quality scan under-reported by 15× and was believed because it did not look like a tool.
The rubric stays unclosed until it has been run against a deck with seeded defects and found them.
That deck is the same artifact CLAUDE.md rule 6 has been asking for since T-014, and it now has a task: [T-024](T-024-build-the-reference-deck-and-validate-the-ruleset.md).

**Child fix tasks raised**
- [T-026](T-026-settle-who-scores-a-deck-and-whether-the-score-is-shown.md) — the two §8 questions that
  are the owner's, not this task's. Both are now decidable against a real deck rather than in the abstract.

**What validating the rubric revealed, beyond the pass**

Recorded here because it changes how the rubric should be *used*, not what it says. Of the ten
dimensions, **five are catchable mechanically and five are not**: S3, S5, S6, D2 and D3 were found by
the auto and render gates; **S1, S2, S4, D1 and D4 are invisible to any static or measured check.** A
pipeline that stops at the gate ships a deck whose headline is a topic label, whose figures contradict
each other, and whose slides are ordered by topic. That is DS-191 demonstrated rather than asserted,
and it is a constraint on [T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md).

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-06 | → done | Last criterion closed by [T-024](T-024-build-the-reference-deck-and-validate-the-ruleset.md): ten seeded defects, **all scored 0 or 1, no anchor corrected**. The cap question is answered too, and the answer reframes it — the cap governs measurement rounds, not fixes (F-13). Two owner decisions move to [T-026](T-026-settle-who-scores-a-deck-and-whether-the-score-is-shown.md); the EVALUATION edits F-13 implies move to [T-025](T-025-reconcile-the-thirteen-ruleset-findings-from-the-reference-deck.md). |
| 2026-08-06 | → review | `docs/EVALUATION.md` written. Unblocked early: T-022 landed the `DS-nnn` IDs and the `Check` column the same day, and the `Check` column turned out to be what makes the pipeline routable — 59 `auto` before 32 `render` before 36 `judge` is the cost ordering, derived rather than asserted. **Held at `review`, not closed: the rubric has never been run against a deck with seeded defects**, and an unvalidated rubric passes everything. |
| 2026-08-06 | → proposed | Raised by the owner: *a design system without an effective and efficient pipeline is just decoration.* The gap is precise — the brief has a pass/fail check and a prose critique, and **neither produces a score, so neither can drive a loop.** Pass/fail cannot show progress and prose cannot show convergence, so nothing in the repository states what "good enough" means. Blocked on [T-022](T-022-split-the-design-system-from-its-rationale.md) because a rubric cannot cite rules that have no IDs. |
