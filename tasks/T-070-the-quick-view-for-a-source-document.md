---
id: T-070
title: The quick view — a source document rendered inside the deck
type: deliverable
status: done
phase: review
parent: null
blocked_by: [T-069]
related: [T-019]
work_package: v0.3
owner: the project owner
business_value: medium
effort: l
created: 2026-08-10
updated: 2026-08-10
deliverables:
  - tools/deck/quickview.py
  - shell/shell.html
  - shell/components.css
  - shell/deck.js
  - docs/COMPONENT-CONTRACT.md
---

# T-070 — The quick view: a source document rendered inside the deck

## 1. Specify

**Outcome**
A source cited by [`DS-105`](../docs/DESIGN-SYSTEM.md)'s provenance mark can open **inside the
deck** — a reading view of the source's content, carried in the file, needing no network and no
access to the author's filesystem.

**Why this one**
Requested by the owner on 2026-08-10 as the third of three link behaviours, alongside a local file
and an external URL. [T-069](T-069-extend-the-provenance-mark-to-multiple-sources.md) settles those
two on rule 1's existing precedent: a local-file link is an authoring form and a defect in a
delivered deck, and an external URL is legal because it needs network to follow rather than to
render. **That leaves the quick view as the only target that works unconditionally**, which is what
makes it worth building rather than a convenience on top of the other two.

**It is also the only one of the three that is not a rule change.** Local and external are decisions
about what DS-105 permits. This is a build-mode capability: something has to read a source document
and produce a displayable rendering of it, and nothing in this repository does that today.

**What makes it hard, stated before the work rather than discovered in it**
- **Size.** `docs/research/R5-assets-and-licences.md` measured a full 12-slide deck with three
  embedded faces, icons, a motion library and SVG diagrams at **192 KB**, and the shipping reference
  deck is 221 KB. Embedding is cheap for *fonts*; a set of source documents is a different order of
  magnitude and has no measured bound. **A measurement comes before a design here**, or the feature
  ships a deck nobody can email.
- **Fidelity is a claim, and the request already concedes it** — *"as it interpreted the original
  content to make it displayable"*. An interpreted rendering is a **derived artifact that asserts it
  represents a source**, which is DS-102's problem in a new place: a misrepresented source is a
  fabricated citation wearing a quick view. What the quick view promises about fidelity has to be
  written down and visible to the reader.
- **The reading view already exists and is not this.** `shell/` carries a reading view of the *deck*
  (`.doc`), which is the deck's own content re-laid-out. A source quick view is a second reading
  surface with a different subject, and **DS-136** says patterns are built once and reused — so
  whether these are one component or two is a design decision, not an implementation detail.
- **Licence and confidentiality.** Embedding a source copies it into a file that gets emailed. A
  deck built from a client's internal document would carry that document to everyone who receives
  the deck. **This is the one failure mode that is worse than not having the feature**, and the
  default has to be the safe one.

**Scope**
- In: reading a source into a displayable form, carrying it in the deck, and the surface that shows
  it.
- In: a measured size bound, on real source documents, before the design is fixed.
- In: what the deck tells a reader about fidelity, and what it tells an author about what they are
  about to embed.
- In: the three admission tests, and whichever types pass them — SVG, inert HTML, and Markdown or
  plain text at minimum.
- In: the DS-110 amendment and the gate change that enforces its boundary. It cannot be a separate
  task in practice — the boundary is a container this task's component defines, so the rule and the
  thing it is scoped to have to land together.
- Out: DS-105's text and the provenance component — [T-069](T-069-extend-the-provenance-mark-to-multiple-sources.md),
  which this is blocked by, because there is no point building a target for a mark whose form is
  undecided.
- Out: `.docx` and `.pdf`, which need a parser this repository does not have and **L-07** will not
  let it acquire. A separate task with a measured case behind it, not a widening of this one.
- Out: **video**. Settled as linked-never-embedded, which makes it DS-105's external-URL case
  rather than a quick view, and it needs nothing from here.

**Inputs**
- [T-069](T-069-extend-the-provenance-mark-to-multiple-sources.md) — the mark, its component, and
  which link targets are legal.
- [`docs/research/R5-assets-and-licences.md`](../docs/research/R5-assets-and-licences.md) — the
  192 KB measurement and the method that produced it, which is the method to reuse.
