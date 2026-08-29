# DS-110 cannot tell a rasterised diagram from a drawing, so front matter has to fail it

| Field | Value |
| :--- | :--- |
| **Target** | `htmldeck` — Gábor's own repository, cloned under `C:\Work\AgentPlugins` |
| **Kind** | Feature — narrow an existing rule |
| **Status** | `closed` — closed 2026-08-29 by [T-265](../../../tasks/T-265-ds-110-cannot-tell-a-rasterised-diagram-from-a-drawing.md). **The finding is taken and the deck's failure is gone; the weaker form was implemented and the primary refused.** Allowing any raster in a `front`/`back` section names a slide kind, and both `DS-085` and `DS-242` warn that a kind allowed to relax a rule hands the next kind the same argument — so the escape is granted by **place**: a raster outside a slide's `.body` carrying no `role="img"`. That admits this drawing without naming a stage, and a raster in a lobby's `.body` still fails. **`role="img"` is read as the literal attribute**, because the wider reading — an element with the img role carrying a label — refuses this report's own `<img … alt="A pencil drawing">`. **Two things were taken that this report did not ask for**: the `DS-110` row now says it protects legibility and consistency rather than portability, which is the half this report identified; and a raster in the style block or a script keeps failing, because a background paints on any element and so sits in no place at all. Reproduced on htmldeck's own `examples/measure-first/measure-first.html` before anything was written: the same raster inside `.body` gives `1 failure(s): DS-110`, outside it the whole gate passes, and the untouched deck is green. |
| **Found while** | Putting the presenter's own drawing on the lobby of `D4 — Executive Board Presentation`, on 2026-08-25 |
| **Version seen** | `0.6.0` |

## What the rule says

DS-110 is `hard` and machine-checked: **no raster image the deck produces, ever** — a raster is legal
only inside a quick view, where it is a quoted source rather than something the deck drew.

## Why the rule is right

A rasterised **diagram** is the defect it exists to stop. It cannot take the theme, it does not
scale, its type stops matching the deck's type, and it is the single fastest way to make a built deck
look assembled from screenshots. Nothing here argues with that.

## Where it is wrong

A lobby is front matter. DS-242 already says so, and says the lobby carries **nothing from the
argument** — no finding, no number, no verdict. A drawing on it carries no data, is not read, and is
not compared with anything. It is the one image on a deck for which every reason behind DS-110 is
absent.

The presenter supplied a pencil drawing of his own and asked for it on the lobby. The alternatives
were all worse:

| Alternative | Why it was not taken |
| :--- | :--- |
| Trace it to SVG paths | No tracer installed, and a hand trace of a pencil drawing does not look like the drawing |
| Keep the drawn SVG emblem | He had already seen one and rejected it |
| Put it in the reading view only, where DS-110 allows a raster | The lobby is what the room looks at while it fills. The reading view is where nobody is sitting |

So the deck now carries a third recorded rule failure to do something the rule was never written to
prevent.

## Evidence

```
python tools/deck/check.py <deck>
```

```
3 failure(s): DS-110, DS-217, DS-218
    DS-110    no raster the deck produces; a quoted source may be raster inside a quick view
```

The image is a 900 px alpha PNG, 175 KB embedded, on a `data-stage="front"` section, inside no figure
and beside no data.

## What is missing

The rule cannot express *not on a slide that carries an argument*, which is the distinction it is
actually making.

## Proposed fix

Narrow DS-110 by where the raster sits, not by whether one exists:

- allow a raster inside a `data-stage="front"` or `data-stage="back"` section — the lobby and the
  colophon, which DS-242 already defines as carrying nothing from the argument;
- keep the rule exactly as it is everywhere else;
- keep the size ceiling, wherever one is wanted — a lobby drawing is not a licence to embed four
  megabytes.

A weaker version, if the above is too permissive: allow it only where the element is **not** inside
`.body` and carries no `role="img"` label naming data. That is closer to the real test, and harder
to explain.

Either way `DESIGN-SYSTEM.md`'s DS-110 row should say what the rule is protecting, because *no raster
the deck produces, ever* reads as a portability rule and is really a **legibility and consistency**
rule about diagrams.
