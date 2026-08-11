---
id: T-016
title: The interaction and motion layer
type: deliverable
status: done
phase: review
parent: null
blocked_by: [T-014]
related: [T-002, T-005, T-007, T-017, T-021]
work_package: PH1
shipped_in: 0.1.0
owner: maintainer
created: 2026-08-06
updated: 2026-08-12
deliverables:
  - docs/COMPONENT-CONTRACT.md
  - examples/reference-deck.html
  - tools/deck/render.py
  - tools/deck/audit.py
  - tools/deck/component.py
---

# T-016 — The interaction and motion layer

## 1. Specify

**Outcome**
The library of interactive and animated components the build mode composes into slides — turning
cards, toggles, tabs, floating information layers, tooltips, plus the motion and 3D vocabulary that
makes the deck feel built rather than assembled. Sparse enough to present live, complete enough to
read alone.

**Why this one**
Progressive disclosure is the owner's signature technique and was absent from `docs/BRIEF.md`
entirely. It is what lets one file serve a live audience and a lone reader instead of compromising
between them. Richness here is wanted, not rationed — the corpus's minimal-JavaScript habit is
history, not a target.

**Scope**
- In: the component set, its markup contract, and the motion vocabulary — transitions, slide
  entrances, 2D animation, 3D effects, depth and parallax where they carry meaning.
- In: an editorial rule for the split — what belongs on the face of the slide versus behind the
  interaction. A deck that hides the wrong half is worse than one that hides nothing.
- In: a motion rest state. Animation that never settles is unreadable on a projector, and the
  presenter is talking over it.
- Out: the portability envelope — which techniques survive `file://` and the target browser is
  T-017's job. This task assumes that answer and builds inside it.
- Out: motion for its own sake. Richness is the licence; noise is still a defect.
- Out: **the motion tokens.** [T-007](T-007-define-the-parametric-theme-layer.md) landed them
  2026-08-09 — 14 of them, banded, in [`docs/THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) §3.6.
  This task **consumes** that contract; a component that hard-codes a duration is now a gate
  failure rather than a style note.

**Measured 2026-08-09, before planning.** What exists, and what the words *the technique exists,
the contract does not* are actually worth:

| | |
| :--- | :--- |
| named motions implemented | **4 of 4** — `rise` · `open` · `current` · `pulse`, one `@keyframes` each |
| elements carrying `.rise` | **63** |
| disclosure components | **10**, each a `disc-btn` · `disc-mark` · `disc-label` · `disc-panel` set |
| buttons, and `aria-expanded` attributes | **15** and **14** |
| `prefers-reduced-motion` | **honoured in one block**, covering all four motions, the slide transition and the ruler — **and never rendered under it**, which is why DS-143 is excused in `check.py` rather than checked |
| **3D of any kind** | **0** — no `rotateX`/`perspective`/`translateZ`, no `<canvas>`, no WebGL |
| frame rate, ever measured | **never**, on any deck, on any machine |
| markup contract a generator could emit | **none written** |

So this task is **not** "build the interaction layer" — most of it is running. It is three things
the 2026-08-07 log row named and one the measurement adds: **the contract**, **the 3D class**,
**the reduced-motion pass**, and **a frame-rate number with a machine beside it**.

**Inputs**
- [`examples/reference-deck.html`](../examples/reference-deck.html) — the working instance of
  everything except 3D.
- [`docs/THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) §3.6 — the motion tokens and their bands.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §5.1–§5.3, and **DS-140 as amended
  2026-08-09** — still a closed vocabulary of four, now with banded durations.
- [`tools/deck/check.py`](../tools/deck/check.py) — the `DEFERRED` entry for DS-143, which names the
  reduced-motion pass as *cheap, and the first thing to build after this task*.
- [`tools/deck/render.py`](../tools/deck/render.py) — the harness, and **DS-221's pin-motion-off
  rule**, which a second never-quiescent animation makes harder.
- [`docs/LESSONS.md`](../docs/LESSONS.md) — **L-36**, **L-44** (a new motion check must declare what
  it does with an absent subject), **L-45**, **L-26**.

**Acceptance criteria**
- [x] Component set defined with a stable markup contract the generator can emit — **met
      2026-08-09**: [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md), 59 authored
      parts over 8 sections, parsed by `tools/deck/component.py` and gated as **DS-229**
- [x] ~~Motion vocabulary defined as **tokens** — durations, easings, distances, depth — so it swaps
      with the theme (T-007) rather than being hard-coded per component~~ **met 2026-08-09 by
      [T-007](T-007-define-the-parametric-theme-layer.md)**: 14 motion tokens, banded, and
      `themes/lattice.css` moves every one of them. Kept struck through rather than deleted,
      because a criterion that disappears is one nobody can check was satisfied
- [x] **Every component reads its motion from those tokens** — the half T-007 could not deliver,
      since it owns the contract and this task owns the components that must honour it. **Met
      2026-08-09** in two halves that needed different instruments: eleven rules named in
      `COMPONENT-CONTRACT.md` §3.8 must *read* the tokens the contract lists, and `theme.py`'s
      literal scan grew easing so that *no curve is written outside the region*. The second half
      was the gap — the scan had covered lengths and durations since T-007 and never easing
