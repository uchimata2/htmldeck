---
id: T-199
title: The back pager button never plays its press animation
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-112, T-185, T-198]
work_package: PH1
shipped_in: 0.5.0
owner: the project owner
business_value: high
effort: xs
created: 2026-08-20
updated: 2026-08-20
deliverables: []
---

# T-199 - The back pager button never plays its press animation

## 1. Specify

**Outcome**
Pressing the back button pinches, the way pressing the forward button does. Today it does not, and
the owner reported it on 2026-08-20.

**Root cause - CSS specificity, in
[`../shell/components.css`](../shell/components.css) lines 522-524**

    .btn.btn--pager:hover        {transform:rotate(var(--pager-tilt))}          /* 0,3,0 */
    .btn.btn--pager.is-back:hover{transform:rotate(calc(-1 * var(--pager-tilt)))} /* 0,4,0 */
    .btn.btn--pager:active       {transform:scale(var(--pager-pinch))}          /* 0,3,0 */

A press happens while the pointer is hovering, so both rules apply. On **forward**, `:hover` and
`:active` tie at `0,3,0` and `:active` wins on source order - the pinch plays. On **back**, the
`.is-back:hover` rule is `0,4,0` and outranks `:active`, so the transform stays a rotation and the
pinch never renders. The rule that gives the back button its correct leaning direction is the rule
that eats its press.

The fix is to give the back button its own `:active`, or to raise `:active`'s specificity for both.
Whichever is chosen, the two buttons must end up symmetric by construction rather than by luck -
today forward works by source order, which is the same accident one edit away from breaking it too.

**Why nothing caught it.** [T-185](T-185-no-instrument-here-can-watch-an-animation-play.md) - no
instrument here can watch an animation play. A static check sees both declarations present and has
no way to know one never wins. This is the first reported defect of that shape, and it is worth
recording against T-185 as evidence for what that instrument would have been for.

**Scope**
- In: the specificity fix, and symmetry between the two pager buttons asserted rather than observed.
- In: a check, if one is cheap - the cascade is computable from the stylesheet without playing
  anything, so *does every `:active` transform survive the matching `:hover`* may be a static rule.
- Out: the timings. [T-198](T-198-give-affordance-motion-its-own-band-faster-than-content-motion.md)
  carries those, and the two tasks touch the same three lines - whichever lands second rebases.

**Acceptance criteria**
- [ ] Both pager buttons pinch on press, verified by looking at the deck and not by reading the CSS.
- [ ] The symmetry is asserted by something - a fixture, a check, or a single rule serving both.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Reproduce the cascade, not the CSS | a class-swapped cascade probe in Chrome |
| 2 | Name `.is-back` on the press selector so the two buttons are symmetric | `shell/components.css` |
| 3 | Gate it | `ds240_press_beats_hover`, seeded with the defect first |

## 3. Implement

**Decisions & assumptions**
- **The check was written, watched passing, and was wrong** - 2026-08-20. Its first draft matched hover and press rules by base *string*, and reported the seeded T-199 defect as clean: the two rules do not share a base, `.btn.btn--pager.is-back` against `.btn.btn--pager`. Subset, not equality, is the relation - which is the mechanism of the fault itself. Caught only because the defect was seeded back in before the green was believed (**L-04**).
- **And its second draft found nothing either, for a different reason**: the house pattern `([^{}]+)\{([^{}]*)\}` reads the comment above a rule as part of its selector, and this ruleset comments nearly every rule, so `endswith(':active')` matched nothing at all. `_rules()` strips comments first and is the one place that now happens.

**Outputs produced**
- `shell/components.css`
- `tools/deck/audit.py`
- `docs/COMPONENT-CONTRACT.md` - `.btn` and `.btn.btn--pager:active`, which were animating with no contract row

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Both pager buttons pinch on press, verified by looking rather than by reading CSS | **pass** | Chrome, cascade rebuilt with `:hover`/`:active` swapped for classes of equal weight and identical order: `back_press` resolves to `matrix(0.94,0,0,0.94,0,0)` at `0.1s`, where before it stayed at the -3 degree lean |
| The symmetry is asserted by something | **pass** | `ds240_press_beats_hover`, watched failing against the restored defect and passing on all three shipped decks |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-20 | -> proposed | Created. |
| 2026-08-20 | -> in_progress | Root cause is specificity, not a missing rule. |
| 2026-08-20 | -> done | Both criteria met, measured in the browser. |
