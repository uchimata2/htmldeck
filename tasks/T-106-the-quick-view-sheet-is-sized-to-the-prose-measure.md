---
id: T-106
title: The quick-view sheet is sized to the prose measure, so a source's tables are crushed
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-070, T-109, T-110]
work_package: PH1
owner: the project owner
business_value: high
effort: xs
created: 2026-08-12
updated: 2026-08-12
deliverables:
  - shell/components.css
  - docs/THEME-CONTRACT.md
---

# T-106 — The quick-view sheet is sized to the prose measure, so a source's tables are crushed

## 1. Specify

**Outcome**
The quick-view overlay is sized for what it actually holds. Today it is sized for prose, and a
source document that carries a wide table is squeezed into a reading column while the full height of
the viewport sits unused beside it.

**The mechanism, measured**
[`shell/components.css`](../shell/components.css) `.qv-sheet`:

```
width:min(var(--doc-measure), 100%);max-height:100%;
```

`--doc-measure` is the **reading measure** — the token that decides how wide a line of body text may
run before it stops being comfortable. It was reused here for a surface whose job is different. A
prose measure is an upper bound chosen so lines stay short; a quoted source is not lines of prose,
it is headings, tables, fences and lists, and the same bound turns a seven-column value table into a
column of wrapped fragments.

Both properties are wrong in the same direction and for the same reason. `max-height:100%` lets the
sheet use every pixel of height; `width` refuses to use the width. The result is a tall, narrow
window — reported from the first real deck built on the published plugin as *"kinda awkward to
compress that big letters into such a narrow window"*.

**One token doing two jobs is the defect.** The fix is a token of its own, not a different number in
the same place: the reading view legitimately wants a prose measure, and it must keep it.

**Scope**
- In: a `--qv-measure` token in [`THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md), defaulted wide
  enough for a source document's tables and bounded so the sheet never becomes edge-to-edge.
- In: `.qv-sheet` reading the new token.
- In: the reading view (`.doc`) keeps `--doc-measure` unchanged, and that is verified rather than
  assumed.
- Out: **what the sheet's contents look like.** Table rules, heading scale and alternating rows are
  [T-110](T-110-the-quick-view-styles-a-source-as-deck-copy-not-as-a-document.md). This task changes
  how much room they get, nothing about how they are drawn.
- Out: the source mark itself and the colophon — [T-109](T-109-one-source-reference-component-rendered-in-three-places.md).

**Inputs**
- [`shell/components.css`](../shell/components.css) — `.qv`, `.qv-sheet`, and the `.doc` block that
  legitimately owns `--doc-measure`.
- [`docs/THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) — where a new token is declared.
- [T-070](T-070-the-quick-view-for-a-source-document.md) — the feature, and why the sheet exists.
- Evidence: `D6-executive-board-presentation.html`, the first deck built on the published plugin by
  an adopting project. Its quick views carry the value tables that exposed this. **The deck itself is
  not copied into this repository** (CLAUDE.md, *Publishing constraints*); it is cited as the report.

**Acceptance criteria**
- [ ] `.qv-sheet` no longer references `--doc-measure`.
- [ ] `--qv-measure` has a row in [`THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) saying what it
      bounds and why it is not the prose measure.
- [ ] A quick view holding a seven-column table renders that table without per-cell wrapping at
      1280 and at 1920 viewport width.
- [ ] The reading view's prose measure is unchanged, checked by rendering a `.doc` before and after.
- [ ] `python tools/deck/check.py` green on the reference deck.
- [ ] Opened and looked at, offline.

**Open questions**
- None. The token's default value is an implementation decision, taken from what a source document's
  widest realistic table needs.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Measure the widest table in a real source quick view at the current width | the number the token has to clear |
| 2 | Declare `--qv-measure` in the theme contract and the shipping theme | contract row, token |
| 3 | Point `.qv-sheet` at it | `components.css` |
| 4 | Render both surfaces, before and after, and confirm `.doc` did not move | screenshots |
| 5 | `check.py`, then look at it offline | verdict |

## 3. Implement

**Decisions & assumptions**
-

**Outputs produced**
-

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :--- | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-12 | → proposed | Created. Reported by the first adopting project against published `0.2.2`, found in its own exam deck. Located to one declaration: `.qv-sheet` reuses `--doc-measure`, the prose measure, for a surface that holds tables. |
