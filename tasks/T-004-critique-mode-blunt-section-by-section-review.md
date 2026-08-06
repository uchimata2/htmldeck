---
id: T-004
title: Critique mode — blunt section-by-section review
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: [T-014]
related: [T-002]
work_package: WP3
owner: maintainer
created: 2026-08-04
updated: 2026-08-06
deliverables: []
---

# T-004 — Critique mode — blunt section-by-section review

## 1. Specify

**Outcome**
A mode that reviews a deck slide by slide, bottom line up front, with no diplomatic padding.

**Why this one**
The most useful artifact in the corpus is a critique, not a deck. It caught a structural gap in the argument, a two-column format that only landed on one side, a "Venn diagram" whose sets did not overlap, a metaphor used four times, a typo on the most important slide, and generator branding left in a corner. This is the part users cannot do for their own work.

**Acceptance criteria**
- [ ] Opens with a verdict, then grades each slide
- [ ] Names specific defects with the slide they are on — no general advice
- [ ] Run against a deck with known defects and found them
- [ ] Voice stays direct; no compliment sandwich
- [ ] **When sources are supplied, reconciles the deck against them** — and reconciles the sources
      against each other, because a deck inherits their disagreements
- [ ] Run against a deck built from sources that contradict each other, and found the contradiction
- [ ] States plainly when it reviewed the deck alone, so a clean report is not read as "the content
      is right"

**The second class of finding**

The corpus critique's findings are all inside one deck. `docs/BRIEF.md` § *The critique pass* records
a second class, from a five-document set audited before its deck was built: figures correct where
written and wrong where quoted, a summary contradicting the table above it, a count drifted from the
model it described. Each document had passed its own review. **All of them were found by counting,
not reading** — so this mode needs a counting pass, not only a reading pass.

The cheap technique that worked: one table of every figure in the material, its origin, and every
place it is reused.

**Open questions**
- Should critique be able to apply its own fixes, or only report?
- Does the counting pass belong here or in the build check (T-005)? They overlap. Likely: T-005
  gates automatically, critique explains and prioritises.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <path>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-04 | → proposed | Seeded from `docs/BRIEF.md` when the project folder was prepared. |
| 2026-08-05 | (no change) | Added the cross-document class of finding and the counting pass, after a source-document audit found nine defects that five per-document reviews had all passed. Evidence in `docs/BRIEF.md`. |
| 2026-08-06 | (no change) | Owner answered BRIEF open question 6 — sources are supplied, so the cross-document reconciliation added above is now a **standing** part of this mode rather than a conditional one. Two further inputs landed: R3 §6's 12 anti-patterns are directly usable as named defect classes, and R2 §11 gives this mode a testable disclosure check — close every panel and read the deck; if a slide stops making its argument, the tier split is wrong. R4 §2 found the critique format has **zero prior art**, so R1 §14's severity scheme is the only source for it. |
| 2026-08-06 | (no change) | **T-014 closed.** [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) **§6 owns the twelve anti-patterns and the named defect classes; this mode consumes them and must not restate them** — a check and the standard it tests cannot be two documents. Kept there deliberately, and T-014 recorded it as the assumption to revisit if this task disagrees when planned. M3–M6, M8, M9 and M11 were **deferred to here** as the report's format. The severity scheme (M2) stays in the design system as shared vocabulary. §11 conditions 15 and 23 are explicitly **not machine-checkable** and belong to this mode. |
| 2026-08-06 | (no change) | **This mode is now the reporting face of a defined evaluator, not a free-standing review.** [`docs/EVALUATION.md`](../docs/EVALUATION.md) supplies the dimensions, anchors, threshold and the four stop outcomes; the design system supplies `DS-nnn` IDs so a finding can cite a rule and a fix can be verified against it. **Three consequences:** findings carry a rule ID and a dimension score, not just prose; the report must state **which passes ran** (auto / render / per-slide / whole-deck), since the whole-deck pass is where cross-slide defects live; and the four outcomes are **not interchangeable** — PASS, CAP, STALL and OSCILLATION need different reports, and OSCILLATION is a finding about the *ruleset* that belongs in `DESIGN-RATIONALE.md` §2. |
