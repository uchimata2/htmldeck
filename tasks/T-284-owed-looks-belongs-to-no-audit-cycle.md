---
id: T-284
title: Give OWED-LOOKS.md an audit cycle, or a rule that says which one reads it
type: fix
status: proposed
phase: specify
parent: T-219
blocked_by: []
related: [T-273, T-223]
work_package: PH3
owner: the project owner
business_value: medium
effort: xs
created: 2026-08-30
updated: 2026-08-30
deliverables: []
---

# T-284 - Give OWED-LOOKS.md an audit cycle, or a rule that says which one reads it

## 1. Specify

**Outcome**
`python tools/docs/cycles.py` exits 0. Today it exits **1**, on one file:

```
  UNASSIGNED  docs/OWED-LOOKS.md
The partition no longer holds: 1 file(s) in no cycle, 0 rule(s) matching nothing, 0 cycle(s) empty
without saying why.
```

**Why it is open and nothing has said so.** `cycles.py` is deliberately not a gate - `check_all.py`
carries the reason in `NOT_RUN`, and it is a good one: a tracked file with no audit reader is a
defect in [T-219](T-219-pre-release-audit-of-the-whole-repository.md)'s coverage and not in the
release, and wiring it in would block a release over an unassigned document. So the failure is real
and silent, and it surfaced here only because a handoff sweep ran the tool by hand on 2026-08-30.

**What it costs.** Cycle 40's acceptance criterion is *every tracked file is read, skipped with a
stated reason, or produced a finding*. That claim cannot be made over a file no cycle reads, so the
audit cannot close honestly while this holds - and `B23` is where it would be found, one batch
before the release.

**How it arrived.** [T-273](T-273-the-owed-looks-have-no-queue-to-accumulate-in.md) created
[`../docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md) while closing `B7` on 2026-08-29, under the
remediation order's `s4` *absorb what a batch finds*. The file was correct, its home was correct, and
no cycle rule was written for it - which is the failure mode
[T-223](T-223-derive-the-audit-cycles-membership-instead-of-counting-it.md) made **visible** rather
than impossible: a derived partition reports the hole instead of hiding it, and reporting it is all
it can do.

**Scope**
- In: the cycle rule that gives `docs/OWED-LOOKS.md` a reader, in `tools/docs/cycles.py`'s rule table
- In: **which cycle**, which is the only real question. The file is the audit's own machinery rather
  than a project document, so cycle 21's *the audit's own record* and cycle 1's *the human-facing
  set* both have a claim, and the answer decides who re-reads it at cycle 41
- Out: making `cycles.py` a gate. `check_all.py`'s stated reason for excluding it is unchanged by
  this, and cycle 42 is where that question already sits
- Out: any other unassigned file. There is exactly one today, and a sweep for the next is what
  `cycles.py` already does on every run

**Inputs**
- `python tools/docs/cycles.py` - the partition and its verdict, which is the whole of the evidence
- `tools/check_all.py`'s `NOT_RUN` entry for `cycles.py` - why this is not a release blocker
- [T-223](T-223-derive-the-audit-cycles-membership-instead-of-counting-it.md) - why the membership is
  derived, and why that is what made this reportable at all

**Acceptance criteria**
- [ ] `python tools/docs/cycles.py` exits 0 and reports no unassigned file, no rule matching nothing
      and no silently empty cycle
- [ ] the cycle chosen is stated with its reason, in the rule table rather than in this record
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- Which cycle reads it - see scope bullet 2. Decidable from the rule table's own reasons; it does not
  need the owner.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision - rationale - date>

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
| 2026-08-30 | -> proposed | Found by the handoff's reconcile sweep after `B13`, running `cycles.py` by hand to check a figure in [`../docs/AUDIT-METHOD.md`](../docs/AUDIT-METHOD.md). **`PH3`**: no adopter meets it, the published plugin behaves correctly, and it is this repository's own audit machinery - so `CLAUDE.md`'s one condition for reopening `PH1` is not met. **`xs`**: one rule row and the reason for it. |
