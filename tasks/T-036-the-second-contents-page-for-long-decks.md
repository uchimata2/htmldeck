---
id: T-036
title: Continue the contents page onto a second sheet for decks past the measured bound
type: deliverable
status: proposed
phase: specify
parent: T-034
blocked_by: []
related: [T-034, T-005]
work_package: PH2
owner: maintainer
business_value: high
effort: m
created: 2026-08-08
updated: 2026-08-12
deliverables: []
---

# T-036 — Continue the contents page onto a second sheet for decks past the measured bound

## 1. Specify

**Outcome**
The printed contents page continues onto a **second sheet** when one sheet can no longer carry every
slide, so a long deck's contents page degrades by growing rather than by dropping entries. Decks at
or under the bound are unaffected and still print exactly one contents page.

**Why this exists rather than being folded into [T-034](T-034-a-contents-page-for-the-printed-deck.md)**
T-034 measured where its single page stops working, and the numbers put the problem outside the
target case rather than inside it — **the bound is 16 slides and the hard limit is 24, against a
target deck of 12**. Building a second page there and then would have been building for a deck size
nothing in this project currently produces. It is raised instead of dropped because the gap is real
and stated in the ruleset: **DS-226** requires that a compressing page *never drops an entry*, and
past 24 slides compression physically cannot honour that — at 25 slides a box has **89 du of height
for 96 du of number, title and padding**. A deck that long is therefore non-conformant today, and a
rule with a known unimplementable range needs either the implementation or an amendment.

**The two numbers this task inherits, both measured 2026-08-08** — see
[T-034](T-034-a-contents-page-for-the-printed-deck.md) §1 *The bound*, which is the home of the
measurement and is not restated here:

- **16 slides** — the largest deck where the page does its whole job, description included.
- **24 slides** — the largest deck where number and title still render at all.

**Scope**
- In: the continuation rule — when a second sheet is added, and how the boxes divide across sheets.
- In: the consequence for the printed page count, which stops being `n` + 1.
- Out: changing the single-page layout itself. That is T-034's and it is measured and settled.
- Out: an on-screen equivalent. The overlay index scrolls, so it has no equivalent problem.

**Inputs**
- [`T-034`](T-034-a-contents-page-for-the-printed-deck.md) §1 — the geometry, the conversion, the
  compression rule, and the measured bound.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §5.4 — DS-225 and DS-226.

**Acceptance criteria**
- [ ] A deck past the bound prints a contents page that carries **every** slide, with no entry
      dropped and no title clipped
- [ ] A deck at or under the bound prints **exactly one** contents page, unchanged from T-034
- [ ] The page count rule is restated wherever it is asserted — `DESIGN-SYSTEM.md` §5.4 and
      [T-005](T-005-build-check-the-gate-the-deck-must-pass.md)'s print row both currently say
      `n` + 1
- [ ] Measured on a deck built past the hard limit, not asserted
- [ ] Printed from a double-clicked file and **looked at** (**L-01**, **L-35**)

**Open questions**
- ~~**Where does the split fall — by count, or by stage?**~~ **Answered 2026-08-09: at a stage
  boundary.** The contents page exists to show the argument's structure, so a split that cuts a
  stage in half renders the argument as a paging artifact — the reader meets *where am I* at the
  sheet break, which is the failure the ruler was built to prevent. Filling sheet one and spilling
  the remainder is simpler to build and was rejected on that: the printed sheet **is** the
  deliverable here, not an export of it.
- ~~**Is the trigger the bound (16) or the hard limit (24)?**~~ **Answered 2026-08-09: 16, the
  measured bound.** `contents_bound.py` measured **16 entries with descriptions against 24
  without**, and the description is what makes a contents page more than a list of titles.
  Splitting at 24 keeps the page count down and accepts a description-free map anywhere between 17
  and 24 — a quality cliff nobody chose per deck and nothing would report.

