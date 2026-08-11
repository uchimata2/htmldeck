---
id: T-052
title: Settle the two hard-judge failures the checklist's first run found in the reference deck
type: fix
status: done
phase: review
parent: T-048
blocked_by: []
related: [T-024, T-028, T-040, T-044]
work_package: none
shipped_in: 0.1.0
owner: the project owner
created: 2026-08-09
updated: 2026-08-12
deliverables:
  - docs/DESIGN-SYSTEM.md
  - docs/DESIGN-RATIONALE.md
  - examples/reference-deck.html
  - examples/reference-deck-seeded-defects.html
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
| 1 | DS-036 — bind *never load-bearing* to the 16–17 band its own second sentence names | An amended rule that stops colliding with DS-026 |
| 2 | DS-208 — replace slide 10's headline with a literal claim, and its `data-name` with it | *The general fund carries this* |
| 3 | DS-107 — move `Check` from `judge` to `—`, the third recommendation the owner approved with these two | 25 hard-judge rules become 24; the bind-the-checker set becomes 5 |
| 4 | Regenerate the fixture, because the deck changed | `--check` caught the drift before anything else did |
| 5 | Re-derive every count DS-107's move changed, and correct the live prose; annotate the dated records | `judge` 43 → 42, `Check —` 6 → 7, and four documents |
| 6 | Record in `DESIGN-RATIONALE.md` why DS-036 moved and DS-208 did not | §5.7, beside the two rules that said more than they meant |
| 7 | Re-judge both rules against the deck, and look at the changed slide offline | Verdicts in §4 |

## 3. Implement

**Decisions & assumptions**
- **DS-036: the rule moved, and the legend is what settles it.** DS-026 is `hard` and requires a
  *visible legend*; the deck draws it in mono. If mono at 18 may not carry meaning, the legend
  cannot be mono, and the decoder for the colour semantics becomes typographically indistinguishable
  from what it decodes. **Two `hard` rules binding against each other is §2.1's *"a compliant deck
  could not exist"* class**, settled by the reason rather than the wording — and the reason is in
  DS-036's own second sentence, which already names **16–17** as the marginalia band. — 2026-08-09
- **DS-208: the deck moved, and that asymmetry is the point.** Here the rule's reason was intact and
  only the deck breached it. *Frequency has no ribbon* → **The general fund carries this**: five
  words, a claim, literal, and it names the sharpest of the slide's three costs without duplicating
  the bottom line. **Two `hard` rules failed together and moved in opposite directions**, which is
  what asking *which side is the reason on* produces and *which side is cheaper* would not. — 2026-08-09
- **DS-107's `Check` moved to `—`** on the same reasoning as T-048 §4 recorded: its obligation is on
  whoever builds the check, which is what DS-190, DS-191, DS-220 and DS-221 carry. It leaves the
  hard-judge checklist at 24 and adds nothing to it that reads a deck. — 2026-08-09
- **Counts were re-derived, not adjusted.** `judge` 43 → 42 and `Check —` 6 → 7 in `BRIEF.md`;
  twenty-five → twenty-four in `EVALUATION.md` §1.1 and §8.1 and `DESIGN-RATIONALE.md` §5.8. **The
  dated records were annotated rather than rewritten** — T-042's findings table, T-048's review and
  L-43 all state 25, which was true when written. — 2026-08-09

