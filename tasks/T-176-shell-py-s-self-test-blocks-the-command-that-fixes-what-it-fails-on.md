---
id: T-176
title: shell.py's self-test asserts repository state, so it blocks the one command that fixes it
type: fix
status: done
phase: review
shipped_in: unreleased
parent: null
blocked_by: []
related: [T-109, T-036, T-124]
work_package: PH1
owner: the project owner
business_value: critical
effort: s
created: 2026-08-17
updated: 2026-08-17
deliverables:
  - tools/deck/shell.py
---

# T-176 — shell.py's self-test asserts repository state, so it blocks the one command that fixes it

## 1. Specify

**Outcome**
`python tools/deck/shell.py sync` runs after a change to `shell/shell.html`, which is the only
moment anyone needs it to. Today it refuses, and it refuses for the change it exists to propagate.

**What happens**
`self_test()` fixture 1 makes two assertions off the tracked reference deck:

| # | Assertion | What it is about |
| :--- | :--- | :--- |
| a | `fill(cut(deck)) == deck` — the cut round-trips | **the tool**. Correct here |
| b | `cut(deck)[0] == shell/shell.html` — what is left is the shell | **the repository**, not the tool |

`main()` runs `self_test()` before every subcommand and exits when it fails, so (b) turns *a deck is
one edit behind the shell* into *this tool is wrong, anything below means nothing*. **That state is
reached by editing `shell/shell.html` — and the command that resolves it is `sync`, which is inside
the door it just locked.**

**How it was found**
[T-109](T-109-one-source-reference-component-rendered-in-three-places.md) added one `<p>` to the
quick view's header in `shell/shell.html`. Every `shell.py` subcommand then exited 2 on
`FAIL and what is left is shell/shell.html / first at line 102`, with no deck yet touched.

**Why the shape matters more than the fix.** (b) is not a missing check, it is a **duplicated** one
that lost its verdict on the way. `check(deck)` already reports exactly this drift, by name, as
`SKELETON`, and `sync` already repairs it — the tool knows the answer and offers it as a service.
Restating that fact inside the self-test converts a serviceable finding into a fatal one, and the
self-test is the one place that cannot offer the repair. **A self-test may only assert things about
the tool**; the moment it asserts what a tracked file currently contains, it fails on precisely the
commits that change that file.

**Scope**
- In: fixture 1(b) in `tools/deck/shell.py`'s `self_test()`.
- In: a fixture proving the round-trip on a skeleton the test **builds**, so 1(a)'s coverage is
  kept rather than traded away.
- In: whatever states the drift instead, given `check` already names it — a notice at most.
- Out: `check` and `sync` themselves. Neither is wrong; (b) is the only defect here.
- Out: the same shape anywhere else in `tools/`. If it is there too it is another task, and this
  one is on the critical path of the ranked-first task.

**Inputs**
- `tools/deck/shell.py` — `self_test()` fixture 1, `check()`, `sync`.
- **L-77** — the last time this file's two verdicts disagreed about what a file is.

**Acceptance criteria**
- [ ] With `shell/shell.html` edited and no deck synced, `python tools/deck/shell.py sync` runs and
      reports the drift instead of refusing.
- [ ] The cut is still proved lossless, on a fixture the test owns.
- [ ] A deck genuinely behind the shell is still failed by `check`, named as `SKELETON` — asserted
      by breaking one, as every other fixture in this file is.
- [ ] `python tools/check_all.py` green.

**Open questions**
- None. The owner's standing rule is that a check forbidding a legal change is a defect in the
  check ([`docs/LESSONS.md`](../docs/LESSONS.md), *ship in phases; rigour must not block*).

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Replace 1(b) with a round-trip on a skeleton the test builds, so the tool's claim is proved without naming a tracked file | `shell.py` |
| 2 | Prove the drift is still caught, by breaking a deck's skeleton and asserting `check` says `SKELETON` | `shell.py` |
| 3 | Run `sync` against the state that provoked this, and the full gate | verdict |

## 3. Implement

**Decisions & assumptions**
- 2026-08-17 — **fixture 1 is built, not read.** `new("Fixture", "Subtitle")` fills the shell's own
  regions, so cutting it and comparing the remainder to `shell/shell.html` asserts what `cut` and
  `fill` do rather than what a tracked deck currently contains. Both original claims survive; only
  their subject changed, from a file anyone may edit to a value this function produces.
- 2026-08-17 — **the reference deck keeps a fixture, narrowed to losslessness.** 270 KB of authored
  slides, three embedded faces and a sprite is input the built skeleton cannot stand in for, and
  `fill(cut(x)) == x` on it cannot go false by anyone editing the shell.
- 2026-08-17 — **nothing replaces the deleted assertion, and nothing needs to.** `check()` reports
  the drift as `SKELETON`, `sync` repairs it, and the fixture asserting both was already three rows
  below the one removed. Adding a warning would have restated the same fact a third time.

**Outputs produced**
- [`tools/deck/shell.py`](../tools/deck/shell.py) — `self_test()` fixture 1.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :--- | :--- |
| `sync` runs with `shell.html` edited and no deck synced | met | It was run in exactly that state, four times, and it is what carried T-109's shell into all three decks. Before the fix every subcommand exited 2 |
| The cut is still proved lossless, on a fixture the test owns | met | `the cut round-trips` on the built skeleton, plus `and it round-trips on a real deck` on the reference deck |
| A deck behind the shell is still failed as `SKELETON` | met | `a deck behind in SKELETON fails check` / `and sync brings it back` / `and says SKELETON is what moved` — three fixtures, all by breaking a deck on purpose |
| `python tools/check_all.py` green | met | Green on the run that closed T-109, which carries this change |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-17 | → proposed | Raised from [T-109](T-109-one-source-reference-component-rendered-in-three-places.md)'s implement phase, which it blocks outright: one `<p>` added to `shell/shell.html` and every `shell.py` subcommand exits 2, including the `sync` that propagates it. `PH1` because it is a defect in the published plugin — an adopter who edits the shell meets it on the same command this repository ships them, and `shell.py sync` is what `PUBLISHING.md` §8.1 and `L-77` both point at. |
| 2026-08-17 | → done | Specified, planned, implemented and reviewed the same hour, because it sat on the critical path of the ranked-first task rather than beside it. **53 of 53 fixtures behave as specified** and the count went up by one: the built skeleton carries both assertions and the real deck keeps the losslessness one. Nothing produced by this task renders, so §7 step 3's look is not owed — the same ground the 2026-08-16 unattended batch was selected on. The reusable half is **L-112**. |
