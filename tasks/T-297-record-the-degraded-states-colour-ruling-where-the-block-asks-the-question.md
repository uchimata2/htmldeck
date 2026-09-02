---
id: T-297
title: Record the degraded state's colour ruling in the block that asks the question
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-253]
work_package: PH3
owner: the project owner
business_value: low
effort: s
created: 2026-09-03
updated: 2026-09-03
shipped_in: 0.7.0
deliverables:
  - shell/components.css
  - examples/reference-deck.html
  - examples/sort-window/sort-window.html
  - examples/measure-first/measure-first.html
  - examples/portfolio-review/portfolio-review.html
---

# T-297 — Record the degraded state's colour ruling in the block that asks the question

## 1. Specify

**Outcome**

[`../shell/components.css`](../shell/components.css)'s DS-009 comment stops calling the degraded
state's palette *a question for an eye* and states the answer instead, and every deck that embeds the
shared component block carries the corrected text. The ruling exists — owed look 12, taken
2026-09-03 — and this file was the only place left that disagreed with it.

**Scope**

- In: the closing sentence of the DS-009 comment in `shell/components.css`, and the re-sync of every
  deck that embeds the shared component block.
- Out: **the four literals themselves.** The ruling was to keep them. A task that changes a colour
  here is a different task and would need its own look.
- Out: `PR-79`'s register row, which closed 2026-09-02 and is not reopened by this.

**Inputs**

- [`../docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md) row 12 — the ruling and its wording.
- [`../shell/components.css`](../shell/components.css) — the comment, at the end of the DS-009 block.

**Acceptance criteria**

- [x] The comment states the ruling, its date, and that it holds for **every** theme rather than for
      `lattice` — so a template the rule 4 generator produces does not read as reopening it.
- [x] The comment still carries the reason the values must be literal, which the ruling does not touch.
- [x] `python tools/deck/shell.py check <deck>` passes for all four decks in `check_all.py`'s `DECKS`.
- [x] `python tools/check_all.py` and `python tools/tasks/lint.py` both green, run separately.

**Open questions**

- ~~none. The decision this task records was the only one, and the owner took it.~~ Still none at
  close; nothing in the work raised one.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Replace the closing sentence of the DS-009 comment with the ruling | `shell/components.css` |
| 2 | `python tools/deck/shell.py sync <deck> --write` for each deck in `DECKS` | four decks re-synced |
| 3 | Regenerate the seeded-defects fixture, which is derived from the reference deck | `examples/reference-deck-seeded-defects.html` |
| 4 | Both gates, separately, then commit | a green tree |

## 3. Implement

**Decisions & assumptions**

- **The ruling is written as binding on the block, not on `lattice`** — 2026-09-03. The look was
  taken on a pair, so the tempting sentence is *it reads fine beside `lattice` too*. That wording
  would be reopened by the next theme, and rule 4's generator exists to produce more of them. The
  comment says the answer holds for every theme and that a colour change here needs its own look.
- **Step 3 of the closing checklist is met by proof rather than by a look** — 2026-09-03. The
  checklist asks that anything the task produced that renders has been opened offline. Nothing
  produced here renders: every changed line in all five deck files is prose inside a `/* … */`
  comment, with no selector, declaration or brace touched. Measured over `git diff -U0` on each of
  the five files — 11 changed lines each, 0 of them carrying `{`, `}`, `/*`, `*/`, or a
  `property: value;` pair. A look would have been a look at an unchanged rendering, and saying so is
  more honest than recording one.
- **Six figures moved and were corrected in the same change** — 2026-09-03. The comment grew by 468
  bytes, so every deck grew by 468 bytes, and `figures.py` binds each deck's KB claim to the document
  that states it. It failed the run, which is the binding working. `README.md` (two), `examples/README.md`
  (four) and `docs/BRIEF.md` (one) now state 318, 317, 428 and 317 KB.

**Outputs produced**

- `shell/components.css` — the DS-009 comment's closing paragraph.
- The four decks in `DECKS`, re-synced with `shell.py sync --write`, and
  `examples/reference-deck-seeded-defects.html`, regenerated with `seed_defects.py` because it is
  derived from the reference deck.
- `README.md`, `examples/README.md` and `docs/BRIEF.md` — seven stale size figures, consequential
  rather than intended.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The comment states the ruling, its date, and that it holds for every theme | pass | Names the pair that was read, and says a colour change here needs its own look |
| The comment keeps the reason the values must be literal | pass | That paragraph is untouched; only the closing sentence was replaced |
| `shell.py check <deck>` passes for all four decks | pass | Run inside `check_all.py`, per deck |
| Both gates green, run separately | pass | `lint.py` all 5 passed; `check_all.py` 42 ran, 2 skipped with a reason, 0 failed, 225 s |

**Child fix tasks raised**

- none.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-03 | → proposed | Created, from owed look 12's ruling. The comment is the one place that still poses a settled question. |
| 2026-09-03 | → done | **Closed the same day, and the cost was not the comment.** The edit is one paragraph; the work is that `components.css` is the shared block, so five deck files change and seven size figures in three documents go stale with them. `figures.py` caught every one and named it — the binding `PR-04` asked for, working on a change nobody made for it. **Nothing renders differently** and this is proved rather than looked at: all 55 changed lines across the five decks are comment prose, none carrying a selector, a declaration or a brace. |
