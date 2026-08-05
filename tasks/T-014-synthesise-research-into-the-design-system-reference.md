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
areas, with each rule traced to its source in R1–R5 and marked as **hard** (enforced by the build
check), **default** (applied unless overridden) or **guidance** (judgement).

**Why this one**
Five research documents are not a plugin. This is where they become one set of rules, where the
conflicts between the owner's habits and external principle are resolved rather than averaged, and
where the plugin's near-zero-config promise is made good — every rule settled here is a question
the skill never has to ask. Per the brief's carried lesson, this is a reference the skill *points
at* on demand, not text loaded on every run.

**Scope**
- In: writing style and the banned-terminology list · UX and reading behaviour · UI controls and
  navigation · colour · design language · deck structure and pacing · content practice · headings
  and subtitles · illustration · icons · diagrams · layout and grid · external tools and skills.
- In: resolving every conflict surfaced in R1–R5, with the reason recorded.
- Out: the three standing decisions — fonts (T-001), charts (T-006), one style or several (T-007).
  This reference states them once they are decided; it does not pre-empt them.

**Inputs**
- `docs/research/R1-corpus-conventions.md` … `R6-portability-contract.md`
- `docs/BRIEF.md`

**Acceptance criteria**
- [ ] All thirteen coverage areas present, none left as a placeholder
- [ ] Every rule carries a source reference and a hard/default/guidance label
- [ ] Every conflict found in research is resolved explicitly, with the reason
- [ ] Ends with a **re-scoping proposal** for the owner where research contradicts `docs/BRIEF.md` —
      this is an expected outcome, not a planning failure
- [ ] The hard rules are stated in a form a check can actually test
- [ ] Structured for on-demand loading — the skill body must not need to restate it
- [ ] Free of personal, client and machine data

**Open questions**
- Where the owner's habit and external principle disagree and both are defensible, does habit win
  by default? — owner

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
