---
id: T-148
title: Give a measured figure a durable home
type: deliverable
status: proposed
phase: specify
parent: T-130
blocked_by: []
related: [T-130]
work_package: PH3
owner: the project owner
business_value: medium
effort: xs
created: 2026-08-14
updated: 2026-08-14
deliverables: []
---

# T-148 — Give a measured figure a durable home

## 1. Specify

**Outcome**
A figure this project measures once stops living only in the chain of session handovers, where it
propagates without anything able to check it. **The finding is `CE-08`**, stated in
[`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
§8; it is not restated here.

**The instance is measured and recorded** in [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md)
§8, `BP-2`: five successive handoffs carried *"the release gate takes 7–11 minutes"*; it is **154
seconds**. No committed document was wrong, because **no committed document stated it at all** — the
figure had no durable home, so nothing could be stale and nothing could be checked.

**This repository already has the mechanism**: `tools/docs/figures.py` binds a pasted figure to the
command that produces it and reports drift. A figure with a home is a figure that mechanism can
reach; a figure in a handoff is outside every gate this project owns.

**Scope**
- In: where a measured figure of this kind belongs, and the run-time figure as the first instance.
- In: whether it is bound as a checked figure or written as a dated measurement, which are different
  contracts.
- Out: the handoff format, which belongs to a skill this project does not own — observations about it
  go to [`../docs/upstream/handoff-skill.md`](../docs/upstream/handoff-skill.md).

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.2 — read before starting; §8 `BP-2` — the
  instance
- `R8` §8 — `CE-08` in full
- **L-74** in [`../docs/LESSONS.md`](../docs/LESSONS.md) — make a stored copy fail loudly in both
  directions

**What specifying must settle**
- Which figures qualify. *Everything measured* is a rule nobody keeps; *the release gate's run time*
  is one figure and not a rule at all.
- Whether the home is a checked figure under `figures.py` or a dated line in
  [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md), and what each costs when it goes stale.

**Acceptance criteria**
- Written at `specify`. §6.2 owns what an audit task owes beyond them.

**Open questions**
- ~~**Whether this needs a specify pass at all.**~~ **Answered 2026-08-14 by the owner: it does not
  need a decision pass.** It is `xs` with a known instance and a mechanism that already ships, so a
  specification written only to decide whether to spend the hour costs about what the hour costs.
  **This left the decision batch and takes the ordinary lifecycle in its turn** — `specify → plan →
  implement → review` in one pass, which is mandatory however small
  ([`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §2). What was dropped is the parking, not the phases.

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
| 2026-08-14 | → proposed | Raised at the owner's direction with the rest of the unraised findings; it ranked eleventh and was never a candidate. Scheduled to `plan` and no further, with one argument against that for this row in particular: it is `xs`, its instance is already measured, and the mechanism it would use ships — so the specification may be the expensive half. |
| 2026-08-14 | (unchanged) | **Removed from the decision batch the same day, the argument above accepted.** It sits in the execution order as ordinary work and runs the whole lifecycle when its turn comes. A task whose worth is not in doubt does not need a pass to establish it. |
