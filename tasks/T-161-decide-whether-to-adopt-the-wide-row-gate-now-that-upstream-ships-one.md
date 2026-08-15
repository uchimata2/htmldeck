---
id: T-161
title: Decide whether to adopt the wide-row gate now that upstream ships one
type: decision
status: done
phase: review
parent: null
blocked_by: []
related: [T-139, T-160, T-157, T-163]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-15
updated: 2026-08-15
shipped_in: unreleased
deliverables: []
---

# T-161 — Decide whether to adopt the wide-row gate now that upstream ships one

## 1. Specify

**Outcome**
This project has a written answer to *does a table row wider than its header get gated here*, taken
against evidence rather than against the estimate that produced the first answer. The question was
settled once, in the negative, and **three things have changed since** — none of which existed when
the trade was made.

**Why this exists**
`O-T4` in [`../docs/upstream/taskmd.md`](../docs/upstream/taskmd.md) records this project declining
the gate: *a cell past the header is not a broken pointer, and a checker for two rows would outlive
the fault*. That was sound on the evidence then — **two rows, both noticed**, fixed by
[T-139](T-139-two-rows-in-brief-md-carry-a-cell-the-table-cannot-render.md).

What is new:

- **taskmd built it and it is a problem, not an advisory** — it moves the exit status, commit
  `d6623e7`, unreleased. Their reasoning: every advisory they print reports a *legal* state a project
  may mean, and text that renders nowhere is not a state anyone can mean. Our proposal for an advisory
  is recorded there as the rejected alternative.
- **Their instance was one row nobody had noticed, in a closed record, destroying evidence** for six
  days with `check` green — a materially different case from our two.
- **The obvious implementation is wrong, and they said how.** GFM splits a row into cells *before*
  parsing inline spans, so **a backtick does not protect a pipe**. A checker that blanks code spans
  first — which is what every other text check would do — goes silent on a row that is broken twice.

**The measurement, taken 2026-08-15 before this task existed**
The question *how red would our first run be* was answered directly, because the decision is not worth
arguing without it. A throwaway scanner, proven on a specimen written outside the repository:

| | |
| :--- | :--- |
| Files scanned | 307 |
| Rows wider than their header | **0** |
| Unescaped pipes inside a code span | **0** |
| Specimen, at the same moment | 2 wide and 1 span, fired |

**So the upgrade does not turn this tree red**, which is the opposite of what taskmd predicted, and the
reason is [T-139](T-139-two-rows-in-brief-md-carry-a-cell-the-table-cannot-render.md) already swept.
That removes the cost objection from the decision and leaves only the question of whether this project
wants its own instrument for a class upstream now gates for it.

**The scanner's own false positives are the part worth carrying.** It scored **3,150** code-span pipes
on the first run and the true count is 0 — a regex starting at any backtick reads a *closing* one as an
opener, so the cell boundary after a span looks like a pipe inside it. Two more followed: YAML front
matter read as a table row, which made the shipped task template the only defect in the tree, and a run
of three backticks in prose read as an open span. **Each was caught by reading the hits, not by the
specimen** — the specimen had a positive case for both checks and a negative case for only one, so the
span check was never tested for false alarms at all. That is a sharper statement than *prove the
scanner before you believe its zeros*: **a check with no negative case in its fixture is unproven in
the direction that produces noise**, and noise is what gets a gate switched off. Candidate lesson at
close.

**Scope**
- In: the decision, written down with its reasoning, whichever way it goes
- In: if the answer is yes, where it lives — `refcheck.py` already reads documents and resolves links,
  and is the only tool in the neighbourhood
- In: telling taskmd the measured result, since they predicted a non-zero first run for this project
  specifically
- Out: **pinning the taskmd version.** Their release cannot turn this tree red, so the option they
  offered is not needed here and buying it would cost the upgrades
- Out: re-litigating `O-T4`'s original trade. It was right on its evidence; this is new evidence

**Inputs**
- [`../docs/upstream/taskmd.md`](../docs/upstream/taskmd.md) `O-T4`, and the thread it points to
- [T-139](T-139-two-rows-in-brief-md-carry-a-cell-the-table-cannot-render.md) — the two rows, and why
  the tree is clean now
- [`../tools/docs/refcheck.py`](../tools/docs/refcheck.py) — the candidate home

