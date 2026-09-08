---
tool: htmldeck
version: 0.7.0
date: 2026-09-07
severity: defect
---

# `slidefacts.py` reports "the slide carries none" under `Controls` on every slide, HTML or SVG

Filed 2026-09-07 against SVG plates only. **Widened the same day**, after slide 21's four ordinary
HTML buttons reported the same: the section is empty on every page of a 22-page deck, whatever the
control is drawn with, so the original title understated it and the original fix would not have
been enough.

## Expected

`slidefacts.py <deck> <n>` prints what a slide says, so a builder can hold it against the slide's
own specification entry. Its `Controls` section is the half that answers *what can the reader do
here*. A `<button>` is a control by any definition, and a target carrying `role="button"` and
`tabindex="0"` is one by the accessibility tree's. Either should appear there — or the section
should say which of the two it reads.

## Actual

Nothing appears there, on any slide.

```
$ for n in 3 6 8 12 22; do python tools/deck/slidefacts.py deck/nextep.html $n; done
page  3 -> Controls:  - (the slide carries none)     # slide 2, turning cards
page  6 -> Controls:  - (the slide carries none)     # slide 5, period controls
page  8 -> Controls:  - (the slide carries none)     # slide 7, one long reveal
page 12 -> Controls:  - (the slide carries none)     # slide 11, four HTML buttons
page 22 -> Controls:  - (the slide carries none)     # slide 21, four HTML buttons
```

Pages 12 and 22 are the ones that settle it, because their controls need no interpretation at all:

```html
<button class="walkbtn" type="button" id="runNext" data-walk="next">Next step</button>
```

Four of those, in the slide's own subtree, each with a text label and each keyboard-operable. The
plated case is the same report from the other direction:

```html
<rect class="p1plate" x="0" y="0" width="749" height="32" data-plate="exact"
      data-rail="The platform's own resolved closing link. No parsing, no inference. 47 of 91."
      tabindex="0" role="button" aria-describedby="rail-s18" aria-label="Exact, 47 of 91"/>
```

Both work. Measured in a real browser on the same build: the plates set `data-hot` on `mouseenter`
and `data-pin` on `Enter`, and the buttons drive the tour through all five stages and back to rest.

It is not this deck's markup. Page 14, whose fourteen rule tiles are the reference implementation of
the plate pattern, reports the same.

## Why it matters

The per-slide build loop uses `slidefacts.py` as its comparison step: run it, hold it against the
specification entry, and a drift is a defect in one of the two. With `Controls` empty on every page,
the entry's **Interaction** section has nothing to compare against anywhere in the deck, and the
report reads identically whether a slide's controls are present, absent or wired wrong. A section
that is empty on one page invites a look; a section that is empty on all of them stops being read.

Paired with the `render.py state` finding already filed here, neither tool that inspects an
interaction can see one: `state` cannot see a plate's paint change, and `slidefacts` cannot see that
any control exists.

## Suggested fix

Collect `Controls` from the accessibility contract rather than from the element name: anything in
the slide's own subtree carrying `role="button"`, `role="tab"`, `role="switch"` or a `tabindex`,
**and every `<button>`**, SVG included. Print its accessible name, which these already carry in
`aria-label` or in their own text.
