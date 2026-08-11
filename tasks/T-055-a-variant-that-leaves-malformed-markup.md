---
id: T-055
title: Close the slide-is-not-a-section variant's open tag, so it tests the tag and not parser repair
type: fix
status: done
phase: review
parent: T-053
blocked_by: []
related: [T-038, T-005]
work_package: PH2
shipped_in: 0.1.5
owner: the project owner
business_value: medium
effort: xs
created: 2026-08-09
updated: 2026-08-12
deliverables:
  - tools/deck/static_variants.py
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
| 1 | Record what the variant breaks today, before touching it | this file §3 |
| 2 | Add the matching closing edit, anchored on something unique | [`static_variants.py`](../tools/deck/static_variants.py) |
| 3 | Re-measure, and run the whole suite | this file §4 |

## 3. Implement

**Decisions & assumptions**
- **The anchor is the slide's own bottom line, not `</section>`** — 2026-08-10. `build` replaces the
  first occurrence and exits if an anchor is missing, so an anchor has to be both present and the
  *right* one: `</section>` appears once per slide, and the provenance mark above it — `Ridership
  model` — appears five times. The bottom line *"is half the headway"* is unique in the deck, and the
  edit carries the two lines beneath it so the pair reads as one region rather than a coincidence.
- **Measured before and after rather than only after** — the criterion asks what else it breaks, and
  a list produced only after the fix cannot show the fix worked.

**What the variant broke, before and after**

| Rule | Before | After |
| :--- | :--- | :--- |
| DS-080 — *slides that are not a `<section>`* | FAIL, its own rule | FAIL, its own rule |
| DS-091 — *slides without exactly one headline: 1* | FAIL | — |
| DS-130 — *disclosure control in the tab order: False* | FAIL | — |
| DS-168 — *targets under 24 CSS px* | NO SUBJECT | — |
| DS-075 — *reflow scrollWidth at 320 px: overflowing 311* | FAIL | — |

**All four went away, which is more than expected.** §1 predicted the collateral would shrink; it
went to nothing. That is the strongest form of the claim: the variant now breaks exactly the rule it
names, and every one of those four rows was Chrome's repair of a `<div>` that never closed — the
headline it reported missing had been lifted out of the slide by the parser, not omitted by the
variant.

**Outputs produced**
- [`static_variants.py`](../tools/deck/static_variants.py) — a second edit on the
  `slide-is-not-a-section` entry, with the reason next to it.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The variant is well-formed HTML | met | The `<div>` now closes with `</div>`; nothing else in the document moved. |
| It still breaks DS-080, and the suite still catches it | met | `slide-is-not-a-section breaks DS-080 -> CAUGHT`, and the whole suite is 24 of 24 static, 7 of 7 rendered, 2 of 2 reduced-motion. |
| What else it breaks is measured and written down | met | The table in §3, measured on both sides of the change. It is now nothing. |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-10 | → done | One closing tag, and the collateral went from four rules to none rather than merely shrinking. Worth recording because of what those four were: **every one was Chrome repairing the markup**, including a DS-091 row reporting a headline-less slide whose headline the parser had moved. A fixture can mis-attribute a catch this quietly, and the only thing that made it visible was a *new* check firing on it (T-053) — not a review of the fixture. |
| 2026-08-10 | (specify) | **Estimated `medium`/`xs`.** `medium` because one of the suite's 24 variants proves nothing about the rule it names — it fails five and tests Chrome's parser repair — and a fixture that mis-attributes a catch is the shape of defect this project keeps finding; `xs` because the fix is one closing tag. **Stays in `PH2`.** |
| 2026-08-09 | → proposed | Found by [T-053](T-053-enforce-the-headline-ds-091-requires.md): the new DS-091 headline check fired on this variant, and the slide it names does have a headline. Chasing that showed the variant never closes its own tag. |
