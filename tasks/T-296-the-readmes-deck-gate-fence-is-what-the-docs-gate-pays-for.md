---
id: T-296
title: Decide what a documentation commit may skip on the front page, since one README fence is the whole cost
type: decision
status: proposed
phase: specify
parent: T-287
blocked_by: []
related: [T-285, T-286, T-292]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
finding: CE-18
created: 2026-09-02
updated: 2026-09-02
deliverables: []
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

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Put the three candidates to the owner with the measurement beside each | the ruling |
| 2 | Implement it, and seed the check that the skip cannot go silent | the change |
| 3 | Time both modes on one frozen tree | the table |

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
| 2026-09-02 | → proposed | Raised in B20 by [T-292](T-292-the-docs-gate-is-four-fifths-one-render.md), which refused its own remedy on a measurement. `CE-18` named the coverage account as what runs the deck gate inside `figures.py`; emptying `ACCOUNTS` leaves the run in place, so the subject is the README's output fence and the remedy is a different one. **Not absorbed into B20** under §4's elastic: every candidate removes something the front page guarantees on every documentation commit, which is a ruling rather than a fix. `PH3`. |
