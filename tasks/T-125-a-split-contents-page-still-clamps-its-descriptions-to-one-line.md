---
id: T-125
title: Decide whether a split contents page should take a further sheet rather than clamp every description to one line
type: decision
status: done
phase: review
shipped_in: unreleased
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
- [x] The ruling is recorded with its reason, on whichever side it falls
- [x] If the capacity moves, it is implemented and DS-226 restates it
- [x] A 25-entry deck is **printed and looked at** under the ruling (**L-01**, **L-35**, **L-76**)

**Open questions**
- ~~**Does a splitting contents page cap its sheets at 12 rather than 16?**~~ **Answered 2026-08-13
  by the owner: yes, split at 12.** So the rule has two numbers: **one sheet up to 16, then sheets of
  at most 12.** The trigger is untouched — a deck at or under 16 still prints the single sheet T-034
  measured and T-116 fixed — and what moves is the capacity of a sheet once the page is already
  continuing. The three costs are accepted as stated above: a second number, a discontinuity at 17,
  and five sheets rather than three for a 43-entry deck whose argument is one stage of 40.

## 2. Plan

**The shape of the change.** `contentsSheets` uses one number three times: the trigger for splitting,
the argument to `splitLongRuns`, and the ceiling of the binary search that balances the sheets. The
ruling separates the first from the other two. So the edit is a second constant and three call sites,
not a new rule — and the binary search already reaches below the cap, which is why only two of the
eight measured shapes move at all.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Print the 25-entry scratch deck under today's rule first, so the change has a measured *before* from this session rather than a quoted one (**L-35**) | the before row |
| 2 | The second number in [`shell/deck.js`](../shell/deck.js): `CONTENTS_CAP` 16 stays the trigger; a new sheet capacity of 12 takes the other two uses | the rule |
| 3 | Carry the shell to the three tracked decks — `shell.py sync --write` for the two authored ones, and regenerate the seeded-defects deck rather than syncing it (**L-77**) | the decks |
| 4 | Re-baseline [`tools/deck/contents_bound.py`](../tools/deck/contents_bound.py): the per-sheet invariant becomes *16 on a lone sheet, 12 once split*, two of the eight case expectations move, and the report states both numbers | the instrument |
| 5 | Restate DS-226 and §5.4 with the two numbers and the three accepted costs | the ruleset |
| 6 | Print 25 again and **look at it**, with 17 and 43 as the pair that must not regress (**L-01**, **L-76**) | the after rows |
| 7 | `python tools/check_all.py` | the gate |
| 8 | Close the record: §3, §4, the log, the index, and the unreleased set | the record |

## 3. Implement

**Decisions & assumptions**
- **The second number is a second constant, `SHEET_CAP = 12`, and `CONTENTS_CAP` keeps its meaning.**
  `contentsSheets` used one number three ways — the trigger for splitting, the argument to
  `splitLongRuns`, and the ceiling of the balancing search. The ruling separates the first from the
  other two, so the edit is three call sites. Naming them apart is what stops the next reader
  moving one and meaning both. — 2026-08-13
- **Six of the eight measured shapes did not move, and that is the finding.** The balancing search
  already drove most shapes below 12: at 43 entries in seven even stages it had settled on 12
  before this task existed. Only the two shapes that were *buying a sheet back with fragments*
  changed — 25 entries, and the 43 whose argument is one stage of 40. The ruling costs less than
  its own argument-against predicted, and the accepted cost that did land is the second one. — 2026-08-13
- **The 25-entry deck printed 8 · 10 · 7, not the 8 · 8 · 9 the split table shows.** Both are
  correct: the table's case is 25 entries in seven even stages, and the scratch deck is 24 in seven
  stages plus a colophon, which is a different shape. Worth stating because the two numbers sit
  next to each other in this record. — 2026-08-13
- **The instrument's worked example had to move with the rule.** `ceil(n / 16)` *is a floor, not the
  answer* was demonstrated by the seven-even-stages 43, which under a cap of 12 lands exactly on its
  floor of four. The claim is still true and is now shown by the 40-entry stage, which takes five
  where the arithmetic says four. A number changed under a sentence that did not — the class of
  error a wholesale re-baseline hides. — 2026-08-13
- **Deviation: `shell.py` would not run.** Its self-test asserted that the reference deck was
  already in step with the shell, so editing `shell/deck.js` disabled the command that carries the
  edit to the decks. Raised and fixed as
  [T-126](T-126-shell-py-refuses-every-command-while-a-tracked-deck-is-behind-the-shell.md) rather
  than folded in here — different subject, and it is the first thing an adopter hits after
  `sync` ships. — 2026-08-13

