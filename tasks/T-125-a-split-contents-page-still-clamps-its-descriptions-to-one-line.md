---
id: T-125
title: Decide whether a split contents page should take a further sheet rather than clamp every description to one line
type: decision
status: specified
phase: plan
parent: null
blocked_by: []
related: [T-036, T-034, T-116]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-13
updated: 2026-08-13
deliverables:
  - shell/deck.js
  - tools/deck/contents_bound.py
  - docs/DESIGN-SYSTEM.md
---

# T-125 — Decide whether a split contents page should take a further sheet rather than clamp every description to one line

## 1. Specify

**Outcome**
A ruling on the capacity of a contents sheet *once the page is already splitting*, and the
implementation of whichever answer is taken. Today it is 16, the same number that triggers the
split. The candidate is 12, the largest sheet that still shows a three-line description.

**What was seen, and where**
[T-036](T-036-the-second-contents-page-for-long-decks.md) built the continuation and printed decks
at 17, 25 and 43 entries. **The 25-entry deck is the weak one.** It splits into sheets of 12 and 13,
the 13 puts both sheets in the four-row band, and that band clamps every description to **one line**
— `Spend the $5.6M grant on bus…`, `The 12 March budget vote is the…`, thirteen of them. Sheet one
then leaves a whole row empty, because the shared grid is taken from the larger sheet. The 17-entry
deck, one band down, prints **three full lines** on both of its sheets.

So a longer deck gets a **better** map than a shorter one, and the difference is a page count nobody
chose.

**The argument for 12, which is the answered question's own**
T-036 §1 settled the trigger at 16 rather than 24 on one reason: *"the description is what makes a
contents page more than a list of titles… splitting at 24 accepts a description-free map anywhere
between 17 and 24 — a quality cliff nobody chose per deck and nothing would report."* One band
deeper the same sentence applies to 13–16, where the description is a clamped fragment rather than a
sentence. And the Outcome of T-036 is that the page *"degrades by growing rather than by dropping
entries"* — accepting fragments to save a sheet is degrading in the other direction.

**The argument against, which is why this is raised and not taken**
Three things, and the third is decisive on its own.

1. **It is a second number.** The rule becomes *one sheet up to 16, then sheets of at most 12*, and a
   discontinuity appears at 17: a 16-entry deck prints fragments on one sheet where a 17-entry deck
   prints sentences on two.
2. **It costs sheets on the pathological shape.** A deck of 43 whose argument is one stage of 40 goes
   from three sheets to five, the last carrying the colophon alone.
3. **The trigger was answered by the owner and re-measured twice** — T-034 measured 16/24, T-116
   re-measured them against a three-line description in every entry and both held, and the owner's
   instruction for T-036 was to build against 16/24. Moving the capacity inside a task told to use
   that number would be taking a ruling rather than reading one (**L-37**).

**Not a defect in what shipped.** Every T-036 criterion is met and the printed sheets are clean. The
one-line clamp at 13–16 entries is DS-226 working as written, and `examples/reference-deck.html` has
printed exactly that way since its colophon took it to 13 — the owner has seen that page.

**Scope**
- In: the ruling, and the per-sheet capacity that follows from it.
- In: whichever of the two the ruling takes, implemented in `shell/deck.js` and re-measured.
- Out: the trigger. 16 stays whatever this decides — a deck at or under it prints one sheet.
- Out: the row bands themselves. They are measured and DS-226 owns them.

**Inputs**
- [T-036](T-036-the-second-contents-page-for-long-decks.md) §3 — the finding, with the counts.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §5.4, DS-226 — the bands and the rule.
- `tools/deck/contents_bound.py` — re-measures both the bands and the split.

**Acceptance criteria**
- [ ] The ruling is recorded with its reason, on whichever side it falls
- [ ] If the capacity moves, it is implemented and DS-226 restates it
- [ ] A 25-entry deck is **printed and looked at** under the ruling (**L-01**, **L-35**, **L-76**)

**Open questions**
- ~~**Does a splitting contents page cap its sheets at 12 rather than 16?**~~ **Answered 2026-08-13
  by the owner: yes, split at 12.** So the rule has two numbers: **one sheet up to 16, then sheets of
  at most 12.** The trigger is untouched — a deck at or under 16 still prints the single sheet T-034
  measured and T-116 fixed — and what moves is the capacity of a sheet once the page is already
  continuing. The three costs are accepted as stated above: a second number, a discontinuity at 17,
  and five sheets rather than three for a 43-entry deck whose argument is one stage of 40.

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
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-13 | → specified | **Answered the day it was raised: the owner ruled yes, split at 12.** §1 needed no other change — it was written as a decision with both sides argued, so the ruling closes it rather than rewriting it. What is left is implementation and re-measurement: the cap in `shell/deck.js`, the eight cases in `contents_bound.py` re-baselined, DS-226 restated, and a 25-entry deck printed and looked at. |
| 2026-08-13 | → proposed | Raised by [T-036](T-036-the-second-contents-page-for-long-decks.md) from a printed sheet rather than from a gate — the 25-entry deck's map is poorer than the 17-entry deck's, and nothing mechanical can see that. Raised rather than taken because the number it would move is one the owner answered and two tasks re-measured; T-034's own precedent for this shape is raising T-036 instead of building it (**L-37**). `PH3` and `medium`: it is a quality improvement to a page that works, not a defect in one that does not. |
