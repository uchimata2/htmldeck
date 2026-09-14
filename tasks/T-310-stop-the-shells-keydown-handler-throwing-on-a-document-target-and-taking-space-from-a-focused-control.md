---
id: T-310
title: Stop the shell's keydown handler throwing on a document target and taking Space from a focused control
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-299, T-268]
work_package: PH1
shipped_in: unreleased
owner: the project owner
business_value: high
effort: s
created: 2026-09-13
updated: 2026-09-14
deliverables: [shell/deck.js]
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

**From the adopter report** `02`, `12`.

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
- [T-299](T-299-triage-the-third-adopters-report.md) section 3, where `12` was ruled in part

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
| 1 | Guard `matches`, and return before the pager when Space lands on a focused control, in `shell/deck.js` | the fix |
| 2 | Sync the four decks and what derives from them, in `TOOLING.md` §1.14's order | synced decks |
| 3 | In the Browser pane, on a copy of the reference deck before the sync and after it: `ArrowRight` dispatched on `document`, then a real Space and a real Enter on a focused slide button | the evidence in §3 |
| 4 | `lint.py`, then the full `check_all.py`, run separately | the gate |

## 3. Implement

**Decisions & assumptions**
- The guard is `tg.matches && tg.matches(...)`, the idiom the ruler line already used. Record `02`'s
  second proposal, a navigation function a deck can call, is new chrome and out of scope. — 2026-09-14
- Space returns before the pager on a focused `button`, `[role="button"]`, `a[href]`, `input`,
  `select` or `textarea` anywhere on the page, not only on the stage. A focused chrome button is a
  control too, and Space is its activation. — 2026-09-14
- The real key presses are the owner's. The Browser pane's `key` action is not a real press:
  `key space` and `key Return` raised a keydown with an empty `key`, `type " "` raised no keydown, and
  `key Enter` raised `Enter` with no activation click. — 2026-09-14
- `tools/deck/audit.py` said twice that a keydown dispatched on `document` throws. That was true of
  the shell it described and is false after this fix, so both comments now name the shell that does
  it. — 2026-09-14

**Evidence**, on two copies of the reference deck: one taken before the shell sync, one after.

| Probe | Before | After |
| :--- | :--- | :--- |
| `ArrowRight` dispatched on `document` | `TypeError: e.target.matches is not a function`, slide unchanged | slide 1 to 2, no error |
| Space dispatched on a focused `.disc-btn` | `defaultPrevented` true, the deck paged | `defaultPrevented` false, slide unchanged |
| Space dispatched on `body` | not run | the deck paged, `defaultPrevented` true |
| The owner: a real Space on the focused slide-2 disclosure button | the slide moved | the panel toggled and the slide stayed |
| The owner: a real Enter on the same button | not reported | the panel toggled |

**Enter has no case in the handler, before or after**, so record `12`'s Enter half does not
reproduce on this shell. The capture-phase listener that record describes is not this shell's.

**Outputs produced**
- `shell/deck.js`, synced into the four decks, with the seeded fixture re-derived and four byte
  figures in `examples/README.md` re-measured by `tools/docs/figures.py`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Records `02` and `12` closed with the remedy measured by a real key press, or deferred | met | `02`'s case is a dispatched event by definition, so it is measured that way, and the owner's real presses show no regression. `12`: Space measured by the owner in both decks; its Enter half closes as not reproduced |
| Each fix proved by seeding the defect and watching it fire, in both directions | met | The copy before the sync fires both defects and the copy after fires neither. The table in section 3 |
| `lint.py` and `check_all.py` green, run separately | met | Run in that order on the tree this task's commit carries. The counts are in the pull request |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-13 | -> proposed | Raised by T-299 from the third adopter's records `02` and `12`, which share the shell's keydown handler. `PH1`: an adopter met both in the published `0.7.0`. `12` is accepted for Space, and its Enter half is left to be measured. |
| 2026-09-14 | -> in_progress | Section 1 was complete from triage and needed no change. Planned, and started in a fresh session as the fresh-session arm of `T-290`. |
| 2026-09-14 | in_progress -> done | `matches` guarded and Space left to a focused control, each measured in both directions; Space and Enter by the owner's real press. Record `12`'s Enter half closes as not reproduced. |
