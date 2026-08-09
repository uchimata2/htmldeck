---
id: T-057
title: The 3D visual class, the frame-rate figure, and DS-140's fifth motion
type: deliverable
status: proposed
phase: specify
parent: T-016
blocked_by: []
related: [T-007, T-016, T-019, T-033]
work_package: v0.2
owner: maintainer
created: 2026-08-09
updated: 2026-08-09
deliverables:
  - docs/DESIGN-SYSTEM.md
  - docs/LESSONS.md
---

# T-057 — The 3D visual class, the frame-rate figure, and DS-140's fifth motion

## 1. Specify

**Outcome**
The three capabilities [T-016](T-016-the-interaction-and-motion-layer.md) specified and did not
build: a **functional 3D visual** whose motion *is* the depth encoding, a **frame-rate figure** with
the machine it was measured on stated beside it, and the **DS-140 amendment** the first of those
forces. Split out of T-016 on 2026-08-09 so that v0.1 ships; none of the three is a shipping
requirement, and all three are wanted.

**Why it is separate rather than dropped**
The reference deck runs four named motions, ten disclosure sets and a ruler, and the gate holds it
to all of them. What it does not have is 3D of any kind — measured, `0` — and no deck in this
repository has ever had its frame rate measured on any machine. Those are **capabilities the layer
does not yet reach**, not defects in what it does. A first release that says so is honest; one that
holds itself back for them is slower for no reader's benefit.

**Scope**
- In: a functional 3D visual — one that encodes something a 2D rendering would lose — with a
  **chosen static projection** as its reduced-motion and print fallback, and DS-218's stop control
  reaching it.
- In: the DS-140 question that visual forces, argued and settled either way.
- In: a frame-rate instrument, and a number with a machine beside it.
- In: demonstrating the result on a real 12-slide deck, in both renderings, opened and looked at.
- Out: **the component contract and the motion tokens.** T-016 landed both;
  [`COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) says what a 3D component would have to
  declare, and every named motion already reads its easing and duration from the theme.
- Out: 3D for emphasis. Permitted (DS-144) and not what this task is for.

**Inputs**
- [T-016](T-016-the-interaction-and-motion-layer.md) §1 — the measurement, the owner's answer on
  what 3D is for, and the three consequences it names.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §5.2 — **DS-140**, still a closed vocabulary
  of four; **DS-144**, which permits a 3D card reveal and forbids a 3D slide transition; **DS-218**,
  the stop control every looping motion owes.
- [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) §3.8 — what a new motion has to
  declare to be part of the layer rather than beside it.
- [`docs/research/R7-printable-mode.md`](../docs/research/R7-printable-mode.md) §5.2 — print loses
  3D, already recorded.
- [`docs/LESSONS.md`](../docs/LESSONS.md) — **L-38**, **L-45**, **L-15**.

**Acceptance criteria**
- [ ] **A functional 3D visual demonstrated** — one that encodes something a 2D rendering would
      lose — with a **chosen static projection** as its reduced-motion and print fallback, not a
      frozen mid-wobble frame, and with DS-218's stop control reaching it
- [ ] **DS-140 has a named side**: a fifth motion, or an exemption clause with a stated reason.
      Argued from a rendering rather than from a plan, and settled **before** the figure ships —
      a deck that fails its own gate is the worse outcome
- [ ] The new motion, whichever way DS-140 goes, reads its duration and easing from the theme and
      carries a row in [`COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) §3.8
- [ ] Frame rate held on a real 12-slide deck with the heaviest slide on screen; **number stated,
      and the machine it was measured on stated with it**
- [ ] Demonstrated on a real 12-slide deck, opened and looked at offline, in both renderings

**Open questions**
- **Is the wobble a fifth motion or an exemption to DS-140?** T-016 §1 argues the case for the
  exemption — the oscillation *is* the depth encoding, so it is the one class of never-settling
  motion that satisfies §9.2's *motion must encode something* — and records that this is a
  **ruleset change to raise, not a licence to take quietly**, on
  [T-033](T-033-reconcile-ds-131-with-the-chrome-budget.md)'s precedent. Owner, with the rendering
  in hand.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | **The frame-rate instrument**, and a number with the machine beside it. Independent of the rest, and the only one of the three that measures what already exists | a measurement stage, and the figure recorded in §3 |
| 2 | **Build the 3D figure** to the point where it can be looked at — the visual, its motion, and the chosen static projection | a figure, in a working deck |
| 3 | **Raise the DS-140 question with that rendering in hand**, and settle it | a `DESIGN-SYSTEM.md` amendment with a named side |
| 4 | **Wire it to the contracts**: the motion's tokens in `THEME-CONTRACT.md` §3.6, its rule in `COMPONENT-CONTRACT.md` §3.8, DS-218's stop control reaching it | rows in both contracts, and the gate green |
| 5 | Demonstrate, offline, in both renderings; record what generalises | the deck, and [`docs/LESSONS.md`](../docs/LESSONS.md) |

**Approach decisions**

- **Steps 2 and 3 are one decision and the order inside it is fixed.** Build the figure far enough
  to argue from, settle the rule, *then* ship. T-016 recorded this and it is the reason the two
  steps travel together rather than the 3D landing first and the ruleset catching up.
- **The frame-rate step is first because it is independent.** It needs no 3D and no rule change,
  and it is the one measurement this repository has never taken, so it stops being owed on the day
  it runs.

## 3. Implement

**Not started.**

**Decisions & assumptions**
- <none yet>

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
| 2026-08-09 | → proposed | **Split out of [T-016](T-016-the-interaction-and-motion-layer.md) so that v0.1 ships.** T-016 replanned into eight steps on 2026-08-09 and completed four: the reduced-motion render, the component contract, the gate that holds a deck to it, and the editorial split rule. The remaining four are **capabilities the interaction layer does not reach**, not defects in what it does — the deck has no 3D at all, and no deck here has ever had its frame rate measured. Holding a release for them buys no reader anything, and each is wanted, so they move rather than being dropped. **The order inside the task is the part worth carrying over**: the wobble is a fifth motion or an exemption, DS-140 is a closed vocabulary of four, and shipping the figure before the ruleset has a named side produces a deck that fails its own gate. |
