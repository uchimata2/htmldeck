---
id: T-185
title: No instrument here can watch an animation play, so any rule about motion over time is unverifiable
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-111, T-112, T-041, T-057, T-183]
work_package: PH3
owner: the project owner
business_value: high
effort: m
created: 2026-08-18
updated: 2026-08-22
shipped_in: 0.5.0
deliverables: [tools/deck/render.py]
---

# T-185 — No instrument here can watch an animation play, so any rule about motion over time is unverifiable

## 1. Specify

**Outcome**
There is one command that renders a deck in a browser whose **document timeline actually runs**, and
reports what an animation did — that it started, that it ended, and what the element looked like part
way through. Today nothing here can answer any of those, so every rule about motion over time rests
on reading the CSS.

**Measured 2026-08-18, on three instruments**

| Instrument | What it does with a running CSS animation |
| :--- | :--- |
| the preview pane | `document.timeline.currentTime === 0`. `getAnimations()` reports `playState: "running"`, `currentTime: 0`, **forever**. A screenshot refuses: *the Browser pane is not displayed, so the page is not compositing frames* |
| `render.py` headless | **pins motion off before capturing**, by design (DS-221, and the settling problem its own docstring describes). Under `--virtual-time-budget` a 420 ms animation fires no `animationend` after 1.2 s of chained timeouts |
| Claude in Chrome | not connected in this environment |

The pane's reading is the sharp one: **an animation reported as `running` whose `currentTime` never
leaves 0** is an instrument that says yes to every question about whether motion works. It is
**L-110**'s dead instrument with a different face — the tell is not a picture that fails to change,
it is a clock that does not tick.

**What this actually blocks.** It is not one task's inconvenience:

- [T-111](T-111-a-named-slide-transition-chosen-per-deck.md) is built, gated and green, and is held
  at `in_progress` because *the transition has never been seen to play*.
- [T-112](T-112-motion-density-and-the-split-between-content-and-affordance-motion.md) is about
  motion density, which is a claim about several animations at once.
- [T-041](T-041-implement-the-nine-glitch-free-conditions.md)'s conditions are largely about what
  happens *during* a change.
- [T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md) needs a frame rate,
  which is the same measurement one level harder.

**Why `high`.** The project's own rule is that a deck is looked at (`CLAUDE.md` rule 6), and for
motion that is currently impossible rather than merely skipped. A gate that is green on a deck whose
motion has never run is exactly the shape of **L-05**, and four open tasks depend on it.

**Scope**
- In: making at least one instrument advance a real timeline, and proving it does — the proof is a
  reading that *changes*, not a run that succeeds.
- In: reporting an animation's lifecycle: did it start, did it end, and one sampled state part way
  through.
- In: a way to capture a deck **mid-transition** on purpose. `render.py` pins motion off for good
  reasons; this needs the opposite, and it needs to be a different verb rather than a flag that
  weakens the existing guarantee.
- Out: changing DS-221 or the reasons captures pin motion off. The default stays; this adds a
  deliberate exception with its own name.
- Out: a frame-rate figure. That is T-057's, and it needs this first.

**Inputs**
- [`tools/deck/render.py`](../tools/deck/render.py) — the Chrome runner, the virtual-time budget,
  and the settling problem it documents.
- [`docs/lessons/L-110.md`](../docs/lessons/L-110.md) — the instrument that fails silently.
- [T-111](T-111-a-named-slide-transition-chosen-per-deck.md) §3 — the three readings above, in the
  terms they were taken.

**Acceptance criteria**
- [ ] One command renders a deck with a timeline that advances, proved by a reading that changes
      between two samples of the same page
- [ ] It reports, for a named animation: started, ended, and one intermediate state
- [ ] It can capture a deck mid-transition, and the capture is visibly different from the settled one
- [ ] The existing motion-pinned capture path is unchanged and still the default
- [ ] T-111's transition is verified through it, and T-111 closes

**Open questions**
- Whether the answer is a different Chrome invocation (no virtual-time budget, a real timeline, a
  screenshot on a timer) or a different instrument entirely. The first is cheap to try and should be
  tried first.

**One fallback is not an agent's to take, and it is worth knowing before the attempt.** If the
Chrome-invocation route fails, the remaining instrument is the real browser named in the table
above, and connecting it is the **owner's** action rather than this task's: the extension has to be
installed and signed in under the same account. So a run can legitimately reach the end of the cheap
path and stop with nothing left to try. **That is a clean stopping point, not a failure**, and it
should be reported as one rather than worked around with a weaker instrument.

## 2. Plan

**Take the cheap path first, as §1's open question says: a different Chrome invocation.** Four of
them, on a page carrying one 420 ms animation, and the test is whether **any reading moves**.