**Acceptance criteria**
- [ ] The decision is written where a later session finds it without reading this task
- [ ] If **no**, the refusal names what would change it, so it is not re-asked from scratch a third time
- [ ] If **yes**, the checker has a fixture with a **negative case for every check it makes**, not only
      a positive one
- [ ] taskmd is told the measured first-run result against their prediction
- [ ] The measurement is reproducible — the scanner is thrown away, so whatever replaces it states how
      the number was got

**Open questions**
- **Is a gate worth building for a class that is now gated upstream anyway?** `taskmd check` runs inside
  `python tools/tasks/lint.py`, so once their release lands this project gets the rule for free on
  every task edit — but **only over the files `check` reads**, which is tasks and the documents it
  resolves, not `skills/` or `examples/`. **Recommend: no own checker, and record the coverage gap as
  the thing that would change it** — if a wide row ever appears in `skills/`, the answer flips. *The
  owner decides; this is the whole decision.*
  > **Corrected 2026-08-15 by [T-163](T-163-correct-the-coverage-claim-that-carried-the-wide-row-refusal.md).**
  > There is no coverage gap. `check` reads every Markdown document a clone would receive, both trees
  > included — taskmd's correction on the thread, reproduced here with a seeded probe in each. **The
  > answer this question produced is unchanged; the reason offered for it was false.** Left standing
  > rather than rewritten, because what a closed record said is part of what it decided.

## 2. Plan

**The owner answered the open question on 2026-08-15: no own checker.** So this task writes a refusal
down, rather than building anything. The work is entirely in making the refusal survive — a decision
recorded only in the task that took it gets re-asked, and this one has now been asked twice.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Put the refusal in [`../tools/docs/refcheck.py`](../tools/docs/refcheck.py)'s module docstring, with what would reverse it and the implementation trap | The decision where a session touching the checkers finds it, without this task |
| 2 | Tell taskmd the measured first-run result against their prediction, and that we are not building our own | The thread carries the negative they warned us about |
| 3 | Mint the fixture lesson §1 flagged as a candidate | **L-103** |
| 4 | Gates, commit, push | `lint`, `check_all`, one commit |

## 3. Implement

**Decisions & assumptions**
- **No own checker — the owner's ruling, 2026-08-15.** `taskmd check` runs inside
  `python tools/tasks/lint.py`, so once their release lands this repository gets the rule on every task
  edit for nothing. A second instrument for a class already gated is the
  checker-that-outlives-the-fault argument aimed at itself, which is the same argument `O-T4` used to
  decline it the first time — **still right, on entirely different evidence.**
- **The refusal went in a tool docstring, not a document** — 2026-08-15.
  [`../tools/docs/refcheck.py`](../tools/docs/refcheck.py) already carries the boundary between what
  taskmd's `check` covers and what this repository checks itself, including the last time upstream
  ruled and this file survived it. A second home for the same boundary is **L-13**.
- **The reversing condition is a coverage gap, stated as a trigger rather than a caveat** —
  2026-08-15. `check` reads tasks and the documents it resolves, not `skills/` or `examples/`. **The
  first wide row that appears there is the reason to build it**, and the docstring says so, so the
  third asking of this question starts from an answer.
  > **Wrong, and replaced 2026-08-15 by [T-163](T-163-correct-the-coverage-claim-that-carried-the-wide-row-refusal.md).**
  > The gap does not exist, so the trigger could never fire — which is the failure this decision was
  > written to prevent, one level up: a trigger nobody can trip reads as a permanent answer. The
  > docstring now names `python tools/tasks/lint.py` ceasing to run `taskmd check` instead, that being
  > the whole of this repository's cover for the class.
- **No register row was added for the scanner's false positives** — 2026-08-15. They are facts about
  a throwaway instrument written here, not observations about taskmd's tool, and the register is for
  the latter. They went in the thread, where they are useful, and in **L-103**, where they are ours.

