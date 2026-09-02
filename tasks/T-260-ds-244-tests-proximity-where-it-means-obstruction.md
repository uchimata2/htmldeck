---
id: T-260
title: Decide what DS-244 measures, from the two findings that contradict each other
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
shipped_in: unreleased
deliverables: []
---

# T-260 — Decide what DS-244 measures, from the two findings that contradict each other

## 1. Specify

**Outcome**
`DS-244` decides whether anything is actually obscured. Today it compares text against text and nothing else, which makes it **wrong in both directions at once** — the pair of findings is why this is one task. It **misses** a label crossing the rectangle it labels, the commonest way a hand-built figure goes wrong, three instances in one evening on slides it called clean. It **refuses** a cross-fade in place, because it does not read `opacity` and cannot see that only one of the pair is ever visible — three constructions rejected in a row on one slide.

**From the adopter report** [`013`](../docs/adopter-reports/claimai/013-ds-244-sees-label-over-label-but-not-label-over-shape.md), [`022`](../docs/adopter-reports/claimai/022-ds-244-refuses-a-cross-fade-in-place.md).

**Scope**
- In: reading the computed `opacity` before pairing two labels
- In: comparing a text rect against `rect`, `path` and `line` in the same `svg.fig` — and the test has to be *crosses a shape edge*, never *touches a shape*, because a label centred in its own box is legitimate
- In: **saying which frame was measured** where opacity is animated
- In: **at minimum, saying in the rule row what the measurement does not do**, so nobody reads a pass as *the labels are placed correctly*
- Out: anything the records above do not name. The report is a closed one-way hand-over — there is no
  channel back and none is expected, so a question this task cannot answer is settled here rather
  than asked.

**Inputs**
- the records above, [`013`](../docs/adopter-reports/claimai/013-ds-244-sees-label-over-label-but-not-label-over-shape.md), [`022`](../docs/adopter-reports/claimai/022-ds-244-refuses-a-cross-fade-in-place.md) — each carries its evidence, its version and its own proposed fix
- **Read the two records together or neither makes the point.** `013` says the rule is too blind and `022` says it is too strict; together they say it tests proximity of two text runs where it means obstruction
- [T-204](T-204-an-instrument-for-mark-collisions.md), which built `DS-244` and recorded text-against-line as *reports, never gates* after measuring 16 firings for 1 real defect. **That calibration is a term in this decision** and must not be quietly reversed
- `022` records that the rule improved the slide three times while being wrong — it is a report, not a complaint

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
| 1 | Read the opacity chain before pairing two labels, and count the labels dropped | `seen()` in the probe; `hidden` travels per slide |
| 2 | Add `text/shape` — a label whose own area falls past `STRADDLE_FRACTION` outside a **filled `rect`** — and leave it out of `GATED_KINDS` | `outside_fraction()`, the `rects` collection, and a self-test asserting the kind does **not** gate |
| 3 | Count the ungated kinds separately, and name the frame in the verdict | `noted_of()`; the row says *measured at rest, motion pinned* |
| 4 | Calibrate on the tracked decks, which is what the ruling asks for | **0 firings of `text/shape` across five decks.** No false-alarm rate exists to have, which is the argument for reporting rather than the hedge it looks like |
| 5 | Prove both new behaviours on a seeded deck, both ways | Cross-fade: gates when both are visible, silent when one is at `opacity:0`. Straddle: **90% outside** reported, and nothing for the same label centred |
| 6 | Re-run T-204's own count, to be sure the opacity guard did not swallow the rule it narrows | **15 label-on-line**, and the pre-change tool answers 15 on the same tree |
| 7 | Say in the row what a pass does not claim | The `DS-244` row's three stated limits |

## 3. Implement

