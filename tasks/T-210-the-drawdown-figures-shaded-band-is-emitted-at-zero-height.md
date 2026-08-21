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

**The band's meaning had to be settled before the arithmetic could be, and it is — ruled by the
owner 2026-08-21: the band is 5.1 points measured from zero**, spanning the zero line down to the
`-5.1` level. The alternative reading, the span between `-5.1` and the trough, shades **1.7** points
rather than 5.1 and so contradicts the caption — *"Renewables carried 5.1 points of the 6.8"* — which
is what decided it. The operands follow: `rect(tx - 40, zero_y, 80, ry - zero_y)`, and both are now
above the trough rather than straddling it.

*Recorded here because a ruling is a fact about this task, and because §1's original wording asked
the question rather than answering it.*

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
- [ ] The band spans the zero line to the `-5.1` level, per the owner's ruling above, and the figure
      says so in its own text so the next reader does not re-open it.
- [ ] The band renders, confirmed by looking at the printed and screen slide, not by the markup.
- [ ] An identity in the generator's self-test fails if the band's height returns to zero — proved
      by seeding it, the method T-203 and T-207 both used.
- [ ] The decision on `rect()`'s clamp is recorded either way, with the count of callers that pass
      a computed extent.

**Open questions**
- ~~Whether `rect()` refusing is safe.~~ **Answered 2026-08-21 by the owner: it refuses, and the
  build fails.** A silent wrong picture is the worse failure, and the clamp's only effect is to hide
  one. The count of callers passing a computed extent is measured and reported **before** the refusal
  lands — the fourth acceptance criterion is therefore a precondition of the change rather than a
  record of it.
- ~~Whether any other figure is passing a computed extent that the clamp is already absorbing.~~
  **Not a question for the owner.** Nobody had looked, and the clamp means nothing would have shown
  up — so it is the measurement the ruling above requires, and it is step 1 of §2.

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
| 2026-08-21 | (no change) | **The owner ruled what the band means: 5.1 points measured from zero**, spanning the zero line to the `-5.1` level. The alternative - the span between `-5.1` and the trough - shades 1.7 points and contradicts the caption, which is what decided it. §1 and the first acceptance criterion updated; the task stays `proposed` because nothing has been built. The two open questions about `rect()`'s clamp are untouched and are still the wider half. |
| 2026-08-21 | (no change) | **The owner ruled on the clamp: `rect()` refuses a non-positive extent and the build fails.** A silent wrong picture is worse than a broken build, and the clamp's only effect is to hide one. Two consequences: the caller count §1 asked for becomes a **precondition** of the change rather than a record of it, and the second open question stops being a question — it is the measurement the ruling requires. The task stays `proposed` because nothing has been built. |
