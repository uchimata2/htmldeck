---
id: T-183
title: DS-063 failed once in four full-gate runs on a tree no code change touched
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-179, T-054]
work_package: PH3
owner: the project owner
business_value: high
effort: m
created: 2026-08-18
updated: 2026-08-18
deliverables: [tools/deck/contract.py]
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

<not started>

## 3. Implement

**Decisions & assumptions**
- <none yet>

**Outputs produced**
- <none yet>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :--- | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-18 | → proposed | Observed rather than looked for: four gate runs in one session, the fourth red on a tree differing from the third by two Markdown files, the fifth green on that same tree. Raised instead of re-run and forgotten, because the thing that makes it worth a record is exactly that re-running made it go away. `PH3` by [`../CLAUDE.md`](../CLAUDE.md)'s rule — the published plugin's decks are correct and no adopter is affected; what is affected is this repository's own confidence in its gate. |
