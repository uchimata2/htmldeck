---
id: T-111
title: A named slide transition, chosen per deck, with slide and immediate as the shipping pair
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-016, T-041, T-057, T-112]
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-08-12
updated: 2026-08-12
deliverables:
  - shell/deck.js
  - shell/components.css
  - docs/DESIGN-SYSTEM.md
  - docs/THEME-CONTRACT.md
---

# T-111 — A named slide transition, chosen per deck, with slide and immediate as the shipping pair

## 1. Specify

**Outcome**
Moving between slides is a chosen effect rather than whatever the stylesheet happens to do. A deck
names its transition; two are available, both conformant; the duration is a token.

**The two**

**`slide`.** The outgoing slide shrinks slightly, gains a soft drop shadow, and eases out to the left
when advancing or to the right when going back. **The incoming slide does not animate** — it is
revealed, as though it had been there all along. That asymmetry is the design, not a simplification
of it: two slides moving at once is the mush that makes presentation-software transitions read as
cheap, and animating one halves the cost on a dense slide.

**`immediate`.** No transition. Named, so that choosing nothing is a decision a deck records rather
than a default nobody examined.

**Default duration 500 ms**, a theme token. That lands exactly on **DS-141**'s cap, and DS-141
already reserves 400–500 ms for an inter-slide transition — this task builds the thing the rule was
written for.

**What is deliberately not here**
The owner ruled on 2026-08-12: **no book-page curl and no explosion.** Both are to be brainstormed
separately and neither is in scope. For the record of why the question arises at all: **DS-144**
forbids 3D slide transitions and flashy cuts, so the curl needs an amendment; the explosion needs
that *and* a **DS-150** answer to *what does this encode?*, which it does not have, *and* it is
per-element transforms across a dense slide at a frame rate this project has never measured on any
machine ([T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md)). Recorded so
the brainstorm starts from the constraints rather than rediscovering them.

**Scope**
- In: `slide` and `immediate`, named in [`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) as a closed
  vocabulary, extensible only by amendment.
- In: direction taken from the navigation direction, including the ruler's jumps — a jump backwards
  by six slides is still backwards.
- In: duration and easing as theme tokens.
- In: **`prefers-reduced-motion` collapses any transition to `immediate`** (DS-143), and the deck
  still navigates.
- In: transitions pinned off for print and for headless capture — DS-224 and DS-221 both already
  require this of motion, and a transition is the case they were written before.
- In: what happens when a reader advances mid-transition. A queued or interrupted transition that
  leaves two slides visible is a glitch, and [T-041](T-041-implement-the-nine-glitch-free-conditions.md)
  owns the general form of that.
- Out: **the book curl and the explosion.** Owner's decision, 2026-08-12.
- Out: **motion density** — [T-112](T-112-motion-density-and-the-split-between-content-and-affordance-motion.md).
  A transition is navigation, not content motion, and density does not select it.
- Out: a per-slide transition override. One deck, one transition.

**Inputs**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §5.2 — **DS-140** (the closed four-motion
  vocabulary, which a transition sits outside), **DS-141** (the 400–500 ms reservation), **DS-143**,
  **DS-144**, **DS-221**, **DS-224**.
- [`shell/deck.js`](../shell/deck.js) — `go()`, and the ruler's jump path.
- [T-016](T-016-the-interaction-and-motion-layer.md) — the motion layer this extends.

**Acceptance criteria**
- [ ] Both transitions are named in the ruleset and selectable per deck.
- [ ] `slide` animates only the outgoing slide, and the direction follows navigation direction in all
      three navigation paths — keys, pager, ruler jump.
- [ ] Duration and easing are theme tokens; the default is 500 ms.
- [ ] With `prefers-reduced-motion`, both behave as `immediate`.
- [ ] A printed deck and a headless capture show no transition state.
- [ ] Advancing twice inside one transition leaves exactly one slide visible.
- [ ] Demonstrated on a real 12-slide deck with diagrams, opened and looked at, offline.
- [ ] `python tools/deck/check.py` green; `render.py` green.

**Open questions**
- None. The two-transition scope is the owner's decision of 2026-08-12.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Write the vocabulary and the tokens into the ruleset and theme contract | rows |
| 2 | Build `slide`, outgoing-only, direction-aware | `deck.js`, `components.css` |
| 3 | Wire reduced-motion, print and capture to `immediate` | three paths |
| 4 | Interrupt it — advance mid-transition, jump mid-transition | glitch verdict |
| 5 | Run it on a real 12-slide deck and look at it offline | verdict |

## 3. Implement

**Decisions & assumptions**
- 2026-08-12 — owner: build `slide` and `immediate` only. Book curl and explosion deferred to a
  separate brainstorm, not declined outright.

**Outputs produced**
-

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :--- | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-12 | → proposed | Created from the first adopting project's feedback on published `0.2.2`. Four transitions were requested; the owner cut it to two the same day and deferred the other two to a brainstorm. The DS-144 and DS-150 collisions are recorded in §1 so the brainstorm starts from them. |