- [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) §4 — the existing reading view.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-102 on sourcing, DS-136 on building a
  pattern once, DS-001 on the one-file constraint the whole feature has to survive.

**Acceptance criteria**
- [x] A deck carrying quick views for its sources **opens offline by double-click and renders
      glitch-free** — the constraint the feature exists inside, checked rather than assumed
- [x] A measured size cost, on a real 12-slide deck with real source documents, stated as a number
      and a method someone else could re-run
- [x] The reader can tell a quick view from the source: what it promises about fidelity is on the
      surface, not in documentation
- [x] Embedding is **opt-in per source**, and an author is told what a deck will carry before it
      carries it — the confidentiality failure is the one that must not be reachable by default
- [x] The quick view and the deck's own reading view are one component or two, with the reason
      recorded (**DS-136**)
- [x] Every class it styles has a `COMPONENT-CONTRACT.md` row (**DS-229**)
- [x] **Each admitted type is admitted by the three tests, not by a list** — a type nobody
      anticipated is decided by running the tests, and one that fails is refused with which
      test it failed
- [x] Embedded HTML cannot alter the deck around it: demonstrated with a source that tries
      to, not asserted
- [x] **The gate fails a raster the build produced and passes one the quick view quotes** —
      demonstrated with a deck carrying both, so the boundary is shown rather than claimed.
      This is the criterion that decides whether DS-110 was narrowed or lost
- [x] Where a source exists as both vector and raster, the builder takes the vector form,
      and a deck carrying the raster of such a source is a defect the critique pass names

**Open questions**
- **Superseded 2026-08-10 by the owner — the format set is extended.** The original decision, kept
  here rather than edited away: *"Markdown and plain text, and no other format in this task,"* on
  the grounds that neither needs a parser **L-07** would forbid. **That reason does not carry over
  to the extension, and it does not resist it either** — SVG and HTML are text, and a raster is
  bytes to base64. None of them needs a dependency, so the extension is *cheaper* against L-07 than
  the `.docx`/`.pdf` alternative the original decision rejected. The set is now decided by the three
  admission tests below rather than by enumeration.
- **Settled 2026-08-10 — a type is admissible if it passes three tests, and the list is derived
  from them rather than written down.** *"…and other compatible types"* as an open clause is the
  shape this repository rejects everywhere else: DS-230's kinds are closed, and DS-000 makes a new
  value a ruleset change with a stated reason precisely so a vocabulary cannot grow by whoever
  needed something. So:
  1. **It embeds with zero external references** (**DS-001**), or it is not a quick view — it is a
     link, which DS-105 already handles.
  2. **It executes no script into the deck.** A source is evidence; evidence that can rewrite the
     argument around it is not evidence.
  3. **It keeps the deck inside the measured size bound** this task already requires.

  A type that passes all three is in without a further decision; one that fails any is out, or is
  a rule change with its reason. **SVG** passes all three and rule 3 already prefers it. **HTML**
  passes only when it is inert — see below. **Video** passes 1 and 2 and is entirely a question of
  3. **Raster** fails a rule rather than a test — see below.

- **Settled 2026-08-10 by the owner — DS-110 is *narrowed by scope*, and its force is unchanged
  everywhere it already applied.** The distinction is between what a deck **makes** and what it
  **quotes**, and it is the whole of the amendment:
  - **What the build produces stays vector, always.** No path through build mode may emit a raster.
    DS-110's reason is intact — a rasterised diagram cannot scale, theme or diff — and this is not
    relaxed, softened, or made conditional. **A deck that rasterises its own content is as much a
    defect after this change as before it.**
  - **A source may be quoted in the form it exists in**, raster included, and only inside the
    quick-view surface. A screenshot is frequently the only form a source has, and refusing it means
    the feature cannot show the commonest evidence there is.
  - **Vector wins wherever the source offers a choice.** Where a source is available as SVG, HTML or
    text *and* as a raster, the builder takes the vector form. Raster is the last resort, not a
    parallel option — *"until raster graphics is the only option"* is the owner's wording and it is
    a rule the builder obeys, not a preference it weighs.

  **The scope marker is what makes this enforceable rather than aspirational.** DS-110 is `auto`, so
  a check already scans for raster; after this it must tell *inside the quick view* from
  *everywhere else*. That needs a structural container the ruleset names and the component contract
  contracts — so the amendment cannot land before the component does, which is one more reason this
  task sits behind [T-069](T-069-extend-the-provenance-mark-to-multiple-sources.md).
