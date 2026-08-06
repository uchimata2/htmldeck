---
id: T-029
title: Stop the deliverable exemption silently dropping pointers from the check
type: fix
status: done
phase: review
parent: T-026
blocked_by: []
related: [T-018]
work_package: none
owner: maintainer
created: 2026-08-06
updated: 2026-08-07
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
  undelivered deliverable, so it is the live case the exemption exists for. Its references to
  `R7-printable-mode.md` are what any change here has to keep working.

**Acceptance criteria**
- [ ] Declaring an **existing** file as a deliverable does not change the checked-pointer count.
      Verified on this task's own front-matter: emptying `deliverables:` and restoring it must give
      the **same** count, where today it gives 251 and 247. Verified again with `docs/LESSONS.md`
      written in both forms, since defect 2 makes the form matter
- [ ] A task can still **declare a deliverable that does not exist yet** — T-018 keeps passing,
      and `task.py deliverables` still reports `R7-printable-mode.md` as declared and not on disk
- [ ] A **dead** pointer to a path no task declares is still reported. The fix must not be
      "exempt less" achieved by exempting nothing and breaking the repository
- [ ] `check`'s output states the number of pointers exempted, not only the number checked
- [ ] `TASK-WORKFLOW.md` §6 describes the corrected rule
- [ ] `python tools/tasks/task.py check --closing` passes on the whole repository

**Open questions**
- ~~**Does the exemption earn its place at all?**~~ **Answered 2026-08-07: no — delete it.** The
  owner ruled for deletion over repair. The anticipated cost was right: two prose references now
  name their unproduced file instead of pointing at it. What the question did not anticipate is
  that deletion needs front-matter excluded from the scan, or no task can declare an unproduced
  output at all — see §3.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Baseline recorded — 247 with this task's `deliverables:` declared, 251 with it emptied | the difference the fix must close to zero |
| 2 | Decide the open question — fix the exemption, or delete it | **deleted**; §3 |
| 3 | Delete the `declared` set and its test; stop scanning front-matter, or nothing can declare an unproduced output | corrected `task.py` |
| 4 | Report what was **not** scanned on the OK line | a check that says what it skipped |
| 5 | Re-run the four criteria above, including the deliberate re-declaration of `docs/LESSONS.md` | measured results in §4 |
| 6 | Correct `TASK-WORKFLOW.md` §6 | the specification and the tool agreeing |

## 3. Implement

**Decisions & assumptions**

- **The open question is answered: delete the exemption, do not fix it.** — owner, 2026-08-07.
  One fewer rule for `check` to get subtly wrong, and the exemption's only live case (T-018) turned
  out not to need it.
- **The deletion could not be total, and the reason is load-bearing.** `deliverables:` is *itself*
  pointer-shaped — a declaration naming `R7-printable-mode.md` under `docs/research/` matches the
  pointer pattern like any prose mention would. With the exemption simply removed, **a task could not declare an
  unproduced output at all**, which contradicts `task.py deliverables` existing to report on
  exactly those. So one narrow rule replaces it: **front-matter is not scanned for pointers.**
  — 2026-08-07
- **Why that is not the same rule wearing a new hat.** The old exemption keyed on the *target*: one
  declaration exempted that path in every document in the repository, permanently, with no way to
  see it had happened. The new one keys on the *site*: one field, in the one file that declares it,
  and it is impossible to trigger by naming a file someone else cites. It cannot widen. — 2026-08-07
- **Scope changed, and it is recorded rather than smoothed over.** §1 put *"changing what counts as
  a pointer"* out of scope. Not scanning front-matter is exactly that, and it was written when the
  plan was to fix the exemption rather than delete it. The ruling forced it; the alternative was a
  tool that cannot express an unproduced deliverable. — 2026-08-07
- **The measured cost was 15× the reported one.** The finding said six pointers. Deleting the
  exemption took the checked count from **247 to 357** — it had been hiding **110**, because most
  declared deliverables are long-lived documents (`DESIGN-SYSTEM.md`, `EVALUATION.md`, the R-notes,
  `task.py`, `TASK-WORKFLOW.md`) that the rest of the repository cites constantly. Six was what one
  new declaration added, not what the rule was costing. — 2026-08-07
