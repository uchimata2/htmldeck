---
id: T-109
title: One source-reference component, typed by what the source is, rendered in three places
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-069, T-070, T-103, T-106, T-108, T-110]
work_package: PH3
owner: the project owner
business_value: high
effort: l
created: 2026-08-12
updated: 2026-08-12
deliverables:
  - shell/components.css
  - shell/icons.svg
  - docs/COMPONENT-CONTRACT.md
  - docs/DESIGN-SYSTEM.md
  - skills/htmldeck/references/build.md
---

# T-109 — One source-reference component, typed by what the source is, rendered in three places

## 1. Specify

**Outcome**
A source reference is one component. It knows what kind of thing it points at, it shows an icon that
says so, it carries an identifier when the identifier is short enough to help, and it offers the best
route to the source that survives delivery. The provenance mark, the list behind a multi-source mark,
and the colophon all render that one component — so the colophon stops telling the reader to go and
find the links on earlier slides.

**Why now**
DS-105's link clause had no instance anywhere until an adopting project shipped a real deck on the
published plugin ([T-069](T-069-extend-the-provenance-mark-to-multiple-sources.md) recorded that both
example decks cited none of their three sources). The first deck to use it in anger produced the
whole of this task's evidence in one report.

**The three-place rule is the point.** Today the colophon is authored separately from the mark, which
is why it drifted into a slide of bare titles with a footnote pointing backwards. Rendering one
component in three places is **DS-136** applied to the thing that most obviously needed it.

**The type ladder**
A source is one of four kinds, and the kind decides both the icon and the route:

| Kind | Icon | Route |
| :--- | :--- | :--- |
| External URL | link | opens in a new tab |
| Renderable local document | file | opens its carried quick view |
| Local document that cannot be rendered | file | plain text, no route |
| More than one source on a slide | knowledgebase | opens the list, each row rendered as above |

**A local file does not become a link, and this is settled.** The reporting project asked for local
files to open in a new tab. **DS-105 already rules against it** and the reason is rule 2: the
recipient double-clicks the file on a machine that has never seen the author's paths, so every such
link is dead on arrival, and DS-105's *never a dead link* is the hard half. The resolution the
project already chose is the right one — **the deck carries the rendering**
([T-070](T-070-the-quick-view-for-a-source-document.md)) — and this task generalises it into the
ladder above rather than adding a link form that cannot survive delivery. Recorded here because the
request will be made again.

**Scope**
- In: the four-kind vocabulary, closed, with a row each in
  [`COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md).
- In: an icon per kind in [`shell/icons.svg`](../shell/icons.svg), including the knowledgebase mark
  the multi-source case needs.
- In: an optional short identifier, with a stated length bound above which it is dropped. **The bound
  is a number in the contract, not a judgement at build time** — an identifier that helps a reader is
  short, and a long one is noise that costs the title its room.
- In: the colophon rendering the same component, one row per source, each row routed.
- In: the quick-view header naming the **source file** as well as the title, so the original can be
  found — the reporting project asked for this and it is the same fact the component already holds.
- In: [`build.md`](../skills/htmldeck/references/build.md) teaching the build how to determine a
  source's kind, and what to emit when it cannot.
- In: whatever of this `check.py` can decide, with a written reason for each clause it cannot.
- Out: **the sheet's width** — [T-106](T-106-the-quick-view-sheet-is-sized-to-the-prose-measure.md).
- Out: **the sheet's typography** — [T-110](T-110-the-quick-view-styles-a-source-as-deck-copy-not-as-a-document.md).
- Out: **what stage the colophon declares** — [T-108](T-108-a-deck-has-no-back-matter-stage-so-the-colophon-is-labelled-with-the-last-argument-stage.md).
- Out: generating a rendering for a source type the quick view cannot admit. T-070's three admission
  tests stand; a source that fails them is the third row of the ladder — plain text, no route.

**Inputs**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — **DS-105**, including the `file://` clause
  this task declines to relax, and the disclosure interaction rules the mark obeys.
- [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) §3.2 — `.sources` as it stands.
- [T-069](T-069-extend-the-provenance-mark-to-multiple-sources.md) — the multi-source mark, and the
  finding that the link clause had no instance.
- [T-103](T-103-build-md-drops-ds-105s-link-clause-for-a-single-source-slide.md) — the single-source
  form, and why it has no button.
- [T-070](T-070-the-quick-view-for-a-source-document.md) §1 — the three admission tests, which decide
  rows two and three of the ladder.

**Acceptance criteria**
- [ ] Four kinds, closed, each with a contract row and an icon.
- [ ] The colophon and the provenance mark render from one component; changing the component changes
      both, demonstrated by changing it.
- [ ] The colophon carries no instruction to look for links on earlier slides.
- [ ] An identifier longer than the contract's bound is dropped, and the title keeps its room.
- [ ] A source that fails T-070's admission tests renders as plain text with no route, and no dead
      link appears anywhere in the deck.
- [ ] The quick-view header names the source file.
- [ ] A 12-slide deck carrying all four kinds is built and every route is followed by hand, offline,
      with the network disabled.
- [ ] `python tools/deck/check.py` green; every DS-105 clause it cannot decide is named with a reason.

**Open questions**
- None outstanding. The owner accepted the ladder and the local-file ruling on 2026-08-12.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Write the four-kind vocabulary and the identifier bound into the contract | contract rows |
| 2 | Draw the missing icons | `icons.svg` |
| 3 | Build the component once; render it in the mark, the list and the colophon | `components.css`, shell |
| 4 | Teach `build.md` how to type a source and what to do when it cannot | `build.md` |
| 5 | Build a 12-slide deck carrying all four kinds | test deck |
| 6 | Follow every route by hand, offline | verdict |
| 7 | Extend `check.py`; write the reason for each undecidable clause | `check.py`, ruleset |

## 3. Implement

**Decisions & assumptions**
- 2026-08-12 — a local file is never emitted as a `file://` link in a delivered deck. DS-105 already
  says so; the request to change it was declined with the reason recorded in §1.

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
| 2026-08-12 | → proposed | Created from the first adopting project's feedback on published `0.2.2`. Scoped as one component rendered three times rather than as two separate improvements to the mark and the colophon, because authoring them separately is what let the colophon drift. |
