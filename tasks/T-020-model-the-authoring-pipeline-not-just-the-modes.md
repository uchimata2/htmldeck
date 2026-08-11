---
id: T-020
title: Model the authoring pipeline, not just the three modes
type: decision
status: done
phase: review
parent: null
blocked_by: []
related: [T-002, T-003, T-004, T-014, T-015, T-023, T-030]
work_package: WP1
shipped_in: 0.1.0
owner: maintainer
created: 2026-08-06
updated: 2026-08-12
deliverables: []
---

# T-020 — Model the authoring pipeline, not just the three modes

## 1. Specify

**Outcome**
A decision on whether htmldeck models the owner's full authoring pipeline — with its intermediate
artifacts and its approval gates — or keeps the three-mode shape the brief currently describes. If
the pipeline is adopted, the mode list, `docs/BRIEF.md` § *What to build*, and the input contract of
build mode all change.

**Why this one**
**The research already found this and the build plan never absorbed it.** Raised 2026-08-06 when
the owner described their working process and it did not match anything in the repository.

[R1 §10](../docs/research/R1-corpus-conventions.md) records the pipeline from two unrelated
foundation specs:

> requirements → foundation spec → slide-by-slide spec → **review of the spec** → build → review of
> the build → owner review → fix

R1 §2 adds that specification precedes implementation, that the deck is built **page by page and
explicitly not in one pass**, that each slide is specified for structure · text · visuals ·
animations · interactive elements · title · bottom line, and that building happens **in batches so
feedback lands before the whole deck is built out**. R1 §10 names the **nine-section Foundation
Spec** both specs share and says it is what the plugin should generate before writing any HTML, plus
the **governing idea in one line** written before anything else.

[R4 §9](../docs/research/R4-prior-art.md) then grades A′1–A′3 and A′5–A′11 as **`O` — owner-authored**,
noting the source deck skill *"has no specification-document concept at all — no governing idea, no
foundation spec, no review cycle, no trace table, no timing budget."* By R4 §2's own framing, that
makes this pipeline one of the places the owner's taste is most visible, and it has **zero prior
art**.

`docs/BRIEF.md` § *What to build* still lists three modes — brief, build, critique — plus a check.
That section predates the corpus research and was never reconciled with it. The words "outline" and
"approval" do not appear anywhere in the repository.

**Scope**
- In: whether a **foundation spec** and a **slide-by-slide spec** are artifacts the plugin produces,
  or internal reasoning it never surfaces.
- In: whether the **specification review** — the second critique format R1 §14 proves, run before
  any HTML exists — becomes part of critique mode or a mode of its own. T-004 currently reviews a
  built deck only.
- In: whether **batched build** (a few slides, then feedback) is the default rather than one pass.
- In: **where the convergence loop sits, and it is now the centre of this task.** Added by the owner
  2026-08-06: *a design system without an effective and efficient pipeline is just decoration.*
  [`docs/EVALUATION.md`](../docs/EVALUATION.md) defines the loop — evaluate → report → fix →
  re-evaluate, with four distinct stop conditions. **This task decides where it runs**, and the
  placement questions are real:
  - Does the loop run **per batch** (converge 3 slides, then build the next 3) or **once at the end**
    over the whole deck? Per batch converges cheaply on craft but cannot see D1 Spine or D4
    Consistency, which are whole-deck dimensions by construction. **The likely answer is both, at
    different depths** — per-slide dimensions per batch, whole-deck dimensions once — but that is a
    hypothesis and it changes the cost profile substantially.

    > **Narrowed by [T-026](T-026-settle-who-scores-a-deck-and-whether-the-score-is-shown.md),
    > 2026-08-06.** The hypothesis's clean split no longer holds: EVALUATION §8.1 rules that **S1,
    > S2 and S4 — per-slide dimensions — are scored in one fresh-context read of the whole deck**,
    > alongside D1–D4. So a per-batch loop can carry only S3, S5 and S6; three of the five
    > dimensions no mechanical check can reach are whole-deck-timed regardless of batching. The
    > open question is now *what a batch loop is worth when it covers only the three mechanically
    > checkable dimensions*, not whether to split by per-slide vs whole-deck.
  - Does the loop run **before or after** the owner's approval gate? Running it first means the owner
    reviews converged work; running it after means the loop does not burn iterations on slides the
    owner was going to cut. **These are opposite optimisations and the corpus does not settle it.**
  - Does the **specification review** (the second critique format, run before any HTML exists) get
    its own rubric, or is it out of the loop's scope? The rubric's dimensions are mostly about
    rendered artifacts; S1 Claim, S2 Evidence, D1 Spine and D3 Close would all work against a
    slide-by-slide spec. **If they do, defects get caught before any HTML is written**, which is the
    cheapest place to catch them and is exactly what the owner's pipeline was already doing.
