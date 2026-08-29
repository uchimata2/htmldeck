---
id: T-280
title: Every render pays a fresh Chrome launch, and the launch is most of the render
type: fix
status: done
phase: review
parent: null
blocked_by: [T-279]
related: [T-279]
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-08-29
updated: 2026-08-29
deliverables: [tools/deck/render.py, tools/deck/contract.py, tasks/TOOLING.md]
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

**What the sizing probes measured, 2026-08-29, before any code changed.** Six launches per cell on
an idle 16-core machine, `--dump-dom`, through `render.chrome_run` unmodified:

| What | Serial, per launch | 4 at once, per launch | Speed-up |
| :--- | ---: | ---: | ---: |
| `about:blank` — the launch floor | 0.351 s | 0.235 s | 1.49x |
| `examples/reference-deck.html` | 0.526 s | 0.303 s | **1.74x** |
| So: page work per render | 0.175 s | | |
| `mkdtemp` + `rmtree` for the throwaway profile | **0.0003 s** | | |
| Same launch against a **shared** profile | 0.295 s | | saves 0.05 s |

**Three things follow, and two of them cut against the spec's own framing.**

1. **The share holds, the seconds do not.** §1 recorded 0.94 s and 0.58 s, a 62% floor; today the
   same pair is 0.526 s and 0.351 s, a **67%** floor. The absolute figures differ by machine state
   and the share does not, which is `T-279` §3's rule arriving from a second direction. Roughly
   **two thirds of every render is Chrome starting**, and that is the figure to carry.
2. **The isolation the spec worried about is nearly free.** The throwaway profile costs 0.0003 s to
   create and remove, and a launch that reuses one profile saves 0.05 s of 0.345 s — **15% of the
   floor, 8% of a render**. So `--user-data-dir` is not what a shared browser would be buying;
   process startup is. Giving up the isolation guarantee for the profile alone is not a trade worth
   naming.
3. **Parallelism saturates at two, not at sixteen.** Blank-page launches ran 1.49x at 2 workers,
   1.45x at 4, 1.53x at 8 and 1.37x at 12 — flat inside noise from 2 upward on a 16-core machine.
   Launching Chrome is not CPU-bound, so cores do not buy throughput here, and a worker count above
   about 4 is decoration. Real deck renders reach **1.74x**, better than blank ones because the page
   work parallelises where the startup does not.

**And hypothesis *(a)* has a cost the spec did not price.** Reusing one browser means driving it
over CDP, whose DOM-returning half is WebSocket-only; `urllib` reaches `/json/*` and nothing more.
`tools/` currently imports **zero** third-party packages and the repository ships no requirements
file, so *(a)* is either a new dependency in the instrument that decides false greens, or a
hand-rolled WebSocket client in it. That is the thing to weigh against its ceiling, not the profile.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Size the launch before touching anything — blank against deck, serial against parallel, profile setup on its own | The table above |
| 2 | Fan out **at the call site, not inside `chrome_run`** — one launch per job, order preserved, every job keeping its own process, its own throwaway profile and its own blackholed DNS | A `render` helper taking a list of jobs and a worker count, and the count's justification |
| 3 | Convert only the browser-bound loops that dominate the ranking: `contract_variants.py`, `static_variants.py`, and `render.measure`'s per-slide loop | Three call sites, and a stated reason for every browser-driven tool left serial |
| 4 | Prove the instrument unchanged — run both seeded suites before and after, compare CAUGHT and MISSED as **sets** | The two set comparisons, quoted rather than counted |
| 5 | Re-run `check_all.py` and state the saving as a **share** off its own ranking | Before and after shares for the commands that dominate |
| 6 | Decide *(a)* on that evidence and record the answer either way | §3's decision row — a refusal is a complete outcome |

## 3. Implement

**Built *(b)*, refused *(a)*, and the refusal is the more useful half.**

