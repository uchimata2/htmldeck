---
id: T-109
title: One source-reference component, typed by what the source is, rendered in three places
type: deliverable
status: done
phase: review
shipped_in: unreleased
parent: null
blocked_by: []
related: [T-069, T-070, T-103, T-106, T-108, T-110, T-176]
work_package: PH3
owner: the project owner
business_value: high
effort: l
created: 2026-08-12
updated: 2026-08-17
deliverables:
  - shell/components.css
  - shell/icons.svg
  - shell/shell.html
  - shell/deck.js
  - docs/COMPONENT-CONTRACT.md
  - docs/DESIGN-SYSTEM.md
  - skills/htmldeck/references/build.md
  - tools/deck/quickview.py
  - tools/deck/audit.py
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
- In: whatever of this the gate can decide, with a written reason for each clause it cannot. The
  rows live in [`audit.py`](../tools/deck/audit.py), which `check.py` reads.
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

**What "one component" is, concretely, because the shell and the deck own different halves.** The
shell owns the CSS and the script; the deck owns the markup. So the component is **`.sources-item`
and its interior** — the identifier, the kind glyph, and the one route the kind allows — contracted
once, styled once, and driven by one delegated handler. The three places are the one-source mark, the
multi-source box, and the colophon, and they differ only in which wrapper the items sit in.

**The colophon's list is `.sources` too, which is what makes the criterion demonstrable.** Today the
colophon is `.colo` / `.colo-row` / `.colo-id` / `.colo-name` — **four CSS rules authored inside the
deck's own `<style>`, with no shell rule, no icon, no route and no contract row.** That is the whole
mechanism of the drift §1 found: nothing shared could have kept the two in step, because nothing was
shared. Deleting those four rules in favour of the shell's component is the change that makes
*"changing the component changes both"* a fact rather than a claim.

**Where `.sources` may sit has to widen, and `.slide` is the honest bound.** The contract's parser
takes one parent per part and checks it as an **ancestor**, so `.provenance` becomes `.slide` at
`0-1`: a slide declares its sources once, in its provenance mark or — on the colophon — in its body.

**Six copies of one source is a cost this design does not pay.** `deck.js` keys `qvSrc` off
`data-qv` across the whole stage, so the colophon's rows carry `.sources-open` controls and no
`.qv-src` templates of their own; they resolve to the templates the citing slides already carry.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Add the two Lucide glyphs the ladder needs and nothing has — an external-link mark and a knowledgebase mark — with their licence line | `shell/icons.svg` |
| 2 | Contract the four kinds, the per-item parts, the identifier bound as a number, and `.sources` at `.slide` | `docs/COMPONENT-CONTRACT.md` |
| 3 | Extend DS-105 to carry the ladder and the colophon's obligation in all three renderings | `docs/DESIGN-SYSTEM.md` |
| 4 | Style the item once — identifier, glyph, route — give `.sources--list` the colophon's block form, and fix the mark's case treatment | `shell/components.css` |
| 5 | Name the source file in the quick-view header | `shell/shell.html`, `shell/deck.js` |
| 6 | Teach the build to type a source and emit its row; teach `quickview.py` to carry the file name through | `build.md`, `tools/deck/quickview.py` |
| 7 | Rebuild the published colophon on the component and sync the shell into every shipped deck | `examples/`, `shell.py sync` |
| 8 | Extend `check.py`; write the reason for each DS-105 clause it cannot decide | `check.py`, ruleset |
| 9 | Build a 12-slide deck carrying all four kinds; follow every route by hand, offline; print it | verdict |

**Order is forced from step 2.** The contract is the input `component.py` reads, so every later step
is checked against it — writing the CSS first would be checking the shell against the old table.

## 3. Implement

**Decisions & assumptions**
- 2026-08-12 — a local file is never emitted as a `file://` link in a delivered deck. DS-105 already
  says so; the request to change it was declined with the reason recorded in §1.
