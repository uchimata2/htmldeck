---
id: T-283
title: Make DS-218 report no subject where it has none, rather than a pass
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-257, T-231]
work_package: PH1
owner: the project owner
business_value: high
effort: s
created: 2026-08-30
updated: 2026-08-30
deliverables: []
---

# T-283 - Make DS-218 report no subject where it has none, rather than a pass

## 1. Specify

**Outcome**
`check.py`'s `DS-218` row reports `NO SUBJECT` on a deck carrying no looping motion, the way
`DS-140` already does one line below it on the same absence. Today it reports `pass`, and the
condition is `len(data["infinite"]) == 0 or data["motionPersistent"]` - an `or` whose first term
short-circuits the whole test away.

**Measured, on the deck that shipped it** ([T-257](T-257-ds-218-passes-the-shipped-example-vacuously.md)
section 3). Delete the stop control from `portfolio-review` as it shipped in `0.6.0` and the row
prints `control reachable while motion runs: False - no control` and reports **pass**. The same
seed on the same deck once it carries one looping motion reports **FAIL**. So the gate could state
the control was absent and pass the deck in the same line, and only the deck's own lack of motion
was hiding it.

**Why this is not closed by T-257.** That task gave one deck a subject. Every deck an adopter
builds without a looping motion still gets the same unearned `pass`, and the report this came from
is an adopter's.

**Scope**
- In: the `DS-218` tuple in `tools/deck/audit.py`, and whatever `check.py` counts as a `NO SUBJECT`
  row rather than a passing one
- In: **the account.** `NO SUBJECT` is already a reported state with a home in the run's totals, so
  the change moves a row between two existing columns rather than inventing a third
- In: a negative fixture proving the row can reach all three states - `NO SUBJECT` with no looping
  motion, `pass` with one and a reachable control, `FAIL` with one and no control
- Out: `DS-218`'s rule row in `DESIGN-SYSTEM.md`. **The rule's force does not change** - it says
  what a looping deck owes, and a deck with no looping motion has always owed nothing. This is
  what the instrument says about that deck, not what the rule requires of it
- Out: the other rules in the same shape. `DS-140` is already correct and
  [T-231](T-231-two-packaging-checks-have-no-subject-at-all.md) holds the packaging gate's pair;
  a sweep for the rest is that task's or a later one's

**Inputs**
- [T-257](T-257-ds-218-passes-the-shipped-example-vacuously.md) section 3 - the seeded measurement,
  in both directions, and the row text each run printed
- **L-57**, the absent-subject class, and **T-051**, which raised `DS-140` out of exactly this shape
- the comment above the `DS-140` tuple in `tools/deck/audit.py`, which argues the case already:
  *a deck with no flow is legitimate and this is not a failure; it is the rule going undecided,
  which the account calls silent*

**Acceptance criteria**
- [ ] a deck with no looping motion reports `DS-218` as `NO SUBJECT`, and the run's account counts
      it where the other silent rows are counted
- [ ] the three states are each proved by a fixture, and the `FAIL` one fires for the reason it
      names (**L-125**)
- [ ] the five tracked decks are unaffected, or each change of state is explained
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None. The shape is settled by `DS-140`, which sits four lines away in the same list and already
  does this.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision - rationale - date>

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
| 2026-08-30 | -> proposed | Raised while closing [T-257](T-257-ds-218-passes-the-shipped-example-vacuously.md), whose seeded run printed the defect: `False - no control` beside `pass`. **`PH1`**: `check.py` ships in `0.6.0` and this is the instrument an adopter runs, which is `CLAUDE.md`'s one condition for reopening the phase. It is separated from `T-257` rather than absorbed because it changes a verdict for every deck the gate reads, which [`../docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) section 4 routes to a task. |
