# Build mode

Load this at stage 6, once the slide-by-slide specification has been reviewed. It is **how a deck
gets written**; what makes a deck good is `${CLAUDE_PLUGIN_ROOT}/docs/DESIGN-SYSTEM.md`'s job and
nothing here repeats it.

**The input is a reviewed `<slug>.slides.md`, not a brief.** Nine fields per slide are already
decided. This stage composes them; it does not invent narrative.

---

## 1. Start from the shell, never from a blank file or another deck

Roughly 170 KB of every deck is the same deck — three embedded faces, the shared component block,
the script, the chrome, the reading view. It is not authored, it is assembled:

```
python ${CLAUDE_PLUGIN_ROOT}/tools/deck/shell.py new <slug>.html \
    --title "<the deck's name>" --subtitle "<one line: who, when, and any illustrative-subject note>"
```

That writes a deck with the shell in place and no slides. **Do not copy
`${CLAUDE_PLUGIN_ROOT}/examples/reference-deck.html` and edit it** — it is the structural reference,
and a copy carries twelve slides of someone else's content plus a `<style id="slides">` composition
written for them.

Then set the argument's stages, which the ruler and the printed contents page both render. They come
from the outline in `<slug>.foundation.md`, and they are declared in the deck's own script — the
three `var` lines at the top, `DECK`, `STAGES` and `STAGE_ICON`. Every stage icon must exist in
`${CLAUDE_PLUGIN_ROOT}/shell/icons.svg`; look at the set before choosing:

```
python ${CLAUDE_PLUGIN_ROOT}/tools/deck/shell.py icons --sheet <somewhere>.svg
```

**Never draw an icon** (DS-112). If the set has nothing for a concept, use the nearest one that is
honest rather than invent path data.

Then check the specification pair against itself, before any slide is written:

```
python ${CLAUDE_PLUGIN_ROOT}/tools/deck/spec.py <slug>.foundation.md <slug>.slides.md
```

It decides four things the two documents can only get wrong together — a slide citing a source the
foundation does not list, a listed source no slide uses, a slide with no `Sources` answer at all,
and a slide whose sources contradict the figure ledger. **A source nothing uses is either a missing
citation or a stale file**, and both are findings. Run it again after §4 writes a deviation back.

**A fifth verdict needs the built deck and waits for §5.** Given the `.html` as a third argument,
`SPEC-5` checks the ledger in the other direction: every slide a row's `Used on` names has to show
the row's value. Here it reports no subject, which is correct — there is no deck yet.

## 2. Write the slides, in batches of three

Three slides, then the loop in §3, then the next three. **Batching is not about scoring** — it is
that components are built once and reused, so a defect found in batch one is fixed once rather than
in twelve places.

Per slide, the parts and their attributes are `${CLAUDE_PLUGIN_ROOT}/docs/COMPONENT-CONTRACT.md`
§3.2–§3.8, and `component.py check` decides them. Read it before the first slide. Three things it
will not tell you, because they are this stage's judgement:

- **The `<style id="slides">` block is yours to write and it is the only CSS you write.** Composition
  goes there — a ledger's tracks, a stat's split, a closing slab. **The shared component block is not
  yours**: adding a rule to it is caught by `shell.py check`, and it means a second deck will inherit
  a layout written for this one.
- **Every value that could differ between themes is a token.** No colour, length, duration or easing
  curve outside the theme region; `theme.py check` fails one and names it under DS-010.
- **A diagram's ink starts where the slide's text starts.** The `<svg>` is already on the
  column — the shell puts it there — but the element is scaled to the content column, so the
  drawing lands wherever the viewBox puts it. **Set the viewBox so the leftmost drawn thing sits
  at its left edge**, and the diagram shares the grid the headline, the fragments and the bottom
  line are on. Getting this wrong is invisible until a row of text sits directly under the
  diagram, and then it reads as a step rather than a margin. `python tools/deck/figgrid.py <deck>`
  measures it; it reports rather than gates, because the decks written before this rule do not
  pass it yet (T-184).
