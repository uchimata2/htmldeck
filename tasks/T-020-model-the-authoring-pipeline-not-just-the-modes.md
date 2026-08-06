---
id: T-020
title: Model the authoring pipeline, not just the three modes
type: decision
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-002, T-003, T-004, T-014, T-015, T-023]
work_package: WP1
owner: maintainer
created: 2026-08-06
updated: 2026-08-06
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
- Should this be a hard `blocked_by` on T-002 and T-015 rather than `related`? It is left as
  `related` so it does not silently deadlock the backlog, but building build mode before this is
  settled risks building it against the wrong input contract. — owner
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
| 2026-08-06 | (no change) | **A constraint on the pipeline, now measured rather than argued.** [T-024](T-024-build-the-reference-deck-and-validate-the-ruleset.md) validated the rubric against a seeded-defect deck and found the split: **five of the ten dimensions are catchable mechanically and five are not.** S1 Claim, S2 Evidence, S4 Density, D1 Spine and D4 Consistency are invisible to any static or measured check, so **the pipeline cannot end at the gate** — a gate-only run ships a deck whose headline is a topic label and whose figures contradict each other. F-13 also reframes the loop's cap: it governs measurement rounds, not fixes. |
| 2026-08-06 | → proposed | Raised when the owner described their authoring process and it matched nothing in the repository — despite R1 having captured it and R4 having graded it owner-authored with zero prior art. The gap is between research and the build plan, not in the research. |
| 2026-08-06 | (no change) | **Sequencing settled by the owner: T-014 first, this task consumes it.** The design system is standing and shared; the foundation spec is per-deck and references it. Testing the hypothesis against R1 §10 sharpened it — under one theme, only the narrative spine and the governing idea are genuinely per-deck, so the foundation spec is a **selection sheet**, not a parallel nine-section document. Scope question 1 re-framed accordingly. Still `proposed`; nothing else in the spec was worked. |
| 2026-08-06 | (no change) | **The owner made the convergence loop this task's centre**, on the grounds that a design system without an effective and efficient pipeline is decoration. [`docs/EVALUATION.md`](../docs/EVALUATION.md) ([T-023](T-023-the-deck-evaluation-rubric-and-convergence-loop.md)) now defines the loop; **this task places it**, and three placement questions were added to scope — per-batch versus end-of-deck, before or after the approval gate, and whether the spec review gets the rubric before any HTML exists. That last one matters most: S1, S2, D1 and D3 all work against a slide-by-slide spec, which would catch those defects at the cheapest possible point — which is what the owner's own pipeline was already doing. |
