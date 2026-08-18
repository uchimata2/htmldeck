---
id: T-112
title: Motion density, and the split between content motion and affordance motion
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: [T-185]
related: [T-016, T-041, T-057, T-111]
work_package: PH3
owner: the project owner
business_value: high
effort: l
created: 2026-08-12
updated: 2026-08-18
deliverables:
  - shell/deck.js
  - shell/components.css
  - docs/DESIGN-SYSTEM.md
  - docs/THEME-CONTRACT.md
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
- 2026-08-12 — owner: density 0–100, default 10; affordance motion exempt. Recorded from the feedback
  verbatim in §1 because the design target is a matter of taste and the wording is the specification.

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
| 2026-08-12 | → proposed | Created from the first adopting project's feedback on published `0.2.2`. Scoped around the content/affordance split rather than as "more animation", because the exemptions the owner listed are all affordances and that is what makes one parameter coherent. |
| 2026-08-12 | (no change) | Density questioned and kept. The owner read the note about what density must not do as a recommendation to drop it; it was the opposite. Reasons for keeping it written into §1 so the question does not have to be re-asked: a knob the owner owns, a reproducible artifact, and two builds of one specification that match. |
| 2026-08-12 | (no change) | The pager's hover and press motions are the one part of this that waits on [T-114](T-114-the-chrome-row-layout-the-pager-deserves-the-corner.md). Building them before the pager's shape is settled is building them twice. Not `blocked_by` — everything else here can start. |
| 2026-08-18 | (no change) | **Not started, and the reason is a gate rather than a preference.** Six of the eight acceptance criteria are readings of motion over time — *density 0 leaves every affordance motion running and every content motion still*, *each is looked at*, *nothing moves under reduced motion at density 100*, and the demonstration at three densities. Nothing in this environment has a running document timeline ([T-185](T-185-no-instrument-here-can-watch-an-animation-play.md)), so building this now would put a second large unverifiable change on the shared shell and leave it exactly where [T-111](T-111-a-named-slide-transition-chosen-per-deck.md) is. `blocked_by` set rather than a note, because this is a real gate and it should propagate. |