- **Settled 2026-08-10 by the owner — video is linked, never embedded, and therefore is not a
  quick-view type at all.** It fails admission test 1 by decision rather than by measurement: a
  linked video is not carried in the file, so it is not a quick view — **it is the external-URL case
  DS-105 already handles**, and it needs nothing from this task. This *removes* scope rather than
  adding it, and it removes the one item that could have put a deck beyond emailing.
- **HTML is the one that can break its host.** A source's markup carries its own CSS, its own ids
  and possibly script, all of which land in the deck's document. It must be rendered **inert**, so
  test 2 is structural rather than a promise about the input. Deciding *how* is `plan`'s; that it
  must be inert is `specify`'s.
- **Settled 2026-08-10 by the owner — an overlay over the current slide, not a page.** Returning to
  the argument costs one dismissal, and the deck's slide count stops depending on how many sources
  it cites — which matters because slide count is a pacing decision and citation count is not.
  A `.doc`-style page would reuse more of what exists; it also interrupts more, and the thing being
  interrupted is the argument the source is supporting.

**N-1, from the first external deck — the need this task was already the answer to, arriving from
someone who had not read it.** Routed here 2026-08-11 by
[T-092](T-092-product-feedback-from-the-first-external-deck.md). A deck owner reviewing a finished
twelve-slide board deck said its source lines were useless: `D5 §2` names a document the reader
cannot identify and cannot open, and the reader was not the author. That is a scoping input rather
than a new requirement — it says which half of the quick view is load-bearing. **What the reader
wanted first was the document's title, not its contents**, and a title is available with none of
this task's machinery. Whatever the overlay ends up rendering, a mark that says only a slug fails
the need before the overlay is reached.

