# htmldeck — the component contract

**What markup a deck is made of, and what a generator has to emit to make one.** The rules that
decide whether an interaction is any good are [`DESIGN-SYSTEM.md`](DESIGN-SYSTEM.md)'s; the values
that make it look like this deck are [`THEME-CONTRACT.md`](THEME-CONTRACT.md)'s. This file says only
**which elements exist, where they sit, how many of them there are, and what they carry.**

It exists because [T-002](../tasks/T-002-build-mode-the-self-contained-deck-generator.md) has to emit
a deck and there was nothing to emit *against*. The technique was never the gap —
[`../examples/reference-deck.html`](../examples/reference-deck.html) has run ten disclosure sets, a
ruler, four named motions and 63 staggered entrances since T-028. **The contract was the gap**, and
the measurement that opened this half of [T-016](../tasks/T-016-the-interaction-and-motion-layer.md)
is what its absence was worth: *markup contract a generator could emit — none written.*

```
python tools/deck/component.py parts                     # this document, as data
python tools/deck/component.py check <deck>              # a deck against it
```

---

## 1. A component is a rule in the shared block

**The deck has three style regions and the boundary between them is what makes this document
short.** They are not three ways of writing CSS; they are three different owners.

| Region | Owns | Contracted by |
| :--- | :--- | :--- |
| `<style id="theme">` | Every value a second theme would change. | [`THEME-CONTRACT.md`](THEME-CONTRACT.md) |
| `<style>` — the unnamed one | **The components.** Every element more than one slide can use. | this file |
| `<style id="slides">` | One deck's composition: a ledger with three tracks, a cost list, a closing slab. | nothing — a generated deck emits its own |

So **every class the shared block styles is a component**, and the completeness check is that
sentence run backwards: a class styled there and absent from the tables below fails the gate. That
is the same test `theme.py` applies to an undeclared custom property, and it exists for the same
reason — *an undocumented part is one a generator cannot emit.*

The converse does not hold, and one part proves it: `.disc-label` carries no rule of its own and is
still required, because the script reads it to build the reading view's headings. **A part with no
styling is still a part** — the boundary sets what must be contracted, not what may be.

**Why the boundary is drawn at the style block rather than by naming components.** Because a list
of components maintained by hand drifts from the deck the first time someone adds one, and nothing
notices. The `#slides` block is already the line this project draws between *look* and
*composition* ([`THEME-CONTRACT.md`](THEME-CONTRACT.md) §5); drawing the markup line in the same
place means one boundary is maintained, not two.

**Three classes in the shared block sit under a `.doc` scope and style composition, not
components** — `.doc .figwrap`, `.doc .stat-figure`, `.doc .ledger`. The reading view is a
different rendering of the same slides (DS-070), so it has to undo the stage's composition to
reflow it. Those rules belong to the reading view, and the classes they name stay `#slides`'.

## 2. What a row says

| Column | Means |
| :--- | :--- |
| **Part** | The class. This is the identity; the check finds elements by it. |
| **Element** | The tag it must be, or `—` where the deck uses several and none is required. |
| **Sits in** | The nearest **contracted** ancestor — not the immediate parent, which composition wrappers change. `on .x` instead means *a second class on the same element*: a modifier. `—` is a root. |
| **Count** | How many, **per instance of what it sits in**. `1` · `0-1` · `1+` · `0+`. |
| **Attributes** | Required on every instance. Absent ones fail; extra ones do not. `attr:text` additionally requires the value to contain `text`, which is how `style:--i` says *a `.rise` carries its stagger index* rather than merely *a style attribute*. `attr:a/b/c` instead requires the value to be **one of** the listed alternatives — a closed set, which is how `data-disc` carries DS-230's four editorial kinds and no fifth. `attr:#NAME` requires a **zero-based index into the deck's own `var NAME = [...]`** — a range this document cannot enumerate, because its length is a per-deck fact written in the deck. |
| **Source** | Who writes it — §2.1. |

### 2.1 The four sources, and what each one is checked for

**A static scan can only see what the author wrote**, so the column exists to stop the gate
reporting a script's work as missing markup — and to stop *unused* being a shrug.

| Source | Means | Checked for |
| :--- | :--- | :--- |
| `author` | In the file as delivered. | Element, place, count, attributes. |
| `script` | The deck's own script creates it at runtime. | Its **rule** exists in the shared block; instances are not counted here. |
| `print` | Generated into `@media print` only. | The same, in the **print** block. |
| `vocabulary` | Styled, emittable, and **this deck contains none.** | **Zero instances** — one appearing means the row is misfiled and must become `author`. |

`vocabulary` is checked in the opposite direction on purpose. *Declared and unused* is otherwise
unfalsifiable, and the deck already carries the lesson: a stale `.ribbon button::before` survived
T-035 because **a rule that matches nothing looks exactly like a rule that passed**.

*The `script` and `print` rows above stated a check that did not exist until 2026-08-29 (`PR-34`,
closed by [T-242](../tasks/T-242-the-contracts-against-the-checkers-that-decide-them.md)). The
structural pass skips both sources, and the completeness pass runs the other way — it iterates the
**styled** classes and asks which have a row — so a contracted class with no rule at all was
examined by nobody, in exactly the shape `vocabulary`'s reason describes. Four rows carry the two
sources and all four happen to be styled, which is why nothing had surfaced; `component.py` now
decides it, and the count of rows travels with the verdict so* 0 problems *over four rows and over
none are not the same fact.*

