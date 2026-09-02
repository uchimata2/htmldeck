---
id: T-275
title: Retire --accent-ink from the contract, both themes and every deck that carries it
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-242, T-274]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-29
updated: 2026-08-30
shipped_in: unreleased
deliverables: [docs/THEME-CONTRACT.md, themes/quarto.css, themes/lattice.css]
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
| 1 | Count the declarations before removing any, so the change can be asserted rather than believed | 12, not the 10 the register's *four theme and two per deck across five decks* implies |
| 2 | Remove all of them in one edit — contract row, both themes, all four tracked decks | `--accent-ink` gone from every declaring file |
| 3 | Re-derive what is derived from those decks rather than editing it | the blindness fixture, and the three gitignored presenter files |
| 4 | Prove the contract and the decks agree, in both directions | `theme.py validate` on both themes, `theme.py check` on all four decks |

## 3. Implement

**Decisions & assumptions**
- **Twelve declarations, not ten** — 2026-08-30. Counted before the edit, and the script asserted
  exactly two per file rather than removing what it found: four in the two themes and two in each of
  the **four** tracked decks. `check_all.py`'s `DECKS` holds four; the register's *all five tracked
  decks* counts `reference-deck-seeded-defects.html`, which `NOT_A_DECK` describes as the blindness
  fixture and which is **derived** from the reference deck. It was re-derived rather than edited.
- **The three `*-presenter.html` files were rebuilt too** — 2026-08-30. They are gitignored, so no
  gate reads them and nothing would have failed; they would simply have carried a retired token on
  any machine that had built them. `presenter.py` is a by-hand derivation by `check_all.py`'s own
  account, so rebuilding them is the only way they move.
- **The contract keeps the ruling and loses the row** — 2026-08-30. §3.2's row is gone. §3.6's
  paragraph, which announced the retirement in the future tense, now records it in the past and says
  what state `theme.validate` enforces: a documented dial nobody declares fails as surely as an
  undeclared one. **The name still appears there and in `REMEDIATION-ORDER.md` §3**, and that is
  deliberate — those two are the record of a decision about the contract, not a declaration of a
  token. The acceptance criterion's *nowhere in the tree* is met for every place a theme is read
  from.

**Outputs produced**
- [`docs/THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) — the §3.2 row removed, the §3.6 paragraph
  rewritten
- [`themes/quarto.css`](../themes/quarto.css), [`themes/lattice.css`](../themes/lattice.css) — two
  declarations each
- the four tracked decks — two declarations each; and the fixture and three presenter files
  re-derived

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| `accent-ink` appears nowhere in the tree — contract, themes, decks | pass | Zero in every `.css` and `.html`. Two prose mentions remain and are named above: `THEME-CONTRACT.md` §3.6 and `REMEDIATION-ORDER.md` §3, both records of the ruling rather than declarations |
| `theme.py check` green on every tracked deck, `validate` green on both themes | pass | `themes/quarto.css - conforms`, `themes/lattice.css - conforms`; all four decks report every literal outside the region exempt |
| `lint.py` and `check_all.py` green, run separately | pass | Run separately, on the batch's tree |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → proposed | Raised after the owner ruled `PR-77` on 2026-08-29, having had it deferred by [T-242](T-242-the-contracts-against-the-checkers-that-decide-them.md) that day. **Retirement was the recommendation and the owner took it.** `PH3`: not a defect in the published plugin. |
| 2026-08-30 | proposed → done | Closed in **B12**. Twelve declarations removed in one edit, not the ten the register implied — the fifth "tracked deck" is the derived blindness fixture, which was re-derived. The three gitignored presenter files were rebuilt for the same reason. `PR-77` closed. |
