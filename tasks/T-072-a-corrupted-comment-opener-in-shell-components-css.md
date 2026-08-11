---
id: T-072
title: A corrupted comment opener in shell/components.css would swallow the rule beneath it
type: fix
status: cancelled
shipped_in: 0.2.1
phase: specify
parent: null
blocked_by: []
related: [T-069, T-089]
owner: the project owner
created: 2026-08-10
updated: 2026-08-12
deliverables: []
---

# T-072 — A corrupted comment opener in `shell/components.css` would swallow the rule beneath it

> **This file is a reconstruction, written 2026-08-11 by
> [T-089](T-089-a-withdrawn-task-was-deleted-rather-than-cancelled.md). It is not the original.**
> The task was raised and withdrawn on 2026-08-10, and its file was deleted before it was ever
> committed — `git log --diff-filter=A -- 'tasks/T-072*'` returns nothing, so no version of it
> survives in the working tree or in history. Everything below is sourced from
> [T-069](T-069-extend-the-provenance-mark-to-multiple-sources.md) §3 and
> [`../docs/LESSONS.md`](../docs/LESSONS.md) **L-56**, which are what remained. Nothing here is
> recalled, and no wording of the original is reproduced, because none is available to reproduce.
>
> It exists so this ID answers for itself. Without it the sequence has a hole at T-072 and the board
> gives no hint whether the task was withdrawn or lost — the distinction
> [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §3.1 now makes a rule.

## 1. Specify

**What was raised**
During [T-069](T-069-extend-the-provenance-mark-to-multiple-sources.md), `shell/components.css`
appeared to open a comment with `\*` rather than `/*`. That would be a real defect and a nasty one:
`\*` is a valid CSS escape, so the parser reads the comment's text as a selector and **swallows the
rule beneath it**, leaving a declaration that matches nothing. The mechanism was worked out and the
consequence traced to a live rule before the task was raised.

**Why it does not stand**
**The file was correct.** The backslash was the search tool's own escaping in its context display,
not a byte in the file. Reading the same line with a second tool, and with `git show HEAD:`, printed
`/*` both times.

**What came of it instead**
[`../docs/LESSONS.md`](../docs/LESSONS.md) **L-56** — a reading tool's rendering is not the file's
bytes, and a one-character defect needs two readers. The trap is worth the entry: a plausible
mechanism makes a rendering artifact **more** convincing rather than less, and the CSS reasoning here
was correct about a character that was not there.

**What this file deliberately does not carry**
- **No work package.** The original's was never recorded anywhere that survives, and assigning one
  now would be the reconstruction claiming to know something it does not.
- **No acceptance criteria, plan or implementation.** The task was withdrawn in `specify`; it never
  had them, and writing plausible ones would make this a forgery rather than a record.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-11 | → cancelled | Reconstructed as a stub by [T-089](T-089-a-withdrawn-task-was-deleted-rather-than-cancelled.md), under the disposal rule that task wrote into [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §3.1: a task withdrawn on a false premise is `cancelled` and retained. The status change is dated to the reconstruction rather than to the withdrawal, because that is when this file came to exist; the withdrawal itself was 2026-08-10 and is recorded in T-069 §3. |
| 2026-08-10 | → proposed | Raised during [T-069](T-069-extend-the-provenance-mark-to-multiple-sources.md) and withdrawn the same day once the file was read a second way. Reconstructed from that task's §3 and **L-56**; this row records what happened, not what the original file said. |
