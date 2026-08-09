---
id: T-066
title: Make the absent-subject rule a fixture instead of a sweep
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-051, T-065]
work_package: v0.1
owner: the project owner
business_value: critical
effort: m
created: 2026-08-10
updated: 2026-08-10
deliverables: []
---

# T-066 — Make the absent-subject rule a fixture instead of a sweep

## 1. Specify

**Outcome**
No verdict row can fail a deck for not containing the thing it judges, and **the gate proves that
about itself on every run** rather than a person proving it once with a script.

**Why this exists**
This is the third time the same defect has been found, each time by someone tripping over it:

| | What was found | How |
| :--- | :--- | :--- |
| T-051 | Rules **passing** on an absent subject | A fixture built to be missing things |
| T-065 | Four rules **failing** on an absent subject | An outside project's deck |
| here | **Three more**, one of them still failing that project after v0.1.2 shipped | The same project re-running the fix |

**T-065 marked its sweep criterion met, and it was not.** The sweep was a one-off script that
segmented each verdict row at the first `),`, so any row whose expression sat on a later line was
truncated before it was read. It reported one candidate. Re-run with balanced-paren parsing it
reports five. That criterion is now recorded as `not met` on T-065.

**The three that were missed**

| Rule | Expression | With nothing found |
| :--- | :--- | :--- |
| DS-160 | `not thirdTier and data.get("panelCount", 0) > 0` | **False** — identical clause to DS-164, which T-065 called the sharpest find |
| DS-113 | `not unusedSymbols and data.get("symbolCount", 0) > 0` | **False** — a deck using no icons fails a rule about *unused* icons |
| DS-143 | `risen > 0 and risenHidden == 0` | **False** — and invisible to the current fixture, see below |

**The fixture has two holes, and they are the actual defect**

1. **It only asks which rows PASS on an absent subject.** `ABSENCE_IS_A_PASS` is a declared table
   with a reason per entry, enforced every run. There is no mirror, so a row that *fails* on an
   absent subject is checked by nobody. That asymmetry is why T-051 could convert three rows and
   leave four beside them, and why T-065 could convert four and leave three.
2. **It evaluates `render_verdicts` and `split_verdicts` only.** `reduced_verdicts` produces rows
   too, and DS-143 is one of them, so an entire family is outside the discipline.

Against a measurement in which nothing was found, **eight rows currently fail**: DS-070, DS-075,
DS-076, DS-081, DS-113, DS-135, DS-160, DS-217. Some of those are correct — a deck with no reflow
view genuinely fails DS-070, and a deck with no slides genuinely fails DS-081. **Which is which is
exactly what a declared table is for**, and none of it is written down today.

**Scope**
- In: `ABSENCE_IS_A_FAIL`, mirroring `ABSENCE_IS_A_PASS`: every row that fails on the
  nothing-was-found measurement is declared with its shape and its reason, and an undeclared one
  fails the self-test.
- In: extending the fixture to **every** verdict producer, `reduced_verdicts` included.
- In: converting whichever rows the table shows to be absent-subject cases rather than real
  verdicts. DS-160, DS-113 and DS-143 are already known.
- In: a check that the two tables cannot both claim a rule.
- Out: the `undecided` bucket in `check.py`, which T-065 settled and which is right.
- Out: the reporting project's remaining findings on its own deck.

**Acceptance criteria**
- [ ] Every verdict row that fails on an absent subject is declared with a reason, or converted
- [ ] `reduced_verdicts` is inside the fixture, and adding a producer that is not fails the run
- [ ] DS-160, DS-113 and DS-143 are undecided on a deck lacking their subject
- [ ] The reference deck's verdicts are unchanged, checked by diff
- [ ] The seeded-defect deck still fails everything it is supposed to
- [ ] A declaration that outlives its row is reported, as `ABSENCE_IS_A_PASS` already does
- [ ] **The sweep is deleted.** If a hand-run script is still needed, this task has not finished

**Open questions**
- **Is `symbolCount > 0` in DS-113 a real requirement?** A deck with no icons may be a defect under
  a different rule, but DS-113 is about *unused* symbols and cannot be violated by a deck with none.
  Same question shape as DS-164's, which was answered by deleting the clause.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Extend the fixture to every verdict producer and print what fails on nothing-found | The list |
| 2 | Classify all eight, plus whatever `reduced_verdicts` adds, into declared-fail or convert | The table, in §3 |
| 3 | Write `ABSENCE_IS_A_FAIL` and make an undeclared failure fail the self-test | The edited `audit.py` |
| 4 | Convert the rows that are absent-subject cases | The edited rows |
| 5 | Diff the reference deck; run the seeded-defect deck; delete the sweep | Both runs |
| 6 | Patch release, and tell the reporting project which version carries it | The tag |

## 3. Implement

**Decisions & assumptions**
- <recorded as the work is done>

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
| 2026-08-10 | → proposed | Raised on the third finding of one defect, and the third is the one that matters: **v0.1.2 shipped claiming a complete sweep and the sweep was broken**, so DS-160 kept failing the very project whose report produced the fix. [T-065](T-065-four-rules-still-fail-a-deck-for-not-having-their-subject.md) §3 recorded a deliberate decision not to build the general table because it was *"a bigger change than a patch release should carry"*. That was wrong, and it is the whole reason this task exists: **a hand-run script is not a gate**, which is this repository's own position turned on itself. `v0.1` because the published gate still fails legitimate decks. |
