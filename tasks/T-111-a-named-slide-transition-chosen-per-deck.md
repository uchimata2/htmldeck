---
id: T-111
title: A named slide transition, chosen per deck, with slide and immediate as the shipping pair
type: deliverable
status: done
phase: review
parent: null
blocked_by: []
related: [T-016, T-041, T-057, T-112, T-185]
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-08-12
updated: 2026-08-22
shipped_in: 0.5.0
deliverables:
  - shell/deck.js
  - shell/components.css
  - docs/DESIGN-SYSTEM.md
  - docs/THEME-CONTRACT.md
---

# T-111 — A named slide transition, chosen per deck, with slide and immediate as the shipping pair

## 1. Specify

**Outcome**
Moving between slides is a chosen effect rather than whatever the stylesheet happens to do. A deck
names its transition; two are available, both conformant; the duration is a token.

**The two**

**`slide`.** The outgoing slide shrinks slightly, gains a soft drop shadow, and eases out to the left
when advancing or to the right when going back. **The incoming slide does not animate** — it is
revealed, as though it had been there all along. That asymmetry is the design, not a simplification
of it: two slides moving at once is the mush that makes presentation-software transitions read as
cheap, and animating one halves the cost on a dense slide.

**`immediate`.** No transition. Named, so that choosing nothing is a decision a deck records rather
than a default nobody examined.

**Default duration 500 ms**, a theme token. That lands exactly on **DS-141**'s cap, and DS-141
already reserves 400–500 ms for an inter-slide transition — this task builds the thing the rule was
written for.

**What is deliberately not here**
The owner ruled on 2026-08-12: **no book-page curl and no explosion.** Both are to be brainstormed
separately and neither is in scope. For the record of why the question arises at all: **DS-144**
forbids 3D slide transitions and flashy cuts, so the curl needs an amendment; the explosion needs
that *and* a **DS-150** answer to *what does this encode?*, which it does not have, *and* it is
per-element transforms across a dense slide at a frame rate this project has never measured on any
machine ([T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md)). Recorded so
the brainstorm starts from the constraints rather than rediscovering them.

