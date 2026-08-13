---
id: T-036
title: Continue the contents page onto a second sheet for decks past the measured bound
type: deliverable
status: done
phase: review
shipped_in: unreleased
parent: T-034
blocked_by: []
related: [T-034, T-005, T-116]
work_package: PH2
owner: maintainer
business_value: high
effort: m
created: 2026-08-08
updated: 2026-08-13
deliverables:
  - shell/deck.js
  - shell/components.css
  - tools/deck/contents_bound.py
  - tools/deck/printpages.py
  - docs/DESIGN-SYSTEM.md
  - examples/reference-deck.html
---

# T-036 — Continue the contents page onto a second sheet for decks past the measured bound

## 1. Specify

**Outcome**
The printed contents page continues onto a **second sheet** when one sheet can no longer carry every
slide, so a long deck's contents page degrades by growing rather than by dropping entries. Decks at
or under the bound are unaffected and still print exactly one contents page.

**Why this exists rather than being folded into [T-034](T-034-a-contents-page-for-the-printed-deck.md)**
T-034 measured where its single page stops working, and the numbers put the problem outside the
target case rather than inside it — **the bound is 16 slides and the hard limit is 24, against a
target deck of 12**. Building a second page there and then would have been building for a deck size
nothing in this project currently produces. It is raised instead of dropped because the gap is real
and stated in the ruleset: **DS-226** requires that a compressing page *never drops an entry*, and
past 24 slides compression physically cannot honour that — at 25 slides a box has **89 du of height
for 96 du of number, title and padding**. A deck that long is therefore non-conformant today, and a
rule with a known unimplementable range needs either the implementation or an amendment.

**The two numbers this task inherits, both measured 2026-08-08** — see
[T-034](T-034-a-contents-page-for-the-printed-deck.md) §1 *The bound*, which is the home of the
measurement and is not restated here:

- **16 slides** — the largest deck where the page does its whole job, description included.
- **24 slides** — the largest deck where number and title still render at all.

**One sheet is not enough either, and the task title understates it**
The title says *second sheet* because 24 was the number in front of it when it was raised. The
target moved on 2026-08-13: [`../CLAUDE.md`](../CLAUDE.md) *Verifying* records a peer presenting
**43 slides** and the next deck from the same sources being longer again. Two sheets of 16 carry 32,
so at 43 a two-sheet rule drops eleven entries and fails this task's first acceptance criterion.
**The rule is therefore stated for `k` sheets** — one sheet per 16 entries — and *second sheet* is
the first case of it rather than the whole of it. Nothing else in the specification changes: 16 is
still the trigger, the stage boundary is still where the split falls.

**Scope**
- In: the continuation rule — when a sheet is added, and how the boxes divide across sheets.
- In: the consequence for the printed page count, which stops being `n` + 1.
- In: **the grid every sheet uses.** The sheets are one contents page continued, so they cannot
  each pick their own column and row count from their own entry count — two sheets printing boxes
  of different heights read as a rendering fault rather than as a continuation. This is a rule
  about how the boxes divide across sheets, which is the first scope line, and not a change to
  the single-page layout below.
- Out: changing the single-page layout itself. That is T-034's and it is measured and settled.
- Out: an on-screen equivalent. The overlay index scrolls, so it has no equivalent problem.

**Inputs**
- [`T-034`](T-034-a-contents-page-for-the-printed-deck.md) §1 — the geometry, the conversion, the
  compression rule, and the measured bound.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §5.4 — DS-225 and DS-226.

**Acceptance criteria**
- [ ] A deck past the bound prints a contents page that carries **every** slide, with no entry
      dropped and no title clipped — verified at **43 slides**, the longest length anyone has
      reported presenting, as well as just past the bound
- [ ] A deck at or under the bound prints **exactly one** contents page, unchanged from T-034
- [ ] **The split falls at a stage boundary** wherever the argument offers one, and where a single
      stage is itself longer than a sheet the entry survives and the boundary is what yields
- [ ] **Every sheet prints the same grid** — same columns, same rows, same box height — so the
      sheets read as one page continued
- [ ] **Each sheet says which of how many it is**, on the sheet, so a reader holding sheet one
      knows the map is not finished
