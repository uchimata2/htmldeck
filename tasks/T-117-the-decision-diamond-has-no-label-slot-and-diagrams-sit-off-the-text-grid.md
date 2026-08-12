---
id: T-117
title: The decision diamond has no label slot, and diagrams sit off the text grid
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-016, T-109, T-115]
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-08-13
updated: 2026-08-13
deliverables:
  - docs/COMPONENT-CONTRACT.md
  - shell/components.css
  - skills/htmldeck/references/build.md
---

# T-117 — The decision diamond has no label slot, and diagrams sit off the text grid

## 1. Specify

**Outcome**
Two diagram components gain what they are missing: a decision diamond that carries its own label, and
a diagram that shares the slide's text grid. Both are gaps in the contract rather than authoring
mistakes, which is why both recur across a deck built carefully against it.

**The two, seen in the render**

**1. The diamond has nowhere to put its label.** Slides 2 and 8 of the first adopting project's deck
both render an **empty rhombus with its caption floating underneath** — `WITHIN BUDGET`,
`WITHIN THE BAND`. The reader has to bind a free-standing caption to a shape by proximity, and on
slide 8 the caption sits below a diamond whose two exits are already labelled `INSIDE` and `OUTSIDE`,
so three pieces of text compete for one node. The deck's own specification says the diamond is
*"sized from its own label so the outline never crosses the text"* — **which is what the author
wanted and the component cannot do**, so the build put the label outside instead. Two slides, one
missing slot.

*This is also [T-115](T-115-the-specification-can-assert-a-layout-the-shell-cannot-honour.md)'s
pattern with a different ending: there the specification asked for something the shell could not do
and the result still read well, so nothing noticed. Here the same thing happened and the result is
weaker. The two tasks are the same gap seen from opposite sides — one adds the check, this one
closes an instance.*

**2. Diagrams are inset from the text grid.** On slides 4, 6 and 7 the diagram's left edge and the
slide's text left edge disagree — by roughly 190, 220 and 60 units respectively — because the diagram
is centred in the body rather than placed on the column grid the header, the fragments and the bottom
line all share. Every one of those slides puts a row of text *directly beneath* the diagram, so the
misalignment is visible as a step rather than as a margin.

**Scope**
- In: a **label slot on the decision node**, sized from the label the way the specification already
  assumed, with the branch labels staying on the edges.
- In: a rule that a diagram **shares the slide's column grid**, and what that means when a diagram is
  genuinely wider or narrower than the text.
- In: contract rows for both in [`COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) — DS-229
  requires every component the style block styles to have one, and these are the components that
  will be edited.
- In: [`build.md`](../skills/htmldeck/references/build.md) updated, so a build stops working around
  the gap by moving the label out.
- In: whatever a gate can decide — a diagram whose left edge does not sit on a grid column is
  measurable; whether a diamond *needs* a label is not.
- Out: **rebuilding the adopting project's deck.** Its diagrams are its own; this changes what the
  next one can do.
- Out: a general diagram layout engine. Two named gaps, closed.

**Inputs**
- [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) — the diagram components as they
  stand, and DS-229's completeness half.
- [`shell/components.css`](../shell/components.css) — the grid the slide's text sits on.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — **DS-136**, patterns built once and reused;
  the grid rules the text already obeys.
- [T-016](T-016-the-interaction-and-motion-layer.md) — where the diagram components came from.

**Acceptance criteria**
- [ ] A decision node renders its label inside itself, sized so the outline never crosses the text,
      with branch labels still on the edges.
- [ ] A diagram's left edge sits on the same column as the slide's text, demonstrated on a slide that
      puts text directly beneath a diagram.
- [ ] Both have contract rows.
- [ ] `build.md` no longer produces the workaround.
- [ ] Demonstrated on a real 12-slide deck with at least two diagrams, opened and looked at, offline.
- [ ] `check.py` green, and the grid clause either gated or excused with a reason.

**Open questions**
- What a diagram wider than the text measure does. Decided during implementation from the grid's own
  reason: the column grid is what makes a slide read as one object, so a wide diagram spans whole
  columns rather than ignoring them.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Measure the inset on the three slides that show it | the numbers |
| 2 | Add the label slot; re-render the two diamond slides | shell, two renderings |
| 3 | Put diagrams on the column grid | shell |
| 4 | Contract rows for both | contract |
| 5 | Fix `build.md`'s workaround | `build.md` |
| 6 | Build a deck with two diagrams and look at it offline | verdict |

## 3. Implement

**Decisions & assumptions**
-

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
| 2026-08-13 | → proposed | Both found by looking at the rendered deck, neither reported. Opened as one task because both are contract gaps in the same layer and both were worked around silently by a careful build — the diamond's label moved outside, the diagram centred instead of placed. A gap a good build routes around is a gap that never gets reported. |
