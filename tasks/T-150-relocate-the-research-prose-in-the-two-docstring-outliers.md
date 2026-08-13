---
id: T-150
title: Relocate the research prose in the two docstring outliers
type: deliverable
status: proposed
phase: specify
parent: T-130
blocked_by: []
related: [T-130]
work_package: PH3
owner: the project owner
business_value: low
effort: s
created: 2026-08-14
updated: 2026-08-14
deliverables: []
---

# T-150 — Relocate the research prose in the two docstring outliers

## 1. Specify

**Outcome**
Two files stop carrying a research record inside their docstrings, and carry a pointer to it instead.
**The finding is `CE-12`**, stated in [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.1; it
is not restated here.

**Docstrings are 30% of `tools/**/*.py` and that is this project's deliberate style, not a finding** —
the audit rejected the general sweep in writing (§5.1), on the method's own test. Two files sit far
outside it: `tools/portability/build_probes.py` at **85% docstring (52,408 of 61,484 bytes)** and
`tools/deck/print_variants.py` at **58%**. `tools/deck/audit.py` is 36% and the largest file in the
tree, so its 52,230 bytes of docstring is the biggest single block.

**The risk is the finding's own**: these are the files whose behaviour is least obvious, which is
plausibly why they carry the most explanation. A relocation that makes a probe's reasoning
unfindable costs more than it saves. **Deletion is not the change.**

**Scope**
- In: those files only, and only prose that is a research record rather than a rule for the next
  editor.
- In: the pointer left behind, which is the part that decides whether this was worth doing.
- Out: the general sweep over rationale prose. Rejected 2026-08-08 by the method's own test, and
  reopening it is not this task.
- Out: any behaviour change. Docstrings only.

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.2 — read before starting; §6.1 — `CE-12`;
  §5.1 — the rejection this task must not quietly reverse
- `R8` §4.1 — the test for whether prose is doing work

**What specifying must settle**
- The test that separates *research record* from *rule for the next editor*, applied to a sample
  before any file is touched.
- Whether `audit.py` is in or out. It is not an outlier by ratio and is the largest block by volume,
  and those two facts point opposite ways.
- Where relocated prose lands in `docs/research/`, and what the pointer must say to be followed.

**Acceptance criteria**
- Written at `specify`. §6.2 owns what an audit task owes beyond them.

**Open questions**
- **Is it worth doing at all?** The gain is `M` on a read path taken rarely — these files are edited
  seldom — against a risk the audit states plainly. This is the row most likely to be `cancelled` on
  its own merits rather than on size.

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
| 2026-08-14 | → proposed | Raised at the owner's direction with the rest of the unraised findings; it ranked last of the thirteen and was never a candidate. **Scheduled to `plan` and no further.** The task exists partly to record a decision either way: the general sweep is already rejected in writing, and these two outliers are the only part of `F3` that survived that rejection. |
