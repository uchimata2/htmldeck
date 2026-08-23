---
id: T-224
title: Give the blindness fixture its own instrument in cycle 17
type: fix
status: done
phase: review
parent: T-219
blocked_by: []
related: [T-223, T-044]
work_package: PH3
owner: the project owner
business_value: high
effort: xs
created: 2026-08-23
updated: 2026-08-23
shipped_in: unreleased
deliverables:
  - docs/AUDIT-METHOD.md
  - tasks/T-219-pre-release-audit-of-the-whole-repository.md
  - docs/PRE-RELEASE-AUDIT.md
  - docs/lessons/L-137.md
---

<!--
The lifecycle, which edge to use, and where each fact lives: the taskmd skill's METHOD.md.
Field names and allowed values: `.taskmd/config.md`.
-->

# T-224 — Give the blindness fixture its own instrument in cycle 17

## 1. Specify

**Outcome**

Cycle 17 can be run without reading a fixture built to fail as a set of findings.
`examples/reference-deck-seeded-defects.html` carries one seeded defect per evaluation dimension on
purpose, at score 0; cycle 17's brief as written points the four deck gates at all five files and
says *look at each*, so the fixture's reds arrive indistinguishable from a real deck's. At the end,
every document that states cycle 17's subject states the same subject as
[`../tools/docs/cycles.py`](../tools/docs/cycles.py)'s rule table, the fixture's instrument is named
separately from the decks', and `docs/AUDIT-METHOD.md` §2's `.html` figure is true of the tree.

`PR-01` in [`../docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) §3 is the finding and its
row is the only home for the statement. `PR-66` is the same finding raised again and is withdrawn.

**Scope**

- In: the wording of cycle 17's subject and brief wherever it is stated —
  [`../docs/AUDIT-METHOD.md`](../docs/AUDIT-METHOD.md) §2, and
  [T-219](T-219-pre-release-audit-of-the-whole-repository.md) §1's scope bullet and §2's cycle 17 row.
- In: the two figures `PR-01` names, both reached only by counting the fixture.
- In: measuring the remedy's hypothesis before committing to it (**L-90**), and recording which way
  it went and why.
- Out: running cycle 17. This task makes it runnable; the cycle is its own session.
- Out: `tools/docs/cycles.py`. Its rule table already states the subject correctly and its figures are
  derived — the prose is what disagrees with it.
- Out: `PR-21`, the missing `Instrument` column, which is batched to cycle 40 and is a wider change
  than this row.

**Inputs**

- [`../docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) §3 — `PR-01`'s row, and `PR-66`'s.
- [`../docs/AUDIT-METHOD.md`](../docs/AUDIT-METHOD.md) §2.
- [T-219](T-219-pre-release-audit-of-the-whole-repository.md) §1, §2 and §3.
- `tools/check_all.py`'s `DECKS` and `NOT_A_DECK`; `tools/examples/seed_defects.py --check`.

**Acceptance criteria**

- [ ] Every document stating cycle 17's subject states the same subject as `cycles.py`'s rule table,
      and the wording is re-derived from the command rather than copied between documents.
- [ ] Cycle 17's brief names an instrument for the fixture that is not a deck gate whose reds the
      fixture exists to produce.
- [ ] `docs/AUDIT-METHOD.md` §2's `.html` figure says what it counts: the tracked count and the
      cycle-17 byte figure are both true of the tree.
- [ ] The remedy's hypothesis — cut the fixture into a row of its own, or keep it in 17 with its own
      instrument — is measured, decided, and the reasoning recorded in §3.
- [ ] `python tools/docs/cycles.py --cycle 17` and `--plan` run clean, and `python tools/tasks/lint.py`
      is green.
- [ ] `PR-01`'s row carries this task and its status, and `PR-66` still reads withdrawn.

**Open questions**

- None. The one question — which shape the remedy takes — is this task's to settle by measurement,
  per §3's decision.

## 2. Plan

