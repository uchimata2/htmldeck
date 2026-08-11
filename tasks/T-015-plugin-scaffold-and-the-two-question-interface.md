---
id: T-015
title: Plugin scaffold and the two-question interface
type: deliverable
status: done
phase: review
parent: null
blocked_by: [T-014, T-020]
related: [T-002, T-003, T-012, T-027]
work_package: WP2
shipped_in: 0.1.0
owner: maintainer
created: 2026-08-06
updated: 2026-08-12
deliverables:
  - .claude-plugin/plugin.json
  - skills/htmldeck/SKILL.md
  - skills/htmldeck/references/pipeline.md
  - skills/htmldeck/references/artifacts.md
  - tools/plugin/check_scaffold.py
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
| 1 | Lay out the manifest and the plugin directories per R5 §6 | `plugin.json`, under `.claude-plugin/` |
| 2 | Write the run shape — seven stages, two gates, what each hands the next, and which task owns each stage | `pipeline.md`, under `skills/htmldeck/references/` |
| 3 | Write the artifact contract — naming, location, and the two file templates | `artifacts.md`, under `skills/htmldeck/references/` |
| 4 | Write the skill body — the two questions, the defaults, the gate rule, and the load-on-demand table | `SKILL.md`, under `skills/htmldeck/` |
| 5 | Build the scaffold check, with a self-test on cases whose answer is known (**L-04**) | `check_scaffold.py`, under `tools/plugin/` |
| 6 | Trace the interface under three run shapes — normal, both gates declined, both questions unanswered — counting every stop | the counts, in §3 |
| 7 | Exercise the artifact contract on a neutral topic to the build hand-off | the two specification files, and what §3 records about where the run stops |

**Approach decisions**

- **The plugin is the repository, not a subdirectory of it.** R5 §6 describes what *htmldeck's
  repository* must contain, and `${CLAUDE_PLUGIN_ROOT}` then resolves the existing `docs/` and
  `examples/` without copying them. The alternative — a `plugin/` subtree — would duplicate the
  design system into `references/`, which is **L-13** exactly.
- **The references the skill loads are the documents that already exist.** `SKILL.md` points at
  `docs/DESIGN-SYSTEM.md`, `docs/EVALUATION.md` and `examples/reference-deck.html` in place. Only
  two reference files are *written* here, and both carry something no document owns yet: the run
  shape, and the artifact contract.
- **`docs/DESIGN-RATIONALE.md` is on a never-load list, in the skill body.** BRIEF says no runtime
  loads it; a rule stated only in a document the runtime does not read is not enforced.
- **No `commands/` directory.** A slash command per mode is a configuration surface, and §1 defers
  extension. The skill triggers from what the user asks for.
- **Step 7 stops at the build hand-off, deliberately.** Build mode is T-002 and does not exist, so a
  deck produced here would be a toy — which **L-02** rules out as evidence and CLAUDE.md rules out
  as a verification bar. What step 7 proves is the part this task owns: the questions, the stops and
  the artifacts. The criterion that needs the other half is marked in §4 rather than claimed.

## 3. Implement

### 3.1 The interface, traced under three run shapes

The criteria this task turns on are behavioural, and the behaviour is written rather than compiled.
So it is traced twice — once by enumerating every interrogative in the three skill files, and once
by walking each run shape through them.

**Enumeration.** Three `?` characters exist across `SKILL.md`, `pipeline.md` and `artifacts.md`.
Two are the questions (`SKILL.md` lines 15–16). The third is *"What does this animation encode?"*,
which the author asks about their own animation and never puts to the user. Every other imperative
to ask is either a **prohibition** (*never ask a third question*, *never ask whether to skip the
gates*, *never ask which*) or a **gate** (*Ask for: cuts, additions, reordering…*), which is a
reaction to a shown artifact rather than a question answered in advance.

**The three run shapes.**

