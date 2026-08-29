---
id: T-272
title: Make render.py motion enumerate the same animation set on every run of one deck
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-255]
work_package: PH1
owner: the project owner
business_value: high
effort: s
created: 2026-08-29
updated: 2026-08-29
deliverables: []
---

# T-272 — Make render.py motion enumerate the same animation set on every run of one deck

## 1. Specify

**Outcome**
`render.py motion` reports the same animations on the same deck every time it is run. Today it does
not: six consecutive runs of `python tools/deck/render.py motion examples/reference-deck.html
--into 3` on an unchanged tree returned **`17, 17, 18, 17, 17, 17`**. The eighteenth is
`(effect) on i#rulerRing.ruler-ring`, a 200 ms transition on the chrome, present in one run of six.

**Why it matters more than one row.** This is an instrument, and wave 1 of
[`../docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) exists because *work verified against
a lying instrument has to be verified again*. A before-and-after taken with this tool — which is
exactly what [T-232](T-232-two-entrance-motions-do-not-collapse-for-print.md) and
[T-268](T-268-three-chrome-and-timing-defects-in-deck-js.md) in B9 will do — can differ by an
animation for no reason in the deck. It is also the second intermittent instrument this batch has
met: [T-254](T-254-density-py-write-corrupts-every-self-closing-svg-tag.md)'s defect gave `0, 3, 3`
over three runs and cost the adopter the better part of a session for the same reason. **An
instrument that answers differently twice teaches a reader to distrust the deck rather than the
tool.**

**Scope**
- In: why the ruler ring's transition is in the set on some runs and not on others. The probe
  clicks `next` in a synchronous loop, so whether a CSS transition is created at all may depend on
  a style recalculation that the loop does not force — **that is a hypothesis and it is measured
  before anything is changed**
- In: whichever of *make it deterministic* or *report the variation honestly* the measurement
  supports. A count that is stated as stable and is not is worse than one that says it varies
- In: a run count high enough to say what the rate is, rather than one that saw it once
- Out: the seek arithmetic — [T-255](T-255-render-py-motion-seeks-past-the-delay.md) owns it and
  is closed
- Out: `--shots`, unless the measurement shows the same cause reaches it

**Inputs**
- [`tools/deck/render.py`](../tools/deck/render.py) — `MOTION_PROBE`, the click loop and the
  `before` set that decides which animations belong to the navigation
- the six runs above, taken 2026-08-29 on this tree while closing `T-255`
- [T-254](T-254-density-py-write-corrupts-every-self-closing-svg-tag.md) — the other intermittent
  instrument in this batch, and the record of what intermittency costs a reader

**Acceptance criteria**
- [ ] the rate is **measured over enough runs to state it**, before and after
- [ ] the set is stable across those runs, **or** the tool says which of its animations it cannot
      promise and why
- [ ] whichever it is, it is proved by seeding — the failing direction shown to fail (**L-125**)
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None yet. The hypothesis in the scope is a hypothesis; whoever implements it measures before
  committing to it.

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
| 2026-08-29 | → proposed | Found while closing [T-255](T-255-render-py-motion-seeks-past-the-delay.md), by diffing two post-fix runs of one command on one unchanged deck. Raised under [`../docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) §4's *absorb what a batch finds* and **added to the running batch B1**, which is what that authority says to do rather than filing it for later. **`PH1`**: `render.py` ships in the published `0.6.0`, and `CLAUDE.md`'s condition is a defect in the published plugin rather than who found it. `parent: null` and `related:` — a task that raises another is not its parent, on the owner's `T-057`/`T-016` precedent. |
