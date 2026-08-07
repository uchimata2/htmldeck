# examples

Two decks, produced by [T-024](../tasks/T-024-build-the-reference-deck-and-validate-the-ruleset.md).
Both are single self-contained `.html` files with **zero external references**; open either by
double-clicking it, with the network off.

| File | What it is |
| :--- | :--- |
| [`reference-deck.html`](reference-deck.html) | The reference deck. 12 slides, built by hand against [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md). |
| [`reference-deck-seeded-defects.html`](reference-deck-seeded-defects.html) | The same deck with **one deliberate defect per evaluation dimension**. A test fixture, not an example to copy. |

**Riverbend is an illustrative city. It does not exist.** Every figure in either deck is an output
of the assumptions stated on the slide that uses it. Nothing is attributed to a real agency, study
or place — see *Provenance*, below.

---

## The reference deck

*Buy frequency before bikes* — a mid-size city choosing between building a bike-share network and
raising bus frequency, with one capital grant that closes in March.

**178 KB in one file.** Three embedded typefaces (97 KB of it), nine Lucide icons, seven
hand-written SVG figures, and the deck shell. No libraries, no build step, no network.

### Using it

| | |
| :--- | :--- |
| `←` `→` `space` `Home` `End` | Move between slides |
| `d` | Open or close this slide's detail |
| `r` | Switch between the presentation and the reading view |
| `m` | Motion on or off |
| `t` | Light or dark |
| `f` | Fullscreen |
| `Esc` | Close an open detail panel |

Clickable dots, prev/next, swipe and the mouse wheel all work too. Disclosure never interacts with
advancing: arrows move, `d` toggles, and neither affects the other.

### The reading view

The **Read** control switches to a conforming alternate version — one column, normal flow, type in
`rem`, every detail panel already open. It auto-engages when the stage scales below 0.5 — 960 CSS
px of width on a 16:9-or-taller window, and sooner on a short one — and never in fullscreen.
Position is preserved in both directions.