**No row below is `vocabulary` today, and that is the correct number rather than a gap.** Five were
until 2026-08-12, and every one of them turned out to be a class this document defines *for a deck
to use* — so the source was asserting something about the reference deck and enforcing it against
everybody else's (T-105). The source stays defined for the case it is actually for: a class the
shared block styles that a deck must **not** author. A row only earns it by being that, never by
being unused so far.

---

## 3. The components

### 3.1 The stage

| Part | Element | Sits in | Count | Attributes | Source |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `.viewport` | `div` | — | `1` | `id` | author |
| `.stage` | `main` | `.viewport` | `1` | `id` `aria-label` | author |
| `.sr` | — | — | `1+` | — | author |
| `.contents` | `div` | — | `0+` | — | print |
| `.preflight` | `div` | — | `1` | — | author |
| `.preflight-say` | `p` | `.preflight` | `1` | `id` | author |

**`.preflight` is the only part that ships visible and is hidden by script rather than the other way
round** (DS-009). It carries what a recipient reads when the deck cannot present itself — no
JavaScript, or a capability the preflight named — and the marker that reveals it is authored on
`<html>`, so it is what an unsupported browser paints rather than what one is switched to.

### 3.2 The slide

Every slide is a `<section>` (DS-080) and carries its own name, its stage and an accessible label;
the ruler and the printed contents page are both **renderings of those attributes**, so a slide
that omits one goes missing from the navigation rather than looking wrong.

**`data-stage` is the stage's position, not its name.** `deck.js` subscripts `STAGES` and
`STAGE_ICON` with it, so `data-stage="2"` is the third stage the deck declares and
`data-stage="Problem"` is nothing at all — a deck written that way opens, renders and reads
correctly, and has no ruler and no arrow keys. It said only `data-stage` here until 2026-08-12, and
the reference deck was the sole place the value was written down (T-102).

**Two values are not positions: `data-stage="back"` and `data-stage="front"`.** `back` marks a slide
as **back matter** — outside the argument rather than late in it — and a colophon, an appendix, a
sources page or a glossary may carry it. `front` marks a **lobby** (DS-242), the slide an audience
looks at while the room fills. Nothing else may be either: a slide the reader is meant to be argued
*to* is in a stage, however near the beginning or the end it sits. What they change, in every
rendering of the manifest at once:

| | A slide in a stage | `data-stage="back"` | `data-stage="front"` |
| :--- | :--- | :--- | :--- |
| Ruler tick | a section tick where it opens a stage | never a section tick | never a section tick |
| Ruler label at rest | the stage's name | **the slide's own name** | **the slide's own name** |
| Ruler label on hover | the slide's name | unchanged | unchanged |
| Any stage's slide count | counted | counted in none | counted in none |
| Contents box label | the stage's name | `Back matter` | `Front matter` |
| Contents box mark | the stage's mark | **none** — DS-113/114 key the mark to the stage, and there is no stage | **none**, for the same reason |

**The two differ in exactly one row, the contents box label**, and that is the whole of the
difference — `deck.js` binds them together as a `matter` flag and every other site reads the flag
rather than either value. *The sentence above read `back` is the one value that is not a position
until 2026-08-29, thirty-four lines before this section's own note granting `front` the same
standing. `PR-39`, closed by [T-242](../tasks/T-242-the-contracts-against-the-checkers-that-decide-them.md).
**Stated as a table with a column rather than as a corrected sentence**, because a third value would
need the sentence corrected again and needs only a column here.*

The constant is the shell's rather than the deck's because there is no stage entry to read a word
from, and *Back matter* is true of all four of the things that may carry it where *Colophon* is true
of one. **The absent mark is the rule holding, not a gap.** Added by
[T-108](../tasks/T-108-a-deck-has-no-back-matter-stage-so-the-colophon-is-labelled-with-the-last-argument-stage.md);
before it, back matter had to declare an argument stage, and this repository's own reference deck
invented an eighth one — with `STAGE_ICON` left at seven, so the colophon's contents box printed
with a mark that referenced nothing.

| Part | Element | Sits in | Count | Attributes | Source |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `.slide` | `section` | `.stage` | `1+` | `data-name` `data-stage:#STAGES` `aria-label` | author |
| `.eyebrow` | `p` | `.slide` | `1` | — | author |
| `.tick` | `span` | `.eyebrow` | `1` | — | author |
| `.headline` | `h2` | `.slide` | `1` | — | author |
| `.standfirst` | `p` | `.slide` | `0-1` | — | author |
| `.body` | `div` | `.slide` | `1` | — | author |
| `.bottom-line` | `p` | `.slide` | `1` | — | author |
| `.bottom-line--center` | — | `on .bottom-line` | `0+` | — | author |
| `.provenance` | `p` | `.slide` | `1` | — | author |

*One scoped exemption, and the only one in this table: a slide with `data-stage="front"` — a lobby (DS-242) — carries no `.provenance`. The mark says what the argument rests on, and front matter is not the argument; it is DS-225's *back matter carries no mark* at the other end. **It names one part and one stage on purpose.** DS-085 warns that a slide kind allowed to relax the contract hands the next slide kind the same argument, so everything else on a lobby is the ordinary contract — header, body, one bottom line. Added 2026-08-20 by [T-200](../tasks/T-200-add-a-lobby-slide-and-count-the-argument-not-the-file.md).*

