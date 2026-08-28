---
id: T-243
title: Re-bind five checks on what is true at run time instead of on a name
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

# T-243 — Re-bind five checks on what is true at run time instead of on a name

## 1. Specify

**Outcome**
Five checks decide a property rather than recognise a spelling - the shape [T-214](T-214-ds-142s-checker-is-an-allow-list-of-one-class-name.md) and [T-202](T-202-amend-ds-122-into-a-threshold-and-bind-its-check-on-structure.md) each fixed once. Today DS-239's ranking finds its subject by class name; the figure ledger recognises one deck's vocabulary so `FIG-1`'s denominator is what the pattern admits; DS-032's check names one licence where the rule names a class; `theme.py`'s self-test builds its negative fixtures out of the **tracked theme's current text**, so a legitimate edit breaks the test; and two variant suites accept an anchor matching more than once.

**Closes** `PR-44`, `PR-45`, `PR-49`, `PR-54`, `PR-57` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: `density.py`'s class lists, `content.py`'s `UNITS`, `audit.py`'s `STATIC` entry for DS-032, `theme.py`'s `self_test` fixtures, and the two variant suites' anchors
- In: **nothing else** - every finding this task closes is named above, and each statement stays in the register rather than being restated here (the method's umbrella condition 2)
- In: **from the ClaimAI adopter report, [`020`](../docs/adopter-reports/claimai/020-ds-229-keys-motion-rows-to-exact-selector-text.md)** — `DS-229` keys the contract's motion rows to **exact selector text**, so `:where(.slide[data-played]) .pulse` no longer has a row the contract can find — the tokens are declared, the motion works, and the gate reports the row unsatisfied. Scoping a motion to a state is the ordinary way to say *this plays on arrival*, and the rule makes the natural construction fail and the awkward one pass
- In: **from the ClaimAI adopter report, [`021`](../docs/adopter-reports/claimai/021-ds-239-re-derives-m-rank-so-removing-one-motion-invalidates-the-rest.md)** — `DS-239` re-derives `--m-rank` **from the deck**, so ranks are properties of the set rather than of a motion: removing two of five content motions left the other three wrong with nothing in the edit touching them. `PR-44` already names this rule. The record's added half is that **the gate should print the value it derives, per motion** — it knows it, and printing it turns a bisection into an edit
- Out: any finding not in the list above
- Out: committing to a remedy before measuring it. A remedy is a hypothesis (the method's section 5); a fix that the measurement refuses is reported here and its finding stays open

**Inputs**
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3 - the rows for `PR-44`, `PR-45`, `PR-49`, `PR-54`, `PR-57`
- **L-125** - before amending a rule, read what its gate actually tests
- the memory entry *a self-test must not assert repo state*, which `PR-54` is an instance of
- [`020`](../docs/adopter-reports/claimai/020-ds-229-keys-motion-rows-to-exact-selector-text.md), [`021`](../docs/adopter-reports/claimai/021-ds-239-re-derives-m-rank-so-removing-one-motion-invalidates-the-rest.md) — the adopter records merged into this task by [T-225](T-225-triage-the-claimai-adopter-report.md), because this task already owns the class. Each carries its own evidence and version.

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
