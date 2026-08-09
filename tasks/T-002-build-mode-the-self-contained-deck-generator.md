---
id: T-002
title: Build mode — the self-contained deck generator
type: deliverable
status: planned
phase: implement
parent: null
blocked_by: [T-001, T-007, T-014, T-015, T-016, T-020]
related: [T-021, T-028]
work_package: v0.1
owner: maintainer
created: 2026-08-04
updated: 2026-08-09
deliverables:
  - shell/shell.html
  - shell/components.css
  - shell/deck.js
  - shell/icons.svg
  - tools/deck/shell.py
  - skills/htmldeck/references/build.md
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

**Scope**

- In: **stage 6 of the pipeline** — a reviewed `<slug>.slides.md` becomes `<slug>.html`, batched as
  [`pipeline.md`](../skills/htmldeck/references/pipeline.md) *Stage 6* specifies, with the gate run
  per batch rather than at the end.
- In: **the invariant half of a deck, shipped as source a run assembles from.** 97 KB of base64
  faces, the shared component block and the deck script are not authorable per run, and
  [`SKILL.md`](../skills/htmldeck/SKILL.md) already forbids the other route — the reference deck is
  *"the structural reference, not a template to fill"*. So build mode gets a **shell**: the head,
  the theme region, the component block, the script, the chrome and the reading view, held in one
  place and instantiated, never retyped and never copied into a second home.