| `.sources` | `span` | `.slide` | `0-1` | — | author |
| `.sources--one` | — | `on .sources` | `0+` | — | author |
| `.sources--list` | — | `on .sources` | `0+` | — | author |
| `.sources-btn` | `button` | `.sources` | `0-1` | `aria-expanded` `aria-controls` | author |
| `.sources-mark` | `svg` | `.sources` | `0-1` | `aria-hidden` | author |
| `.sources-label` | `span` | `.sources-btn` | `1` | — | author |
| `.sources-box` | `span` | `.sources` | `1` | `id` | author |
| `.sources-item` | `span` | `.sources-box` | `1+` | — | author |
| `.sources-id` | `span` | `.sources-item` | `0-1` | — | author |
| `.sources-icon` | `svg` | `.sources-item` | `0-1` | `aria-hidden` | author |
| `.sources-link` | `a` | `.sources-item` | `0-1` | `href` | author |
| `.sources-open` | `button` | `.sources-item` | `0-1` | `type` `data-qv` `data-file` | author |
| `.qv-src` | `template` | `.sources-item` | `0-1` | `data-qv` | author |
| `.qv` | `div` | — | `1` | `id` `hidden` `role` `aria-modal` `aria-labelledby` | author |
| `.qv-sheet` | `div` | `.qv` | `1` | — | author |
| `.qv-head` | `header` | `.qv-sheet` | `1` | — | author |
| `.qv-title` | `p` | `.qv-head` | `1` | `id` | author |
| `.qv-file` | `p` | `.qv-head` | `1` | `id` | author |
| `.qv-note` | `p` | `.qv-head` | `1` | — | author |
| `.qv-close` | `button` | `.qv-head` | `1` | `id` `aria-label` | author |
| `.qv-body` | `div` | `.qv-sheet` | `1` | `id` | author |
| `.qv-doc` | `article` | `.qv-body` | `0-1` | — | script |
| `.qv-href` | `span` | `.qv-doc` | `0+` | — | author |

**The multi-source mark is `<span>`s inside the `<p>`, and that is a parser constraint rather than a
preference.** A `<div>` inside a `<p>` is closed by the HTML parser, so a box built that way would
sit **outside** the mark in the DOM while looking correct in the file — the deck would lose DS-223's
print placement without anything appearing wrong. Keeping the box inside `.provenance` is also what
keeps that row at `1`: a slide has one provenance mark, and what changed is what the mark may
contain.

**`.sources-item` is `1+`, and since 2026-08-12 a one-item box is the point rather than a
pointless design.** The mark has three shapes and the two modifiers name which:

| | `.sources-btn` | `.sources-mark` | `.sources-box` | Reads as |
| :--- | :--- | :--- | :--- | :--- |
| Two or more sources | the control, labelled | the knowledgebase glyph | shut at load, opens below the mark | a disclosure (DS-138) |
| One source, `.sources--one` | **absent** | that source's kind glyph | always open, on the line | the provenance line itself |
| The colophon, `.sources--list` | **absent** | **absent** | always open, one row per line | the slide's whole body |

So `.sources-btn` is `0-1` and `.sources-mark` sits in `.sources` rather than in the button: **the
glyph is what a reader recognises, and at one source it is the whole affordance.** A slide resting
on one source used to be a bare uppercase title in the corner, which the owner of the first
adopting deck read as a subtitle and said so (T-103). The box survives at one source because it is
where `.sources-link` and `.sources-open` live — a single **local** source keeps its route to the
quick view, which it had no way to reach while the route ran through a control it did not get.

### 3.2.1 What kind of thing a source is, and the route that follows

**Four kinds, closed.** A source reference is one component wherever it appears, and the kind decides
both the glyph and the only route the reference may offer:

| Kind | `.sources-icon` glyph | The route in `.sources-item` | Which part carries it |
| :--- | :--- | :--- | :--- |
| External URL | `link` | opens in a new tab | `.sources-link` with an `https://` href |
| Renderable local document | `file-text` | opens the quick view this deck carries | `.sources-open` |
| Local document the quick view cannot admit | `file-text` | none | plain text in the `.sources-item` |
| More than one source on the slide | `library` | opens the box, each row typed as above | `.sources-btn`, and the rows below it |

**The fourth kind is the mark's, not an item's** — it types the slide rather than a document, so it
appears on `.sources-mark` and never on `.sources-icon`. A slide citing two documents shows the
knowledgebase glyph in the corner and a file glyph on each row inside. Showing the single-source
glyph on a multi-source mark is the defect this row closes: it read as one document and gave a count
where the reader wanted to know which two.

**`.sources-icon` is `0-1` because a one-source mark already carries the kind.** At `.sources--one`
the `.sources-mark` *is* the item's glyph, and a second copy of it on the same line says nothing
twice. The item carries its own glyph exactly where the mark cannot speak for it — inside a
multi-source box, and in the colophon.

**`.sources-link` is DS-105's link clause, and the clause is about reachability rather than
count.** A source reachable from where the deck is presented is a working link at any number of
sources; one that is not is plain text, or a `.sources-open` where a quick view can carry it.
Never a dead link, and a `file://` href is an authoring form rather than a shipping one. **A local
file is therefore never row one**, however tempting: the recipient double-clicks the deck on a
machine that has never seen the author's paths, so the href is dead on arrival (rule 2, DS-105).

