---
id: T-080
title: taskmd check resolves a markdown link inside a code fence, so pasted output cannot be quoted
type: fix
status: in_progress
phase: implement
parent: null
blocked_by: []
related: [T-063, T-073, T-079]
work_package: v0.2
owner: the project owner
business_value: medium
effort: xs
created: 2026-08-10
updated: 2026-08-10
deliverables: []
---

# T-080 — taskmd check resolves a markdown link inside a code fence, so pasted output cannot be quoted

## 1. Specify

**Outcome**
A task file can paste the output of `taskmd index` without the check treating the pasted row's
link as one of its own. As with [T-079](T-079-the-boards-dependency-columns-list-closed-tasks.md)
the change is upstream's, so the outcome here is a decided behaviour and a proposal carrying it,
delivered the same way.

**Why this one**
**This project states results as what was actually produced**, so pasted tool output is everywhere
in the task record — and `taskmd index` emits markdown links by construction, one per row. Quoting a
board row therefore puts a bracketed id followed by a parenthesised filename inside a fence, and
`check` resolves it as a live link.

**What it cost, 2026-08-10.** Drafting T-079's proposal, a row was pasted as evidence with the
filename abridged to an ellipsis. The run went red:

```
BROKEN LINK   tasks/T-079-the-boards-dependency-columns-list-closed-tasks.md -> …

1 problem(s) over 78 task(s)
```

The fix was to paste a *resolvable* link instead. **That is the part worth fixing: the checker did
not find a defect, it edited the evidence.** A quotation that has to be adjusted to satisfy a link
checker is no longer a quotation, and the adjustment is invisible to whoever reads it later.

**Why this is not the same ask as `refcheck`'s.** [`refcheck.py`](../tools/docs/refcheck.py)
deliberately reads inside fences — *every repo-relative `.md` path written in prose or printed by a
tool* — and that has caught real defects, so **blanket fence-skipping is the wrong proposal** and
this project would not want it. The narrow claim is about **link syntax**: a bracketed label with a
parenthesised target renders, inside a fence or a code span, as literal characters — nobody can
follow it and it cannot be broken. A bare path in a fence is a different thing and may stay checked.

**Scope**
- In: markdown-link syntax inside fenced code blocks, in `check`'s link resolution.
- In: **inline code spans, which behave the same** — measured, not assumed. Writing this task
  reproduced the defect three more times in one run, every one of them a link-shaped example wrapped
  in backticks in prose. **A task describing the defect could not be written without committing it**,
  which is the strongest statement of it available and is why the examples above are now paraphrased
  rather than shown.
- In: the proposal, delivered as a task in taskmd's tracker the way T-079's was — same maintainer,
  and the two pair naturally.
- Out: bare paths inside fences, and any change to `refcheck.py`, which wants them.

**Inputs**
- [T-079](T-079-the-boards-dependency-columns-list-closed-tasks.md) §3 — the fence that triggered it
  and the channel the proposal goes through.
- [T-063](T-063-improvements-to-propose-upstream-to-taskmd.md) — the five earlier proposals, and the
  house format for one.

**Acceptance criteria**
- [ ] The behaviour is decided and written down, including that inline spans were left alone and why.
- [ ] The proposal is delivered upstream and named here.
- [ ] A task file in this repository can quote a `taskmd index` row verbatim, abridged filename and
      all, and `python tools/tasks/lint.py` stays green.
- [ ] If upstream declines, the workaround is written down where a task author will meet it —
      `TASK-WORKFLOW.md`, not this file.

**Open questions**
- none.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Reproduce against the current source, and check whether inline spans behave the same | this file §1, **done 2026-08-10** |
| 2 | Write the proposal | taskmd's own **T-112**, **done 2026-08-10** |
| 3 | Deliver it as a task in taskmd's tracker | **done 2026-08-10** |

## 3. Implement

**Decisions & assumptions**
- **Argue it from taskmd's own T-092, not from this project's practice** — 2026-08-10. T-092 decided
  that a bare path in prose is not a reference, separating a pointer from *a path merely being
  discussed*, and its acceptance criteria demanded that a false-positive boundary be **proven rather
  than asserted**. Link syntax inside a fence is that same boundary one syntax over, so the ask is
  consistency with a decision they have already taken rather than a new rule from an adopter. The
  mechanism confirms it was never decided: `LINK.finditer` runs over the whole file text with no
  notion of a fence.
- **Do not ask for blanket fence-skipping** — 2026-08-10, as scoped. Bare paths inside fences stay
  checked upstream and here: `refcheck.py` reads them deliberately and has caught real defects, so
  the two tools disagree about paths on purpose and only agree about link syntax.

**Outputs produced**
- The proposal, delivered as **T-112**, *Stop check resolving a link that is displayed rather than
  navigable*, in taskmd's own tracker — same channel as T-079's, left for the maintainer to index.
  Named by id and title rather than by path, since the file is in another repository.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-10 | (implement) | **Received upstream**, with T-111 — taskmd informed, reindexed, project updated. Their decision is not known here and is not assumed. Until it lands, the workaround stands and is written where a task author meets it: paraphrase link syntax, or paste a target that really resolves. |
| 2026-08-10 | → in_progress | **Delivered as taskmd's T-112**, the same channel as T-079. Reading their source first moved the argument onto their own T-092, which had already separated a pointer from a path being discussed and had asked for false-positive boundaries to be proven — so this is a gap in enforcement of a settled rule, not a request for a new one. Their repository is green on this today only because no task there quotes an index row; the defect belongs to whoever pastes the tool's own output, which is this project's method. One consequence found while writing: `links += 1` runs on every match, so the count their T-095 added to the summary is inflated by strings nobody can follow. Open on their side; nothing outstanding here. |
| 2026-08-10 | → proposed | Raised on the owner's word after the defect turned a run red while T-079's own proposal was being drafted. `medium` because this project pastes tool output as a matter of method and `index` output carries a link per row, so it recurs rather than being one bad afternoon; `xs` because the change is upstream's and the ask is narrow. Kept out of T-079 deliberately: that task is scoped to `index`, and one task carrying two unrelated upstream defects is harder to close than two carrying one each. |