**Then, if nothing moves, ask a different question of the same browser.** A CSS animation is an
`Animation` object with a settable `currentTime`, and setting it is not the timeline running —
but if the computed style follows the seek, then the keyframes, the timing function and every
intermediate state are measurable without a frame ever being produced. That is a smaller claim than
§1's Outcome and it answers all three of the questions the Outcome's second half asks.

**Steps**
1. Four invocations, one page, one animation. Report which readings move.
2. If the animation clock does not run, test whether it seeks.
3. Build the verb on whichever works, and be exact in its own docstring about what it proves.
4. Verify T-111's transition through it.

## 3. Implement

**The measurement the task asked for, and it settles the question in a way §1 did not expect.**
One page, one 420 ms linear animation on `transform`/`opacity`, four invocations of the same Chrome
`render.py` already uses:

| Invocation | `document.timeline.currentTime` | animation `currentTime` | `animationstart` / `end` |
| :--- | :--- | :--- | :--- |
| as `render.py` runs it | 0, 0, 0, 0 | 0 | neither fired |
| no virtual-time budget | — the dump happened before the timer | — | — |
| budget + `--run-all-compositor-stages-before-draw` | 0, 0, 0, 0 | 0 | neither fired |
| budget + **`--disable-gpu`** | **0, 0, 199.99, 899.96** | 0 | neither fired |

A second pass added a **main-thread** property (`width`) beside the compositor one, and it made no
difference: with `--disable-gpu` the document timeline advances and **no animation advances with
it**, on either property. So the finding is sharper than *headless cannot watch motion*:

> **The clock a CSS animation runs on is frame production, not time.** Headless produces no frames,
> so `document.timeline` can be made to tick and every animation on the page still sits at 0.

**So the verb seeks.** A third pass set `currentTime` explicitly and read the computed style back:
opacity 0, 0.25, 0.5, 0.75, 1 at five offsets of a linear fade, and an eased `width` reading
286.67 px at 25% rather than the 137.5 px a straight line would give — the curve, not an
approximation of it. The Web Animations API is the instrument; the seek is the movement.

**Decisions & assumptions**
- **`motion` is a verb, not a flag on `shots`** — 2026-08-19, and §1's scope requires it.
  `PROBE`'s `quiet` half pins motion off for DS-221's reasons; putting the guarantee and its
  exception in one place is how the next edit reaches both. `MOTION_PROBE` is separate and the
  self-test fails if it ever contains `animation:none`.
- **Report per animation as a fraction of its own duration; capture on one absolute clock** —
  2026-08-19. They are different questions. A lifecycle is *this* animation's, where a fraction is
  the right unit. A frame is the page's, and this page's animations are staggered at delays 0, 60,
  120, 180, 240 and run for 340, 420, 1200 and 4500 ms — so seeking each to the same fraction
  composites moments that never co-occur and produces something that **looks exactly like a frame**.
  The capture takes an absolute `t` and puts each animation at `t - delay`.
- **Only the animations the navigation created ride its clock** — 2026-08-19, and this was
  found by looking at the output rather than by reasoning. The first capture at `t = 0` came out
  nearly blank: the slide being left had finished its own `rise` animations long before, they carry
  `fill: both`, and seeking them to 0 rewound them to their invisible start. **Nothing in a frozen
  clock distinguishes a finished animation from one that has not begun** — both read
  `currentTime: 0` — so the probe takes the animation set *before* the click, and what is new
  belongs to the navigation while what was there is put at its end. That is **L-122**.
- **`--back` exists because DS-235 names two keyframes** — 2026-08-19. Direction follows the
  navigation, so the only way to reach `slide-leave-back` is to arrive at a slide by going back to
  it. Advance one further, then take Previous.
- **The clock's span is stated, and taken over the navigation's own finite animations** —
  2026-08-19. DS-140's `Current` loops at 4500 ms on a slide nobody is looking at; letting it into
  the span puts every offset past the end of a 420 ms transition, and five captures of a settled
  page look exactly like five captures of a transition that does not move. `motion_span` is pure
  and holds a fixture for exactly that.
- **What a green run does not prove, said in the docstring rather than assumed** —
  2026-08-19. Frame rate, dropped frames and compositor behaviour are all downstream of frame
  production. T-057's figure still needs a real browser, and §1's owner-only fallback is
  therefore **not** spent: it was the fallback for the cheap path failing, and the cheap path
  reached further than expected rather than all the way.

**T-111's transition, measured for the first time.** Forward, on the reference deck:

