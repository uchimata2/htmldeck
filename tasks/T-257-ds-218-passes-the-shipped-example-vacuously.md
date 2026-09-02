---
id: T-257
title: Make portfolio-review pass DS-218 for a reason, rather than for having no looping motion
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-225]
work_package: PH1
owner: the project owner
business_value: critical
effort: s
created: 2026-08-29
updated: 2026-08-30
shipped_in: unreleased
deliverables: [tools/examples/portfolio_charts.py, examples/portfolio-review/portfolio-review.html]
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

**Where the motion goes, and why there.** The deck has no looping motion and no dashed flow, so
`DS-218` and `DS-140` both go undecided on it - and it already declares `--current-dash` and
`--current-dur` in its theme region and ships the `Motion` control, so it pays for the mechanism
and uses none of it. The one slide that is a flow is **11, *Three tranches, one gate***: an axis
running left to right into a decision node. `.current` goes on its **first segment**, the one that
enters the gate.

**`--motion-subject: live` has to be true, and here it is.** The gate's own label is
`realised vs 4.5%` and the slide's note reads *the committee reviews the realised discount before
tranche two*. What the gate measures **accrues over the interval before it** - so the segment
running into the gate carries something genuinely in flight, and the segment **after** the gate
does not, which is why only one of the two axis lines takes the class. That is also the encoding
(`DS-150`): the gate has an input that accumulates, and the flow is where it accumulates.