- **A decision node carries its label inside itself.** Use `.decision` — a `<g>` holding one
  `.decision-shape` path and its `.decision-label` text — and **size the rhombus from the label**,
  which is arithmetic only the build can do because SVG cannot grow a path to fit text. An
  axis-aligned text block of half-width `w` and half-height `h` fits half-diagonals `A`, `B` when
  `w/A + h/B <= 1`; leave margin rather than landing on 1.0. Branch labels stay outside on their
  edges as `.decision-branch`, which is **a `.lab` in every respect** — so whatever the slides
  block does to `.lab` it does to `.decision-branch` in the same rule. A deck that steps `.lab` up
  a size and leaves the branch label behind renders it smaller than the edge labels beside it, and
  DS-035 catches that only on a diagram whose viewBox scales *down* (T-184).
  **Never put the label under the shape and hope**: that was the only
  option before T-117 and it left the reader binding a caption to a rhombus by proximity, on one
  slide beside two branch labels already.
- **A `<marker>`, gradient or filter belongs in the slide that uses it** (DS-232). Every slide but
  the current one is `visibility:hidden`, and a hidden subtree paints nothing for a visible one to
  reference — so a marker defined once and reused across slides draws on exactly one of them,
  whichever you happen to be looking at. Define it again in each slide that needs it. The sprite is
  the exception: it sits outside every slide, which is why `<use href="#i-name">` is fine anywhere.
- **Tier two is a decision, not a leftover.** Every `.disc` declares its kind in `data-disc` —
  `derivation` · `scope` · `condition` · `instances`, and no fifth (DS-230). If what is behind the
  click is none of those four, it belongs on the slide or nowhere. A bottom line may never depend on
  a figure that lives only behind the click (DS-231).

**The provenance mark is rendered from the slide's `Sources` field, never invented here** (DS-105).
`none` is no mark at all, unless the deck is illustrative and the slide carries that note instead.
A mark that says the same thing on every slide of a deck resting on three documents is the defect
this field exists to end — it was true of both example decks until 2026-08-10.

**Every mark carries the glyph.** The count decides the *control*, and reachability decides the
*route to the source* — two questions, and reading the second off the first is what made a
one-source slide a bare title in the corner that its first reader took for a subtitle (T-103):

| Sources | Mark |
| :--- | :--- |
| One | `.sources.sources--one` — the glyph and the title, no button, the box open on the line |
| Two or more | the `.sources` control — glyph, label, and a box that opens below it |

**Type each source before you write its row.** Four kinds, closed, and the kind decides the glyph
and the only route the row may offer. Ask the questions in this order and stop at the first yes:

| Ask | Kind | The row is |
| :--- | :--- | :--- |
| Is it an `https://` URL? | external URL | `.sources-icon` on `link`, and an `<a class="sources-link">` |
| Is it a local document `quickview.py` admits? | renderable local document | `.sources-icon` on `file-text`, and a `.sources-open` beside its `.qv-src` template |
| Is it a local document it cannot admit? | unrenderable local document | `.sources-icon` on `file-text`, and **plain text — no route** |
| Does the slide rest on more than one? | multi-source | the *mark* takes `library`; every row inside is still typed by the three above |

**When you cannot decide, the row is plain text.** A guess costs the reader a control that does
nothing, or worse a link that resolves nowhere — and *never a dead link* is DS-105's hard half. The
three admission tests that settle rows two and three are `quickview.py`'s own, so the honest way to
ask is to run it: what it refuses is row three.

**A local file never becomes a link, however convenient.** The recipient double-clicks the deck on a
machine that has never seen your paths, so a `file://` href is dead on arrival — an authoring form
and a defect in a delivered deck, on the same footing as `linked` mode. Ship the quick view instead.

**The identifier is optional and bounded at six characters.** `D1`, `WP3`, `R5` help a reader match
a row to a document; anything longer is dropped rather than truncated, and the title keeps the room.
It goes in its own `.sources-id`, never inside the title — a title reading `D1 · Something` is one
string the colophon and the mark then have to agree about by hand.

