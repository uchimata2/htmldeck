---
id: T-112
title: Motion density, and the split between content motion and affordance motion
type: deliverable
status: done
phase: review
parent: null
blocked_by: []
related: [T-016, T-041, T-057, T-111, T-185]
work_package: PH3
owner: the project owner
business_value: high
effort: l
created: 2026-08-12
updated: 2026-08-22
shipped_in: 0.5.0
deliverables:
  - shell/components.css
  - shell/shell.html
  - themes/quarto.css
  - tools/deck/density.py
  - docs/DESIGN-SYSTEM.md
  - docs/THEME-CONTRACT.md
  - docs/COMPONENT-CONTRACT.md
  - skills/htmldeck/references/build.md
---

# T-112 — Motion density, and the split between content motion and affordance motion

## 1. Specify

**Outcome**
Two things that are currently one. **Affordance motion** — what tells a reader that a control is a
control — always runs. **Content motion** — what animates the argument on the slide — runs as often
as a `density` parameter says, from 0 to 100, defaulting to 10. A deck at the default is mostly
still, with the occasional moment; a deck at 100 moves everywhere it conformantly can.

**The design target, in the reporter's words**
*"The deck should not be a continuously wobbly bunch of pixels, like worms in the sand, but some
hidden gentle animation, like the '0', look like easter eggs during the boring business topics."*

**The `0` is the model, and it is worth being precise about why.** On slide 3 of the first real deck,
the markup is:

```html
<p class="statfig pulse">0</p>
<p class="statcap">measurements of forecast quality.</p>
```

Nobody designed that moment. It is **DS-147** — *count-up on headline statistics, one emphasis pulse*
— applied mechanically to a figure that happened to be zero. The count-up has nowhere to travel, so
the number sits there and pulses under a headline reading *"Nothing here measures the forecast."* The
wit is emergent; the system produced it. **That is the argument for what density must and must not
do:** it decides *how many conformant motions run*, and never invents a per-slide effect. Delight
came from applying one rule without exception until the content made it land.

**The split**

| | Governed by density | Examples |
| :--- | :--- | :--- |
| **Affordance motion** | No — always on | Pager button rotating ~3° on hover and pinching on press · the hovered element's highlight fading in · the ruler's ring easing between dots · **DS-140's `Current`**, the dashed flow arrows |
| **Content motion** | Yes | An arrowhead scaling out of its line · matrix dots popping in, wobbly, in a random order inside 500 ms total · a `statfig` counting up and pulsing |

The line is *what the motion is for*. Affordance motion answers **"is this thing interactive, and did
I just touch it?"** — a reader needs that answer at density 0 as much as at 100, so density has no
say. Content motion answers a question about the argument, and how much of it a deck wants is taste.

**The parameter stays, and this was tested.** On 2026-08-12 the owner asked whether the recommendation
was to drop density and let the build place gentle motion by judgement instead. It was not. Judgement
at build time gives the owner no knob, gives a review no reproducible artifact, and makes two builds
of one specification differ — the deck stops being diffable, which this project depends on
everywhere else. **The constraint below is a bound on what density may do, not a doubt about
having it.**

**Density is a budget, not a switch, and it must be deterministic.** At 10 the deck picks a small
number of eligible elements; at 100 it picks all of them. The selection has to be **stable across
rebuilds** — a deck that animates different things each time it is built cannot be reviewed, cannot
be compared byte for byte, and would fail the diff discipline this project already runs. Seeded from
something the deck already carries, never from a clock or an unseeded random.

**Density does not license non-conformant motion.** Every rule that binds motion today still binds at
100: **DS-141**'s 500 ms cap, **DS-142**'s ban on continuous ambient motion over static content,
**DS-143**, and above all **DS-150** — *every animation answers "what does this encode?"* Each motion
in the table earns its place under DS-150 on its own (an arrowhead encodes direction, a dot pop
encodes arrival, a highlight encodes *this is what I am pointing at*). Density decides **how much**
conformant motion runs, never whether a decorative motion is admitted. **No DS-140 amendment is
expected**; if a requested motion turns out not to fit the four, that is an amendment to argue
separately, not something density smuggles in.

