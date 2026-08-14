---
id: T-143
title: Split the release chronology out of CLAUDE.md
type: deliverable
status: done
phase: review
shipped_in: unreleased
parent: T-130
blocked_by: []
related: [T-130, T-134, T-144]
work_package: PH3
owner: the project owner
business_value: high
effort: s
created: 2026-08-14
updated: 2026-08-14
deliverables:
  - CLAUDE.md
  - docs/RELEASE-HISTORY.md
---

# T-143 — Split the release chronology out of CLAUDE.md

## 1. Specify

**Outcome**
[`../CLAUDE.md`](../CLAUDE.md) carries the rules that must bind before a session knows what kind of
work it is doing, and nothing else. The dated narrative of what shipped when, which release carried
which fix and which task found which defect moves to a document nothing loads by default. **The
finding is `CE-01`**, stated in
[`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
§8; it is not restated here.

**This is one of the two cuts [T-134](T-134-state-the-tier-model-and-bound-tier-1-as-a-relation.md)
was raised to make decidable**, and it is the larger of them. The bound now exists, the file reports
itself over it, and this task is what pays the debt down rather than arguing about it.

**Measured at the audit, 2026-08-13:** the chronology was **6,980 of 15,630 bytes — 45% of a tier-1
file paid on every turn**. The file is **18,642 bytes** now, so re-measure before claiming a saving
and again after (`docs/CONTEXT-AUDIT.md` §6.2, rule 1). The section T-134 added is a rule and stays.

**The extraction is the work, not the move.** Narrative paragraphs written over time embed real
rules — the phase-is-not-a-version paragraph is the clearest, and it is a rule wrapped in the
incident that produced it. A section moved wholesale takes those with it out of tier 1, where they
stop binding.

**Scope**
- In: naming every operative rule inside the paragraphs to be moved, **before** anything moves.
- In: the chronology's new home, its statement of its own tier, and the pointer to it from tier 1.
- In: re-measuring `CLAUDE.md` against its own bound and correcting the debt statement, which is the
  one sentence in the file that this task is expected to falsify.
- Out: `docs/BRIEF.md`'s *Release phases*. That is `CE-05`, a different document, and `m`.
- Out: rewording a rule while moving it. A move that also edits is two changes nobody can review.
- Out: the humanizer. `CLAUDE.md` is a plugin file and stays AI-optimized
  ([`../docs/PUBLISHING.md`](../docs/PUBLISHING.md)).

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.2 — what a session working an audit
  finding owes beyond the finding. Read before starting
- [`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
  §8 — `CE-01` in full; §9, P1 — the local precedent for the split
- [`../CLAUDE.md`](../CLAUDE.md) — *What loads every turn, and what bounds it*: the bound this task
  is measured against, and the command that measures it

**Acceptance criteria**
- [ ] Every operative rule inside the moved text is listed **before** the move, and each one ends in
      exactly one home
- [ ] Nothing that must bind before a session knows its kind of work leaves tier 1
- [ ] The new document states what tier it is and what loads it — nothing, by default
- [ ] `CLAUDE.md` is re-measured against the smallest document it defers to, and its debt statement is
      corrected to what is true after the move, including the case where the debt is cleared
- [ ] The saving is stated as before and after, dated, with the command that produced both
- [ ] `python tools/docs/refcheck.py` green — every reference into the moved text still resolves

**Re-measured 2026-08-14, and the bound changed hands since the debt statement was written.**
`CLAUDE.md` is **19,035 bytes**; the smallest document it defers to is now
[`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) at **11,407**, not `.taskmd/config.md` at 14,087. The workflow
document was 23,210 bytes until [T-147](T-147-one-workflow-file-per-lifecycle-phase.md) cut it to
11,407 in `7ec5cad`, which is the same day the debt statement was written and after it. **So the
debt is 7,628 bytes over, not 4,555**, and the sentence in tier 1 is wrong in both terms.
`L-90` applies to what follows: this says where the weight is, not what removing it is worth.

**The `T-143` / `T-144` boundary, decided here so neither task edits the other's text.**
Both cut narrative out of the same paragraphs, so the split is by **destination**, which is checkable:

- **T-143 takes text whose destination is the new history document** — a fact with no other home.
- **T-144 takes text whose destination is an existing lesson entry** — a fact already homed under
  [`../docs/lessons/`](../docs/lessons).

By that line the *phase-is-not-a-version* paragraphs are **T-144's**, not this task's, even though
this record named them: their incident is already `L-69` in full, so what they need is a deletion and
a pointer rather than a move. Everything else in the chronology is T-143's.

**The rule inventory — every operative rule inside the text to be moved, listed before anything
moves.** Each ends in exactly one home. `R4` and `R5` are the ones this task hands to T-144.

| | Rule | Where it ends |
| :-- | :--- | :--- |
| R1 | `reference/` is a prompt, not prior art: nothing in it is code to copy or behaviour to verify | stays in tier 1 |
| R2 | The repository is public at `github.com/uchimata2/htmldeck` and `master` is the published branch | stays in tier 1 |
| R3 | The current published version — bound to tier 1 by [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) §8 step 2, which names this file as one of the three that carry it | stays in tier 1, as a version string and not a history |
| R4 | A patch takes the next patch number on the published line, whatever phase its tasks belong to | stays in tier 1 — **T-144's paragraph**, `L-69` |
| R5 | `work_package` is the phase, `shipped_in` is the version; never write a phase with a `v` | stays in tier 1 — **T-144's paragraph**, `L-69` |
| R6 | A shipped release and an open phase are not a contradiction | folds into `R5` — it is the same distinction |
| R7 | A defect in the published plugin is a `PH1` **phase** task, not a later improvement | folds into `R8` — it is stated twice today |
| R8 | Which phase a new task takes: `PH1` only for such a defect, `PH3` for `l` or `xl`, and since PH2 shipped everything else that is not such a defect | stays in tier 1 — it binds before a session knows its kind of work |
| R9 | Read the brief first; its *Decisions taken* section overrides anything older in it | stays in tier 1 |
| R10 | A task's classification is this project's to make, not its filer's — a published gate that fails a deck for using a class the contract defines is a defect in the check whatever the report calls it | stays in tier 1 |
| R11 | Build mode, critique mode and the gate exist and are where the paragraph says | stays in tier 1, as a map without dates or counts |
| R12 | 12 slides is the floor, not the target; a long deck is untested territory and a result says which length it was measured at | stays in tier 1 |
| R13 | `printgeom.py` reads the paper and asserts `PRINT-2` and `PRINT-3` — two numbers and nothing wider; rule 6 is not satisfied by a screen render at any length nor by a green `PRINT-2` | stays in tier 1 |
| R14 | `python tools/check_all.py` is step 1 of a release and a tool in none of its three outcomes fails the run | stays in tier 1 |

**Open questions** — both answered in this section; kept with their answers rather than deleted.
- **Its own document, or the one `CE-05` would create?** — **Its own**: `RELEASE-HISTORY.md`, under
  `docs/`.
  `CE-05` landed on 2026-08-14 as [T-145](T-145-move-brief-mds-release-phases-to-its-own-document.md)
  and created [`../docs/RELEASE-PHASES.md`](../docs/RELEASE-PHASES.md), so the option is now real
  rather than hypothetical — and it is the wrong home twice over. That document is **101,254 bytes**
  and answers *which phase does this task belong to and why*, one row per task; a chronology answers
  *what shipped when*. Folding them puts a reader who wants three dates into the largest document in
  `docs/`. The third candidate, `PUBLISHING.md` §8.1, answers *what does this release newly require of
  an adopter's deck*, which is a third question again. — the implementer, per the recommendation.

## 2. Plan

**Six steps. The inventory is already done — it is §1's table, written before any edit, which is what
acceptance criterion 1 asks for.** The order puts every deletion of an already-homed duplicate before
the move, so the new document never receives a copy of something `PUBLISHING.md` or
`RELEASE-PHASES.md` already holds.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Sweep for pointers into the text being moved — `§`-references, `CLAUDE.md`-relative anchors, and any document that cites this file for a release fact (`L-91`: what breaks after a move is what no checker binds) | The list of references to repoint, or the finding that there are none |
| 2 | Delete from tier 1 the chronology that is **already** homed elsewhere and point instead: the PH1/PH2/PH3 derivation and the `l` line (`RELEASE-PHASES.md` §*Release phases*), `0.2.4`'s empty row (`PUBLISHING.md` §8.1), and `check_all.py`'s replacement story (`PUBLISHING.md` §8) | Three deletions, three pointers, nothing copied into the new document |
| 3 | Write `RELEASE-HISTORY.md`, under `docs/`: its tier, what loads it (nothing), its boundary against the other three release documents, and the chronology itself in date order | The new document |
| 4 | Cut the chronology out of `CLAUDE.md`, leaving `R1`, `R2`, `R3`, `R8`–`R14` stated operatively. `R4` and `R5` are left untouched for T-144 | `CLAUDE.md`, rewritten in the four affected sections |
| 5 | Re-measure both terms of the bound with the file's own command and correct the debt statement to what is true after the move | The before/after figures, dated, in §3 |
| 6 | `python tools/docs/refcheck.py`, `python tools/tasks/lint.py` | Both green |

## 3. Implement

**The saving, before and after, with the command that produced both.** Measured 2026-08-14 with
`../CLAUDE.md`'s own command, which is the one the bound names:

```bash
python -c "import pathlib;[print(f'{p.stat().st_size:>7}  {p}') for p in map(pathlib.Path,'CLAUDE.md docs/BRIEF.md docs/PUBLISHING.md tasks/TASK-WORKFLOW.md tasks/README.md .taskmd/config.md'.split())]"
```

| | Before | After | Change |
| :--- | ---: | ---: | ---: |
| `CLAUDE.md` | 19,035 | **15,416** | **−3,619, −19.0%** |
| The bound — `TASK-WORKFLOW.md` | 11,407 | 11,407 | unchanged |
| Over the bound by | 7,628 | **4,009** | −3,619 |
| Largest section, and its share | *What this is*, 7,208 / 37.9% | *What this is*, 3,760 / 24.4% | −3,448; the section keeps the title and loses the dates |

*Section sizes are byte-exact against `HEAD:CLAUDE.md` with `\r\n` normalised — `git show` piped
through a text-mode subprocess reads 19,268 for a 19,035-byte file, and the 233-byte gap is one per
line.*

**The audit's `45%` was already 37.9% before this task touched anything**, and the section had not
shrunk: it was 6,980 of 15,630 on 2026-08-13 and 7,208 of 19,035 on 2026-08-14. The section grew by
228 bytes and its *share* fell by seven points, because the file around it grew by 3,405. A share is
a ratio and the denominator here moves faster than the numerator — which is the same class of error
as `L-92`, arrived at from the other side.

**The finding's own figure was not the saving, and this is `L-90` a fifth time.** `CE-01` measured
the chronology at **6,980 bytes**; **3,619** came out. The difference is the fourteen rules in §1's
table, which is the whole of what *the extraction is the work* means — the row could say where the
weight was and could not say how much of it was load-bearing. Anyone reading `CE-01`'s `L` band as a
forecast of 6,980 bytes would have been wrong by 48%.

**Decisions & assumptions**
- **The new document is its own, `RELEASE-HISTORY.md`, and it is tier 3** — §1's open question, and
  the reasoning is there. It declares its tier and states the boundary against the other three
  documents that touch releases, as a table, so the next release fact has one obvious destination —
  2026-08-14.
- **Three paragraphs were deleted rather than moved**, because their content already had a home:
  the phase derivation and the `l` line ([`../docs/RELEASE-PHASES.md`](../docs/RELEASE-PHASES.md)),
  `0.2.4`'s empty row and `check_all.py`'s replacement story
  ([`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) §8.1 and §8). Copying them into a new document
  would have built `CE-04`'s defect while fixing `CE-01`'s — 2026-08-14.
