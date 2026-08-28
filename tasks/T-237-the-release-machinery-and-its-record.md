---
id: T-237
title: Reconcile the release documents with the releases that actually ran
type: fix
status: proposed
phase: specify
parent: T-219
blocked_by: []
related: []
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-08-29
updated: 2026-08-29
deliverables: []
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
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <the files this task changed>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- <T-NNN or "none">

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`Med`**, grouped: the owner ruled on 2026-08-29 that a severity obliges a disposition before the release rather than a file count, on the precedent that the method already accepts many findings to one task at `Low`. Every finding keeps its id and its statement in the register. |
