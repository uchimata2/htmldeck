---
id: T-212
title: Eight of ten figures never call the clipped-label guard, and the guard cannot see an anchor
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-203, T-207, T-210]
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-08-21
updated: 2026-08-21
shipped_in: 0.6.0
deliverables: [tools/assets/chart_probe.py, tools/examples/portfolio_charts.py]
---

# T-212 — Eight of ten figures never call the clipped-label guard, and the guard cannot see an anchor

## 1. Specify

**Outcome**
Every label the chart generator emits is checked against the viewBox that will clip it, using that
figure's own viewBox and that label's own anchor. Today two of the ten figures call the guard, both
hand it a literal that belongs to a third figure, and the guard itself assumes an anchor that three
of the figures do not use.

**How it was found**
Closing [T-210](T-210-the-drawdown-figures-shaded-band-is-emitted-at-zero-height.md) on 2026-08-21.
That task lengthened `fig_drawdown`'s annotation to `"5.1 pts renewables, from zero"` to satisfy an
acceptance criterion. It printed as **"5.1 PTS RENEWABLES, FROM"**, clipped at the figure's right
edge — and **every instrument stayed green**: the generator's 33 identities, `check.py` at 0
failures, and the deck's own annotation identity, which compares a label to the polyline it
annotates and not to the edge of the box it is drawn in. **Only the rendered slide showed it**,
which is `CLAUDE.md` rule 6 earning its place.

**The guard already exists, which is what makes this a defect rather than a gap.**
[`tools/assets/chart_probe.py`](../tools/assets/chart_probe.py) `:77` is `guard_label`, whose own
docstring says it exists to *prevent the clipped label*, and whose self-test has a fixture named
*clipped label refused*. [`tools/examples/portfolio_charts.py`](../tools/examples/portfolio_charts.py)
imports it at `:42`. It is called from exactly **two** of the ten figures.

| Figure | viewBox | Calls `guard_label` |
| :--- | :--- | :---: |
| `fig_curve` | `120 0 1060 400` | no |
| `fig_limit_bar` | `120 0 1728 170` | no |
| `fig_area` | `120 0 1728 470` (default) | **yes** |
| `fig_contribution` | `120 0 1728 480` | no |
| `fig_waterfall` | `120 0 1728 470` (default) | no |
| `fig_scatter` | `120 0 1728 470` (default) | **yes** |
| `fig_top3` | `120 0 1728 190` | no |
| `fig_drawdown` | `120 0 660 310` | no |
| `fig_tranches` | `120 0 660 310` | no |
| `fig_timeline` | `240 0 1450 480` | no |

**And it cannot simply be switched on, which is the half worth measuring before deciding.** Both
existing calls pass the literal `1728 - 120, 470`. That is neither a figure's viewBox width nor its
right edge in the coordinate space the labels are placed in — the default viewBox starts at `x=120`,
so its x-coordinates run to `1848`. Measured 2026-08-21 against `fig_drawdown`'s real geometry:

- handed `width=660`, the figure's viewBox width, the guard **refuses the clipped label** — the true
  hit this task is about;
- handed `width=780`, the same figure's right edge in x, it **passes it** — blind;
- handed `width=660`, it *also* refuses `"5.1 pts renewables"`, **the label that ships and renders
  correctly** — a false alarm on a good figure.

The cause of the false alarm is that `guard_label` tests `x ± approx_w / 2`: it assumes every label
is centre-anchored. `fig_drawdown`'s annotation is `anchor="start"`, and `start` and `end` anchors
are used across the generator. **A guard that fails a correct figure is worse than one nobody
calls**, which is why the anchor comes first and the call sites second.

**Scope**
- In: giving `guard_label` the anchor, so its estimated box is the box the renderer will draw.
- In: giving each figure's guard call that figure's own viewBox, derived rather than written twice.
- In: calling it for every label in all ten figures, and counting the false alarms before keeping it.
- Out: the width estimate itself. `len(text) * font_px * 0.62` is deliberately generous and this
  task does not re-derive it.
- Out: a browser-measured label box. `markhits.py` reads real geometry and is the instrument for
  that; this guard is build-time and standard-library, and that is why it is cheap enough to run on
  every label.

