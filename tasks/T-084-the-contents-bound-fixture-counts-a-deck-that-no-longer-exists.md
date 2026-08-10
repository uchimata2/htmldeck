---
id: T-084
title: The contents-bound fixture counts a deck that no longer exists, and has been red since the day the deck changed
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-036, T-069, T-078, T-083]
work_package: v0.2
owner: the project owner
business_value: high
effort: s
created: 2026-08-10
updated: 2026-08-10
deliverables: []
---

# T-084 — The contents-bound fixture counts a deck that no longer exists, and has been red since the day the deck changed

## 1. Specify

**Outcome**
`python tools/deck/contents_bound.py` runs. Today it refuses to, and the measurement
[T-036](T-036-the-second-contents-page-for-long-decks.md) depends on cannot be taken.

**Why this one**
Found 2026-08-10 while [T-078](T-078-write-down-the-release-sequence.md) was writing the release
sequence into [`PUBLISHING.md`](../docs/PUBLISHING.md) §8 — that is, while checking that a list of
gates was a list of gates that run:

    SELF-TEST FAILED
      - the deck built 13 contents boxes, expected 12 - the reference deck changed and these
        numbers describe a different deck

**The tool says exactly what happened, which is to its credit and is why this is `s`.** The cause is
measured rather than assumed: checking out `examples/reference-deck.html` as it stood before
[T-069](T-069-extend-the-provenance-mark-to-multiple-sources.md)'s commit makes the tool run to
completion, and restoring the current file makes it refuse again. T-069 landed earlier the same day,
its deliverables list names that deck, and nothing connected the two.

**This is the third gate outside the routine list found red in one session**, after the shared shell
being stale on `examples/sort-window/` and
[T-083](T-083-the-generated-example-deck-fails-a-hard-rule-and-nothing-recorded-it.md)'s DS-064. All
three were invisible because the README prints five commands and that set had become the list. §8 of
[`PUBLISHING.md`](../docs/PUBLISHING.md) now declares the enumeration and names what would close it;
this task is one of the instances that made the declaration necessary.

**Scope**
- In: what the thirteenth box is, and whether 13 is now correct or the deck grew one it should not
  have.
- In: whichever of the two follows — re-baseline the fixture, or fix the deck.
- In: why a task whose deliverables named the deck did not run this. The tool is not obscure and its
  failure is loud; the gap is in when it runs.
- Out: T-036's own subject, the second contents sheet. This task restores the instrument T-036 needs;
  it does not use it.
- Out: the sweep-nine-deck-sizes design, which is why the tool is separate and is not the defect.

**Inputs**
- `python tools/deck/contents_bound.py` — its own message names the deck and both numbers.
- [T-069](T-069-extend-the-provenance-mark-to-multiple-sources.md) — the change that did it, and what
  it added to the deck.
- [T-036](T-036-the-second-contents-page-for-long-decks.md) — the task that consumes the measurement.

**Acceptance criteria**
- [ ] The tool runs, and what it now measures is stated
- [ ] Whether 13 is right is decided from the deck rather than from the fixture's expectation
- [ ] If the fixture is re-baselined, its numbers say which deck they describe, so the next change
      to that deck fails for a reason a reader can act on
- [ ] The gate list in [`PUBLISHING.md`](../docs/PUBLISHING.md) §8 still names this command, and it is
      green there

**Open questions**
- none

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |

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
| 2026-08-10 | → proposed | Raised from [T-078](T-078-write-down-the-release-sequence.md), which had to run each gate it was about to write down and found this one refusing to start. Attribution measured by checking the pre-T-069 deck out and back. `high` because a refusing self-test is a check nobody is getting an answer from, and T-036 is queued behind the measurement; `s` because the message names the deck and both numbers, so the work is one decision about which of them is wrong. `v0.2`: a fix. |
