---
id: T-305
title: Let render.py see an SVG paint change, a scripted hover, and a figure painting over its neighbour
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-299, T-267]
work_package: PH1
shipped_in: unreleased
owner: the project owner
business_value: medium
effort: m
created: 2026-09-13
updated: 2026-09-14
deliverables: [tools/deck/render.py, skills/htmldeck/references/build.md]
---

# T-305 — Let render.py see an SVG paint change, a scripted hover, and a figure painting over its neighbour

## 1. Specify

**Outcome**
`render.py` reports a difference where one was painted, or says plainly what it did not exercise.
Today it reports confidently on three states it never reached:

- `state` compares `STATE_DEEP` (`tools/deck/render.py` `:1280`-`:1281`), which holds `color`,
  `background`, `borderColor`, `transform`, `boxShadow`, `outline` and `filter` and no SVG paint
  property. So a `fill` or `stroke` change reports that nothing measured differs.
- `state --hover` substitutes the `:hover` rule onto an attribute (`tools/deck/render.py`
  `:1262`-`:1274`) and dispatches no event, so an effect a script runs on `mouseenter` never runs.
- `measure` checks a figure only against the stage (`tools/deck/render.py` `:325`, `:350`-`:354`), and
  never against its own track. So a figure painting over the prose beneath it reports zero overflow.

**From the adopter report** [`06`](../docs/adopter-reports/nextep/2026-09-07-measure-reports-no-overflow-while-a-figure-paints-over-the-prose.md), [`08`](../docs/adopter-reports/nextep/2026-09-07-render-state-cannot-see-an-svg-fill-change.md), [`09`](../docs/adopter-reports/nextep/2026-09-07-render-state-hover-fires-css-hover-but-no-mouseenter.md).

**Re-run in triage, 2026-09-13, on this tree.** `state --hover ".ruler-ticks button"` on a copy of the
reference deck printed the record's message for `08`, and the tick's `mouseenter` label write did not
run for `09`. `06` was confirmed from source.

**`09` re-opens a choice, not an oversight.** T-267 chose substitution on purpose and prints
*substituted trigger*. The remedy is a decision recorded here: dispatch pointer events at the
element's centre, or keep substitution and say in the report that script handlers were not exercised.

**Scope**
- In: `fill`, `fillOpacity`, `stroke`, `strokeWidth` and `strokeDasharray` in `STATE_DEEP`
- In: the hover decision above, measured on a deck whose hover effect is scripted
- In: a figure's box compared against its own container, from the geometry `measure` already collects
- Out: anything the records above do not name. The report is a closed one-way hand-over, so a
  question this task cannot answer is settled here rather than asked

**Inputs**
- the three records above, each with its command, its version and its own proposed fix
- [T-299](T-299-triage-the-nextep-adopter-report.md) section 3, where the three were ruled together

**Acceptance criteria**
- [ ] records `06`, `08` and `09` are each closed with the remedy measured, or deferred with the reason
      recorded in this task
- [ ] each fix is proved by seeding the defect and watching it fire, in both directions (**L-125**)
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None. Each record carries its evidence and a proposed fix; the proposal is a hypothesis to measure
  before committing to it.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Measure each record's premise on this tree before designing: `08` and `09` on a fixture with the unchanged tool, whether a dispatched event reaches `:hover`, and `06` seeded into a copy of the reference deck | the before direction, §3 |
| 2 | `08`: the five SVG paint properties read by `shown(deep)` and listed in `STATE_DEEP`, and the failure message names them as SVG paint | `tools/deck/render.py` |
| 3 | `09`: take the decision in §1, then report what the dispatched events changed | `tools/deck/render.py` |
| 4 | `06`: each `svg.fig` compared with its own container, as `measure` overflow rows | `tools/deck/render.py` |
| 5 | Prove each fix in both directions: the fixed tool on the seed, the seed's defect removed, and the fix patched back out of the tool in memory | §3 |
| 6 | Run `measure` over the four tracked decks and read every row the new check reports | §3 |
| 7 | Self-test guards, `build.md`'s `--hover` paragraph, lint, then the full gate | — |

## 3. Implement

**Decisions & assumptions**
- `09` keeps the substitution and adds the events: a dispatched `mouseenter` runs every listener and
  leaves `:hover` unmatched, so each route reaches one half of a hover and a deck's hover can need
  both. Reversible. — 2026-09-14
- The events go to the named element, with its centre as their coordinates, not to the element hit
  at the centre: the centre of a `fill:none` rect hits its `svg`, so a hit-tested target hovers an
  element nobody named, and `--probe` already answers what is on top. Reversible. — 2026-09-14
- What the listeners changed is counted from mutation records taken synchronously. A hover with no
  style change passes when a listener changed the DOM, and one with neither still fails. An effect a
  handler defers to a timer or draws on a canvas is not counted, and the report says so. Reversible.
  — 2026-09-14
