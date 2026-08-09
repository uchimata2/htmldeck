---
id: T-043
title: Make the gate's coverage account provable, and derive the counts the documents state
type: fix
status: proposed
phase: specify
parent: T-042
blocked_by: []
related: [T-005, T-037, T-038]
work_package: none
owner: the project owner
created: 2026-08-09
updated: 2026-08-09
deliverables:
  - tools/deck/check.py
  - tools/deck/ruleset.py
---

# T-043 — Make the gate's coverage account provable, and derive the counts the documents state

## 1. Specify

**Outcome**
`tools/deck/check.py`'s coverage account partitions the owned rules — every owned rule in exactly
one bucket, the buckets summing to the total — and the self-test fails when it does not.
`tools/deck/ruleset.py` gains a mode that reports the counts the documents state, so the figures in
`BRIEF.md` and `EVALUATION.md` are re-derived rather than re-typed.

**Why this one**
`account()`'s docstring already claims the property: *"Every owned rule lands in exactly one
bucket."* It does not hold, and the assertion that would have caught it was written and disabled:

```
owned 111  checked 79  byRuleset 4  deferred 29  silent 0
sum of buckets 112
checked & byRuleset -> ['DS-072']
```

DS-072 carries `Reach: off-gate` — *"headless has no user gesture to enter fullscreen with… a person
pressing F11 is the only real demonstration"* — and `contract.py` emits a `pass` for it anyway. The
verdict's own text is honest, so nothing is mis-measured; what is wrong is the **account**, and the
account is the deliverable T-005's own log calls the point of the task: *"Silent went from 64 to 0,
and that is the deliverable."* An account that cannot add up is the same defect as a silent rule
with the sign flipped, which is exactly what `staleExcusals` was built to catch — and it never
looks at `cited & by_ruleset`, the one pair that occurs.

`check.py:251` is the assertion that should have failed:

```python
if len(a["silent"]) != len(own) - 3 - len(...) - len(...):
    pass          # the arithmetic is asserted below in the form that matters
```

The comment is false. No later assertion checks the partition.

**The second half is the same fault in prose.** `EVALUATION.md` §1 already records the rule counts
going stale twice and instructs *"re-derive them, never adjust them by hand"* — and nothing derives
them. `ruleset.py` computes every figure those documents quote and no consumer compares the two.

**Scope**
- In: making the account a partition, and deciding what an `off-gate` rule that a stage nonetheless
  measures is reported as.
- In: a self-test that fails on a non-partition and on `cited & by_ruleset`, replacing the disabled
  assertion rather than sitting beside it.
- In: `ruleset.py --counts` (or equivalent) printing every figure the documents state — totals by
  `Label`, by `Check`, by `Reach`, and the owned/hard split — in a form that can be pasted or diffed.
- Out: **changing any verdict.** No rule gains or loses a check here; only the bookkeeping moves.
- Out: correcting the figures where the documents state them. That is
  [T-045](T-045-sweep-the-stale-claims-across-the-live-documents.md), which this task unblocks.
- Out: a check that reads the documents and fails on a stale number. Tempting and larger than it
  looks — a count in prose has no stable anchor — and it should be raised on evidence that pasting
  is not enough, not assumed now.

**Inputs**
- [`tools/deck/check.py`](../tools/deck/check.py) — `account()`, `self_test()`, and the `DEFERRED` table
- [`tools/deck/ruleset.py`](../tools/deck/ruleset.py) — the `excused` property and the counts
- [`tools/deck/contract.py`](../tools/deck/contract.py) — the DS-072 verdict
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — the `Reach` column's contract
- [T-042](T-042-audit-the-whole-repository-against-itself.md) §2, F-2 and F-13

**Acceptance criteria**
- [ ] `checked + excusedByRuleset + deferred + silent == owned`, asserted in `self_test()` and shown
      to fail when it is broken on purpose (**L-04**)
- [ ] `cited & by_ruleset` is a reported fault, in the same shape as `staleExcusals`
- [ ] No rule appears in two buckets on the reference deck
- [ ] The disabled `if …: pass` is gone, not left beside its replacement
- [ ] `ruleset.py` prints every count `BRIEF.md` and `EVALUATION.md` quote, derived, in one run
- [ ] The reference deck still passes, and the printed headline states the corrected split

**Open questions**
- ~~Is an `off-gate` rule that a stage nonetheless measures `checked` or `excused`?~~ **Answered
  2026-08-09 by the reason `Reach` was given a column.** `DESIGN-SYSTEM.md` defines `off-gate` as
  *"decidable in principle but not by this instrument"* — so a measurement taken against a **double**
  is not the rule being decided, and counting it as `checked` is the gate claiming a reach the
  ruleset denies it. **DS-072 is `excused`, and its measurement stays in the output as a note under
  the excusal** rather than as a verdict. That keeps the information, keeps the account honest, and
  makes the general rule one line: *a rule the ruleset excuses is never `checked`, whatever a stage
  happens to measure.*

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <path>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-09 | → proposed | Raised by [T-042](T-042-audit-the-whole-repository-against-itself.md), findings F-2 and F-13. **The account is one over on 111 rules and the assertion that would have said so is `if …: pass` under a comment claiming the arithmetic is asserted elsewhere** — it is not. DS-072 is `checked` and excused by the ruleset at the same time. Ordered first among the audit's children because five documents and four task files quote the figure it corrects, so fixing the prose first would write the wrong number twice. |
