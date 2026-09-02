---
id: T-262
title: Exclude provenance from DS-092's paragraph half, and give any source ceiling its own rule
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-225]
work_package: PH1
owner: the project owner
business_value: high
effort: s
created: 2026-08-29
updated: 2026-08-29
shipped_in: 0.7.0
deliverables: []
---

# T-262 — Exclude provenance from DS-092's paragraph half, and give any source ceiling its own rule

## 1. Specify

**Outcome**
`DS-092` reads prose. Today the provenance mark is authored as a `<p class="provenance">`, so the rule counts the **sources box** as a paragraph: six source items each ending in a full stop read as six sentences and the slide fails. That puts an invisible ceiling of about three sources plus a verification line on any slide — against an author who asked to *repeat the source controls freely* — and two slides had to be trimmed, one losing a pointer with no other home.

**From the adopter report** [`012`](../docs/adopter-reports/claimai/012-ds-092-counts-a-sources-box-as-prose.md).

**Scope**
- In: excluding `.sources-box` from the paragraph-length half; the twenty-word sentence cap stays, because a source description past twenty words is a genuine defect
- In: **if a source ceiling is wanted, its own rule with its own number and message**, so a builder reads *this slide cites too many things* rather than *this slide's prose is too long*
- Out: anything the records above do not name. The report is a closed one-way hand-over — there is no
  channel back and none is expected, so a question this task cannot answer is settled here rather
  than asked.

**Inputs**
- the record above, [`012`](../docs/adopter-reports/claimai/012-ds-092-counts-a-sources-box-as-prose.md) — each carries its evidence, its version and its own proposed fix
- the component contract, which already distinguishes provenance from body copy by class

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
| 1 | Reproduce on this repository's own deck: grow one sources box past three items, each ending in a full stop | **Passed.** The seed was not yet the record's shape |
| 2 | Measure what the check sees rather than assume it. A probe dumping every `.provenance` run's text and sentence count | `2 sourcesCorridor model, 2026.Corridor model, 2026.…` — **one** sentence. The items are authored with no whitespace between the spans, and the sentence split needs whitespace after a terminator |
| 3 | Seed the whitespace authored markup actually has — one item per line — and re-run | `paragraphs over 4 sentences: 1` — the record's verdict line, to the word |
| 4 | Subtract the box from the paragraph before the sentences are counted, leaving the sentence half reading the whole run | `audit.py`: the run is cloned, `.sources-box` removed, and the paragraph counted on what is left |
| 5 | Seed the two things the rule must still catch | A five-sentence verification line beside the box, and a source item of twenty-five words. Both still FAIL |
| 6 | Amend the `DS-092` row, and settle the record's second suggestion | The row carries the prose/pointer distinction and the refusal of a source ceiling |

## 3. Implement

**Decisions & assumptions**
- **The box is subtracted from the paragraph; the provenance mark is not skipped.** 2026-08-29. The record proposes excluding `.provenance` and then corrects itself to `.sources-box`, and the correction is right: a verification line sits in the same `<p>` beside the box, it is prose, and skipping the whole mark would stop reading it. Only the box's text is removed.
- **The twenty-word sentence cap keeps reading source items.** 2026-08-29. The record asks for this in as many words, and it is the half of the rule that was never the complaint.
- **No source-count rule is added.** 2026-08-29. The record offers it conditionally — *if some ceiling on source count is wanted*. Nobody has said it is: the ceiling of about three was an accident of the prose rule, not a decision, and `.sources-item` is `1+` in the component contract. Inventing a number here would re-impose the same undecided limit with a better error message, and the remediation order's authority covers amending a row rather than adding a rule. It stays a `DS-000` question for whoever wants one.
- **Reproducing it needed something the record does not state**: the reference deck authors its source items with no whitespace between the spans, so `textContent` concatenates them and `2026.Corridor` never matches the sentence split. The defect therefore depends on the deck's own whitespace, which is worth knowing about any check that reads `textContent` for sentences. Recorded in the closed record rather than as a lesson, because it is one instrument's boundary rather than a general habit.
- **No look is owed.** The checker's verdict moved; no deck did.

**Outputs produced**
- [`tools/deck/audit.py`](../tools/deck/audit.py) — DS-092's paragraph half
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — the `DS-092` row
- [`docs/adopter-reports/claimai/012-ds-092-counts-a-sources-box-as-prose.md`](../docs/adopter-reports/claimai/012-ds-092-counts-a-sources-box-as-prose.md) — closed

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Record [`012`](../docs/adopter-reports/claimai/012-ds-092-counts-a-sources-box-as-prose.md) closed with its remedy measured | pass | Closed. Its primary fix taken in the precise form it names; its conditional second suggestion refused with the reason |
| Each fix proved by seeding the defect and watching the check fire, in both directions (**L-125**) | pass | Six terminated source items: **FAIL** before, **pass** after. A five-sentence verification line beside the box and a twenty-five-word source item both still **FAIL**, which is the paragraph half and the sentence half each still alive |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | pass | Both run at the end of B5, on a tree nothing was editing |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → proposed | Raised by [T-225](T-225-triage-the-claimai-adopter-report.md), the triage of the ClaimAI adopter report. **`PH1`**: a defect an adopter met in the published `0.6.0`, which is `CLAUDE.md`'s one condition for reopening the phase. Verified against this tree before the record was actioned — the report's `Version seen` was stamped rather than re-run on fourteen of the twenty-seven. |
| 2026-08-29 | → done | Batch **B5**. The sources box is subtracted from DS-092's paragraph half and read in full by its sentence half. A source ceiling was offered by the record and refused: the ceiling of about three was an accident, not a decision, and replacing it with a chosen number is a `DS-000` question nobody has asked. |
