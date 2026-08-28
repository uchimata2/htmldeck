# DS-244 catches a label over a label, and never a label over the shape it labels

| Field | Value |
| :--- | :--- |
| **Target** | `htmldeck` — Gábor's own repository, cloned under `C:\Work\AgentPlugins` |
| **Kind** | Defect |
| **Status** | `open` |
| **Found while** | Rebuilding slides 8, 18 and 21 of `D4 — Executive Board Presentation`, on 2026-08-25 |
| **Version seen** | `0.6.0` |

## What happens

DS-244 reports *slides setting one diagram label over another*, and it does that well:

```
DS-244   slides setting one diagram label over another: 1 of 21 - slide 9 'Every one' over 'CR-03'   FAIL
```

It compares **text against text**. It does not compare text against the `<rect>`, `<path>` or
`<line>` the text sits beside. So the commonest way a diagram label goes wrong — running into or
across the box it labels — passes the gate silently.

Three instances in one evening, all on slides the gate called clean:

| Slide | What the render showed | What the gate said |
| :--- | :--- | :--- |
| 8 | *No rung fits* printed across the ladder rectangles | DS-244 pass |
| 18 | Two condition titles ran past their box's right edge | every rule pass |
| 21 | Three branch labels each ran into the box they name | DS-244 pass |

Each was found by rendering the slide and looking at it, which is the check the design system says is
owed anyway (**L-01**) — but a builder who trusts a green gate will ship all three.

## What is missing

The rule's own name promises less than a reader assumes. *One diagram label over another* is read as
*labels do not collide*, and a label crossing its own rectangle is a collision.

## Proposed fix

Two options, in increasing order of cost.

1. **Extend the comparison to authored shapes.** The probe already has each text node's client rect;
   comparing it against `rect`, `path` and `line` bounding boxes in the same `svg.fig` is the same
   loop with a second list. Overlap with the shape a label *belongs* to is legitimate — a label
   centred inside its box — so the test has to be *crosses a shape edge*, not *touches a shape*: flag
   a text run whose rect straddles a shape boundary rather than sitting wholly inside or wholly
   outside it.
2. **At minimum, rename it and say what it does not do.** `DESIGN-SYSTEM.md`'s DS-244 row should say
   the measurement is label against label only, so nobody reads a pass as *the labels are placed
   correctly*.

The first is worth the cost. Text leaving its box is the single most common defect in a hand-built
SVG figure, and it is the one a check can see perfectly well.
