---
id: T-010
title: Research external deck-design and presentation UX principles
type: research
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-014]
work_package: WP1
owner: maintainer
created: 2026-08-06
updated: 2026-08-06
deliverables: [docs/research/R2-external-principles.md]
---

# T-010 — Research external deck-design and presentation UX principles

## 1. Specify

**Outcome**
A digest of established, citable principles for presentation design and on-screen reading, filtered
to the ones that change a decision in this plugin — and explicitly listing the ones that do not, so
they are not re-litigated later.

**Why this one**
The corpus shows what the owner does; it cannot say whether it is right. External principle gives
the conventions a defensible basis, and supplies vocabulary and structure the plugin can point at
instead of paraphrasing.

**Scope**
- In: narrative and structure (pyramid principle, SCR, assertion-evidence), cognitive load and
  signalling, typographic scale and measure for projected and on-screen reading, colour theory and
  contrast, data-visualisation practice, accessibility (WCAG AA as the floor), and presentation-UX
  specifics — navigation affordances, progress indication, keyboard and touch control, and how a
  deck behaves when it is *read* rather than presented.
- Out: PowerPoint-specific and Markdown-slide-framework guidance except where it transfers.
- Out: anything that cannot be tied to a rule the plugin would enforce.

**Acceptance criteria**
- [ ] Each principle recorded with source, and a one-line statement of what it changes here
- [ ] Conflicts between sources named rather than averaged away
- [ ] A "considered and rejected" list with reasons
- [ ] Accessibility floor stated concretely (contrast ratios, minimum sizes, focus behaviour)
- [ ] Cross-checked against the already-installed `artifact-design`, `dataviz` and
      `artifact-diagramming` skills — where they already own a rule, point at them (T-012 covers
      the reuse decision)

**Answered 2026-08-06 — presented live, with the detail hidden behind interaction.** The deck is
primarily presented, but supporting detail sits behind turning cards, toggles, tabs, floating
layers and tooltips so a recipient can consume it alone. That resolves the density conflict
by splitting the two audiences across an interaction layer rather than compromising between them,
and it makes **progressive disclosure a first-class research area for this task**: signalling
that something is hidden, disclosure affordances, and the cost of interaction during a live talk.
Build implications are T-016.

**Open questions**
- What does the research say about disclosure a *presenter* has to operate live? An affordance
  that reads well to a lone reader can be a liability on stage.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Gather sources by area | source list |
| 2 | Extract only decision-changing rules | rule table |
| 3 | Write up with conflicts and rejections | `docs/research/R2-external-principles.md` |

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
| 2026-08-06 | → proposed | Created from the owner's direction to research external principles. |
