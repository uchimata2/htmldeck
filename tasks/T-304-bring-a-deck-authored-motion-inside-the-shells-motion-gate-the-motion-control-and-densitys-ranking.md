---
id: T-304
title: Bring a deck-authored motion inside the shell's motion gate, the Motion control and density's ranking
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-299, T-243, T-257]
work_package: PH1
shipped_in: unreleased
owner: the project owner
business_value: high
effort: m
created: 2026-09-13
updated: 2026-09-14
deliverables: [shell/components.css, tools/deck/audit.py, tools/deck/density.py, tools/deck/static_variants.py, skills/htmldeck/references/build.md]
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

**From the adopter report** `04`, `05`, `07`.

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
- [T-299](T-299-triage-the-third-adopters-report.md) section 3, where the three were ruled together

**Acceptance criteria**
- [x] records `04`, `05` and `07` are each closed with the remedy measured, or deferred with the reason
      recorded in this task
- [x] each fix is proved by seeding the defect and watching it fire, in both directions (**L-125**),
      and the motion is looked at playing and stopping in a rendered deck
- [x] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None. Each record carries its evidence and a proposed fix; the proposal is a hypothesis to measure
  before committing to it.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Measure the three ways to gate a deck's motion, and a stop that reaches any class, in headless Chrome | §3 |
| 2 | Gate `--m-on` on the rank and stop every animation under `data-motion="off"` | `shell/components.css` |
| 3 | Make DS-218 read each loop after the toggle, and seed a loop the control does not stop | `tools/deck/audit.py`, `tools/deck/static_variants.py` |
| 4 | Read a kind from any rule for the class, and name at `write` a motion no rule classifies | `tools/deck/density.py` |
| 5 | Write the idiom where a builder meets it | `skills/htmldeck/references/build.md` |
| 6 | `../tasks/TOOLING.md` §1.14 over the four decks, the owed look, lint, then the full gate | §3 |

## 3. Implement

**Decisions & assumptions**
- `--m-on` is set on `[style*="--m-rank"]`, every ranked element, instead of on four class names:
  measured, it gates a ranked element, an unranked one and a ranked figure's child correctly.
  Reversible. — 2026-09-14
- Record `04`'s `--m-on` on `.slide` is rejected on measurement: a custom property inherits its
  computed value, so a rank-1 element under it ran 0 s. A gate keyed on `--motion-kind` through a
  style query is rejected on measurement too: the query reads an ancestor, so an element declaring
  its own kind ran 0 s. Reversible. — 2026-09-14
- The Motion control stops every element and pseudo-element by zero duration, zero delay and one
  iteration, `!important`. Record `07`'s blanket `animation:none` is rejected because it drops the
  fill and leaves a reveal at its hidden start (DS-224). Its cheaper `check.py` pairing is rejected
  because it leaves the stop to every author. Reversible. — 2026-09-14
- DS-218 sets `data-motion="off"` before the pin and fails a loop whose computed iteration count is
  still `infinite`. The scope named `animationName`, and under a zero-duration stop the name stays,
  so the iteration count is the reading. Reversible. — 2026-09-14
- `density.py` takes a kind from any rule for the class, and the rule's own declaration wins.
  `write` prints a line per motion no rule classifies. A line per classified class with no element
  is rejected, because every deck carries four shell classes it may not use. Reversible. — 2026-09-14
- No contract row describes `--m-on`, so the contract is unchanged, and `build.md` gains the idiom.
  Reversible. — 2026-09-14

Measured in headless Chrome through `render.chrome_run`, on a page outside the repository at density
100.

| Case | `animation-duration` | Iterations |
| :--- | :--- | :--- |
| rank 1, `--m-on` on the rank | 1s | 1 |
| rank 101, `--m-on` on the rank | 0s | 1 |
| unranked, `--m-on` on the rank | 0s | 1 |
| child of a rank-1 figure, `--m-on` on the rank | 1s | 1 |
| rank 1, `--m-on` inherited from `.slide` | 0s | 1 |
| own `--motion-kind`, style query | 0s | 1 |
| parent's `--motion-kind`, style query | 1s | 1 |
| a deck's loop, motion on | 2s | infinite |
| the same loop, motion off | 0s | 1 |
| a deck's reveal, motion off | 0s, lands at `opacity` 1 | 1 |

The other direction of each fix:

| Fix | Seeded | Result |
| :--- | :--- | :--- |
| `04` | a ranked class the shell does not name, before the change | 0 s, record `04`'s own measurement on `0.7.0` |
| `05` | the kind on the base rule, the animation on a state rule | ranked; with no kind anywhere, one line at `write` (self-test) |
| `07` | a deck rule that out-ranks the stop: `loop-the-motion-control-does-not-stop` | DS-218 fails with `1 still looping with motion off`; unseeded decks pass |

§1.14 after the shell edit: four decks synced, the seeded fixture regenerated, `density.py check`
`0 wrong` on each, and `README.md`'s `sort-window.html` figure corrected from 317 KB to 318 KB.

**Records closed:** `04` by the rank-keyed gate, `05` by the lookup and the `write` line, and `07` by
the stop and DS-218's reading.

**The look is owed**: [`../docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md) row 13.

**Outputs produced**
- `shell/components.css`: `--m-on` on the rank, and the stop for every animation
- `tools/deck/audit.py`: DS-218's reading after the toggle, its measured key and a self-test state
- `tools/deck/density.py`: `motion_rules` reads a kind from any rule, `unranked`, self-test cases
- `tools/deck/static_variants.py`: `loop-the-motion-control-does-not-stop`
- `skills/htmldeck/references/build.md`: the idiom and what the shell does for it

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| records `04`, `05` and `07` closed with the remedy measured | **pass** | §3 |
| each fix seeded in both directions, and the motion looked at | **pass**, look owed | Both directions in §3's tables. The look is `OWED-LOOKS.md` row 13, as `../docs/REMEDIATION-ORDER.md` §4 requires of an unattended session |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | **pass** | Lint, then the full gate on the finished tree |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-14 | -> done | The gate keys on the rank, the Motion control stops every animation, DS-218 reads the stop and density reads a kind from any rule. Records `04`, `05` and `07` closed. The look is owed as `OWED-LOOKS.md` row 13. |
| 2026-09-13 | -> proposed | Raised by T-299 from the third adopter's records `04`, `05` and `07`. `PH1`: an adopter met all three in the published `0.7.0`. `05` arrived as a `suggestion` and is ruled a defect, because the tool reports success on a deck it did not rank. |
