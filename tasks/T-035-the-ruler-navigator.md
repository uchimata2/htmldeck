---
id: T-035
title: Replace the stage ribbon with a ruler navigator, and rescope the chrome budget it breaks
type: deliverable
status: review
phase: review
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
it fits in a fixed width no matter how long the deck is. **Four** amendments to
[`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) admit it — DS-217 twice, DS-131 once, DS-216 once —
and each is narrower than "allow dots again".

**Why this one**
Raised by the owner 2026-08-08. The stated problem is real and is **measured in the deck as it
stands** — see *The two bounds* below, which is the home of these numbers. The chrome row carries
seven stage *names* costing **856 design units**, and the ribbon's content wants **1249.5 units
inside the 1180-unit box** it is given; the six flexible connectors, each compressed to 22.0, absorb
the difference, which is why the row still renders cleanly. Text labels wrap. Add a stage, or
lengthen a stage name, and the connectors have nothing left to give, so the navigation takes a
second line and starts competing with the slide — the exact failure DS-217 exists to prevent.
**The current design is at capacity, not one stage away from it.**

> *This paragraph originally cited the deck's own comment — "~1450 of the 1728 available design
> units, 84% used". **That figure does not reproduce**: the ribbon is 1180 of 1726, or 68.4%, and
> the comment predates the control labels growing. The premise was right and its evidence was
> stale, so both the comment and this paragraph now carry measured numbers instead.*

A ruler answers it structurally rather than by trimming: tick marks have a fixed small width, so the
element's footprint stops depending on how the stages are named.

### What the ruleset says today, and which side has to move

Three rules bear on this, and **all three were reconciled hours before this task was raised**, by
[T-033](T-033-reconcile-ds-131-with-the-chrome-budget.md). That makes the amendment discipline in
**L-37** binding here rather than optional: the owner's proposal contradicts rules on the books, so
it is a rule amendment with a named side, not a licence.

| Rule | Says today | Does the ruler break it? |
| :--- | :--- | :--- |
| DS-216 | One encoding of position; a second only if it encodes a **different** fact — stage versus slide. | **The ruler alone conforms better than what ships** — it carries slide *and* stage in **one** element, where the deck spends a ribbon plus a counter on the same two facts. **But keeping the counter breaks it**, because the ruler already holds both facts, so the counter is the same fact at a different precision rather than a different fact. Amended below, with a cap. |
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
   rather than asserted.** ***Measured 2026-08-08, in two stages: 24, then 17.*** The controls cost
   546 units — a third of the row, and what the eyeballed reduction from 36 underestimated — which
   gives **24 if the ticks have all the remaining space**. They do not: the label shares the row,
   and at the shipped 52-unit pitch the answer as built is **17**. See *The two bounds* below and
   §3, which are the home of those numbers. *This was originally written as the point where the ruler degrades to
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
- In: the **four** amendments above — DS-217 twice, DS-131 once, DS-216 once — which the owner has
  now taken.
- In: **the counter stays**, and DS-216 gains the two-element cap that keeps it from being a
  precedent for a third.
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

### The two bounds, measured 2026-08-08 — plan step 2, and both estimates were wrong

Measured by [`tools/deck/chrome_row.py`](../tools/deck/chrome_row.py) in real offline Chrome,
self-testing, at two stage scales to prove the design-unit conversion is scale-independent.

**The row, and where it actually goes.**

| | Design units | Note |
| :--- | ---: | :--- |
| `.chrome` row | **1726.0** | Not 1728. The 2 units are the stage's own border |
| ribbon box | 1180.0 | 68.4% of the row |
| gap | 40.0 | real space, unusable by either side |
| controls block | 506.0 | `count` 85.4 · `prev` 52 · `next` 52 · `toDoc` 82.8 · `motion` 143.8 |
| **left for the ruler** | **1180.0** | the row is **100% allocated** — there is no spare |

**The target bound is 24, not ~30, and the difference is the controls.** §1 derived ~30 from
1728 ÷ 48 = 36 and then reduced it by eye. **The controls had never been measured, and they cost
546 units — 32% of the row** once the gap is counted. Against the 1180 that is actually free,
DS-168's 48-unit floor gives **1180 ÷ 48 = 24 targets**. So the number that goes into DS-217's
amendment 2 is **24**, and it is the point where small ticks stop being targets — not where the
ruler fails.

**The premise is confirmed, but not by the number this task quoted.** §1 cites the deck's own
comment — *"~1450 of the 1728 available design units — 84% used"*. **That does not reproduce**: the
ribbon is 1180 of 1726, which is 68.4%, and the comment predates the control labels growing. The
premise survives on better evidence than the figure it was resting on: the ribbon's content wants
**1249.5 units inside a 1180 box**, and the six flexible connectors — each now compressed to 22.0
units — absorb the 69.5-unit difference. Seven stage names alone are 856 units. **So the row is at
capacity today, not one stage away from it**, and it renders cleanly only because the connectors
are already giving up their space. The stale comment has been corrected in the deck.

**The mark floor.** At the 0.5 hand-over — measured at k = 0.5056, since the stage is *hidden* at
0.4685 and shown at 0.5056, so **DS-071's threshold behaves exactly as written** — a design unit is
0.506 CSS px:

| Mark | CSS px at the floor | Rendered verdict |
| ---: | ---: | :--- |
| 2 du | 1.01 | one device pixel — a speck, and the quiet colour disappears |
| 3 du | 1.52 | still faint; quiet marks barely register |
| **4 du** | **2.02** | **the first size that reads as a mark in both colours** |
| 5 du | 2.53 | comfortable |
| 10 du | 5.06 | what the lit dot ships at today |

**The inactive marks are the binding constraint, not the current one.** The degraded mode has one
accent mark and many quiet ones, and at 1–2 px the low-contrast quiet colour vanishes well before
the accent does. **Recommended floor: 4 du, with 5 du if the ruler is to stay legible on a poor
projector.** *This verdict was reached by rendering the candidates at native size and looking, and
it is a one-to-two device pixel judgement made through a screenshot — the owner should confirm it
on a real 1× display before it is written into a rule (**L-15**).*

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
- [ ] Slide and stage are both readable from the one element, and the deck carries **exactly two**
      position-encoding elements — the ruler and the counter — never a third (DS-216 as amended)
- [ ] Every small tick names **itself**, not its section — checked on a stage that contains more
      than one slide, where the two would otherwise be indistinguishable
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
- [ ] The **four** amendments are in `DESIGN-SYSTEM.md` with the reasoning in `DESIGN-RATIONALE.md`,
      each naming which side moved — including the definition of *regular repeating scale*, the
      per-target naming clause in DS-131, and DS-216's two-element cap
- [ ] `audit.py` reports zero mechanical failures and both variant suites still catch 7 of 7
- [ ] The deck is **looked at** at 1920 wide and at the 0.5 scale floor (**L-01**)

**Open questions — all three answered by the owner 2026-08-08, and the answers added a fourth
amendment. None is open.**

- ~~Do the three amendments stand as argued?~~ **All three stand, with two tightenings, and both
  tightenings narrow rather than widen.**
  - **Amendment 1 gains a definition of *regular repeating scale*: uniform mark, uniform pitch, no
    per-item label at rest.** Undefined, "scale" is a loophole — any evenly-spaced row of controls
    could claim it and escape the budget entirely, which would leave DS-217 enforceable against
    nothing. A row of twelve labelled buttons is not a scale however regularly it is spaced.
  - **Amendment 3 gains: the naming is *per target*, not per group.** See the coupling below.
- ~~Do small ticks announce their own slide, or their section?~~ **Their own slide.**
- **These two answers are one decision, and separating them would break the rule they are meant to
  preserve.** Amendment 3 narrows DS-131 from *not one target per slide* to *not one **unnamed**
  target per slide. **It is only safe while ticks name themselves.** Had ticks announced their
  section, twelve targets would carry seven labels — a reader still could not name a tick before
  clicking it, so they would be exactly the unnamed targets DS-131 exists to forbid, and the
  amendment would have gutted the rule while appearing to preserve it. That is why the per-target
  naming clause is written **into the amended rule** rather than left as a fact about this deck:
  the rule has to carry its own precondition.
- ~~What happens to the counter?~~ **Kept — and it costs a fourth amendment, which is the widest of
  the four and is therefore capped.** DS-216's test today is *a second encoding is permitted only
  when it encodes a **different fact*** — stage versus slide. The ruler already carries both facts
  in one element, so the counter is the same fact at a different **precision**: the ruler is read at
  a glance, the counter states the position exactly. That argument is sound but it swaps DS-216's
  test from *fact* to *register*, and **register is far easier to claim than fact** — a progress bar
  reads as "approximate position" too, and this task's own scope excludes progress bars *because*
  DS-216 forbade a third encoding. So the amendment is taken **with a cap that does the work the
  old test used to**: a second encoding is permitted for a different fact **or a different
  register**, and **the total is never more than two elements, regardless of how well a third is
  justified**. Ruler plus counter is two. A progress bar would be a third and stays forbidden.

**Four amendments, then, not three** — DS-217 twice, DS-131 once, DS-216 once. All four are the
owner's, taken 2026-08-08, and each names which side moved (**L-37**).

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | ~~Take the three open questions and the amendments~~ — **done 2026-08-08**, and the answers made it four | the rulings, in §1 |
| 2 | ~~Measure the real chrome row~~ — **done 2026-08-08**, both estimates were wrong: the bound is **24**, not ~30, and the mark floor is **4 du** | the two bounds, in §1 |
| 3 | Build the ruler from **`manifest()`**, which [T-034](T-034-a-contents-page-for-the-printed-deck.md) already shipped — number, title, stage — rather than reading the slides again | the ruler component |
| 4 | Wire the reveal: title-swap on hover **and** focus, instant, no transition, restore on blur, with a per-tick accessible name that does not depend on the swap | the reveal |
| 5 | Settle the arrow-key precedence (**DS-137**) deliberately, following DS-166's shape, and write it down | the precedence rule |
| 6 | Build the two-mode degradation — ticks as targets below the bound, marks above it | the degradation |
| 7 | Amend DS-131, DS-216 and DS-217, and record the reasoning in `DESIGN-RATIONALE.md` | ruleset |
| 8 | Re-run the gates, and look at the deck at 1920 and at the 0.5 scale floor (**L-01**) | the verdicts |

**Approach decisions**

- **The ruler consumes `manifest()`; it does not read the slides.** T-034 built the manifest for
  exactly this and shipped it, so the coupling the two tasks were specified around is now real
  rather than promised. If the ruler needs a field the manifest lacks, the field is added *there*
  (**L-08**).
- **Step 2 comes before step 3, and the bound is measured on the real row rather than derived on
  paper.** §1's ~30 is arithmetic against 1728 usable units; the row also carries five controls
  whose real cost is unmeasured, and the ruler has to share with them.
- **The reveal and the accessible name are built together in step 4, not retrofitted.** The visible
  title-swap is a sighted-user affordance and the accessible name is the non-visual route; building
  one first and adding the other later is how the two end up disagreeing (**DS-163**).
- **Step 5 is its own step because the collision already exists in the shipping deck.** The
  `keydown` listener is on `document` and guards only `input,textarea`, so arrows advance the deck
  while a chrome button holds focus. That is tolerable at seven buttons and a real conflict at
  thirty ticks — and **L-38** applies: the failure is at a deck length nothing has been run at yet.
- **The low end gets looked at as well as the high end (L-38).** The lesson T-034 just paid for is
  that a sweep runs in the direction its brief names; this task's brief is all about *long* decks,
  so a short one is the case that will go unrendered unless it is named here.

## 3. Implement

**Decisions & assumptions**

- **The pitch is `--disc-hit` (52 du), not DS-168's bare 48.** The token already sits above the
  floor on purpose, and reusing it makes a tick the same size as every other hit target in the
  deck. **The first build declared 48 and drew 52**, so the capacity arithmetic was overstated by
  four units per tick — `chrome_row.py` now measures the rendered cell and fails if the declared
  constant and the drawn one disagree. — 2026-08-08
- **The capacity is 17, and the three earlier numbers were each wrong for a different reason.**
  36 was the whole row ignoring the controls; ~30 was that reduced by eye; 24 was the measured free
  space **assuming ticks had it all**. As built the label shares the row, and at a 52-unit pitch
  that leaves **17**. Each correction came from measuring one more thing that had been assumed. —
  2026-08-08
- **The label is part of the ruler, not a third encoding — and this is a judgement against a rule
  I had just written, so it is stated rather than buried.** DS-216 caps position encodings at two,
  and the ruler plus the counter is two. The label names whichever tick is under the cursor and, at
  rest, where you are. **The test applied: an independent encoding survives the others being
  removed, and this one does not** — take the ticks away and the label has nothing to say. It is a
  component's caption, not a third indicator. That reading is now written into DS-216 so the next
  component is not free to reinvent it. — 2026-08-08
- **Ticks are bars, not dots.** DS-131's history is twelve unlabelled *dots*, and drawing dots again
  would read as the removed thing returning even though these are named targets. A ruler has tick
  lines; the shape says which component this is. — 2026-08-08
- **DS-137's precedence rule, and it is stated in two places on purpose.** While focus is inside the
  ruler the arrows move between ticks and do **not** advance the deck; Home/End go to the ends;
  Enter or Space jumps. Everywhere else they advance, unchanged. The ruler's handler stops
  propagation *and* the document handler checks for ruler focus — the rule is that the ruler owns
  the arrows while focused, and a rule that depends on which listener was registered first is not a
  rule. Same shape as DS-166. — 2026-08-08
- **`audit.py` implements amendment 1 by verifying the claim, never trusting it.** `data-scale`
  earns the one-item count only if the element is a uniform mark at uniform pitch with no per-item
  label at rest. It defends itself in practice: the `chrome-over-budget` variant stuffs the row,
  the ticks compress unevenly, the pitch stops being uniform, and **the exemption withdraws itself**
  — the gate reports *"claims data-scale but is not regular — counted as n"*. — 2026-08-08
- **`chrome_row.py`'s model of the row was wrong and had been right by accident.** It inferred the
  gap from the distance between the two blocks, which equalled the CSS gap only while the ribbon
  filled its space. The ruler's flexible label takes the slack instead, so the inferred gap became
  596 du and free space collapsed to the ticks' own width — and it fed that into the deck's own
  layout function, which then reported a false *dense*. It now reads the row's `gap` directly. —
  2026-08-08
- **The seeded-defect suite caught its own staleness, and the variant was re-anchored rather than
  deleted.** `three-position-encodings` patched `.ribbon`, which no longer exists; its self-test
  said so and refused to run. The defect it seeds is unchanged and now proves the **new** cap: a
  progress bar beside the ruler and the counter is a third encoding, and it is caught. — 2026-08-08

- **A second tick style ships beside the first, as a theme parameter rather than a fork.**
  Requested by the owner 2026-08-08 after seeing the bars: `data-ticks="dot"` gives **big dots for
  stage starts, small dots for sub-pages, and a ring that slides between positions**. The two
  styles share one manifest, one target set, one keyboard model and one degradation — only the mark
  and the current-position treatment differ, which is what CLAUDE.md rule 4 asks for and what a
  later template generator will pick between. **DS-131 as amended admits dots**: the prohibition
  moved onto *unnamed*, and the twelve dots T-028 removed were unlabelled. `bar` stays the deck's
  default because it is the one that has been gated and looked at end to end. — 2026-08-08
- **The ring adds no motion to DS-140's vocabulary.** It is a **transition**, so DS-141 governs —
  under 500 ms, ease-in-out — and it reuses `--scale-dur` (300 ms) rather than inventing a duration.
  Its position is **measured off the current tick** rather than computed from the pitch, because
  the pitch is only uniform while the ruler is undegraded. It is dropped in the degraded mode,
  where a 30-unit ring would cover its neighbours. — 2026-08-08
- **Size means structure, colour and the ring mean selection, and the two are kept apart.** The
  first build grew the lit dot to stage size, which made slide 8 read as a stage start. Colour now
  marks selection and size goes on meaning section-versus-slide. — 2026-08-08
- **A defect in the capture harness, found because it looked exactly like a CSS bug.** The dots
  rendered as ovals and the lit one refused to take the accent, through three rounds of chasing
  specificity that was never wrong. **`*` does not match pseudo-elements**, so
  [`render.py`](../tools/deck/render.py)'s motion-pinning — `*{transition:none!important}` — covered
  every element and none of the `::before` marks the ruler draws its ticks with, and every capture
  photographed a transition mid-flight. Fixed to `*,*::before,*::after`. **This is DS-221's rule
  failing inside the instrument rather than in the deck**, and the reason it cost so much is that a
  mid-transition capture does not look like a broken capture — it looks like broken CSS
  (**L-35**: suspect the measurement first). — 2026-08-08

**Outputs produced**
- [`examples/reference-deck.html`](../examples/reference-deck.html) — the ruler, both tick styles,
  its label, the degradation, and the keyboard precedence
- [`tools/deck/render.py`](../tools/deck/render.py) — motion-pinning that reaches pseudo-elements
- [`tools/deck/chrome_row.py`](../tools/deck/chrome_row.py) — the two bounds, re-measurable
- [`tools/deck/audit.py`](../tools/deck/audit.py) — amendment 1, enforced by verification
- [`tools/deck/deliverable_variants.py`](../tools/deck/deliverable_variants.py) — re-anchored
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) · [`docs/DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md)

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Row width does not grow with the number of stages or the length of their names | **met** | The indicator went from **1180 du to 624 du** on the same deck, and its width is now `n` × 52 regardless of what the stages are called |
| Every tick a named jump target, revealed by replacing the title in the bar — hover **and** focus, instant, restoring on blur, not a tooltip | **met** | Verified in real Chrome: focusing tick 4 put *"Waiting is the trip"* in the label and blur restored *"Claim"*. No transition on the label. DS-138 forbade a tooltip here — the chrome sits 40 du off the foot |
| Every tick carries its own accessible name, no live region | **met** | `aria-label` per tick — section: *"Go to Claim: Buy frequency before bikes"*; small: *"Go to slide 4: Waiting is the trip"*. The label element is `aria-hidden`, so the swap is never announced |
| Small ticks name **themselves**, not their section | **met** | Checked on stage 2, which holds two slides — its ticks name slide 3 and slide 4 separately. This is the precondition amendment 3 rests on |
| Slide and stage readable from one element, no third encoding | **met** | `audit.py` DS-216: *encodings of position: 2 (ruler, slide counter)* |
| The bound measured on the real row and written into DS-217 as where small ticks stop being targets | **met** | **17**, by [`chrome_row.py`](../tools/deck/chrome_row.py). Written into DS-217 with the derivation |
| Past the bound: section ticks stay large and selectable, small ticks become marks, still reads as a ruler | **met** | Verified by driving the real path — widening the controls until `fitRuler()` chose dense — not by forcing the attribute, which `fitRuler` correctly undid. Section ticks stay 52 du targets, small ticks collapse to 8 du marks and leave the tab order |
| Minimum mark size measured at the 0.5 floor on a 1× display, not chosen | **partly** | Measured: **4 du = 2.02 CSS px**, and the binding constraint is the inactive marks, not the current one. **The 1–2 pixel judgement was taken through a screenshot and is owed a look on real hardware** (**L-15**) before it hardens into a rule |
| Tick hit areas ≥ 48 × 48 du, checked not eyeballed | **met** | 52 du — `--disc-hit`. `audit.py` DS-168: *targets under 24 CSS px: 0* |
| Arrow-key precedence decided and written down (DS-137) | **met** | Ruler owns the arrows while focused. Verified both ways: an arrow inside the ruler moved focus 3 → 4 and **left the slide unchanged**; the same key outside advanced the deck |
| `aria-current` still marks the current position | **met** | Moves with the lit tick, and roving `tabindex` follows it, so tabbing in lands where you are |
| The four amendments in `DESIGN-SYSTEM.md`, reasoning in `DESIGN-RATIONALE.md` | **met** | DS-131, DS-216, DS-217 ×2, each naming which side moved; *Which side moved, second time* records why three narrowed and one widened with a cap |
| `audit.py` zero failures, both suites 7 of 7 | **met** | Plus `check_scaffold`, `print_variants`, `contents_bound` and `chrome_row` self-tests |
| The deck is **looked at** at 1920 and at the 0.5 scale floor | **partly** | Rendered and looked at both, plus the degraded mode. **The owner has not seen it yet**, and on a change to the deck's primary navigation that is the verdict that counts |

