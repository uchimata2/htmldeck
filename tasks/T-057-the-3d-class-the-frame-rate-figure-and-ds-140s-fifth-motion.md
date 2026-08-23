---
id: T-057
title: The 3D visual class, the frame-rate figure, and DS-140's fifth motion
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: [T-214]
related: [T-007, T-016, T-019, T-033, T-187, T-215]
work_package: PH3
owner: maintainer
business_value: medium
effort: l
created: 2026-08-09
updated: 2026-08-23
deliverables:
  - docs/DESIGN-SYSTEM.md
  - docs/LESSONS.md
---

# T-057 — The 3D visual class, the frame-rate figure, and DS-140's fifth motion

## 1. Specify

**Outcome**
A **functional 3D visual** whose motion *is* the depth encoding, with a chosen static projection as
its reduced-motion, print and low-density fallback. Split out of
[T-016](T-016-the-interaction-and-motion-layer.md) on 2026-08-09 so that PH1 ships; not a shipping
requirement, and wanted.

**This was three deliverables and is now one.** *Restated 2026-08-22.* The **DS-140 amendment** the
3D visual was said to force no longer exists to make: asked on 2026-08-19 to rule the wobble a fifth
motion or an exemption, the owner rejected both and the frame under them, and
[T-187](T-187-open-the-motion-vocabulary-into-a-style-guide.md) opened DS-140 into a suggested set
plus an admission test with no name in it. The **frame-rate figure** is
[T-215](T-215-the-frame-rate-instrument-and-a-number-with-its-machine.md), split out on 2026-08-22
on this task's own plan step 1, which calls it independent of the rest and the only one of the three
that measures something that already exists. **Re-estimated `l` from `xl`** on what is left. The
title still says *fifth motion* and is now wrong twice over; the file is not renamed because the id
is pointed at from many documents.

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
- In: the motion passing **DS-140's admission test and DS-142**, argued from the rendering. What
  changed here on 2026-08-22 is the question, not the obligation - see the criterion below.
- In: demonstrating the result on a real 12-slide deck, in both renderings, opened and looked at.
- Out: **the frame-rate instrument and its figure**, now
  [T-215](T-215-the-frame-rate-instrument-and-a-number-with-its-machine.md). It measures what
  already exists and nothing here gates it.
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
      lose — with a **chosen static projection** as its reduced-motion, print **and low-density**
      fallback, not a frozen mid-wobble frame, and with DS-218's stop control reaching it.
      *Low-density added 2026-08-22: DS-238 is a third path to a stopped motion and nothing wired
      the fallback to it — see the decision below*
- [ ] **The motion passes DS-140's admission test, clause by clause, argued from the rendering
      rather than from a plan** — what it encodes (DS-150), that the slide was not built around it
      (DS-243), its declared kind (DS-237), its band or its `--motion-long` licence (DS-141), and
      that it survives reduced motion (DS-143), print (DS-224) and the stop control (DS-218).
      **And it passes DS-142**, which the admission test does not name and which fails any infinite
      animation outside one hardcoded class until
      [T-214](T-214-ds-142s-checker-is-an-allow-list-of-one-class-name.md) lands. Settled **before**
      the figure ships — a deck that fails its own gate is still the worse outcome
      *(restated 2026-08-22; what it replaced asked for a ruling that no longer exists to take)*
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
  in hand. **Answered 2026-08-19, by rejecting the question rather than by choosing a side.** Put to
  the owner, they declined both options and the frame under them: *"please don't limit the animation
  to a specific 'allow list'."* DS-140 becomes a suggested set plus principles, which makes the
  wobble neither a fifth name nor an exemption — it is admissible if it follows the principles. The
  amendment and its blast radius are
  [T-187](T-187-open-the-motion-vocabulary-into-a-style-guide.md); **this task's acceptance criterion
  *DS-140 has a named side* is therefore satisfied elsewhere and must be restated when this is
  planned**, because as written it asks for a ruling that no longer exists to take.
  **Restated 2026-08-22**, and the restatement found what the dissolved question was hiding: see the
  two decisions below.

**Decisions taken 2026-08-22, on the owner's word, so the plan does not re-open them**

- **The rule that actually blocks this figure is DS-142, not DS-140.** The admission test admits a
  looping motion nobody has named; `audit.py` reports any element whose computed
  `animationIterationCount` is `infinite` and which does not carry the class `.current` as ambient,
  and DS-142 is a `hard`/`auto` prohibition. A wobble whose oscillation *is* the depth encoding is
  infinite by construction, so **it fails the published gate today whatever DS-140 says**. That is
  [T-214](T-214-ds-142s-checker-is-an-allow-list-of-one-class-name.md), raised as `PH1` and recorded
  here as this task's `blocked_by` — the one real edge this task has ever had.
