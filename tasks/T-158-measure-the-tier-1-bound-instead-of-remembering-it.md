---
id: T-158
title: Measure the tier-1 bound instead of remembering it
type: fix
status: done
phase: review
parent: T-130
blocked_by: []
related: [T-130, T-134, T-143, T-144, T-152, T-153]
work_package: PH3
shipped_in: 0.3.0
owner: the project owner
business_value: medium
effort: s
created: 2026-08-14
updated: 2026-08-15
deliverables: [tools/docs/figures.py]
---

# T-158 — Measure the tier-1 bound instead of remembering it

## 1. Specify

**Outcome**
The two figures in [`../CLAUDE.md`](../CLAUDE.md)'s tier-1 bound are checked by something that runs on
a trigger this project already has, so a drift is reported rather than discovered by the next session
that happens to re-measure.

**Why it exists**
Raised at [T-153](T-153-run-the-audit-methods-phase-2-over-this-repositorys-own-audit.md)'s review, as
the acceptance criterion that task closed **not met**. `R8` §3.1 step 16 requires phase 2 to leave at
least one thing that re-measures without being asked; phase 2 could not, and the reason is a collision
rather than a difficulty. [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §10.4 is the report.

**The evidence, and it is about this repository's most-paid number.**
- Tier 1 measured **15,034** when T-152 closed and **15,208** hours later. **174 bytes drifted and
  nothing reported it.**
- `CLAUDE.md`'s own debt statement records that it *has now been wrong in both terms twice*.
- `python tools/docs/figures.py` reads both figures as **unanchored** — *in a sentence naming no
  field* — among 413 others. The file carries the measuring command in a fence and pastes no output,
  which is the one shape that tool cannot bind.

**Scope**
- In: a mechanism that compares the stated pair against the measured pair, on an existing trigger —
  `tools/tasks/lint.py` or `tools/check_all.py`, not a new entry point.
- In: **the reporting level.** `CLAUDE.md` is knowingly over its bound, so a check that fails on the
  inequality blocks every release until a debt this project has chosen to carry is paid. What must
  fail is the **stated figure disagreeing with the measured one**, which is a fact about the page and
  not a design choice (`CLAUDE.md`, *a check that forbids a design choice is a defect in the check*).
- In: a self-test on a synthetic fixture, not on the current contents of a tracked file (**L-78**,
  **L-85**) — the fixture rule matters more than usual here, because the subject *is* a tracked file
  whose size this task will change.
- Out: changing the bound, its comparison set, or which document owns the figures. **This task makes
  an existing rule enforceable; it does not re-open it.**
- Out: picking a side in the collision below. That is the open question and it is the owner's.

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §10.4 — the collision, both routes, and why
  neither is takeable without a ruling
- [`../CLAUDE.md`](../CLAUDE.md) *What loads every turn* — the bound, the command, and the rule that a
  figure about that file cannot be corrected anywhere else
- [`../tools/docs/figures.py`](../tools/docs/figures.py) — the mechanism that exists for this shape,
  and the reason it cannot see this instance

**Acceptance criteria**
- [ ] The stated pair is compared against the measured pair on a trigger that already runs
- [ ] A seeded drift in either term fails, in both directions, demonstrated rather than asserted
- [ ] The inequality being unmet does **not** fail anything — only a stated figure disagreeing with the
      measured one does
- [ ] The self-test builds its own instance and does not read the live `CLAUDE.md`
- [ ] `CLAUDE.md`'s byte cost of this change is stated, and it is zero or argued

**Open questions**
- ~~**Which rule yields?**~~ **Settled by the owner 2026-08-14: neither.** Teach `figures.py` to run a
  fenced command whose output is **not** pasted, and compare its result against the prose figures in
  the same document. **Both settled rules stand and tier 1 gains nothing** — the file already carries
  the command in a fence, so the change is to the tool's reach rather than to any page.

  *The two routes that were refused, kept because a later session will rediscover them:* pasting the
  command's output beside the figure lands new bytes on surface A, the file the audit was cutting;
  moving the figures out contradicts *a figure about this file cannot be corrected anywhere else*,
  which was itself written because a session recorded the pair elsewhere and left it wrong. Each is
  cheaper to implement than the chosen route and each spends a rule. **L-100** is the general form.

  **What this makes the task.** A change to `figures.py`'s fence handling, not a change to any policy
  — which also means the acceptance criteria below are unchanged and criterion 5 is now trivially
  satisfiable rather than argued.

## 2. Plan

**The comparison is presence, not label-binding, and that is the plan's one real decision.**
`figures.py` binds a prose numeral by making its sentence name the label a command printed. Measured
against this page, that rule fails in both directions at once: the live sentence says *"15,208 bytes
against `tasks/TASK-WORKFLOW.md`'s 11,925"* and names no `CLAUDE.md`, so the first term binds
**nothing**; while the record sentence beside it says *"it read 18,807 against `.taskmd/config.md`'s
14,087"*, which names a label the command **does** print and would be reported `STALE` for stating a
figure that was true in the past. One term unwatched and one false alarm — which is T-068's measured
result reappearing, and the reason `declared()` already says these pages *"are not accounts of
command output"*.

So the direction inverts: rather than *every written numeral must be printed*, the rule is **every
measured term must be written**. A term the page does not state fails; a numeral the page states and
no longer measures is a record and is not judged. This is the only rule of the two that can be right
about a page which deliberately keeps its own history.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | `run()` splits with `shlex`, not `str.split` — a fence carrying `python -c "…"` is one argument and `.split()` shreds it | `run()` executes a quoted command |
| 2 | Declare `MEASURED`: which document carries a measurement fence, the command prefix that authorises it, and the subject path. **Its own allowlist** — `RUNNABLE` is untouched, so no shape-rule widening lets a document run what it likes | `MEASURED`, and a per-document grant |
| 3 | `missing_measurements()` — a declared fence the document no longer carries fails the run, on `ARTIFACTS`' and `ACCOUNTS`' condition: a hand-kept list is allowed only where it cannot cover nothing quietly | the entry cannot go stale in silence |
| 4 | `measurement()` — run the fence, read `<size> <path>` lines into `{path: size}`, separators normalised (`pathlib` prints `docs\BRIEF.md` on Windows and `docs/BRIEF.md` elsewhere) | the six sizes, keyed by path |
| 5 | `measured_pair()` — the pair is *(the subject's own size, the smallest of the rest)*, which is the page's bound restated as arithmetic over the same output. Nothing is hand-kept but the subject | `(15208, 11925)` today |
| 6 | `measured_rows()` — each term must appear as a prose numeral in that document, commas normalised (`15,208` vs `15208`). Absent → `STALE`, which the existing `fails` sum already counts | the verdict |
| 7 | Wire into `declared()` and `report()`; print the pair and the path each term came from, because a binding nobody can read is a claim (**L-63**) | a readable row |
| 8 | Self-test: a synthetic document with a synthetic fence, seeded four ways — each term stated too high and too low — plus one fixture whose declared fence is gone | four reds and one, judged by message |

## 3. Implement

**Decisions & assumptions**
- **The comparison inverts: every measured term must be written, not every written numeral measured**
  — 2026-08-15. Forced by measuring the page, not chosen: label-binding leaves the first term
  unwatched and reports the record sentence beside it `STALE`. Generalised as **L-104**.
- **`RUNNABLE` is untouched; the grant is per-document** — 2026-08-15. Widening that allowlist's
  *shape* to admit `python -c` would let any fence in any scanned page run arbitrary code, which is
  the opposite of what it exists for. `MEASURED` authorises one command prefix in one named document,
  and `missing_measurements()` fails when the document stops carrying it — `ARTIFACTS`' and
  `ACCOUNTS`' condition, so a hand-kept grant cannot come to cover nothing quietly.
- **Only the subject is declared; the other term is derived** — 2026-08-15. The pair is *(the
  subject's own size, the smallest of the rest)*, which is the page's own bound as arithmetic over
  the same output. Naming the second document anywhere would be a third copy of a fact that has
  already changed hands twice.
- **A measured value counts once, however often the page states it** — 2026-08-15. `15,208` appears
  twice; both occurrences leave `unanchored`, which is the rule the block's own claims already follow
  through `spoken`. Measured: `unanchored` 413 → 410, `compared` 21 → 23.
- **Found while fixturing, and left alone: `PROSE_NUMERAL` cannot match a figure that ends a
  sentence** — the `.` is excluded so `0.2.4` is not read as two numerals. It is pre-existing, out of
  this task's scope, and it fails **loudly** here rather than silently: a figure moved to the end of a
  sentence reads as *not stated* and reddens the run. Noted rather than fixed.

**Outputs produced**
- [`tools/docs/figures.py`](../tools/docs/figures.py) — `shlex` splitting in `run()`; `MEASURED`,
  `doc_text`, `measurement_fence`, `missing_measurements`, `measurement`, `measured_pair`,
  `measured_rows`; wired into `declared()` and `report()`; self-test fixture 13 and one live guard.
- [`docs/lessons/L-104.md`](../docs/lessons/L-104.md) and its row in
  [`docs/LESSONS.md`](../docs/LESSONS.md).
- **No change to `CLAUDE.md`.** It is 15,208 bytes before and after.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The stated pair is compared against the measured pair on a trigger that already runs | met | `figures.py` is already in `tools/check_all.py`'s `WIDE` manifest. No entry point was added. The report now prints `CLAUDE.md  15208 CLAUDE.md, 11925 tasks/TASK-WORKFLOW.md` under *what a document measures itself*. |
| A seeded drift in either term fails, in both directions, demonstrated rather than asserted | met | Demonstrated twice over. Through the real `declared()` path on the live page's text held in memory: `15,208 → 15,209` gives `STALE … measures CLAUDE.md at 15208 and the page states no such figure`, and `11,925 → 11,924` the same for `tasks/TASK-WORKFLOW.md`. In the self-test, fixture 13 seeds **four** ways — each term stated one too high and one too low — because a figure goes stale by the file growing *or* by the page being edited wrong, and only one of those moves the number down. |
| The inequality being unmet does **not** fail anything — only a stated figure disagreeing with the measured one does | met | `measured_pair()` computes the two values and never compares them to each other; there is no `<` in the path. The run is green today with the bound knowingly unmet at 15,208 against 11,925. |
| The self-test builds its own instance and does not read the live `CLAUDE.md` | met | Fixture 13 is a synthetic page carrying a synthetic fence that prints `1300 a.md / 1100 b.md / 2000 c.md`; `measured_rows` and `missing_measurements` both take their document text and their entry as arguments. The one live assertion is `missing_measurements()` — *is anything watching* — never *is the figure current*, so a real drift reddens the run instead of crashing the test (**L-78**, **L-85**). |
| `CLAUDE.md`'s byte cost of this change is stated, and it is zero or argued | met | **Zero.** 15,208 bytes before and after — the file was not opened for editing. The route the owner took on 2026-08-14 is what buys this: the page already carried the command in a fence, so the change was to the tool's reach. |

**What this does not do.** It watches the two figures the page states. It cannot tell anyone the
sentence around them is still true, and it does not know whether the bound is met — which is
deliberate and is criterion 3. The gap it closes is the one measured: 174 bytes drifted between
T-152's close and this task's raising with nothing to report it.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-15 | → done | All five criteria met, none `not met`. **The number that governs what every session pays is now checked by something rather than remembered by someone**, and `R8` §3.1 step 16's obligation — phase 2 leaves at least one thing that re-measures unasked — is discharged; `docs/CONTEXT-AUDIT.md` §10.4 recorded it open. One finding kept beyond the task: **L-104**, that a page keeping its own history has to be checked in the opposite direction, which is why label-binding could never have worked here. Nothing this task produced renders, so §7 step 3 does not apply. |
| 2026-08-15 | → in_progress | Implemented as planned, with one correction found by the fixture rather than by reading: `PROSE_NUMERAL` cannot match a figure that **ends a sentence**, because the `.` is excluded to keep `0.2.4` whole. The first fixture wrote its figure sentence-final and reported the second term `STALE` against a page that plainly stated it. Pre-existing, out of scope, and it fails loudly rather than silently — recorded in §3 and left alone. |
| 2026-08-15 | → planned | §2 written. **The plan's decision is the direction of the comparison**, and it was forced by measuring the page rather than by preference: label-binding leaves the first term unwatched and reports the record sentence beside it as `STALE`, so the rule inverts to *every measured term must be written*. Two facts settled before planning: the fence **runs** (`shlex`, and `pathlib` prints `\` separators on this platform), and `figures.py` is already in `check_all.py`'s `WIDE` manifest, so criterion 1's trigger exists and no entry point is added. Measured today: **15208 / 11925**, which is what the page states — the check lands green, and a check that lands red would have been a different task. |
| 2026-08-15 | → specified | **§1 was complete on 2026-08-14 and the status was never advanced** — written, ruled on, and left at `proposed`. Recorded as its own row rather than folded into the one above, because the phase was earned on a different day by a different session. |
| 2026-08-14 | (question settled) | **The owner took the third route: neither rule yields.** `figures.py` learns to run a fenced command whose output is not pasted and compare against the prose in the same document. Both settled rules stand, tier 1 gains nothing, and the task becomes a tool change rather than a policy change. The two refused routes are kept in §1 because each is cheaper and each spends a rule, which is the shape a later session will rediscover. |
| 2026-08-14 | → proposed | Raised at T-153's review against the one acceptance criterion that closed **not met**: `R8` step 16 requires phase 2 to leave something that re-measures unasked, and it could not. **The blocker is a collision, not a difficulty** — every route is cheap and each is forbidden by a different settled rule, which is **L-100**. The evidence is 174 bytes of undetected drift in the number that governs what every session pays, plus a debt statement that has been wrong in both terms twice, plus `figures.py` reading both figures as unanchored among 413. `s`, `PH3` because PH2 has shipped and this is not a defect in the published plugin. |
