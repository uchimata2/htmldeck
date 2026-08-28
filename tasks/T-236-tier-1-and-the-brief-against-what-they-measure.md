---
id: T-236
title: Correct tier 1's three figures and settle the tier-2 set the owner already ruled on
type: decision
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

# T-236 — Correct tier 1's three figures and settle the tier-2 set the owner already ruled on

## 1. Specify

**Outcome**
[`CLAUDE.md`](../CLAUDE.md) and [`BRIEF.md`](../docs/BRIEF.md) state figures that are re-derivable and currently wrong: the shipped decks' size by one deck and 640,565 bytes, the ruleset counts stale inside the paragraph that says to re-derive them, and rule 1's two figures which the specification records as measured false. **The tier-2 set is the decision half** - the owner ruled on 2026-08-23 that a tier-2 document is entered at the start of work of a kind, which makes `AUDIT-METHOD.md` a term and tier 1's debt 9,810 rather than the 2,248 the file states.

**Closes** `PR-11`, `PR-12`, `PR-14`, `PR-112` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: `CLAUDE.md`'s tier section, rules 1 and 6, and `BRIEF.md`'s three-documents table
- In: **nothing else** - every finding this task closes is named above, and each statement stays in the register rather than being restated here (the method's umbrella condition 2)
- Out: any finding not in the list above
- Out: committing to a remedy before measuring it. A remedy is a hypothesis (the method's section 5); a fix that the measurement refuses is reported here and its finding stays open

**Inputs**
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3 - the rows for `PR-11`, `PR-12`, `PR-14`, `PR-112`
- `PR-14`'s status cell, which carries the owner's ruling and the corrected figures
- [T-143](T-143-split-the-release-chronology-out-of-claude-md.md) and [T-144](T-144-give-each-cumulative-rule-one-operative-home.md) - the two cuts this bound was written to make decidable, both spent

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
