---
id: T-015
title: Plugin scaffold and the two-question interface
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: [T-014, T-020]
related: [T-002, T-003, T-012]
work_package: WP2
owner: maintainer
created: 2026-08-06
updated: 2026-08-07
deliverables: []
---

# T-015 — Plugin scaffold and the two-question interface

## 1. Specify

**Outcome**
The installable plugin skeleton — manifest, skill body, reference files, commands — that runs
end to end and asks the user exactly two questions before building.

**Why this one**
This is where the near-zero-config promise is either kept or lost. Everything the design system
settles is a question the skill must *not* ask. Standing this up early gives a working v1 to test
against, ahead of the build mode being finished.

**Scope**
- In: plugin manifest and directory layout per the packaging conventions found in T-012.
- In: the skill body — short, per the carried lesson, pointing at `docs/DESIGN-SYSTEM.md` and the
  archetype library on demand rather than restating them.
- In: the run-time interface, and only this:
  1. **Content length** — max and/or min.
  2. **Anything to align to** — an existing brand, deck, or source material. Optional.
  Everything else comes from the design system.
- In: sensible behaviour when the user answers neither — defaults must produce a good deck.
- Out: the deck generator itself (T-002), critique (T-004), the check (T-005).
- Out: any further configuration surface. Extension is explicitly deferred.

**Acceptance criteria**
- [ ] Installs into a clean Claude Code setup with no path editing
- [ ] Asks exactly the two questions, and nothing else, on a normal run
- [ ] Runs to completion with both questions unanswered, using defaults
- [ ] The always-loaded skill body stays short; the design system loads on demand
- [ ] Works in a project on an unrelated topic — no assumption about deck subject

**Open questions**
- ~~Does this replace T-003 (brief mode's six-section elicitation), or does the six-section brief
  become an internal structure the skill fills in silently from the two answers?~~ **Answered
  2026-08-07 by [T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md): both.** It
  replaces T-003, now `cancelled`, **and** the six sections become the internal structure the skill
  fills from the two answers plus any sources. See the log row below for what the interface gains.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Lay out the manifest and directories | plugin skeleton |
| 2 | Write the skill body and the two-question flow | skill |
| 3 | Wire the on-demand references | reference loading |
| 4 | Install clean and run end to end | install test |

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
| 2026-08-07 | (no change) | **[T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md) resolved the two-question conflict, and the two questions survive.** The distinction the owner ratified: a **question** is what the user must supply in advance, a **gate** is a generated artifact they react to, and the promise constrains only the first. So this task's central criterion stands as written — but the interface grows two skippable gates, **outline sign-off** and **detailed-spec sign-off**, defaulting to on, each independently declinable. **The specification files are written unconditionally**, gates or no gates. Also settled: this task's own open question — **it does replace T-003**, now `cancelled`, with the six sections surviving as the internal shape of the requirements stage. `BRIEF.md`'s *Interface* row carries the refined wording. |
| 2026-08-07 | (no change) | **Blocked on [T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md), added by [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md).** T-020's stated job includes resolving the two-question conflict and amending `BRIEF.md` to match; the central acceptance criterion here is *asks exactly the two questions, and nothing else, on a normal run*. If the promise is reworded to "two questions, then shows its work at three points", that criterion is **wrong rather than incomplete**, and so is the interface built to it. T-020's own open question proposed this edge and declined to add it; the audit found no deadlock to justify the caution — T-020 has no blockers. |
| 2026-08-06 | → proposed | Created to carry the owner's two-question, near-zero-config requirement. |