**Scope**
- In: the `content` / `affordance` split, written into
  [`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) as a property every motion declares.
- In: `--motion-density`, a **theme token with a build-time override**. A token because rule 4 makes
  every value that could differ between themes one; overridable because the reporter wants it per
  deck.
- In: a deterministic, seeded selection rule, specified in
  [`build.md`](../skills/htmldeck/references/build.md) precisely enough that two builds of one
  specification animate the same elements.
- In: the four affordance motions in the table above, built.
- In: the two content motions in the table above, built — the arrowhead and the wobbly dot pop.
- In: **`prefers-reduced-motion` outranks density.** At 100 with reduced motion, the semantics
  survive (DS-143) — the dashed arrows stay dashed.
- In: **DS-218's stop control still applies at any density.** `Current` is infinite and is affordance
  motion, so density 0 does not switch it off; the deck's motion control is what stops it, and that
  control is therefore a compliance obligation rather than chrome. This is the constraint that binds
  [T-114](T-114-the-chrome-row-layout-the-pager-deserves-the-corner.md), and it is written in both.
- In: what `check.py` can decide — a motion with no declared kind, a duration over the cap, a
  selection that is not reproducible.
- Out: **slide transitions** — [T-111](T-111-a-named-slide-transition-chosen-per-deck.md). Navigation,
  not content.
- Out: a fifth named motion, 3D, and the frame-rate instrument —
  [T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md).
- Out: hover behaviour on data charts. There is no chart component yet
  ([T-113](T-113-evaluate-an-embeddable-chart-library-against-hand-authored-svg.md)).

**Inputs**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §5.2 — DS-140 through DS-150, and DS-218.
- [`docs/THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) — where the token is declared.
- [T-016](T-016-the-interaction-and-motion-layer.md) — the motion layer and its four named motions.
- [T-041](T-041-implement-the-nine-glitch-free-conditions.md) — density 100 is the case most likely to
  produce the glitches that task enumerates; the two are read together.
- [T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md) — **no deck in this
  repository has had its frame rate measured on any machine.** Density 100 on a dense deck is exactly
  where that matters.

**Acceptance criteria**
- [ ] Every motion in the shipping theme declares `content` or `affordance`, and `check.py` fails one
      that declares neither.
- [ ] Density 0 leaves every affordance motion running and every content motion still.
- [ ] Density 100 runs every eligible content motion and violates no rule in DS-140 to DS-150.
- [ ] Two builds of one specification at one density animate the same elements, proved by diffing the
      two outputs.
- [ ] The four affordance motions and the two content motions are built and each is looked at.
- [ ] With `prefers-reduced-motion` at density 100, the dashed arrows stay dashed and nothing moves.
- [ ] Demonstrated at density 0, 10 and 100 on a real 12-slide deck with diagrams, opened and looked
      at, offline.
- [ ] `python tools/deck/check.py` green at all three densities.

**Open questions**
- What density 10 selects *first* when a slide has several eligible elements. Decided during
  implementation from the rule's own reason — the argument's key figure before its decoration.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Classify every motion the shipping theme already runs as content or affordance | the split, applied to what exists |
| 2 | Write the split and the token into the ruleset and the theme contract | rows |
| 3 | Specify the seeded selection rule in `build.md` | the rule, reproducible |
| 4 | Build the four affordance motions | shell |
| 5 | Build the arrowhead and the dot pop | shell |
| 6 | Diff two builds at one density | determinism verdict |
| 7 | Render at 0, 10, 100; reduced-motion at 100 | four renderings, looked at |
| 8 | Extend `check.py` | gate |

## 3. Implement

**Decisions & assumptions**

