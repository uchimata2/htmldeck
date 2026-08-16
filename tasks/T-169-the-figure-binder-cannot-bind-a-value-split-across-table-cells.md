---
id: T-169
title: The figure binder cannot bind a value whose label sits in another table cell
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-167, T-128, T-170, T-171]
work_package: PH1
shipped_in: unreleased
owner: the project owner
business_value: medium
effort: s
created: 2026-08-16
updated: 2026-08-16
deliverables:
  - tools/deck/content.py
  - tools/deck/audit.py
---

# T-169 — The figure binder cannot bind a value whose label sits in another table cell

## 1. Specify

**FIG-1 reports a sourced figure as unsourced.**
[T-128](T-128-publish-the-adopter-deck-as-a-worked-example.md)'s deck states the stop-or-go gate at
**month 4** on the slide *€450k in, €1.2m a year out*. `check.py` says:

```
FIG-1   figures on a slide that appear in no source: 1 of 30
        ledger: ["450k in, 1.2m a year out", "4 stop", "month-4 stop-or-go gate"]
```

**The figure is in the source.** `examples/measure-first/sources/D5-management-decision-matrix.md`
carries it twice — once in a table row that holds both halves,
`| **Set the stop-or-go gate** | … | Month 4 |`, and once in prose, *judge the whole programme on
the evidence it produces in month 4*.

**~~Hypothesis, not yet a finding.~~ Replaced 2026-08-16 — the mechanism is below.** The hypothesis
was that the two *labels* fail to overlap: the deck's `month-4` glues the word to the numeral, D5's
label is *month*, two sets with nothing in common and the figure falls out. It is wrong. The labels
were never compared, because the two sides never produced a matching **value** for them to be
compared under.

**The mechanism, from the code.** `FIGURE` in [`tools/deck/content.py`](../tools/deck/content.py)
recognises a figure as **numeral-then-unit** and in no other order — `\d+\s?(?:UNITS)`. Two
consequences, and the failure needs both:

1. **The sources state the gate as unit-then-numeral every time, so they carry no figure for it at
   all.** D5 writes `| … | Month 4 |` in the decision row, *evidence it produces in month 4* in
   prose, and `subject to the month-4 gate` in the funding row. `FIGURE` finds **nothing** in any of
   them. Across all five source documents there is not one figure of kind `month` — 142 source
   figures, none of them this one. There was never anything to bind to.
2. **What the deck contributed is a phantom.** The run `month-4 stop-or-go gate` matched
   **`4 stop`** — the numeral bound to `stop`, taken out of the compound `stop-or-go`, because
   `stops?` is in `UNITS` and nothing requires the unit word to end where the match does. Its
   `kind` is therefore `stop`, not `month`, so even a source figure reading `4 months` would have
   been filtered out one line before any label was compared: `build_ledger` tests `kind` first and
   only then calls `overlap`.

**The premise in this task's title is also wrong.** A markdown table row is one unit —
`source_units` splits paragraphs but keeps `\n(?=\s*\|)` rows whole — so `**Set the stop-or-go
gate**` and `Month 4` are already in the same unit and the same label set. Nothing here is split
across cells. The title is left as filed so the id keeps resolving; the defect is the ordering, not
the cells.

**Reproduced** with `python tools/deck/content.py examples/measure-first/measure-first.html
examples/measure-first/sources`, which prints the offending ledger row as
`| month- or-go gate | 4 stop | - | 450k in, 1.2m a year out |`.

**Why it matters now.** It was recorded as a false alarm on 2026-08-16 and left unraised, on the
grounds that it was 1 of 30 and the binder is documented as approximate. [T-167](T-167-checkpy-reads-a-quoted-source-as-the-decks-own-slide-copy.md)
then cleared the other three failures, and this became **the only thing between T-128's deck and a
green gate**. A false alarm nobody can act on is cheap until it is the last one standing.

