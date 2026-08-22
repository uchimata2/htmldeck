---
id: T-041
title: Implement the nine glitch-free conditions R6 defined and nothing adopted
type: deliverable
status: done
phase: review
parent: null
blocked_by: []
related: [T-005, T-016, T-019]
work_package: PH3
owner: maintainer
business_value: high
effort: l
created: 2026-08-09
updated: 2026-08-22
shipped_in: 0.6.0
deliverables: [tools/deck/glitchfree.py, docs/lessons/L-129.md]
---

# T-041 — Implement the nine glitch-free conditions R6 defined and nothing adopted

## 1. Specify

**Outcome**
`tools/deck/check.py` decides all nine conditions in
[`R6 §8`](../docs/research/R6-portability-contract.md), or names the ones it cannot with a reason,
in the same account that already covers the `DS-nnn` rules.

**Why this one**
**CLAUDE.md rule 2 requires a deck to render glitch-free in recent Chrome/Edge**, and that is a
testable statement only once it is decomposed. R6 §8 decomposed it into nine conditions *"for T-005
to implement"*, [`BRIEF.md`](../docs/BRIEF.md) recorded that assignment — and
**[T-005](T-005-build-check-the-gate-the-deck-must-pass.md)'s own §1 never adopted them.** Its
acceptance criterion says *fails when the deck does not render glitch-free from `file://`* and then
scopes itself, in its own sentence, to the **restricted-origin** class. So the criterion was met as
written and seven of the nine conditions were never anyone's.

**This is L-39 in a new shape and it is worth stating.** Nothing was recorded falsely: R6 proposed,
BRIEF relayed the proposal, and T-005 wrote a narrower criterion. The gap is **between** two
documents that each read correctly on their own, and it survived because no check compares a
research recommendation against the task that inherited it. Found on 2026-08-09 while reconciling
the two at close, not by either.

**Where the nine stand**

| # | Condition | Today |
| :--- | :--- | :--- |
| 1 | Zero external references | **built** — DS-001 |
| 2 | No console errors, no unhandled rejections | **half** — DS-005 and DS-006 catch the restricted-origin causes statically; nothing observes the console. Named as unmet in T-005's own review |
| 3 | Every declared face actually loaded | **not built** — `render.py`'s probe reports `document.fonts.status` and no verdict reads it |
| 4 | No text in a fallback family | **not built** |
| 5 | Nothing overflows its stage | **measured, not gated** — `render.py report()` prints overflow findings; `check.py` emits no verdict |
| 6 | Layout stable after fonts settle | **not built** |
| 7 | Every canvas/WebGL surface drew something | **not built**, and no deck here has a canvas — so it must fail on *nothing measured* rather than pass on it |
| 8 | Every slide reached without a script error | **implicit** — the probe's `goTo` throws if it cannot drive the deck, which reads as NO RESULT; not a named verdict |
| 9 | Looked at, by a person | **not a check and never will be** (**L-01**) — CLAUDE.md rule 6 owns it |

**Re-verified 2026-08-22, before planning off a table written ten days earlier.** All nine rows
are unchanged. Row 2: one `onerror` exists in the whole package and it belongs to `rulerstrip.py`'s
image load, so nothing observes the console. Row 3: `render.py` `:199` still reports
`document.fonts.size + '/' + document.fonts.status` into a payload that only `render.report()`
prints. Row 5: `render.py` `:249` still collects `overflow` findings that no `check.py` verdict
reads. Rows 4, 6 and 7 have no producer at all - `preflight.py`'s `uses_canvas` and `uses_webgl`
belong to [T-019](T-019-build-the-capability-preflight-the-deck-ships-wit.md)'s in-deck instrument,
which this scope excludes, and `audit.py`'s DS-111 and DS-119 read canvas *markup* rather than
canvas *output*. Row 7's subject is still absent from every deck here.

**Scope**
- In: conditions 2 to 8, as verdicts in `check.py`'s existing row shape, each with its own ID —
  these are not `DS-nnn` rules and must not borrow one (**T-038**).
- In: a seeded variant per condition, in `static_variants.py`, since **a check that has never been
  seen to fail is a claim about the instrument** (**L-36**, **L-42**).
