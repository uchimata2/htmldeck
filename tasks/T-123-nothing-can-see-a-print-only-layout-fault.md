---
id: T-123
title: Nothing can see a print-only layout fault, and one reached two shipped decks
type: decision
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-034, T-036, T-084, T-116]
work_package: PH3
owner: the project owner
business_value: high
effort: l
created: 2026-08-13
updated: 2026-08-13
deliverables: []
---

# T-123 — Nothing can see a print-only layout fault, and one reached two shipped decks

## 1. Specify

**Outcome**
A decision on whether this repository gates the printed *geometry* of a deck, and not only its page
count — taken with the cost of the instrument on the table, because the cost is the reason the
question is open rather than obvious.

**What happened**

[T-116](T-116-the-printed-contents-page-collides-at-thirteen-entries.md) was a collision on the
printed contents page that **no gate could see, and that the one tool aimed at that page reported as
clean**. The two readings, same deck, same day:

| | box height | rows 2→3 gap | verdict |
| :--- | ---: | ---: | :--- |
| `contents_bound.py`, print rules lifted onto screen | 175.7 du | +26.0 du | clean |
| the printed PDF | 200.2 pt = 267 du | −49.2 pt | rows print through each other |

The divergence is Chrome's paged layout giving a grid item its own content height rather than its
track, where the screen zeroes the item's automatic minimum because `overflow:hidden` says to. **No
screen measurement can see it**, whatever the fixture holds — T-116 verified that by re-running the
screen reading with the tall fixture and the CSS still broken, and it stayed clean.

It reached `examples/reference-deck.html`, which is 13 entries and printed with two overlapping row
pairs and its footnote inside a card, and it reached the first adopting project's presented deck.
Both were shipped. Every gate was green for both.

**Why this is not simply "add a check"**

Three things stand in the way, and they are the substance of the decision:

1. **The owner ruled the opposite on 2026-08-08.** `printpages.py` asserts the page count and only
   the count; DS-222 to DS-226 are left to the print a person does under `CLAUDE.md` rule 6, on the
   argument that a gate claiming those five would be claiming a judgement it cannot make
   ([T-038](T-038-the-gate-emits-verdicts-for-judge-rules-and-one-wrong-id.md)). T-116 is evidence against that ruling —
   *collision* is geometry, not judgement — but overturning it is the owner's call, which is why
   this is a `decision` and not a `fix`.
2. **The instrument is not cheap.** Reading card positions out of Chrome's PDF needs a graphics-state
   stack: the rounded cards are béziers, not `re` operators, and the content stream nests `q`/`cm`.
   A throwaway that ignored the nesting returned coordinates in the tens of thousands. It is a real
   parser, and it is pinned to what Chrome's PDF writer emits.
3. **The obvious shortcut is barred.** pymupdf reads this correctly in four lines and was used
   throughout T-116's diagnosis, but it is not a repository dependency and `contents_bound.py` is
   pure standard library by **L-07**. Taking a dependency for one gate is its own decision.

**Scope**
- In: whether the printed geometry is gated at all, and if so, what it asserts. The narrow useful
  assertion is *no card overlaps another and none reaches the footnote* — a `>` between numbers, not
  a judgement.
- In: what the instrument costs, decided against L-07 and against a new dependency.
- In: whether `contents_bound.py` keeps measuring on screen at all once something measures on paper.
- Out: the second contents sheet — [T-036](T-036-the-second-contents-page-for-long-decks.md).
- Out: DS-222 to DS-226 as judgements. This is about geometry only, which is what makes it
  answerable where T-038 was not.

**Inputs**
- [T-116](T-116-the-printed-contents-page-collides-at-thirteen-entries.md) §3 — the mechanism, the
  two readings, and the prototype that priced the parser.
- [T-038](T-038-the-gate-emits-verdicts-for-judge-rules-and-one-wrong-id.md) — the 2026-08-08 ruling this would revisit.
- [`tools/deck/printpages.py`](../tools/deck/printpages.py) — where a geometry assertion would go,
  and the existing pure-stdlib PDF reading to build on.
- [`tools/deck/contents_bound.py`](../tools/deck/contents_bound.py) — the tool that reported clean.

**Acceptance criteria**
- [ ] A decision is recorded, either way, with the cost that decided it.
- [ ] If the answer is yes: a seeded overlap is caught, and a correct page passes — measured against
      both, not against the correct one alone (**L-05**).
- [ ] If the answer is no: the limitation is stated where someone about to trust the screen numbers
      will read it, and the manual print step is named in the release gate rather than assumed.

**Open questions**
- ~~Should the printed geometry be gated at all?~~ **Answered by the owner 2026-08-13: yes,
  narrowly.** The assertion is *no card overlaps another and none reaches the footnote*, and nothing
  wider. So the 2026-08-08 ruling stands where it was aimed — DS-222 to DS-226 as *judgements* stay
  with the person who prints — and it is narrowed only where the property is arithmetic. What is
  left for `specify` is the instrument, not the question.
- Is `examples/` the only surface this gates, or does an adopter's deck get it too — the owner.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |

## 3. Implement

**Decisions & assumptions**
-

**Outputs produced**
-

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-13 | → proposed | Raised out of T-116, which found a printed collision that the screen measurement reported as clean and that reached two shipped decks. `PH3` and `l`: the instrument is a PDF graphics-state parser or a new dependency, and either way it revisits the owner's 2026-08-08 ruling on what the print gate asserts. |
| 2026-08-13 | (no change) | **The owner answered the same day: yes, narrowly.** Gate *no card overlaps another and none reaches the footnote*, and nothing else. The type stays `decision` because the decision is what was asked for and it is now recorded; the remaining work is the instrument, and this task carries it under its second acceptance criterion. **Stays `PH3` and out of `0.2.3`** — `l` puts it there by the rule in [`../CLAUDE.md`](../CLAUDE.md), and the release it would protect is three tasks that are nearly done. Not `blocked_by` anything. |