**`.sources-id` is `0-1` and the bound is six characters.** An identifier helps a reader only while
it is short enough to read as a label rather than as text — `D1`, `WP3`, `R5`, `T-109`, `§3.2` are
all six or fewer. **Above six it is dropped rather than truncated**, and the title keeps the room: a
truncated identifier is worse than none, because it looks like a reference the reader could resolve.
The number lives here rather than in the build, because a bound decided per deck is not a bound.

**`.sources` sits in `.slide` at `0-1`, and that is wider than it looks.** It reads as *a slide
declares its sources once* — in its provenance mark on an argument slide, in its body on the
colophon. It was `.provenance` until 2026-08-17, which is what forced the colophon to author a
private list of bare titles with no icon and no route
([T-109](../tasks/T-109-one-source-reference-component-rendered-in-three-places.md)); the slide whose
whole purpose was the sources was the one slide that routed to none of them, and its bottom line sent
the reader back through twelve slides to find marks it could have carried itself. **`.sources--list`
is that fix and nothing more** — the same items, the same routes, laid out as the body instead of as
a corner.

**A colophon row carries `.sources-open` and no `.qv-src` of its own.** The script keys its template
map off `data-qv` across the whole stage, so the row resolves to the template the citing slide
already carries. Five documents quoted twice would be the size cost this feature has to justify,
spent on nothing.

**The quick view is two components' worth of rows for one reason: the surface is the shell's and
the content is the deck's.** `.qv` and everything under it ship empty in `shell/shell.html`, like the
chrome and the reading view — a deck carrying no quick view still carries the surface. What varies
per deck is `.sources-open` and `.qv-src`, and both sit inside the `.sources-item` for the source
they belong to, because the provenance mark is where a reader asks the question. All of them are
`author` in this table's vocabulary, which distinguishes **markup in the file** from markup a script
creates — `tools/deck/quickview.py` writes two of them and that does not make them a third kind.

**`.qv-src` is a `<template>` and the element is the rule, not a wrapper choice.** Its content is
inert to the parser: nothing inside it loads, renders or executes until the script clones it. That
is what makes T-070's second admission test — *a source executes no script into the deck* — a
property of where the source sits rather than a promise about what a sanitiser caught. A `<div
hidden>` would look equivalent and would load every image in it.

**`.qv-file` names the source file and `.qv-title` names the document**, which are two different
answers to *what am I reading*. The title is the deck's own name for the source and is what the
reader recognises; the file name is what they type to find the original outside the deck. It ships
in `shell.html` as an empty `<p>` the script fills from the control's `data-file`, and stays empty
where the source has no file — a deck citing an external URL has nothing to put there.

**`.qv-doc` is `script` and not `build`**, because the article is created when a quick view is
opened. What the build writes is the template's *contents*; the container the reader sees is the
script's, like `.doc`'s sections.

**`.sources` is not a `.disc` and must not be counted as one** — see DS-105 and DS-230. It shares the
disclosure interaction rules and none of its vocabulary, which is why it is contracted here beside
the mark it belongs to rather than in §3.3.

**`.headline` sits in the slide, not in its header, and that is measured rather than tidied.**
Eleven of the twelve put it in `<header>`; the closing slide puts it inside `.body` so the ask can
be set large and centred. Writing `header` into this row would make the contract describe eleven
slides and fail the twelfth, which is the deck it was extracted from.

### 3.3 Disclosure

The component §5.3 governs, used ten times. **The panel's `id` is the button's `aria-controls`**,
and both sit inside one `.disc` — three facts a generator gets wrong independently, and the last
one silently: a panel wired to a button on another slide still opens.

| Part | Element | Sits in | Count | Attributes | Source |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `.disc` | `div` | `.slide` | `0-1` | `data-disc:derivation/scope/condition/instances` | author |
| `.disc--edge` | — | `on .disc` | `0+` | — | author |
| `.disc-btn` | `button` | `.disc` | `1` | `aria-expanded` `aria-controls` | author |
| `.disc-mark` | `span` | `.disc-btn` | `1` | `aria-hidden` | author |
| `.disc-label` | `span` | `.disc-btn` | `1` | — | author |
| `.disc-panel` | `div` | `.disc` | `1` | `id` `hidden` | author |
| `.row` | `div` | `.disc-panel` | `1+` | — | author |
| `.k` | `span` | `.row` | `1` | — | author |
| `.opening` | — | `on .disc-panel` | `0+` | — | script |
| `.disc-lead` | `p` | `.doc` | `0+` | — | script |

`.disc-label` is the rule DS-164 turns on — the control's real label, as against the mark beside
it, which is `aria-hidden` because it says the same thing to the eye only. `.disc-lead` exists
because the reading view renders every panel open with no control above it (DS-073), so the label
that was on the button has to become a heading or the panel arrives unannounced.

**`data-disc` carries the panel's editorial kind, and it was a valueless attribute until
2026-08-09.** The four values are DS-230's — `derivation` · `scope` · `condition` · `instances` —
and **that rule owns what they mean**; this table owns only that one of them is written and no
fifth is invented, which is all a parser can decide. The set is closed here for the reason DS-140's
is: an open list is a name for whatever went behind the click. The script selects on `[data-disc]`,
presence and not value, so the kind reaches the gate and the critique pass without reaching the
runtime. **Like `data-scale` on the ruler it is a claim rather than decoration** — the difference is
that `data-scale`'s claim is verified by the render gate and this one is verified by a person,
which is why DS-230 is `judge` and says so.

### 3.4 The chrome

