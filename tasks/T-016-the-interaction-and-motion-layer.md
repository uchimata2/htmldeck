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
- [ ] **A functional 3D visual demonstrated** — one that encodes something a 2D rendering would
      lose — with a **chosen static projection** as its reduced-motion and print fallback, not a
      frozen mid-wobble frame, and with DS-218's stop control reaching it
- [ ] The editorial split rule written, and applied in the demonstration deck
- [ ] Demonstrated on a real 12-slide deck, opened and looked at, in both modes: presented, and
      read cold by someone who was not in the room
- [ ] *Optional mode:* a forced-printable variant exists and reveals disclosure content. Not a
      gate on the design — see T-005

**Open questions**
- ~~Does the deck need an explicit "reveal all" control for the reading case? — owner~~ **Answered
  2026-08-07 by the owner: no. The reading view *is* reveal-all.** DS-073 already inlines tier two
  there with the control not rendered, so the reading case has an entire rendering rather than a
  button. A second global control would be a third encoding of one fact — the DS-216 failure
  [T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) paid to remove, and it
  would land on the chrome budget the same task cut from 96 design units to 52.
- ~~Should disclosure state be shareable via URL fragment, so a recipient can be pointed at an
  opened layer? — owner~~ **Answered 2026-08-07 by the owner: slide index and view only.** The
  fragment carries which slide and which rendering — restored on load, and **not written per
  toggle**, because a history entry per panel makes the browser Back button stop meaning "the
  previous slide". Per-panel state is deliberately not encoded: *"point me at that content"* is
  already answered by the reading view, which shows all of it. Encoding open panels is a state
  serializer this task does not owe until someone asks for it.
