---
id: T-261
title: Re-derive whether audit.PROBE can stay unpinned, on a deck whose entrance moves the axis
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-225, T-254]
work_package: PH1
owner: the project owner
business_value: critical
effort: s
created: 2026-08-29
updated: 2026-08-29
deliverables: []
---

# T-261 — Re-derive whether audit.PROBE can stay unpinned, on a deck whose entrance moves the axis

## 1. Specify

**Outcome**
`DS-035` decides legible type rather than mid-entrance geometry. Today the probe scales the computed font size by the element's screen CTM, so an ordinary `scaleY(0)` entrance with `fill-mode:both` puts the determinant at 0 and the rule fails three display-size headings at **0 du** — and the row says *text below 16 design units*, which sends a builder looking for a font size.

**From the adopter report** [`006`](../docs/adopter-reports/claimai/006-ds-035-measures-text-through-its-transform.md).

**Scope**
- In: measuring the rest state, or naming the transform as the cause when `sqrt(|det|)` is under 1
- In: **`DS-035` saying when a CTM is degenerate**, deferred here by [T-254](T-254-density-py-write-corrupts-every-self-closing-svg-tag.md) on 2026-08-29. Adopter record [`015`](../docs/adopter-reports/claimai/015-density-py-write-corrupts-a-self-closing-svg-tag.md) item 3 is the source: a broken tag made the browser reparent a subtree, and three untouched labels came back at `0.0 du` — **not small type, no type**, reported as a type-size failure. It is the same measurement and the same row as the clause above, which is why one task owns both. **This task closes that record's item 3**
- In: **re-deriving [T-209](T-209-six-more-probes-measure-a-page-whose-entrance-never-ran.md)'s verdict for `audit.PROBE`**, which is the part worth more than the fix — see the inputs
- In: the `DS-035` row saying the measurement is taken through the element's transform. Nothing in it hints that an entrance can fail a legibility rule
- Out: anything the records above do not name. The report is a closed one-way hand-over — there is no
  channel back and none is expected, so a question this task cannot answer is settled here rather
  than asked.

**Inputs**
- the record above, [`006`](../docs/adopter-reports/claimai/006-ds-035-measures-text-through-its-transform.md) — each carries its evidence, its version and its own proposed fix
- **This finding refutes a measurement the audit recorded as settled.** T-209 left `audit.PROBE` unpinned and its comment in `tools/deck/audit.py` reads *its geometry rows were measured both ways on the portfolio deck and are identical, so pinning buys nothing here*. That was one deck, whose entrances happen not to move the axis `DS-035` reads; this deck's do. **The conclusion does not generalise and the comment states it as if it does.**
- the design problem underneath: the same probe must stay unpinned for `DS-140`, `DS-142` and `DS-218`, which read `animationIterationCount`, and settled for `DS-035`, which reads geometry. One probe cannot be both, so this is a split rather than a flag

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
| 2026-08-29 | (no change) | **Gained `DS-035`'s degenerate-CTM question**, deferred here by [T-254](T-254-density-py-write-corrupts-every-self-closing-svg-tag.md) while B1 ran, with the reasoning in that task's §1. Two tasks amending one probe is the rework [`../docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) exists to avoid, so this task now closes adopter record `015` item 3 as well as `006`. Nothing else about its scope moved. |
| 2026-08-29 | → proposed | Raised by [T-225](T-225-triage-the-claimai-adopter-report.md), the triage of the ClaimAI adopter report. **`PH1`**: a defect an adopter met in the published `0.6.0`, which is `CLAUDE.md`'s one condition for reopening the phase. Verified against this tree before the record was actioned — the report's `Version seen` was stamped rather than re-run on fourteen of the twenty-seven. |
