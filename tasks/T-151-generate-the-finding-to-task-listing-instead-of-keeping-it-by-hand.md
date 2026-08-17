---
id: T-151
title: Generate the finding-to-task listing instead of keeping it by hand
type: deliverable
status: done
phase: review
parent: null
blocked_by: []
related: [T-130, T-137]
work_package: PH3
shipped_in: 0.3.0
owner: the project owner
business_value: medium
effort: s
created: 2026-08-14
updated: 2026-08-14
deliverables:
  - tools/docs/findings.py
  - tasks/TOOLING.md
  - docs/RELEASE-PHASES.md
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
every task file naming a finding — and the result was one more copy of facts that already existed,
correct on the day and stale by the next closure. **Measured 2026-08-14: 325,695 bytes across those
six sources**, of which 268,780 is the 18 task files that name a `CE-nn`.

**The same shape has a second instance in this repository, and it is worse.** The execution-order
table in [`../docs/RELEASE-PHASES.md`](../docs/RELEASE-PHASES.md) numbers its rows, and its own notes
cite those numbers — *after 3 and 4*, *needs 8 and 9* — so **every insertion is a hand renumbering
pass across the table and the prose around it**, owed every time and stated in the document as owed.
Three passes were done on 2026-08-13 and 2026-08-14 alone. Whether this task covers that too is the
scope question below. *This paragraph named `BRIEF.md` until 2026-08-14; `CE-05` had moved the section
out the same day this task was raised, which is the defect class writing another instance of itself.*

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

### 1a. What specifying settled — 2026-08-14

**The link goes in task front matter, as `finding:`, and there is no register file.**
[`../.taskmd/config.md`](../.taskmd/config.md) *Format* says a task field the schema does not name is
**carried, never interpreted**, and `shipped_in` is that rule already running in this repository: it
is not in *Vocabularies*, it is never validated, and it shows on the board only because
`index_columns` names it. `finding:` is the same shape, so the schema does not resist and no probe was
needed to learn it. **`finding` is added to `context_fields`** so a session reading one task sees
which finding it serves; that is a one-line config edit, not a schema change.

**A register file was rejected on the task's own argument.** It would be a second home for facts the
§6 table already holds, free to drift from it — the failure this task exists to remove, re-created by
its own remedy.

