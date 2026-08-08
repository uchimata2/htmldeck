---
id: T-035
title: Replace the stage ribbon with a ruler navigator, and rescope the chrome budget it breaks
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-033, T-028, T-016, T-027, T-034]
work_package: WP2
owner: maintainer
created: 2026-08-08
updated: 2026-08-08
deliverables: []
---

# T-035 — Replace the stage ribbon with a ruler navigator, and rescope the chrome budget it breaks

## 1. Specify

**Outcome**
The deck's position indicator is a **ruler**: a small tick per slide, a large tick at each stage
start, every tick a named jump target. It replaces the stage-name ribbon, which does not scale, and
it fits in a fixed width no matter how long the deck is. Three rules in
[`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) are amended to admit it, and the amendments are
narrower than "allow dots again".

**Why this one**
Raised by the owner 2026-08-08. The stated problem is real and is **measurable in the deck as it
stands**: the chrome row carries seven stage *names*, and the deck's own CSS comment records the row
at **~1450 of the 1728 available design units — 84% used with seven stages**. Text labels wrap.
Add a stage, or lengthen a stage name, and the navigation takes a second line and starts competing
with the slide, which is the exact failure DS-217 exists to prevent. **The current design is one
stage away from the problem it was built to solve.**

A ruler answers it structurally rather than by trimming: tick marks have a fixed small width, so the
element's footprint stops depending on how the stages are named.

### What the ruleset says today, and which side has to move

Three rules bear on this, and **all three were reconciled hours before this task was raised**, by
[T-033](T-033-reconcile-ds-131-with-the-chrome-budget.md). That makes the amendment discipline in
**L-37** binding here rather than optional: the owner's proposal contradicts rules on the books, so
it is a rule amendment with a named side, not a licence.

| Rule | Says today | Does the ruler break it? |
| :--- | :--- | :--- |
| DS-216 | One encoding of position; a second only if it encodes a **different** fact — stage versus slide. | **No — it conforms better than what ships.** The ruler encodes slide *and* stage in **one** element, where the deck currently spends a ribbon plus a counter on the same two facts. |
| DS-131 | Click-to-jump to a bounded set of **named** targets. *"Not one target per slide."* | **Yes, as written** — a tick per slide is one target per slide. |
| DS-217 | Chrome budget ~12 labelled or interactive items; *"per-slide dots stop scaling somewhere around ten slides."* | **Yes, twice** — 12 ticks + 7 large + 4 buttons + a counter is ~24 items, and a 12-slide deck is already past "around ten". |

**Three amendments, and each is narrower than it first looks.**

1. **DS-217 counts a regular repeating scale as one item, not as *n*.** The budget's stated reason
   is that past it *"the navigation reads as an interface rather than as a deck"* — it counts items
   because items are what make a frame noisy. **A regular tick array is perceived as one object**,
   the way a ruler is one object and not three hundred marks. So the metric is wrong for this shape,
   not the intent. Amending *how it counts* keeps the budget meaningful for everything else;
   raising the number would not.
2. **DS-217's "somewhere around ten slides" is replaced by a derived bound.** DS-168 requires
   targets ≥ 24 × 24 CSS px, which **inside the stage means ≥ 48 × 48 design units** — the stage
   bottoms out at 0.5 scale. The chrome row has **1728 usable design units**, so ticks alone could
   carry at most 36 targets, and fewer once the right-hand controls take their share: **the real
   bound is around 30 and must be measured, not asserted.** That replaces a taste figure with a
   number that falls out of the accessibility floor — and it is the first honest answer to *how long
   is too long*, which DS-217 has been guessing at.
3. **DS-131's *"not one target per slide"* narrows to *not one **unnamed** target per slide*.**
   This is the amendment worth arguing for, because it means the rule written yesterday mostly
   survives. T-033 established that *named* is the load-bearing word — a target the reader can
   identify **before** clicking. The objection was never to the count; it was to twelve unlabelled
   dots. A tick that announces its slide is a named target, and the rule keeps its point.

### Where the proposal needs changing, and why

**Small ticks must carry the slide's own title, not their section's.** The request has hovering a
large tick *and its successor small ticks* show the **section** title. That gives twelve targets
carrying seven distinct labels, so a small tick is a jump to a slide the reader **cannot name before
clicking** — precisely what amendment 3 is trying to preserve. The fix costs nothing: every slide
already has `data-name`, so the small tick can announce its own slide and the large tick its stage.
Then the whole ruler is named targets and DS-131 needs only the narrowing above.

**Hover cannot be the only route — DS-163.** *"Never hover-only. Tooltips may supplement; never the
only route to content."* Whatever hover reveals, keyboard focus must reveal identically, and every
tick needs an accessible name whether or not anything is revealed. Not a blocker; a requirement.

**The ESC overlay and the ruler are complementary, not alternatives.** The request compares the
ruler against the pop-up navigator seen elsewhere. **The ruleset already names the overlay as the
answer for the case the ruler cannot serve** — DS-131, as reworded by
[T-033](T-033-reconcile-ds-131-with-the-chrome-budget.md), says a deck whose stages are uneven or
long enough that landing on one is not a useful jump *owes an on-demand slide index*, and building
it is [T-016](T-016-the-interaction-and-motion-layer.md)'s. So the shape is: **ruler up to the
measured bound, overlay index beyond it**, and past the bound the ruler degrades to large ticks
only. Choosing one to the exclusion of the other is the thing to avoid.

**Scope**
- In: the ruler component — small ticks per slide, large ticks per stage start, current position lit.
- In: named jump targets on every tick, with hover **and** focus parity.
- In: the three amendments above, once the owner takes them.
- In: measuring the target-count bound on the real chrome row rather than deriving it on paper.
- In: whatever the right-hand controls and title need so the two sit together.
- Out: building the on-demand slide index. Named as the answer past the bound; owned by
  [T-016](T-016-the-interaction-and-motion-layer.md).
- Out: the printed deck. Print hides the chrome entirely, and the paper equivalent is
  [T-034](T-034-a-contents-page-for-the-printed-deck.md).
- Out: reinstating a progress bar. DS-216 still forbids a third encoding, and the ruler already
  carries both facts.

**Inputs**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-131, DS-163, DS-168, DS-216, DS-217.
- [`T-033`](T-033-reconcile-ds-131-with-the-chrome-budget.md) — what *named targets* was decided to
  mean, and why DS-131 was the side that moved last time.
- [`T-027`](T-027-specify-the-slide-deliverable-and-the-outline-contract.md) — the owner's
  *"extremely noisy"*, which is what the budget encodes.
- [`docs/DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) — *Three encodings of one fact* and
  *Which side moved*.
