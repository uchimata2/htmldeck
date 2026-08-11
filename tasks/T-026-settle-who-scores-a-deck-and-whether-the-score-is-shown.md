---
id: T-026
title: Settle who scores a deck, and whether the score reaches the user
type: decision
status: done
phase: review
parent: T-023
blocked_by: []
related: [T-002, T-004, T-020, T-024]
work_package: WP2
shipped_in: 0.1.0
owner: maintainer
created: 2026-08-06
updated: 2026-08-12
deliverables: [docs/EVALUATION.md]
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
- ~~Both questions in the Outcome are themselves the open questions.~~ **Both answered by the owner
  2026-08-06**, and the answer to the first is not the recommendation that was on the table — see
  §3.2.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | State each option's cost in passes, using T-024's deck as the unit | a cost table |
| 2 | Put the two rulings to the owner with the T-024 evidence attached | two decisions |
| 3 | Rewrite EVALUATION §8 from recommendations into rulings | the corrected document |

## 3. Implement

### 3.1 The cost table (plan step 1)

Costs are **scoring passes**, using T-024's deck as the unit: 12 slides, PASS in 2 measurement
rounds, cap 3. §6.3's regression sweep is what makes later rounds cheaper than the first for the
per-slide options.

| Option | Round 1 | Per later round | T-024's deck (2 rounds) | At cap 3 |
| :--- | :-: | :-: | :-: | :-: |
| Author scores everything | 0 | 0 | **0** | 0 |
| Author per-slide, fresh-context whole-deck | 1 | 1 | **2** | 3 |
| **Author per-slide + one fresh judgement pass** (chosen) | 2 | 2 | **4** | 6 |
| Fresh context scores everything | 13 | 1 + 12×(touched fraction) | **~25** | ~37 |

The middle two differ by one pass per round and by three dimensions: the standing recommendation put
only D1 and D4 in fresh context, leaving S1, S2 and S4 — three of the five judgement-only dimensions
— with the author.

### 3.2 Decisions & assumptions

- **Who scores: the author takes S3/S5/S6 per slide; one fresh-context pass takes S1, S2, S4, and
  D1–D4.** All five judgement-only dimensions move to fresh context, not two of them. Cost accepted:
  2 passes per round (4 for a T-024-sized deck, 6 at the cap), against 1 for the recommendation and
  ~25 for full fresh-context scoring. — owner, 2026-08-06
- **S1/S2/S4 are scored in one read of the whole deck, not twelve isolated ones.** Recorded as a
  substantive claim rather than a cost compromise: S4's "a first-time reader needs this" and S2's
  "one side argued and the other not" are judgements about the deck a reader meets, and isolated
  per-slide context cannot make them. — 2026-08-06
- **Visibility: outcome and findings, never the numbers.** No per-slide total, no whole-deck total,
  no per-dimension score. A dimension at 0 or 1 still reaches the user, as a finding naming the
  dimension — §5 already makes it one regardless of the total. Cost accepted: none in passes;
  opacity is the cost — the user cannot see how close to threshold a deck sits. — owner, 2026-08-06
- **Stated limit on what 8.1 buys.** Fresh context removes the build history, not the author. Where
  the same model scores its own work without that history, the ruling buys independence of memory,
  not of judgement. Written into EVALUATION §8.1 rather than left implicit, per L-05. — 2026-08-06
- **Assumption, load-bearing for the cost table:** a "pass" is one read of the artifact in one
  context. If the pipeline that implements this (T-020) cannot start a genuinely fresh context, the
  cost is unchanged but §8.1's independence claim is not met — and that is a finding against T-020,
  not a licence to re-open this ruling.

### 3.3 Outputs produced

- [`docs/EVALUATION.md`](../docs/EVALUATION.md) — §8 rewritten from three open questions into
  **§8.1 / §8.2 / §8.3, three rulings**; §2's stage table, §6's loop diagram, §6.1's reporting note,
  §6.3's regression sweep, §6.4's cost and §5's threshold reconciled to the new split.
- [`docs/LESSONS.md`](../docs/LESSONS.md) — **L-29**, *evidence arriving after a recommendation must
  re-derive it, not ratify it*. This task is its case: the evidence confirmed the recommendation's
  reasoning while showing its scope was three dimensions short, and confirmation of the reasoning is
  what made the gap easy to miss. **Not declared in `deliverables:`** — see the tooling finding in §4.
- [`docs/BRIEF.md`](../docs/BRIEF.md) — two rows added to *Decisions taken*, and the `EVALUATION.md`
  line in *What to build* no longer describes §8 as open.
