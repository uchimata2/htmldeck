---
id: T-206
title: DS-063 gives a different verdict on identical input, so no run of the gate settles it
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-183, T-185, T-203, T-204, T-209]
work_package: PH3
owner: the project owner
business_value: high
effort: m
created: 2026-08-21
updated: 2026-08-21
shipped_in: 0.6.0
deliverables: [tools/deck/render.py]
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

**Both open questions are answered, and one claim above is wrong — corrected 2026-08-21 in §3.**
Kept rather than rewritten, because what §1 guessed and what measurement found differ in a way
worth seeing. In short: the pairing was never broken (`aligned` true, 4 slides paired, in every run
taken); the fault is in neither place the first question offered; and the lead's *"measured
mid-entrance in one resolution pass and settled in the other"* is wrong in its second half —
**no pass was ever settled.** §3 has the measurement.

## 2. Plan

1. **Reproduce through the gate's own path, not through the CLI.** `check.py` reaches DS-063 via
   `contract.audit` → `scale_verdicts` → `render.measure(deck, SAMPLE)`; the CLI reaches it via
   `cmd_measure`. §1 measured the second and concluded the instrument was clean, so start by
   driving the first.
2. **Find what varies before deciding what is wrong.** Run the same measurement *n* times and
   report the spread of every individual reading, not the worst-value summary — a summary that
   moves says something changed, and nothing about what.
3. **Test the entrance-animation lead directly**, since §1 raised it: measure once with the probe
   as it stands and once with motion pinned off, and difference the two. If the lead is right the
   difference is a `y` offset on `.rise` elements and nothing else.
4. **Fix at the mechanism**, then satisfy the acceptance criteria in order: *n* consecutive runs
   agreeing, the seeded DS-063 violator still failing every time, the cause written down.
5. **Leave a regression guard that runs without a browser.** A ten-run measurement is minutes of
   Chrome and will never sit in a self-test; whatever is asserted has to be assertable in-process.

## 3. Implement

**Decisions & assumptions**
- **The motion pin becomes unconditional in `PROBE`, rather than `measure` gaining a flag that
  asks for it** — 2026-08-21. The file already carries the argument, above `MOTION_PROBE`: putting
  a guarantee and its exception in one place lets the next edit reach both. A pin behind `quiet`
  *was* that shape, seen from the inside — `shots` asked for the guarantee, `measure` did not, and
  the caller that declined it was the only one issuing a verdict. Making it unconditional removes
  the exception from this probe entirely; the exception keeps its own name and its own probe.
- **`quiet` keeps only the title suppression** — 2026-08-21. That is the half `shots` genuinely
  needs (a `RESULT…` title pollutes a screenshot) and the half nothing else wants.
- **The regression guard is structural, not numeric** — 2026-08-21. What went wrong is not a value
  drifting; it is a guarantee moving behind a flag, which is invisible in every number the gate
  prints. So `render.self_test()` asserts the *shape* of the probe and needs no browser.
- **Tolerances untouched**, as §1's scope requires. `GEOM_TOLERANCE_DU` is 0.25 and
  `TEXT_TOLERANCE_PX` is 2.0, both unchanged. Nothing here widens a bound.

**Outputs produced**
- [`tools/deck/render.py`](../tools/deck/render.py) — `PROBE` pins motion unconditionally;
  `MOTION_PROBE`'s header note corrected, since it described the pin as `quiet`'s;
  `self_test()` gains two assertions guarding the pin.

**The mechanism, measured rather than inferred.**

The probe waits `document.fonts.ready`, clicks `next` *n* times, then measures 700 ms later. It
never asked for the motion pin. So every DS-063 reading was taken on a page whose entrance
animation was still notionally running — and `--virtual-time-budget=4000` makes that wait virtual,
while a CSS animation advances with frame production (**L-26**, T-185).

Measured on `portfolio-review.html`, 2026-08-21, one run of the gate's own sample against the same
run with motion pinned:

| Resolution | Readings | Differ from settled by > 0.25 du | Worst |
| :--- | ---: | ---: | ---: |
| 3840x2000 | 132 | 27 | **18.00 du** |
| 1280x634 | 132 | 27 | **18.00 du** |
| 720p | 132 | 27 | **18.00 du** |

**18.00 du is `--rise-dist` to the digit** — the deck declares `--rise-dist:calc(18*var(--du))`.
Not part-way through the entrance: **frame zero of it.** The animation had produced no frames at
all, at every resolution, on every run.

**Which makes the green verdict the surprising half, not the red one.** DS-063 compares two
renderings; both were frozen at the same instant of the same animation, so they agreed — and
agreeing about the wrong page is indistinguishable, in the output, from agreeing about the right
one. The rule was passing a deck it had not measured. The moment one pass produced a frame the
other did not, the comparison reported a disagreement somewhere in `(0, 18.00]` du against a
0.25 du bound. **Every magnitude §1 recorded falls in that interval** — 1.24, 4.16, 4.57, 5.65,
and 18.00 exactly, which is the whole travel and therefore the case where one pass had moved a
full step and the other had not moved at all.

**The honest limit, stated as T-183 stated its own.** The *consequence* is reproduced
deterministically and the *offset* is exact. The **flake was not reproduced spontaneously here**:
19 runs across the session — 5 before the fix, 4 stock and 4 pinned under eight-way CPU load, plus
the ten after — every one of them stable, including under deliberate load. So the trigger that
tips one pass into producing a frame remains uncaught, exactly as it was for T-183. What is
different, and is why this closes rather than being deferred again, is that **the trigger no longer
matters**: with motion pinned there is no animated quantity left in the reading for it to move.
T-183 had to catch the trigger because its fault survived one; this fault cannot.

