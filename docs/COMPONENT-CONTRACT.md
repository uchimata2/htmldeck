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
| **Attributes** | Required on every instance. Absent ones fail; extra ones do not. `attr:text` additionally requires the value to contain `text`, which is how `style:--i` says *a `.rise` carries its stagger index* rather than merely *a style attribute*. `attr:a/b/c` instead requires the value to be **one of** the listed alternatives — a closed set, which is how `data-disc` carries DS-230's four editorial kinds and no fifth. |
| **Source** | Who writes it — §2.1. |

### 2.1 The four sources, and what each one is checked for

**A static scan can only see what the author wrote**, so the column exists to stop the gate
reporting a script's work as missing markup — and to stop *unused* being a shrug.

| Source | Means | Checked for |
| :--- | :--- | :--- |
| `author` | In the file as delivered. | Element, place, count, attributes. |
| `script` | The deck's own script creates it at runtime. | Its **rule** exists in the shared block; instances are not counted here. |
| `print` | Generated into `@media print` only. | The same. |
| `vocabulary` | Styled, emittable, and **this deck contains none.** | **Zero instances** — one appearing means the row is misfiled and must become `author`. |

`vocabulary` is checked in the opposite direction on purpose. *Declared and unused* is otherwise
unfalsifiable, and the deck already carries the lesson: a stale `.ribbon button::before` survived
T-035 because **a rule that matches nothing looks exactly like a rule that passed**. Five rows
below are `vocabulary`, and the number is meant to be looked at rather than grown.

---

## 3. The components

### 3.1 The stage

| Part | Element | Sits in | Count | Attributes | Source |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `.viewport` | `div` | — | `1` | `id` | author |
| `.stage` | `main` | `.viewport` | `1` | `id` `aria-label` | author |
| `.sr` | — | — | `1+` | — | author |
| `.contents` | `div` | — | `0+` | — | print |

### 3.2 The slide

Every slide is a `<section>` (DS-080) and carries its own name, its stage and an accessible label;
the ruler and the printed contents page are both **renderings of those attributes**, so a slide
that omits one goes missing from the navigation rather than looking wrong.

| Part | Element | Sits in | Count | Attributes | Source |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `.slide` | `section` | `.stage` | `1+` | `data-name` `data-stage` `aria-label` | author |
| `.eyebrow` | `p` | `.slide` | `1` | — | author |
| `.tick` | `span` | `.eyebrow` | `1` | — | author |
| `.headline` | `h2` | `.slide` | `1` | — | author |
| `.standfirst` | `p` | `.slide` | `0-1` | — | author |
| `.body` | `div` | `.slide` | `1` | — | author |
| `.bottom-line` | `p` | `.slide` | `1` | — | author |
| `.bottom-line--center` | — | `on .bottom-line` | `0+` | — | author |
| `.provenance` | `p` | `.slide` | `1` | — | author |
| `.sources` | `span` | `.provenance` | `0-1` | — | author |
| `.sources-btn` | `button` | `.sources` | `1` | `aria-expanded` `aria-controls` | author |
| `.sources-mark` | `svg` | `.sources-btn` | `1` | `aria-hidden` | author |
| `.sources-label` | `span` | `.sources-btn` | `1` | — | author |
| `.sources-box` | `span` | `.sources` | `1` | `id` | author |
| `.sources-item` | `span` | `.sources-box` | `1+` | — | author |

**The multi-source mark is `<span>`s inside the `<p>`, and that is a parser constraint rather than a
preference.** A `<div>` inside a `<p>` is closed by the HTML parser, so a box built that way would
sit **outside** the mark in the DOM while looking correct in the file — the deck would lose DS-223's
print placement without anything appearing wrong. Keeping the box inside `.provenance` is also what
keeps that row at `1`: a slide has one provenance mark, and what changed is what the mark may
contain.

