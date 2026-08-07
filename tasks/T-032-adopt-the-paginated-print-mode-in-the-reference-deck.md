---
id: T-032
title: Adopt the paginated print mode in the reference deck, and decide whether print carries tier two
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-018, T-021, T-028, T-016]
work_package: WP2
owner: maintainer
created: 2026-08-07
updated: 2026-08-07
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
- <decision — rationale — date>

**Outputs produced**
- <path — one line on what it is>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-07 | (no change) | **The tier-two decision is taken: the slides only, with the loss stated. §1 now has no open question and the plan lost a step.** The cooperative `beforeprint` expansion is declined — not as impossible, since [R7](../docs/research/R7-printable-mode.md) §2 measured both events firing from `file://`, but on cost: double the pages, a detail-page layout nobody has designed, and a second print rendering for [T-005](T-005-build-check-the-gate-the-deck-must-pass.md)'s print row to gate. **What makes the decline cheap is that nothing is unreachable** — the reading view carries all of tier two, so the 38.6% is not lost, only not on paper. **This task is now pure adoption**: replace the `@media print` block with the proven stylesheet, print it from a double-click and look at every page, carry R7 §4's three rules into the ruleset with IDs, and state the two limits — the disclosure loss and Chrome's `file://` header — in one place where the user is told printing exists. Steps 1 and 3 are struck; steps 2, 4, 5, 6 remain. |
| 2026-08-07 | (no change) | **The `file://` header/footer question is answered: warn, once, where the plugin tells the user printing exists — not on the deck.** It folds into the existing criterion about stating what print does not preserve, so it costs one sentence rather than a print-only element on a stage whose chrome was just halved. The reason it is worth a sentence at all is that the path is **machine data printed on every page**, which this repository excludes from anything shared. **The task's other decision — whether print carries tier two — was not taken today and is now the only thing holding plan step 1.** Every other input it needs has existed since [R7](../docs/research/R7-printable-mode.md) closed. |
| 2026-08-07 | (no change) | **The deck this task prints was rewritten by [T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md), and three of its changes reach the printed page.** (1) **Every slide gained a bottom line** in a fourth grid row anchored to the foot of the slide — on a paginated stage that is the element nearest the page edge, so it is the one a wrong `@page` margin clips first, and it is the element the slide exists to deliver. (2) **The chrome went from two rows to one, and from 96 to 52 design units.** The paginated stylesheet hides the chrome anyway, but T-018's finding that *"the stage ends with the nav and the progress bar, not with a slide"* — the empty thirteenth page — was about a chrome element that **no longer exists**: `.progress` was removed as a third encoding of position under DS-216. Re-measure that page count rather than inheriting it. (3) **Slide 2's timeline labels moved** to fix a collision that T-018 found in print and this task's log had flagged as *"whether it also occurs on screen was not checked"* — it did, and it is fixed at source, so it should not reappear in a printed run. **Verified:** `print_variants.py` still passes its self-test and both variants still build against the rewritten deck. |
| 2026-08-07 | (no change) | **The deck's own view logic changed under this task, and the change makes R7 §3's rule more load-bearing rather than less.** [T-021](T-021-the-reflow-view-and-the-resolution-contract.md) rekeyed auto-engage from `max-width: 959px` to the stage scale factor (**DS-071**), so the deck now hands over to the reading view on **short** viewports too — and printing changes the layout viewport, which is exactly the mechanism that printed thirteen blank pages. A print stylesheet must still *assert* the view it wants, including `display`, and now has more geometries to assert it against. **Verified, not assumed:** `python tools/deck/print_variants.py` still passes its self-test — the one that encodes five defects each costing a printed round — and both variants still build. Nothing here is re-opened; the premise is unchanged and the deck still prints the reading view. |
| 2026-08-07 | → proposed | Raised by [T-018](T-018-measure-the-printable-mode-what-printing-from-fi.md) on closing. R7 ruled the printable mode is the paginated stage; the reference deck still prints the reading view, so the worked example currently demonstrates the rejected rendering. Deliberately **not** blocked on anything: the stylesheet exists and is proven, and the tier-two decision needs only the measurement R7 already took. Separated from [T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) rather than folded into it because the tier-two branch is new design work with a page-count consequence, and burying that inside a retrofit would hide the decision. |