**Scope**
- In: `slide` and `immediate`, named in [`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) as a closed
  vocabulary, extensible only by amendment.
- In: direction taken from the navigation direction, including the ruler's jumps — a jump backwards
  by six slides is still backwards.
- In: duration and easing as theme tokens.
- In: **`prefers-reduced-motion` collapses any transition to `immediate`** (DS-143), and the deck
  still navigates.
- In: transitions pinned off for print and for headless capture — DS-224 and DS-221 both already
  require this of motion, and a transition is the case they were written before.
- In: what happens when a reader advances mid-transition. A queued or interrupted transition that
  leaves two slides visible is a glitch, and [T-041](T-041-implement-the-nine-glitch-free-conditions.md)
  owns the general form of that.
- Out: **the book curl and the explosion.** Owner's decision, 2026-08-12.
- Out: **motion density** — [T-112](T-112-motion-density-and-the-split-between-content-and-affordance-motion.md).
  A transition is navigation, not content motion, and density does not select it.
- Out: a per-slide transition override. One deck, one transition.

**Inputs**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §5.2 — **DS-140** (the closed four-motion
  vocabulary, which a transition sits outside), **DS-141** (the 400–500 ms reservation), **DS-143**,
  **DS-144**, **DS-221**, **DS-224**.
- [`shell/deck.js`](../shell/deck.js) — `go()`, and the ruler's jump path.
- [T-016](T-016-the-interaction-and-motion-layer.md) — the motion layer this extends.

**Acceptance criteria**
- [ ] Both transitions are named in the ruleset and selectable per deck.
- [ ] `slide` animates only the outgoing slide, and the direction follows navigation direction in all
      three navigation paths — keys, pager, ruler jump.
- [ ] Duration and easing are theme tokens; the default is 500 ms.
- [ ] With `prefers-reduced-motion`, both behave as `immediate`.
- [ ] A printed deck and a headless capture show no transition state.
- [ ] Advancing twice inside one transition leaves exactly one slide visible.
- [ ] Demonstrated on a real 12-slide deck with diagrams, opened and looked at, offline.
- [ ] `python tools/deck/check.py` green; `render.py` green.

**Open questions**
- None. The two-transition scope is the owner's decision of 2026-08-12.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Write the vocabulary and the tokens into the ruleset and theme contract | rows |
| 2 | Build `slide`, outgoing-only, direction-aware | `deck.js`, `components.css` |
| 3 | Wire reduced-motion, print and capture to `immediate` | three paths |
| 4 | Interrupt it — advance mid-transition, jump mid-transition | glitch verdict |
| 5 | Run it on a real 12-slide deck and look at it offline | verdict |

## 3. Implement

**Decisions & assumptions**
- 2026-08-12 — owner: build `slide` and `immediate` only. Book curl and explosion deferred to a
  separate brainstorm, not declined outright.
- **The choice lives in the theme, not on `<html>`** — 2026-08-18. The first cut put
  `data-transition="slide"` on the root element and it was wrong: `<html>` is *shell*, carried byte
  for byte by `sync`, so an attribute there is every deck's and no deck's own. `--slide-leave-fwd`
  and `--slide-leave-back` name the keyframe — or `none`, which is `immediate` — and the theme
  region is the one a deck varies.
- **A keyframe, not a transition** — 2026-08-18. A transition needs its start state painted in one
  frame and its end state in the next, so it silently does nothing when both land in the same
  frame. An animation carries its own `from`, so it cannot no-op quietly (**L-110**'s shape).
- **The incoming slide's cross-fade was removed** — 2026-08-18. `.slide` carried
  `transition:opacity` since the beginning, which animates the *incoming* slide; §1 says it is
  revealed. Two slides moving at once is what the asymmetry exists to avoid, so keeping the fade
  would have shipped half the rule.
- **Longhands, not the `animation` shorthand** — 2026-08-18, and this was measured rather than
  chosen. See below.
- **Correctness does not depend on `animationend`** — 2026-08-18. The mark is cleared by the next
  `go()` as well, so a missed event tidies late rather than stranding a slide.

**Outputs produced**
- [`shell/components.css`](../shell/components.css) — the two keyframes, the leaving rules, and the
  collapse to `immediate` under reduced motion and under the motion control.
- [`shell/deck.js`](../shell/deck.js) — `go()` marks the outgoing slide with the direction
  *navigation* took, and clears every previous mark first.
- [`themes/quarto.css`](../themes/quarto.css) — five tokens; `--slide-dur` default now **500 ms**.
- [`docs/THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) — five rows.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — **DS-235**, the closed vocabulary.
- [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) — the motion-token rows, which moved
  from `.slide` to `.slide[data-leaving]` and its keyframes.

**What measuring found that reading would not have.**

- **The `animation` shorthand is ambiguous when the token is `none`.**
  `animation:none 420ms ease forwards` computes to `animation-name: forwards` — the parser takes
  `none` for a fill-mode and the next keyword for the name. `immediate` therefore worked *by
  accident*: there is no `@keyframes forwards`, so nothing ran. It would have broken the day
  somebody wrote one, silently. Longhands now; `animation-name` cannot be read as anything else.
- **The drop shadow failed DS-011.** `0 24px 60px rgba(0,0,0,.18)` put a colour literal in a
  `:root` block, which is what that rule counts. Rebuilt from the tokens that already exist —
  `0 var(--shadow-y) var(--shadow-blur) var(--shadow)` — which is what a shadow should have been
  written as regardless.
- **DS-229 caught the contract going stale in the same edit.** Moving the transition off `.slide`
  left the contract claiming `.slide` reads `--slide-dur`, and it no longer does.

**What is verified, and how.** Computed styles read true in a non-compositing pane, so these are
sound:

| Property | Result |
| :--- | :--- |
| direction, pager forward | `data-leaving="fwd"` on the outgoing slide |
| direction, ruler jump backwards | `data-leaving="back"` — the jump is 2 → 0 and it is still *back* |
| interrupt: advance twice inside one transition | exactly **one** slide marked leaving, the first mark cleared |
| `immediate` (`--slide-leave-fwd:none`) | `animation-name:none`, slide `opacity:0 visibility:hidden` |
| motion control off | `animation-name:none`, slide hidden |
| reduced motion | `check.py` DS-143 passes on a forced-reduced-motion render |
| the whole gate | `check.py` green on all three decks |