**`.sources-item` is `1+` and DS-105 says two.** The contract can only say a box has items; *a box
is for more than one source* is an editorial claim about the slide, which is DS-105's to make and
the critique pass's to judge. A one-item box is conformant markup and a pointless design.

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
| `.ruler` | `div` | `.chrome` | `1` | `id` `data-ticks` | author |
| `.ruler-ticks` | `ul` | `.ruler` | `1` | `id` `data-scale` | author |
| `.ruler-ring` | `i` | `.ruler` | `1` | `id` `aria-hidden` | author |
| `.ruler-label` | `p` | `.ruler` | `1` | `id` `aria-hidden` | author |
| `.controls` | `div` | `.chrome` | `1` | — | author |
| `.count` | `p` | `.controls` | `1` | `id` `aria-hidden` | author |
| `.btn` | `button` | `.controls` | `1+` | `id` | author |
| `.chev` | `span` | `.btn` | `0-1` | — | author |
| `.l` | — | `on .chev` | `0+` | — | author |
| `.r` | — | `on .chev` | `0+` | — | author |

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
| `.t-ink` | `text` | `.fig` | `0+` | — | vocabulary |
| `.pos` | — | `.fig` | `0+` | — | vocabulary |
| `.neg` | — | `.fig` | `0+` | — | vocabulary |
| `.caution` | — | `.fig` | `0+` | — | vocabulary |

**The three role classes are `vocabulary` and the reason is worth stating, because it looks like a
mistake and is not.** DS-026 fixes the positive, negative and caution roles deck-wide, and this
deck spends all thirteen of them in the ledger's `<b>` and `<div>` elements — `.ledger .pos` in the
composition block, a different rule to `.fig .pos` here. So the roles are used and the *figure's*
copy of them is not. A figure encoding a loss is the obvious next deck, which is why the rows stay.

### 3.7 Shared pieces

| Part | Element | Sits in | Count | Attributes | Source |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `.icon` | `svg` | `.slide` | `0+` | `aria-hidden` | author |
| `.sm` | — | `on .icon` | `0+` | — | author |
| `.est` | `span` | `.slide` | `0+` | — | author |
| `.legend` | `div` | `.slide` | `0+` | — | author |
| `.mono` | — | — | `0+` | — | vocabulary |

`.est` is the `[est.]` marker DS-102 requires to survive; `.mono` is the same treatment as a
standalone utility and no slide has needed it, `.est` and `.lab` covering the two places a mono
label actually appears.

### 3.8 Motion

Three classes carry DS-140's vocabulary onto elements the rest of these tables already name, so
they sit on anything and contract only *where* they may sit.

| Part | Element | Sits in | Count | Attributes | Source |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `.rise` | — | `.slide` | `0+` | `style:--i` | author |
| `.current` | — | `.fig` | `0+` | — | author |
| `.pulse` | — | `.slide` | `0+` | — | author |

**Every component reads its motion from [`THEME-CONTRACT.md`](THEME-CONTRACT.md) §3.6.** This table
is that sentence made checkable: the rule named on the left must reference the tokens named on the
right, so a theme moving the motion axis moves this deck and not only the four rules someone
remembered to tokenise.

| Rule | Motion | Reads |
| :--- | :--- | :--- |
| `.slide` | the inter-slide transition (DS-141) | `--slide-dur` `--slide-ease` |
| `.rise` | Rise's rest state (DS-140) | `--rise-dist` |
| `.slide[data-played] .rise` | Rise | `--rise-dur` `--rise-ease` `--rise-stagger` |
| `@keyframes rise` | Rise | `--rise-dist` |
| `.current` | Current (DS-140) | `--current-dash` `--current-dur` |
| `.pulse` | Pulse-once (DS-140) | `--pulse-dur` `--pulse-ease` `--pulse-delay` |
| `.opening` | Open (DS-140) | `--open-dur` `--open-ease` |
| `@keyframes open` | Open | `--open-rise` `--open-squash` |
| `.disc-mark::after` | Turn (DS-140) | `--turn-dur` `--turn-ease` |
| `.ruler-ticks button::before` | Scale (DS-140) | `--scale-dur` `--scale-ease` |
| `.ruler[data-ticks="dot"] .ruler-ring` | a transition (DS-141) | `--scale-dur` `--scale-ease` |

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
overshoot on a card reveal reaches for `--turn-ease` rather than writing a curve into itself. A
`cubic-bezier()` outside the region is not a forbidden effect; it is an effect in the wrong place,
and `theme.py check` says so under DS-010.

**An inline `--i`.** Every `.rise` carries `style="--i:n"`, and the number is the element's place in
the stagger — content, not style. It is what makes DS-140's Rise *staggered* rather than a group
of 63 elements arriving together, and a generator computes it per slide.
