---
id: T-018
title: Measure the printable mode — what printing a deck from `file://` actually costs
type: research
status: done
phase: review
parent: null
blocked_by: []
related: [T-002, T-005, T-017, T-021]
work_package: WP1
owner: maintainer
created: 2026-08-06
updated: 2026-08-07
deliverables: [docs/research/R7-printable-mode.md]
---

# T-018 — Measure the printable mode — what printing a deck from `file://` actually costs

## 1. Specify

**Outcome**
A tested statement of what the optional printable mode can promise, and what it costs the design to
support it — so that "printing is optional" is a decision backed by measurement rather than an
assumption that it will be easy when someone gets to it.

**Why this one**
[R6](../docs/research/R6-portability-contract.md) §9 settled the surrounding envelope and then
stopped at an honest gap: `matchMedia('print')` is available from `file://`, so a print stylesheet
can be *authored and detected* — but **whether `window.print()` behaves from a double-clicked file,
and whether a print stylesheet reproduces the deck faithfully at page size, was never tested**.
Nothing in the portability matrix threatens printing and nothing in it confirms printing. That gap
is small, cheap to close, and exactly the kind that gets discovered by a user rather than by us.

Rule 5 in [`CLAUDE.md`](../CLAUDE.md) makes printing *a mode the user can force on, never a
constraint on the design*. That ruling is safe only if the cost is known. If it turns out that a
faithful print mode demands a second layout, the rule stands but the plugin owes the user a plain
statement of what printing does and does not preserve.

**Scope**
- In: does `window.print()` open the print dialog from `file://`, and is it gesture-gated.
- In: whether background colours and images print at all — `print-color-adjust: exact` is the
  usual answer, and whether the browser honours it from a restricted origin is not assumed.
- In: pagination, **both renderings** — the paginated stage at one slide per printed page via
  `@page` size/orientation and break control, and the reflow document as continuous flow. Which of
  the two the printable mode uses is a **finding of this task, not an input to it**; see the ruling
  in the log.
- In: what a print stylesheet costs in KB, measured the way R5 measures everything else.
- In: which parts of a deck **cannot** survive print by construction — progressive disclosure
  behind interaction, motion, 3D, anything whose content is only reachable by clicking. This is
  the important half: the printable mode's honest guarantee is about the *static* deck.
- Out: PDF export through a headless renderer. That is a different mechanism with a different
  dependency profile, and it is scoped with speaker notes in [BRIEF.md](../docs/BRIEF.md) open
  question 4.
- Out: speaker notes.

**Inputs**
- [`docs/research/R6-portability-contract.md`](../docs/research/R6-portability-contract.md) §9 —
  the gap this task closes, and the method that produced the rest of the matrix.
- [`docs/research/R5-assets-and-licences.md`](../docs/research/R5-assets-and-licences.md) — the
  probe deck and how size is measured here.
- [`tools/portability/`](../tools/portability/) — the probe and runner to extend rather than
  reinvent.
- [`examples/reference-deck.html`](../examples/reference-deck.html) — **twelve slides**, so it
  meets the L-02 bar without a deck being written for this task, and it already carries the
  `@media print` block that prints the reflow view. That block is the starting point for one of the
  two renderings, and it has never been printed.

**Method**
The same as T-017's, and for the same reason: **test, do not read.** Print behaviour from a
restricted origin is exactly the sort of thing documentation describes for the HTTP case. Extend
the existing probe rather than building a new one, and honour the two prohibitions T-017 paid for —
**no in-tool preview pane** (it fails optimistically, **L-15**) and **no synthetic input** to
produce the gesture, if one turns out to be required.

Print output is inspected by printing **to a file**, not to a device. Nothing in this task should
send anything to a physical printer. The file is produced through the **browser's own print
dialog**, not by a headless renderer driving `--print-to-pdf`: that is a different code path from
the one a recipient uses, and measuring it would answer a question nobody asked (**L-15**'s failure
direction, arrived at from the other side). Headless is out of scope as a *mechanism* under
*Scope*; this sentence puts it out of scope as an *instrument* too.

