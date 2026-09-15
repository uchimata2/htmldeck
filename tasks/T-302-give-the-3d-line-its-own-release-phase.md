---
id: T-302
title: Give the 3D line its own release phase, so the 1.0.0 backlog can be empty while T-057 stays open
type: admin
status: done
phase: review
parent: null
blocked_by: []
related: [T-057]
work_package: PH3
shipped_in: 1.0.0
owner: the project owner
business_value: high
effort: s
created: 2026-09-13
updated: 2026-09-13
deliverables:
  - .taskmd/config.md
  - tasks/_task-template.md
  - docs/RELEASE-PHASES.md
  - docs/RELEASE-HISTORY.md
  - CLAUDE.md
  - tasks/TASK-WORKFLOW.md
  - README.md
---

# T-302 - Give the 3D line its own release phase, so the 1.0.0 backlog can be empty while T-057 stays open

## 1. Specify

**Outcome**
The board separates what 1.0.0 needs from the 3D line the owner scheduled for 1.1.0, so *the backlog
is empty* is answered by a query rather than by judgement. [T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md)
stays open as the first task of that line and is not counted against 1.0.0.

**Where it came from**
The owner, 2026-09-13: 1.0.0 ships with the community marketplace submission once the backlog is
empty, and it is not to wait for 3D. 3D is 1.1.0, and needs thorough testing, more examples, fixes,
and features that use a 3D library; T-057 is only its beginning. Today T-057 sits in `PH3` beside the
1.0.0 work, and `CLAUDE.md` names three phases.

**Scope**
- In: a phase value for the 3D line in `.taskmd/config.md`'s vocabulary and the task template's menu
- In: `docs/RELEASE-PHASES.md`, and the sentences in `CLAUDE.md` and `tasks/TASK-WORKFLOW.md`
  section 3 that enumerate the phases
- In: moving T-057 into the new phase
- Out: raising the rest of the 1.1.0 work. Those tasks are raised when that line starts
- Out: `shipped_in`, which stays a version and is set at close

**Inputs**
- `docs/RELEASE-PHASES.md`, `.taskmd/config.md`, `tasks/_task-template.md`

**Acceptance criteria**
- [x] `python tools/tasks/query.py list --open --work_package PH3` lists no 3D task, and the new phase
      lists T-057
- [x] every document that enumerates the phases names the new one; if `CLAUDE.md` changes size, its
      measured pair is re-measured in the same edit
- [x] `python tools/tasks/lint.py` green

**Open questions**
- The mechanism - the owner. Recommended: a fourth phase, `PH4`, because this repository already groups
  work by release phase and a phase is what the index divides on. The alternative, a log note on
  T-057, leaves every open-task query counting it toward 1.0.0.
  **Answered by the owner 2026-09-13: `PH4`.**

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Add `PH4` to the `work_package` vocabulary and to the template's menu, which must equal it | `PH4` in `.taskmd/config.md`'s vocabulary row and in `tasks/_task-template.md`'s `work_package` menu |
| 2 | Move T-057 into `PH4` | T-057's front matter reads `work_package: PH4`, with a `(no change)` log row |
| 3 | Record the decision where the phase decisions live | `docs/RELEASE-PHASES.md`: the fourth split under the section that draws the phases, a `PH4` section, and T-057's `PH3` rows saying where it went |
| 4 | Bring every sentence that enumerates the phases in step | `CLAUDE.md`, `tasks/TASK-WORKFLOW.md` section 3, `README.md` and `docs/RELEASE-HISTORY.md` name `PH4` |
| 5 | Re-measure `CLAUDE.md`'s pair in the same edit | its over-bound sentence states the new size, the floor and the debt |
| 6 | Verify by use | the two queries, `python tools/tasks/lint.py`, then `python tools/check_all.py --docs` |

**Decisions**
- **Dated records keep their three phases** - `docs/lessons/L-69.md`, `docs/CONTEXT-AUDIT.md` and
  `docs/PRE-RELEASE-AUDIT.md` state what was true when each was written, and METHOD rule 5 forbids
  rewriting the past. `docs/RELEASE-HISTORY.md` is edited because its sentence reads as the current
  set. 2026-09-13.
