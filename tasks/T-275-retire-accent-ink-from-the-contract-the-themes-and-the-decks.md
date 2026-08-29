---
id: T-275
title: Retire --accent-ink from the contract, both themes and every deck that carries it
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-242, T-274]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-29
updated: 2026-08-29
deliverables: []
---

# T-275 — Retire `--accent-ink` from the contract, both themes and every deck that carries it

## 1. Specify

**Outcome**
`--accent-ink` is gone. [`THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) types it a colour primitive
— *the accent as text on the ground* — and no surface renders it: `var(--accent-ink)` appears nowhere
in the tree, and no tool reads it by name the way `audit.py` reads `--motion-kind`. Two themes carry
four hand-chosen values for it across light and dark, and every tracked deck carries two, so the
themes' promise that every measured pair clears 4.5:1 is being maintained for a colour nobody sees.

**Closes** `PR-77` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) §3.

**Ruled by the owner, 2026-08-29.** The question was *give it the surface the contract describes, or
retire the row and its four values*, and the owner chose to retire. It was put beside `PR-36`'s Turn
question, which the register asked to have decided at the same time; **the two were answered
differently on purpose** — Turn is a named member of a set a rule publishes, and this is a colour role
nothing publishes.

**Scope**
- In: the `--accent-ink` row in [`THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) §3.2, the four
  declarations in `themes/quarto.css` and `themes/lattice.css`, and the two in each tracked deck's
  own theme region
- In: **all of them in one change.** DS-013 fails a deck declaring a token the contract does not name,
  so removing the row while the declarations stand turns a documentation fix into five red decks
- Out: any other token. `PR-36`'s pair is [T-274](T-274-build-the-card-reveal-so-turns-two-dials-have-a-reader.md)'s
  and is being built rather than retired

**Inputs**
- `PR-77` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) §3
- `theme.validate` — the check that fails an undocumented dial, and the one that will fail a
  documented dial nobody declares
- [`REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) wave 4: the five decks are rebuilt once, in
  **B12**, so this belongs in or after that batch unless a rebuild is paid for twice

**Acceptance criteria**
- [ ] `accent-ink` appears nowhere in the tree — contract, themes, decks
- [ ] `python tools/deck/theme.py check` green on every tracked deck, and `validate` green on both
      themes
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None. The decision is taken; what is left is the order it lands in, which the remediation order
  answers.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <the files this task changed>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- <T-NNN or "none">

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → proposed | Raised after the owner ruled `PR-77` on 2026-08-29, having had it deferred by [T-242](T-242-the-contracts-against-the-checkers-that-decide-them.md) that day. **Retirement was the recommendation and the owner took it.** `PH3`: not a defect in the published plugin. |