- In: condition 9 stated in the output as out of the gate's reach, alongside the five blind
  dimensions already named there.
- Out: **the in-deck capability preflight**, which is
  [T-019](T-019-build-the-capability-preflight-the-deck-ships-wit.md) — that runs inside a shipped
  deck on the recipient's machine; this runs in the harness before it ships. Two different
  instruments answering two different questions, and conflating them is how one gets built twice.
- Out: any new `DS-nnn` rule. R6 §8 is a decomposition of CLAUDE.md rule 2, not new design law.

**Inputs**
- [`R6 §8`](../docs/research/R6-portability-contract.md) — the nine, with how each is tested
- [`tools/deck/check.py`](../tools/deck/check.py) — the account, and where a non-`DS` ID already
  lives (`FIG-1` to `FIG-3`, `PRINT-1`, and §7's criterion numbers)
- [`tools/deck/render.py`](../tools/deck/render.py) — the probe already carries the font status and
  the overflow measurement conditions 3 and 5 need

**Acceptance criteria**
- [ ] Each of conditions 2–8 is either a verdict or is excused in writing, in the same account
- [ ] Condition 7 **fails on a deck with no canvas rather than passing** — the subject being absent
      is not the subject being sound
- [ ] Each new verdict has a seeded variant that it catches
- [ ] The reference deck still passes, or the new failure is a real defect and is written down
- [ ] The output names condition 9 as the gate's boundary, not as satisfied

**Open questions**
- ~~**Does the console-error check need a second render, or can the hook ride the existing one?**~~
  **Answered 2026-08-09: the existing one**, as the recommendation stood. The hook must be injected
  in `<head>`, before the deck's own script, so a load-time error is caught; `render.make_probe`
  appends to `</body>` today and needs a second injection point. **That is one change to the
  harness, not a second browser run** — it keeps `EVALUATION.md` §2's one-render-per-stage cost
  model, and it avoids the failure mode a second render introduces: two runs that disagree, where
  the error is real in one and absent in the other and nothing says which reading is the deck's.

## 2. Plan

**The IDs are `GF-2` to `GF-8`, numbered off R6 §8's own table**, so a verdict names the row it
comes from. `GF-1` is absent on purpose: condition 1 is DS-001 and already decided, and minting a
second ID for it would put one condition in two accounts. They sit beside `FIG-1` to `FIG-3`,
`PRINT-1` and `RENDER` as non-`DS` IDs, which is the precedent §1 names (**T-038**).

**They go in a module of their own rather than as rows in `audit.py`.** `figgrid.py` and
`markhits.py` each own their measurement and their probe for one stated reason: a second copy of a
probe beside the verdicts it feeds is the composition that disagreed the first time either half
changed (**L-08**, **L-13**). Seven conditions needing one walk of every slide is the same shape.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Re-verify §1's nine-row table against the tools as they stand, before planning off it | Done - the paragraph after the table in §1. All nine rows unchanged |
| 2 | Give `make_probe` a `<head>` seam and inject an error trap through it, **unconditionally**, on `MOTION_PIN`'s argument; extend T-209's guard to assert both | `render.py` - `ERROR_TRAP`, the `<head>` injection, the guard |
| 3 | Build the module: one probe that walks every slide with the trap listening, and `verdicts(deck)` returning `GF-2` to `GF-8` in `check.py`'s `(rule, what, ok)` shape | `glitchfree.py`, under `tools/deck/` |
| 4 | Wire it into `check.py`: `gather()` calls it, `NOT_STATIC` records why it is outside the browserless half, and the closing text names condition 9 as the gate's boundary beside the five blind dimensions | `check.py` |
| 5 | Seed one variant per condition and prove each red before keeping it - a fourth collector, since `render_failures` reaches `audit.render_verdicts` and nothing else | `static_variants.py` - `GF_VARIANTS` and `glitchfree_failures` |
| 6 | Run `python tools/tasks/lint.py`, then `python tools/check_all.py`, then render and **look at** the example deck offline (CLAUDE.md rule 6, §7 step 3) | §3 and §4, with the verdicts as produced |

**Three decisions taken here, so implementation does not re-open them:**

- **The error trap is unconditional in `make_probe`, and no caller can decline it.** This is
  [T-209](T-209-six-more-probes-measure-a-page-whose-entrance-never-ran.md)'s argument for
  `MOTION_PIN` reused: eight probe sources pass an `extra`, and anything a caller has to remember is
  a thing eight callers will forget (**L-57**). It differs from the pin in one way that matters -
  the pin *changes* the page and the trap only listens - so the pin's `MEASURES_MOTION` exemption
  has no counterpart here and none is added.
- **`GF-7` on a deck with no canvas returns `ok is None`, not `ok is False`.** §1's criterion says
  *fails ... rather than passing*, and its own gloss says why: *the subject being absent is not the
  subject being sound*. `check.py` grew a third state for exactly that after this criterion was
  written - `NO SUBJECT`, which `run()` excludes from `failures` by `is False` and `account()`
  buckets as `undecided`, documented there as *not a coverage fault*. `None` says what the gloss
  asks for. `False` would make a canvas-free deck un-passable, which is a check forbidding a design
  choice, and CLAUDE.md rule 3 permits canvas rather than requiring it. **Recorded as a deviation
  from the criterion's word, reported at review rather than reworded** (`TASK-WORKFLOW.md` §2).
- **`GF-5` uses R6's stated test**, `scrollWidth <= clientWidth` and `scrollHeight <= clientHeight`
  on the stage, rather than adopting `render.py`'s richer `overflow` list. The list is a different
  measurement with a different tolerance, and taking a verdict from it would make the ID name a row
  of R6 §8 that it does not decide.

**Two risks named before they are met, each to be settled with a measurement rather than a guess:**

- **`GF-6` may be vacuous under `--virtual-time-budget`.** A CSS clock there is frame production
  rather than time (**L-26**), so first paint and `document.fonts.ready` can fall in one frame - and
  then *no shift* means *no interval*, which reads as a pass. If the two snapshots come from the
  same frame, the verdict is `None` with that reason, never `True`.
- **`GF-4` may have legitimate offenders.** A generic family used deliberately is not a fallback
  failure. What the reference deck actually does is a measurement, taken at step 3, and whatever it
  shows is written down rather than tuned away.

## 3. Implement

**Decisions & assumptions**
- **The three §2 decisions were taken as planned and none was re-opened.** `GF-2` to `GF-8` off R6's
  numbering, a module of its own, the unconditional `<head>` trap, `GF-7` returning NO SUBJECT on a
  canvas-free deck, and `GF-5` reading R6's stated test. — 2026-08-22
- **`_verdicts_from` had to become `_verdict_rows`, and the reason is a rule this package enforces.**
  `audit.verdict_producers` discovers a producer by matching `def *verdicts*` across every file in
  the directory, so the private helper was counted as a second producer and `check.producer_split`
  stopped the run over it. `figgrid._verdict_from` is the precedent; renaming keeps the helper out
  of a table that describes families of rows. — 2026-08-22
- **The probe has to report `vw` and `vh` even though neither is its subject.** `render.calibrate`
  corrects the outer-window shortfall from them, so a probe that omits them dies in `calibrate` with
  a `KeyError` rather than a message. That is `make_probe`'s contract rather than this module's
  choice, and it is now written where the payload is built. — 2026-08-22
- **Condition 7's measurement moved out of the per-slide walk and became document-wide, taken once
  after it.** Scanning per slide counts one surface once per visit; scanning before the walk gives a
  canvas drawn on entry to slide 9 no chance to have drawn. Running it last means every slide has
  been current at least once. — 2026-08-22
- **`GF-6` was unmeasured on half the corpus, and that was the instrument rather than the decks.** On
  `requestAnimationFrame` alone it returned *no frame was painted before the fonts settled* for
  `sort-window` and `portfolio-review` — a sentence about headless, delivered in the deck's voice.
  Racing a `setTimeout(0)` against the frame callback took the reading to **4 of 4 measured, every
  one across a real interval and every one passing.** Fixed here rather than raised: a condition
  that declines on half the decks it is pointed at is not a condition that was implemented. — 2026-08-22
- **Two seeded variants broke more than their own condition and were narrowed.** `GF-6`'s first seed
  moved a slide **down** 40 px, which pushed content below the stage and failed `GF-5` on 10 of 13
  slides; a negative offset moves the boxes without adding anything to scroll to. `GF-8`'s first
  seed renamed `id="next"` and broke the deck's own init — `GF-8` came back *0 of 13, no slide
  carries data-current*, `GF-2` failed on the resulting throw, and `GF-4` and `GF-6` lost their
  subject. That proves the gate notices a broken deck, which was never in question. The replacement
  adds a fourteenth slide outside the stage, so the walk reaches 13 of 14 and nothing else moves. — 2026-08-22
- **`GF-7`'s pass direction had never been observed and the corpus cannot produce it, so it was
  seeded.** No deck here draws a canvas, so the only state the corpus produces is NO SUBJECT and the
  only state the suite seeded was FAIL. A pixel scan hard-wired to *blank* would have produced
  exactly that record. `GF_PASS_VARIANTS` and `run_must_pass` are the other direction, asserting the
  row comes back `True` rather than merely *not caught* — which NO SUBJECT already satisfies. This is
  **L-129**. — 2026-08-22

**Outputs produced**
- [`tools/deck/glitchfree.py`](../tools/deck/glitchfree.py) — the probe, `GF-2` to `GF-8`, and a
  browser-free self-test holding every row in all the states it can reach.
- [`tools/deck/render.py`](../tools/deck/render.py) — `ERROR_TRAP`, `inject_head`, the second seam
  in `make_probe`, and T-209's guard extended to cover both seams on the page `make_probe` writes.
- [`tools/deck/check.py`](../tools/deck/check.py) — `gather` calls the module, `NOT_STATIC` records
  why it is outside the browserless half, and the closing text names condition 9 as the boundary.
- [`tools/deck/audit.py`](../tools/deck/audit.py) — the seven conditions in `ABSENCE_IS_A_FAIL`, and
  the producer exercised by the absent-subject fixture.
- [`tools/deck/static_variants.py`](../tools/deck/static_variants.py) — `GF_VARIANTS`,
  `GF_PASS_VARIANTS`, `glitchfree_failures` and `run_must_pass`.
- [`docs/lessons/L-129.md`](../docs/lessons/L-129.md) — a check for something the corpus does not
  contain is never seen to pass, and that looks exactly like working.

**What the four shipped decks report**

| Deck | GF-2 | GF-3 | GF-4 | GF-5 | GF-6 | GF-7 | GF-8 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `reference-deck` | pass | pass 3/3 | pass | pass 0/13 | pass | NO SUBJECT | pass 13/13 |
| `sort-window` | pass | pass 3/3 | pass | pass 0/12 | pass | NO SUBJECT | pass 12/12 |
| `measure-first` | pass | pass 3/3 | pass | pass 0/14 | pass | NO SUBJECT | pass 14/14 |
| `portfolio-review` | pass | pass 3/3 | pass | pass 0/12 | pass | NO SUBJECT | pass 12/12 |

**No shipped deck reddened**, so §1's fourth criterion is met in its first branch and there is no new
failure to write down. `GF-7` is NO SUBJECT on all four for the one reason the condition exists:
none of them draws a canvas.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Each of conditions 2–8 is either a verdict or is excused in writing, in the same account | met | All seven are verdicts, in `check.py`'s `(rule, what, ok)` shape, gathered by `gather()` and printed in the same verdict block as the `DS-nnn` rules. None needed excusing. |
| Condition 7 fails on a deck with no canvas rather than passing | met, and the wording deviated from | It returns `ok is None` — NO SUBJECT — not `ok is False`. The criterion's own gloss is *the subject being absent is not the subject being sound*, and `None` is the state `check.py` grew for exactly that after this criterion was written: `run()` excludes it from `failures` by `is False` and `account()` documents it as not a coverage fault. `False` would make a canvas-free deck un-passable, which is a check forbidding a design choice CLAUDE.md rule 3 permits rather than requires. **Reported rather than the criterion reworded** (`TASK-WORKFLOW.md` §2). |
| Each new verdict has a seeded variant that it catches | met | **7 of 7 caught**, through a real browser, each seeded against its own condition after two were narrowed for breaking a second. `GF-7` additionally has the pass direction seeded — 1 of 1 — which is **L-129**. |
| The reference deck still passes, or the new failure is a real defect and is written down | met | `python tools/deck/check.py examples/reference-deck.html` exits 0. All four shipped decks pass all seven; the table in §3 is each one's row. |
| The output names condition 9 as the gate's boundary, not as satisfied | met | The closing paragraph now states that DS-001 and `GF-2` to `GF-8` make *renders glitch-free* eight-ninths measured, and that the ninth is a person — not deferred, not excused, not scheduled — and that the gate reaching green is the moment looking becomes due rather than the moment it is discharged. |

**Looked at, offline** (`TASK-WORKFLOW.md` §7 step 3, CLAUDE.md rule 6). This task produced checks
rather than a deck, and what it changed about rendering is the page `make_probe` writes — so the
subject is whether a deck still renders correctly with a script injected into its `<head>`. Slides 3
and 7 of the reference deck were rendered through the modified probe and opened: the display serif,
the mono eyebrow and the ruler all settle correctly, the disclosure control and the two-series SVG
chart draw in full, and the ruler marks 03/12 and 07/12 with the position mark visible. Nothing the
trap injects shows on the page.

**Child fix tasks raised**
- none. Two candidates were met inside the task instead: `GF-6`'s unmeasured half of the corpus,
  fixed by racing a timer against the frame callback, and `GF-7`'s unobserved pass direction, fixed
  by seeding the subject and recorded as **L-129**.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-22 | (shipped) | **Shipped in `0.6.0`.** The release note carries `docs/PUBLISHING.md` §8.1's row for this version, which names what an adopter must change and the smallest edit that satisfies it. |
| 2026-08-22 | planned → done | **Seven conditions built, seeded and proved.** `GF-2` to `GF-8` in `tools/deck/glitchfree.py`, a second `<head>` seam in `make_probe` for the console trap, and the T-209 guard extended to cover both seams. 7 of 7 seeded variants caught, and `GF-7`'s pass direction seeded as well because the corpus cannot produce it, which is **L-129**. All four shipped decks pass all seven; `GF-6` was unmeasured on two of them until a `setTimeout(0)` was raced against `requestAnimationFrame`. **R6 section 8 is now eight-ninths a verdict and the ninth is a person, which the gate now says in words.** |
| 2026-08-22 | proposed → planned | **Specify re-verified and plan written.** §1's table dates from 2026-08-12 and is the scope, so it was re-derived against the tools first; all nine rows stand. The plan mints `GF-2` to `GF-8` off R6 §8's numbering, puts them in a module of their own on `figgrid`/`markhits` precedent, and takes three decisions up front - the unconditional error trap, `GF-7`'s `NO SUBJECT` on a canvas-free deck, and `GF-5` reading R6's test rather than `render.py`'s overflow list. |
| 2026-08-10 | (specify) | **Estimated `high`/`l`, and moved to `PH3`.** `high` because CLAUDE.md rule 2 is a testable statement only once decomposed, and seven of R6's nine conditions are still nobody's; `l` because each condition needs its own probe, or its own stated reason for not having one, in an account that already partitions 113 rules. `PH3` under the release split set by the owner 2026-08-10, on size. |
| 2026-08-09 | → proposed | **Raised at close, from a gap between two documents that each read correctly alone.** [R6 §8](../docs/research/R6-portability-contract.md) decomposed CLAUDE.md rule 2 into nine testable conditions *"for T-005 to implement"*; [`BRIEF.md`](../docs/BRIEF.md) relayed that; [T-005](T-005-build-check-the-gate-the-deck-must-pass.md)'s §1 wrote a narrower criterion scoped to the restricted-origin class, met it, and closed. **Nothing was recorded falsely and seven conditions were nobody's** — which is the shape worth remembering, because the usual failure is a claim that outran the work and this is the opposite: work that outran nothing, in a corner no one was looking at. Condition 2 is the one T-005 already names as unmet in its own review, so this task inherits a defect that was declared rather than found. |
