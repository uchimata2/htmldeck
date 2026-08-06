---
id: T-020
title: Model the authoring pipeline, not just the three modes
type: decision
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-002, T-003, T-004, T-014, T-015]
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
| 2026-08-06 | → proposed | Raised when the owner described their authoring process and it matched nothing in the repository — despite R1 having captured it and R4 having graded it owner-authored with zero prior art. The gap is between research and the build plan, not in the research. |