**The wider shape is larger than one figure, and it runs both ways.** *Month 4*, *week 2*, *day 30*,
*year 3* — a time word before a numeral is how a plan states a date, and it is ordinary copy in a
deck and in the documents a deck is built from. Every one of them is invisible to the ledger today:
the deck's own `month-19 payback` is not a figure either. So the gap is not that this figure fails
to bind, it is that **a whole class of figure is never offered for binding on either side** — which
is a silent under-report, the opposite of FIG-1's documented over-report, and the direction the
module docstring says these checks do not fail in.

The phantom is the second half and is worse than a miss: `4 stop` is a figure the slide does not
state. Any hyphenated compound opening on a unit word — `stop-or-go`, `day-one`, `month-end` —
mints one, and FIG-1 reports it as *unsourced* rather than as *not a figure*, so the reader is sent
to look for something nobody wrote. Neither rate is visible, because FIG-1 reports a count.

**Scope**
- In: establish the real mechanism from the code before changing anything.
- In: recognise a time word before a numeral as the same figure as the numeral before it, so
  `month 4`, `Month 4` and `month-4` all bind to `4 months`.
- In: stop a unit word taken out of a hyphenated compound from minting a figure.
- In: report which figures FIG-1 failed on, so the next false alarm can be judged without a rerun.
- Out: relaxing FIG-1 into a warning. A rule that cannot be trusted is worse than one that is
  strict, and a deck quoting a figure nobody wrote is exactly what this catches.
- Out: unit-before-numeral for units that are **not** time words. `Route 3` and `Phase 1` name a
  thing, they do not measure one, and admitting them inflates every ledger with identifiers.

**Acceptance criteria**
- [ ] The mechanism is stated from the code, and this task's hypothesis is confirmed or replaced
- [ ] T-128's deck reports `FIG-1` pass with no edit to the deck
- [ ] A fixture carries a time word before its numeral and a unit word inside a compound, red
      before and green after
- [ ] The false-alarm rate is reported as a list, not a count, so the next one can be judged
- [ ] No shipped deck moves

## 2. Plan

All four changes are in [`tools/deck/content.py`](../tools/deck/content.py), the one module that
owns the ledger. Nothing in `check.py` changes: it prints the row text `content.audit` returns.

1. **`TIME_UNITS`, split out of `UNITS`.** The time words become their own constant and `UNITS`
   composes from it, so the two orderings cannot drift apart. One list, two uses.
2. **A second alternation in `FIGURE`** — `(?:TIME_UNITS)[\s-]\d…` — admitting the reversed
   ordering for time words only. It sits *before* the numeral-first branches so `month-4` is taken
   whole rather than leaving `4` to a later branch.
3. **A trailing guard `(?![-\w])` on the numeral-first unit branch**, so a unit word must end where
   the match does. This is what kills `4 stop` out of `stop-or-go`.
4. **`normalise` swaps the reversed form** before it does anything else, so `month-4`, `Month 4` and
   `4 months` are one norm — `4month` — and one `kind`. Without this the two orderings are two
   figures that never meet, which is the defect one layer down.
5. **`audit`'s FIG-1 row names the figures**, capped, after the count.

Each of 2, 3 and 4 gets a `self_test` assertion on strings, per the file's own **L-04** convention.

**How it is verified.** `python tools/check_all.py` for the whole set — the run that is red today
for an unrelated reason (`examples/measure-first/` is undeclared, T-128 step 7) — plus a per-deck
`check.py` on each shipped deck before and after, compared row by row. A ledger is a derived
artifact, so *no shipped deck moves* means the rows compare equal, not that the gate stays green.

**The risk, and where it lands.** Both regex changes alter what counts as a figure, so FIG-2 and
FIG-3 see a different population. The before/after comparison is the instrument for that, and if a
shipped deck does move, the criterion is unmet and the movement is reported rather than absorbed.

## 3. Implement

**Decisions & assumptions**

