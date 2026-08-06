---
id: T-025
title: Reconcile the thirteen ruleset findings the reference deck produced
type: fix
status: proposed
phase: specify
parent: T-024
blocked_by: []
related: [T-005, T-014, T-021, T-022, T-023]
work_package: WP2
owner: maintainer
created: 2026-08-06
updated: 2026-08-06
deliverables: []
---

# T-025 — Reconcile the thirteen ruleset findings the reference deck produced

## 1. Specify

**Outcome**
`docs/DESIGN-SYSTEM.md` and `docs/DESIGN-RATIONALE.md` corrected against the thirteen findings
[T-024](T-024-build-the-reference-deck-and-validate-the-ruleset.md) §3.3 recorded while building to
them, plus `docs/EVALUATION.md` corrected against F-13. Every finding either changes a rule, or is
recorded as considered and rejected with a reason.

**Why this is a separate task, and not part of T-024**
**A test that edits the thing it is testing is not a test.** T-024's job was to build strictly to
the ruleset and record where it broke; changing the rules mid-build would have hidden exactly the
evidence the task existed to produce. The findings are therefore recorded but unapplied, and this
task applies them.

**Scope**
- In: F-01 to F-13, each resolved and the resolution recorded under its rule ID.
- In: the four conflicts between two `hard` rules (F-01, F-03, F-04, F-05) — these are the ones
  where a deck cannot comply with both, so **one of each pair must yield explicitly**.
- In: `DESIGN-RATIONALE.md` §2, which is where the project says conflicts live.
- In: **DS-102 has no provision for an illustrative deck.** "Every figure sourced" cannot be met by a
  deck about a place that does not exist, and the plugin's own example deck is exactly that case.
  T-024 resolved it by making the model the source and saying so on the deck — recorded there as a
  decision rather than a finding, because it did not break the build. The rule should say so, since
  the alternative a builder reaches for is quoting real research from memory, which is a fabricated
  metric wearing a citation.
- In: EVALUATION §6.2/§6.4 (F-13), and EVALUATION §8's cap question, which F-13 answers with
  evidence rather than reasoning.
- Out: rebuilding the reference deck. Where a rule changes, the deck is re-checked against it, not
  rewritten to suit it.
- Out: `T-005`'s build check. This task decides what the rules say; T-005 decides how they are
  tested.

**Inputs**
- [`T-024`](T-024-build-the-reference-deck-and-validate-the-ruleset.md) §3.3 — the findings, each
  with the moment it was found
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) · [`docs/DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) · [`docs/EVALUATION.md`](../docs/EVALUATION.md)
- [`examples/README.md`](../examples/README.md) — the measurements the findings rest on

**Acceptance criteria**
- [ ] Each of F-01 to F-13 has a recorded resolution: rule changed, rule clarified, or rejected with a reason
- [ ] The four `hard`×`hard` conflicts each name which rule yields, in the rule text itself
- [ ] DS-063 carries a stated tolerance, and it is the measured one rather than a guess
- [ ] DS-013's token list covers the data-series and interactive-border roles the deck needed
- [ ] EVALUATION §8's cap question is closed against T-024's evidence
- [ ] `python tools/tasks/task.py check` passes

**Open questions**
- **Does DS-036's mono range move, or does DS-035's floor stop being absolute?** F-01 forces the
  choice and the deck assumed the floor. — owner
- **Should the Motion control (F-03) become a rule of its own?** Every deck with a `Current` flow
  needs it to stay conformant, and no rule currently requires it. — owner

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Sort F-01 to F-13 into: conflict, unimplementable, silence, and check-impossible | four groups, each with a resolution shape |
| 2 | Settle the two owner questions before touching the conflicts | two decisions |
| 3 | Apply rule changes to `DESIGN-SYSTEM.md`, keeping every ID stable | the corrected ruleset |
| 4 | Record every "why" under its ID in `DESIGN-RATIONALE.md` §2 | the rationale |
| 5 | Apply F-13 to `EVALUATION.md` and close §8's cap question | the corrected loop |
| 6 | Re-check the reference deck against every changed rule | a pass, or a new finding |

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
| 2026-08-06 | → proposed | Raised by T-024, which built a real 12-slide deck strictly to the ruleset and produced **thirteen findings** — four of them conflicts between two `hard` rules, three rules unimplementable as written. Kept separate from T-024 on purpose: a test that edits the thing it tests is not a test, so the findings were recorded unapplied. |
