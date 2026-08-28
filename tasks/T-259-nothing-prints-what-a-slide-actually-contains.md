---
id: T-259
title: Ship a per-slide fact printer, so a specification and its deck stop drifting silently
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-225]
work_package: PH3
owner: the project owner
business_value: high
effort: m
created: 2026-08-29
updated: 2026-08-29
deliverables: []
---

# T-259 — Ship a per-slide fact printer, so a specification and its deck stop drifting silently

## 1. Specify

**Outcome**
A reader can ask what a slide actually contains. Today a deck is built from a specification pair and then edited in place — the supported way to work — and from that moment the specification is a claim about the deck that nothing checks. The adopter swept theirs: **twenty-three of twenty-five entries had drifted**, and `check` was green throughout.

**From the adopter report** [`026`](../docs/adopter-reports/claimai/026-nothing-prints-what-a-slide-actually-contains.md).

**Scope**
- In: the printer: one slide's own answer for every field an entry claims — eyebrow, headline, standfirst, bottom line, drawn labels, body copy, controls, motion classes, quick views and sources. `render.py` already parses the deck for `measure` and `motion`
- In: **making no judgement**, which is what made the adopter's ~250-line version usable: a differ would produce noise on every intentional difference and there are many
- In: **saying in the docs that in-place editing forks the specification.** The workflow is supported and the consequence is not written down
- Out: anything the records above do not name. The report is a closed one-way hand-over — there is no
  channel back and none is expected, so a question this task cannot answer is settled here rather
  than asked.

**Inputs**
- the record above, [`026`](../docs/adopter-reports/claimai/026-nothing-prints-what-a-slide-actually-contains.md) — each carries its evidence, its version and its own proposed fix
- a verdict is **out of scope here** and worth considering only once the printer exists and its shape is known — the record says so and it is right
- `tools/deck/spec.py`, which reads the specification and never holds it against the output

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
