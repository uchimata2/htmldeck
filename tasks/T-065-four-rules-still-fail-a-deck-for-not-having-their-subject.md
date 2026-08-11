---
id: T-065
title: Four rules still fail a deck for not having their subject
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-051, T-064]
work_package: PH1
shipped_in: 0.1.2
owner: the project owner
business_value: critical
effort: s
created: 2026-08-10
updated: 2026-08-12
deliverables:
  - tools/deck/audit.py
  - tools/deck/check.py
---

# T-065 — Four rules still fail a deck for not having their subject

## 1. Specify

**Outcome**
A deck specified without disclosures can pass the gate. Today it cannot, and the reason is that four
rules read *"this deck has no disclosure controls"* as *"this deck's disclosure controls are broken"*.

**The report**
From another project, 2026-08-10, building a three-slide proof deck with **zero disclosures, decided
in its foundation spec before any HTML existed**. `check.py` returned 11 failures, four of which the
reporter identified as the gate having no subject: DS-130, DS-164, DS-166, DS-160. Their words:
*"`0 of 0 FAIL` is the instrument reporting an empty set."*

**They were right, and it is narrower and worse than they thought.** Evaluated against an absent
subject, the verdict expressions in `audit.py` give:

| Rule | Expression | With no disclosures |
| :--- | :--- | :--- |
| DS-130 | `data.get("currentDiscReachable") is True` | **False** |
| DS-164 | `not unlabelled and data.get("discControls", 0) > 0` | **False** |
| DS-166 | `arrowAdvancesClosed is True and toggleDoesNotAdvance is True` | **False** |
| DS-146 | `data.get("playedSurvivesReturn") is True` | **False** |

Against the three rules **in the same function** that [T-051](T-051-a-check-with-no-subject-must-not-report-a-pass.md)
already corrected:

| Rule | Expression | With no disclosures |
| :--- | :--- | :--- |
| DS-168 | `None if smallestTarget is None else ...` | `None` — undecided |
| DS-228 | `None if panelsOpenAfterTwo is None else ...` | `None` — undecided |
| DS-138 | `None if panelBelowControl is None else ...` | `None` — undecided |

The probe emits those keys only inside `if (btns.length)`, so absence is *expected* and already has a
representation. **T-051 built the third state and converted three rules to it; four adjacent ones in
the same list were never converted**, and `check.py` handles `None` correctly the moment it gets one.

**DS-164 is the sharpest, because its failure is written as a requirement.** `discControls > 0` says
in code that a conforming deck **must contain at least one disclosure control**. Nothing in
`DESIGN-SYSTEM.md` says that; DS-162's split test treats tier two as a judgement about a particular
slide. So the gate is enforcing a rule the ruleset does not state, which is the failure the coverage
account exists to make impossible.

**Why this matters beyond one reporter**
A deck without progressive disclosure is a legitimate design, and CLAUDE.md's position is that
**a check which forbids a design choice is a defect in the check**. Worse, the failures are
indistinguishable in the output from real ones, so the reporter had to reason about four rules by
hand to find out their deck was fine. That is the cost L-44 describes, paid in the other direction.

**Scope**
- In: DS-130, DS-164, DS-166, DS-146, converted to return `None` when the subject is absent.
- In: **a sweep of every verdict row in `audit.py` for the same shape**, since four were missed once
  already and the reporter found them by accident rather than by a check.
- In: a fixture per converted rule that **fails before the fix** (**L-04**), and the seeded-defect
  deck must still fail all of them when disclosures *are* present and broken.
- In: whether DS-160 belongs in this set — the reporter named it, and the sweep decides.
- Out: DS-081 (`slides: 3`), DS-091, DS-075, DS-076, DS-064, which the reporter identified as
  genuine findings about their deck. DS-081 on a three-slide deck may still be worth a look, but it
  is a different question and gets its own task if so.
- Out: changing what `check.py` does with `None`. It is already right.

