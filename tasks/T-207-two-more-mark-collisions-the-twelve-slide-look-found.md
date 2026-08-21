---
id: T-207
title: Fix two more mark collisions in the portfolio-review deck, found by looking at all twelve slides
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-203, T-204, T-210]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-21
updated: 2026-08-21
shipped_in: unreleased
deliverables: [tools/examples/portfolio_charts.py, examples/portfolio-review/portfolio-review.html]
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

1. **Take the fix from the mechanism §1 named, not from the symptom.** Both defects are the same
   shape: a mark placed at a **fixed offset from one origin** while the mark it lands near is placed
   from a different one, so neither is an input to the other. Nudging either offset moves the
   collision rather than removing it; the fix is to derive the loose mark from the thing it must
   clear.
2. **Slide 4** — the `+21 points` callout sits at `TOP + 4` while the series labels are positioned
   by `spread()`. Derive the callout from the spread result.
3. **Slide 10** — the annotation sits above the trough, and the recovery leg rises steeply out of
   it. Below the trough is the one region the line does not enter, by construction rather than by
   measurement.
4. **Prove both with the instrument [T-204](T-204-an-instrument-for-mark-collisions.md) just
   built**, which is the first time this repository can check this class without a person, and then
   **look anyway** — the instrument is new and its own calibration is one day old.
5. **Then the identities**, in the generator, in the shape T-203 used for the scatter.

## 3. Implement

**Decisions & assumptions**
- **Slide 4's callout moves; it does not merge** — 2026-08-21. §1's open question left merging to
  the owner because it changes what the slide says. Moving changes only where it says it, so it is
  this task's to take, and the question stays open for the owner rather than being answered by
  default.
- **The callout is derived from `end_ys`, the spread result** — 2026-08-21, placed 34 units above
  the topmost series label. A second fixed offset would have been the same fault at a new
  coordinate.
- **The annotation moves below the trough** — 2026-08-21. Everything above the trough is somewhere
  the line has been or is about to be; below it is clear whatever the recovery slope does, so the
  fix does not depend on this deck's numbers.
- **Slide 4's identity is a baseline gap, not a box comparison, and the seeding is what decided
  that** — 2026-08-21. The first version compared the boxes `read_labels` estimates, and **it did
  not fire when the defect was seeded back**: that reader assumes a single 22 px face for every
  label, and these two are set at different sizes, so its estimate showed no overlap where the
  browser measures 39%. A check that cannot see the thing it was written for is worse than no
  check, because it reads as coverage (**L-127** point 4, arriving in the task that cites it). The
  gap between baselines needs no font metrics at all and is the invariant the fix establishes.
- **The self-test's check count is now counted rather than declared** — 2026-08-21, and it is a
  deviation from this task's scope, reported here rather than done silently. `total` read
  `len(FIGURES) + 18`, a constant needing an edit in the same breath as any new identity. It had
  **already drifted once** — T-203 found it reading 12 — and adding two identities here would have
  made it wrong again by exactly the amount added. It is `len(ran)` now, and the run went from a
  false *28 of 28* to a true *30 of 30*.

**Outputs produced**
- [`tools/examples/portfolio_charts.py`](../tools/examples/portfolio_charts.py) — `fig_area`'s
  callout derived from the spread; `fig_drawdown`'s annotation moved below the trough; two
  identities added; the check total derived.
- [`examples/portfolio-review/portfolio-review.html`](../examples/portfolio-review/portfolio-review.html)
  — rebuilt through the four commands the generator prints.

**What the new instrument said, before and after.** DS-244 on this deck read **1 of 9 slides**
setting a label over another — naming slide 4, `'Renewables  31 → 52'` over `'+21 points'`, at 39%
of the smaller box — and 3 label-on-line placements including slide 10's. After the two fixes it
reads **0 of 9** and 2 placements. **Neither defect was seeded**: the instrument was pointed at the
shipped deck and independently named what a third human look had found, which is the strongest
evidence T-204 could have produced for itself.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :--- | :--- |
| Slide 4's callout and series label do not overlap, at any of the three measured resolutions | met | `markhits.py` reports 0 text-over-text on the deck, measured on the rendered page; `check.py`'s DS-244 row reads `0 of 9` and the gate ends `0 failure(s)`. Looked at: `+21 points` sits clear above `Renewables 31 → 52`, both legible |
| Slide 10's annotation does not cross the drawdown line | met | The `5.1 pts renewables` placement is gone from the tool's label-on-line list, which fell from 3 to 2. Looked at: the annotation sits below and right of the trough, clear of the recovery leg |
| The generator's self-test fails if either comes back, proved by seeding each defect | met, after the seeding rejected the first attempt | Two identities beside T-203's scatter pair — *the allocation callout clears the topmost series label by a line* and *the drawdown annotation clears the line it annotates*. Seeded: restoring `TOP + 4` fails the first at `gap 17.8 of 30 needed`, restoring `ty - 26` fails the second naming `5.1 pts renewables`; both pass on the fixed figures, 30 of 30. **The first version of the slide-4 identity did not fire when seeded** and was rewritten — see section 3. That is the criterion earning its place: written and not seeded, it would have shipped as coverage of nothing |
| `check_all.py` green, and all twelve slides looked at again, with the count said out loud | met | See section 3's note and the log row. **Two slides looked at in detail (4 and 10) and the twelve-slide pass repeated**; that pass is what found the third defect below, which is the count being said out loud rather than asserted |

**Child fix tasks raised**
- [T-210](T-210-the-drawdown-figures-shaded-band-is-emitted-at-zero-height.md) — the same figure's
  shaded band is emitted at `height="0.0"` and draws nothing, because `ry - ty` is negative and
  `rect()` clamps with `max(h, 0.0)`. Found by looking at slide 10 after this fix landed. Raised
  rather than fixed: what the band *means* has to be settled first, since 5.1 of 6.8 measured from
  the trough is 1.7 points and measured from zero is a different band.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-21 | → proposed | Raised from T-203's closing look, which covered all twelve slides and found two defects beyond the four it was fixing. Both are labels drawn over another mark, both are on slides that two earlier human looks had already passed, and both were green on every gate. Fifteen defects now in this deck's history, of which no instrument found one. |
| 2026-08-21 | → done, review | Both fixed at the mechanism rather than the offset: slide 4's callout is derived from `spread()`'s result instead of sitting at its own fixed `TOP + 4`, and slide 10's annotation moved below the trough, which is the one region the line does not enter whatever the recovery slope does. **T-204's instrument named slide 4 independently on the shipped deck, unseeded**, and both defects are gone from its output. Two identities added and proved by seeding - and the seeding **rejected the first version of the slide-4 one**, which compared font-metric estimates and did not fire; it is a baseline gap now, which needs no metrics. Reported deviation: the self-test's check total was a hand-kept constant that had already drifted once, so it counts what ran now - a false *28 of 28* became a true *30 of 30*. Looking at the fixed slide 10 found a third defect on the same figure, raised as [T-210](T-210-the-drawdown-figures-shaded-band-is-emitted-at-zero-height.md). |
