---
tool: htmldeck
version: 0.7.0
date: 2026-09-07
severity: gap
---

# `render.py measure` reports zero overflow while a figure paints over the lines beneath it

## Expected

`measure` is the tool a builder runs to find out whether a page fits. A figure drawn on top of the
paragraphs under it is the most visible way a page can fail to fit, so a run that reports **0
overflow findings** should mean the page is clear.

## Actual

It reports 0. `measure` compares the body's content box against the stage, and an SVG that overflows
its own grid track is still inside the body — so the check is answered honestly and the page is
still wrong.

The shape is ordinary rather than exotic. An SVG with `width:100%; height:auto` takes its height
from its intrinsic ratio, not from the track it sits in. Put it in a `grid-template-rows` track that
resolves shorter than that height — which is what happens the moment a paragraph is added to the
same grid — and it overflows downward into the next rows, drawing the figure over them. Nothing
clips it, nothing warns, and every other check in the gate passes.

Measured on this project's deck, slide 27: a 1732 x 480 figure in a `1fr` track, with two paragraphs
added below it in the same grid. The band at the bottom of the figure and the first line of prose
occupied the same pixels; `check.py` passed every rule, and `measure` reported:

```
overflow findings: 0
```

The fix on the deck side is `height:100%` so `meet` scales the drawing to whatever the track gives
it. That is a one-line change **once you know**; the cost is entirely in not knowing, because the
tool that exists to answer *does it fit* said yes.

## What would close it

A row that compares each `.fig` element's rendered box against its own layout container, not only
the body against the stage. It does not need a new pass: the geometry `measure` already collects at
two viewports carries the figure boxes.
