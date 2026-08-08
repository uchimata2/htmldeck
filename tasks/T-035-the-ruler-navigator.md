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
2. **DS-217's "somewhere around ten slides" is replaced by a derived bound — and the bound is not
   where the ruler dies, it is where the small ticks stop being targets.** DS-168 requires targets
   ≥ 24 × 24 CSS px, which **inside the stage means ≥ 48 × 48 design units**, because the stage
   bottoms out at 0.5 scale. The chrome row has **1728 usable design units**, so at most 36 targets
   fit, fewer once the right-hand controls take their share — call it **around 30, to be measured
   rather than asserted.** *This was originally written as the point where the ruler degrades to
   section ticks only. The owner's degradation is better and replaces it — see below, and the
   consequence is that DS-168 stops governing the slide count at all.* The figure is still worth
   deriving: it is the first honest answer to *how long is too long*, where DS-217 has been guessing.
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

**How the target's name is revealed: it replaces the title in the bar, it is not a tooltip.**
*Proposed by the owner 2026-08-08, and it is the only conformant option — a tooltip on this control
is forbidden by a rule already on the books.* **DS-138**: *popovers drop below the element, never
above… a control near the foot of a 1080-unit stage cannot host a panel more than a row or two
deep.* The chrome sits at `bottom: 40du`, so **a tick has 40 design units of room beneath it and a
tooltip has nowhere to go.** Hovering or focusing a tick therefore **overwrites the section/page
title already displayed in the navigation bar** with the target's, and restores it on blur.

Three consequences, all of them arguments for it:

- **No new surface, and no new component.** The label lands in the region the eye already reads for
  that fact, so the bar means one thing rather than two.
- **The redundancy objection answers itself.** Overwriting the title looks like it destroys *where
  am I* exactly when you want to compare — except the **lit tick still encodes current position
  graphically**, so the text is the redundant copy during a hover and is free to be borrowed.
- **It must not animate, and it must restore.** Keyboard-arrowing through thirty ticks would
  otherwise flicker the title thirty times. Instant swap, no transition, restore on blur.

**Hover still cannot be the only route — DS-163.** Focus must reveal identically to hover. Separately
from the visible swap, **every tick carries its own accessible name**, because the swap is a
sighted-user affordance: a screen reader must not depend on it, and it must not be wired to a live
region that announces on every focus move.

**Degradation: the small ticks stop being targets, they do not stop existing.**
*Proposed by the owner 2026-08-08, and it is better than the "section ticks only" degradation this
task first carried.* Past the measured bound the section ticks stay large and selectable, and the
per-slide ticks **shrink to near-pixel marks with only the current one enlarged and coloured**.

That is a strictly better trade, and it changes what the bound means:

- **It drops the affordance, not the information.** The earlier version dropped per-slide position
  entirely; this keeps the ruler reading as a ruler at any length.
- **It takes DS-168 out of the slide count.** DS-168 governs **targets**. Once small ticks are marks
  rather than targets, the 48-design-unit floor applies only to the **section** ticks — of which
  there are seven. 1728 ÷ 48 ≈ **36 sections**, and a deck with 36 sections is not a real case. So
  the ruler effectively **stops having a slide-count ceiling** and acquires a section-count one that
  nothing will reach. The derived ~30 stays meaningful as *the point where the ruler changes mode*,
  which is a much more useful thing for DS-217 to state than a point where it fails.
- **"Almost pixel-size" has a floor, and it is measurable rather than a matter of taste.** The stage
  bottoms out at 0.5 scale, so a mark of *n* design units renders at *n*/2 CSS px: a 2-unit dot is
  one CSS pixel at the floor and will alias to a grey smudge on a 1× display. **Measure the smallest
  mark that survives the 0.5 scale floor on a 1× screen**, and take that as the minimum — do not
  pick a number.

**The ESC overlay and the ruler are complementary, not alternatives.** The request compares the
ruler against the pop-up navigator seen elsewhere. **The ruleset already names the overlay as the
answer for the case the ruler cannot serve** — DS-131, as reworded by
[T-033](T-033-reconcile-ds-131-with-the-chrome-budget.md), says a deck whose stages are uneven or
long enough that landing on one is not a useful jump *owes an on-demand slide index*, and building
it is [T-016](T-016-the-interaction-and-motion-layer.md)'s. With the degradation above the ruler no
longer *fails* at length, so the overlay's job narrows usefully: it is for **reaching a named slide
inside a long section**, which a tick — target or not — cannot do.

