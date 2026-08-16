---
id: T-170
title: The reference deck states four evaluation dates no source carries
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-169]
work_package: PH1
shipped_in: unreleased
owner: the project owner
business_value: high
effort: s
created: 2026-08-16
updated: 2026-08-16
deliverables:
  - examples/sources/programme-timetable.md
---

# T-170 — The reference deck states four evaluation dates no source carries

## 1. Specify

**Outcome**
`python tools/deck/check.py examples/reference-deck.html examples/sources` reports `FIG-1` pass
again, because the four dates the deck states are either in a source or off the slides — decided as
a content question and not by loosening the gate.

**What was found.** [T-169](T-169-the-figure-binder-cannot-bind-a-value-split-across-table-cells.md)
taught the ledger to read a time word before its numeral. The reference deck gained eleven figures
of kind `month`; seven bind to `programme-timetable.md` and **four appear in no source**:

| Figure | Slide | The run |
| :--- | :--- | :--- |
| `months 13` | Month eighteen stays reversible | Boardings on the six trunk routes, months 13 to 18 |
| `month-9` | Month eighteen stays reversible | Service holds at month-9 levels |
| `month 12` | Three things would change this | Measured month 12 · by the annual household survey |
| `month 12` | Three things would change this | Measured month 12 · by the city auditor |

**The sources say none of it.** `examples/sources` states a gate at month 18, 14 months to first
benefit for bike-share and 4 months for bus frequency. There is no month 9, no month 12, and no
measurement window. The deck's evaluation plan invented its own timetable.

**This is FIG-1 doing its job, on the deck this repository ships to demonstrate it.** The figures
were unreadable before T-169, so the row was green on a check that could not see them — the same
shape as **L-105**, one layer along. It is not collateral damage from T-169 and must not be fixed by
narrowing the binder.

**Scope**
- In: decide, per figure, whether the **source** is incomplete or the **deck copy** is unsupported.
- In: whichever of the two is wrong, correct it — and rebuild the deck if it is the deck.
- Out: changing `FIG-1`, `FIGURE` or the binder. T-169 owns those and they are not at fault here.
- Out: `examples/reference-deck-seeded-defects.html`, which is derived from the reference deck by
  `seed_defects.py` and follows it.

**The decision this needs, and why it is not mine to take alone.** Adding the dates to
`programme-timetable.md` turns the gate green in one edit — and *making the source say what the
slide says* is precisely the move FIG-1 exists to catch. It is right only if a real programme
timetable would carry an evaluation schedule, which is a judgement about the fixture's content.
The alternative is to cut the unsupported dates from the deck copy, which costs a rebuild.

**Ruled by the owner 2026-08-16: the source corpus is incomplete. Add the dates to
`programme-timetable.md`.** The deck copy stands.

**What that ruling has to survive**, because
[`examples/sources/README.md`](../examples/sources/README.md) argues against its own worst version:
the sources exist so the content check has a real case *rather than a fixture that agrees with the
deck by construction*. A list of four numbers copied off the slides is that fixture. So each date is
written with the reason it falls where it does — why the measurement window opens at month 13 and
not at month 9, why two of the three tripwires are read at month 12 — and a reader who disagrees
with the timetable can now say so, which is the property a source has and a lookup table does not.

**Acceptance criteria**
- [ ] Each of the four figures has a recorded verdict: source incomplete, or deck copy unsupported
- [ ] `FIG-1` passes on `examples/reference-deck.html` with no change to `content.py`
- [ ] `examples/reference-deck-seeded-defects.html` still derives from the deck — `seed_defects.py --check`
- [ ] No other row on any shipped deck moves

**Open questions**
- ~~Is the fixture's source corpus meant to carry an evaluation timetable~~ — answered 2026-08-16:
  yes, and it was missing them.

## 2. Plan

Three additions to [`examples/sources/programme-timetable.md`](../examples/sources/programme-timetable.md),
each written as a statement the document would have made anyway:

1. **A milestone table** — approval at month 0, first schedule change at month 4, full modelled
   service at month 9, gate at month 18 — plus what *month 9 levels* means, which is the phrase the
   deck's failure branch uses.