- In: the **approval gates** — outline sign-off, preview sign-off, and the review→fix loop — and how
  many iterations are assumed.
- In: the **governing idea in one line**, and which artifact carries it.
- In: **reconciling all of the above with the two-question interface** — see the conflict below.
- Out: building any of it. This decides the shape; the mode tasks build it.
- Out: the design-system rules themselves (T-014).

**The conflict this task exists to resolve**

`docs/BRIEF.md` § *Decisions taken* commits to an interface that **"asks exactly two questions…
nothing else"**, in service of near-zero configuration. The owner's actual process has at least
three interaction points: outline approval, preview approval, and an iterate-until-right loop.

These are reconcilable, and the likely resolution is worth stating so it can be argued with:
**questions and gates are not the same thing.** Two questions up front is a claim about how much the
user must *specify in advance*; a gate is a generated artifact the user *reacts to*. Reacting to an
outline is cheaper for the user than answering questions about structure, and it is how the owner
actually works. If that reading is accepted, the brief's promise needs rewording — from "asks two
questions" to something like "asks two questions and then shows its work at three points".

**But that is a re-scope of a stated owner decision, which is why this is a `decision` task and not
an implementation one.**

**Inputs**
- `docs/research/R1-corpus-conventions.md` §2, §10, §14 — the pipeline, the nine-section spec, and
  the two proven critique formats.
- `docs/research/R1-rules-candidate.md` — rules A4, A6, A′1–A′11.
- `docs/research/R4-prior-art.md` §9 — the provenance verdicts that make this the owner's own.
- `docs/BRIEF.md` — § *What to build* and § *Decisions taken*.

**Acceptance criteria**
- [ ] A decision recorded for each stage: governing idea · foundation spec · slide-by-slide spec ·
      spec review · batched build · preview gate · iteration loop — adopted, rejected, or deferred,
      each with a reason
- [ ] The two-question conflict resolved explicitly, and `docs/BRIEF.md` amended to match whichever
      way it goes
- [ ] The mode list in `docs/BRIEF.md` § *What to build* updated, or explicitly confirmed unchanged
- [ ] Every affected task (T-002, T-003, T-004, T-015) told what changed, by pointer
- [ ] If the pipeline is adopted, build mode's **input contract** is stated — does it consume a
      brief, or a specification?

**Open questions**
- ~~Should this be a hard `blocked_by` on T-002 and T-015 rather than `related`?~~ **Answered
  2026-08-07 by [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md): yes, and on
  T-004 as well.** The deadlock this question feared cannot occur — this task is blocked by nothing,
  so it can always be worked first. The edges now exist, which also means **this task is the head of
  the backlog**: nothing downstream should be specified against an input contract it may change.
