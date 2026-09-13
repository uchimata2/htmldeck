---
id: T-304
title: Bring a deck-authored motion inside the shell's motion gate, the Motion control and density's ranking
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-299, T-243, T-257]
work_package: PH1
owner: the project owner
business_value: high
effort: m
created: 2026-09-13
updated: 2026-09-13
deliverables: []
---

# T-304 — Bring a deck-authored motion inside the shell's motion gate, the Motion control and density's ranking

## 1. Specify

**Outcome**
A motion the deck writes itself runs, stops and is ranked the way a shell motion is. Today three
mechanisms are keyed to the shell's own class names:

- `--m-on` is defined only on `.pulse`, `.arrow-pop`, `.dot-pop` and `.turn`
  (`shell/components.css` `:661`-`:662`), with no default on `.slide` or `:root`. So `build.md`'s own
  duration idiom animates a deck-invented class for zero seconds, and the motion only ever snaps.
- `data-motion="off"` stops only named shell classes (`shell/components.css` `:761` and
  `:765`-`:769`), so the reader's Motion control never reaches a loop the deck wrote. `DS-218` checks
  that the control is reachable and counts loops (`tools/deck/audit.py` `:2987`), and never that
  toggling it stops each one, so the deck passes.
- `density.py write` looks for `--motion-kind` only in the rule that starts the motion
  (`tools/deck/density.py` `:394`), and says nothing when it finds none.

**From the adopter report** [`04`](../docs/adopter-reports/nextep/2026-09-07-a-deck-authored-content-motion-gets-no-motion-gate.md), [`05`](../docs/adopter-reports/nextep/2026-09-07-density-ranks-the-animating-rule-not-the-declaring-class.md), [`07`](../docs/adopter-reports/nextep/2026-09-07-motion-off-does-not-reach-a-deck-authored-motion.md).

**Why the three are one task.** The remedy the records point at keys the gate and the stop off
`--m-rank` or `--motion-kind` rather than off a class name. That makes `density.py`'s ranking
load-bearing, so `05` is a precondition of the fix, not a separate improvement.

**Scope**
- In: an inherited `--m-on`, or a gate keyed on `--motion-kind` — measure both before choosing, and
  record the rejected one
- In: the Motion control stops every motion the deck carries, and `DS-218` reads `animationName` after
  toggling rather than counting
- In: `density.py write` finds `--motion-kind` on any rule for the selector, and prints one line per
  motion it could not rank
- In: the `build.md` sentence and the contract rows that describe the idiom
- Out: anything the records above do not name. The report is a closed one-way hand-over, so a
  question this task cannot answer is settled here rather than asked

**Inputs**
- the three records above, each with its command, its version and its own proposed fix
- [T-299](T-299-triage-the-nextep-adopter-report.md) section 3, where the three were ruled together

**Acceptance criteria**
- [ ] records `04`, `05` and `07` are each closed with the remedy measured, or deferred with the reason
      recorded in this task
- [ ] each fix is proved by seeding the defect and watching it fire, in both directions (**L-125**),
      and the motion is looked at playing and stopping in a rendered deck
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
| 2026-09-13 | -> proposed | Raised by T-299 from Nextep records `04`, `05` and `07`. `PH1`: an adopter met all three in the published `0.7.0`. `05` arrived as a `suggestion` and is ruled a defect, because the tool reports success on a deck it did not rank. |