**Decisions & assumptions**
- **Fan out at the call site over one already-written probe, never across decks** — 2026-08-29.
  This is a constraint found while scoping, not a preference: probe names are **per-tool constants**
  (`contract.html`, `variant.html`, `glitchfree.html`) and `render.out_dir` resolves to the
  **project's** `.assets-cache/deck`, not the deck's. So two different decks rendered concurrently
  through one tool write one path, and each would read the other's page. Both conversions fan out
  over launches that read a probe written once above them, which has no such hazard.
  `in_parallel`'s docstring carries the rule.
- **Four workers, measured** — 2026-08-29. Blank-page launches ran 1.49x at two, 1.45x at four,
  1.53x at eight and 1.37x at twelve on a 16-core machine: flat inside noise from two upward,
  because starting Chrome is not CPU-bound. `HTMLDECK_RENDER_WORKERS` overrides it and `1` restores
  a plain serial loop, which is what a render diagnosis should use.
- **`static_variants.py` stays serial, and this is the reason rather than an omission** — its
  browser half is one launch per variant through `render_failures`, `reduced_failures` and
  `glitchfree.verdicts`, each of which renders once. There is no loop inside a variant to overlap,
  so its only parallelism is *across* variants — exactly the different-decks-one-probe-path
  collision above. Making it safe means giving probes per-deck addresses, which changes `make_probe`
  and `out_dir` for every tool that calls them. That is a wider change than this task, and it is
  worth about **15 s** of a 221 s gate.
- **Refused *(a)*, reusing one browser across renders** — 2026-08-29, on two measurements and one
  fact:
  - **the isolation it would trade away is not where the time is.** `mkdtemp` plus `rmtree` for the
    throwaway profile costs **0.0003 s**, and a launch against a shared profile saves **0.05 s of
    0.345 s**. The spec named `--user-data-dir` as the hazard; the profile is nearly free, and only
    sharing the **process** reaches the remaining 0.30 s;
  - **its ceiling is real but its cost is a protocol.** CDP's DOM-returning half is WebSocket-only —
    `urllib` reaches `/json/*` and no further. `tools/` imports **zero** third-party packages and the
    repository ships no requirements file, so *(a)* is either a new dependency inside the instrument
    that decides false greens, or a hand-rolled WebSocket client inside it;
  - **and *(b)* already took 1.70x off the command *(a)* was aimed at**, while giving up no isolation
    at all. A second, larger speed-up bought with a hand-written protocol and shared storage between
    renders is not a trade this gate should make before it needs to.
- **Nothing was removed.** Same decks, same viewports, same slides, same checks — the launches
  overlap and nothing else changed.

**Outputs produced**
- [`tools/deck/render.py`](../tools/deck/render.py) — `DEFAULT_WORKERS`, `workers()`,
  `in_parallel()`, `measure`'s per-slide loop, and the ordering case in `self_test`
- [`tools/deck/contract.py`](../tools/deck/contract.py) — `sweep`'s per-viewport loop
- [`tasks/TOOLING.md`](TOOLING.md) — what the knob does and when to set it to `1`

**What it measured.** Interleaved on one machine in one session, the **only** variable being the
worker count, so nothing here is a comparison across machine states:

| Command | serial (two runs) | fanned out (two runs) | |
| :--- | ---: | ---: | ---: |
| `contract_variants.py` | 66.2 / 67.9 s | 39.4 / 39.6 s | **1.70x** |
| `check.py examples/reference-deck.html --print-pages` | 29.6 / 28.1 s | 23.1 / 22.3 s | **1.27x** |

And on the gate itself, two `check_all.py` runs minutes apart, the second with the change:

| | before | after | |
| :--- | ---: | ---: | ---: |
| the whole run | 280.0 s | **221.2 s** | 1.27x, 21% off |
| `contract_variants.py` | 67.9 s — **24.2%** | 40.4 s — **18.3%** | matches the isolated 1.70x |
| the four `check.py` deck runs | 27.1 to 29.5 s | 20.7 to 22.9 s | matches the isolated 1.27x |
| `static_variants.py` — untouched | 57.9 s | 57.2 s | 1.01x, as it should be |
| `figures.py` — launches no browser | 27.5 s | 21.7 s | **noise, and it is why the two isolated A/Bs above are the evidence** |