- 2026-08-17 — **the identifier bound is six characters**, written into
  [`COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) §3.2.1 and read from there by the gate.
  Six is what the useful forms need — `D1`, `WP3`, `R5`, `T-109`, `§3.2` — and it is short enough
  that a date or a title fragment cannot pass. **Above it the identifier is dropped, never
  truncated**: a truncated identifier looks like a reference the reader could resolve.
- 2026-08-17 — **the kind glyph rides the mark at one source and the item at several.** A
  `.sources--one` row would otherwise carry the same glyph twice on one line. So `.sources-icon` is
  `0-1`, and `.sources-mark` is `0-1` as well because the colophon's list has no corner mark at all.
- 2026-08-17 — **the case treatment is what buys the corner its room, and the identifier bound is
  not.** §1's fourth finding measured a single-source mark at about a quarter of the row; the length
  was never the cause, the inherited uppercase-mono-letterspaced treatment was. `.sources--one
  .sources-box` now sets the text face, normal tracking and sentence case, and `.sources-id` stays
  mono beside it. **No truncation and no width bound**, which an ellipsis would have quietly become.
- 2026-08-17 — **the colophon's rows carry `.sources-open` and no second copy of each `.qv-src`.**
  `deck.js` keys its template map off `data-qv` across the whole stage, so five documents are quoted
  once, not twice. **Measured 2026-08-17 on `examples/measure-first/measure-first.html`: the
  colophon's whole `.sources--list` block is 2,024 bytes, against 99,163 bytes for the five
  templates it reaches instead of copying.** The deck moved 377,630 → 387,004 over the whole change,
  most of which is the shell sync rather than this slide.
- 2026-08-17 — **the colophon's `.provenance` is empty**, and that is the contract working. A slide
  declares its sources once; this one declares them in its body. The bottom line that replaced the
  false instruction states a property of the *file* rather than of the medium, so it survives into
  the reading view and onto paper, which is what the criterion asks.
- 2026-08-17 — **the source file is named by base name only.** `quickview.py` writes `data-file` and
  the script paints it into `.qv-file`; a directory would describe the author's machine rather than
  the document, and a delivered deck must carry neither.

**What the gate can decide of DS-105, and what it cannot**

Four rows now, where there was one. Three are new and each is a prohibition over something the file
records rather than something a reader judges:

| Clause | Decided | How |
| :--- | :--- | :--- |
| Never a dead link | yes | `provenance_links` — the row T-069 added |
| An identifier past the bound | yes | every `.sources-id` against the contract's six |
| A mark wearing the wrong kind's glyph | yes | the mark's `<use>` resolved through the deck's own sprite to its `data-icon` |
| A control that opens nothing | yes | every `.sources-open`'s `data-qv` against the templates carried |
| *Reachable from where the deck is presented* | **no** | whether a URL resolves for that audience is not a fact the file records. It was already outside the gate and stays there |
| *The colophon carries no instruction to look on earlier slides* | **no** | a reading of a sentence. The sentence that provoked the clause — *open any of the five from the mark in the corner of the slide that cites it* — holds no token a pattern could bind to without also failing honest copy (**L-105**'s shape) |
| *One component in three places* | **no, and it needs none** | `component.py` decides it structurally: all three renderings are `.sources-item`, and a contract row is the only way to style one |

**What the new row found, on a deck this task was not aimed at.** `marks wearing the wrong kind's
glyph: 5 of 11` on [`examples/reference-deck.html`](../examples/reference-deck.html) — the same
defect §1 recorded on the adopter's deck, on the deck this repository writes itself, five times.
Both are fixed. A check written from one deck's symptom caught the class on another, which is the
whole argument for writing the check rather than the fix.

**Outputs produced**
- [`shell/icons.svg`](../shell/icons.svg) — `library` and `link`, 38 → 40 glyphs, Lucide, ISC.
- [`shell/components.css`](../shell/components.css) — `.sources-id`, `.sources-icon`, the item as
  one three-column row, `.sources--list` on screen, in the reading view and on paper, `.qv-file`,
  and the case treatment. **The component is styled in three places because it renders in three,
  and each needed a pass of its own**: design-unit sizes are wrong in a document, and a print block
  that resets the box resets the alignment with it.
- [`shell/shell.html`](../shell/shell.html), [`shell/deck.js`](../shell/deck.js) — `.qv-file`.
- [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) — §3.2.1, the four kinds and the
  bound; `.sources` moved to `.slide`; five new rows.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-105 extended.
- [`skills/htmldeck/references/build.md`](../skills/htmldeck/references/build.md) — how to type a
  source, and what to emit when it cannot be typed.
- [`tools/deck/quickview.py`](../tools/deck/quickview.py) — carries the file name; preserves an
  identifier and a glyph it did not write.
- [`tools/deck/audit.py`](../tools/deck/audit.py) — the three new DS-105 rows.
- All three shipped decks retyped; [T-176](T-176-shell-py-s-self-test-blocks-the-command-that-fixes-what-it-fails-on.md)
  raised and fixed, because `shell.py` refused every subcommand once `shell.html` moved.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :--- | :--- |
| Four kinds, closed, each with a contract row and an icon | met | [`COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) §3.2.1 is the table; `library` and `link` joined `file-text` in [`shell/icons.svg`](../shell/icons.svg), 38 → 40 glyphs |
| The colophon and the mark render from one component, demonstrated by changing it | met | The colophon's `.colo` rules are deleted and its rows are `.sources-item`. Demonstrated twice by accident and once on purpose: the baseline-alignment fix and the hit-area fix each moved the mark and the colophon together, from one `shell/components.css` edit and a `sync` |
| The colophon carries no instruction to look for links on earlier slides — in **all three** renderings | met | Zero occurrences of *from the mark in the corner* in any shipped deck. The replacement states a property of the file rather than of the medium, so it holds on the stage, in the reading view (read back from the DOM) and on paper (printed and looked at, page 14 of 14) |
| The stage's mark and the reading view's open list are one component | met | The reading view's colophon carries 5 `.sources-item` rows, `align-items: baseline`, each routed; the multi-source marks' buttons compute to `display: none` there, which is DS-073 opening what the stage discloses. **Being one component is also what surfaced the reading view's scale defect in both places at once**, and one `.doc` rule fixed both |
| An identifier longer than the bound is dropped, and the title keeps its room | met | Six characters, in the contract, decided by the gate. **Measured in real Chrome at the stage width**: a one-source mark was 485 px of 1918 (25.3%) uppercase-mono and is 379 px (19.8%) in sentence case — §1's *roughly a quarter* confirmed, and 106 px bought back by the case treatment rather than by any bound |
| A source failing T-070's tests renders as plain text with no route, and no dead link anywhere | met | The four-kind fixture carries one, rendered and looked at: no underline, no control, the document glyph. `dead links in a provenance mark: 0` on all three shipped decks and on the fixture |
| The quick-view header names the source file | met | `.qv-file` under the title. Opened from the colophon and looked at: *Current business process analysis* over `D1-current-business-process-analysis.md` |
| A 12-slide deck carrying all four kinds is built, every route followed by hand, offline | **partially met** | A 13-slide deck carrying all four was built and rendered offline, and the colophon shows all four correctly. **Every route was exercised through the shipped delegated handler in a script-running pane and read back** — five colophon controls, each opening the right document with the right title, file and heading, and `scrollTop` 0. **What was not done is a human hand on the control**: the pane available here reports a 0×0 viewport, so it cannot hit-test or screenshot, and coordinate clicking would have been theatre (**L-110**). Recorded as owed rather than claimed |
| `check.py` green; every DS-105 clause it cannot decide named with a reason | met | Four DS-105 rows where there was one, all green on three decks and the fixture. The three it cannot decide are named with their reasons in §3 and in `provenance_verdicts`' docstring |

