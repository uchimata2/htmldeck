---
id: T-294
title: Grade the second context-economy run's bands after its remedies land
type: analysis
status: done
phase: review
parent: T-287
blocked_by: [T-288, T-289, T-290, T-291, T-292, T-293]
related: [T-153]
work_package: PH3
shipped_in: unreleased
owner: the project owner
business_value: medium
effort: s
created: 2026-09-02
updated: 2026-09-14
deliverables: [docs/CONTEXT-AUDIT.md, docs/lessons/L-168.md]
---

# T-294 — Grade the second context-economy run's bands after its remedies land

## 1. Specify

**Outcome**
Phase 2 of [T-287](T-287-audit-what-a-session-pays-per-turn-and-why-it-grows.md), run the way
[T-153](T-153-run-the-audit-methods-phase-2-over-this-repositorys-own-audit.md) ran it for the first
audit and the ecoctx skill's `standing.md` describes: every band in
[`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.3 graded against what its remedy measured,
the remedies priced, and one sentence the pattern reduces to — written into §11.5 there. **Raised
now, blocked on the audit's own repairs**, because a phase that runs later on a trigger nobody
watches is a phase that does not run.

**Scope**
- In: `CE-14` to `CE-22`; the transcript instrument re-run on one later session so the per-turn
  model in §11.2 is graded too, not only the bands.
- Out: a third run.

**Inputs**
- `../docs/CONTEXT-AUDIT.md` §6.3, §11; the closed child tasks' §3 one-line outcomes

**Acceptance criteria**
- [x] Every band has a measured outcome beside it, or the reason none could be taken.
- [x] At least one prediction the measurement refused is named — or the grading was not run honestly.
- [x] The one sentence is written, and §10.2's is either upheld or amended.

**Open questions**
- none

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Collect each child's one-line outcome | the table's measured column |
| 2 | Re-run the transcript instrument on one session after the remedies | the model graded |
| 3 | Write §11.5 | the grading |

## 3. Implement

**Decisions & assumptions**
- The second transcript is this session's, read to its first edit: that is the unit §11 chose, so the model is graded on a like unit. Not reversible. — 2026-09-14
- Each band is graded from its children's §3 and §4 and from its subject re-measured today, with both figures shown where they differ: regrowth is part of the grade. Reversible. — 2026-09-14
- No band is re-classified and §6.3 is left as ranked: `standing.md` step 12 keeps the original and marks the correction beside it. Reversible. — 2026-09-14
- `CE-18` is not re-timed: `T-296`'s pair shares one frozen tree, and a single reading now would compare machines. Reversible. — 2026-09-14
- §10.2's sentence is amended, not upheld: three rows were wrong in the `Finding` cell, so *the inventory was sound* does not survive, while *never about the location* does. §10.2 keeps its text and points at the amendment. Reversible. — 2026-09-14
- Steps 14 and 15 are not run, and step 16 writes no rule. The reasons are in §11.5's step partition. Reversible. — 2026-09-14

**Outputs produced**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §11.5, and one line under §10.2
- [`../docs/lessons/L-168.md`](../docs/lessons/L-168.md)
- [T-287](T-287-audit-what-a-session-pays-per-turn-and-why-it-grows.md) closed, since this was its last open child

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every band has a measured outcome, or the reason none could be taken | met | nine rows in §11.5, each with what its remedy bought and today's figure. `CE-18` gives its reason for not being re-timed, and `CE-22` its reason for not being a band |
| At least one refused prediction named | met | `CE-14`'s effort, `CE-16`'s payback, `CE-17`'s and `CE-18`'s mechanisms, `CE-20`'s count and size, and the model's weighted split |
| The sentence written; §10.2's upheld or amended | met | amended: a finding does not know why the weight is there, and a removal stays removed only where a gate re-measures it |

**Child fix tasks raised**
- none. The memory index, the skill catalogue and the start context have no trigger this repository can wire. §11.5 reports them for the owner as `controller: user`.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-02 | → proposed | Raised by `T-287` as its phase 2, blocked on its six children. `PH3`. |
| 2026-09-14 | → in_progress | B28's last task, in a session of its own so its transcript is its own. All six blockers done. |
| 2026-09-14 | → done | §11.5 written: two bands held as written, three refused, §10.2 amended. L-168. Closes `T-287`. |