- [`examples/reference-deck.html`](../examples/reference-deck.html) — the ribbon it replaces, and
  the 1450-of-1728 measurement in its own comment.

**Acceptance criteria**
- [ ] The chrome row's width **does not grow with the number of stages or the length of their
      names**, measured against the current ribbon on the same deck
- [ ] Every tick is a named jump target, announced on hover **and** on keyboard focus (DS-163),
      with an accessible name in both cases
- [ ] Slide and stage are both readable from the one element, with no third encoding (DS-216)
- [ ] The target-count bound is **measured on the real row**, written into DS-217, and the deck
      degrades to large ticks only past it
- [ ] Tick hit areas are ≥ 48 × 48 design units, or meet DS-168's spacing exception — checked, not
      eyeballed
- [ ] The three amendments are in `DESIGN-SYSTEM.md` with the reasoning in `DESIGN-RATIONALE.md`
- [ ] `audit.py` reports zero mechanical failures and both variant suites still catch 7 of 7
- [ ] The deck is **looked at** at 1920 wide and at the 0.5 scale floor (**L-01**)

**Open questions**
- **Do the three amendments stand as argued?** Each is narrower than "allow per-slide dots again",
  and amendment 3 is the one that decides whether DS-131 keeps its point or loses it. — owner
  decides.
- **Do small ticks announce their own slide, or their section?** The analysis above argues own
  slide; the request said section. It is the difference between a ruler of named targets and a
  ruler of anonymous ones. — owner decides.
- **What happens to the counter?** The ruler encodes slide position, so *"05 / 12"* may now be the
  third encoding DS-216 forbids rather than the permitted second. — owner decides.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Take the three open questions and the three amendments | the rulings |
| 2 | Measure the real chrome row: what the controls cost, what is left for ticks, and the target count that fits at 48 du pitch | the bound |
| 3 | Build the ruler as a component, with focus parity from the start rather than retrofitted | edited deck |
| 4 | Degrade past the bound, and hand the long case to T-016's overlay index | the degradation |
| 5 | Amend DS-131, DS-217 and record the reasoning in `DESIGN-RATIONALE.md` | ruleset |
| 6 | Re-run the gates and look at the deck at both ends of the scale range | the verdicts |

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
| 2026-08-08 | → proposed | Raised by the owner after presenting the deck. **The stated problem is confirmed rather than accepted**: the chrome row runs at ~1450 of 1728 design units with seven stage *names*, so the current design is one stage away from wrapping into the second row DS-217 exists to prevent. Recorded with three named amendments rather than as "allow dots again", because [T-033](T-033-reconcile-ds-131-with-the-chrome-budget.md) settled these exact rules hours earlier and **L-37** makes the amendment explicit: DS-217 counts a regular scale as one item rather than *n*; DS-217's *"around ten slides"* becomes a bound derived from DS-168's 48-design-unit target floor against 1728 usable units — around 30, to be **measured** on the real row; and DS-131's *"not one target per slide"* narrows to *not one **unnamed** target per slide*, which keeps yesterday's rule intact because its point was never the count. **Two changes to the proposal are argued for**: small ticks should announce their own slide rather than their section, or twelve targets carry seven labels and become the unnamed targets DS-131 is about; and hover cannot be the only route (DS-163), so focus parity is a requirement rather than a refinement. **The ESC overlay the request compares against is not the alternative** — DS-131 already names an on-demand slide index as the answer past the bound, and [T-016](T-016-the-interaction-and-motion-layer.md) owns it, so the two compose. |