**The conformance claim, stated in full:** *WCAG 2.2 Level AA, via a conforming alternate version
reachable by a persistent control.* Not "this deck is AA" — the presentation view is a scaled
fixed stage and does not meet 1.4.4 Resize Text or 1.4.10 Reflow on its own. The reading view is
what conforms, the **Read** control is the persistent route to it, and the claim is only true while
both hold. [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §7 owns the wording.

### Provenance

Every figure derives from assumptions printed on the deck, and each slide's disclosure shows the
derivation, the exclusions, and what the model holds constant. Figures the model estimates rather
than derives carry an `[est.]` marker.

This is a deliberate reading of DS-102 (*no fabricated metrics; every figure sourced*). An example
deck about a place that does not exist cannot satisfy that rule by citing anyone, so **the
arithmetic is the source and the deck says so**. Quoting real transit research from memory would
have been the actual violation — a misremembered elasticity is a fabricated metric wearing a
citation.

### What was measured

In real Chrome, from `file://`, with every DNS lookup black-holed:

| | |
| :--- | :--- |
| External references | **0** |
| Embedded faces | 3, all reporting `loaded` offline |
| Body text at 720p | **17.3 px** (26 design units × 0.667) — clears the 16 px floor |
| Two-resolution diff, non-text boxes | **116 values at 3840×2000 vs 1280×634; worst disagreement 0.000 design units** |
| Two-resolution diff, text runs | 336 values, worst **1.17 design units** on an SVG text-run width |
| Reflow at 320 CSS px | `scrollWidth` **320**, zero elements overflowing, zero internal scrollers |
| Reflow auto-engage | correct at all four sweep viewports, including 1280 × 400 (scale 0.37) |
| Smallest interactive target | 30.5 CSS px at 1280×634 |

The layout is identical across a 3.15× scale ratio — every box lands on the same design-unit
coordinate. The 1.17-unit disagreement is text, and it is glyph-advance rounding rather than
layout: a run's width, position *and* height all shift as glyphs round to device pixels. A check
demanding exact equality would fail every deck that contains text.

*The first two rows were measured for the first time on 2026-08-07.* Until then the probe carried
nine keys and **all nine were text runs**, so the earlier line here — *384 values, positions agree
to 0.09* — described text placement under a heading that said geometry, and DS-063's non-text
tolerance had never had a value in it (**L-36**).

---

## The seeded-defect deck

[`docs/EVALUATION.md`](../docs/EVALUATION.md) §7: *a rubric that has never been tested is a rubric
that passes everything.* This file is the test. It is generated, never hand-edited:

```bash
python tools/examples/seed_defects.py
```

It **derives** from the reference deck, so everything except the seeded defect is held constant and
the rubric's response is attributable to the defect rather than to two decks differing in a hundred
ways. Every edit asserts that it matched; a seed that silently no-ops would produce a deck with
fewer defects than this ledger claims.

### The ledger

| Dim | Seeded defect | Where |
| :--- | :--- | :--- |
| **S1** Claim | The headline becomes a topic label — "Wait times". The slide asserts nothing. | Single Number slide |
| **S2** Evidence | A modelled projection is restated as observed fact, and the assumption marker that qualified it is deleted. | Trajectory slide |
| **S3** Encoding | The before/after network diagram is replaced by four cards joined by arrow glyphs. | Before / After slide |
| **S4** Density | The sentence that decides the slide is moved into tier two, so the argument only completes once something is opened. | Ledger slide |
| **S5** Craft | One panel's type is set to 11 design units, below the 18-unit floor, and another panel is knocked 17 units off its grid track. | Small Multiple slide |
| **S6** Motion | The aside gets a looping ambient pulse that encodes nothing. | Uncomfortable Truth slide |
| **D1** Spine | Slides are reordered so the comparison opens the deck and the Why-Now arrives ninth. The sequence stops retiring objections. | whole deck |
| **D2** Pacing | The small multiple is split across three near-identical slides. Same archetype three times, length set by dumping. | whole deck, now 14 slides |
| **D3** Close | The ask becomes a recap and a thank-you. | Close slide |
| **D4** Consistency | The reserve is restated as $2.2M, contradicting the $1.5M the ledger established. | Gate slide |

### What the mechanical gate caught

Running the auto and render gates over both decks:

| Dimension | Good deck | Seeded deck | Caught mechanically |
| :--- | :--- | :--- | :--- |
| S3 | 7 figures, 0 card rows | 8 figures, **1 card row** | yes |
| S5 | 0 runs below the floor | **12 runs at 11 units** | yes |
| S6 | 1 infinite animation (the sanctioned `Current` flow) | **`seededThrob` on a static aside** | yes |
| D2 | 12 sections | **14 sections** | yes |
| D3 | last slide *Approve the frequency package* | last slide ***Thank you*** | yes |
| S1, S2, S4, D1, D4 | — | — | **no — judgement only** |

Five of ten seeded defects are invisible to any static or measured check, which is what
`EVALUATION.md` predicts: those five are `judge` rules. **The gate is necessary and nowhere near
sufficient**, and a pipeline that stops at the gate would ship a deck whose headline is a topic
label, whose figures disagree with each other, and whose slides are ordered by topic.

---

## Reproducing the measurements

The deck is built by hand. Everything asserted about it above is reproducible:

```bash
python tools/deck/audit.py examples/reference-deck.html
```

```bash
python tools/deck/render.py measure examples/reference-deck.html
```

```bash
python tools/deck/contract.py examples/reference-deck.html
```

```bash
python tools/deck/contract_variants.py
```

```bash
python tools/examples/seed_defects.py
```

`audit.py` runs the auto gate, the contrast audit, the render gate and the resolution contract —
43 checks against `DS-nnn` rules. `contract.py` is that last stage on its own: it sweeps four
viewports and two resolutions, because §2.4 and §2.5 are claims about what happens *between*
viewports and no single render can decide them. **`contract_variants.py` breaks each of those
rules on purpose and requires the gate to notice** — a check that has only ever passed is not
evidence that it checks anything, and three of these were caught measuring nothing the first time
it ran. `render.py measure` produces the 720p and two-resolution numbers. `render.py shots`
writes one PNG per slide so the deck can be *looked at*, which is the check none of the others
replace. Both drive **real Chrome with a clean throwaway profile and every DNS lookup black-holed**,
because a preview pane is not a faithful `file://` environment and has given this project a
confident wrong answer four times (**L-06**, **L-15**).

Running the audit over both decks is what produced the table above: the good deck reports **0
mechanical failures**; the seeded deck reports **3** — and the other seven seeded defects are
invisible to it.