**What the work found that the specification did not ask for**

- **The same defect on this repository's own deck.** The new glyph row failed
  [`examples/reference-deck.html`](../examples/reference-deck.html) `5 of 11` — five multi-source
  marks wearing the one-source glyph, the defect §1 recorded on somebody else's deck. Fixed there
  too. A check written from one deck's symptom found the class on another.
- **`shell.py` refused every subcommand once `shell.html` moved** —
  [T-176](T-176-shell-py-s-self-test-blocks-the-command-that-fixes-what-it-fails-on.md), raised and
  closed, **L-112**.
- **Two checks scoped to `<p class="provenance">` stopped seeing the component when it gained a
  second home** — DS-105's own dead-link row reported `0 of 1 examined` and DS-001 failed a URL
  DS-105 admits. Both rebound to the class. **L-113**, and the fixture is why it was caught.
- **Four defects only looking could find**, all introduced by this task and all fixed. Each was
  invisible to every check and visible in a different rendering, which is the argument for looking
  at all three:
  - the quick view's title carried the markup's line break and ten spaces into the header;
  - a colophon row's control stretched to 970 px, so a click on empty space opened a document —
    `justify-self` alone did not move it, because `.sources-open` sets `width:100%`;
  - **on paper** the print block still said `align-items:start`, so identifiers and glyphs printed
    above the title's cap line and read as superscripts;
  - **in the reading view** the item's parts are sized in design units and the reading view is not
    (DS-074), so a 14.5 px title arrived with an 18 px identifier, a 23 px glyph and a 93 px-tall
    control. Now 14.5 / 11.5 / 11.5 / 23.3, measured in the browser both times.

