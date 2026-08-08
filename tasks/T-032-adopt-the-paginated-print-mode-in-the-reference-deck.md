---
id: T-032
title: Adopt the paginated print mode in the reference deck, and decide whether print carries tier two
type: deliverable
status: review
phase: review
parent: null
blocked_by: []
related: [T-018, T-021, T-028, T-016]
work_package: WP2
owner: maintainer
created: 2026-08-07
updated: 2026-08-08
deliverables: [examples/reference-deck.html]
---

# T-032 — Adopt the paginated print mode in the reference deck, and decide whether print carries tier two

## 1. Specify

**Outcome**
`examples/reference-deck.html` prints the **paginated stage** rather than the reading view, and the
owner has ruled on whether print carries the 38.6% of the deck's text that currently sits behind
progressive disclosure.

**Why this one**
[R7](../docs/research/R7-printable-mode.md) ruled that the printable mode is the paginated stage
and that the reading view is not a print target. **The reference deck still does the opposite** —
its committed `@media print` block hides the stage and prints the reading view, which is the
rendering R7 rejected. The deck is the worked example of the ruleset, so it is currently
demonstrating the wrong answer.

The stylesheet that implements the ruling already exists and is proven: `tools/deck/print_variants.py`
emits it, and it was printed and looked at. This task is adoption plus one decision, not authorship.

**The decision this task carries.** R7 §5 records that a printed deck loses everything behind
disclosure — ten panels, 3 543 of 9 177 characters. The affordance is hidden so the paper does not
advertise what it cannot deliver, and R7 states the loss plainly, which satisfies rule 5 as written.
But R7 §2 also measured that **`beforeprint` and `afterprint` fire from `file://`**, so a
*cooperative* printable mode is genuinely available rather than hypothetical:

- expand every panel on `beforeprint`, print each slide's detail on a following page, restore on
  `afterprint`;
- roughly twice the page count, and the printed artifact stops being a handout and becomes a
  document;
- it is **new design work**, which is why R7 raised it here instead of taking it.

**Scope**
- In: replacing the deck's `@media print` block with the paginated one.
- In: the tier-two ruling, and implementing whichever branch the owner takes.
- In: the three rules the paginated rendering depends on, which are general and belong in the
  ruleset, not only in this deck — see *Inputs*.
- Out: the reading view's own pagination. R7 rejected it as a print target; reshaping it is
  precisely the constraint on the design that rule 5 forbids.
- Out: PDF export through a headless renderer.

**Inputs**
- [`docs/research/R7-printable-mode.md`](../docs/research/R7-printable-mode.md) — the ruling, the
  measurements, and §5's list of what print does not preserve.
- [`tools/deck/print_variants.py`](../tools/deck/print_variants.py) — the proven stylesheet, and a
  self-test carrying the three defects that produced blank pages.
- [`T-018`](T-018-measure-the-printable-mode-what-printing-from-fi.md) §3 — the run-by-run record.

**Acceptance criteria**
- [ ] The deck's `@media print` block prints the paginated stage, and the reading view is not the
      print target
- [ ] Printed from a **double-clicked file** through the browser's own dialog, and **looked at**
      (**L-01**) — not headless, which disagreed with the real browser on exactly this (**L-35**)
