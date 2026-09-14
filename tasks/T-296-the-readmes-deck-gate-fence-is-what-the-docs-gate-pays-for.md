---
id: T-296
title: Decide what a documentation commit may skip on the front page, since one README fence is the whole cost
type: decision
status: done
phase: review
parent: T-287
blocked_by: []
related: [T-285, T-286, T-292]
work_package: PH3
shipped_in: 1.0.0
owner: the project owner
business_value: medium
effort: s
finding: CE-18
created: 2026-09-02
updated: 2026-09-14
deliverables: [tools/docs/figures.py, tools/check_all.py, tasks/TOOLING.md]
---

# T-296 — Decide what a documentation commit may skip on the front page, since one README fence is the whole cost

## 1. Specify

**Outcome**
`python tools/check_all.py --docs` stops paying for a headless Chrome render on every documentation
commit, or the owner rules that it should keep paying and the reason is written down.

**Why this is not [T-292](T-292-the-docs-gate-is-four-fifths-one-render.md).** That task asked what
`figures.py`'s **coverage account** should bind to, on `CE-18`'s statement that the account is what
runs `check.py`. Measured 2026-09-02: it is not. Empty `ACCOUNTS` entirely and `check.py` still runs,
because [`../README.md`](../README.md) pastes that command's output in a fence and `figures.py`
compares the paste against a live run. The account is a **second reader of a run that happens
anyway**, so rebinding or skipping it saves nothing. `T-292` closed leaving the account exactly where
it was, and this is the remedy the measurement pointed at instead.

