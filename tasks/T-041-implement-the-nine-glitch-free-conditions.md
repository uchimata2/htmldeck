---
id: T-041
title: Implement the nine glitch-free conditions R6 defined and nothing adopted
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-005, T-016, T-019]
work_package: PH3
owner: maintainer
business_value: high
effort: l
created: 2026-08-09
updated: 2026-08-12
deliverables: []
---

# T-041 — Implement the nine glitch-free conditions R6 defined and nothing adopted

## 1. Specify

**Outcome**
`tools/deck/check.py` decides all nine conditions in
[`R6 §8`](../docs/research/R6-portability-contract.md), or names the ones it cannot with a reason,
in the same account that already covers the `DS-nnn` rules.

**Why this one**
**CLAUDE.md rule 2 requires a deck to render glitch-free in recent Chrome/Edge**, and that is a
testable statement only once it is decomposed. R6 §8 decomposed it into nine conditions *"for T-005
to implement"*, [`BRIEF.md`](../docs/BRIEF.md) recorded that assignment — and
**[T-005](T-005-build-check-the-gate-the-deck-must-pass.md)'s own §1 never adopted them.** Its
acceptance criterion says *fails when the deck does not render glitch-free from `file://`* and then
scopes itself, in its own sentence, to the **restricted-origin** class. So the criterion was met as
written and seven of the nine conditions were never anyone's.

**This is L-39 in a new shape and it is worth stating.** Nothing was recorded falsely: R6 proposed,
BRIEF relayed the proposal, and T-005 wrote a narrower criterion. The gap is **between** two
documents that each read correctly on their own, and it survived because no check compares a
research recommendation against the task that inherited it. Found on 2026-08-09 while reconciling
the two at close, not by either.

**Where the nine stand**

| # | Condition | Today |
| :--- | :--- | :--- |
| 1 | Zero external references | **built** — DS-001 |
| 2 | No console errors, no unhandled rejections | **half** — DS-005 and DS-006 catch the restricted-origin causes statically; nothing observes the console. Named as unmet in T-005's own review |
| 3 | Every declared face actually loaded | **not built** — `render.py`'s probe reports `document.fonts.status` and no verdict reads it |
| 4 | No text in a fallback family | **not built** |
| 5 | Nothing overflows its stage | **measured, not gated** — `render.py report()` prints overflow findings; `check.py` emits no verdict |
| 6 | Layout stable after fonts settle | **not built** |
| 7 | Every canvas/WebGL surface drew something | **not built**, and no deck here has a canvas — so it must fail on *nothing measured* rather than pass on it |
| 8 | Every slide reached without a script error | **implicit** — the probe's `goTo` throws if it cannot drive the deck, which reads as NO RESULT; not a named verdict |
| 9 | Looked at, by a person | **not a check and never will be** (**L-01**) — CLAUDE.md rule 6 owns it |

**Scope**
- In: conditions 2 to 8, as verdicts in `check.py`'s existing row shape, each with its own ID —
  these are not `DS-nnn` rules and must not borrow one (**T-038**).
- In: a seeded variant per condition, in `static_variants.py`, since **a check that has never been
  seen to fail is a claim about the instrument** (**L-36**, **L-42**).
- In: condition 9 stated in the output as out of the gate's reach, alongside the five blind
  dimensions already named there.
- Out: **the in-deck capability preflight**, which is
  [T-019](T-019-build-the-capability-preflight-the-deck-ships-wit.md) — that runs inside a shipped
  deck on the recipient's machine; this runs in the harness before it ships. Two different
  instruments answering two different questions, and conflating them is how one gets built twice.
- Out: any new `DS-nnn` rule. R6 §8 is a decomposition of CLAUDE.md rule 2, not new design law.

**Inputs**
- [`R6 §8`](../docs/research/R6-portability-contract.md) — the nine, with how each is tested
- [`tools/deck/check.py`](../tools/deck/check.py) — the account, and where a non-`DS` ID already
  lives (`FIG-1` to `FIG-3`, `PRINT-1`, and §7's criterion numbers)
- [`tools/deck/render.py`](../tools/deck/render.py) — the probe already carries the font status and
  the overflow measurement conditions 3 and 5 need

**Acceptance criteria**
- [ ] Each of conditions 2–8 is either a verdict or is excused in writing, in the same account
- [ ] Condition 7 **fails on a deck with no canvas rather than passing** — the subject being absent
      is not the subject being sound
- [ ] Each new verdict has a seeded variant that it catches
- [ ] The reference deck still passes, or the new failure is a real defect and is written down
- [ ] The output names condition 9 as the gate's boundary, not as satisfied

**Open questions**
- ~~**Does the console-error check need a second render, or can the hook ride the existing one?**~~
  **Answered 2026-08-09: the existing one**, as the recommendation stood. The hook must be injected
  in `<head>`, before the deck's own script, so a load-time error is caught; `render.make_probe`
  appends to `</body>` today and needs a second injection point. **That is one change to the
  harness, not a second browser run** — it keeps `EVALUATION.md` §2's one-render-per-stage cost
  model, and it avoids the failure mode a second render introduces: two runs that disagree, where
  the error is real in one and absent in the other and nothing says which reading is the deck's.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <path>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-10 | (specify) | **Estimated `high`/`l`, and moved to `PH3`.** `high` because CLAUDE.md rule 2 is a testable statement only once decomposed, and seven of R6's nine conditions are still nobody's; `l` because each condition needs its own probe, or its own stated reason for not having one, in an account that already partitions 113 rules. `PH3` under the release split set by the owner 2026-08-10, on size. |
| 2026-08-09 | → proposed | **Raised at close, from a gap between two documents that each read correctly alone.** [R6 §8](../docs/research/R6-portability-contract.md) decomposed CLAUDE.md rule 2 into nine testable conditions *"for T-005 to implement"*; [`BRIEF.md`](../docs/BRIEF.md) relayed that; [T-005](T-005-build-check-the-gate-the-deck-must-pass.md)'s §1 wrote a narrower criterion scoped to the restricted-origin class, met it, and closed. **Nothing was recorded falsely and seven conditions were nobody's** — which is the shape worth remembering, because the usual failure is a claim that outran the work and this is the opposite: work that outran nothing, in a corner no one was looking at. Condition 2 is the one T-005 already names as unmet in its own review, so this task inherits a defect that was declared rather than found. |