- [x] Every technique used is verified working from `file://` in the target browser, glitch-free —
      **met 2026-08-09**: the render gate and the reduced-motion pass both run real Chrome offline
      with every DNS lookup black-holed, and slides 3, 8 and 10 plus the reading view were captured
      and looked at after the last change
- [ ] ~~Frame rate held on a real 12-slide deck with the heaviest slide on screen; number stated,
      and the machine it was measured on stated with it~~ **Moved 2026-08-09 to
      [T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md)**, which owns
      it in PH2. Struck through rather than deleted: a criterion that disappears is one nobody can
      check went anywhere
- [x] `prefers-reduced-motion` honoured with a genuinely usable fallback, not a dead deck —
      **rendered under it and measured**, which closes DS-143's excusal in `check.py`. It is
      honoured today and has never been rendered that way, and those are different claims. **Met
      2026-08-09** by step 1: three rows from a second render, DS-143 checked rather than excused,
      and two seeded variants caught
- [ ] ~~**A functional 3D visual demonstrated** — one that encodes something a 2D rendering would
      lose — with a **chosen static projection** as its reduced-motion and print fallback, not a
      frozen mid-wobble frame, and with DS-218's stop control reaching it~~ **Moved 2026-08-09 to
      [T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md)**, with the
      DS-140 question it forces. PH2
- [x] The editorial split rule written, and applied in the demonstration deck — **met 2026-08-09**
      by step 4: **DS-230** names what tier two is for and closes its vocabulary at four kinds,
      **DS-231** is the one clause of DS-161 a check can decide, and all ten panels declare their
      kind in `data-disc`
- [x] Demonstrated on a real 12-slide deck, opened and looked at, in both modes: presented, and
      read cold by someone who was not in the room — **met 2026-08-09**: the twelve-slide reference
      deck on the stage, and the same file at a 760 px viewport, where DS-071 hands over on its own
      and every panel inlines with its label as a heading (DS-073). Both offline
- [x] *Optional mode:* a forced-printable variant exists and reveals disclosure content. Not a
      gate on the design — see T-005. **Met before this task**:
      [`tools/deck/print_variants.py`](../tools/deck/print_variants.py) builds both variants, and
      R7 §4's paginated mode is adopted in the deck by
      [T-032](T-032-adopt-the-paginated-print-mode-in-the-reference-deck.md)

**Open questions**
- ~~Does the deck need an explicit "reveal all" control for the reading case? — owner~~ **Answered
  2026-08-07 by the owner: no. The reading view *is* reveal-all.** DS-073 already inlines tier two
  there with the control not rendered, so the reading case has an entire rendering rather than a
  button. A second global control would be a third encoding of one fact — the DS-216 failure
  [T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) paid to remove, and it
  would land on the chrome budget the same task cut from 96 design units to 52.
- ~~Should disclosure state be shareable via URL fragment, so a recipient can be pointed at an
  opened layer? — owner~~ **Answered 2026-08-07 by the owner: slide index and view only.** The
  fragment carries which slide and which rendering — restored on load, and **not written per
  toggle**, because a history entry per panel makes the browser Back button stop meaning "the
  previous slide". Per-panel state is deliberately not encoded: *"point me at that content"* is
  already answered by the reading view, which shows all of it. Encoding open panels is a state
  serializer this task does not owe until someone asks for it.
- ~~How far into 3D is useful rather than decorative?~~ **Answered 2026-08-07 by the owner: 3D is
  wanted for functional visualisation, not only for emphasis.** Three cases named: **a 3D diagram
  under a slight continuous wobble, so that peaks read as peaks**; **a 3D mesh shown as itself**;
  and **decorative 3D for emphasis**, which stays permitted. So the component set carries a **3D
  visual class** — this is not the narrow "a third axis or nothing" reading, and the preference for
  SVG where it is equally good (DS-111) is unchanged, because these are cases where it is not.
  *(The permission question was already settled — the owner granted a full exemption on 2026-08-06,
  so `<canvas>` and WebGL are allowed for diagrams too.)*

  **The wobble is the load-bearing part of the answer and it collides with two rules in this
  task's own scope.** It is *continuous* motion, and the scope line above requires a motion rest
  state; **DS-140** is a closed vocabulary of exactly four motions, `hard` and `auto`-checked, and a
  wobble is a fifth. The resolution this task should argue rather than assume: the oscillation
  **is** the depth encoding — a static projection of a 3D surface is ambiguous and the movement is
  what disambiguates it — so it is the one class of never-settling motion that satisfies §9.2's
  *motion must encode something*. That makes it a **ruleset change to raise, not a licence to take
  quietly**: DS-140 gains a fifth motion or an exemption clause, on the T-033 precedent that a rule
  contradicted by a shipped deck is a defect in the ruleset.

## 2. Plan

