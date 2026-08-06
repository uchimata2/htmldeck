---
id: T-029
title: Stop the deliverable exemption silently dropping pointers from the check
type: fix
status: proposed
phase: specify
parent: T-026
blocked_by: []
related: [T-018]
work_package: none
owner: maintainer
created: 2026-08-06
updated: 2026-08-06
deliverables: [tools/tasks/task.py, tasks/TASK-WORKFLOW.md]
---

# T-029 — Stop the deliverable exemption silently dropping pointers from the check

## 1. Specify

**Outcome**
`task.py check` stops exempting pointers to files that **already exist**, and stops doing it
**differently depending on how the pointer is written**. Today, declaring a path in any task's
`deliverables:` removes every repo-relative mention of that path from validation — permanently, for
every document in the repository, with no output saying so. The exemption keeps the one job it was
written for (a deliverable that has not been produced yet is not a dead pointer) and loses the
coverage it takes silently.

**How it was found**
[T-026](T-026-settle-who-scores-a-deck-and-whether-the-score-is-shown.md) briefly declared
`docs/LESSONS.md` — a file that has existed for weeks — as one of its deliverables. The checked
pointer count **fell by six** and `check` still printed `0 broken`. Nothing in the output
distinguished "six pointers are fine" from "six pointers are no longer looked at". That is the exact
shape **L-05** is about: a check that quietly narrows what it covers reports the same clean line as
one that covers everything.

**The two defects, both in `tools/tasks/task.py`**

| # | Defect | Where |
| :-- | :--- | :--- |
| 1 | **The exemption is unconditional on existence.** `declared` is built from every task's `outputs` regardless of status or whether the file is on disk, and membership alone skips the pointer. The stated rationale — *"that is a promise about the future"* — does not hold for a path that is already there. | the `declared` set, and the `target in declared` test in the pointer loop |
| 2 | **It matches only one written form.** The test compares the **raw link target** against **normalised repo-relative** strings, so `` `docs/LESSONS.md` `` written in prose is exempt while `[…](../docs/LESSONS.md)` written from `tasks/` is not — same file, same repository, opposite treatment. The exemption's coverage is therefore set by where a pointer happens to be written. | same test |

Defect 2 is why the loss was six rather than every mention: only the repo-relative form matched.

**This task demonstrates the defect on itself, and that is the cheapest test available.** Its
`deliverables:` declares `tools/tasks/task.py` and `tasks/TASK-WORKFLOW.md` — both of which have
existed since the repository did. Measured 2026-08-06 by toggling that one line and re-running
`check`: **247 pointers with the declaration, 251 without.** The declaration is correct and stays —
those files *are* this task's outputs — so **the fix is done when that difference is zero.** No
scratch task is needed; the task's own front-matter is the fixture.

**Scope**
- In: making the exemption **conditional on the target not existing**, so an existing file is checked
  no matter who declared it.
- In: resolving the pointer **before** testing it against `declared`, so the two forms behave the
  same. Which way that resolves — normalise both to repo-relative, or drop the string test for a
  path test — is the implementer's call.
- In: **saying what was skipped.** `check`'s output must state how many pointers were exempted and
  why, so a future narrowing is visible rather than silent. This is the part that makes the fix
  hold; the rest can regress without anyone noticing again.
- In: [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §6, whose *What `check` enforces* list states the
  exemption and must state the corrected rule. That file is the specification `task.py` enforces —
  where the two disagree, one of them is a bug.
- Out: changing what counts as a pointer, or the `.gitignore` half of the rule. Neither is implicated.
- Out: any change to `deliverables:` as a field, or to `task.py deliverables`.

**Inputs**
- `tools/tasks/task.py` — the pointer loop in `cmd_check`, and the comment above it that states the
  rationale being corrected
- [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §6 — what `check` enforces, and what it explicitly does not
- [`../docs/LESSONS.md`](../docs/LESSONS.md) — **L-05**, on what a check may claim
- [T-026](T-026-settle-who-scores-a-deck-and-whether-the-score-is-shown.md) §4 — the finding as
  recorded when it was hit
- [T-018](T-018-measure-the-printable-mode-what-printing-from-fi.md) — the one task with an
  undelivered deliverable, so it is the live case the exemption exists for. Its pointers to
  `docs/research/R7-printable-mode.md` must keep passing.

**Acceptance criteria**
- [ ] Declaring an **existing** file as a deliverable does not change the checked-pointer count.
      Verified on this task's own front-matter: emptying `deliverables:` and restoring it must give
      the **same** count, where today it gives 251 and 247. Verified again with `docs/LESSONS.md`
      written in both forms, since defect 2 makes the form matter
- [ ] A pointer to a deliverable that **does not exist yet** is still exempt — T-018's
      `docs/research/R7-printable-mode.md` keeps passing, in whichever form it is written
- [ ] A **dead** pointer to a path no task declares is still reported. The fix must not be
      "exempt less" achieved by exempting nothing and breaking the repository
- [ ] `check`'s output states the number of pointers exempted, not only the number checked
- [ ] `TASK-WORKFLOW.md` §6 describes the corrected rule
- [ ] `python tools/tasks/task.py check --closing` passes on the whole repository

**Open questions**
- **Does the exemption earn its place at all?** T-018 is its only live case, and a task could instead
  write an undelivered output as plain text rather than a pointer. Deleting the exemption is a
  smaller change than fixing it, and one fewer rule for `check` to get subtly wrong. — maintainer

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Baseline recorded — 247 with this task's `deliverables:` declared, 251 with it emptied | the difference the fix must close to zero |
| 2 | Decide the open question — fix the exemption, or delete it | a decision in §3 |
| 3 | Apply it, resolving the pointer before the `declared` test and gating on existence | corrected `task.py` |
| 4 | Add the exempted count to `check`'s output line | a check that says what it skipped |
| 5 | Re-run the four criteria above, including the deliberate re-declaration of `docs/LESSONS.md` | measured results in §4 |
| 6 | Correct `TASK-WORKFLOW.md` §6 | the specification and the tool agreeing |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- `tools/tasks/task.py`
- `tasks/TASK-WORKFLOW.md`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-06 | → proposed | Raised from [T-026](T-026-settle-who-scores-a-deck-and-whether-the-score-is-shown.md) §4, where declaring an existing file as a deliverable dropped six pointers out of validation while `check` still printed `0 broken`. Two defects, not one: the exemption ignores whether the file exists, and it matches only the repo-relative written form. **The output change is the part that matters** — the first defect cost coverage, but printing `0 broken` over a silently narrowed set is what stopped anyone noticing (**L-05**). |
