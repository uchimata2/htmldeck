---
id: T-270
title: Decide what DS-100 and DS-202 should measure, and say the reason in each failure
type: decision
status: done
phase: review
parent: null
blocked_by: []
related: [T-225]
work_package: PH3
owner: the project owner
business_value: low
effort: s
created: 2026-08-29
updated: 2026-08-29
shipped_in: unreleased
deliverables: []
---

# T-270 — Decide what DS-100 and DS-202 should measure, and say the reason in each failure

## 1. Specify

**Outcome**
**A decision.** Two rules test a proxy and their escape hatches teach worse habits than the rules prevent. `DS-100` fires on any `?` immediately preceding a tag, so a question the slide answers on the same face fails — and the word *Why?* was **drawn as a shape** to get past it, putting content outside the reach of every text instrument in the toolchain. `DS-202` allows a bottom line of exactly one sentence, so an author's chosen two-clause form was joined with *and*: not one of his words changed, but the form he picked did.

**From the adopter report** [`023`](../docs/adopter-reports/claimai/023-ds-100-fires-on-any-question-mark-meeting-a-tag.md), [`024`](../docs/adopter-reports/claimai/024-ds-202-refuses-a-two-sentence-bottom-line-the-author-chose.md).

**Scope**
- In: `DS-100`: extending the existing **source-question exemption** to a question the same slide answers. The rule's own code already draws the distinction; it just does not extend it
- In: `DS-202`: **saying the reason in the failure** — *a bottom line is one sentence so it cannot become an argument* is a sentence an author accepts, where `not one sentence: 1` is one they work around
- Out: anything the records above do not name. The report is a closed one-way hand-over — there is no
  channel back and none is expected, so a question this task cannot answer is settled here rather
  than asked.

**Inputs**
- the records above, [`023`](../docs/adopter-reports/claimai/023-ds-100-fires-on-any-question-mark-meeting-a-tag.md), [`024`](../docs/adopter-reports/claimai/024-ds-202-refuses-a-two-sentence-bottom-line-the-author-chose.md) — each carries its evidence, its version and its own proposed fix
- **Two halves of these records are recommended against, and the reasons are here rather than in a reply.** `023` also offers *make the rule reviewable rather than fatal*: `DS-100` is `hard` because a rhetorical question is a house-style failure the corpus measured, and *reviewable* is how a rule quietly stops being enforced. `024` also offers replacing the sentence count with a word or clause cap: that trades a crisp rule for a fuzzy one, and the record itself says `DS-202` caught **eight** bottom lines restating their headline
- both records say plainly they are not arguments to drop the rule, which is why they are worth acting on

**Acceptance criteria**
- [x] every record named above is **closed with its remedy measured**, or explicitly deferred with the
      reason recorded in this task
- [x] each fix is proved by seeding the defect and watching the check fire, in both directions where
      the record's own evidence is a verdict (**L-125**)
- [x] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None yet. Every record carries its own evidence and its own proposed fix; the proposal is a
  hypothesis and whoever implements it measures before committing to it.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | **Measure the ruled `DS-100` condition before writing it** (**L-141**, **L-143**): how many slides in this repository's decks satisfy *a `?` followed, within the slide, by a declarative bottom line*? | the number that decides whether it is a narrowing or an off switch |
| 2 | `DS-202`: put the reason in the failure, keep the count | `tools/deck/audit.py`, `docs/DESIGN-SYSTEM.md` |
| 3 | Prove it by seeding a two-sentence bottom line on a real deck and reading the message an author would see | the reproduction |
| 4 | Whatever step 1 says about `DS-100`, record it where the decision is taken | `docs/REMEDIATION-ORDER.md` §3 |
| 5 | Close both adopter records, each saying which half was taken and which refused | `docs/adopter-reports/claimai/023…`, `024…` |

## 3. Implement

**Decisions & assumptions**