**Child fix tasks raised**
- [T-176](T-176-shell-py-s-self-test-blocks-the-command-that-fixes-what-it-fails-on.md) — done.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-12 | → proposed | Created from the first adopting project's feedback on published `0.2.2`. Scoped as one component rendered three times rather than as two separate improvements to the mark and the colophon, because authoring them separately is what let the colophon drift. |
| 2026-08-12 | (no change) | **Deck rendered offline and looked at**, per CLAUDE.md rule 6. Findings in §1: the colophon routes to none of the five sources it lists although all five are embedded and reachable; the `D1`–`D5` identifiers already exist there without icon or route; a two-source mark carries the one-source glyph. Also added the mark's **case treatment** to scope — the uppercased title, not its length, is what costs the corner its room, and the identifier bound would not have fixed it. |
| 2026-08-17 | → specified | §1 needed no change to close `specify`: the ladder, the local-file ruling and the acceptance criteria were settled on 2026-08-12 and the owner's 2026-08-17 move to rank 1 did not touch scope. Baseline recorded before any edit — `python tools/check_all.py` green, 0 failures, 0 unclassified, 0 stale, 304 s. |
| 2026-08-17 | → planned | §2 rewritten from seven steps to nine, and the two additions are the ones that decide the shape. **The colophon's list is deck-local `.colo` markup with no shell rule and no contract row**, which is the mechanism behind §1's drift rather than another symptom of it — so the plan deletes it instead of decorating it. **`.sources` moves from `.provenance` to `.slide` at `0-1`** because `component.py` takes one parent per part and tests it as an ancestor, and the colophon's copy lives in `.body`. Also settled without cost: the colophon carries `.sources-open` controls and no second copy of each `.qv-src`, because `deck.js` keys `qvSrc` off `data-qv` across the whole stage. |
| 2026-08-17 | → in_progress | Implemented in the plan's order, which the contract forced: `component.py` reads that table, so every later step was checked against it. Two things stopped the run and were fixed as they came — `shell.py` refused every subcommand once `shell/shell.html` moved ([T-176](T-176-shell-py-s-self-test-blocks-the-command-that-fixes-what-it-fails-on.md)), and DS-105's own dead-link row plus DS-001's exemption were both scoped to `<p class="provenance">` and stopped seeing the component in its second home (**L-113**). |
| 2026-08-17 | → done | **Eight criteria met and one partially**, and the one is the hand on the control: every colophon route was exercised through the shipped handler and read back, on a pane whose viewport reports 0×0, so it cannot hit-test or screenshot. Looked at what does render — the colophon on the stage, the quick view opened from it, the four-kind fixture, and page 14 of the printed PDF, which is where the last defect was: the print block still said `align-items:start` and the identifiers printed as superscripts. **The check found the same defect on this repository's own reference deck, five times**, which no amount of fixing the adopter's deck would have reached. Lessons **L-112** and **L-113**. |
