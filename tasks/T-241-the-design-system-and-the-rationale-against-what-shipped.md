---
id: T-241
title: Close three statements the ruleset and its rationale still record as open
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
updated: 2026-09-02
shipped_in: unreleased
deliverables: []
---

# T-241 — Close three statements the ruleset and its rationale still record as open

## 1. Specify

**Outcome**
The ruleset and its rationale describe the product as it is. Today `DESIGN-SYSTEM.md` section 9 records as an open gap the thing the task it cites closed; the rationale records two conflicts as unresolved and one as unowned, both closed by shipped work; and four sections state a coverage count where three carry a re-derive caveat and the fourth - the one with the wrong number - does not.

**Closes** `PR-29`, `PR-97`, `PR-98` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: `DESIGN-SYSTEM.md` section 9's closing paragraph, and `DESIGN-RATIONALE.md` sections 2.2 and 5.8
- In: **nothing else** - every finding this task closes is named above, and each statement stays in the register rather than being restated here (the method's umbrella condition 2)
- Out: any finding not in the list above
- Out: committing to a remedy before measuring it. A remedy is a hypothesis (the method's section 5); a fix that the measurement refuses is reported here and its finding stays open

**Inputs**
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3 - the rows for `PR-29`, `PR-97`, `PR-98`
- the shipped tasks each of the three cites, which are the evidence they are closed

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
| 1 | Measure each remedy before writing it - how many of the nine deliverable-contract rules `EVALUATION.md` actually names, whether the three tasks `§2.2` waits on shipped, and what the `hard` split is today against what `§5.8` states | three readings, recorded in the register's `Status` cells |
| 2 | `PR-29` - keep the half that is about the deck, drop the decayed evidence, and name `T-048` as what **ruled** rather than as what found a gap | `DESIGN-SYSTEM.md` section 9's closing paragraph |
| 3 | `PR-97` - record both resolutions, amend the heading, and rename the column that let the section outlive its work | `DESIGN-RATIONALE.md` section 2.2 |
| 4 | `PR-98` - give the paragraph the caveat its three siblings carry, plus the date its figures belong to | `DESIGN-RATIONALE.md` section 5.8's opening |
| 5 | Close the three register rows and run both gates | `PRE-RELEASE-AUDIT.md` section 3 |

## 3. Implement

**Decisions & assumptions**
- **Each remedy was a hypothesis and was measured first** - the method's section 5. All three held as written, and `PR-97`'s held further than its own remedy asked. 2026-09-02.
- **`PR-29`: no number replaces the wrong one.** The paragraph said *four of the nine*; today seven of the nine appear zero times in `EVALUATION.md`. Writing *seven* would have restored the state that decayed, so the sentence now says being unnamed there **costs those rules nothing** and points at `ruleset.py --gates` for the partition. Same treatment [T-240](T-240-the-evaluation-document-against-itself-and-the-code.md) gave `PR-30` and `PR-32` in this batch. 2026-09-02.
- **`PR-97`: the column is renamed as well as the cells.** The row's own hypothesis is that `State` is why this section outlived its work - a cell designed to say *open* has no unfinished shape - so fixing only the two cells would leave the mechanism in place. The column is `Resolution`, like every other table in the document, and an italic note records the rename. 2026-09-02.
- **`PR-98`: the figures are dated, not refreshed.** They are a historical claim about what forced the ruling; re-deriving them destroys the argument rather than correcting it. `L-95` is the general form and is cited in the paragraph. 2026-09-02.
- **`PR-98`'s `judge` figure stays `PR-30`'s** and is not raised again here - `AM-12`, and the register row says so.

**Outputs produced**
- `docs/DESIGN-SYSTEM.md` - section 9's closing paragraph
- `docs/DESIGN-RATIONALE.md` - section 2.2's heading, preamble, column and both rows; section 5.8's opening
- `docs/PRE-RELEASE-AUDIT.md` - the three rows' `Severity`, `Task` and `Status` cells

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| every finding closed with its remedy measured, or deferred with the reason on its row | **met** | `PR-29`, `PR-97` and `PR-98` closed on their own hypotheses. Nothing deferred, nothing refused |
| each register row's `Task` cell names this task and its `Status` cell says what happened | **met** | rows 112, 180 and 181 of `PRE-RELEASE-AUDIT.md`; severity struck through, as the register does for a dispositioned row |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | **met** | lint: all four passed. **`--docs` refused this diff and was right to**: `docs/DESIGN-SYSTEM.md` is the ruleset the deck gates read, so a verdict that mode would not re-take may have moved. The full gate ran instead |

**Child fix tasks raised**
- none


## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`Med`**, grouped: the owner ruled on 2026-08-29 that a severity obliges a disposition before the release rather than a file count, on the precedent that the method already accepts many findings to one task at `Low`. Every finding keeps its id and its statement in the register. |
| 2026-09-02 | proposed → done | Three findings closed, each remedy measured before it was written and each holding as put. `PR-97` went one step past its remedy and renamed the `State` column to `Resolution`, which is the row's own account of why the section outlived the work that closed it. `PR-29` replaced a stale count with no count. |
