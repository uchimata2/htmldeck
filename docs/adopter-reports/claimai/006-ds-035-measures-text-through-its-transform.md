# DS-035 measures a text run through its transform, so a scale-from-zero entrance fails it at 0 du

| Field | Value |
| :--- | :--- |
| **Target** | `htmldeck` — Gábor's own repository, cloned under `C:\Work\AgentPlugins` |
| **Kind** | Defect |
| **Status** | `open` |
| **Found while** | Building the slide 2 entrance on `D4 — Executive Board Presentation`, on 2026-08-24 |
| **Version seen** | `0.6.0` |

## What happens

DS-035 refuses a text run under 16 design units. For an SVG element the probe scales the computed
font size by the element's screen transform matrix:

```
var m = el.getScreenCTM();
du = fs * (Math.sqrt(Math.abs(m.a*m.d - m.b*m.c)) / k);
```

A perfectly ordinary entrance — `@keyframes … from{transform:scaleY(0)}`, with `animation-fill-mode:
both` and a stagger delay — puts every element that has not started yet at `scaleY(0)`. The
determinant is 0, so `du` is 0, and the rule fails three display-size headings that are at full size
for all but the first frame of their life.

The report gives no clue that a transform is involved:

```
DS-035   text below 16 design units: 3                                  FAIL
```

and the raw rows are `[0, 'NO', 'Three assessments, one answer']` three times. A builder reads
*text below 16 design units* and goes looking for a font size.

## Evidence

```
python tools/deck/check.py <deck>
```

on the deck with a `scaleY(0)` entrance on three `.verdict-no` runs. Replacing the entrance with
`clip-path:inset(100% 0 0 0)` growing to `inset(0 0 0 0)` — the same reading, from the base line
upward, with the type at full size throughout — takes the rule back to pass with nothing else
changed.

## What is missing

The rule is about legible type. A run that is mid-entrance is not illegible type, and no reader ever
sees it at rest. The check should measure the **rest** state, or say that a transform is why the
number is what it is.

## Proposed fix

Two ways, and the second is cheap.

1. Take the measurement with animations settled — the probe already waits for a frame, so a
   `getAnimations()` sweep calling `finish()` before measuring would give every run its rest size.
2. At minimum, **name the cause in the failure**. Where `sqrt(|det|)` is under 1, print the raw
   `font-size` beside the design units and say the element is mid-transform. One extra field turns a
   twenty-minute hunt into a glance.

Whichever is taken, `DESIGN-SYSTEM.md`'s DS-035 row should say that the measurement is taken through
the element's transform. Nothing in it hints that an entrance can fail a legibility rule.
