---
id: T-154
title: Bind the measurements that five live documents state in prose
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-056, T-067, T-130, T-151]
work_package: PH3
owner: the project owner
business_value: high
effort: m
created: 2026-08-14
updated: 2026-08-14
deliverables: []
---

# T-154 — Bind the measurements that five live documents state in prose

## 1. Specify

**Outcome**
A measurement stated in prose in a document a stranger or an adopter reads is either **bound to what
produced it**, **written as a dated record**, or **coarsened until it converges** — and the one class
that can be none of those, a figure counting the repository, stops being enforced by a category
(`volatile`) that has never failed and never can.

**Raised 2026-08-14 from a measurement, not from a hunch.**
[`../tools/docs/figures.py`](../tools/docs/figures.py) reports its own coverage of the five documents
it reads beside the `README.md`: **13 claims compared, 420 numerals unanchored** — *in a sentence
naming no field and in no block linking an artifact, so not judged*. Nobody had ever classified the
420. A throwaway scan, written independently of `figures.py` so it would not measure that tool's blind
spot with the tool that has it, put **42 of them in the measurement class**:

| Document | Numerals | Measurements | What it is |
| :--- | ---: | ---: | :--- |
| [`../CLAUDE.md`](../CLAUDE.md) | 40 | **4** | tier 1, loaded every turn |
| [`../docs/BRIEF.md`](../docs/BRIEF.md) | 111 | **16** | the specification, read first |
| [`../docs/EVALUATION.md`](../docs/EVALUATION.md) | 161 | **1** | the scoring contract |
| `skills/htmldeck/references/pipeline.md` | 25 | **1** | **shipped to adopters** |
| `examples/README.md` | 96 | **20** | **public-facing, the worked example** |
| | **433** | **42** | |

**37 of the 42 carry no date**, so they are live claims rather than records. **42 is a floor, not a
total**: the scan's remaining bucket holds rubric scales, corpus history and range statements that
are correctly unwatched, but it also holds measurements whose unit word the classifier did not know.

**Two defects were confirmed before this task was written, and they are different failures.**

**One — a public document disagrees with the gate, and the check passes.** `examples/README.md` says
*"82 of the 113 rules a gate owns are decided, and the other 31 are named with a reason each"*.
`check.py` prints **84 checked, 115 owned**, which the front `README.md` states correctly and
`figures.py` compares green. The `examples/` copy is green because `claimed()` binds the *part of
whole plus remainder* construction and verifies **82 + 31 = 113** — the claim's internal arithmetic,
not its truth. **A page can hold that sentence forever, stale, with every gate green.** That is not a
bug in `figures.py`; the construction binding was a deliberate improvement over binding by vocabulary
(T-068, T-088) and it does what it says. What is missing is the second half: once the shape is
matched, compare the *values*.

**Two — the self-referential figure went wrong for the third time.** `../CLAUDE.md`'s debt statement
read 15,182 against 11,579 while both terms had moved to 15,034 and 11,925 the same day; the session
that moved them recorded the new pair in a task record and not in the file the figure is about. **The
correction then changed the file it measures** and had to be iterated to a fixed point, which only
converged because the replacement had the same number of digits. A figure that is stable only by
coincidence of character count is not maintained, it is lucky.

**Scope**
- In: the 42 measurements, each routed to one of four outcomes — **bound**, **dated record**,
  **coarsened to a monotone claim**, or **deleted**.
- In: **a `floor` comparison mode** in `figures.py` — fails when the actual value drops below the
  stated one, never on growth. It is what makes a repository-counting figure enforceable at all, and
  it retires the `volatile` category rather than living beside it.
- In: **value comparison for `claimed()`**, so a matched *part of whole* shape is checked against the
  command and not only against itself.
- In: the classifier, if it survives its own review — the throwaway found the defects and its
  `other` bucket is not trustworthy enough to ship as a gate without work.
