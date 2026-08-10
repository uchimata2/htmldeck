---
id: T-073
title: Decide whether to keep refcheck now that upstream has ruled on bare paths
type: analysis
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-062, T-063]
work_package: v0.2
owner: the project owner
business_value: high
effort: s
created: 2026-08-10
updated: 2026-08-10
deliverables: []
---

# T-073 — Decide whether to keep refcheck now that upstream has ruled on bare paths

## 1. Specify

**Outcome**
This project knows whether `tools/docs/refcheck.py` still earns its place, and the decision is made
against what the tool actually reports on this tree rather than against what it was built to do.

**Why this one**
[T-063](T-063-improvements-to-propose-upstream-to-taskmd.md) closed on the exit criterion that its
proposals had been copied upstream and were being processed there. **Upstream answered on 2026-08-10,
and item 1 was decided *out*:** taskmd's `check` will not resolve a path written as prose or inside a
fenced block. Only Markdown link syntax counts as a pointer. That is now documented adopter-facing in
taskmd's README, deliberately, so the next project retiring its own checker is told what it gives up
rather than finding out.

It was decided by measurement, not by argument — including a measurement of **this project's corpus**,
which this project has never seen:

| | taskmd's own tree | **This project** |
| :--- | ---: | ---: |
| Markdown links (dead) | 947 (0) | 1561 (**0**) |
| Distinct bare pointers | 683 | 481 |
| — in the task folder | — | 388 |
| Reported dead | 237 | 31 |
| — in the task folder | 235 | 27 |
| Real defects among them | **0** | **0** |

**19 of those 27 name one file: `tools/tasks/task.py`** — the pre-split tool
[T-062](T-062-retire-the-pre-split-task-tool-and-repoint-what-points-at-it.md) retired. The rest are
`.assets-cache/` and `.kb/` artefacts named as evidence, a bare `examples/README` without its
extension, and an id prefix written with an ellipsis. Of the 4 outside `tasks/`, one is
`.handoff/config.md` naming where the live handoff file *will* be — upstream produces the identical
false positive — one is a research id that is not a path, and two are hook scripts named in config
prose.

**That is the finding this task exists for, and it is not the one T-063 expected.** The argument for
keeping refcheck was coverage upstream would not provide. The coverage is real and the alarms are
not: a task record naming a tool that has since been removed is a **correct dated statement**, and a
path checker cannot tell it from a broken promise. A tracker accumulates those structurally, which is
why the same rule that validates a documentation tree cries wolf over a backlog. Upstream's reasoning
before it measured pointed the other way — this project's own report was the strongest evidence *for*
the feature.

**Do not delete `tools/docs/refcheck.py` on the strength of this alone.** Upstream's T-093 — whether
`check` resolves a **section** reference — is still open, and this file is the offered MIT reference
implementation for it, with the adjacency decision already made. Deleting it would cost upstream that
and cost nothing here to keep.

**Scope**
- In: whether refcheck keeps running, keeps existing without running, or goes.
- In: if it keeps running, what to do about the 31 — because a checker with 31 standing alarms that
  are all correct-but-dead is a checker people learn to skip, which is worse than not having one.
- In: whether the dead pointers are worth fixing *as records*. They are not defects, but 19 of them
  naming one retired file may be worth one sweep, and that is a different question from the checker.
- Out: taskmd's decision, which is made and shipped. This project does not reopen it; if the evidence
  above is wrong for this tree, that is a report upstream, not a change here.
- Out: the section-reference rule, which is upstream's T-093 and is not blocked on anything here.

**Expect the numbers to move when this project updates.** v0.2.0 also shipped upstream's T-094: `check`
now reads only the documents a clone would receive, so gitignored material — `.kb/`, `.assets-cache/`,
the live handoff — drops out of the walk and the document and link counts fall on an unchanged tree.
A new `Scope` line reports how many were skipped. Nothing has broken when that happens; a run of this
project's tracker at v0.2.0 is clean, with 31 documents excluded.

```bash
claude plugin update taskmd@taskmd
```

**Inputs**
- `tools/docs/refcheck.py`, and whatever currently invokes it.
- [T-063](T-063-improvements-to-propose-upstream-to-taskmd.md), for the five proposals as sent and the
  evidence behind each.
- taskmd v0.2.0's README, section *Which documents `check` reads, and which pointers in them* — the
  adopter-facing statement of what is and is not covered.

**Acceptance criteria**
- [ ] The decision is recorded with its rejected alternative
- [ ] If refcheck keeps running: the 31 standing alarms are resolved, suppressed or explained, so a
      clean run means something
- [ ] If it stops running: the file survives at least until upstream's T-093 closes, and the reason is
      written where someone tidying the tools folder will read it
- [ ] Whatever is decided, `docs/` says what validates a pointer in this project and what does not

**Open questions**
- **Keep, park, or delete.** The project owner's. The measurement above is the input; note that it
  says the *corpus* is wrong for the rule, not that the rule is badly built — 450 of this project's
  481 bare pointers resolve correctly.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <path>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- <T-NNN or "none">

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-10 | → proposed | Raised on the upstream answer to T-063 item 1, which came back *out* with a measurement of this tree attached. `high` because the standing assumption here is that refcheck covers something upstream does not, and the measurement says what it covers on this corpus is 31 alarms and no defects — while the one thing it uniquely still buys, the section-reference implementation, is a reason to keep the file rather than to keep running it. `s` because nothing needs building; the evidence is in hand and the work is one decision and its consequences. |
