---
id: T-117
title: The decision diamond has no label slot, and diagrams sit off the text grid
type: deliverable
status: done
phase: review
parent: null
blocked_by: []
related: [T-016, T-109, T-115]
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-08-13
updated: 2026-08-18
shipped_in: unreleased
deliverables:
  - docs/COMPONENT-CONTRACT.md
  - shell/components.css
  - skills/htmldeck/references/build.md
  - tools/deck/figgrid.py
---

# T-117 — The decision diamond has no label slot, and diagrams sit off the text grid

## 1. Specify

**Outcome**
Two diagram components gain what they are missing: a decision diamond that carries its own label, and
a diagram that shares the slide's text grid. Both are gaps in the contract rather than authoring
mistakes, which is why both recur across a deck built carefully against it.

**The two, seen in the render**

**1. The diamond has nowhere to put its label.** Slides 2 and 8 of the first adopting project's deck
both render an **empty rhombus with its caption floating underneath** — `WITHIN BUDGET`,
`WITHIN THE BAND`. The reader has to bind a free-standing caption to a shape by proximity, and on
slide 8 the caption sits below a diamond whose two exits are already labelled `INSIDE` and `OUTSIDE`,
so three pieces of text compete for one node. The deck's own specification says the diamond is
*"sized from its own label so the outline never crosses the text"* — **which is what the author
wanted and the component cannot do**, so the build put the label outside instead. Two slides, one
missing slot.

*This is also [T-115](T-115-the-specification-can-assert-a-layout-the-shell-cannot-honour.md)'s
pattern with a different ending: there the specification asked for something the shell could not do
and the result still read well, so nothing noticed. Here the same thing happened and the result is
weaker. The two tasks are the same gap seen from opposite sides — one adds the check, this one
closes an instance.*

**2. Diagrams are inset from the text grid.** On slides 4, 6 and 7 the diagram's left edge and the
slide's text left edge disagree — by roughly 190, 220 and 60 units respectively. Every one of those
slides puts a row of text *directly beneath* the diagram, so the misalignment is visible as a step
rather than as a margin.

*Measured 2026-08-18, real Chrome at 1920×1234, offline — and it corrects the sentence above.* The
original reading was that *the diagram is centred in the body rather than placed on the column grid*.
**That is not what happens.** The `<svg>` element's left edge is at 96 du on every slide of every
deck, which is exactly where the headline, the bottom line and the body sit. The grid is already
shared. What is inset is **the ink inside the viewBox**: each diagram declares its own viewBox
(`0 0 1900 430`, `0 0 1800 420`, `0 0 1700 380` on the three slides above), the element is scaled to
the 1726 du column, and the leftmost drawn thing starts wherever the author happened to put it.

| Deck | Slides with a diagram | ink − text, per slide |
| :--- | :---: | :--- |
| `measure-first` | 7 | +2, **+186**, +1, **+218**, **+61**, **+165**, **+76** |
| `reference-deck` | 8 | +49, +113, +55, +120, +23, +50, +106, +0 |
| `sort-window` | 6 | +49, +120, +121, +60, +121, +90 |

**So this is not the adopter's deck being careless — it is every deck this repository ships**, the
hand-built reference deck included, and the two slides that come out at +2 and +1 are the accident
rather than the rule. The fix therefore is not a CSS change to where the `<svg>` sits, which is
already right. It is a rule about **what a viewBox may contain**: the leftmost ink sits at the
viewBox's own left edge, so that scaling the element to the column puts the drawing on the column.
That rule is authoring guidance plus a measurement, and the measurement is cheap — the numbers above
came from one probe.

**Scope**
- In: a **label slot on the decision node**, sized from the label the way the specification already
  assumed, with the branch labels staying on the edges.
- In: a rule that a diagram **shares the slide's column grid**, and what that means when a diagram is
  genuinely wider or narrower than the text.