**Rescoped 2026-08-09 to four steps, when the project split into PH1 and PH2.** Steps 5–8 were
capabilities the layer does not reach — no deck here has any 3D, and none has ever had its frame
rate measured — rather than defects in what it does, so they moved to
[T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md) whole, with the order
inside them intact. **This task closes after step 4**, the editorial split rule, which build mode
needs and the other three do not gate.

**Replanned 2026-08-09 against the measurement above.** The original five steps were written when
this task looked like building the layer. Four of the five are already standing in
[`examples/reference-deck.html`](../examples/reference-deck.html), and step 3 belongs to
[T-007](T-007-define-the-parametric-theme-layer.md), which closed. What is left splits into **one
cheap thing that closes an excusal, one contract to extract, and one genuinely new capability** —
and the order is that, because the 3D class is the only step that can change the ruleset.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | **The reduced-motion pass.** A second render with `prefers-reduced-motion` forced, asserting the semantics survive — the dashed arrows stay dashed, every risen element is at rest and visible, no slide is blank. Closes the `DEFERRED` entry `check.py` calls *the first thing to build after this task* | a reduced-motion stage in [`tools/deck/render.py`](../tools/deck/render.py) and rows in [`tools/deck/audit.py`](../tools/deck/audit.py); DS-143 moves from excused to checked |
| 2 | **Extract the markup contract** from the ten disclosure sets and the ruler that already work, the way T-007 extracted the token contract from a region that already existed. Names, required attributes, the ARIA each carries, and which tokens each reads | `COMPONENT-CONTRACT.md`, under `docs/` |
| 3 | **Gate it**: every component instance matches the contract, and **no component hard-codes a duration or an easing** — the criterion T-007's tokens make checkable and nothing checks | rows in `audit.py`, fixtures in [`tools/deck/static_variants.py`](../tools/deck/static_variants.py) |
| 4 | **Write the editorial split rule** — what belongs on the face of the slide and what belongs behind the interaction. §5.3 has the mechanics and no editorial test | a section of the component contract, and a `DESIGN-SYSTEM.md` amendment if it turns out to be a rule |
| 5–8 | ~~The frame-rate instrument · the 3D class · the DS-140 amendment the wobble forces · the demonstration of all three~~ **Moved 2026-08-09 to [T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md)**, and the order inside them travels with them | — |

**Approach decisions**

- **Extract, do not author.** Step 2 follows T-007's shape exactly, and for the same reason: a
  contract written from a working instance can be checked the day it lands, and one written from a
  blank page describes a component nobody has built.
- **Step 1 first because it is the cheapest thing that removes an excusal**, and because every
  later step adds motion that the reduced-motion pass then has to cover. Building it last would
  mean measuring it last.
- **Steps 6 and 7 are one decision, not two.** The wobble is either a fifth motion or it is not,
  and building it before the ruleset says which produces a deck that fails its own gate. Raise the
  amendment with the figure in hand — a rule argued from a rendering beats one argued from a plan —
  but do not ship the figure until the rule has a named side.

## 3. Implement

**All four steps are done.** Steps 5–8 left for
[T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md) when the backlog split
into PH1 and PH2.

**Decisions & assumptions**

- **The contract covers every shared component, not only the two the plan named as its source** —
  2026-08-09. Step 2 says *extract from the ten disclosure sets and the ruler*; those are the
  exemplars the measurement in §1 counted, and a generator emitting only those two cannot emit a
  deck. The acceptance criterion is *the generator can emit*, so the subject is every component,
  with disclosure and the ruler as the worked cases because they are the ones carrying ARIA and
  state.
- **The boundary is the style block, not a list of components** — 2026-08-09. A deck has three
  regions and they already have three owners: `<style id="theme">` holds what a second theme
  changes, `#slides` holds one deck's composition, and the unnamed block holds everything more
  than one slide can use. So **a component is a class the shared block styles**, and the
  completeness check runs that sentence backwards. A hand-kept list of components drifts the first
  time someone adds one; this cannot, because adding a component *is* adding a rule to the block
  the check scans (**L-46**).
- **`vocabulary` is checked backwards, and that is what makes it a claim.** Five classes are
  styled and used nowhere — the figure's three role classes, `.t-ink` and `.mono`. Deleting them
  was considered and rejected: the role classes are DS-026's vocabulary spent in the ledger rather
  than in a figure, which is a fact about this deck and not about the class. Marking them *unused*
  in prose asserts nothing, so the row is falsifiable instead: **an instance appearing fails the
  run** and the row has to be reclassified.
- **DS-229 was added rather than citing DS-136** — 2026-08-09, on DS-228's precedent. DS-136 sits
  on the hard-judge checklist at `Reach: —`, so a mechanical check citing it would claim a reach
  the ruleset denies, which is the defect T-038 removed. Reclassifying DS-136 as `auto` was the
  other option and it moves a genuine judgement out of the evaluator's hands to make a check fit.
  So the general rule stays judgement and **the one instance a check can decide is written down**,
  exactly as DS-228 is written under DS-137. Owned rules 111 → 112, checked 79 → 80.
