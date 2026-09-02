---
id: T-251
title: Correct R9's account of DS-122 and a memory entry recording an edit never made
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
shipped_in: unreleased
deliverables: []
---

# T-251 — Correct R9's account of DS-122 and a memory entry recording an edit never made

## 1. Specify

**Outcome**
Two durable records describe the tree as it is. Today `R9` describes DS-122's rule and its check as they were **before the change R9 itself proposed**, which shipped; and a memory entry records an annotation in tier 1 that was never made and describes a passage that never said what it says.

**Closes** `PR-114`, `PR-120` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: `docs/research/R9-embeddable-chart-library-versus-hand-authored-svg.md` sections 1 and 8, and the memory entry `decide-detailed-questions-yourself`
- In: **nothing else** - every finding this task closes is named above, and each statement stays in the register rather than being restated here (the method's umbrella condition 2)
- Out: any finding not in the list above
- Out: committing to a remedy before measuring it. A remedy is a hypothesis (the method's section 5); a fix that the measurement refuses is reported here and its finding stays open

**Inputs**
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3 - the rows for `PR-114`, `PR-120`
- [T-202](T-202-amend-ds-122-into-a-threshold-and-bind-its-check-on-structure.md), which made the change R9 still describes as proposed
- **`PR-119` and `PR-120` are cycle 25's evidence** and must not be repaired before this task runs - repairing either invalidates the reading that produced them

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
| 1 | Re-verify both rows against the tree before editing | `DS-122` carries the threshold, `T-202` is `done` in `0.6.0`; `CLAUDE.md`'s passage carries no ask-first clause and `git log -S` returns nothing for either string over its whole history |
| 2 | `PR-114` — decide the open half: restate §1's probe table as history, or re-probe it | Decided **history**, on what the table is evidence *about* |
| 3 | `PR-114` — past-tense §1, and a dated closure on §8 in §9's shape | R9, sections 1 and 8 |
| 4 | `PR-120` — cut the `CLAUDE.md` half, keep the memory half, record what was wrong | the memory entry `decide-detailed-questions-yourself` |
| 5 | Close the two register rows, then `lint.py` and `check_all.py --docs`, run separately | Both green |

## 3. Implement

**Decisions & assumptions**
- **§1's probe table is restated as history, not re-probed.** `PR-114` left the choice open. The table's four probes are evidence about the check that was **replaced** — they show a name-list check clearing four things a reader calls chart libraries, which is *why* `T-202` happened. Handing the same probes to the structural check answers a different question and loses **L-125**'s case with it — 2026-09-02
- **The memory entry records what it got wrong rather than dropping it.** The false half claimed an annotation in a file loaded on every turn; deleting the sentence silently would leave nothing saying the claim was ever made — 2026-09-02
- **The register's own line-number citation had drifted** — it points at `audit.py` 694-700 and the comment now opens at **705**. Not raised as a finding: the closure names the comment's first words instead, which is what does not decay — 2026-09-02
- **This task edits the agent memory store, which is machine-local.** It reaches no clone, and no repository document points into it. Recorded here because the register row is the only durable trace of the edit — 2026-09-02

**Outputs produced**
- [`../docs/research/R9-embeddable-chart-library-versus-hand-authored-svg.md`](../docs/research/R9-embeddable-chart-library-versus-hand-authored-svg.md) — §1's paragraph and table framing, §8's dated closure
- the memory entry `decide-detailed-questions-yourself` — machine-local, not in this repository
- [`../docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) — the `PR-114` and `PR-120` status cells

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| every finding closed with its remedy **measured**, or deferred with the reason on its row | pass | Both closed. Both rows were re-verified against the tree first, and `PR-120`'s stated hypothesis — that the sentence pointed at prose which moved — was refused by the history |
| each register row's `Task` cell names this task and its `Status` cell says what happened | pass | Both. The `Task` cells already named it |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | pass | `lint.py` green; `check_all.py --docs` green — one research note and one register, no path `--docs` refuses. **The batch's landing owes the full run** |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-02 | proposed → done | B20. **`PR-114`'s open half is decided on what the evidence is *about*.** §1's probe table shows four chart libraries clearing a rule that forbids chart libraries — that is the argument for `T-202`, not a measurement of today's check, so it is restated as history and §8 gains the dated closure §9 already uses for `T-205`. **`PR-120`'s hypothesis is refused by the history**: the sentence claimed an annotation in `CLAUDE.md` and `git log -S` finds no commit that ever carried one, so the claim was never true rather than drifted. The entry keeps a note of what it got wrong; deleting the sentence would leave nothing saying the claim was made. That store is machine-local and reaches no clone. |
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`Med`**, grouped: the owner ruled on 2026-08-29 that a severity obliges a disposition before the release rather than a file count, on the precedent that the method already accepts many findings to one task at `Low`. Every finding keeps its id and its statement in the register. |
