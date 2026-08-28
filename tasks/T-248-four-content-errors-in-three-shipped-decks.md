---
id: T-248
title: Correct four numbers a shipped deck asserts and its own source contradicts
type: fix
status: proposed
phase: specify
parent: T-219
blocked_by: []
related: []
work_package: PH3
owner: the project owner
business_value: high
effort: m
created: 2026-08-29
updated: 2026-08-29
deliverables: []
---

# T-248 — Correct four numbers a shipped deck asserts and its own source contradicts

## 1. Specify

**Outcome**
Every number a shipped deck states agrees with the source model beside it. Today the reference deck's claim slide spends $5.6M on a package its own ask prices at $4.1M; `sort-window` prints a sort finish its stated rate contradicts by two hours, and the tripwire that should have caught it does not; `portfolio-review` attributes a transmission asset's $29M to renewables **on the slide that is its concentration argument**; and the adopter deck's sanitisation left the source project's own names in the documents beside it.

**Closes** `PR-81`, `PR-84`, `PR-85`, `PR-86` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: the three source models, the slide copy quoting them, and the sanitisation pass on the adopter deck's documents
- In: **nothing else** - every finding this task closes is named above, and each statement stays in the register rather than being restated here (the method's umbrella condition 2)
- Out: any finding not in the list above
- Out: committing to a remedy before measuring it. A remedy is a hypothesis (the method's section 5); a fix that the measurement refuses is reported here and its finding stays open

**Inputs**
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3 - the rows for `PR-81`, `PR-84`, `PR-85`, `PR-86`
- `CLAUDE.md`'s publishing rule, which the adopter deck's remaining names are measured against
- **L-127** - a figure can be arithmetically right and relationally wrong

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
