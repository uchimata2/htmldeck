---
id: T-282
title: The portfolio deck's opening slide carries one of the two figures its specification calls the whole argument
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-233]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-30
updated: 2026-08-30
deliverables: []
---

# T-282 — The portfolio deck's opening slide carries one of the two figures its specification calls the whole argument

## 1. Specify

**Outcome**
`examples/portfolio-review/portfolio-review.html`'s opening slide shows both figures its
specification names. Today it shows **one**.

**What was measured, 2026-08-30, in B12.** `65%` appears **zero** times outside a `<template>` in
the built deck and four times inside one — the `<template>` being the quick view's copy of
`portfolio-model.md`, which is the source document rather than the slide. `52%` appears five times
outside a template. Against that:

- [`portfolio-review.slides.md`](../examples/portfolio-review/portfolio-review.slides.md) slide 1
  specifies *two figures side by side on the content column — `52%` and `65%` — each with a
  four-word label beneath*, and `Pulse-once` on `65%`, *because that is the figure the deck is
  about*;
- its bottom line is specified as *Renewables is 52% of the fund and produced 65% of the year's
  return*, and the foundation's outline table repeats it;
- the foundation's opening paragraph reads *The deck opens on the two figures that are the whole
  argument — a 52% sector share against a 65%…*;
- `portfolio-model.md` agrees: *Renewables is 52% of the fund and produced 65% of the year's
  return. Those two figures are the deck's argument.*

**Why nothing caught it.** `spec.py`'s `SPEC-5` binds a ledger row to the slides its `Used on` cell
names, and the row read `Renewables share of FY26 return | 65% | portfolio-model | 1, 5`. Slide 1 is
front matter and carries no `aria-label="Slide N"`, so `SPEC-5` never saw it; slide 5 **passed on
the dead quick-view payload sitting inside its own `<section>`** — the source document says 65%, and
the rule was reading it. Both halves are now closed:
[T-233](T-233-a-shipped-deck-carries-eleven-copies-of-one-source.md) removed the ten dead payloads
and taught `SPEC-5` to ignore inert `<template>` markup, which is what made this visible.

**Scope**
- In: the opening slide's stat pair, its bottom line, and whatever the addition costs the slide's
  composition
- In: the ledger row, which B12 corrected to `Renewables contribution to FY26 return | +8.1 points |
  5` — what the deck *does* show — and which moves back if the figure lands
- In: the *As built* note beside slide 1 in the slides specification, which is removed when the
  deck matches the wording above it again
- Out: `SPEC-5`'s blindness to front matter. A rule that cannot see an unnumbered slide is a
  separate question and a wider one; this task is the deck
- Out: any other slide

**Inputs**
- [`examples/portfolio-review/portfolio-review.slides.md`](../examples/portfolio-review/portfolio-review.slides.md)
  — slide 1's Structure, Text and Animations lines, which say exactly what to build
- [`examples/portfolio-review/portfolio-review.foundation.md`](../examples/portfolio-review/portfolio-review.foundation.md)
  — the opening paragraph, the ledger and the outline row
- [T-233](T-233-a-shipped-deck-carries-eleven-copies-of-one-source.md) §3 — how it was found

**Acceptance criteria**
- [ ] `65%` is on the opening slide, beside `52%`, with the labels and the `Pulse-once` the
      specification names
- [ ] the ledger row reads the return share again, with a `Used on` naming the slides that show it
- [ ] the *As built* note beside slide 1 is removed, because the deck matches the wording above it
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately
- [ ] the rebuilt opening slide **looked at**, per `CLAUDE.md` rule 6 — two stat figures where one
      stood is a composition change, and a title slide is the one a reader judges first

**Open questions**
- None. The specification says what to build and the source says what the figures are.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <the files this task changed>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- <T-NNN or "none">

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-30 | → proposed | Raised in **B12**, out of [T-233](T-233-a-shipped-deck-carries-eleven-copies-of-one-source.md). Removing ten dead quick-view payloads turned `SPEC-5` red on two ledger rows; one was a wording mismatch and the other was this — a figure the specification, the foundation and the source all call half the deck's argument, which the built deck does not show anywhere a reader can see. **Filed rather than built**, against §4's *absorb what a batch finds*: adding a second stat figure to a title slide is a composition change, and `CLAUDE.md` rule 6 wants a person's eye on it — which §4 forbids an unattended session. B12 corrected the ledger to what the deck does show and recorded the deviation beside slide 1, so nothing is claimed that is not there. |
