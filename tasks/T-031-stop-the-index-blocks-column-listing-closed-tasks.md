---
id: T-031
title: Stop the index `Blocks` column listing closed downstream tasks
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-029, T-030]
work_package: none
owner: maintainer
created: 2026-08-07
updated: 2026-08-08
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
- ~~**Drop closed downstream tasks, or show them struck through / marked?**~~ **Answered
  2026-08-07 by the owner: the proposal, as written.** The board drops them, `context` keeps them
  with their status, and [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §6 gains the rule — *"generated
  views count only open tasks as gated"*. The two views differ because they are read for different
  reasons: the board is read to **choose** work and has no column for a status, `context` is read
  to **do** one task and the closed downstream tasks are the trail explaining why it exists. What
  had to be consistent was the rule, and now it is stated in one place rather than implied by two
  comprehensions.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Survey every place a derived edge list is printed and record which of them already filter, so the fix is to the inconsistency rather than to one line. | The three sites named in §3 |
| 2 | `cmd_index`: filter the *Blocks* column to open tasks, matching the *Blocked by* side, and state the rule in a comment at the point both comprehensions are read. | [`tools/tasks/task.py`](../tools/tasks/task.py) |
| 3 | `cmd_context`: keep closed downstream tasks and mark them, mirroring how `BLOCKED BY` flags the ones still open — the section header claims they are waiting, and for a closed one that is false. | same |
| 4 | Write the rule into [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §6, so the next reader of either comprehension has something to check them against. | [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) |
| 5 | Verify against a constructed open→closed edge, because the instance that raised this closed in the meantime (see §3) and the live board no longer shows it. | Recorded in §4 |
| 6 | Regenerate [`README.md`](README.md), run `check --closing`, and state what moved in the board. | [`README.md`](README.md) |

## 3. Implement

**Decisions & assumptions**
- **The instance that raised this closed before the fix landed, so the board diff is empty** —
  2026-08-08. T-015 is `done`, and a closed task's row moves to the *Closed* table, which has no
  *Blocks* column. Scanning every edge in the backlog, **no open task currently has a closed
  downstream task**, so `index` regenerated `README.md` byte-identical. The defect is latent, not
  gone: the comprehension was still unfiltered, and the next `blocked_by` edge to close would have
  reproduced it. Verified against a constructed edge instead — see §4.
- **Three sites print a derived edge list; one was wrong** — 2026-08-08. `cmd_index`'s *Blocked by*
  column already filtered to open, and `cmd_decisions` already filtered its "blocks" list with
  `t.is_open`. Only `cmd_index`'s *Blocks* column did not. Both correct sites gained a comment
  citing the rule, so the next reader has something to check them against rather than re-deriving
  the argument — the fix is to the inconsistency, per §1's scope.
- **`context` marks closed downstream tasks rather than only showing their status** — 2026-08-08.
  `line()` already printed `done`, but the section heading says *"waiting on this one"*, which is
  false for a closed task. `<-- closed, not waiting` mirrors the `<-- still open` flag the
  `BLOCKED BY` section uses, and open downstream tasks stay unflagged so the marker is signal.

**Outputs produced**
- `tools/tasks/task.py` — `cmd_index` (filter + rule comment), `cmd_context` (mark closed
  downstream), `cmd_decisions` (rule comment; behaviour unchanged).
- [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §6 — *"Generated views count only open tasks as gated"*,
  with the board/`context` split as a table.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| `index` drops closed tasks from the *Blocks* column, and T-015's row no longer names T-003 | partial | The filter is in and verified; **the named instance is unverifiable and was already gone** — T-015 closed on 2026-08-07, so it has no *Blocks* column to check. Verified instead against a constructed pair (open `T-900` ← closed `T-901`, `blocked_by: [T-900]`): the board printed `Blocks: -` where the old comprehension would have printed `T-901`. Both scratch files removed afterwards. |
| `context` shows the same set of downstream tasks as the board, closed ones marked or omitted consistently | pass | Same rule, stated once in `TASK-WORKFLOW.md` §6 and cited from all three call sites. `context T-900` printed `T-901 done ... <-- closed, not waiting`; `context T-002` printed its two open downstream tasks unflagged. |
| A task whose downstream tasks are *all* closed reads as blocking nothing, not as blocking a list | pass | `T-900`'s board row read `Blocks: -`. The existing `or "-"` handles it once the comprehension filters. |
| `check --closing` still passes, and the pointer count does not fall | pass | `OK - 33 tasks, 493 document pointers, 0 broken`, no cycles — the same 493 as before the change. `index` reported 10 active / 23 closed and left `README.md` byte-identical (see §3). |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-08 | → done | Worked through `plan`, `implement` and `review` in one pass. **The board did not move**: T-015 — the row that raised this — closed on 2026-08-07, and no other open task currently has a closed downstream task, so `index` regenerated `README.md` byte-identical and the fix is preventive rather than corrective. Verified against a constructed open→closed edge instead, then removed it. Of the three sites §1 named, only one was wrong; the two already-correct ones gained a comment citing the rule, because the reason this survived repeated reading was that nothing was written down for either comprehension. **The `TASK-WORKFLOW.md` §6 half is the durable part** — the code now cites a rule instead of implying one. |
| 2026-08-07 | (no change) | **Answered by the owner: the proposal stands as written** — board drops, `context` keeps with status, and the rule goes into [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §6. §1 now has no open question, and the task is a three-part edit with a stated rule behind it rather than a one-line filter. **The `TASK-WORKFLOW.md` half is the part that stops this recurring**: the defect was two comprehensions disagreeing with nothing written down for either, which is how it survived being read repeatedly. |
| 2026-08-07 | → proposed | Raised from a finding carried in the session handoff rather than in any durable home — the reason it is a task now. Found while reading the board to start [T-015](T-015-plugin-scaffold-and-the-two-question-interface.md): its *Blocks* column names `T-003`, which is `cancelled`. The cause is one unfiltered comprehension in `cmd_index`, and the same asymmetry may exist in `cmd_context`. Cosmetic in effect, structural in kind — the board is what a session reads to choose work, and the *Blocks* column is criterion (a) of T-030's tie-break rule. |
