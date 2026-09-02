---
id: T-239
title: Reconcile the audit's plan, its ledger and the document binding it to its method
type: fix
status: done
phase: review
parent: T-219
blocked_by: []
related: []
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-29
updated: 2026-09-02
deliverables: []
shipped_in: unreleased
---

# T-239 — Reconcile the audit's plan, its ledger and the document binding it to its method

## 1. Specify

**Outcome**
This run's own record says what the run did. Today a cycle records three of the four things the method says it names; section 2's Files and Bytes cells have drifted from the command that emits them in six of thirty-seven rows; **a tracked file is in none of the partition's three states** because the cycle owning it closed before the file existed; and the document binding this project's audits to their methods names a method for one of three.

**Closes** `PR-21`, `PR-101`, `PR-102`, `PR-115` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: T-219 section 2's cycle programme and cycle 41 row, this register's coverage ledger, and `AUDIT-METHOD.md` section 1
- In: **nothing else** - every finding this task closes is named above, and each statement stays in the register rather than being restated here (the method's umbrella condition 2)
- Out: any finding not in the list above
- Out: committing to a remedy before measuring it. A remedy is a hypothesis (the method's section 5); a fix that the measurement refuses is reported here and its finding stays open

**Inputs**
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3 - the rows for `PR-21`, `PR-101`, `PR-102`, `PR-115`
- `PR-101`, which says step 2's command is the authority and the table is not
- [T-223](T-223-derive-the-audit-cycles-membership-instead-of-counting-it.md) - why the membership is derived rather than tabulated

**Acceptance criteria**
- [x] every finding above is **closed with its remedy measured**, or explicitly deferred with the reason recorded on its register row - the method's obligation for `Med`
- [x] each register row's `Task` cell names this task and its `Status` cell says what happened
- [x] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None yet. The register's `Remedy` column carries a hypothesis for each finding, and the method's
  section 5 says it is a hypothesis: whoever implements this measures before committing to it, and
  records what the measurement said.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Re-measure each of the four rows before touching anything — the method's §5, and the reason B20 refuted three remedies | Four measurements, below |
| 2 | `PR-115` first, because its *prior question* decides whether the answer is a column or a clause | `AUDIT-METHOD.md` §1 |
| 3 | `PR-21` and `PR-101` together — they are the same table, and one adds a column while the other removes two | `T-219` §2 |
| 4 | `PR-102` in the same pass — it is one brief cell in that table | `T-219` §2, cycle 41 |
| 5 | Write each row's disposition into the register's Status cell, saying what the measurement did to the hypothesis | `PRE-RELEASE-AUDIT.md` §3 |
| 6 | Both gates, run separately and in order | green |

## 3. Implement

**What each measurement said, before any remedy was chosen**

| Row | Its hypothesis | What was measured, 2026-09-02 | Verdict |
| :--- | :--- | :--- | :---: |
| `PR-21` | Add an `Instrument` column to both tables; back-filling 38 cycles is *a description of what happened, not a plan* | All 30 of the register's closed ledger rows already name their instrument in prose — 22 name a command, and the other 8 open on *none: all N read whole*, which names reading. `T-219` §2 names it nowhere | **half refused** |
| `PR-101` | Reprint the cells (cheap, decays) or make the comparison a command (lasts) | **26 of 37 sized rows disagree**, against the 6 this row recorded on 2026-08-28. And `T-219` is *inside cycle 7*, so writing cycle 7's byte count into it changes that count — `1,250,171` is not the width of `132,120` | **both refused** |
| `PR-102` | Name cycle 7 in cycle 41's re-read list | Cycle 41's brief read *cycles 1, 3 and 5 again, plus every cycle a remedy touched* — cycle 7 is neither, as the row says | **held** |
| `PR-115` | A `Method` column, but it may be fillable twice of three | Fillable **three of three**: the ruleset audit's method is §3 of its own register, three named tests. And half the row's evidence had moved — `CONTEXT-AUDIT.md` names `ecoctx` now, `T-287`'s doing | **held, and widened** |

**Decisions & assumptions**

- **`PR-101`'s columns are deleted, not reprinted and not gated — 2026-09-02.** The row offered a
  cheap half and a lasting half and the measurement refused both. Reprinting bought five days last
  time and the decay has since quadrupled; a `--plan --check` would have failed forever on cycle 7,
  whose subject contains the table. Deleting them dissolves the fixed point and leaves one command
  as the only answer, which is [T-223](T-223-derive-the-audit-cycles-membership-instead-of-counting-it.md)'s
  own rule reaching the last two columns that still kept a copy. *The alternative not taken:* keep
  `Files`, which does converge, and gate that alone. Refused because the programme is planned — of
  the 43 cycles only 41 and 42 remain and both are unsized — so a hand-copy would be maintained for
  a use that is spent.
- **`PR-21`'s column is filled forward, not back — 2026-09-02.** The ledger answers already, 30 of
  30, so a back-filled cell would be a second copy of a fact with a home. Closed rows carry
  `ledger`, a pointer; cycles 41 and 42 carry a real instrument, which is the case the row was
  actually built on.
- **`PR-102`'s wider half is left open on purpose — 2026-09-02.** Whether the register and
  `AUDIT-METHOD.md` belong to a numbered cycle at all while the run is live is *the method's rather
  than this project's*, in the row's own words. This task took the smaller fix and did not answer it.
- **Nothing was restated into this record.** Each finding's statement stays in the register
  ([`AUDIT-METHOD.md`](../docs/AUDIT-METHOD.md) §2's umbrella condition 2); what is here is what the
  measurement did to the hypothesis, which the register cannot hold for four rows at once.

**Outputs produced**

- [`docs/AUDIT-METHOD.md`](../docs/AUDIT-METHOD.md) — §1 gains a `Method` column, filled three of
  three, and a paragraph recording that the third row *was* the prior question
- [`tasks/T-219-pre-release-audit-of-the-whole-repository.md`](T-219-pre-release-audit-of-the-whole-repository.md)
  — §2 loses `Files` and `Bytes`, gains `Instrument`, and cycle 41's brief names cycle 7; the
  preamble records both refusals with their measurements
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) — the four Status cells
- [`docs/lessons/L-161.md`](../docs/lessons/L-161.md) — the mechanism `PR-101` turned on, met twice in one session and generalising past this audit

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every finding closed with its remedy measured, or deferred with the reason recorded | **met** | All four closed. Two remedies were refused outright and one half-refused, each on a measurement recorded above and summarised in the row's own Status cell |
| Each register row's `Task` cell names this task and its `Status` cell says what happened | **met** | The `Task` cells already named it; the four `Status` cells were `open` and now carry the disposition |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | **met** | Run in that order, on the tree as committed. `cycles.py` still exits 1 on `docs/OWED-LOOKS.md`, which is `T-284`'s and is excluded from `check_all.py` with a stated reason |

**Child fix tasks raised**
- none. `PR-102`'s wider half belongs to taskmd's method rather than to this project, and is
  recorded as left open rather than filed here.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-02 | proposed → done | **Closed in B21, the batch's only task, and three of the four hypotheses did not survive being measured.** `PR-101` lost both halves of its remedy: 26 of 37 rows had drifted where it recorded 6, and cycle 7's row could never converge because the table sits inside cycle 7's own subject — so the two columns are deleted and the command is the only answer. `PR-21` lost its back-fill: all 30 closed ledger rows already name their instrument, 22 by command and 8 by *read whole*. `PR-115` gained rather than lost — its prior question answered yes, three of three, and half its evidence had already been repaired by `T-287`. `PR-102` held, and its wider half was left to the method on the row's own instruction |
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`Med`**, grouped: the owner ruled on 2026-08-29 that a severity obliges a disposition before the release rather than a file count, on the precedent that the method already accepts many findings to one task at `Low`. Every finding keeps its id and its statement in the register. |
