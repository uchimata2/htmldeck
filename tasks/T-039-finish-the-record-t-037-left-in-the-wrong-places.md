---
id: T-039
title: Finish the record T-037 left in the wrong places
type: fix
status: done
phase: review
parent: T-037
blocked_by: []
related: [T-005, T-014, T-021, T-022]
work_package: WP2
owner: maintainer
created: 2026-08-09
updated: 2026-08-09
deliverables: [docs/DESIGN-SYSTEM.md]
---

# T-039 — Finish the record T-037 left in the wrong places

## 1. Specify

**Outcome**
The three parts of [T-037](T-037-record-in-the-ruleset-which-rules-no-check-can-reach.md)'s record
that landed in the wrong document, at the wrong scope, or on a false premise are put right, so that
its `Reach` column and the story of the section that never existed can be read entirely from the
repository without a task file to explain them.

**Why this one**
T-037's own review found three criteria not met. **None of them is a defect in the deliverable** —
the column, its vocabulary, its reader and the number 105 are all as specified and verified. All
three are about *where the record went*, which is precisely the failure class T-037 was raised to
correct, reappearing inside it.

**Scope**

- In: **the conditions 22 / 30 write-off is reachable from the ruleset.** It exists and is correct
  in [`DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) §5.5; the criterion said *the ruleset*,
  and `DESIGN-SYSTEM.md` opens *"The operative ruleset. Nothing else."*
- In: **the three missed `§11` citations** — `T-014`:248, `T-021`:298, `T-022`:107. T-021's is the
  one that matters most: it explains the staleness as *"a numbering T-022 removed when it split the
  design system"*, which is the **wrong cause** and would send the next reader looking for a
  deletion that never happened.
- In: **a verdict on DS-033, DS-061 and DS-065's notes** — whether a *"this rule is checked
  statically rather than at render"* fact belongs in the ruleset at all, or is gate-internal and
  stays with the gate. Deciding it is the work; either answer closes the criterion honestly.
- Out: **changing the `Reach` column, its vocabulary, its values or the number 105.** All verified
  in T-037 and not reopened here.
- Out: `audit.py`'s *"Not gated here, and why"* tail as a whole — it conflates *checked elsewhere*
  with *cannot be checked*, and that is
  [T-005](T-005-build-check-the-gate-the-deck-must-pass.md)'s to fix when the gate learns to derive
  coverage from the ruleset.

**Inputs**
- [T-037](T-037-record-in-the-ruleset-which-rules-no-check-can-reach.md) §4 — the three verdicts and
  what settled each.
- [`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — the `Reach` block near the column table.
- [`DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) §5.5 — the write-off as it stands.
- `tools/deck/audit.py` — the four printed notes.

**Acceptance criteria**
- [ ] A reader in `DESIGN-SYSTEM.md` can learn that two conditions were written off and why, without
      being told to read a task
- [ ] No `§11` reference anywhere in `tasks/` asserts, without correction beside it, that the section
      existed or that something removed it
- [ ] T-021's *"a numbering T-022 removed"* is corrected specifically — the cause, not just the fact
- [ ] DS-033, DS-061 and DS-065 are settled: either their notes are in the ruleset, or it is written
      down that a *which-stage-checks-it* fact is gate-internal and why. **Not left as a third state**
- [ ] `python tools/tasks/task.py check` passes, and the `Reach` reader still reports 158 migrated,
      0 outside the vocabulary, 0 missing a reason

**Open questions**
- **Does the write-off belong in the operative ruleset at all? — owner.** T-037's criterion said *in
  the ruleset*, and the review recorded it not met on that wording. But `DESIGN-SYSTEM.md` is
  *"the operative ruleset, nothing else"*, and two lost condition numbers are history, not an
  operative rule — which is the rationale's job. *Recommended:* **one sentence in the ruleset that
  states the fact and points at §5.5 for the account.** That satisfies the criterion's intent — a
  reader of the ruleset is never left wondering — without moving history into a document that
  declares it carries none. If the owner prefers the criterion read strictly, the whole write-off
  moves instead.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | State the conditions 22 / 30 write-off in the ruleset in one sentence, pointing at `DESIGN-RATIONALE.md` §5.5 for the account | a ruleset reader never left wondering |
| 2 | Settle DS-033 / DS-061 / DS-065 by stating the general rule — `Reach` records *whether* a check can get at a rule, never *which stage* of the gate does it | one clause in the `Reach` block |
| 3 | Correct the three missed `§11` citations, T-021's cause first | three annotated task files |
| 4 | Re-run `task.py check` and the `Reach` reader | green, or a named failure |

**Approach decisions**

- **One sentence in the ruleset pointing at the rationale, rather than moving the write-off —
  2026-08-09.** The open question is taken rather than handed back, because either answer closes the
  criterion and the cost of choosing wrong is one sentence. `DESIGN-SYSTEM.md` declares itself *"the
  operative ruleset. Nothing else"* and two lost condition numbers are history; moving the account
  into it would contradict the document's own first line to satisfy the literal word *ruleset*.
  Pointing at §5.5 satisfies what the criterion was for — a reader of the ruleset is never left
  wondering — without that. *Rejected:* relocating the whole §5.5 passage. The owner can reverse this
  in one edit if they read the criterion strictly.
- **A *which-stage-checks-it* fact is gate-internal and stays with the gate — 2026-08-09.** This is
  the general rule behind DS-033, DS-061 and DS-065, and stating it is better than migrating three
  notes: `Reach` answers *can a check get at this rule*, and *"`audit.py` decides it statically
  rather than at render"* answers a different question that changes whenever the gate is refactored.
  Putting it in the ruleset would make the ruleset stale on a gate change — the coupling this whole
  line of work exists to remove.

## 3. Implement

**Decisions & assumptions**
- Both decisions above were taken at `plan` and are unchanged by the work.

**Outputs produced**
- `docs/DESIGN-SYSTEM.md` — the write-off sentence and the gate-internal clause, in the `Reach` block
- `tasks/T-014-synthesise-research-into-the-design-system-reference.md`,
  `tasks/T-021-the-reflow-view-and-the-resolution-contract.md`,
  `tasks/T-022-split-the-design-system-from-its-rationale.md` — the three missed citations annotated

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A reader in `DESIGN-SYSTEM.md` learns two conditions were written off and why, without being told to read a task | **met** | Three sentences in the `Reach` block: the two are gone, the numbering was not this document's order, and nothing is owed to them because every rule now states its own `Reach`. The account is one hop away at [`DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) §5.5, and no task file is in the path |
| No `§11` reference anywhere in `tasks/` asserts, without correction beside it, that the section existed or that something removed it | **met** | Swept every `§11` in `tasks/`. Three assertions annotated here; the rest are either another document's §11 (R1's, R2's) or text that already states it never existed. One phrasing of my own was caught in the sweep and fixed — T-005's open question read *"now that §11 is gone"*, which asserts it was there |
| T-021's *"a numbering T-022 removed"* is corrected specifically — the cause, not just the fact | **met** | Annotated in place. The row's **fix** was right and its **cause** was wrong, and the note says so, because the wrong cause sends a reader hunting the history for a deletion that never happened |
| DS-033, DS-061 and DS-065 are settled — either their notes are in the ruleset, or it is written down that a *which-stage-checks-it* fact is gate-internal and why. Not left as a third state | **met** | Settled by stating the general rule rather than migrating three notes: `Reach` says whether a check can get at a rule, never which part of the gate does, because that changes on every refactor and would make the ruleset stale on a gate change. *"A rule checked in an unexpected stage is still `yes`"* |
| `task.py check` passes, and the reader still reports 158 migrated, 0 outside the vocabulary, 0 missing a reason | **met** | `OK - 39 tasks, 573 document pointer(s) checked, 0 broken`; reader: `158 migrated, 0 not yet`, `105` expected, `0` outside the vocabulary, `0` missing a reason. `audit.py` unchanged at **0 mechanical failures** |

**All five met.** T-037's three carried criteria are now closed in substance: the ruleset states the
write-off, the `§11` sweep is complete rather than scoped to three named files, and the
DS-033/061/065 question has an answer written down instead of a gap.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-09 | → done | **All five criteria met; [T-037](T-037-record-in-the-ruleset-which-rules-no-check-can-reach.md)'s three carried failures are closed in substance.** The open question was **taken rather than handed back**: the write-off is stated in the ruleset in three sentences pointing at [`DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) §5.5, rather than moving the account into a document whose first line is *"the operative ruleset. Nothing else."* Either answer closed the criterion and choosing wrong costs one sentence, so handing it over would have bought nothing. **DS-033 / DS-061 / DS-065 were settled by stating the general rule instead of migrating three notes** — `Reach` says whether a check can get at a rule, never which part of the gate does, because the latter changes on every refactor and would make the ruleset go stale whenever the gate moved. That is the coupling this whole line of work exists to remove, so migrating the notes would have reintroduced it in miniature. **The `§11` sweep is now complete rather than scoped**, which is what T-037's criterion actually asked for: three assertions annotated — T-014, T-021, T-022 — and **one of my own phrasings caught by the sweep**, T-005's open question reading *"now that §11 is gone"*, which asserts it was once there. T-021's is annotated on its **cause**, not just its fact: the row's fix was right and its explanation — *"a numbering T-022 removed"* — was wrong, and a wrong cause sends the next reader hunting the history for a deletion that never happened. Evidence: `task.py check` **39 tasks, 573 pointers, 0 broken**; reader **158 migrated, 105 expected, 0 outside the vocabulary, 0 missing a reason**; `audit.py` **0 mechanical failures**. |
| 2026-08-09 | → proposed | **Raised by [T-037](T-037-record-in-the-ruleset-which-rules-no-check-can-reach.md)'s review, carrying its three unmet criteria.** None is a defect in what T-037 built: the `Reach` column sits on all 158 rule rows, its reader was made to fail before being trusted, and **105** is derived from the ruleset and stored nowhere. The three failures are all about *where the record went* — the conditions 22 / 30 write-off is in the rationale where the criterion said ruleset; the `§11` sweep covered the three files the criterion named and the criterion said *every*, missing T-014, T-021 and T-022; and the criterion about `audit.py`'s four notes was written believing all four were reachability reasons, which `implement` disproved for three of them. **T-021's is the one to fix carefully**: it records the cause as *"a numbering T-022 removed"*, and nothing was removed, so a reader following it hunts for a deletion that never happened. Worth stating plainly: this is the same defect class T-037 exists to correct, occurring inside T-037. |
