---
id: T-002
title: Build mode — the self-contained deck generator
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: [T-001, T-014, T-015]
related: []
work_package: WP3
owner: maintainer
created: 2026-08-04
updated: 2026-08-06
deliverables: []
---

# T-002 — Build mode — the self-contained deck generator

## 1. Specify

**Outcome**
Generation of a single-file HTML deck: section-per-slide, diagrams, navigation, and the interaction
and motion layer composed in.

**Why this one**
The core of the plugin. The corpus shows the shape that works: 6–16 slides, 5–22 diagrams, CSS
custom properties driving the theme. *Its minimal-JavaScript habit is not carried forward* —
richness is wanted within the portability envelope T-017 defines.

**Acceptance criteria**
- [ ] **Writes the slide copy from source material**, not just the design around supplied words —
      decided 2026-08-06, and the harder of the two paths
- [ ] Output is one file that renders with the network disabled
- [ ] Renders glitch-free **from `file://` in recent Chrome/Edge**, with no console errors
- [ ] Every theme value comes from the token layer (T-007); none hard-coded here
- [ ] Composes the interaction and motion components (T-016) rather than emitting bespoke markup
- [ ] Tested on a real 12-slide deck with diagrams, not a three-slide toy
- [ ] Rendered deck opened and looked at
- [ ] *Opt-in:* a printable variant can be forced. Not a gate

**Open questions**
- ~~Does the plugin write the words?~~ **Answered 2026-08-06: yes**, from source material.
- How much of the narrative decision is the generator's versus the brief's? — resolve with T-015

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
| 2026-08-06 | (no change) | **The generator now has a reference output to be judged against**: [`examples/reference-deck.html`](../examples/reference-deck.html), 12 slides, 178 KB, zero external references, built by hand to the ruleset by [T-024](T-024-build-the-reference-deck-and-validate-the-ruleset.md). That closes the objection in T-024's scope — a generator with no reference output is a generator nobody can review. **What it should automate is now visible rather than assumed**, and so is what it must not: five of the ten evaluation dimensions cannot be checked mechanically, so the build mode cannot self-certify. |
| 2026-08-04 | → proposed | Seeded from `docs/BRIEF.md` when the project folder was prepared. |
| 2026-08-06 | (no change) | Updated for the owner's decisions: writes copy from source material, minimal-JavaScript habit dropped, print demoted to opt-in, `file://` Chrome/Edge render added as a gate. |
| 2026-08-06 | (no change) | **T-014 closed — [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) is now the ruleset this mode builds against.** Two things grow scope, both by pointer: **§9.4** — the heading check is semantic, so build mode must write headings that are *claims*, not labels; and **§9.5** — Layered Detail is a modifier, not a slide type, so the build decides a tier-one/tier-two split for **every** slide rather than selecting a disclosure archetype. **§9.1 is a blocker in practice**: the fixed-stage question needs an owner decision before the stage is built. §3.2 replaces L3's nine archetypes with thirteen plus one modifier. |
| 2026-08-06 | (no change) | **§9.1 is no longer a blocker — the owner settled it: keep the fixed stage, add a reflow view ([T-021](T-021-the-reflow-view-and-the-resolution-contract.md)).** But the stage this mode builds is now specified much more tightly, in [`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §2.4: a **1920×1080 design space, uniformly scaled**, with **exactly one layout — no media queries, no breakpoints, no `max-width` containers, no `vw`/`vh` type inside the stage**. Type is in design units with a hard floor: **nothing under 18, body 24–28**. The reason is measured, not stylistic: under a uniform scale the presenter's viewport cancels out of the screen-share legibility equation, so a responsive presentation layout is illegible over a video call in a way the stage is not. |
| 2026-08-06 | (no change) | **Build mode now has a stated definition of done.** [`docs/EVALUATION.md`](../docs/EVALUATION.md) §5: zero `hard` violations, every slide ≥ 18/24 with no dimension below 2, deck ≥ 12/16 with no dimension below 2. Before this the loop terminated when the agent felt finished. Two things bind the generator directly: the **per-dimension floor** means a slide cannot be shipped on craft while its claim is absent, and **S4 Density's anchor** makes the tier split a build-time decision on every slide rather than a flourish. The design system is also restructured — rules are cited as `DS-nnn` now, and the rationale moved to [`DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md). |
