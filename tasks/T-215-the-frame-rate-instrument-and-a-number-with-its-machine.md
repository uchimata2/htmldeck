---
id: T-215
title: The frame-rate instrument, and a number with the machine it was measured on
type: deliverable
status: proposed
phase: specify
parent: T-057
blocked_by: []
related: [T-057, T-185, T-016]
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-08-22
updated: 2026-08-22
deliverables: []
---

# T-215 — The frame-rate instrument, and a number with the machine it was measured on

## 1. Specify

**Outcome**
A way to measure the frame rate a deck actually holds, and one recorded figure produced with it:
the number, the deck and slide it was taken on, and **the machine it was measured on stated beside
it**. No deck in this repository has ever had its frame rate measured on any machine.

**Why it is its own task**
Split out of [T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md) on
2026-08-22. T-057's own §1 calls itself *"three deliverables wearing one title"* and its plan step 1
says this one is **"independent of the rest, and the only one of the three that measures what
already exists"**. The third deliverable — the DS-140 amendment — was dissolved by the owner's
ruling of 2026-08-19, so T-057 was two things rather than three, and this is the half that needs no
3D visual, no ruleset change and no new component.

**It is the same argument T-016 used to create T-057.** T-016 split at `PH1` so a release would
ship; this splits so a measurement that can be taken today stops waiting behind an `xl` that cannot
start. T-057 has sat `proposed` since 2026-08-09 and this half was never the reason.

**Scope**
- In: an instrument that reports frames produced over a stated interval, on a real deck, with the
  heaviest slide on screen.
- In: one recorded figure, with **the machine named beside it** — that pairing is the deliverable,
  not the number alone.
- In: a stated home for the figure, so a later measurement on another machine adds a row rather
  than overwriting one. A single number with no machine is the thing this task exists to avoid.
- Out: **a gate.** Nothing here fails a deck. A frame-rate threshold is a claim about hardware this
  project does not have a corpus for, and inventing one from a single machine is exactly the
  reasoning **L-05** and the *scope warning* in
  [`docs/upstream/harness.md`](../docs/upstream/harness.md) both refuse.
- Out: the 3D visual, which stays in T-057 and is the case that would make the figure interesting
  rather than the case that makes it measurable.
- Out: any change to `render.py motion`, which seeks rather than plays and is settled (T-185).

**Inputs**
- [T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md) §1 — the criterion
  this inherits verbatim, and the scope sentence it is cut from.
- [T-185](T-185-no-instrument-here-can-watch-an-animation-play.md) — **the constraint that shapes this
  task.** `render.py motion` seeks the timeline and the computed style follows exactly, which makes
  every intermediate state measurable. What it explicitly **cannot** reach is *playback at a frame
  rate*, because headless produces no frames: a CSS animation's clock there is frame production
  rather than time (**L-26**). So this measurement cannot be taken by the headless harness that
  takes every other measurement in this repository.
- [`docs/EVALUATION.md`](../docs/EVALUATION.md) — where a measured figure is recorded, and the
  one-render-per-stage cost model.

**Acceptance criteria**
- [ ] Frame rate held on a real 12-slide deck with the heaviest slide on screen; **number stated,
      and the machine it was measured on stated with it** — inherited verbatim from T-057
- [ ] The instrument runs somewhere a person can repeat it, and what it needs is written down
- [ ] The figure's home takes a second row for a second machine without contradicting the first
- [ ] Nothing this task adds can fail a deck

**Open questions**
- **Where does the measurement run, given that headless produces no frames?** T-185 recorded that
  playback at a frame rate *"needs the owner's browser"*. That makes this the first measurement here
  taken outside the harness, so the instrument's output has to carry its own provenance rather than
  inheriting the harness's. **Owner** — whether they will run it, and on what.
- **What counts as *the heaviest slide*?** A count of animated elements is derivable and is probably
  the right proxy, but the honest answer may be *the slide with the 3D visual on it*, which does not
  exist until T-057. **Decide during specify**: if the answer is the second, this task measures the
  heaviest slide that exists today and T-057 re-measures, which is a row rather than a rewrite.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |

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
| 2026-08-22 | → proposed | **Split out of [T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md) while restating that task's dissolved DS-140 criterion.** T-057 was three deliverables wearing one title, the third went with the owner's 2026-08-19 ruling, and its own plan calls this half independent and the only one measuring something that already exists. `m` rather than `l` because there is no visual to build and no rule to change; `PH3` because it is not a defect in the published plugin. **The constraint carried over from T-185 is the whole shape of it**: headless produces no frames, so this is the first measurement here that cannot be taken by the harness. |
