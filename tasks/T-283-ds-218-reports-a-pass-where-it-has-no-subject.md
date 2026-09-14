---
id: T-283
title: Make DS-218 name the absence when it passes a deck with no looping motion
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-257, T-231]
work_package: PH1
shipped_in: unreleased
owner: the project owner
business_value: high
effort: s
created: 2026-08-30
updated: 2026-09-13
deliverables: [tools/deck/audit.py]
---

# T-283 - Make DS-218 name the absence when it passes a deck with no looping motion

## 1. Specify

**Outcome**
`check.py`'s `DS-218` row reports `NO SUBJECT` on a deck carrying no looping motion, the way
`DS-140` already does one line below it on the same absence. Today it reports `pass`, and the
condition is `len(data["infinite"]) == 0 or data["motionPersistent"]` - an `or` whose first term
short-circuits the whole test away.

**Restated 2026-09-13 on the owner's ruling**, recorded under open questions; the paragraph above
is the original outcome. `DS-218` stays a declared conditional pass on a deck with no looping
motion, and the row names that absence rather than printing the reachability reading, so a pass
no longer sits beside `False - no control`.

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
  *Out since 2026-09-13: the pass stays, so no row moves.*
- In: a negative fixture proving the row can reach all three states - `NO SUBJECT` with no looping
  motion, `pass` with one and a reachable control, `FAIL` with one and no control
  *Since 2026-09-13 the first of the three is a pass whose row names the absence.*
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
- [ ] a deck with no looping motion reports `DS-218` as a pass whose row names that absence, and a
      deck with looping motion keeps the reachability reading. *Restated 2026-09-13 and agreed by the
      owner; the original read: a deck with no looping motion reports `DS-218` as `NO SUBJECT`, and
      the run's account counts it where the other silent rows are counted*
- [ ] the three states are each proved by a fixture, and the `FAIL` one fires for the reason it
      names (**L-125**)
- [ ] the five tracked decks are unaffected, or each change of state is explained
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None. The shape is settled by `DS-140`, which sits four lines away in the same list and already
  does this.
- **Raised 2026-09-13, before plan. It changes the outcome, so the owner answers.** The premise
  above does not hold. `DS-140` is a universal (*every `Current` is dashed*), so `None` on no flow
  is right for it. `DS-218` is a conditional (*if motion loops, a control is reachable*), and
  `ABSENCE_IS_A_PASS` in `tools/deck/audit.py` rules in writing that a conditional with no
  subject passes: *vacuous truth is the right answer*. Its self-test enforces that, and `DS-143`'s
  flow-dash row and `DS-219` are declared the same way, so criterion 1 would convert one
  conditional of three. **Recommended:** keep the declared pass, and make the row name the absence
  (*no looping motion - no control owed*) instead of printing `False - no control` beside `pass`.
  That line is the contradiction T-257's seed printed, and the wording is what the adopter's record
  `018` asked about.
  **Answered by the owner 2026-09-13: keep the pass and fix the row.** Criterion 1 is restated to
  match.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Give the `DS-218` row a second text for a deck with no looping motion; the verdict expression is untouched | the row in `render_verdicts`, `tools/deck/audit.py` |
| 2 | Hold the row to three states in `self_test`, beside `DS-140`'s: a pass that names the absence, a pass on a reachable control, a failure on an unreachable one - the last two differ in `motionPersistent` alone | the fixture in `self_test`, `tools/deck/audit.py` |
| 3 | Seed the defect back twice - the old reading on a vacuous pass, and a verdict that ignores `motionPersistent` - and watch the self-test refuse each, then restore | the measurement, in section 3 |
| 4 | `check.py --json` on the five tracked decks, reading each `DS-218` row and verdict | a table in section 3 |
| 5 | `lint.py`, then `check_all.py`, run separately | both results, in section 3 |

## 3. Implement

**Decisions & assumptions**
- **The row keeps its reachability text wherever motion loops, and gains a second only for the
  vacuous pass** - 2026-09-13. Rejected: `NO SUBJECT`, which the owner ruled out by keeping the
  declared conditional; one text for both cases, which is what printed `False - no control` beside a
  pass; and editing the `ABSENCE_IS_A_PASS` entry, whose statement - no looping motion, no
  obligation - is exactly what the ruling kept.
- **The verdict reads `motionPersistent` before the looping count, and the vacuous text carries
  `motionControl` and `motionReach`** - 2026-09-13. The first version failed `self_test` with
  *motionPersistent, motionReach are modelled and no row reads them*: the unread-key check runs on
  the empty measurement, where the old order short-circuited past `motionPersistent` and the new
  text read neither. The verdict is unchanged for every input, since `motionPersistent` is a bool.
  Rejected: evaluating both texts only to satisfy the check, which hides which reading the row
  prints.

**Outputs produced**
- `tools/deck/audit.py` - the `DS-218` row in `render_verdicts`, and its three-state fixture in `self_test`

