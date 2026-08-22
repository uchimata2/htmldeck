---
id: T-210
title: The drawdown figure's shaded band is emitted at zero height, and rect() clamps the sign error away
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-203, T-204, T-207, T-212]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-21
updated: 2026-08-21
shipped_in: 0.6.0
deliverables: [tools/examples/portfolio_charts.py, examples/portfolio-review/portfolio-review.html]
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

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Count the `rect()` callers passing a computed extent, **before** changing anything — the precondition the owner's ruling attached to it | the blast radius, measured |
| 2 | Correct the band's operands to the ruling: from the zero line down to `-5.1` | `fig_drawdown` |
| 3 | Make `rect()` refuse a non-positive extent | `rect` |
| 4 | Build every figure and see whether the refusal fires anywhere else — this is the second open question, and it is a measurement rather than a question | the answer, either way |
| 5 | Add identities that read the band out of the emitted figure, relationally | `selftest` |
| 6 | Seed each way the band can go wrong and prove each is caught | evidence |
| 7 | Rebuild the deck, run the four-command chain, and **look at the slide on screen and on paper** | rule 6 |

## 3. Implement

**Decisions & assumptions**
- **The caller count, taken before the refusal landed, as the ruling required: seven call sites, and
  every one of them passes at least one extent derived from the data.** Five pass it as an inline
  subtraction — `x45 - L`, `x52 - x45`, `x1 - x0 - 6`, `ry - ty`, `base - ytop` — and two pass a
  variable computed upstream. So the refusal reaches every caller, which is the point: the clamp was
  protecting all seven from the fault that was live in one. The one place that legitimately produces
  a small extent, `MIN_BAR_PX` in `fig_contribution` and `fig_waterfall`, floors it **above** zero
  and is unaffected. — 2026-08-21
- **The second open question is answered by measurement, and the answer is no.** With `rect()`
  refusing, all ten figures build and the self-test's 33 checks pass. **No other figure was passing
  a computed extent the clamp was absorbing.** Nobody had looked, and the reason nobody could is
  that the clamp made looking impossible; making it refuse *is* the instrument. — 2026-08-21
- **The band's height is 107.7 units, from `y=81.1` at the zero line to `188.8`, against a trough at
  `cy=224.7`.** Read out of the emitted figure, not computed a second time. — 2026-08-21
- **The identities are relational, and stated against the figure's own other marks.** The band's top
  is compared to the emitted zero grid line and its foot to the emitted trough circle, rather than
  to a second copy of the figure's scale constants — **L-08** for the copy, **L-127** for the shape,
  since a band of the right height in the wrong place is exactly the defect the first version had.
  — 2026-08-21
- **The visible label was lengthened to say *from zero*, and looking at the slide is what refused
  it.** `"5.1 pts renewables, from zero"` ran past the figure's viewBox and printed as *5.1 PTS
  RENEWABLES, FROM*. The self-test stayed green — its annotation identity compares the label to the
  polyline, not to the viewBox edge — and `check.py` reported 0 failures. **So the criterion is met
  by the figure's description instead**, which now reads *"shaded from the zero line down to minus
  5.1"*, and the visible label is unchanged. — 2026-08-21
- **That miss is a finding rather than a detail, and it is
  [T-212](T-212-eight-of-ten-figures-never-call-the-clipped-label-guard.md).** The toolkit already
  has `guard_label`, which exists precisely to refuse a label its viewBox will clip. Two of the ten
  figures call it. `fig_drawdown` is one of the eight that do not. — 2026-08-21

**Outputs produced**
- [`tools/examples/portfolio_charts.py`](../tools/examples/portfolio_charts.py) — `rect()` refuses;
  `fig_drawdown`'s band and description; three identities in `selftest`.
