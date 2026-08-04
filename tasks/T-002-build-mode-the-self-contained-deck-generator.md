---
id: T-002
title: Build mode — the self-contained deck generator
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: [T-001]
related: []
work_package: none
owner: maintainer
created: 2026-08-04
updated: 2026-08-04
deliverables: []
---

# T-002 — Build mode — the self-contained deck generator

## 1. Specify

**Outcome**
Generation of a single-file HTML deck: section-per-slide, inline SVG, keyboard navigation, print stylesheet.

**Why this one**
The core of the plugin. The corpus shows the shape that works: 6–16 slides, 5–22 inline SVGs, minimal JavaScript, CSS custom properties driving the theme.

**Acceptance criteria**
- [ ] Output is one file that renders with the network disabled
- [ ] Tested on a real 12-slide deck with diagrams, not a three-slide toy
- [ ] Prints to PDF without clipping
- [ ] Rendered deck opened and looked at

**Open questions**
- Does the plugin write the words, or only build around words the user supplies?

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