- **The wobble is `content` under DS-237, and the chosen static projection is the animation's fill
  state.** `content` because it answers a question about the argument rather than about the hand,
  which is DS-237's own line — nobody is touching the figure. That has a consequence nothing had
  met: **DS-238 lets density stop a content motion, and it does so by multiplying duration by zero
  rather than by removing the name**, so a wobble below its rank freezes at whatever the fill state
  gives — the *frozen mid-wobble frame* the first criterion above forbids. Making the chosen
  projection the fill state settles it **by construction and adds no rule**, which is the same
  reason DS-238 multiplies duration instead of removing the name: for `rise`, removing it would
  strand the element at `opacity:0`.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | ~~The frame-rate instrument~~ **moved to [T-215](T-215-the-frame-rate-instrument-and-a-number-with-its-machine.md) on 2026-08-22**, on this row's own argument: it is independent of the rest and measures what already exists, so nothing about it needs the 3D visual to exist first | — |
| 2 | **Build the 3D figure** to the point where it can be looked at — the visual, its motion, and the chosen static projection | a figure, in a working deck |
| 3 | **Answer DS-140's admission test against that rendering, clause by clause, and check it against DS-142** — which needs [T-214](T-214-ds-142s-checker-is-an-allow-list-of-one-class-name.md) to have landed, or the answer is *the gate rejects it* for a reason that is not about this figure | seven answers recorded in §3, and a green DS-142 |
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
| 2026-08-23 | (no change) | **`parent` cleared to `null`, on the owner's ruling.** taskmd `0.6.0`'s `CLOSED PARENT` check found [T-016](T-016-the-interaction-and-motion-layer.md) `done` with this task open. The owner ruled it is not a child, and this record corroborates it without being asked: the 2026-08-09 row below says this task was *split out of* T-016, which is a spin-off rather than a part of the umbrella. T-016 was already in `related`, and stays `done`. Raised and closed by [T-221](T-221-answer-the-three-defects-taskmd-0-6-0s-wider-check-set-found.md). |
| 2026-08-22 | (no change) | **The DS-140 criterion is restated, the task is split, and the restatement found the rule nobody had asked.** The criterion demanded *a named side* - a ruling the owner dissolved on 2026-08-19 - so the question became which rule now decides whether a 3D wobble is admissible. **DS-140's test admits it and DS-142's checker rejects it, on a class name**: [T-214](T-214-ds-142s-checker-is-an-allow-list-of-one-class-name.md), `PH1`, and this task's first real `blocked_by`. Two decisions taken so the plan need not re-open them - the wobble is `content` under DS-237, and the chosen static projection is the animation's fill state, which closes a **third** path to a stopped motion that neither reduced motion nor print covers. The frame-rate half is [T-215](T-215-the-frame-rate-instrument-and-a-number-with-its-machine.md), split on this task's own plan step 1. **Re-estimated `l` from `xl`**: three deliverables became one. |
| 2026-08-19 | (no change) | **The DS-140 question is settled, and not by either answer this task offered.** Asked to choose between a fifth motion and an exemption, the owner rejected the allow-list itself and ruled that DS-140 becomes a suggested set plus principles, with the rules protecting observable behaviour left `hard`. Raised as [T-187](T-187-open-the-motion-vocabulary-into-a-style-guide.md), because the closure is cited by six rules and one `audit.py` self-test and cannot be edited in one row. **What this changes here**: the ordering constraint the 2026-08-09 row called the part worth carrying over is gone — the ruleset no longer has to take a side before the figure ships — so the 3D visual and the frame-rate figure are now separable from the rule change. `blocked_by` deliberately not set: T-187 is not a gate on building the visual, and the visual is T-187's first consumer rather than its input. |
| 2026-08-10 | (specify) | **Estimated `medium`/`xl`, and moved to `PH3`.** `medium` because all three are wanted and none is a shipping requirement — that is precisely why T-016 split them out rather than holding PH1; `xl` because it is three deliverables and not one: a functional 3D visual with a chosen static projection as its reduced-motion and print fallback, a frame-rate figure with the machine stated beside it, and the DS-140 amendment the first forces. `PH3` under the release split set by the owner 2026-08-10, as the largest new capability on the board. |
| 2026-08-09 | → proposed | **Split out of [T-016](T-016-the-interaction-and-motion-layer.md) so that PH1 ships.** T-016 replanned into eight steps on 2026-08-09 and completed four: the reduced-motion render, the component contract, the gate that holds a deck to it, and the editorial split rule. The remaining four are **capabilities the interaction layer does not reach**, not defects in what it does — the deck has no 3D at all, and no deck here has ever had its frame rate measured. Holding a release for them buys no reader anything, and each is wanted, so they move rather than being dropped. **The order inside the task is the part worth carrying over**: the wobble is a fifth motion or an exemption, DS-140 is a closed vocabulary of four, and shipping the figure before the ruleset has a named side produces a deck that fails its own gate. |