- [`examples/portfolio-review/portfolio-review.html`](../examples/portfolio-review/portfolio-review.html)
  — rebuilt through the four-command chain.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The band spans the zero line to the `-5.1` level, and the figure says so in its own text | **met** | Height 107.7, from `y=81.1` at the zero line to `188.8`. The text is the figure's **description** — *"shaded from the zero line down to minus 5.1"* — rather than the on-slide label, which clipped when it was lengthened. The deviation and its reason are in §3. |
| The band renders, confirmed by looking at the printed and screen slide, not by the markup | **met** | Both looked at. **Screen:** slide 10 rendered in real Chrome, offline; the band sits under the dashed zero line and stops above the trough dot. **Paper:** the deck printed to PDF, page 11 rasterised and read; the band prints identically and nothing is clipped. The first screen look is what caught the clipped label. |
| An identity in the generator's self-test fails if the band's height returns to zero, proved by seeding | **met** | Three identities. **Seed C** — the reversed operands *and* the clamp restored — reproduces the original defect exactly and turns all three red, the first reading `height=0.0`. **Seed B**, a legal band anchored at the trough, turns two red. **Seed A**, the reversed operands against the live refusal, is refused by `rect()` before any identity runs, naming the file, the line and the value: `height=-35.889`. The file was restored and verified byte-identical after each. |
| The decision on `rect()`'s clamp is recorded either way, with the count of callers that pass a computed extent | **met** | It refuses. Seven call sites, every one passing at least one data-derived extent, five as an inline subtraction. Counted **before** the change, which is what the owner's ruling required. |
| *(closing checklist step 3)* | **met** | Both renderings opened and looked at, offline. |

**Child fix tasks raised**
- [T-212](T-212-eight-of-ten-figures-never-call-the-clipped-label-guard.md) — the clipped-label
  guard exists and eight of the ten figures never call it.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-22 | (shipped) | **Shipped in `0.6.0`.** The release note carries `docs/PUBLISHING.md` §8.1's row for this version, which names what an adopter must change and the smallest edit that satisfies it. |
| 2026-08-21 | → proposed | Found by looking at slide 10 after T-207's annotation fix landed on the same figure. The emitted rectangle carries `height="0.0"`: `ry - ty` is negative because `y` grows downward, and `rect()`'s `max(h, 0.0)` turns the sign error into a legal invisible mark. Two faults, and the clamp is the wider one — it protects every caller from discovering a wrong sign. Not a one-line fix, because 5.1 of 6.8 measured from the trough is 1.7 points and measured from zero is a different band, so what the shading means has to be decided first. `PH3`: the deck is shipped and the missing mark is an omission rather than a wrong statement. |
| 2026-08-21 | (no change) | **The owner ruled what the band means: 5.1 points measured from zero**, spanning the zero line to the `-5.1` level. The alternative - the span between `-5.1` and the trough - shades 1.7 points and contradicts the caption, which is what decided it. §1 and the first acceptance criterion updated; the task stays `proposed` because nothing has been built. The two open questions about `rect()`'s clamp are untouched and are still the wider half. |
| 2026-08-21 | (no change) | **The owner ruled on the clamp: `rect()` refuses a non-positive extent and the build fails.** A silent wrong picture is worse than a broken build, and the clamp's only effect is to hide one. Two consequences: the caller count §1 asked for becomes a **precondition** of the change rather than a record of it, and the second open question stops being a question — it is the measurement the ruling requires. The task stays `proposed` because nothing has been built. |
| 2026-08-21 | proposed → done | Both faults fixed and both open questions closed by measurement. The band is 107.7 units from the zero line to `-5.1`, stopping above the trough; `rect()` refuses a non-positive extent, counted first at seven call sites, all of them passing a data-derived extent. **No other figure was passing one the clamp absorbed** — all ten build. Three relational identities read the band out of the emitted figure, and three seeded defects prove them, including the original one reproduced exactly. **Looking is what earned its place here**: the gate was green and the screen render showed a label I had just clipped, which the description now carries instead. That miss raised [T-212](T-212-eight-of-ten-figures-never-call-the-clipped-label-guard.md) — the guard for it already exists and eight of ten figures never call it. |