- ~~**This task and [T-014](T-014-synthesise-research-into-the-design-system-reference.md)
  overlap.**~~ **Settled by the owner 2026-08-06, before either document was written — the design
  system is standing and shared; the foundation spec is per-deck and references it.** T-014 goes
  first; this task consumes its output.

  Tested against the material, the split is sharper than the hypothesis stated. Under CLAUDE.md
  rule 4 (**one** theme), four of the nine sections — visual system · motion · interaction model ·
  technical stack — have no per-deck variable left; three more — linguistic style · recurring
  elements · layout structures — are standing catalogues a deck **selects from**; the quality bar is
  the standing check plus per-deck additions. Only the **narrative spine** and the governing idea
  are genuinely per-deck.

  **Consequence for this task's scope:** the first in-scope question below is no longer "is the
  foundation spec an artifact with nine authored sections" but "**is the per-deck selection sheet
  surfaced, and what does it carry beyond the narrative spine and the governing idea**". The
  anti-drift rule is fixed either way: **it cites `docs/DESIGN-SYSTEM.md`, it never restates it.**

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Re-read R1 §2, §10, §14 and the A′ rules as one pipeline description rather than as scattered rules | the pipeline, stated once |
| 2 | Decide each stage: adopt / reject / defer, with the reason | stage decisions |
| 3 | Resolve the two-question conflict and reword the brief's promise if needed | amended `docs/BRIEF.md` |
| 4 | Propagate to T-002, T-003, T-004, T-015 by pointer | log rows on each |

## 3. Implement

### 3.1 The pipeline, stated once

Assembled from R1 §2, §10 and §14 rather than left scattered across three notes. Reading right to
left, **two of the four reviews happen before any HTML exists**, and that is the whole shape of it.

```
governing idea (one line)
    └─→ requirements ─→ foundation spec ─→ slide-by-slide spec ─→ REVIEW OF THE SPEC
                                                                        │
                        ┌───────────────────────────────────────────────┘
                        ▼
                  build, in batches ─→ review of the build ─→ OWNER REVIEW ─→ fix
```

> **This diagram is the corpus record, and it is missing a stage — corrected 2026-08-07 while
> [T-015](T-015-plugin-scaffold-and-the-two-question-interface.md) tried to wire it.** There is no
> **outline** node here, although [`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §3.5 makes one
> `hard`: DS-210 says an outline exists before any slide does, and DS-212 says the slide-by-slide
> spec is *expanded from it*. The decided pipeline — outline included, both gates placed — is under
> the gates row in 3.2. Kept as it was, with this note, because the diagram's job is to record what
> R1 §§2/10/14 show; the additions are decisions, and decisions belong in 3.2.

Per-slide, the spec fixes **structure · text · visuals · animations · interactive elements · title ·
bottom line** (R1 §2). That last field is worth naming: the slide-by-slide spec is the first place
the deliverable contract (DS-201 to DS-209) can be satisfied at all, which is the contract
[T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) exists because no deck
here met.

**A correction to this task's own §1, from R4 §9.** §1 says R4 grades *"that whole structure"* as
owner-authored with zero prior art. R4 is narrower and the difference matters. **A4** (specify
slide-by-slide before building) and **A6 / A′4** (review the spec before any HTML) are graded
**`I` — inherited**; the source skill says *"map source to slides"* and *"verify before writing
HTML"*. What has zero prior art is the **specification as a written document** — the governing idea,
the foundation spec, the trace table, the timing budget, plus **A5** (build the spec page by page)
and **A7** (build slides in batches), all `O`.

So the sequence is table stakes and **the artifact is the departure.** That reframes the central
question of this task: not *should there be a specify-then-review step* — there should, and the
source skill agrees — but *should the specification be a document somebody can read.*

### 3.2 The stage decisions

| Stage | Decision | Reason |
| :--- | :--- | :--- |
| **Governing idea** | **Adopt.** One line, written before anything else, carried as the first line of the foundation spec. Not a gate of its own. | `O`, zero prior art, and it costs one sentence. R1 §10's rationale is the argument: *"A deck with six colours is decorated. A deck with one accent used with total discipline is designed."* |
| **Foundation spec** | **Adopt, as a selection sheet — not nine authored sections.** Per-deck content is the governing idea, the narrative spine, the archetypes and elements this deck selects, and any per-deck additions to the quality bar. **It cites [`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md); it never restates it.** | T-014's ruling, already recorded in §1: under CLAUDE.md rule 4 four of the nine sections have no per-deck variable left, and three more are standing catalogues a deck selects from. Only the spine and the governing idea are genuinely per-deck. |
| **Slide-by-slide spec** | **Adopt.** The seven fields from R1 §2, one row per slide. It is the artifact the spec review reads and the input build mode consumes. | It is the only place the pipeline's two cheapest reviews have anything to act on, and the only place a bottom line exists before it is a layout problem. |
| **Spec review** | **Adopt, inside critique mode as a second format — not a mode of its own. And it gets the rubric.** | R1 §14 proves two critique formats and both are critiques; the input type differs, not the job. Splitting them doubles the mode surface for a difference in argument type. See 3.3 for which dimensions it can carry. |
| **Batched build** | **Adopt as the default.** Build a few slides, run the cheap half of the loop, then continue. | `O` (A7), and the mechanism is DS-136: interaction patterns are built once and reused, so **a component defect found in batch one is fixed once instead of in twelve places.** That, not scoring, is what batching buys. |
| **Approval gates** | **Two, and each is independently skippable — see 3.5.** *(a)* **Outline sign-off** on the outline, before it is expanded; *(b)* **detailed-spec sign-off** after the spec review, carrying its *"Open — needs a decision"* items. The fix cycle is not a gate. **Placement corrected 2026-08-07 — see under this table.** | R1 §10's pipeline has exactly one human review; R1 §14 shows the spec review escalating open decisions, which is the second. R1 §15 is explicit that the owner wants to be asked: *"Please ask, argue, do not accept and guess blindly."* |
| **Iteration loop** | **Runs before the owner review, not after.** | See 3.4 — this task's §1 recorded it as unsettled, and it is not. |

