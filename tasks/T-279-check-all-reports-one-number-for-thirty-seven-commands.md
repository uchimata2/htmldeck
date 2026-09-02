---
id: T-279
title: Time each command check_all runs, so the gate's cost is measured rather than guessed
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-131, T-132]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-29
updated: 2026-08-29
shipped_in: unreleased
deliverables: []
---

# T-279 — Time each command check_all runs, so the gate's cost is measured rather than guessed

## 1. Specify

**Outcome**
`python tools/check_all.py` reports what each command cost, and ends with the few that dominate
named rather than left to be discovered. Today it prints **one** number for the whole run — `0
failure(s), 0 unclassified, 0 stale - 419 s` — so *which* of its 37 commands spends that time has
never been measured, and the first person to ask had to write a throwaway harness outside the
repository to find out.

**Where this came from.** The owner asked on 2026-08-29 whether a batch could be made faster without
giving up quality. Answering it needed a ranking, and there was none: `check_all.py` times only
`time.time() - started` around the whole run. The throwaway put the answer beyond doubt in one pass —
**seven commands are 95.1% of 452.9 s, and the other thirty are 22.2 s between them** — which is
exactly the shape a gate should be able to say about itself.

**Why this is worth a task rather than a note.** The ranking is not a curiosity; it decides where
optimisation may be attempted at all. Two of the three speed-ups the owner accepted follow directly
from it, and the one that was **refused** — making `--print-pages` conditional — was refused on the
strength of knowing it is 41.5%, not on a guess. A number nobody can re-derive is a number the next
session will guess at again.

**Scope**
- In: `tools/check_all.py` — a per-command duration, and a closing block naming the commands that
  dominate, printed on every run
- In: the same discipline the rest of that file already keeps — the account is a **partition**, so
  the per-command times must sum to the reported total rather than approximately to it
- Out: **changing what runs, or in what order.** This task measures; it removes no coverage and
  reorders nothing
- Out: parallelising anything, and reusing a browser between renders. Both are real and both are
  [T-280](T-280-every-render-pays-a-fresh-chrome-launch.md)'s, which this task's numbers are what
  justify
- Out: `--verbose` and `--quiet`'s existing contract, which is about output volume rather than time

**Inputs**
- `tools/check_all.py`'s `run_step`/`Result` and the `started = time.time()` it already keeps
- The throwaway's ranking, recorded in §3 so the first `--list`-driven measurement is not lost

**Acceptance criteria**
- [ ] every command's duration is printed beside it, and the run ends with the dominating commands
      named and their share of the total
- [ ] the per-command times **sum to the reported total** within the run's own overhead, and the
      report says what the difference is rather than hiding it
- [ ] a skipped command is distinguishable from one that took no time — `skipped` is not `0.0s`
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None. The shape is settled by the file's own idiom: it reports a partition and prints at zero.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Time each command where it is already run, in `run_step`, and carry it on `Result` | a duration per command, measured at the one place every command goes through |
| 2 | Print it beside each command, and keep `skipped` visibly distinct from a fast run | a line a reader can scan |
| 3 | A closing block: the commands that dominate, their share, and the cumulative share, slowest first | the ranking, without a throwaway |
| 4 | Reconcile the sum against the wall clock and print the difference rather than hiding it | the partition discipline this file keeps everywhere else |
| 5 | Both gates, run separately | green |

## 3. Implement

**Decisions & assumptions**

- **Timed in `run_one`, which is the one place every command goes through** — 2026-08-29. That makes
  the durations a partition of the run by construction rather than by anybody remembering to add
  one, which is the same reasoning the tool partition in this file already rests on. The reconcile
  line proves it: **280.4 s in commands against 280.4 s on the clock**, 0.1 s of it this file's own
  discovery and report.
- **`skipped` carries `seconds=None`, not `0.0`** — 2026-08-29. A command that did not run took no
  time in a different sense from one that ran fast, and printing `0.0s` would put a skipped checker
  at the fast end of a ranking that is about what to attack.