- **The `DS-100` half is refused, by its own measurement — 2026-08-29.** The ruling accepts report
  `023`'s proposal 1, whose condition the report states as *a `?` followed, within the slide, by a
  declarative bottom line*. Measured on the three tracked decks first: **38 slides, 38 with a bottom
  line, 38 declarative — 100%.** The component contract puts exactly one `.bottom-line` on every
  slide and `DS-202` requires it to be one factual sentence, so the guard is true by construction.
  Written as ruled it would have taken a `hard` rule to zero findings behind a green verdict, which
  is **L-143** exactly and which B6 has already paid for once. **`DS-100` is therefore unchanged**,
  and the question of what it should measure instead is recorded in
  [`../docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) §3, on `PR-36` and `PR-77`'s
  precedent — the mechanism is a new rule question, not a detail of the one ruled, and §4's
  authority does not reach it.
- **A recommendation went with it, and so did its limit.** Narrow by *where* the question sits — a
  `?` in a slide's `<header>` fails, one anywhere else in slide copy passes. It admits both of the
  adopter's cases and still fails *Why does this matter?* as a headline. **It cannot be calibrated
  here**: all three decks carry zero `?` in copy, so there is no firing rate to compare and the
  recommendation rests on the argument rather than on a count. Said in the order rather than
  implied.
- **`DS-202` keeps its count and gains its reason — 2026-08-29.** The report's other proposal, a
  word or clause cap, was refused as ruled: it trades a crisp rule for a fuzzy one, and the same
  task that raised the report found eight bottom lines restating their own headline. The failure now
  reads *one sentence is the rule so the line cannot become an argument; shorten it rather than
  joining the two with `and`* — the second clause names the workaround the report actually took, so
  the message answers the thing an author is about to do.

**A defect in the reproduction, recorded because it is the same trap twice in one batch.** The first
seeded bottom line read `Treatment works. It stops short` with no final stop. The probe counts
terminal punctuation, so that is **one** sentence end, and the seeded defect came back green — a
defect that was never seeded, wearing the same green as a fix that works. Caught by asking why the
control and the seeded case agreed.

**Outputs produced**
- [`tools/deck/audit.py`](../tools/deck/audit.py) — the `DS-202` failure's reason clause
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — the `DS-202` amendment note. **`DS-100`'s
  row is untouched**
- [`docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) §3 — the refused ruling, its
  measurement and the recommendation
- [`docs/adopter-reports/claimai/023-…`](../docs/adopter-reports/claimai/023-ds-100-fires-on-any-question-mark-meeting-a-tag.md)
  and [`024-…`](../docs/adopter-reports/claimai/024-ds-202-refuses-a-two-sentence-bottom-line-the-author-chose.md)

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every record closed with its remedy measured, **or explicitly deferred with the reason recorded in this task** | pass | `024` closed. **`023` deferred**, which is the second limb of this criterion rather than a miss: its ruled remedy was refused by measurement, the reason is above, and the open question is in the order's §3 where the decision is taken |
| Each fix proved by seeding the defect and watching the check fire, in both directions (**L-125**) | pass | On `measure-first.html` itself. Control `bottom lines that are not one sentence: 0` pass; a bottom line seeded to two sentences gives `1 - Larkfield Dental Group - one sentence is the rule so the line cannot become an argument; shorten it rather than joining the two with `and`` **FAIL**. Nothing to prove for `DS-100`, which is unchanged |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | pass | Recorded in the batch's closing run |

**A look is owed: no.** This task changes one failure message and three documents, and leaves
`DS-100` alone. Nothing any deck renders changes, so
[`../docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md) takes no row.

**Child fix tasks raised**
- none. The `DS-100` question is the owner's and is recorded in the order's §3; a task is what
  follows the ruling, as `T-274` and `T-275` followed the last two.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → done | Implemented in **B8**, and **half the ruling was refused by its own measurement**. `DS-202` keeps its count and its failure now says why the count is one. `DS-100` is **unchanged**: the ruled condition — a `?` followed by a declarative bottom line — holds on **38 of 38** slides across the three tracked decks, because the contract puts one on every slide and `DS-202` makes it declarative. That is an off switch behind a green verdict (**L-143**), so the question of what `DS-100` should measure went to [`../docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) §3 with a recommendation and its stated limit, on `PR-36` and `PR-77`'s precedent. Report `024` closed, `023` deferred. |
| 2026-08-29 | → proposed | Raised by [T-225](T-225-triage-the-claimai-adopter-report.md), the triage of the ClaimAI adopter report. **`PH3`**: not a defect in the published plugin's behaviour, so `CLAUDE.md`'s rule puts it in the main line rather than reopening a shipped phase. |
