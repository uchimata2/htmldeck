---
id: T-315
title: Make the inline term's underline a theme token, solid in the shipped theme
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-309]
work_package: PH3
owner: the project owner
business_value: low
effort: s
created: 2026-09-14
updated: 2026-09-14
deliverables: []
---

# T-315 — Make the inline term's underline a theme token, solid in the shipped theme

## 1. Specify

**Outcome**
A theme chooses how an inline term's underline is drawn, and `quarto` draws it as a continuous line in
its accent. Today `shell/components.css` hard-codes a dotted underline on `.term-btn`.

**Ruled by the owner** at [`OWED-LOOKS.md`](../docs/OWED-LOOKS.md) row 15, 2026-09-14: a continuous
underline, as a theme option, and the default in this theme.

**Scope**
- In: a theme token for the underline's style, its row in `docs/THEME-CONTRACT.md`, and a value in
  both shipped themes
- Out: the term's colour, which is the accent already

**Acceptance criteria**
- [ ] measured in Chrome: `.term-btn`'s `text-decoration-style` follows the token, and a theme setting
      another legal value changes it
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |

## 3. Implement

**Decisions & assumptions**
- <what was decided>: <why, in one sentence>. <Reversible | Not reversible>. — YYYY-MM-DD

**Outputs produced**
- `deliverables/...`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- <T-NNN or "none">

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-14 | -> proposed | Raised from the owner's look at row 15. `PH3`. Batched into B28 first by the owner's ruling. |
