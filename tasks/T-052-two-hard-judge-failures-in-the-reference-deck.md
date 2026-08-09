---
id: T-052
title: Settle the two hard-judge failures the checklist's first run found in the reference deck
type: fix
status: proposed
phase: specify
parent: T-048
blocked_by: []
related: [T-024, T-028, T-040, T-044]
work_package: none
owner: the project owner
created: 2026-08-09
updated: 2026-08-09
deliverables: []
---

# T-052 — Settle the two hard-judge failures the checklist's first run found in the reference deck

## 1. Specify

**Outcome**
DS-036 and DS-208 either pass on `examples/reference-deck.html`, or the rule that fails is amended
with a recorded reason. **Which of the two moves is the work**, and it is a different answer for each.

**Why this one**
[T-048](T-048-gate-the-hard-rules-only-judgement-can-reach.md) built the hard-judge checklist and ran
it. Twenty-three of the twenty-five passed; these two did not, and **neither is visible to any
mechanical check** — which is the whole argument for the checklist existing, arriving on its first
run.

### DS-036 — *mono labels are never load-bearing*, and in this deck they routinely are

Measured in the browser: the ledger's centre column, its legend, the figure annotations and the
eyebrow are all **JetBrains Mono, 18 design units, uppercase, tracked 1.4px** — exactly the role
DS-036 governs. They are not marginalia:

| Where | The mono text | What it carries |
| :--- | :--- | :--- |
| Slide 5, ledger centre column | `CAPITAL` · `OPERATING` · `PEOPLE REACHED` · `FIRST BENEFIT` · `WEATHER-LIMITED` · `WHERE IT WINS` | The only statement of what each row compares. Cover the column and six pairs of figures mean nothing |
| Slide 5, legend | `STRONGER` · `WEAKER` · `DECIDES IT` | The only decoder for the colour semantics — and **DS-026 requires this legend to be visible** |
| Slide 4, figure annotations | `15 MINUTES NOT MOVING · 44% OF THE TRIP` · `WHERE THE WAIT COMES FROM · HEADWAY 22 MINUTES` | A **finding**, set in the marginalia role |

**The tension is structural, not a slip.** DS-026 obliges the deck to carry a visible legend and
DS-036 forbids the role it is drawn in from carrying meaning. One of the two has to give, and
deciding which is this task.

**Both answers are defensible and the reasons differ.** Amending DS-036 — *the 16–17 band is
marginalia; 18 is a label role and may carry meaning* — reads naturally against the rule's own
second sentence, which already reserves **16–17** for marginalia and says nothing about 18. Changing
the deck means moving row labels and the legend out of mono, which touches the archetype that
[T-024](T-024-build-the-reference-deck-and-validate-the-ruleset.md) validated the ruleset against.
**Read the rule's second sentence before choosing** — it may be that the rule already says what the
deck does and the "never load-bearing" clause was written for the narrower band.

### DS-208 — *no native-speaker idiom*, and slide 10's headline is one

> **Frequency has no ribbon**

A ribbon-cutting metaphor: the recommendation offers no ceremonial moment. DS-208 names *cultural
metaphors* explicitly and gives the test — **no sentence should need a second pass** — and a reader
who takes "ribbon" literally gets nothing. DS-208 also distinguishes itself from DS-097 on exactly
this point: *a reader can look a term up, and cannot look up an idiom they have misread as literal.*

**DS-207 is not in conflict**, and the interaction is worth stating because it looks like one:
DS-207 allows wit in the headline and bans it in the bottom line. The bottom line here is factual
and passes. DS-208 is not about wit — it is about idiom — so *wit is permitted, idiomatic wit is
not*, and this headline is the second.

**This one is much more likely to be a deck fix than a rule fix.** The slide's point survives a
literal headline; the metaphor is the only thing lost.

**Scope**
- In: deciding, per rule, whether the deck or the rule moves, with the reason recorded where the
  change lands.
- In: re-running the hard-judge checklist over both rules afterwards.
- In: regenerating `examples/reference-deck-seeded-defects.html` if the deck changes —
  `python tools/examples/seed_defects.py --check` will say so.
- Out: the other twenty-three rules, which passed.
- Out: widening `DESIGN-SYSTEM.md`'s mono role beyond what DS-036 already says. If the rule moves,
  it moves to what its own second sentence implies, not to whatever makes the deck pass.

**Inputs**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-036, DS-026, DS-207, DS-208
- [`examples/reference-deck.html`](../examples/reference-deck.html) — slides 4, 5 and 10
- [T-048](T-048-gate-the-hard-rules-only-judgement-can-reach.md) §4 — the run that found these

**Acceptance criteria**
- [ ] DS-036 passes, or DS-036 is amended and the amendment cites its own second sentence
- [ ] DS-208 passes, or DS-208 is amended with a recorded reason
- [ ] If the rule moved, `DESIGN-RATIONALE.md` records why the deck did not
- [ ] The mechanical gate still reports zero failures, and the seeded fixture still derives
- [ ] The deck is opened offline and **looked at** if it changed (**L-01**)

**Open questions**
- none — both are the implementer's, decided from each rule's own stated reason.

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
| 2026-08-09 | → proposed | Raised by [T-048](T-048-gate-the-hard-rules-only-judgement-can-reach.md), whose first run of the hard-judge checklist found them. **Both were invisible to every mechanical check in the repository, which is the argument for the checklist arriving on the day it was built.** DS-036 is the interesting one: it is not a slip but a structural tension with DS-026, which *requires* a visible legend that the deck draws in the role DS-036 forbids to carry meaning — and DS-036's own second sentence reserves only the **16–17** band for marginalia while the deck's mono is at 18, so the rule may already permit what the deck does. DS-208 is simpler and probably a deck fix: *Frequency has no ribbon* is a ribbon-cutting metaphor, DS-208 names cultural metaphors explicitly, and the slide loses nothing but the joke. |
