---
tool: htmldeck
version: 0.7.0
date: 2026-09-07
severity: defect
---

# `render.py state --hover` paints the CSS hover and never fires `mouseenter`

## Expected

`render.py state <deck> --slide N --hover "<selector>" --shot` is the tool a build loop uses to
look at a hover state. A deck's hover behaviour is usually two things at once: a CSS `:hover` rule
that paints the target, and a script that does the rest — writing a caption, setting a state
attribute, announcing to a live region. The capture should show both, or fail.

## Actual

It shows the first and silently drops the second. The capture is a picture of a hover that half
happened, and the half it keeps is the half that needs no script — so the picture looks right.

Measured on a 24-page deck whose plate pattern paints the hovered row in CSS and writes the row's
sentence into a shared `aria-live` rail from a `mouseenter` listener:

- `render.py state deck/nextep.html --slide 24 --hover "[data-plate='undeclared-1']" --shot`
  produces a capture in which **the row is painted** and **the rail still holds its resting
  sentence**.
- The same page, driven in a real browser at the same size with a real pointer, paints the row
  **and** replaces the rail's text.

The second run is the control, and it is what makes this a tool defect rather than a deck defect:

```js
// after a real pointer hover over the same element
document.querySelector('#rail-s23').textContent.slice(0, 60)
// -> "The board still says open. A merged change in the same repos"
```

```js
// after render.py's --hover, the same read returns the resting sentence
// -> "Point at a row for what the board says, and what the merged"
```

## Why it costs more than it looks

A capture that shows the paint reads as proof the interaction works, so the loop's *look at it*
step passes on a page whose script never ran. This deck shipped a page for a whole batch with its
plates unwired — the rows carried the deck's own class and not the one the shared handler looks for
with `closest()` — and the owed look was recorded as this exact command. Had the command been run,
it would have produced a convincing picture of the defect.

It is the same shape as `slidefacts.py` reporting no control on any slide: the tool that exists to
inspect an interaction cannot see the part of it that is scripted.

## Suggested fix

Dispatch real pointer events at the element's centre — `mouseover`, `mouseenter`, `mousemove` —
before the capture, rather than applying a hover state to the renderer alone. Where that is not
possible, print what was applied, so a reader can tell a CSS-only hover from a full one; a tool
that cannot see half of an interaction should say so rather than photograph the other half.

## Status

Open. Not fixed upstream. It blocks nothing: the workaround is to drive the hover in a real
browser and read the DOM, which is what this project now does for every scripted interaction.
