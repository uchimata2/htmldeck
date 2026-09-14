---
id: T-298
title: Decide what the clause sweep owes for a rule the clause table cannot hold
type: decision
status: done
phase: review
parent: null
blocked_by: []
related: [T-278, T-244, T-054]
work_package: PH3
shipped_in: unreleased
owner: the project owner
business_value: medium
effort: s
created: 2026-09-03
updated: 2026-09-14
deliverables: [tools/deck/check.py]
---

# T-298 — Decide what the clause sweep owes for a rule the clause table cannot hold

## 1. Specify

**Outcome**
`CONJUNCTIONS_OWED` is empty, because the sweep that fills it and the table that empties it agree
about which rules are theirs. Today they do not: the sweep reads every `hard` rule and records a
conjunction wherever it finds one, and `CLAUSES` refuses a row for any rule `ruleset.owned()`
excludes — `check in ("auto", "render")`. A `hard judge` rule falls between the two and can be
recorded as owing rows it is structurally forbidden to receive.

**Where this came from.** [T-278](T-278-write-the-clause-rows-the-sweep-found-owing.md) wrote the
nine rows the sweep had counted and found that **DS-230 could not take one**: adding it produced
`CLAUSE TABLE DS-230 - the ruleset does not own it`, which fails the run. T-278 closed eight and
left the ninth in the queue with the reason beside it, because the two available exits are both
wrong on their own:

- **Drop it from `CONJUNCTIONS_OWED`.** It would then be swept, judged a conjunction, and recorded
  nowhere — the exact silence the queue's own comment says it exists to prevent.
- **Widen the guard.** The guard is right on its own terms. `CLAUSES` exists because one satisfied
  row moves a rule into `checked` and hides a clause nothing reaches; a `judge` rule is never in
  `checked`, so there is no coverage claim to see through. Worse, DS-230's second clause *is*
  decided — `component.py` closes `data-disc` against the four kinds — but that row reports under
  **DS-229** by design, so a `True` under DS-230 would claim coverage the gate never reports there.

**Scope**
- In: the decision — whether the sweep stops recording conjunctions for rules the clause table
  cannot hold, or a second record holds them, or the guard learns the difference between *not
  tabulated* and *not gate-owned*
- In: whichever of `sweep_faults`, `sweep_debt` or `clause_account` the decision changes, and the
  self-test that would have caught the disagreement
- Out: writing DS-230's clause rows. That is what the decision decides
- Out: DS-230's own text. The rule is `judge` and nothing here argues it should not be

**Inputs**
- `tools/deck/check.py` — `CLAUSES`'s preamble, `CONJUNCTIONS_OWED`, `sweep_debt`,
  `clause_account`, and `check.py:1196`'s self-test, which probes the guard with `DS-999`, an id the
  ruleset does not tabulate at all — so it has never separated the two failures the guard reports
  with one message
- `tools/deck/ruleset.py` — `OWNED = ("auto", "render")` and the `owned` property
- [T-244](T-244-the-gates-own-coverage-account.md) §3, which built the sweep

**Acceptance criteria**
- [ ] `CONJUNCTIONS_OWED` is empty, or the document says which record holds a rule like DS-230 and
      why that is not the queue
- [ ] a self-test distinguishes a clause row for a rule the ruleset does not tabulate from one for a
      rule it tabulates and does not own
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- **Is DS-230 the only rule in this position, or the first one anybody looked at?** The sweep has
  read every `hard` rule, so the question is answerable by counting `hard judge` rules whose text is
  a conjunction. Answer it before choosing an exit — a single instance and a family argue for
  different remedies.
  **Answered 2026-09-14: a family, of at least seven. §3.**

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Answer §1's question: read every `hard` rule the gate does not own, and count the conjunctions | §3 |
| 2 | Choose the exit from the clause table's own reason | §3 |
| 3 | Empty `CONJUNCTIONS_OWED`, make `sweep_debt` refuse a rule the gate does not own, and split the guard's fault into *not tabulated* and *not owned* | `tools/deck/check.py` |
| 4 | Self-test both splits, and the refusal with DS-230 put back in the queue | `tools/deck/check.py` |
| 5 | Lint, then the batch's full gate | — |