The second axis segment, the markers and the rhombus are untouched, so the motion adds nothing to
the slide's design (`DS-243`).

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Put `.current` on `fig_timeline`'s first axis segment in `tools/examples/portfolio_charts.py`, and say in the docstring what it encodes | the builder |
| 2 | Rebuild the deck and confirm `DS-218` reports a non-zero `looping` count and `DS-140` stops reporting `no dashed flow in this deck` | `portfolio-review.html` |
| 3 | Seed the defect in both directions (**L-125**): with the control removed the row must fail, and with it present pass | the measurement, recorded in section 3 |
| 4 | Record the look this owes in [`OWED-LOOKS.md`](../docs/OWED-LOOKS.md) - the session may not look ([`REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) section 4) | a queue row |
| 5 | `python tools/tasks/lint.py` and `python tools/check_all.py`, run separately | two green runs |

## 3. Implement

**Decisions & assumptions**
- **The motion is `Current` on slide 11's first axis segment, and the segment after the gate stays
  plain** - 2026-08-30. The alternative homes were slide 3's limit bar and slide 4's five-line drift
  chart, and both were rejected for the same reason: `.current` animates a stroke dash, and neither
  slide has a stroke whose subject is in flight. Slide 3's overshoot is a fill and slide 4's lines
  are five years of history. Slide 11 is the deck's only flow, and the thing flowing is what the
  gate measures - so the class went on the segment that enters the gate and on nothing else.
- **`--motion-subject: live` is asserted, not inherited, so it had to be true.** It is: the gate's
  label is `realised vs 4.5%` and the slide's note says the committee reviews the realised discount
  before tranche two, so the quantity accrues across the interval the segment draws.
- **The deck already declared `--current-dash` and `--current-dur` and already shipped the `Motion`
  control.** It paid for the whole mechanism and used none of it, which is why this fix is one class
  attribute rather than a theme change.
- **The vacuity reached four rows, not one.** `DS-140` reported *no dashed flow in this deck* and
  `NO SUBJECT`, and `DS-143`'s *the flow stays dashed with motion off* had nothing to measure
  either. Both now read `7px, 6px` on a live probe.

**The measurement - seeded in both directions (L-125)**

The seed is the same in both runs: `id="motion"` renamed so the probe's
`document.getElementById('motion')` finds nothing. What differs is only whether the deck carries a
looping motion.

| Deck under test | `DS-218` row | Verdict |
| :--- | :--- | :---: |
| **Before this fix**, control seeded away | `control reachable while motion runs: False - no control` | **pass** |
| **After this fix**, control seeded away | `control reachable while motion runs: False - no control` | **FAIL** |
| **After this fix**, untouched | `control reachable while motion runs: True - one click inside #...` | pass |

**The first row is the defect, printed.** The rule reported the control absent and passed anyway,
because `len(infinite) == 0 or motionPersistent` short-circuits on the empty first term. The deck
could have shipped with no stop control at all and this gate would have said so and passed it.

**What the rebuild put back, and why it is fixed in the builder** (**L-148**)

The gate came back red on this deck with two failures neither this task nor `T-226` had touched:
`DUPLICATE Portfolio model - 11 templates carry this title`, and `DRIFTED Portfolio model` at word
560 against a source nobody had edited.

**Both are the rebuild reverting work that had been done to the built file.**
[T-233](T-233-a-shipped-deck-carries-eleven-copies-of-one-source.md) removed ten duplicated
quick-view payloads from `portfolio-review.html` on 2026-08-30 and did not change
`tools/examples/portfolio_charts.py`, which writes it - so `provenance()` still emitted a
`<template>` per control and the first rebuild since put all ten back. The drift is the same shape
one level down: the builder rendered the quick view with its own `md_to_html`, and `quickview.py
check` compares against `render`, which emits `<i>` where the builder left `*text*` literal.

**And a third, from a different task, on the next run.** `SPEC-5` then failed on slide 6:
[T-248](T-248-four-content-errors-in-three-shipped-decks.md) had corrected `$131M` to `$102M` in
three places and retitled the disclosure - in the built file - so the rebuild put all four back.
That one had been **looked at and confirmed by the owner** ([`../docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md)
row 8), which is the part worth keeping: an answered look was silently re-opened by a command.

Fixed where the file is produced rather than in the file. `provenance()` now writes one template
per title for the whole deck, and `quick_view()` calls `quickview.render` - so the template the
deck carries is the one the check compares, by construction rather than by two renderers staying in
step. The revaluation figure is now **derived**: `REVALUATION` holds the three lines the disclosure
prints, `REVAL_RENEWABLE` sums the renewables ones, and the self-test asserts it is not the
three-line total - which is what `$131M` was. **The deck fell 410,414 -> 323,085 bytes**, back to
the size `T-233` had bought it; `quickview.py check` reports `2 match, 0 drifted` on 2 carried where
it had reported 12; and the rebuilt deck's visible text now differs from the shipped one in
**nothing** - every hand-landed correction is reproduced by the command that writes the file.

**Outputs produced**
- `tools/examples/portfolio_charts.py` - `fig_timeline` puts `.current` on the first axis segment,
  and its docstring records what the motion encodes and why the second segment does not take it
- `examples/portfolio-review/portfolio-review.html` - rebuilt through the four composed steps
- `tools/examples/portfolio_charts.py` - also `provenance()` and `quick_view()`, which is
  **L-148**: `T-233`'s fix had been made to the built file and the rebuild reverted it
- [`../docs/lessons/L-148.md`](../docs/lessons/L-148.md) - a fix applied to a generated file has a
  half-life, and the gate that finds it is the next rebuild
- [`../docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md) - row 10, the look this owes

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| every record named above is closed with its remedy measured, or explicitly deferred | pass | Adopter report [`018`](../docs/adopter-reports/claimai/018-ds-218-passes-the-shipped-example-only-because-it-has-no-looping-motion.md) is closed. Its remedy was a hypothesis offering two routes; the second - move the control out of the menu - was removed by the owner's reversal ([T-277](T-277-put-motion-back-inside-the-more-menu.md)), so the first was taken and measured |
| each fix is proved by seeding the defect and watching the check fire, in both directions (**L-125**) | pass | The table in section 3. The before/after pair is the proof: the same seed reads `pass` on the shipped deck and `FAIL` on the fixed one |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | pass | Recorded in the log row below |

**What this task did not do, and why it is a separate record**

`DS-218` still returns `pass` rather than `NO SUBJECT` when a deck carries no looping motion, and
the first row of the table above is what that costs. Giving this deck a subject removes the symptom
from **this** deck and leaves the instrument unchanged for every deck an adopter builds -
`DS-140` one line down already reports `NO SUBJECT` on the same absence, so the gate is
inconsistent with itself. That is an instrument change reaching every deck the gate runs on, which
[`../docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) section 4 routes to a task rather
than to a fix in place.

**Child fix tasks raised**
- [T-283](T-283-ds-218-reports-a-pass-where-it-has-no-subject.md)

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | (no change) | **Reconciled against [T-277](T-277-put-motion-back-inside-the-more-menu.md), which landed the reversal this record was already carrying a note about.** Two statements here had gone false rather than merely out of date: the outcome cited a `COMPONENT-CONTRACT.md` sentence that `T-277` deleted, and scope bullet 2 asked for verdict wording about a state that is now correct. Both corrected, and **the title with them** - it promised to *say why a control is not persistent*, which is no longer a thing this task can say. `PH1` and the scope are untouched: what is left is the example passing on `0 looping`, which is the vacuity the adopter reported and is unaffected by the ruling. |
| 2026-08-29 | → proposed | Raised by [T-225](T-225-triage-the-claimai-adopter-report.md), the triage of the ClaimAI adopter report. **`PH1`**: a defect an adopter met in the published `0.6.0`, which is `CLAUDE.md`'s one condition for reopening the phase. Verified against this tree before the record was actioned — the report's `Version seen` was stamped rather than re-run on fourteen of the twenty-seven. |
| 2026-08-30 | proposed → done | **B13.** Two of the three scope bullets were already spent by [T-277](T-277-put-motion-back-inside-the-more-menu.md), so what was left was the vacuity alone. `Current` goes on slide 11's timeline, on the segment entering the gate and on nothing after it. **The vacuity reached four rows, not one** — `DS-218`, `DS-140` and two of `DS-143`'s were all undecided on the same absence, and all four now measure. The seeded pair is the proof and it is exact: the same seed reads **pass** on the deck as `0.6.0` shipped it and **FAIL** on the fixed one. The instrument half went to [T-283](T-283-ds-218-reports-a-pass-where-it-has-no-subject.md). **The rebuild reverted `T-233` and the gate caught it** — fixed in the builder, recorded as **L-148**. One look owed on slide 11. |
