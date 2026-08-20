---
id: T-115
title: A specification can assert a layout the shell cannot honour, and nothing reads the two together
type: deliverable
status: done
phase: review
parent: null
blocked_by: []
related: [T-109, T-114]
work_package: PH3
owner: the project owner
business_value: medium
effort: l
created: 2026-08-12
updated: 2026-08-18
shipped_in: 0.5.0
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
- **No checker ships, and the census is why** — 2026-08-18. Not because the decidable subset is
  empty; because reaching it from prose means matching a phrase, and the phrase is wrong more often
  than it is right. Numbers below.
- **The pass lives in `critique.md` §3.3, not in `spec.py`** — 2026-08-18. `spec.py` was the
  tempting home: it already takes the specification pair plus the optional deck, and SPEC-5 already
  waits on the built deck. But it is pure standard library and runs *before* a deck exists, and
  every claim here needs either a render or a token comparison. A sixth SPEC verdict would have made
  the tool's own instructions unrunnable.
- **Judge against the container, never the stage** — 2026-08-18. This is the whole technique, and it
  is what the census measured.
- **DS-234 is `default`/`judge`, not `hard`** — 2026-08-18. A specification may deliberately describe
  an intent the deck approximates; the rule is that the mismatch is *reported and directed*, not that
  it is forbidden.

**Outputs produced**
- [`skills/htmldeck/references/critique.md`](../skills/htmldeck/references/critique.md) §3.3 —
  the specification-conformance pass; §3 is now *Three formats*.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-234, the general obligation.
- [T-182](T-182-the-shipped-example-decks-specification-carries-three-false-claims-about-the-deck.md)
  — the three false claims the pass found in this repository's own published example.

**The census, which is the finding.** Every `Structure` field of both shipped decks, swept by hand,
with the geometry measured in real Chrome at 1920×1234, offline.

- **The content column is 1726 du of a 1918 du stage** — the stage less `--pad-x` either side. Every
  full-bleed element measures exactly 1726, i.e. **100.0% of the column**.
- So a diagram reading *90% of the stage* is at full width. **Judged against the stage, the phrase
  *full width* is false 3 times across the two decks; judged against the column it is false once.**
  That is **2 false alarms against 1 true hit**, and it is the number that decided no checker ships.
- The one true hit is structural rather than incidental: `.bottom-line` is
  `max-width:var(--bottom-measure)` = 1500 du inside a 1726 du column, so it **cannot** span on any
  slide of any deck. That shape — an element the theme caps below its own container, described as
  filling it — is decidable from the CSS alone, with no render at all.
- **Fractional claims are the trap and stay judgement.** *Upper two thirds* appears 3 times in
  `measure-first`, against diagrams filling 70.8%, 78.6% and 83.1% of their container. A checker
  flags all three; a reader accepts all three. The rule reports a fraction only where the deck
  contradicts the claim's intent.

**What the pass found on its regression case.** Run against `measure-first` and its specification, it
returns the bottom-line claim, plus two the task had listed as suspected: only two of three figures
per side reach display size (84 px), and slide 2's diamond is not sized from its label because there
is no label slot — which is [T-117](T-117-the-decision-diamond-has-no-label-slot-and-diagrams-sit-off-the-text-grid.md).
`sort-window`'s specification came back clean; its own *full-width* claim is true at 100.0% of the
column, and that is the case a stage-relative rule would have failed.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The critique pass accepts a specification alongside the deck and reports claim-by-claim mismatches, with a recommended direction of repair for each | met | `critique.md` §3.3. The direction is per claim and both directions occur in the regression case: two *fix the specification*, one *fix the deck* |
| Run against the first adopting project's deck and its specification, it finds the bottom-line claim | met | Found, and measured rather than asserted: 1500 du inside a 1726 du column. It also found the two further claims §1 suspected |
| The decidable subset is measured and reported, **including if it is empty** | met | Not empty, and smaller than it looks: one shape — an element the theme caps below its container. Reported with the false-alarm count that bounds it |
| False alarms are counted against true hits on at least two real decks before any automatic part ships | met | 1 hit against 2 false alarms for the phrase-matching rule, across both shipped decks. **No automatic part ships**, which is what that number decided |
| A ruleset row exists for the general obligation | met | DS-234, `default`/`judge`. Rows 166 → 167 |
| A deck arriving with no specification still critiques, and says the step was skipped and why | met | §3.3 opens on it, and forbids inferring a specification from the deck — that would compare the deck against itself |

**Child fix tasks raised**
- [T-182](T-182-the-shipped-example-decks-specification-carries-three-false-claims-about-the-deck.md)
  — the three false claims in this repository's own published example specification. Raised rather
  than fixed here, which is what §1's scope books.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-12 | → proposed | Created by the owner from a finding made while looking at the first adopting project's deck beside its specification. Scoped as a class rather than as slide 1's sentence: two more claims in the same specification are false in the same way, and the reason none of them was caught is that a false layout claim damages nothing downstream. |
| 2026-08-18 | proposed → specified | §1's instance re-derived from the shell rather than taken on trust: `.bottom-line` carries `max-width:var(--bottom-measure)` and the token resolves to 1500 du, so the cap is real and unconditional. Scope and the six criteria stand. |
| 2026-08-18 | specified → planned | The six plan steps stand. Two things settled before any writing: the pass belongs in `critique.md` and not in `spec.py`, whose standard-library, no-deck-required contract a sixth verdict would break; and step 5's false-alarm count is the step that decides steps 2 and 3, so it runs before either is written up. |
| 2026-08-18 | planned → in_progress → done | The census was the work, and it **overturned the count this task started from**. Judged against the stage, three *full width* claims read false; judged against the content column — 1726 du, which every full-bleed element fills exactly — one does. Two false alarms against one hit, so no checker ships, and DS-234 is `judge` with the calibration written into it. The surviving hit is structural rather than lucky: a bottom line is capped 226 du below the column it is said to span, on every slide of every deck. Raised [T-182](T-182-the-shipped-example-decks-specification-carries-three-false-claims-about-the-deck.md) for the three false claims in this repository's own published example, per §1's scope. |
