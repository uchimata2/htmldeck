# DS-244 refuses a cross-fade in place, because it cannot see that one of the pair is at opacity 0

| Field | Value |
| :--- | :--- |
| **Target** | `htmldeck` — Gábor's own repository, cloned under `C:\Work\AgentPlugins` |
| **Kind** | Defect |
| **Status** | `closed` — closed 2026-08-29 by [T-260](../../../tasks/T-260-ds-244-tests-proximity-where-it-means-obstruction.md). **Item 1 implemented**: the opacity chain is read before two labels are paired, so a cross-fade in place is no longer a collision. Proved both ways on a seeded deck — the pair at `opacity:0`/`1` stops gating and is counted as *hidden at rest*, and the same pair with both visible still gates. **Item 2 is answered rather than implemented, and the answer is a stated limit**: `render.MOTION_PIN` forces `transition:none` and `animation:none` before the probe reads anything, so there is exactly one frame, it is at rest, and a pair that overlaps only mid-transition is not measured at all. The row says so now. A per-element *this one is animated* would be a guess: the pin also erases `animation-name`, so nothing in the page can tell an animated opacity from a static one afterwards. **The first form of this guard was wrong in a way worth recording**: `visibility` is inherited and every off-screen slide carries `visibility:hidden`, so reading it absolutely reported **129 hidden labels** on the reference deck and took T-204's fifteen label-on-line placements to zero — a guard swallowing the rule it was meant to narrow. It is measured against the slide now. |
| **Severity** | Medium — it refuses a standard technique three times running, and the deck has to be redesigned around the instrument |
| **Found while** | Building slide 5's banded axis and residual-risk toggle, on 2026-08-26 — `E44` |
| **Version seen** | 0.6.0 |

## What happens

A cross-fade in place is two labels at the same coordinates, one fading out as the other fades in —
the ordinary way to animate a value changing. `DS-244` reads two diagram labels at one point and
fails the slide. It does not read `opacity`, so it cannot see that only one of the pair is ever
visible.

It refused three constructions in a row on one slide: the two column headers, then the two score
columns, then the twelve cells. Each rebuild moved the labels apart, and the third design is better
than the first — **the rule was useful even while it was wrong**, which is why this is a report and
not a complaint.

## What to change

1. **Read the computed `opacity` of each label before pairing them.** Two labels that are never
   visible together are not overlapping labels.
2. **Where opacity is animated rather than static, say which frame was measured.** A pair that
   overlaps only mid-transition is a different finding from one that overlaps at rest.

## Related

- [`013-ds-244-sees-label-over-label-but-not-label-over-shape.md`](013-ds-244-sees-label-over-label-but-not-label-over-shape.md)
  — **the opposite complaint about the same rule, and both are true.** `DS-244` refuses an overlap
  that is not one, and misses an overlap that is: a label over the rectangle it labels goes
  unreported. Read together they say the rule is testing the wrong thing — proximity of two text
  runs, rather than whether anything is actually obscured.
