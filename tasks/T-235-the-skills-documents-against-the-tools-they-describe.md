---
id: T-235
title: Reconcile the skill's documents with the tools and rules they describe
type: fix
status: proposed
phase: specify
parent: T-219
blocked_by: []
related: []
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-29
updated: 2026-08-29
deliverables: []
---

# T-235 — Reconcile the skill's documents with the tools and rules they describe

## 1. Specify

**Outcome**
An adopter reading the skill meets figures and commands the tree supports. Today two bare `python tools/...` commands survive where a check exists to catch them and cannot see them; three documents disagree how many fields a slide has and the gate takes the larger side; the critique document states the hard-rule count twice, ten lines apart, and both are wrong; and the skill tells an adopter a deck is under 200 KB when no deck this repository ships is.

**Closes** `PR-08`, `PR-09`, `PR-10`, `PR-13` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: the four skill documents, `SKILL.md`, `BRIEF.md`'s *Delivery mode* row, and `check_scaffold.py`'s command check
- In: **nothing else** - every finding this task closes is named above, and each statement stays in the register rather than being restated here (the method's umbrella condition 2)
- Out: any finding not in the list above
- Out: committing to a remedy before measuring it. A remedy is a hypothesis (the method's section 5); a fix that the measurement refuses is reported here and its finding stays open

**Inputs**
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3 - the rows for `PR-08`, `PR-09`, `PR-10`, `PR-13`
- [`skills/htmldeck/SKILL.md`](../skills/htmldeck/SKILL.md)
- [T-231](T-231-two-packaging-checks-have-no-subject-at-all.md) - why the command check sees nothing today, which has to land first or this task's proof is vacuous

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
