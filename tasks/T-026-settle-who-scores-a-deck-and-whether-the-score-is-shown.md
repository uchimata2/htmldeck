---
id: T-026
title: Settle who scores a deck, and whether the score reaches the user
type: decision
status: proposed
phase: specify
parent: T-023
blocked_by: []
related: [T-002, T-004, T-020, T-024]
work_package: WP2
owner: maintainer
created: 2026-08-06
updated: 2026-08-06
deliverables: []
---

# T-026 — Settle who scores a deck, and whether the score reaches the user

## 1. Specify

**Outcome**
Two decisions recorded in [`docs/EVALUATION.md`](../docs/EVALUATION.md) §8, replacing the
recommendations there with rulings: **who runs the scoring pass**, and **whether the number is ever
shown to the user**. Both currently sit as "Open — needs a decision", and both shape what
[T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md) and
[T-004](T-004-critique-mode-blunt-section-by-section-review.md) can build.

**Why now, and why they were not settled with the rubric**
[T-023](T-023-the-deck-evaluation-rubric-and-convergence-loop.md) deliberately left them open: they
are cost-and-trust decisions for the owner, not properties of the rubric. They were also not
decidable in the abstract. **They are now** —
[T-024](T-024-build-the-reference-deck-and-validate-the-ruleset.md) produced a real 12-slide deck,
a validated rubric, and a scoring pass whose limitations were recorded rather than hidden.

**What T-024 contributes to each decision**

| Question | The evidence now available |
| :--- | :--- |
| **Who scores?** | T-024's scores were the author's, and the task says so in §4.1. The rubric caught every seeded defect — but the seeded deck was scored knowing defects existed. **The untested case is the one that matters: an author scoring its own unseeded work.** T-024 also shows the shape of the risk — D4 scored 4 only after counting; on reading alone it was a 2, and the author had read past the contradiction repeatedly. |
| **Does the score reach the user?** | The deck reached PASS at 18–22 per slide and 16/16 whole-deck. Those numbers look like precision the rubric does not have — §0 of EVALUATION says so directly. The findings, by contrast, were all actionable. |

**Scope**
- In: the two rulings, written into EVALUATION §8 as decisions with their reasoning.
- In: the **cost** of each option, stated in passes rather than adjectives — a fresh-context
  whole-deck pass is one pass over a finished artifact; a fresh-context per-slide pass is twelve.
- In: the consequence for the **five judgement-only dimensions** (S1, S2, S4, D1, D4 — T-023 §4).
  These are the dimensions no gate can cover, so whoever scores them *is* the quality mechanism.
- Out: changing any anchor or threshold. That is the rubric, and it is closed.
- Out: implementing whichever scorer is chosen — that is T-020's pipeline.

**Inputs**
- [`docs/EVALUATION.md`](../docs/EVALUATION.md) §8 — the two questions, with recommendations already stated
- [`T-024`](T-024-build-the-reference-deck-and-validate-the-ruleset.md) §4.1–§4.2 — a real scoring pass, its results, and its stated limitation
- [`docs/LESSONS.md`](../docs/LESSONS.md) — **L-05**, on what a check may claim

**Acceptance criteria**
- [ ] EVALUATION §8 states a decision for each question, not a recommendation
- [ ] Each decision records the cost it accepts, in passes
- [ ] The ruling on *who scores* says explicitly how the five judgement-only dimensions are covered
- [ ] The ruling on *visibility* says what the user sees instead, if not the number
- [ ] `python tools/tasks/task.py check` passes

**Open questions**
- Both questions in the Outcome are themselves the open questions. — owner

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | State each option's cost in passes, using T-024's deck as the unit | a cost table |
| 2 | Put the two rulings to the owner with the T-024 evidence attached | two decisions |
| 3 | Rewrite EVALUATION §8 from recommendations into rulings | the corrected document |

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
| 2026-08-06 | → proposed | Split out of [T-023](T-023-the-deck-evaluation-rubric-and-convergence-loop.md) at its closure. Both questions are the owner's and neither was decidable before a real deck existed; T-024 now supplies the evidence, including the honest limitation that its own scores were the author's. |