**The decided pipeline, with the outline restored and both gates placed.** Settled by the owner
2026-08-07, on a contradiction [T-015](T-015-plugin-scaffold-and-the-two-question-interface.md)
raised: the gates row above originally put outline sign-off *"after the spec review"*, which
`DESIGN-SYSTEM.md` §3.5 contradicts and which **3.4 of this section argues against on its own
terms** — the cut decision is what protects the loop from wasted work, so it has to arrive *before*
the expansion it is meant to save, not after it.

```
governing idea (one line)
    └─→ requirements ─→ foundation spec ─→ outline ─→ OUTLINE SIGN-OFF
                                                            │
                    ┌───────────────────────────────────────┘
                    ▼
        slide-by-slide spec ─→ REVIEW OF THE SPEC ─→ DETAILED-SPEC SIGN-OFF
                                                            │
                    ┌───────────────────────────────────────┘
                    ▼
              build, in batches ─→ review of the build ─→ OWNER REVIEW ─→ fix
```

**The rule, stated so it survives the diagram: each gate immediately follows the artifact it gates,
and immediately precedes the expensive expansion of it.** The accepted cost is that the first gate
signs off an **unreviewed** outline — DS-213 reviews the *specification*, so at outline time there
is nothing yet to review, and an outline is three fields per slide (DS-211), which is cheap to read
and cheap to cut from.

### 3.3 What the spec review can actually score

The question §1 raised — *does the spec review get its own rubric, or is it out of the loop's
scope* — has a sharper answer than either option. **The rubric mostly already works against a
specification**, and the dimensions it reaches are the expensive ones.

| Works against a slide-by-slide spec | Needs a rendered artifact |
| :--- | :--- |
| **S1 Claim** — a headline is a claim or a label on paper | **S3 Encoding** — the chart exists or it does not |
| **S2 Evidence** — a figure has a source or it has none | **S4 Density** — a tier split is a rendered judgement |
| **D1 Spine** — the argument holds or breaks at step two | **S5 Craft** — measured, not specified |
| **D2 Pacing** — slide count and archetype rhythm are spec-level facts | **S6 Motion** — the same |
| **D3 Close** — the closing line is written before it is styled | **D4, visual half** — consistency of look |
| **D4, source-reconciliation half** — figures against sources and against each other | |

**This is the result that changes the cost of the whole pipeline.** Three of the five dimensions no
mechanical check can reach — S1, S2, D1 — are checkable **before any HTML exists**, along with D2,
D3 and half of D4. R1 §14's own findings are the evidence that this is not theoretical: an invented
number in a title supported by no source (S2), a narrative conceit that silently breaks at step two
(D1), and *"missing content rather than error"* — half a stated goal absent, four items counted but
never named (S2, D3). Its closing observation is the one to carry: **"The four Major findings were
all substance, not polish."**