- [ ] The page count rule is restated wherever it is asserted — `DESIGN-SYSTEM.md` §5.4,
      [T-005](T-005-build-check-the-gate-the-deck-must-pass.md)'s print row and
      `printpages.py` all currently say `n` + 1
- [ ] Measured on a deck built past the hard limit, not asserted
- [ ] Printed from a double-clicked file and **looked at** (**L-01**, **L-35**)

**Open questions**
- ~~**Where does the split fall — by count, or by stage?**~~ **Answered 2026-08-09: at a stage
  boundary.** The contents page exists to show the argument's structure, so a split that cuts a
  stage in half renders the argument as a paging artifact — the reader meets *where am I* at the
  sheet break, which is the failure the ruler was built to prevent. Filling sheet one and spilling
  the remainder is simpler to build and was rejected on that: the printed sheet **is** the
  deliverable here, not an export of it.
- ~~**Is the trigger the bound (16) or the hard limit (24)?**~~ **Answered 2026-08-09: 16, the
  measured bound.** `contents_bound.py` measured **16 entries with descriptions against 24
  without**, and the description is what makes a contents page more than a list of titles.
  Splitting at 24 keeps the page count down and accepts a description-free map anywhere between 17
  and 24 — a quality cliff nobody chose per deck and nothing would report.

*Both answered while [T-052](T-052-two-hard-judge-failures-in-the-reference-deck.md) was closing
out the audit run, so the task is fully specified whenever it is picked up. **It stays parked**: it
only bites past 24 slides and the target is 12.*

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | The **sheet rule** in `deck.js` — group the manifest into runs of one stage, split a run longer than a sheet, then pack the runs into the fewest sheets with the largest one as small as possible. Exported beside `contentsLayout` for the same reason that one is | `contentsSheets()`, and the export |
| 2 | Render **one `<section class="contents">` per sheet**, every sheet on one grid taken from the largest, each carrying its *n of k* marker and the screen-only line | `buildContents()` |
| 3 | Pin the grid rows so the sheets cannot disagree about box height, and set the marker | `shell/components.css` |
| 4 | Teach `contents_bound.py` the new invariant: the shipped split never hands a sheet more than the bound, so the dense band and the hard limit are unreachable through it | the tool, and the assertion |
| 5 | `printpages.py` expects `n` + sheets, with the sheet count **read from the deck's DOM** rather than recomputed here (T-120, **L-08**) | the gate |
| 6 | Measure on scratch decks at 17, 25 and **43** slides — past the bound, past the hard limit, and at the longest length anyone has reported | the numbers |
| 7 | Amend `DESIGN-SYSTEM.md` §5.4 and DS-225 · DS-226, and [T-005](T-005-build-check-the-gate-the-deck-must-pass.md)'s print row | ruleset, gate |
| 8 | Propagate the shell into the three tracked decks byte for byte | `shell.py check` green |
| 9 | Run the release gate, then **print from a double-click and look at every sheet** (**L-01**, **L-35**, **L-76**) | green gates, and the §4 verdicts |

**Approach decisions**

- **The sheets are balanced, not filled and spilled.** Fill-and-spill is simpler and was rejected on
  the render: 17 slides would print 16 boxes on sheet one and **a single box on sheet two**, which
  is the stretched-empty-box fault T-034 already paid to fix at the short end. Balancing makes it
  9 and 8.
- **The split point is chosen by minimising the largest sheet, over stage boundaries only.** Binary
  search the per-sheet capacity down from 16 and pack greedily at each candidate — deterministic,
  exact for that objective, and about fifteen lines. A scoring heuristic over candidate cuts would
  be longer and would need defending every time it surprised someone.
- **A stage longer than one sheet is split by count**, and this is the one place the answered
  question yields. DS-226 says an entry is never dropped; the stage boundary is a preference about
  where the cut reads well. Where the two collide the invariant wins, and the record says so rather
  than the code doing it quietly.
- **`contentsLayout` is untouched, dense band and all.** It is the layout of **one sheet**, and step
  1 makes its dense band and its hard limit unreachable — but unreachable by the cap, not gone. The
  tool keeps measuring the full range, because that is what says what happens if the cap ever moves,
  and gains an assertion that the shipped rule stays inside it. Deleting the branch would leave the
  ruleset's two numbers with no instrument.