**What the numbers came out as**

Printed through real Chrome and read out of the PDF's own rectangles, the same instrument T-036
used (**L-76**). Every row is clean on every sheet: no card overlaps another, and none reaches the
footnote.

| deck | before | after | descriptions |
| ---: | :--- | :--- | :--- |
| 13, the reference deck | 1 sheet, 13 | **unchanged** | one line, and the owner has seen it |
| 17 | 2 sheets, 8 · 9 | **unchanged** | three lines, before and after |
| 25 | 2 sheets, 12 · 13 | 3 sheets, **8 · 10 · 7** | one line → **three lines** |
| 43 | 4 sheets, 12 · 12 · 12 · 7 | **unchanged** | three lines, before and after |

Row gaps stayed at `+20.2` throughout and the footnote band at 735.7–751.5 pt, which is the geometry
T-116 recorded. The 25-entry deck's first sheet also loses the empty row it used to print: the shared
grid is taken from the largest sheet, and the largest sheet is no longer a band deeper than the rest.

**Outputs produced**
- [`shell/deck.js`](../shell/deck.js) — `SHEET_CAP`, the three call sites, and the ruling with its
  three accepted costs written where the number is
- [`tools/deck/contents_bound.py`](../tools/deck/contents_bound.py) — the per-sheet invariant is now
  *16 on a lone sheet, 12 once split*; two of the eight expectations re-baselined by hand before the
  run; the docstring, the worked example and the report state both numbers
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-226 restates the rule as two numbers
- The three tracked decks, carrying the shell byte for byte:
  [`examples/reference-deck.html`](../examples/reference-deck.html),
  [`examples/sort-window/sort-window.html`](../examples/sort-window/sort-window.html) and
  [`examples/reference-deck-seeded-defects.html`](../examples/reference-deck-seeded-defects.html),
  the last **regenerated rather than synced** (**L-77**)

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The ruling is recorded with its reason, on whichever side it falls | **met** | DS-226 carries the rule, the reason and the three accepted costs; `shell/deck.js` carries them beside the constant; §1 carries the argument on both sides |
| If the capacity moves, it is implemented and DS-226 restates it | **met** | `SHEET_CAP = 12` in the shell and in all three tracked decks. `contents_bound.py` exercises eight stage shapes through the shipped rule and no split sheet comes back over 12 |
| A 25-entry deck is **printed and looked at** under the ruling | **met** | 3 sheets, 8 · 10 · 7, printed through real Chrome and looked at. Every description is three full lines and states something — `The three corridors bike-share wins carry 12,200 weekday trips; the three frequency wins carry 36,000.` where the same box read `The three corridors bike-share wi…` before |

**Child fix tasks raised**
- [T-126](T-126-shell-py-refuses-every-command-while-a-tracked-deck-is-behind-the-shell.md) — found
  while carrying this edit to the decks, fixed the same day

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-13 | → done | Built, printed and looked at the same day it was raised and ruled on. **Two of eight measured shapes moved**, because the balancing search already reached below the new cap for the rest — the ruling's own argument-against overestimated what it would cost, and the one cost that did land is the 40-entry stage going from three sheets to five. The 25-entry deck now prints three sheets of full sentences where it printed two of fragments. One deviation, `shell.py` refusing to run, went out as [T-126](T-126-shell-py-refuses-every-command-while-a-tracked-deck-is-behind-the-shell.md). |
| 2026-08-13 | → planned | Planned as a second constant and three call sites. The step nobody could skip is step 1: print the 25-entry deck under the old rule first, so the *before* is measured in this session rather than quoted from T-036 (**L-35**). |
| 2026-08-13 | → specified | **Answered the day it was raised: the owner ruled yes, split at 12.** §1 needed no other change — it was written as a decision with both sides argued, so the ruling closes it rather than rewriting it. What is left is implementation and re-measurement: the cap in `shell/deck.js`, the eight cases in `contents_bound.py` re-baselined, DS-226 restated, and a 25-entry deck printed and looked at. |
| 2026-08-13 | → proposed | Raised by [T-036](T-036-the-second-contents-page-for-long-decks.md) from a printed sheet rather than from a gate — the 25-entry deck's map is poorer than the 17-entry deck's, and nothing mechanical can see that. Raised rather than taken because the number it would move is one the owner answered and two tasks re-measured; T-034's own precedent for this shape is raising T-036 instead of building it (**L-37**). `PH3` and `medium`: it is a quality improvement to a page that works, not a defect in one that does not. |