Two rules stand between a reader and the source today, both recorded as **U-01** and **U-02** in
[`../docs/DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) §2.2 and neither ruled on: DS-105
forbids a link that cannot be shown live, which a `file://` source beside the deck cannot be, and
DS-092's four-sentence bound on the mark cannot hold five sources carrying titles. U-01 is this
task's to close — the overlay is the other way to satisfy it, and the one that does not need a live
link at all.

## 2. Plan

**Where the content lives decides everything else, and the shell's own structure decides that.**
`shell.py` cuts the shell out of the reference deck in **ten named regions**; everything outside them
is invariant and `shell.py check` compares it byte for byte. So a per-deck quick view cannot be a new
region without changing that contract — but it does not need to be. The rendered source goes inside
the **slide that cites it**, in a `<template class="qv-src">` beside its `.sources-item`, which is
already per-deck content inside the `SLIDES` region. The **surface** — one empty overlay — is shell,
like the reading view and the chrome.

`<template>` is doing real work there and is not a wrapper: its content is inert by the parser's own
rules. Nothing inside it loads, renders, or runs until it is cloned, so admission test 2 is a
property of where the source sits rather than a promise about what the sanitiser caught.

**It also gives DS-110 the container its amendment needs.** *Inside a quick view* becomes
*inside `template.qv-src` or `.qv-body`*, which a check can decide by position rather than by
intent — the thing §1 said the scope marker has to be.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | The surface in the shell: the overlay, its type, its dismissal, and its precedence with the disclosure and the sources box | `shell/shell.html`, `shell/components.css`, `shell/deck.js` |
| 2 | The builder: read a source, run the three admission tests, render it inert, report what it will embed and what that costs **before** writing | `tools/deck/quickview.py` |
| 3 | Round-trip both shipped decks through the new shell, so `shell.py check` stays green and the two files stay one fact | `examples/reference-deck.html`, `examples/sort-window/sort-window.html` |
| 4 | Amend DS-110 by scope, and give every new class its contract row | `docs/DESIGN-SYSTEM.md`, `docs/COMPONENT-CONTRACT.md` |
| 5 | Teach the gate the boundary, and demonstrate both sides of it on one deck | `tools/deck/audit.py` |
| 6 | Measure: a real 12-slide deck with its real sources, before and after, stated as a method | The measurement, in §3 |
| 7 | Open the built deck offline and look at it, with the network down | §4, per CLAUDE.md rule 6 |

**Decided here rather than in `implement`, because a criterion asks for it: two components, one type
block.** `.doc` re-lays *this deck's own* content as a page you read instead of the slides; the quick
view is an overlay over the current slide showing *another document*. Different subject, different
lifecycle, different dismissal. What DS-136 requires is that the *pattern* be built once, and it is:
the overlay reuses the disclosure's precedence rule (**DS-137** — one thing open at a time), and the
reading typography is the `--doc-*` tokens, not a second set. Two components that share a type scale
is reuse; one component with a `data-kind` switch would be a component that is two things.

## 3. Implement

**Decisions & assumptions**
- **The rendered source lives in a `<template>` inside the slide that cites it** — 2026-08-11. Not a
  wrapper choice: template content is inert to the parser, so nothing in a source loads, renders or
  executes until the script clones it, and a `<script>` that arrived inside one does not run when
  cloned either. Admission test 2 becomes a property of *where the source sits*. It also keeps the
  shell's ten regions intact — the surface is shell, the content is the `SLIDES` region — and gives
  DS-110 a container a check can decide by position.
- **One template per source, a control on every mark that cites it** — 2026-08-11. `Throughput
  model` is cited by six slides. Six copies of one document would be the size cost this feature has
  to justify, spent on nothing; the script keys the templates by `data-qv` and every control finds
  the one copy.
- **The control is delegated from `document`, not bound per element** — 2026-08-11, and this came
  from looking rather than from design. `buildDoc()` clones every slide into the reading view *after*
  the handlers are bound, so the reading view's fifteen controls were buttons that did nothing — in
  the view where the deck is read alone, which is exactly the reader who wants the source. The
  overlay went `position:fixed` with it, because the reading view scrolls.
- **What the sanitiser removes is reported, not absorbed** — 2026-08-11. A quoted source that
  quietly lost three elements is a rendering that misrepresents its original, which is DS-102's
  problem wearing a quick view. `plan` prints one line per category removed.
- **The vector-over-raster clause is named in `critique.md`, not carved into its own rule** —
  2026-08-11. It is not decidable from the deck: the gate cannot know what sat beside the source on
  disk. The rival was a new `hard` `judge` rule (`DS-232`), which would have put it on the critique
  worksheet by construction — rejected on cost rather than on merit, because a new rule moves the
  ruleset counts that six documents state and `figures.py` would then walk the whole set. Recorded
  here so the choice is visible: if the clause needs an ID later, the work is the counts, not the
  rule.
- **`--scrim` is the one new token**, and `--qv-w` was not needed — the quick view's measure is
  `--doc-measure`, which is the same decision the reading view already made about comfortable
  reading width.

**Two defects this found in itself, both by running it rather than reading it**
- **The sanitiser stripped tags and left their bodies.** `<style>` vanished and its rules stayed
  behind as text, followed by an orphan `</style>`. The pattern ended at `</\1>|/?>` and `.*?` took
  the shorter branch — the opening tag's own `>`. Found by embedding a hostile source and reading the
  template that landed in the deck (**L-01**). The fixture now asserts in the terms that failed: the
  *body text*, not the tag.
- **`stem()` again, one file over.** Not this task's, but the same shape: `figures.py`'s new artifact
  rule went green having judged half its units. Noted here because it is the second instance in two
  tasks, and the transferable half is in T-088.

**The measurement — a real 12-slide deck with its real sources**

| | bytes | |
| :--- | ---: | :--- |
| `examples/sort-window/` before | 233 143 | 12 slides, 3 sources cited 15 times |
| after, carrying all three sources | 242 699 | +9 556, **+4.1%** |
| the sources themselves | 7 167 | Markdown, rendered to inert HTML |
| the controls and templates around them | 2 389 | 15 controls, 3 templates |
| the bound | 2 097 152 | half of the smallest attachment limit still in wide use |

**The method, so it can be re-run:** `quickview.py plan` prints the deck's size before, each
source's rendered cost, and the total after, without writing anything;
`quickview.py list <deck>` prints what a deck already carries. The deck stays inside a mail
attachment by two orders of magnitude, which is the answer to §1's *"a measurement comes before a
design here"* — for text sources. A raster source is the case that could still spend the bound, and
the bound is enforced rather than advisory: past it, nothing is written.

**Outputs produced**
- [`../tools/deck/quickview.py`](../tools/deck/quickview.py) — the builder: the three admission
  tests, the Markdown renderer, the sanitiser, the wiring, `plan` / `add` / `list`.
- [`../shell/shell.html`](../shell/shell.html), [`../shell/components.css`](../shell/components.css),
  [`../shell/deck.js`](../shell/deck.js) — the surface, its type, its dismissal, its print rule.
- [`../themes/quarto.css`](../themes/quarto.css), [`../themes/lattice.css`](../themes/lattice.css),
  [`../docs/THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) — `--scrim`.
- [`../docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-110 narrowed by scope.
- [`../docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) — eleven rows and why the
  `<template>` is the rule rather than a wrapper.
- [`../tools/deck/audit.py`](../tools/deck/audit.py) — `ds110_no_produced_raster`, and the fixture
  that shows both sides of the boundary.
- [`../skills/htmldeck/references/critique.md`](../skills/htmldeck/references/critique.md) §4 — the
  vector-over-raster finding no check can reach.
- Both shipped decks, round-tripped through the new shell; `examples/sort-window/` carries its three
  sources.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A deck carrying quick views opens offline by double-click and renders glitch-free | met | `examples/sort-window/` opened from `file://` with the network irrelevant — the gate's DS-001 row is what makes that a property rather than a hope, and it passes. Opened, exercised and read: the overlay opens from a slide and from the reading view, Escape closes it, advancing closes it, the sheet fits the viewport (638 of 720 px) and the console is clean. |
| A measured size cost on a real 12-slide deck with real sources, stated as a number and a method | met | The table in §3. **+9 556 bytes, +4.1%**, three real Markdown sources cited across fifteen marks; the method is `quickview.py plan`, which reports before/after without writing. |
| The reader can tell a quick view from the source | met | `.qv-note` is part of the component and sits in the header of every quick view: *rendered from the source and carried in this deck. Not the original file.* It spans both grid columns so a long title cannot push it out of sight. |
| Embedding is opt-in per source, and the author is told what a deck will carry before it carries it | met | `plan` is the default posture and writes nothing; `add` is the exception. Each source is named individually — there is no *embed everything* — and the run prints its rendered cost and every category the sanitiser removed before a byte is written. The failure this guards is a client's internal document reaching everyone who receives the deck, which is why the safe direction is the default one. |
| The quick view and the reading view are one component or two, with the reason | met | **Two, sharing one type scale**, decided in §2 and recorded in `components.css` and the contract: `.doc` re-lays this deck as a page, `.qv` shows another document over the current slide. What DS-136 requires is that the pattern be built once, and it is — the precedence rule is the disclosure's (DS-137) and the typography is the `--doc-*` tokens. |
| Every class it styles has a `COMPONENT-CONTRACT.md` row (DS-229) | met | Eleven rows, and DS-229 caught two mistakes on the way: `shell`/`build` are not sources in that document's vocabulary (`author` means *markup in the file*, whoever wrote it), and `.qv` is a root like `.viewport`, not a child of `.body`. `component.py check` is clean and `check.py` reports `0 failure(s)` on both decks. |
| Each admitted type is admitted by the three tests, not by a list | met | `render()` dispatches on what a type *is*: text and Markdown render, SVG and HTML render after being made inert, raster embeds as a data URI, and anything failing a test is refused **naming the test** — `test 1 (zero external references, DS-001)`, `test 2 (executes no script)`, or the size bound, which refuses at the deck level and writes nothing. |
| Embedded HTML cannot alter the deck around it: demonstrated, not asserted | met | A hostile source was written and embedded: a `<style>` hiding every slide, a `<script>` rewriting the stage, a `<div id="stage">` colliding with the deck's own id, and a `javascript:` link. The template that landed in the deck carries the two paragraphs and nothing else; the run reported all four neutralisations. **The first attempt failed this test** — the tags went and their bodies stayed — and that is what the demonstration was for. Verified at the file level and by fixture; the browser pane would not load a second local file to re-check it rendered, so the rendered check is the shipped deck's, not this one's. |
| The gate fails a raster the build produced and passes one the quick view quotes | met | One raster, two decks, the real gate: in a slide's body → `DS-110 … FAIL`, `1 failure(s)`; the same bytes inside `template.qv-src` → `DS-110 … pass`, `0 failure(s)`. `audit.self_test` holds both halves plus the mixed case, so the narrowing cannot quietly become a loss. |
| Vector wins where a source offers both, and a raster of such a source is a defect the critique pass names | met | The builder refuses a raster whose vector sibling exists, by name: *`x.svg` exists beside it, and where a source offers a vector form the builder takes it.* The half no check can reach — whether a vector form existed at all — is `critique.md` §4, stated as the reason it is there. |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-11 | (shipped) | **Shipped in `0.2.1`.** The quick view reaches an adopter for the first time here; the release note describes it as sources opening inside the deck. |
| 2026-08-11 | → done | All ten criteria met. **The template is the design decision**: a rendered source sits in `<template class="qv-src">` inside the slide that cites it, which makes admission test 2 a property of where the source sits rather than a promise about the sanitiser, keeps the shell's ten regions intact, and gives DS-110's amendment a container a check decides by position. Measured **+4.1%** on the real 12-slide deck carrying three real sources - two orders of magnitude inside a mail attachment - and the bound refuses rather than warns. Two defects found by running it and not by reading it: the sanitiser stripped tags and left their bodies, and the reading view's fifteen controls were dead because `buildDoc()` clones the slides after the handlers bind. The vector-over-raster clause went to `critique.md` rather than becoming `DS-232`, on cost - a new rule moves the ruleset counts six documents state - and that trade is recorded rather than left to be re-derived. |
| 2026-08-10 | (specify) | **Moved to `v0.3`** under the release split set by the owner 2026-08-10. Estimates unchanged: `l` and a new capability is the definition of the later phase, and this task's own raising note already called it *the largest thing on the v0.2 board and the least certain to be worth it*. |
| 2026-08-10 | (specify) | **Both owner questions closed.** *Raster:* DS-110 is narrowed by **scope**, not by force — the build may never emit a raster, and that half is untouched; a source may be *quoted* as raster inside the quick view only; and where a source offers both forms the builder takes the vector one. The enforceable part is a structural container the gate can key on, which is why the amendment cannot land before the component and is kept in this task rather than split out. *Video:* **linked, never embedded** — which drops it from this task entirely, since a linked video is DS-105's external-URL case and not a quick view. That removes the one admitted type that could have put a deck beyond emailing. |
| 2026-08-10 | (specify) | **Format set extended by the owner: HTML, video, PNG, SVG "and other compatible types".** Recorded as three **admission tests** rather than a list, because an open-ended clause is the shape DS-230 and DS-000 exist to prevent — embeds with zero external references, executes no script into the deck, stays inside the measured size bound. SVG passes outright. **PNG collides with DS-110 — *No raster images. Ever.*, `hard` and `auto` — so a deck carrying one fails `check.py` today**; recommended as a quick-view-scoped exception, and it is the owner's. Video is unlegislated and is entirely a size question. HTML is the one that can break its host and must be inert structurally. The superseded decision is kept verbatim in §1 rather than edited away. |
| 2026-08-10 | (specify) | **Both open questions settled by the owner**, as recommended: Markdown and plain text only, and an overlay rather than a page. The cost of the format decision is recorded rather than smoothed over — for a while the quick view will not open the formats most real source material uses, so the mark falls back to plain text or a URL more often than not. Still blocked by T-069. |
| 2026-08-10 | → proposed | Split from the owner's provenance request as the part that is a **capability rather than a rule**. Blocked by [T-069](T-069-extend-the-provenance-mark-to-multiple-sources.md): the mark's form decides what a quick view is a target *of*. Four hazards written down before any work — unmeasured size against a 221 KB shipping deck, fidelity as a DS-102-shaped claim, a second reading surface against DS-136, and **embedding a confidential source into a file that gets emailed**, which is the one outcome worse than not building this. `l` and `medium`: the largest thing on the v0.2 board and the least certain to be worth it, which is exactly the pair that should not be started before T-069 answers what it is for. |