- **Step 9 is last for the reason it was last in T-034, and T-116 raised the price.** The one fault
  this page has shipped twice lives only in paged layout, and no screen measurement in step 6
  reaches it (**L-76**).

## 3. Implement

**Decisions & assumptions**

- **`ceil(n / 16)` is a floor on the sheet count, not the answer, and the 43-slide case is where
  that showed.** The plan's self-test expected three sheets at 43 entries and the rule returned
  four. It was right and the expectation was wrong: seven even stages of 43 entries are runs of
  7 · 6 · 6 · 6 · 6 · 6 · 6, and no three contiguous groups of those come in at or under 16 — the
  closest is 13 · 12 · 18. The answered question says the boundary is preferred to the paging, so
  the fourth sheet is the specification working rather than an inefficiency. The number is now
  written into the tool's cases with the arithmetic beside it, because *the obvious formula is
  wrong here* is exactly the sentence the next reader needs. — 2026-08-13
- **The footnote repeats on every sheet, and the second reason is mechanical.** The first is that
  paper gets separated, so a sheet read alone still owes the reader R7 §5's statement. The second
  decides it: the line occupies height, so a sheet without it hands its grid more room and prints
  taller boxes than its neighbours — the exact thing the shared grid exists to prevent. — 2026-08-13
- **The *n of k* marker goes on sheet one too, which is the sheet that needs it.** A reader holding
  the last sheet can tell it is the last; a reader holding the first has no other signal that the map
  is unfinished. It costs nothing: the eyebrow is already there and already says `Contents`.
  — 2026-08-13
- **`printpages.py` gained a second Chrome launch rather than a copy of the split rule.** It needs
  `k` to know what to expect, and computing `k` in Python would be a second implementation of a rule
  the deck already ships — which is [T-120](T-120-printpages-standalone-defaults-the-slide-count-to-a-hardcoded-twelve.md)'s
  defect with a different constant. It counts `section.contents` in the deck's own DOM instead. The
  check keeps its teeth: the DOM count and the PDF page count are two different measurements, so a
  print stylesheet that failed to render the sheets still fails the gate. — 2026-08-13
- **A finding that is not a defect, raised as [T-125](T-125-a-split-contents-page-still-clamps-its-descriptions-to-one-line.md).**
  Printed at 25 entries the page splits 12 / 13, the 13 puts both sheets in the four-row band, and
  that band clamps every description to **one line**; at 17 entries, one band down, both sheets print
  three full lines. So a longer deck gets a better map than a shorter one. The fix would be a second
  capacity — sheets of at most 12 once splitting — and the argument for it is this task's own
  answered question, one band deeper. It is raised rather than taken because 16 is the number the
  owner answered, T-116 re-measured and this task was instructed to build against (**L-37**), and
  because nothing shipped is wrong: `examples/reference-deck.html` has printed one-line descriptions
  since its colophon took it to 13. — 2026-08-13

**What the numbers came out as**

Printed through real Chrome, then read out of the PDF's own rectangles — the instrument T-116 had to
build by hand, because the fault class this page has shipped twice lives only in paged layout
(**L-76**). Every row is clean: no card overlaps another, and none reaches the footnote.

| deck | sheets | entries per sheet | row gaps, pt | last card / footnote, pt |
| ---: | ---: | :--- | :--- | :--- |
| 13, the reference deck | 1 | 13 | +19.5 +20.2 +19.5 | 712.1 / 735.7 |
| 17 | 2 | 8 · 9 | +20.2 +20.2 | 712.1 / 735.7 |
| 25 | 2 | 12 · 13 | +19.5 +20.2 +19.5 | 712.1 / 735.7 |
| 43 | 4 | 12 · 12 · 12 · 7 | +20.2 +20.2 | 712.1 / 735.7 |

The long decks are scratch inputs built by cloning the reference deck's slides and rewriting
`data-stage`, exactly as T-034 measured its bound — a deck deliberately too long is a measurement,
not a repository artefact.

**Outputs produced**
- [`shell/deck.js`](../shell/deck.js) — `stageRuns`, `splitLongRuns`, `sheetsNeeded`,
  `contentsSheets`, the second export, and `buildContents` split into a per-sheet renderer
