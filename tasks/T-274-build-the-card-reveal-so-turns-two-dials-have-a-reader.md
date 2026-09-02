---
id: T-274
title: Build the card reveal, so DS-140's Turn is a component rather than two dials
type: deliverable
status: done
phase: review
parent: null
blocked_by: []
related: [T-242, T-275]
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-08-29
updated: 2026-08-29
shipped_in: 0.7.0
deliverables: []
---

# T-274 — Build the card reveal, so DS-140's Turn is a component rather than two dials

## 1. Specify

**Outcome**
`--turn-dur` and `--turn-ease` have a reader. DS-140 names four motions as a starter set — *what a
deck gets without designing anything* — and Turn, a card reveal, is the one no deck has ever built:
both themes declare its two dials, all five tracked decks carry them, and `var(--turn-dur)` appears
nowhere in the tree. [`COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) §5 sends an author
wanting an overshoot on a card reveal to `--turn-ease`, which today changes nothing.

**Closes** `PR-36`'s Turn half in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) §3.
`PR-36`'s other half — `--scale-ease`'s cell naming a reader that left — was fixed by
[T-242](T-242-the-contracts-against-the-checkers-that-decide-them.md) on 2026-08-29.

**Ruled by the owner, 2026-08-29.** The question was *build the component, or retire the two tokens
and let DS-140's set lose a name*, put with retirement recommended as the cheaper answer. **The owner
chose to build it**, which makes the starter set true rather than shorter.

**Scope**
- In: the component — a card reveal in `shell/components.css`, its keyframes, and the rows it owes
  in [`COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) §3.8 and its parts table
- In: what every content motion owes: `--motion-kind`, a `--m-rank` under DS-239, the reduced-motion
  and preflight collapses, and DS-141's cap without a licence
- In: a deck that uses it, or the reveal is unfalsifiable in the same way the tokens were
- Out: **DS-140's set.** Its four names are unchanged; this makes the fourth one real
- Out: the deck rebuild. Adding to the shared block invalidates all five tracked decks, and
  [`REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) rebuilds them once, in **B12**

**Inputs**
- `PR-36` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) §3
- [`docs/THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) §3.6 — the two dials and their bands
- [T-198](T-198-give-affordance-motion-its-own-band-faster-than-content-motion.md), which moved three
  rules **off** Turn's pair in 2026-08-20 and is why nothing reads it now
- `component.unrowed_motions`, added by [T-242](T-242-the-contracts-against-the-checkers-that-decide-them.md):
  a new rule animating on a token fails the gate until it has a row, so the row is not optional

**Acceptance criteria**
- [x] `var(--turn-dur)` and `var(--turn-ease)` are read by a component in the shared block
- [x] the component has its rows, and `component.py check` is green on every tracked deck
- [x] the reveal is visible in a deck, and the look it owes is queued in
      [`docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md)
- [x] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- **Which deck carries the first card reveal, and on which slide.** Answerable by whoever builds it;
  it is a composition decision, not a rule question.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Build `.turn` on the two dials it has, and nothing else | `shell/components.css` |
| 2 | **Let the new DS-224 check fire on it before collapsing it** — the component is the first real test of T-232's mechanism | the measurement |
| 3 | The four collapses and the density rank a content motion owes | `shell/components.css` |
| 4 | The contract rows, without which `unrowed_motions` fails the gate | `docs/COMPONENT-CONTRACT.md` |
| 5 | Put the first card reveal in a deck, and re-derive the ranks with the tool that owns them | `examples/reference-deck.html` |
| 6 | **Measure that both dials reach the animation**, which is the finding | the probe |
| 7 | Queue the look; close the register row and the theme contract's two cells | `docs/OWED-LOOKS.md`, `docs/PRE-RELEASE-AUDIT.md`, `docs/THEME-CONTRACT.md` |

## 3. Implement

**Decisions & assumptions**

- **Turn is exactly its two dials and adds no third — 2026-08-29.** The obvious card reveal is a
  rotation, and an angle is a magnitude that would want a token, which would mean two new theme
  rows for a component built to close a finding about unread tokens. So the reveal scales from its
  own centre line: `scaleY(0)` to `scaleY(1)`, endpoints rather than magnitudes, on `dotpop` and
  `arrowpop`'s precedent. `--rise-dist` and `--open-squash` are what a magnitude looks like here,
  and Turn has none.
- **It is gated on `data-arrived`, and it is that attribute's first reader — 2026-08-29.**
  [T-268](T-268-three-chrome-and-timing-defects-in-deck-js.md) built it in the same batch and
  DS-146 now advises it. A reveal is the motion the gate was built for: on `data-played` the card
  would do most of its turning underneath the outgoing slide. The two tasks fit rather than merely
  landing together.
- **The DS-224 check written in T-232 caught this component before it shipped anywhere.** Step 2
  was run on purpose: with the CSS in and no print collapse, `component.py check` reported
  `entrance motions whose print state paints nothing: 1 - .slide[data-arrived] .turn`, and
  `unrowed_motions` reported the missing contract row beside it. That is the mechanism doing the
  job its three-times-late history asked for, on the first opportunity anyone gave it.
- **The first card reveal replaces Rise on the closing headline, rather than joining it.** Every
  element in these decks already rises, so any placement is either a replacement or a second
  entrance motion on one region. The close is one card-shaped block and the deck's most important
  slide, and turning the ask face-up is what the motion means. **It is a composition decision this
  task was told to take** (§1's open question) and it is the half a session cannot check — row 4 of
  [`../docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md), with the fallback stated: if it reads as a
  flourish, the fix is the placement, because Turn is built and contracted either way.
