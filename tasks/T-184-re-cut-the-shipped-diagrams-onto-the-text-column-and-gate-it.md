---
id: T-184
title: Re-cut the shipped diagrams onto the text column, and turn the measurement into a gate
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-117, T-115, T-182]
work_package: PH3
owner: the project owner
business_value: medium
effort: l
created: 2026-08-18
updated: 2026-08-22
shipped_in: 0.5.0
deliverables:
  - examples/reference-deck.html
  - examples/sort-window/sort-window.html
  - examples/measure-first/measure-first.html
  - tools/deck/figgrid.py
  - tools/deck/check.py
  - docs/DESIGN-SYSTEM.md
---

# T-184 — Re-cut the shipped diagrams onto the text column, and turn the measurement into a gate

## 1. Specify

**Outcome**
Every diagram in every deck this repository ships starts its ink on the same column as the slide's
text, and the measurement that says so is a gated rule rather than a tool somebody has to remember
to run.

**The finding this starts from**
[T-117](T-117-the-decision-diamond-has-no-label-slot-and-diagrams-sit-off-the-text-grid.md) landed
the rule for what a build writes from now on, and the measurement that decides it —
`python tools/deck/figgrid.py <deck>`. Its first run, 2026-08-18:

| Deck | Diagrams | Off the column by more than 4 du |
| :--- | :---: | :---: |
| `examples/reference-deck.html` | 8 | 7 |
| `examples/sort-window/sort-window.html` | 6 | 6 |
| `examples/measure-first/measure-first.html` | 7 | 5 |
| **total** | **21** | **18** |

Offsets run from +22.7 to +217.9 design units. **The `<svg>` element is not the problem** — it sits
at 96 du on every slide of every deck, exactly where the headline and the bottom line sit. Each
diagram declares its own viewBox, the element is scaled to the 1726 du content column, and the
drawing starts wherever the author left it inside that box.

**Why this was split off rather than done in T-117.** Shifting every `x` in a viewBox is mechanical,
but a re-cut diagram is then owed a look (`CLAUDE.md` rule 6), and 18 looks is the cost — not the
arithmetic. T-117 was `m` and this is not. The split is [T-054](T-054-record-which-clauses-of-a-rule-the-gate-decides.md)'s
precedent: make the hole visible and countable first, close it as its own work.

**Scope**
- In: re-cutting the 18 diagrams so their ink starts on the text column, deck by deck, each one
  looked at offline after the change.
- In: promoting `figgrid.py` from a reporting tool to a gated rule — a `DS-nnn` row, a verdict
  reached by `check.py`, and its entry moving out of `check_all.py`'s `NOT_RUN` table.
- In: the two slides that already measure +1.3 and +2.2 du. They are inside the tolerance and are
  the accident rather than the rule; leaving them is correct, and saying so is part of the record.
- In: `measure-first` slide 8's decision node, the second of the two T-117 found. T-117 re-cut
  slide 2 as its demonstration and left this one, and it is the same surgery.
- Out: changing what a diagram *says*. This is placement, not redrawing.
- Out: the tolerance. 4 du is `figgrid.py`'s and it is not this task's to move; if it turns out to
  be wrong, that is a finding with a measurement behind it, not an adjustment.

**Inputs**
- [`tools/deck/figgrid.py`](../tools/deck/figgrid.py) — the measurement, and the tolerance.
- [`skills/htmldeck/references/build.md`](../skills/htmldeck/references/build.md) §2 — the rule as a
  build must now follow it.
- [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) §3.6 — `.decision` and its parts.
- [T-117](T-117-the-decision-diamond-has-no-label-slot-and-diagrams-sit-off-the-text-grid.md) §3 —
  the worked re-cut of one node, with the arithmetic that sized it.

**Acceptance criteria**
- [ ] `python tools/deck/figgrid.py` reports 0 diagrams off the column across all three decks
- [ ] Every re-cut diagram has been opened and looked at offline; the record says which and at what
      length
- [ ] The rule is gated — a `DS-nnn` row, decided by `check.py`, with the full gate green
- [ ] `figgrid.py` no longer sits in `check_all.py`'s `NOT_RUN`, and the partition still holds
- [ ] `measure-first` slide 8's decision node carries its label inside itself
- [ ] No diagram's meaning changed; the re-cut is placement only