- Two documents corrected where the rulings made them stale:
  [T-024](T-024-build-the-reference-deck-and-validate-the-ruleset.md) §4.1, whose stated limitation
  cited §8 as a recommendation, and
  [T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md) §1, whose per-batch/whole-deck
  hypothesis no longer holds now that S1/S2/S4 are whole-deck-timed.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| EVALUATION §8 states a decision for each question, not a recommendation | **met** | §8.1 and §8.2 are rulings, each opening with **Ruling**; §8.3 records the cap, closed earlier by T-025. The section heading is now "Decisions taken". |
| Each decision records the cost it accepts, in passes | **met** | §8.1: 2 passes per round, 4 for a T-024-sized deck, 6 at cap, against 0 / 1 / ~25 for the alternatives. §8.2: none in passes, with opacity named as the cost it does carry. |
| The ruling on *who scores* says explicitly how the five judgement-only dimensions are covered | **met** | §8.1 names S1, S2, S4, D1, D4 and assigns **all five** to the fresh-context pass, with T-024 §4.2 cited for why they are the ones that matter and T-024 §4.1's D4 result for why the author is the wrong scorer for them. |
| The ruling on *visibility* says what the user sees instead, if not the number | **met** | §8.2 *What the user sees instead*: outcome, every finding with severity and rule ID or dimension, what was fixed and remaining `Note`s on a PASS, and any dimension at 0 or 1 named as a finding. |
| `python tools/tasks/task.py check` passes | **met** | See the log row below. |

**Reconciliation beyond the criteria.** The rulings changed the pipeline's shape, so five other
places in EVALUATION were corrected rather than left describing the old one: §2's stages 3–4, §5's
threshold (a slide's 24 points now span two scorers), §6's diagram, §6.1 (no outcome prints the
score), §6.3's sweep, and §6.4's cost. A ruling recorded in §8 while §2 still describes the
superseded pipeline is the single-source-of-truth failure this project keeps finding.

**A tooling finding, raised in passing and not fixed here.** `docs/LESSONS.md` was briefly declared
as a deliverable of this task. **`check`'s pointer count fell by six and it still printed
`0 broken`** — because `check` **exempts any path some task declares as a deliverable**
(`tools/tasks/task.py`, the `declared` set), on the stated rationale that a deliverable is *"a
promise about the future"*. That rationale does not hold for a file that already exists: declaring
one silently drops every repo-relative mention of it out of validation, for every document in the
repository, and nothing in the output distinguishes that from six pointers being fine. The
declaration was reverted — the lesson is an edit to a shared document, not an output this task
promises. **Raised as [T-029](T-029-stop-the-deliverable-exemption-silently-dropping-pointers.md)**,
which also carries the second defect found while writing it up: the exemption compares the **raw**
link target against **normalised repo-relative** paths, so the same file is exempt when written
`` `docs/LESSONS.md` `` and checked when written `[…](../docs/LESSONS.md)`. Both are changes to
`task.py` and TASK-WORKFLOW §6, and neither belongs in a decision task.

**Not verified here.** Neither ruling has been *run* — §8.1's independence claim and §8.2's report
shape are both exercised for the first time by [T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md).
This task settles what the pipeline must do; it does not demonstrate it.

**Child fix tasks raised**
- [T-029](T-029-stop-the-deliverable-exemption-silently-dropping-pointers.md) — the deliverable
  exemption above. Two defects, not one: it ignores whether the file exists, **and** it matches only
  the repo-relative written form, so `` `docs/LESSONS.md` `` is exempt where
  `[…](../docs/LESSONS.md)` is not.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-06 | → done | Both rulings taken by the owner and written into EVALUATION §8 as §8.1 and §8.2. **The first departs from the recommendation the task carried:** all five judgement-only dimensions go to the fresh-context pass, not the two (D1, D4) the recommendation covered — the owner bought S1, S2 and S4 for one extra pass per round. §8's heading changed from "Open — needs a decision" to "Decisions taken"; six other places in the document that described the superseded pipeline were reconciled (§4 *Reconciliation*). `task.py check` passes. |
| 2026-08-06 | (no change) | **EVALUATION §8's third question — *"is the cap 2 or 3?"* — was closed by [T-025](T-025-reconcile-the-thirteen-ruleset-findings-from-the-reference-deck.md)**, against T-024's evidence rather than by decision: 2 measurement rounds measured, cap stays 3. It was never this task's, and this task's two remain open and unchanged. Recorded so §8's three entries are not read as three open questions. |
| 2026-08-06 | → proposed | Split out of [T-023](T-023-the-deck-evaluation-rubric-and-convergence-loop.md) at its closure. Both questions are the owner's and neither was decidable before a real deck existed; T-024 now supplies the evidence, including the honest limitation that its own scores were the author's. |
