---
id: T-082
title: The worked example's figure ledger omits figures that reach slides, so the ledger cannot be the authority it is treated as
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-071, T-086]
work_package: PH2
shipped_in: 0.2.0
owner: the project owner
business_value: medium
effort: s
created: 2026-08-10
updated: 2026-08-12
deliverables:
  - examples/sort-window/sort-window.foundation.md
  - examples/sort-window/sources/throughput-model.md
  - examples/sort-window/sources/fleet-and-cost-model.md
  - examples/sort-window/sources/service-calendar.md
---

# T-082 — The worked example's figure ledger omits figures that reach slides, so the ledger cannot be the authority it is treated as

## 1. Specify

**Outcome**
[`examples/sort-window/sort-window.foundation.md`](../examples/sort-window/sort-window.foundation.md)'s
figure ledger holds **every** figure that reaches a slide, so the rule it is quoted under — the
ledger is authoritative where it and a slide disagree — is a rule about a complete record rather than
a partial one.

**Why this one**
Found 2026-08-10 while assigning per-slide sources in
[T-071](T-071-the-intermediate-specifications-carry-their-references.md). Three figures appear in the
slide specification and have no ledger row, and all three are in the source documents, so none is
fabricated — the ledger is incomplete, not wrong:

| Figure | Where it ships | Where it comes from |
| :--- | :--- | :--- |
| 31,900 peak volume | slide 10's disclosure, as the condition that breaks the recommendation | the throughput model's busiest single day |
| $140k slot premium | slide 9's disclosure, as half of the cost build-up | the fleet and cost model |
| $170k six-person crew | slide 9's disclosure, the other half | the fleet and cost model |

Two more were found the same way and **fixed in T-071**, because that task's new check reads the
`Used on` column and could not be calibrated against cells known to be wrong: `Sort rate` and
`Proposed second cut-off` both omitted slide 10, which cites each of them.

**Why this matters more than three missing rows.** DS-102 is a `hard` rule and the ledger is how this
project discharges it for an illustrative deck. T-071 then made the ledger **authoritative** in a
check: where a slide's declared sources and the ledger disagree, the slide is corrected. A record that
wins arguments has to be complete, or the checks built on it are calibrated against a subset and quietly
agree with whatever is missing.

**The pattern behind all five is one thing: a figure behind a disclosure.** Every omission is in tier
two — a derivation panel or a condition panel. Tier one was ledgered carefully; the click was not. That
is a rule about where to look, not an accident, and it is the part worth carrying beyond this task.

**Scope**
- In: the three missing rows, with `Origin` and `Used on` filled from the source documents.
- In: a sweep of the remaining ten disclosure panels for the same omission, since three of the five
  found so far came from one place.
- In: whether anything should **check** this. The content half of
  [`check.py`](../tools/deck/check.py) reconciles the deck against `sources/`; whether it also
  reconciles the deck against the *ledger* is the open question, and the answer decides whether this
  recurs.
- Out: the reference deck, which is a different deck with a different ledger. Check it separately if
  the sweep here finds a pattern.
- Out: DS-102's wording, which is correct as it stands.

**Inputs**
- [`examples/sort-window/sort-window.foundation.md`](../examples/sort-window/sort-window.foundation.md)
  — the ledger, and the two `Used on` cells T-071 corrected.
- [`examples/sort-window/sort-window.slides.md`](../examples/sort-window/sort-window.slides.md) — every
  figure that ships, tier one and tier two.
- `examples/sort-window/sources/` — the three source documents all five figures were traced to.

**Acceptance criteria**
- [ ] The three rows exist, with an origin traced to a source document and a correct `Used on`
- [ ] The other ten disclosure panels have been swept, and what the sweep found is recorded — including
      "nothing", which is a result
- [ ] Whether ledger completeness gets a check is decided, with the reason
- [ ] `python tools/deck/spec.py` on the pair stays green, and its SPEC-4 row is now calibrated against
      a complete ledger

**Open questions**
- none

## 2. Plan

