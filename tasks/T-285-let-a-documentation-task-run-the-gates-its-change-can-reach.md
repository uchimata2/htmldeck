---
id: T-285
title: Let a documentation task run the gates its change can reach, and keep the full run for the batch
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-279, T-280]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-09-02
updated: 2026-09-02
deliverables: []
---

# T-285 — Let a documentation task run the gates its change can reach, and keep the full run for the batch

## 1. Specify

**Outcome**
`python tools/check_all.py --docs` runs the repository-wide gates and prints the per-deck gates and
the two rendered-variant suites as **skipped, with the reason** — *no deck-facing path changed since
the last full green* — and **refuses the flag** when the diff against that tree touches `tools/deck/`,
`shell/`, `themes/` or `examples/`. A documentation task's commit is gated by the checks whose subject
it changed, in well under a minute; the batch's landing runs the full gate on the tree that is pushed,
exactly as today.

**Measured 2026-09-01, on B17's last run.** 211 seconds: the two seeded-variant suites 93 s (44%),
`check.py` over the four decks 83 s (39%), `figures.py` 21 s, the other 32 commands 9 s. B17's three
tasks changed documents, `figures.py`, `check_all.py` and a new checker; four full runs re-proved the
deck gates four times against a tree where nothing they read had moved. The gate was about 14 of the
batch's 47 minutes, and B18 to B22 are documentation batches.

**Asked for by the owner on 2026-09-02**, after B17, as [T-279](T-279-check-all-reports-one-number-for-thirty-seven-commands.md)
and [T-280](T-280-every-render-pays-a-fresh-chrome-launch.md) were after B11: *can a batch be made
faster without giving up quality*. The shape follows `check_all.py`'s own partition — a gate that does
not run is **skipped with a stated reason**, never absent — so the saving is declared in the output
rather than taken by habit.

**Scope**
- In: the `--docs` flag, the skip reason, and the refusal by path prefix, which errs towards the full
  run: a diff touching any of the four prefixes cannot run in docs mode
- In: what *the last full green* is compared against. Recommended: `origin/master`, because under
  [`../docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) §4 a pushed tree is a fully gated
  one, so no machine-local state is needed and nothing has to survive a `git pull`
- In: the partition's self-test asserts both directions — a diff touching `shell/` under `--docs`
  refuses, and a docs-only diff skips exactly the deck gates and the two rendered suites
- In: `HTMLDECK_RENDER_WORKERS` at 8 against the default 4, as an interleaved A/B on the two variant
  suites — T-280's method, one variable at a time — kept only if the verdicts stay byte-identical
  and the time falls; recorded either way
- In: `tasks/TASK-WORKFLOW.md` §7 and `tasks/TOOLING.md`'s gate rule, so the closing criterion says
  which run a documentation task's commit owes and which the batch's landing owes
- Out: skipping a gate by a hash of its declared inputs. That is a hand-kept input list per checker,
  the shape this repository distrusts, and the remaining batches are documents
- Out: any change to what a full run does or prints

**Inputs**
- [`../tools/check_all.py`](../tools/check_all.py) — `WIDE`, `PER_DECK`, the partition and its self-test
- [`../tools/deck/render.py`](../tools/deck/render.py) — `DEFAULT_WORKERS`, and T-280's byte-identity proof
- [`TOOLING.md`](TOOLING.md) §1 — the two-gates rule and the rule against editing while one runs
- [`../docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) §4 — commit per task, push per batch

**Acceptance criteria**
- [ ] `--docs` on a docs-only diff prints every deck gate and both rendered suites as skipped with
      the reason, runs everything else, and finishes in under 40 s on the machine B17 measured
- [ ] `--docs` on a diff touching any of the four prefixes refuses, naming the path, and the
      self-test proves both directions
- [ ] A full run's verdicts are unchanged byte for byte
- [ ] The workers A/B is recorded with both timings and the byte-identity result, whichever way it went
- [ ] `TASK-WORKFLOW.md` §7 and `TOOLING.md` say what a documentation task's commit owes and what a
      batch's landing owes

**Open questions**
- Whether the comparison base is `origin/master` or a recorded last full green — the owner. The
  recommendation above is `origin/master`; the cost if that is wrong is one full run per batch that
  docs mode could have skipped

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <path>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- <T-NNN or "none">

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-02 | → proposed | Asked for by the owner after B17, from the question *why does a batch take so long*. Measured first: 83% of a 211 s full run renders decks and fixtures no documentation task can change, and B17 paid it four times. `PH3` per `CLAUDE.md`: this repository's own tooling, not a defect in the published plugin. To be implemented in a session of its own, by the owner's instruction. |