- **The reversed ordering is admitted for time words only** — 2026-08-16. `TIME_UNITS` is split out
  of `UNITS` and `UNITS` composes from it, so one list serves both orderings and they cannot drift.
  A time word before a numeral still measures something; `Route 3` and `Phase 1` name a thing, and
  admitting them would fill every ledger with identifiers no reader repeats as a number.
- **The compound guard is `(?!-)`, not `(?![-\w])`** — 2026-08-16, and this is a correction made
  during the work. The wider guard is the one that is right in principle: it would also stop
  `4 stopover` minting `4 stop`. It cost a real figure. `runs()` deletes an inline tag instead of
  replacing it, so `<span>The other 5%</span><span>The 02:30 …` arrives as `5%The`, the wider guard
  read that as a compound, and `sort-window`'s `5%` left the ledger. Narrowed to the hyphen and the
  gluing raised as [T-171](T-171-the-ledger-glues-two-words-together-at-every-inline-tag.md), which
  restores the wider guard once the run text is right. Fixing the gluing here would have changed
  every label in every ledger inside a task about the binder.
- **The reversed form is turned round in one exported function, `content.unreverse`** — 2026-08-16,
  and this is the second correction made during the work. It began as three lines inside
  `normalise`, which is enough for the ledger and was not enough for the deck: **`audit.magnitude`
  reads `content.FIGURE` too**, and it reduced `month 18` to the whole string instead of to `18`, so
  the figure matched nothing on the slide face and `DS-231` failed the reference deck for citing
  behind a click a number that slide shows three times. A false alarm this task created. One
  function, imported by both — the discipline the `QUICK_VIEW` comment already states, applied where
  it is hardest to see, because the second reader is in another module and fails on another rule.
- **The FIG-1 row names up to six figures and then counts the rest** — 2026-08-16. Uncapped, a
  badly-sourced deck prints a page into a table row; six is enough to judge whether the row is the
  documented over-report or a real defect, which is the whole reason the criterion exists.
- **`months 13 to 18` yields one figure, not two** — 2026-08-16, accepted. A range's second endpoint
  has no unit of its own and is not matched. It changes no verdict here (13 is unsourced either way)
  and is noted in [T-170](T-170-the-reference-deck-states-four-dates-no-source-carries.md).

**Outputs produced**

- [`tools/deck/content.py`](../tools/deck/content.py) — `TIME_UNITS`; the reversed branch in
  `FIGURE`; the `(?!-)` guard on its unit branch; `REVERSED` and `unreverse`, used by `normalise`;
  the named figures in `audit`'s FIG-1 row; six `self_test` assertions.
- [`tools/deck/audit.py`](../tools/deck/audit.py) — `magnitude` turns the reversed form round
  through `content.unreverse` before reducing it.

**Measured twice, at two altitudes, and the second found what the first could not.** The ledger
comparison — every row of every ledger this repository can build — caught the `5%` regression and
sized the change. It saw nothing of `DS-231`, which is another module's row over the same regex.

**The whole gate, before and after: 114 rows on each of four decks.**

| Deck | Rows moved | Verdicts moved |
| :--- | :--- | :--- |
| `examples/sort-window/sort-window.html` | **none of 114** | none |
| `examples/measure-first/measure-first.html` | FIG-1 `1 of 30` → `0 of 34`; DS-231's population `1` → `2` | **FIG-1 FAIL → pass** |
| `examples/reference-deck.html` | FIG-1 `0 of 69` → `4 of 80`; DS-231's population `6` → `8` | **FIG-1 pass → FAIL** |
| `examples/reference-deck-seeded-defects.html` | FIG-1 `2 of 80` → `6 of 91`; DS-231's population `10` → `12` | none — it fails by design |

