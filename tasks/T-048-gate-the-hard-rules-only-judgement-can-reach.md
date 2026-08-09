---
id: T-048
title: Gate the twenty-five hard rules only a judgement pass can reach
type: deliverable
status: proposed
phase: specify
parent: T-042
blocked_by: []
related: [T-004, T-005, T-023, T-026, T-027, T-037]
work_package: WP2
owner: the project owner
created: 2026-08-09
updated: 2026-08-09
deliverables:
  - docs/EVALUATION.md
  - docs/DESIGN-RATIONALE.md
---

# T-048 — Gate the twenty-five hard rules only a judgement pass can reach

## 1. Specify

**Outcome**
`EVALUATION.md` names who emits a pass/fail for every `hard` rule whose `Check` is `judge`, and a
rule that has neither a verdict nor a written excusal is a failed run — the same device
[T-005](T-005-build-check-the-gate-the-deck-must-pass.md) built for the mechanical half, at the
judgement layer where it does not yet exist.

**Why this one**
`EVALUATION.md` §1 is unambiguous. `hard` rules are **gates**, the result is *"pass / fail, per rule
ID"*, and the gate covers **114 `hard`** rules. §2's pipeline then assigns stage 1 to the 66 `auto`
rules and stage 2 to the 45 `render` rules. Derived from the ruleset:

```
hard = 114    auto|render 85    judge 25    Check '—' 4 (they bind the checker, not the deck)
```

**25 `hard` rules are `judge`, and nothing in the pipeline produces a pass/fail for any of them.**
Stages 3 and 4 produce 0–4 dimension scores, and §1 says in the same breath that `hard` rules are
**never scored** — so those 25 are declared gates and excluded from the only machinery that touches
them. Fourteen are at least reachable through a dimension's cited rule list. **Eleven are named
nowhere in `EVALUATION.md` at all:**

```
DS-021  the accent carries meaning wherever it appears
DS-093  never justify a statement with sentences
DS-097  the reader is bright and new to the field
DS-099  respectful, positive, professional
DS-107  the word-list check is necessary and not sufficient, and must say so
DS-112  never hand-draw icons
DS-137  two simultaneous interactions need a defined precedence rule
DS-201  every slide delivers exactly one thing
DS-204  never bury the deliverable in a list, a paragraph or a table cell
DS-207  the deliverable is stated factually and directly
DS-208  no native-speaker idiom
```

DS-136 is a twelfth in substance: it appears only in a §6.3 aside about regression sweeps, never as
a gate or a dimension.

**This is L-41 one layer up.** *A check with no rule is as wrong as a rule with no check, and much
harder to see.* T-005 closed the mechanical half by making a silent rule a red run the same
afternoon. The judgement half has no counterpart — a `hard` `judge` rule can be added and nothing
anywhere notices it is unowned, which is how eleven accumulated. **Four of them are §3.4's
deliverable contract**, the section `DESIGN-RATIONALE.md` §3 records as the one the owner named
after reading the reference deck, and the reason the publishing gate and
[T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) exist.

**Scope**
- In: the hard-judge gate — where it runs, what it emits, and what makes a run fail.
- In: deriving its jurisdiction from the ruleset at run time, never a list in the document
  (**L-08**). `ruleset.py` already computes it.
- In: reconciling §1's *"never scored"* with the dimension anchors that cite `hard` rules, so a rule
  is not both gated and scored without the document saying which is which.
- In: §5's threshold condition 1, *"Zero `hard` violations"*, saying that it spans both gates.
- Out: new rules, amended rules, and re-labelling any rule from `hard` to `default` to make this
  smaller. **If a rule turns out not to deserve `hard`, that is a ruleset finding to raise, not a
  shortcut to take inside this task.**
- Out: `check.py`. Nothing here is mechanical; the gate reads a deck and answers.
- Out: the critique report's format, which is
  [T-004](T-004-critique-mode-blunt-section-by-section-review.md)'s. This decides what it must
  carry, not how it prints.