| Run shape | Questions asked | Stops after the questions | Specification files |
| :--- | :---: | :---: | :---: |
| Normal — nothing volunteered | **2** | 2 — gate 1, gate 2 | both |
| Both gates declined | **2** | **0** | both |
| Both questions unanswered | **2**, unanswered; defaults used | 2 | both |

**The question count does not move.** Declining the gates *removes* stops rather than adding one,
which is the distinction the two-question promise now rests on, and it holds in the artifact rather
than only in the argument for it.

### 3.2 What the dry run exercised, and what it did not

Run shape three — **both questions unanswered** — on a neutral topic with no sources: equipment
lending at a public library, 10 slides, chosen so that nothing in the skill could be leaning on a
deck subject.

**Exercised:** stages 1 to 4 in full, and stage 5 far enough to populate its output section. Both
specification files were produced from the templates, sharing one slug, in one directory.

**Not exercised, and this is the honest half:** the gates. A dry run has no second party to sign
anything off, so gate behaviour above is **traced, not run**. Nor was stage 6 — build mode is T-002
and does not exist, and a toy deck built to fill the gap would be evidence of nothing (**L-02**).

### 3.3 Two findings the dry run produced, both fixed

1. **A presentation-only run could invent a number and let it read as measured.** `pipeline.md`
   stage 2 said what to do when sources *are* supplied — build the reconciliation table, every
   figure traceable to one — and said nothing about the other branch. The dry run needed five
   figures and had no source for any of them, so it had to invent the rule itself, which means
   every run would invent it differently. **This is the S2 Evidence failure, and it is the one a
   presentation-only run cannot catch for itself**, because there is nothing to check against.
   Fixed: stage 2 now carries the branch — mark on the slide as a placeholder the author must
   replace, or it does not ship.
2. **Gate 2 said what to show and what to do when declined, but never what to ask for.** Gate 1
   had all three. Fixed, and the fix carries the reason the two gates ask for different things:
   asking for whole-specification approval at gate 2 would re-ask what gate 1 settled, and a user
   asked twice waves both through.

**Decisions & assumptions**

- **No `repository` field in the manifest — 2026-08-07.** R5 §6 lists it as wanted for
  distribution, and this repository has no remote yet. A plausible-looking URL would be a dead
  pointer shipped in the one file a marketplace reads.
  [T-008](T-008-package-document-and-publish.md) adds it with the remote.
- **Version `0.1.0`.** Nothing is published, and three of the seven stages are thin.
- **The path rule is blanket, not keyed on the word "load" — 2026-08-07.** The first version of the
  check flagged a bare path only inside a sentence containing *load*, which let `Build to
  <a doc>` straight past. **That is L-30 exactly**: a rule keyed on one value exempts everything
  the value does not match. Replaced with *every* bare repo-relative path in a skill file, which
  then found **13 real instances** the keyed version had passed, including four in the load table
  itself.
- **Fixture paths in the scaffold check are assembled from components, not written as literals —
  2026-08-07.** Written literally, `tools/tasks/task.py check` reads them as pointers into this
  repository and reports four dead ones, because nothing distinguishes a fictional path in a test
  table from a real reference in prose. Assembling them makes them what they are: structured data.
  **This is the same distinction `task.py` already draws for front-matter**, arrived at
  independently and from the other side.
- **Assumed: the outline is a section of the foundation spec, not a third file.** The dry run
  supports it — gate 1 shows a section of a document that exists, rather than a fragment with no
  home — but no run has been through gate 1 with a real second party. One line to change.