- ~~How far into 3D is useful rather than decorative?~~ **Answered 2026-08-07 by the owner: 3D is
  wanted for functional visualisation, not only for emphasis.** Three cases named: **a 3D diagram
  under a slight continuous wobble, so that peaks read as peaks**; **a 3D mesh shown as itself**;
  and **decorative 3D for emphasis**, which stays permitted. So the component set carries a **3D
  visual class** — this is not the narrow "a third axis or nothing" reading, and the preference for
  SVG where it is equally good (DS-111) is unchanged, because these are cases where it is not.
  *(The permission question was already settled — the owner granted a full exemption on 2026-08-06,
  so `<canvas>` and WebGL are allowed for diagrams too.)*

  **The wobble is the load-bearing part of the answer and it collides with two rules in this
  task's own scope.** It is *continuous* motion, and the scope line above requires a motion rest
  state; **DS-140** is a closed vocabulary of exactly four motions, `hard` and `auto`-checked, and a
  wobble is a fifth. The resolution this task should argue rather than assume: the oscillation
  **is** the depth encoding — a static projection of a 3D surface is ambiguous and the movement is
  what disambiguates it — so it is the one class of never-settling motion that satisfies §9.2's
  *motion must encode something*. That makes it a **ruleset change to raise, not a licence to take
  quietly**: DS-140 gains a fifth motion or an exemption clause, on the T-033 precedent that a rule
  contradicted by a shipped deck is a defect in the ruleset.

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
| 2026-08-07 | (no change) | **The 3D question is answered and §1 now has none open: 3D is wanted for functional visualisation, not only for emphasis.** A wobbling 3D diagram whose motion resolves depth, a mesh shown as itself, decorative emphasis kept. One acceptance criterion added for it. **Three consequences this task inherits, none of them optional.** (1) **A ruleset change to raise**: DS-140 is a closed vocabulary of exactly four motions, `hard` and `auto`-checked, and a continuous wobble is a fifth — it needs a rule or an exemption clause, on [T-033](T-033-reconcile-ds-131-with-the-chrome-budget.md)'s precedent that a rule a shipped deck contradicts is a ruleset defect rather than a deck defect. (2) **The fallback is a chosen projection, not a frozen frame** — a paused wobble is the ambiguous static rendering the motion existed to fix, and it is what `prefers-reduced-motion`, the reading view and print all get ([R7](../docs/research/R7-printable-mode.md) §5.2 already records that print loses 3D). (3) **A second never-quiescent animation now exists**, so **DS-221**'s pin-motion-off-before-capture applies to it too, and [T-005](T-005-build-check-the-gate-the-deck-must-pass.md)'s render gate has one more thing to hold still before it measures. Also reaches [T-007](T-007-define-the-parametric-theme-layer.md), whose tokens cannot reach inside a WebGL scene unless the scene is plumbed to read them, and [T-019](T-019-build-the-capability-preflight-the-deck-ships-wit.md), which now has a real capability to preflight and a degraded state to design. |
| 2026-08-07 | (no change) | **Two of the three open questions answered by the owner, and both answers remove work rather than adding it.** *No reveal-all control* — the reading view is it, so the stage keeps the chrome budget [T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) cut. *The fragment carries slide and view only* — restored on load, never written per toggle, which keeps Back meaning "the previous slide"; per-panel state is not encoded until someone asks. **The 3D question is now the only one left in this task, and it is the one that decides its size** — it is also the only open question in the backlog that can still change what [T-002](T-002-build-mode-the-self-contained-deck-generator.md) has to emit and what [T-019](T-019-build-the-capability-preflight-the-deck-ships-wit.md) has to preflight, so it wants answering before either is planned rather than when this task is worked. |
| 2026-08-07 | (no change) | **The tier-two question this task shared with [T-021](T-021-the-reflow-view-and-the-resolution-contract.md) is settled, and it removes work from here.** The owner ruled that the reflow view **inlines** tier two — panels open in normal flow, the disclosure control not rendered — and **DS-073** now states it. So the disclosure component has **one context, not two**: it is designed for the stage, and the reading view is a document rendering that does not operate it. §5.3's rules stay written for the stage. [R7 §5](../docs/research/R7-printable-mode.md) had already decided the same question the same way for print, so all three renderings now agree. |
| 2026-08-07 | (no change) | `related` gains [T-021](T-021-the-reflow-view-and-the-resolution-contract.md) — which the row below already said to settle the tier-two question *with*, without the edge ever being written. Added by [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md), which also recorded that a working instance of this layer already exists: [`examples/reference-deck.html`](../examples/reference-deck.html) carries a disclosure component used ten times and a `rise` entrance used fifty-three, on tokenised durations and easings. **What is absent is the contract, not the technique** — no stable markup contract for a generator to emit, no theme-swap demonstration, no frame-rate figure, and no `prefers-reduced-motion` fallback shown to work. |
| 2026-08-06 | → proposed | Created after the owner identified progressive disclosure as their signature technique — absent from the brief. |
| 2026-08-06 | (no change) | Rewritten: print demoted from lead criterion to optional mode, minimal-JavaScript constraint dropped, motion and 3D added as first-class scope, after owner feedback. Retitled from "The progressive-disclosure interaction layer". |
| 2026-08-06 | (no change) | **T-014 closed, and it raises this task's standing.** [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) **§9.3** — progressive disclosure is load-bearing, not a signature flourish: it is the reason the deck can be two things. **§9.5** — Layered Detail is a **modifier on every archetype**, not one archetype among fourteen; R2 and R3 reached this independently. §5.3 gives eleven rules, nine of them `hard`, including the two-tier ceiling, the closed-deck test, the ≥24×24 px target and the independent-axes keyboard model. **§9.2** — motion must encode something; §5.2 keeps the four-motion vocabulary as the mechanism that makes it hold. |
| 2026-08-06 | (no change) | **[T-021](T-021-the-reflow-view-and-the-resolution-contract.md) raises a question this task shares:** the reflow view must carry **all** tier-two content, or it is not a conforming alternate version. Whether it does that by keeping the disclosure affordances or by inlining tier two is open, and §5.3's rules are written for the stage. Settle it with T-021 rather than separately. |