The gesture question is already settled and needs no new decision:
[R6](../docs/research/R6-portability-contract.md) §3 records that the activation is a real human
click, that an OS-level synthetic version was built and **withdrawn**, and that hard-to-collect
gesture rows are collected by hand. `tools/portability/run_probes.py` already carries
`ask_for_gesture()`, which asks the operator and waits. The print rows reuse it.

**Acceptance criteria**
- [ ] `window.print()` behaviour from a double-clicked file recorded on Chrome and Edge, with
      versions, and with an explicit statement of whether it needs a user activation
- [ ] Background/colour fidelity recorded, including whether `print-color-adjust: exact` is honoured
- [ ] Both renderings demonstrated on the **same real 12-slide deck**, not a toy (**L-02**) — the
      paginated stage at one slide per page, and the reflow document as continuous flow
- [ ] Both printed results **looked at**, not merely generated (**L-01**)
- [ ] A ruling on which rendering the printable mode uses, and with it an answer to the open
      question [T-021](T-021-the-reflow-view-and-the-resolution-contract.md) carries — *do the
      reflow view and the print stylesheet share one document rendering?*
- [ ] Size cost of the print stylesheet measured, not estimated — per rendering, so the choice
      between them is priced
- [ ] An explicit list of what the printable mode does **not** preserve, written for the user
- [ ] A ruling: does rule 5 survive as written, or does printing need something from the design
      after all — surfaced as a candidate change of direction if so

**Open questions**
- Does the print path deserve a row in the build check (T-005), or is it out of scope for a gate
  that only runs on the default `portable` mode? — owner decides once the cost is known.

## 2. Plan

**Approach decisions**

- **Extend `probe.html`, do not build a second probe** — the three-channel readback, the stale-window
  guard and the version capture all exist and all took a bug each to get right. The print rows are
  four automatic rows and one gesture row in the existing structure.
- **`window.print()` is a gesture row, not an automatic one, and its timeout is minutes not
  seconds.** It raises a modal dialog and does not return until that dialog is dismissed, so an
  automatic row would report `timeout` on a feature that works — the same false negative shape as
  the fullscreen row that nearly libelled the contract (**L-17**). The operator is present anyway,
  by the gesture rule.
- **`beforeprint` / `afterprint` are measured, and they are the rows that matter most.** If they
  fire from `file://`, the deck can **open every progressive-disclosure element before the print
  begins and close it afterwards** — which moves disclosure content from the "cannot survive print"
  list to the "survives, if the deck cooperates" list. §1's honest-guarantee criterion is written
  assuming the pessimistic answer; these two rows are what decide whether that assumption holds.
  Nothing in R6 measured them.
