---
id: T-274
title: Build the card reveal, so DS-140's Turn is a component rather than two dials
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-242, T-275]
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-08-29
updated: 2026-08-29
deliverables: []
---

# T-274 — Build the card reveal, so DS-140's Turn is a component rather than two dials

## 1. Specify

**Outcome**
`--turn-dur` and `--turn-ease` have a reader. DS-140 names four motions as a starter set — *what a
deck gets without designing anything* — and Turn, a card reveal, is the one no deck has ever built:
both themes declare its two dials, all five tracked decks carry them, and `var(--turn-dur)` appears
nowhere in the tree. [`COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) §5 sends an author
wanting an overshoot on a card reveal to `--turn-ease`, which today changes nothing.

**Closes** `PR-36`'s Turn half in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) §3.
`PR-36`'s other half — `--scale-ease`'s cell naming a reader that left — was fixed by
[T-242](T-242-the-contracts-against-the-checkers-that-decide-them.md) on 2026-08-29.

**Ruled by the owner, 2026-08-29.** The question was *build the component, or retire the two tokens
and let DS-140's set lose a name*, put with retirement recommended as the cheaper answer. **The owner
chose to build it**, which makes the starter set true rather than shorter.

**Scope**
- In: the component — a card reveal in `shell/components.css`, its keyframes, and the rows it owes
  in [`COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) §3.8 and its parts table
- In: what every content motion owes: `--motion-kind`, a `--m-rank` under DS-239, the reduced-motion
  and preflight collapses, and DS-141's cap without a licence
- In: a deck that uses it, or the reveal is unfalsifiable in the same way the tokens were
- Out: **DS-140's set.** Its four names are unchanged; this makes the fourth one real
- Out: the deck rebuild. Adding to the shared block invalidates all five tracked decks, and
  [`REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) rebuilds them once, in **B12**

**Inputs**
- `PR-36` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) §3
- [`docs/THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) §3.6 — the two dials and their bands
- [T-198](T-198-give-affordance-motion-its-own-band-faster-than-content-motion.md), which moved three
  rules **off** Turn's pair in 2026-08-20 and is why nothing reads it now
- `component.unrowed_motions`, added by [T-242](T-242-the-contracts-against-the-checkers-that-decide-them.md):
  a new rule animating on a token fails the gate until it has a row, so the row is not optional

**Acceptance criteria**
- [ ] `var(--turn-dur)` and `var(--turn-ease)` are read by a component in the shared block
- [ ] the component has its rows, and `component.py check` is green on every tracked deck
- [ ] the reveal is visible in a deck, and the look it owes is queued in
      [`docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md)
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- **Which deck carries the first card reveal, and on which slide.** Answerable by whoever builds it;
  it is a composition decision, not a rule question.

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
| 2026-08-29 | → proposed | Raised after the owner ruled `PR-36`'s open half on 2026-08-29, having had it deferred by [T-242](T-242-the-contracts-against-the-checkers-that-decide-them.md) that day as a `DS-000` question a batch's authority did not cover. **The recommendation was to retire and the owner chose to build**, so the starter set keeps its fourth name and gains a body. `PH3`: not a defect in the published plugin. |