**Consequence for [T-004](T-004-critique-mode-blunt-section-by-section-review.md):** it takes two
input types and reports differently for each — spec review as `ID · Severity · Slide · Finding ·
Fix` with Major/Minor/Note, then *"Open — needs a decision"*, then counts; design audit as headline
verdict, coverage table, findings with the principle violated, then an explicit keep-vs-rebuild
split. R1 §14 gives both formats; neither is invented here.

### 3.4 Where the loop runs — both placement questions

**Per batch or once at the end: both, at different depths — and they are not the same loop.**
[T-026](T-026-settle-who-scores-a-deck-and-whether-the-score-is-shown.md) killed the clean split
§1 hypothesised, because S1, S2 and S4 are scored in one fresh-context read of the whole deck. What
survives for a batch is the auto gate, the render gate, and **S3, S5, S6** — which is not a scoring
round at all. So:

- **Per batch:** auto gate + render gate + S3/S5/S6 on the batch. Cheap, and it catches a component
  defect before the component is reused.
- **Once, on the whole deck:** the measurement round [`EVALUATION.md`](../docs/EVALUATION.md) §6
  defines, including the fresh-context judgement pass.

**The ruling this forces, and `EVALUATION.md` does not currently make it: batch loops must not count
against the iteration cap.** The cap is 3 and it counts whole-deck measurement rounds (§6.4). If a
batch loop counted, a four-batch deck would exhaust the cap **before the deck existed** — the same
arithmetic error §6.2 already corrected once, when a literal reading of *"fix one at a time"* would
have capped a deck that needed 23 fixes.

**Before or after the owner's approval gate: before — and the corpus does settle this, contrary to
§1.** R1 §10's sequence is *build → review of the build → owner review → fix*: the machine review is
second, the human third. `EVALUATION.md` §6.4 already relies on that reading, setting the cap at 3
because R1 gives *"two machine iterations before a human sees it, plus one."*

The objection §1 raised — that running the loop first burns iterations on slides the owner was going
to cut — is real and is answered somewhere else. **The outline gate is what protects the loop from
wasted work**, because a slide is cut at the spec stage, before any HTML exists. That is what the two
pre-HTML reviews are *for*. Buying the same protection by deferring the loop would pay for it with
an owner review of unconverged work, which is the more expensive of the two.

### 3.5 The artifact and the gate are separate decisions — the owner's ruling

**Settled by the owner 2026-08-07, and it splits a pair this task had treated as one.**

- **The specification files are always written.** Not optional, not conditional on the gates, not
  an internal representation. The foundation spec and the slide-by-slide spec exist on disk for
  every run.
- **The gates are optional, and independently so.** Three shapes the user can ask for: **both**
  gates, **one** of the two, or **neither** — deliver the result.

**Why the split is the right one, stated because it resolves the §1 conflict rather than
compromising on it.** The two-question promise is about **what the user must supply and attend
to**. A file written to disk costs the user nothing until they choose to open it; a gate costs
attention. So the promise constrains gates and has nothing to say about artifacts — which is why
the specs can be unconditional and the interruptions cannot.

Two things follow, and both are load-bearing:

1. **The spec review always has something to read.** Its value does not depend on the user
   attending a gate, so a fully skipped run still catches S1, S2, D1, D2, D3 before any HTML
   exists (3.3). **Skipping the gates costs the user's *cut* decision, not the review.**
2. **A skipped run is still inspectable afterwards.** The specs are the trace of what was decided
   and why, available when the deck turns out wrong, which is the moment nobody has the context any
   more.

**Default: both gates on. — assumption, 2026-08-07.** Taken from the owner's phrasing — *"whether
the user asks you to skip the gates"* puts skipping on the user's side of the request, so the
unasked-for state is the gated one. It is also what [`BRIEF.md`](../docs/BRIEF.md)'s *Purpose* row
implies: the plugin encodes **this owner's** conventions, and this owner's process has both reviews.
**One line to change if that reading is wrong.**