- **Two rendering variants, built from `examples/reference-deck.html`, kept out of the repository.**
  Same deck, same content, two print stylesheets — artefacts go to `.assets-cache/` like every other
  probe output, and the repository keeps the script and the numbers (R6's rule). Whether either
  stylesheet lands in the reference deck for good is [T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md)'s
  and [T-021](T-021-the-reflow-view-and-the-resolution-contract.md)'s business, not this task's.
- **Steps 2 and 4 are operator-run and scripted in advance.** Both need a real human click, and
  step 4 also needs the print dialog's destination and the save path chosen by hand. Written as a
  numbered script before the run rather than improvised during it, because a mis-run gesture row is
  indistinguishable from a refusal (**L-17** again).

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Add the print rows to `build_probes.py` — `matchMedia('print')` already exists; add `beforeprint`/`afterprint` firing, `print-color-adjust` support, `@page` support, and `window.print()` as a fifth gesture row | probe rows, self-test still passing |
| 2 | Run them: clean profile and literal double-click, Chrome and Edge, offline, with the operator's clicks | result set, with both browser versions |
| 3 | Build the two rendering variants from the reference deck — paginated stage, and reflow document | two variants in `.assets-cache/` |
| 4 | Print each variant to a file through the browser's own dialog, both browsers | four PDFs |
| 5 | Look at all four, page by page, and record what survived and what did not | findings, per rendering |
| 6 | Measure each stylesheet's size cost the way R5 measures | two figures |
| 7 | Rule: which rendering the printable mode uses, whether it shares one with the reflow view, and whether rule 5 survives as written | the ruling |
| 8 | Write the note | `R7-printable-mode.md`, under `docs/research/` |

## 3. Implement

**Decisions & assumptions**

- **A separate `probe-print.html`, not more rows in `probe.html`** — 2026-08-07. This reverses §2's
  first approach decision, and the reason is the second one: the print dialog is **modal**. A print
  row inside `probe.html` blocks the shared title channel and the shared result payload, so a run
  that stalled on a dialog would cost the 91-row matrix that was carrying it. `probe-3d.html`
  already establishes the pattern of a focused second page with its own light plumbing, so this is
  the file's habit rather than a departure from it. The 91 rows are also left untouched, which
  keeps R6's numbers comparable.
- **The no-activation attempt runs *before* the download, not after** — 2026-08-07. Its result then
  travels in the JSON rather than only in a title the gesture payload later overwrites. The
  accepted cost is that a browser which does **not** gate `print()` blocks there until the operator
  presses Escape; the page banner and the runner script both say so, and the block is itself the
  measurement. The runner's download wait is 150 s on this page for the same reason — 25 s would
  report a working run as a download failure.
- **`window.print()` is measured twice, and the pair is the row** — 2026-08-07. Once with no
  activation and once with a live one. Neither answers "is it gesture-gated from `file://`" alone,
  and reporting either alone is L-17's shape: a harness failure wearing a measurement's clothes.
- **Tier-two panels stay hidden in the paginated variant** — 2026-08-07. They are absolutely
  positioned overlays; unhiding them onto a fixed 1920×1080 box overlaps the content they explain.
  The loss is recorded as a finding rather than papered over. **The reflow variant does not have
  this problem** — `buildDoc()` already clones every slide and opens every panel (DS-073), so tier
  two travels into that rendering by construction, whether or not the reader ever switched views.
- **The variants are artefacts and stay out of the repository** — 2026-08-07. `.assets-cache/print/`,
  gitignored, per R6's rule that the repository keeps the script and the numbers. Neither
  stylesheet is proposed for the reference deck here; that is T-021's and T-028's call.
- **Steps 2 and 4 cannot be run by the agent** — 2026-08-07. Not a scheduling preference: **L-15**
  and R6 §1 prohibit answering these questions from an in-tool preview pane, because it reports
  capabilities as available that a real restricted origin denies, and the gesture must be a real
  human one per R6 §3. Both are operator-run, scripted in advance.

**Outputs produced**
- [`tools/portability/build_probes.py`](../tools/portability/build_probes.py) — builds
  `probe-print.html`: 7 automatic rows, 1 no-activation attempt, 1 gesture attempt. Its self-test
  gained checks for the placeholders, the six named rows, and **the absence of synthetic input**,
  so the technique R6 §3 withdrew cannot creep back in unnoticed.
- [`tools/portability/run_probes.py`](../tools/portability/run_probes.py) — the print probe's own
  operator script, and a 150 s download wait on that page.
- [`tools/deck/print_variants.py`](../tools/deck/print_variants.py) — emits both renderings from
  the committed deck, self-testing the replacement anchor first.
- **Size cost, measured (step 6, done ahead of the run):** the paginated stylesheet is **1 811 B**
  and the reflow one **1 110 B**. Against the deck as committed — which already carries a 232 B
  print block — the deltas are **+1.5 KB** and **+0.8 KB** on a 178.2 KB deck. Neither is a reason
  to refuse printing.
**Measured, step 2 — Chrome 151 and Edge 151, offline, clean profile, `file://`. Identical on all
nine rows.**

| Row | Result |
| :--- | :--- |
| `window.print()` present | PASS |
| **gesture-gated?** | **No.** The no-activation attempt opened a real dialog and blocked until Escape — 116 s on Chrome, 29 s on Edge — and threw nothing. With an activation it behaves identically. **The pair is the finding**: printing needs no user gesture from a restricted origin. |
| `beforeprint` / `afterprint` | **Both fire, from `file://`, in both browsers, in both attempts.** R6 never measured this. It is what lets a deck open its disclosure content before printing and close it after. |
| `matchMedia('print').matches` **inside** `beforeprint` | **`false`.** The media query does not report printing at the moment a deck would act on it. A deck must use the **events**, not the query — R6 recorded the query as "available" and that is true but not useful. |
| `print-color-adjust: exact` | PASS, both the standard and `-webkit-` spellings |
| `break-inside: avoid`, `break-after: page` | PASS |
| `@page` | Parses as `CSSPageRule`; the `size` descriptor is exposed on `.style` |
| `@page` margin boxes | Survive parsing (which is not the same as rendering, and was not tested) |

**Steps 3–5 — the first run failed, and the failure was mine.** The paginated variant printed
**thirteen blank pages**. The PDF says how blank: correct geometry (1440×810 pt = exactly the
1920×1080 px `@page`), one white rectangle on page 1, **no font resources at all**. Three defects,
each measured rather than guessed:

1. **The deck changes its own view while printing, and the print stylesheet has to survive that.**
   This is the finding of the task, and it took three printed runs to see. The deck switches to the
   reading view below 960 px and sets `viewport.hidden` when it does (`reference-deck.html` line
   ~1408) — and **printing is what makes it switch**, because printing changes the layout viewport.
   `.viewport[hidden]{display:none}` then hides the stage, and overriding `position` never touches
   `display`. So:
   - run 1 hid the reading view with `!important` *and* the stage was hidden by `[hidden]` →
     **thirteen blank pages**;
   - run 2 dropped the `.doc` rule → **the reading view printed**, which looked like a fix and was
     not: the paginated stylesheet had still never rendered a single slide;
   - run 3 forces `display` on both `.viewport` and `.viewport[hidden]` → the stage prints, from
     either view state.

   An earlier note here called the mechanism unexplained. It is not: the colour-marker measurement
   that ruled out a view change was taken **headlessly**, and headless does not flip the view. That
   is the same instrument error §1 scoped headless out for, caught by the same rule.
2. **`.slide:last-child` never matched**, so the twelfth slide kept its page break and emitted an
   empty thirteenth page. The stage ends with the nav and the progress bar, not with a slide.
   `section.slide:last-of-type` is the fix.
3. **Pinning `@page { size }` removes the reader's paper controls** — confirmed twice, on both
   variants: orientation on the reflow one, the whole layout section on the paginated one. A print
   stylesheet that dictates paper takes a decision away from the person holding the printer. The
   reflow variant now sets `margin` only. The paginated one **keeps** its pinned 1920×1080 page,
   because there the page shape *is* the design — but that is now a stated cost, not an accident.
4. **`break-inside: avoid` on whole sections wasted 45% of the pages.** A section is a slide's
   worth of content, often most of a page tall, so any that would not fit was pushed whole and left
   the remainder blank: **22 pages, nine of them carrying a third of their neighbours' text.**
   Allowing sections to break and protecting only figures, tables and panels: **12 pages, same
   content.** This is what "the page breaks are terrible" was.
5. **`.slide{position:static}` scatters the disclosure panels.** A slide is the containing block
   for its own absolutely positioned descendants; making it static hands them to the page.
   `position:relative` keeps it in flow *and* keeps it a containing block.
6. **`print-color-adjust:exact` makes the dialog's "Background graphics" tick inert.** That is why
   toggling it changed nothing. Defensible here — this design's backgrounds are content, not
   decoration, and the property exists to say so — but it is one more reader decision the deck
   quietly takes.
7. **Chrome's default header/footer prints the deck's absolute `file://` path** across the foot of
   every page. Not reachable from CSS, and it is a real disclosure: a recipient printing a deck
   leaks their own directory layout into the paper copy. The printable mode can warn; it cannot fix.
8. **Disclosure controls print as collapsed buttons advertising content that is not there.**
   Worse than losing tier two silently. But `beforeprint` fires (measured above), so the fix is
   available and cheap: open every panel on `beforeprint`, close them on `afterprint`.

Corrected, both renderings produce real output. **Awaiting re-verification by a real print**, which
is the only evidence this task may cite for a rendering claim.

**A note on instruments, because it matters to how much of the above can be believed.** Headless
Chrome was used **only to diagnose** the blank pages, never to measure the printable mode: it is a
different code path from the one a recipient uses, which is why §1 puts it out of scope. Every
claim above about *behaviour* comes from the probe run in a real browser; every claim about *the
rendering* is pending the real print. `render.py`'s header warns that DS-140's infinite animation
can make a headless capture blank (**L-26**), which would have made the whole diagnosis worthless,
so the decisive comparison was repeated with motion pinned off: **byte-for-byte identical**. The
artifact was not in play.

- `R7-printable-mode.md`, under `docs/research/` — **written as a name, not a path, because it
  does not exist yet.** `check` reports a pointer-shaped string to a missing file as a dead
  pointer, and since T-029 there is no exemption for declared deliverables. The front-matter
  `deliverables:` field carries the real path, and `task.py deliverables` is what reports on it.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| `window.print()` behaviour from a double-clicked file on Chrome and Edge, with versions, and an explicit statement of whether it needs a user activation | met | [R7](../docs/research/R7-printable-mode.md) §2. Chrome 151 and Edge 151, identical on all nine rows. **It needs no activation** — called without one it opened a real dialog and blocked until dismissed, 116 s and 29 s, `threw=no`. Measured twice, with and without, because either alone is unattributable (**L-17**). |
| Background/colour fidelity recorded, including whether `print-color-adjust: exact` is honoured | met | R7 §2 — both the standard and `-webkit-` spellings, both browsers. R7 §5.4 records the consequence nobody asked for: it makes the dialog's "Background graphics" checkbox inert. |
| One-slide-per-page pagination demonstrated on a **real 12-slide deck**, not a toy (**L-02**) | met | R7 §4. Twelve pages, one slide per page, 1920 × 1080 px, fonts embedded. `examples/reference-deck.html` is twelve slides, so no deck was written for the task. |
| Both renderings demonstrated on the **same** deck | met | R7 §4, both from `tools/deck/print_variants.py` off the committed deck. |
| Both printed results **looked at**, not merely generated (**L-01**) | met | Page by page, as images, across five export rounds. Looking is what found the second failure: the export "worked" and was printing the **reading view**, which no page count or byte size would have shown. |
| A ruling on which rendering the printable mode uses, and with it an answer to T-021's open question | met | R7 §4 — **the paginated stage**; the reading view is not a print target. T-021's *do the reflow view and the print stylesheet share one document rendering?* is answered **no**, measured rather than asserted. |
| Size cost of the print stylesheet measured, not estimated — per rendering | met | R7 §6. 3 063 B and 2 422 B; +2.7 KB and +2.1 KB on a 178.2 KB deck. Under 2% either way. |
| An explicit list of what the printable mode does **not** preserve, written for the user | met | R7 §5, five entries. The largest is **38.6% of the deck's text** behind disclosure — counted, not estimated. Two were not anticipated in §1: the reader's paper choice, and the absolute `file://` path Chrome prints on every page. |
| A ruling: does rule 5 survive as written, or does printing need something from the design after all — surfaced as a candidate change of direction if so | met | R7 §7 — **it survives, and it did work here**: rule 5 is what said to stop reshaping the reading view. One clarification added, that "optional" obliges the mode to state its limits. The candidate change of direction — a cooperative mode using `beforeprint` to carry tier two — is **raised, not taken**, as [T-032](T-032-adopt-the-paginated-print-mode-in-the-reference-deck.md). |
| *(open question)* Does the print path deserve a row in the build check (T-005)? | deferred, deliberately | §1 assigned this to the owner "once the cost is known". The cost is now known and it is small, but the check runs on `portable` mode and printing is optional — so this is T-005's call with R7 in hand, not a verdict to take here. Recorded rather than dropped. |

**What this task got wrong, since the record is worth more than the score.** Three of the five
printed rounds failed on defects in the stylesheet or the harness rather than on browser behaviour,
and the instrument rules are what caught each: headless disagreeing with the real browser
(**L-35**, new), a quality metric counting the browser's own header and footer as content, and
verification on the wrong paper size. The measurement that mattered — §2's nine rows — was right
from the first run, in both browsers.

**Child fix tasks raised**
- [T-032](T-032-adopt-the-paginated-print-mode-in-the-reference-deck.md) — the reference deck still
  prints the reading view, which R7 rejected, and the tier-two decision needs an owner.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-07 | (no change) | **The one question this task closed with deferred is now answered, and it landed where §4 said it would.** The owner ruled 2026-08-07 that the print path **does** earn a row in [T-005](T-005-build-check-the-gate-the-deck-must-pass.md), **opt-in only** — it runs when a printable deck was asked for and not otherwise, so printing stays a mode rather than becoming a gate on the design (rule 5). The row asserts [R7](../docs/research/R7-printable-mode.md) §4's three rules and the page count; the page count is in it because this task's own worst failure was **silent** — thirteen blank pages that no presentation check can see. Recorded here so the deferral has a visible end: §4's verdict row said *"recorded rather than dropped"*, and this is the drop being avoided. |
| 2026-08-07 | → done | [R7](../docs/research/R7-printable-mode.md) written; every criterion has a verdict in §4 and the one open question is deferred to T-005 deliberately rather than dropped. **The ruling: the printable mode is the paginated stage, and the reading view is not a print target** — which answers T-021's shared-rendering question with a measured *no*. Rule 5 survives as written, with one clarification: "optional" obliges the mode to state its limits, so R7 §5 lists them, the largest being 38.6% of the deck's text behind disclosure. The owner ruled that print states the loss and hides the affordance rather than carrying tier two; the cooperative alternative `beforeprint` makes possible is raised as [T-032](T-032-adopt-the-paginated-print-mode-in-the-reference-deck.md), which also has to correct the reference deck — it still prints the rendering R7 rejected. **L-35** is new and is the task's most reusable output: an instrument scoped out for being a different code path will eventually prove it. Five printed rounds, three of which failed on this task's own stylesheet or harness rather than on the browser. |
| 2026-08-07 | → planned | Eight steps, two of them operator-run. The plan found something §1 had not: **`beforeprint`/`afterprint` were never measured by R6**, and they decide how much of §1's honest-guarantee criterion is even true. If they fire from `file://`, a deck can open every disclosure element before printing and close it after, which moves progressive-disclosure content out of the "cannot survive print" list — the pessimistic assumption §1 was written on. Two rows, and they may be the most load-bearing measurement in the task. Also settled: `window.print()` is a **gesture** row with a minutes-long timeout, because it raises a modal dialog and does not return until dismissed — as an automatic row it would report `timeout` on a working feature, which is L-17's shape exactly. |
| 2026-08-07 | → specified | §1 accepted, with one scope change the owner ruled on. It had scoped in *"one slide per printed page"* — a pre-commitment the only existing implementation contradicts: the reference deck's `@media print` block hides the stage and prints the **reflow document**. §1 assumed pagination, the code assumed document flow, and neither task had ruled. **Ruling: measure both renderings on the same deck and let the printed evidence decide**, rather than settling by assertion which of the two the printable mode uses. It costs one extra stylesheet in a run that happens anyway, and it converts [T-021](T-021-the-reflow-view-and-the-resolution-contract.md)'s open question — *do the reflow view and the print stylesheet share one document rendering?* — from a question T-021 inherits into an acceptance criterion here. Two criteria widened, one added, the size measurement made per-rendering so the choice is priced. Also settled without needing a decision: the print pass takes its gesture by real human click through the existing `ask_for_gesture()`, per R6 §3, and prints through the browser's own dialog rather than a headless renderer — both now written into *Method* so the plan cannot drift into them. §2's steps table still reads as written before this ruling and is the next phase's work. |
| 2026-08-07 | (no change) | `related` gains [T-021](T-021-the-reflow-view-and-the-resolution-contract.md), added by [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md). T-021 carries the open question *do the reflow view and the print stylesheet share one document rendering?* — and it is answerable only with the measurement this task takes. The reference deck's `@media print` block already prints the reflow view, so the two modes are coupled in the only implementation that exists, without either task having ruled that they should be. |
| 2026-08-06 | (no change) | [`examples/reference-deck.html`](../examples/reference-deck.html) now carries a minimal `@media print` block that prints the reflow view rather than the stage. **It has never been printed or measured** — it is a starting point for this task, not a result. |
| 2026-08-06 | → proposed | Created. R6 §9 recorded printing as untested and said so plainly rather than guessing; raised as its own task so the gap cannot be lost. Deliberately **not** blocked on the print mode being specified — the measurement is useful input to that specification, not a consequence of it. |
