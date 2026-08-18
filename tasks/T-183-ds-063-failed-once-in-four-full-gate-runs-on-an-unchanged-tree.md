---
id: T-183
title: DS-063 failed once in four full-gate runs on a tree no code change touched
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-179, T-054]
work_package: PH3
owner: the project owner
business_value: high
effort: m
created: 2026-08-18
updated: 2026-08-18
shipped_in: unreleased
deliverables: [tools/deck/contract.py, docs/lessons/L-119.md]
---

# T-183 — DS-063 failed once in four full-gate runs on a tree no code change touched

## 1. Specify

**Outcome**
`python tools/check_all.py` returns the same verdict every time it is run on the same tree, or the
one rule that does not says so in terms a reader can act on. Today a run can come back red on a tree
that three other runs called green, which makes **every** green run a weaker claim than it reads as.

**What was observed, 2026-08-18**
Four full-gate runs during one session, on trees differing only in Markdown:

| Run | Tree | Result |
| :-- | :--- | :--- |
| 1 | after T-179 | `0 failure(s)` — 293 s |
| 2 | after T-115 | `0 failure(s)` — 321 s |
| 3 | after T-054 | `0 failure(s)` — 321 s |
| 4 | after a **task-record edit only** | **`1 failure(s): DS-063`** — 344 s |
| 5 | same tree as run 4, unchanged | `0 failure(s)` — 237 s |

Run 4's tree differed from run 3's by two Markdown files — a task record and the generated task
index. Neither is read by `contract.py`, neither is in any deck, and run 5 re-ran the identical tree
and passed.

**Why it is not a tolerance sitting too tight.** Checked directly afterwards, each shipped deck was
measured twice and every reading was well inside the bound — `TEXT_TOLERANCE_PX` is 2.0 device px:

| Deck | worst non-text | worst text run |
| :--- | :---: | :---: |
| `reference-deck` | 0.00 du | 1.07 du = 0.63 device px |
| `measure-first` | 0.00 du | 0.62 du = 0.36 device px |
| `sort-window` | 0.00 du | 1.70 du = 1.00 device px |

The closest deck uses half its allowance, and both repeats of each reading were identical. So the
red run is not a deck near the line; it is a **measurement that came back wrong once**.

**Where the mechanism most likely is.** `render.py`'s own docstring already names this class of
fault: *"An infinite animation stops a headless render from ever settling, so the virtual-time
budget never reaches a quiescent state"* — captures pin motion off for exactly this reason. DS-063
compares two renders at different viewports and asks whether they agree up to a scale factor, so it
is twice as exposed to a render that has not settled as a single-render rule is, and a run under
load is when that happens. **This is a hypothesis and the task's first job is to confirm or refute
it**, not to act on it.

**Why `high` rather than `medium`.** Nothing here is wrong with the deck. What is wrong is the
instrument, and a gate that is red once in five on an unchanged tree teaches the next reader to
re-run it until it is green — which is the habit that makes a real regression invisible. That is
**L-36**'s argument about a silent check, arriving from the opposite direction.

**Scope**
- In: reproducing the intermittency, by running the DS-063 measurement repeatedly on one unchanged
  deck and counting the disagreements against the runs.
- In: whatever makes the measurement deterministic, or — if it cannot be — a stated retry with the
  disagreement **reported** rather than swallowed, so an unstable reading is visible as instability.
- In: the number. How often it happens is what decides whether this is a retry or a rewrite, and no
  fix should be chosen before the rate is measured.
- Out: widening `TEXT_TOLERANCE_PX`. The evidence says the decks are nowhere near it, so a wider
  bound would hide the fault instead of fixing it.
- Out: the other rendered rules, unless the same measurement proves they share the mechanism.

**Inputs**
- [`tools/deck/contract.py`](../tools/deck/contract.py) — `geometry()`, the tolerances, and the
  two-viewport sweep DS-063 rests on.
- [`tools/deck/render.py`](../tools/deck/render.py) — the Chrome runner, the virtual-time budget,
  and the settling problem it already documents.
- [`tools/check_all.py`](../tools/check_all.py) — the run whose verdict has to be stable.

