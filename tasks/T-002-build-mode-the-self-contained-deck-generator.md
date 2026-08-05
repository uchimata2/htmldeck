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
| 2026-08-04 | → proposed | Seeded from `docs/BRIEF.md` when the project folder was prepared. |
| 2026-08-06 | (no change) | Updated for the owner's decisions: writes copy from source material, minimal-JavaScript habit dropped, print demoted to opt-in, `file://` Chrome/Edge render added as a gate. |
