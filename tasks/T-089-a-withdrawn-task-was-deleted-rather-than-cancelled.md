---
id: T-089
title: A task withdrawn on a false premise was deleted rather than cancelled, and no rule said which
type: admin
status: done
phase: review
parent: null
blocked_by: []
related: [T-003, T-069]
work_package: PH3
shipped_in: 0.2.1
owner: the project owner
business_value: low
effort: xs
created: 2026-08-11
updated: 2026-08-12
deliverables:
  - tasks/T-072-a-corrupted-comment-opener-in-shell-components-css.md
  - tasks/TASK-WORKFLOW.md
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
- [x] `TASK-WORKFLOW.md` states the disposal, and states it as a rule rather than as an anecdote: a
      task withdrawn because its premise was false is `cancelled`, not deleted.
- [x] The rule says why, in one clause — a deleted ID resolves to nothing, and the next reader has no
      way to know whether it was withdrawn or lost.
- [x] `tasks/T-072-*.md` exists, is `cancelled`, and cites T-069 and L-56.
- [x] The stub is marked as reconstructed and dated, so it is not mistaken for the original file.
- [x] `python tools/tasks/lint.py` is green, and the board shows no gap between T-071 and T-073.

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
- **The rule went into §3.1, not §5.** §1 named §5 *Statuses*; that section is *The log*, and the
  status vocabulary is §3.1. Corrected in passing rather than handed back — the rule belongs beside
  the sentence naming `done` and `cancelled` as the closed statuses, which is where a reader deciding
  between them is standing.
- **The stub carries no `work_package`, and says so.** The original's was never recorded anywhere
  that survives. Several closed tasks already show `-` in that column, so the absence is a shape the
  board holds; inventing `PH2` from the date would have been the reconstruction claiming to know
  something it does not, in the one file whose entire purpose is to be honest about what is left.
- **No acceptance criteria, plan or implementation in the stub either.** It was withdrawn in
  `specify` and never had them. Plausible ones would make it a forgery rather than a record.
- **Its `→ cancelled` row is dated to the reconstruction, not the withdrawal.** That is when the file
  came to exist. The withdrawal keeps its own row at 2026-08-10, so the two facts stay apart.

**Outputs produced**
- [T-072](T-072-a-corrupted-comment-opener-in-shell-components-css.md) — the stub, headed by a
  blockquote saying it is a reconstruction, what it was built from, and that no original survives in
  the tree or in history.
- [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §3.1 — the disposal rule, its one-clause reason, and a note
  naming both instances: the hole T-072 was, and T-003 as the precedent that was already right.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| `TASK-WORKFLOW.md` states the disposal as a rule | met | §3.1, in the imperative and in its own paragraph — *a task withdrawn because its premise proved false is `cancelled`, and its file is kept. It is never deleted.* The instance sits below it in italics, so the rule reads without the anecdote. |
| The rule says why, in one clause | met | *A deleted ID resolves to nothing, so the next reader cannot tell withdrawn from lost.* |
| `tasks/T-072-*.md` exists, is `cancelled`, cites T-069 and L-56 | met | Both cited, and both as the *sources* of its content rather than as related reading — the point of the file is that it is second-hand. |
| The stub is marked as reconstructed and dated | met | A blockquote before §1, carrying the date, the author task, the two sources, and the `git log --diff-filter=A` result that establishes nothing survives to reproduce. |
| `lint.py` green, no gap between T-071 and T-073 | met | `OK - 92 task(s)` (91 before), refcheck `0 broken`, and the board's closed table runs T-071, T-072, T-073 with no gap. |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-11 | (shipped) | **Shipped in `0.2.1`.** The disposal rule and the reconstituted `T-072` stub travel with the repository rather than with the plugin, so this is the release they became public in. |
| 2026-08-11 | → done | All five criteria met. **The rule was the cheap half; the stub is what makes it true.** A disposal rule saying *retain* while its only instance stayed deleted would have left exactly the hole it was written to close, which is why section 1 scoped both together. Two things the reconstruction had to refuse: a work package and a set of acceptance criteria, both easy to infer and neither recorded anywhere that survives - a reconstructed file that fills its own gaps is worse than the deletion it repairs, because it reads as evidence. Section 1 also pointed the rule at section 5, which is *The log*; it went to section 3.1 beside the status vocabulary instead. |
| 2026-08-11 | → proposed | Raised from the pre-PH3 audit, which found the T-072 hole by counting index rows against filenames — 87 files against IDs running to T-088. The owner settled both questions the audit put: **`cancelled` and retained**, and **`PH3`**. `PH3` is against the size rule, which sends `xs` to PH2 — recorded here rather than left to be re-derived, because PH2 has shipped and reopening it is reserved for adopter defects, which this is not. `low` value: it costs nobody anything today, and the audit that found it was not a gate and does not repeat. |