**The sweep had to be mechanical, because the tools share one blind spot.** `content.py`'s `FIGURE`
pattern requires a currency mark, a separator, a decimal, a magnitude letter or a unit word, so
`6 rounds`, `04:10`, `27 of 31` and `31 peak working days` are not figures to it. Sweeping by eye
against the same instrument that missed them would measure the blind spot twice, so step 1 extracts
every number-bearing run per slide with a deliberately wider pattern and marks bare-number runs as
scale marks.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Extract every number-bearing text run of the built deck, per slide, tier one and tier two, wider than `FIGURE` and marking axis ticks as scale | The sweep, over all twelve slides and all ten panels |
| 2 | Reconcile each against the ledger's 29 rows, in both directions — figures with no row, and rows naming a slide that does not show the value | The row list and the `Used on` corrections |
| 3 | Trace every unledgered figure to a source document; where none carries it, decide whether the source gains it or the deck loses it | The orphan list and its disposition |
| 4 | Where a figure's `Origin` is a source a slide does not declare, correct the slide — SPEC-4's rule, in the direction it names | Slide `Sources` fields, and the deck's provenance marks to match |
| 5 | Rewrite the ledger complete and corrected; update the source list's *What it carries* cells | [`sort-window.foundation.md`](../examples/sort-window/sort-window.foundation.md) |
| 6 | Decide the check question against what step 1 proved about the instrument | §3 *Decisions*, and a child task if the answer is yes |
| 7 | Run the gates, and open the deck offline | §4 |

## 3. Implement

**What the sweep found.** The ledger went from 29 rows to 58. Three of the 29 additions are this
task's; the other 26 came from the sweep, and 4 existing rows were over-claiming rather than under.

| What | Count | Where |
| :--- | ---: | :--- |
| Figures with no row, traced to a source already carrying them | 15 | tier one and tier two |
| Figures with no row and **in no source document** | 11 | slides 6 and 10 |
| Rows naming a slide that does not show the value | 4 | `12.4%`, `2.4%`, `84%`, `16%` |
| Rows omitting a slide that does show it | 8 | including `01:00`, `95%`, `4%`, `19 September` |
| Slides whose `Sources` omitted a source they cite | 2 | slides 4 and 11 |

**Decisions & assumptions**

- **The eleven unsourced values were given to the sources, not taken off the deck** — 2026-08-10.
  Slide 6's `instances` panel ships four round counts, four departure times and *27 of 31 peak
  nights*; slide 10 ships a crew shift of *22:00 to 02:30, five nights a week*. None was in any
  source, so the deck's own claim — every figure is an output of the assumptions in `sources/` — was
  false. These sources are illustrative and this project authors them, so the district table gained
  `Rounds` and `First away` columns, the calendar gained the board date and the crew hire lead, and
  the cost model gained the crew's shift. Deleting good tier-two detail to make a record true would
  have been the wrong repair to a record that was the thing at fault.
- **What earns a row is now written into the foundation** — 2026-08-10. Every value the deck states
  as a fact, with one exclusion: arithmetic the deck performs on screen from figures that already
  have rows. `2h 19m` is slide 5's panel working, not a figure it asserts. Exactly one value in the
  deck falls under the exclusion, which is a line worth having precisely because it is narrow.
- **Slide 1 carries no row, and it is a judgement** — 2026-08-10. Its eyebrow prints the occasion
  and its standfirst introduces the term *a nightly window that closes at 01:00*. Neither presents a
  measurement, the slide declares `Sources: none`, and the deck gives it no provenance mark. Claiming
  it would have forced a provenance mark onto a manifesto title slide to satisfy SPEC-4.
- **Two slides were corrected rather than the ledger** — 2026-08-10, SPEC-4's own rule. Slide 4 draws
  the 4% contractual threshold and declared only the throughput model; slide 11 reads its gate over
  the 31 peak working days and declared only the fleet and the calendar. Both were invisible before,
  because a figure with no row is a figure SPEC-4 has nothing to compare.
- **The ledger is grouped by source now** — 2026-08-10. At 58 rows, completeness is only checkable by
  a reader who can hold one source document beside one block.
- **The check question: half of it, and not the half asked about** — 2026-08-10. Completeness cannot
  be gated. It needs something that enumerates every figure on a slide, and `content.py`'s `FIGURE`
  is the only such thing here: it reported *0 unsourced of 69* on this deck while eleven values sat
  in no source, because it cannot see `6 rounds`, `04:10`, `27 of 31` or `31 peak working days`. A
  gate on that instrument would certify a ledger missing exactly what this sweep found. Widening it
  to any digit makes every axis tick a figure. So completeness stays DS-102's `judge`.
  **The reverse direction is exact and gets a check**: searching for a known value on a known slide
  needs no recogniser, and it catches the four over-claims found here.
  [T-086](T-086-check-that-every-ledger-row-appears-on-the-slides-its-used-on-names.md) carries it,
  as `m` rather than `s` — no existing tool takes both a foundation and a deck.

**Outputs produced**
- [`examples/sort-window/sort-window.foundation.md`](../examples/sort-window/sort-window.foundation.md)
  — the ledger, 58 rows, with what earns a row and what does not