- [`shell/components.css`](../shell/components.css) — the declared row count, so sheets cannot
  disagree about box height
- [`tools/deck/contents_bound.py`](../tools/deck/contents_bound.py) — eight stage shapes through the
  shipped split rule, three invariants asserted over each, and the split printed as a table
- [`tools/deck/printpages.py`](../tools/deck/printpages.py) — `n` + `k`, with `k` read from the DOM
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — §5.4 amended, DS-226 restated
- [`tools/deck/check.py`](../tools/deck/check.py) — the two `not asserted here` reasons
- [T-005](T-005-build-check-the-gate-the-deck-must-pass.md) — the print row says `n` + `k`
- The three tracked decks, carrying the shell byte for byte (`shell.py check`):
  [`examples/reference-deck.html`](../examples/reference-deck.html),
  [`examples/sort-window/sort-window.html`](../examples/sort-window/sort-window.html) and
  [`examples/reference-deck-seeded-defects.html`](../examples/reference-deck-seeded-defects.html)

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every slide carried, no entry dropped and no title clipped, at **43 slides** and just past the bound | **met** | Printed: 43 entries over four sheets (12 · 12 · 12 · 7), 17 over two (8 · 9), 25 over two (12 · 13). Page counts `47 = 43 + 4`, `19 = 17 + 2`, `27 = 25 + 2`, each read out of the PDF two ways and required to agree. Nothing is clipped, because nothing reaches the compression band any more: the cap holds every sheet at or under 16, and the tool fails the run if one comes back over |
| A deck at or under the bound prints **exactly one** contents page, unchanged from T-034 | **met** | `examples/reference-deck.html`, 13 entries, one sheet, 14 pages. The printed geometry is the one T-116 recorded — last card 712.1 pt, footnote 735.7–751.5, all row gaps positive — and the eyebrow reads `CONTENTS` with no marker, because the marker only exists above one sheet |
| The split falls at a **stage boundary**, and where one stage is longer than a sheet the entry survives and the boundary yields | **met** | Eight stage shapes through the shipped rule, asserted in `contents_bound.py`: every sheet carries whole stage runs where the shape allows one. The two shapes with no boundary at all — 20 entries in one stage, 43 entries in a stage of 40 — split by count into even pieces, and the invariant that catches a mistake there is the one DS-226 states: the flattened sheets must equal the manifest, every entry once and in order |
| **Every sheet prints the same grid** | **met** | `--crows` is the largest sheet's row count and every sheet takes it. Measured on paper rather than in the stylesheet: at 43 slides the fourth sheet's seven cards sit at the same 202 pt row pitch as the twelve on sheets one to three, and the page simply ends a row early. Before the declared row count that sheet would have divided the page into two taller rows |
| **Each sheet says which of how many it is** | **met** | `CONTENTS · 1 OF 2` through `4 OF 4`, in the eyebrow, on every sheet including the first — which is the sheet that needs it |
| The page count rule is restated wherever it is asserted | **met** | `DESIGN-SYSTEM.md` §5.4 (a dated amendment, `n` + `k`), DS-226, [T-005](T-005-build-check-the-gate-the-deck-must-pass.md)'s print row, and `printpages.py` in both its docstring and its arithmetic. `check.py`'s two *not asserted here* reasons carried the old number too and were corrected with them |
| Measured on a deck built past the hard limit, not asserted | **met** | 25 and 43, both past the old hard limit of 24, both built as scratch decks from cloned slides with `data-stage` rewritten to the shape being tested. The hard limit is now unreachable through the shipped rule, which is what made 25 measurable rather than broken |
| Printed from a **double-clicked** file and looked at (**L-01**, **L-35**) | **partly** | Four decks printed through real Chrome's own print path, offline, and **looked at as pages** — the four sheets above are in this session, and the card rectangles were read out of the PDFs rather than off the screen, which is the only instrument that sees this page's fault class (**L-76**). What is not discharged is the literal criterion: nobody double-clicked the file and used the print dialog. That is the owner's, it is cheap, and the exposure is small — the shipped decks' printed geometry is measured identical to what T-116 shipped, so the change that is unwitnessed by a dialog print is confined to the scratch decks |
| *(added)* No sheet reaches the compression bands the ruleset stated as unimplementable | **met** | The reason DS-226 needed this task: past 24 entries a box had 89 du of height for 96 du of content and no compression resolved it. With the cap in force the largest sheet any of the eight shapes produces is 16, and `contents_bound.py` fails the run on a sheet over the bound — so the range the rule could not honour is now unreachable rather than merely undocumented |

