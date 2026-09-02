---
id: T-298
title: Decide what the clause sweep owes for a rule the clause table cannot hold
type: decision
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-278, T-244, T-054]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-09-03
updated: 2026-09-03
deliverables: []
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

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <the files this task changed>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- <T-NNN or "none">

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-03 | → proposed | Raised by [T-278](T-278-write-the-clause-rows-the-sweep-found-owing.md) while writing the nine rows the sweep counted. **The defect is a disagreement between two records, not a missing row**: `sweep_faults` reads every `hard` rule and `CLAUSES` accepts only `auto` and `render` ones, so the queue can hold a rule the table must refuse. Found by attempting it — the row was written, the run went red on `clausesForRulesNotOwned`, and the guard's message names jurisdiction where the self-test only ever probed existence. **`PH3`**: not a defect an adopter met in the published `0.6.0`, so `CLAUDE.md`'s one condition for reopening `PH1` does not apply. |
