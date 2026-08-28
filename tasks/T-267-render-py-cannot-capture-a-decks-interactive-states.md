---
id: T-267
title: Give render.py a capture path for a deck's disclosed states
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-225]
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-08-29
updated: 2026-08-29
deliverables: []
---

# T-267 — Give render.py a capture path for a deck's disclosed states

## 1. Specify

**Outcome**
A state that exists only after a click can be reviewed by picture. Today `measure`, `shots` and `motion` all capture a slide at rest, and the only element the tool ever presses is `#next` / `#prev`. **So the part of a deck that cannot be printed is also the part that cannot be reviewed by picture** — and the ninth gate condition is a person looking at it.

**From the adopter report** [`016`](../docs/adopter-reports/claimai/016-render-py-cannot-capture-a-decks-interactive-states.md).

**Scope**
- In: pressing a named control, hovering a named target, and opening a named quick view before the capture — each replaces one hand-built workaround with a flag
- In: **hit-testing: capture what is under a point.** It is the half neither workaround reaches and the question an author most wants a picture for
- Out: anything the records above do not name. The report is a closed one-way hand-over — there is no
  channel back and none is expected, so a question this task cannot answer is settled here rather
  than asked.

**Inputs**
- the record above, [`016`](../docs/adopter-reports/claimai/016-render-py-cannot-capture-a-decks-interactive-states.md) — each carries its evidence, its version and its own proposed fix
- the two workarounds the adopter found and their cost — roughly twenty minutes of setup per state, rebuilt from memory each time. **They are why this is a feature rather than a defect**
- what is left after both: no capture of a state *in motion*, because a pane that does not composite freezes a transition at its start value
- [T-260](T-260-ds-244-tests-proximity-where-it-means-obstruction.md) — hit-testing is what would close the gate's own blind spot to overlap

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
| 2026-08-29 | → proposed | Raised by [T-225](T-225-triage-the-claimai-adopter-report.md), the triage of the ClaimAI adopter report. **`PH3`**: not a defect in the published plugin's behaviour, so `CLAUDE.md`'s rule puts it in the main line rather than reopening a shipped phase. |