**Child fix tasks raised**
- none yet — the two `partly` rows are owner looks, not defects.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-08 | → review | **The ruler is built, gated and looked at; two verdicts are the owner's.** Steps 3–7 landed together. The indicator went from **1180 du to 624 du** on the same deck and its width no longer depends on what the stages are called. Three numbers were corrected on the way. **The pitch is `--disc-hit` (52 du), and the first build declared 48 while drawing 52** — `chrome_row.py` now measures the rendered cell and fails on drift. **Capacity is 17, not 24**: 24 assumed the ticks had the whole free row, and the label shares it. **`chrome_row.py`'s own model of the row was wrong and had been right by accident** — it inferred the gap from the distance between two blocks, which equalled the CSS gap only while the ribbon filled its space; with the ruler's flexible label taking the slack it read 596 du of gap, collapsed free space to the ticks' own width, and fed that into the deck's layout function to produce a false *dense*. One judgement is flagged rather than buried: **the ruler's label is part of the ruler, not DS-216's forbidden third encoding**, on the test that an independent encoding survives the others being removed — this one does not, so it is a caption. That reading is now in DS-216. **Amendment 1 is enforced by verification rather than trust**, and it defends itself: stuff the row and the ticks compress unevenly, the pitch stops being uniform, and the exemption withdraws itself. **The seeded-defect suite caught its own staleness** — `three-position-encodings` anchored on `.ribbon`, refused to run, and was re-anchored rather than deleted; it now proves the new cap by catching a progress bar as a third encoding. Eight gates green. **What is owed: the owner has not looked at the ruler**, and on a change to the deck's primary navigation that is the verdict that counts; and the 4 du mark floor is a one-to-two pixel call taken through a screenshot, owed a look on real hardware (**L-15**) before it hardens into a rule. |
| 2026-08-08 | → in_progress | **Step 2 measured, and both estimates it was checking turned out wrong.** [`chrome_row.py`](../tools/deck/chrome_row.py) prices the row in real offline Chrome at two scales. **The target bound is 24, not ~30**: §1 derived 36 from 1728 ÷ 48 and reduced it by eye, but **the five controls had never been measured and they cost 546 units — 32% of the row**, leaving 1180, which is 24 targets at DS-168's floor. That is the number for DS-217's amendment 2. **The row is also 1726 units, not 1728** — the two are the stage's own border. **The premise is confirmed but its cited evidence is not**: the *"~1450 of 1728, 84% used"* quoted from the deck's own comment does not reproduce — the ribbon is 1180 of 1726, or 68.4% — because the comment predates the control labels growing. The premise stands on stronger evidence instead: the ribbon's content wants **1249.5 units in a 1180 box** and the six connectors, each compressed to 22.0, absorb the difference, so **the row is at capacity now rather than one stage short of it** and renders cleanly only because the connectors are already yielding. The stale comment was corrected in the deck rather than left to be quoted again. **The mark floor is 4 du (2.02 CSS px)**, measured at k = 0.5056 — and the run confirmed DS-071 empirically, the stage being hidden at 0.4685 and shown at 0.5056. **The binding constraint is the inactive marks, not the current one**: at one to two pixels the quiet colour vanishes well before the accent does, which the numbers alone would not have shown. That verdict is a one-to-two device pixel judgement taken through a screenshot and is flagged for the owner to confirm on real hardware (**L-15**). |
| 2026-08-08 | → planned | **All open questions answered, and the answers turned three amendments into four.** The owner took amendments 1–3 **with two tightenings, both narrowing**: *regular repeating scale* is defined as uniform mark, uniform pitch and no per-item label at rest, because undefined it is a loophole any evenly-spaced row of controls could claim, leaving DS-217 enforceable against nothing; and DS-131's narrowing carries a **per-target naming clause** rather than a per-group one. That second tightening matters more than it reads: **amendment 3 and the own-slide answer are one decision**, since ticks announcing their *section* would give twelve targets seven labels — still unnamable before clicking, still exactly what DS-131 forbids — so the amendment would have gutted the rule while appearing to preserve it. The precondition is written into the rule rather than left as a fact about this deck. **The counter is kept, and that is the fourth amendment**: the ruler already carries both facts, so `05 / 12` is the same fact at a different *precision*, which swaps DS-216's test from **fact** to **register** — and register is far easier to claim, a progress bar being the obvious next claimant, which this task's own scope excludes on DS-216's authority. Taken with a **cap that does the work the old test used to**: a second encoding is permitted for a different fact or register, and the total is never more than two elements however well a third is argued. §2 was rewritten around the fact that [T-034](T-034-a-contents-page-for-the-printed-deck.md) has since **shipped `manifest()`**, so the ruler consumes it rather than reading the slides again, and around **L-38** — this task's brief is entirely about long decks, so a short one is the case that will go unrendered unless the plan names it. |
| 2026-08-08 | (no change) | **§1 gained what the raising session had measured but never written down, and one of the findings is a conflict this task now has to settle.** The row's real geometry — 1728 usable design units, `bottom: 40du`, and the five elements in the `.controls` block the ruler must share the row with. The current-position idiom the owner's degradation describes **already ships**: `data-lit` plus `transform: scale(1.5)` on a 10-unit dot, which also anchors the mark-size measurement (10 units is 5 CSS px at the 0.5 scale floor, so a 4-unit mark is 2 px and a 2-unit mark is 1). The lit dot **transitions**, and the title swap must not inherit that. **The conflict: arrow keys are already taken globally.** The `keydown` listener is on `document` and guards only against `input,textarea`, so the arrows advance the deck even while a chrome button holds focus — tolerable with seven ribbon buttons, a genuine collision with thirty ticks, and **DS-137 requires the precedence rule to be stated** rather than left to listener order. DS-166 already fixes the shape of the answer for disclosure and should be followed here. Also recorded for [T-016](T-016-the-interaction-and-motion-layer.md): **`Escape` is already bound in the reading view**, so an ESC-opened slide index has a conflict in one of the two views. |
| 2026-08-08 | (no change) | **Two refinements from the owner, both adopted, and one of them resolves a rule collision this task had not spotted.** (1) **The target's name replaces the title in the navigation bar rather than appearing as a tooltip** — and that turns out to be the *only* conformant option, not merely the tidier one: **DS-138** requires popovers to drop below their control and warns that a control near the foot of the stage cannot host one, and the chrome sits at `bottom: 40du`, so a tooltip on a tick has forty design units of room and nowhere to go. Added with the conditions that make it safe: instant swap, no transition, restore on blur, and an accessible name on every tick independent of the swap, because the swap is a sighted-user affordance. (2) **Past the bound the small ticks become marks rather than disappearing** — strictly better than the "section ticks only" degradation written yesterday, because it drops the *affordance* and keeps the *information*. **Its consequence is larger than it looks: DS-168 governs targets, so once small ticks are not targets the 48-unit floor applies only to the seven section ticks, and the ruler stops having a slide-count ceiling at all** — 1728 ÷ 48 ≈ 36 *sections*, which no real deck reaches. The derived ~30 survives as the point where the ruler **changes mode**, which is a more useful thing for DS-217 to state than a point where it fails. *"Almost pixel-size"* gained a measurable floor rather than a chosen number: at the 0.5 scale floor a 2-unit mark is one CSS pixel and will alias on a 1× display, so the minimum is measured there. **Also recorded: the overlay index and [T-034](T-034-a-contents-page-for-the-printed-deck.md)'s printed contents page are one content source rendered twice**, so whichever lands first builds the slide manifest and the other consumes it (**L-08**). |
| 2026-08-08 | → proposed | Raised by the owner after presenting the deck. **The stated problem is confirmed rather than accepted**: the chrome row runs at ~1450 of 1728 design units with seven stage *names*, so the current design is one stage away from wrapping into the second row DS-217 exists to prevent. Recorded with three named amendments rather than as "allow dots again", because [T-033](T-033-reconcile-ds-131-with-the-chrome-budget.md) settled these exact rules hours earlier and **L-37** makes the amendment explicit: DS-217 counts a regular scale as one item rather than *n*; DS-217's *"around ten slides"* becomes a bound derived from DS-168's 48-design-unit target floor against 1728 usable units — around 30, to be **measured** on the real row; and DS-131's *"not one target per slide"* narrows to *not one **unnamed** target per slide*, which keeps yesterday's rule intact because its point was never the count. **Two changes to the proposal are argued for**: small ticks should announce their own slide rather than their section, or twelve targets carry seven labels and become the unnamed targets DS-131 is about; and hover cannot be the only route (DS-163), so focus parity is a requirement rather than a refinement. **The ESC overlay the request compares against is not the alternative** — DS-131 already names an on-demand slide index as the answer past the bound, and [T-016](T-016-the-interaction-and-motion-layer.md) owns it, so the two compose. |
