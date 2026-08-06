---
id: T-007
title: Define the parametric theme layer
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: [T-001, T-014]
related: [T-002, T-016, T-021]
work_package: WP2
owner: maintainer
created: 2026-08-04
updated: 2026-08-07
deliverables: []
---

# T-007 — Define the parametric theme layer

## 1. Specify

**Outcome**
A decision on how visual identity is chosen per deck.

**Why this one**
The corpus decks look designed **because they do not share a template**. A plugin shipping one house style will produce decks that look like each other — which is the problem it exists to solve.

**Decided 2026-08-06 — one theme, built parametrically.** The owner chose **exactly one** robust,
fully-resolved look across every layer, not several and not per-topic generation. Variety is a
later problem, solved by a tool that generates *new* templates — a surveying step plus a script
that lays out the structure, writes the specs and generates content. That tool is **not** in scope
now. What is in scope now is making it cheap to add: every layer parametric from the start.

This overrides `docs/BRIEF.md` open question 3, and stands in tension with the brief's rule 3
("decks must not look like each other"). That rule is satisfied later, by the generator.

**What is left of this task**
Not a decision any more — the parametric theme layer that the decision requires.

**Acceptance criteria**
- [ ] One complete look defined across all thirteen coverage areas, with no unresolved choices
- [ ] Every value that could differ between themes is a **token**, not a hard-coded value —
      colour, type scale, spacing, radii, stroke weights, diagram styling, interaction styling
- [ ] The token set is documented as the contract a future generated theme must satisfy
- [ ] Swapping the token file alone produces a visibly different, still-coherent deck —
      demonstrated, not asserted
- [ ] No theme-specific value reachable anywhere outside the token layer

**Open questions**
- What is the minimum token set that makes a future theme genuinely distinct rather than a
  recolour? Recolouring is not the goal — the corpus decks differ structurally too.

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
| 2026-08-07 | (no change) | `related` gains T-016 and T-021 — the motion tokens that swap with this layer, and the second of the two renderings it must carry. [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md) also recorded a measurement that changes what *starting* this task means: **[`examples/reference-deck.html`](../examples/reference-deck.html) already carries 57 custom properties**, spanning colour, type scale, spacing, radii, stroke, shadow, motion durations and easings, `--measure`, `--du` and a tokenised disclosure mark. The token *layer* exists, as one hand-built instance. The **contract** does not, and neither does the swap demonstration the criteria above ask for. This task extracts and proves; it does not author from nothing. |
| 2026-08-04 | → proposed | Seeded from `docs/BRIEF.md` when the project folder was prepared. |
| 2026-08-06 | (no change) | Owner decided: one theme now, every layer parametric, template generator deferred. Task reframed from a decision to the token layer that decision requires. |
| 2026-08-06 | (no change) | **T-014 closed.** [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §1.2 fixes the token layer this task builds: parametricity is **hard**, not tidy practice, because a value hard-coded now is a value the generator cannot vary. Token vocabulary extended beyond the corpus's `--ink`/`--bg`/`--line`/`--shadow` with `--measure` and a tokenised disclosure mark. **C7 (one palette per deck) was dropped and D1's per-deck font rotation with it** — this task's variety comes from the generator, never from per-deck improvisation. **§9.1 gates it**: the stage question is an owner decision. |
| 2026-08-06 | (no change) | **Ungated — the owner settled §9.1: fixed stage plus a reflow view ([T-021](T-021-the-reflow-view-and-the-resolution-contract.md)).** Two consequences for the token layer: type tokens are **design units on a 1920×1080 stage**, not `px` and not `clamp()`/`vw` (those belong to the reflow view and fight the transform inside the stage); and the token set must carry **two renderings**, the stage and the reflow document, from one source of values. |