- In: **the authored half** — per-slide `<section>` markup, the `<style id="slides">` composition
  block, figures, icons and disclosure, written against
  [`COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md).
- In: **the deviation protocol** the last open question below rules — resolve, write back, report.
- In: **the plugin wiring**: what the skill loads at stage 6, and the rows in
  [`pipeline.md`](../skills/htmldeck/references/pipeline.md) that currently say this mode is unbuilt.
- In: **one real 12-slide deck with diagrams, produced through it**, on a fresh neutral topic with
  its own sources, so the content half of the gate has something to reconcile against.
- Out: **critique mode's two report formats** — stage 5 and stage 7's outputs are
  [T-004](T-004-critique-mode-blunt-section-by-section-review.md)'s. This mode runs the gate and the
  per-batch dimensions; it does not define how a review reads.
- Out: **new rules.** This mode builds against the ruleset. The one exception is a deviation that
  contradicts an artifact, which is written back by the protocol above — and if a deviation turns
  out to be general rather than local, it is raised as a task, not legislated here.
- Out: everything the release phases put in v0.2 — 3D ([T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md)),
  the capability preflight ([T-019](T-019-build-the-capability-preflight-the-deck-ships-wit.md)),
  R6's remaining glitch-free conditions ([T-041](T-041-implement-the-nine-glitch-free-conditions.md)),
  the second printed contents sheet ([T-036](T-036-the-second-contents-page-for-long-decks.md)).
- Out: the template generator [`../CLAUDE.md`](../CLAUDE.md) rule 4 defers. The shell is
  parameterised for it; it is not built here.
- Out: **printing as a gate.** Opt-in, and it stays that way.

**Inputs**
- `docs/DESIGN-SYSTEM.md` — the ruleset the deck is built against, all of it
- `docs/COMPONENT-CONTRACT.md` — what markup to emit; `component.py check` decides it
- `docs/THEME-CONTRACT.md` — what a theme supplies; `theme.py check` decides it
- `docs/EVALUATION.md` §5 and §6 — the definition of done and the loop that reaches it
- `skills/htmldeck/references/pipeline.md` and `skills/htmldeck/references/artifacts.md` — the
  stage this mode is, and the three files a run leaves on disk
- `examples/reference-deck.html` — the structural reference and the shell's parent
- `themes/quarto.css` and `themes/faces/` — the theme region, already one home
- `tools/deck/check.py`, `component.py`, `theme.py`, `render.py` — the gate, run per batch

**Acceptance criteria**
- [ ] **Writes the slide copy from source material**, not just the design around supplied words —
      decided 2026-08-06, and the harder of the two paths
- [ ] Output is one file that renders with the network disabled
- [ ] Renders glitch-free **from `file://` in recent Chrome/Edge**, with no console errors
- [ ] Every theme value comes from the token layer (T-007); none hard-coded here
- [ ] Composes the interaction and motion components (T-016) rather than emitting bespoke markup
- [ ] **Departs from the specification when compliance requires it** rather than building a
      non-conformant slide or looping on one — the deviation is this mode's call, not a question
      returned to the user
- [ ] Every deviation is written back into the specification file it contradicts, so the artifacts
      record what was built
- [ ] Deviations reach the user at delivery as **brief bullet points**
- [ ] Tested on a real 12-slide deck with diagrams, not a three-slide toy
- [ ] Rendered deck opened and looked at
- [ ] **The shell has exactly one home**, and a check fails it having drifted from the parts it is
      assembled from — the fixture lesson (**L-05**, `seed_defects.py --check`) applied to the half
      of a deck nobody rewrites
- [ ] **The produced deck passes the whole gate**: `check.py` 0 failures with `--sources` supplied
      so the content half runs, `component.py check` every part, `theme.py check` 0 non-exempt
      literals — and the batch loop ran them, not only the final pass
- [ ] **The plugin loads this mode at stage 6**: `pipeline.md` stops recording it as unbuilt,
      `check_scaffold.py` stays green and `SKILL.md` stays under its byte budget
- [ ] **All three artifacts land beside the deck** — `<slug>.html`, `<slug>.foundation.md`,
      `<slug>.slides.md` — each written when its stage produced it, per `artifacts.md`
- [ ] *Opt-in:* a printable variant can be forced. Not a gate

**Open questions**
- ~~Does the plugin write the words?~~ **Answered 2026-08-06: yes**, from source material.
- ~~How much of the narrative decision is the generator's versus the brief's?~~ **Answered
  2026-08-07 by the owner: the specification decides the narrative, and the generator may depart
  from it where compliance requires — every departure recorded, and reported briefly.**
  [T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md) already put the spine, the
  outline and the bottom lines upstream and that stands: this mode invents no narrative. What the
  ruling did not cover is the case the owner named — **a specification can turn out unbuildable.**
  A slide that will not fit the stage, or that a `hard` rule fails on, cannot be built as written,
  and a generator with no authority to change it either ships a non-conformant slide or loops on
  it. So the generator holds **implementation authority above the detailed spec**: it resolves the
  layout or the rule conflict itself rather than returning a decision to a user who cannot picture
  the outcome. Two obligations come with the authority — **every deviation is written back into the
  artifacts it contradicts**, the slide-by-slide spec and, where the outline moved, the foundation
  spec, so those files record what was *built* rather than what was intended; and **the user is
  told at delivery, in brief bullet points**, not a rationale per item.

## 2. Plan

**The shape: nine steps, and the first four exist so the fifth can be short.** Build mode is a
reference file an agent follows, and a reference file that has to describe 582 lines of CSS and 564
lines of script is one nobody follows correctly twice. Steps 1–4 move that half out of prose and
into source with a drift check on it; step 5 is then free to be about the part that is actually a
judgement — what goes on a slide.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Lift the invariant regions out of [`examples/reference-deck.html`](../examples/reference-deck.html) — the head and its font licences, the shared component block (lines 262–843), the chrome, the reading view, and the script (1619–2183) — into shipped source | `shell/shell.html`, `shell/components.css`, `shell/deck.js` |
| 2 | Curate the icon source **DS-112 requires and this repository does not have**: the reference deck's nine, plus the concepts a general deck needs, as one sprite with its licence beside it | `shell/icons.svg` |
| 3 | Build the assembler: `new` (a skeleton with no slides), `icons` (sync the sprite to the `<use>` references actually in the deck — DS-113 mechanically), `check` (the drift check), and a self-test on fixtures whose answers are known (**L-04**) | `tools/deck/shell.py` |
| 4 | Prove the single home — `shell.py check` over the reference deck must pass, since that is the deck the parts were lifted from. A shell that has drifted from its parent is the stale-fixture failure again (**L-05**) | a green run, and the check named in [`examples/README.md`](../examples/README.md) |
| 5 | Write build mode itself: instantiate, author one slide against [`COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md), the batch loop, **the deviation protocol**, and the delivery report | `build.md`, under `skills/htmldeck/references/` |
| 6 | Wire it into the plugin: the load row in [`SKILL.md`](../skills/htmldeck/SKILL.md), and the two rows in [`pipeline.md`](../skills/htmldeck/references/pipeline.md) that record stage 6 as unbuilt | edits, and `check_scaffold.py` still green inside the byte budget |
| 7 | Run the whole pipeline on a **fresh neutral topic with its own sources** — governing idea through to a built deck, in four batches of three | `examples/<slug>/` — the deck, `<slug>.foundation.md`, `<slug>.slides.md`, and its `sources/` |
| 8 | Gate it and **look at it**: `check.py --sources`, `component.py check`, `theme.py check`, `render.py shots`, every slide opened offline, the print variant forced once | the measurements, and the deviation bullets the run owes the user |
| 9 | Close: the `examples/README.md` row, whatever earned a place in [`LESSONS.md`](../docs/LESSONS.md); then this file's implement and review sections, `index` and `check --closing` | a closed task |

**Approach decisions**

- **The agent edits the deck file; the tool does not compose it from fragments.** — `shell.py new`
  writes a skeleton and then gets out of the way, because the build is **batched** (three slides,
  gate, three more) and a compose-from-fragments design turns every batch into a rebuild of the
  whole file. Editing in place is also what makes step 3's `check` worth having: it is the thing
  that notices when a batch edit strayed into the shared block. — 2026-08-09
- **The sprite is synced from the deck, not declared by hand.** — DS-113 says *only the icons used*,
  and that is a fact about the file rather than a thing to remember; `shell.py icons` reads the
  `<use href="#i-…">` references and rewrites the sprite to match. — 2026-08-09
- **The icon set is curated once and looked at, rather than drawn per deck.** — DS-112 forbids
  hand-drawn icons and names Lucide, and nothing in this repository ships one, so every deck so far
  has depended on an agent recalling path data correctly. That is the same risk once instead of
  every run, and this time it gets rendered and inspected. — 2026-08-09
- **The produced deck ships under `examples/<slug>/`, all four parts together.** — `artifacts.md`
  puts the three run outputs in one directory; keeping the sources beside them makes the directory
  the worked example of the artifact contract, not just a deck. — 2026-08-09
- **Four batches of three.** — Twelve slides, and the batch exists so a component defect is fixed
  once; three is the smallest batch that contains more than one archetype. — 2026-08-09

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
| 2026-08-09 | → planned | **Nine steps, and one thing the plan found that §1 did not: DS-112 forbids hand-drawn icons, names Lucide, and nothing in this repository ships an icon source.** So every deck built here has depended on an agent recalling path data correctly, the reference deck's nine included — which is a `hard` rule satisfied by luck. `shell/icons.svg` is step 2 and it converts that into one curated set that gets rendered and looked at. The other decision worth reading is that **the tool writes a skeleton and the agent then edits the deck in place**, rather than composing it from fragments: the build is batched, and a compose design makes every batch a whole-file rebuild. The produced deck's paths join `deliverables:` at step 7, when its slug is fixed. |
| 2026-08-09 | → specified | **§1 completed: scope, inputs and four more criteria.** The scope decision worth reading is the first one in, and it was forced by arithmetic rather than preference: a deck is 225 KB of which 97 KB is base64 faces and roughly 580 lines is a shared component block, so **the invariant half cannot be authored per run** — and the other route is already closed, because [`SKILL.md`](../skills/htmldeck/SKILL.md) calls the reference deck *"the structural reference, not a template to fill"*. So build mode instantiates a **shell** and authors only what differs per deck: the sections, the `<style id="slides">` composition, the figures and the icons. That is also what makes the criterion *every theme value comes from the token layer* mechanically true rather than a thing to remember — the theme region already has one home in `themes/`, and the shell keeps it. **The new criteria are the shell's single home, the whole gate on the produced deck with `--sources` so the content half runs, the plugin actually loading this mode at stage 6, and all three artifacts landing beside the deck.** |
| 2026-08-09 | (no change) | **The last blocker closed, and this task is now the only thing between the repository and a v0.1 that ships.** All six of `blocked_by` are `done`. What [T-016](T-016-the-interaction-and-motion-layer.md) hands over is the answer to *what does the generator emit*, in three documents rather than one: [`COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) — 59 authored parts, their element, place, count and attributes, and the eleven rules that must read a motion token — is what the criterion *composes the components rather than emitting bespoke markup* now means, and `component.py check` decides it; [`THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) is the other criterion's, and `theme.py check` fails a length, duration or easing curve written outside the region. **The third is new and is the one that changes what this mode has to decide: DS-230.** §5.3 gave build mode eleven mechanical rules about disclosure and no editorial test, so a generator satisfying every one of them could still put an appendix behind the click. Tier two is now one of four kinds — `derivation` · `scope` · `condition` · `instances` — the list is closed, and **every `.disc` declares which in `data-disc`**, so the split is a decision this mode makes explicitly rather than by accident. **DS-231** is the mechanical half: a bottom line citing a figure that lives only behind the click fails the gate. |
| 2026-08-07 | (no change) | **The last open question is answered, and the answer gives this mode an authority it did not have: it may depart from the specification to keep the deck compliant.** Three acceptance criteria added for it. The owner's reason is the failure mode a strict-obedience generator has no exit from — a slide that will not fit the stage or that a `hard` rule fails on cannot be built as specified, so obedience means shipping a non-conformant slide or looping. **The loop already has language for the two cases this does *not* cover:** [`EVALUATION.md`](../docs/EVALUATION.md) §6.1's **STALL** (a design decision wearing a finding's clothes — escalate) and **OSCILLATION** (two rules in tension — stop and name them, and record it in [`DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) §2). Deviation authority is for what the generator *can* resolve; those two outcomes remain the exits for what it cannot, and this ruling does not weaken them. **Where the deviations are written is already fixed** by [`artifacts.md`](../skills/htmldeck/references/artifacts.md): `<slug>.slides.md` and, when the outline moved, `<slug>.foundation.md` — both of which exist to be *"what a reader opens when the deck turns out wrong"*, which they are not if they record only the intent. The user-facing half is bullet points at delivery, and it is the first thing this mode must report that is not the deck. |
| 2026-08-07 | (no change) | **[T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md) settled this mode's input contract, and it is not a brief.** Build mode consumes a **reviewed slide-by-slide specification** — seven fields per slide, structure · text · visuals · animations · interactive elements · title · bottom line — produced upstream from the two answers, the sources and the foundation spec. Two consequences beyond the input type: **the build is batched by default**, a few slides at a time, each batch running the auto gate, the render gate and S3/S5/S6 before the next is written, because DS-136 reuse means a component defect found in batch one is fixed once rather than twelve times; and **the bottom line arrives specified rather than invented at layout time**, which is the contract [T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) exists because no deck met. T-020 §3.2, §3.4, §3.6. |
| 2026-08-07 | (no change) | **Three blockers added by [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md).** [T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md) because it decides this mode's **input contract** — a brief or a specification — and a generator specified against the wrong one is respecified rather than adjusted; T-020's own open question proposed exactly this edge and left it `related` only to avoid a deadlock that does not exist, since T-020 has no blockers of its own. [T-007](T-007-define-the-parametric-theme-layer.md) and [T-016](T-016-the-interaction-and-motion-layer.md) because two acceptance criteria above already require every theme value to come from the token layer and every component to be composed rather than emitted bespoke: with neither contract in existence, the only thing this mode can do is hard-code, which [`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §1.2 calls `hard`. `related` gains T-021, the other half of the two renderings, and T-028, the reference output this mode is judged against. |
| 2026-08-06 | (no change) | **The generator now has a reference output to be judged against**: [`examples/reference-deck.html`](../examples/reference-deck.html), 12 slides, 178 KB, zero external references, built by hand to the ruleset by [T-024](T-024-build-the-reference-deck-and-validate-the-ruleset.md). That closes the objection in T-024's scope — a generator with no reference output is a generator nobody can review. **What it should automate is now visible rather than assumed**, and so is what it must not: five of the ten evaluation dimensions cannot be checked mechanically, so the build mode cannot self-certify. |
| 2026-08-04 | → proposed | Seeded from `docs/BRIEF.md` when the project folder was prepared. |
| 2026-08-06 | (no change) | Updated for the owner's decisions: writes copy from source material, minimal-JavaScript habit dropped, print demoted to opt-in, `file://` Chrome/Edge render added as a gate. |
| 2026-08-06 | (no change) | **T-014 closed — [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) is now the ruleset this mode builds against.** Two things grow scope, both by pointer: **§9.4** — the heading check is semantic, so build mode must write headings that are *claims*, not labels; and **§9.5** — Layered Detail is a modifier, not a slide type, so the build decides a tier-one/tier-two split for **every** slide rather than selecting a disclosure archetype. **§9.1 is a blocker in practice**: the fixed-stage question needs an owner decision before the stage is built. §3.2 replaces L3's nine archetypes with thirteen plus one modifier. |
| 2026-08-06 | (no change) | **§9.1 is no longer a blocker — the owner settled it: keep the fixed stage, add a reflow view ([T-021](T-021-the-reflow-view-and-the-resolution-contract.md)).** But the stage this mode builds is now specified much more tightly, in [`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §2.4: a **1920×1080 design space, uniformly scaled**, with **exactly one layout — no media queries, no breakpoints, no `max-width` containers, no `vw`/`vh` type inside the stage**. Type is in design units with a hard floor: **nothing under 18, body 24–28**. The reason is measured, not stylistic: under a uniform scale the presenter's viewport cancels out of the screen-share legibility equation, so a responsive presentation layout is illegible over a video call in a way the stage is not. |
| 2026-08-06 | (no change) | **Build mode now has a stated definition of done.** [`docs/EVALUATION.md`](../docs/EVALUATION.md) §5: zero `hard` violations, every slide ≥ 18/24 with no dimension below 2, deck ≥ 12/16 with no dimension below 2. Before this the loop terminated when the agent felt finished. Two things bind the generator directly: the **per-dimension floor** means a slide cannot be shipped on craft while its claim is absent, and **S4 Density's anchor** makes the tier split a build-time decision on every slide rather than a flourish. The design system is also restructured — rules are cited as `DS-nnn` now, and the rationale moved to [`DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md). |