- **`tools/docs/cycles.py` gains no band.** Cycle 38 already takes every closed task no earlier band
  claims, so a closed `PH4` task has a cycle; a band of its own is owed when there is closed `PH4` work
  to size it on. 2026-09-13.
- **T-057's `PH3` row stays where it is**, marked as moved, and the `PH4` row points back to it. Moving
  the row would erase what `PH3` contained, which that document keeps on purpose; copying it would
  make two homes. 2026-09-13.

## 3. Implement

**Decisions & assumptions**
- **`CLAUDE.md` places 3D work in `PH4` before the size rule is applied**, so a 3D task estimated `l`
  does not land in `PH3`. The clauses are read in order, which is already how `PH1` wins. 2026-09-13.
- **`README.md`'s new sentence has not been through the humanizer.** `docs/PUBLISHING.md` runs that
  pass per release over the covered set, so the sentence joins the next release's pass. 2026-09-13.
- **`docs/RELEASE-PHASES.md`'s opener now says *one section per phase*** where it said *three
  tables*, so the next phase cannot make it stale. 2026-09-13.

**Outputs produced**
- `.taskmd/config.md`: `PH4` in the vocabulary row, and one sentence dating it
- `tasks/_task-template.md`: `PH4` in the `work_package` menu
- [T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md): `work_package: PH4`,
  with a log row
- `docs/RELEASE-PHASES.md`: the fourth split, a `PH4` section, and T-057's two `PH3` rows marked as
  moved
- `CLAUDE.md`: four phases and the `PH4` placement clause, and its over-bound sentence re-measured
- `tasks/TASK-WORKFLOW.md` section 3, `README.md` and `docs/RELEASE-HISTORY.md`: the sentences that
  enumerate the phases

**Verification, by use** - all run 2026-09-13 on branch `t-302-ph4-3d-line`, after the last content
edit and before this section was written
- `python tools/tasks/query.py list --open --work_package PH3` lists twelve tasks and no 3D task;
  `--work_package PH4` lists T-057 alone.
- `python tools/tasks/lint.py`: all 5 passed, and `tasks/README.md` was regenerated.
- `python tools/check_all.py --docs`: 9 ran, 35 skipped with a reason, 0 failed, 0 unclassified,
  against `origin/master` `bcf89e4`. It refused nothing, so no deck-facing path changed.
- `CLAUDE.md`'s own measuring command after the last edit to it: 15,968 bytes against
  `docs/AUDIT-METHOD.md`'s 8,040, which is what the rewritten sentence states. It was 15,899.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| the open `PH3` list has no 3D task, and the new phase lists T-057 | met | section 3, first verification row |
| every document that enumerates the phases names the new one, and `CLAUDE.md`'s pair is re-measured | met | seven documents. The dated records keep three phases, by the plan's first decision. `CLAUDE.md` grew 69 bytes, and its sentence was rewritten in the same edit |
| `python tools/tasks/lint.py` green | met | 5 of 5 |

**Nothing this task produced renders.** No deck, shell, theme or example changed, and the `--docs`
gate's refusal rule confirms it.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-13 | -> proposed | Raised on the owner's direction of the same day: 3D is 1.1.0 and must not hold 1.0.0. `PH3`, since it is neither a published defect nor `l`. |
| 2026-09-13 | (no change) | The owner chose `PH4`. Still `proposed`. |
| 2026-09-13 | proposed -> specified | The owner's answer closes the one open question, and the criteria stand as written. |
| 2026-09-13 | specified -> planned | Six steps. Three decisions: dated records keep their three phases, `cycles.py` gains no band, and T-057's `PH3` row stays and is marked. |
| 2026-09-13 | planned -> in_progress | Started on branch `t-302-ph4-3d-line`. |
| 2026-09-13 | in_progress -> done | All three criteria met. `PH4` holds T-057, the open `PH3` list is what 1.0.0 needs, and `CLAUDE.md` is re-measured at 15,968 bytes. `shipped_in: unreleased`. |