- **The version string stays in tier 1**, against the instinct to move it with the rest of the
  release facts: `PUBLISHING.md` §8 step 2 names this file as one of the three that carry it, so
  removing it would silently break a release step. `R3` — 2026-08-14.
- **The coverage split — 84 of 115 — stays in tier 1 too.** `tools/docs/figures.py` declares
  `CLAUDE.md` as a document that states it, so it is a live gated figure rather than a date, and
  moving it would leave a declared document stating nothing — 2026-08-14.
- **The bound's comparison set is tier 2, and that clause is new.** It was never written down, and it
  has to be: a document split out of tier 1 is smaller than what it was cut from, so if tier-3
  documents counted, **the bound could never be satisfied by splitting** — every cut would create a
  new smaller term. `RELEASE-PHASES.md` was already outside the list, so this states the existing
  practice rather than changing it — 2026-08-14.
- **The phase-is-not-a-version paragraphs were left untouched for T-144**, per §1's boundary. They
  are the one part of this section a reader would expect this task to have cut.

**Outputs produced**
- [`../docs/RELEASE-HISTORY.md`](../docs/RELEASE-HISTORY.md) — new, 10,047 bytes, five sections
- [`../CLAUDE.md`](../CLAUDE.md) — four sections rewritten: *What loads every turn*, *What this is*,
  *Publishing constraints*, *Verifying*
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) — §2.2's `CLAUDE.md` row and §6's rank-5 row,
  both struck with the old values kept
