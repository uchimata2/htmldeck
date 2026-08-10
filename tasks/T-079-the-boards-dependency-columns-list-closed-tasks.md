---
id: T-079
title: The board's dependency columns list closed tasks, so open rows read as blocked
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-031, T-062, T-063, T-073]
work_package: v0.2
owner: the project owner
business_value: medium
effort: s
created: 2026-08-10
updated: 2026-08-10
deliverables: []
---

# T-079 — The board's dependency columns list closed tasks, so open rows read as blocked

## 1. Specify

**Outcome**
[`tasks/README.md`](README.md) stops presenting a satisfied dependency as a live one. An open task
whose every blocker is closed reads as startable on the board, the way `taskmd list --open` already
ranks it. Since the generator is upstream, the outcome is a **decided behaviour and a proposal
carrying it**, not a local patch.

**Why this one**
The board is what gets read to decide what to work on, and today it disagrees with the tool.
Three open rows name a closed task in *Blocked By*:

| Row | Names | Which is |
| :--- | :--- | :--- |
| [T-019](T-019-build-the-capability-preflight-the-deck-ships-wit.md) | T-002 | `done` 2026-08-09 |
| [T-070](T-070-the-quick-view-for-a-source-document.md) | T-069 | `done` 2026-08-10 |
| [T-071](T-071-the-intermediate-specifications-carry-their-references.md) | T-069 | `done` 2026-08-10 |

`taskmd list --open` ranks all three among the startable tasks, correctly — the sort's *blocked
last* key resolves the edge against the blocker's status. So the defect is in the rendering of the
column and nowhere else, which is what makes it cheap and what makes it easy to leave.

**This project already decided this question once.** [T-031](T-031-stop-the-index-blocks-column-listing-closed-tasks.md)
found the retired `tools/tasks/task.py` filtering closed tasks out of *Blocked by* and not out of
*Blocks*, and fixed the second to match the first — its argument was that a dependency column
naming closed work *"overstates how much a task releases"* to whoever reads the board first.
[T-062](T-062-retire-the-pre-split-task-tool-and-repoint-what-points-at-it.md) then retired that
tool for taskmd, and the behaviour came back on both sides at once: `Blocks` on T-002's row names
`T-008`, which closed 2026-08-09. **Nothing recorded this**, and
[T-063](T-063-improvements-to-propose-upstream-to-taskmd.md)'s five upstream proposals do not cover
it — the migration was measured for coverage of *commands*, and this is a difference in output that
no command list would show. **L-57** is the shape: a comparison is bounded by what it reads, and
from inside it that boundary is invisible.

**The counter-argument, stated so the proposal answers it.** `.taskmd/config.md` *Ordering* defends
listing a blocked task: *"hiding it would make `list` and `list --limit 1` describe different sets,
and would conceal the graph from someone asking why nothing is moving."* That is an argument about
which **rows** appear, and it is right. It says nothing about what a dependency **cell** should
contain, and reading it as though it did is what would keep this defect. The graph is still fully
recoverable from the closed task's own row and from front-matter either way.

**Scope**
- In: decide what the cell should show when a dependency is closed — dropped, or kept and marked.
- In: write the proposal against taskmd's `index`, with the T-031 precedent and the counter-argument
  above, and send it upstream the way T-063's five were sent.
- In: both sides of the edge, `Blocked By` and `Blocks` — they were made consistent once and the
  proposal should not split them again.
- Out: a local index generator, or post-processing `README.md` after `taskmd index`. The file
  carries a *do not hand-edit* marker and re-deriving it here would put a second generator in a
  repository that just retired one.
- Out: the front-matter. A satisfied `blocked_by` edge is provenance and stays.

**Inputs**
- [`T-031`](T-031-stop-the-index-blocks-column-listing-closed-tasks.md) §1 and its review table — the
  argument and the constructed pair it was verified against.
- [`.taskmd/config.md`](../.taskmd/config.md) *Ordering* — the sort key that already resolves the edge.
- [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §4 — `blocked_by` is the only edge that gates.

**Acceptance criteria**
- [ ] The behaviour is decided and written down with its reason, including which of drop-or-mark won.
- [ ] The proposal is sent upstream, recorded here the way T-063 recorded its five.
- [ ] The three rows above are named as the instances, so a later reader can check whether the
      accepted change reached them.
- [ ] If upstream declines, this task records the decision to live with it rather than closing silent
      — an unfixed defect with a reason is a different state from a forgotten one.

**Open questions**
- Drop the closed dependency from the cell, or keep it marked (struck through, or suffixed)? T-031
  dropped it. Marking preserves the graph on the page at the cost of a busier column — the project
  owner decides, and the proposal carries whichever.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Settle drop-or-mark, and record the reason | this file §3 |
| 2 | Write the proposal — symptom, the three instances, the T-031 precedent, the ordering counter-argument | this file §3 |
| 3 | Send it upstream to taskmd | this file §3 |
| 4 | Re-run `python tools/tasks/lint.py` and record what the board shows | this file §4 |

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
| 2026-08-10 | → proposed | Raised by the owner from a status review that found the board and `taskmd list --open` disagreeing about three rows. `medium` because it misleads exactly the reader the board exists for and the cost is one column, not because anything is broken downstream — the sort is already right; `s` because the decision is small, the precedent is written, and the change itself is upstream's. `v0.2` under the release split set the same day: a minor fix. |
