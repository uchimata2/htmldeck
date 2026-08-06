---
id: T-016
title: The interaction and motion layer
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: [T-014]
related: [T-002, T-005, T-007, T-017, T-021]
work_package: WP3
owner: maintainer
created: 2026-08-06
updated: 2026-08-07
deliverables: []
---

# T-016 — The interaction and motion layer

## 1. Specify

**Outcome**
The library of interactive and animated components the build mode composes into slides — turning
cards, toggles, tabs, floating information layers, tooltips, plus the motion and 3D vocabulary that
makes the deck feel built rather than assembled. Sparse enough to present live, complete enough to
read alone.

**Why this one**
Progressive disclosure is the owner's signature technique and was absent from `docs/BRIEF.md`
entirely. It is what lets one file serve a live audience and a lone reader instead of compromising
between them. Richness here is wanted, not rationed — the corpus's minimal-JavaScript habit is
history, not a target.

**Scope**
- In: the component set, its markup contract, and the motion vocabulary — transitions, slide
  entrances, 2D animation, 3D effects, depth and parallax where they carry meaning.
- In: an editorial rule for the split — what belongs on the face of the slide versus behind the
  interaction. A deck that hides the wrong half is worse than one that hides nothing.
- In: a motion rest state. Animation that never settles is unreadable on a projector, and the
  presenter is talking over it.
- Out: the portability envelope — which techniques survive `file://` and the target browser is
  T-017's job. This task assumes that answer and builds inside it.
- Out: motion for its own sake. Richness is the licence; noise is still a defect.

**Acceptance criteria**
- [ ] Component set defined with a stable markup contract the generator can emit
- [ ] Motion vocabulary defined as **tokens** — durations, easings, distances, depth — so it swaps
      with the theme (T-007) rather than being hard-coded per component
- [ ] Every technique used is verified working from `file://` in the target browser, glitch-free
- [ ] Frame rate held on a real 12-slide deck with the heaviest slide on screen; number stated,
      and the machine it was measured on stated with it
- [ ] `prefers-reduced-motion` honoured with a genuinely usable fallback, not a dead deck
- [ ] The editorial split rule written, and applied in the demonstration deck
- [ ] Demonstrated on a real 12-slide deck, opened and looked at, in both modes: presented, and
      read cold by someone who was not in the room
- [ ] *Optional mode:* a forced-printable variant exists and reveals disclosure content. Not a
      gate on the design — see T-005

**Open questions**
- Does the deck need an explicit "reveal all" control for the reading case? — owner
- Should disclosure state be shareable via URL fragment, so a recipient can be pointed at an
  opened layer? — owner
- How far into 3D is useful rather than decorative? *(The permission question is settled — the
  owner granted a full exemption on 2026-08-06, so `<canvas>` and WebGL are allowed for diagrams
  too. What remains is the judgement call: WebGL costs theming and diffability, so SVG stays the
  preference where it is equally good.)*

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Catalogue the interaction and motion patterns already in the corpus (from T-009) | pattern list |
| 2 | Design the component set and its markup contract | component spec |
| 3 | Define the motion token set | motion tokens |
| 4 | Write the editorial split rule | disclosure guidance |
| 5 | Build and demonstrate on a 12-slide deck, measuring frame rate | working components |

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
| 2026-08-07 | (no change) | `related` gains [T-021](T-021-the-reflow-view-and-the-resolution-contract.md) — which the row below already said to settle the tier-two question *with*, without the edge ever being written. Added by [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md), which also recorded that a working instance of this layer already exists: [`examples/reference-deck.html`](../examples/reference-deck.html) carries a disclosure component used ten times and a `rise` entrance used fifty-three, on tokenised durations and easings. **What is absent is the contract, not the technique** — no stable markup contract for a generator to emit, no theme-swap demonstration, no frame-rate figure, and no `prefers-reduced-motion` fallback shown to work. |
| 2026-08-06 | → proposed | Created after the owner identified progressive disclosure as their signature technique — absent from the brief. |
| 2026-08-06 | (no change) | Rewritten: print demoted from lead criterion to optional mode, minimal-JavaScript constraint dropped, motion and 3D added as first-class scope, after owner feedback. Retitled from "The progressive-disclosure interaction layer". |
| 2026-08-06 | (no change) | **T-014 closed, and it raises this task's standing.** [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) **§9.3** — progressive disclosure is load-bearing, not a signature flourish: it is the reason the deck can be two things. **§9.5** — Layered Detail is a **modifier on every archetype**, not one archetype among fourteen; R2 and R3 reached this independently. §5.3 gives eleven rules, nine of them `hard`, including the two-tier ceiling, the closed-deck test, the ≥24×24 px target and the independent-axes keyboard model. **§9.2** — motion must encode something; §5.2 keeps the four-motion vocabulary as the mechanism that makes it hold. |
| 2026-08-06 | (no change) | **[T-021](T-021-the-reflow-view-and-the-resolution-contract.md) raises a question this task shares:** the reflow view must carry **all** tier-two content, or it is not a conforming alternate version. Whether it does that by keeping the disclosure affordances or by inlining tier two is open, and §5.3's rules are written for the stage. Settle it with T-021 rather than separately. |
