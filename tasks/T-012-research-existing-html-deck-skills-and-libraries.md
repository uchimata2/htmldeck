---
id: T-012
title: Research existing HTML-deck skills, plugins and libraries to build on
type: research
status: done
phase: review
parent: null
blocked_by: []
related: [T-009, T-014, T-015]
work_package: WP1
shipped_in: 0.1.0
owner: maintainer
created: 2026-08-06
updated: 2026-08-12
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

Ordered so the gating deliverable lands first: T-014 is blocked on rule provenance, not on the
library survey. Steps 1–2 answer it; a session that runs out of room after step 2 has still
unblocked the project.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Read the source skills the corpus was built with, **from the skills themselves** — `visual-explainer` first, then `humanize-writing` / `humanize-prose` and the `bpmn` skill. Their files are on disk but outside every documented skill location, and the sandboxed shell cannot see them (R4 §1); invoking the skill reveals its base directory, then read `references/` and `templates/` — that is where the substance is | what each skill owns, in its own words |
| 2 | **Provenance pass over every R1 rule** — owner-authored · inherited · departure, judged against step 1's text; each departure's argument recorded | verdict column filled in `R1-rules-candidate.md` |
| 3 | Assess the remaining overlapping skills (`artifact-design`, `artifact-diagramming`, `dataviz`, `marp-slides`, `pptx-design`, `pptx-build`, `document-figures`) | depend / borrow / avoid, each with vendor-vs-defer split |
| 4 | Survey published HTML-deck skills and plugins in the wider ecosystem | candidate list |
| 5 | Survey deck frameworks and the motion/3D libraries on licence, inlined size and `file://` behaviour | framework and library verdicts |
| 6 | Survey plugin packaging conventions from the locally installed `plugin-dev` plugin (a real, readable example) | packaging notes for T-015 and T-008 |
| 7 | Answer the detection question — how a skill establishes another is present without failing noisily | detection contract with fallbacks |
| 8 | Write up | `docs/research/R4-prior-art.md` |

## 3. Implement

**Decisions & assumptions**
- Provenance verdicts live in `R4-prior-art.md` §9, **not** in `R1-rules-candidate.md` — 2026-08-06.
  R1's Verdict column belongs to T-014 (keep/drop/amend); mixing a second verdict axis into the
  same tables would put two owners in one column. R1's warning box now points at R4 instead.
- A fourth verdict, `O/S`, was added to the three the specify section named — 2026-08-06.
  B7/B19/B22/B23 are owner-authored but already ship in the owner's *own* `humanize-writing`
  skill. They are neither "inherited from a third party" nor "build it ourselves": the correct
  action is to defer, which is a different instruction to T-014 than either original category
  gives.
- Steps 4–6 deferred rather than rushed — 2026-08-06. Provenance was sequenced first because it
  gates T-014; the framework and library survey gates only T-001/T-006/T-016/T-015/T-008.

**Outputs produced**
- `docs/research/R4-prior-art.md` — §§1–4, 7, 9 complete; §§5–6 explicitly marked not done
- `docs/research/R1-rules-candidate.md` — warning box replaced with the resolved result; gaps
  register rows G-2, G-4, G-8, G-10 corrected to record that they were closed by inherited
  material

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Each candidate assessed on what it owns, licence, self-containment, verdict | **Met** | 9 libraries and frameworks measured and licence-verified — R5 §3. Ecosystem: 257 marketplace plugins searched, zero deck plugins (R4 §8) |
| Explicit depend / borrow-ideas / avoid for every installed skill listed | **Met** | Deck skill: borrow ideas, vendor nothing. `humanize-writing`: defer (R4 §7). The remaining overlapping skills fall out of R4 §7's capability-first contract — htmldeck never branches on installation, so each is an enhancement applied to a finished artefact, never a dependency |
| Publishing-format survey feeding T-015 and T-008 | **Met** | R5 §6, read from the first-party `plugin-dev` plugin |
| A stated list of what htmldeck must build itself | **Met** | R4 §8: the deck shell, diagram and chart SVG, the terminology check, and the critique mode. It vendors only anime.js, and only on request |
| **Every R1 rule carries a provenance verdict** | **Met** | All 154, R4 §9 |
| The owner's departures listed, each argument recorded | **Met, and it corrected R1** | 22 found against R1's 5. G11 reclassified as owner-authored; F11 downgraded to half a departure; 17 previously unflagged — R4 §3 |

**Child fix tasks raised**
- none. The four criteria left unmet at the provenance pass were closed 2026-08-06 by running
  steps 4–6 together with T-013, which is where they always belonged — same licence pages, same
  question.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-06 | → proposed | Created from the owner's direction not to reinvent existing work. |
| 2026-08-06 | (no change) | Scope widened to rule provenance after R1 showed an unknown share of its rules are quoted from the visual-explainer skill rather than authored by the owner. This now gates T-014. |
| 2026-08-06 | -> specified | Specify section complete; next step is planning. Selected as the next task ahead of T-010 because the provenance verdict gates T-014. |
| 2026-08-06 | -> planned | Plan reordered to put rule provenance first, since that is what gates T-014. |
| 2026-08-06 | -> in_progress | Steps 1–3 and 7 done; `R4-prior-art.md` written. All 154 R1 rules carry a provenance verdict, which lifts the provenance gate R1's warning box raised. **T-014 itself remains blocked** — by T-010, T-011, T-013, T-017 and by this task's own steps 4–6. Earlier wording here and in commit `192c3af` overstated that as "T-014 is unblocked"; corrected in R4's status note. |
| 2026-08-06 | (no change) | Correction to the previous entry's premise: the overlapping skills **do** have files on disk, in the desktop app's data tree. The sandboxed PowerShell tool reports that path as non-existent and returns nothing from a recursive search; Bash and the file tools read it fine. Recorded in R4 §1 — it is rule M11 again, and it cost two wrong conclusions in one session. |
| 2026-08-06 | -> done | Steps 4–6 completed as one survey with T-013, which is what the handoff sequenced them as. All six acceptance criteria now met. Frameworks and libraries measured rather than estimated (R5 §3); packaging read from `plugin-dev` (R5 §6); ecosystem searched across 257 marketplace plugins with zero deck plugins found. **GSAP rejected on a missing redistribution grant, not on capability** — it has no LICENSE file at all. R4 §§5, 6, 8 rewritten from "NOT DONE" to the results. |
