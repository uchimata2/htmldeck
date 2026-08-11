---
id: T-079
title: The board's dependency columns list closed tasks, so open rows read as blocked
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-031, T-062, T-063, T-073]
work_package: PH2
shipped_in: 0.1.5
owner: the project owner
business_value: medium
effort: s
created: 2026-08-10
updated: 2026-08-12
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
- ~~Drop the closed dependency from the cell, or keep it marked?~~ **Settled 2026-08-10 by the owner:
  drop it, as T-031 did.** The proposal carries that and no alternative. Kept struck through rather
  than deleted, because the rival is what makes the decision legible to whoever reads the proposal
  upstream.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Settle drop-or-mark, and record the reason | this file §3 |
| 2 | Write the proposal — symptom, the three instances, the T-031 precedent, the ordering counter-argument | this file §3, **done 2026-08-10** |
| 3 | Send it upstream to taskmd | taskmd's own **T-111**, **done 2026-08-10** |
| 4 | Re-run `python tools/tasks/lint.py` and record what the board shows | this file §4 |

## 3. Implement

**Decisions & assumptions**
- **Drop the closed dependency from the cell rather than marking it** — the owner's, 2026-08-10, as
  recommended. Three reasons, in the order they carry weight upstream: this project already decided
  it once in [T-031](T-031-stop-the-index-blocks-column-listing-closed-tasks.md) and a precedent is
  a stronger proposal than a preference; the graph is not lost, since the closed task's own row and
  both front-matters still carry the edge; and a mark is a rendering rule taskmd would have to
  maintain for a fact no reader of the board is asking for. **The cell is for what gates the task,
  and nothing else does.**

**Outputs produced**
- The proposal below, drafted 2026-08-10 and **delivered** as a task file in taskmd's own tracker:
  **T-111**, *Stop the index showing a closed task as a live blocker*, written in taskmd's schema and
  left for the maintainer to index. That was the channel the owner chose over an issue or a patch.
  Named by id and title rather than by path — the file is in another repository, and a path written
  here would be a pointer this one cannot keep true.