**Acceptance criteria**
- [ ] A deck with no disclosure controls is **undecided** on all four rules, not failing
- [ ] Those rules still **fail** a deck whose disclosures are genuinely broken, proven on the
      seeded-defect deck
- [ ] The account reports them under `silentNoSubject`, so coverage does not silently drain
- [ ] Every other verdict row in `audit.py` has been checked for the same shape, with the result
      recorded whether or not it found anything
- [ ] The reference deck's verdicts are unchanged, checked by diffing a run before and after

**Open questions**
- **Does a subjectless rule leave the run red?** It currently lands in `silent`, which is a coverage
  fault, so the run still fails — correctly, since coverage is a claim. But then a legitimately
  disclosure-free deck can never get a green run, which is the reporter's problem restated one level
  up. This is the real decision in the task and belongs to the owner.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Settle the open question above, since it decides whether this is a four-line fix or a change to the account | The decision, in §3 |
| 2 | Fixtures for the four rules, absent-subject and broken-subject, failing first | The failing run |
| 3 | Convert the four expressions | The edited `audit.py` |
| 4 | Sweep every other verdict row for the same shape and record the result either way | The sweep, in §3 |
| 5 | Diff the reference deck's verdicts before and after; run the seeded-defect deck | Both runs |

## 3. Implement

**Decisions & assumptions**

- **The open question is answered: `undecided` is its own bucket and does not fail the run —
  2026-08-10, owner's call, on this recommendation.** The code's fear of a forgiving bucket that
  coverage drains into is real but does not reach here, and the reason is structural: **a rule enters
  `undecided` only by its check executing and returning `None`.** A rule with no check never produces
  a row, so it still falls to `silent` and still fails. You cannot arrive in the new bucket by
  neglect. The deeper argument is that coverage is a claim about the **gate**, not about one deck: a
  check that ran and found nothing has full coverage, and tying the coverage verdict to whether this
  deck happens to use disclosures made the account report on the wrong subject.

- **No threshold on how many rules may go undecided — 2026-08-10.** A deck could in principle dodge
  the ruleset by omitting features. The answer is not a number: **L-51** settles that when meaning
  rather than quantity separates two cases, an invented threshold is worse than none. The count and
  the rule IDs print on every run, so it is visible, and judging it is the judgement half's job.

- **DS-164's `> 0` was a rule the ruleset does not contain.** `not unlabelled and discControls > 0`
  required a conforming deck to **have** a disclosure control. `DESIGN-SYSTEM.md` says no such thing.
  That clause is gone, not merely guarded: with no controls the rule is undecided, with controls it
  checks their labels.

- **The sweep found two more candidates and cleared both, with the reason.** DS-070 (`docOn`) and
  DS-135 (`titleCarriesSlide`) have the same `is True` shape, but the probe emits both keys
  **unconditionally** as plain booleans, so `False` there is a real verdict on a real measurement
  rather than an absent subject. Recorded because the criterion asked for the result either way.

- **A general `ABSENCE_IS_A_FAIL` table was considered and not built — 2026-08-10.** `audit.py`
  already has that discipline in the pass direction, and the mirror would need to separate rows
  reading `ALWAYS_MEASURED` keys from rows reading conditional ones, which is a bigger change than a
  patch release should carry. What went in instead is a direct assertion over the seven disclosure
  rows, which is provable and fails without the fix. **The asymmetry of that fixture is why this
  defect survived T-051**, and that is worth someone's time later rather than now.