- **The ranks were re-derived, not written.** DS-239 derives `--m-rank` from the whole deck, so a
  third content motion moves the other two. `density.py write` did it: `pulse` 1, `arrow-pop` 34,
  `turn` 67.

**What the harness could not measure, and how the claim was split.** The first probe navigated to
the closing slide and waited for `data-arrived`. It gave **two different answers from one unchanged
deck**, then overran Chrome's virtual-time budget in five runs of six: under
`--virtual-time-budget` timers advance and the frame clock barely does, so `animationend` — which
is what lands the arrival — is dispatched unpredictably. That is the instrument, not the deck. So
the two claims are measured by the two tasks that own them: **T-268 owns *when* `data-arrived`
lands** and proves it with its own probe, which drives the leaving animation to its end and passes
deterministically; **T-274 owns whether the reveal reads its dials once arrived**, which is a
computed-style fact and needs no clock. The rest state is still read off the deck's own markup
before anything is set, so *not running before arrival* is measured rather than assumed. Five runs,
five identical answers.

**And one measurement that would have reported the fix as broken.** `getTiming().easing` is
`linear` for every CSS animation — the effect's easing is not `animation-timing-function`, which
applies per keyframe. Read that way, `--turn-ease` looks unread. The dials are read off the
computed properties instead.

**Outputs produced**
- [`shell/components.css`](../shell/components.css) — `.turn`, `@keyframes turn`, the density list,
  and the four collapses
- [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) §3.8 — the parts row and two motion
  rows
- [`examples/reference-deck.html`](../examples/reference-deck.html) — the first card reveal, and
  three re-derived ranks
- [`docs/THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) — both dial rows, and the note that named
  this task
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) — `PR-36` closed
- [`docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md) — row 4

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| `var(--turn-dur)` and `var(--turn-ease)` are read by a component in the shared block | pass | `.slide[data-arrived] .turn`. Measured on the built deck rather than read off the CSS: `animationDuration` `0.42s` against a `--turn-dur` of `420ms`, `animationTimingFunction` `ease-in-out` against a `--turn-ease` of `ease-in-out` |
| The component has its rows, and `component.py check` is green on every tracked deck | pass | One parts row and two motion rows. Both `unrowed motions: 0` and the motion-token check green on all four decks; the batch's closing `check_all.py` covers every one |
| The reveal is visible in a deck, and the look it owes is queued | pass | `examples/reference-deck.html` slide 12. At rest the card is `opacity:0` with nothing running; once the slide has arrived, `turn` runs and it ends `opacity:1`. Queued as row 4 of [`OWED-LOOKS.md`](../docs/OWED-LOOKS.md) |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | pass | Recorded in the batch's closing run |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → done | Built in **B9**, closing `PR-36`'s Turn half. `.turn` scales from its own centre line on exactly the two dials it has - an angle would have wanted a third token, which is the wrong thing to add to a fix for unread tokens. It is gated on `data-arrived` and is that attribute's first reader, which [T-268](T-268-three-chrome-and-timing-defects-in-deck-js.md) built in the same batch. **T-232's new DS-224 check caught it before it shipped**, on the first opportunity anyone gave that mechanism. The first card reveal replaces Rise on the reference deck's closing ask - a composition decision this task was told to take, and the half a session cannot check: row 4 of [`../docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md). |
| 2026-08-29 | → proposed | Raised after the owner ruled `PR-36`'s open half on 2026-08-29, having had it deferred by [T-242](T-242-the-contracts-against-the-checkers-that-decide-them.md) that day as a `DS-000` question a batch's authority did not cover. **The recommendation was to retire and the owner chose to build**, so the starter set keeps its fourth name and gains a body. `PH3`: not a defect in the published plugin. |
