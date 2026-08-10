---
id: T-055
title: Close the slide-is-not-a-section variant's open tag, so it tests the tag and not parser repair
type: fix
status: proposed
phase: specify
parent: T-053
blocked_by: []
related: [T-038, T-005]
work_package: v0.2
owner: the project owner
business_value: medium
effort: xs
created: 2026-08-09
updated: 2026-08-10
deliverables: []
---

# T-055 — Close the slide-is-not-a-section variant's open tag, so it tests the tag and not parser repair

## 1. Specify

**Outcome**
The `slide-is-not-a-section` variant produces well-formed HTML, so the rule it is said to break is
broken by the thing the variant names.

**Why this one**
The variant rewrites the opening tag and leaves the closing one:

```
'<section class="slide" data-name="Waiting is the trip"'  ->  '<div class="slide" data-name="Waiting is the trip"'
```

The `</section>` stays, so the document is malformed and Chrome repairs it — and what the variant
then tests is the repair. The collateral makes it visible: that one variant fails **DS-130, DS-168
and DS-075** as well as its named DS-080, and since [T-053](T-053-enforce-the-headline-ds-091-requires.md)
added the headline check it fails **DS-091** too, reporting *"Waiting is the trip"* as a slide with
no headline. The slide has a headline; the parser moved it.

`static_variants.py` states the standard this falls short of in its own words — *the edit is the
smallest one that breaks the rule and nothing else, because a variant that breaks three rules proves
nothing about any of them*. It is also T-038's discriminator applied to the suite rather than to the
gate: **the thing measured has to be the thing cited.**

DS-080 is genuinely caught either way, so this is not a hole in the gate. It is a variant that
proves less than it appears to, and the appearance is the problem.

**Scope**
- In: replacing the matching `</section>` so the variant is a well-formed `div`.
- In: re-recording what the variant then breaks, since the collateral list is expected to shrink.
- Out: the other variants' collateral. DS-075 under the S3 seed is documented and real, and
  `examples/README.md` explains why collateral is kept out of the seeded-defect ledger.

**Inputs**
- [`tools/deck/static_variants.py`](../tools/deck/static_variants.py) — `RENDER_VARIANTS`
- [`examples/reference-deck.html`](../examples/reference-deck.html) — the slide the variant edits
- [T-038](T-038-the-gate-emits-verdicts-for-judge-rules-and-one-wrong-id.md) — the thing measured is the thing cited

**Acceptance criteria**
- [ ] The variant is well-formed HTML
- [ ] It still breaks DS-080, and the suite still catches it
- [ ] What else it breaks is measured and written down, not assumed to be nothing

**Open questions**
- none.

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
| 2026-08-10 | (specify) | **Estimated `medium`/`xs`.** `medium` because one of the suite's 24 variants proves nothing about the rule it names — it fails five and tests Chrome's parser repair — and a fixture that mis-attributes a catch is the shape of defect this project keeps finding; `xs` because the fix is one closing tag. **Stays in `v0.2`.** |
| 2026-08-09 | → proposed | Found by [T-053](T-053-enforce-the-headline-ds-091-requires.md): the new DS-091 headline check fired on this variant, and the slide it names does have a headline. Chasing that showed the variant never closes its own tag. |
