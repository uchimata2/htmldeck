---
id: T-003
title: Brief mode — elicit the six-section prompt
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: [T-015]
related: [T-002]
work_package: WP3
owner: maintainer
created: 2026-08-04
updated: 2026-08-06
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
| 2026-08-04 | → proposed | Seeded from `docs/BRIEF.md` when the project folder was prepared. |
| 2026-08-06 | (no change) | Owner answered BRIEF open question 6: the plugin **does** receive source documents. Brief mode therefore has to ask for them — they populate the `## Resources` section, which already has the slot. Absence is a legitimate state and must not be treated as a failure. Decision recorded once, in `docs/BRIEF.md`; not restated here. |
