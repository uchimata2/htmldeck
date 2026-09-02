---
id: T-240
title: Correct EVALUATION.md's four internal contradictions and its account of the stage split
type: fix
status: done
phase: review
parent: T-219
blocked_by: []
related: []
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-08-29
updated: 2026-09-02
shipped_in: unreleased
deliverables: []
---

# T-240 — Correct EVALUATION.md's four internal contradictions and its account of the stage split

## 1. Specify

**Outcome**
[`EVALUATION.md`](../docs/EVALUATION.md) describes the evaluation the code implements. Today the hard-judge checklist is sized three different ways and none is today's number; section 3 states an invariant its own paragraph contradicts three lines later; the ruleset figures are stale; **two sections are numbered 6.3 and both are cited**, so a citation landing on the wrong one is indistinguishable from a correct one; and the stage-1/stage-2 split section 2 describes is not the one `audit.py` implements.

**Closes** `PR-30`, `PR-31`, `PR-32`, `PR-33`, `PR-50` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: `EVALUATION.md` sections 1.1, 2, 3, 6's heading sequence and 8.1, and `audit.py`'s opening
- In: **nothing else** - every finding this task closes is named above, and each statement stays in the register rather than being restated here (the method's umbrella condition 2)
- Out: any finding not in the list above
- Out: committing to a remedy before measuring it. A remedy is a hypothesis (the method's section 5); a fix that the measurement refuses is reported here and its finding stays open

**Inputs**
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3 - the rows for `PR-30`, `PR-31`, `PR-32`, `PR-33`, `PR-50`
- `PR-33`'s remedy column, whose hypothesis is that the second section is not a subsection of the loop at all, so a number outside section 6 may be worth more than 6.5 - which only moves the next collision one append along

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
| 1 | Measure every remedy before writing it - the checklist's real size, the five stale cells, the three unlisted rules, the heading sequence and its citations, and `check.static_rows` against the ruleset's `Check` column | five readings, recorded in the register's `Status` cells |
| 2 | `PR-32` - delete the five figures in section 1's table and section 2's stage rows, and name `ruleset.py --counts` under section 1's table | `EVALUATION.md` sections 1 and 2 |
| 3 | `PR-50` - say what each stage decides rather than which `Check` set it covers, and correct `audit.py`'s opening | `EVALUATION.md` section 2, `tools/deck/audit.py` |
| 4 | `PR-30` - delete the three checklist sizes; section 1.1's own *the split is derived, never listed here* applied one line down | `EVALUATION.md` sections 1.1 and 8.1 |
| 5 | `PR-31` - scope section 3's invariant to what this rubric scores, and name the three rules owned elsewhere | `EVALUATION.md` section 3's preamble |
| 6 | `PR-33` - renumber the second `6.3` outside section 6 and move the citations that meant it | `EVALUATION.md` section 9, `T-215`, `RELEASE-PHASES.md` |
| 7 | Close the five register rows and run both gates | `PRE-RELEASE-AUDIT.md` section 3 |

## 3. Implement

**Decisions & assumptions**
- **Every remedy in the register was a hypothesis and each was measured first** - the method's section 5. Four held as written; one held in part. 2026-09-02.
- **`PR-50`: the stage *names* are kept, against the remedy's implication.** Describing the stages by what they need is the fix; renaming them is not. *Auto gate* and *render gate* are the tree's vocabulary in some fifteen files and in two further lines of `EVALUATION.md` itself, and this task's scope is *nothing else*. The names are marked historical where they are defined, and the cells beside them now say what each stage actually decides. 2026-09-02.
- **`PR-33`: section 9 at the end, not section 7 in place.** Renumbering the collision away by inserting a new section 7 would move `EVALUATION.md`'s sections 7 and 8, cited on **53** lines against the moved section's **5**. Counted with `grep -rn` over `docs`, `tasks`, `skills` and the repository root. 2026-09-02.
- **`PR-32` inherits `T-236`'s ruling rather than re-arguing it.** That task closed `PR-12` on 2026-09-01 by deleting figures and pointing at the command; the same treatment is applied to the five cells its scope did not reach.
- **The historical counts in section 1.1's account of what the checklist found are left alone** - *eleven were named nowhere in this document* is a dated record of a past state, not a live figure, and no finding names it.

**Outputs produced**
- `docs/EVALUATION.md` - sections 1, 1.1, 2, 3's preamble, 8.1, and the heading sequence
- `tools/deck/audit.py` - the module docstring's account of the two stages
- `docs/PRE-RELEASE-AUDIT.md` - the five rows' `Severity`, `Task` and `Status` cells
- [T-215](T-215-the-frame-rate-instrument-and-a-number-with-its-machine.md) and [`docs/RELEASE-PHASES.md`](../docs/RELEASE-PHASES.md) - five citations moved to section 9
- [`docs/lessons/L-155.md`](../docs/lessons/L-155.md) and its index row - a resolver proves an id exists, never that it is unique, which is why `refcheck.py` was green on both sixes

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| every finding closed with its remedy measured, or deferred with the reason on its row | **met** | `PR-30`, `PR-31`, `PR-32`, `PR-33` closed on their own hypotheses; `PR-50` closed with the renaming half refused and the reason measured on the row. Nothing deferred |
| each register row's `Task` cell names this task and its `Status` cell says what happened | **met** | rows 113 to 116 and 133 of `PRE-RELEASE-AUDIT.md`; severity struck through as the register does for a dispositioned row |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | **met** | lint: all four passed. **`--docs` refused this diff and was right to**: `tools/deck/audit.py` is a path the skipped gates read, so a verdict that mode would not re-take may have moved. The full gate ran instead - 40 ran, 2 skipped with a reason, 0 failed, 209 s |

**Child fix tasks raised**
- none


## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`Med`**, grouped: the owner ruled on 2026-08-29 that a severity obliges a disposition before the release rather than a file count, on the precedent that the method already accepts many findings to one task at `Low`. Every finding keeps its id and its statement in the register. |
| 2026-09-02 | proposed → done | Five findings closed, each remedy measured before it was written. `PR-50`'s remedy held in part: the stages are described by what they need, and the **names are kept** because they are the tree's vocabulary and this task's scope is *nothing else*. `PR-33` took a number at the end of the document rather than inserting one, on a citation count of 53 against 5. |
