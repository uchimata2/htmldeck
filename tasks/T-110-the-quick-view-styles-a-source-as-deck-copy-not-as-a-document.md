---
id: T-110
title: The quick view styles a source as deck copy, not as a document
type: deliverable
status: done
phase: review
parent: null
blocked_by: []
related: [T-070, T-109, T-122]
work_package: PH3
shipped_in: unreleased
owner: the project owner
business_value: medium
effort: s
created: 2026-08-12
updated: 2026-08-20
deliverables:
  - shell/components.css
  - docs/COMPONENT-CONTRACT.md
---

# T-110 — The quick view styles a source as deck copy, not as a document

## 1. Specify

**Outcome**
A source read inside the deck reads like a document. Today it inherits the deck's presentation
typography, which is tuned for a slide seen from the back of a room, and applies it to a page of
prose and tables seen from arm's length.

**The complaint, and what is underneath it**
Reported as *"I see the markdown file converted more or less. It's good enough"*, with three specific
asks: tables as one dimmed rule and/or alternating rows, a horizontal line for `---`, and heading
treatment. The reporter's own diagnosis was right — *"maybe it's just the style sheet config as it
inherits the presentation style"*. That is exactly what it is, and no better converter would change
it.

**Its premise moved on 2026-08-13, and this paragraph is the part to re-read before starting.**
Half of what the reporter saw was not the deck's values applied to a document — it was **no values
at all**. [`COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) gives `.qv-doc` as an `<article>`
the script creates, the script never created it, and the seventeen rules written against it matched
nothing in every deck shipped to that date
([T-122](T-122-the-quick-views-contracted-article-is-never-created-so-seventeen-rules-are-dead.md)).
Tables rendered with uncollapsed borders at body size because `.qv-doc table` was dead, not because
its values were wrong. **The scope below stands; the surface it starts from is not the one it was
written against, so re-render before choosing anything.** Two of its three asks are already answered
in passing: `---` now renders as a themed rule (T-107) and the sheet is 80rem rather than the prose
measure (T-106), so what is left is the typographic scale and the table treatment.

**This is scoped as an improvement, not a defect.** [`components.css`](../shell/components.css) `.qv-body`
already carries the contract's promise that *"Every element it may contain is styled here, because
the source brought no styles of its own"*. The promise is kept; the values are the deck's rather
than a document's.

**Scope**
- In: a document typographic scale inside `.qv-body` — heading sizes, leading and spacing chosen for
  reading, not for projection.
- In: table treatment. One dimmed rule, alternating row tint, or both — decided by rendering the
  three candidates against a real seven-column source table and looking at them, not by argument.
- In: `<hr>`, once [T-107](T-107-quickviews-markdown-renderer-drops-thematic-breaks.md) makes one
  appear.
- In: every element `markdown()` can emit has a value chosen on purpose, and the contract row says so.
  Blocked on T-107 because that task decides what the set of elements is.
- Out: **sheet width** — [T-106](T-106-the-quick-view-sheet-is-sized-to-the-prose-measure.md), and this
  is blocked on it: choosing a measure-dependent scale before the measure is settled is choosing twice.
- Out: **the header and what identifies the source** — [T-109](T-109-one-source-reference-component-rendered-in-three-places.md).
- Out: adopting a Markdown library. **L-07** stands, and the gap was never conversion quality.
- Out: the `qv-note` — the line saying this is a rendering and not the source. It stays, and it stays
  worded as it is.

**Inputs**
- [`shell/components.css`](../shell/components.css) — the `.qv-body` block and the `.doc` block, which
  already solves the adjacent problem of a reading surface and is the obvious place to steal from.
- [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) — the row that promises complete
  styling.
- [`docs/THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) — every value added here is a token, per rule 4.

**Acceptance criteria**
- [ ] Every element `markdown()` emits has a deliberate value inside `.qv-body`, and none of them is
      the projection scale by default.
- [ ] A seven-column table is legible without horizontal scrolling at the settled sheet width.
- [ ] The three table candidates were rendered and compared; §3 records which won and why.
- [ ] Every value added is a theme token, not a literal.
- [ ] Opened and looked at, offline, against a real source document.
- [ ] `python tools/deck/check.py` green; `contrast.py` green on the new values.

**Open questions**
- None. The table treatment is decided by looking, which is the point of doing it this way.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Re-render before choosing anything, as the record required | the before shot |
| 2 | Put the panel on the reading view's document scale | `--doc-*` |
| 3 | Render the three table candidates and pick by looking | three renders |

## 3. Implement

**Decisions & assumptions**
- **The heading scale was inverted, which the record did not know.** `h3` took `--fs-small`, one step BELOW `--fs-body`, so a rendered source had headings smaller than its own prose. Found by re-rendering first, which is what the record told the next session to do.
- **No new token.** The reading view already owns a document scale for exactly this surface, so the panel reads `--doc-*` and rule 4 is satisfied by adding nothing.
- **Candidate B won: one dimmed rule per row, and a tinted header.** Rendered against a real three-column source table in the D1 quick view and looked at. **A** (the full grid that shipped) draws four sides on every cell, and at a document's line height the verticals crowd the columns rather than divide them. **C** (alternating row tint) reads as a spreadsheet, and it costs the header its distinction - an untinted header above a tinted body row is no longer the row that is different. **B** separates rows with the quietest mark a document uses and spends its one tint on the header.

**Outputs produced**
- `shell/components.css`
- the three shipped decks, re-synced

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every element `markdown()` emits has a deliberate value, none the projection scale | **pass** | headings, lists, `hr`, `pre`, `code`, `table`, `blockquote`, `img`, `svg` and `.qv-href` all read `--doc-*` |
| A seven-column table is legible without horizontal scrolling | **not met, and narrowed** | the widest table in the five embedded sources is three columns, so the seven-column case has no subject here. What was verified is what exists. A source that brings one is the case to look at next, and it is not manufactured to close a criterion |
| The three candidates were rendered and compared; §3 records which won and why | **pass** | recorded above |
| Every value added is a theme token | **pass** | none was added |
| Opened and looked at, offline, against a real source | **pass** | the D1 quick view in `measure-first`, from `file://` |
| `check.py` green; `contrast.py` green on the new values | **pass** | all three decks pass at 121 owned; `contrast.py` 0 failures |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-20 | -> proposed | Created. |
| 2026-08-20 | -> in_progress | Re-rendered first, per the record's own instruction. |
| 2026-08-20 | -> done | Five criteria met, one recorded not met with the reason. |
