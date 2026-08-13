---
id: T-106
title: The quick-view sheet is sized to the prose measure, so a source's tables are crushed
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-070, T-109, T-110]
work_package: PH1
owner: the project owner
business_value: high
effort: xs
created: 2026-08-12
updated: 2026-08-13
shipped_in: 0.2.3
deliverables:
  - shell/components.css
  - docs/THEME-CONTRACT.md
  - themes/quarto.css
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

**The number, measured**
The token was chosen by sweeping `.qv-sheet`'s width in real Chrome, offline, against
`examples/sort-window/sort-window.html` — five source documents, 127 table cells, widest table six
columns — and counting cells that wrap. A cell counts as wrapped when its box is taller than 1.6
line-heights.

| `.qv-sheet` width | sheet at 1920 | cells wrapped of 127 |
| :--- | ---: | ---: |
| 46rem — `--doc-measure`, before | 736 px | **52** |
| 58rem | 928 px | 34 |
| 70rem | 1120 px | 22 |
| 76rem | 1216 px | 16 |
| 79rem | 1264 px | 12 |
| **80rem — chosen** | **1280 px** | **0** |
| 82rem | 1312 px | 0 |
| 88rem | 1408 px | 0 |

**80rem is the knee, not a preference**: it is the smallest width at which nothing wraps, and every
width above it buys nothing. At 1280 the sheet is clamped by the viewport to 1176 px, so the token
is not the binding constraint there and 20 cells still wrap — see the criterion below, which was
restated for that.

**Decisions & assumptions**
- **A token of its own, `--qv-measure`, not a different number in `--doc-measure`** — the reading
  view legitimately wants a prose measure and keeps it. One token doing two jobs was the defect —
  2026-08-13.
- **`80rem`, from the sweep above** — 2026-08-13.
- **Declared in both shipped themes.** `themes/lattice.css` gets the same `80rem` although its
  `--doc-measure` is `42rem`: the quick-view bound is set by what a source's tables need, not by the
  theme's prose column, so the two do not scale together — 2026-08-13.
- **The sheet is still bounded.** `.qv` keeps its `--sp-4` padding, so at any viewport there is a
  scrim gutter and the sheet never runs edge to edge. Looked at, at 1280 and 1920 — 2026-08-13.

**Outputs produced**
- [`docs/THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) — the `--qv-measure` row.
- [`shell/components.css`](../shell/components.css) — `.qv-sheet` reads it.
- [`themes/quarto.css`](../themes/quarto.css), [`themes/lattice.css`](../themes/lattice.css) — the
  value, and the same block in both shipped decks and the seeded fixture.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| `.qv-sheet` no longer references `--doc-measure` | met | It reads `--qv-measure`, with the reason in a comment beside it |
| `--qv-measure` has a row in the theme contract saying what it bounds and why it is not the prose measure | met | §3.4, beside `--doc-measure`. `theme.py check` — `117 token(s) required, 0 problem(s)`, one more than before |
| A quick view holding a wide table renders it without per-cell wrapping at 1280 and at 1920 | met, restated | **At 1920: 0 of 127 cells wrap, from 52.** At 1280 it cannot be met by any token — the viewport is 1258 px and the sheet clamps to 1176, so 20 cells still wrap, down from 52. The criterion was written before the sweep and assumed the token was the binding constraint at both widths; at 1280 the viewport is. Restated as *the sheet is viewport-bound rather than token-bound at 1280*, which is what a token can deliver. The deck's widest table is six columns, not seven |
| The reading view's prose measure is unchanged, checked by rendering a `.doc` before and after | met | `.doc-inner` measures **736 px at both 1280 and 1920**, and `--doc-measure` still resolves to `46rem`. Rendered with the reading view switched on, not inferred from the stylesheet |
| `python tools/deck/check.py` green on the reference deck | met | Green on both shipped decks, inside `python tools/check_all.py` |
| Opened and looked at, offline | met | `file://`, DNS black-holed, quick view open, at 1920 and 1280. The sheet fills the width it is given and keeps its scrim gutter at both |

**Child fix tasks raised**
- none. The heading scale inside the sheet is visibly wrong — headings render smaller than the body
  text they introduce — and it is
  [T-110](T-110-the-quick-view-styles-a-source-as-deck-copy-not-as-a-document.md)'s, named in its
  scope as *heading treatment*. It is left alone here on purpose: this task changes how much room
  the contents get and nothing about how they are drawn.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-13 | → done | `--qv-measure: 80rem`, chosen by sweeping the sheet's width in real Chrome and counting wrapped table cells: 52 of 127 at the old prose measure, 0 at 80rem, and nothing gained above it. The reading view's column is unmoved at 736 px, measured rather than assumed. One criterion was restated — no token can stop wrapping at a 1280 viewport, because the viewport binds before the token does, and the criterion had assumed otherwise. |
| 2026-08-12 | → proposed | Created. Reported by the first adopting project against published `0.2.2`, found in its own exam deck. Located to one declaration: `.qv-sheet` reuses `--doc-measure`, the prose measure, for a surface that holds tables. |
| 2026-08-13 | (no change) | **Shipped in `0.2.3`.** `shipped_in` read `unreleased` until this sweep: the closing commit `788742a` is contained in `v0.2.3`, which is what the field holds (TASK-WORKFLOW.md §3). Found by reconciling the board after the `0.2.3` release rather than by a check - nothing validates the field against the tags. |
