---
id: T-139
title: Two rows in BRIEF.md carry a cell the table cannot render
type: fix
status: done
phase: review
shipped_in: unreleased
parent: null
blocked_by: []
related: [T-131]
work_package: PH3
owner: the project owner
business_value: medium
effort: xs
created: 2026-08-13
updated: 2026-08-13
deliverables:
  - docs/BRIEF.md
  - docs/LESSONS.md
---

# T-139 — Two rows in BRIEF.md carry a cell the table cannot render

## 1. Specify

**Outcome**
Every cell written into a table in the tracked record reaches a reader. Today two do not.

**What was measured**
Scanned 2026-08-13 across every tracked markdown file, skipping fenced blocks: **two rows have more
cells than their header, and both are in [`../docs/BRIEF.md`](../docs/BRIEF.md)** — the `T-130` and
`T-135` rows, three cells against a two-column header. GitHub-flavoured markdown drops every cell
past the header's count, so that content renders nowhere.

Both are the same edit: a task closed, its row gained a *what actually happened* cell, and the
original *what it adds* rationale was pushed right rather than folded in. **The intent was to keep
the original and the outcome side by side**, which the table has no column for. Every other closed
row in the same table folds them into one cell, so the convention already exists and two rows depart
from it.

**It was raised as three, and the correction belongs in the specification**
The first scan also named the `T-108` row. That was the instrument, not the record: it treated
`` | | | `` — a legal two-column header whose labels are empty — as a separator row, skipped the real
header, and measured the following rows against the width of the wrong line. **The rule is that a
separator contains a dash**; with that, `T-108`'s row is two cells against a two-column header and
correct. Corrected before any of the work was done, because a fix list built from a mis-tuned
instrument is how a correct row gets edited (**L-86**).

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
| 1 | Re-tune the scan — a separator row contains a dash — and re-run it before touching a row | Two rows, not three |
| 2 | Correct this task's own count, title, filename and [`BRIEF.md`](../docs/BRIEF.md) row, before the fix | A specification that matches the record |
| 3 | Fold each third cell into the second, keeping every word, introduced as *why it was raised, unchanged from when it was open* | Two rows at their header's width |
| 4 | Write the form above the table, where the next closure edits | The ruling, in one place |
| 5 | Re-run the scan across the tracked record | Zero rows over header |

## 3. Implement

**Decisions & assumptions**
- **Fold, do not add a column** — 2026-08-13. Both alternatives keep the content; the column would
  widen a table whose second cell is already a paragraph, and would leave every other closed row in
  it needing an empty third cell. Folding matches the nine closed rows that were already right, so
  the convention is being restored rather than invented.
- **The corrected form is written above the table, not in this task** — 2026-08-13. The next closure
  reads the table, not the record of the task that fixed it, and a ruling nobody meets at the moment
  of editing is a ruling that gets re-decided (**L-13**).
- **No gate is proposed** — 2026-08-13. A cell past the header is not a broken pointer, so neither
  `refcheck.py` nor `taskmd check` can be extended into it without becoming a markdown renderer. The
  scan that found it is twenty lines and lives in the session that needed it; a tracked tool for two
  rows across 182 files would cost more than the fault does, and `check_all.py` would then owe it a
  manifest entry forever. Reconsider if it recurs after the ruling above.
- **The count was wrong when the task was raised, and the specification was corrected before the
  fix** — 2026-08-13. Three, not two, because the scan read `` | | | `` as a separator. Kept as
  **L-86**, and the title, filename and `BRIEF.md` row were all corrected: a wrong number that
  reaches three homes outlives the session that made it.

**Outputs produced**
- [`../docs/BRIEF.md`](../docs/BRIEF.md) — the two rows folded, and the form stated above the table
- [`../docs/LESSONS.md`](../docs/LESSONS.md) — **L-86**

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| No row in any tracked markdown file has more cells than its header | met | **0 rows over header across 182 tracked markdown files**, from two — and the scan was re-tuned first, which is what turned three into two |
| The three rows' content survives the fix — nothing is deleted to make a row fit | met, and the criterion itself was wrong | **Two rows, not three.** Both third cells were folded into the second whole, introduced as *why it was raised, unchanged from when it was open*; nothing was cut. The `T-108` row named in §1 was never defective |
| The form a closed row takes is written where the next closure meets it | met | Above the PH3 table in `BRIEF.md`: strike the title, add **done `<date>`**, what happened first, the original rationale after it, **two cells** — with the reason a third renders nowhere |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-13 | → done | Zero rows over header across 182 tracked files, from two. **The first thing this task did was correct itself**: the scan that raised it read `\| \| \|` — a two-column header with empty labels — as a separator, so the `T-108` row was measured against the wrong width and named as a defect it never had. Title, filename, `BRIEF.md` row and this specification were all corrected before a single row was edited, because a fix list from a mis-tuned instrument is how a correct row gets changed. **L-86.** No gate is proposed and the reason is written down: a cell past the header is not a broken pointer, and a tracked tool for two rows would outlive the fault. |
| 2026-08-13 | → in_progress | Fold rather than widen. Nine closed rows in the same table were already right, so this restores a convention instead of inventing one. |
| 2026-08-13 | → planned | Five steps, and the first two are *fix the instrument* and *fix this task's own numbers*. Neither was in the original scope. |
| 2026-08-13 | → specified | Raised and specified in one sitting during T-131's close, with the deliverables left empty on purpose — which of `BRIEF.md`'s two forms wins was the work, not an input to it. |
| 2026-08-13 | → proposed | Found while closing [T-131](T-131-expose-the-trackers-query-commands-so-the-board-is-not-read-whole.md), which struck through a row in the same table and had to choose a form. **Not caught by any gate, and no gate is proposed yet**: `refcheck.py` and `taskmd check` both resolve pointers, and a cell nobody can see is not a broken pointer. It was found by counting cells against headers across the whole record rather than by reading the table, which is the only way this class shows itself. `PH3` by the placement rule — an internal document, not a defect in the published plugin. |