**Outputs produced**
- `.claude-plugin/plugin.json`
- `skills/htmldeck/SKILL.md` — 4,968 bytes of an 8,192-byte budget
- `skills/htmldeck/references/pipeline.md`
- `skills/htmldeck/references/artifacts.md`
- `tools/plugin/check_scaffold.py` — six checks, ten self-test fixtures, all passing

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Installs into a clean setup with no path editing; every intra-plugin path through `${CLAUDE_PLUGIN_ROOT}` | **part** | **The path half is met and mechanically enforced** — `check_scaffold.py` passes with ten fixtures, and the strict rule found 13 real violations the first version missed. **The install half is not demonstrated**: nothing here installed the plugin into a clean setup. That is already [T-008](T-008-package-document-and-publish.md)'s criterion *"installs from a clean clone"*, so it is left there rather than duplicated. |
| Asks exactly the two questions, and nothing else, on a normal run | met | §3.1. Two interrogatives exist in the whole package; the third `?` is the author's own motion check. **Verified against the instructions, not against a live run** — see the row above for why that half is elsewhere. |
| A run with both gates declined asks the same two questions and stops nowhere | met | §3.1, row two. Declining removes stops; it adds none. |
| The skill never asks whether to skip the gates | met | Stated as a prohibition in both `SKILL.md` and `pipeline.md`, and no interrogative for it exists to contradict them. |
| Runs to completion with both questions unanswered, using defaults | **part** | Defaults exist (8–12 slides, no alignment material, both gates on) and the dry run used them through stage 4. **"Completion" needs stage 6, which is build mode — T-002, and out of scope here by §1.** Recorded as part rather than met, because a run that stops at the build hand-off is not a finished deck and should not read as one. |
| Both specification files exist on disk after every run, beside the deck and named after it | met | Demonstrated once, on the hardest default case. Both files, one slug, one directory. The *"including a fully declined one"* clause is traced rather than run — the artifact path does not branch on the gates, which is the point of writing them unconditionally. |
| The stages run in T-020 §3.2's order, each gate immediately before the expansion it gates | met | `pipeline.md` — outline inside stage 3, gate 1, then stage 4 expands it. This is the order the owner settled 2026-08-07, and the reason it had to be settled first. |
| The always-loaded skill body stays short; the design system loads on demand | met | 4,968 bytes of 8,192, enforced by the check rather than by intention. Nothing from `DESIGN-SYSTEM.md` is paraphrased in the body except four of the nine §0 rules, which are named as pointers into it. |
| Works in a project on an unrelated topic — no assumption about deck subject | met | The dry run was a public-library equipment-lending case, picked for having nothing to do with software, decks or this repository. Nothing in the three skill files names a subject domain. |

**Two things worth saying beyond the criteria**

- **The scaffold check found more than it was built to find.** It was written for the manifest and
  the path form; the strict path rule then caught 13 live mis-resolutions, four of them in the load
  table that is the skill's whole routing job. A bare `docs/DESIGN-SYSTEM.md` in a user's project
  resolves against *their* `docs/` — the failure would have been silent and would have looked like
  a bad deck rather than a bad path.
- **The dry run earned its place, and the cheap half is the half that paid.** Both findings in §3.3
  came from stages 1 to 4 — writing the two files, not building anything. That is the same result
  T-020 §3.3 predicted for the pipeline and it is the first time this project has seen it from the
  inside.

**Child fix tasks raised**
- none. Both `part` verdicts land on tasks that already carry them — the install proof is
  [T-008](T-008-package-document-and-publish.md)'s criterion, and completion through stage 6 is
  [T-002](T-002-build-mode-the-self-contained-deck-generator.md)'s whole subject. Raising a task
  for either would duplicate an edge the backlog already has.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-07 | → done | **The plugin exists and runs its own pipeline; seven of nine criteria met, two `part` and both left where they already belong.** Five outputs: the manifest, a 4,968-byte skill body, the run shape, the artifact contract, and a scaffold check with ten self-test fixtures. **Two findings, and neither came from the thing that was built.** The scaffold check's first path rule keyed on the word *load* and let `Build to <a doc>` past — **L-30**, and replacing it with a blanket rule found **13 live mis-resolutions**, four of them inside the load table that is the skill's entire routing job. The dry run then found that a **presentation-only run could invent a figure and let it read as measured**, because stage 2 specified only the branch where sources exist; and that gate 2 said what to show and what to do when declined but never what to *ask for*. Both fixed. The `part` verdicts are honest ones: the plugin has not been installed into a clean setup (T-008's criterion) and cannot run past the build hand-off (T-002's subject). Two lessons: the keyed-rule case is a **second instance of L-30**, recorded there because inclusions key on values as readily as exemptions do; and **L-34** is new — a test fixture is indistinguishable from live input, which is what makes it useful and what makes it collide with every other scanner over the same repository. |