**A deck with a colophon renders the same component there**, `.sources.sources--list` in the slide's
body, one row per source, each row typed and routed exactly as above. **It carries no instruction to
find the links on earlier slides**: that sentence is merely unhelpful on the stage and untrue in the
reading view and on paper, where there are no corners and nothing to open.

The markup for all of it is `${CLAUDE_PLUGIN_ROOT}/docs/COMPONENT-CONTRACT.md` §3.2 and §3.2.1, and
`component.py check` decides it.

**A batch that introduces a `<template>`, a `<canvas>` or a `getContext` changes what the deck's
capability preflight has to test** (DS-009), so re-derive it — the block is only correct for the
deck as it stood when it was written:

```
python ${CLAUDE_PLUGIN_ROOT}/tools/deck/shell.py preflight <slug>.html
```

`shell.py check` in §3 reports a stale block the way it reports a stale sprite, so a forgotten run
is a red check rather than a deck that fails silently on a browser nobody has.

Sync the sprite whenever a batch introduced an icon — it keeps DS-113 true by construction:

```
python ${CLAUDE_PLUGIN_ROOT}/tools/deck/shell.py icons <slug>.html --set <concept>=<lucide-name>,<concept>=<lucide-name>
```

**`--set` takes one comma-separated value, not one flag per icon.** Repeating the flag is refused
with a message saying so; it used to wire the first pair and drop the rest, which surfaced two steps
later as *icon `i-x` is used and nothing says which Lucide glyph it is*.

## 3. The per-batch loop

Run all five on the batch. The first two are cheap and catch the expensive mistakes.

```
python ${CLAUDE_PLUGIN_ROOT}/tools/deck/shell.py check <slug>.html
python ${CLAUDE_PLUGIN_ROOT}/tools/deck/component.py check <slug>.html
python ${CLAUDE_PLUGIN_ROOT}/tools/deck/theme.py check <slug>.html
python ${CLAUDE_PLUGIN_ROOT}/tools/deck/check.py <slug>.html [--sources <dir>] --quiet
python ${CLAUDE_PLUGIN_ROOT}/tools/deck/render.py shots <slug>.html --out <dir>
```

**If the deck names a transition, look at it too.** `render.py motion <slug>.html --into 1 --shots`
seeks the animations a navigation starts along one clock and writes a frame at each point, which is
the only way anything here can show you a transition part way through — headless produces no
frames, so nothing plays. It reports what does not play either: an animation whose computed style
does not move across the offsets never reached the element the CSS names.

**Pass `--quiet` to that fourth command and read the default without it.** A passing run prints its
notes and one line carrying the rule partition — 345 bytes instead of 17,581 — and a run that is
not passing prints everything either way, so the flag costs no diagnosis. Drop it when you want the
per-rule listing to read yourself; that listing is why the default is the default.

`--out` is optional and the default is right: shots, probes and measurements go to
`.assets-cache/deck/` **under the deck's own project**, never under the plugin. Add
`<slides>` before it — `0,4,6`, zero-based — to render a subset.

**If `shell.py check` reports `COMPONENTS differs` or `SCRIPT differs` on a deck you did not edit
there, the deck was built on an older release of this plugin.** That is not a defect in the deck and
there is nothing to hand-patch:

```
python ${CLAUDE_PLUGIN_ROOT}/tools/deck/shell.py sync <slug>.html
python ${CLAUDE_PLUGIN_ROOT}/tools/deck/shell.py sync <slug>.html --write
```

The first reports which regions move and confirms every per-deck region is untouched; the second
applies it. Run the first and read it — a deck one release behind and a deck whose shell someone
edited deliberately are the same bytes. `sync` fixes only the shared half: anything `check.py`,
`component.py` or `spec.py` reports is the deck's own content and stays yours.

**If either command reports `TOKENS`, the upgrade is not finished.** A release can add a theme token
that the shared block reads and the deck declares — the block is shell and `sync` installs it, the
declaration is a theme value in a per-deck region `sync` must never touch. So the sync succeeds and
`theme.py` then fails DS-013 on a token you never had the chance to declare:

