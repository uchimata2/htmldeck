---
id: T-110
title: The quick view styles a source as deck copy, not as a document
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: [T-106, T-107]
related: [T-070, T-109]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-12
updated: 2026-08-12
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
| 1 | Wait on T-106 and T-107 — the measure and the element set | — |
| 2 | List every element `markdown()` emits | the styling target |
| 3 | Build the three table candidates | three renderings |
| 4 | Look at them and choose | decision in §3 |
| 5 | Tokenise every value; contrast-check | theme rows |
| 6 | Render a real source and look at it offline | verdict |

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
| 2026-08-12 | → proposed | Created from the first adopting project's feedback on published `0.2.2`. Blocked on T-106 and T-107: the measure and the element set are both inputs, and choosing a scale before either is settled means choosing twice. |
