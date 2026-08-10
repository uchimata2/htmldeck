---
id: T-082
title: The worked example's figure ledger omits figures that reach slides, so the ledger cannot be the authority it is treated as
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-071]
work_package: v0.2
owner: the project owner
business_value: medium
effort: s
created: 2026-08-10
updated: 2026-08-10
deliverables: []
---

# T-082 — The worked example's figure ledger omits figures that reach slides, so the ledger cannot be the authority it is treated as

## 1. Specify

**Outcome**
[`examples/sort-window/sort-window.foundation.md`](../examples/sort-window/sort-window.foundation.md)'s
figure ledger holds **every** figure that reaches a slide, so the rule it is quoted under — the
ledger is authoritative where it and a slide disagree — is a rule about a complete record rather than
a partial one.

**Why this one**
Found 2026-08-10 while assigning per-slide sources in
[T-071](T-071-the-intermediate-specifications-carry-their-references.md). Three figures appear in the
slide specification and have no ledger row, and all three are in the source documents, so none is
fabricated — the ledger is incomplete, not wrong:

| Figure | Where it ships | Where it comes from |
| :--- | :--- | :--- |
| 31,900 peak volume | slide 10's disclosure, as the condition that breaks the recommendation | the throughput model's busiest single day |
| $140k slot premium | slide 9's disclosure, as half of the cost build-up | the fleet and cost model |
| $170k six-person crew | slide 9's disclosure, the other half | the fleet and cost model |

Two more were found the same way and **fixed in T-071**, because that task's new check reads the
`Used on` column and could not be calibrated against cells known to be wrong: `Sort rate` and
`Proposed second cut-off` both omitted slide 10, which cites each of them.

**Why this matters more than three missing rows.** DS-102 is a `hard` rule and the ledger is how this
project discharges it for an illustrative deck. T-071 then made the ledger **authoritative** in a
check: where a slide's declared sources and the ledger disagree, the slide is corrected. A record that
wins arguments has to be complete, or the checks built on it are calibrated against a subset and quietly
agree with whatever is missing.

**The pattern behind all five is one thing: a figure behind a disclosure.** Every omission is in tier
two — a derivation panel or a condition panel. Tier one was ledgered carefully; the click was not. That
is a rule about where to look, not an accident, and it is the part worth carrying beyond this task.

**Scope**
- In: the three missing rows, with `Origin` and `Used on` filled from the source documents.
- In: a sweep of the remaining ten disclosure panels for the same omission, since three of the five
  found so far came from one place.
- In: whether anything should **check** this. The content half of
  [`check.py`](../tools/deck/check.py) reconciles the deck against `sources/`; whether it also
  reconciles the deck against the *ledger* is the open question, and the answer decides whether this
  recurs.
- Out: the reference deck, which is a different deck with a different ledger. Check it separately if
  the sweep here finds a pattern.
- Out: DS-102's wording, which is correct as it stands.

**Inputs**
- [`examples/sort-window/sort-window.foundation.md`](../examples/sort-window/sort-window.foundation.md)
  — the ledger, and the two `Used on` cells T-071 corrected.
- [`examples/sort-window/sort-window.slides.md`](../examples/sort-window/sort-window.slides.md) — every
  figure that ships, tier one and tier two.
- `examples/sort-window/sources/` — the three source documents all five figures were traced to.

**Acceptance criteria**
- [ ] The three rows exist, with an origin traced to a source document and a correct `Used on`
- [ ] The other ten disclosure panels have been swept, and what the sweep found is recorded — including
      "nothing", which is a result
- [ ] Whether ledger completeness gets a check is decided, with the reason
- [ ] `python tools/deck/spec.py` on the pair stays green, and its SPEC-4 row is now calibrated against
      a complete ledger

**Open questions**
- none

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
- <T-NNN or "none">

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-10 | → proposed | Raised from [T-071](T-071-the-intermediate-specifications-carry-their-references.md), which needed the `Used on` column to be right before it could check anything against it and found five cells that were not. Two were corrected there because the new check read them; three are additions and are this task's. `medium` because nothing shipped is a fabricated figure — every one traces to a source — but a ledger that wins disagreements has to be complete to deserve that; `s` because the sweep is ten panels and the rows are three. `v0.2`: a minor fix to a worked example. |
