---
id: T-016
title: The interaction and motion layer
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: [T-014]
related: [T-002, T-005, T-007, T-017]
work_package: WP3
owner: maintainer
created: 2026-08-06
updated: 2026-08-06
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
| 2026-08-06 | → proposed | Created after the owner identified progressive disclosure as their signature technique — absent from the brief. |
| 2026-08-06 | (no change) | Rewritten: print demoted from lead criterion to optional mode, minimal-JavaScript constraint dropped, motion and 3D added as first-class scope, after owner feedback. Retitled from "The progressive-disclosure interaction layer". |
