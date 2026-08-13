---
id: T-131
title: Expose the tracker's query commands so the board is not read whole
type: deliverable
status: proposed
phase: specify
parent: T-130
blocked_by: []
related: [T-130]
work_package: PH3
owner: the project owner
business_value: high
effort: xs
created: 2026-08-13
updated: 2026-08-13
deliverables:
  - tools/tasks/query.py
---

# T-131 — Expose the tracker's query commands so the board is not read whole

## 1. Specify

**Outcome**
A session can ask *what next* and *what does this task point at* with one command, instead of reading
[`README.md`](README.md) whole. **The finding is `CE-02`**, stated in full in
[`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
§8 and ranked first in [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6; it is not restated
here.

**Why it is first on the ranked list**
Measured 2026-08-13: the generated board is **33,676 bytes** and `taskmd list --open` answers the
same question in **1,901** — 17.7× — while `taskmd context T-130` answers one task in **790**. The
hard part is already solved: [`lint.py`](../tools/tasks/lint.py) locates the installed skill by
globbing the version directory, so a plugin update cannot break it silently. This adds an entry
point beside it and changes no data.

**Scope**
- In: a tool exposing at least `list` and `context`, using the same locator as `lint.py`.
- In: [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §6 pointing at it, beside the four commands it already
  states are not what an agent can run.
- In: a line saying an agent asks rather than reads the board.
- Out: changing the generated board, which is for people.
- Out: duplicating the locator. If two files would carry it, it moves to one (**L-13**).
- Out: wrapping `index` or `check` — [`lint.py`](../tools/tasks/lint.py) owns those and chains them.

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6, `CE-02`, and §7.2 `O-T2` — the same
  finding written as an observation for taskmd, whose backlog was read
- [`../tools/tasks/lint.py`](../tools/tasks/lint.py) — the locator, and the precedent for the shape
- [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §6

**Acceptance criteria**
- [ ] One command returns the open board, and one returns a single task's context, from any working
      directory, standard library only (**L-07**)
- [ ] The locator has exactly one home across the repository, and a plugin version bump does not
      break either tool
- [ ] `TASK-WORKFLOW.md` §6 names it where it currently says the bare `taskmd` command does not
      resolve, so a reader meets the answer at the sentence that states the problem
- [ ] Measured after the change: the bytes a session pays to learn what to work on next, against
      33,676
- [ ] `python tools/check_all.py` stays green — a new tool under `tools/` that no manifest table
      names is `UNCLASSIFIED` and **fails the run**, so the manifest entry is part of this task

**Open questions**
- None.

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
| 2026-08-13 | → proposed | Raised from [T-130](T-130-audit-the-context-economy-of-an-agent-driven-repository.md)'s ranking at the owner's review, first of four. `CE-02`, and the highest measured saving per unit of effort in that audit: 33,676 bytes against 1,901, with no risk and the locating problem already solved by a file that ships. **Its manifest entry in `check_all.py` is inside the task rather than after it** — a tracked tool no table names fails the release run, which is the gate working as designed and a trap if it is met at release time. |