**The findings register is [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6's ranking table,
parsed where it stands.** It already carries every field the listing owes — id, family, statement,
gain, effort, risk, where it is stated — and its **rank cell is the structural state marker**: a
struck-through rank (`~~10~~`) is a closed finding, a bare one is open. Nothing is added to that
document and nothing is compressed in it.

**Derived means a command, and the documents are *checked*, not generated.** Both tables involved
carry a per-row argument that is the reason the row survives a re-read — §6's *What* cell and the
execution order's third cell — so a generated block would put a marker fence around prose a person
edits, and the generator would own writing that is not derivable. `tools/docs/figures.py` is the
precedent this follows: the figure stays hand-written where a reader needs it, and a checker fails
when it stops matching what produced it.

**The execution order is in scope, and its fix is two-part.** The renumbering pass is expensive
because of the *notes*, not the numbers: five of them cite positions (*after 3 and 4*, *needs 8 and
9*, *10–12 are rework*, *after 7*, *ground 18–21*), so an insertion cascades out of the table into the
prose. **The notes are rewritten to cite task ids**, which removes the cascade at its source; the
checker then asserts the number column is a consecutive `1..n` over the open rows, which catches a
botched renumbering. No generated block there either, for the same reason.

**A per-item band is declared in the table rather than known.** `CE-04` is banded `xs` **each** and
its row is closed while [T-152](T-152-give-look-at-the-rendered-deck-one-operative-home.md) is open —
a state a naive *all its tasks are closed* rule would fail, and the one
[`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §9 says nothing in the table marks. So **an
Effort cell ending in `each` declares the band per-item**, and for those findings a closed row with
open tasks is reported rather than failed. That turns §9's prose observation into something a reader
and a program both see, which is the finding's own shape applied to the finding table.

**Scope**
- In: the single structured home for each finding's key fields — `id`, one-line title, subject or
  owner, band, effort, the task it became, that task's status.
- In: the command, and its output size as an acceptance criterion rather than an afterthought.
- In: **the check that fails in both directions** (**L-74**) — a finding whose task closed and still
  reads open, and a task naming a finding that does not exist, both stop the run.
- In: deciding whether the finding→task link lives in task front matter, which makes
  [`../.taskmd/config.md`](../.taskmd/config.md) the file that changes, or in a register file the
  tasks are matched against. **Settled in §1a: front matter.**
- In: the execution order's row numbers, per §1a — the note rewrite and the consecutive-`1..n` check.
- Out: the findings' prose. The argument in a row is why the row survives a re-read; **nothing here
  compresses it.**
- Out: mirroring the board. A table of task ids outside the tracker's markers is a second board and
  the `DUPLICATE INDEX` advisory is right to say so — this keys on findings and *references* tasks.
- Out: T-137's packaging. This produces the evidence; that task carries it outward.
- Out: **a finding with no task at all.** It is reported as unlinked and does not fail the run — every
  finding has one today, and a finding raised before its task exists is a legal state, not drift.

**Acceptance criteria**
- [ ] One command answers *which finding is which task, and what state is it in*, for all 13 findings
- [ ] **Its default output is under 2,000 bytes**, against the 325,695 measured across the six sources
      in §1; a listing nobody can read whole has moved the cost rather than removed it
- [ ] A `--check` mode prints under 200 bytes on a green run (`CE-03`'s precedent)
- [ ] **Both failing directions are asserted in a self-test with synthetic fixtures**, not read
      (**L-74**, **L-78**, **L-85**): a closed row with an open non-per-item task, and a task naming a
      finding that does not exist
- [ ] The per-item exception is exercised by the same self-test, so `CE-04`'s real state stays green
      for the declared reason rather than by accident
- [ ] The execution order's five position-citing notes cite task ids instead, and the checker asserts
      the open rows are a consecutive `1..n`
- [ ] Every `CE-nn` task carries `finding:`, and `context_fields` shows it
- [ ] Pure standard library (**L-07**), runs from any working directory, self-test first (**L-04**)
- [ ] `python tools/tasks/lint.py` green, and `tools/check_all.py`'s partition still accounts for
      every tracked tool

**Open questions**
- ~~**Is `s` right?**~~ **Answered at `specify`, 2026-08-14: yes.** The schema does not resist — a
  carried field needs no vocabulary row, which `shipped_in` has been proving here since 2026-08-12 —
  so the register file that would have made it larger is not needed. The execution-order half was
  taken into scope on the same reading: its fix is a note rewrite plus one assertion, not a second
  generator.

## 2. Plan

**Seven steps. The links are written before the checker enforces them**, so no moment exists in which
a green gate means the data is absent rather than consistent.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Add `finding: CE-nn` to the front matter of every task that serves a finding, and `finding` to `context_fields` in [`../.taskmd/config.md`](../.taskmd/config.md) | The link, in its one home |
| 2 | Mark `CE-04`'s Effort cell `xs` **each** in [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6, so the per-item band is declared where §9 says nothing declares it | One cell, and a rule a program can read |
| 3 | Rewrite the execution order's five position-citing notes to cite task ids | [`../docs/RELEASE-PHASES.md`](../docs/RELEASE-PHASES.md), with the renumbering cascade gone |
| 4 | Write `tools/docs/findings.py`: parse §6's table and the execution order, read the tasks, join, print | The listing, under 2,000 bytes |
| 5 | Add `--check`: the two failing directions, the per-item exception, the consecutive-`1..n` assertion, and a self-test with synthetic fixtures that asserts all of them | The gate, under 200 bytes green |
| 6 | Wire it: a fourth step in `tools/tasks/lint.py`, and `NOT_RUN` in `tools/check_all.py` naming that gate — `refcheck.py`'s precedent exactly | Both gates account for it |
| 7 | Update the documents the wiring makes wrong: [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §6 and §7, [`TOOLING.md`](TOOLING.md), and the handoff config's `tracker_lint` note | *Three checks* becomes four wherever it is written |

**Why `lint.py` and not `check_all.py` alone.** The drift this removes is created at the moment a task
closes, and `check_all.py` is the release gate — 154 seconds, run at a release, not at a closure. A
check that fires days after the state it guards is a report, not a gate. `refcheck.py` is already
wired exactly this way and is classified `NOT_RUN` in `check_all.py` for it, so this adds a step to a
chain rather than a pattern to the repository.

**Not touched, and why.** §6's *What* cells, §6.1's finding statements, and the execution order's
third cell are all argument and stay hand-written — that is §1a's ruling, not an omission. The board
is not mirrored: the listing names tasks and reads their status from the tracker, and prints no table
of task ids that `DUPLICATE INDEX` would be right about.

## 3. Implement

**What the question cost, before and after.** Measured 2026-08-14, the six sources against the
command that replaces them.

| | Bytes |
| :--- | ---: |
| [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6 and §6.1 | 15,042 |
| the same document's §9 | 9,744 |
| [`R8`](../docs/research/R8-context-economy-for-coding-agents.md) §8 | 12,151 |
| the three documents under [`../docs/upstream/`](../docs/upstream) | 19,978 |
| the 18 task files naming a `CE-nn` | 268,780 |
| **the six sources** | **325,695** |
| `python tools/docs/findings.py` | **1,317** |
| `python tools/docs/findings.py --check` | **61** |

**247× on the listing, and the answer is now correct by construction rather than on the day it was
written.** The comparison is honest about what it is not: the six sources hold the *arguments*, and
none of them is compressed or moved. What was removed is the fourteenth copy of the *link*.

**The marker the finding table already carried, and nobody read.**
[`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §9 said *nothing in the table says which bands
are per-item*. `CE-04`'s Effort cell has read `` `xs` each `` since the row was written — the marker
was there, unread, while the fact it encodes was being restated in prose one section away. **No edit
to §6 was needed**; the tool reads the cell and §9 is corrected. That is the finding's own mechanism
caught in the act, and it is why the per-item rule is enforced rather than remembered.

**The link had a prose marker in 13 of the 14 tasks and it was not usable.** Thirteen carry the
sentence **The finding is `CE-nn`**; T-143 does not, and eleven *other* task files mention a `CE-nn`
without serving one — T-130 names eleven of them and T-137 nine. Binding on the sentence would have
been vocabulary, would have missed T-143, and would have counted T-130 as serving eleven findings.
The front-matter field is the structural home, and this is the evidence for it rather than the
argument for it.

**Two defects in the checker, both found by running it against the real documents.** A band cell
corrected under §6.2's rule keeps its old value struck through, so stripping markup printed `L S` as
`CE-07`'s band; the struck span is now dropped first. And the numbering rule refused position `2`
holding two tasks — which is a **shared cell**, the thing the document reaches for *instead of* a
renumbering, and the mechanism this task exists to protect. A span (`10–12`) owes one task per
position; a single number does not.

**The gate fires end-to-end, against a case whose answer was known** (**L-86**). `CE-08`'s rank was
struck while T-148 was still open, and `--check` exited 1 naming both. Restored, and green.

**Where it runs, and why not the release gate.** `tools/tasks/lint.py`, as a fourth step —
`refcheck.py`'s precedent exactly, and `check_all.py` classifies it `NOT_RUN` for the same reason.
The disagreement it catches is *created* at a task closure, and `check_all.py` is what a release runs.
A check that fires days after the edit that broke the thing is a report.

**Decisions & assumptions**
- **The link is `finding: CE-nn` in task front matter; there is no register file.** The schema carries
  an unnamed field without interpreting it and `taskmd check` passed 152 tasks and 912 field values
  with no complaint on the first run — the empirical half of what
  [`../.taskmd/config.md`](../.taskmd/config.md) already stated — 2026-08-14.
- **The documents are checked, never generated.** Every row in both tables carries an argument, and a
  generated block would put a marker fence around prose a person edits — 2026-08-14.
- **The execution order's notes cite task ids now.** The renumbering was expensive because of the
  notes, not the numbers; five cited positions and the cascade ended at the table's edge. What is left
  is a consecutive-`1..n` assertion — 2026-08-14.
- **[`../CLAUDE.md`](../CLAUDE.md) stopped enumerating the checkers.** Its *Working method* named three
  and said `TASK-WORKFLOW.md` owns *all three*; the wiring made that the second time the count went
  stale. It names `lint.py` and points, which is **−87 bytes off tier 1** and cannot go stale again —
  2026-08-14.

**Outputs produced**
- `tools/docs/findings.py` — the listing and the gate, 18,390 bytes, pure standard library
- `finding: CE-nn` in 14 task files, and `finding` in `context_fields` in
  [`../.taskmd/config.md`](../.taskmd/config.md)
- [`../docs/RELEASE-PHASES.md`](../docs/RELEASE-PHASES.md) — five notes repointed to task ids, and the
  rule stated above the table
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) — §9's per-item claim corrected, §6.2's
  closure obligation made checkable
- `tools/tasks/lint.py`, `tools/check_all.py`, [`TOOLING.md`](TOOLING.md),
  [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §6 and §7, [`../CLAUDE.md`](../CLAUDE.md),
  [`../.handoff/config.md`](../.handoff/config.md) — the wiring, and *three checks* is four everywhere
  it was written

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| One command answers *which finding is which task, and what state is it in*, for all 13 findings | met | 13 findings, 14 tasks, `CE-04` twice |
| Default output under 2,000 bytes against 325,695 | met | **1,317** — 247× |
| `--check` under 200 bytes on a green run | met | **61** |
| Both failing directions asserted in a self-test with synthetic fixtures | met | four `link` assertions and four on the execution order; fixtures are `CE-9n`/`T-90n`, so no tracked file's current state is asserted (**L-85**) |
| The per-item exception exercised by the same self-test | met | `CE-92` is the fixture; `CE-04`'s real state is green for the declared reason |
| The execution order's notes cite ids, and the numbering is asserted | met | five notes repointed; `--check` reports *execution order consecutive* |
| Every `CE-nn` task carries `finding:`, and `context_fields` shows it | met | `query.py context T-148` prints `finding CE-08` |
| Pure standard library, runs from anywhere, self-test first | met | `os`, `re`, `sys`; root from `__file__` |
| `lint.py` green, and `check_all.py`'s partition still complete | met | four checks pass; `findings.py` is `NOT_RUN` with its reason, so no `UNCLASSIFIED` |

**What this does not do.** It does not tell you a finding's band was right, which is phase 2's job
(`R8` §3.1), and it does not read the arguments — the six sources are still where the reasoning is.
It removes one class of error: the register, the execution order and the tracker can no longer
disagree silently.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-14 | → proposed | Raised at the owner's direction after a hand-assembled finding-to-task listing cost six sources and produced a copy that was stale on arrival. **Not an audit finding** — `CE-nn` is closed at thirteen and this is new capability, so it takes an ordinary task id and no finding number. It is the local proof of a requirement written the same day into T-137, which is blocked on T-136; building it here first is this project's own rule about local precedent, not impatience. |
| 2026-08-14 | → specified | §1a settled all three questions and the open one. The schema does not resist a carried field — `shipped_in` is that mechanism already running here — so the register file that would have made this larger is not needed and `s` holds. The execution order came into scope on the same reading: its fix is a note rewrite plus one assertion. **Two corrections to §1 first**: it named `BRIEF.md` as the execution order's home, which `CE-05` had moved out the same day this task was raised, and *thirteen task files* measured 18. |
| 2026-08-14 | → planned | Seven steps, links written before the checker enforces them. |
| 2026-08-14 | → in_progress → done | Built, wired and green. **Step 2 turned out to be no edit at all**: `CE-04`'s Effort cell already read `xs` **each**, so the marker §9 said was missing had been there since the row was written — §9 is corrected instead. Two defects in the checker were found by running it against the real documents, both in the reading of a table cell rather than in the rules. The gate was proved end-to-end against a known answer and restored (**L-86**). `../CLAUDE.md` gave up its checker enumeration in the same pass, −87 bytes off tier 1, because the wiring made that list stale for the second time. |