### 3.6 Build mode's input contract

**Build mode consumes a reviewed slide-by-slide specification, not a brief.** Two answers plus any
sources produce the requirements; the requirements produce the foundation spec; the foundation spec
and the sources produce the slide-by-slide spec; the spec is reviewed and signed off; build mode
consumes that. This is the acceptance criterion §1 asks for, and it is why
[T-002](T-002-build-mode-the-self-contained-deck-generator.md) is `blocked_by` this task.

**Decisions & assumptions**
- **The specification sequence is inherited; the specification *document* is the departure —
  2026-08-07.** R4 §9 grades A4 and A6 as `I`, not `O`. Recorded because §1 overstated it, and
  because it moves the question this task has to answer.
- **The spec review is a format of critique mode, not a fourth mode — 2026-08-07.** Both formats are
  critiques over different input types; two modes would duplicate the reporting machinery for one
  difference in input.
- **Batch loops are not measurement rounds — 2026-08-07.** Required by the cap arithmetic, and
  `EVALUATION.md` §6.4 has to say so; today it does not.
- **Assumed: the two pre-HTML reviews are worth their cost.** Untested here. The evidence is R1
  §14's finding that the Major defects were substance rather than polish, which is the class a spec
  can carry — but this project has not yet run a spec review of its own.