**Outputs produced**
- `tools/deck/audit.py` (four rules, and the fixture)
- `tools/deck/check.py` (the account split)

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A deck with no disclosure controls is undecided, not failing, on all four | **met** | Asserted directly in `audit.self_test()` over DS-130, DS-164, DS-166, DS-146, plus T-051's three as regression guards |
| They still fail a deck whose disclosures are genuinely broken | **met** | Seeded-defect deck still fails 4: DS-035, DS-075, DS-141, DS-142. Reference deck still `0 failure(s)` with an unchanged 113/81/0/4/28 account |
| The account reports them so coverage cannot drain | **met** | New `undecided, no subject` line prints the count and IDs every run, and the partition still sums to owned |
| Every other verdict row checked for the same shape | **NOT MET** | **Corrected 2026-08-10.** The sweep was a one-off script and it under-reported: it segmented rows at the first `),`, so every multi-line verdict was truncated before its expression was read. Re-run with balanced-paren parsing it finds **five** candidates, not one. **DS-160 is a fifth instance of this defect** and was reported still failing by the same project after v0.1.2 shipped. Carried to [T-066](T-066-make-the-absent-subject-rule-a-fixture-instead-of-a-sweep.md) |
| Reference deck verdicts unchanged | **met** | `113 / 81 / 0 / 4 / 28`, `undecided 0`, `SILENT 0`, partition holds |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-10 | (no change) | **A second correction, and this one is to a clearance rather than to a miss.** §3 records that the sweep *"found two more candidates and cleared both"* — DS-070 and DS-135 — on the ground that the probe emits `docOn` and `titleCarriesSlide` **unconditionally as plain booleans**. Measured under [T-066](T-066-make-the-absent-subject-rule-a-fixture-instead-of-a-sweep.md): that is true of neither. `out.titleCarriesSlide` is assigned **inside `if (btns.length)`**, so a deck with no disclosure controls never has DS-135 measured and the row reports `False` — the same defect this task existed to remove, cleared by name. `out.docOn` sits inside `if (doc)`, which happens to leave DS-070 correct, but for the reason that a reflow view is required rather than for the reason given. The same false premise is written into `audit.self_test`'s comment, where it also claims both rows read `ALWAYS_MEASURED` keys; neither key is in it. **A sweep that clears a row is making the same size of claim as one that converts it**, and this one was not checked either. Both are T-066's to fix. |
| 2026-08-10 | (no change) | **One criterion is downgraded to `not met` after the fact, and the reason matters more than the miss.** The sweep this task relied on was a throwaway script that cut each verdict row at the first `),`, so any row whose expression sat on a later line was never examined. **DS-160 carries the identical `panelCount > 0` clause to DS-164** and was left in, which the reporting project found by re-running v0.1.2 and seeing it still fail. DS-113 has the same shape again, and DS-143 is invisible to the existing fixture entirely because it comes from `reduced_verdicts`, which that fixture never evaluates. **The deferral recorded in §3 - that a general `ABSENCE_IS_A_FAIL` table was 'a bigger change than a patch release should carry' - is what let three more through, so it was the wrong call and is reversed in [T-066](T-066-make-the-absent-subject-rule-a-fixture-instead-of-a-sweep.md).** A hand-run sweep is not a gate, which is this repository's own position applied to itself. |
| 2026-08-10 | → done | **Four rules converted, and the account gained the bucket they belong in.** The owner took the open question on the recommendation that `undecided` is not a coverage fault: a rule reaches it only by its check running, so nothing drains there by neglect, and coverage is a claim about the gate rather than about one deck. **DS-164's `discControls > 0` was the sharpest find** - it required a conforming deck to contain a disclosure, which the ruleset nowhere states. The sweep cleared DS-070 and DS-135 with a reason. The new fixture was shown to fail first by reverting one rule. What is left for later, written down rather than fixed quietly: `audit.py`'s absent-subject discipline still only runs in the pass direction, and that asymmetry is why T-051 could convert three rules and leave four beside them. |
| 2026-08-10 | → proposed | Reported from another project and **reproduced by evaluating the expressions directly** rather than by rebuilding their deck. The report said four rules were reporting an empty set as a failure; it is four, they are named, and three rules **in the same list** were already converted by [T-051](T-051-a-check-with-no-subject-must-not-report-a-pass.md), which built the undecided state and did not finish applying it. **DS-164 is the one to read first**: its expression requires `discControls > 0`, which enforces in code a rule the ruleset never states, namely that a conforming deck must contain a disclosure. `PH1` because the published gate fails a legitimate deck. |