- **Two prose references had to change form**, which is the price the ruling accepts: T-018's plan
  step and outputs list now name `` `R7-printable-mode.md`, under `docs/research/` `` instead of
  pointing at a file that does not exist. The front-matter still carries the real path.
  — 2026-08-07

**Outputs produced**
- `tools/tasks/task.py` — the `declared` set and its test deleted; `strip_front_matter` added and
  applied to the pointer scan; the OK line now reports what was **not** scanned
- [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) — §3's `deliverables` row and §6's enforcement list state
  the corrected rule, including how to write an output that does not exist yet
- [T-018](T-018-measure-the-printable-mode-what-printing-from-fi.md) — its two prose references to
  the undelivered R7 rewritten as a name plus its directory

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Declaring an **existing** file as a deliverable does not change the checked-pointer count | **met** | Measured on this task's own front-matter: **357 declared, 357 emptied**, where the baseline was 247 and 251. Repeated with `docs/LESSONS.md` — the file that produced the original finding — added to the declaration: still 357. |
| A task can still **declare a deliverable that does not exist yet** | **met** | T-018 passes; `task.py deliverables` still reports 26 declared outputs, **1 not on disk yet**. |
| A **dead** pointer to a path no task declares is still reported | **met** | Injected a path-shaped reference to a non-existent `R99` note under `docs/research/` into prose → `DEAD POINTER` reported. Injected the same path *as a declared deliverable and* in prose → **also reported**, where before the deletion it would have been silently exempt. That second case is the whole point. Both injections were reverted; this task file names no path-shaped string that does not resolve, which `check` is what confirms. |
| `check`'s output states the number of pointers exempted, not only the number checked | **met, reworded by the ruling** | With the exemption deleted there is no per-pointer exemption left to count, so the criterion's literal form has nothing to report. What it was written to prevent is served instead: the OK line now reads `12 document(s) not scanned (.gitignore); front-matter is not scanned.` — the two remaining silences, stated. |
| `TASK-WORKFLOW.md` §6 describes the corrected rule | **met** | §6 states both skips and that `check` prints them, and records what the deleted exemption had been costing. §3's `deliverables` row says how to write an unproduced output. |
| `python tools/tasks/task.py check --closing` passes on the whole repository | **met** | `OK - 29 tasks, ... 357 document pointer(s) checked, 0 broken`. |

**The 110 is the finding worth carrying**, and it is now **L-30**. The task was raised over six
pointers, which is what one new declaration cost. The rule had been costing **110 of 357** — nearly
a third of the repository's pointers unchecked — and no output had ever said so. **The number a
defect is reported at is the number someone happened to measure**, not the number it is worth. The
generic form, in [`../docs/LESSONS.md`](../docs/LESSONS.md): an exemption keyed on a *value* has no
fixed size, so prefer one keyed on a *site* — which is exactly the trade this fix made.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-07 | → done | **Owner ruled: delete the exemption rather than fix it.** Deletion could not be total — `deliverables:` is itself pointer-shaped, so removing the exemption outright would make declaring an unproduced output impossible. One narrow rule replaces it: front-matter is not scanned. That keys on the *site* rather than the *target*, so unlike its predecessor it cannot widen beyond the one field that declares it. **The exemption had been hiding 110 of 357 pointers**, not the six the task was raised over — six was one new declaration's marginal cost, not the standing one. §1 had put "changing what counts as a pointer" out of scope; the ruling forced it, and §3 records that rather than smoothing it over. |
| 2026-08-06 | → proposed | Raised from [T-026](T-026-settle-who-scores-a-deck-and-whether-the-score-is-shown.md) §4, where declaring an existing file as a deliverable dropped six pointers out of validation while `check` still printed `0 broken`. Two defects, not one: the exemption ignores whether the file exists, and it matches only the repo-relative written form. **The output change is the part that matters** — the first defect cost coverage, but printing `0 broken` over a silently narrowed set is what stopped anyone noticing (**L-05**). |
