---
id: T-278
title: Write the clause rows for the nine conjunctions the sweep found owing
type: fix
status: done
phase: review
parent: T-219
blocked_by: []
related: [T-244, T-054]
work_package: PH3
shipped_in: 0.7.0
owner: the project owner
business_value: medium
effort: m
created: 2026-08-29
updated: 2026-09-03
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
| 1 | Record the `UNREACHED` count before anything is written, from `clause_account()` itself rather than by adding up rows | 7 rules, 20 clauses, 11 decided, **9 unreached** |
| 2 | For each of the nine, read the checks that already report under it and decide each clause: named check, or an excusal in `DEFERRED`'s shape | a verdict per clause, 20 of them |
| 3 | Write the rows into `CLAUSES` and empty `CONJUNCTIONS_OWED` | `tools/deck/check.py` |
| 4 | Re-run `clause_account()`, `sweep_debt()` and `sweep_faults()` and state the count after | 15 rules, 38 clauses, 23 decided, **15 unreached** |
| 5 | Answer the open question in §1 in the row itself, not only here | DS-218's second clause is a `look` |
| 6 | `python tools/tasks/lint.py`, then `python tools/check_all.py` — separately, never at once | both green |

## 3. Implement

**Decisions & assumptions**

- **DS-218's second clause is a `look`, and that answers §1's open question — 2026-09-03.** *The
  deck still reads with motion off* is a property of the rendered deck seen by somebody. Its
  mechanical half already has an owner: DS-143 decides that nothing is left animating under
  `prefers-reduced-motion` and that no risen element is stranded at `opacity:0`. What DS-218 adds is
  whether the deck still **argues** with the motion stopped — whether a diagram whose meaning was in
  the movement still says it — and no threshold expresses that. `CLOSING_KINDS` already carries
  `look` for exactly this, subject `None`, so the excusal names the look rather than inventing a
  number. The question asked whether to decide it from the rule's own reason; the rule's own reason
  is that a person reads it.
- **DS-230 could not take a row, and it stays in `CONJUNCTIONS_OWED` — 2026-09-03.** Writing its two
  clauses turned the run red: `CLAUSE TABLE DS-230 - the ruleset does not own it`, because
  `ruleset.owned()` is `check in ("auto", "render")` and DS-230 is `judge`. **The guard is right**:
  `CLAUSES` exists because one satisfied row moves a rule into `checked` and hides a clause nothing
  reaches, and a `judge` rule is never in `checked`, so there is no coverage claim to see through.
  Its second clause *is* decided — `component.py` closes `data-disc` against the four kinds — but
  that row reports under **DS-229** by design, so `True` under DS-230 would claim coverage the gate
  never reports there. Dropping it from the queue instead would be the silence the queue exists to
  prevent, so it is left with the reason written beside it and the decision handed to
  [T-298](T-298-decide-what-the-clause-sweep-owes-for-a-rule-the-clause-table-cannot-hold.md).
- **DS-202's two open clauses close on an amendment, not on work — 2026-09-03.** *Factual* is a
  reading of a sentence, DS-100's *active voice* one rule family over. *Not the headline restated*
  is different and lands in the same place for a different reason: both subjects are in the DOM, so
  it is reachable, but *restated* is an overlap and any cut-off is a number chosen to fit the decks
  in hand (**L-38**). T-270 found eight bottom lines restating their own headline **by reading
  them**, which is evidence that the fault is real and that a person is what found it.
- **The clause split is the sweep's, not a fresh reading — 2026-09-03.** §1's scope says
  `CONJUNCTIONS_OWED` is the list; its *value* is the split the sweep saw, and re-splitting a rule
  here would make the queue's record unfalsifiable. So DS-146 gets the two clauses recorded for it
  and not a third for the `data-arrived` sentence the rule gained later.

**What the account did before and after** — from `clause_account()`, not from adding up rows:

| | rules | clauses | decided | UNREACHED |
| :--- | ---: | ---: | ---: | ---: |
| before | 7 | 20 | 11 | **9** |
| after | 15 | 38 | 23 | **15** |

The eighteen new clauses are twelve decided and six not, and the six are the thing the count of nine
was standing in for: DS-141's *eased rather than linear*, DS-146's *Rise, not a stroke-dash*,
DS-202's *factual* and *not the headline restated*, DS-218's *reads with motion off*, and DS-238's
*runs at or above its rank*. **`UNREACHED` rose by six and that is the task working** — the holes
existed before and were inside rules the run reported as covered.

**Outputs produced**
- `tools/deck/check.py` — eight `CLAUSES` entries; `CONJUNCTIONS_OWED` reduced to DS-230 with the
  reason beside it
- [T-298](T-298-decide-what-the-clause-sweep-owes-for-a-rule-the-clause-table-cannot-hold.md) — the
  sweep-membership decision DS-230 needs

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| `CONJUNCTIONS_OWED` is empty and `sweep_debt` reports 0 | **not met, and narrowed rather than dropped** | Eight of nine. DS-230 is `judge`, and `clausesForRulesNotOwned` fails the run on a clause row for a rule the ruleset does not own — see §3. `sweep_debt` reports 1, with no fault: the entry is consistent with `SWEPT` and now carries the reason it cannot be paid. [T-298](T-298-decide-what-the-clause-sweep-owes-for-a-rule-the-clause-table-cannot-hold.md) owns the decision |
| every new clause is decided by a named check or carries an excusal `closing_faults` accepts | met | `clause_account()['clauseExcusalFaults']` is empty; six excusals, kinds `work` ×3, `amendment` ×2, `look` ×1 |
| the `UNREACHED` count is stated before and after | met | 9 → 15, §3's table, read off `clause_account()` both times |
| `lint.py` and `check_all.py` green, run separately | met | In that order, never concurrently (`TOOLING.md` §1.2). `lint: all 5 passed`; `check_all: 42 ran, 2 skipped with a reason, 0 failed, 0 unclassified, 0 stale`. The full run was owed rather than `--docs`, because the change reaches `tools/deck/check.py` |

**Open questions** — §1's one question is answered in §3 and written into DS-218's own clause row,
not only here.

**Child fix tasks raised**
- [T-298](T-298-decide-what-the-clause-sweep-owes-for-a-rule-the-clause-table-cannot-hold.md) — the
  sweep records a conjunction for a rule the clause table is forbidden to hold

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → proposed | Raised by [T-244](T-244-the-gates-own-coverage-account.md) while closing `PR-43`. **The register's remedy was measured and its sizing refused**: it read *two rows, and then the sweep*, and running the sweep the dated sentence had stopped covering found **eleven** conjunctions among 24 unswept rules, not two. T-244 wrote the two named rows and the mechanism that makes the sweep impossible to lose again; these nine are the rest, held as a counted backlog printed on every run rather than written unreviewed at the end of a batch. **`PH3`**: not a defect an adopter met in the published `0.6.0`, so `CLAUDE.md`'s one condition for reopening `PH1` does not apply. |
| 2026-09-03 | proposed → done | Eight of the nine written; **18 clauses, 12 decided and 6 not**, and `UNREACHED` rose 9 → 15 because the holes were inside rules the run already reported as covered. §1's open question answered: DS-218's *reads with motion off* is a `look`, not a threshold. **The ninth was refused by the table's own guard** — DS-230 is `judge`, `ruleset.owned()` is `("auto", "render")`, and a clause row for it fails the run; it stays in `CONJUNCTIONS_OWED` with the reason beside it and [T-298](T-298-decide-what-the-clause-sweep-owes-for-a-rule-the-clause-table-cannot-hold.md) owns the exit. Found by attempting the row rather than by reading the guard. |
