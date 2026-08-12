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

**What the rendered deck shows, 2026-08-12**
Rendered offline in real Chrome with motion pinned (`render.py shots`), and looked at. Three things
the written report did not reach:

1. **The colophon renders every source as unreachable, and it is the one slide where every source is
   reachable.** All five documents have embedded quick views — `D1` through `D5`, confirmed in the
   markup — so any of them opens offline from inside the file. The colophon lists all five as plain
   text with no icon and no route, its own provenance mark reads **"THE FIVE DOCUMENTS ABOVE"** as
   plain text rather than a control, and its bottom line is the instruction *"Open any of the five
   from the mark in the corner of the slide that cites it."* **The slide whose entire purpose is the
   sources is the slide that routes to none of them**, and sends the reader back through twelve
   slides to find marks it could have carried itself.
2. **The `D1`–`D5` identifiers already exist there**, set in mono to the left of each title. Half the
   ladder is built; it has no icon and no route.
3. **A multi-source mark carries the single-source file glyph.** Slide 10 reads *"📄 2 SOURCES"* —
   same icon as a one-source slide, and a count where the reader wants to know *which two*. The
   knowledgebase mark this task adds is what distinguishes them.

**The full rendering already exists — in the reading view.** Captured the `.doc` view offline and
looked at it. There, `.doc .sources-btn{display:none}` opens every mark, and a two-source slide shows
**`D5 · Management decision matrix` / `D2 · Predictive analytics and data readiness`** in a tinted
box — identifier and title, one row per source, which is most of the ladder this task specifies.
**So half of this work is unifying two renderings that already exist**, not inventing one: the stage
hides behind a count what the reading view already spells out. Build the component from the doc
form's behaviour and give the stage a disclosure onto it.

**And the colophon's instruction is false in two of the three renderings.** *"Open any of the five
from the mark in the corner of the slide that cites it"* survives verbatim into the reading view,
where there are no corners and the sources are already inline, and onto **paper**, where there is
nothing to open at all. Confirmed in the exported PDF, page 14. A sentence that is merely unhelpful
on the stage is simply untrue in the other two.

**A fourth, about width.** A single-source mark renders as `D1 · CURRENT BUSINESS PROCESS ANALYSIS`,
uppercased and letterspaced, and takes roughly a quarter of the row. The identifier bound below is
the wrong instrument for that — **the case treatment is**. Sentence case on the title, with the
`D1` staying mono, buys the room back without truncating anything.

**Scope**
- In: the four-kind vocabulary, closed, with a row each in
  [`COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md).
- In: **the mark's case treatment**, decided by rendering it both ways at the real stage width.
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
- [ ] The colophon carries no instruction to look for links on earlier slides — checked in **all
      three renderings**, since the current sentence is false in the reading view and on paper.
- [ ] The stage's mark and the reading view's open list are one component, not two behaviours.
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
| 2026-08-12 | (no change) | **Deck rendered offline and looked at**, per CLAUDE.md rule 6. Findings in §1: the colophon routes to none of the five sources it lists although all five are embedded and reachable; the `D1`–`D5` identifiers already exist there without icon or route; a two-source mark carries the one-source glyph. Also added the mark's **case treatment** to scope — the uppercased title, not its length, is what costs the corner its room, and the identifier bound would not have fixed it. |
