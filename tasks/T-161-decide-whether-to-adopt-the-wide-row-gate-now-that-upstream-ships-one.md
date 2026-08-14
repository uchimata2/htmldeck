---
id: T-161
title: Decide whether to adopt the wide-row gate now that upstream ships one
type: decision
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-139, T-160, T-157]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-15
updated: 2026-08-15
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

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <none yet>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-15 | → proposed | Raised from taskmd's second follow-up on the report thread: they built the gate this project declined, as a **problem rather than an advisory**, and warned that our first run would be non-zero. **It is zero — 307 files, 0 wide rows, 0 code-span pipes**, because T-139 already swept. Measured before the task existed, which is the honest record: the question was *does this affect us*, and a task to decide something that turned out not to apply would have been the wrong artifact. `s`, `decision`, `PH3`. |