| 2026-08-07 | → planned | Seven steps, and two approach decisions that shaped everything after. **The plugin is the repository, not a subtree of it** — `${CLAUDE_PLUGIN_ROOT}` then resolves the existing `docs/` and `examples/` in place, where a `plugin/` subtree would have duplicated the design system into `references/` and put two copies of the ruleset one edit apart (**L-13**). And **step 7 stops at the build hand-off deliberately**: build mode does not exist, and a three-slide toy built to fill the gap is what **L-02** rules out as evidence. |
| 2026-08-07 | → specified | **Both open questions answered by the owner, so §1 is complete and accepted.** *Gate placement:* **each gate immediately follows the artifact it gates** — the outline is signed off before it is expanded, and the specification review's open decisions land at the gate directly after it. This **reverses the placement clause in [T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md) §3.2**, which had put outline sign-off after the specification review; corrected there, in [`BRIEF.md`](../docs/BRIEF.md) § *What to build*, and noted in [`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §3.5, whose DS-210 → DS-212 order is what exposed it. *Artifact location:* **alongside the output deck, named after it** — a temporary working directory would forfeit T-020 §3.5's own second reason for writing the files at all. §2's plan is stale against this scope and is the next phase's work. |
| 2026-08-07 | (no change) | **§1 reworked to absorb [T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md); still `proposed`, because it raises two questions only the owner can close.** The two questions and their criterion survive verbatim — the promise constrains what the user supplies in advance. What grew is the **run shape**: the stage wiring, the artifact contract (both specification files written unconditionally, on every run), and the two declinable gates. Three criteria added to hold the distinction the promise now rests on — a fully declined run asks the *same* two questions and stops nowhere; the skill never asks *whether* to skip; and the specification files exist even then. An **Inputs** section was added, which the file never had. **The finding this rework produced: T-020 §3.2 and [`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §3.5 place the outline gate in different places**, and the pipeline diagram in T-020 §3.1 and [`BRIEF.md`](../docs/BRIEF.md) omits the outline entirely although **DS-210 is `hard`**. This task cannot wire a contradiction, so both are open questions with a recommendation, not assumptions. §2's plan is deliberately untouched — it is the next phase's work and it is stale against this scope. |
| 2026-08-07 | (no change) | **[T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md) resolved the two-question conflict, and the two questions survive.** The distinction the owner ratified: a **question** is what the user must supply in advance, a **gate** is a generated artifact they react to, and the promise constrains only the first. So this task's central criterion stands as written — but the interface grows two skippable gates, **outline sign-off** and **detailed-spec sign-off**, defaulting to on, each independently declinable. **The specification files are written unconditionally**, gates or no gates. Also settled: this task's own open question — **it does replace T-003**, now `cancelled`, with the six sections surviving as the internal shape of the requirements stage. `BRIEF.md`'s *Interface* row carries the refined wording. |
| 2026-08-07 | (no change) | **Blocked on [T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md), added by [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md).** T-020's stated job includes resolving the two-question conflict and amending `BRIEF.md` to match; the central acceptance criterion here is *asks exactly the two questions, and nothing else, on a normal run*. If the promise is reworded to "two questions, then shows its work at three points", that criterion is **wrong rather than incomplete**, and so is the interface built to it. T-020's own open question proposed this edge and declined to add it; the audit found no deadlock to justify the caution — T-020 has no blockers. |
| 2026-08-06 | → proposed | Created to carry the owner's two-question, near-zero-config requirement. |