**Two row texts move on three decks and one verdict moves in the whole repository.** `DS-231` reads
more cited figures and still passes everywhere. `FIG-2`, `FIG-3`, `FIG-4` and all 110 presentation
and contract rows are identical on every deck. The reference deck's four are a real finding, not
damage — [T-170](T-170-the-reference-deck-states-four-dates-no-source-carries.md).

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The mechanism is stated from the code, and this task's hypothesis is confirmed or replaced | met | **Replaced.** §1 carries it: the sources never produced a figure for the gate at all, and the deck produced a phantom of a different `kind`, so the labels the hypothesis blamed were never compared. Three hypotheses about this module have now been stated and all three were wrong |
| T-128's deck reports `FIG-1` pass with no edit to the deck | met | `0 of 34`, from `1 of 30`. No file under `examples/measure-first/` was touched |
| A fixture carries a time word before its numeral and a unit word inside a compound, red before and green after | met | Six assertions in `self_test`, on strings per **L-04**. Red measured on the old code before the edit: `month-4 stop-or-go gate` returned `['4 stop']` and `month 4` returned `[]` |
| The false-alarm rate is reported as a list, not a count | met | The FIG-1 row names up to six figures with their slides. It is what identified the reference deck's four in one line, without a rerun |
| No shipped deck moves | **not met** | One verdict moves in the whole repository: `examples/reference-deck.html`, `FIG-1` pass → FAIL, on four figures no check here could previously see — [T-170](T-170-the-reference-deck-states-four-dates-no-source-carries.md). `sort-window` is identical on all 114 rows. The one other movement, `DS-231` on the same deck, **was** damage and is fixed rather than routed. **`tools/deck/check.py` is red on the reference deck from this commit until T-170 closes**, and it is red honestly |

**On the unmet criterion.** It was written to stop the binder being loosened until a deck passed, and
it caught the opposite — a check that got stricter because it stopped being blind. Narrowing
`FIGURE` until the reference deck went green would have been the failure the criterion exists to
prevent, wearing the criterion as cover. Recorded unmet with the finding routed, per
[`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §2.

**Closing checklist step 3 does not apply.** This task produced no rendered output — no deck was
built or rebuilt, and no file that renders was edited. The four ledgers above are the evidence.

**Child fix tasks raised**
- [T-170](T-170-the-reference-deck-states-four-dates-no-source-carries.md) — the reference deck's
  four unsourced dates. `PH1`, and it holds the release gate red.
- [T-171](T-171-the-ledger-glues-two-words-together-at-every-inline-tag.md) — `runs()` glues two
  words together at every inline tag it deletes, which is why this task's guard had to be narrowed.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-16 | → proposed | Raised out of [T-167](T-167-checkpy-reads-a-quoted-source-as-the-decks-own-slide-copy.md)'s review. Recorded as a false alarm earlier the same day and deliberately not raised; that judgement was right on the evidence then and wrong by the end of the session, which is the reason to write the promotion down rather than quietly file it. |
| 2026-08-16 | → specified | §1's hypothesis replaced by the mechanism read out of the code. It was wrong, and so was the premise in the title: the sources state the gate as *unit then numeral* every time and `FIGURE` reads only *numeral then unit*, so nothing was ever offered for binding. Scope and two criteria rewritten around that; the title is left alone so the id keeps resolving. |
| 2026-08-16 | → planned | Five changes, all in `content.py`. The verification is a row-by-row ledger comparison on all four decks rather than a verdict check, because a ledger is derived and a green gate hides movement inside it. |
| 2026-08-16 | → in_progress | Implemented, and corrected twice by measurement. `(?![-\w])` dropped `sort-window`'s `5%`, which the ledger comparison caught and a verdict check would not have. Then the whole gate caught what the ledger comparison could not: `DS-231`, in `audit.py`, failed the reference deck because `magnitude` did not know the reversed form — so the swap moved out of `normalise` into `content.unreverse` and both modules read it. |
| 2026-08-16 | → done | Four criteria met, one **not met**: the reference deck's `FIG-1` moves pass → FAIL on four dates no source carries. Kept rather than tuned away — [T-170](T-170-the-reference-deck-states-four-dates-no-source-carries.md) — and [T-171](T-171-the-ledger-glues-two-words-together-at-every-inline-tag.md) raised for the gluing that forced the narrower guard. `tools/check_all.py` is red on the reference deck until T-170 closes. |
