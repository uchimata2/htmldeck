---
id: T-048
title: Gate the twenty-five hard rules only a judgement pass can reach
type: deliverable
status: done
phase: review
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
  - docs/LESSONS.md
  - tools/deck/ruleset.py
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
- ~~**Does the checklist run per slide or once per deck?**~~ **Answered 2026-08-09, and §8.1's
  argument does carry — it was checked rather than assumed.** §8.1 scores S1, S2 and S4 in one read
  of the whole deck because *"a first-time reader needs this"* and *"one side argued and the other
  not"* are judgements about the deck a reader actually meets, which a slide read in isolation
  cannot make. **Every per-slide rule in this set has the same shape.** DS-201's *exactly one thing*
  is only decidable against what the neighbouring slides deliver; DS-208's *no sentence should need
  a second pass* is a claim about a reader moving through the deck; DS-204's *buried* means buried
  relative to what else is on offer. So: **one pass over the whole deck, and a rule whose subject is
  a slide names the slide in its verdict.** Confirmed by the run — DS-036's failure is only visible
  as a pattern across slides 4 and 5, and one slide alone reads as a local choice.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Derive the jurisdiction in `ruleset.py --gates`, and **assert that every `hard` rule has exactly one gate** | The arithmetic that would have caught F-3 on day one, and a partition self-test |
| 2 | Write `EVALUATION.md` §1.1 — the two halves, where the checklist runs, what it emits, what fails a run | A gate described, with its membership derived rather than listed |
| 3 | Settle the *never scored* contradiction in §1 by saying what a cited `hard` rule in a dimension list is for | Context for the anchor, not a scoring input |
| 4 | Extend §5 condition 1 to both halves, and §8.1 to say the checklist costs no extra pass | A threshold that means what it says |
| 5 | **Run the checklist against `examples/reference-deck.html`** — 25 verdicts, evidence each | §4, and two failures |
| 6 | **Run it against the seeded fixture** and check it catches defects the mechanical gate misses | Seven failures across five dimensions, four of them mechanically invisible |
| 7 | Record in `DESIGN-RATIONALE.md` §5.8 why the 25 are gated rather than demoted | The argument, where the reasons live |
| 8 | Promote the generic form to `LESSONS.md` **after** the shape was known, not before | **L-43** |

## 3. Implement

**Decisions & assumptions**
- **The checklist's membership is derived and the document never lists it.** `ruleset.py --gates`
  partitions all 114 `hard` rules across their gates, and `self_test()` exits when the parts do not
  sum. **That assertion is the real deliverable** — F-3 existed because no arithmetic covered `hard`
  at all, so twenty-five rules could be declared gates with nothing gating them and no run would
  disagree. A list in `EVALUATION.md` would have drifted the same way (**L-08**). — 2026-08-09
- **One pass over the whole deck, not one per slide** — the second open question, answered by
  checking §8.1's argument rather than assuming it carries. It does, and the run confirmed it:
  DS-036's failure is a *pattern* across slides 4 and 5, and either slide alone reads as a local
  choice. — 2026-08-09
- **An excusal is about the instrument, never about the rule.** *"No deck here has an appendix"* is
  a reason; *"hard to judge"* is not, because a `hard` rule nobody can judge has the wrong label and
  that is a ruleset finding. Written into §1.1 because it is the seam where a pass/fail checklist
  degrades into a formality. — 2026-08-09
- **L-43 was written after the run, not before it.** Criterion 8 asks for the generic form and says
  in terms not to write it early: the lesson has to say what to *do* about an unowned `hard` rule,
  and that is what this task decided. What it says is sharper than the pre-run guess — the danger is
  not the omission but **the reassurance**, since a green run stops the question being asked again.
  — 2026-08-09

**Outputs produced**
- [`docs/EVALUATION.md`](../docs/EVALUATION.md) — §1.1, the *never scored* reconciliation in §1,
  §5 condition 1, and the cost note in §8.1
