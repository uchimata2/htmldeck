---
id: T-086
title: Check that every figure ledger row appears on the slides its Used on names
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-082, T-071]
work_package: v0.2
owner: the project owner
business_value: medium
effort: m
created: 2026-08-10
updated: 2026-08-10
deliverables: []
---

# T-086 — Check that every figure ledger row appears on the slides its Used on names

## 1. Specify

**Outcome**
A gate reads a foundation's figure ledger against the built deck and fails a row whose `Used on`
names a slide that does not show the value. The check is exact rather than heuristic, because it
searches for a known string on a known slide instead of deciding what a figure is.

**Why this one**
[T-082](T-082-the-worked-examples-figure-ledger-omits-figures-that-reach-slides.md) §3 decided the
ledger's two directions are not equally checkable, and this is the half that is. Its sweep found
four rows over-claiming — `12.4%` named slides 4 and 9, `2.4%` named 11 and 12, `84%` named 7, `16%`
named 5 — and the deck shows none of them there. SPEC-4 reads `Used on` to decide whether a slide's
`Sources` field is right, so a cell naming a slide the figure never reached mis-calibrates the one
check built on the ledger.

**The other direction stays a judge rule, and T-082 §3 records why.** Completeness needs something
that can enumerate every figure on a slide; `content.py`'s `FIGURE` pattern cannot see `6 rounds`,
`04:10`, `27 of 31` or `31 peak working days`, and widening it to any digit makes every axis tick a
figure. A completeness gate built on that instrument would pass a ledger missing exactly what this
sweep found missing.

**Scope**
- In: a new rule, over `foundation.md` plus the built `.html`, that every `Used on` slide shows the
  row's value.
- In: where it lives. `spec.py` compares two specifications and takes no deck; `content.py` takes a
  deck and sources and builds its own ledger rather than reading the hand-written one. Neither
  signature fits, and picking one over a third tool is the first decision.
- In: how a row that legitimately renders differently is handled — `4.1 / 11.2 / 15.9 / 18.7%` is
  one row and four marks, and `first working week of January` is prose. A rule that cannot express
  those will be switched off rather than fixed.
- Out: ledger completeness, which T-082 §3 decided stays `judge`.
- Out: the reference deck's ledger, until this runs on `sort-window` first.

**Inputs**
- [`tools/deck/spec.py`](../tools/deck/spec.py) — SPEC-4 and the `used_on` parser to reuse.
- [`tools/deck/content.py`](../tools/deck/content.py) — `runs()` and the per-slide split, which
  already solve reading a deck's text per slide.
- [`examples/sort-window/sort-window.foundation.md`](../examples/sort-window/sort-window.foundation.md)
  — 58 rows, complete and corrected, which is the calibration case.

**Acceptance criteria**
- [ ] The rule exists, and names the row and the slide when it fails
- [ ] It is green on `sort-window` as T-082 left it
- [ ] It is red on a seeded defect — a `Used on` cell given a slide that does not show the value —
      and the seed asserts it landed
- [ ] The multi-value and prose row forms are handled, or explicitly excluded with a recorded reason
- [ ] `docs/PUBLISHING.md` §8's gate list names it, if it is a gate a release runs

**Open questions**
- Which tool owns it — a third input to `spec.py`, a second reader in `content.py`, or its own file.
  Decide at `plan`, from which one already reads the deck per slide.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- <T-NNN or "none">

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-10 | (no change) | Owner settled the scope on the day it was raised: **exact direction only**. Widening `content.py`'s figure pattern to gate completeness as well was put and declined, so the `Out:` line above is a decision rather than a proposal and is not to be re-argued at `plan`. |
| 2026-08-10 | → proposed | Raised from [T-082](T-082-the-worked-examples-figure-ledger-omits-figures-that-reach-slides.md) §3, which decided the checkable half of the ledger question and left the implementation here rather than growing a fix to a worked example into a tool change. `m` and not `s`: no existing tool takes both a foundation and a deck, so this adds an input to a signature rather than a rule to a list. `v0.2`, being under the `l` line. |