**Open questions**
- Whether a diagram genuinely wider than the text column spans it or is inset deliberately. T-117's
  §1 answered the principle — a wide diagram spans whole columns rather than ignoring them — and
  the first deck that has one decides the practice.

## 2. Plan

**The offset is two faults, not one, and they need different mechanisms.** Measured 2026-08-19 by
splitting each diagram's offset into the part contributed by the `<svg>`'s aspect letterbox and the
part contributed by the drawing's own inset inside its viewBox:

| Cause | What it is | Where | Fix |
| :--- | :--- | :--- | :--- |
| **Letterbox** | `.fig` is `width:100%;height:100%`, so a viewBox taller in proportion than its wrap is fitted by height, and the default `preserveAspectRatio` (`xMidYMid`) then **centres** it — the drawing starts inset by half the slack with no author involved | 9 diagrams, 1.3 to 140.2 du | `preserveAspectRatio="xMinYMid meet"` on every `.fig` — the designed mechanism for this, scale and vertical centring unchanged |
| **Ink inset** | The drawing genuinely starts right of its own viewBox origin — an author's left margin | 12 diagrams, 2.2 to 121.0 du | Shift the viewBox `min-x` by the inset, converted to user units through the svg's own CTM |

Six diagrams carry both. Two carry neither beyond the tolerance (`measure-first` slides 2 and 5, at
+2.2 and +1.3), and those are the two §1 says to leave.

**Why not one mechanism for both.** Encoding the letterbox into `min-x` works — it was measured
doing so — but it pushes ink outside the viewBox rectangle and leaves a `min-x` that means *half the
aspect slack on this slide's wrap* rather than *where the drawing starts*. The next diagram edited
on that slide inherits a number nothing explains. `xMinYMid` says what is meant, and the shift then
carries only the author's own margin.

**Steps**
1. Measure the split per diagram, in real Chrome through `render.py` — the same reading `figgrid.py`
   gates on, so the fix is computed in the units the gate decides.
2. Write `preserveAspectRatio="xMinYMid meet"` on every `.fig` in all three decks, uniformly rather
   than only where a letterbox is measured today: the wrap height is a layout outcome, so a diagram
   with no slack now grows one when the slide above it changes.
3. Shift `min-x` on the diagrams whose ink is still inset.
4. Re-measure with `figgrid.py`; look at every changed slide offline.
5. Promote the measurement: a `DS-nnn` row, a verdict in `check.py`, out of `check_all.py`'s
   `NOT_RUN`.
6. `measure-first` slide 8's decision node takes its label inside itself, per T-117 §3's arithmetic.

**Order.** The decks are hand-authored examples rather than shell output, so this is not a `shell/`
cascade and `sync` is not owed. The gate promotion lands last, after the decks can pass it.

## 3. Implement

**Decisions & assumptions**
- **Two mechanisms, because the offset had two causes** — 2026-08-19, and it is §2's finding rather
  than a preference. `preserveAspectRatio="xMinYMid meet"` kills the letterbox; the `min-x` shift
  kills the author's margin. Encoding both into `min-x` also measures clean and was rejected: it
  pushes ink outside the viewBox rectangle and leaves a number meaning *half this wrapper's aspect
  slack*, which the next author has no way to read.
- **`preserveAspectRatio` is written on every `.fig`, not only where a letterbox is measured** —
  2026-08-19. The wrapper's height is a layout outcome, so a diagram with no slack today grows one
  when the slide above it gains a line. 21 of 21 carry it; 9 needed it on the day.
- **The shift is computed from the rendered page, never from the markup** — 2026-08-19. The offset
  is read in real Chrome and divided by the svg's own CTM scale, so the number written into `min-x`
  is in the viewBox's units and nulls exactly what `figgrid.py` measures.
- **The gate reads `figgrid`; it does not re-implement it** — 2026-08-19. `figgrid.verdicts` is
  DS-236's row and `check.py` gathers it, at the cost of one more Chrome launch per deck. A second
  copy of the probe inside `audit.py` would have saved that launch and is the composition that
  disagreed the first time either half changed (**L-08**, **L-13**).