**Inputs**
- [`docs/EVALUATION.md`](../docs/EVALUATION.md) §1, §2, §5, §8.1
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — the `Label` and `Check` columns
- [`tools/deck/ruleset.py`](../tools/deck/ruleset.py) — the derivation
- [`docs/LESSONS.md`](../docs/LESSONS.md) — **L-08**, **L-36**, **L-41**
- [T-042](T-042-audit-the-whole-repository-against-itself.md) §2, F-3

**Acceptance criteria**
- [ ] Every `hard` rule with `Check: judge` has a named owner in `EVALUATION.md`, derived from the
      ruleset rather than listed
- [ ] A rule in neither *pass*, *fail* nor *excused in writing* fails the run, stated as a rule
- [ ] §1's *"never scored"* and the dimension anchors that cite `hard` rules no longer contradict
      each other
- [ ] The pass count in §8.1 is unchanged, or the increase is stated and accepted
- [ ] Run once against `examples/reference-deck.html`, and the verdicts recorded — a gate that has
      never been applied is a gate nobody has tested (**L-04**, **L-24**)
- [ ] Run once against `examples/reference-deck-seeded-defects.html` and shown to **fail** on at
      least one seeded defect the mechanical gate misses
- [ ] `DESIGN-RATIONALE.md` records why the 25 are gated by judgement rather than demoted
- [ ] The generic form is promoted to [`docs/LESSONS.md`](../docs/LESSONS.md) — **a completeness
      device built for one class makes the classes it does not cover harder to see, not easier**,
      because the green run now covers for them. It is deliberately **not** written before this task
      lands: a lesson has to state how to act, and what to do about an unowned `hard` rule is exactly
      what this task decides

**Open questions**
- ~~Do the 25 get a pass/fail checklist, or does §1 stop calling them gates?~~ **Answered 2026-08-09
  from §1's own stated reason.** §1 justifies *hard rules are never scored* with one sentence:
  *"averaging a hard failure into a score is how a deck ships with a wrong number on the title slide
  and an 84%."* That reason is about **dilution by arithmetic** and says nothing about who observes
  the failure — so it does not license leaving the rule unobserved. **The 25 keep gate status and
  gain a pass/fail checklist**, run inside the existing fresh-context pass (§8.1) before it scores
  anything, emitting rule IDs rather than numbers. The alternative — dropping *gate* and letting the
  dimensions carry them — silently demotes DS-201, DS-204, DS-207 and DS-208 from **defect** to *a
  point off a score*, which is the dilution §1's reason forbids, applied to the four rules the
  release gate exists for. **Cost: 25 yes/no judgements inside a pass that already reads the whole
  deck, so §8.1's "2 passes per measurement round" is unchanged** — that is what makes the answer
  affordable and is the reason it beats a separate pass.
- **Does the checklist run per slide or once per deck?** Nine of the 25 are per-slide claims
  (DS-201, DS-204, DS-207, DS-208, DS-093, DS-097) and the rest are deck-wide (DS-021, DS-112,
  DS-114). §8.1's *"why one pass and not twelve"* argument probably settles it the same way it
  settled S1/S2/S4 — whoever plans this should check that it does rather than assume it.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

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
| 2026-08-09 | → proposed | Raised by [T-042](T-042-audit-the-whole-repository-against-itself.md), finding F-3, and the only one of the audit's twenty-one that needed a ruling rather than an edit. **`EVALUATION.md` §1 declares 114 `hard` rules to be gates; 85 are `auto` or `render` and are gated, 4 bind the checker rather than the deck, and the remaining 25 are `judge` and are gated by nothing** — eleven of them are not mentioned in the document at all, four being §3.4's deliverable contract. The question is answered in §1 above from §1-of-EVALUATION's own reason: the ban on scoring `hard` rules is about dilution by arithmetic, not about leaving them unobserved, so they keep gate status and gain a pass/fail checklist inside the fresh-context pass at no extra pass cost. Ordered last among the audit's children because it may change `EVALUATION.md`'s structure and everything else is an edit. |