One row, inside DS-217's budget. The ruler's ticks are **built from the slide manifest**, so they
are `script` here and their per-tick obligations — a name each, a uniform mark, a uniform pitch —
are DS-131's and DS-217's, measured in the render gate rather than read out of the file.

| Part | Element | Sits in | Count | Attributes | Source |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `.chrome` | `nav` | `.stage` | `1` | `aria-label` | author |
| `.navbox` | `div` | `.chrome` | `1` | — | author |
| `.ruler` | `div` | `.navbox` | `1` | `id` `data-ticks` | author |
| `.ruler-ticks` | `ul` | `.ruler` | `1` | `id` `data-scale` | author |
| `.ruler-ring` | `i` | `.ruler` | `1` | `id` `aria-hidden` | author |
| `.ruler-label` | `p` | `.ruler` | `1` | `id` `aria-hidden` | author |
| `.count` | `p` | `.navbox` | `1` | `id` `aria-hidden` | author |
| `.more` | `div` | `.chrome` | `1` | `id` | author |
| `.more-menu` | `div` | `.more` | `1` | `id` `hidden` | author |
| `.btn` | `button` | `.chrome` | `1+` | `id` | author |
| `.btn--pager` | — | `on .btn` | `1+` | — | author |
| `.is-back` | — | `on .btn--pager` | `0-1` | — | author |
| `.chev` | `span` | `.btn` | `0-1` | — | author |
| `.l` | — | `on .chev` | `0+` | — | author |
| `.r` | — | `on .chev` | `0+` | — | author |

**`.arrow-pop` and `.dot-pop` are content motions, and they sit on the figure rather than on what moves (T-112).** A `<marker>` renders in its own context and inherits from where it is *defined*, so a rank on the referencing line never reaches the arrowhead — and a matrix's dots interleave with its row labels, so they cannot be wrapped in one element without moving the labels. Both are therefore one motion per figure with one `--m-rank`, which is also the right unit: ranking each arrowhead separately would pop three of a diagram's five, and that is the incoherence DS-237 rejected for `rise`. A `.dot-pop` figure's dots each carry `--dp`, their place in the arrival order, derived by `tools/deck/density.py` and checked by it.

**What may sit in the navigation container, and what may not (T-114).** `.navbox` holds the
controls that answer *where am I, and how do I move*: the ruler, the counter, and the two pager
buttons. Nothing else may go in it. `Read` switches rendering and `Motion` switches playback —
neither is navigation, and both sit outside. The rule is not tidiness: the complaint that opened
T-114 was that the pager read as an afterthought, and the pager was not under-styled, it was in the
wrong company. A container that admits *the other chrome controls too* is the container that caused
it, so the boundary is stated as a closed list rather than as a principle to interpret.

`.navbox` is also what `rulerAvailableDu()` measures. Capacity is a property of the box the ruler
competes for width inside, and admitting one more control to the container silently spends the
ruler's targets — which is DS-217's bound moving without anyone editing DS-217.

**`.more`, and why it is not a `.disc`.** DS-230's tier-two vocabulary is closed at four kinds, and
a chrome menu is not content the face provokes a question about — so `More` is its own component,
on the footing DS-105 gives `.sources`. It obeys the disclosure *interaction* rules regardless: a
real label (DS-164), click rather than hover (DS-163), shut at load (DS-227), and one thing open at
a time (DS-137). Its menu opens **upward**, which satisfies DS-138 rather than excusing it: that
rule's first sentence binds every panel to open fully inside the stage, and its second fixes
*below* for tier two and the provenance box only. At the foot of a 1080-unit stage, up is the
direction that satisfies the first.

**Where `Motion` sits is decided at build time, and the gate reads it (DS-218, T-114 step 7a).** A
persistent stop control is what DS-218 asks for, and a control one click inside a shut menu is not
reachable while the motion runs. So `#motion` sits **inside `.more-menu`** in a deck with nothing
looping, and **as a sibling of `.more`** in a deck that loops. That is the `CHROME_TAIL` slot in
[`../shell/README.md`](../shell/README.md), and `audit.py` fails a looping deck whose control is in
the menu — the placement is a static fact about the built markup, which is the whole reason it is
decided at build time and not by the script.

**`.is-back` is on the Previous pager and nowhere else, and it exists so a motion can carry a direction.** T-112's pager tilt leans the control toward where it goes; without a class saying which of the two this is, both would lean the same way and the tilt would encode nothing, which is DS-150's test failed by a motion that looks fine. It is a modifier on `.btn--pager` rather than a match on `#prev`, because an id is a handle for the script and a class is what a stylesheet is allowed to know.

**The pager is exactly two, and the table says `1+` because the count vocabulary has no `2`.** `.btn--pager` is the row's only filled surface — the weight half of T-114's fix, where `.navbox` is the company half. Both were in the ruled sketch; the container is a drawn box and the pager is filled, and neither reads as the change on its own.

**`.btn` is bound to `.chrome`, not to its box, and that is a limit of this table rather than a
looser rule.** A chrome button has three possible parents now — `.navbox`, `.more` and
`.more-menu` — and the `Sits in` column holds one. The closed list above is the rule; what the
gate can currently decide is that a `.btn` is somewhere in the chrome.

**One consequence, stated because it is a cost rather than a feature.** The tail is a per-deck
region now, so `shell.py check`'s byte comparison no longer owns the `More`, `Read` and `Motion`
labels — a deck may reword them and the shell check stays green. What guards them instead is this
table, through `component.py`. The one-slot design was ruled on 2026-08-18; this is what it spends.