**The hypothesis is measured first, and it decides the shape of every step after it.** `PR-01`'s
remedy proposes cutting cycle 17 to the four decks `DECKS` names and giving the fixture a row of its
own. A row of its own is a cycle number, and cycle numbers are cited. Step 1 prices that before any
document is edited.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Price the remedy. Count the citations a renumber would falsify, and check whether `cycles.py` can hold a cycle id that is not an integer. | A decision recorded in §3: cut, or keep the membership and split the instrument. |
| 2 | Re-derive cycle 17's subject and both figures from `python tools/docs/cycles.py --cycle 17`, and the tracked `.html` count from `git ls-files '*.html'`. | The numbers every following step writes, taken from the command and not from a document. |
| 3 | Correct [`../docs/AUDIT-METHOD.md`](../docs/AUDIT-METHOD.md) §2's instrument-only bullet: what it counts, and the fixture's own instrument. | One bullet that is true of the tree. |
| 4 | Correct [T-219](T-219-pre-release-audit-of-the-whole-repository.md) §1's scope bullet and §2's cycle 17 row — subject to match `cycles.py`, brief split into the decks' instrument and the fixture's. | Cycle 17 runnable without reading seeded reds as findings. |
| 5 | Update `PR-01`'s `Task` and `Status` cells in [`../docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) §3, and check `PR-66` still reads withdrawn. | The register and the tracker tell the same story. |
| 6 | `python tools/docs/cycles.py --cycle 17`, then `--plan`, then `python tools/tasks/lint.py`. | Three green runs, none of them concurrent. |

## 3. Implement

**Decisions & assumptions**

- **Half of `PR-01`'s remedy was refused, and it was refused by measurement rather than by taste.**
  The row proposes cutting cycle 17 to the four decks and *giving the fixture a row of its own*. A row
  of its own is a cycle number: `tools/docs/cycles.py`'s rule table is keyed on an integer and prints
  the id with `%-3d`, so the fixture takes either a new number — renumbering 18 to 43 — or nothing.
  `git ls-files -z | xargs -0 grep -ohE "cycle (1[89]|[2-3][0-9]|4[0-3])"` counts **99 citations in
  tracked files, 85 of them `cycle 40`**, which is one per open finding in the register. A renumber
  falsifies every one of them to separate two instruments that a single brief can name in two
  sentences — 2026-08-23
- **The membership was never the defect; the instrument was.** `python tools/docs/cycles.py --cycle 17`
  prints five files and 1,773,568 bytes under the subject *The shipped decks and the blindness
  fixture*, which is correct, and `PR-01`'s own row says so. What cycle 17's brief said was *Render
  each offline and look at it. `check.py`, `audit.py`, `printgeom.py`, `glitchfree.py`* — four deck
  gates pointed at a file seeded to score 0 on all ten evaluation dimensions. So the fix is one row's
  Brief column and two sentences of prose, not a re-cut partition — 2026-08-23
- **The fixture's instrument is `python tools/examples/seed_defects.py --check` and nothing else.**
  Run today it exits 0, reports the file is byte-for-byte what regenerating produces (322,257 bytes),
  and lists the seeded defect behind each of the ten dimensions. That is the only question a cycle can
  ask of it: **is it still derived from the reference deck rather than edited.** Its score is a known
  answer, so scoring it measures the rubric and not the fixture, which belongs to whoever grades the
  rubric rather than to a coverage cycle — 2026-08-23
- **Three documents were re-derived from the command, not from each other.** The four-deck figure
  1,451,311 and the six-file tracked count are computed here for the first time; every document that
  now states them also names the command that reproduces them, per **L-95** point 4 — 2026-08-23
- **`PR-21` was left alone.** The missing `Instrument` column is what let cycle 17's instrument sit
  inside a prose brief, and this task is the proof of what that costs — but it is batched to cycle
  40 across thirty-eight written rows, and back-filling those is not this row's remedy — 2026-08-23

**Outputs produced**

- [`../docs/AUDIT-METHOD.md`](../docs/AUDIT-METHOD.md) §2 — the instrument-only bullet now covers the
  decks and the fixture separately, states what its figures count, and points at the command.
- [T-219](T-219-pre-release-audit-of-the-whole-repository.md) §1's scope bullet, §2's cycle 17 row
  (subject and a two-part brief), §3's Medium counts and its child-task list.