`figures.py` moved 21% with nothing touching it, which sizes the run-to-run variance at about the
same magnitude as `check.py`'s whole improvement. That is exactly the trap `T-279` section 3 warns
about, and it is why the claim rests on the interleaved A/B rather than on the two gate runs — the
gate numbers **agree** with it, they do not carry it.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The seeded-variant suites report an **identical** set of CAUGHT and MISSED before and after, compared as sets | pass | `contract_variants` 8 rows, `static_variants` 48 rows, sets equal. **Stronger than asked**: both suites' entire output is byte-identical, and so is `check.py`'s at `HTMLDECK_RENDER_WORKERS=1` against `4`. The before came from the committed tree with the change stashed, not from the new code with the knob turned down |
| The saving is **measured on the gate** and stated as a before/after from `T-279`'s ranking | pass | 280.0 s → 221.2 s, and `contract_variants` 24.2% → 18.3% of the run. Backed by an interleaved A/B, because a command the change cannot reach moved 21% between those same two runs |
| If a hypothesis is refused, the measurement that refused it is recorded and says so plainly | pass | *(a)* refused in section 3, on the 0.0003 s profile cost, the 0.05 s shared-profile saving, and CDP's WebSocket-only DOM half against a toolchain with zero third-party imports |
| Whatever isolation a shared browser gives up is **named**, and either shown not to matter or restored | pass | **None is given up.** Every job keeps its own process, its own throwaway `--user-data-dir` and its own `MAP * ~NOTFOUND`. The hazard the spec named belongs to *(a)*, which was refused |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | pass | Both green on the tree as committed, run separately |

**And the fan-out's own failure mode is seeded, not assumed.** `in_parallel` returning results in
completion rather than job order is silent — callers index what they get back, and one displaced row
reports a catastrophic disagreement on a deck with nothing wrong with it (T-183). `render.self_test`
runs eight jobs that finish in reverse and requires job order. Seeded by swapping `ex.map` for
`as_completed`: the self-test failed with that message, and passed again when it was put back.

**Child fix tasks raised**
- none. `static_variants`' variant-level fan-out is named in section 3 with what it would cost and
  what it is worth; it is a candidate, not a defect, and nobody has asked for 15 s

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → proposed | Raised while adding `T-279`'s timing, from the measurement that answering *what is slow* turned up: a render is **0.94 s** and a blank page is **0.58 s** of it, so most of every render is Chrome starting. `contract_variants.py` alone makes **114** launches and spends **100%** of its wall time in them. **Blocked by `T-279`** rather than merely related: without the per-command ranking there is no before/after to state, and a speed-up nobody can measure is the kind of claim this repository does not accept. **`PH3`**: tooling, not a defect an adopter met in the published `0.6.0`. |
| 2026-08-29 | planned → done | Built *(b)* and **refused *(a)***. The gate went 280.0 s → **221.2 s** and `contract_variants.py` 1.70x, measured by an interleaved A/B on the worker knob alone — because `figures.py`, which launches no browser, moved 21% between the same two gate runs and would have carried a third of the claim if those runs were the evidence. Both seeded suites print **byte-identical** output before and after. The scoping found a constraint nobody had written down: probe names are per-tool constants and `out_dir` is per-project, so a fan-out across decks would have two renders reading one file — which is why `static_variants` stays serial. |
| 2026-08-29 | proposed → planned | Planned off four sizing probes taken before any edit, recorded in §2. Two of them cut against §1's framing: the throwaway profile costs **0.0003 s**, so the isolation a shared browser would give up is not where the time is, and parallel launches **saturate at two workers** on a 16-core machine, so *(b)*'s ceiling is about **1.74x** on real renders rather than anything core-shaped. The launch share reproduced at **67%** against §1's 62% while the seconds did not, which is `T-279` §3 again. *(a)* is now priced: CDP's DOM half is WebSocket-only, and `tools/` imports zero third-party packages. |
