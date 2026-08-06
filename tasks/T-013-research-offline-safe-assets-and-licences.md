---
id: T-013
title: Research offline-safe assets — icons, illustration, fonts, diagram tooling
type: research
status: done
phase: review
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
- [x] Every candidate carries its licence, verified from the source, and a redistribution verdict
- [x] Embedding cost measured, not estimated: bytes added to a real 12-slide deck
- [x] A recommended default set, with the fallback if the default proves too heavy
- [x] Offline rendering verified with the network actually disabled

**Open questions**
- ~~Is a file-size ceiling per deck acceptable, and what is it? Embedded fonts and icons trade
  directly against it.~~ — **answered 2026-08-06, and the answer widened the task.** No fixed
  ceiling: report the cost instead, and expose delivery as a **configuration parameter** the deck
  author sets. The owner's stated default is CDN references, with embedding or local-file
  references available on request.

  **This contradicted CLAUDE.md rule 1 and R4's J1 finding**, so it was carried as a candidate
  change of direction rather than adopted silently — see §4 of `R5-assets-and-licences.md`. The
  owner asked for a measured recommendation on which way the default should fall; that
  recommendation became an output of this task, and **the owner accepted it the same day**.
  Delivery is now settled the other way: embed by default, `linked` for authoring only.

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
- **Run this task and T-012 steps 4–6 as one survey** — 2026-08-06. They ask the same
  licence-and-size question of different assets; splitting them means reading the same licence
  pages twice.
- **Measure at the latin-subset woff2, not the full family** — 2026-08-06. That is the file a
  browser actually downloads, so it is the honest embedding cost. It also avoids a font-tooling
  dependency, which L-07 forbids in project tooling.
- **No deck-specific subsetting** — 2026-08-06. It would need `fonttools`. At 97 KB for a
  three-face identity there is no incentive, so the dependency is not worth taking. Recorded as
  not-measured in R5 §7 rather than quietly skipped.
- **Icons inline as `<svg>`, never as a `data:` URI** — 2026-08-06. No base64 surcharge, and the
  glyph inherits `currentColor` so it themes with the deck. Verified in the probe deck.
- **RemixIcon excluded on licence, not quality** — 2026-08-06. It relicensed in January 2026 to
  custom terms prohibiting distribution as a standalone icon pack; vendoring the set into a
  published repository sits too close to that. Lucide (ISC) has no such question.
- **GSAP rejected on the absence of a redistribution grant** — 2026-08-06. Free to use and its
  prohibited-use clause does not bite, but there is no LICENSE file in the repository at all.
  anime.js is MIT and 11 KB larger.
- **The probe deck is a measurement vehicle and is not committed** — 2026-08-06. It is written to
  gitignored `.assets-cache/`; the repository keeps the generator and the numbers. Neutral topic,
  per CLAUDE.md.

**Outputs produced**
- `docs/research/R5-assets-and-licences.md` — the survey, the measurements and the delivery-mode
  recommendation
- `tools/assets/measure.py` — reproduces every figure; self-tests before it will measure
- `tools/assets/build_probe_deck.py` — builds the 12-slide deck the totals were taken from
- `docs/research/R4-prior-art.md` §§5, 6, 8 — rewritten from "NOT DONE" (T-012's steps 4–6)

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every candidate carries its licence, verified from the source, and a redistribution verdict | **Met** | 15 typefaces (OFL 1.1), 6 icon sets, 9 libraries. Verified from source, which is what caught the two that summaries get wrong: RemixIcon relicensed in Jan 2026, and GSAP has no LICENSE file at all |
| Embedding cost measured, not estimated: bytes added to a real 12-slide deck | **Met** | 191.8 KB total, itemised in R5 §7. Built by `build_probe_deck.py`, not estimated |
| A recommended default set, with the fallback if the default proves too heavy | **Met** | Instrument Serif · Space Grotesk · JetBrains Mono at 97.3 KB; fallback Figtree + Instrument Serif at 53.6 KB. Icons: Lucide, with Phosphor as the lighter option |
| Offline rendering verified with the network actually disabled | **Met** | Opened from `file://`, no server. 0 external references; `document.fonts.status === "loaded"` with all 3 faces; all 12 slides looked at (L-01) |

**Child fix tasks raised**
- none. One decision is referred to the owner rather than raised as a task: R5 §4 recommends
  **embedding by default** and reversing the stated CDN-by-default direction. That is the owner's
  call, and it should be settled before T-014 synthesises the design system — whether a deck must
  work offline changes what the design system may assume.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-06 | → proposed | Created to cover the icon, illustration and font coverage areas. |
| 2026-08-06 | → in_progress | Taken with T-012 steps 4–6 as one survey. Owner answered the file-size open question and widened it: delivery becomes a configuration parameter, with CDN proposed as the default. That contradicts CLAUDE.md rule 1, so producing a measured recommendation on the default became an output of this task. |
| 2026-08-06 | → done | All four acceptance criteria met. **The headline measurement changes the premise of the open question**: a complete 12-slide deck with three embedded faces, icons, a motion library and four SVG diagrams is 191.8 KB with zero external references, rendering correctly offline. Embedding is not expensive, so R5 §4 recommends embed-by-default with `linked` as a development mode. Referred to the owner, not decided here. Also settled: Mermaid's 3.48 MB runtime never ships (pre-render to SVG instead), no chart library, and htmldeck writes its own 9.1 KB deck shell rather than vendoring a framework. |
