---
id: T-185
title: No instrument here can watch an animation play, so any rule about motion over time is unverifiable
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-111, T-112, T-041, T-057, T-183]
work_package: PH3
owner: the project owner
business_value: high
effort: m
created: 2026-08-18
updated: 2026-08-18
deliverables: [tools/deck/render.py]
---

# T-185 — No instrument here can watch an animation play, so any rule about motion over time is unverifiable

## 1. Specify

**Outcome**
There is one command that renders a deck in a browser whose **document timeline actually runs**, and
reports what an animation did — that it started, that it ended, and what the element looked like part
way through. Today nothing here can answer any of those, so every rule about motion over time rests
on reading the CSS.

**Measured 2026-08-18, on three instruments**

| Instrument | What it does with a running CSS animation |
| :--- | :--- |
| the preview pane | `document.timeline.currentTime === 0`. `getAnimations()` reports `playState: "running"`, `currentTime: 0`, **forever**. A screenshot refuses: *the Browser pane is not displayed, so the page is not compositing frames* |
| `render.py` headless | **pins motion off before capturing**, by design (DS-221, and the settling problem its own docstring describes). Under `--virtual-time-budget` a 420 ms animation fires no `animationend` after 1.2 s of chained timeouts |
| Claude in Chrome | not connected in this environment |

The pane's reading is the sharp one: **an animation reported as `running` whose `currentTime` never
leaves 0** is an instrument that says yes to every question about whether motion works. It is
**L-110**'s dead instrument with a different face — the tell is not a picture that fails to change,
it is a clock that does not tick.

**What this actually blocks.** It is not one task's inconvenience:

- [T-111](T-111-a-named-slide-transition-chosen-per-deck.md) is built, gated and green, and is held
  at `in_progress` because *the transition has never been seen to play*.
- [T-112](T-112-motion-density-and-the-split-between-content-and-affordance-motion.md) is about
  motion density, which is a claim about several animations at once.
- [T-041](T-041-implement-the-nine-glitch-free-conditions.md)'s conditions are largely about what
  happens *during* a change.
- [T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md) needs a frame rate,
  which is the same measurement one level harder.

**Why `high`.** The project's own rule is that a deck is looked at (`CLAUDE.md` rule 6), and for
motion that is currently impossible rather than merely skipped. A gate that is green on a deck whose
motion has never run is exactly the shape of **L-05**, and four open tasks depend on it.

**Scope**
- In: making at least one instrument advance a real timeline, and proving it does — the proof is a
  reading that *changes*, not a run that succeeds.
- In: reporting an animation's lifecycle: did it start, did it end, and one sampled state part way
  through.
- In: a way to capture a deck **mid-transition** on purpose. `render.py` pins motion off for good
  reasons; this needs the opposite, and it needs to be a different verb rather than a flag that
  weakens the existing guarantee.
- Out: changing DS-221 or the reasons captures pin motion off. The default stays; this adds a
  deliberate exception with its own name.
- Out: a frame-rate figure. That is T-057's, and it needs this first.

**Inputs**
- [`tools/deck/render.py`](../tools/deck/render.py) — the Chrome runner, the virtual-time budget,
  and the settling problem it documents.
- [`docs/lessons/L-110.md`](../docs/lessons/L-110.md) — the instrument that fails silently.
- [T-111](T-111-a-named-slide-transition-chosen-per-deck.md) §3 — the three readings above, in the
  terms they were taken.

**Acceptance criteria**
- [ ] One command renders a deck with a timeline that advances, proved by a reading that changes
      between two samples of the same page
- [ ] It reports, for a named animation: started, ended, and one intermediate state
- [ ] It can capture a deck mid-transition, and the capture is visibly different from the settled one
- [ ] The existing motion-pinned capture path is unchanged and still the default
- [ ] T-111's transition is verified through it, and T-111 closes

**Open questions**
- Whether the answer is a different Chrome invocation (no virtual-time budget, a real timeline, a
  screenshot on a timer) or a different instrument entirely. The first is cheap to try and should be
  tried first.

**One fallback is not an agent's to take, and it is worth knowing before the attempt.** If the
Chrome-invocation route fails, the remaining instrument is the real browser named in the table
above, and connecting it is the **owner's** action rather than this task's: the extension has to be
installed and signed in under the same account. So a run can legitimately reach the end of the cheap
path and stop with nothing left to try. **That is a clean stopping point, not a failure**, and it
should be reported as one rather than worked around with a weaker instrument.

## 2. Plan

<not started>

## 3. Implement

**Decisions & assumptions**
- <none yet>

**Outputs produced**
- <none yet>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :--- | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-18 | → proposed | Raised out of [T-111](T-111-a-named-slide-transition-chosen-per-deck.md), which is built and green and cannot be closed because nothing here can watch it move. Three instruments measured and all three refuse in different ways; the pane's is the one worth remembering, since it reports an animation as `running` at `currentTime: 0` indefinitely rather than failing. `PH3` by [`../CLAUDE.md`](../CLAUDE.md)'s rule — no published deck is broken, but four open tasks are held behind it. |
