---
id: T-087
title: Sweep the reference deck's figure ledger for the pattern T-082 found
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-082, T-086]
work_package: v0.2
owner: the project owner
business_value: medium
effort: m
created: 2026-08-10
updated: 2026-08-11
deliverables: [examples/sources/ridership-model.md, examples/reference-deck.html, examples/README.md]
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
- ~~Whether a deck that is a *shell and theme reference* rather than an argued case owes a figure
  ledger at all.~~ **Answered 2026-08-11: it owes a record, and it already has one — a different
  one.** Not a ledger, and it does not need one. Its record is **source-level**: a colophon naming
  three model documents, what each carries and which slides rest on it, with a per-slide provenance
  mark saying the same from the other end. `sort-window`'s is **figure-level**: 58 rows binding a
  value to a source *and to the slides it appears on*. The deciding evidence is that the deck asserts
  **157 figure occurrences across twelve slides** — a deck making that many claims is not discharging
  DS-102 by being a theme sample — and that its existing record, once checked, was wrong in the way
  a ledger would have caught. Retrofitting a `.foundation.md` was rejected: it would make the deck
  claim to be a build-mode output, which it is not, and `SPEC-5` would then be checkable here at the
  cost of the one example that shows what a hand-built deck's provenance looks like.

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
| 1 | Establish what plays the ledger's part, and settle the open question from what the deck carries | §1's answer: a source-level record, not a figure-level one |
| 2 | Rebuild the extractor, wider than `content.py` and narrower than the attempt §1 records as failed | A throwaway that reads the numeric core and *shows* its context instead of matching it |
| 3 | Sweep every figure against the three model documents | The unsourced list, per slide, with context |
| 4 | Check the record against **itself** — the colophon's slide lists against the twelve provenance marks | Both directions, per source |
| 5 | Check the record against the **deck** — attribute each figure to the sources that carry it, and compare with what its slide declares | SPEC-4's question, asked of a deck with no ledger to ask it from |
| 6 | Disposition every finding: source it, correct it, or record why it has none | Edits to the model documents and to the deck's provenance marks |
| 7 | Re-run every gate the deck passes, regenerate what derives from it, and look at the changed slides offline | The verdict lines, and the shots |

## 3. Implement

**Decisions & assumptions**
- **The record was self-consistent and still wrong, which is the whole finding** — 2026-08-11. The
  colophon's three slide lists matched the twelve provenance marks **exactly, in both directions**,
  before anything was touched. That agreement proved only that the record agrees with itself.
  Checked against the figures, **three slides cited sources they did not declare**. Carried out as
  **L-65**.
- **Two of those three were corrected in the deck; the third was not** — 2026-08-11. Slide 2 is the
  timetable slide — budget vote, grant close, the nineteen days, the three-year cycle — and declared
  the cost model alone; it now declares the programme timetable too. Slide 10's disclosure carries
  six per-corridor figures that only the ridership model holds, and now declares it. **Slide 1 was
  left alone**: its `month 18` is a forward reference to the gate that slide 11 argues and declares,
  and its `March 2027` is a dateline. [T-082](T-082-the-worked-examples-figure-ledger-omits-figures-that-reach-slides.md)
  §3 already declined to force a provenance mark onto a title slide, and this is that case.
- **The twelve corridor figures were sourced, not cut** — 2026-08-11, which is T-082's rule and this
  task's scope line. Slides 6 and 10 assert new daily trips per corridor under both proposals; the
  ridership model carried **one of the twelve**. It now carries all twelve, as a three-column table,
  plus the year-one basis that makes `2029` and `2028` derivations rather than assertions.
- **The corridor names were fixed in the source, not in the deck** — 2026-08-11. The deck says
  *Riverside Park*, *University Spur*, *Airport Road*; the model said *Riverside*, *Mill Row*,
  *Harbour Gate*, against identical weekday-trip values, so they are three names for the same three
  corridors. The deck is what a reader sees and rewriting its content is out of scope, so the model
  took the deck's names.
- **One statement in the model was wrong rather than missing** — 2026-08-11. It read *the six trunk
  routes carry 36,000*; 36,000 is the sum of the three corridors frequency wins, and the deck says
  so. Corrected in the model.