- **`figgrid.py` stays in `check_all.py`'s `NOT_RUN`, against this task's own acceptance criterion**
  — 2026-08-19. The criterion assumed promotion meant a separate per-deck gate. It does not: a tool
  whose checks run inside another gate is `NOT_RUN` *with the gate named*, which is exactly how
  `refcheck.py` and `findings.py` sit there. Running it a second time on its own would launch Chrome
  again to decide a row already decided. The entry now names `check.py`; the partition holds.
- **The two diagrams inside the tolerance were left** — 2026-08-19, per §1. `measure-first` slide 2
  still reports +2.2 du and slide 5 now reports 0.0, the `preserveAspectRatio` having removed its
  1.3 du of letterbox as a side effect.

**The re-cut, measured before and after**

| Deck | Diagrams | Off before | Letterbox | Ink inset | Off after |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `reference-deck` | 8 | 7 | 4 | 3 | **0** |
| `sort-window` | 6 | 6 | 0 | 6 | **0** |
| `measure-first` | 7 | 5 | 5 | 6 | **0** |
| **total** | **21** | **18** | **9** | **12** | **0** |

Six diagrams carried both causes, which is why the middle columns sum past 18.

**Slide 8's decision node, and its arithmetic.** The rhombus went from half-diagonals 58/58 with
`within the band` sitting 29 units *below* it, to **155/58** with the label inside on two lines. The
label measures 99.0 × 59.7 in viewBox units, so `w/A + h/B = 49.5/155 + 29.8/58 = 0.834` — inside
the bound with margin, per T-117 §3. Width rather than height because the top vertex is where the
incoming connector lands: raising it would have left 11 units for a 21-unit arrowhead. Both terminal
boxes moved outward into the viewBox's slack, which is T-117's own precedent for that move.

**What looking caught, twice, and no gate could.** The first cut sized the connectors to the
rhombus and not to the branch labels: `INSIDE` measured 641.4–714.6 against a connector spanning
641–715, so it filled the gap exactly and touched the box at one end and the diamond at the other.
Both connectors went to 140 units. **Then the gate caught the second one** — `DS-035`, two text runs
at 15.0 design units — and it is a defect T-117 left behind: this deck's slides block steps `.lab`
up to `--fs-small` because `--fs-mono` renders under the floor once a viewBox scales it, and
`.decision-branch` was not in that rule. It only shows on a diagram whose viewBox scales **down**;
slide 2's scales up at 1.0788, which is why T-117's own demonstration passed. Fixed in the deck's
slides block, and the rule is now in `build.md` §2 beside the class. The same edit made slide 2's
`YES` match `DRAFT`, `SHEETS` and `NUMBER` in size — the other half of the defect T-117 fixed for
case.

**Both findings are carried out of the task.** The centred viewBox is **L-120** and the class that matches another only where the two are declared together is **L-121**.

**One figure in T-117's record does not reproduce.** It states slide 2's label as 89.4 × 61.7 user
units; measured from `getBBox` on 2026-08-19 it is 80.5 × 60.7, and the ratio comes out 0.696 rather
than 0.74. Both are comfortably inside the bound, so the conclusion stands and the closed record is
left as it was; the difference is measurement method, not a defect.

**Outputs produced**
- [`examples/reference-deck.html`](../examples/reference-deck.html) — 8 `.fig` re-cut.
- [`examples/sort-window/sort-window.html`](../examples/sort-window/sort-window.html) — 6 re-cut.
- [`examples/measure-first/measure-first.html`](../examples/measure-first/measure-first.html) — 7
  re-cut, slide 8's decision node rebuilt, and the `.lab` step-up extended to `.decision-branch`.
- [`tools/deck/figgrid.py`](../tools/deck/figgrid.py) — `verdicts()`, DS-236's row, and a self-test
  holding it to both absent subjects.
- [`tools/deck/check.py`](../tools/deck/check.py) — gathers it, with its `NOT_STATIC` reason.
- [`tools/deck/audit.py`](../tools/deck/audit.py) — DS-236 in `ABSENCE_IS_A_FAIL`, and the producer
  inside the fixture.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-236, `hard` / `render` / gated.
- [`skills/htmldeck/references/build.md`](../skills/htmldeck/references/build.md) §2 — the branch
  label's sizing rule.