2. **The measurement window** in the review gate section: months 13 to 18 against the same months
   two years earlier, and why it opens at 13.
3. **A tripwire reading table** — which tripwire is read at month 4 and which two at month 12, and
   by whom.

**Deliberately no figures other than the dates.** The tripwire thresholds — the headway limit, the
demand trigger, the cost ceiling — already live in `cost-model.md` and `ridership-model.md`.
Restating them here would put the same quantity in two source documents, which is what `FIG-4`
reports as a conflict candidate for a person to read, and this document would be manufacturing the
reading list.

**Verified** by the same instrument T-169 ended on: every row of the per-deck gate, 114 of them,
on all four decks, before and after.

## 3. Implement

**Decisions & assumptions**

- **Reasons, not just numbers** — 2026-08-16. See §1. Each date carries why it falls there, so the
  document stays a model of the programme rather than a lookup table keyed by what the slides say.
- **The deck was not touched and not rebuilt** — 2026-08-16. `quickview.py list
  examples/reference-deck.html` reports **0 quick views**, so the deck embeds no copy of any source
  and editing one leaves nothing in it stale. The three `qv-src` hits in the file are the shared
  shell's styles.
- **`examples/sources/README.md` needed no change** — 2026-08-16. It already describes the timetable
  as carrying *dates, durations, thresholds and the review gate*, which is what was added.

**Outputs produced**

- [`examples/sources/programme-timetable.md`](../examples/sources/programme-timetable.md) — the
  milestone table and its paragraph, two sentences in *The review gate*, the tripwire table and its
  paragraph.

**Measured — 114 gate rows on each of four decks, against the state T-169 left:**

| Deck | Rows moved |
| :--- | :--- |
| `examples/reference-deck.html` | FIG-1 `4 of 80` → **`0 of 80`**, and nothing else |
| `examples/reference-deck-seeded-defects.html` | FIG-1 `6 of 91` → **`2 of 91`** — its two seeded `$2.2M` defects and nothing more |
| `examples/sort-window/sort-window.html` | **none** |
| `examples/measure-first/measure-first.html` | **none** |

`python tools/deck/check.py examples/reference-deck.html --sources examples/sources` — **0
failure(s)**.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Each of the four figures has a recorded verdict: source incomplete, or deck copy unsupported | met | All four **source incomplete**, ruled by the owner 2026-08-16. The deck copy stands and was not edited |
| `FIG-1` passes on `examples/reference-deck.html` with no change to `content.py` | met | `0 of 80`. `tools/deck/content.py` is untouched since T-169's commit |
| `examples/reference-deck-seeded-defects.html` still derives from the deck — `seed_defects.py --check` | met | `OK - exactly what regenerating produces (276899 bytes)`. The tool is [`tools/examples/seed_defects.py`](../tools/examples/seed_defects.py), not `tools/deck/` as this criterion implied |
| No other row on any shipped deck moves | met | One row moves on each of two decks and both are `FIG-1` falling. 113 of 114 rows identical on the reference deck; `sort-window` and `measure-first` identical throughout |

**Closing checklist step 3 does not apply.** The task produced a Markdown source document. No deck
was built or rebuilt, and the deck embeds no copy of it.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-16 | → proposed | Raised out of [T-169](T-169-the-figure-binder-cannot-bind-a-value-split-across-table-cells.md)'s review, which recorded *no shipped deck moves* as **not met** against exactly these four figures. The gate is red on the reference deck from that commit until this closes. |
| 2026-08-16 | → specified | The owner ruled the open question the same day: the source corpus is incomplete, add the dates. The deck copy stands. |
| 2026-08-16 | → planned | Three additions, dates only. The tripwire thresholds are left where they already live — restating them here would have this document manufacturing its own `FIG-4` reading list. |
| 2026-08-16 | → in_progress | Written with the reason each date falls where it does, which is what keeps the file a model rather than a lookup table keyed by the slides — the failure `examples/sources/README.md` warns about in its own second paragraph. |
| 2026-08-16 | → done | All four criteria met. `FIG-1` `4 of 80` → `0 of 80`; the reference deck is green on all 114 rows for the first time since T-169 landed, and the seeded fixture is back to its two designed defects. |