`data-scale` is a claim, not decoration: DS-217 counts a regular repeating scale as **one** item
rather than *n*, and the gate verifies the claim — uniform mark, uniform pitch, no per-item label
at rest — rather than trusting the attribute. `.ruler-ring` and `.ruler-label` are `aria-hidden`
because every tick already carries its own accessible name, and announcing the visible swap on
each focus move would say it twice.

### 3.5 The reading view

| Part | Element | Sits in | Count | Attributes | Source |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `.doc` | `article` | — | `1` | `id` `aria-label` | author |
| `.doc-inner` | `div` | `.doc` | `1` | — | author |
| `.doc-head` | `header` | `.doc-inner` | `1` | — | author |
| `.t` | `h1` | `.doc-head` | `1` | — | author |
| `.s` | `p` | `.doc-head` | `1` | — | author |
| `.viewswitch` | `button` | — | `1` | `id` | author |

The reading view's **body** is not in this table: it is a clone of the twelve slides, so its parts
are §3.2's and §3.3's, and contracting them twice would be two homes for one fact.

### 3.6 The figure

A diagram is drawn (DS-111), and it takes its colours from classes rather than from `fill=`
attributes, because a presentation attribute loses to any class rule and renders the wrong colour
(DS-214). These are that vocabulary. Every one of them is `0+`: which marks a figure uses is the
figure's business.

| Part | Element | Sits in | Count | Attributes | Source |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `.fig` | `svg` | `.slide` | `0+` | `viewBox` `role` `aria-label` | author |
| `.arrow-pop` | — | `on .fig` | `0+` | — | author |
| `.dot-pop` | — | `on .fig` | `0+` | — | author |
| `.lab` | `text` | `.fig` | `0+` | — | author |
| `.val` | `text` | `.fig` | `0+` | — | author |
| `.name` | `text` | `.fig` | `0+` | — | author |
| `.axis` | `line` | `.fig` | `0+` | — | author |
| `.grid` | `line` | `.fig` | `0+` | — | author |
| `.accent` | — | `.fig` | `0+` | — | author |
| `.accent-s` | — | `.fig` | `0+` | — | author |
| `.quiet` | — | `.fig` | `0+` | — | author |
| `.quiet-s` | — | `.fig` | `0+` | — | author |
| `.t-accent` | `text` | `.fig` | `0+` | — | author |
| `.t-soft` | `text` | `.fig` | `0+` | — | author |
| `.t-faint` | `text` | `.fig` | `0+` | — | author |
| `.t-paper` | `text` | `.fig` | `0+` | — | author |
| `.t-caution` | `text` | `.fig` | `0+` | — | author |
| `.t-ink` | `text` | `.fig` | `0+` | — | author |
| `.decision` | `g` | `.fig` | `0+` | — | author |
| `.decision-shape` | `path` | `.decision` | `1` | `d` | author |
| `.decision-label` | `text` | `.decision` | `1+` | — | author |
| `.decision-branch` | `text` | `.fig` | `0+` | — | author |
| `.pos` | — | `.fig` | `0+` | — | author |
| `.neg` | — | `.fig` | `0+` | — | author |
| `.caution` | — | `.fig` | `0+` | — | author |

**The decision node is one group, and that is the whole of T-117's first half.** `.decision-shape`
carries the rhombus and `.decision-label` the text inside it; the branch labels stay outside as
`.decision-branch`, because they belong to the edges leaving the node rather than to the node. Before
this there was no slot, so a build that wanted a labelled decision had to put the caption underneath
and hope the reader bound them — which two slides of a carefully built deck did, one of them next to
two branch labels already. **The shape's size is the build's arithmetic** (`build.md`), because SVG
cannot grow a path to fit text; what the contract fixes is that the label is *inside the group whose
centre it is placed on*, so the two cannot drift apart again.

**The three role classes were `vocabulary` until 2026-08-12, and the deck they were waiting for
arrived.** DS-026 fixes the positive, negative and caution roles deck-wide, and the reference deck
spends all thirteen of them in the ledger's `<b>` and `<div>` elements — `.ledger .pos` in the
composition block, a different rule to `.fig .pos` here — so the figure's copy of them was unused.
The note under the old rows said *a figure encoding a loss is the obvious next deck, which is why
the rows stay*; an adopting project then built exactly that deck and had to choose between drawing
the loss in red and passing the gate (T-105). `.t-ink` moved with them: it is the sibling of five
`author` text roles and would have failed the next deck to colour figure text explicitly.

**The chart-engine declaration is a figure part, and it lives in the head** (DS-122, T-202). A deck
whose charts the reader is expected to *interrogate* may carry an engine, and it says so once:

| Part | Element | Sits in | Count | Attributes | Source |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `htmldeck-chart-engine` | `meta` | `head` | `0..1` | `name` `content` | author |

`content` is four `key=value` pairs separated by `;` — **`engine`**, **`version`**, **`licence`**
and **`output`**. All four are required, `output` must be `svg`, and `licence` must be an SPDX
identifier whose terms permit redistribution inside a single file, which is the same test DS-032
applies to an embedded face. **A deck that declares nothing is held to the hand-authored default**,
which is where every deck this repository ships stands today.

**Why the head and not beside the chart.** Beside it is more local, and it was the alternative
considered. It loses on two counts: it multiplies the places a deck can forget one, and a check
reading it would first have to decide which chart each declaration governs before it could say
anything at all. One block is one thing to find and one licence to read — the same shape DS-009's
preflight already uses for a whole-deck capability.

