---
id: T-087
title: Sweep the reference deck's figure ledger for the pattern T-082 found
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-082, T-086]
work_package: v0.2
owner: the project owner
business_value: medium
effort: m
created: 2026-08-10
updated: 2026-08-10
deliverables: []
---

# T-087 — Sweep the reference deck's figure ledger for the pattern T-082 found

## 1. Specify

**Outcome**
The reference deck's figures are reconciled against its own provenance record on the same terms
`sort-window` now is: every value the deck asserts is traceable, and no record cell claims a slide
that does not show the value.

**Why this one**
[T-082](T-082-the-worked-examples-figure-ledger-omits-figures-that-reach-slides.md) §1 put the
reference deck out of scope with a condition attached — *check it separately if the sweep here finds
a pattern*. It found one, three times over:

- 26 figures with no ledger row, against three expected, and five of them tier one rather than
  behind a disclosure;
- **eleven values in no source document at all**, which is a DS-102 failure and not a bookkeeping
  one;
- twelve `Used on` cells wrong in both directions, and two slides declaring fewer sources than they
  cite.

**The condition has triggered, and the instrument now exists.** T-082's sweep was a throwaway
extractor written because `content.py`'s `FIGURE` pattern cannot see `6 rounds`, `04:10` or
`31 peak working days` — it reported *0 unsourced of 69* on a deck with eleven unsourced values.
Rebuilding it is most of this task's cost, and **L-62** is the reason it must not simply be the
existing gate rerun.

**Scope**
- In: the reference deck, its sources if it has them, and whatever record plays the ledger's part.
- In: whether it has an equivalent record at all. If it does not, the finding is that a deck this
  project ships as its reference discharges DS-102 differently from the one it ships as its worked
  example, and that difference is the deliverable rather than a defect list.
- Out: building the gate. That is
  [T-086](T-086-check-that-every-ledger-row-appears-on-the-slides-its-used-on-names.md), and this
  task is the second calibration case for it rather than a consumer of it.
- Out: rewriting the reference deck's content. A figure with no source is fixed the way T-082 fixed
  its eleven — by sourcing it, unless the value is wrong.

**Inputs**
- [`examples/reference-deck.html`](../examples/reference-deck.html) — the deck.
- [T-082](T-082-the-worked-examples-figure-ledger-omits-figures-that-reach-slides.md) §2 and §3 —
  the sweep method and the rule for what earns a row, both reusable verbatim.
- [`docs/LESSONS.md`](../docs/LESSONS.md) — **L-62**, which is why step 1 is not `content.py`.

**Acceptance criteria**
- [ ] Every figure the reference deck asserts is listed, with a source or a recorded reason it has
      none
- [ ] Any value in no source is dispositioned — sourced, corrected, or removed — and which, per value
- [ ] Every record cell naming a slide is verified against what that slide shows
- [ ] The gates the reference deck already passes stay green, and it has been opened and looked at
      offline
- [ ] If the reference deck has no ledger-equivalent, that is recorded as the finding, with what it
      relies on instead

**Open questions**
- Whether a deck that is a *shell and theme reference* rather than an argued case owes a figure
  ledger at all. Decide at `specify`, after reading what figures it actually carries.

**What reconnaissance on 2026-08-10 already established**, so it is not rediscovered:

- **It ships no specification pair.** `examples/` holds `reference-deck.html` and
  `examples/sources/` — three source documents and a README — and no `.foundation.md` or
  `.slides.md`. It was built by hand before those two formats existed. So there is no ledger to
  sweep, and AC 5 is the live branch rather than AC 1's: the finding is what it relies on instead,
  which is `examples/sources/` plus the colophon [T-069](T-069-extend-the-provenance-mark-to-multiple-sources.md) added.
- **The open question leans yes, and not on principle.** 13 sections carry `class="slide"`, all 13
  declare `aria-label="Slide N"`, and a wide sweep found **102 distinct figure-shaped values** across
  them. A deck asserting that many figures is not discharging DS-102 by being a theme sample.
- **`spec.py` is usable here the moment a foundation exists.** `SPEC-5` shipped with
  [T-086](T-086-check-that-every-ledger-row-appears-on-the-slides-its-used-on-names.md), and
  `spec.slide_text`, `spec.canonical` and `spec.shows` are importable — the slide-number reader and
  the value matcher no longer have to be rebuilt, only the *figure extractor* does.
- **The first wide pattern over-captured and must not be reused as written.** Allowing a trailing
  word after the numeral produced keys like `12,200 weekday`, `18 is` and `2029, and`, which then
  fail to match a source that phrases the same figure differently — 48 of 102 reported as unsourced,
  most of them artefacts. Separate the numeric core from its context: match the core, show the
  surrounding words to the reader, and judge on the core. **L-62** still holds — wider than the gate,
  and thrown away afterwards — but wider means *more numerals*, not *longer strings*.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- <T-NNN or "none">

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-10 | (no change) | Reconnaissance only, recorded in §1 rather than acted on: no specification pair exists, 102 figure-shaped values sit across 13 slides, `SPEC-5`'s matcher is now reusable, and the first wide pattern over-captured in a way the next attempt must avoid. Left at `proposed` deliberately — the sweep and the per-value disposition are the task, and starting them with no room to finish is what T-068 cost a session by. |
| 2026-08-10 | → proposed | Raised by [T-082](T-082-the-worked-examples-figure-ledger-omits-figures-that-reach-slides.md) §1's own condition, which put the reference deck out of scope unless the sweep found a pattern. It found one three times the expected size, including eleven values traceable to no source. `m` rather than `s` because the throwaway extractor has to be rebuilt — L-62 rules out sweeping with the gate that missed them. `v0.2`, under the `l` line. |
