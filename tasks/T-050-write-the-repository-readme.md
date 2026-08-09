---
id: T-050
title: Write the repository README — what exists, what does not, and how to run it
type: deliverable
status: proposed
phase: specify
parent: T-042
blocked_by: []
related: [T-008, T-015, T-005, T-024]
work_package: final
owner: the project owner
created: 2026-08-09
updated: 2026-08-09
deliverables:
  - README.md
---

# T-050 — Write the repository README — what exists, what does not, and how to run it

## 1. Specify

**Outcome**
`README.md` at the repository root: what htmldeck is, what a visitor can run today, what it produces,
and — stated rather than implied — which of the three modes do not exist yet.

**Why this one, and why not inside T-008**
The repository has **no `README.md`**, and `CLAUDE.md` says in its first section that it goes to
GitHub. Every other document assumes a reader who already knows what the project is: `CLAUDE.md`
opens with *"Read this before doing anything in this folder"*, `BRIEF.md` opens by pointing back at
`CLAUDE.md`, and `examples/README.md` describes two decks without saying what built them.

[T-008](T-008-package-document-and-publish.md) owns *"an installable plugin with an honest README"*
and is `blocked_by` **T-002** (build mode) and **T-004** (critique mode). **A README depends on
neither.** It describes what exists — the ruleset, the gate, the reference deck, the pipeline
scaffold — and an honest one says the two modes are unbuilt, which is a sentence, not a blocker.
Splitting it out also matches how T-008 is written: its remaining criteria are about *installing and
publishing*, and the README is the only one of them that is true today.

**The honesty constraint is the whole design.** This project's own **L-05** — *say which half you
checked* — applies to its front door. A README describing a three-mode plugin would be describing
the plan; what ships today is a ruleset, an evaluator, a build check, a reference deck and a skill
that stands up the pipeline by hand.

**Scope**
- In: what htmldeck is, in a paragraph a stranger understands.
- In: what runs today, with the commands, and what each proves.
- In: what does not exist yet, named, not softened — build mode
  ([T-002](T-002-build-mode-the-self-contained-deck-generator.md)) and critique mode
  ([T-004](T-004-critique-mode-blunt-section-by-section-review.md)).
- In: the reference deck as the argument for the project, with the one measurement that carries it
  — one file, zero external references, opens offline.
- In: where to go next, per audience: a user (`skills/htmldeck/SKILL.md`), someone judging the
  design position (`docs/DESIGN-SYSTEM.md`), someone continuing the work (`CLAUDE.md`, `tasks/`).
- In: the licence, and the font licences that travel with the embedded faces (DS-032).
- Out: install instructions and the marketplace entry —
  [T-008](T-008-package-document-and-publish.md)'s, and they are not true until it lands.
- Out: restating the ruleset, the rationale or the brief. **Point, do not paraphrase** (**L-13**);
  a second copy of the design system in the README is a second copy to maintain.
- Out: screenshots. Raster images are banned in decks by DS-110 and a README screenshot of a deck
  goes stale the way `examples/README.md` just did.

**Inputs**
- [`CLAUDE.md`](../CLAUDE.md) — what this is and the rules that survive
- [`docs/BRIEF.md`](../docs/BRIEF.md) — the definition of done, for the *what does not exist* section
- [`examples/README.md`](../examples/README.md) — the deck's measurements, after
  [T-044](T-044-restore-the-seeded-defect-fixture-and-its-claims.md) re-takes them
- [T-042](T-042-audit-the-whole-repository-against-itself.md) §2, F-12

**Acceptance criteria**
- [ ] `README.md` exists at the root and is the first thing a GitHub visitor sees
- [ ] Every command it lists was **run from a clean clone** in the session that wrote it, and its
      real output is what the README quotes
- [ ] The unbuilt modes are named in the README's own voice, not left to be inferred from `tasks/`
- [ ] Every figure it states is cited from the document that owns it, none re-typed
- [ ] Read by someone who has not seen the repository, and the question *"what is this and what can
      I do with it?"* is answered above the fold
- [ ] No personal, client or machine data — `CLAUDE.md`'s publishing constraint
- [ ] `python tools/tasks/task.py check` passes with the new document's pointers included

**Open questions**
- ~~Does the README belong to T-008 or to its own task?~~ **Answered 2026-08-09: its own task, now.**
  T-008's blockers are two *modes*; a README depends on neither, and the repository is already
  public without one. T-008 keeps install, the marketplace entry and the publish itself, and gains
  `related: T-050`.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

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
| 2026-08-09 | → proposed | Raised by [T-042](T-042-audit-the-whole-repository-against-itself.md), finding F-12. **A repository stated to be published, with no `README.md`** — every document in it opens by addressing a reader who already knows what the project is. Split out of [T-008](T-008-package-document-and-publish.md) rather than left there because T-008 is gated on build mode and critique mode and **a README depends on neither**; an honest one names them as unbuilt, which is a sentence rather than a blocker. Best written after [T-044](T-044-restore-the-seeded-defect-fixture-and-its-claims.md) re-measures the deck, so the two front doors state the same numbers. |
