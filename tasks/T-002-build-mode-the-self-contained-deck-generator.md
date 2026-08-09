---
id: T-002
title: Build mode — the self-contained deck generator
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: [T-001, T-007, T-014, T-015, T-016, T-020]
related: [T-021, T-028]
work_package: v0.1
owner: maintainer
created: 2026-08-04
updated: 2026-08-09
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
- [ ] **Departs from the specification when compliance requires it** rather than building a
      non-conformant slide or looping on one — the deviation is this mode's call, not a question
      returned to the user
- [ ] Every deviation is written back into the specification file it contradicts, so the artifacts
      record what was built
- [ ] Deviations reach the user at delivery as **brief bullet points**
- [ ] Tested on a real 12-slide deck with diagrams, not a three-slide toy
- [ ] Rendered deck opened and looked at
- [ ] *Opt-in:* a printable variant can be forced. Not a gate

**Open questions**
- ~~Does the plugin write the words?~~ **Answered 2026-08-06: yes**, from source material.
- ~~How much of the narrative decision is the generator's versus the brief's?~~ **Answered
  2026-08-07 by the owner: the specification decides the narrative, and the generator may depart
  from it where compliance requires — every departure recorded, and reported briefly.**
  [T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md) already put the spine, the
  outline and the bottom lines upstream and that stands: this mode invents no narrative. What the
  ruling did not cover is the case the owner named — **a specification can turn out unbuildable.**
  A slide that will not fit the stage, or that a `hard` rule fails on, cannot be built as written,
  and a generator with no authority to change it either ships a non-conformant slide or loops on
  it. So the generator holds **implementation authority above the detailed spec**: it resolves the
  layout or the rule conflict itself rather than returning a decision to a user who cannot picture
  the outcome. Two obligations come with the authority — **every deviation is written back into the
  artifacts it contradicts**, the slide-by-slide spec and, where the outline moved, the foundation
  spec, so those files record what was *built* rather than what was intended; and **the user is
  told at delivery, in brief bullet points**, not a rationale per item.

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
| 2026-08-09 | (no change) | **The last blocker closed, and this task is now the only thing between the repository and a v0.1 that ships.** All six of `blocked_by` are `done`. What [T-016](T-016-the-interaction-and-motion-layer.md) hands over is the answer to *what does the generator emit*, in three documents rather than one: [`COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) — 59 authored parts, their element, place, count and attributes, and the eleven rules that must read a motion token — is what the criterion *composes the components rather than emitting bespoke markup* now means, and `component.py check` decides it; [`THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) is the other criterion's, and `theme.py check` fails a length, duration or easing curve written outside the region. **The third is new and is the one that changes what this mode has to decide: DS-230.** §5.3 gave build mode eleven mechanical rules about disclosure and no editorial test, so a generator satisfying every one of them could still put an appendix behind the click. Tier two is now one of four kinds — `derivation` · `scope` · `condition` · `instances` — the list is closed, and **every `.disc` declares which in `data-disc`**, so the split is a decision this mode makes explicitly rather than by accident. **DS-231** is the mechanical half: a bottom line citing a figure that lives only behind the click fails the gate. |
| 2026-08-07 | (no change) | **The last open question is answered, and the answer gives this mode an authority it did not have: it may depart from the specification to keep the deck compliant.** Three acceptance criteria added for it. The owner's reason is the failure mode a strict-obedience generator has no exit from — a slide that will not fit the stage or that a `hard` rule fails on cannot be built as specified, so obedience means shipping a non-conformant slide or looping. **The loop already has language for the two cases this does *not* cover:** [`EVALUATION.md`](../docs/EVALUATION.md) §6.1's **STALL** (a design decision wearing a finding's clothes — escalate) and **OSCILLATION** (two rules in tension — stop and name them, and record it in [`DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) §2). Deviation authority is for what the generator *can* resolve; those two outcomes remain the exits for what it cannot, and this ruling does not weaken them. **Where the deviations are written is already fixed** by [`artifacts.md`](../skills/htmldeck/references/artifacts.md): `<slug>.slides.md` and, when the outline moved, `<slug>.foundation.md` — both of which exist to be *"what a reader opens when the deck turns out wrong"*, which they are not if they record only the intent. The user-facing half is bullet points at delivery, and it is the first thing this mode must report that is not the deck. |
| 2026-08-07 | (no change) | **[T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md) settled this mode's input contract, and it is not a brief.** Build mode consumes a **reviewed slide-by-slide specification** — seven fields per slide, structure · text · visuals · animations · interactive elements · title · bottom line — produced upstream from the two answers, the sources and the foundation spec. Two consequences beyond the input type: **the build is batched by default**, a few slides at a time, each batch running the auto gate, the render gate and S3/S5/S6 before the next is written, because DS-136 reuse means a component defect found in batch one is fixed once rather than twelve times; and **the bottom line arrives specified rather than invented at layout time**, which is the contract [T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) exists because no deck met. T-020 §3.2, §3.4, §3.6. |
| 2026-08-07 | (no change) | **Three blockers added by [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md).** [T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md) because it decides this mode's **input contract** — a brief or a specification — and a generator specified against the wrong one is respecified rather than adjusted; T-020's own open question proposed exactly this edge and left it `related` only to avoid a deadlock that does not exist, since T-020 has no blockers of its own. [T-007](T-007-define-the-parametric-theme-layer.md) and [T-016](T-016-the-interaction-and-motion-layer.md) because two acceptance criteria above already require every theme value to come from the token layer and every component to be composed rather than emitted bespoke: with neither contract in existence, the only thing this mode can do is hard-code, which [`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §1.2 calls `hard`. `related` gains T-021, the other half of the two renderings, and T-028, the reference output this mode is judged against. |
| 2026-08-06 | (no change) | **The generator now has a reference output to be judged against**: [`examples/reference-deck.html`](../examples/reference-deck.html), 12 slides, 178 KB, zero external references, built by hand to the ruleset by [T-024](T-024-build-the-reference-deck-and-validate-the-ruleset.md). That closes the objection in T-024's scope — a generator with no reference output is a generator nobody can review. **What it should automate is now visible rather than assumed**, and so is what it must not: five of the ten evaluation dimensions cannot be checked mechanically, so the build mode cannot self-certify. |
| 2026-08-04 | → proposed | Seeded from `docs/BRIEF.md` when the project folder was prepared. |
| 2026-08-06 | (no change) | Updated for the owner's decisions: writes copy from source material, minimal-JavaScript habit dropped, print demoted to opt-in, `file://` Chrome/Edge render added as a gate. |
| 2026-08-06 | (no change) | **T-014 closed — [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) is now the ruleset this mode builds against.** Two things grow scope, both by pointer: **§9.4** — the heading check is semantic, so build mode must write headings that are *claims*, not labels; and **§9.5** — Layered Detail is a modifier, not a slide type, so the build decides a tier-one/tier-two split for **every** slide rather than selecting a disclosure archetype. **§9.1 is a blocker in practice**: the fixed-stage question needs an owner decision before the stage is built. §3.2 replaces L3's nine archetypes with thirteen plus one modifier. |
| 2026-08-06 | (no change) | **§9.1 is no longer a blocker — the owner settled it: keep the fixed stage, add a reflow view ([T-021](T-021-the-reflow-view-and-the-resolution-contract.md)).** But the stage this mode builds is now specified much more tightly, in [`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §2.4: a **1920×1080 design space, uniformly scaled**, with **exactly one layout — no media queries, no breakpoints, no `max-width` containers, no `vw`/`vh` type inside the stage**. Type is in design units with a hard floor: **nothing under 18, body 24–28**. The reason is measured, not stylistic: under a uniform scale the presenter's viewport cancels out of the screen-share legibility equation, so a responsive presentation layout is illegible over a video call in a way the stage is not. |
| 2026-08-06 | (no change) | **Build mode now has a stated definition of done.** [`docs/EVALUATION.md`](../docs/EVALUATION.md) §5: zero `hard` violations, every slide ≥ 18/24 with no dimension below 2, deck ≥ 12/16 with no dimension below 2. Before this the loop terminated when the agent felt finished. Two things bind the generator directly: the **per-dimension floor** means a slide cannot be shipped on craft while its claim is absent, and **S4 Density's anchor** makes the tier split a build-time decision on every slide rather than a flourish. The design system is also restructured — rules are cited as `DS-nnn` now, and the rationale moved to [`DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md). |
