---
id: T-018
title: Measure the printable mode — what printing a deck from `file://` actually costs
type: research
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-002, T-005, T-017]
work_package: WP1
owner: maintainer
created: 2026-08-06
updated: 2026-08-06
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
- In: pagination — one slide per printed page, via `@page` size/orientation and break control.
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

**Method**
The same as T-017's, and for the same reason: **test, do not read.** Print behaviour from a
restricted origin is exactly the sort of thing documentation describes for the HTTP case. Extend
the existing probe rather than building a new one, and honour the two prohibitions T-017 paid for —
**no in-tool preview pane** (it fails optimistically, **L-15**) and **no synthetic input** to
produce the gesture, if one turns out to be required.

Print output is inspected by printing **to a file**, not to a device. Nothing in this task should
send anything to a physical printer.

**Acceptance criteria**
- [ ] `window.print()` behaviour from a double-clicked file recorded on Chrome and Edge, with
      versions, and with an explicit statement of whether it needs a user activation
- [ ] Background/colour fidelity recorded, including whether `print-color-adjust: exact` is honoured
- [ ] One-slide-per-page pagination demonstrated on a **real 12-slide deck**, not a toy (**L-02**)
- [ ] The printed result **looked at**, not merely generated (**L-01**)
- [ ] Size cost of the print stylesheet measured, not estimated
- [ ] An explicit list of what the printable mode does **not** preserve, written for the user
- [ ] A ruling: does rule 5 survive as written, or does printing need something from the design
      after all — surfaced as a candidate change of direction if so

**Open questions**
- Does the print path deserve a row in the build check (T-005), or is it out of scope for a gate
  that only runs on the default `portable` mode? — owner decides once the cost is known.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Extend the portability probe with the print rows | probe rows |
| 2 | Run them, Chrome and Edge, offline, clean profile, plus a literal double-click | result set |
| 3 | Build a 12-slide deck with a print stylesheet and print it to a file | printed artefact |
| 4 | Look at the printed output and record what survived and what did not | findings |
| 5 | Measure the stylesheet's size cost | figure |
| 6 | Write the note and rule on rule 5 | `docs/research/R7-printable-mode.md` |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- `docs/research/R7-printable-mode.md`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-06 | (no change) | [`examples/reference-deck.html`](../examples/reference-deck.html) now carries a minimal `@media print` block that prints the reflow view rather than the stage. **It has never been printed or measured** — it is a starting point for this task, not a result. |
| 2026-08-06 | → proposed | Created. R6 §9 recorded printing as untested and said so plainly rather than guessing; raised as its own task so the gap cannot be lost. Deliberately **not** blocked on the print mode being specified — the measurement is useful input to that specification, not a consequence of it. |