| seek | opacity | transform |
| ---: | ---: | :--- |
| 0 ms | 1 | `matrix(1, 0, 0, 1, 0, 0)` |
| 105 | 0.870838 | `matrix(0.99225, 0, 0, 0.99225, -14.864, 0)` |
| 210 | 0.5 | `matrix(0.97, 0, 0, 0.97, -57.54, 0)` |
| 315 | 0.129162 | `matrix(0.94775, 0, 0, 0.94775, -100.216, 0)` |
| 420 | 0 | `matrix(0.94, 0, 0, 0.94, -115.08, 0)` |

Backward is the same curve mirrored — `+115.08` at 420 ms instead of `-115.08`, which is
DS-235's *left when advancing, right when going back* measured rather than read. **Exactly one
animation targets a `section.slide`**, and it is the outgoing one; the incoming slide carries no
transition of its own, which is DS-235's asymmetry holding.

**Outputs produced**
- [`tools/deck/render.py`](../tools/deck/render.py) — `motion`, `MOTION_PROBE`, `motion_span`,
  `--into` / `--at` / `--back` / `--shots`, and four self-test fixtures.
- [`docs/lessons/L-122.md`](../docs/lessons/L-122.md) — a frozen clock makes a finished thing
  and an unstarted thing read alike.
- [`examples/README.md`](../examples/README.md) and
  [`skills/htmldeck/references/build.md`](../skills/htmldeck/references/build.md) — the verb,
  and the boundary of what it proves.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :--- | :--- |
| One command renders a deck with a timeline that advances, proved by a reading that changes between two samples | **partly — and the part that fails is the finding** | `--disable-gpu` does make `document.timeline.currentTime` advance (0, 0, 199.99, 899.96), which is literally the proof asked for; **and no animation advances with it**, on a compositor property or a main-thread one. The reading that changes is the seek, not the clock §3 |
| It reports, for a named animation: started, ended, and one intermediate state | **pass** | Name, duration, easing, fill, delay, iterations, and the computed state at any offsets asked for. Start and end are the 0% and 100% rows |
| It can capture a deck mid-transition, and the capture is visibly different from the settled one | **pass** | Five frames on one clock across a 580 ms navigation, 119–134 KB and each different. Looked at offline: at 0 ms the outgoing slide is settled, at 145 ms it is shrinking and sliding left under the arriving headline, at 580 ms the new slide is settled |
| The existing motion-pinned capture path is unchanged and still the default | **pass** | `PROBE` untouched; `shots` re-run and identical in behaviour. The self-test fails if `MOTION_PROBE` ever pins motion off |
| T-111's transition is verified through it, and T-111 closes | **the transition is verified; T-111 is left to close itself** | Both keyframes measured — §3's table and its mirror. T-111 is **not** closed here: its criteria also cover keys and ruler-jump navigation, reduced motion, and a duration the criterion states as 500 ms against a measured 420. Closing it inside this task would be asserting five criteria nobody checked, which is the shape this task exists to remove. It is unblocked and is the next task |

**On §1's owner-only fallback.** It is **not** spent. It was the fallback for the cheap path
failing; the cheap path reached an instrument that seeks, which is further than expected and less
than the Outcome's first clause. A real browser is still what a frame rate needs (T-057), and
connecting one is still the owner's action.

**Child fix tasks raised**
- none. The one thing this cannot reach — playback at a real frame rate — already has a task
  in [T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md), which names it.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-22 | (shipped) | **`shipped_in` set to `0.5.0`, back-filled.** The field was never written, so this task read as belonging to no release while being closed. **Derived, not assumed**: the commit that set `status: done` is an ancestor of `v0.5.0`, which `git tag --contains` answers. Found while reading the unreleased set for `0.6.0` — eight tasks closed 2026-08-19 all carried an empty field, and a ninth ([T-187](T-187-open-the-motion-vocabulary-into-a-style-guide.md)) closed after the tag and belonged to `0.6.0` instead. |
| 2026-08-18 | → proposed | Raised out of [T-111](T-111-a-named-slide-transition-chosen-per-deck.md), which is built and green and cannot be closed because nothing here can watch it move. Three instruments measured and all three refuse in different ways; the pane's is the one worth remembering, since it reports an animation as `running` at `currentTime: 0` indefinitely rather than failing. `PH3` by [`../CLAUDE.md`](../CLAUDE.md)'s rule — no published deck is broken, but four open tasks are held behind it. |
| 2026-08-19 | → done | `render.py motion`, on the cheap path, and it settled the question differently from how §1 framed it. `--disable-gpu` makes the document timeline advance and **no animation advances with it** — the clock a CSS animation runs on is frame production, not time, and headless produces no frames. So the verb **seeks**: the computed style follows `currentTime` exactly, which makes every intermediate state measurable and a transition something a person can look at. Two defects in the instrument found by looking at its own output, the second being **L-122**. T-111's transition measured in both directions; T-111 itself left to close against its own criteria. |
