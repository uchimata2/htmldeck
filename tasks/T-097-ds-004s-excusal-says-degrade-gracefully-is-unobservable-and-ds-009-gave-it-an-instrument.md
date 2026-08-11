---
id: T-097
title: DS-004's excusal says degrading gracefully is unobservable, and DS-009 gave half of it an instrument
type: analysis
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-019, T-017, T-041]
work_package: PH3
owner: maintainer
business_value: medium
effort: s
created: 2026-08-11
updated: 2026-08-12
deliverables: []
---

# T-097 — DS-004's excusal says degrading gracefully is unobservable, and DS-009 gave half of it an instrument

## 1. Specify

**Outcome**
DS-004's excusal and its `Reach` cell say which half of the rule is unobservable, rather than the
whole clause, so the coverage account stops claiming a blindness the repository no longer has.

**Why this one**
DS-004 is *renders glitch-free in recent Chrome/Edge; other engines degrade gracefully; mobile is
secondary.* Two homes say the same thing about it, both written before 2026-08-11:

- the ruleset's `Reach` cell — *degrade gracefully is unobservable from a single-engine harness and
  is not silently dropped by being recorded here*;
- `check.py`'s `DEFERRED` — *Triage: `default`. Other engines degrade gracefully is unobservable from
  a single-engine harness, which the ruleset's own `Reach` cell already says.*

**[T-019](T-019-build-the-capability-preflight-the-deck-ships-wit.md) made the degrading part of it a
thing this repository renders and looks at.** DS-009 ships a degraded state and
`preflight.py prove` produces it on demand, four ways, with a control that must not degrade. The
banner, the flowed document and the marker are all read back out of a real browser.

**The excusal is now imprecise rather than wrong, and that is the interesting part.** What is still
unobservable is the *cross-engine* claim: no Firefox, no Safari, no mobile, exactly as
[R6](../docs/research/R6-portability-contract.md) §9 and §10 record. What is no longer unobservable
is **whether a deck that loses a capability degrades or goes blank**, which is the behaviour the
clause is actually about and the one a recipient experiences. An excusal that names the whole clause
hides a capability the gate has.

**Nothing in the account can catch this class.** `staleExcusals` fires when a rule is excused **and**
checked; DS-004 is excused and not checked, so the partition is intact and the excusal is simply less
true than it was. That is a second reason to do it by hand and a candidate reason to raise something
wider.

**Scope**
- In: rewording the `DEFERRED` entry and the `Reach` cell so each names the half it means.
- In: deciding whether the degradation behaviour becomes a **checked** row under DS-004, or stays
  DS-009's and is cited from DS-004 — one rule's mechanism satisfying another's clause is a shape
  this ruleset has (DS-073 guarded by DS-070) and it should be recorded the same way.
- In: whether the account should be able to notice an excusal that has gone stale **without** the
  rule becoming checked. It cannot today, and this is the instance that shows why.
- Out: testing Firefox, Safari or mobile. That is not this task and would not be `s`.
- Out: R6 §8's nine glitch-free conditions, which are
  [T-041](T-041-implement-the-nine-glitch-free-conditions.md)'s.

**Inputs**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) DS-004's row, and DS-009's.
- [`tools/deck/check.py`](../tools/deck/check.py) — `DEFERRED["DS-004"]`, and `account`, which cannot
  see this.
- [`docs/research/R6-portability-contract.md`](../docs/research/R6-portability-contract.md) §9, §10 —
  what is genuinely not evidence about another engine.

**Acceptance criteria**
- [ ] DS-004's excusal names the half it excuses, and the half it no longer does
- [ ] The ruleset's `Reach` cell agrees with it, in the ruleset's own words
- [ ] Whether the degradation clause is checked, or cited to DS-009, is decided and written down
- [ ] The coverage account is unchanged in arithmetic, or its change is stated
- [ ] A note on whether an excusal can be held to its own closing condition mechanically, or a task
      raised saying it cannot

**Open questions**
- Should every `DEFERRED` entry carry its **CLOSES WHEN** as a field a check can read, rather than as
  a sentence at the end of the reason? *Recommend yes, in a later task: most entries already end with
  one, and a machine-readable form is what would let the account notice this class rather than a
  person sweeping the record after a release.*

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | State the two halves separately and check each against what the repository can now render | the split |
| 2 | Decide checked-here or cited-to-DS-009, in the shape DS-073/DS-070 already uses | the decision |
| 3 | Reword the `DEFERRED` entry and the `Reach` cell together | `check.py`, `DESIGN-SYSTEM.md` |
| 4 | Say what the account can and cannot notice about a stale excusal, and raise what follows | a note or a task |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <none yet>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-11 | → proposed | Raised from the closed-record sweep after `0.2.1`. The sweep was looking for commitments that escaped the board and found the mirror image: a written-down blindness that had quietly stopped being one. `medium` because nothing is broken and a gate is claiming less than it has; `s` because the work is two rewordings and one decision. `PH3` by [`../CLAUDE.md`](../CLAUDE.md)'s rule. |
