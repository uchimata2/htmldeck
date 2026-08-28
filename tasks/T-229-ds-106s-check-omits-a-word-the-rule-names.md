---
id: T-229
title: Derive DS-106's banned-terminology list from the rule instead of restating it
type: fix
status: proposed
phase: specify
parent: T-219
blocked_by: []
related: []
work_package: PH1
owner: the project owner
business_value: critical
effort: s
created: 2026-08-29
updated: 2026-08-29
deliverables: []
---

# T-229 — Derive DS-106's banned-terminology list from the rule instead of restating it

## 1. Specify

**Outcome**
No word DS-106's own sentence bans is missing from the check that decides it. Today `audit.ds106_no_banned_terminology` matches ten words and **`actually` is not among them**, while the rule names it - so `examples/measure-first/` uses it three times in slide copy and `examples/reference-deck.html` once, and both pass a `hard` rule the gate reports as checked.

**Closes** `PR-48` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: the four instances in two shipped decks
- In: **deriving the fallback list from the rule's own row**, which is the register's hypothesis and is against the obvious fix: adding one word closes the instance and leaves the class, because the list is written twice and nothing compares them
- Out: the four categories DS-106 names that no check implements - that is DS-107's, and a category nobody has built is a different thing from a word the rule wrote down

**Inputs**
- `PR-48` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) DS-106 and DS-107
- `tools/deck/ruleset.py` - the precedent for deriving from a row

**Acceptance criteria**
- [ ] every word DS-106's sentence names is decided by the check, proved by seeding each
- [ ] the four instances are gone from both decks and the decks rebuild
- [ ] `python tools/check_all.py` green

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
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`High`**: the method's section 4 gives that level one obligation beyond a child task — *the release does not go out while it is open*. |
