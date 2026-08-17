---
id: T-171
title: The ledger glues two words together at every inline tag it deletes
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-169]
work_package: PH1
shipped_in: 0.3.0
owner: the project owner
business_value: medium
effort: s
created: 2026-08-16
updated: 2026-08-16
deliverables:
  - tools/deck/content.py
---

# T-171 — The ledger glues two words together at every inline tag it deletes

## 1. Specify

**What is wrong.** `runs()` in [`tools/deck/content.py`](../tools/deck/content.py) deletes an inline
tag — `INLINE.sub("", frag)` — instead of replacing it with a boundary. Where two inline elements
butt together with no whitespace between them, which is how a deck's key/value rows are written,
the last word of one and the first word of the next arrive as **one word**:

| In the deck | In the run | In the label |
| :--- | :--- | :--- |
| `<span class="k">The other 5%</span><span>The 02:30 …` | `5%The 02:30 …` | — |
| `<span class="k">If it fails</span><span>Service holds …` | `failsService holds …` | `failsservice` |
| `<span class="k">Measure</span><span>Boardings on …` | `MeasureBoardings on …` | `measureboardings` |
| `<span class="k">What they get</span><span>Nothing until …` | `getNothing until …` | `getnothing` |

**Why it matters.** `label_of` is a set of significant words, and a glued word matches nothing. Two
documents describing one figure in the same words fail to bind because one of them wrote the words
inside adjacent tags — and the failure is invisible, because a label full of `customershigh` and
`getnothing` looks like the approximate matching the module documents.

**It cost a real figure once already.** T-169's first cut guarded the unit branch of `FIGURE` with
`(?![-\w])`, so a unit word could not run on into a compound. `5%The` read as a compound and
`sort-window`'s `5%` left the ledger. The guard was narrowed to `(?!-)` rather than the gluing
fixed, because the two are different defects and the wider guard is the one that is actually right.

**Scope**
- In: replace a deleted inline tag with a space, and prove no figure is split by it.
- In: restore the `(?![-\w])` guard on `FIGURE`'s unit branch once the gluing is gone, so
  `4 stopover` stops minting `4 stop`.
- Out: the non-inline split, which is correct and load-bearing — see the comment above `INLINE`.

**The risk is the reverse direction.** A space where a tag was could split a figure written across
one: `$<b>5.6M</b>` becomes `$ 5.6M`, and `<b>5.6</b>M` becomes `5.6 M`. Both patterns already
allow one `\s?`, so both should survive — that is a prediction, and the before/after ledger
comparison is what tests it.

**Acceptance criteria**
- [ ] A deleted inline tag leaves a word boundary, asserted in `self_test` on strings
- [ ] Every ledger this repository can build is compared before and after; every change is a glued
      word coming apart, and none is a figure lost or a verdict moved
- [ ] `FIGURE`'s unit branch carries the `(?![-\w])` guard, with `4 stopover` asserted
- [ ] No shipped deck moves

## 2. Plan

**The comparison comes first, and it is the plan's centre.** [`L-106`](../docs/lessons/L-106.md) was
written from this module three days' work ago: a verdict cannot verify a change to a matcher, and the
artefact to compare is the one the **consumer** sees. This change has two consumers — the ledger, and
`audit.magnitude`, which reduces a cited figure for `DS-231` in another file. So both are snapshotted
before anything is edited, on all four decks that build a ledger.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Snapshot `content.py`'s ledger and `check.py`'s full row list, for all four decks, before any edit | 8 files, the *before* side of the comparison |
| 2 | `INLINE.sub("", frag)` → `INLINE.sub(" ", frag)` in `runs()` | a deleted inline tag leaves a word boundary |
| 3 | Restore `(?![-\w])` on `FIGURE`'s unit branch, in place of the narrowed `(?!-)` | `4 stopover` stops minting `4 stop` |
| 4 | Extend `self_test` with both halves on strings: a glued pair comes apart, and the two split-figure forms `$<b>5.6M</b>` and `<b>5.6</b>M` survive | known answers, no files (**L-04**) |
| 5 | Snapshot again and diff row by row. Every moved row is classified: a glued word coming apart, or a defect | the *after* side, and the verdict on step 2 |
| 6 | Update the comment above the unit-branch guard, which currently records why the guard is narrow | the reason no longer holds and must not be left standing |

**What step 5 must show.** Every difference is a label or a value gaining a boundary. **No figure
leaves any ledger** — that is the direction the risk points, and `$ 5.6M` / `5.6 M` are the two
shapes that could lose one. **No verdict moves on a shipped deck.**

## 3. Implement

