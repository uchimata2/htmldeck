---
id: T-240
title: Correct EVALUATION.md's four internal contradictions and its account of the stage split
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

# T-240 — Correct EVALUATION.md's four internal contradictions and its account of the stage split

## 1. Specify

**Outcome**
[`EVALUATION.md`](../docs/EVALUATION.md) describes the evaluation the code implements. Today the hard-judge checklist is sized three different ways and none is today's number; section 3 states an invariant its own paragraph contradicts three lines later; the ruleset figures are stale; **two sections are numbered 6.3 and both are cited**, so a citation landing on the wrong one is indistinguishable from a correct one; and the stage-1/stage-2 split section 2 describes is not the one `audit.py` implements.

**Closes** `PR-30`, `PR-31`, `PR-32`, `PR-33`, `PR-50` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: `EVALUATION.md` sections 1.1, 2, 3, 6's heading sequence and 8.1, and `audit.py`'s opening
- In: **nothing else** - every finding this task closes is named above, and each statement stays in the register rather than being restated here (the method's umbrella condition 2)
- Out: any finding not in the list above
- Out: committing to a remedy before measuring it. A remedy is a hypothesis (the method's section 5); a fix that the measurement refuses is reported here and its finding stays open

**Inputs**
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3 - the rows for `PR-30`, `PR-31`, `PR-32`, `PR-33`, `PR-50`
- `PR-33`'s remedy column, whose hypothesis is that the second section is not a subsection of the loop at all, so a number outside section 6 may be worth more than 6.5 - which only moves the next collision one append along

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