## 3. Implement

**Decisions & assumptions**
- §1's question is answered by reading the 34 `hard` rules no gate here owns: DS-230 is not alone.
  At least six more state more than one testable assertion, DS-036, DS-085, DS-102, DS-112, DS-167
  and DS-235, and none was recorded anywhere. Twelve statements were read cut at 330 characters, so
  six is a floor. Reversible. — 2026-09-14
- The exit is the queue's membership. `CONJUNCTIONS_OWED` holds only rules a gate here owns, and
  `sweep_debt` fails a run that puts any other rule there. The clause table's own reason decides it:
  a row exists to see through a `checked` claim, a rule no gate owns is never `checked`, and its
  judge reads the whole statement. §1's objection to dropping DS-230 does not reach such a rule, for
  the reason §1 gives against widening the guard. Reversible. — 2026-09-14
- Widening the guard is refused for T-278's reason, recorded in §1. A second record for these
  conjunctions is refused because nothing would read it: the evaluator applies each whole statement
  already ([`../docs/EVALUATION.md`](../docs/EVALUATION.md) §1.1). Reversible. — 2026-09-14
- The sweep still reads every `hard` rule. A rule whose `Check` moves into a gate changes its row, so
  the sweep reports it `CHANGED` and it is read again as a rule the queue can hold. Reversible.
  — 2026-09-14
- The guard's two failures are reported apart: an id the ruleset does not tabulate, and a tabulated
  rule no gate here owns. Reversible. — 2026-09-14
- The exit was decided here rather than put to the owner, because it follows from the table's own
  reason. The pull request names it so the owner can reverse it. Reversible. — 2026-09-14

| Case | Before | After |
| :--- | :--- | :--- |
| `sweep_debt()`, what is owed | `['DS-230']` | `[]` |
| a clause row for `DS-999`, which the ruleset does not tabulate | `clausesForRulesNotOwned: ['DS-999']` | `clausesForRulesNotTabulated: ['DS-999']` only |
| a clause row for `DS-230`, tabulated as `judge` | `clausesForRulesNotOwned: ['DS-230']`, the same key | `clausesForRulesNotOwned: ['DS-230']` only |
| DS-230 put back in the queue | no fault | `SWEEP DS-230 is owed clause rows the clause table must refuse` |

**Outputs produced**
- `tools/deck/check.py`: `CONJUNCTIONS_OWED` emptied; `sweep_debt` refuses a rule no gate here owns;
  `clause_account` reports *not tabulated* apart from *not owned*; three self-test cases

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| `CONJUNCTIONS_OWED` is empty, or the document says which record holds a rule like DS-230 and why that is not the queue | **pass** | Empty. No record holds DS-230, and §3 says why that is not a silence |
| a self-test distinguishes a clause row for a rule the ruleset does not tabulate from one for a rule it tabulates and does not own | **pass** | `DS-999` lands only in *not tabulated*, and a rule picked from the ruleset's non-owned set lands only in *not owned* |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | **pass** | Lint, then the batch's full gate on the finished tree |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-14 | -> done | Closed on the queue's membership, decided from the clause table's own reason rather than put to the owner. §1's question came first: DS-230 has at least six siblings, so the remedy is a rule of membership rather than a row. |
| 2026-09-14 | -> in_progress | Step 1 answered §1's question before an exit was chosen. |
| 2026-09-14 | -> planned | Five steps. |
| 2026-09-14 | -> specified | §1 was complete as raised. |
| 2026-09-03 | → proposed | Raised by [T-278](T-278-write-the-clause-rows-the-sweep-found-owing.md) while writing the nine rows the sweep counted. **The defect is a disagreement between two records, not a missing row**: `sweep_faults` reads every `hard` rule and `CLAUSES` accepts only `auto` and `render` ones, so the queue can hold a rule the table must refuse. Found by attempting it — the row was written, the run went red on `clausesForRulesNotOwned`, and the guard's message names jurisdiction where the self-test only ever probed existence. **`PH3`**: not a defect an adopter met in the published `0.6.0`, so `CLAUDE.md`'s one condition for reopening `PH1` does not apply. |
