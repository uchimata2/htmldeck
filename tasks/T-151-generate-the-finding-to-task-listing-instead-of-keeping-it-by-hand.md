---
id: T-151
title: Generate the finding-to-task listing instead of keeping it by hand
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-130, T-137]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-14
updated: 2026-08-14
deliverables: []
---

# T-151 — Generate the finding-to-task listing instead of keeping it by hand

## 1. Specify

**Outcome**
One command answers **which finding is which task, and what state is it in**, in an output small
enough to read whole — and the tables that show the same facts in prose documents are generated from
that source or checked against it, so they cannot quietly disagree.

**Raised from the cost of doing it by hand, 2026-08-14.** Assembling that picture once meant reading
[`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6's ranking table, its §6.1 finding
statements, the `any`-marked statements in
[`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
§8, the §9 candidate table, the three documents under [`../docs/upstream/`](../docs/upstream), and
thirteen task files — and the result was a fourteenth copy of facts that already existed, correct on
the day and stale by the next closure.

**The same shape has a second instance in this repository, and it is worse.** The execution-order
table in [`../docs/BRIEF.md`](../docs/BRIEF.md) numbers its rows, and its own notes cite those
numbers — *after 3 and 4*, *needs 8 and 9* — so **every insertion is a hand renumbering pass across
the table and the prose around it**, owed every time and stated in the document as owed. Three passes
were done on 2026-08-13 and 2026-08-14 alone. Whether this task covers that too is the scope question
below.

**This is the local half of a requirement now written into
[T-137](T-137-package-the-context-economy-method-as-a-skill.md)**, which packages the audit method as
a skill and is **blocked on T-136**. The order is deliberate: everything portable in this method was
proven here first ([`R8`](../docs/research/R8-context-economy-for-coding-agents.md) §6), and a
generator designed in the abstract for other people's repositories is the one thing this project has
no evidence for. What is learned here is what T-137 packages.

**Scope**
- In: the single structured home for each finding's key fields — `id`, one-line title, subject or
  owner, band, effort, the task it became, that task's status.
- In: the command, and its output size as an acceptance criterion rather than an afterthought.
- In: **the check that fails in both directions** (**L-74**) — a finding whose task closed and still
  reads open, and a task naming a finding that does not exist, both stop the run.
- In: deciding whether the finding→task link lives in task front matter, which makes
  [`../.taskmd/config.md`](../.taskmd/config.md) the file that changes, or in a register file the
  tasks are matched against.
- Out: the findings' prose. The argument in a row is why the row survives a re-read; **nothing here
  compresses it.**
- Out: mirroring the board. A table of task ids outside the tracker's markers is a second board and
  the `DUPLICATE INDEX` advisory is right to say so — this keys on findings and *references* tasks.
- Out: T-137's packaging. This produces the evidence; that task carries it outward.

**Inputs**
- [T-137](T-137-package-the-context-economy-method-as-a-skill.md) §1 — the five criteria the skill
  owes, which this task is the local proof of
- [`../.taskmd/config.md`](../.taskmd/config.md) — the schema, which outranks any prose about the
  fields, and the file a front-matter answer would change
- `tools/tasks/query.py` — the precedent for *ask the board, never read it*: 94 bytes to answer *what
  next*
- `tools/docs/figures.py` — the precedent for a checker that binds a written figure to what produced
  it

**What specifying must settle**
- Front-matter field or register file. A field makes the link inseparable from the task and touches
  the schema; a register file keeps the schema still and adds a document that can drift from the
  tasks — which is the failure this task exists to remove.
- Whether the execution order's row numbers are in scope, or a second task. They are the same defect
  and a different data shape.
- What *derived* means for a document that must also carry an argument: generated block with markers,
  or hand-written prose with a checker that fails on disagreement.

**Acceptance criteria**
- Written at `specify`, and the output-size criterion is not optional: a listing nobody can read whole
  has moved the cost rather than removed it.

**Open questions**
- **Is `s` right?** It is `s` if the link goes in front matter and `taskmd check` tolerates the field;
  it is larger if the schema resists and the register file has to be reconciled against the tasks.
  — the implementer, at `specify`, after reading the schema rather than guessing at it.

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
| 2026-08-14 | → proposed | Raised at the owner's direction after a hand-assembled finding-to-task listing cost six sources and produced a copy that was stale on arrival. **Not an audit finding** — `CE-nn` is closed at thirteen and this is new capability, so it takes an ordinary task id and no finding number. It is the local proof of a requirement written the same day into T-137, which is blocked on T-136; building it here first is this project's own rule about local precedent, not impatience. |