- **The cut is a share, not a count** — 2026-08-29. A fixed *top N* flatters a faster machine and
  hides a slow command on a slower one; cutting at 95% names however many commands actually
  dominate. **On this tree that is seven, and the other thirty are 13.7 s between them.**
- **The row that crosses the threshold is printed before breaking, and the first version got this
  wrong** — 2026-08-29. Cutting *above* the crossing row left a **41 s** command inside a bucket
  whose own label reads *none of them the reason a run is slow*. It shipped that way for exactly one
  run, which is the argument for printing a reconcile line: the sum was right while the story was
  not.
- **The absolute total moves between runs and the shares do not** — 2026-08-29, measured across
  three full runs at **452.9 s**, **417.8 s** and **280.4 s** on an otherwise unchanged tree. The
  ranking held: `contract_variants` 23.6–25.2%, `static_variants` 18.7–21.1%, `figures.py`
  9.9–10.6%. So a before/after for [T-280](T-280-every-render-pays-a-fresh-chrome-launch.md) has to
  be stated as a **share**, or as a same-session pair — a wall-clock figure quoted across sessions
  is the kind of number `L-95` is about.
- **The sweep caught this task's own neighbour, which is the first evidence it works on a real
  edit** — 2026-08-29. Recording the owner's ruling on `DS-218` changed that rule's row, and the run
  went red with `SWEEP DS-218 CHANGED since it was read`. Re-read and re-recorded: the edit added a
  confirmation, not a testable assertion, and `DS-218` was already in `CONJUNCTIONS_OWED`.

**Outputs produced**
- [`tools/check_all.py`](../tools/check_all.py) — `Result.seconds`, the timing in `run_one`, and the
  *where the time went* block with its reconcile line
- [`tools/deck/check.py`](../tools/deck/check.py) — `DS-218`'s sweep digest re-recorded

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every command's duration printed, and the run ends with the dominating commands named and their share | pass | Seven named at 95.1%, slowest first, with each command's share and the cumulative share |
| The per-command times **sum to the reported total**, and the report says what the difference is | pass | `280.4s in commands, against 280.4s on the clock - 0.1s is this file's own discovery and report`. The gap is printed, not absorbed |
| A skipped command is distinguishable from one that took no time | pass | `seconds=None` for a skip; it never enters the ranking, so it cannot masquerade as fast |
| `lint.py` and `check_all.py` green, run separately | pass | Run separately. The gate went red once mid-task — the clause sweep catching this session's own `DS-218` edit — which is the mechanism working, not a defect |

**Child fix tasks raised**
- [T-280](T-280-every-render-pays-a-fresh-chrome-launch.md) — the launch floor the ranking exposed:
  a render is 0.94 s and a blank page is 0.58 s of it

**Nothing rendered, so no look is owed.** The change is to a report about the gate; no deck, theme
or shell file is touched.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → done | Timed in `run_one`, the one place every command goes through, so the durations are a partition by construction - and the reconcile line proves it at **280.4 s in commands against 280.4 s on the clock**. Seven commands are **95.1%** and the other thirty are **13.7 s** between them. **The first version's tail bucket lied**: it cut above the crossing row, leaving a 41 s command inside a bucket labelled *none of them the reason a run is slow*. Measured across three runs, the **absolute total moves** - 452.9, 417.8, 280.4 s on an unchanged tree - **and the shares do not**, so `T-280`'s before/after must be a share or a same-session pair. The clause sweep went red mid-task on this session's own `DS-218` edit, re-read and re-recorded: the first evidence it fires on a real change. |
| 2026-08-29 | → proposed | Raised after the owner asked whether a batch could be made faster without giving up quality. The question could not be answered from the repository — `check_all.py` reports one number for 37 commands — so a throwaway harness ranked them outside the tree, and this task moves that capability inside it. **`PH3`**: tooling the owner asked for, not a defect an adopter met in the published `0.6.0`. |
