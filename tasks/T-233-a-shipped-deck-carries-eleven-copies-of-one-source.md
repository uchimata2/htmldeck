---
id: T-233
title: Remove the ten dead quick-view payloads, and fix the verb that writes them
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

# T-233 — Remove the ten dead quick-view payloads, and fix the verb that writes them

## 1. Specify

**Outcome**
A deck carries one copy of each source it quotes, and the verb that repairs a drifted quick view writes the copy the deck reads. Today `portfolio-review.html` carries 12 templates and 2 distinct payloads - `Portfolio model` eleven times at 8,451 bytes each, **84,510 bytes and 21.3% of the deck** - and `deck.js` keys on `data-qv` so the last wins and ten are dead. `rewire()` substitutes with `count=1`, so the repair writes the copy nobody reads.

**Closes** `PR-83` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: the ten copies, which are byte-identical to the eleventh so removing them is a deletion
- In: **which of the three sites is the defect** - the register's hypothesis names `wire()`, `rewire()`'s `count=1` and the gate's dedupe, and says each is right on a deck with one copy per source and wrong on this one
- Out: the quick view's design, which is correct and is what the docstrings state

**Inputs**
- `PR-83` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3
- [`tools/deck/quickview.py`](../tools/deck/quickview.py) - `wire()` and `rewire()`
- [`shell/deck.js`](../shell/deck.js) - the `qvSrc` lookup

**Acceptance criteria**
- [ ] the deck carries one template per distinct payload, and its byte count is stated before and after
- [ ] `rewire()` repairs the copy the deck actually reads, proved by drifting one and repairing it
- [ ] the quick view **opened and looked at** on the rebuilt deck, per `CLAUDE.md` rule 6

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