```
python ${CLAUDE_PLUGIN_ROOT}/tools/deck/shell.py tokens <slug>.html
python ${CLAUDE_PLUGIN_ROOT}/tools/deck/shell.py tokens <slug>.html --write
```

The first names each token and the value the shipped theme gives it; the second adds exactly those,
in a marked block at the end of your theme region. It only ever **adds** — a token you already
declared is a value you chose, and nothing rewrites it. Change any of the written values afterwards
if this deck wants a different look.

Then score **S3 Encoding · S5 Craft · S6 Motion** on the batch's slides, per
`${CLAUDE_PLUGIN_ROOT}/docs/EVALUATION.md`. **And look at the shots.** A deck that passes every
check can still be a deck nobody can read; that is why the render step is in the loop and not at the
end.

**Batch loops do not count against the iteration cap.** The cap is 3 and it counts whole-deck
rounds — a four-batch deck counting batch loops would exhaust it before the deck existed.

## 4. When the specification cannot be built

A slide that will not fit the stage, or that a `hard` rule fails on, cannot be built as written.
**Resolve it here.** This stage holds implementation authority above the detailed specification, and
returning the decision to a user who cannot picture the outcome is not an option — nor is shipping a
non-conformant slide, nor looping on one.

Two obligations come with that authority, and the first is the one under pressure to produce a deck:

1. **Write the deviation back into the artifact it contradicts** — `<slug>.slides.md`, and
   `<slug>.foundation.md` too when the outline moved. Those files exist to be what a reader opens
   when the deck turns out wrong, which they are not if they record only the intent.
2. **Tell the user at delivery, as brief bullet points.** One line each, no rationale per item.
3. **Say which deviations are worth reporting back to htmldeck**, in one line at delivery. A
   deviation reading *built X instead of Y, because rule Z* is not only a decision this build made —
   it is a rule costing a reader something, written down by the one person positioned to notice, and
   it reaches nobody because it lives in a log the maintainer never sees. Two of the six needs in the
   first external review had been sitting in that project's own build log for weeks. Nothing here
   asks the user to file anything; the obligation is to say which entries are candidates rather than
   let a closed workaround look like a settled question.

**This is not the exit for everything.** `${CLAUDE_PLUGIN_ROOT}/docs/EVALUATION.md` §6.1 keeps its
two: **STALL** — a design decision wearing a finding's clothes — escalates, and **OSCILLATION** —
two rules genuinely in tension — stops and names them. Deviation authority is for what this stage
*can* resolve.

## 5. Delivery

Stop when `${CLAUDE_PLUGIN_ROOT}/docs/EVALUATION.md` §5 says the deck is done, not when it feels
finished. **Then run the specification pair once more, this time with the deck**, which is the only
point at which every slide it names exists:

```
python ${CLAUDE_PLUGIN_ROOT}/tools/deck/spec.py <slug>.foundation.md <slug>.slides.md <slug>.html
```

`SPEC-5` fails a `Used on` cell that names a slide not showing the value. It is not a per-batch
check: mid-build, half the slides it names have not been written, and every one of those would
report as missing.

Then hand over:

- **The deck and both specification files**, in the delivery directory, per
  `${CLAUDE_PLUGIN_ROOT}/skills/htmldeck/references/artifacts.md`.
- **The deviation bullets** from §4, if there were any.
- **What printing does and does not do** — three sentences, and
  `${CLAUDE_PLUGIN_ROOT}/skills/htmldeck/references/pipeline.md` has them. Say them once, at
  handover, never on the deck's own surface.
- **Which half was checked.** A run with no sources is presentation-only and has to say so; a
  presentation-only check presented as a clean pass is a false one. If such a run needed a figure, it
  ships marked as a placeholder for the author to replace, or it does not ship.

**A clean gate is not a good deck.** Five of the ten dimensions are invisible to every check above,
so the run is not over when the tools go quiet.