- Amended [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §*Generated views*, which asserted the filtered
  behaviour as current fact and had been false since the migration.

---

#### Proposal to taskmd — `index` renders a satisfied dependency as a live one

**The evidence.** taskmd 0.1.1. `taskmd index` writes this row for a task whose only blocker closed
on 2026-08-09:

```
| [T-019](T-019-build-the-capability-preflight-the-deck-ships-wit.md) | Build the capability
preflight every deck ships with | `PH3` | `proposed` | `specify` | - | - | T-002 | - |
```

(One row, wrapped here, with the trailing *Related* column cut.)

`Blocked By: T-002`. `taskmd context T-019`, same tree, same minute:

```
BLOCKED BY
  T-002        done        Build mode — the self-contained deck generator

STATE  open, no blocker outstanding
```

And `taskmd list --open` ranks that task **third of fifteen**, ahead of everything genuinely held.

**So this is not an imported preference — two of taskmd's three surfaces already implement the rule
and the third does not.** `context` flags an edge `<-- still open` only when the far end is open, and
prints `STATE open, no blocker outstanding` when none is; the sort's blocked-last key resolves each
dependency edge against `tasks[target].is_open`. `index_block`'s `row` renders
`", ".join(task.links(n))` for every link name alike, so in the one artifact a person reads to choose
work, a satisfied dependency is indistinguishable from a live one. Three of fifteen open rows in this
repository name a closed blocker today, and the `Blocks` side has the same shape.

**Proposal.** Filter **dependency-kind** edges to open tasks in `index_block`'s `row`, leaving
`parent`, `children` and every soft edge alone — a closed parent is still a parent; a closed blocker
is not still a blocker. Both halves of the test already exist in `cli.py`:

```python
schema.edges[name].kind == "dependency"    # as context already tests
tasks[target].is_open                      # as is_blocked already tests
```

**Apply the same view to the column-in-use test.** `names` comes from
`any(t.links(n) for t in tasks.values())`, computed before any filtering, so a project whose
dependency edges are all satisfied would keep a column of dashes — which is the defect
`index_block`'s own docstring records as already fixed for `work_package`: *omitting an unused column
is derived from the data rather than configured*. Filtering the cells without filtering the column
selection reintroduces it one edge kind over.

**What this loses, stated.** The board stops showing the historical edge. Nothing else stops: the
front-matter keeps it, `context` prints it with the blocker's status beside it, and the closed task's
own row is untouched. The project sending this made the same change to its own pre-taskmd index
generator and wrote the reason down as *the cell is for what gates the task, and nothing else does*.

---

## 4. Review

**Upstream accepted it and it has shipped.** taskmd's T-111 is `done`, and **taskmd 0.3.0** — installed
here on 2026-08-10 by [T-081](T-081-the-installed-taskmd-is-two-minor-versions-behind.md) — filters
dependency-kind edges to open tasks in both columns. Verified on this board rather than read from a
release note:

| Row | Cell | Was | Now |
| :--- | :--- | :--- | :--- |
| [T-019](T-019-build-the-capability-preflight-the-deck-ships-wit.md) | *Blocked By* | `T-002`, closed 2026-08-09 | empty |
| [T-070](T-070-the-quick-view-for-a-source-document.md) | *Blocked By* | `T-069`, closed 2026-08-10 | empty |
| [T-071](T-071-the-intermediate-specifications-carry-their-references.md) | *Blocked By* | `T-069` | the row is closed; T-071 shipped the same day |
| [T-084](T-084-the-contents-bound-fixture-counts-a-deck-that-no-longer-exists.md) | *Blocks* | — | `T-036`, and nothing closed |

The last row is the half that matters most: the `Blocks` side was the one this project fixed once in
T-031 and lost in the migration, so seeing it carry an **open** dependency and no closed ones is the
evidence that both directions landed, not just the one the symptom showed.

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The behaviour is decided and written down with its reason, including drop-or-mark | met | Drop, in §3, with the owner's three reasons in the order they carry weight upstream. |
| The proposal is sent upstream, recorded here the way T-063 recorded its five | met | Delivered as taskmd's **T-111**, in their schema, argued from their own T-102. |
| The three rows above are named as the instances, so a later reader can check | met | Named in §1 and checked in the table above. Two are empty and the third closed on its own. |
| If upstream declines, this task records the decision to live with it | **not applicable** | They did not decline. Kept as written rather than reworded to fit the outcome — a criterion covering the other branch is not a criterion that failed. |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-10 | → done | **Accepted upstream and shipped.** Their T-111 is `done` and taskmd 0.3.0 filters both columns; installing it here is what made the answer visible, and the answer was checked against this board rather than a release note. Two of the three named rows now show an empty *Blocked by* and the third closed on its own; T-084's *Blocks* carries an open dependency and nothing closed, which is the `Blocks` half T-031 fixed once and the migration lost. Criterion 4 covered the branch where they declined, and is marked not applicable rather than reworded. |
| 2026-08-10 | (implement) | **Received upstream**: the owner reports taskmd informed, reindexed and its project updated, so T-111 is in their tracker rather than sitting untracked in a working copy. **What they decided is not known here** and is deliberately not guessed — this task stays open on that, and the next thing it needs is their answer, not more argument from this side. |
| 2026-08-10 | → in_progress | **Delivered upstream as a task in taskmd's own tracker, `T-111`**, on the owner's instruction — not an issue and not a patch, so the maintainer indexes it and owns it from there. Written in taskmd's schema, estimated to match **their** T-102, and explicit that the ids in its evidence belong to this project. Reading their backlog first found T-102 — *Show which rows list has already worked out are blocked*, `done`, the same defect on `list` and argued the same way — so the proposal leads with their precedent rather than ours. Nothing is outstanding on this side; the task stays open because criterion 4 is upstream's answer, and closing now would record a fix that has not happened. |
| 2026-08-10 | (implement) | **Writing it up found a third instance, in this repository.** `TASK-WORKFLOW.md` §*Generated views* asserted that a closed task is absent from both columns — as **current behaviour**, not as an aim. That was true of `task.py` and false from the moment T-062 swapped the tool, and it survived because the sentence reads correctly and nothing checks a prose claim against a generated file. Amended to say which surfaces observe the rule and which does not. **This is the argument for T-079 twice over: the same swap broke a column and a paragraph, and neither had a watcher.** Generalised as **L-59**. |
| 2026-08-10 | (implement) | **Proposal drafted, not sent.** Reading `cli.py` moved the argument off this project's precedent and onto taskmd's own inconsistency: `context` and the blocked-last sort both resolve a dependency edge against the far end's status, and `index` alone does not — `taskmd context T-019` prints *open, no blocker outstanding* for the row the board marks `Blocked By: T-002`. That is a stronger case than T-031, which is now the closing note rather than the argument. One thing the symptom did not show came out of the same read: `names` is computed before any filtering, so filtering only the cells would leave a column of dashes — the defect `index_block`'s docstring says was already fixed for `work_package`. |
| 2026-08-10 | (specify) | **The one open question closed by the owner, as recommended: drop, not mark.** Step 1 of the plan is done and the reason is in §3. What remains is the proposal itself and sending it — the change is upstream's to make, so this task cannot close on a green run here. |
| 2026-08-10 | → proposed | Raised by the owner from a status review that found the board and `taskmd list --open` disagreeing about three rows. `medium` because it misleads exactly the reader the board exists for and the cost is one column, not because anything is broken downstream — the sort is already right; `s` because the decision is small, the precedent is written, and the change itself is upstream's. `PH2` under the release split set the same day: a minor fix. |
