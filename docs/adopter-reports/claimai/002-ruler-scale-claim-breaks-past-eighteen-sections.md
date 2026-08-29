# DS-217 fails on any deck past eighteen sections

| Field | Value |
| :--- | :--- |
| **Target** | `htmldeck` — Gábor's own repository, cloned under `C:\Work\AgentPlugins` |
| **Kind** | Defect |
| **Status** | `closed` — closed 2026-08-29 by [T-263](../../../tasks/T-263-ds-217-fails-on-any-deck-past-eighteen-sections.md). **The finding is real and is fixed; both proposed remedies were refused, and so was the stated cause.** Measured on this repository's own reference deck spliced to 43 slides: the widths differ by **1e-4 CSS px**, four orders of magnitude below the half-pixel bucket the old test rounded into, so sub-pixel rounding never produced a third cluster and *give it a tolerance* would have changed nothing. What does produce one is **two mark sizes sitting side by side**: minor/minor, minor/major and major/major are three centre-to-centre distances, and the ruler shows the third wherever a stage holds a single slide. `regularScale()` now accepts either lattice a scale can be — evenly spaced centres, or evenly spaced edges — with at most two mark sizes, and the tolerance is there as well. Reproduced by `python tools/deck/longdeck.py examples/reference-deck.html 25 --solo-stage`, which fails at 30 items before the change and passes at 6 after; three seeded irregularities still fire. |
| **Found while** | Building `D4 — Executive Board Presentation` at htmldeck stage 6, on 2026-08-24 |
| **Version seen** | `0.6.0` |

## What happens

`audit.py`'s `regularScale()` verifies the ruler's `data-scale` claim rather than trusting it:
uniform mark, uniform pitch, no per-item label at rest, and at most two clusters of gap and of
width. Past a certain tick count the measured pitch stops falling into two clusters, the claim is
refused, and every tick is counted as its own chrome item. DS-217's budget is about twelve, so the
verdict is a failure the deck cannot act on: no change to a slide moves it.

## Evidence

Measured on the ClaimAI deck by truncating it and re-running the gate. The deck is otherwise
unchanged between runs.

```
python tools/deck/check.py <deck> --quiet
```

| Sections in the deck | DS-217 |
| ---: | :--- |
| 18 | pass |
| 19 | `labelled or interactive chrome items: 24  [claims data-scale but is not regular - counted as n]` |
| 20 | `… 25 …` |
| 25 | `… 30 …` |

The threshold is between 18 and 19 sections, and the count then rises one per slide.

## What is missing

A deck of more than eighteen slides has no way to satisfy DS-217. The rule's own amendment says a
regular repeating scale counts as one item because a tick array is perceived as one object — which
is exactly as true at twenty-five ticks as at twelve. The failure is in how regularity is measured,
not in what the deck renders: the ruler still looks like one object.

## Proposed fix

Two candidates, and the first is smaller.

1. **Give `regularScale()` a tolerance.** Cluster gaps and widths to the nearest whole design unit
   rather than the nearest half CSS pixel, or accept a gap set whose spread is under one unit. Sub-
   pixel layout rounding across many flex items is what produces the third cluster, and it is not a
   difference a reader can see.
2. **Let the ruler's dense mode carry the claim.** The shell already sets `data-dense` past the
   measured capacity. If the dense ruler is a deliberate two-cluster form, the check could read
   `data-dense` and test the two clusters it declares rather than discovering them.

## Why the deck could not work around it

DS-082 already requires a recorded reason past twelve slides, and this deck has one: it answers six
exam questions across four perspectives, and each answer has to sit on a slide's own surface.
Compressing to eighteen would put two messages on one slide, which DS-201 forbids.