**Child fix tasks raised**
- [T-125](T-125-a-split-contents-page-still-clamps-its-descriptions-to-one-line.md) — a split page's
  sheets are capped at 16, so a 25-entry deck lands in the four-row band and clamps every description
  to one line where a 17-entry deck prints three. Raised rather than taken: the number it would move
  is the one the owner answered and this task was told to build against.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-13 | → done | **Eight criteria met, one partly, and one added.** The page continues onto as many sheets as the argument needs — 43 slides print four, 25 print two, 17 print two, and the reference deck at 13 prints the one sheet it always did with its geometry measured identical to what T-116 shipped. The partly is the literal print-and-look: four decks were printed through real Chrome's print path and read out of the PDFs' own rectangles, but nobody double-clicked a file and used the dialog, and that stays the owner's (**L-35**). The added criterion is the one this task existed for — DS-226's unimplementable range past 24 entries is now unreachable rather than merely documented. **Two findings are recorded elsewhere rather than only here.** [T-125](T-125-a-split-contents-page-still-clamps-its-descriptions-to-one-line.md) carries the one thing deliberately not fixed: a 25-entry deck's sheets land in the four-row band and clamp every description to one line, where a 17-entry deck prints three, so the shorter deck gets the better map. Raised rather than taken, because the capacity it would move is the number the owner answered and this task was told to build against (**L-37**). And **L-77** is the mistake this session made and the gate caught: `reference-deck-seeded-defects.html` is generated by `seed_defects.py`, propagating the shell into it by hand deleted its eleven seeded lines, and `shell.py check` then reported the file clean because by its own measure it was. |
