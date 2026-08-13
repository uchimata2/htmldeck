---
id: T-126
title: Stop shell.py refusing every command while a tracked deck is behind the shell
type: fix
status: done
phase: review
shipped_in: unreleased
parent: null
blocked_by: []
related: [T-124, T-125, T-101]
work_package: PH3
owner: the project owner
business_value: high
effort: xs
created: 2026-08-13
updated: 2026-08-13
deliverables:
  - tools/deck/shell.py
  - docs/LESSONS.md
---

# T-126 — Stop shell.py refusing every command while a tracked deck is behind the shell

## 1. Specify

**Outcome**
`shell.py sync <deck> --write` runs when a tracked deck is behind the shell, which is the only
situation the command exists for. Today it refuses, because one self-test fixture asserts that
`examples/reference-deck.html` is **already** in step — so editing `shell/deck.js` disables the tool
that carries the edit to the decks, and every other `shell.py` command with it.

**What was seen, and where**
Found 2026-08-13 by [T-125](T-125-a-split-contents-page-still-clamps-its-descriptions-to-one-line.md),
on the first shell edit after [T-124](T-124-an-adopter-cannot-refresh-a-decks-shell-after-an-upgrade.md)
shipped `sync`. One line of `shell/deck.js` changed, then:

```
  FAIL and the reference deck is already synced, so it is a no-op
42 of 43 fixtures behaved as specified.
SELF-TEST FAILED - the tool itself is wrong; anything below means nothing.
```

The tool exits 2 and does nothing. `check`, `sync`, the sprite commands and `--set` are all behind
the same gate, so the whole tool is down until the decks are in step — which is what `sync` was for.

**Why the fixture is wrong rather than unlucky**
It is not testing the tool. `sync(original) == original` asserts the **current contents of a
repository artifact**, and the artifact is one this command's whole purpose is to change. The tool
is correct in exactly the case the fixture calls a failure.

The property is also already owned elsewhere: `tools/check_all.py` runs `shell.py check` over every
tracked deck, which is the gate that fails a release when a deck is behind. So the fixture is
redundant as a state check and blocking as a self-test.

**This is the family L-71 named, one step over.** There the assertion took the reference
*environment* for the definition of correct and blocked every adopter; here it takes the reference
*repository state*, and blocks the maintainer at the one moment the command is needed. Both silence
the instrument that would report the problem.

**Scope**
- In: the fixture, replaced by one that tests the property on a deck the fixture itself makes.
- In: the lesson, since this is a second member of a family with one already recorded.
- Out: the self-test's refuse-on-failure behaviour. It is right (**L-04**) and stays.
- Out: `check_all.py`, which already asserts the tracked decks are in step.

**Inputs**
- `tools/deck/shell.py` — the fixture, and the three sync fixtures above it that do test the tool.
- [`docs/LESSONS.md`](../docs/LESSONS.md) — **L-71**, the family.

**Acceptance criteria**
- [x] With a tracked deck behind the shell, `shell.py sync <deck> --write` runs and syncs it
- [x] The self-test still fails a `sync` that drops a per-deck region, and still fails a stale deck
- [x] Nothing else loses coverage: the tracked-deck-in-step property is still asserted somewhere

**Open questions**
- none

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Replace the fixture with the same assertion on a deck **the self-test synced itself**, so it tests sync's no-op property rather than the repository's state | `shell.py` |
| 2 | Re-run the self-test with the reference deck deliberately behind, and with it in step — both must pass | the evidence |
| 3 | Record the lesson beside **L-71** | `LESSONS.md` |

## 3. Implement

**Decisions & assumptions**
- **The fixture is replaced, not deleted.** `sync(sync(original)) == sync(original)` keeps the
  property — *a deck already in step is not changed* — on a deck the self-test brings into step
  itself, and keeps it on the one input worth having it on: the reference deck, which has something
  in every per-deck region where a fresh skeleton is vacuous. — 2026-08-13
- **The repository-state half goes nowhere new**, because `check_all.py` already runs `shell.py
  check` over every tracked deck. Adding a replacement assertion would have been a second board for
  a fact that has one. — 2026-08-13
- **Shown to fail before it was believed** (**L-04**). With `sync` sabotaged to be non-idempotent
  the new fixture trips, alongside the two it sits between:

```
  FAIL sync leaves every per-deck region of the reference deck untouched moved: ['SLIDES']
  FAIL and syncing a deck that is already in step changes nothing
  FAIL sync is idempotent
40 of 43 fixtures behaved as specified.
```

**Outputs produced**
- [`tools/deck/shell.py`](../tools/deck/shell.py) — the fixture, and a comment carrying why the old
  one was wrong rather than unlucky
- [`docs/LESSONS.md`](../docs/LESSONS.md) — **L-78**, beside the **L-71** it extends

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| With a tracked deck behind the shell, `sync --write` runs and syncs it | **met** | The blocked case itself: `shell/deck.js` edited, then `43 of 43 fixtures behaved as specified` and `examples/reference-deck.html - 1 region(s) synced, 12 per-deck region(s) untouched` |
| The self-test still fails a `sync` that drops a per-deck region, and still fails a stale deck | **met** | The three `a deck behind in X fails check` / `and sync brings it back` pairs are untouched and green, and the sabotage above trips the per-deck-region fixture |
| Nothing else loses coverage | **met** | `check_all.py` runs `shell.py check` over each tracked deck, which is where a deck behind the shell fails a release |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-13 | → done | One fixture, and the lesson it earned. The interesting part is not the fix but what it says about the shape: **the tool was correct in exactly the case the fixture called a failure**, which is why the failure message named the right line and still read as an accusation against the code. The state it was standing in for was already gated elsewhere, so nothing was traded away. |
| 2026-08-13 | → planned | Raised and planned in one step: it blocks [T-125](T-125-a-split-contents-page-still-clamps-its-descriptions-to-one-line.md) mid-implementation, the cause was in the failure message, and the fix is one fixture. `PH3` because `sync` shipped in T-124 and T-124 is **unreleased** — no published plugin carries this. |
