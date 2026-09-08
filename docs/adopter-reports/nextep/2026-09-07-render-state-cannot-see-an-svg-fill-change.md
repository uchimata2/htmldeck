---
tool: htmldeck
version: 0.7.0
date: 2026-09-07
severity: defect
---

# `render.py state` reports "nothing measured differs" for any SVG paint change

## Expected

`render.py state <deck> --slide N --hover "<selector>" --shot` is the documented way to prove an
interaction state. A figure's hover target is an SVG `<rect>`, and the state it changes is its
paint. The tool should see that change, or say that paint is outside what it reads.

## Actual

It reports the state as having no effect:

```
! nothing measured differs: not the box, and none of color, background, borderColor,
  transform, boxShadow, outline, filter.
  the substitution ran, so either no rule reaches this element or its effect is in a
  property this reads none of
```

The list is the whole story: `fill`, `fill-opacity`, `stroke` and `stroke-width` are not in it,
and those are the only properties an SVG mark can change. The message's second branch is correct
and is the one that applies, but a builder reads the first — *no rule reaches this element* — and
goes looking for a CSS defect that is not there. One build cycle was spent moving a working hover
from script to CSS on that reading before the properties list was read closely.

## Proof

The deck's plate is `fill:none` at rest and `fill:var(--accent); fill-opacity:.06` on
`.p1row:hover`. Served over `http.server` and read in a real browser, dispatching the same event
the tool simulates:

```js
const plate = document.querySelectorAll('.slide')[8].querySelector("[data-plate='c1']");
const label = plate.closest('.p1row').querySelector('.p1label');
plate.dispatchEvent(new MouseEvent('mouseenter'));
[getComputedStyle(plate).fillOpacity, getComputedStyle(label).fill];
```

Before: `["1", "rgb(35, 33, 29)"]` — `fill` is `none`, so nothing paints.
After: `["0.06", "rgb(90, 75, 143)"]` — the tint and the accent label.

`render.py state` photographed both and called them identical.

## Cost

Every P1 plate in a deck is an SVG rectangle, which is what the plate pattern is for. The tool
that exists to prove an interaction state cannot prove this one, so the proof falls back to a
browser and a console line, and the `--shot` it does write is evidence only to a person who opens
it. The same blind spot hides a stroke-width change on a data mark.

## Suggested

Add `fill`, `fillOpacity`, `stroke`, `strokeWidth` and `strokeDasharray` to the measured set, and
say `svg paint` in the failure message's property list so the second branch is reachable by
reading rather than by elimination.
