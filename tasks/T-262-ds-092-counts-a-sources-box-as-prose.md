---
id: T-262
title: Exclude provenance from DS-092's paragraph half, and give any source ceiling its own rule
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-225]
work_package: PH1
owner: the project owner
business_value: high
effort: s
created: 2026-08-29
updated: 2026-08-29
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
| 2026-08-29 | → proposed | Raised by [T-225](T-225-triage-the-claimai-adopter-report.md), the triage of the ClaimAI adopter report. **`PH1`**: a defect an adopter met in the published `0.6.0`, which is `CLAUDE.md`'s one condition for reopening the phase. Verified against this tree before the record was actioned — the report's `Version seen` was stamped rather than re-run on fourteen of the twenty-seven. |
