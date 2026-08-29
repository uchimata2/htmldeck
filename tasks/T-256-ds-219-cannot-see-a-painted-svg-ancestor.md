---
id: T-256
title: Walk the full ancestor chain for DS-219's ground, and settle the doubt the rationale records
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-225]
work_package: PH1
owner: the project owner
business_value: critical
effort: m
created: 2026-08-29
updated: 2026-08-29
deliverables: []
---

# T-256 — Walk the full ancestor chain for DS-219's ground, and settle the doubt the rationale records

## 1. Specify

**Outcome**
`DS-219` measures a label against the ground a reader actually sees. Today it walks to the nearest painted background and **stops at the mark**, so a pale label on a pale card resting on a filled panel is measured against the card alone and can never reach 3:1. The adopter's deck fails **40 of 46 labels** and has since the build; every attempt to fix it made the slide worse.

**From the adopter report** [`019`](../docs/adopter-reports/claimai/019-ds-219-cannot-see-a-painted-svg-ancestor.md).

**Scope**
- In: compositing painted ancestors rather than stopping at the first
- In: **saying so where the walk cannot resolve a ground** — an unmeasurable pair and a failing pair are different findings
- In: **settling the `never`**: [`DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) section 5.7 is headed *two rules that said more than they meant* and says of this one that *the prohibition outran its own argument*. This is independent evidence for a doubt this repository already recorded, from a deck built without knowing the section existed
- Out: anything the records above do not name. The report is a closed one-way hand-over — there is no
  channel back and none is expected, so a question this task cannot answer is settled here rather
  than asked.

**Inputs**
- the record above, [`019`](../docs/adopter-reports/claimai/019-ds-219-cannot-see-a-painted-svg-ancestor.md) — each carries its evidence, its version and its own proposed fix
- [T-241](T-241-the-design-system-and-the-rationale-against-what-shipped.md), which closes `PR-97` — the rationale recording conflicts as unresolved. **This task supplies the evidence that one of them can now be settled**
- the second face in the record: seven unfilled `rect`s are black, `DS-215` reported fourteen runs under 4.5:1 and `DS-219`'s count rose by the same fourteen — the rule sees a painted *sibling* it was never meant to measure and misses the *ancestor* that is the real ground

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
| 1 | Reproduce the record's shape on this repository's own deck — a pale card whose only real contrast comes from a panel *inside* the figure | Baseline 0 of 3 failing; with the panel behind a paled card, **1 of 3 FAIL**, measured against the page |
| 2 | Read `DESIGN-RATIONALE.md` §5.7 before amending anything, because the record offers it as corroboration | §5.7 records a **settled** amendment from 2026-08-09, not an open doubt. The corroboration does not hold, and item 3 of the record is answered rather than done |
| 3 | Rewrite the ground walk: the figure's own shapes, taking those painted before the mark, then the DOM chain, then the body — composited | `groundOf(el, stopAt)` in `audit.py`, with `rgba()` and `over()` beside it |
| 4 | Separate *unmeasurable* from *failing*, and keep an all-unmeasurable deck from reading as a pass | `markPairsUnmeasurable`; the row names them, and the verdict is `None` when nothing is measurable |
| 5 | Prove all three directions | `panel` **FAIL → pass**; `nopanel` **still FAIL**; a gradient fill **FAIL → pass, 1 unmeasurable named**; every mark a gradient → **NO SUBJECT** |
| 6 | Amend the rule row, and put the measurement where the doubt is recorded | The `DS-219` row; `DESIGN-RATIONALE.md` §5.7; [L-142](../docs/lessons/L-142.md) |

## 3. Implement

**Decisions & assumptions**
- **Fix the walk, keep the rule, re-measure** — the owner's ruling, [`REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) §3, and the measurement supports it. With the walk corrected, the record's own shape passes and a pale card with **nothing** behind it still fails. The rule's force is intact; what was wrong was the surface its first number was taken against.
- **The record's item 3 is answered, not done.** 2026-08-29. It reads `DESIGN-RATIONALE.md` §5.7 as an open doubt about DS-219 and offers the deck as the case for settling it. §5.7 is a record of a *settled* amendment — the ban became two measurements on 2026-08-09 — so there was no `never` left to settle. §5.7 now carries the re-measurement, which is the evidence [T-241](T-241-the-design-system-and-the-rationale-against-what-shipped.md) needs for `PR-97`.
- **The ground composites alpha rather than reading three channels.** 2026-08-29. `lum()` ignores the fourth channel, so a half-transparent overlay was measured as if it covered. A layer that does not cover is not a ground, and the walk now stops at the first layer that does.
- **Only shapes painted *before* the mark count as its ground.** 2026-08-29. Document order is paint order in SVG, so anything at or after the mark is drawn over it and is not underneath it. Without this the mark's own fill would have entered its own ground.
- **`paintedBehind` is left alone.** 2026-08-29. It serves DS-214/DS-215 and asks a different question — what is behind a *text run* — so changing both from one task would have moved two rules while measuring one. The record's *second face* is a deck defect anyway: an SVG `rect` with no fill declaration is black, and one fill rule cleared it.
- **No look is owed.** No deck changed. *A caveat worth stating: this rule is about what a reader sees, and what changed is the check's model of that. The five tracked decks' verdicts are unmoved, so nothing here is waiting on an eye — but the first deck that relies on a composited ground is a good candidate for the owner's looking pass.*

**Outputs produced**
- [`tools/deck/audit.py`](../tools/deck/audit.py) — `groundOf`, the `rgba`/`over` helpers, the unmeasurable bucket and the `DS-219` row
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — the `DS-219` row
- [`docs/DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) §5.7 — the re-measurement
- [`docs/lessons/L-142.md`](../docs/lessons/L-142.md), [`docs/LESSONS.md`](../docs/LESSONS.md)
- [`docs/adopter-reports/claimai/019-ds-219-cannot-see-a-painted-svg-ancestor.md`](../docs/adopter-reports/claimai/019-ds-219-cannot-see-a-painted-svg-ancestor.md) — closed

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Record [`019`](../docs/adopter-reports/claimai/019-ds-219-cannot-see-a-painted-svg-ancestor.md) closed with its remedy measured | pass | Items 1 and 2 implemented and measured; item 3 answered — the section it rests on records a settled amendment, not an open doubt |
| Each fix proved by seeding the defect and watching the check fire, in both directions (**L-125**) | pass | Four fixtures. `panel` **1 of 3 FAIL → 0 of 3 pass**; `nopanel` **still FAIL**, so the rule keeps its force; one gradient fill → pass with **1 unmeasurable** named; every mark a gradient → **NO SUBJECT**, not a pass |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | pass | Both run at the end of B6, on a tree nothing was editing |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → proposed | Raised by [T-225](T-225-triage-the-claimai-adopter-report.md), the triage of the ClaimAI adopter report. **`PH1`**: a defect an adopter met in the published `0.6.0`, which is `CLAUDE.md`'s one condition for reopening the phase. Verified against this tree before the record was actioned — the report's `Version seen` was stamped rather than re-run on fourteen of the twenty-seven. |
| 2026-08-29 | → done | Batch **B6**. The ground is composited over every painted layer under the mark, the figure's own shapes included, and an unmeasurable pair is no longer reported as a failed one. **The record's wider claim is refused**: §5.7 records a settled amendment, and with the walk fixed the deck's shape passes while a genuinely pale mark still fails. Kept as [L-142](../docs/lessons/L-142.md). |
