---
id: T-134
title: State the tier model and bound tier 1 as a relation
type: decision
status: proposed
phase: specify
parent: T-130
blocked_by: []
related: [T-130, T-133]
work_package: PH3
owner: the project owner
business_value: high
effort: s
created: 2026-08-13
updated: 2026-08-13
deliverables:
  - CLAUDE.md
---

# T-134 — State the tier model and bound tier 1 as a relation

## 1. Specify

**Outcome**
This project states what its always-loaded set is, how membership is decided, and what bounds it —
so that every later cut to [`../CLAUDE.md`](../CLAUDE.md) is decided against a rule rather than
negotiated. **The finding is `CE-11`**, stated in
[`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.1; it is not restated here.

**This adopts a decision already taken upstream, and that is the point.** The taskmd project settled
this in its own audit: the membership rule is *what the harness loads without being asked* — a
property of the tree rather than a list someone maintains — with three tiers, a budget on tier 1
only, and the bound written as a **relation** to something counted from the same tree so that no
number and its justification can drift apart. It rejected, in writing, both alternatives an outsider
arrives with: widening the budget to cover every file, and budgeting each file separately. Nothing
here is being invented, and the audit that found this went looking for something to send upstream and
found the answer already there — see [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §7.2,
`O-T1`.

**Measured here, 2026-08-13:** tier 1 is **338 lines across three files** — the global preferences
(92), this project's `CLAUDE.md` (207), and the memory index (39) — or **27,633 bytes / ~6,908
estimated tokens**, before a skill-description block of a further ~5,200.

**It is an enabler and saves nothing by itself.** `CE-01` (split the release chronology out of
`CLAUDE.md`) and `CE-04` (one operative home per cumulative rule) are the cuts it makes decidable,
and it should land first so those cuts are not chosen to fit a number nobody agreed.

**Scope**
- In: the membership rule, the tiers, and the bound, written in the file they govern — which under
  this model is tier 1 itself, where a reader meets the boundary at the moment it binds them.
- In: **establishing tier 1 by observation, not by any file's claim about itself.** A document
  asserting a load discipline the harness does not implement is worse than one over budget, because
  it makes the bound unfalsifiable — that is the upstream finding's sharpest half.
- In: the measurement, dated, with the command that reproduces it.
- In: stating explicitly that tiers 2 and 3 carry no budget, and what that accepts.
- Out: moving any content. A budget that also chooses the cut is a cut chosen to fit a number; the
  moves are `CE-01` and `CE-04` and they are not this task.
- Out: a hand-set constant. It is the pair that has to be edited together, and it always loses.
- Out: the global preferences file, which is not this repository's.

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §2.1 and §6.1 — the measurement and `CE-11`
- [`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
  §2.1 — the tier model, the membership rule and the relation-bound, stated portably
- The upstream precedent, read at execution rather than named here

**Acceptance criteria**
- [ ] The always-loaded set is named by a **rule**, not a list, and the rule is checkable against the
      tree
- [ ] Tier 1 was established by observation — what a session receives unasked — and the method is
      recorded, not just the answer
- [ ] The bound is a relation between two quantities both counted from the tree; **no constant is
      written anywhere**
- [ ] Tiers 2 and 3 are stated as carrying no budget, with what that accepts written down
- [ ] Today's measurement is recorded with its date and its command, in a place where being stale
      makes it evidence rather than a false rule
- [ ] If the project is over its own bound on the day it is set, that is stated as dated debt naming
      the task that closes it — **an unmet budget that reads as met is worse than no budget**
- [ ] No content moves

**Open questions**
- **Which relation?** taskmd bounds tier 1 against the flat, single-document alternative its split
  replaced. This project has no such alternative, so the second term has to be chosen. — the owner,
  or the implementer from the rule's own reason.

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
| 2026-08-13 | → proposed | Raised from [T-130](T-130-audit-the-context-economy-of-an-agent-driven-repository.md)'s ranking at the owner's review, fourth of four and the only one above `xs`. `CE-11`, and **the direction of travel is upstream to here**: the audit went looking for something to send taskmd about context budgeting and found they had settled it first, in more detail, with both alternatives rejected in writing. It saves nothing by itself — it decides what `CE-01` and `CE-04` are allowed to cut, which is why it is ranked with them rather than after them. One question is left open on purpose: taskmd's bound has a natural second term and this project's does not, so which relation to use is a choice rather than a copy. |