- [`examples/sort-window/sources/throughput-model.md`](../examples/sort-window/sources/throughput-model.md)
  — district rounds, first departures, and the loading-sequence stability
- [`examples/sort-window/sources/fleet-and-cost-model.md`](../examples/sort-window/sources/fleet-and-cost-model.md)
  — the crew's shift and nights
- [`examples/sort-window/sources/service-calendar.md`](../examples/sort-window/sources/service-calendar.md)
  — the board date and the crew hire lead
- [`examples/sort-window/sort-window.slides.md`](../examples/sort-window/sort-window.slides.md) —
  slides 4 and 11 `Sources`
- [`examples/sort-window/sort-window.html`](../examples/sort-window/sort-window.html) — slides 4 and
  11 provenance marks
- [`docs/LESSONS.md`](../docs/LESSONS.md) — **L-62**

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The three rows exist, with an origin traced to a source document and a correct `Used on` | met | `31,900` → slide 10, `$140k` → 9, `$170k` → 9 and 10. The last ships on slide 10's tier one as well, which the specification did not say |
| The other ten disclosure panels swept, and what the sweep found recorded — including "nothing" | met | §3's table. Two panels were clean; the sweep also ran over tier one, which is where 5 of the 26 additions came from |
| Whether ledger completeness gets a check is decided, with the reason | met | No, and the reason is that the only figure recogniser here cannot see the figures that went missing. The checkable half is [T-086](T-086-check-that-every-ledger-row-appears-on-the-slides-its-used-on-names.md) |
| `spec.py` on the pair stays green, and SPEC-4 is calibrated against a complete ledger | met | All four pass. SPEC-4 failed first against slides 4 and 11 and was resolved in the slides' direction, which is the rule it states |

**Verification**

```
  SPEC-1   every slide answers Sources                        pass
  SPEC-2   every named slug is listed                         pass
  SPEC-3   every listed source is used                        pass
  SPEC-4   slides agree with the ledger                       pass

  FIG-1  figures on a slide that appear in no source: 0 of 69  pass
  FIG-2  figures disagreeing with the source they came from: 0 pass
  FIG-3  figures appearing twice in the deck with different values: 0 pass

  check.py    0 failure(s): none
  refcheck.py OK - 1189 document pointer(s) checked, 0 broken
```

**FIG-1 read *pass* before this task and after it, and the number of source figures moved from 53 to
54.** That is the whole of what the existing content gate could see of eleven fabricated values being
given sources — which is L-62, stated as a measurement.

**Looked at.** Slides 4 and 11 captured with `python tools/deck/render.py shots`, real Chrome,
network black-holed. Slide 4's provenance mark reads *2 sources* where it read *Throughput model*,
slide 11's reads *3 sources*, both collapsed at rest, and neither slide's layout moved.

**Child fix tasks raised**
- [T-086](T-086-check-that-every-ledger-row-appears-on-the-slides-its-used-on-names.md)

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-10 | (no change) | Owner ratified the direction taken on the eleven unsourced values: the sources gained them, the deck kept them. The rival — cutting them from the deck, which is the honest move when a real engagement's sources are not yours to write — was put and declined. Recorded because these sources are authored fiction and a later reader will otherwise re-open the question. |
| 2026-08-10 | → done | Ledger complete at 58 rows. The sweep was three times the size the specification expected: 26 additions beyond the three named, 12 `Used on` cells corrected in both directions, and — the finding that changed the fix — eleven values on slides 6 and 10 that were in no source at all, so the sources gained them rather than the deck losing them. Two slides declared fewer sources than they cite and were corrected in SPEC-4's own direction, which took the deck's provenance marks with them. The check question is answered no for completeness and yes for the reverse direction, raised as [T-086](T-086-check-that-every-ledger-row-appears-on-the-slides-its-used-on-names.md). **L-62** carries the method finding: FIG-1 read `0 unsourced of 69` throughout. |
| 2026-08-10 | → planned | Plan set. Step 1 is a throwaway extractor rather than the existing figure pattern, because sweeping with the instrument that missed the first three would measure its blind spot twice. |
| 2026-08-10 | → proposed | Raised from [T-071](T-071-the-intermediate-specifications-carry-their-references.md), which needed the `Used on` column to be right before it could check anything against it and found five cells that were not. Two were corrected there because the new check read them; three are additions and are this task's. `medium` because nothing shipped is a fabricated figure — every one traces to a source — but a ledger that wins disagreements has to be complete to deserve that; `s` because the sweep is ten panels and the rows are three. `PH2`: a minor fix to a worked example. |