*Both answered while [T-052](T-052-two-hard-judge-failures-in-the-reference-deck.md) was closing
out the audit run, so the task is fully specified whenever it is picked up. **It stays parked**: it
only bites past 24 slides and the target is 12.*

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
| 2026-08-13 | (no change) | **Split, not absorbed.** The owner asked for this task in `0.2.3`. It is a **capability** — a second sheet for decks past the bound — and what `0.2.3` needs is the **defect** below the bound, so that went to [T-116](T-116-the-printed-contents-page-collides-at-thirteen-entries.md) as `PH1`/`critical` and this stays `PH2`. T-116 also takes the bound re-measurement, since fixing the track sizing moves it; **this task reads the new number rather than the old one.** Not `blocked_by` — §1's questions were answered from a run made while the tool worked — but do not build the second sheet against 16 / 24. |
| 2026-08-13 | (no change) | **T-116 closed and the bound did not move: 16 / 24 stands, and the line above is discharged.** It was re-measured with a three-line description in every entry, which is the tallest realistic case and the one the old fixture lacked, and both numbers came back the same. The collision it was raised for was **not** a track-sizing fault at all — the tracks were right on both surfaces — so nothing here shifts. Build the second sheet against 16 / 24. |
| 2026-08-12 | (no change) | **The bound is already wrong, and the printed page is already broken — at 13 entries, not 24.** Looked at the first adopting project's exported PDF: page 1 is the generated contents page and its **fourth row collides with the page footnote** — card 13's last line and the words *"Detail behind the disclosure panels is on screen only"* print through each other — while rows 2 and 3 have card borders touching where entries with three-line bottom lines overrun their track. **16 / 24 was measured against boxes whose bottom lines were shorter than real ones.** So this task's premise is no longer *the next deck will be longer*; it is *a shipped deliverable already prints wrong*. The re-measurement is now in scope, not just the second sheet. |
| 2026-08-12 | (no change) | **Re-estimated `low` → `high`, and unparked.** Nothing about the task changed; its premise did. The `low` of 2026-08-10 rested on one sentence — *"the bound bites at 24 slides against a target deck of 12, so nothing this project produces reaches it"* — and the owner has now said the next deck is not limited to 12. **16 is the bound and 24 the hard limit**, so a deck of the size being planned crosses the first and can reach the second, where DS-226's invariant clips an entry. The work is no longer outside the target case; it is in front of it. Stays in `PH2`: the reason it sits there is unchanged. |
| 2026-08-10 | (no change) | **Unblocked the same day.** [T-084](T-084-the-contents-bound-fixture-counts-a-deck-that-no-longer-exists.md) closed: the fixture was counting twelve boxes for a deck that now builds thirteen, and re-baselining it restored the tool. It re-measures **16 as the bound and 24 as the hard limit** — the same pair this task was specified on — so nothing in §1 moves and the edge is removed. |
| 2026-08-10 | (no change) | **Now `blocked_by` [T-084](T-084-the-contents-bound-fixture-counts-a-deck-that-no-longer-exists.md).** `contents_bound.py` refuses to start — its fixture expects 12 contents boxes and the reference deck now builds 13 — so the instrument that measured this task's 16-entry bound, and the only thing that could verify a split, does not run. The specification is unaffected: both its open questions were answered from a run made while the tool still worked. A hard edge rather than `related` because the *verification* is genuinely gated, which is the test `TASK-WORKFLOW.md` §4 sets. Recorded during T-078's sweep of the release gate list, which is what found the tool red. |
| 2026-08-10 | (specify) | **Estimated `low`/`m`.** `low` because the bound bites at 24 slides against a target deck of 12, so nothing this project produces reaches it — what the task buys is closing DS-226's known-unimplementable range, not serving a reader; `m` for print pagination that must carry every entry across a break. **Stays in `PH2`** under the release split set by the owner 2026-08-10: moderate in size, and a conformance fix to a page that exists rather than a new capability. |
| 2026-08-08 | → proposed | Raised by [T-034](T-034-a-contents-page-for-the-printed-deck.md) on the strength of its own measurement rather than on a hunch. T-034 specified the second page as the *presumptive* answer past its single-page bound and said the measurement would decide whether the question cost anything; it measured **16 as the bound and 24 as the hard limit against a target deck of 12**, which puts the work outside the target case — so it is raised, not built. What stops it being simply dropped is that **DS-226 states an invariant the implementation cannot honour past 24 slides**: a box then has 89 du of height for 96 du of number, title and padding, so an entry is necessarily clipped. A ruleset with a known unimplementable range needs either this task or an amendment, and that choice is better made deliberately than by silence. |
