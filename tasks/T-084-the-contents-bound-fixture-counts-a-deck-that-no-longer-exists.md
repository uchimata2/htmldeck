---
id: T-084
title: The contents-bound fixture counts a deck that no longer exists, and has been red since the day the deck changed
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-036, T-069, T-078, T-083]
work_package: PH2
shipped_in: 0.1.5
owner: the project owner
business_value: high
effort: s
created: 2026-08-10
updated: 2026-08-12
deliverables:
  - tools/deck/contents_bound.py
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
| 1 | Find out what the thirteenth box is, from the deck | this file §3 |
| 2 | Re-baseline or fix the deck, whichever the answer says | [`contents_bound.py`](../tools/deck/contents_bound.py) |
| 3 | Run it, and check the bound against the numbers T-036 was specified on | this file §4 |

## 3. Implement

**What the thirteenth box is**
`examples/reference-deck.html` carries **thirteen** `<section class="slide…">` elements: twelve
slides and the **colophon** [T-069](T-069-extend-the-provenance-mark-to-multiple-sources.md) added
after the close under a named DS-085 exemption. The contents page is derived from the manifest rather
than authored, so it builds one box per section — thirteen. Counted off the deck: the last two are
`class="slide close"` and `class="slide"` named *Sources*, and the deck's `aria-label`s run to
*Slide 13*.

**Decisions & assumptions**
- **13 is right; the fixture was wrong** — 2026-08-10. Nothing in the deck grew a box it should not
  have. The number was true of the deck as it stood before T-069 and went false the moment the
  colophon landed, which took this tool from *measuring* to *refusing* and left it there.
- **Deliberately still a hard-coded number, not derived** — 2026-08-10. §1 asked which of the two was
  wrong, not how to stop the question recurring, and the honest answer to the second is that this
  assertion **exists to trip when the deck moves under the measurement**. A value read from the deck
  would agree with every deck and catch nothing. What a re-baseline owes instead is saying which deck
  its number describes, so the next trip is readable — and the comment now names the twelve slides
  and the colophon, and the change that made it thirteen.

**Outputs produced**
- [`tools/deck/contents_bound.py`](../tools/deck/contents_bound.py) — `AUTHORED = 13`, the failure
  message naming what the thirteenth is, and the paragraph explaining why the number is not derived.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The tool runs, and what it now measures is stated | met | Runs to completion and prints the sweep across seventeen deck sizes. |
| Whether 13 is right is decided from the deck | met | Counted off the deck, not inferred from the fixture: twelve slides plus T-069's colophon. |
| A re-baselined number says which deck it describes | met | The comment names both halves and the change that moved it, so the next trip reads as a fact rather than a mystery. |
| The gate list in `PUBLISHING.md` §8 still names this command, and it is green there | met | Named, and green in the full run made for `v0.1.5`. |

**The bound is unchanged, which is the result that matters downstream:**

    THE BOUND      16 slides - the largest deck that still shows a description
    THE HARD LIMIT 24 slides - the largest deck whose number and title render at all

Those are the two numbers [T-036](T-036-the-second-contents-page-for-long-decks.md) was specified
against, so its specification stands and its `blocked_by` edge is released.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-10 | → done | The fixture was wrong and the deck was not: thirteen is twelve slides plus T-069's colophon, counted off the deck. **Left hard-coded on purpose** — this assertion exists to trip when the deck moves, so deriving it would make it agree with everything; what it owed was saying which deck it describes, which is now in the comment. The bound came back **16 / 24**, the same pair T-036 was specified on, so that task's edge is released and its specification stands untouched. Shipped in **`v0.1.5`**. |
| 2026-08-10 | → proposed | Raised from [T-078](T-078-write-down-the-release-sequence.md), which had to run each gate it was about to write down and found this one refusing to start. Attribution measured by checking the pre-T-069 deck out and back. `high` because a refusing self-test is a check nobody is getting an answer from, and T-036 is queued behind the measurement; `s` because the message names the deck and both numbers, so the work is one decision about which of them is wrong. `PH2`: a fix. |
