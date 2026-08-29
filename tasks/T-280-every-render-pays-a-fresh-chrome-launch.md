---
id: T-280
title: Every render pays a fresh Chrome launch, and the launch is most of the render
type: fix
status: proposed
phase: specify
parent: null
blocked_by: [T-279]
related: [T-279]
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-08-29
updated: 2026-08-29
deliverables: []
---

# T-280 — Every render pays a fresh Chrome launch, and the launch is most of the render

## 1. Specify

**Outcome**
The gate spends its time measuring decks rather than starting browsers. **A render costs 0.94 s and
0.58 s of that is Chrome starting and stopping** — `render.chrome_run` spawns a fresh process with a
fresh throwaway profile for each one, and one checker makes 114 of them.

**The measurement, taken 2026-08-29** and the whole reason this is a task rather than an instinct:

| What | Measured |
| :--- | :--- |
| A render of `reference-deck.html`, `--dump-dom` | **0.94 s** (two runs, 0.95 / 0.93) |
| A render of a **blank page**, same flags | **0.58 s** (0.57 / 0.59) — launch, profile, teardown, no page work |
| So: page work per render | **0.36 s**, and **0.58 s is floor** |
| `contract_variants.py` | **114 launches**, 106.7 s in Chrome, **100%** of its 106.9 s wall |
| `static_variants.py` | **37 launches**, 36.3 s in Chrome, **43%** of its 83.9 s wall |
| The whole gate | 452.9 s; the seven dominating **commands** are 95.1% of it |

**114 launches × 0.58 s ≈ 66 s of `contract_variants`' 107 s is process startup**, and nothing is
being measured during it.

**But *browser-driven command* and *time spent in a browser* are not the same figure, and conflating
them would send this task at the wrong half.** `static_variants` spends **47.7 s outside Chrome** —
more than half its run — building fifty variant decks and deciding the static ones in Python. And
`figures.py`, fifth in the ranking at 45.5 s, launches no browser at all. So of the seven dominating
commands, **two are all browser, one is mostly not, and one is none of it.** This task is the launch
floor; `static_variants`' Python half is a separate question nobody has opened yet, and it is worth
about as much.

**Two hypotheses, and neither is adopted here.** *(a)* **Reuse one browser** across renders, driving
it rather than re-launching it. *(b)* **Run the launches in parallel**, since they are independent.
Both are plausible and both are **hypotheses about an instrument**, which is the one place this
repository refuses to guess.

**Why this needs the seeded suites rather than a stopwatch.** A faster gate that decides differently
is not a faster gate, it is a broken one — the whole B1 wave exists because three instruments were
answering wrongly and everything verified against them had to be verified again. Two specific
hazards, and each is a reason the current design may be right:

- **The throwaway profile is an isolation guarantee, not an accident.** `--user-data-dir` is a fresh
  temporary directory per launch and `--host-resolver-rules=MAP * ~NOTFOUND` blackholes DNS. A
  shared browser shares storage and cache between renders, so a variant could pass because an
  earlier render left something behind — a false green in the exact instrument that decides false
  greens.
- **Parallel Chromes contend.** The geometry rules read layout, which should be load-independent;
  the motion rules read animation state, which may not be. `render.py` already carries a seam
  between motion facts and settled geometry for a related reason (T-261).

**Scope**
- In: `tools/deck/render.py`'s `chrome_run` and whatever reuse or parallelism a measurement supports
- In: **proving the instrument unchanged** — the seeded-variant suites produce the same CAUGHT and
  MISSED sets before and after, which is what makes a speed-up admissible at all
- In: refusing either hypothesis and recording why, if that is what the measurement says. **A
  refusal is a complete outcome here**, and eight consecutive batches have produced one
- Out: removing any check, deck or viewport from the gate. This is the same work, faster, or it is
  nothing
- Out: `--print-pages`, which the owner ruled on 2026-08-29 stays unconditional — its 41.5% is
  known and accepted, and skipping it by condition is a silent cap
- Out: the per-command ranking itself, which is [T-279](T-279-check-all-reports-one-number-for-thirty-seven-commands.md)

**Inputs**
- [T-279](T-279-check-all-reports-one-number-for-thirty-seven-commands.md) — the ranking this rests
  on, and the instrument that will say whether anything got faster
- `tools/deck/render.py` `chrome_run`, and the flags each launch carries
- `static_variants.py`, `contract_variants.py` — the fixtures that decide whether the instrument
  still decides the same things

**Acceptance criteria**
- [ ] the seeded-variant suites report an **identical** set of CAUGHT and MISSED before and after,
      compared as sets rather than as counts
- [ ] the saving is **measured on the gate**, not on a microbenchmark, and stated as a before/after
      from `T-279`'s own ranking
- [ ] if a hypothesis is refused, the measurement that refused it is recorded here and the finding
      says so plainly
- [ ] whatever isolation a shared browser gives up is **named**, and either shown not to matter or
      restored some other way
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- **Is a shared browser's leaked state reachable by any rule the suites decide?** Not known. The
  cheapest answer is probably empirical: run the suites against a reused browser and compare sets,
  rather than reasoning about what Chrome persists.
- **How much parallelism does this machine actually have to give?** Unmeasured. Two independent
  Chromes may be nearly free or may halve each other's speed, and that decides whether *(b)* is
  worth any of *(a)*'s risk.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <the files this task changed>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- <T-NNN or "none">

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → proposed | Raised while adding `T-279`'s timing, from the measurement that answering *what is slow* turned up: a render is **0.94 s** and a blank page is **0.58 s** of it, so most of every render is Chrome starting. `contract_variants.py` alone makes **114** launches and spends **100%** of its wall time in them. **Blocked by `T-279`** rather than merely related: without the per-command ranking there is no before/after to state, and a speed-up nobody can measure is the kind of claim this repository does not accept. **`PH3`**: tooling, not a defect an adopter met in the published `0.6.0`. |