**Outputs produced**
- This section — the pipeline stated once, seven stage decisions, and the two placement rulings.
- Pending the owner's answer below: amendments to [`BRIEF.md`](../docs/BRIEF.md) *What to build* and
  the *Interface* row, and to [`EVALUATION.md`](../docs/EVALUATION.md) §6.4 for the cap ruling.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A decision per stage — governing idea · foundation spec · slide-by-slide spec · spec review · batched build · preview gate · iteration loop — each with a reason | met | §3.2, seven rows. **All seven adopted, none rejected or deferred** — with two reshaped rather than taken as proposed: the foundation spec is a selection sheet, not nine authored sections (T-014's ruling), and the spec review is a *format* of critique mode, not a mode. |
| The two-question conflict resolved explicitly, and `BRIEF.md` amended | met | §3.5. Questions constrain what the user supplies in advance; gates are artifacts they react to. The owner split it further: **files unconditional, gates optional and independently skippable.** `BRIEF.md`'s *Interface* row carries it. |
| The mode list in `BRIEF.md` § *What to build* updated, or confirmed unchanged | met | Updated. Brief mode absorbed, build mode's input restated as a reviewed specification, critique mode given two formats, and the pipeline diagram added under it. |
| Every affected task told what changed, by pointer | met | Log rows on T-002 (input contract, batching, the specified bottom line), T-004 (two input types, six dimensions, both report formats), T-015 (the two questions survive; it does replace T-003), T-003 (cancelled, with what survives). |
| If the pipeline is adopted, build mode's input contract is stated | met | §3.6 — a **reviewed slide-by-slide specification**, not a brief. |

**Two findings beyond the criteria**

- **The spec review reaches three of the five dimensions no mechanical check can reach**, plus D2,
  D3 and half of D4 — before any HTML exists (§3.3). T-024 measured that five of ten dimensions are
  invisible to every static and measured check, and that result has until now read as *"the pipeline
  cannot end at the gate"*. It also means the opposite and cheaper thing: **most of what the gate
  cannot see does not need a rendered deck to be seen.** Untested here — no spec review has been run
  in this project — and recorded as an assumption in §3, not as a result.
- **`EVALUATION.md` §6.4 needed a ruling it did not have**, and batching is what exposed it: at a cap
  of 3, a four-batch deck counting batch loops would exhaust the cap before the deck existed. Same
  arithmetic error §6.2 had already corrected once for fixes. Amended.

**One assumption the owner should overturn if it is wrong:** gates default to **on** (§3.5). Read
from the owner's phrasing, in which skipping is what the user asks for. One line in `BRIEF.md` and
one in §3.5 if it should be the other way.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-07 | (no change) | **One decision in §3.2 was wrong and is corrected — the outline gate's placement.** It read *"outline sign-off **after the spec review**"*, which contradicts [`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §3.5 — DS-210 puts the outline before any slide, DS-212 expands the slide-by-slide spec *from* it — and contradicts **§3.4 of this task**, which argues the cut decision is what protects the loop from wasted work and therefore has to precede the expansion it saves. Found by [T-015](T-015-plugin-scaffold-and-the-two-question-interface.md), which had to wire the gates and could not wire a contradiction; ruled by the owner the same day. **The rule now stated so it survives the diagram: each gate immediately follows the artifact it gates.** §3.1's diagram was left as the corpus record and annotated — the outline it omits is a `hard` rule but not an R1 observation — and the decided pipeline lives under §3.2's table. `BRIEF.md` § *What to build* carried the same omission and is corrected too. **This is the second thing this task recorded that its own later sections disagreed with**, after §1's provenance claim; both were caught by a downstream task reading it closely rather than by the review here. Generalised as **L-33** in [`LESSONS.md`](../docs/LESSONS.md) — a decision recorded in prose is unchecked until something has to wire it. |
| 2026-08-07 | → done | **The pipeline is adopted whole — all seven stages, none rejected.** Two were reshaped rather than taken as proposed: the foundation spec is a **selection sheet** under one theme, and the spec review is a **format of critique mode**, not a fourth mode. The owner settled the conflict this task existed for by splitting a pair it had treated as one — **specification files unconditional, gates optional and independently skippable** — which leaves the two-question promise intact, because the promise constrains what the user supplies in advance and a file costs nothing until it is opened. Two corrections to this task's own §1: R4 grades A4 and A6 as **inherited**, so the specify-then-review sequence is table stakes and the *document* is the departure; and the corpus **does** settle loop placement — R1 §10 runs the machine review before the owner review, which `EVALUATION.md` §6.4 was already relying on. The finding worth carrying is §3.3: **six of the ten dimensions are checkable against a specification, three of them among the five no check can reach.** Amended `BRIEF.md` (*What to build*, *Interface*) and `EVALUATION.md` §6.4; propagated to T-002, T-004, T-015; cancelled T-003. |
| 2026-08-06 | (no change) | **A constraint on the pipeline, now measured rather than argued.** [T-024](T-024-build-the-reference-deck-and-validate-the-ruleset.md) validated the rubric against a seeded-defect deck and found the split: **five of the ten dimensions are catchable mechanically and five are not.** S1 Claim, S2 Evidence, S4 Density, D1 Spine and D4 Consistency are invisible to any static or measured check, so **the pipeline cannot end at the gate** — a gate-only run ships a deck whose headline is a topic label and whose figures contradict each other. F-13 also reframes the loop's cap: it governs measurement rounds, not fixes. |
| 2026-08-06 | → proposed | Raised when the owner described their authoring process and it matched nothing in the repository — despite R1 having captured it and R4 having graded it owner-authored with zero prior art. The gap is between research and the build plan, not in the research. |
| 2026-08-06 | (no change) | **Sequencing settled by the owner: T-014 first, this task consumes it.** The design system is standing and shared; the foundation spec is per-deck and references it. Testing the hypothesis against R1 §10 sharpened it — under one theme, only the narrative spine and the governing idea are genuinely per-deck, so the foundation spec is a **selection sheet**, not a parallel nine-section document. Scope question 1 re-framed accordingly. Still `proposed`; nothing else in the spec was worked. |
| 2026-08-06 | (no change) | **The owner made the convergence loop this task's centre**, on the grounds that a design system without an effective and efficient pipeline is decoration. [`docs/EVALUATION.md`](../docs/EVALUATION.md) ([T-023](T-023-the-deck-evaluation-rubric-and-convergence-loop.md)) now defines the loop; **this task places it**, and three placement questions were added to scope — per-batch versus end-of-deck, before or after the approval gate, and whether the spec review gets the rubric before any HTML exists. That last one matters most: S1, S2, D1 and D3 all work against a slide-by-slide spec, which would catch those defects at the cheapest possible point — which is what the owner's own pipeline was already doing. |
