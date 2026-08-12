---
id: T-115
title: A specification can assert a layout the shell cannot honour, and nothing reads the two together
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-109, T-114]
work_package: PH3
owner: the project owner
business_value: medium
effort: l
created: 2026-08-12
updated: 2026-08-12
deliverables:
  - skills/htmldeck/references/critique.md
  - docs/DESIGN-SYSTEM.md
---

# T-115 — A specification can assert a layout the shell cannot honour, and nothing reads the two together

## 1. Specify

**Outcome**
The critique pass reads the deck **and its specification** and reports where the deck does not do
what the specification says it does. Today it reads only the deck, so a specification is free to
describe a deck that was never built and nothing in the pipeline disagrees.

**The instance that found it**
Slide 1 of the first deck built on published `0.2.2`. Its specification says the bottom line sits

> *below both, spanning the full width, so the reader's eye lands on the join rather than on either
> column.*

It does not span the full width and it cannot. [`shell/components.css`](../shell/components.css):

```
.bottom-line{ ... max-width:var(--bottom-measure) }
.bottom-line::before{ width:var(--rule-len) ... }
```

Both are theme tokens, so the bottom line is **always** left-anchored and short-ruled, on every slide
of every deck. **The cap is correct** — a bottom line at display size running the full 1920 would be
unreadable, and that is exactly what a measure is for. The specification is what is wrong.

**Why this is worth a task rather than a wording fix**
The sentence survived a build, four gates, a render, a presentation to an exam board, and two passes
of my own reading of the markup. It was found by **looking at the deck next to its specification**,
which nothing in the pipeline does. And the deck is fine — it reads well, and the slide's argument
lands. So the failure is silent by construction: **nothing downstream of a false layout claim is
damaged, which is why nothing catches it.**

The class is larger than layout. Any specification sentence asserting a property of the built deck —
*spans the full width*, *three figures at display weight*, *the diamond is sized from its own label*
— is a claim about an artifact that does not exist when the sentence is written. Two of those three
examples are also false in the same deck. **A specification is a plan being read as a description.**

**Scope**
- In: a critique step that takes the specification as a **second input** and reports, claim by claim,
  where the built deck does not match it. Judgement, and it stays judgement — see below.
- In: the **decidable subset**, if one exists that is worth having. A claim naming a property the
  shell bounds with a token (`--bottom-measure`, `--rule-len`, `--doc-measure`) is a claim a program
  could compare against the token. Whether that subset is large enough to earn a checker is a finding
  of this task, not an assumption of it. **`0` decidable claims is an acceptable outcome** and must
  be reported as one rather than worked around.
- In: the direction the report points. A mismatch has **two** repairs — fix the deck, or fix the
  specification — and the critique says which it thinks and why. Slide 1's answer is *fix the
  specification*, and a pass that assumed the deck was always wrong would have argued for removing a
  measure that is doing its job.
- In: a rule in [`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) for the general obligation, at the
  altitude the ruleset uses for judgements.
- Out: **automatic parsing of arbitrary prose claims.** Not decidable, and pretending otherwise
  produces a checker whose false alarms cost more than the defect —
  **bind on structure, not vocabulary**.
- Out: making the specification a required input to `check.py`. The gate runs on decks that arrive
  without one; this belongs to critique, which is a reading pass by construction.
- Out: fixing the reference decks' own specifications. Raised as children if this finds any.

**Inputs**
- [`skills/htmldeck/references/critique.md`](../skills/htmldeck/references/critique.md) — the review
  as it stands, and where a second input would enter it.
- [`shell/components.css`](../shell/components.css) — `.bottom-line`, and the tokens that bound it.
- [`docs/THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) — the token list is the candidate set for any
  decidable subset.
- [`CLAUDE.md`](../CLAUDE.md) rule 6 and rule 7 — looking is what found this, and critique is where
  what looking finds is supposed to land.

**Acceptance criteria**
- [ ] The critique pass accepts a specification alongside the deck and reports claim-by-claim
      mismatches, with a recommended direction of repair for each.
- [ ] Run against the first adopting project's deck and its specification, it finds the bottom-line
      claim. It is the regression case.
- [ ] The decidable subset is measured and reported, **including if it is empty**.
- [ ] False alarms are counted against true hits on at least two real decks before any automatic part
      ships.
- [ ] A ruleset row exists for the general obligation.
- [ ] A deck arriving with no specification still critiques, and says the step was skipped and why.

**Open questions**
- Whether the reference decks' own specifications carry claims like this. Likely, and it is cheap to
  find out once the pass exists — the answer decides whether child tasks are raised.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Sweep one real deck's specification by hand for claims about the built artifact | the claim census, and how many are false |
| 2 | Classify each claim: decidable against a token, decidable by render, judgement only | the subset, or the finding that there is none |
| 3 | Write the critique step, judgement first | `critique.md` |
| 4 | Regression: slide 1's bottom line | the pass finds it |
| 5 | False alarms against true hits, two decks | the number that decides any automatic part |
| 6 | Ruleset row | `DESIGN-SYSTEM.md` |

## 3. Implement

**Decisions & assumptions**
-

**Outputs produced**
-

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :--- | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-12 | → proposed | Created by the owner from a finding made while looking at the first adopting project's deck beside its specification. Scoped as a class rather than as slide 1's sentence: two more claims in the same specification are false in the same way, and the reason none of them was caught is that a false layout claim damages nothing downstream. |