- **The easing half belongs to the theme contract, not this one** — 2026-08-09. *No component
  hard-codes a duration or an easing* has two homes and only one was built: `theme.py`'s literal
  scan has covered lengths and durations since T-007, and an easing is neither, so
  **`cubic-bezier` was unreachable by every check in the repository.** Extending that scan keeps
  one home for *what may not be written outside the region* (**L-08**). The line it draws is a
  rule's number against a look: **a keyword is quoting DS-141, a curve is choosing a feel.** The
  deck writes eight easing keywords and one curve, and the curve is `--rise-ease`, in the region.
- **The rows live in a module of their own, not in `audit.py`** — a deviation from step 3's stated
  output, taken for the reason `theme.py` is not in `audit.py` either: a contract that is *parsed*
  needs the parser beside it, and `audit.py` holds the checks that read a deck directly. The
  verdicts still reach the gate through `check.py`'s row list, which is what the plan meant.
- **Every named motion now carries an easing dial, and DS-141's keyword was the defect** —
  2026-08-09, second pass, after the owner read the first as a ban on bespoke easing and said so.
  It was. Closing the curve gap left four of DS-140's motions with `ease-in-out` written into their
  components because DS-141 named that keyword, so a deliberate overshoot on a card reveal had no
  legal home. **The fault was in the rule, not the check**: *max 500 ms, ease-in-out* is one
  theme's curve stated as the ruleset's, which is the third time that shape has been found here
  (**L-45**) and the first on a value that is a word rather than a number. DS-141 now says *eased
  rather than linear*; `--open-ease`, `--turn-ease`, `--scale-ease`, `--pulse-ease` and
  `--slide-ease` join `--rise-ease`; and `themes/lattice.css` moves three of them, so the axis is
  demonstrated rather than declared. `linear` survives in the two places the mechanism requires it.
  **This is the standing shape of the answer when a check reads as over-strict**: the gate keeps
  the value out of the component, and the theme is where the choice goes — not a loosened rule.

- **The editorial rule is DESIGN-SYSTEM.md's, not the component contract's** — 2026-08-09, a
  deviation from step 4's stated output. The plan said *a section of the component contract*; the
  contract's own opening says the rules that decide whether an interaction is any good are the
  ruleset's, and it is **parsed**, so an editorial rule written into it would be prose the parser
  ignores sitting in a document that just spent a step establishing its boundary. So **DS-230** is
  the rule and the contract carries only the encoding — one attribute value, checked for closure.
- **Two rules rather than one, on the DS-228 and DS-229 precedent** — 2026-08-09. The editorial
  half is a judgement (`judge`), and the one clause a program can settle — *the bottom line never
  cites a figure that lives only behind the click* — is **DS-231**, `auto`. Folding them into one
  ID would have made the rule claim a reach the check does not have, which is the defect T-038 spent
  a task removing.
- **The kind goes in `data-disc`, which was a required attribute carrying nothing** — 2026-08-09.
  A `judge` rule with no trace in the artefact is re-derived by everyone who reviews it (**L-47**),
  and the slot already existed: the script selects on `[data-disc]`, presence and not value, so
  filling it costs the runtime nothing. The gate verifies **closure only**, and DS-230's row says
  so rather than leaving the reach to be assumed.
- **Two candidate rules were measured against the ten panels and thrown away**, which is what makes
  the third a finding — 2026-08-09. *The label shares a word with the face* fails on slide 5
  ("What each figure excludes" names the ledger without naming anything in it). *Every row key names
  something the face shows* fails on three panels, because the keys are roles in the panel's own
  argument — `Input` · `Step` · `Result` — not labels borrowed from the slide. What survived is
  about the **question** the face provokes, and a question is a judgement.
- **DS-231's two sides needed different strictness, and the reference deck is what proved it** —
  2026-08-09. Read strictly on both sides the row failed slide 3, whose stat figure `11` and unit
  `minutes, average wait` are two elements, so `11 minutes` is never one figure on that face. The
  deck was right and the instrument was wrong. **A gate row that over-reports blocks a conforming
  build**, which is the opposite trade from the figure ledger's (**L-48**).
- **The reduced-motion pass is a second render, not a second reading of the file** — 2026-08-09.
  Chrome takes `--force-prefers-reduced-motion`, so the deck is rendered again with the preference
  set and three things are measured in that state: what is still animating, whether any risen
  element is still hidden, and whether the flow's `stroke-dasharray` survived. The dash row is
  declared a **conditional** — a deck with no flow diagram owes nothing — rather than left to the
  expression to decide (**L-44**).
- **`mediaMatches` is checked before anything else is believed.** If the flag does not take, every
  row below it would report the *default* state while claiming to report the reduced one, which is
  a worse failure than no measurement. It reports `False`, not a pass.
- **The variant found that the deck disables motion twice, and only one path was seeded** —
  2026-08-09. An `@media (prefers-reduced-motion:reduce)` block applies at parse time, and
  `:root[data-motion="off"]`, which the script sets from `matchMedia` on load, applies after it and
  outranks it. Breaking only the media query changed nothing the probe could see. **A variant that
  breaks one of two redundant paths is evidence that the check cannot see the other one** — the
  seed now breaks both, and the row fails at 5 of 5 hidden.