- In: contract rows for both in [`COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) — DS-229
  requires every component the style block styles to have one, and these are the components that
  will be edited.
- In: [`build.md`](../skills/htmldeck/references/build.md) updated, so a build stops working around
  the gap by moving the label out.
- In: whatever a gate can decide — a diagram whose left edge does not sit on a grid column is
  measurable; whether a diamond *needs* a label is not.
- Out: **rebuilding the adopting project's deck.** Its diagrams are its own; this changes what the
  next one can do.
- Out: a general diagram layout engine. Two named gaps, closed.

**Inputs**
- [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) — the diagram components as they
  stand, and DS-229's completeness half.
- [`shell/components.css`](../shell/components.css) — the grid the slide's text sits on.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — **DS-136**, patterns built once and reused;
  the grid rules the text already obeys.
- [T-016](T-016-the-interaction-and-motion-layer.md) — where the diagram components came from.

**Acceptance criteria**
- [ ] A decision node renders its label inside itself, sized so the outline never crosses the text,
      with branch labels still on the edges.
- [ ] A diagram's **ink** — not its `<svg>` element, which is already aligned — sits on the same
      column as the slide's text, demonstrated on a slide that puts text directly beneath a diagram.
- [ ] Both have contract rows.
- [ ] `build.md` no longer produces the workaround.
- [ ] Demonstrated on a real 12-slide deck with at least two diagrams, opened and looked at, offline.
- [ ] `check.py` green, and the grid clause either gated or excused with a reason.

**Open questions**
- What a diagram wider than the text measure does. Decided during implementation from the grid's own
  reason: the column grid is what makes a slide read as one object, so a wide diagram spans whole
  columns rather than ignoring them.
- **Whether the three shipped decks are re-cut, or only the rule and the gate land.** The measurement
  above turns this from *one deck's diagrams* into 21 diagrams across three decks, one of which §1's
  scope explicitly excludes from rebuilding. Shifting every `x` in a viewBox is mechanical, but each
  re-cut diagram is then owed a look (rule 6), which is the real cost and is not `m`. **The
  recommendation is to land the component, the contract rows, the build rule and the gate, take the
  gate's first run as a recorded finding rather than a failure, and raise the re-cut as its own
  task** — the same split T-054 used for the checks it made visible without building.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Measure the inset on the three slides that show it | the numbers |
| 2 | Add the label slot; re-render the two diamond slides | shell, two renderings |
| 3 | Put diagrams on the column grid | shell |
| 4 | Contract rows for both | contract |
| 5 | Fix `build.md`'s workaround | `build.md` |
| 6 | Build a deck with two diagrams and look at it offline | verdict |

**Re-planned 2026-08-18, after §1's measurement widened the second half.** Steps 1, 2, 4 and 5 stand.
Step 3 changes subject — the `<svg>` is already on the column, so there is no CSS placement to fix —
and step 6 is answered by re-cutting a node in a deck that already has one rather than building a
deck to hold it. **Split on the owner's ruling**: this task lands the component, the contract rows,
the build rule and the measurement; [T-184](T-184-re-cut-the-shipped-diagrams-onto-the-text-column-and-gate-it.md)
re-cuts the 18 diagrams already shipped and promotes the measurement to a gated rule. The
measurement's first run is a **recorded finding, not a failure** — which is why `figgrid.py` reports
and does not gate.

## 3. Implement

**Decisions & assumptions**
- **The decision node is a `<g>`, not a path plus a nearby text** — 2026-08-18. `.decision` holds
  `.decision-shape` and `.decision-label`, so the label is inside the group whose centre it is
  placed on and the two cannot drift apart again.
- **The rhombus is sized by the build, not by CSS** — 2026-08-18. SVG cannot grow a path to fit
  text, so `build.md` carries the arithmetic and the contract carries the shape.
- **`.decision-branch` is a `.lab` in every respect** — 2026-08-18, *including its uppercase*, and
  that was found by looking rather than by any gate. See below.
- **The measurement reports and does not gate** — 2026-08-18, per the owner's split. Gating it now
  would be red on three correct-looking decks from the moment it landed.
- **A speculative `.is-accent` rule was written and then removed** — 2026-08-18. DS-229 failed it
  as an uncontracted class, correctly: nothing used it, and a rule matching nothing looks exactly
  like a rule that passed. Removed rather than given a row.

**Outputs produced**
- [`shell/components.css`](../shell/components.css) — `.decision-shape`, `.decision-label`,
  `.decision-branch`.
- [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) §3.6 — four rows and the note.
- [`skills/htmldeck/references/build.md`](../skills/htmldeck/references/build.md) §2 — both rules,
  with the fitting arithmetic.
- [`tools/deck/figgrid.py`](../tools/deck/figgrid.py) — the grid measurement, classified in
  `check_all.py` as a measurement with what it is instead of a checker.
- [`examples/measure-first/measure-first.html`](../examples/measure-first/measure-first.html) —
  slide 2's decision node re-cut as the demonstration.
- [T-184](T-184-re-cut-the-shipped-diagrams-onto-the-text-column-and-gate-it.md) — the re-cut and
  the promotion to a gate.

**The demonstration, and its arithmetic.** Slide 2's node moved centre 1200 → 1225 (the midpoint of
the gap, so the two connectors match instead of being 34 and 82) and half-diagonals 74/74 → 106/96.
The label measures 89.4 × 61.7 in viewBox units, and an axis-aligned block of half-width `w` and
half-height `h` fits half-diagonals `A`, `B` when `w/A + h/B ≤ 1`: here **44.7/106 + 30.8/96 =
0.74**, so the outline clears the text with room rather than landing on the bound. The terminal box
moved right by 40 into the viewBox's own slack. The deck's markup carried a comment reading *"the
label sits above the diamond, never inside it"* — the workaround in the build's own words — and it
went with the gap it described.

**What looking caught that nothing else could.** The first cut rendered the branch label `yes` in
**lower case** beside `DRAFT`, `SHEETS` and `NUMBER`. `.lab` carries `text-transform:uppercase` and
the new class did not. Every gate passed: no check here reads a text transform, and the class was
contracted, styled and used. It is the second finding in two tasks that only a render produced, and
it is `CLAUDE.md` rule 6 earning its place.

**The measurement's first run — the recorded finding.**

| Deck | Diagrams | Off the column by more than 4 du |
| :--- | :---: | :---: |
| `reference-deck` | 8 | 7 |
| `sort-window` | 6 | 6 |
| `measure-first` | 7 | 5 |
| **total** | **21** | **18** |

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :--- | :--- |
| A decision node renders its label inside itself, sized so the outline never crosses the text, with branch labels still on the edges | met | `.decision` on `measure-first` slide 2, looked at offline in real Chrome. `w/A + h/B = 0.74`, and `YES` sits on the outgoing edge |
| A diagram's **ink** sits on the same column as the slide's text, demonstrated on a slide that puts text directly beneath a diagram | **not met here, by design** | The *rule* and the *measurement* landed; the shipped diagrams do not pass yet — 18 of 21. Split to [T-184](T-184-re-cut-the-shipped-diagrams-onto-the-text-column-and-gate-it.md) on the owner's ruling, with the first run recorded as a finding rather than a failure. §1's second open question is what made this the right split |
| Both have contract rows | met | Four rows in §3.6 for the decision node. The grid rule is authoring guidance plus a measurement, so it has no component to contract — it is `build.md` §2 and `figgrid.py` |
| `build.md` no longer produces the workaround | met | §2 carries both rules, and forbids the caption-underneath explicitly. The deck's own comment recording the workaround is gone with it |
| Demonstrated on a real 12-slide deck with at least two diagrams, opened and looked at, offline | met | `measure-first`, 13 slides and 7 diagrams. Slide 2 rendered in real Chrome offline, twice — the second time because the first look found the lowercase branch label |
| `check.py` green, and the grid clause either gated or excused with a reason | met | `0 failure(s)` on all three decks; DS-229 caught a speculative uncontracted class on the way and it was removed. The grid clause is **not gated, with the reason recorded** in `check_all.py`'s own table, where a partition entry must say what a tool is instead of a checker |

**Child fix tasks raised**
- [T-184](T-184-re-cut-the-shipped-diagrams-onto-the-text-column-and-gate-it.md) — re-cut the 18
  diagrams and promote the measurement to a gated rule. `l`, because the arithmetic is mechanical
  and the 18 looks are not.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-13 | → proposed | Both found by looking at the rendered deck, neither reported. Opened as one task because both are contract gaps in the same layer and both were worked around silently by a careful build — the diamond's label moved outside, the diagram centred instead of placed. A gap a good build routes around is a gap that never gets reported. |
| 2026-08-18 | proposed → specified | Both halves re-derived by measurement rather than read off the render. The diamond half stands exactly as written: slides 2 and 8 draw a bare `<path>` rhombus — `M1200 138 L1274 212 L1200 286 L1126 212 Z` and `M870 223 L928 281 L870 339 L812 281 Z` — with the label a separate `<text>` at the shape's centre x and below it, and on slide 8 the branch labels `inside` and `outside` beside it, so three texts do compete for one node. **The grid half is corrected**: the `<svg>` is at 96 du on every slide of every deck and is already on the column, so nothing is centred in the body; what is inset is the ink inside the viewBox. It is also not the adopter's deck alone — all three shipped decks show it, the reference deck by +23 to +120. That changes the fix from a CSS placement to a rule about viewBox content, and it raises a scoping question §1 could not have known to ask, now recorded as the second open question. |
| 2026-08-18 | specified → planned | Re-planned rather than followed: §1's measurement removed step 3's subject (the `<svg>` is already on the column) and turned step 6 into re-cutting a node in a deck that has one. **Split on the owner's ruling** — component, contract, build rule and measurement here; the 18 re-cuts and the gate in [T-184](T-184-re-cut-the-shipped-diagrams-onto-the-text-column-and-gate-it.md). |
| 2026-08-18 | planned → in_progress → done | `.decision` landed with its label inside, demonstrated on `measure-first` slide 2 — sized `w/A + h/B = 0.74` so the outline clears the text, with the terminal box moved into the viewBox's own slack. **Looking is what earned its keep**: the first cut rendered `yes` in lower case beside three uppercase siblings, and no gate here reads a text transform. DS-229 separately caught a speculative `.is-accent` rule and it was removed rather than contracted. The grid half is a rule plus a measurement — 18 of 21 diagrams off the column, recorded as a finding — and the second criterion is **not met by design**, which is what the split books. |
