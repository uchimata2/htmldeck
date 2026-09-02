---
id: T-242
title: Reconcile the component and theme contracts with what their checkers read
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
updated: 2026-08-29
shipped_in: unreleased
deliverables: []
---

# T-242 — Reconcile the component and theme contracts with what their checkers read

## 1. Specify

**Outcome**
A contract row states what a checker decides. Today section 2.1 states a check for two of its four sources; the motion-rule table has no completeness half and two rules animate with no row in it; two theme-contract motion tokens are read by nothing tracked and a third names a rule that does not govern it; section 3.2 calls `data-stage` back the one value outside the argument where a second now exists; and `--accent-ink` is four hand-chosen colours across two themes with nothing deriving them.

**Closes** `PR-34`, `PR-35`, `PR-36`, `PR-39`, `PR-77` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: `COMPONENT-CONTRACT.md` sections 2.1, 3.2 and 3.8, `THEME-CONTRACT.md` section 3.6 and its `--accent-ink` row, `tools/deck/component.py`, and the two theme files
- In: **nothing else** - every finding this task closes is named above, and each statement stays in the register rather than being restated here (the method's umbrella condition 2)
- Out: any finding not in the list above
- Out: committing to a remedy before measuring it. A remedy is a hypothesis (the method's section 5); a fix that the measurement refuses is reported here and its finding stays open

**Inputs**
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3 - the rows for `PR-34`, `PR-35`, `PR-36`, `PR-39`, `PR-77`
- `motion_gaps` in [`tools/deck/component.py`](../tools/deck/component.py)
- [T-200](T-200-add-a-lobby-slide-and-count-the-argument-not-the-file.md), which added the second stage value section 3.2 has not caught up with

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
| 1 | `PR-39` first, because it is the one with no code in it | §3.2's sentence reads *two values are not positions*, and the comparison table has a `front` column |
| 2 | `PR-35`: add the two rows, then the direction that would have caught them | `unrowed_motions` in `component.py`, plus §3.8's completeness half in its own words |
| 3 | Run the new direction before trusting the finding's list | **A third instance the finding did not name**: `.ruler[data-dense] .ruler-ring`, animating on `--afford-dur` and `--afford-ease` with no row |
| 4 | `PR-34`: implement the one-line check §2.1 already states | `unstyled_rows` and `print_css`; `at_rule_span` factored out so the print block is matched once |
| 5 | `PR-36`: separate the error from the decision | `--scale-ease`'s cell corrected to its real readers; Turn's two cells say **no shipped component reads it** |
| 6 | `PR-77`: re-measure, then record it beside `PR-36` as the register asks | `var(--accent-ink)` still appears nowhere. Both recorded as one decision in `THEME-CONTRACT.md` §3.6 |
| 7 | Seed both new checks, both ways | Seven assertions in `component.self_test`, including that a rule switching motion **off** is not a motion |

## 3. Implement

**Decisions & assumptions**
- **Three findings closed and two deferred, and the split is error against decision.** 2026-08-29. `PR-34`, `PR-35` and `PR-39` are things the documents say that are not true, and each has one right answer. `PR-36`'s Turn half and `PR-77` are the same question — a documented dial with no surface — and answering it either way is a `DS-000` change: build the component DS-140 names, or retire the tokens and lose a name from its set. The remediation order's standing authority covers amending a rule row, not answering a ninth rule question, so both are **deferred with the reason on their register rows**, which is what the method's `Med` obligation allows.
- **What deferring changed anyway.** 2026-08-29. A deferral that leaves the documents implying a reader is not a deferral, it is a delay with a cost. So both Turn cells now say *no shipped component reads it*, `THEME-CONTRACT.md` §3.6 records the choice and its two options, and `COMPONENT-CONTRACT.md` §5 stops sending an author to `--turn-ease` without saying it is wired to nothing. The two questions are recorded **together and where the decision will be taken**, rather than in two register rows nobody opens — which is what `PR-77`'s own remedy asks for.
- **The reverse motion check found a third instance on its first run**, which is the argument for writing the direction rather than the two rows. `PR-35` named `.arrow-pop marker path` and `.dot-pop circle`; `.ruler[data-dense] .ruler-ring` was animating unrowed and nobody had counted it. Adding the rows without the direction would have bought until the next motion, exactly as the remedy predicted.
- **A rule that switches motion off is not a rule that starts one.** 2026-08-29. The reduced-motion collapse, the preflight and the density gate all declare `animation:none`, and a completeness check that counted them would have demanded rows for three whole families of non-motion. Reading the value rather than the property is what keeps that out, and it is asserted rather than left to hold by luck.
- **`unrowed_motions` reuses `selector_covers`.** A rule the contract's own selector covers — `:where(.slide[data-played]) .pulse` for `.pulse` — is accounted for. The scope rule already existed for the other direction and had to hold in both, or the natural construction would fail the new check while the awkward one passed, which is the defect the adopter's `020` recorded.
- **No look is owed.** Nothing renders differently: two documents state what was already true, and two checks decide what two documents already claimed.

**Outputs produced**
- [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) — §2.1's note and its `print` cell, §3.2's sentence and table, §3.8's four rows and its completeness half, §5's `--turn-ease` clause
- [`docs/THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) — `--scale-ease`'s cell, Turn's two cells, and §3.6's record of the deferred decision
- [`tools/deck/component.py`](../tools/deck/component.py) — `unrowed_motions`, `unstyled_rows`, `print_css`, `at_rule_span`, two verdict rows and seven self-test assertions
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) — `PR-34`, `PR-35`, `PR-39` closed; `PR-36`, `PR-77` deferred with reasons

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every finding closed with its remedy measured, or explicitly deferred with the reason recorded on its register row | pass | `PR-34`, `PR-35`, `PR-39` closed and measured. `PR-36`'s error half fixed and its decision half deferred; `PR-77` deferred beside it. Both deferrals carry the reason and the two options on the row |
| Each register row's `Task` cell names this task and its `Status` cell says what happened | pass | Five rows rewritten; `findings.py --check` green |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | pass | Both run at the end of B7, on a tree nothing was editing |

**Child fix tasks raised**
- [T-273](T-273-the-owed-looks-have-no-queue-to-accumulate-in.md) — raised while closing this batch, not by this task's own findings

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`Med`**, grouped: the owner ruled on 2026-08-29 that a severity obliges a disposition before the release rather than a file count, on the precedent that the method already accepts many findings to one task at `Low`. Every finding keeps its id and its statement in the register. |
| 2026-08-29 | → done | Batch **B7**. Three findings closed and two deferred, the split being error against decision: `PR-36`'s Turn half and `PR-77` are one `DS-000` question and are recorded together where it will be taken. **The reverse motion check found a third unrowed rule on its first run**, which is why the direction was worth writing rather than the two rows the finding named. |
