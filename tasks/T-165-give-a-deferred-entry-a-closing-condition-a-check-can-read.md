---
id: T-165
title: Give a deferred entry a closing condition a check can read
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-097, T-019, T-051]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-15
updated: 2026-08-15
deliverables: []
---

# T-165 — Give a deferred entry a closing condition a check can read

## 1. Specify

**Outcome**
Every entry in [`tools/deck/check.py`](../tools/deck/check.py)'s `DEFERRED` carries its **closing
condition** as a field a check can read, so an excusal that has stopped being true is reported rather
than found by a person sweeping the record after a release.

**Why it exists**
Raised at [T-097](T-097-ds-004s-excusal-says-degrade-gracefully-is-unobservable-and-ds-009-gave-it-an-instrument.md)'s
review, against its fifth acceptance criterion — *a note on whether an excusal can be held to its own
closing condition mechanically, or a task raised saying it cannot*. **It cannot, and the instance is
the task that raised this one.**

**The gap, stated precisely.** `staleExcusals` fires when a rule is **excused and checked** — the two
halves contradicting each other. DS-004 was excused and **not** checked, so the partition stayed
intact for nine months while the excusal quietly stopped being true: T-019 shipped DS-009's preflight,
which made *degrade gracefully* observable, and nothing anywhere could notice that half of DS-004's
reason had died. The account was not wrong; it was **silent by construction**, which is the harder
case and the one **L-54** names — an excusal outlives its subject and its stated reason goes false
with it.

**Why a closing condition is the right field.** Most `DEFERRED` entries already end with one in prose
— *CLOSES WHEN a second engine is in the harness*, *closed by the harness exposing it*. A sentence
cannot be evaluated; a field can be pointed at the thing that would close it. The shape this
repository already trusts for a hand-kept declaration is `figures.py`'s `ARTIFACTS` and `ACCOUNTS`,
and `audit.py`'s `ABSENCE_IS_A_PASS`: **a declaration that comes to cover nothing fails the run**.

**Scope**
- In: a closing-condition field on each `DEFERRED` entry, and a check that reads it.
- In: deciding what a closing condition may be **bound to** — another rule's id, a tool that must not
  exist, a capability the harness must gain. An entry whose condition binds to nothing is the defect
  this task is about, so it must fail rather than be accepted.
- In: the sweep — every existing `DEFERRED` entry gets one, or is reported.
- Out: re-deciding any excusal. This makes them answerable, it does not answer them.
- Out: the same question for the ruleset's `Reach` cells. One home at a time; `Reach` is prose in a
  table and a different problem.

**Inputs**
- [T-097](T-097-ds-004s-excusal-says-degrade-gracefully-is-unobservable-and-ds-009-gave-it-an-instrument.md)
  §1 and §4 — the instance, and why the account cannot see it
- [`tools/deck/check.py`](../tools/deck/check.py) — `DEFERRED`, and `account`
- [`tools/deck/audit.py`](../tools/deck/audit.py) `ABSENCE_IS_A_PASS` — a hand-kept table whose claims
  are **verified rather than trusted**, which is the pattern to copy
- **L-54**, **L-84**, **L-97**

**Acceptance criteria**
- [ ] Every `DEFERRED` entry carries a closing condition in a form a check reads, or is reported
- [ ] A condition that binds to nothing fails the run, demonstrated on a seeded entry
- [ ] An excusal whose condition is **already satisfied** is reported — that is DS-004's case, and the
      one nothing can see today
- [ ] The coverage account's arithmetic is unchanged, or its change is stated
- [ ] The self-test builds its own entries and does not assert the live table's contents (**L-78**)

**Open questions**
- **Can a closing condition be checked without running the thing that would close it?** DS-004's was
  *a second engine in the harness*; nothing can test that cheaply. A condition naming another **rule
  id** is decidable from the ruleset alone, which suggests two kinds and only one of them
  enforceable. — the implementer, at `specify`.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <none yet>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-15 | → proposed | Raised at T-097's review against its fifth acceptance criterion, which asked for exactly this decision: an excusal **cannot** be held to its closing condition mechanically today. **The evidence is T-097 itself** — DS-004's reason half-died when T-019 shipped DS-009's preflight, and `staleExcusals` could not see it because it only fires on a rule that is excused *and* checked. `s`, `PH3` because PH2 has shipped and this is not a defect in the published plugin. |
