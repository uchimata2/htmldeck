---
id: T-050
title: Write the repository README — what exists, what does not, and how to run it
type: deliverable
status: done
phase: review
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
| 1 | **Clone the repository to a clean directory** and run every candidate command there | Real output, from a state a visitor can reproduce — not from the working tree |
| 2 | Write the page around what those runs actually printed | Five commands, five quoted outputs, none re-typed |
| 3 | Name the two unbuilt modes, and the two failing rules, in the README's own voice | *What does not exist yet*, with task links |
| 4 | Point at every document rather than paraphrasing it (**L-13**) | A table per audience, and no second copy of the ruleset |
| 5 | Re-clone **with the README in it** and re-run, because the page's own pointers move the count it quotes | The one figure the first pass got wrong, corrected from a second run |
| 6 | Licence, font licences, and the illustrative-city notice | The three things a visitor may not redistribute without |

## 3. Implement

**Decisions & assumptions**
- **Every quoted output came from a clean clone, not from the working tree.** The difference is not
  cosmetic: the working tree carries `.assets-cache/` and `deliverables/_working/`, and a clone
  carries neither — which is how F-18 was found in the first place. The clone run reproduced it
  exactly, printing `note: deliverables\_working does not exist, so the leftover-file check had
  nothing to run against`, and that is the correct behaviour after
  [T-046](T-046-extend-task-py-to-what-it-cannot-see.md). — 2026-08-09
- **The page had to be cloned twice.** Its first version quoted `732 document pointer(s)` — true
  when measured, and false the moment the README's own twenty-seven pointers joined the repository.
  A front door that quotes a count its own existence changes is the audit's recurring defect in
  miniature, so the figure was re-measured from a clone that contained the page: **759**. — 2026-08-09
- **The two failing `hard` rules are named on the front page.** They were found hours earlier by
  [T-048](T-048-gate-the-hard-rules-only-judgement-can-reach.md) and it would have been easy to
  leave them to `tasks/`. The mechanical gate is green and says so; a README that quoted only the
  green half would be the exact claim **L-05** is about. — 2026-08-09
- **No screenshots**, per scope — and the reason held up: `examples/README.md` had just gone stale in
  six places, and an image is the one thing no check in this repository can re-measure. — 2026-08-09

**Outputs produced**
- [`README.md`](../README.md) — 27 pointers, all resolving; five commands, all run from a clean clone

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| `README.md` exists at the root and is the first thing a GitHub visitor sees | **met** | Root of the repository. The first two paragraphs say what it is and that build mode is not built |
| Every command **run from a clean clone** in this session, and its real output quoted | **met** | Cloned twice — `git clone` to a temporary directory, five commands, output pasted from those runs. The clone reproduced F-18's symptom exactly, which is the check that the clone was really clean |
| The unbuilt modes named in the README's own voice, not inferred from `tasks/` | **met** | *"Build mode does not exist. Nothing in this repository writes a deck."* — plus critique mode, plus the two `hard` rules currently failing the deck |
| Every figure cited from the document that owns it, none re-typed | **met** | 214 KB, 160/161, 111/78/33, 114/85/25/4, 52 tasks, 759 pointers, 10 of 10 fixtures — every one pasted from a run, and the pointer count re-measured after the README changed it |
| Read cold: *"what is this and what can I do with it?"* answered above the fold | **met, with the limit stated** | The first screen answers both — one sentence on what a deck is, one on what the repository holds, one naming what is missing. **This was read cold by its author, which is not the same as by a stranger**; the criterion asked for a reader who has not seen the repository and no such reader was available. Recorded as a limit rather than claimed as satisfied |
| No personal, client or machine data | **met** | No paths outside the repository, no names, no hostnames. The clone was made under a temporary directory and no part of that path appears on the page |
| `python tools/tasks/task.py check` passes with the new document's pointers included | **met** | `OK - 52 tasks, … 759 document pointer(s) checked, 0 broken` — up 27 from 732, which is the README's own pointers being checked |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-09 | → done | **Written from a clean clone, and the clone earned its place twice.** Running the commands there rather than in the working tree reproduced F-18's symptom — `deliverables/_working` absent, because git carries no empty directory — which is both the check that the clone was genuinely clean and confirmation that [T-046](T-046-extend-task-py-to-what-it-cannot-see.md)'s fix behaves correctly for the reader the check is about. **Then the page had to be cloned a second time**, because its first version quoted `732 document pointer(s)`, true when measured and false the moment the README's own twenty-seven pointers existed. A front door quoting a count its own existence changes is this audit's recurring defect in miniature, and it was worth catching on the one document nobody would re-check. **The honesty constraint drove the structure rather than decorating it.** The gate's output is quoted *with* its 33 unchecked rules rather than as `0 failure(s)`; the two `hard` rules failing the deck as of this morning are on the front page, hours after [T-048](T-048-gate-the-hard-rules-only-judgement-can-reach.md) found them; and the seeded-defect fixture is described by what it **misses** — seven of ten dimensions — because that is the argument for the judgement pass existing. One criterion is recorded as met **with its limit stated**: the page was read cold by its author, and the criterion asked for a stranger. |
| 2026-08-09 | → planned | §1 accepted as written, with its open question already answered — the README is its own task because [T-008](T-008-package-document-and-publish.md)'s blockers are two *modes* and a README depends on neither. Six steps, and step 1 is the clone: writing the page first and verifying afterwards is how a README ends up describing the plan. |
| 2026-08-09 | → proposed | Raised by [T-042](T-042-audit-the-whole-repository-against-itself.md), finding F-12. **A repository stated to be published, with no `README.md`** — every document in it opens by addressing a reader who already knows what the project is. Split out of [T-008](T-008-package-document-and-publish.md) rather than left there because T-008 is gated on build mode and critique mode and **a README depends on neither**; an honest one names them as unbuilt, which is a sentence rather than a blocker. Best written after [T-044](T-044-restore-the-seeded-defect-fixture-and-its-claims.md) re-measures the deck, so the two front doors state the same numbers. |
