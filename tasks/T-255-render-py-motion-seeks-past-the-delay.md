---
id: T-255
title: Add the delay in the report branch and drop the subtraction in the capture branch
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-225]
work_package: PH1
owner: the project owner
business_value: critical
effort: s
created: 2026-08-29
updated: 2026-08-29
deliverables: []
---

# T-255 — Add the delay in the report branch and drop the subtraction in the capture branch

## 1. Specify

**Outcome**
`render.py motion` samples an animation's own life. Today two branches write a seek and both are off by the delay: the report branch takes a fraction of duration from a clock that already includes the delay, and the capture branch subtracts the delay from an absolute clock that was already correct. **A working motion reads as dead** — *the computed style DOES NOT MOVE* is printed as a finding about the deck when it is a finding about the seek. Any non-zero delay shifts the whole report invisibly, and `rise` at delays 0, 60, 120, 180 and 240 is htmldeck's own reference stagger.

**From the adopter report** [`017`](../docs/adopter-reports/claimai/017-render-py-motion-seeks-a-fraction-of-duration-and-ignores-the-delay.md).

**Scope**
- In: both branches, `render.py` `:597-598` and `:602`
- In: **the verdict line naming which it is** — an animation that interpolates to nothing and one whose sampled range never left the delay are different findings, and the second is the tool's own fault
- Out: anything the records above do not name. The report is a closed one-way hand-over — there is no
  channel back and none is expected, so a question this task cannot answer is settled here rather
  than asked.

**Inputs**
- the record above, [`017`](../docs/adopter-reports/claimai/017-render-py-motion-seeks-a-fraction-of-duration-and-ignores-the-delay.md) — each carries its evidence, its version and its own proposed fix
- the adopter's reproduction: at `delay 600, duration 300` the five offsets are `0, 75, 150, 225, 300` and every one falls inside the delay
- the 100% offset reading `opacity 0.99902` on a staggered entrance — the report stops at 340 where the animation's real end is 400, so the frame labelled 100% is not the settled state

**Acceptance criteria**
- [ ] every record named above is **closed with its remedy measured**, or explicitly deferred with the
      reason recorded in this task
- [ ] each fix is proved by seeding the defect and watching the check fire, in both directions where
      the record's own evidence is a verdict (**L-125**)
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None yet. Every record carries its own evidence and its own proposed fix; the proposal is a
  hypothesis and whoever implements it measures before committing to it.

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
| 2026-08-29 | → proposed | Raised by [T-225](T-225-triage-the-claimai-adopter-report.md), the triage of the ClaimAI adopter report. **`PH1`**: a defect an adopter met in the published `0.6.0`, which is `CLAUDE.md`'s one condition for reopening the phase. Verified against this tree before the record was actioned — the report's `Version seen` was stamped rather than re-run on fourteen of the twenty-seven. |
