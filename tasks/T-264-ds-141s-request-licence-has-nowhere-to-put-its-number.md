---
id: T-264
title: Give a licensed long motion somewhere to state its duration
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-225]
work_package: PH1
owner: the project owner
business_value: high
effort: s
created: 2026-08-29
updated: 2026-08-29
deliverables: []
---

# T-264 — Give a licensed long motion somewhere to state its duration

## 1. Specify

**Outcome**
An author who is granted `DS-141`'s `request` licence can write the duration they asked for. Today three rules close every route: `DS-013` refuses a theme token the contract does not name, `DS-010` refuses the literal in the slides region, and the only declared dial near the value is Pulse-once's, which [T-198](T-198-give-affordance-motion-its-own-band-faster-than-content-motion.md) already recorded borrowing as a defect. **The licence exists and cannot be used** — the adopter shipped the third route and recorded the deviation.

**From the adopter report** [`005`](../docs/adopter-reports/claimai/005-a-deck-cannot-express-an-author-requested-duration.md).

**Scope**
- In: a per-deck motion band the theme contract names — one duration and one delay token reserved for `--motion-long` rules, unset by default. **This is the better of the two candidates**: it keeps the value where a generator can find it, which is the whole argument `DS-013` rests on
- In: **the asymmetry the record found second**: a custom property holding the same value is exempt from `DS-010` and a literal duration is not. The loophole is open for a delay and shut for a duration, and neither is a decision anyone took
- Out: anything the records above do not name. The report is a closed one-way hand-over — there is no
  channel back and none is expected, so a question this task cannot answer is settled here rather
  than asked.

**Inputs**
- the record above, [`005`](../docs/adopter-reports/claimai/005-a-deck-cannot-express-an-author-requested-duration.md) — each carries its evidence, its version and its own proposed fix
- [T-187](T-187-open-the-motion-vocabulary-into-a-style-guide.md), which created `--motion-long` and its four reason values, `request` among them

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
| 2026-08-29 | → proposed | Raised by [T-225](T-225-triage-the-claimai-adopter-report.md), the triage of the ClaimAI adopter report. **`PH1`**: a defect an adopter met in the published `0.6.0`, which is `CLAUDE.md`'s one condition for reopening the phase. Verified against this tree before the record was actioned — the report's `Version seen` was stamped rather than re-run on fourteen of the twenty-seven. |
