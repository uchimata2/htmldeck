---
id: T-237
title: Reconcile the release documents with the releases that actually ran
type: fix
status: done
phase: review
parent: T-219
blocked_by: []
related: []
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-08-29
updated: 2026-09-02
shipped_in: 0.7.0
deliverables:
  - tools/docs/tables.py
---

# T-237 — Reconcile the release documents with the releases that actually ran

## 1. Specify

**Outcome**
The three release documents describe what happened. Today a blank line splits the release-requirements table so nine of twelve rows render under the wrong release; the chronology opens by contradicting the table beneath it; **fourteen phase tasks have no row in the decision record and eleven of them shipped in `0.6.0`**; the size rule's stated exception is two rows and is now eighty-eight; and the closing paragraph's count of unimplemented conditions disagrees with its own table.

**Closes** `PR-16`, `PR-17`, `PR-24`, `PR-25`, `PR-26` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: `PUBLISHING.md` section 8.1, `RELEASE-HISTORY.md` section 1, and `RELEASE-PHASES.md`'s `PH3` table and preamble
- In: **nothing else** - every finding this task closes is named above, and each statement stays in the register rather than being restated here (the method's umbrella condition 2)
- Out: any finding not in the list above
- Out: committing to a remedy before measuring it. A remedy is a hypothesis (the method's section 5); a fix that the measurement refuses is reported here and its finding stays open

**Inputs**
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3 - the rows for `PR-16`, `PR-17`, `PR-24`, `PR-25`, `PR-26`
- `PUBLISHING.md` section 8 step 8, which is where a missing row is supposed to be added

**Acceptance criteria**
- [ ] every finding above is **closed with its remedy measured**, or explicitly deferred with the reason recorded on its register row - the method's obligation for `Med`
- [ ] each register row's `Task` cell names this task and its `Status` cell says what happened
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None yet. The register's `Remedy` column carries a hypothesis for each finding, and the method's
  section 5 says it is a hypothesis: whoever implements this measures before committing to it, and
  records what the measurement said.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Re-measure all five findings against today's tree before deciding anything — each register `Remedy` is a hypothesis | Four confirmed as stated; `PR-24` confirmed in kind and refuted in quantity |
| 2 | `PR-16` — delete the blank line, then decide the durable half by measuring the class rather than arguing it | The defect is four instances, not one; `tools/docs/tables.py` |
| 3 | `PR-17` — delete the opening count; the table and `chronology.py` already hold the facts | `RELEASE-HISTORY.md` §1 opens on the authority |
| 4 | `PR-24` — refuse the fourteen rows on the measurement; correct the opener's claim and step 8's unproven half | `RELEASE-PHASES.md` opener, `PUBLISHING.md` §8 step 8 |
| 5 | `PR-25` — state the rule, drop the enumeration, write no replacement figure | `RELEASE-PHASES.md` `PH3` preamble |
| 6 | `PR-26` — keep the historical list, delete the running claim about it | `RELEASE-PHASES.md` closing paragraph |
| 7 | Close the five register rows with what the measurement said, write the lessons, run both gates separately | `PRE-RELEASE-AUDIT.md` §3, `L-156`, `L-157` |

## 3. Implement

**Decisions & assumptions**
- **`PR-16`'s durable half is worth a tool, and the measurement is what decided it** — the class was
  scanned before the instance was fixed, and the one reported blank line was **four**: `PUBLISHING.md`
  §8.1, two in `RELEASE-PHASES.md`'s own phase tables, one in `T-024`. All four fixed
  — 2026-09-02
- **The check is not *a blank line between two rows*** — that is legal wherever two tables sit
  together, and the naive form had 3 true against 3 false on this tree. A table that genuinely starts
  after the gap opens with a header **and its delimiter row**; requiring that absent gives 4 hits and
  0 false alarms. Proved both ways on the real file, not only in the self-test — 2026-09-02
- **`PR-24`'s fourteen back-filled rows are refused on the measurement.** It is **85** today and
  rising by about a task a day, so the remedy would have been false again inside a week — which is
  this finding's own argument turned on its own remedy. The half of it about the step held exactly:
  the stated proof is satisfied by `RELEASE-HISTORY.md` alone, so the half naming `RELEASE-PHASES.md`
  had no proof and had silently stopped. **No proof was invented for it** — a release writes nothing
  into a decision record, so the step names one home — 2026-09-02
- **No replacement figure was written anywhere.** `PR-25`'s 88-of-110 is 138 of 161 five days on, and
  `PR-17`'s two numbers move at every release. Both counts are deleted and their commands left —
  `T-236`'s rule, and these are the cases it was written for — 2026-09-02
- **`PR-26` keeps the list and deletes the claim about it.** What PH1 shipped without is a fact about
  the decision and does not move; *the rest of this list still stands* is a summary of a table in the
  same file, and it had been wrong twice — 2026-09-02

**Outputs produced**
- `tools/docs/tables.py` — new, wired into `check_all.py`'s `WIDE`
- [`docs/PUBLISHING.md`](../docs/PUBLISHING.md) — §8.1's split table, §8 step 8
- [`docs/RELEASE-HISTORY.md`](../docs/RELEASE-HISTORY.md) — §1's opening count
- [`docs/RELEASE-PHASES.md`](../docs/RELEASE-PHASES.md) — opener, `PH3` preamble, closing paragraph, two split tables
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) — the five rows closed
- [`docs/lessons/L-156.md`](../docs/lessons/L-156.md), [`docs/lessons/L-157.md`](../docs/lessons/L-157.md), and the regenerated index
- [`tasks/T-024-build-the-reference-deck-and-validate-the-ruleset.md`](T-024-build-the-reference-deck-and-validate-the-ruleset.md) — one split table, absorbed in place

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| every finding closed with its remedy measured, or deferred with the reason on its row | met | All five closed. Two remedies were changed by the measurement and both changes are on the row: `PR-24`'s fourteen rows refused at 85, `PR-16`'s one instance widened to four |
| each register row's `Task` cell names this task and its `Status` cell says what happened | met | `python tools/docs/findings.py --check` exits 0 |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | met | See the log row |

**Child fix tasks raised**
- none. Nothing found here needed one: the three unreported split tables are the same one-character
  defect and were fixed in place under the remediation order's §4, and the checker that found them
  is this task's own deliverable.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`Med`**, grouped: the owner ruled on 2026-08-29 that a severity obliges a disposition before the release rather than a file count, on the precedent that the method already accepts many findings to one task at `Low`. Every finding keeps its id and its statement in the register. |
| 2026-09-02 | proposed → done | B19. Five findings closed, two of them against their own stated remedy. `PR-16`'s one reported blank line was **four** once a tool asked the question ([L-156](../docs/lessons/L-156.md)); `PR-24`'s fourteen missing rows were **85**, and the half of step 8 that named the file had no proof and had stopped running unnoticed ([L-157](../docs/lessons/L-157.md)). No count was re-derived anywhere — three were deleted. |