- `06` compares each `svg.fig` with its parent box and with its in-flow siblings, because a grid
  track is not an element: where the figure is the grid item, as in the record, only the siblings
  show the overlap. Out-of-flow figures and neighbours are skipped as layered on purpose, and the
  tolerance is 2 du. The rows are `measure`'s report: no gate reads them, because `glitchfree.py`'s
  GF-5 reads its own probe. Reversible. — 2026-09-14
- `08` holds the record's five paint properties in a tuple of their own, so the failure message
  names them as SVG paint. Reversible. — 2026-09-14

Every seeded run used a copy outside the repository. "Patched out" means the fix was removed from the
loaded module and the written probe was confirmed to lack it.

| Record | Case | Tool | Result |
| :--- | :--- | :--- | :--- |
| — | six pointer and mouse events dispatched on a rect with a `:hover` rule and listeners | headless Chrome | all six listeners ran; `matches(':hover')` false; fill `none` |
| `08` | fixture: `:hover` sets `fill` and `fill-opacity` on a rect | unchanged | `nothing measured differs`, exit 1 |
| `08` | same | fixed | `fill: none -> rgb(90, 75, 143)`, `fillOpacity: 1 -> 0.06`, exit 0 |
| `08` | same | paint reads patched out | `nothing measured differs`, exit 1 |
| `08` | fixture: `:hover` sets `fill:none`, which is the rest value | fixed | `nothing measured differs`, naming SVG paint, exit 1 |
| `09` | fixture: the rule above, and a `mouseenter` listener rewriting a paragraph | unchanged | capture shows `resting sentence` |
| `09` | same | fixed | `the listeners changed 1 element(s): p#rail`; capture shows `hovered sentence` |
| `09` | same | dispatch patched out | `0 pointer and mouse event(s)`; capture shows `resting sentence` |
| `09` | fixture: the rule and no listener | fixed | `no listener changed the DOM`, both paint deltas, exit 0 |
| `09` | reference deck, `.ruler-ticks li:nth-child(2) button` | fixed | `p#rulerLabel.ruler-label` changed; capture shows `WHY NOW`; exit 0 |
| `09` | same | dispatch patched out | `nothing measured differs`, exit 1; capture shows `CLAIM`, the label at rest |
| `06` | reference deck copy: slide 2's figure `height:auto` in a `minmax(0,1fr)` track, two paragraphs below | unchanged | `overflow findings: 0`; the shot shows the figure drawn over both paragraphs |
| `06` | same | fixed | 6 rows, `figure paints over its neighbour p.seed-prose`, both paragraphs at each resolution |
| `06` | same | check patched out | `overflow findings: 0` |
| `06` | same prose, figure `height:100%` | fixed | `overflow findings: 0` |
| `06` | the four tracked decks, every slide; their sources hold 31 `svg` tags classed `fig` | fixed | no row from the new check. `measure-first`'s three `body content spills` rows come from the unchanged branch |

**Outputs produced**
- `tools/deck/render.py`: `state --hover` reads SVG paint, dispatches the pointer events and names
  what they changed; `measure` compares each figure with its container; four self-test guards
- `skills/htmldeck/references/build.md`: the `--hover` paragraph
- [L-166](../docs/lessons/L-166.md): a capture proves a state change only where the states look
  different

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| records `06`, `08` and `09` each closed with the remedy measured, or deferred with the reason | **pass** | All three closed. `09`'s choice was measured before it was taken, and the answer is both routes rather than either |
| each fix proved by seeding the defect and watching it fire, in both directions | **pass** | §3's table: each seed fires on the fixed tool, fires on nothing once its fix is patched out, and goes quiet once the seed's own defect is removed. The captures were opened and looked at, which found that the first ruler tick proved nothing ([L-166](../docs/lessons/L-166.md)) |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | **pass** | Lint first, then the full gate on the finished tree, since the diff reaches `tools/deck/` |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-14 | -> done | All three records closed, each proved in both directions. `09` dispatches the events and keeps the substitution, because each reaches one half of a hover. No look is owed: no deck changed, and the captures the tool writes were looked at. |
| 2026-09-14 | -> in_progress | Batch B26 started. Step 1 ran first. |
| 2026-09-14 | -> planned | Seven steps. Step 1 measures before anything is designed. |
| 2026-09-14 | -> specified | §1 was complete as raised, and its one choice is decided in §3. |
| 2026-09-13 | -> proposed | Raised by T-299 from Nextep records `06`, `08` and `09`, which share `render.py`. `PH1`: an adopter met all three in the published `0.7.0`. `06` arrived as a `gap` and is ruled a defect, because `measure` reports zero overflow over a real overlap. |