- **`rise` is affordance motion, and counting settled it rather than argument** — 2026-08-19,
  and it is the decision the whole task rests on. §1's table gives examples, not a classification,
  and `rise` appears in neither column. The shipped decks carry **68, 58 and 33** risen elements
  against **1, 1 and 2** pulses — so a density governing `rise` would, at the default of 10, run six
  of a deck's sixty-eight entrances: *some elements of some slides arriving and the rest simply
  appearing.* That is not a quieter deck, it is an inconsistent one. And by the split's own test —
  *what is the motion for* — the entrance answers *the deck just moved and here is what it says now*,
  which is the arriving half of the gesture whose leaving half is DS-235's transition. Splitting one
  gesture across the two kinds would make the split describe the stylesheet rather than the reader.
  It was written as the classification to overturn first if any of this were wrong, and
  **the owner confirmed it on 2026-08-19** — so it is a ruling rather than an inference, and
  DS-237 says so. Everything else in this task follows from it.
- **Density is a rank, and the rank is derived** — 2026-08-19. `--m-rank` per content motion,
  `--motion-density` per theme, and a motion runs when the density reaches its rank. The rank is
  `floor((i-1)/n*100)+1` over `(tier, slide, document order)`, so the first always ranks 1 and runs
  at any density above 0, and 100 runs everything. Nothing reads a clock or an unseeded random.
- **The whole figure is one content motion, not one per mark** — 2026-08-19. Ranking each
  arrowhead separately would pop three of a diagram's five, which is the same incoherence that put
  `rise` on the other side of the split. It is also forced by the DOM: a `<marker>` renders in its
  own context and inherits from where it is *defined*, so a rank on the referencing line never
  reaches the arrowhead, and a matrix's dots interleave with its row labels and cannot be wrapped.
- **`--m-on` multiplies the duration, never removes the name** — 2026-08-19. A zero-duration
  animation still applies its fill state; removing the name would strand a risen element at
  `opacity:0`, which is DS-224's failure in a new place.
- **`min`/`max` rather than the CSS function that reads better** — 2026-08-19. DS-033 bans that
  function's name anywhere inside the stage, as the idiom for fluid type. This arithmetic is unitless
  and has nothing to do with type, but the rule is a prohibition on the construct rather than on the
  use, and evading it by argument is worse than writing the same thing twice as long. The ban is on
  the literal text, so a comment naming the function fails the check too.
- **The tier answers §1's open question** — 2026-08-19, *what density 10 selects first when a
  slide has several eligible elements*: the argument's key figure before its decoration. Pulse is
  tier 1, the arrowheads tier 2, the dot matrix tier 3. On `measure-first` that puts the **`0`** —
  the moment §1 names as the model, and the one nobody designed — at rank 1, so the shipped default
  runs exactly it and nothing else.

**What density does, measured across the whole span** (real Chrome, offline, 2026-08-19):

| Deck | Motion | rank | at 0 | at 10 | at 100 |
| :--- | :--- | ---: | :---: | :---: | :---: |
| `measure-first` | `.pulse` — the `0` | 1 | still | **runs** | **runs** |
| | `.pulse` — the safeguard | 34 | still | still | **runs** |
| | `.dot-pop` — 72 dot animations | 67 | still | still | **runs** |
| `reference-deck` | `.pulse` | 1 | still | **runs** | **runs** |
| | `.arrow-pop` — 4 arrowheads | 51 | still | still | **runs** |
| both | `rise`, `Current` — affordance | — | **runs** | **runs** | **runs** |

**Two defects, and both were found by looking rather than by any check.**

1. **At density 0 the matrix went blank.** A zero-duration animation still honours its **delay**,
   and `fill:both` paints the FROM keyframe for the whole of it — so a matrix switched off by
   density disappeared for 280 ms and then appeared, and an arrowhead for 120 ms. Density 0 has to
   mean no motion, not a late one. The delay is multiplied by the same `--m-on`, which collapses the
   animation to a single instant at t=0 where the fill lands on the end state. **The gate was green
   through all of it**: every rule about what may animate was satisfied by an animation that made
   the content vanish.
