---
id: T-028
title: Retrofit the reference deck to the deliverable contract and thin its chrome
type: fix
status: proposed
phase: specify
parent: T-027
blocked_by: []
related: [T-002, T-005, T-021, T-024, T-025]
work_package: WP2
owner: maintainer
created: 2026-08-06
updated: 2026-08-06
deliverables: []
---

# T-028 — Retrofit the reference deck to the deliverable contract and thin its chrome

> **This task gates the first published version of the plugin** — owner, 2026-08-06.
> [`BRIEF.md`](../docs/BRIEF.md) *Decisions taken* → **Release gate**, and its definition of done
> carries the criterion. Nothing else is blocked by it; publishing is.

## 1. Specify

**Outcome**
[`examples/reference-deck.html`](../examples/reference-deck.html) carries a **bottom line on every
slide** per DS-201 to DS-209, and its navigation obeys DS-216 and DS-217. It becomes an example of
the ruleset as it now stands, rather than of the ruleset as it stood before the owner reviewed it.

**Why this is separate from T-027**
T-027 wrote the rules and repaired the two defects that broke **hard** rules — the stage clipping
(DS-200) and 28 dead `fill=` attributes, one of which rendered at 2.17:1 (DS-214, DS-215). What is
left is not a defect list. **Every slide needs a sentence it does not currently have**, and adding a
bottom line to a slide that was composed without one changes its layout, its emphasis and often its
headline. That is a rewrite, and it should be looked at rather than patched.

**The deck's current state against the new rules**

| Rule | Now | Needed |
| :--- | :--- | :--- |
| DS-202 bottom line on every slide | **absent on all 12** | one factual sentence per slide, no reasoning |
| DS-203 second-most-prominent element | n/a | a defined slot in the slide template, not a per-slide invention |
| DS-209 one emphasis, and it is the deliverable | several slides emphasise two or three things | one |
| DS-216 one encoding of position | **three** — spine ribbon, 12 dots, progress bar | one primary, plus at most one encoding a *different* fact |
| DS-217 chrome budget | **23 labelled items, 96 design units** | ~12 items; per-slide dots stop scaling near ten slides |

**The owner's words on the chrome, which are the acceptance test:** *"The bottom navigation area with
the subtitles above it are extremely noisy with that many dots."*

**Scope**
- In: a bottom line per slide, written before the layout changes — the outline contract (DS-210,
  DS-211) applied to a deck that already exists.
- In: a slot for it in the shared slide template, so it is one component reused, not twelve inventions.
- In: thinning the chrome to one position encoding within the DS-217 budget, keeping click-to-jump.
- In: re-running the gate and **looking at every slide** afterwards.
- Out: changing the deck's topic, argument or figures. The spine survived review; only the
  presentation of each slide's point changes.
- Out: any further rule change. If a rule proves unbuildable here, it is a finding for T-025, not an
  edit to `DESIGN-SYSTEM.md`.

**Inputs**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §3.4, §3.5, and DS-216/DS-217
- [`T-027`](T-027-specify-the-slide-deliverable-and-the-outline-contract.md) — the rules and why they exist
- [`T-024`](T-024-build-the-reference-deck-and-validate-the-ruleset.md) §3.1 — the deck's spine, which stands

**Acceptance criteria**
- [ ] Every slide has a bottom line: one sentence, factual, no reasoning, not the headline restated
- [ ] The bottom line is the second-most-prominent text on the slide, verified by rendered measurement
- [ ] No slide emphasises more than one thing
- [ ] Exactly one primary encoding of position; chrome within DS-217's budget
- [ ] `python tools/deck/audit.py` reports zero mechanical failures
- [ ] Every slide opened offline and looked at, and the result stated as what was seen

**Open questions**
- **Does the bottom line replace the standfirst, or sit below the body?** The standfirst currently
  does some of this work on some slides and none on others. — this task, against a rendered slide

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Write the twelve bottom lines first, as an outline, with no HTML open | the outline |
| 2 | Add one bottom-line slot to the slide template and place it | the component |
| 3 | Reduce each slide to a single emphasis, the deliverable | the slides |
| 4 | Thin the chrome to one position encoding inside the budget | the navigation |
| 5 | Gate, measure, and look at all twelve offline | the verdicts |

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
| 2026-08-07 | (no change) | **A label collision on slide 2's timeline, found while looking at [T-018](T-018-measure-the-printable-mode-what-printing-from-fi.md)'s printed output** and recorded here because it is a deck defect, not a print defect. Two markers sit close enough that their labels overlap and read as one word — *"Budget vote"* against *"Grant closes"*, and *"12 Mar 2027"* against *"31 Mar 2027"*. **Whether it also occurs on screen was not checked**, so treat that as the first question rather than an assumption; the print rendering uses the same 1920×1080 stage geometry, which makes it likely. Noted rather than fixed: T-018 was measuring the printable mode, and quietly editing the deck it was measuring would have invalidated its own run. |
| 2026-08-07 | (no change) | [R7](../docs/research/R7-printable-mode.md) ruled the printable mode is the **paginated stage**, so this deck's committed `@media print` block — which prints the reading view — is now the rejected rendering. Adoption is [T-032](T-032-adopt-the-paginated-print-mode-in-the-reference-deck.md), split out rather than folded in here because it carries an owner decision about tier two with a page-count consequence. |
| 2026-08-06 | (no change) | **Made a release gate by the owner: this lands before the first published version.** Recorded in `BRIEF.md` *Decisions taken* and added to its definition of done as a seventh criterion. The reasoning is that the example deck is the plugin's argument for itself, so shipping one that fails the deliverable contract argues against the ruleset it is meant to demonstrate. No `blocked_by` edge exists for it — nothing else in the backlog is gated, only publishing. |
| 2026-08-06 | (no change) | Confirmed still open by [T-025](T-025-reconcile-the-twelve-ruleset-findings-from-the-reference-deck.md): the three simultaneous position encodings (DS-216/DS-217) are visible in every capture taken during its re-check, and no rule change there touched them. |
| 2026-08-06 | → proposed | Raised by [T-027](T-027-specify-the-slide-deliverable-and-the-outline-contract.md). The owner's review produced two hard-rule defects, fixed there, and one change that is a rewrite rather than a fix: **no slide in the deck states its deliverable**, because the rule requiring it did not exist when the deck was built. Chrome density comes with it — three encodings of position, which the owner called *"extremely noisy"*. |