- [ ] Twelve pages, one slide per page, no blank page at either end
- [ ] The owner's tier-two ruling recorded with its rationale, and implemented
- [ ] The three general rules R7 §4 identified are carried into
      [`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) with IDs, not left only in a research note:
      a print stylesheet asserts the view it wants including `display`; a slide stays a containing
      block for its own overlays; entrance animations are disabled for print
- [ ] What print does not preserve is stated **to the user**, wherever the deck or the plugin
      tells them printing exists

**Open questions**
- ~~Does the deck warn about Chrome's header/footer printing its absolute `file://` path (R7 §5.5)?
  It cannot be fixed from CSS, only warned about. — owner decides.~~ **Answered 2026-08-07 by the
  owner: yes, one line — and it goes where the plugin tells the user printing exists, not on the
  deck.** The warning is real: the path is a machine path, printed on every page, and it is exactly
  the class of data this repository's publishing constraints exclude from anything shared. It stays
  off the deck's own surface because the alternative is print-only chrome on a stage
  [T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) just cut from 96 design
  units to 52, and because the person who needs the warning is the one *about to* print, not the
  one holding the paper. This merges with the last acceptance criterion below — the same sentence
  that states what print does not preserve states this.
- ~~**The decision in this task's title.** Whether print carries tier two.~~ **Answered 2026-08-07
  by the owner: the slides only, with the loss stated.** Print stays the paginated stage as
  [R7](../docs/research/R7-printable-mode.md) ruled it — twelve pages, panels closed, the affordance
  hidden — and the deck says once that the detail behind them is screen-only. **The cooperative
  `beforeprint` expansion is not built.** It was genuinely available rather than hypothetical (R7 §2
  measured both events firing from `file://`), and it was declined on cost against benefit: roughly
  twice the page count, a detail-page layout nobody has designed, and a **second** print rendering
  for [T-005](T-005-build-check-the-gate-the-deck-must-pass.md)'s new print row to gate — against a
  reading view that already carries all of tier two for anyone who wants the whole argument. This is
  rule 5 held to: printing is a mode the user can force on, never a constraint on the design, and
  the cooperative branch is the one that would have started constraining it.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | ~~Take the tier-two decision~~ — **taken 2026-08-07 by the owner, see §1: slides only** | the ruling, recorded in §1 |
| 2 | Replace the deck's `@media print` block with the paginated stylesheet | edited deck |
| 3 | ~~Implement the tier-two branch if the cooperative mode is chosen~~ — **not applicable; the cooperative mode was declined** | — |
| 4 | Print from a double-click, both browsers, and look at every page | printed artefact |
| 5 | Carry the three general rules into the ruleset with IDs | `DESIGN-SYSTEM.md` rules |
| 6 | State the limits where the user is told printing exists | user-facing text |

## 3. Implement

**Decisions & assumptions**
- **The adopted block is the proven stylesheet, with two corrections the deck's own history
  forced** — 2026-08-08. `.progress` was dropped from the hide list, because
  [T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) removed the progress bar
  as a third encoding of position (DS-216) and hiding a class that no longer exists is dead CSS;
  and the `:last-child` comment now says the stage ends with **the chrome nav**, not *"the nav and
  the progress bar"*. **The rule it justifies is unchanged** — `section.slide:last-of-type` is
  still required, confirmed against the live DOM rather than inherited: `.stage > :last-child` is
  `.chrome`, so `:last-child` still would not match the twelfth slide.
- **`print_variants.py` was repaired, not left broken** — 2026-08-08. Adopting the paginated block
  deleted the string its self-test anchored on (`.doc section{break-inside:avoid}`), so the script
  failed its own test the moment the deck changed — an unavoidable consequence of the adoption
  rather than a separate defect. It now anchors on `[hidden]{display:block!important`, the rule the
  rendering lives or dies by, so a failure means *the deck changed* rather than *someone
  reformatted the CSS*. Its docstring no longer says the reflow variant is what the deck does.
- **The three rules went in as DS-222, DS-223 and DS-224 under a new §5.4**, not into §1.1 or §2.4
  — 2026-08-08. Printing is a behaviour of the deck, so it sits beside the reflow view's rules. The
  section states the ruling itself (the printable mode *is* the paginated stage) so the three rules
  have something to be rules *about*.
- **R7 §4's third defect is not one of the three, and it is folded into DS-222 rather than dropped**
  — 2026-08-08. §1's criterion names *assert the view including `display`* · *containing block* ·
  *entrance animations*, while R7's own bullet list names *containing block* · *`:last-child` does
  not match* · *entrance animations*. The criterion won, because the `display` assertion cost two
  printed rounds and R7 records it as the rule the rendering lives or dies by. `:last-child` is a
  **corollary inside DS-222** — both are the same failure, a selector that does not match what its
  author assumed — rather than a fourth ID nobody asked for.
- **The user-facing statement went into `pipeline.md` at handover, because nothing told the user
  printing exists at all** — 2026-08-08. `grep -i print` over `skills/` and `.claude-plugin/`
  returned nothing before this. It is three sentences at stage 7: slides one per page with the
  dialog's layout controls greyed out; disclosure content stays on screen; **turn headers and
  footers off**, which is where the owner's `file://` ruling landed. Not `SKILL.md` — that file is
  under a byte budget and substance belongs in `references/`.

**Outputs produced**
- [`examples/reference-deck.html`](../examples/reference-deck.html) — `@media print` replaced;
  187 409 → 191 533 bytes, **+4.0 KB**, all of it stylesheet and comment.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §5.4 — the ruling plus DS-222, DS-223, DS-224.
- [`skills/htmldeck/references/pipeline.md`](../skills/htmldeck/references/pipeline.md) — *Handing
  it over*, at stage 7.
- [`tools/deck/print_variants.py`](../tools/deck/print_variants.py) — self-test anchor moved.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The deck's `@media print` block prints the paginated stage, and the reading view is not the print target | pass | `.viewport,.viewport[hidden]{display:block!important…}` forces the stage back regardless of which view the deck has decided it is in; `.doc{display:none!important}` takes the reading view out. Verified in the live DOM that **all 10 print selectors match at least one element** — no dead rule in the block. |
| Printed from a **double-clicked file** through the browser's own dialog, and **looked at** (L-01) — not headless | **not yet — owner action** | The only step here that cannot be done from this session: it needs a human double-click and the browser's own dialog, and headless is disqualified on this exact question (**L-35**). Everything checkable without printing was checked (rows above and below). Instructions are in the log row for 2026-08-08. |
| Twelve pages, one slide per page, no blank page at either end | **predicted, not observed** | Structurally verified in the live DOM: **12 `section.slide`**, `section.slide:last-of-type` **is** the twelfth, and `.stage > :last-child` is `.chrome` — so the last slide's `break-after` is cancelled and no thirteenth page should be emitted. T-018's original thirteenth page came from this exact selector. **Counting the pages is the print run's job**, and this row is a prediction until it happens. |
| The owner's tier-two ruling recorded with its rationale, and implemented | pass | Recorded in §1 and in the log; implemented as `.slide .disc{display:none!important}` — panels and control both hidden, so the paper advertises nothing it cannot deliver. The cooperative `beforeprint` expansion is **not** built, as ruled. The deck's own comment states the 38.6% and says the reading view carries it on screen. |
| The three general rules R7 §4 identified are carried into `DESIGN-SYSTEM.md` with IDs | pass | **DS-222** assert the view including `display` (with the `:last-child` corollary), **DS-223** the slide stays a containing block, **DS-224** entrance animations off for print — all `hard` · `render`, in a new **§5.4** that also states the ruling. |
| What print does not preserve is stated **to the user**, wherever the deck or the plugin tells them printing exists | pass | Nothing told them before — `pipeline.md` stage 7 now does, in three sentences, covering the pinned page size, the disclosure loss, and the `file://` header. |

**Gates re-run after the edit:** `audit.py` **0 mechanical failures**; `deliverable_variants.py`
**7 of 7**; `contract_variants.py` **7 of 7**; `check_scaffold.py` **10 of 10 fixtures**, SKILL.md
4 968 of 8 192 bytes; `print_variants.py` self-test **ok** and both variants build.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-08 | → review | **Steps 2, 5 and 6 are done; step 4 — the print run — is the owner's, and it is the only thing between this and `done`.** The deck now carries the paginated block (+4.0 KB), DS-222/223/224 are in a new `DESIGN-SYSTEM.md` §5.4, and `pipeline.md` tells the user at handover what printing does and does not do — **nothing told them before**, so the criterion was not a rewording, it was the first statement of it. Two things the adoption forced and neither was assumed: `.progress` came out of the hide list because T-028 deleted the element, and `print_variants.py` had to be repaired because adoption deleted the string its self-test anchored on. Everything checkable without paper was checked in the live DOM — 12 slides, `:last-of-type` **is** the twelfth, `.stage > :last-child` is `.chrome`, and all 10 print selectors match something. **What that does not settle is the page count**, which is the whole point of L-01 and is why this is `review` and not `done`. **To finish it:** double-click [`examples/reference-deck.html`](../examples/reference-deck.html) — do not open it in a preview pane (**L-15**) — print through the browser's own dialog with headers and footers **off**, save to PDF, and look at every page. Expect **12 pages**, one slide each, backgrounds intact, no disclosure controls, and no blank page at either end. |
| 2026-08-07 | (no change) | **The tier-two decision is taken: the slides only, with the loss stated. §1 now has no open question and the plan lost a step.** The cooperative `beforeprint` expansion is declined — not as impossible, since [R7](../docs/research/R7-printable-mode.md) §2 measured both events firing from `file://`, but on cost: double the pages, a detail-page layout nobody has designed, and a second print rendering for [T-005](T-005-build-check-the-gate-the-deck-must-pass.md)'s print row to gate. **What makes the decline cheap is that nothing is unreachable** — the reading view carries all of tier two, so the 38.6% is not lost, only not on paper. **This task is now pure adoption**: replace the `@media print` block with the proven stylesheet, print it from a double-click and look at every page, carry R7 §4's three rules into the ruleset with IDs, and state the two limits — the disclosure loss and Chrome's `file://` header — in one place where the user is told printing exists. Steps 1 and 3 are struck; steps 2, 4, 5, 6 remain. |
| 2026-08-07 | (no change) | **The `file://` header/footer question is answered: warn, once, where the plugin tells the user printing exists — not on the deck.** It folds into the existing criterion about stating what print does not preserve, so it costs one sentence rather than a print-only element on a stage whose chrome was just halved. The reason it is worth a sentence at all is that the path is **machine data printed on every page**, which this repository excludes from anything shared. **The task's other decision — whether print carries tier two — was not taken today and is now the only thing holding plan step 1.** Every other input it needs has existed since [R7](../docs/research/R7-printable-mode.md) closed. |
| 2026-08-07 | (no change) | **The deck this task prints was rewritten by [T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md), and three of its changes reach the printed page.** (1) **Every slide gained a bottom line** in a fourth grid row anchored to the foot of the slide — on a paginated stage that is the element nearest the page edge, so it is the one a wrong `@page` margin clips first, and it is the element the slide exists to deliver. (2) **The chrome went from two rows to one, and from 96 to 52 design units.** The paginated stylesheet hides the chrome anyway, but T-018's finding that *"the stage ends with the nav and the progress bar, not with a slide"* — the empty thirteenth page — was about a chrome element that **no longer exists**: `.progress` was removed as a third encoding of position under DS-216. Re-measure that page count rather than inheriting it. (3) **Slide 2's timeline labels moved** to fix a collision that T-018 found in print and this task's log had flagged as *"whether it also occurs on screen was not checked"* — it did, and it is fixed at source, so it should not reappear in a printed run. **Verified:** `print_variants.py` still passes its self-test and both variants still build against the rewritten deck. |
| 2026-08-07 | (no change) | **The deck's own view logic changed under this task, and the change makes R7 §3's rule more load-bearing rather than less.** [T-021](T-021-the-reflow-view-and-the-resolution-contract.md) rekeyed auto-engage from `max-width: 959px` to the stage scale factor (**DS-071**), so the deck now hands over to the reading view on **short** viewports too — and printing changes the layout viewport, which is exactly the mechanism that printed thirteen blank pages. A print stylesheet must still *assert* the view it wants, including `display`, and now has more geometries to assert it against. **Verified, not assumed:** `python tools/deck/print_variants.py` still passes its self-test — the one that encodes five defects each costing a printed round — and both variants still build. Nothing here is re-opened; the premise is unchanged and the deck still prints the reading view. |
| 2026-08-07 | → proposed | Raised by [T-018](T-018-measure-the-printable-mode-what-printing-from-fi.md) on closing. R7 ruled the printable mode is the paginated stage; the reference deck still prints the reading view, so the worked example currently demonstrates the rejected rendering. Deliberately **not** blocked on anything: the stylesheet exists and is proven, and the tier-two decision needs only the measurement R7 already took. Separated from [T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) rather than folded into it because the tier-two branch is new design work with a page-count consequence, and burying that inside a retrofit would hide the decision. |