- [`../docs/RELEASE-PHASES.md`](../docs/RELEASE-PHASES.md) — this task's PH3 row folded to two cells

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every operative rule inside the moved text is listed **before** the move, and each one ends in exactly one home | **met** | §1's table, fourteen rules, written in the `specify` phase. Two fold into another rule (`R6` into `R5`, `R7` into `R8`) and two are handed to T-144 (`R4`, `R5`); the other ten are stated in tier 1 |
| Nothing that must bind before a session knows its kind of work leaves tier 1 | **met** | Checked rule by rule against §1's table. The two that would have been easy to lose are `R3`, the version string bound to tier 1 by `PUBLISHING.md` §8 step 2, and `R10`, a classification rule that existed only inside the T-105 anecdote |
| The new document states what tier it is and what loads it — nothing, by default | **met** | Second paragraph: *Tier 3. Nothing loads this document*, with the reason and the boundary table against the other three release documents |
| `CLAUDE.md` re-measured against the smallest document it defers to, and its debt statement corrected | **met** | 15,416 against 11,407. The correction was larger than expected: the old statement was wrong in **both** terms, and the file names its predecessor values so the error is legible |
| The saving is stated as before and after, dated, with the command that produced both | **met** | §3, with `CLAUDE.md`'s own command. −3,619 bytes, −19.0%, still 4,009 over the bound |
| `python tools/docs/refcheck.py` green | **met** | `2219 document pointer(s) checked, 0 broken`; `739 section reference(s) resolved, 0 dead`. `taskmd check` and `figures.py` green too — the last matters because it declares this file as one that states the coverage split |

