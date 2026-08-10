---
id: T-089
title: A task withdrawn on a false premise was deleted rather than cancelled, and no rule said which
type: admin
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-003, T-069]
work_package: v0.3
owner: the project owner
business_value: low
effort: xs
created: 2026-08-11
updated: 2026-08-11
deliverables: []
---

# T-089 — A task withdrawn on a false premise was deleted rather than cancelled, and no rule said which

## 1. Specify

**Outcome**
`tasks/TASK-WORKFLOW.md` states which disposal a withdrawn task gets, and the one existing instance
matches it. A task raised on a premise that proves false is closed `cancelled` and its file is kept,
so the ID answers for itself instead of resolving to nothing.

**Why this one**
**The ID sequence has a hole at T-072 and the board gives no hint of it.** The task was raised during
[T-069](T-069-extend-the-provenance-mark-to-multiple-sources.md) for a corrupted comment opener in
`shell/components.css` that would swallow the rule beneath it; the mechanism was right and the
character was never there — a search tool's escaping rather than a byte, recorded as **L-56**. The
file was then deleted, and it was deleted before it was ever committed, so **it is absent from git
history as well as from the working tree**: `git log --diff-filter=A -- 'tasks/T-072*'` returns
nothing. What survives is two sentences in another task's implement log and its `→ planned` row.

That is one indirection too many. Every other closed task answers at its own ID, including the one
other withdrawal: [T-003](T-003-brief-mode-elicit-the-six-section-prompt.md) is `cancelled` and
retained, and reading it explains itself without knowing which task cancelled it. **Two disposals for
withdrawn work, no written rule, and the quieter one leaves no record at the ID anyone would look
up.** The audit of 2026-08-11 found the hole by counting index rows against filenames, which is not a
gate and will not run again by itself.

**The rule is the owner's, decided 2026-08-11: `cancelled` and retained.** This task writes it down
and applies it to T-072. It does not reopen the question.

**Scope**
- In: the disposal rule in [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md), next to the status vocabulary that
  already names `cancelled` as a closed status — the sentence is missing, not the vocabulary.
- In: **T-072 reconstituted as a `cancelled` stub.** A rule that says *retain* while its only
  instance stays deleted leaves exactly the hole the rule exists to close.
- In: the stub is explicit that it is written after the fact from **L-56** and T-069's log, and does
  **not** reproduce a file that no longer exists. It records what was raised, why it was withdrawn,
  and where the lesson lives.
- Out: any change to `.taskmd/config.md`. The vocabulary already carries `cancelled`; what is missing
  is guidance on when to reach for it, and that is `TASK-WORKFLOW.md`'s job by its own §4 precedent.
- Out: an upstream proposal. Nothing here is taskmd's behaviour — `check` is right to say nothing
  about an ID that was never created.
- Out: re-litigating L-56 or T-069's finding. The premise was false; that is settled and is the
  reason the stub exists rather than an argument against it.

**Inputs**
- [T-069](T-069-extend-the-provenance-mark-to-multiple-sources.md) §3 — the withdrawal, in the
  *Decisions & assumptions* list, and the `→ planned` log row that raised it.
- [`docs/LESSONS.md`](../docs/LESSONS.md) — **L-56**, the trap itself.
- [T-003](T-003-brief-mode-elicit-the-six-section-prompt.md) — the retained-`cancelled` precedent, and
  the shape a withdrawn task's file takes here.
- [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §5 *Statuses* — where `cancelled` is already enumerated.

**Acceptance criteria**
- [ ] `TASK-WORKFLOW.md` states the disposal, and states it as a rule rather than as an anecdote: a
      task withdrawn because its premise was false is `cancelled`, not deleted.
- [ ] The rule says why, in one clause — a deleted ID resolves to nothing, and the next reader has no
      way to know whether it was withdrawn or lost.
- [ ] `tasks/T-072-*.md` exists, is `cancelled`, and cites T-069 and L-56.
- [ ] The stub is marked as reconstructed and dated, so it is not mistaken for the original file.
- [ ] `python tools/tasks/lint.py` is green, and the board shows no gap between T-071 and T-073.

**Open questions**
- none. The disposal and the work package were both settled by the owner on 2026-08-11.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Read T-069 §3 and its `→ planned` row, and L-56, for everything that survives about T-072 | the stub's content, sourced rather than recalled |
| 2 | Write the stub at T-072's ID, `cancelled`, marked reconstructed | `tasks/T-072-*.md` |
| 3 | Write the disposal rule into `TASK-WORKFLOW.md` §5 | the rule and its one-clause reason |
| 4 | `python tools/tasks/lint.py` | index regenerated, check and refcheck green |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- `tasks/...`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-11 | → proposed | Raised from the pre-v0.3 audit, which found the T-072 hole by counting index rows against filenames — 87 files against IDs running to T-088. The owner settled both questions the audit put: **`cancelled` and retained**, and **`v0.3`**. `v0.3` is against the size rule, which sends `xs` to v0.2 — recorded here rather than left to be re-derived, because v0.2 has shipped and reopening it is reserved for adopter defects, which this is not. `low` value: it costs nobody anything today, and the audit that found it was not a gate and does not repeat. |