**The overlay and the printed contents page are one content source, two renderings.**
[T-034](T-034-a-contents-page-for-the-printed-deck.md) generates its boxes from each slide's number,
title, bottom line and stage; the overlay needs exactly those fields plus current-position
highlighting. **Neither should clone slides independently** — the deck already has the precedent in
`buildDoc()`, and two derivations of one fact is how they drift (**L-08**). Whichever of the two
lands first builds a **slide manifest** — number, title, bottom line, stage, mark — and the other
consumes it. The renderings legitimately differ; the manifest must not.

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

### What the deck already does — measured 2026-08-08, so the specify pass need not re-derive it

Read this before writing the detailed spec. It is the state of
[`examples/reference-deck.html`](../examples/reference-deck.html) as it stands.

**The row the ruler moves into.** `.chrome` is `position:absolute; left/right: --pad-x;
bottom: 40du`, so it spans **1728 usable design units** and sits **40 units off the foot of the
stage** — the number behind the DS-138 argument above. It carries two things: `<ul class="ribbon"
id="ribbon">` on the left, and a `.controls` block on the right holding **five elements** —
`#count`, `#prev`, `#next`, `#toDoc`, `#motion`. The ruler replaces the first; the second is what it
must share the row with, and is what step 2's measurement has to price.

**The ribbon is generated, not authored**, in a boot loop that fills `ribbonBox` and wires click
handlers during boot — there is already a comment in the source explaining that its handler is a
function declaration rather than a `var` **because it is called before its definition is reached**.
The ruler inherits that ordering constraint.

**The current-position idiom already exists and is the one the owner's degradation describes.** The
lit stage gets `data-lit`, and CSS gives it `background: var(--accent)` plus **`transform:
scale(1.5)`** on a **10-unit** dot. So "current one enlarged and coloured" is not a new mechanism —
it is what ships. It also gives the mark-size measurement its anchor: **10 units renders at 5 CSS px
at the 0.5 scale floor**, so a 4-unit mark lands at 2 px and a 2-unit mark at 1 px.
`aria-current="true"` is already set on the lit item and must survive the rewrite.

**The dot currently animates**, with `transition: background/transform var(--scale-dur) ease-in-out`.
The title swap decided above must **not** inherit that — it is an instant swap, and a transition on
a label that changes on every focus move is the flicker the decision is guarding against.

### A keyboard collision this task has to resolve — DS-137

**Arrow keys are already taken, globally.** The `keydown` listener is on `document` and its only
guard is `e.target.matches('input,textarea')` — so `ArrowRight` / `ArrowLeft` / `PageUp` /
`PageDown` / space / `Home` / `End` advance the deck **even when a chrome button has focus**. That is
tolerable with seven ribbon buttons. **With thirty ticks it is a real conflict**, because the
conventional keyboard idiom for a tick group is arrow-to-move-within-it, and those keys advance the
slide instead. **DS-137 requires a defined precedence rule for exactly this**, and DS-166 already
fixes the shape of the answer for disclosure — arrows advance, a separate key toggles, the two do
not interact. Decide the same way here, deliberately: either ticks are Tab-reachable only, or the
handler learns to yield when focus is inside the ruler. Do not leave it to whichever listener runs
first.

**`Escape` is already bound, and it matters for the overlay this task hands off to.** In the reading
view `Escape` returns to the stage; on the stage it is free. So an ESC-opened slide index
([T-016](T-016-the-interaction-and-motion-layer.md)) has a conflict to resolve in one of the two
views, not in neither.

**Acceptance criteria**
- [ ] The chrome row's width **does not grow with the number of stages or the length of their
      names**, measured against the current ribbon on the same deck
- [ ] Every tick is a named jump target. The name is revealed by **replacing the title in the
      navigation bar**, on hover **and** on keyboard focus alike (DS-163), instantly and with no
      transition, restoring on blur — **not** by a tooltip, which DS-138 forbids on a control this
      near the foot of the stage
- [ ] Every tick carries its own accessible name independent of the visible swap, and focus movement
      does not announce through a live region
- [ ] Slide and stage are both readable from the one element, with no third encoding (DS-216)
- [ ] The target-count bound is **measured on the real row** and written into DS-217 as the point
      where **small ticks stop being targets**, not where the ruler fails
- [ ] Past the bound: section ticks stay large and selectable, per-slide ticks become marks with
      only the current one enlarged and coloured, and the ruler still reads as a ruler
- [ ] The minimum mark size is **measured at the 0.5 scale floor on a 1× display**, not chosen
- [ ] Interactive tick hit areas are ≥ 48 × 48 design units, or meet DS-168's spacing exception —
      checked, not eyeballed
- [ ] The arrow-key precedence between advancing the deck and moving within the ruler is **decided
      and written down** (DS-137), not left to listener order