- [`../docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) §3 — `PR-01` closed, rank struck
  through, this task on its `Task` cell, and the header paragraph that said one remedy would land.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every document stating cycle 17's subject states `cycles.py`'s subject, re-derived from the command | met | Four places now read *the shipped decks and the blindness fixture*: `cycles.py`'s rule table, [`../docs/AUDIT-METHOD.md`](../docs/AUDIT-METHOD.md) §2, and [T-219](T-219-pre-release-audit-of-the-whole-repository.md) §1's scope bullet and §2's row. §1's grade table already said it and was not touched |
| Cycle 17's brief names an instrument for the fixture that is not a deck gate | met | `seed_defects.py --check` and nothing else. The brief now has two halves with their byte figures, so the two instruments cannot be read as one |
| `AUDIT-METHOD.md` §2's `.html` figure says what it counts | met | Six tracked; five are cycle 17's at 1,773,568; four decks at 1,451,311 and the fixture at 322,257; `shell/shell.html` is cycle 16's. It was *five tracked `.html` files*, which was wrong about the tree and about which five |
| The hypothesis is measured, decided, and the reasoning recorded | met, and half refused | 99 citations of cycles 18 to 43 in tracked files, 85 of them `cycle 40`. §3's first decision. **`not met` was available and is not what happened** — the remedy was priced and half of it declined, which the register's *a remedy is a hypothesis* clause exists to allow |
| `cycles.py --cycle 17` and `--plan` clean, `lint.py` green | met | Both exit 0, cycle 17 unchanged at 5 files and 1,773,568 bytes — which is the point: no membership moved. `lint.py` green with the eleven baselined advisories and no new one |
| `PR-01` carries this task and its status; `PR-66` still withdrawn | met | Rank struck through, `Task` cell links here, `Status` says which half was refused and why. `PR-66`'s row is untouched and its id stays spent |

**What was looked at**

Nothing this task produced renders. The outputs are three Markdown documents and a lessons file;
`CLAUDE.md` rule 6 and [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §7 step 3 bind a task that produces
something renderable, and this one does not. **The deck side of cycle 17 is unchanged and unrun** —
looking at the four decks offline is cycle 17's own work, not this task's, and that is exactly the
boundary `PR-01` was blocking.

**Lesson recorded**

[L-137](../docs/lessons/L-137.md) — *deriving what a check reads does not derive how it reads it*.
The membership was derived and right; the instrument beside it was prose and wrong, and the derived
half is the one every check looks at. It names the cheap guard, which is `PR-21`'s `Instrument`
column, still batched to cycle 40.

**Child fix tasks raised**

- none. `PR-21` is the adjacent finding and stays where it is: back-filling an instrument cell across
  thirty-eight written cycle rows is cycle 40's triage, not this row's remedy.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-23 | → proposed | Created from `PR-01`, the pre-release audit's one standing exception to the rule that triage waits for cycle 40. It gates cycle 17 rather than the run's closing claim, which is the clause that makes it an exception. |
| 2026-08-23 | → specified | Scope and criteria written before the work. Phase and type re-derived from [`../CLAUDE.md`](../CLAUDE.md) rather than taken from the register: `PH3` because this is not a defect in the published plugin, `fix` because a written subject disagrees with a derived one. |
| 2026-08-23 | → planned | Six steps, and step 1 prices the remedy before anything is edited. `PR-01`’s remedy is a hypothesis and the register says so; the part to measure is whether the fixture can have a row of its own without renumbering the cycles that cite each other. |
| 2026-08-23 | → in_progress | Step 1 priced the remedy and refused half of it: a row of its own is a cycle number and 99 tracked citations of cycles 18 to 43 depend on the numbering. The membership stays as `cycles.py` derives it; the instrument is split. Three documents and the register edited. |
| 2026-08-23 | → done | Six criteria, all met, one of them by refusing half the remedy after pricing it. `PR-01` is closed after sixteen cycles and one duplicate; cycle 17 can be run. [L-137](../docs/lessons/L-137.md) carries the general half. |