**Closed 2026-08-19, on the instrument
[T-185](T-185-no-instrument-here-can-watch-an-animation-play.md) built.** The paragraph below is
what was true on 2026-08-18 and is kept because it is why this task waited; §4 carries what the
instrument then measured. Two things it found that the 2026-08-18 table could not:

- **the transition's own curve, in both directions** — the outgoing slide scales 1 → 0.94 and
  translates 0 → −115.08 px going forward, and 0 → **+115.08** going back, over 420 ms with
  opacity 1 → 0. Mirrored exactly, which is DS-235's *left when advancing, right when going back*
  measured rather than read;
- **exactly one animation targets a `section.slide`**, and it is the outgoing one. *The incoming
  slide does not animate* was an inference from the CSS; it is now a reading.

**What is NOT verified, and why the task stays open.** **No instrument in this session has a running
document timeline**, so nothing here can watch the transition actually play:

- the preview pane reports `document.timeline.currentTime === 0` and refuses a screenshot with
  *the Browser pane is not displayed, so the page is not compositing frames* — a frozen timeline,
  on which `getAnimations()` reports `playState: "running"` with `currentTime: 0` forever;
- `render.py`'s headless runner pins motion off before it captures, by design, and under
  `--virtual-time-budget` the same animation never fires `animationend`;
- Claude in Chrome, the one real compositing browser available, is not connected.

So three of §1's criteria — the visual demonstration, the printed deck, and *animates only the
outgoing slide* as a thing seen rather than inferred — cannot be closed today. `CLAUDE.md` rule 6
and `tasks/TASK-WORKFLOW.md` §7 step 3 both say a task does not reach `done` on a green gate, so it
does not. [T-185](T-185-no-instrument-here-can-watch-an-animation-play.md) carries the instrument.

## 4. Review

Re-measured 2026-08-19 in real Chrome, offline, on the 13-slide reference deck. Every row is a
reading taken that day rather than carried from §3.

| Acceptance criterion | Result | Note |
| :--- | :--- | :--- |
| Both transitions named in the ruleset and selectable per deck | **pass** | DS-235 names both. `immediate` selected the way a deck selects it — `--slide-leave-fwd:none` — computes `animation-name:none` and the leaving slide goes straight to `opacity:0 visibility:hidden` |
| `slide` animates only the outgoing slide, and the direction follows navigation in all three paths — keys, pager, ruler jump | **pass** | Keys: `ArrowRight` → `slide-leave-fwd`, `ArrowLeft` → `slide-leave-back`. Pager: `fwd`. Ruler: forward to slide 5 → `fwd`, then a **four-slide jump backwards** → `back`. Direction is the navigation's, not the slide numbers'. And only one animation targets a `section.slide` — T-185 §3 |
| Duration and easing are theme tokens; the default is 500 ms | **pass, with the deck's own value recorded** | `themes/quarto.css` carries `--slide-dur:500ms`. All four decks here carry **420 ms**, which the tokens exist to allow — `shell/deck.js` says so in its own words, *a deck may set `--slide-dur` to anything the contract allows*, and 420 is inside DS-141's 400–500 ms reservation. Computed on the deck: `0.42s / ease-in-out / forwards` |
| With `prefers-reduced-motion`, both behave as `immediate` | **pass** | Every one of the five navigations above, re-run under `--force-prefers-reduced-motion`: `animation-name:none`, `0s`, `fill:none`, `opacity:0 visibility:hidden`. The deck still navigates, which is the half of DS-143 a `display:none` would have broken |
| A printed deck and a headless capture show no transition state | **pass** | Measured rather than reasoned: the deck was put into the state that should break it — motion **off**, one page turned, so the mark cannot be cleared by `animationend` and the leaving slide computes `opacity:0 visibility:hidden` on screen — and then printed. **All 14 pages are identical to a plain print**, ink and character count. What saves it is `@media print`'s `.slide{opacity:1!important;visibility:visible!important}`, written for DS-224 rather than for this, and `!important` outranks an animation's own fill state |
| Advancing twice inside one transition leaves exactly one slide visible | **pass** | Two `next` clicks with no wait: **one** slide marked leaving, and 2 slides computing `visible` — the arriving one and the one leaving, which is the transition rather than a stranded slide. Under reduced motion the same two clicks leave **1** visible, the leaving slide already hidden |
| Demonstrated on a real 12-slide deck with diagrams, opened and looked at, offline | **pass** | Five frames across the 580 ms navigation on the 13-slide reference deck, looked at: at 0 ms the outgoing slide is settled, at 145 ms it is smaller and sliding left under the arriving headline, at 290 ms it is a ghost, at 580 ms the new slide is settled and the old one is gone |
| `python tools/deck/check.py` green; `render.py` green | **pass** | `python tools/check_all.py` green over the whole set |

