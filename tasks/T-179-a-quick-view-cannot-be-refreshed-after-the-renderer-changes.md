---
id: T-179
title: A quick view cannot be refreshed after the renderer changes, so a renderer fix never reaches a deck that already carries one
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-070, T-107, T-121]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-18
updated: 2026-08-18
deliverables: [tools/deck/quickview.py]
---

# T-179 — A quick view cannot be refreshed after the renderer changes, so a renderer fix never reaches a deck that already carries one

## 1. Specify

**Outcome**
A deck that already carries a quick view can be re-rendered from the same source with the current
`markdown()`, without rebuilding the deck and without hand-editing its HTML.

**The mechanism, measured**
`wire()` finds where to put a quick view with `item_pattern(title)`, which matches a **bare**
provenance item:

```
<span class="sources-item">(ITEM_HEAD)<title></span>
```

Once wired, that span holds a `<button class="sources-open">` and a `<template class="qv-src">`, so
the pattern no longer matches and `add` refuses. Measured 2026-08-18 on a copy of the shipped
`measure-first` deck:

```
REFUSED  Current business process analysis  no provenance item reads 'Current business process
         analysis' in this deck.
```

The refusal is correct for its own question — it is the T-069 guard that stops a quick view being
attached to a source no slide cites. It is simply also the only answer available to *refresh*, which
is a different question nothing asks on this deck's behalf.

**What it cost, already spent.** [T-121](T-121-the-quick-view-renderer-flattens-nested-lists-and-drops-indented-code.md)
fixed the renderer and proved the fix against the shipped sources: **4 of the 8 embedded sources
render differently**, and the difference is not cosmetic — the old renderer broke a wrapped list
item into `<li>first line</li></ol><p>the rest of the sentence</p><ol>`, splitting one sentence
across an item and a paragraph and shattering one `<ol>` into three. Two shipped decks carry that
today, and T-121 could not reach them.

**Scope**
- In: a way to re-render the quick views a deck already carries, from the sources named on the
  command line, replacing the `<template>` contents in place.
- In: the refusal above keeps meaning what it means for a source no slide cites. Refresh is a
  different verb, not a relaxation of that guard.
- In: it reports what changed, in the terms `plan` already uses — bytes before and after, per
  source — because a refresh silently rewriting a shipped deck is the failure mode here.
- In: refreshing the two decks that carry the T-121 defect, and looking at the result offline.
- Out: rebuilding a deck from its specification. That is the build, and it is not this.
- Out: any change to what `markdown()` produces — T-121 settled that.
- Out: what a quick view looks like, which is
  [T-110](T-110-the-quick-view-styles-a-source-as-deck-copy-not-as-a-document.md)'s.

**Inputs**
- [`tools/deck/quickview.py`](../tools/deck/quickview.py) — `item_pattern`, `wire`, `carried`,
  `plan`.
- [`examples/measure-first/measure-first.html`](../examples/measure-first/measure-first.html) and
  its [`sources/`](../examples/measure-first/sources) — 5 quick views, 4 of them affected.
- [`examples/sort-window/sort-window.html`](../examples/sort-window/sort-window.html) — 3 quick
  views, none affected; the control case that proves a refresh is byte-identical when the renderer
  agrees with what is already embedded.

**Acceptance criteria**
- [ ] A deck already carrying a quick view can be re-rendered from its source without rebuilding it
- [ ] Refreshing `sort-window` changes nothing, byte for byte — the renderer agrees with what is
      embedded, so a refresh must be a no-op
- [ ] Refreshing `measure-first` replaces exactly the 4 affected templates and leaves the 5th alone
- [ ] A source no slide cites is still refused, with the T-069 wording unchanged
- [ ] The two shipped decks are refreshed, gated, and looked at offline

**Open questions**
- None. Whether this is a new subcommand or a flag on `add` is an implementation choice, and the
  criteria above hold either way.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | A pattern that matches an already-wired item, beside the bare one | `quickview.py` |
| 2 | The refresh path: re-render, swap the `<template>` body, report the byte delta | `quickview.py` |
| 3 | A self-test fixture per branch — refuses an uncited source, no-ops when nothing changed | self-test |
| 4 | Refresh both shipped decks; gates; open the changed quick views and look | the decks |

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
| 2026-08-18 | → proposed | Raised out of [T-121](T-121-the-quick-view-renderer-flattens-nested-lists-and-drops-indented-code.md), which fixed the renderer and then could not deliver the fix to the two decks that need it. `PH3` by [`../CLAUDE.md`](../CLAUDE.md)'s rule — the published plugin is not broken by this, and a deck built after T-121 renders correctly from the start, so it is not a defect that reopens `PH1`. What makes it worth its own record rather than a note is that the gap is in the *tool's verbs*, not in one deck: every future renderer change will hit it again. |
