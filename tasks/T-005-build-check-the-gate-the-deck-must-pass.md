---
id: T-005
title: Build check — the gate the deck must pass
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: [T-002]
related: [T-001, T-007, T-016]
work_package: WP3
owner: maintainer
created: 2026-08-04
updated: 2026-08-06
deliverables: []
---

# T-005 — Build check — the gate the deck must pass

## 1. Specify

**Outcome**
An automated check run on every generated deck.

**Why this one**
Cheap to build, and it converts several house rules from hopes into failures.

**Acceptance criteria**

*Presentation — always run*
- [ ] Fails on any external reference
- [ ] Fails on banned terminology
- [ ] Fails on a `<section>` with no heading
- [ ] Checks contrast against WCAG AA
- [ ] Fails when the deck does not render glitch-free **from `file://`** in the target browser —
      the restricted-origin failures (ES modules, `fetch`, XHR, some WebGL texture paths) are the
      likeliest way a rich deck ships broken. See T-017
- [ ] Fails on a console error or unhandled rejection on load or during navigation
- [ ] Fails on a theme value hard-coded outside the token layer — see T-007
- [ ] *Opt-in only:* when the user has asked for a printable deck, fails if disclosure content is
      dropped or slides clip. Not run otherwise — printing is a mode, not a gate
- [ ] Proven **failing** on each class before being trusted

*Content — run when source documents are supplied*
- [ ] Fails when a figure on a slide appears in no source
- [ ] Fails when a figure on a slide disagrees with the source it came from
- [ ] Fails when the same figure appears twice in the deck with different values
- [ ] Proven **failing** on each of those three before being trusted

*Honesty*
- [ ] The output states which half ran. "Presentation-only" is a legitimate result; reported as a
      clean pass, it is a false one
- [ ] Ships with a self-test on a case whose answer is known, and the self-test is part of the
      deliverable, not a one-off

**Why the content half exists**

A deck can pass every presentation check and still put a wrong number in front of a board. The
evidence is in `docs/BRIEF.md` § *The critique pass*: a five-document set where every document
passed its own review, and the figure that reached the board's decision cell was wrong in eight
places. Nothing on this task's presentation list would have caught it.

**Open questions**
- Is the check a separate command, or always part of build?
- Does the content half need the sources parsed, or is "the user pastes them in" enough? Ties to
  open question 6 in `docs/BRIEF.md`.

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
| 2026-08-05 | (no change) | Acceptance criteria split into presentation and content halves, plus an honesty criterion, after a source-document audit showed the presentation list cannot catch a wrong figure. Evidence in `docs/BRIEF.md`. |
| 2026-08-06 | (no change) | Added disclosure-layer and token-layer criteria after the owner identified progressive disclosure as their signature technique and chose a parametric single theme. |
| 2026-08-06 | (no change) | Corrected: print demoted from hard gate to opt-in mode, and the keyboard/hover criteria dropped, after the owner ruled that printing overrides nothing and that rich interaction is wanted. Replaced by `file://` render and console-error gates. |
| 2026-08-06 | (no change) | Owner answered BRIEF open question 6: **the check has two halves.** The content half reconciles every figure against the supplied sources and against itself; the presentation half runs regardless. When sources are absent the check runs presentation-only and **says which half it ran** — that requirement is now load-bearing rather than advisory. Also: "every `<section>` has a heading" becomes semantic — the heading must be a claim, not a label (R2 P-01) — and R2 §9 gives the accessibility floor as testable numbers. |
| 2026-08-06 | (no change) | **T-014 closed.** [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) **§11 states the hard rules as 26 numbered testable conditions**, written for this task to consume without reading the whole reference. Five corpus rules were deferred here as mechanics: K2, K3, K4, K6, K7. **Two constraints on what this check may claim:** X-10 — the banned-terminology check is necessary and not sufficient and must say so, never reporting a clean pass as "reads as human-written"; and conditions 15 and 23 are not machine-checkable, listed so they are not silently dropped. |
| 2026-08-06 | (no change) | **Seven new conditions — [`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §11 items 13–19, the resolution contract.** Renumbering note: the behavioural half is now 20–30 and the content half 31–33; the two not machine-checkable are **22 and 30**. **Condition 17 is the one to build first** — render the deck at 3840×2000 and at 1280×634 and diff up to a uniform scale factor. It is cheap and it catches the entire accidental-breakpoint class in one pass, which is the defect that produced "broken slides on my own monitor". Also new: a design-unit type floor (nothing under 18, body ≥ 24) that is measured in stage units, not rendered pixels. |
| 2026-08-06 | (no change) | **Scope is now enumerable rather than described.** [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) gives every rule a `DS-nnn` ID and a `Check` value: **this task owns the 59 `auto` rules and the 32 `render` rules**; the 36 `judge` rules belong to the evaluator. [`docs/EVALUATION.md`](../docs/EVALUATION.md) §1 fixes the contract: **`hard` rules are gates and are never scored**, so this check reports pass/fail per rule ID and never contributes to a total. §2 puts it first in the pipeline, because a judgement pass on a deck with external references is wasted. §6.3 adds a requirement this task would not otherwise have: the auto gate **re-runs on the whole deck every iteration**, since a fix routinely reintroduces what an earlier one removed. |
