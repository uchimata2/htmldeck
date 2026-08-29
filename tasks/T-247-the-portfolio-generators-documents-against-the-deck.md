---
id: T-247
title: Correct the generator's account of a chart it no longer draws and a count stated three ways
type: fix
status: done
phase: review
parent: T-219
blocked_by: []
related: []
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-29
updated: 2026-08-30
deliverables: [tools/examples/portfolio_charts.py]
---

# T-247 — Correct the generator's account of a chart it no longer draws and a count stated three ways

## 1. Specify

**Outcome**
The portfolio generator's documents describe the deck it builds. Today two specifications and the tool's own docstring describe a stacked area chart the deck has not carried since it was re-cut, and the deck carries ten charts where three places say seven.

**Closes** `PR-71`, `PR-72` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: `fig_area`'s docstring and the module docstring in `tools/examples/portfolio_charts.py`, the section banner, and the specification rows that restate them
- In: **nothing else** - every finding this task closes is named above, and each statement stays in the register rather than being restated here (the method's umbrella condition 2)
- Out: any finding not in the list above
- Out: committing to a remedy before measuring it. A remedy is a hypothesis (the method's section 5); a fix that the measurement refuses is reported here and its finding stays open

**Inputs**
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3 - the rows for `PR-71`, `PR-72`
- `examples/portfolio-review/` - the specification pair and the deck itself

**Acceptance criteria**
- [ ] every finding above is **closed with its remedy measured**, or explicitly deferred with the reason recorded on its register row - the method's obligation for `Med`
- [ ] each register row's `Task` cell names this task and its `Status` cell says what happened
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None yet. The register's `Remedy` column carries a hypothesis for each finding, and the method's
  section 5 says it is a hypothesis: whoever implements this measures before committing to it, and
  records what the measurement said.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Measure the count three ways before writing any of them down | `len(FIGURES)` 10, `svg class="fig"` 10, and the ten mapped to slides off their own docstrings |
| 2 | Test the remedy's hypothesis that the self-test already prints the count | it does not — it prints 33, the number of checks |
| 3 | Give the count one home and print it, rather than correcting a second copy of it | `len(FIGURES)` printed; the banner carries no number |
| 4 | Write the deviation **beside** the reviewed wording in both specifications, never instead of it | an *As built* item on slide 4 and in the Visuals row |

## 3. Implement

**Decisions & assumptions**
- **`PR-72`'s hypothesis is refused on the measurement** — 2026-08-30. It reads *`len(FIGURES)` is
  printed by the self-test's own total already*, and it is not: the self-test printed
  `%d of %d checks passed` from `len(ran)`, which is **33**. So the count had no printed home at all,
  and the banner was the only place a reader met a number. The banner now carries **none** and the
  self-test prints `10 figure builder(s) in FIGURES` — which is what the hypothesis was reaching for
  (**L-13**, one home for one quantity), arrived at from the opposite direction.
- **The module docstring's count is an argument and keeps a number** — 2026-08-30. *A deck needs ten
  charts instead of one* is the sentence that justifies the file's length and feeds T-113's
  denominator; removing the number there would remove the argument. Corrected rather than derived.
- **`PR-71`'s direction was taken as the register proposed** — 2026-08-30. A specification is a
  record of what was reviewed, so the reviewed wording stands and the deviation goes **beside** it:
  slide 4 keeps every line and gains an *As built* item, and the foundation's Visuals row keeps its
  seven-chart sentence and gains *As built: ten, and slide 4 is not stacked* with all ten listed.
  Nothing above either note was edited.
- **The module docstring named a chart kind the deck stopped carrying** — 2026-08-30. Its *three
  kinds this file adds to the probe's four* read *stacked area, waterfall and scatter*; the first has
  been five lines since the deck was re-cut. Corrected in the same pass, because it is the same
  sentence's mistake as `PR-71`'s.

**Outputs produced**
- [`tools/examples/portfolio_charts.py`](../tools/examples/portfolio_charts.py) — the module
  docstring, `fig_area`'s docstring, the section banner, and the printed figure count
- [`examples/portfolio-review/portfolio-review.slides.md`](../examples/portfolio-review/portfolio-review.slides.md)
  — slide 4's *As built* item
- [`examples/portfolio-review/portfolio-review.foundation.md`](../examples/portfolio-review/portfolio-review.foundation.md)
  — the Visuals row's *As built* half

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every finding closed with its remedy **measured**, or deferred with the reason on its row | pass | `PR-71` closed on the direction the row proposed; `PR-72` closed with its hypothesis **refused** and the refusing measurement recorded on the row |
| Each register row's `Task` cell names this task and its `Status` cell says what happened | pass | Both rows struck and written |
| `lint.py` and `check_all.py` green, run separately | pass | Run separately, on the batch's tree |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`Med`**, grouped: the owner ruled on 2026-08-29 that a severity obliges a disposition before the release rather than a file count, on the precedent that the method already accepts many findings to one task at `Low`. Every finding keeps its id and its statement in the register. |
| 2026-08-30 | proposed → done | Closed in **B12**. `PR-72`'s hypothesis was **refused on the measurement** — the self-test printed 33 checks, not 10 figures, so the count had no printed home; it has one now and the banner has no number. `PR-71` took the direction the row proposed: the deviation is written beside the reviewed wording, not instead of it. A third error in the same docstring — *stacked area* as a chart kind the deck no longer carries — was corrected with it. |