- [ ] `aria-current` still marks the current position, as the ribbon does today
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
| 2 | Measure the real chrome row: what the controls cost, what is left for ticks, the target count that fits at 48 du pitch, and the smallest mark that survives 0.5 scale on a 1× display | the two bounds |
| 3 | Build the ruler as a component, with focus parity and the title-swap reveal from the start rather than retrofitted | edited deck |
| 4 | Build the two-mode degradation — ticks as targets below the bound, marks above it | the degradation |
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
| 2026-08-08 | (no change) | **§1 gained what the raising session had measured but never written down, and one of the findings is a conflict this task now has to settle.** The row's real geometry — 1728 usable design units, `bottom: 40du`, and the five elements in the `.controls` block the ruler must share the row with. The current-position idiom the owner's degradation describes **already ships**: `data-lit` plus `transform: scale(1.5)` on a 10-unit dot, which also anchors the mark-size measurement (10 units is 5 CSS px at the 0.5 scale floor, so a 4-unit mark is 2 px and a 2-unit mark is 1). The lit dot **transitions**, and the title swap must not inherit that. **The conflict: arrow keys are already taken globally.** The `keydown` listener is on `document` and guards only against `input,textarea`, so the arrows advance the deck even while a chrome button holds focus — tolerable with seven ribbon buttons, a genuine collision with thirty ticks, and **DS-137 requires the precedence rule to be stated** rather than left to listener order. DS-166 already fixes the shape of the answer for disclosure and should be followed here. Also recorded for [T-016](T-016-the-interaction-and-motion-layer.md): **`Escape` is already bound in the reading view**, so an ESC-opened slide index has a conflict in one of the two views. |
| 2026-08-08 | (no change) | **Two refinements from the owner, both adopted, and one of them resolves a rule collision this task had not spotted.** (1) **The target's name replaces the title in the navigation bar rather than appearing as a tooltip** — and that turns out to be the *only* conformant option, not merely the tidier one: **DS-138** requires popovers to drop below their control and warns that a control near the foot of the stage cannot host one, and the chrome sits at `bottom: 40du`, so a tooltip on a tick has forty design units of room and nowhere to go. Added with the conditions that make it safe: instant swap, no transition, restore on blur, and an accessible name on every tick independent of the swap, because the swap is a sighted-user affordance. (2) **Past the bound the small ticks become marks rather than disappearing** — strictly better than the "section ticks only" degradation written yesterday, because it drops the *affordance* and keeps the *information*. **Its consequence is larger than it looks: DS-168 governs targets, so once small ticks are not targets the 48-unit floor applies only to the seven section ticks, and the ruler stops having a slide-count ceiling at all** — 1728 ÷ 48 ≈ 36 *sections*, which no real deck reaches. The derived ~30 survives as the point where the ruler **changes mode**, which is a more useful thing for DS-217 to state than a point where it fails. *"Almost pixel-size"* gained a measurable floor rather than a chosen number: at the 0.5 scale floor a 2-unit mark is one CSS pixel and will alias on a 1× display, so the minimum is measured there. **Also recorded: the overlay index and [T-034](T-034-a-contents-page-for-the-printed-deck.md)'s printed contents page are one content source rendered twice**, so whichever lands first builds the slide manifest and the other consumes it (**L-08**). |
| 2026-08-08 | → proposed | Raised by the owner after presenting the deck. **The stated problem is confirmed rather than accepted**: the chrome row runs at ~1450 of 1728 design units with seven stage *names*, so the current design is one stage away from wrapping into the second row DS-217 exists to prevent. Recorded with three named amendments rather than as "allow dots again", because [T-033](T-033-reconcile-ds-131-with-the-chrome-budget.md) settled these exact rules hours earlier and **L-37** makes the amendment explicit: DS-217 counts a regular scale as one item rather than *n*; DS-217's *"around ten slides"* becomes a bound derived from DS-168's 48-design-unit target floor against 1728 usable units — around 30, to be **measured** on the real row; and DS-131's *"not one target per slide"* narrows to *not one **unnamed** target per slide*, which keeps yesterday's rule intact because its point was never the count. **Two changes to the proposal are argued for**: small ticks should announce their own slide rather than their section, or twelve targets carry seven labels and become the unnamed targets DS-131 is about; and hover cannot be the only route (DS-163), so focus parity is a requirement rather than a refinement. **The ESC overlay the request compares against is not the alternative** — DS-131 already names an on-demand slide index as the answer past the bound, and [T-016](T-016-the-interaction-and-motion-layer.md) owns it, so the two compose. |
