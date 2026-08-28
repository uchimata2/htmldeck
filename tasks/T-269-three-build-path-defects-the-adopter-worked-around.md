---
id: T-269
title: Unwrap a provenance row, read a rich Sources field, and convert bold across a line break
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

# T-269 — Unwrap a provenance row, read a rich Sources field, and convert bold across a line break

## 1. Specify

**Outcome**
Three build-path tools handle input the adopter's deck actually contained. Today the reading view undoes the sources **box** and never the **item**, so `white-space:nowrap` survives into a document that must fold to 320 px and one long row holds the page open — while `DS-075` reports `overflowing: 0` because the probe scans `#docBody *` and the wide element is outside it; `spec.py` splits a `Sources` field on commas and semicolons and treats every fragment as a slug, so a field naming its section breaks `SPEC-2`, `SPEC-3` and `SPEC-4` at once; and a quick view leaves `**bold**` unconverted when the emphasis spans a line break.

**From the adopter report** [`003`](../docs/adopter-reports/claimai/003-reading-view-never-unwraps-a-provenance-row.md), [`004`](../docs/adopter-reports/claimai/004-spec-py-cannot-read-a-sources-field-that-carries-a-section.md), [`007`](../docs/adopter-reports/claimai/007-quickview-leaves-bold-unconverted-across-a-line-break.md).

**Scope**
- In: `.doc .sources-item{white-space:normal}` beside the `.doc .sources-box` rule it belongs with — **a deck should not have to repair the reading view**, and this one did
- In: splitting the `Sources` field on `;` only and taking the leading token, so both forms read; and `artifacts.md` stating the field's grammar, because today the only statement of it is a regex
- In: normalising a paragraph before the inline pass — **and a gate**: a scan for unconverted `**`, `__` or a leading `#` in rendered quick-view content, run where `spec.py` runs
- In: widening the `DS-075` probe's scan, or naming the widest element whatever the count says
- Out: anything the records above do not name. The report is a closed one-way hand-over — there is no
  channel back and none is expected, so a question this task cannot answer is settled here rather
  than asked.

**Inputs**
- the records above, [`003`](../docs/adopter-reports/claimai/003-reading-view-never-unwraps-a-provenance-row.md), [`004`](../docs/adopter-reports/claimai/004-spec-py-cannot-read-a-sources-field-that-carries-a-section.md), [`007`](../docs/adopter-reports/claimai/007-quickview-leaves-bold-unconverted-across-a-line-break.md) — each carries its evidence, its version and its own proposed fix
- each record carries its own reproduction; `003`'s is the one that cost most, because the failure named a number with nothing beside it

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