- [`tools/check_all.py`](../tools/check_all.py) — `figgrid.py` reclassified.
- `CLAUDE.md`, [`README.md`](../README.md), [`docs/BRIEF.md`](../docs/BRIEF.md),
  [`docs/EVALUATION.md`](../docs/EVALUATION.md), [`docs/PUBLISHING.md`](../docs/PUBLISHING.md),
  [`skills/htmldeck/references/pipeline.md`](../skills/htmldeck/references/pipeline.md) — every
  stated coverage figure moved with the rule: **84 of 114 → 85 of 115**, 168 rows → 169, 121 hard →
  122, 88 mechanically gated → 89.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :--- | :--- |
| `figgrid.py` reports 0 diagrams off the column across all three decks | **pass** | `0 of 21`, from 18 of 21. Re-run: `python tools/deck/figgrid.py examples/reference-deck.html examples/sort-window/sort-window.html examples/measure-first/measure-first.html` |
| Every re-cut diagram opened and looked at offline; the record says which and at what length | **pass** | All 18, plus `measure-first` slides 2 and 5 whose letterbox the `preserveAspectRatio` removed, and slide 8 three times over as the decision node was fitted. Lengths: `reference-deck` 13 slides, `sort-window` 12, `measure-first` 13. Two defects came out of it and neither had another route in — see §3 |
| The rule is gated — a `DS-nnn` row, decided by `check.py`, with the full gate green | **pass** | DS-236, `hard` / `render` / gated. `check.py` reports it `pass` and the account partitions at 115 = 85 checked + 3 excused in the rules + 27 excused here |
| `figgrid.py` no longer sits in `check_all.py`'s `NOT_RUN`, and the partition still holds | **deviated** | It stays there, and the entry now names the gate that reads it. §3 has the argument: a tool whose checks run inside another gate is what `NOT_RUN` is for, and `refcheck.py` and `findings.py` sit there on the same ground. The partition holds |
| `measure-first` slide 8's decision node carries its label inside itself | **pass** | `.decision` group, half-diagonals 155/58, `w/A + h/B = 0.834` |
| No diagram's meaning changed; the re-cut is placement only | **pass** | Every edit is a `viewBox` `min-x`, a `preserveAspectRatio`, or — on slide 8 alone — the decision node T-117 left, whose two terminal boxes moved outward without changing what they say |

**The open question §1 left** — whether a diagram genuinely wider than the text column spans it or is
inset deliberately — is **still open and still correct to be**. None of the 21 is wider than the
column; every one of them was inset by an accident or a margin, which is why they all resolved to
`min-x` and an alignment keyword. The first deck that has a genuinely wide diagram decides the
practice, exactly as §1 said.

**Child fix tasks raised**
- none. The one defect found beyond the scope — `.decision-branch` not following a deck's `.lab`
  restyle — was one line in the deck and one sentence in `build.md`, which is below the bar for a
  task of its own.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-22 | (shipped) | **`shipped_in` set to `0.5.0`, back-filled.** The field was never written, so this task read as belonging to no release while being closed. **Derived, not assumed**: the commit that set `status: done` is an ancestor of `v0.5.0`, which `git tag --contains` answers. Found while reading the unreleased set for `0.6.0` — eight tasks closed 2026-08-19 all carried an empty field, and a ninth ([T-187](T-187-open-the-motion-vocabulary-into-a-style-guide.md)) closed after the tag and belonged to `0.6.0` instead. |
| 2026-08-18 | → proposed | Split out of [T-117](T-117-the-decision-diamond-has-no-label-slot-and-diagrams-sit-off-the-text-grid.md) on the owner's ruling, once measuring turned *one deck's diagrams* into 18 across three decks. `l` rather than `m` because the arithmetic is mechanical and the looking is not. `PH3` by [`../CLAUDE.md`](../CLAUDE.md)'s rule: the decks render correctly and no adopter is affected, so it does not reopen `PH1`. |
| 2026-08-19 | → done | 18 of 21 diagrams re-cut and the measurement promoted to **DS-236**, decided by `check.py`. The offset was two faults — an aspect letterbox nobody chose and the drawing's own margin — and they took different mechanisms. Slide 8's decision node rebuilt with its label inside. Two defects found by looking that no gate reached, one of them a `.decision-branch` sizing hole left by [T-117](T-117-the-decision-diamond-has-no-label-slot-and-diagrams-sit-off-the-text-grid.md). One acceptance criterion deviated from, with the argument in §4. |