**Evidence** - 2026-09-13
- `self_test` on the fix: `SELF-TEST OK`. The first version was red on the unread-key check, which is
  the second decision above.
- Seeded back, each seed refused for the state it breaks; `audit.py` then restored byte-identical and
  `SELF-TEST OK` again:

| Seed | Self-test |
| :--- | :--- |
| the vacuous branch prints the reachability reading (`if True else`) | `FAILED: DS-218 does not report a vacuous pass that names its absence - it gave True on 'control reachable while motion runs: False - not measured ...'` |
| the verdict ignores `motionPersistent` (`or True`) | `FAILED: DS-218 does not report a failure on an unreachable control - it gave True on 'control reachable while motion runs: False - not measured ...'` |

- `check.py --json` on each tracked file. Every one reports `DS-218` as a pass with the reachability
  reading, so no deck's state moved:

| File | Looping | `DS-218` |
| :--- | ---: | :--- |
| `examples/reference-deck.html` | 1 | `control reachable while motion runs: True - one click inside #moreMenu, opened by a persistent keyboard-operable button` - pass |
| `examples/sort-window/sort-window.html` | 1 | the same reading - pass |
| `examples/measure-first/measure-first.html` | 3 | the same reading - pass |
| `examples/portfolio-review/portfolio-review.html` | 1 | the same reading - pass |
| `examples/reference-deck-seeded-defects.html` | 1 | the same reading - pass; the run exits 1 on the fixture's seeded defects, which is its purpose |

- **The new text on a real render.** None of the five has no looping motion, so the vacuous branch
  was rendered on a scratch copy of the reference deck with its one `infinite` replaced by `1`:
  `no looping motion in this deck - no stop control owed (present: True - one click inside #moreMenu,
  opened by a persistent keyboard-operable button)` - pass. The copy is not kept.
- The other two declared conditionals already name their absence on a vacuous pass - `DS-143`
  prints `NO FLOW DIAGRAM IN THIS DECK`, `DS-219` its denominator - so `DS-218` was the only one
  printing a reading of `False` beside a pass.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| a deck with no looping motion reports `DS-218` as a pass whose row names that absence, and a deck with looping motion keeps the reachability reading *(restated with the owner)* | met | The scratch copy with no looping motion rendered `no looping motion in this deck - no stop control owed (...)` and passed; the five tracked files, all looping, print the reachability reading. `self_test` holds both states |
| the three states are each proved by a fixture, and the `FAIL` one fires for the reason it names (**L-125**) | met | A vacuous pass, a pass and a failure; the last two differ in `motionPersistent` alone. Seeded back twice, and each seed was refused for the state it breaks - section 3 |
| the five tracked decks are unaffected, or each change of state is explained | met | All five pass on the branch this task did not change, because each has looping motion (1, 1, 3, 1, 1). The fifth is the blindness fixture rather than a deck - `check_all.py` lists it under `NOT_A_DECK` - and was checked all the same |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | met | lint: all 5 passed. check_all: 42 ran, 2 skipped with a reason, 0 failed, 0 unclassified, 0 stale, 195 s - one after the other on the tree with section 3 written |

**Child fix tasks raised**
- none. The other two declared conditionals already name their absence on a vacuous pass (section 3), so there is no sweep to raise

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-30 | -> proposed | Raised while closing [T-257](T-257-ds-218-passes-the-shipped-example-vacuously.md), whose seeded run printed the defect: `False - no control` beside `pass`. **`PH1`**: `check.py` ships in `0.6.0` and this is the instrument an adopter runs, which is `CLAUDE.md`'s one condition for reopening the phase. It is separated from `T-257` rather than absorbed because it changes a verdict for every deck the gate reads, which [`../docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) section 4 routes to a task. |
| 2026-09-13 | (no change) | Specify reopened before plan: criterion 1 conflicts with `ABSENCE_IS_A_PASS`, which declares `DS-218` a conditional that passes on an absent subject. The question and a recommendation are in section 1. Still `proposed` at `specify` until the owner answers. |
| 2026-09-13 | -> specified | The owner answered: keep the declared pass and make the row name the absence. Criterion 1 restated beside its original, the scope annotated, the title changed to match, and `deliverables` names `tools/deck/audit.py`. |
| 2026-09-13 | -> planned | Five steps. The shape decision and its three rejected alternatives are in section 3. |
| 2026-09-13 | -> in_progress | Steps 1 and 2 written in one edit; step 3 run straight after. |
| 2026-09-13 | -> done | Four criteria met, the first as restated with the owner. No look owed: the change is a row of gate text and no deck changed. No lesson: the quantifier line the original spec missed is already `ABSENCE_IS_A_PASS`'s header, and its self-test would have refused the original remedy as a stale declaration. `shipped_in: unreleased` - a `PH1` fix reaches adopters at the next release. |
