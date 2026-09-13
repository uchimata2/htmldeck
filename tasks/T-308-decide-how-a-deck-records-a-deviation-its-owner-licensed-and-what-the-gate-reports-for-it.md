---
id: T-308
title: Decide how a deck records a deviation its owner licensed, and what the gate reports for it
type: decision
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-299, T-225, T-264, T-265]
work_package: PH3
owner: the project owner
business_value: high
effort: m
created: 2026-09-13
updated: 2026-09-13
deliverables: []
---

# T-308 — Decide how a deck records a deviation its owner licensed, and what the gate reports for it

## 1. Specify

**Outcome**
A deck whose owner licensed a departure from a rule can say so in the deck, and `check.py` reports
that failure as licensed instead of red on every run. Today there is one per-deck licence, `DS-141`'s
theme token from [T-264](T-264-ds-141s-request-licence-has-nowhere-to-put-its-number.md), and only
that rule reads it. `check.py`'s excusal mechanism excuses a **rule** from automated checking for the
whole project, not a **deck** from one rule.

**Two adopters have met this, and one of them built a wrapper for it.** ClaimAI's four
permanently-failing rules led [T-225](T-225-triage-the-claimai-adopter-report.md) to rule that a deck
of that shape should fail at most one rule, *by an explicit decision rather than by exhaustion*, and
there is still no place to record the decision. Nextep ended with three owner-ruled failures,
`DS-110`, `DS-100` and `DS-005`, red on every run and held by a forty-line wrapper.

**From the adopter report** [`17`](../docs/adopter-reports/nextep/2026-09-08-the-gate-has-no-route-for-a-deviation-the-owner-licensed.md).

**Not a defect, and why that matters for the scope.** The three rules fire correctly on that deck, so
the gate does what it says. What is missing is vocabulary. That also separates `17` from ClaimAI's
`023`, which was a rule firing outside its scope and was answered by narrowing `DS-100`.

**Scope**
- In: where a licence lives — in the deck, beside its specification, or both
- In: what a licence must carry — the rule, the reason, who licensed it, and when
- In: what the gate prints and exits with for a licensed failure, an unlicensed one, and a licence
  whose rule now passes
- In: whether some rules may never be licensed
- In: if the decision is to build it, the mechanism, proved on a seeded deck
- Out: the individual rule changes [T-265](T-265-ds-110-cannot-tell-a-rasterised-diagram-from-a-drawing.md)
  and T-270 carry

**Inputs**
- the record above, and its forty-line wrapper as the shape an adopter reached for unaided
- `DS-141`'s licence token, the one precedent in this tree

**Acceptance criteria**
- [ ] the decision is recorded here with the rejected alternatives and their reasons
- [ ] if the decision is to build: a seeded deck licensing one rule shows the gate reporting it licensed,
      and the same deck with the licence removed shows it failing (**L-125**)
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- Whether a deck may license a `hard` rule at all — the project owner. Recommended: yes, with the rule,
  the reason and the date required in the deck and printed on every run. An author who can never reach
  zero stops reading the gate, which is T-225's ruling, and a licence the gate prints stays visible
  where a wrapper hides it.
  **Answered by the owner 2026-09-13: yes, as recommended.**

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- `deliverables/...`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- <T-NNN or "none">

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-13 | -> proposed | Raised by T-299 from Nextep record `17`. `PH3` and `decision`: the rules fire correctly, so no published behaviour is wrong, and the open question is the owner's. |
| 2026-09-13 | (no change) | The owner answered the open question: a deck may license a `hard` rule, with the rule, the reason and the date stated in the deck and printed on every run. Still `proposed`. |
