---
id: T-014
title: Synthesise the research into the htmldeck design-system reference
type: analysis
status: proposed
phase: specify
parent: null
blocked_by: [T-009, T-010, T-011, T-012, T-013, T-017]
related: []
work_package: WP1
owner: maintainer
created: 2026-08-06
updated: 2026-08-06
deliverables: [docs/DESIGN-SYSTEM.md]
---

# T-014 — Synthesise the research into the htmldeck design-system reference

## 1. Specify

**Outcome**
One authoritative reference stating every rule htmldeck applies, across all thirteen coverage
areas, with each rule traced to its source in **R1–R6** and marked as **hard** (enforced by the
build check), **default** (applied unless overridden) or **guidance** (judgement).

**Why this one**
Six research documents are not a plugin. This is where they become one set of rules, where the
conflicts between the owner's habits and external principle are resolved rather than averaged, and
where the plugin's near-zero-config promise is made good — every rule settled here is a question
the skill never has to ask. Per the brief's carried lesson, this is a reference the skill *points
at* on demand, not text loaded on every run.

**Scope**
- In: writing style and the banned-terminology list · UX and reading behaviour · UI controls and
  navigation · colour · design language · deck structure and pacing · content practice · headings
  and subtitles · illustration · icons · diagrams · layout and grid · external tools and skills.
- In: resolving every conflict surfaced in R1–R6, with the reason recorded — by the tie-break rule
  answered below, not case by case.
- In: **the four named candidate changes of direction** research produced, each to be adopted or
  overruled deliberately rather than inherited: R2 §12.1 (motion must encode something), R2's
  finding that progressive disclosure is load-bearing, R3 §8's finding that Layered Detail is a
  *modifier on the other archetypes* rather than one of them, and R2 P-01's upgrade of the heading
  check from structural to semantic.
- Out: **non-Latin scripts.** Settled 2026-08-06 — see *Script scope* in `docs/BRIEF.md`. Do not
  write a CJK or RTL rule, and do not leave a placeholder for one.
- Out: the three standing decisions — fonts (T-001), charts (T-006), one style or several (T-007).
  This reference states them once they are decided; it does not pre-empt them.

**Inputs**
- `docs/research/R1-corpus-conventions.md` … `R6-portability-contract.md` — all six.
- `docs/BRIEF.md`, whose *Decisions taken* table now carries the two settled 2026-08-06 (script
  scope, conflict tie-break) and whose open question 6 is answered.
- `docs/research/R1-rules-candidate.md` — the 154 rules with the Verdict column **this task owns**
  (keep / drop / amend). R4 §9 filled the provenance column; the verdict column is still empty.

**Where the highest-value material already sits**, so the synthesis does not start from a blank
page: R1 §13 has the five-category banned-terminology list and the caveat that a word list is
necessary and not sufficient; R1 §14 has the critique format and severity scheme, which R4 §2 shows
has **zero prior art** — it is entirely the owner's; R2 §9 has the accessibility floor as numbers;
R3 §3 and §6 have the 14 archetypes and 12 anti-patterns.

**Acceptance criteria**
- [ ] All thirteen coverage areas present, none left as a placeholder
- [ ] Every rule carries a source reference and a hard/default/guidance label
- [ ] Every conflict found in research is resolved explicitly, with the reason
- [ ] Ends with a **re-scoping proposal** for the owner where research contradicts `docs/BRIEF.md` —
      this is an expected outcome, not a planning failure
- [ ] The hard rules are stated in a form a check can actually test
- [ ] Structured for on-demand loading — the skill body must not need to restate it
- [ ] Free of personal, client and machine data

**Answered 2026-08-06 — split by rule type, and [R2](../docs/research/R2-external-principles.md)'s
evidence grades are what make it operable.**

- **Principle wins on anything measurable** — accessibility, contrast, encoding accuracy,
  legibility. These are R2's **E1** and **E2** material: controlled results and specifications. A
  corpus habit that contradicts one of them loses, and the loss is recorded.
- **Habit wins on aesthetic and structural choices** where the evidence is weak or absent — R2's
  **E3** and **E4** material. This is most of what makes a deck look like this owner's rather than
  generated, and it is the thing the plugin exists to encode.

So the tie-break is not a judgement call per conflict: **look up the grade, then apply the rule.**
A conflict where the external side is E3 or E4 is not a conflict — habit stands.

**Open questions**
- None outstanding. The two that would have blocked this task were settled by the owner on
  2026-08-06: this one, and BRIEF open question 6 (the plugin **does** receive source documents and
  reconciles against them — see `docs/BRIEF.md`).

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Merge R1–R5 into one rule set | draft rule list |
| 2 | Surface and resolve conflicts | resolution table |
| 3 | Label hard / default / guidance | labelled rules |
| 4 | Restructure for on-demand loading | `docs/DESIGN-SYSTEM.md` |

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
| 2026-08-06 | → proposed | Created as the join point between research and build. |
| 2026-08-06 | (no change) | **Unblocked** — all six blockers closed with T-010 and T-011. Spec updated for what landed since it was written: R6 exists (references said R1–R5), the four candidate changes of direction are named in scope, and `R1-rules-candidate.md`'s empty Verdict column is recorded as this task's to fill. Owner settled both blocking decisions the same day — the conflict tie-break (split by rule type) and BRIEF open question 6 (sources are supplied and reconciled). Non-Latin ruled out of scope. **Still `proposed`: the spec has not been worked through, only made current.** |