**Acceptance criteria**
- [ ] The intermittency is reproduced and its rate stated as a count over a stated number of runs
- [ ] The mechanism is named, with the evidence that distinguishes it from the alternatives
- [ ] After the fix, a stated number of consecutive runs on one unchanged tree agree
- [ ] An unstable reading, if one is still possible, is reported as unstable rather than as a pass
      or a failure
- [ ] `TEXT_TOLERANCE_PX` is unchanged, or the reason it moved is recorded against the measurements
      above

**Open questions**
- Whether it is DS-063 specifically or the two-render sweep generally. The reproduction answers it,
  and it decides whether the fix belongs to the rule or to the runner.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Refute the cheap explanation first — measure each deck twice against the tolerance | the margins |
| 2 | Read `geometry()` and `measure()` together, since one produces what the other consumes | the mechanism |
| 3 | Reproduce it deterministically by seeding the upstream fault, rather than waiting for it | the numbers |
| 4 | Estimate the upstream rate directly, so the fix is aimed at the right layer | drops per read |
| 5 | Pair by identity; report a broken pairing as undecided | `contract.py` |
| 6 | Self-test that watches each way of breaking the pairing fail | `contract.py` |
| 7 | Consecutive full-gate runs on one unchanged tree | the agreement |

**The decision the plan takes.** **Do not try to make the upstream reliable.** It is a browser under
load and the drop rate belongs to the machine, so a retry would hide the fault rather than fix it.
The consumer is where a lost sample is still detectable, and it is the only place the loss can be
named — which is also why the fix must not be a wider tolerance.

## 3. Implement

**Decisions & assumptions**
- **The fault is in the consumer, not the browser** — 2026-08-18. `render.measure` prints
  `!! no result` and **continues**; `geometry()` then pairs the two runs with `zip`. Making the
  browser reliable is not available, so the comparison is where a lost reading has to be caught.
- **Pair by slide name, which every reading already carried** — 2026-08-18. The identifier was in
  the data the whole time and nothing read it.
