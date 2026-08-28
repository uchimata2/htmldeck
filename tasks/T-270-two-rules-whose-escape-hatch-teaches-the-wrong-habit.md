---
id: T-270
title: Decide what DS-100 and DS-202 should measure, and say the reason in each failure
type: decision
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-225]
work_package: PH3
owner: the project owner
business_value: low
effort: s
created: 2026-08-29
updated: 2026-08-29
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
- [ ] every record named above is **closed with its remedy measured**, or explicitly deferred with the
      reason recorded in this task
- [ ] each fix is proved by seeding the defect and watching the check fire, in both directions where
      the record's own evidence is a verdict (**L-125**)
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None yet. Every record carries its own evidence and its own proposed fix; the proposal is a
  hypothesis and whoever implements it measures before committing to it.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <the files this task changed>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- <T-NNN or "none">

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → proposed | Raised by [T-225](T-225-triage-the-claimai-adopter-report.md), the triage of the ClaimAI adopter report. **`PH3`**: not a defect in the published plugin's behaviour, so `CLAUDE.md`'s rule puts it in the main line rather than reopening a shipped phase. |