**Decisions & assumptions**
- The guard is restored to `(?![-\w])` rather than left at `(?!-)` — 2026-08-16. T-169 narrowed it
  under protest, in its own comment: the wider form is the right one and it was paying for this
  defect. With the gluing gone it is no longer paying for anything.
- `runs()` substitutes a **space**, not an empty string — the minimal change, and both figure shapes
  that span a tag already tolerate one `\s?`. The prediction was recorded in §1 before the run and
  step 5 is what tests it.
- **A lesson was raised rather than a follow-up task** — 2026-08-16. The result exceeded the
  specification in a way the specification had no words for, and the transferable half is how the
  criterion was written, not anything left undone here. [`L-107`](../docs/lessons/L-107.md).

**Outputs produced**
- [`tools/deck/content.py`](../tools/deck/content.py) — three edits: `runs()` substitutes a space,
  `FIGURE`'s unit branch is back to `(?![-\w])`, and `self_test` gained four assertions covering both
  directions of the trade.
- [`docs/lessons/L-107.md`](../docs/lessons/L-107.md) and its index row.

**The comparison, which is the evidence.** Both artefacts, all four decks that build a ledger,
before and after. Every ledger row reduced to `(value, origin, used on)` and the two multisets
differenced — labels are truncated to four words for display, so a label diff reports formatting and
the multiset reports figures.

| Deck | Ledger rows before → after | Lost | Gained | Gate rows moved |
| :--- | :---: | :---: | :---: | :--- |
| `reference-deck` | 81 → 82 | **0** | 1 | `FIG-1` count only, `0 of 80` → `0 of 81`, pass either side |
| `sort-window` | 70 → 74 | **0** | 4 | `FIG-1` count only, `0 of 69` → `0 of 73`, pass either side |
| `measure-first` | 35 → 35 | **0** | 0 | none |
| seeded-defects fixture | 92 → 93 | **0** | 1 | `FIG-1` count only; the same two unsourced figures, `2 of 91` → `2 of 92`, FAIL either side by design |

**Nothing was lost and six figures were recovered**, which the specification did not predict: the
gluing was not only corrupting labels, it was **hiding figures from the ledger entirely**. `FIGURE`
opens `(?<![\w.$])`, so `gate18%` is not a figure at all — `18%` on the reference deck and
`$468k`, `$140k`, `7,200` and `4%` on `sort-window` had never entered any ledger. All six bind to a
source, so no verdict moved. That is [`L-107`](../docs/lessons/L-107.md).

`python tools/check_all.py`: **25 checkers ran, 1 failed** — `figures.py`, which is
[T-172](T-172-the-shell-sync-falsified-four-published-deck-figures.md) and predates this change.
Every per-deck gate is green.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A deleted inline tag leaves a word boundary, asserted in `self_test` on strings | met | `runs()` on two butting `<span>`s returns one run reading `If it fails Service holds the slot`, and `label_of` over it carries `fails` and `service` as separate words |
| Every ledger this repository can build is compared before and after; every change is a glued word coming apart, and none is a figure lost or a verdict moved | met, and it under-described the result | Four decks, both artefacts. **0 rows lost, 0 verdicts moved.** Every changed row is a glued word coming apart. **Six rows were gained**, which the criterion had no bucket for — the finding, not a failure |
| `FIGURE`'s unit branch carries the `(?![-\w])` guard, with `4 stopover` asserted | met | `FIGURE.search("4 stopover services")` returns nothing. The guard T-169 narrowed under protest is restored, and the comment recording why it was narrow is replaced by why it is wide |
| No shipped deck moves | met | No deck file was edited — `git status` clean of `examples/`. Read the stricter way (**L-106**: *no row moves*, not *no gate moves*): 0 rows lost on either shipped deck, and `check.py` exits identically on all four |

**Child fix tasks raised**
- none

## 4. Review

| Acceptance criterion | Result | Note |
## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-16 | → done | Specified, planned, implemented and reviewed in one unattended pass. **All four criteria met, and the second was under-written**: nothing was lost and **six figures were recovered**, because the gluing was also hiding figures from `FIGURE`'s opening lookbehind. `L-107` is the part that outlives this — a corruption defect is usually an omission defect too, and a criterion with only *unchanged* and *damaged* in it cannot see the difference. **§7 step 3 is not owed**: this task produced nothing that renders, which is the property it was selected into the unattended batch for. |
| 2026-08-16 | → proposed | Raised out of [T-169](T-169-the-figure-binder-cannot-bind-a-value-split-across-table-cells.md)'s implementation, which hit it as a regression and narrowed its own guard rather than widen its scope. |