**Inputs**
- [`tools/assets/chart_probe.py`](../tools/assets/chart_probe.py) `:77` — `guard_label`, and the
  `clipped label refused` fixture in its self-test.
- [`tools/examples/portfolio_charts.py`](../tools/examples/portfolio_charts.py) — `svg`, `text`, the
  `VIEWBOX` default and the ten figures.
- [T-210](T-210-the-drawdown-figures-shaded-band-is-emitted-at-zero-height.md) §3 — the clipped
  label, and what stayed green while it shipped.

**Acceptance criteria**
- [ ] `guard_label` takes the anchor and estimates the box the renderer draws for `start`, `middle`
      and `end`.
- [ ] Every figure passes **its own** viewBox, taken from one place rather than written beside the
      guard call and again in the `svg()` call.
- [ ] Every `text()` a figure emits is guarded, not a chosen subset.
- [ ] The false-alarm count on the shipping deck is **zero**, stated as a number rather than as a
      green run.
- [ ] T-210's clipped label is refused, proved by seeding it back.
- [ ] The deck rebuilds through its four-command chain and `check.py` is green.

**Open questions**
- None. The anchor question is answered by measurement above, and the rest follows from it.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Give `guard_label` an `anchor` parameter and compute the box per anchor; keep the centre default so existing callers are unchanged in meaning | `chart_probe.py` |
| 2 | Add a fixture per anchor to `chart_probe`'s own self-test, including the `start`-anchored clip it was blind to | evidence the guard sees what it claims |
| 3 | Make each figure's viewBox a value the figure states **once** and pass it to both `svg()` and the guard | `portfolio_charts.py` — one home per viewBox |
| 4 | Route every `text()` call through the guard, and **count the false alarms** on the shipping deck before keeping it | a number, per memory's *count false alarms against true hits* |
| 5 | Seed T-210's clipped label back and prove it is refused | evidence |
| 6 | Rebuild the deck through the four-command chain, run `check.py`, and look at the slides that changed | rule 6 |

## 3. Implement

**Decisions & assumptions**
- **The guard moved into `svg()`, which is the only place that holds a figure's body and its
  viewBox at once.** Guarding there means a figure cannot forget to opt in — **L-128**: a guarantee
  a caller can decline is not a guarantee. It also made the criterion *every `text()` is guarded*
  structural rather than forty edits, and it deleted the two hand-written calls instead of adding
  eight more. — 2026-08-21
- **`read_labels` stopped being a second copy of the box arithmetic, and the copy that was wrong was
  the guard's.** This file's `read_labels` has always read the anchor; `guard_label` never did. Both
  now call `chart_probe.label_box`, which is the one home — the file's own comment already claimed
  this (*"two estimates of one quantity disagree the first time either changes"*) and it was not
  true. — 2026-08-21
- **The margin is a parameter because the strict one refused seven of the ten figures.** Six of the
  seven were labels flush at the viewBox origin, which is how these figures place their axis
  labels; the breathing room is the slide's padding around the figure, not the figure's own. Flush
  is not clipped. `LABEL_MARGIN` stays the default for `chart_probe`'s own charts, where it was
  calibrated. — 2026-08-21
- **The slack is 2% of the viewBox width, and both sides of the threshold are measured.** With the
  margin at zero, one figure was still refused: `fig_scatter`'s *equal return per unit of risk*,
  estimated to overrun by **18 units on a 1728-wide box, 1%**. The rendered slide shows it well
  inside — the estimate over-reports because one font size stands in for every label class. The real
  defect from T-210 overran by **150 units on a 660-wide box, 23%**. Nothing sits between 1% and
  23%, so 2% separates them with an order of magnitude to spare. **This is a threshold with both
  sides measured rather than a tolerance chosen to make a run go green** (**L-51**). — 2026-08-21
- **`chart_probe`'s own tally was declared and already wrong.** It printed *SELFTEST OK - 12 checks*
  against eleven assertions. T-207 fixed exactly this in the sibling file; the count is derived from
  a `ran` list now and reads **16**. Not in the scope as written, and the same defect class, found
  because adding fixtures made me edit the number. — 2026-08-21

