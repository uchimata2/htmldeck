---
id: T-206
title: DS-063 gives a different verdict on identical input, so no run of the gate settles it
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-183, T-203, T-204]
work_package: PH3
owner: the project owner
business_value: high
effort: m
created: 2026-08-21
updated: 2026-08-21
deliverables: []
---

# T-206 — DS-063 gives a different verdict on identical input, so no run of the gate settles it

## 1. Specify

**Outcome**
`check.py`'s DS-063 row returns the same verdict every time it is pointed at the same bytes. Today it
does not, and a row that answers differently on each run cannot fail a release honestly or pass one.

**How it was found**
While closing [T-203](T-203-four-chart-defects-the-decks-look-missed.md) on 2026-08-21. The deck was
unchanged between runs, the command was byte-identical, and nothing else was running:

| Run | Worst disagreement | Verdict | Named element |
| :--- | :--- | :--- | :--- |
| 1 | 5.65 du | FAIL | `Top three assets hold 34% / body / w` |
| 2 | 18.00 du | FAIL | `Concentration, not performance / bottomLine / y` — **and the non-text row failed too, at 18.00 du of 0.25 allowed** |
| 3 | 1.24 du | pass | `Top three assets hold 34% / svgName / w` |
| 4 | 4.16 du | FAIL | — |
| 5 | 4.57 du | FAIL | — |
| 6 (inside `check_all.py`) | — | pass | — |

**What is stable, which is the useful half.** `render.py measure` is *repeatable* when it is given a
slide list: slide 1 alone read 0.00 du three times, slide 8 alone read 1.24 du three times, and a
whole-deck `measure` read 1.24 du on both this deck and the one committed at `2475ee5`. So the
instrument is not inherently noisy — something in how the gate drives it is. That is the first place
to look, and it is why this is filed against DS-063's use of `render.py` rather than against
`render.py` itself.

**A lead, not a diagnosis.** Run 2 moved a `y` coordinate by 18 du on two elements that both carry
the `rise` entrance animation, and `render.py`'s own docstring records that under this invocation a
CSS animation's clock is frame production rather than time (**L-26**, T-185). An element measured
mid-entrance in one resolution pass and settled in the other would produce exactly this. Unproven.

**This is [T-183](T-183-ds-063-failed-once-in-four-full-gate-runs-on-an-unchanged-tree.md)'s
symptom, after T-183's fix — and it is that task's own unfinished half.** T-183 found DS-063
pairing the two resolution runs by *position*, so one dropped reading shifted every pair after it,
and repaired it to pair by name (**L-119**, shipped in `0.5.0`). It could not reach the **trigger**:
*0 drops in 30 reads, 0 wrong slides in 72*, recorded there as a limit rather than smoothed over.
Two things follow.

- **The magnitudes say this is not the old bug returning.** A shifted pairing produced 314.14 du
  where 0.00 was right, and 816.41 where 1.70 was. What is seen now is 4.16 to 18.00 — wrong, but
  wrong by a factor, not by three orders. So the name-pairing repair is holding and something else
  is moving the readings.
- **The trigger T-183 could not catch is now catchable.** It took 30 reads to find nothing then; it
  took six runs to see four failures now. Whatever this is, it can be reproduced on demand, which
  is the thing that was missing.

**`PH3`, on T-183's own reasoning**, quoted because it is the same judgement and should not be made
twice: *the published plugin's decks are correct and no adopter is affected; what is affected is
this repository's own confidence in its gate.*

**Scope**
- In: making DS-063's verdict a function of the deck's bytes.
- In: a regression test that would have caught this — the same deck measured *n* times, same answer.
- Out: changing what DS-063 *means*, or its tolerances. A flaky check and a wrong threshold are
  different faults and fixing them together hides which one moved.

**Inputs**
- [T-183](T-183-ds-063-failed-once-in-four-full-gate-runs-on-an-unchanged-tree.md) — **start here.**
  The pairing fix, and § by § what it ruled out: the tolerance was refuted by evidence, not by
  preference, and the trigger is named as unreached.
- [`docs/lessons/L-119.md`](../docs/lessons/L-119.md) — pairing two independent measurements by
  position turns a rare dropped sample into a false verdict.
- [`tools/deck/contract.py`](../tools/deck/contract.py) — `geometry()`, where the pairing and the
  verdict live.
- [`tools/deck/render.py`](../tools/deck/render.py) — `measure`, `calibrate`, `read_result`, and the
  docstring's account of headless animation timing.
- [T-185](T-185-no-instrument-here-can-watch-an-animation-play.md) — the measurement behind L-26.

**Acceptance criteria**
- [ ] Ten consecutive `check.py` runs on one unchanged deck return the same DS-063 verdict and the
      same worst value.
- [ ] The same holds for a deck that genuinely violates DS-063 — the row still fails, every time.
- [ ] The cause is named in §3, not merely suppressed. A tolerance widened until the noise fits is
      not a fix and is out of scope above.

**Open questions**
- Whether the fault is in the gate's use of `render.py` or in `render.py` under a whole-deck sweep.
  The evidence points at the former, since single-slide and whole-deck `measure` are both stable.
- Whether a broken pairing is still being reported as **undecided** rather than as a failure, which
  is what T-183 built it to do. If DS-063 is failing where it should be declining to answer, that is
  a smaller fix than the trigger and should be checked first.

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
| 2026-08-21 | → proposed | Raised while closing T-203, which could not tell whether its own change had broken the gate. Six runs of one command on one unchanged file: four FAIL at 4.16, 4.57, 5.65 and 18.00 du, two pass. `render.py measure` is repeatable on the same deck — single-slide readings identical three times over, and a whole-deck read identical on this deck and on the one committed at `2475ee5` — so the noise is in how the gate drives it rather than in the instrument. **Filed against T-183 rather than as a new discovery**: that task repaired the pairing and named the trigger as beyond its reach at 0 drops in 30 reads. The magnitudes rule out the old bug returning — a shifted pairing gave 314 and 816 du, this gives 4 to 18 — and the trigger it could not catch now reproduces in a handful of runs. `PH3` on T-183's own reasoning, quoted in §1. |
