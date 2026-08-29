---
id: T-257
title: Make portfolio-review pass DS-218 for a reason, rather than for having no looping motion
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-225]
work_package: PH1
owner: the project owner
business_value: critical
effort: s
created: 2026-08-29
updated: 2026-08-29
deliverables: []
---

# T-257 — Make portfolio-review pass DS-218 for a reason, rather than for having no looping motion

## 1. Specify

**Outcome**
`examples/portfolio-review/` satisfies `DS-218` because it is measured, not because it has no subject. Today it passes with `0 looping`, so the rule never fires. *This sentence also said the control sits inside the shut menu, which `COMPONENT-CONTRACT.md` called not persistent. Both halves went 2026-08-29: `T-277` put the control back in the menu on every deck and deleted that sentence from the contract. The vacuity is untouched and is the whole of what is left.* **An author reads the example, copies its chrome, and the first looping motion they add fails a rule about motion on a deck whose motion is fine.** Reproduced on this tree: `present: True, 0 looping — pass`.

**From the adopter report** [`018`](../docs/adopter-reports/claimai/018-ds-218-passes-the-shipped-example-only-because-it-has-no-looping-motion.md).

**Scope**
- In: giving the example one looping motion, or moving its control out of the menu
- In: **the verdict saying what is wrong**: when `present: True` and the control is inside a shut menu, the row should read *the control exists but is not persistent*. The contract already has the sentence and the gate does not print it
- In: **whether the menu is genuinely disqualifying** — the adopter's author chose it twice for a clean chrome bar. If a one-click-deep control is acceptable where the menu button itself is persistent and keyboard-reachable, the rule should say so; if not, the example must not model it
- **The third bullet is answered, and not the way this task was scheduled to assume.** The owner reversed the ruling on 2026-08-29 - a control one click inside a persistent, keyboard-reachable menu button **is** reachable, so the menu is not disqualifying and *Motion* goes back inside it on every deck. [T-277](T-277-put-motion-back-inside-the-more-menu.md) carries that, in `B11`, and it amends `DS-218` and `COMPONENT-CONTRACT.md` section 3.4. **What is left here is the example's own defect and nothing about the rule**: `portfolio-review` still passes `DS-218` with `0 looping`, and giving it one looping motion so it passes for a reason is still owed - now for the vacuity alone. **The verdict wording this task owed is spent, not inherited.** It asked the row to read *the control exists but is not persistent* when the control sits inside a shut menu - a state that is now correct, so there is nothing to say about it. `T-277` gave the row the thing this bullet was really after: it prints `motionReach`, the step of the walk that succeeded or failed, so a pass says why it passed. Bullet 2 is closed by that and needs no work here.
- Out: anything the records above do not name. The report is a closed one-way hand-over — there is no
  channel back and none is expected, so a question this task cannot answer is settled here rather
  than asked.

**Inputs**
- the record above, [`018`](../docs/adopter-reports/claimai/018-ds-218-passes-the-shipped-example-only-because-it-has-no-looping-motion.md) — each carries its evidence, its version and its own proposed fix
- **L-57**, the absent-subject class this repository has now met nine times
- [T-231](T-231-two-packaging-checks-have-no-subject-at-all.md) — the same class in the packaging gate, raised by the audit. The general form both want is that an instrument prints its denominator

**Acceptance criteria**
- [ ] every record named above is **closed with its remedy measured**, or explicitly deferred with the
      reason recorded in this task
- [ ] each fix is proved by seeding the defect and watching the check fire, in both directions where
      the record's own evidence is a verdict (**L-125**)
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None yet. Every record carries its own evidence and its own proposed fix; the proposal is a
  hypothesis and whoever implements it measures before committing to it.

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
| 2026-08-29 | (no change) | **Reconciled against [T-277](T-277-put-motion-back-inside-the-more-menu.md), which landed the reversal this record was already carrying a note about.** Two statements here had gone false rather than merely out of date: the outcome cited a `COMPONENT-CONTRACT.md` sentence that `T-277` deleted, and scope bullet 2 asked for verdict wording about a state that is now correct. Both corrected, and **the title with them** - it promised to *say why a control is not persistent*, which is no longer a thing this task can say. `PH1` and the scope are untouched: what is left is the example passing on `0 looping`, which is the vacuity the adopter reported and is unaffected by the ruling. |
| 2026-08-29 | → proposed | Raised by [T-225](T-225-triage-the-claimai-adopter-report.md), the triage of the ClaimAI adopter report. **`PH1`**: a defect an adopter met in the published `0.6.0`, which is `CLAUDE.md`'s one condition for reopening the phase. Verified against this tree before the record was actioned — the report's `Version seen` was stamped rather than re-run on fourteen of the twenty-seven. |
