---
id: T-139
title: Three rows in BRIEF.md carry a cell the table cannot render
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-131]
work_package: PH3
owner: the project owner
business_value: medium
effort: xs
created: 2026-08-13
updated: 2026-08-13
deliverables: []
---

# T-139 — Three rows in BRIEF.md carry a cell the table cannot render

## 1. Specify

**Outcome**
Every cell written into a table in the tracked record reaches a reader. Today three do not.

**What was measured**
Scanned 2026-08-13 across all 181 tracked markdown files, skipping fenced blocks: **three rows have
more cells than their header, and all three are in [`../docs/BRIEF.md`](../docs/BRIEF.md)** — the
`T-108` row against a one-column header, and the `T-130` and `T-135` rows against a two-column one.
GitHub-flavoured markdown drops every cell past the header's count, so that content renders nowhere.

All three are the same edit: a task closed, its row gained a *what actually happened* cell, and the
original *what it adds* rationale was pushed right rather than folded in. **The intent was to keep
the original and the outcome side by side**, which the table has no column for. Every other closed
row in the same table folds them into one cell, so the convention already exists and two rows depart
from it.

**Scope**
- In: the three rows, brought to their header's width with nothing lost — fold, or add the column.
- In: deciding which, once, and stating it where the next closure will read it. A third form
  appearing at the next close is the same defect returning.
- Out: any other table. The scan found none.
- Out: a gate. Consider one only if the decision makes a rule a checker could hold; a rule this
  narrow may be worth less than the tool that enforces it.

**Inputs**
- [`../docs/BRIEF.md`](../docs/BRIEF.md) — the *Release phases* tables
- [T-131](T-131-expose-the-trackers-query-commands-so-the-board-is-not-read-whole.md) §3 — where
  this was found, while closing a row in the same table

**Acceptance criteria**
- [ ] No row in any tracked markdown file has more cells than its header
- [ ] The three rows' content survives the fix — nothing is deleted to make a row fit
- [ ] The form a closed row takes is written where the next closure meets it

**Open questions**
- None.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <none yet>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-13 | → proposed | Found while closing [T-131](T-131-expose-the-trackers-query-commands-so-the-board-is-not-read-whole.md), which struck through a row in the same table and had to choose a form. **Not caught by any gate, and no gate is proposed yet**: `refcheck.py` and `taskmd check` both resolve pointers, and a cell nobody can see is not a broken pointer. It was found by counting cells against headers across the whole record rather than by reading the table, which is the only way this class shows itself. `PH3` by the placement rule — an internal document, not a defect in the published plugin. |
