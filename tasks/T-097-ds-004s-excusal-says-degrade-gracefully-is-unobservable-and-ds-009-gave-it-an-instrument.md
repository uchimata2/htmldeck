---
id: T-097
title: DS-004's excusal says degrading gracefully is unobservable, and DS-009 gave half of it an instrument
type: analysis
status: done
phase: review
parent: null
blocked_by: []
related: [T-019, T-017, T-041]
work_package: PH3
shipped_in: 0.3.0
owner: maintainer
business_value: medium
effort: s
created: 2026-08-11
updated: 2026-08-15
deliverables: [docs/DESIGN-SYSTEM.md, tools/deck/check.py]
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
- **The degradation clause is cited to DS-009, not made a checked row under DS-004** — 2026-08-15.
  DS-009 already ships the mechanism `hard`/`auto`, so a second row would be one mechanism with two
  ids and would drift the first time either moved (**L-13**). It is recorded the way DS-073 is
  *guarded by* DS-070 in `audit.py`'s `ABSENCE_IS_A_PASS` — the shape §1 named.
- **The coverage arithmetic is deliberately unchanged.** DS-004 stays deferred and unchecked, so the
  gate's split stays **84 of 115**, verified after the edit. Had the clause become a checked row the
  account would have moved, and `figures.py`'s `ACCOUNTS` binds that split across five documents —
  a ripple this task's `s` estimate never contained.
- **Both homes were reworded in the same edit**, because they are two statements of one fact and the
  failure mode is that they stop agreeing (**L-13**). The `Reach` cell keeps the ruleset's voice and
  the `DEFERRED` entry keeps the gate's; neither quotes the other.
- **The fifth criterion is answered `no`, and a task carries it.** An excusal cannot be held to its
  closing condition mechanically — `staleExcusals` fires only when a rule is excused **and** checked,
  and DS-004 was excused and not checked, so the account was silent by construction rather than
  wrong. Raised as
  [T-165](T-165-give-a-deferred-entry-a-closing-condition-a-check-can-read.md).

**Outputs produced**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-004's `Reach` cell.
- [`tools/deck/check.py`](../tools/deck/check.py) — `DEFERRED["DS-004"]`.
- [T-165](T-165-give-a-deferred-entry-a-closing-condition-a-check-can-read.md) — the task the fifth
  criterion asked for.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| DS-004's excusal names the half it excuses, and the half it no longer does | met | `DEFERRED["DS-004"]` now opens *Only the cross-engine half is unobservable* and states what T-019 changed, printed by `check.py` in the deferred list. |
| The ruleset's `Reach` cell agrees with it, in the ruleset's own words | met | Reworded in the same edit, in the ruleset's voice rather than by quoting the gate — the two are one fact with two homes, and the failure mode is that they stop agreeing (**L-13**). |
| Whether the degradation clause is checked, or cited to DS-009, is decided and written down | met | **Cited to DS-009.** One mechanism, one home; DS-009 is already `hard`/`auto`, so a second row under DS-004 would duplicate it. Recorded in the shape `audit.py` uses for *DS-073 guarded by DS-070*, which §1 named as the precedent. |
| The coverage account is unchanged in arithmetic, or its change is stated | met | **Unchanged: 84 of 115**, re-derived after the edit, and `ruleset.py --counts` still reports 115 owned, 89 hard, 4 excused. Deliberate — see §3. |
| A note on whether an excusal can be held to its own closing condition mechanically, or a task raised saying it cannot | met | **It cannot, and a task carries it**: [T-165](T-165-give-a-deferred-entry-a-closing-condition-a-check-can-read.md). `staleExcusals` fires only on a rule that is excused *and* checked; DS-004 was excused and not checked, so nothing could notice its reason half-dying when T-019 shipped DS-009. The account was silent by construction, not wrong — **L-54**. |

**Child fix tasks raised**
- [T-165](T-165-give-a-deferred-entry-a-closing-condition-a-check-can-read.md) — give a deferred entry
  a closing condition a check can read.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-15 | → done | All five criteria met. **The interesting half is the fifth**: the excusal was not wrong, it was *less true than it was*, and nothing in the account could ever have said so — which is the class T-165 now carries. The two rewordings were the cheap part and the arithmetic was deliberately left alone, since making the clause a checked row would have moved a split five documents state. |
| 2026-08-15 | → in_progress | Both homes reworded in one edit; the degradation clause cited to DS-009 rather than given a second row. |
| 2026-08-15 | → planned | §2 was already written when the task was raised on 2026-08-11 and needed no revision — the four steps survived four days and one release. Recorded as its own row because the phase was earned then, not today. |
| 2026-08-15 | → specified | §1 complete since 2026-08-12; the status was never advanced. |
| 2026-08-11 | → proposed | Raised from the closed-record sweep after `0.2.1`. The sweep was looking for commitments that escaped the board and found the mirror image: a written-down blindness that had quietly stopped being one. `medium` because nothing is broken and a gate is claiming less than it has; `s` because the work is two rewordings and one decision. `PH3` by [`../CLAUDE.md`](../CLAUDE.md)'s rule. |
