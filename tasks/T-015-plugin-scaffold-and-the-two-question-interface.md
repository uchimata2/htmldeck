---
id: T-015
title: Plugin scaffold and the two-question interface
type: deliverable
status: specified
phase: specify
parent: null
blocked_by: [T-014, T-020]
related: [T-002, T-003, T-012, T-027]
work_package: WP2
owner: maintainer
created: 2026-08-06
updated: 2026-08-07
deliverables: []
---

# T-015 — Plugin scaffold and the two-question interface

## 1. Specify

**Outcome**
The installable plugin skeleton — manifest, skill body, reference files, commands — that **runs the
adopted pipeline end to end**, asks the user exactly two questions, writes both specification files
unconditionally, and stops at two gates the user can decline.

**Why this one**
This is where the near-zero-config promise is either kept or lost. Everything the design system
settles is a question the skill must *not* ask. Standing this up early gives a working v1 to test
against, ahead of the build mode being finished.

**What [T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md) changed here, 2026-08-07.**
This section was written against a three-mode plugin; the plugin now runs a seven-stage pipeline.
The two questions survive unchanged — the promise constrains **what the user must supply in
advance**, and a gate is an artifact they react to — but three things this task owns are new: the
**stage wiring**, the **artifact contract** (both specification files exist on disk for every run,
gates or no gates), and the **gates themselves**, defaulting to on and independently declinable.
The interface is therefore two questions **plus a run shape**, and the run shape is the part that
did not exist when this was first specified.

**Scope**
- In: plugin manifest and directory layout per [R5 §6](../docs/research/R5-assets-and-licences.md) —
  `.claude-plugin/plugin.json`, component directories at the plugin root, auto-discovered
  `skills/<name>/SKILL.md`, and `${CLAUDE_PLUGIN_ROOT}` for every intra-plugin path.
- In: the skill body — short, per the carried lesson, pointing at
  [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) and the archetype library on demand rather
  than restating them.
- In: the run-time interface, and only this:
  1. **Content length** — max and/or min.
  2. **Anything to align to** — an existing brand, deck, or source material. Optional, and it is
     the slot [`BRIEF.md`](../docs/BRIEF.md) open question 6 assigns the source documents to.
  Everything else comes from the design system.
- In: **the requirements assembly.** The six sections of
  [`BRIEF.md`](../docs/BRIEF.md) § *The prompt structure that works* are the internal shape of the
  requirements stage, filled from the two answers plus any supplied sources. **No section is asked
  for.** This is what absorbed T-003.
- In: **the stage wiring** — the scaffold invokes each pipeline stage in order and passes the
  artifact of one to the next. It defines the sequence and the hand-offs; the stages themselves are
  other tasks.
- In: **the artifact contract** — the foundation spec and the slide-by-slide spec are written
  **unconditionally**, on every run, including one where the user declines both gates (T-020 §3.5),
  **alongside the output deck and named after it** (owner, 2026-08-07). Two files, not three: **the
  outline is a section of the foundation spec**, which is what makes the outline gate a sign-off on
  a document that exists rather than on a fragment — one line to change if that reading is wrong.
- In: **the two gates** — outline sign-off and detailed-spec sign-off. Default **on**, each
  independently declinable, and **the skill never asks whether to skip them**: skipping is something
  the user volunteers, because asking would be a third question.
- In: sensible behaviour when the user answers neither question — defaults must produce a good deck.
- Out: the deck generator itself (T-002), the critique formats (T-004), the check (T-005), the token
  layer (T-007), the interaction layer (T-016). The scaffold calls them; it does not build them.