2. **A class literal inside a CSS comment was counted as a ninth figure.** `figures.py` counts
   `class="…fig…"` across the file, and a comment of mine explaining where `.arrow-pop` goes wrote
   one. Reworded; the tool is right to be literal and the fix belongs on the writing side.

**And one the gate caught that reading would not have.** DS-143 failed with *still animating under
reduced motion: 2 (arrowpop, arrowpop)* — the two new content motions had been written into the
motion-control collapse and not into the reduced-motion one. §1 says the preference outranks
density; it did not, on the two motions added the same afternoon.

**Outputs produced**
- [`shell/components.css`](../shell/components.css) — the split's documentation, `--motion-kind`
  on all nine motion rules, the `--m-on` gate, and the four new motions.
- [`shell/shell.html`](../shell/shell.html) — `.is-back` on the Previous pager, so a motion can
  carry a direction.
- [`themes/quarto.css`](../themes/quarto.css) — `--motion-density` and five dials.
- [`tools/deck/density.py`](../tools/deck/density.py) — the derivation, `list` / `check` / `write`,
  and DS-237, DS-238 and DS-239's rows.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-237, DS-238, DS-239.
- [`docs/THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) — six token rows.
- [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) — `.is-back`, `.arrow-pop`,
  `.dot-pop`.
- [`skills/htmldeck/references/build.md`](../skills/htmldeck/references/build.md) §2 — what a build
  declares, and that `--m-rank` is never written by hand.
- The three shipped decks, and the coverage figures across seven documents: **85 of 115 → 88 of 118**.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every motion in the shipping theme declares content or affordance, and `check.py` fails one that declares neither | **pass** | DS-237, `9 of 9` declared. The check finds every rule that *starts* a motion and skips every rule that stops one — a fixture holds it to that, because requiring a kind on each reduced-motion collapse would put the declaration everywhere and mean nothing |
| Density 0 leaves every affordance motion running and every content motion still | **pass** | §3's table, measured. And the *look* is what caught the version of this that passed every check while blanking the matrix |
| Density 100 runs every eligible content motion and violates no rule in DS-140 to DS-150 | **pass** | `check.py` green on a copy of the deck at 100 as well as at 0 — the gate normally sees only the shipped 10 |
| Two builds of one specification at one density animate the same elements, proved by diffing the two outputs | **pass, by a stronger route** | Ranking a ranked deck is byte-identical (`sha256` `aaf7426d8ddd989b` both times). But the claim is now carried by **derivation** rather than by a diff: `density.py check` recomputes the whole set and holds a deck **nobody rebuilt** to it, which a diff of two builds cannot do |
| The four affordance motions and the two content motions are built and each is looked at | **pass, with one limit stated** | Pager tilt and pinch, and the highlight fade, built; ruler ring and `Current` already existed. Arrowhead and dot matrix built and looked at mid-motion and settled. **A hover state cannot be photographed here** — the pointer is the one input this harness has none of — so the pager's two states were forced to the values their rules set and looked at, which shows the geometry and says nothing about the pointer triggering it |
| With `prefers-reduced-motion` at density 100, the dashed arrows stay dashed and nothing moves | **pass** | At density 100 under a forced-reduced-motion render: `stillAnimating = 0`, and the flow keeps `stroke-dasharray: 7px, 6px`. Measured at 0 as well, and the two agree |
| Demonstrated at density 0, 10 and 100 on a real 12-slide deck with diagrams, opened and looked at, offline | **pass** | On the 13-slide `reference-deck` and the 13-slide `measure-first`. At 10 the deck shows one moment — the `0` — and is otherwise still, which is the design target in one sentence |
| `python tools/deck/check.py` green at all three densities | **pass** | 0, 10 and 100. `python tools/check_all.py` green over the whole set |

**What this does not settle, and it is a judgement rather than a gap.** Whether 3° of tilt, a 1.18
overshoot and an 8 ms dot gap are the *right* values is taste, and a still frame is a poor witness
for it — the instrument can show that the motion is there and where it gets to, not whether it feels
gentle. They are theme tokens precisely so that answer can be changed without touching a rule.

**And one question this task shipped an answer to without being asked: is 10 the right default?** It is the figure §1 proposed and nothing since has tested it. What it now means concretely, which §1 could not have known, is that a deck shows **exactly one moment** — rank 1 and nothing else — because a deck carries so few content motions that the second is already at rank 34 or 51. So the default is closer to *one easter egg per deck* than to *a tenth of the motion*, and whether that is the intent is the owner's. `python tools/deck/density.py list <deck>` shows what any other value would turn on, and changing it is one token.

**Child fix tasks raised**
- none.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-22 | (shipped) | **`shipped_in` set to `0.5.0`, back-filled.** The field was never written, so this task read as belonging to no release while being closed. **Derived, not assumed**: the commit that set `status: done` is an ancestor of `v0.5.0`, which `git tag --contains` answers. Found while reading the unreleased set for `0.6.0` — eight tasks closed 2026-08-19 all carried an empty field, and a ninth ([T-187](T-187-open-the-motion-vocabulary-into-a-style-guide.md)) closed after the tag and belonged to `0.6.0` instead. |
| 2026-08-12 | → proposed | Created from the first adopting project's feedback on published `0.2.2`. Scoped around the content/affordance split rather than as "more animation", because the exemptions the owner listed are all affordances and that is what makes one parameter coherent. |
| 2026-08-12 | (no change) | Density questioned and kept. The owner read the note about what density must not do as a recommendation to drop it; it was the opposite. Reasons for keeping it written into §1 so the question does not have to be re-asked: a knob the owner owns, a reproducible artifact, and two builds of one specification that match. |
| 2026-08-12 | (no change) | The pager's hover and press motions are the one part of this that waits on [T-114](T-114-the-chrome-row-layout-the-pager-deserves-the-corner.md). Building them before the pager's shape is settled is building them twice. Not `blocked_by` — everything else here can start. |
| 2026-08-18 | (no change) | **Not started, and the reason is a gate rather than a preference.** Six of the eight acceptance criteria are readings of motion over time — *density 0 leaves every affordance motion running and every content motion still*, *each is looked at*, *nothing moves under reduced motion at density 100*, and the demonstration at three densities. Nothing in this environment has a running document timeline ([T-185](T-185-no-instrument-here-can-watch-an-animation-play.md)), so building this now would put a second large unverifiable change on the shared shell and leave it exactly where [T-111](T-111-a-named-slide-transition-chosen-per-deck.md) is. `blocked_by` set rather than a note, because this is a real gate and it should propagate. |
| 2026-08-19 | proposed → done | The split, the density, the derivation and the four motions. **`rise` is affordance**, and counting settled that rather than argument: 68, 58 and 33 risen elements against 1, 1 and 2 pulses, so a density governing rise would run six of sixty-eight entrances and leave a deck inconsistent rather than quiet. Density therefore governs the moment layered on top, and on `measure-first` rank 1 is the **`0`** §1 names as the model — the shipped default runs exactly it. Two defects found by looking, the sharper one a matrix that went blank at density 0 because a zero-duration animation still honours its delay; one more caught by DS-143, which the two new motions had been left out of. |
| 2026-08-19 | (no change) | **The owner confirmed the `rise` classification**, which was the one call this task put up for review. It is recorded in DS-237 as a ruling rather than as this task's reasoning, because the rule is `hard` and the next person to read it should not have to re-derive why the deck's most common motion sits on the side density cannot reach. No code changed: the classification was already what shipped. |
| 2026-08-19 | (no change) | **§4's other question is answered: 10 is not the default the owner wants.** Put to them with what 10 concretely does — one motion, not a tenth of them — the ruling was *"raise it to 100%. Initial tests better with recognizing all of them. Reducing it is a matter of optimization, later."* So the restraint this task designed for is deferred rather than rejected, and the figure moves while the motions are still being built and looked at. Carried by [T-188](T-188-raise-the-shipped-motion-density-default-to-100.md) rather than reopening this task, because the value is one token but is asserted as a fact in four documents. |
