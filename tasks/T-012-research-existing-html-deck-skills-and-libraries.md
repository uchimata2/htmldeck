---
id: T-012
title: Research existing HTML-deck skills, plugins and libraries to build on
type: research
status: specified
phase: specify
parent: null
blocked_by: []
related: [T-009, T-014, T-015]
work_package: WP1
owner: maintainer
created: 2026-08-06
updated: 2026-08-06
deliverables: [docs/research/R4-prior-art.md]
---

# T-012 — Research existing HTML-deck skills, plugins and libraries to build on

## 1. Specify

**Outcome**
A prior-art survey with a build/borrow/depend verdict on each candidate, so htmldeck reuses what
already exists and only builds what is genuinely missing.

**Why this one**
The owner does not start projects from the ground up. Presentation tooling is a crowded field and
several relevant skills are already installed locally — writing a worse version of any of them
would be the main way this project fails. This also answers the "other skills to rely on" coverage
item directly.

**Scope**
- In: Claude Code skills and plugins already available in this environment that overlap —
  `artifact-design`, `artifact-diagramming`, `dataviz`, `visual-explainer`, `marp-slides`,
  `pptx-design`, `pptx-build`, `humanize-prose`, `humanize-writing`, `document-figures` — assessed
  for what each already owns and whether htmldeck should depend on it or deliberately not.
- In: published HTML-deck skills and plugins from the wider Claude Code ecosystem.
- In: deck frameworks (reveal.js, Slidev, Marp, Spectacle, impress.js) and the licence and
  self-containment implications of vendoring versus reimplementing.
- In: **animation, motion and 3D libraries** — GSAP, Motion, anime.js, three.js and the lighter
  WebGL wrappers — assessed on licence, inlined size, and whether they run from `file://`.
  Added 2026-08-06 when richness replaced the minimal-JavaScript constraint.
- In: **the skills the corpus decks were actually built with** — added 2026-08-06 when R1 showed an
  unknown share of its `stated` rules are quoted from a general-purpose deck skill rather than
  authored by the owner. Named in the corpus: **`anthropic-skills:visual-explainer`** (cited as an
  authority throughout, and a stated requirement in one spec), the owner's own
  `Humanizer/humanize-writing.skill`, and a project-local `bpmn-diagram` skill. `visual-explainer`
  is a built-in skill with no file on disk — read it by invoking it via the Skill tool.
- In: **a provenance verdict on every R1 rule** — owner-authored · inherited from the skill ·
  **owner's deliberate departure from the skill**. The departures matter most: they are positions
  argued against a default, which is where taste is actually visible. R1's flagged candidates are
  L1 (fixed 1600×900 scaled stage vs the skill's `100dvh` flex default), J1–J2 (self-containment
  vs CDN), D3 (embedded faces), F11 (the four-motion vocabulary) and G11 (the spine ribbon).
- In: the corpus helper scripts.
- Out: anything requiring a build step, a package manager at deck-open time, or a network fetch.

**Acceptance criteria**
- [ ] Each candidate assessed on: what it owns, licence, self-containment, and verdict
- [ ] For every installed skill listed above, an explicit depend / borrow-ideas / avoid decision
      with the reason
- [ ] Publishing-format survey done: what a Claude Code plugin repo must contain, and how skills,
      commands and references are laid out (feeds T-015 and T-008)
- [ ] A stated list of what htmldeck must build itself because nothing covers it
- [ ] **Every R1 rule carries a provenance verdict** — owner-authored / inherited / departure
- [ ] The owner's departures from the skill are listed and each one's argument recorded

**Answered 2026-08-06 — self-contained core, optional enhancement.** htmldeck ships everything it
needs to work standalone for a user who installed nothing else, and uses the other skills when
they happen to be present. So the assessment of each candidate must produce two verdicts, not one:
what htmldeck vendors, and what it defers to when available. Detection and graceful degradation
are part of the design, and every enhancement path needs a stated fallback.

**Open questions**
- How does a skill reliably detect that another skill is installed, without failing noisily when
  it is not? — research this task

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Inventory installed overlapping skills and read what each owns | overlap table |
| 2 | Survey published HTML-deck skills and plugins | candidate list |
| 3 | Survey deck frameworks against self-containment | framework verdicts |
| 4 | Survey plugin packaging conventions | packaging notes |
| 5 | Write up with verdicts and the build-ourselves list | `docs/research/R4-prior-art.md` |

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
| 2026-08-06 | → proposed | Created from the owner's direction not to reinvent existing work. |
| 2026-08-06 | (no change) | Scope widened to rule provenance after R1 showed an unknown share of its rules are quoted from the visual-explainer skill rather than authored by the owner. This now gates T-014. |
| 2026-08-06 | -> specified | Specify section complete; next step is planning. Selected as the next task ahead of T-010 because the provenance verdict gates T-014. |
