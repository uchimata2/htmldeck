---
id: T-122
title: The quick view's contracted `.qv-doc` article is never created, so seventeen style rules are dead
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-070, T-107, T-110]
work_package: PH1
owner: maintainer
business_value: high
effort: xs
created: 2026-08-13
updated: 2026-08-13
shipped_in: unreleased
deliverables: [shell/deck.js]
---

# T-122 — The quick view's contracted `.qv-doc` article is never created, so seventeen style rules are dead

## 1. Specify

**Outcome**
The element [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) says the script creates
exists in the rendered page, so the rules written against it apply.

**The mechanism, measured**
The contract is specific:

| `.qv-doc` | `article` | `.qv-body` | `0-1` | — | script |

and the note beside it says *"the article is created when a quick view is opened"*. It was not.
`openQuick()` appended the template's clone straight into `#qvBody`, so **`.qv-doc` was absent from
the DOM of every deck this project has ever shipped**, and the seventeen `.qv-doc …` rules in
[`shell/components.css`](../shell/components.css) matched nothing.

Measured in real Chrome on `examples/sort-window/sort-window.html`, quick view open, before and
after:

| Property | Rule that owns it | Before | After |
| :--- | :--- | :--- | :--- |
| `.qv-doc` in the DOM | the contract | absent | `ARTICLE` |
| table `border-collapse` | `.qv-doc table` | `separate` | `collapse` |
| table width at 1920 | `.qv-doc table{width:100%}` | 784 px, content-driven | 1196 px |
| `th` font size | `.qv-doc table{font-size:var(--fs-small)}` | 26 px, the body size | 22.5 px |

**Nothing could have caught it.** `component.py check`'s placement rule reads the deck's static
markup and reports `no contracted class sits where the contract does not put it: 0 problem(s)` — a
class the script creates at open time is in no file for it to read. The contract's own `script`
origin column is the marker for exactly this family, and no check reads that column.

**Found while verifying [T-107](T-107-quickviews-markdown-renderer-drops-thematic-breaks.md)**,
whose criterion is that a thematic break renders *themed*. It rendered at the browser's default grey
because the rule that themes it is one of the seventeen.

**It changes [T-110](T-110-the-quick-view-styles-a-source-as-deck-copy-not-as-a-document.md)'s
premise.** That task reads the complaint as *values chosen for a slide, applied to a document*, and
its own diagnosis quotes the reporter: *"maybe it's just the style sheet config"*. Half of what the
reporter saw was not the deck's values at all — it was no values, because the selector named a class
nothing carried. T-110's scope stands; the surface it starts from is not the one it was written
against.

**Scope**
- In: `openQuick()` creates the contracted `<article class="qv-doc">` and clones into it.
- Out: what the rules should say. Seventeen rules becoming live is a visible change to a shipped
  surface, and choosing better values on it is T-110's, unchanged.
- Out: a check that reads the contract's `script` origin column. Raised as a gap rather than built
  here — see §4.

**Inputs**
- [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) — the `.qv-doc` row and the note.
- [`shell/deck.js`](../shell/deck.js) — `openQuick()`.
- [`shell/components.css`](../shell/components.css) — the seventeen rules.

**Acceptance criteria**
- [x] `.qv-doc` is in the DOM when a quick view is open, as the `<article>` the contract names
- [x] The four properties above take their contracted values, measured in real Chrome
- [x] `component.py check` and `shell.py check` green on both shipped decks
- [x] Looked at, offline

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Create the article in `openQuick()`, propagate to both decks and the seeded fixture | `deck.js` |
| 2 | Re-measure the four properties in real Chrome | the table above |
| 3 | Re-run the deck gates | verdicts |

## 3. Implement

**Decisions & assumptions**
- **Create the element rather than repoint the selector at `.qv-body`** — the contract already names
  the element, its tag, its parent and its cardinality, and a stylesheet edited to match a defect is
  how the contract stops being the source of truth (**L-08**) — 2026-08-13.
- **The values are not touched.** Seventeen rules go from dead to live in one step and that is the
  whole change; what they should say is T-110's question — 2026-08-13.

**Outputs produced**
- [`shell/deck.js`](../shell/deck.js), and the same block in both shipped decks and the seeded
  fixture.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| `.qv-doc` is in the DOM as the contracted `<article>` | met | `{'article': True, 'articleTag': 'ARTICLE'}` |
| The four properties take their contracted values | met | `collapse`, 1196 px, 22.5 px, and `hr` at `--line` rather than the UA grey. The before column was measured on the same deck in the same run shape |
| `component.py check` and `shell.py check` green on both decks | met | `every class the shared block styles has a row: 87 styled, 0 uncontracted`; the shell cut round-trips |
| Looked at, offline | met | Rendered from `file://` with DNS black-holed, quick view open, at 1280 and 1920 |

**Child fix tasks raised**
- none. **One gap recorded instead**: no check reads the contract's `origin` column, so a class the
  script creates is asserted by nothing. It is the mechanism that hid this for the whole life of the
  feature, and it is written up in
  [T-110](T-110-the-quick-view-styles-a-source-as-deck-copy-not-as-a-document.md)'s inputs rather
  than as a task of its own, because the check needs a rendered DOM and that is a decision about the
  gate set rather than a fix.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-13 | → done | Found while verifying T-107's *renders themed* criterion, which could not be met: the rule that themes an `<hr>` is one of seventeen written against a class no deck carried. Three lines in `openQuick()`. `PH1` — it is a defect in the published plugin, and it is the reason a quoted source has always rendered at slide scale. **It changes T-110's premise**, which is the part worth reading twice: that task was scoped against values chosen badly, and half of what it describes is no values at all. |