- **`FIG-1` read `0 unsourced of 69` before and after twenty values were sourced** — 2026-08-11.
  Its pattern sees 69 figures where the throwaway sees 157 occurrences, so it was as blind here as
  **L-62** found it on the worked example. This is the second deck on which that has been measured,
  and it is why the sweep was not the gate rerun.
- **The out-of-sync sprite failed `DS-063` as well as `DS-113`, and only one of them named the
  cause** — 2026-08-11. Adding slide 2's source mark made `shell.py check` red, as designed, and
  `check.py` red too with two DS-063 geometry failures. Running the remedy `shell.py check` prints —
  `shell.py icons` — cleared both, and three consecutive `check.py` runs are clean since. Stated as
  observed rather than as a proven mechanism. The gate list already runs `shell.py` before
  `check.py`, which is what made the expensive failure interpretable.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every figure the reference deck asserts is listed, with a source or a recorded reason it has none | met | 157 occurrences swept across the twelve slides. 153 resolve to one of the three model documents; **four have a recorded reason and no source** — the deck's own build date `6 Aug 2026`, slide 6's `0–700` shared axis maximum, and slide 7's `2,000` and `6,000` y-axis ticks. A scale mark is not a figure a reader repeats, which is `content.py`'s own rule and T-082's for on-screen arithmetic |
| Any value in no source is dispositioned — sourced, corrected, or removed — and which, per value | met | **Twenty sourced**: the twelve per-corridor new-daily-trip values, the three corridor names, the `2027`–`2031` modelled period, and the derived `2029` and `2028`. **One corrected**: *the six trunk routes carry 36,000* → the three frequency wins. **Four excused**, above. Nothing removed |
| Every record cell naming a slide is verified against what that slide shows | met | Both directions and both records. The colophon's three slide lists against the twelve provenance marks: exact before and after. The marks against the figures: **three slides under-declared**, two corrected in the deck and one recorded as not a defect. The colophon's lists were updated to match |
| The gates the reference deck already passes stay green, and it has been opened and looked at offline | met | `shell.py`, `component.py`, `theme.py`, `check.py --sources` (82 checked, 0 failing), `static_variants`, `contents_bound`, `ruleset --counts`, `check_scaffold`, `figures.py` (`0 stale`), `lint.py`, and `seed_defects.py --check` after regenerating the derived deck. Slides 6, 10 and the corrected 2 were rendered from `file://` and read |
| If the reference deck has no ledger-equivalent, that is recorded as the finding, with what it relies on instead | met | It has one, and it is source-level rather than figure-level. §1's answer, and the reader-facing version is in [`examples/README.md`](../examples/README.md) under *Provenance*, where someone comparing the two shipped decks will meet it |

**Child fix tasks raised**
- none.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-11 | → done | The condition T-082 attached has been discharged, and the answer is not the one the title assumed: there is no ledger here to sweep, and the deck does not owe one. Its record is source-level and it was **self-consistent and wrong** — the colophon and the twelve provenance marks agreed exactly, while three slides cited sources they did not declare (**L-65**). Twenty values sourced, one source statement corrected, four excused with reasons, two slides' marks and both colophon lists fixed. Every gate green, the derived seeded deck regenerated, three slides read offline. `FIG-1` reported `0 unsourced of 69` throughout, on the second deck to measure that (**L-62**). |
| 2026-08-11 | → planned | §1 answered and §2 written in one pass: the open question is a `specify` decision and the plan is the sweep it implies. Worked straight through rather than parked, on the owner's instruction to run the full lifecycle. |
| 2026-08-10 | (no change) | Reconnaissance only, recorded in §1 rather than acted on: no specification pair exists, 102 figure-shaped values sit across 13 slides, `SPEC-5`'s matcher is now reusable, and the first wide pattern over-captured in a way the next attempt must avoid. Left at `proposed` deliberately — the sweep and the per-value disposition are the task, and starting them with no room to finish is what T-068 cost a session by. |
| 2026-08-10 | → proposed | Raised by [T-082](T-082-the-worked-examples-figure-ledger-omits-figures-that-reach-slides.md) §1's own condition, which put the reference deck out of scope unless the sweep found a pattern. It found one three times the expected size, including eleven values traceable to no source. `m` rather than `s` because the throwaway extractor has to be rebuilt — L-62 rules out sweeping with the gate that missed them. `v0.2`, under the `l` line. |
