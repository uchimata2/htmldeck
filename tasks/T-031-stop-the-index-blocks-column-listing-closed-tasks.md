---
id: T-031
title: Stop the index `Blocks` column listing closed downstream tasks
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-029, T-030]
work_package: none
owner: maintainer
created: 2026-08-07
updated: 2026-08-07
deliverables: []
---

# T-031 — Stop the index `Blocks` column listing closed downstream tasks

## 1. Specify

**Outcome**
`python tools/tasks/task.py index` filters both sides of a `blocked_by` edge the same way, so the
generated board in [`README.md`](README.md) stops claiming an open task is holding up work that is
already closed.

**Why this one**
`cmd_index` filters the two directions of the same edge inconsistently
([`tools/tasks/task.py`](../tools/tasks/task.py), `cmd_index`):

```python
blockers   = ", ".join(b for b in t.blocked_by
                       if b in tasks and tasks[b].is_open) or "-"   # closed dropped
downstream = ", ".join(t.blocks) or "-"                             # closed kept
```

The *Blocked by* column drops closed upstream tasks — correctly, because a closed blocker no longer
gates. The *Blocks* column keeps closed downstream ones. **Today's board shows the consequence**:
T-015's row reads `Blocks: T-002, T-003` while T-003 is `cancelled`, so the index reports T-015 as
holding up a task nobody will ever work.

**It is small, and it is the class of defect this project has already paid for twice.** L-08 —
a derived view is only as good as its derivation — and [T-029](T-029-stop-the-deliverable-exemption-silently-dropping-pointers.md),
where a filter that looked reasonable hid 110 of 357 pointers. The board is the artifact a session
reads first to decide what to work on, and an inflated *Blocks* column overstates how much a task
unblocks — which is criterion **(a)** of the tie-break rule
[T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md) §3 used to derive the build
order.

**Scope**
- In: filter `t.blocks` to open tasks in `cmd_index`, matching the `blocked_by` side.
- In: the same check on every other place a derived edge list is printed — `cmd_context`
  (§*BLOCKS*), `cmd_decisions` — so the fix is to the inconsistency, not to one line of it.
- In: regenerating [`README.md`](README.md) and stating what changed in it.
- Out: changing what `t.blocks` *contains*. The derivation is right; only the presentation filters.
- Out: re-deriving T-030's build order. Its tie-break input changes for T-015 only, and the order
  is a dated judgement, not a derivation — see T-030 §3.

**Inputs**
- [`tools/tasks/task.py`](../tools/tasks/task.py) — `cmd_index`, `cmd_context`, `cmd_decisions`.
- [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §4 — `blocked_by` is the only edge that gates, and a
  closed task is not gated.
- [`docs/LESSONS.md`](../docs/LESSONS.md) — L-05, L-08, L-09.

**Acceptance criteria**
- [ ] `index` drops closed tasks from the *Blocks* column, and T-015's row no longer names T-003
- [ ] `context` shows the same set of downstream tasks as the board, closed ones marked or omitted
      consistently — whichever, it is the same rule in both
- [ ] A task whose downstream tasks are *all* closed reads as blocking nothing, not as blocking a
      list
- [ ] `python tools/tasks/task.py check --closing` still passes, and the pointer count does not fall

**Open questions**
- **Drop closed downstream tasks, or show them struck through / marked?** `context` already prints
  each downstream task's status, so it can afford to keep them; the board's column cannot, because
  it has no room for a status. Consistency of *rule* matters more than identical output —
  **maintainer decides.** Proposed: the board drops them, `context` keeps them with their status,
  and the rule stated in `TASK-WORKFLOW.md` §6 is *"generated views count only open tasks as
  gated"*.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- `tools/tasks/task.py`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-07 | → proposed | Raised from a finding carried in the session handoff rather than in any durable home — the reason it is a task now. Found while reading the board to start [T-015](T-015-plugin-scaffold-and-the-two-question-interface.md): its *Blocks* column names `T-003`, which is `cancelled`. The cause is one unfiltered comprehension in `cmd_index`, and the same asymmetry may exist in `cmd_context`. Cosmetic in effect, structural in kind — the board is what a session reads to choose work, and the *Blocks* column is criterion (a) of T-030's tie-break rule. |