- Out: **what a good foundation spec or slide-by-slide spec says.** The fields are fixed by
  [`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §3.5 (DS-210 to DS-213) and T-020 §3.2; this task
  owns the file existing, not its quality.
- Out: any further configuration surface. Extension is explicitly deferred.

**Inputs**
- [T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md) §3.1 the pipeline, §3.2 the seven
  stage decisions, §3.5 the artifact/gate split, §3.6 build mode's input contract.
- [`docs/BRIEF.md`](../docs/BRIEF.md) — the *Interface* row of *Decisions taken*, § *What to build*
  and its pipeline diagram, § *The prompt structure that works*, open question 6.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §3.5 — DS-210 to DS-213, what the outline must
  name and what the specification must carry.
- [`docs/research/R5-assets-and-licences.md`](../docs/research/R5-assets-and-licences.md) §6 —
  plugin packaging, surveyed from a worked example rather than from documentation.
- [`docs/research/R4-prior-art.md`](../docs/research/R4-prior-art.md) §7–§8 — the capability-first
  contract (htmldeck never branches on what else is installed) and what it must build itself.
- [`docs/LESSONS.md`](../docs/LESSONS.md) — L-12, what is read every time must be short.

**Acceptance criteria**
- [ ] Installs into a clean Claude Code setup with no path editing, and every intra-plugin path
      resolves through `${CLAUDE_PLUGIN_ROOT}` — no absolute paths, no `~`, nothing
      working-directory-relative
- [ ] Asks exactly the two questions, and nothing else, on a normal run
- [ ] **A run with both gates declined asks exactly the same two questions and stops nowhere** —
      the gates are not questions, and declining them removes stops rather than adding one
- [ ] **The skill never asks whether to skip the gates.** Unprompted, the gated run is what happens
- [ ] Runs to completion with both questions unanswered, using defaults
- [ ] **Both specification files exist on disk after every run, including a fully declined one**,
      beside the deck and named after it
- [ ] The stages run in the order T-020 §3.2 fixes, with **each gate immediately before the
      expansion of the artifact it gates** — the outline is signed off before it becomes a
      slide-by-slide spec, not after
- [ ] The always-loaded skill body stays short; the design system loads on demand
- [ ] Works in a project on an unrelated topic — no assumption about deck subject

**Open questions**
- ~~Does this replace T-003 (brief mode's six-section elicitation), or does the six-section brief
  become an internal structure the skill fills in silently from the two answers?~~ **Answered
  2026-08-07 by [T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md): both.** It
  replaces T-003, now `cancelled`, **and** the six sections become the internal structure the skill
  fills from the two answers plus any sources. See the log row below for what the interface gains.
- ~~**Where does the outline gate sit? T-020 §3.2 and `DESIGN-SYSTEM.md` §3.5 disagree, and this
  task cannot wire both.**~~ **Answered by the owner 2026-08-07: each gate immediately follows the
  artifact it gates, and immediately precedes the expensive expansion of it.** T-020 §3.2 had placed
  outline sign-off *"after the spec review"*; DS-210 to DS-213 place the outline **before** the
  slide-by-slide spec, which is then expanded from it and only then reviewed. Under T-020's
  placement the human signed off an outline the specification had already superseded, and the cut
  decision — which **T-020 §3.4 itself names as the thing that protects the loop from wasted
  work** — arrived after the expansion it was meant to save. **The pipeline this task wires:**

  ```
  governing idea ─→ requirements ─→ foundation spec ─→ outline ─→ OUTLINE SIGN-OFF
      └─→ slide-by-slide spec ─→ spec review ─→ DETAILED-SPEC SIGN-OFF
          └─→ build, in batches ─→ build review ─→ owner review ─→ fix
  ```

  The spec review's *"Open — needs a decision"* items land at the **detailed-spec** gate, the gate
  directly after it, which is what T-020's rationale needs; it does not need the outline gate to
  carry them. **The accepted cost, stated rather than smoothed:** the first gate asks the human to
  sign off an **unreviewed** outline. Accepted because DS-213 reviews the *specification* — at
  outline time there is nothing yet to review — and because an outline is three fields per slide
  (DS-211), which is cheap to read and cheap to cut from. **Propagated:** T-020 §3.1 and §3.2,
  [`BRIEF.md`](../docs/BRIEF.md) § *What to build*, [`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md)
  §3.5.