- Out: the deck-quality figures in `examples/README.md` that describe a **specific artifact on a
  date** — 262 KB, 12 slides, 58 rows. Those are records of a shipped file and the artifact binding
  (T-088) already covers the ones that matter.
- Out: rubric scales, ranges and corpus history — `0–4`, `6–16 slides`, `1–3 script tags`. They
  describe decisions and past measurements, not current state, and enforcing them would be wrong.
- Out: task records. 20 of `CE-04`'s 34 occurrences were citations and this project has ruled
  repeatedly that a record is history (**L-96**, `figures.py`'s `DONE_ROW`).
- Out: raising this as a `CE-nn`. The audit's numbering closed at thirteen.

**Inputs**
- `figures.py`'s module docstring — the two-kinds-of-number rule, and why binding by vocabulary was
  rejected at 30 false alarms against 5 true ones. **This task must not reintroduce that.**
- **L-95** — write the decision a figure drives, and let the command print the figure
- **L-96** — a survey is evidence about the day it was taken; re-measure the 42 before acting
- **L-74** — a stored copy must fail loudly in both directions
- [T-056](T-056-humanize-the-human-facing-documents-before-publishing.md) — six stale figures found
  by hand, which is why `figures.py` exists
- [T-067](T-067-the-published-upgrade-instructions-do-not-upgrade.md) §4 — why a figure counting the
  repository has never converged, which is the argument `figures.py`'s `volatile` category rests on

**What specifying must settle**
- **Whether a floor can be stated without weakening the page.** *Over 2,000 pointers, 0 broken* is
  monotone and enforceable; the exact count is neither. The claim that carries the evidence is
  `0 broken` and it never drifts — the count only carries scale.
- **Where the four outcomes are declared.** A per-figure declaration is a hand-kept list, which is
  the failure `check_all.py`'s manifest exists to prevent; the alternative is a rule the shape of the
  sentence decides.
- **Whether the classifier ships.** A gate that classifies 315 numerals as *other* and is right about
  most of them is exactly the instrument that gets believed (`.taskmd/config.md`, *The tasks folder*).

**Acceptance criteria**
- [ ] Both confirmed defects are **seeded as known-answer fixtures first** and the new check is shown
      to fail on each before either is fixed (**L-86**, **L-55**: the exit status proves the seed, the
      message proves the assertion)
- [ ] `examples/README.md`'s claim matches what `check.py` prints, and a wrong value fails the run
- [ ] `figures.py` gains a `floor` mode; the `volatile` category is retired or its remaining members
      are named with why a floor cannot hold them
- [ ] Every one of the 42 has a recorded outcome — bound, dated, coarsened or deleted — and the
      account is a **partition**, so a measurement in none of them fails
- [ ] The re-measure happens at `specify`; the table above is dated and this task may not trust it
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green
- [ ] No figure is enforced that counts the repository without a floor — enforcing a non-convergent
      number is the defect, not the remedy

**Open questions**
- **Is `m` right?** It is `m` if the four outcomes can be decided by the sentence's shape and the two
  `figures.py` changes are small. It is larger if the 42 each need a judgement, which is 42 decisions
  in five documents, two of which ship to other people. — the implementer, at `specify`, after
  re-measuring rather than trusting the table above.
- **Does `pipeline.md`'s single measurement change what an adopter's build does?** It is the only one
  of the five inside the shipped skill, and a wrong number there is a defect in the product rather
  than in the documentation. — the implementer, at `specify`.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <none yet>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-14 | → proposed | Raised at the owner's direction after `figures.py`'s own report — *420 unanchored* — was classified for the first time. **Not a finding**: `CE-nn` closed at thirteen and this is new capability. The measurement found two confirmed defects before the task was written, and they are different failures: a public page disagreeing with the gate while `claimed()` verifies only the claim's internal arithmetic, and `../CLAUDE.md`'s self-referential debt figure wrong in both terms for the third time — corrected here to a fixed point that holds only because the replacement had the same digit count. |