- [`docs/DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) §5.8 — gated, not demoted
- [`docs/LESSONS.md`](../docs/LESSONS.md) — **L-43**
- [`tools/deck/ruleset.py`](../tools/deck/ruleset.py) — `gates()`, `--gates`, and the partition
  assertion in `self_test()`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every `hard` `judge` rule has a named owner in `EVALUATION.md`, derived rather than listed | **met** | §1.1 names the hard-judge checklist as the owner and points at `ruleset.py --gates` for membership. `114 = hard, so every hard rule has an owner`, and `self_test()` exits if the three gates stop summing to 114 |
| A rule in neither *pass*, *fail* nor *excused in writing* fails the run, stated as a rule | **met** | §1.1: *"A rule in none of those three states fails the run"*, plus the clause that separates an instrument excusal from a rule nobody can judge — the second being a ruleset finding, not a skipped row |
| §1's *"never scored"* and the dimension anchors that cite `hard` rules no longer contradict | **met** | §1 now says a `hard` rule cited in a dimension list is **context for the anchor, not a scoring input**, and its verdict comes from a gate |
| The pass count in §8.1 is unchanged, or the increase is stated and accepted | **met, unchanged** | The checklist runs inside the existing fresh-context pass, before scoring. §8.1 says so and gives the reason a separate pass was rejected |
| Run once against `examples/reference-deck.html`, verdicts recorded (**L-04**, **L-24**) | **met — and it failed twice** | 25 verdicts below. **23 pass, 2 fail**: DS-036 and DS-208, neither reachable by any check in this repository. Raised as [T-052](T-052-two-hard-judge-failures-in-the-reference-deck.md) |
| Run once against the seeded fixture and shown to **fail** on at least one seeded defect the mechanical gate misses | **met** | **Seven failures across five dimensions**, four of them mechanically invisible. DS-116's text names the S3 seed almost verbatim — *"Four boxes joined by arrow glyphs is not a flow diagram"* |
| `DESIGN-RATIONALE.md` records why the 25 are gated by judgement rather than demoted | **met** | §5.8, including the part that decided it: demoting DS-201/204/207/208 into the dimensions converts them from defect to a point off a score, and those four are why the release gate exists |
| The generic form promoted to `LESSONS.md` | **met** | **L-43** — *a completeness device built for one class makes the classes it does not cover harder to see*. Written after the run, as criterion 8 required |

### The run — `examples/reference-deck.html`

One pass, whole deck, before any scoring. **23 pass · 2 fail · 0 unowned.**

| Rule | Verdict | Evidence |
| :--- | :---: | :--- |
| DS-021 | pass | The accent marks the current tick, the Centre interchange, the timed connection, the disclosure `+` and the bottom-line rule — the thing being pointed at in every case. No decorative use |
| **DS-036** | **fail** | Mono at **18 du, uppercase, tracked 1.4px** carries the ledger's row labels, its legend, and slide 4's `15 MINUTES NOT MOVING · 44% OF THE TRIP` — a finding in the marginalia role. Measured in the browser, not read off the CSS |
| DS-084 | pass | Every slide folds derivation and exclusions into a panel; nothing is cut to fit |
| DS-085 | pass | Slide 12 is an ask, not a recap: *Approve the frequency package*, one dated action |
| DS-090 | pass | Twelve headlines, twelve claims — *Eleven minutes decides this*, *Frequency compounds, bikes plateau* |
| DS-093 | pass | Detail is carried by the ledger, the small multiples, the timeline and the network diagram. Standfirsts are one sentence of setup |
| DS-097 | pass | *Headway* is the only term of art and the deck defines it in place — a panel titled *Why the wait is half the headway* and a diagram labelled `22 MINUTES APART`. `Trunk route` is the closest call and resolves from context |
| DS-099 | pass | Slide 10 states three costs against its own recommendation without disparaging the alternative |
| DS-102 | pass | Every figure derives from assumptions printed on the slide; `[est.]` survives on the 94-days figure |
| DS-107 | pass | `check.py`'s closing paragraph says it in terms. **Note: this rule's subject is the instrument, not the deck** — see below |
| DS-112 | pass | Nine Lucide symbols in a sprite. The seven SVGs are diagrams, not icons |
| DS-114 | pass | Bike = bike-share, bus = frequency, warning = cost, calendar-clock = the deadline. No icon carries two ideas |
| DS-116 | pass | Slide 9 branches where the process branches, at the month-18 gate |
| DS-121 | pass | Position and length throughout; no area, no hue for magnitude, no second y-axis |
| DS-123 | pass | One icon-led list on slide 10 and no card grid, stat strip or pill row |
| DS-136 | pass | One disclosure component, one ruler, one control set, reused on every slide |
| DS-137 | pass | The ruler owns the arrows while a tick holds focus, stated in **both** handlers so it does not depend on listener order; DS-228 gives the disclosure pair its rule |
| DS-150 | pass | Two motions: staggered entry encoding reading order, and the dashed flow encoding direction |
| DS-161 | pass | Every bottom line sits outside the panel; closed, each slide still delivers |
| DS-162 | pass | Panels carry derivations and exclusions. The argument survives without any of them |
| DS-167 | pass | Ruler, prev/next, Read and Motion are visible throughout and none is needed to follow the argument |
| DS-201 | pass | One bottom line per slide, one sentence each |
| DS-204 | pass | The deliverable is never in a list, a paragraph or a cell — it has its own slot at the foot |
| DS-207 | pass | Twelve factual bottom lines. Slide 10's metaphor is in the headline, which DS-207 permits |
| **DS-208** | **fail** | Slide 10's headline **Frequency has no ribbon** is a ribbon-cutting metaphor. DS-208 names cultural metaphors and gives the test — *no sentence should need a second pass* |

**One thing the run found about the ruleset rather than the deck.** **DS-107's subject is the
checker, not the deck** — *the word-list check must say it is not sufficient* is an obligation on
whoever writes the check, which is exactly what `Check: —` means and what DS-190, DS-191, DS-220 and
DS-221 carry. It is `judge`, so it lands in a checklist that reads decks. Not corrected here: scope
puts re-labelling out, and a `Check` value is a ruleset edit. Recorded so it is not re-derived.

### The run — `examples/reference-deck-seeded-defects.html`

**Seven failures, across five of the ten dimensions**, and the mechanical gate sees three of the
ten. This is the criterion that tests whether the checklist is worth its cost.

| Rule | Seed | Mechanically visible? |
| :--- | :--- | :--- |
| DS-090 | **S1** — the headline becomes *Wait times*, a topic label | no |
| DS-102 | **S2** — a modelled curve restated as *observed across comparable cities*, assumption marker deleted | no |
| DS-116 | **S3** — the network diagram becomes four cards joined by arrow glyphs | only as collateral, via DS-075's reflow overflow |
| DS-123 | **S3** — the same card row, against *"boxes everywhere" is the rejected pattern* | as above |
| DS-161 | **S4** — the deciding sentence moves into tier two; closed, the slide no longer makes its point | no |
| DS-204 | **S4** — the deliverable ends up inside a panel row | no |
| DS-085 | **D3** — the close becomes *Thank you* and a recap | **no** — and the mechanical gate passes it, because DS-203 and DS-205 ask only that a bottom line exists and is not hidden |

**DS-116's rule text names the seeded defect almost verbatim** — *"Four boxes joined by arrow glyphs
is not a flow diagram"* — which is the strongest evidence available that the checklist reads the
rules rather than the deck's reputation.

**Two seeded defects the checklist does not catch either, stated because a gate's blind spots are
its own to declare.** **D1** (slides reordered so the spine stops retiring objections) and **D4**
(the reserve restated as $2.2M against the ledger's $1.5M) have no `hard` `judge` rule between them
— D1 is carried by A-01, A-02 and DS-134, D4 by DS-114 and DS-135, and none of those five is
`hard`+`judge`. **Both remain scored dimensions and neither is gated by anything.** That is correct
rather than a gap — they are quality judgements, not defects with rule IDs — but it means *zero
`hard` violations* still does not mean *no known defect*, and §5's three conditions are three for
that reason.

**Child fix tasks raised**
- [T-052](T-052-two-hard-judge-failures-in-the-reference-deck.md) — DS-036 and DS-208 on the
  reference deck

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-09 | → done | **The checklist failed the reference deck on its first run, which is the result that justifies it.** Twenty-three of twenty-five passed; **DS-036 and DS-208 did not**, and neither is reachable by any check in this repository — the deck had been green through every gate since [T-040](T-040-fix-the-three-reference-deck-defects-the-new-gate-found.md). DS-036 is the substantial one and it is **structural rather than a slip**: mono at 18 du carries the ledger's row labels, its legend — which DS-026 *obliges* the deck to show — and a finding on slide 4 (`44% OF THE TRIP`), so a `hard` rule forbidding that role to carry meaning collides with another `hard` rule requiring it to. [T-052](T-052-two-hard-judge-failures-in-the-reference-deck.md) settles which moves; DS-036's own second sentence reserves only the 16–17 band for marginalia, so the rule may already permit what the deck does. **Against the seeded fixture it caught seven rules across five dimensions**, six of them mechanically invisible, and DS-116's text names the S3 seed almost verbatim. **The real deliverable is not the checklist but the arithmetic under it**: `ruleset.py --gates` partitions all 114 `hard` rules across their gates and `self_test()` exits when the parts stop summing — F-3 existed because *nothing counted `hard` at all*, so twenty-five rules could be declared gates with nothing gating them and every run would agree. **Both open questions were answered from the documents' own reasons rather than by preference.** §1's ban on scoring `hard` rules is about dilution by arithmetic and therefore forbids scoring them without permitting ignoring them — demoting DS-201, DS-204, DS-207 and DS-208 into the dimensions would convert the four rules the release gate exists for from *defect* into *a point off a score*. And §8.1's one-pass argument was **checked rather than assumed**, then confirmed by the run: DS-036's failure is a pattern across two slides and either slide alone reads as a local choice. **L-43 came out sharper for having been written afterwards** — the danger in a partial completeness device is not the omission but the reassurance, because a green run stops anyone asking the question again. |
| 2026-08-09 | → planned | §1 accepted with its first open question already answered; the second — per slide or once per deck — was left open on purpose and is answered above by checking §8.1's argument against these twenty-five rules rather than assuming it transfers. Eight steps, ordered so the derived jurisdiction and its partition assertion come **first**: the document describes a gate whose membership it must never carry, so the tool has to be able to produce it before the prose can point at it. |
| 2026-08-09 | → proposed | Raised by [T-042](T-042-audit-the-whole-repository-against-itself.md), finding F-3, and the only one of the audit's twenty-one that needed a ruling rather than an edit. **`EVALUATION.md` §1 declares 114 `hard` rules to be gates; 85 are `auto` or `render` and are gated, 4 bind the checker rather than the deck, and the remaining 25 are `judge` and are gated by nothing** — eleven of them are not mentioned in the document at all, four being §3.4's deliverable contract. The question is answered in §1 above from §1-of-EVALUATION's own reason: the ban on scoring `hard` rules is about dilution by arithmetic, not about leaving them unobserved, so they keep gate status and gain a pass/fail checklist inside the fresh-context pass at no extra pass cost. Ordered last among the audit's children because it may change `EVALUATION.md`'s structure and everything else is an edit. |