- ~~**A second, smaller disagreement in the same place: the pipeline diagram has no outline in
  it.**~~ **Fixed with the answer above, 2026-08-07.** T-020 §3.1 and
  [`BRIEF.md`](../docs/BRIEF.md) § *What to build* both ran *requirements → foundation spec →
  slide-by-slide spec → spec review*, with no outline node, while **DS-210 is `hard`.** Recorded
  separately because fixing the gate order without fixing the diagram would have left the
  contradiction standing in the document a reader reaches first.
- ~~**Where do the specification files land, and are they the user's to keep?**~~ **Answered by the
  owner 2026-08-07: alongside the output deck, named after it.** T-020 §3.5's second reason for
  writing them unconditionally is inspectability *after* the deck turns out wrong, which only holds
  if they outlive the run — so a temporary working directory forfeits half of why they are written
  at all.

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
| 2026-08-07 | → specified | **Both open questions answered by the owner, so §1 is complete and accepted.** *Gate placement:* **each gate immediately follows the artifact it gates** — the outline is signed off before it is expanded, and the specification review's open decisions land at the gate directly after it. This **reverses the placement clause in [T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md) §3.2**, which had put outline sign-off after the specification review; corrected there, in [`BRIEF.md`](../docs/BRIEF.md) § *What to build*, and noted in [`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §3.5, whose DS-210 → DS-212 order is what exposed it. *Artifact location:* **alongside the output deck, named after it** — a temporary working directory would forfeit T-020 §3.5's own second reason for writing the files at all. §2's plan is stale against this scope and is the next phase's work. |
| 2026-08-07 | (no change) | **§1 reworked to absorb [T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md); still `proposed`, because it raises two questions only the owner can close.** The two questions and their criterion survive verbatim — the promise constrains what the user supplies in advance. What grew is the **run shape**: the stage wiring, the artifact contract (both specification files written unconditionally, on every run), and the two declinable gates. Three criteria added to hold the distinction the promise now rests on — a fully declined run asks the *same* two questions and stops nowhere; the skill never asks *whether* to skip; and the specification files exist even then. An **Inputs** section was added, which the file never had. **The finding this rework produced: T-020 §3.2 and [`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §3.5 place the outline gate in different places**, and the pipeline diagram in T-020 §3.1 and [`BRIEF.md`](../docs/BRIEF.md) omits the outline entirely although **DS-210 is `hard`**. This task cannot wire a contradiction, so both are open questions with a recommendation, not assumptions. §2's plan is deliberately untouched — it is the next phase's work and it is stale against this scope. |
| 2026-08-07 | (no change) | **[T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md) resolved the two-question conflict, and the two questions survive.** The distinction the owner ratified: a **question** is what the user must supply in advance, a **gate** is a generated artifact they react to, and the promise constrains only the first. So this task's central criterion stands as written — but the interface grows two skippable gates, **outline sign-off** and **detailed-spec sign-off**, defaulting to on, each independently declinable. **The specification files are written unconditionally**, gates or no gates. Also settled: this task's own open question — **it does replace T-003**, now `cancelled`, with the six sections surviving as the internal shape of the requirements stage. `BRIEF.md`'s *Interface* row carries the refined wording. |
| 2026-08-07 | (no change) | **Blocked on [T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md), added by [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md).** T-020's stated job includes resolving the two-question conflict and amending `BRIEF.md` to match; the central acceptance criterion here is *asks exactly the two questions, and nothing else, on a normal run*. If the promise is reworded to "two questions, then shows its work at three points", that criterion is **wrong rather than incomplete**, and so is the interface built to it. T-020's own open question proposed this edge and declined to add it; the audit found no deadlock to justify the caution — T-020 has no blockers. |
| 2026-08-06 | → proposed | Created to carry the owner's two-question, near-zero-config requirement. |