### 3.7 Shared pieces

| Part | Element | Sits in | Count | Attributes | Source |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `.icon` | `svg` | `.slide` | `0+` | `aria-hidden` | author |
| `.sm` | — | `on .icon` | `0+` | — | author |
| `.est` | `span` | `.slide` | `0+` | — | author |
| `.legend` | `div` | `.slide` | `0+` | — | author |
| `.mono` | — | — | `0+` | — | author |

`.est` is the `[est.]` marker DS-102 requires to survive; `.mono` is the same treatment as a
standalone utility and no slide here has needed it, `.est` and `.lab` covering the two places a
mono label actually appears. **It was `vocabulary` until 2026-08-12** and moved with the figure
roles (T-105): a utility the contract styles and documents for a deck to use is one a deck may
use, and unused-in-*this*-deck is not the same claim.

### 3.7a The presenter panel — **never in a shipped deck**

**This is the one region in this document that a conforming deck must not contain.** It is here
because it has to be written down somewhere and because a deck author reading the contract end to
end should meet it and understand why it is not theirs to use.

A **presenter build** is a second artifact derived from a shipped deck by
[`tools/deck/presenter.py`](../tools/deck/presenter.py): the same deck, plus the speaker notes its
specification authors in the optional `Notes` field. It is written as `<slug>-presenter.html`, it is
one self-contained file that opens by double-clicking — a presenter is a recipient too — and it
**fails `check.py`**.

| Part | Element | Sits in | Count | Attributes | Source |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `#pb-bar` | `div` | `body` | `0` in a deck, `1` in a presenter build | — | `presenter.py` |
| `#pb-notes` | `div` | `body` | `0` in a deck, `1` in a presenter build | — | `presenter.py` |
| `.speaker-note` | `div` | `#pb-notes` | `0` in a deck, `1` in a presenter build | — | `presenter.py` |

**`.speaker-note` is the marker, and it is the note rather than a flag beside it.** DS-088's check
fails on that class name, so a presenter build is unshippable **because it carries notes** — not
because it carries a token announcing that it carries notes. A separate flag would be a second thing
to keep in sync, and a build that lost it would pass. This is why the count column reads `0` in a
deck: the rule and the contract say the same thing in two places, and neither can drift from the
other without the gate going red.

**Every length in the panel's CSS is one of the deck's own tokens** (§4), so a presenter build fails
on DS-088 **and nothing else**. That is asserted rather than assumed: T-213 §3 records the run. A
build failing three rules invites a maintainer to tidy the other two away, and the shortest path to
a quiet gate is deleting the notes.

### 3.8 Motion

Three classes carry DS-140's suggested starter set onto elements the rest of these tables already
name, so they sit on anything and contract only *where* they may sit. **They are what a deck gets
without designing a motion, not the set it is held to** — DS-140 admits a motion that passes its
test, and a deck adding one adds a row here rather than arguing an exemption.

| Part | Element | Sits in | Count | Attributes | Source |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `.rise` | — | `.slide` | `0+` | `style:--i` | author |
| `.current` | — | `.fig` | `0+` | — | author |
| `.pulse` | — | `.slide` | `0+` | — | author |

**A rule that starts a motion declares `--motion-subject`, and a looping one is failed without it.**
`live` says the motion's subject is genuinely in flight, `static` says it is not, and DS-142 reads
the declaration back rather than inferring it from a class name — the same split DS-237 makes with
`--motion-kind` and DS-230 with `data-disc`. `.current` carries `--motion-subject:live` and passes on
that, not on its name. **The property is registered `inherits:false` in `shell/components.css`**, so
a motion nested inside a live subject is judged on its own declaration; that registration is
load-bearing rather than housekeeping, and removing it exempts a whole subtree.

**Every component reads its motion from [`THEME-CONTRACT.md`](THEME-CONTRACT.md) §3.6.** This table
is that sentence made checkable: the rule named on the left must reference the tokens named on the
right, so a theme moving the motion axis moves this deck and not only the four rules someone
remembered to tokenise.

| Rule | Motion | Reads |
| :--- | :--- | :--- |
| `.slide[data-leaving]` | the inter-slide transition (DS-141, DS-235) | `--slide-dur` `--slide-ease` |
| `.slide[data-leaving="fwd"]` | which transition, going forward (DS-235) | `--slide-leave-fwd` |
| `.slide[data-leaving="back"]` | the same, going back | `--slide-leave-back` |
| `@keyframes slide-leave-fwd` | the `slide` transition's travel | `--slide-shift` `--slide-scale` `--slide-leave-shadow` |
| `@keyframes slide-leave-back` | the same, mirrored | `--slide-shift` `--slide-scale` `--slide-leave-shadow` |
| `.rise` | Rise's rest state (DS-140) | `--rise-dist` |
| `.slide[data-played] .rise` | Rise | `--rise-dur` `--rise-ease` `--rise-stagger` |
| `@keyframes rise` | Rise | `--rise-dist` |
| `.current` | Current (DS-140), licensed long by `--motion-long:loop` | `--current-dash` `--current-dur` |
| `.pulse` | Pulse-once (DS-140), licensed long by `--motion-long:emphasis` | `--pulse-dur` `--pulse-ease` `--pulse-delay` |
| `.opening` | Open (DS-140) | `--open-dur` `--open-ease` |
| `@keyframes open` | Open | `--open-rise` `--open-squash` |
| `.disc-mark::after` | a control answering the hand (DS-240) | `--afford-dur` `--afford-ease` |
| `.ruler-ticks button::before` | a control answering the hand (DS-240) | `--afford-dur` `--afford-ease` |
| `.ruler[data-ticks="dot"] .ruler-ring` | a control answering the hand (DS-240) | `--afford-dur` `--afford-ease` |
| `.ruler[data-dense] .ruler-ring` | the same ring past the capacity bound (DS-217, DS-240) | `--afford-dur` `--afford-ease` |
| `.btn` | a control answering the hand (DS-240) | `--afford-dur` `--afford-ease` |
| `.btn.btn--pager:active` | the press (DS-240) | `--press-dur` `--press-ease` |
| `.arrow-pop marker path` | an arrowhead arriving after its line (DS-140, DS-141) | `--scale-dur` `--scale-ease` `--arrow-pop-delay` |
| `.dot-pop circle` | a matrix's dots arriving one at a time (DS-140, DS-141) | `--scale-dur` `--scale-ease` `--dot-stagger` |
| `@keyframes dotpop` | the dot's overshoot | `--dot-overshoot` |

