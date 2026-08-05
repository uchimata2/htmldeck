---
id: T-013
title: Research offline-safe assets — icons, illustration, fonts, diagram tooling
type: research
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-001, T-006, T-014]
work_package: WP1
owner: maintainer
created: 2026-08-06
updated: 2026-08-06
deliverables: [docs/research/R5-assets-and-licences.md]
---

# T-013 — Research offline-safe assets — icons, illustration, fonts, diagram tooling

## 1. Specify

**Outcome**
A shortlist of icon sets, illustration approaches, typefaces and diagram-authoring routes that can
be embedded in a single HTML file, redistributed from a public repository, and rendered with the
network disabled — each with its licence recorded.

**Why this one**
Self-containment is the first requirement and every deck in the corpus fails it, mostly on web
fonts. Icons and illustration are the other two things a deck reaches for that quietly become
network references. Getting the licence-clean shortlist settled early unblocks the font decision
(T-001), the chart decision (T-006) and the whole build mode.

**Scope**
- In: icon sets with permissive licences and SVG sources small enough to inline; the subset the
  plugin ships versus fetches at author time.
- In: illustration strategy — geometric/abstract SVG, generated motifs, or none — and how to keep
  it from looking like clip art.
- In: typefaces whose licence permits redistribution, subsetting technique, and the size cost of
  embedding measured on a real 12-slide deck.
- In: diagram authoring — hand-written SVG, generated SVG, Mermaid pre-rendered to SVG at build
  time — and which survives the offline rule.
- In: **animation and 3D libraries as vendorable assets** — licence, minified size, and whether
  they initialise from `file://` at all. Added 2026-08-06 when the minimal-JavaScript constraint
  was dropped; the envelope comes from T-017.
- Out: raster images in any form; the brief already bans them.

**Acceptance criteria**
- [ ] Every candidate carries its licence, verified from the source, and a redistribution verdict
- [ ] Embedding cost measured, not estimated: bytes added to a real 12-slide deck
- [ ] A recommended default set, with the fallback if the default proves too heavy
- [ ] Offline rendering verified with the network actually disabled

**Open questions**
- Is a file-size ceiling per deck acceptable, and what is it? Embedded fonts and icons trade
  directly against it. — owner

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Shortlist icon sets and verify licences | icon table |
| 2 | Shortlist typefaces and verify licences | font table |
| 3 | Measure subsetting and embedding cost | size measurements |
| 4 | Assess illustration and diagram routes | approach notes |
| 5 | Write up with a recommended default | `docs/research/R5-assets-and-licences.md` |

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
| 2026-08-06 | → proposed | Created to cover the icon, illustration and font coverage areas. |