**Outputs produced**
- [`tools/deck/audit.py`](../tools/deck/audit.py) — `REDUCED_PROBE`, `reduced_motion_data`,
  `reduced_verdicts`.
- [`tools/deck/check.py`](../tools/deck/check.py) — the second render wired into `gather`,
  DS-143's `DEFERRED` entry closed on the condition it named for itself, and the component stage
  added beside the theme one.
- [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) — 59 authored parts, 5
  `vocabulary`, 3 `script`, 1 `print`, over 8 sections; 11 motion rules; a state table; and the
  easing line, cross-referenced to `THEME-CONTRACT.md` §5 where it is enforced.
- `component.py`, under `tools/deck/` — parses that document, does not restate it.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §5.1 — **DS-229**, and
  [`docs/DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) §5.9 for why it exists rather than a
  row under DS-136.
- [`docs/THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) §5 and
  [`tools/deck/theme.py`](../tools/deck/theme.py) — `curves()`, and DS-010's row now scanning for
  an easing curve outside the region.
- [`tools/deck/static_variants.py`](../tools/deck/static_variants.py) — `REDUCED_VARIANTS`, plus
  five new static fixtures, one per new claim.
- [`docs/LESSONS.md`](../docs/LESSONS.md) — **L-46**, **L-47**, **L-48**.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §5.3 — **DS-230** and **DS-231**;
  [`docs/DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) §5.10 for the ten-panel extraction and
  the two candidate rules it ruled out.
- [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) §2 and §3.3 — the closed-set
  attribute form, and what `data-disc` now carries; `component.py` enforces closure.
- [`tools/deck/audit.py`](../tools/deck/audit.py) — `split_verdicts`, `split_data`, `magnitude`,
  and DS-231's `ABSENCE_IS_A_PASS` row.
- [`docs/EVALUATION.md`](../docs/EVALUATION.md) §S4 — DS-230 cited, and the `4` band given the
  question to ask.
- [`examples/reference-deck.html`](../examples/reference-deck.html) — ten `data-disc` values, and
  [`examples/reference-deck-seeded-defects.html`](../examples/reference-deck-seeded-defects.html)
  regenerated, which also picked up the easing change it had been stale on since `f65196a`.

**Where it stands**

```
python tools/deck/check.py examples/reference-deck.html    81 checked, 28 excused, 0 SILENT, 0 failing
                                                           113 owned, buckets sum to 113
                                                           DS-229 authored parts: 59 required, 0 problems
                                                           DS-229 classes styled: 69, 0 uncontracted
                                                           DS-229 motion rules: 11, 0 gaps
                                                           DS-231 bottom-line figures behind the click: 0 of 6
                                                           DS-010 literals 38 exempt, curves 0
python tools/deck/static_variants.py                       22 static · 7 rendered · 2 reduced-motion, all caught
python tools/deck/component.py check <themed build>        5 of 5, so the contract survives a theme swap
```

The gate was 78 checked / 29 excused before step 1, 79 / 28 of 111 before steps 2 and 3, and 80 of
112 before step 4. **The reference deck needed no edit to pass its own markup contract**, which is
what *extract, do not author* is supposed to produce and is not evidence that the contract is weak —
the fixtures are. **Step 4 needed ten**, and every one of them is an attribute value declaring a
decision the deck had already taken; no panel's content moved.

**DS-231 is thin and says so in its own row.** Six figures are cited by a bottom line across ten
panels, and exactly one of them — slide 3's `11` — also sits inside its panel and is cleared by the
face, so the subtraction is exercised rather than merely defined. Three panels hold no figure at
all. A row that prints `0 of 6` rather than `pass` is the whole reason that is visible.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Component set defined with a stable markup contract the generator can emit | **met** | [`COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md), 59 authored parts over 8 sections, parsed by `component.py` and gated as **DS-229**. `python tools/deck/component.py check` — 5 of 5 |
| ~~Motion vocabulary defined as tokens~~ | **met by [T-007](T-007-define-the-parametric-theme-layer.md)** | 14 motion tokens, banded, in [`THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) §3.6; `themes/lattice.css` moves every one |
| Every component reads its motion from those tokens | **met** | Two instruments for two halves: `COMPONENT-CONTRACT.md` §3.8 names 11 rules and the tokens each must read, and `theme.py`'s literal scan grew easing so no curve is written outside the region. `DS-010 — 38 literal(s), 38 exempt, 0 curve(s)` |
| Every technique verified working from `file://` in the target browser, glitch-free | **met** | Real Chrome, throwaway profile, `--host-resolver-rules=MAP * ~NOTFOUND`. Slides 3, 8 and 10 captured after the last change and looked at; everything at rest and visible |
| ~~Frame rate held on a real 12-slide deck~~ | **moved** | To [T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md), PH2. Never measured on any deck on any machine, and that is a capability this layer does not reach rather than a defect in it |
| `prefers-reduced-motion` honoured with a genuinely usable fallback | **met** | A second render with the preference forced. Three rows, DS-143 moved from excused to checked, and the variant found the deck disables motion by two redundant paths — a seed breaking one proved the check could not see the other |
| ~~A functional 3D visual demonstrated~~ | **moved** | To [T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md), PH2, with the DS-140 amendment the wobble forces, because they are one decision |
| The editorial split rule written, and applied in the demonstration deck | **met** | **DS-230** — four closed kinds, extracted from the ten panels (3 · 3 · 3 · 1) — and **DS-231**, the one clause of DS-161 a check can decide. Applied: all ten panels declare a kind, and `component.py` refuses a fifth. [`DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) §5.10 carries the two candidate rules the measurement ruled out |
| Demonstrated on a real 12-slide deck, opened and looked at, in both modes | **met** | The stage at 1920×1234, and the same file at a 760 px viewport where DS-071 hands over on its own: every panel inlined and open, each label promoted to a heading, the control not rendered (DS-073). Offline both times |
| *Optional:* a forced-printable variant exists and reveals disclosure content | **met** | [`print_variants.py`](../tools/deck/print_variants.py) builds two; the REFLOW variant prints the reading view, which has already opened every panel, so tier two reaches paper. Not a gate — T-005's |

**Child fix tasks raised**
- none. One defect found in passing and left where it was found:
  [`tools/examples/seed_defects.py`](../tools/examples/seed_defects.py)'s S2 disclosure removal has
  never matched — its lookahead expects the panel to sit immediately before `.provenance` and the
  bottom line is between them — and it reports success regardless, because the `applied.append`
  beside it asserts nothing. It is a fixture generator over-reporting its own coverage, it predates
  this task, and S2 carries two other seeds that do apply, so it is
  [T-058](T-058-the-seeded-defect-generator-reports-edits-that-never-matched.md) rather than a
  reason to hold this task open.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-11 | (no change) | **N-2 and N-3, from the first external deck**, routed here by [T-092](T-092-product-feedback-from-the-first-external-deck.md). N-2: `Ctrl+R` is bound, and it takes the browser's reload from a presenter mid-talk - a shortcut this layer chose against one the platform owns, and the cost lands in the one situation the deck exists for. N-3: disclosure attaches to the slide, so a figure with three parts cannot reveal one of them; the reader who wanted detail about a single element got the whole slide's tier two. Both are the layer working as specified and failing a reader, which is why they arrive as needs rather than as defects. |
| 2026-08-09 | → done | **Step 4 of 4 done, and the task closes: §5.3 now says what tier two is *for*.** Every other rule there is a test to **reject** — DS-162 says what must be tier one, DS-161 says the slide must stand closed, DS-170 says long text goes behind rather than on — so a deck could satisfy all eleven and still put an appendix behind the click, which is exactly what a generator with only rejection rules will write. **DS-230** names the four kinds tier two comes in — `derivation` · `scope` · `condition` · `instances` — closed for DS-140's reason rather than for tidiness, and **DS-231** is the one clause of DS-161 a program can settle: *a bottom line never cites a figure that lives only behind the click.* The gate reads **81 checked of 113 owned**, up from 80 of 112. **The rule was extracted, and two candidates were thrown away to get it.** *The label shares a word with the face* fails on slide 5 — "What each figure excludes" names the ledger without naming anything in it — and *every row key names something the face shows* fails on three panels, because the keys are roles in the panel's own argument (`Input` · `Step` · `Result`) and not labels borrowed from the slide. What survived is about the **question** the face provokes, which is a judgement, which is why DS-230 is `judge`. The ten panels then sorted 3 · 3 · 3 · 1 with no remainder, and **the deck needed no content change** — ten attribute values, declaring decisions it had already taken. **Two things this cost that are worth carrying.** The kind is written into `data-disc` because a `judge` rule with no trace in the artefact is re-derived by every reviewer (**L-47**), and the slot was already there and empty — the gate verifies **closure only**, and the rule's own row says so rather than letting a green run read as the claim being checked. And DS-231's two sides needed **different strictness**: read strictly on both, it failed slide 3, whose `11` and `minutes, average wait` are two elements — the deck was right, and **a gate row that over-reports blocks a conforming build**, which is the opposite trade from the figure ledger's (**L-48**). Rendered and looked at offline in both modes: the stage, and the same file at 760 px where DS-071 hands over on its own and every panel inlines with its label as a heading. Found in passing and raised rather than fixed here: [T-058](T-058-the-seeded-defect-generator-reports-edits-that-never-matched.md) — the seeded-defect generator's S2 disclosure removal has never matched and reports success anyway. |
| 2026-08-09 | (no change) | **Rescoped to four steps: 5–8 move to [T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md), and this task closes after the editorial split rule.** The owner set a two-phase plan — a working PH1 that ships, then PH2 — and asked which of the backlog is genuinely between here and a release. Three of these four steps are not: the deck has **no 3D at all** and no deck in this repository has ever had its **frame rate** measured, and both of those are capabilities the interaction layer does not reach rather than defects in what it does. The DS-140 amendment travels with the 3D because it is the same decision. **Step 4 stays** — [T-002](T-002-build-mode-the-self-contained-deck-generator.md) has to decide what goes behind a disclosure and §5.3 gives it mechanics with no editorial test, so the rule is a build-mode input and not a polish item. The three criteria that left are **struck through and pointed at their new home** rather than deleted, on the same reasoning the tokens criterion was: a criterion that disappears is one nobody can check went anywhere. |
| 2026-08-09 | (no change) | **Motion easing is a theme dial on every named motion, and DS-141 is amended.** Raised by the owner, who read the new curve check as a ban on bespoke easing and wanted the flexibility back: *there could be subtle effects adding emphasis where another type of animation fits better.* They were right, and the fault was in the rule rather than in the check. DS-141 said *max 500 ms, **ease-in-out***, which is one theme's curve stated as the ruleset's — the third instance of that shape after DS-034's line height and DS-140's durations, and the first on a value that is a **word**, which is why it hid longer: nobody audits a keyword for being a sample (**L-45**). What the cap and its rationale argue is that a transition is short and eased; nothing argues which easing. So DS-141 now reads *eased rather than linear*, five easing tokens join `--rise-ease`, and the five motions plus the ruler ring read them. **`themes/lattice.css` moves three** — Turn overshoots so a card reveal reads as a flick, Scale and the slide transition ease out so the outgoing scene does not brake — which makes the axis demonstrated rather than declared, on T-007's own lesson that only a second artefact finds a pin. `linear` survives exactly where the mechanism needs it: a looping dash stutters at the seam under anything else, and a zero-duration `visibility` step has nothing to ease. **The variant suite caught its own staleness** — two seeds anchored on text this change rewrote, and the self-test refused to run rather than reporting 18 of 20; both were repointed, and the easing seed now adds a new transition rather than rewriting a tokenised one, so it breaks DS-010 alone. Rendered and looked at offline in both themes: everything at rest and visible, which is the failure a missing token would have produced. |
| 2026-08-09 | (no change) | **Steps 2 and 3 of 8 done: the markup is a contract, and DS-229 is the rule that holds a deck to it.** [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) names 59 authored parts, 11 motion rules and the state every one of them changes; `component.py` parses it rather than restating it, the way `theme.py` reads the token contract. The gate reads **80 checked of 112 owned**, up from 79 of 111. **Two decisions are the substance.** *DS-229 was added rather than citing DS-136*: DS-136 is on the hard-judge checklist at `Reach: —`, so a mechanical check citing it claims a reach the ruleset denies, and reclassifying it would move a real judgement out of the evaluator's hands — so the general rule stays judgement and the one instance a check can decide is written down, on DS-228's precedent under DS-137. *The completeness half runs from the CSS back to the document* — every class the shared style block styles must have a row — because **a component is added by writing a rule, which is exactly when nobody remembers the contract exists** (**L-46**). **What the extraction found that reading had not:** *no component hard-codes a duration or an easing* was half a claim. `theme.py`'s scan has covered lengths and durations since T-007 and an easing is neither, so a `cubic-bezier` written in a component was unreachable by every check in the repository. §5 of the theme contract now draws the line where the rules already draw it — **a keyword quotes DS-141, a curve chooses a feel** — and the deck's eight keywords pass while its one curve is `--rise-ease`, inside the region. **Five classes are styled and used nowhere**, and rather than delete them they are marked `vocabulary` and checked backwards: an instance appearing fails the run. The reference deck needed no edit to pass, and the five new fixtures are what makes that a result rather than a hope. |
| 2026-08-09 | → in_progress | **Step 1 of 8 done: the reduced-motion pass, and DS-143 is now checked rather than excused.** The gate reads **79 checked / 28 excused**, up from 78 / 29, and the excusal closed on the condition it had written for itself. Three rows from a second render with `--force-prefers-reduced-motion`: nothing still animating, no risen element still hidden, and the flow's dasharray surviving at 7px 6px. **The variant is the part worth carrying**: the deck disables motion by two redundant paths — the `@media` block at parse time and `:root[data-motion="off"]` set from `matchMedia` on load — and a seed that broke only the first changed nothing the probe could see. **A variant that breaks one of two redundant paths is evidence about the other one**, not about the check. Both are seeded now and the row fails at 5 of 5 hidden. |
| 2026-08-09 | → planned | **Specified and replanned against a measurement, and the measurement halves the task.** Four of the five original steps are already standing in the reference deck — **4 of 4 named motions implemented, 63 risen elements, 10 disclosure sets, 15 buttons, `prefers-reduced-motion` honoured in one block** — and step 3, the motion tokens, closed with [T-007](T-007-define-the-parametric-theme-layer.md): 14 of them, banded, and `themes/lattice.css` moves every one. That criterion is struck through as met rather than deleted, and a new one takes the half T-007 could not deliver — **every component reads its motion from the contract**, which is now checkable and unchecked. What the measurement adds to the known gaps: **frame rate has never been measured on any deck on any machine**, and `prefers-reduced-motion` is *honoured* but has **never been rendered under**, which is why DS-143 sits excused in `check.py` — two different claims that read the same in a task file. Eight steps now, ordered so the cheap excusal-closing render comes first and the 3D class comes last, because **steps 6 and 7 are one decision**: T-007 banded DS-140's durations and deliberately left it a closed vocabulary of four, so the wobble-is-a-fifth-motion collision is untouched and still owed. |
| 2026-08-07 | (no change) | **The 3D question is answered and §1 now has none open: 3D is wanted for functional visualisation, not only for emphasis.** A wobbling 3D diagram whose motion resolves depth, a mesh shown as itself, decorative emphasis kept. One acceptance criterion added for it. **Three consequences this task inherits, none of them optional.** (1) **A ruleset change to raise**: DS-140 is a closed vocabulary of exactly four motions, `hard` and `auto`-checked, and a continuous wobble is a fifth — it needs a rule or an exemption clause, on [T-033](T-033-reconcile-ds-131-with-the-chrome-budget.md)'s precedent that a rule a shipped deck contradicts is a ruleset defect rather than a deck defect. (2) **The fallback is a chosen projection, not a frozen frame** — a paused wobble is the ambiguous static rendering the motion existed to fix, and it is what `prefers-reduced-motion`, the reading view and print all get ([R7](../docs/research/R7-printable-mode.md) §5.2 already records that print loses 3D). (3) **A second never-quiescent animation now exists**, so **DS-221**'s pin-motion-off-before-capture applies to it too, and [T-005](T-005-build-check-the-gate-the-deck-must-pass.md)'s render gate has one more thing to hold still before it measures. Also reaches [T-007](T-007-define-the-parametric-theme-layer.md), whose tokens cannot reach inside a WebGL scene unless the scene is plumbed to read them, and [T-019](T-019-build-the-capability-preflight-the-deck-ships-wit.md), which now has a real capability to preflight and a degraded state to design. |
| 2026-08-07 | (no change) | **Two of the three open questions answered by the owner, and both answers remove work rather than adding it.** *No reveal-all control* — the reading view is it, so the stage keeps the chrome budget [T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) cut. *The fragment carries slide and view only* — restored on load, never written per toggle, which keeps Back meaning "the previous slide"; per-panel state is not encoded until someone asks. **The 3D question is now the only one left in this task, and it is the one that decides its size** — it is also the only open question in the backlog that can still change what [T-002](T-002-build-mode-the-self-contained-deck-generator.md) has to emit and what [T-019](T-019-build-the-capability-preflight-the-deck-ships-wit.md) has to preflight, so it wants answering before either is planned rather than when this task is worked. |
| 2026-08-07 | (no change) | **The tier-two question this task shared with [T-021](T-021-the-reflow-view-and-the-resolution-contract.md) is settled, and it removes work from here.** The owner ruled that the reflow view **inlines** tier two — panels open in normal flow, the disclosure control not rendered — and **DS-073** now states it. So the disclosure component has **one context, not two**: it is designed for the stage, and the reading view is a document rendering that does not operate it. §5.3's rules stay written for the stage. [R7 §5](../docs/research/R7-printable-mode.md) had already decided the same question the same way for print, so all three renderings now agree. |
| 2026-08-07 | (no change) | `related` gains [T-021](T-021-the-reflow-view-and-the-resolution-contract.md) — which the row below already said to settle the tier-two question *with*, without the edge ever being written. Added by [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md), which also recorded that a working instance of this layer already exists: [`examples/reference-deck.html`](../examples/reference-deck.html) carries a disclosure component used ten times and a `rise` entrance used fifty-three, on tokenised durations and easings. **What is absent is the contract, not the technique** — no stable markup contract for a generator to emit, no theme-swap demonstration, no frame-rate figure, and no `prefers-reduced-motion` fallback shown to work. |
| 2026-08-06 | → proposed | Created after the owner identified progressive disclosure as their signature technique — absent from the brief. |
| 2026-08-06 | (no change) | Rewritten: print demoted from lead criterion to optional mode, minimal-JavaScript constraint dropped, motion and 3D added as first-class scope, after owner feedback. Retitled from "The progressive-disclosure interaction layer". |
| 2026-08-06 | (no change) | **T-014 closed, and it raises this task's standing.** [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) `§9.3` — progressive disclosure is load-bearing, not a signature flourish: it is the reason the deck can be two things. **§9.5** — Layered Detail is a **modifier on every archetype**, not one archetype among fourteen; R2 and R3 reached this independently. §5.3 gives eleven rules, nine of them `hard`, including the two-tier ceiling, the closed-deck test, the ≥24×24 px target and the independent-axes keyboard model. **§9.2** — motion must encode something; §5.2 keeps the four-motion vocabulary as the mechanism that makes it hold. |
| 2026-08-06 | (no change) | **[T-021](T-021-the-reflow-view-and-the-resolution-contract.md) raises a question this task shares:** the reflow view must carry **all** tier-two content, or it is not a conforming alternate version. Whether it does that by keeping the disclosure affordances or by inlining tier two is open, and §5.3's rules are written for the stage. Settle it with T-021 rather than separately. |