**Outputs produced**
- [`../tools/docs/refcheck.py`](../tools/docs/refcheck.py) — the refusal, the reversing condition, the trap
- [`../docs/lessons/L-103.md`](../docs/lessons/L-103.md) — a check with no negative case in its fixture
- The reply on [`uchimata2/taskmd#1`](https://github.com/uchimata2/taskmd/issues/1)

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The decision is written where a later session finds it without reading this task | met | `refcheck.py`'s module docstring — the file that already owns the boundary between upstream's `check` and this repository's own, and the file anyone touching the checkers opens first. |
| If **no**, the refusal names what would change it | met, then void | The `skills/` and `examples/` coverage gap, written as a trigger: *the first wide row that appears there is the reason to build the narrow thing*. The question has been asked twice; the third asking starts from an answer rather than from the argument. **Corrected 2026-08-15 by [T-163](T-163-correct-the-coverage-claim-that-carried-the-wide-row-refusal.md): the gap does not exist, so this criterion was met by a condition that cannot occur.** The criterion is right and the artifact satisfying it was not; the docstring now names a trigger that can fire. |
| If **yes**, a fixture with a negative case for every check | n/a | The answer was no. The requirement outlived the branch as **L-103**, which is the general form and applies to every checker here rather than to the one not built. |
| taskmd is told the measured first-run result against their prediction | met | Posted, with the three false positives, since ours is the mirror of the trap they warned about — they said blanking code spans makes the rule silent; a naive span detector is deafening. |
| The measurement is reproducible | met | The scanner is thrown away as planned, so the record carries the method rather than the tool: cells split on unescaped pipes with code spans **not** protected, front matter skipped, fenced blocks skipped, backtick **runs** matched pairwise, escaped `\|` inside a span left alone. Anyone can rebuild it; **L-103** says what to prove about it first. |

**On closing a decision task with nothing built**
Every output here is prose, and the temptation with a `no` is to close it as a non-event. It is not
one: the cost objection that carried the first refusal — *a checker for two rows would outlive the
fault* — had been quietly destroyed by upstream shipping the rule, and the refusal now stands on a
completely different argument. **A decision that reaches the same answer by a new route is not the old
decision still holding**, and recording it as though it were would leave the next session defending a
reason that no longer applies.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-15 | (no change) | **This repository produced two instances of the defect, and no gate saw either.** Folding four closed rows into `../docs/RELEASE-PHASES.md` by script left a stray `\|` before each appended note, so two rows carried **three cells in a two-column table**. Found by counting pipes, fixed in the same session, and the tree is back to **0 wide** — so the measurement this refusal rests on still holds and **the recommendation is unchanged**. Recorded because the *cost* half of the argument moved: the refusal assumed the fault arrives one noticed row at a time, and a batch edit produces them silently and in pairs. The reversing condition is still the right one and still has not tripped — T-163 established that taskmd's gate is unreleased, so `taskmd check` would not have caught these either. **No task raised**: this row is evidence for the decision this task owns, not a new decision. |
| 2026-08-15 | record corrected, status unchanged | **The reversing condition this task shipped was false, and [T-163](T-163-correct-the-coverage-claim-that-carried-the-wide-row-refusal.md) replaced it the day after.** taskmd corrected the premise on the report thread — `check` reads every Markdown document a clone would receive, `skills/` and `examples/` included — and it was reproduced here with a seeded probe in each tree before being accepted. **The refusal is unchanged and stands on better ground than it was given.** Three places in this record stated the premise; each is annotated where it stands rather than rewritten. |
| 2026-08-15 | → done | **The owner ruled: no own checker.** The refusal is in `../tools/docs/refcheck.py`'s docstring with its reversing condition — the `skills/` and `examples/` coverage gap, written as a trigger so the third asking of this question starts from an answer. **The same verdict as `O-T4`'s, reached by a different argument**: the original reason was that a checker for two noticed rows would outlive the fault, and upstream shipping the rule destroyed that reasoning while leaving the answer standing. Recorded as a new decision rather than as the old one holding. The measurement went back to taskmd against their prediction, and the fixture finding is **L-103** — a check with a positive case and no negative case is unproven in the direction that produces noise, which is how a specimen passed while its scanner scored 3,150. |
| 2026-08-15 | → proposed | Raised from taskmd's second follow-up on the report thread: they built the gate this project declined, as a **problem rather than an advisory**, and warned that our first run would be non-zero. **It is zero — 307 files, 0 wide rows, 0 code-span pipes**, because T-139 already swept. Measured before the task existed, which is the honest record: the question was *does this affect us*, and a task to decide something that turned out not to apply would have been the wrong artifact. `s`, `decision`, `PH3`. |