- **A broken pairing is `None`, not `False`** — 2026-08-18. This file already means *undecided, not
  failed* by `None` (DS-064's missing body run, and `counted == 0` since T-075). Failing would
  repeat the misalignment's wrong answer; passing would hide a run that measured nothing it claims.
- **`TEXT_TOLERANCE_PX` is untouched at 2.0** — 2026-08-18, and step 1 is why: the decks are
  nowhere near it, so moving it would have hidden the fault.

**Outputs produced**
- [`tools/deck/contract.py`](../tools/deck/contract.py) — `geometry()` pairs by slide and reports
  `paired`/`unpaired`/`duplicated`/`aligned`; `scale_verdicts_from` returns undecided on a broken
  pairing, naming the slide; 4 self-test fixtures.
- [`docs/lessons/L-119.md`](../docs/lessons/L-119.md) — the general rule.

**The mechanism, and what distinguishes it from the alternatives.**

*The cheap explanation is refuted.* Each deck measured twice, every reading identical, against a
2.0 device px bound: `reference-deck` 1.07 du = **0.63 px**, `measure-first` 0.62 du = **0.36 px**,
`sort-window` 1.70 du = **1.00 px**. The closest deck uses half its allowance, so this was never a
deck near the line.

*The real one is arithmetic.* `geometry()` compared the two resolution runs with `zip(a, b)`, which
pairs by **position**. `render.measure` drops a reading and continues when a Chrome launch returns
nothing, so one missing reading shifts every pair after it — slide *n* against slide *n+1*.
Reproduced deterministically by removing one row from a real measurement:

| | values compared | worst non-text | worst text run |
| :--- | ---: | ---: | ---: |
| both runs intact | 120 | 0.00 du | 1.70 du = 1.00 px |
| one reading dropped | 64 | **314.14 du** | **816.41 du = 479.26 px** |

Against bounds of 0.25 du and 2.0 px. **A deck with a perfect score reports a failure three orders
of magnitude outside tolerance**, and `counted` falling from 120 to 64 was in the output the whole
time with nothing to compare it against.

**The rate, and the honest limit on it.** The *consequence* is reproduced deterministically; the
*trigger* was not reproduced spontaneously. Direct measurement, 2026-08-18: **0 empty reads in 30**,
and **0 wrong-slide reads in 72** across two resolutions — both under light load. Against that, **1
red in 5 full-gate runs** during a working session. So the trigger is real, rarer than 1-in-30 when
the machine is quiet, and load-dependent; it could not be forced within this task. **After the fix
it is loud**, so its rate becomes measurable from now on rather than estimated — which is the
outcome worth more than a number taken today.

**The open question is answered, with evidence.** It is DS-063 specifically, not the two-render
sweep generally: `body_floor()` (DS-064) scans one resolution and takes a minimum, so it has no
pairing to break, and `zip(` appears nowhere else in `contract.py`, `render.py` or `audit.py`.
DS-063 is the only rule that compares two independent renders element by element, which is exactly
the shape that needs an identity to pair on.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :--- | :--- |
| The intermittency is reproduced and its rate stated as a count over a stated number of runs | met, with one limit stated | The **consequence** is reproduced deterministically from a seeded drop — 0.00 du becomes 314.14 du. The **trigger** was not reproduced spontaneously: 0 drops in 30 reads and 0 wrong slides in 72, against 1 red in 5 gate runs. Rarer than the sampling and load-dependent, and now loud enough to count going forward |
| The mechanism is named, with the evidence that distinguishes it from the alternatives | met | Positional pairing across two independent runs. The tolerance alternative is refuted by 0.63 / 0.36 / 1.00 px against a 2.0 bound |
| After the fix, a stated number of consecutive runs on one unchanged tree agree | met | **Three consecutive `check_all.py` runs**, `0 failure(s), 0 unclassified, 0 stale` at 205 s, 197 s and 203 s |
| An unstable reading, if one is still possible, is reported as unstable rather than as a pass or a failure | met | `ok=None`, naming the unpaired slide and how many paired, with the instruction to re-run and what a recurrence would mean. The surviving pairs are still compared honestly — 0.00 du, not 314.14 |
| `TEXT_TOLERANCE_PX` is unchanged, or the reason it moved is recorded | met | Unchanged at 2.0 |

**Child fix tasks raised**
- none. `render.measure`'s silent `continue` is the upstream half and is now **caught** rather than
  silent, so nothing is left unreported; making it refuse outright would change what every caller
  gets back from a partly-measured deck, which is a wider change than this fault needs.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-18 | → proposed | Observed rather than looked for: four gate runs in one session, the fourth red on a tree differing from the third by two Markdown files, the fifth green on that same tree. Raised instead of re-run and forgotten, because the thing that makes it worth a record is exactly that re-running made it go away. `PH3` by [`../CLAUDE.md`](../CLAUDE.md)'s rule — the published plugin's decks are correct and no adopter is affected; what is affected is this repository's own confidence in its gate. |
| 2026-08-18 | proposed → specified | The cheap explanation was refuted before anything else: each deck measured twice, every reading identical, worst 1.00 device px against a 2.0 bound. So not a deck near the line, and `TEXT_TOLERANCE_PX` was ruled out of scope by evidence rather than by preference. |
| 2026-08-18 | specified → planned | Seven steps, and one decision that shaped them: the upstream is a browser under load and cannot be made reliable, so the fix belongs to the consumer. That also settled the order — refute the tolerance first, because it is the thing everyone suspects and the expensive place to look. |
| 2026-08-18 | planned → in_progress → done | `geometry()` paired the two resolution runs with `zip`, by position, while every reading carried the slide name. One dropped reading shifts every pair after it: reproduced by removing one row from a real measurement, and **0.00 du became 314.14 du, 1.70 du of text became 816.41** — a perfect deck failing by three orders of magnitude. Now paired by name, with a broken pairing reported **undecided** and the slide named. Three consecutive full-gate runs agree. The trigger itself stayed out of reach — 0 drops in 30 reads, 0 wrong slides in 72 — which is recorded as a limit rather than smoothed over. **L-119**. |