**Closes** `CE-18` in [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.3 — reopened against
its true subject.

**The decision, and why it is the owner's.** Every candidate trades away something the front page
currently guarantees on every documentation commit:

- **Skip the render-driving fence under `--docs`, with a printed reason.** The full gate still
  compares it, and the batch's landing owes the full gate in every case. The cost is that a
  documentation commit can change the README's pasted gate output and go green.
- **Paste a cheaper command's output.** `ruleset.py --counts` prints the ruleset half with no render
  at all. The cost is that the front page stops showing what the gate says about a real deck, which
  is the thing a reader is being shown.
- **Keep paying.** 33 s per documentation commit, and the guarantee stays whole.

**Scope**
- In: the README fence, `figures.py`'s handling of a render-driving command, and `check_all.py`'s
  argv for one entry if the first candidate is taken.
- Out: the coverage account, which `T-292` settled; the full gate's own behaviour.

**Inputs**
- `../docs/CONTEXT-AUDIT.md` §6.3, `CE-18`
- `T-292` §3 — the measurement that reshaped this

**Acceptance criteria**
- [ ] The candidate taken is measured before and after, in both modes, on one tree.
- [ ] Whatever the front page stops guaranteeing on a documentation commit is written down where a
      reader of that guarantee will meet it.
- [ ] Full gate green.

**Open questions**
- Which candidate. The owner's, because each one trades a guarantee rather than an implementation.
  **Answered by the owner 2026-09-13: the first** — skip the render-driving fence under `--docs`,
  with a printed reason. The full gate still compares it at every batch landing.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Put the three candidates to the owner with the measurement beside each | the ruling, 2026-09-13 |
| 2 | Time both gate modes on the unchanged tree, before any edit | the before row |
| 3 | Measure which prose figures bind to `check.py`'s output, since a skip must not unbind them | the binding list |
| 4 | Implement the skip in `figures.py`, pass it from `check_all.py`, and seed the checks that it cannot go silent | the change |
| 5 | Time both modes again on the committed tree | the after row |

## 3. Implement

**Decisions & assumptions**
- **The skip is conditional, which removes the cost the ruling accepted** — 2026-09-14. The owner
  took candidate 1 with its stated cost: a documentation commit could change the pasted gate output
  and stay green. Under `--docs`, `figures.py` now reads the `check.py` block instead of running it
  only while the block is identical to its copy at `origin/master`. Everything `check.py` reads is
  under a path `check_all.py --docs` refuses on, so the full gate that tree took gives the same
  answer. A commit that edits the block still pays for the render. Reversible: drop the base
  comparison in `docs_skips()`.
- **The pasted block stands in for the run, so the prose stays bound** — 2026-09-14. Measured before
  the change with `figures.py --report`: two prose figures bind to `check.py`'s output, 93 `checked`
  and 122 `owned by a gate`, and both lines are in the paste. The declared account resolves from the
  same two lines. Nothing that was compared becomes unbound.
- **The base and the refusal are loaded from `check_all.py`, not restated** — 2026-09-14. So
  `figures.py --docs` run alone cannot skip a block that `check_all.py --docs` would refuse to skip.
- **What a documentation commit still loses** is a render verdict that moves with no file changing,
  such as a browser update. Every deck gate `--docs` skips already has that gap, and the batch
  landing's full run closes it. Written in [`TOOLING.md`](TOOLING.md) §1.4, where `--docs` is
  described, and in `DOCS_SKIPPED`'s comment.

**Measured 2026-09-14**, one machine, `check_all.py` wall seconds. Before: tree `3b7e821`, clean.
After: the same commit plus this task's diff, frozen for both runs.

| Mode | Before | After | Verdict both times |
| :--- | ---: | ---: | :--- |
| `--docs` | 25.6 | 8.5 | 9 ran, 35 skipped, 0 failed |
| full | 203.2 | 202.0 | 42 ran, 2 skipped, 0 failed |

`figures.py` alone, after: 3.1 s under `--docs` and 20 s in full. Its partition is the same in both
modes — 17 fences, 11 prose numerals, 33 figures in 5 documents — and `--docs` adds one line naming
the block it read instead of ran. **Seeded, not assumed:** an untracked file under `tools/deck/` made
`docs_base()` skip nothing, and the probe file was removed. The self-test's fixture 13 covers the
rest: a base whose block differs, a base that does not resolve, a page that moves a skipped block,
and a `DOCS_SKIPPED` entry naming no command.

**Outputs produced**
- `tools/docs/figures.py` — `DOCS_SKIPPED`, `docs_skips()`, `missing_docs_skips()`, `docs_base()`,
  the `skipped` row in the partition, and fixture 13
- `tools/check_all.py` — a list as a WIDE entry's third element is its docs-mode argv tail, and the
  self-test asserts it
- `tasks/TOOLING.md` §1.4 — what `--docs` does to the README block, and what it still loses
- `docs/CONTEXT-AUDIT.md` — `CE-18` closed
- [`../docs/lessons/L-165.md`](../docs/lessons/L-165.md) — skip on a checked base, not on a mode

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The candidate taken is measured before and after, in both modes, on one tree | met | The table in §3. Each pair ran on one frozen tree, and the before pair ran before any edit |
| Whatever the front page stops guaranteeing on a documentation commit is written down where a reader of that guarantee will meet it | met | Less is lost than the ruling accepted, because the skip is conditional. The remainder, a render verdict that moves with no file changing, is in `TOOLING.md` §1.4 and in `DOCS_SKIPPED`'s comment beside the code that makes the skip |
| Full gate green | met | The after full run in §3: exit 0 |

**Open question answered.** The owner chose the first candidate on 2026-09-13. §3's first decision
records how it was carried out and why the result is stronger than the ruling asked for.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-02 | → proposed | Raised in B20 by [T-292](T-292-the-docs-gate-is-four-fifths-one-render.md), which refused its own remedy on a measurement. `CE-18` named the coverage account as what runs the deck gate inside `figures.py`; emptying `ACCOUNTS` leaves the run in place, so the subject is the README's output fence and the remedy is a different one. **Not absorbed into B20** under §4's elastic: every candidate removes something the front page guarantees on every documentation commit, which is a ruling rather than a fix. `PH3`. |
| 2026-09-13 | (no change) | The owner chose the first candidate. Still `proposed`. |
| 2026-09-14 | → specified | B25. §1 was complete and its one open question answered, so specifying added nothing. |
| 2026-09-14 | → planned | §2 rewritten: time both modes before any edit, and measure what binds to `check.py` before skipping it. |
| 2026-09-14 | → in_progress | The measurement moved the design. Only 93 and 122 bind to `check.py`, and both are pasted, so the pasted block can stand in for the run. The skip keys on the block matching the base, not on the mode. |
| 2026-09-14 | → done | `--docs` 25.6 → 8.5 s, full unchanged and green. `CE-18` closed, L-165 written. |
