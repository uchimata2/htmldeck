---
id: T-278
title: Write the clause rows for the nine conjunctions the sweep found owing
type: fix
status: proposed
phase: specify
parent: T-219
blocked_by: []
related: [T-244, T-054]
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-08-29
updated: 2026-08-29
deliverables: []
---

# T-278 — Write the clause rows for the nine conjunctions the sweep found owing

## 1. Specify

**Outcome**
`check.py`'s `CONJUNCTIONS_OWED` is empty, because each of its nine rules has a `CLAUSES` row whose
every clause is either decided by a named check or excused with a closing condition. The gate's
clause-level account then covers every `hard` rule whose statement is a conjunction, rather than
seven of sixteen.

**Where this came from.** [T-244](T-244-the-gates-own-coverage-account.md) replaced the clause
sweep's dated sentence with a record tied to the ruleset, and then had to run the sweep the
sentence had stopped covering — **24 `hard` rules** had arrived or moved under it. Reading those 24
found **eleven** conjunctions where `PR-43`'s remedy predicted two. T-244 wrote rows for the two the
register named, `DS-073` and `DS-242`, and **recorded the other nine as a counted backlog instead of
writing them at the end of a batch**, which is this task.

**Why it was not folded into T-244.** Nine rules is about twenty clauses, and a clause row is not
bookkeeping: each one asks *does any check decide this*, and where nothing does it asks for a
closing condition somebody has to be able to defend. Written quickly they would be nine excusals
saying *not checked*, which inflates the account without sharpening it — the exact failure the
`CLAUSES` preamble warns against. The nine are visible and counted in the meantime, printed on
every run, which is the difference between a known hole and an unknown one.

**Scope**
- In: a `CLAUSES` row for each of `DS-110`, `DS-122`, `DS-141`, `DS-146`, `DS-202`, `DS-218`,
  `DS-229`, `DS-230`, `DS-238`, and the matching entries removed from `CONJUNCTIONS_OWED`
- In: for each clause, either the check that decides it or an excusal in `DEFERRED`'s shape — a
  reason somebody can read, and a condition that would end it
- Out: **writing the missing checks.** A clause with no check gets an excusal naming what would
  close it; building that check is its own task, the way `DS-034`'s two open clauses already sit
- Out: the sweep mechanism itself, which is `T-244`'s and is done
- Out: any rule not in the nine. `CONJUNCTIONS_OWED` is the list, and it is derived from a sweep
  rather than from a reading taken again here

**Inputs**
- `check.py`'s `CONJUNCTIONS_OWED`, whose value for each rule is the clause split the sweep saw
- `CLAUSES`'s existing rows — `DS-034`'s two excused clauses are the worked example of a clause
  that is real, unreached, and honestly recorded
- [T-244](T-244-the-gates-own-coverage-account.md) §3, for how the nine were judged

**Acceptance criteria**
- [ ] `CONJUNCTIONS_OWED` is empty and `sweep_debt` reports 0
- [ ] every new clause is decided by a named check or carries an excusal `closing_faults` accepts
- [ ] the clause account's `UNREACHED` count is stated here **before and after**, so the task
      records what it revealed rather than only that it finished
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- **`DS-218`'s second clause — *the deck still reads with motion off* — may not be a check's at
  all.** It is close to a rule 6 look, and if it is, the excusal says so and names the look rather
  than inventing a threshold. Decide it from the rule's own reason and record the decision.

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
| 2026-08-29 | → proposed | Raised by [T-244](T-244-the-gates-own-coverage-account.md) while closing `PR-43`. **The register's remedy was measured and its sizing refused**: it read *two rows, and then the sweep*, and running the sweep the dated sentence had stopped covering found **eleven** conjunctions among 24 unswept rules, not two. T-244 wrote the two named rows and the mechanism that makes the sweep impossible to lose again; these nine are the rest, held as a counted backlog printed on every run rather than written unreviewed at the end of a batch. **`PH3`**: not a defect an adopter met in the published `0.6.0`, so `CLAUDE.md`'s one condition for reopening `PH1` does not apply. |