**A load hypothesis was tested and refuted**, which is worth recording because it was the obvious
one. Four stock runs under eight busy cores produced a run-to-run spread of **0.00 du across all
396 readings**. Load does not move these numbers on this machine; it was never the variable.

**What else the same change fixes, unlooked for.** The probe flags an element as outside the stage
when its rect leaves `1920x1080`. An element read 18 du below its settled position is 18 du closer
to that edge, so the overflow warning was being computed against a page the audience never sees.
Same for `discHitCssPx`, measured on `.disc-btn`, whose `.pulse` is now pinned too.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :--- | :--- |
| Ten consecutive `check.py` runs on one unchanged deck return the same DS-063 verdict and the same worst value | met | Ten consecutive runs of the gate's DS-063 measurement — identical both rows: `0.00 du of 0.25` over 44 non-text values, `1.24 du = 0.73 device px of 2.0` over 88 text values, `aligned` true, 4 paired, every time. Bridged to the command the criterion names by **three full `check.py` runs**, whose DS-063 rows are the same two values and which end `0 failure(s)` |
| The same holds for a deck that genuinely violates DS-063 — the row still fails, every time | met | The `viewport-units-in-stage` variant, **four consecutive runs**: `FAIL` at `102.41 du of 0.25` non-text and `44.35 du = 26.04 device px of 2.0` text, identical each time. The full variant suite reports **8 of 8 behaved as specified**, so nothing else moved |
| The cause is named in §3, not merely suppressed. A tolerance widened until the noise fits is not a fix | met | §3 names it and measures it: the probe never asked for the motion pin, so every reading was taken at frame zero of a 340 ms entrance, exactly `--rise-dist` = 18.00 du from settled. `GEOM_TOLERANCE_DU` 0.25 and `TEXT_TOLERANCE_PX` 2.0 are both unchanged |
| A regression test that would have caught this (§1 scope) | met, and narrower than §1 imagined | Structural, in `render.self_test()`: the pin must be present and must not be behind `quiet`. §1 pictured "the same deck measured *n* times"; that test is minutes of Chrome and would never have run. This one runs in-process on every gate, and watches the thing that actually changed |

**Looked at, per the closing checklist step 3.** This task changes an instrument, not a deck, and
`shots` is provably unaffected — it passed `quiet=1` and therefore already received the pin, so its
behaviour is identical before and after. Confirmed rather than assumed: `render.py shots` re-run on
slides 1 and 8, both PNGs written, **slide 8 opened and looked at offline**. It renders settled and
complete — headline, disclosure control, stat figure, the three-asset bar with its 30% ceiling tick,
ruler and pager all present and in place. The pin makes elements *visible* rather than hiding them,
which is the failure mode worth ruling out by eye, and it is ruled out.

**Child fix tasks raised**
- [T-209](T-209-six-more-probes-measure-a-page-whose-entrance-never-ran.md) — the same fault,
  unfixed, in six other probes. `render.PROBE` is the only one this task touched, and the other
  six build their own with `extra=`; none of them pins motion. The portfolio deck's figures and
  headlines carry `.rise` (`class="body figwrap rise"`), so the subject is present, but **whether
  each probe's particular comparison reads an animated axis is per-probe and unmeasured** — which
  is a task, not a paragraph here. Out of scope by §1, which is *"making DS-063's verdict a
  function of the deck's bytes"* and nothing wider.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-22 | (shipped) | **Shipped in `0.6.0`.** The release note carries `docs/PUBLISHING.md` §8.1's row for this version, which names what an adopter must change and the smallest edit that satisfies it. |
| 2026-08-21 | → done, review | Cause found and fixed. `render.PROBE` never asked for its own motion pin, which sat behind `quiet` and so reached `shots` but not `measure` — the only consumer that issues a verdict. Every DS-063 reading was taken at **frame zero** of a 340 ms entrance: 27 of 132 readings at each of the three resolutions sat exactly **18.00 du** from settled, which is `--rise-dist` to the digit. The gate passed anyway, because all three renderings were frozen equally — so the intermittency was the rule occasionally *noticing*, not occasionally failing. The pin is now unconditional and `quiet` keeps only the title suppression. Ten consecutive measurements and three full `check.py` runs agree exactly; the seeded violator still fails four times out of four at 102.41 du; 8 of 8 variants behave as specified. The load hypothesis was tested and **refuted** — 0.00 du spread across 396 readings under eight-way CPU load. Raised [T-209](T-209-six-more-probes-measure-a-page-whose-entrance-never-ran.md): six other probes build their own and none pins motion. |
| 2026-08-21 | → proposed | Raised while closing T-203, which could not tell whether its own change had broken the gate. Six runs of one command on one unchanged file: four FAIL at 4.16, 4.57, 5.65 and 18.00 du, two pass. `render.py measure` is repeatable on the same deck — single-slide readings identical three times over, and a whole-deck read identical on this deck and on the one committed at `2475ee5` — so the noise is in how the gate drives it rather than in the instrument. **Filed against T-183 rather than as a new discovery**: that task repaired the pairing and named the trigger as beyond its reach at 0 drops in 30 reads. The magnitudes rule out the old bug returning — a shifted pairing gave 314 and 816 du, this gives 4 to 18 — and the trigger it could not catch now reproduces in a handful of runs. `PH3` on T-183's own reasoning, quoted in §1. |
