---
id: T-315
title: Make the inline term's underline a theme token, solid in the shipped theme
type: deliverable
status: done
phase: review
parent: null
blocked_by: []
related: [T-309]
work_package: PH3
shipped_in: unreleased
owner: the project owner
business_value: low
effort: s
created: 2026-09-14
updated: 2026-09-14
deliverables: [shell/components.css, themes/quarto.css, themes/lattice.css, docs/THEME-CONTRACT.md, tools/deck/theme.py]
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
- [x] measured in Chrome: `.term-btn`'s `text-decoration-style` follows the token, and a theme setting
      another legal value changes it
- [x] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Measure the underline before the change | §3 |
| 2 | Add the token to the contract, both themes and the shell, and teach `theme.py` a list of words | `docs/THEME-CONTRACT.md`, `themes/`, `shell/components.css`, `tools/deck/theme.py` |
| 3 | Sync, measure, record the look, lint, gate | §3 |

## 3. Implement

**Decisions & assumptions**
- `--term-line` is a `shape` token whose Legal cell is `solid, dotted, dashed`, and both shipped themes
  declare `solid`. `lattice` takes the same default: the owner's preference is the continuous line,
  and a theme that wants another word now has a legal place to write it. Reversible. — 2026-09-14
- The token is `optional`, and the shell reads `var(--term-line, solid)`. `shell.py sync` does not
  rewrite a deck's theme region, so every deck built before this, the four tracked ones included,
  would otherwise fail DS-013 for a token it never had. Reversible. — 2026-09-14
- The Legal form is a comma-separated list, and `theme.py` learned it: a declared value outside the
  list fails, and the self-test proves it both ways. Commas, not pipes, because the contract is a
  Markdown table and a pipe splits the cell when it renders. Reversible. — 2026-09-14

On a copy of the reference deck with one inline term, in headless Chrome:

| Case | `text-decoration-style` | Colour |
| :--- | :--- | :--- |
| before, as shipped | `dotted` | the accent, `#5A4B8F` |
| before, `--term-line: dotted` set on `:root` | `dotted`, the token read by nothing | the accent |
| after, as shipped, the deck's theme region carrying no `--term-line` | `solid`, the shell's default | the accent |
| after, `--term-line: dotted` set on `:root` | `dotted` | the accent |

`theme.py validate` passes both themes, and `theme.py check` on the reference deck reports DS-013
`132 token(s) required, 4 optional, 0 problem(s)`.

§1.14 after the shell edit: four decks synced, the fixture regenerated, `density.py check` `0 wrong`
on each, and the byte figures corrected.

**The look is owed**: [`../docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md) row 21.

**Outputs produced**
- `shell/components.css`: `.term-btn` reads the token
- `themes/quarto.css` and `themes/lattice.css`: `--term-line:solid`
- `docs/THEME-CONTRACT.md`: the `--term-line` row
- `tools/deck/theme.py`: the list-of-words Legal form, and its self-test

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| the underline's style follows the token, and another legal value changes it | **pass**, look owed | §3's table. The look is `OWED-LOOKS.md` row 21 |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | **pass** | Lint, then the full gate on the finished tree |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-14 | -> done | `--term-line` is an optional theme token, `solid` in both themes and the shell's default, and `theme.py` validates its list of words. The look is owed as `OWED-LOOKS.md` row 21. |
| 2026-09-14 | -> proposed | Raised from the owner's look at row 15. `PH3`. Batched into B28 first by the owner's ruling. |