**Outputs produced**
- [`tools/assets/chart_probe.py`](../tools/assets/chart_probe.py) — `label_box`; `guard_label` gains
  `anchor`, `min_x`, `min_y`, `margin` and `slack`; five new fixtures; the tally is counted.
- [`tools/examples/portfolio_charts.py`](../tools/examples/portfolio_charts.py) — `guard_labels`
  called from `svg()`; `LABEL_FONT_PX`; `read_labels` delegates; the two hand-written calls removed.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| `guard_label` takes the anchor and estimates the box the renderer draws for `start`, `middle` and `end` | **met** | `label_box` computes the span; five fixtures cover the three anchors and the viewBox origin, in both directions — a label refused when `start`-anchored and accepted when centred at the same x, and one accepted at an offset origin and refused when the origin is read as zero. |
| Every figure passes **its own** viewBox, taken from one place | **met** | `svg()` parses the viewBox string it was already given and hands the origin, width and height to the guard. No figure names its viewBox twice. |
| Every `text()` a figure emits is guarded, not a chosen subset | **met** | Guarding happens in `svg()`, through which every figure's body passes. The two hand-written call sites were removed rather than multiplied. |
| The false-alarm count on the shipping deck is **zero**, stated as a number | **met** | **0 of 10 figures refused.** The path there is the evidence: **7 of 10** with the default margin, **1 of 10** with the margin at zero, **0 of 10** with the measured 2% slack. The one that survived to the last step was looked at on the rendered slide before the slack was chosen, not after. |
| T-210's clipped label is refused, proved by seeding it back | **met** | Seeded: `'5.1 pts renewables, from zero'` at x=484, `start`-anchored, refused as `est. 484..880` against a 660-wide viewBox starting at 120. A second seed, the same label `end`-anchored past the left edge, is refused as `est. -66..180`. The file was restored and verified byte-identical after each. |
| The deck rebuilds through its four-command chain and `check.py` is green | **met** | `0 failure(s): none`. **The deck's bytes are unchanged by this task** — the only diff against `HEAD` is T-210's two lines, the band rectangle and the figure description. A guard that changes no output is the correct outcome here. |
| *(closing checklist step 3)* | **met** | Slides 7 and 10 were rendered and looked at while this task was open — slide 7 is what decided the slack. Neither changed, so there is nothing further this task produced to look at. |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-22 | (shipped) | **Shipped in `0.6.0`.** The release note carries `docs/PUBLISHING.md` §8.1's row for this version, which names what an adopter must change and the smallest edit that satisfies it. |
| 2026-08-21 | → proposed | Raised by [T-210](T-210-the-drawdown-figures-shaded-band-is-emitted-at-zero-height.md), whose lengthened annotation printed clipped while the generator's 33 identities, `check.py` and the deck's own annotation identity were all green. The guard for exactly this exists and two of ten figures call it. `PH3`: the shipped deck is correct, and the exposure is the next label somebody lengthens. |
| 2026-08-21 | proposed → planned | §1 and §2 written together, because the measurement that decides the design was taken while T-210 was open. **The guard cannot be switched on as it stands**: handed `fig_drawdown`'s own viewBox width it refuses the clipped label *and* the correct one, because it assumes a centre anchor and that label is `start`-anchored. So the anchor is step 1 and the call sites are step 4, with the false-alarm count as the thing that decides whether it stays on. |
| 2026-08-21 | planned → done | The guard moved into `svg()`, so a figure cannot decline it (**L-128**), and `read_labels` stopped being a second copy of the box arithmetic — the copy that was wrong was the guard's, which never read the anchor. **The false-alarm count is the part worth keeping**: 7 of 10 figures refused with the inherited margin, 1 of 10 with the margin at zero, 0 of 10 with a slack of 2% of the viewBox width. That threshold has both sides measured — the real defect overran by 23% and the tightest correct label by 1%, with nothing between — and the correct label was looked at on the rendered slide before the number was chosen. T-210's clipped label is refused when seeded back. **The deck's bytes are unchanged.** `chart_probe`'s declared tally was found wrong on the way through, 12 claimed against 11 run, and is now counted at 16. |