| 2026-08-13 | → in_progress | **The plan's arithmetic was wrong before the code was.** The self-test expected three sheets at 43 slides — `ceil(43 / 16)` — and the rule returned four. Seven even stages give runs of 7 · 6 · 6 · 6 · 6 · 6 · 6 and no three contiguous groups of those fit in 16, so `ceil(n / 16)` is a floor and the fourth sheet is the answered question working: the boundary is preferred to the paging. Recorded in the tool beside the case rather than quietly corrected. Two edits went past the literal plan and both are in §3 — the footnote repeats on every sheet because it takes height and a sheet without it would print taller boxes, and `printpages.py` took a second Chrome launch rather than a Python copy of the split rule. |
| 2026-08-13 | → planned | Nine steps, and three of the five approach decisions were taken against a simpler alternative rather than in a vacuum. **Balanced sheets over fill-and-spill**, because 17 slides filled and spilled is 16 boxes then one, and a lone box on a sheet is the fault T-034 already fixed at the short end. **The largest sheet minimised by binary search over stage boundaries**, because it is exact and short where a scoring heuristic is neither. **`contentsLayout` left alone**, dense band and hard limit included: the cap makes them unreachable rather than wrong, and deleting them would leave DS-226's two numbers with no instrument. |
| 2026-08-13 | → specified | **Both open questions were already answered, so specifying was reading the task against a target that had moved under it.** One thing changed and one was added. The title says *second sheet* because 24 was the number in front of it in August; `../CLAUDE.md` *Verifying* now records a presented deck of **43 slides**, and two sheets of 16 carry 32 — so a two-sheet rule fails this task's own first criterion by eleven entries. The rule is stated for **`k` sheets** instead, which changes no answered question: 16 is still the trigger and the stage boundary is still the cut. Added to scope: **the grid every sheet uses**, because sheets that each size themselves from their own entry count print boxes of different heights, and two sheets of one page that disagree about box height read as a rendering fault. Four criteria added — the stage boundary, the shared grid, the sheet-of-sheets marker, and 43 slides as a measured length rather than 25. |
| 2026-08-13 | (no change) | **Split, not absorbed.** The owner asked for this task in `0.2.3`. It is a **capability** — a second sheet for decks past the bound — and what `0.2.3` needs is the **defect** below the bound, so that went to [T-116](T-116-the-printed-contents-page-collides-at-thirteen-entries.md) as `PH1`/`critical` and this stays `PH2`. T-116 also takes the bound re-measurement, since fixing the track sizing moves it; **this task reads the new number rather than the old one.** Not `blocked_by` — §1's questions were answered from a run made while the tool worked — but do not build the second sheet against 16 / 24. |
| 2026-08-13 | (no change) | **T-116 closed and the bound did not move: 16 / 24 stands, and the line above is discharged.** It was re-measured with a three-line description in every entry, which is the tallest realistic case and the one the old fixture lacked, and both numbers came back the same. The collision it was raised for was **not** a track-sizing fault at all — the tracks were right on both surfaces — so nothing here shifts. Build the second sheet against 16 / 24. |
| 2026-08-12 | (no change) | **The bound is already wrong, and the printed page is already broken — at 13 entries, not 24.** Looked at the first adopting project's exported PDF: page 1 is the generated contents page and its **fourth row collides with the page footnote** — card 13's last line and the words *"Detail behind the disclosure panels is on screen only"* print through each other — while rows 2 and 3 have card borders touching where entries with three-line bottom lines overrun their track. **16 / 24 was measured against boxes whose bottom lines were shorter than real ones.** So this task's premise is no longer *the next deck will be longer*; it is *a shipped deliverable already prints wrong*. The re-measurement is now in scope, not just the second sheet. |
| 2026-08-12 | (no change) | **Re-estimated `low` → `high`, and unparked.** Nothing about the task changed; its premise did. The `low` of 2026-08-10 rested on one sentence — *"the bound bites at 24 slides against a target deck of 12, so nothing this project produces reaches it"* — and the owner has now said the next deck is not limited to 12. **16 is the bound and 24 the hard limit**, so a deck of the size being planned crosses the first and can reach the second, where DS-226's invariant clips an entry. The work is no longer outside the target case; it is in front of it. Stays in `PH2`: the reason it sits there is unchanged. |
| 2026-08-10 | (no change) | **Unblocked the same day.** [T-084](T-084-the-contents-bound-fixture-counts-a-deck-that-no-longer-exists.md) closed: the fixture was counting twelve boxes for a deck that now builds thirteen, and re-baselining it restored the tool. It re-measures **16 as the bound and 24 as the hard limit** — the same pair this task was specified on — so nothing in §1 moves and the edge is removed. |
| 2026-08-10 | (no change) | **Now `blocked_by` [T-084](T-084-the-contents-bound-fixture-counts-a-deck-that-no-longer-exists.md).** `contents_bound.py` refuses to start — its fixture expects 12 contents boxes and the reference deck now builds 13 — so the instrument that measured this task's 16-entry bound, and the only thing that could verify a split, does not run. The specification is unaffected: both its open questions were answered from a run made while the tool still worked. A hard edge rather than `related` because the *verification* is genuinely gated, which is the test `TASK-WORKFLOW.md` §4 sets. Recorded during T-078's sweep of the release gate list, which is what found the tool red. |
| 2026-08-10 | (specify) | **Estimated `low`/`m`.** `low` because the bound bites at 24 slides against a target deck of 12, so nothing this project produces reaches it — what the task buys is closing DS-226's known-unimplementable range, not serving a reader; `m` for print pagination that must carry every entry across a break. **Stays in `PH2`** under the release split set by the owner 2026-08-10: moderate in size, and a conformance fix to a page that exists rather than a new capability. |
| 2026-08-08 | → proposed | Raised by [T-034](T-034-a-contents-page-for-the-printed-deck.md) on the strength of its own measurement rather than on a hunch. T-034 specified the second page as the *presumptive* answer past its single-page bound and said the measurement would decide whether the question cost anything; it measured **16 as the bound and 24 as the hard limit against a target deck of 12**, which puts the work outside the target case — so it is raised, not built. What stops it being simply dropped is that **DS-226 states an invariant the implementation cannot honour past 24 slides**: a box then has 89 du of height for 96 du of number, title and padding, so an entry is necessarily clipped. A ruleset with a known unimplementable range needs either this task or an amendment, and that choice is better made deliberately than by silence. |
