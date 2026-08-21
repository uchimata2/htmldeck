---
id: T-207
title: Fix two more mark collisions in the portfolio-review deck, found by looking at all twelve slides
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-203, T-204]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-21
updated: 2026-08-21
deliverables: []
---

# T-207 — Fix two more mark collisions in the portfolio-review deck, found by looking at all twelve slides

## 1. Specify

**Outcome**
Slides 4 and 10 carry no label drawn over another mark. Both are the same class as the four
[T-203](T-203-four-chart-defects-the-decks-look-missed.md) fixed, and both survived every gate.

**How they were found**
By the twelve-slide look T-203's last acceptance criterion required, on 2026-08-21 — after the four
fixes were in and `check_all.py` was green. **Neither slide is one of the two T-113's look missed**:
slides 4 and 10 were both covered by that pass and by the owner's review, and passed both. So this is
not a coverage failure like the last one; it is the same blind spot in a pair of human looks, which
is the argument [T-204](T-204-an-instrument-for-mark-collisions.md) exists to make.

**The two, with the mechanism**

| Slide | Symptom | Mechanism |
| :--- | :--- | :--- |
| **4** — five-series allocation | the `+21 points` callout and the `Renewables 31 → 52` series label are set on top of each other | The callout is placed relative to the accent series' end point and the series label by `spread()`, and neither is an input to the other. They land about 18 px apart on a 22 px face, so the ascenders of one meet the descenders of the other |
| **10** — the drawdown line | `5.1 PTS RENEWABLES` is drawn across the recovery leg of the line | The annotation sits at a fixed offset from the trough. The line rises steeply out of the trough, so the label's own box crosses the segment it is annotating |

**Scope**
- In: the two fixes, in [`tools/examples/portfolio_charts.py`](../tools/examples/portfolio_charts.py),
  and the rebuild chain the generator prints.
- In: extending the generator's own geometry identities to cover both, in the shape T-203 added for
  the scatter — a label box against a line, and a label box against another label.
- Out: the general instrument. That is still T-204's, and these two are two more subjects for it.

**Inputs**
- [`tools/examples/portfolio_charts.py`](../tools/examples/portfolio_charts.py) — `fig_area`,
  `fig_drawdown`, and the `read_labels` / `seg_hits_box` helpers T-203 added above `selftest`.
- [T-203](T-203-four-chart-defects-the-decks-look-missed.md) §3 — the four fixes and the identities,
  which this repeats rather than reinvents.

**Acceptance criteria**
- [ ] Slide 4's callout and series label do not overlap, at any of the three measured resolutions.
- [ ] Slide 10's annotation does not cross the drawdown line.
- [ ] The generator's self-test fails if either comes back, proved by seeding each defect and
      watching the check fire — the method T-203 used on its own two.
- [ ] `check_all.py` green, and all twelve slides looked at again, with the count said out loud.

**Open questions**
- Whether slide 4's callout should move or merge into the series label. Merging is fewer marks and
  is probably right, but it changes what the slide says rather than only where it says it, so it is
  the owner's call rather than this task's.

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
| 2026-08-21 | → proposed | Raised from T-203's closing look, which covered all twelve slides and found two defects beyond the four it was fixing. Both are labels drawn over another mark, both are on slides that two earlier human looks had already passed, and both were green on every gate. Fifteen defects now in this deck's history, of which no instrument found one. |
