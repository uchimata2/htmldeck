---
id: T-210
title: The drawdown figure's shaded band is emitted at zero height, and rect() clamps the sign error away
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-203, T-204, T-207]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-21
updated: 2026-08-21
deliverables: []
---

# T-210 — The drawdown figure's shaded band is emitted at zero height, and rect() clamps the sign error away

## 1. Specify

**Outcome**
Slide 10's drawdown figure draws the band its own docstring promises, or stops promising it. Today
it emits a rectangle of zero height, which renders nothing at all.

**How it was found**
While fixing [T-207](T-207-two-more-mark-collisions-the-twelve-slide-look-found.md)'s annotation on
the same figure, 2026-08-21 — by looking at the slide after the fix and noticing the shading was not
there. The emitted markup says it outright:

```
<rect class="caution" x="390.0" y="224.7" width="80.0" height="0.0"/>
```

`fig_drawdown`'s docstring is *"the trough marked, and the part of it that is renewables shaded"*.
There is no shading. Nothing else in the deck says the band should exist, so it has been missing for
as long as the figure has, and no gate can see it — a mark that draws nothing has no geometry to
measure, so even [T-204](T-204-an-instrument-for-mark-collisions.md)'s new instrument passes it.

**The mechanism, and it is two faults**
The call is `rect(tx - 40, ty, 80, ry - ty, "caution")`, where `ty` is the trough at `-6.8` and `ry`
the `-5.1` level. Because `y` grows downward and `-5.1` is *above* `-6.8`, `ry - ty` is **negative**
— about −36. Then [`rect()`](../tools/examples/portfolio_charts.py) clamps: `max(h, 0.0)`. So:

1. **The arithmetic has its operands the wrong way round.** `rect(x, ry, w, ty - ry)` is the band
   between those two levels.
2. **`rect()` silently absorbs it.** The clamp turns an impossible rectangle into a legal invisible
   one. A negative extent is a caller error every time — nothing legitimately asks for one — and
   swallowing it converts a loud failure into a mark that is simply absent. That is the more
   interesting half, because the clamp protects **every** `rect()` caller from ever learning it got
   a sign wrong.

**And the band's meaning has to be settled before the arithmetic can be, which is why this is not a
one-line fix.** The figure claims 5.1 points of a 6.8-point drawdown are renewables. Between the
`-5.1` level and the trough is **1.7** points, not 5.1. Measuring 5.1 from zero instead gives the
span from the zero line to `-5.1`. The two readings put the band in different places and say
different things, and only one of them matches the caption. Someone has to choose.

**Scope**
- In: what the band means, and the arithmetic that follows from it.
- In: whether `rect()` should refuse a negative extent rather than clamp it, and what that does to
  its other callers.
- Out: the two collisions on this figure and slide 4. Those are T-207 and are fixed.

**Inputs**
- [`tools/examples/portfolio_charts.py`](../tools/examples/portfolio_charts.py) — `fig_drawdown`
  and `rect`.
- [T-207](T-207-two-more-mark-collisions-the-twelve-slide-look-found.md) — the same figure, and the
  look that surfaced this.
- [`docs/lessons/L-127.md`](../docs/lessons/L-127.md) — a figure can be arithmetically right and
  relationally wrong; this is the third case, where the mark is not drawn at all.

**Acceptance criteria**
- [ ] The band's meaning is stated in the figure, and the arithmetic matches the caption's 5.1
      against 6.8.
- [ ] The band renders, confirmed by looking at the printed and screen slide, not by the markup.
- [ ] An identity in the generator's self-test fails if the band's height returns to zero — proved
      by seeding it, the method T-203 and T-207 both used.
- [ ] The decision on `rect()`'s clamp is recorded either way, with the count of callers that pass
      a computed extent.

**Open questions**
- Whether `rect()` refusing is safe. It is called by every figure, and a refusal turns a silent
  wrong picture into a build failure — which is right, but it should be counted before it is done.
- Whether any other figure is passing a computed extent that the clamp is already absorbing. Nobody
  has looked; the clamp means nothing would have shown up.

## 2. Plan

*Not started.*

## 3. Implement

**Decisions & assumptions**
-

**Outputs produced**
-

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :--- | :--- |
|  |  |  |

**Child fix tasks raised**
-

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-21 | → proposed | Found by looking at slide 10 after T-207's annotation fix landed on the same figure. The emitted rectangle carries `height="0.0"`: `ry - ty` is negative because `y` grows downward, and `rect()`'s `max(h, 0.0)` turns the sign error into a legal invisible mark. Two faults, and the clamp is the wider one — it protects every caller from discovering a wrong sign. Not a one-line fix, because 5.1 of 6.8 measured from the trough is 1.7 points and measured from zero is a different band, so what the shading means has to be decided first. `PH3`: the deck is shipped and the missing mark is an omission rather than a wrong statement. |
