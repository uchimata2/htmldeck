---
id: T-003
title: Brief mode — elicit the six-section prompt
type: deliverable
status: cancelled
phase: specify
parent: null
blocked_by: [T-015]
related: [T-002, T-020]
work_package: WP3
shipped_in: 0.1.0
owner: maintainer
created: 2026-08-04
updated: 2026-08-12
deliverables: []
---

# T-003 — Brief mode — elicit the six-section prompt

## 1. Specify

**Outcome**
A mode that turns whatever the user has into a Role / Context / Goal / Requirements / Format / Resources brief.

**Why this one**
The structure is taken from a real prompt in the corpus that produced one of the better decks — see `reference/example-prompt.md`. Two of its defaults are worth keeping verbatim: keep the text short but the message strong, and avoid the terminology that marks text as machine-written.

**Acceptance criteria**
- [ ] Produces all six sections from an underspecified request
- [ ] Format defaults match the corpus: single-file, 6–9 pages, respectful and professional
- [ ] The banned-terminology list ships, is configurable, and is applied at build time rather than hoped for

**Open questions**
- Should the brief be a file in the project, or ephemeral?

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |

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
| 2026-08-07 | → cancelled | **Absorbed into the pipeline by [T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md), on the owner's ruling.** The six-section structure is not dropped — it survives as the **internal shape of the requirements** the skill assembles from the two answers plus any supplied sources, feeding the foundation spec. What is cancelled is the *mode*: a separate elicitation dialogue is a third way in, against a near-zero-config promise, and the pipeline already has a requirements stage to carry it. The two defaults this task existed to keep verbatim survive with it — *keep it short in text but send a strong message*, and the banned-terminology list shipped and applied at build time, which is [T-005](T-005-build-check-the-gate-the-deck-must-pass.md)'s to enforce. Its own open question — file or ephemeral — is answered by T-020 §3.5: **the specification files are always written.** |
| 2026-08-07 | (no change) | `related` gains [T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md), added by [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md). **This mode's continued existence is an open question** — [T-015](T-015-plugin-scaffold-and-the-two-question-interface.md) §1 asks whether the scaffold replaces it or whether the six-section brief becomes an internal structure filled in silently from the two answers, and T-020's pipeline decision is what settles it. No `blocked_by`: the gate reaches here transitively through T-015, and a second edge would only duplicate it. |
| 2026-08-04 | → proposed | Seeded from `docs/BRIEF.md` when the project folder was prepared. |
| 2026-08-06 | (no change) | Owner answered BRIEF open question 6: the plugin **does** receive source documents. Brief mode therefore has to ask for them — they populate the `## Resources` section, which already has the slot. Absence is a legitimate state and must not be treated as a failure. Decision recorded once, in `docs/BRIEF.md`; not restated here. |
