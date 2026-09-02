---
id: T-265
title: Decide whether DS-110 narrows by where a raster sits
type: decision
status: done
phase: review
parent: null
blocked_by: []
related: [T-225]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-29
updated: 2026-08-29
shipped_in: 0.7.0
deliverables: []
---

# T-265 — Decide whether DS-110 narrows by where a raster sits

## 1. Specify

**Outcome**
**A decision, not a fix.** `DS-110` bans every raster the deck produces. The adopter's presenter supplied a pencil drawing for the lobby — front matter, which `DS-242` already defines as carrying nothing from the argument — and the deck now ships a permanent failure to do something the rule was never written to prevent. Every alternative was worse: no tracer installed, the drawn emblem already rejected, and the reading view is where nobody is sitting.

**From the adopter report** [`011`](../docs/adopter-reports/claimai/011-ds-110-cannot-tell-a-rasterised-diagram-from-a-drawing.md).

**Scope**
- In: the decision, argued both ways, with `DS-000`'s stated reason either way
- In: **the rule row saying what it protects.** *No raster the deck produces, ever* reads as a portability rule and is really a legibility and consistency rule about diagrams — that is the half worth doing whichever way the decision goes
- Out: anything the records above do not name. The report is a closed one-way hand-over — there is no
  channel back and none is expected, so a question this task cannot answer is settled here rather
  than asked.

**Inputs**
- the record above, [`011`](../docs/adopter-reports/claimai/011-ds-110-cannot-tell-a-rasterised-diagram-from-a-drawing.md) — each carries its evidence, its version and its own proposed fix
- **My recommendation is the record's own weaker form, not its primary.** Allowing any raster in a `front`/`back` section is broader than the argument supports; allowing one that is not inside `.body` and carries no `role="img"` label naming data is closer to the real test. It is harder to explain, which is a cost worth paying for a rule this load-bearing
- `CLAUDE.md` rule 3 — *still never raster images* — which this would amend and which is why the owner decides it

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
| 1 | **Reproduce on this repository's own deck before writing anything** (**L-141**). Put the same raster on `measure-first.html`'s lobby twice — inside `.body`, where the adopter put it, and as a sibling of `.body` — and run the whole gate on each, with the untouched deck as the control | the reproduction, and the answer to the question the ruling does not settle: whether the position it allows is a position the *rest* of the gate permits |
| 2 | Narrow `ds110_no_produced_raster` by **place**, on top of T-070's narrowing by **scope** | `tools/deck/audit.py` |
| 3 | Assert both directions and both boundaries in the self-test, on T-070's pattern | `tools/deck/audit.py` |
| 4 | Say what the rule protects, and record the amendment with its stated reason | `docs/DESIGN-SYSTEM.md`, and the failure line the gate prints |
| 5 | Correct `CLAUDE.md` rule 3, which states the ban this amends | `CLAUDE.md` |
| 6 | Close the adopter record | `docs/adopter-reports/claimai/011…`, and its `README.md` row |

## 3. Implement

**Decisions & assumptions**

- **The ruling is implementable, and step 1 is what proved it — 2026-08-29.** The position the
  ruling allows had to be a position the contract permits, and nothing in the ruling says it is.
  Measured: both positions fail **`DS-110` and nothing else**, on a control that is green. So
  `DS-229` does not object to an unclassed element beside `.body`, and narrowing `DS-110` is the
  whole of the change. Had the second position failed a second rule, the ruling would have bought
  the adopter nothing and this task would have reported that instead of implementing it.
- **`role="img"` is read as the literal attribute, not as *an element with the img role carrying a
  label* — 2026-08-29.** The wider reading fails the adopter's own image, which is
  `<img … alt="A pencil drawing">`: an `<img>` has the img role implicitly and `alt` names it. A
  test that refuses the case the ruling was given to permit is the wrong test. The literal reading
  is also the more explainable rule — *do not dress the raster as a figure that names data* is a
  thing an author does on purpose.
- **A raster outside every slide keeps failing — 2026-08-29, not asked for and taken anyway.** The
  ruling narrows by *where a raster sits*, and a `data:` URI in the style block sits nowhere: it is
  a background that can paint on any element, `.body` included. Implemented as written, the
  narrowing would have opened `background-image` as a hole nothing else in the gate covers. This is
  T-070's own discipline — a rule narrowed everywhere it is not measured has been lost rather than
  narrowed — and the self-test asserts it.
- **No stage is named, and that is the ruling's point.** The report's primary form keyed the escape
  to `data-stage="front"`/`"back"`. `DS-085` and `DS-242` both warn that a slide kind allowed to
  relax a rule hands the next slide kind the same argument, and the place test avoids naming a kind
  at all. A lobby therefore earns no blanket exemption: a raster in a **lobby's** `.body` still
  fails, which step 1's fixture A asserts and the self-test repeats.

**Outputs produced**
- [`tools/deck/audit.py`](../tools/deck/audit.py) — `_class_tokens`, `_body_spans`, `RASTER`, the
  rewritten `ds110_no_produced_raster`, its five new self-test assertions, and the failure line
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — the `DS-110` row: what it protects, both
  narrowings, and the amendment note
- [`../CLAUDE.md`](../CLAUDE.md) — rule 3's *still never raster images* is now *still never a
  rasterised diagram (DS-110)*, and the bound figure re-measured in the same edit as the rule
  requires: **15,597 bytes** against `tasks/TASK-WORKFLOW.md`'s **13,324**
- [`docs/adopter-reports/claimai/011-…`](../docs/adopter-reports/claimai/011-ds-110-cannot-tell-a-rasterised-diagram-from-a-drawing.md)
  and that folder's `README.md` — closed

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every record closed with its remedy measured | pass | Adopter record `011`. **Its remedy was not taken as proposed**: the primary form was refused for `DS-085`'s reason and the weaker form implemented, which is the ruling. The `role="img"` half was measured against the report's own image and read literally, for the reason in §3 |
| Each fix proved by seeding the defect and watching the check fire, in both directions (**L-125**) | pass | On `measure-first.html` itself, not on a fixture: raster inside `.body` → `1 failure(s): DS-110`; the same raster outside `.body` → `0 failure(s)`; untouched control → `0 failure(s)`. Five self-test assertions carry the same pair plus the three boundaries |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | pass | Recorded in the batch's closing run, not cited from an earlier one |

**A look is owed: no.** This task changes a rule and its checker. It changes nothing any deck
renders — no tracked deck carries a raster, and none gained one — so
[`../docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md) takes no row.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → done | Ruled by the owner and implemented in **B8**. The narrowing is by **place** on top of T-070's by **scope**, and the ruling's own question — whether the position it allows is one the rest of the gate permits — was measured first: both positions fail `DS-110` and nothing else. Two things were taken that nobody asked for and one refused: a raster in the style block keeps failing (it sits in no place, so a place-based escape cannot reach it), `role="img"` is read as the literal attribute (the wider reading refuses the adopter's own image), and the report's primary form was refused for `DS-085`'s reason. |
| 2026-08-29 | → proposed | Raised by [T-225](T-225-triage-the-claimai-adopter-report.md), the triage of the ClaimAI adopter report. **`PH3`**: not a defect in the published plugin's behaviour, so `CLAUDE.md`'s rule puts it in the main line rather than reopening a shipped phase. |