*The first three read Turn's and Scale's pairs until 2026-08-20. They were never reveals — each is
a control saying* this is the thing you are pointing at *— and borrowing a reveal's clock is what
made the pager's press take 420 ms.
[T-198](../tasks/T-198-give-affordance-motion-its-own-band-faster-than-content-motion.md) moved
them onto the band DS-240 states, and added the two rows below them, which were animating with no
row here at all.*

**This table has a completeness half, and it is the direction the check could not see.** Section 1
says a class styled in the shared block and absent from the tables below fails the gate; the same
holds here: **a CSS rule that starts a motion on a token and has no row is a gap in this table**, not
only a row whose rule has stopped reading its tokens. *Added 2026-08-29 by
[T-242](../tasks/T-242-the-contracts-against-the-checkers-that-decide-them.md), closing `PR-35`.
`component.motion_gaps` iterated **this table** and asked whether the CSS agreed, so a rule with no
row at all was invisible to a table that calls itself* that sentence made checkable *— which is the
defect T-198 fixed once by hand and nothing stopped recurring. **Three rules were animating unrowed
when the check was written**: `.arrow-pop marker path` and `.dot-pop circle`, which the finding
named, and `.ruler[data-dense] .ruler-ring`, which it did not and the new direction found on its
first run. A rule switching motion **off** reads `none` and is not a motion, so the reduced-motion
collapse, the preflight and the density gate need no rows and are not named as exceptions.*

**Durations are covered from the other side and are not re-checked here.**
`theme.py check` scans every length, duration and easing curve written outside the theme region and
reports how many were exempt; a component inventing its own 300 ms is that scan's defect, under
DS-010. This table is the positive claim the scan cannot make — *the token is read* rather than *no
literal was written* — and the difference is a component that animates nothing at all.

---

## 4. State

The attributes that change while the deck runs. **A generator emits the left-hand column; the
script owns the right.** Nothing here is a second home for a rule: each row names the rule that
governs it.

| Attribute | On | At load | Changes to | Governed by |
| :--- | :--- | :--- | :--- | :--- |
| `aria-expanded` | `.disc-btn` | `false` | `true` while its panel is open | DS-227, DS-228 |
| `hidden` | `.disc-panel` | present | absent while open | DS-227 |
| `data-current` | `.slide` | on slide 1 only | follows the current slide | DS-132 |
| `data-played` | `.slide` | absent | set once, never removed | DS-146 |
| `inert` `aria-hidden` | `.slide` | on every slide but the current | follows `data-current` inverted | DS-132 |
| `data-lit` `aria-current` | a ruler tick | on the first tick | follows the current slide | DS-134 |
| `data-dense` | `.ruler` | absent | set past the measured capacity | DS-217 |
| `data-motion` | `:root` | from `matchMedia` | toggled by the control | DS-143, DS-218 |
| `data-on` | `.doc` `.viewswitch` | absent | set in the reading view | DS-071 |

**`data-played` is set once and never removed, and that is the rule rather than an optimisation**
(DS-146): a chart that re-animates on the way back tells the reader something changed when nothing
did.

---

## 5. What a component may still write for itself

Two things, and neither is a look — the same test [`THEME-CONTRACT.md`](THEME-CONTRACT.md) §5
applies to lengths.

**`linear`, where anything else would be wrong.** A looping dash stutters at the seam under any
easing, and a zero-duration `visibility` step has nothing to ease. Those are the deck's only two,
and they are the mechanism's word rather than a choice. **Every other easing is a dial** — each of
DS-140's named motions has one, and so does the slide transition — so a component wanting an
overshoot on a card reveal reaches for `--turn-ease` rather than writing a curve into itself —
**though no shipped component reads that pair yet: the reveal was ruled to be built on 2026-08-29 and
is [T-274](../tasks/T-274-build-the-card-reveal-so-turns-two-dials-have-a-reader.md)'s**. A
`cubic-bezier()` outside the region is not a forbidden effect; it is an effect in the wrong place,
and `theme.py check` says so under DS-010.

**An inline `--i`.** Every `.rise` carries `style="--i:n"`, and the number is the element's place in
the stagger — content, not style. It is what makes DS-140's Rise *staggered* rather than a group
of 63 elements arriving together, and a generator computes it per slide.
