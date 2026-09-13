---
id: T-310
title: Stop the shell's keydown handler throwing on a document target and taking Space from a focused control
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-299, T-268]
work_package: PH1
owner: the project owner
business_value: high
effort: s
created: 2026-09-13
updated: 2026-09-13
deliverables: []
---

# T-310 — Stop the shell's keydown handler throwing on a document target and taking Space from a focused control

## 1. Specify

**Outcome**
The shell's one keyboard entry point survives any event target, and leaves a focused control's own
keys to that control. Today it fails in two ways:

- `shell/deck.js` `:579` calls `e.target.matches` unguarded. A `keydown` dispatched on `document`
  has a target with no `matches`, so the handler throws and the slide does not move. Fifteen lines
  further down, the same handler already writes `e.target.closest && ...`.
- `:600` advances the deck on `' '` and calls `preventDefault` with no exemption for a focused
  control. So a real `<button>` on a slide cannot be pressed with Space, and the deck advances instead.

**From the adopter report** [`02`](../docs/adopter-reports/nextep/2026-09-06-a-synthetic-keydown-on-document-throws-in-the-shell-handler.md), [`12`](../docs/adopter-reports/nextep/2026-09-07-the-shell-cancels-enter-and-space-before-a-deck-button-sees-them.md).

**Re-run in triage, 2026-09-13, on this tree.** Dispatching `ArrowRight` on `document` in a copy of the
reference deck threw `TypeError: e.target.matches is not a function`, and the slide was unchanged.

**`12` holds for Space, and its Enter half is not in the source.** The record describes a capture-phase
listener cancelling both keys. On this tree the listener is registered on `document` in the bubble
phase, and Enter has no case in it. The triage's synthetic Enter press was inconclusive, so this task
measures Enter with a real key press. If Enter works, that half of `12` closes as not reproduced, with
the measurement.

**Scope**
- In: the `matches` guard, in the idiom the handler already uses
- In: Space left to a focused `button`, `[role="button"]`, `a[href]`, `input`, `select` or `textarea`
- In: the Enter measurement above
- Out: anything the records above do not name. The report is a closed one-way hand-over, so a
  question this task cannot answer is settled here rather than asked

**Inputs**
- the two records above, each with its command, its version and its own proposed fix
- [T-299](T-299-triage-the-nextep-adopter-report.md) section 3, where `12` was ruled in part

**Acceptance criteria**
- [ ] records `02` and `12` are each closed with the remedy measured by a real key press in a rendered
      deck, or deferred with the reason recorded in this task
- [ ] each fix is proved by seeding the defect and watching it fire, in both directions (**L-125**)
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None. Each record carries its evidence and a proposed fix; the proposal is a hypothesis to measure
  before committing to it.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- `deliverables/...`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- <T-NNN or "none">

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-13 | -> proposed | Raised by T-299 from Nextep records `02` and `12`, which share the shell's keydown handler. `PH1`: an adopter met both in the published `0.7.0`. `12` is accepted for Space, and its Enter half is left to be measured. |