**Two things the plan did not predict, both recorded above rather than only here.** The bound's
smaller term had changed hands on the morning of the same day and nothing noticed, so the debt
statement this task was told to correct was already false in a way the task's own record repeated.
And the comparison set had to be written down, because splitting content out of tier 1 creates a
document smaller than tier 1 — an unstated rule that, read the other way, makes the bound
unsatisfiable by the exact remedy it was written to prompt.

**Child fix tasks raised**
- none. The remaining 4,009 bytes are
  [T-144](T-144-give-each-cumulative-rule-one-operative-home.md), already open and next.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-14 | → done | **`CLAUDE.md` 19,035 → 15,416, and the finding's 6,980 was never the saving** — 3,619 bytes were narrative and the rest was fourteen rules that stayed, which prices *the extraction is the work* for the first time and is `L-90` a fifth time. Three of the paragraphs in scope needed **no new home at all**: `PUBLISHING.md` §8 and §8.1 and `RELEASE-PHASES.md` already held them, so they were deleted against a pointer, and a fourth home was not built while fixing the finding about too many homes. Two things nobody predicted, both worth more than the bytes. **The bound's smaller term had changed hands the same morning** and the debt statement was wrong in both terms — a rule that reports itself can still report a stale number, and this one had been re-copied into the task that was raised to fix it. **And the comparison set had to be stated**: a document split out of tier 1 is smaller than tier 1, so counting tier 3 would make the bound unsatisfiable by splitting, which is the remedy it exists to prompt. |
| 2026-08-14 | → in_progress | Built in the planned order, and step 2 paid for itself immediately: sweeping for already-homed content before writing anything turned three of the paragraphs from moves into deletions. The version string and the coverage split both stayed against the instinct to move them — one is bound to this file by `PUBLISHING.md` §8 step 2, the other by `figures.py`'s declared-document list, and both would have failed a gate silently. |
| 2026-08-14 | → planned | Six steps, and the order is the point: every deletion of an already-homed duplicate happens **before** the new document is written, so a fact that `PUBLISHING.md` §8.1 or `RELEASE-PHASES.md` already holds is deleted rather than copied to a fourth home. Three of the paragraphs in scope turned out to need no new home at all. |
| 2026-08-14 | → specified | **Both open questions closed here, and the re-measurement moved the finding's second term.** The bound's smaller side changed hands on 2026-08-14 after the debt statement was written — `TASK-WORKFLOW.md` fell to 11,407 in `7ec5cad` — so the file is 7,628 bytes over, not 4,555, and the sentence naming `.taskmd/config.md` was already wrong when this task was raised. The `CE-05` question is answerable now rather than hypothetically: the document it would have used exists, is 101,254 bytes, and answers a different question. **The T-143/T-144 boundary is drawn by destination** — a fact with no home goes to the new document and is T-143's; a fact already in a lesson entry needs a pointer, not a move, and is T-144's — which hands the phase-is-not-a-version paragraphs to T-144 despite this record naming them. |
| 2026-08-14 | → proposed | Raised at the owner's direction, with [T-144](T-144-give-each-cumulative-rule-one-operative-home.md), the day after T-134 set the bound and reported the file 4,555 bytes over it. `CE-01` was a candidate at T-130's review and left unraised then; the debt statement in tier 1 names it, so the choice was a task or a citation, and the owner took the task. The larger of the two cuts T-134 enables. |