**Outputs produced**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-036 amended, DS-107's `Check` moved
- [`docs/DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) §5.7 — why DS-036 moved and DS-208 did not
- [`examples/reference-deck.html`](../examples/reference-deck.html) — slide 10's headline and `data-name`
- [`examples/reference-deck-seeded-defects.html`](../examples/reference-deck-seeded-defects.html) — regenerated
- Counts corrected in [`docs/BRIEF.md`](../docs/BRIEF.md) and
  [`docs/EVALUATION.md`](../docs/EVALUATION.md); [`docs/LESSONS.md`](../docs/LESSONS.md) tensed

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| DS-036 passes, or is amended and the amendment cites its own second sentence | **met — amended** | *"The 16–17 band is reserved for marginalia and is never load-bearing; at 18 the mono role is a label and may carry meaning."* Re-judged by measurement: **every mono run on the stage is at 18 (×127), 22 (×29) or 24 (×1) — none in the 16–17 band**, so the amended rule has no violation to find |
| DS-208 passes, or is amended with a recorded reason | **met — the deck moved** | Slide 10 reads **The general fund carries this**. Five words, a claim, no idiom; DS-091's six-word ceiling holds and `DS-135 the page title carries the slide's name: True` |
| If the rule moved, `DESIGN-RATIONALE.md` records why the deck did not | **met** | §5.7, as a third case beside DS-045 and DS-219 — and it records the asymmetry, since DS-208 went the other way in the same task |
| The mechanical gate still reports zero failures, and the seeded fixture still derives | **met** | `0 failure(s): none` · `buckets sum to 111 = owned` · `OK - … is exactly what regenerating produces (227494 bytes)`. The fixture check earned its keep: it caught the deck edit the moment it happened, `regenerating would change 4 line(s) (+2/-2)` |
| The deck is opened offline and **looked at** (**L-01**) | **met** | Re-rendered through `render.py shots`, real Chrome, DNS black-holed, all twelve slides; slide 10 examined. The headline now leads its own first row — claim above, figure beneath — which is S1's anchor 4 rather than a repetition |

**Measured while re-judging DS-036, observed and deliberately not raised.** One run of uppercase
mono sits at **24 du** — `.stat-unit`, the *"minutes, average wait"* under slide 3's big numeral —
outside DS-036's stated 16–18 range. The 22 du runs are not in scope: they are `.val`, mono
**numerals** in figures at `text-transform: none`, which is not the label role DS-036 describes. The
single 24 du case is a role the ruleset does not name, and **inventing a rule so an observation has
somewhere to live is what `DESIGN-RATIONALE.md` §5.7 warns against**. Recorded here so the next
audit finds it already weighed; one line of a task if anyone wants it chased.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-09 | → done | **Two `hard` rules failed together and moved in opposite directions, which is the result worth keeping.** DS-036's reason was in the wrong place and the deck was right: *never load-bearing* was written across the whole 16–18 range while the rule's own next sentence reserves **16–17** for marginalia, and the wide reading collided with **DS-026**, which obliges the deck to show a visible legend it draws in mono — §2.1's *"a compliant deck could not exist"* class, settled by the reason. DS-208's reason was intact and the deck was wrong, so *Frequency has no ribbon* became **The general fund carries this**; the slide lost only the joke. **Asking which side the reason is on produced opposite answers on the same afternoon**, where asking which side is cheaper would have moved the rule both times. DS-107's `Check` moved to `—` alongside them, taking the hard-judge checklist to 24. **The fixture check earned its keep within minutes of existing** — the headline edit made `seed_defects.py --check` go red immediately, `regenerating would change 4 line(s)`, which is precisely the drift that went unnoticed for four revisions before [T-044](T-044-restore-the-seeded-defect-fixture-and-its-claims.md). Re-judging DS-036 was done by **measuring every mono run on the stage** rather than by re-reading the slides: 18 ×127, 22 ×29, 24 ×1, and nothing in the band the amended rule restricts. One 24 du uppercase run is recorded in §4 as observed and not raised, because the ruleset does not name that role and inventing one so an observation has a home is the failure §5.7 exists to warn about. |
| 2026-08-09 | → planned | §1 accepted as written — it had already framed both rules with the evidence and named which was likely to move each way, and the owner approved all three recommendations together. Seven steps, with *regenerate the fixture* explicit rather than assumed, because the deck is edited here and the fixture derives from it. |
| 2026-08-09 | → proposed | Raised by [T-048](T-048-gate-the-hard-rules-only-judgement-can-reach.md), whose first run of the hard-judge checklist found them. **Both were invisible to every mechanical check in the repository, which is the argument for the checklist arriving on the day it was built.** DS-036 is the interesting one: it is not a slip but a structural tension with DS-026, which *requires* a visible legend that the deck draws in the role DS-036 forbids to carry meaning — and DS-036's own second sentence reserves only the **16–17** band for marginalia while the deck's mono is at 18, so the rule may already permit what the deck does. DS-208 is simpler and probably a deck fix: *Frequency has no ribbon* is a ribbon-cutting metaphor, DS-208 names cultural metaphors explicitly, and the slide loses nothing but the joke. |