**Decisions & assumptions**
- **`text/shape` reports and does not gate** — the owner's ruling, [`REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) §3, and T-204's precedent. **The calibration is the argument, and it came back empty**: across the five tracked decks the new kind fires **0 times**, so there is no evidence in either direction and a kind gating on none has a false-alarm rate nobody has measured. 2026-08-29.
- **Only a filled `rect` is compared.** 2026-08-29. Record `013` asks for `rect`, `path` and `line`. A `rect`'s bounding box **is** the rectangle; a filled `<path>`'s is not, and box-versus-box is the precise false alarm this tool's own self-test was written to refuse. Stroked, unfilled marks are already `text/line`, so adding them would double-count. This is narrower than the record asks and the reason is the record's own principle.
- **The test is *crosses an edge*, never *touches a shape*** — the record specifies this and it is the whole design. A label centred in the box it names is the correct placement and is what every diagram is made of.
- **Item 2 of record `022` is answered rather than implemented.** 2026-08-29. `render.MOTION_PIN` erases `animation-name` before the probe runs, so nothing in the page can afterwards tell an animated opacity from a static one; a per-element claim would be a guess dressed as a measurement. What is true and now stated is that **there is one frame, and it is at rest** — so a pair overlapping only mid-transition is not measured at all.
- **The first form of the opacity guard was wrong, and the way it was wrong is the lesson.** `visibility` is inherited and every off-screen slide is `visibility:hidden`, so reading it absolutely reported **129 hidden labels** on the reference deck and took the label-on-line count to **0**. A guard meant to narrow a rule had silenced it. Caught by re-running T-204's own count rather than by reading the code — which is why step 6 exists as a step rather than as a check at the end. Kept as [L-143](../docs/lessons/L-143.md): a guard added to narrow a rule can silence it, and the number that catches that is the rule's own prior count.
- **T-204's 16 is now 15 on the same four decks and 30 slides, and it did not move here.** 2026-08-29. The pre-change tool answers 15 on today's tree too; the decks have been rebuilt since 2026-08-21. The historical figure is annotated in place rather than restated, because it is a record of what was measured then.
- **No look is owed by this task.** Nothing renders differently. *Worth saying, though: `text/shape` exists precisely to catch what only a person catches today, and its first real evidence will come from a deck that has the defect — the owner's looking pass is where that arrives.*

**Outputs produced**
- [`tools/deck/markhits.py`](../tools/deck/markhits.py) — `seen()`, the `rects` collection, `outside_fraction()`, `noted_of()`, `STRADDLE_FRACTION`, the verdict text and eight self-test assertions
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — the `DS-244` row's three stated limits
- [`docs/adopter-reports/claimai/013-ds-244-sees-label-over-label-but-not-label-over-shape.md`](../docs/adopter-reports/claimai/013-ds-244-sees-label-over-label-but-not-label-over-shape.md), [`022-ds-244-refuses-a-cross-fade-in-place.md`](../docs/adopter-reports/claimai/022-ds-244-refuses-a-cross-fade-in-place.md) — closed

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Records [`013`](../docs/adopter-reports/claimai/013-ds-244-sees-label-over-label-but-not-label-over-shape.md) and [`022`](../docs/adopter-reports/claimai/022-ds-244-refuses-a-cross-fade-in-place.md) closed with their remedies measured | pass | Both closed. `013`'s first option taken and narrowed to filled rectangles with the reason; `022`'s first item implemented and its second answered as a stated limit |
| Each fix proved by seeding the defect and watching the check fire, in both directions (**L-125**) | pass | Cross-fade **gates with both visible, silent with one at `opacity:0`**, and the hidden label is counted rather than dropped silently. A label straddling a filled rect reports at **90% outside**; centred in the same box it reports nothing. Eight new self-test assertions, including that `text/shape` must not be in `GATED_KINDS` |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | pass | Both run at the end of B6, on a tree nothing was editing |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → proposed | Raised by [T-225](T-225-triage-the-claimai-adopter-report.md), the triage of the ClaimAI adopter report. **`PH1`**: a defect an adopter met in the published `0.6.0`, which is `CLAUDE.md`'s one condition for reopening the phase. Verified against this tree before the record was actioned — the report's `Version seen` was stamped rather than re-run on fourteen of the twenty-seven. |
| 2026-08-29 | → done | Batch **B6**. The rule now reads opacity before pairing, measures a label across the box it names, and says in its own row what a pass does not claim. **The new kind reports**: calibrated across five decks it fires zero times, so there is no false-alarm rate to gate on. The opacity guard's first form silenced the rule entirely — 129 hidden labels, 15 label-on-line placements to 0 — and was caught by re-running T-204's count rather than by reading the diff. |
