---
id: T-169
title: The figure binder cannot bind a value whose label sits in another table cell
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-167, T-128]
work_package: PH1
owner: the project owner
business_value: medium
effort: s
created: 2026-08-16
updated: 2026-08-16
deliverables:
  - tools/deck/content.py
---

# T-169 — The figure binder cannot bind a value whose label sits in another table cell

## 1. Specify

**FIG-1 reports a sourced figure as unsourced.**
[T-128](T-128-publish-the-adopter-deck-as-a-worked-example.md)'s deck states the stop-or-go gate at
**month 4** on the slide *€450k in, €1.2m a year out*. `check.py` says:

```
FIG-1   figures on a slide that appear in no source: 1 of 30
        ledger: ["450k in, 1.2m a year out", "4 stop", "month-4 stop-or-go gate"]
```

**The figure is in the source.** `examples/measure-first/sources/D5-management-decision-matrix.md`
carries it twice — once in a table row that holds both halves,
`| **Set the stop-or-go gate** | … | Month 4 |`, and once in prose, *judge the whole programme on
the evidence it produces in month 4*.

**Hypothesis, not yet a finding.** The ledger keyed the deck's figure as value `4`, label `stop`.
The slide writes **`month-4`**, hyphenated, so the word that would have matched D5 is glued to the
numeral and the binder took the next word instead. D5's own label for that value is *month*. Two
label sets with no overlap, and the figure falls out. **`label_of` has not been read**, and the fix
starts by reading it rather than by acting on this paragraph.

**Why it matters now.** It was recorded as a false alarm on 2026-08-16 and left unraised, on the
grounds that it was 1 of 30 and the binder is documented as approximate. [T-167](T-167-checkpy-reads-a-quoted-source-as-the-decks-own-slide-copy.md)
then cleared the other three failures, and this became **the only thing between T-128's deck and a
green gate**. A false alarm nobody can act on is cheap until it is the last one standing.

**The wider shape.** A hyphenated compound carrying a numeral — `month-4`, `2×2`, `top-3` — is
ordinary deck copy, and the corpus is full of it. If the hypothesis holds, every such figure is
unbindable, and the rate is invisible because FIG-1 reports a count rather than a list.

**Scope**
- In: read `label_of` and establish the real mechanism before changing anything.
- In: bind a figure whose label is hyphenated to it, and one whose label is in an adjacent cell.
- Out: relaxing FIG-1 into a warning. A rule that cannot be trusted is worse than one that is
  strict, and a deck quoting a figure nobody wrote is exactly what this catches.

**Acceptance criteria**
- [ ] The mechanism is stated from the code, and this task's hypothesis is confirmed or replaced
- [ ] T-128's deck reports `FIG-1` pass with no edit to the deck
- [ ] A fixture carries a hyphenated figure and a cell-split label, red before and green after
- [ ] The false-alarm rate is reported as a list, not a count, so the next one can be judged
- [ ] No shipped deck moves

## 2. Plan

_Not planned._

## 3. Implement

_Not started._

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-16 | → proposed | Raised out of [T-167](T-167-checkpy-reads-a-quoted-source-as-the-decks-own-slide-copy.md)'s review. Recorded as a false alarm earlier the same day and deliberately not raised; that judgement was right on the evidence then and wrong by the end of the session, which is the reason to write the promotion down rather than quietly file it. |