**One thing the re-measurement cost, and it is worth writing down.** The first keyboard reading said
the arrows do not navigate at all — and the fault was the probe. A synthetic `KeyboardEvent`
dispatched on `document` gives a listener a `Document` as `e.target`, and the handler's first line
is `e.target.matches('input,textarea')`, which a Document does not have. The listener threw and the
deck sat still, which reads exactly like a broken key binding. Dispatched on `document.body`, where
a real key press lands, all four bindings work. **A negative result from an instrument nobody
checked is not evidence** — the same shape as **L-06** and **L-110**, one level down.

**Child fix tasks raised**
- none.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-22 | (shipped) | **`shipped_in` set to `0.5.0`, back-filled.** The field was never written, so this task read as belonging to no release while being closed. **Derived, not assumed**: the commit that set `status: done` is an ancestor of `v0.5.0`, which `git tag --contains` answers. Found while reading the unreleased set for `0.6.0` — eight tasks closed 2026-08-19 all carried an empty field, and a ninth ([T-187](T-187-open-the-motion-vocabulary-into-a-style-guide.md)) closed after the tag and belonged to `0.6.0` instead. |
| 2026-08-12 | → proposed | Created from the first adopting project's feedback on published `0.2.2`. Four transitions were requested; the owner cut it to two the same day and deferred the other two to a brainstorm. The DS-144 and DS-150 collisions are recorded in §1 so the brainstorm starts from them. |
| 2026-08-18 | proposed → in_progress | Built. The transition is the outgoing slide's alone — the incoming cross-fade that had been there since the beginning is gone, because §1 says the incoming slide is *revealed* and keeping the fade would have shipped half the rule. The choice moved from an attribute on `<html>` to a pair of theme tokens once it was clear `<html>` is shell and `sync` carries it byte for byte, so no deck could have chosen. Direction and interrupt behaviour are measured and correct, including a ruler jump backwards. Three defects came out of measuring rather than reading: the `animation` shorthand parsing `forwards` as the animation name when the token is `none`, a shadow literal failing DS-011, and the component contract still claiming `.slide` reads the transition tokens. |
| 2026-08-18 | (no change) | **Held open on the instrument, not on the work.** Nothing available here has a running document timeline — the preview pane reports `document.timeline.currentTime === 0` and will not composite, `render.py` pins motion off before capturing, and Claude in Chrome is not connected. So the deck cannot be *looked at* moving, and `CLAUDE.md` rule 6 is the bar. Raised [T-185](T-185-no-instrument-here-can-watch-an-animation-play.md); this closes behind it. |
| 2026-08-18 | in_progress → blocked | The implementation is finished and the gate is green; what is missing is a look, and no instrument here can give one. `blocked` rather than `in_progress` because nothing further can be done on this task until [T-185](T-185-no-instrument-here-can-watch-an-animation-play.md) lands — which is what that status is for, and the dependency propagates so nothing downstream reads this as available. |
| 2026-08-19 | blocked → in_progress | [T-185](T-185-no-instrument-here-can-watch-an-animation-play.md) closed, so the transition can be looked at. Its measurement of this deliverable is in T-185 §3; what remains here is this task's own criteria, which reach further than the transition curve. |
| 2026-08-19 | in_progress → done | Closed on [T-185](T-185-no-instrument-here-can-watch-an-animation-play.md)'s instrument, and every criterion re-measured rather than carried forward. The curve is now a reading in both directions, mirrored; all three navigation paths give the direction the navigation took, including a four-slide ruler jump backwards; reduced motion collapses every path; and the print criterion was settled by **printing the state that should break it** — motion off, one page turned — and finding all 14 pages identical to a plain print. The deck's 420 ms against the theme's 500 ms default is the token working, and is recorded rather than changed. |
