---
id: T-156
title: Make the screening partition a figure a checker can count
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-136, T-154, T-130]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-14
updated: 2026-08-14
deliverables: []
---

# T-156 — Make the screening partition a figure a checker can count

## 1. Specify

**Outcome**
The sentence *"the three verdicts partition the catalogue: N adopted, M rejected, K deferred, summing
to S"* stops being prose nobody checks. A command counts the rows of the screening table in
[`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §4 and the catalogue rows in
[`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
§7, and a gate fails when either the four numbers in the sentence or the two documents' totals
disagree with what is actually there.

**Why this exists**
Found while re-running the research
([T-136](T-136-re-run-the-external-research-with-a-recorded-search-record.md)). **The claim has been
wrong twice and no gate said so** — first at nineteen entries with two missing, then at twenty-one
with fourteen missing. Both times the arithmetic inside the sentence was self-consistent, because the
sentence was checked against itself.

**It is a part-of-whole claim with no binding.** `tools/docs/figures.py` binds exactly this shape, but
only through a declared `ACCOUNTS` entry naming a command whose output carries the labels — and there
is no command that prints these counts. The claim is a *count of table rows the document itself
contains*, which is the easiest kind of figure to derive and the only one here still hand-maintained.
**L-97** is the general rule: a check anchored on the value that drifts goes blind exactly when it is
needed.

**Scope**
- In: a command that counts the two tables and prints the four numbers with their labels.
- In: an `ACCOUNTS` entry binding the §4 sentence to it, or a reason recorded for why the existing
  binding cannot serve and what does instead.
- In: the cross-document check — the size stated in `R8` §7 and in `CONTEXT-AUDIT.md` §4 must agree.
- Out: changing any verdict. This is a checker, not a re-screening.
- Out: generalising to every table in the tree. **Two documents, one claim.**

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §4 and §4.1 — the claim and how it was found
- `tools/docs/figures.py` — `ACCOUNTS`, and the module docstring's account of what a binding owes
- [T-154](T-154-bind-the-measurements-that-five-live-documents-state-in-prose.md) §3 — the false-alarm
  count that decides whether a binding of this shape is worth keeping
- **L-84**, **L-97**

**Acceptance criteria**
- [ ] A command prints the three verdict counts and the total, from the tables themselves
- [ ] A seeded wrong number in either document fails the gate, and the failure names which document
- [ ] A row added to `R8` §7 and left unscreened in §4 fails the gate — that is the case the partition
      never caught
- [ ] The check runs inside `python tools/check_all.py`, or its absence there is recorded with a reason
- [ ] No verdict text is edited by this task

**Open questions**
- **Does this belong in `figures.py` or beside it?** `figures.py` binds a claim to a command's output;
  here the "command" would be a counter written for one document pair, which may not earn a place in a
  general tool. — the implementer, from `figures.py`'s own docstring on what buys `ACCOUNTS` its place.

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
| 2026-08-14 | → proposed | Raised by [T-136](T-136-re-run-the-external-research-with-a-recorded-search-record.md) while re-running the research. **The partition sentence has been wrong twice and is checked by nobody**: it is a part-of-whole claim over rows the document itself contains, and `figures.py` binds that shape only through a declared `ACCOUNTS` entry pointing at a command — which does not exist for it. `PH3` because PH2 has shipped and this is not a defect in the published plugin. |
