---
id: T-230
title: Derive DS-063's slide sample from the deck instead of fixing it at four indices
type: fix
status: proposed
phase: specify
parent: T-219
blocked_by: []
related: []
work_package: PH1
owner: the project owner
business_value: critical
effort: s
created: 2026-08-29
updated: 2026-08-29
deliverables: []
---

# T-230 — Derive DS-063's slide sample from the deck instead of fixing it at four indices

## 1. Specify

**Outcome**
DS-063 returns a verdict on a deck of any legal length. Today `contract.SAMPLE` is slides 1, 5, 8 and 12 and the probe clamps at the last slide, so **an eight-slide deck measures slide 8 twice**, the duplicate guard correctly refuses the comparison, and the row reports *undecided* while advising a re-run that will recur forever. DS-082's default length is 8-12 and DS-081's floor is 6, so most of the legitimate band loses the rule on every run.

**Closes** `PR-53` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: `contract.SAMPLE`, derived from the deck's own slide count the way `render.py` already reads it and refuses to guess it
- In: **whether a duplicate the sampler caused should read differently from one a dropped render caused** - they need opposite fixes and the message today states only the second
- Out: DS-063's tolerances, which [T-206](T-206-ds-063-gives-a-different-verdict-on-identical-input.md) settled and this must not move

**Inputs**
- `PR-53` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3
- [T-183](T-183-ds-063-failed-once-in-four-full-gate-runs-on-an-unchanged-tree.md) - the duplicate guard and why it exists

**Acceptance criteria**
- [ ] a six-slide and an eight-slide deck both get a **decided** DS-063 verdict, measured
- [ ] a genuinely dropped render still reads `undecided` with its own message, seeded
- [ ] `python tools/check_all.py` green on every shipped deck

**Open questions**
- None yet. The register's `Remedy` column carries a hypothesis for each finding, and the method's
  section 5 says it is a hypothesis: whoever implements this measures before committing to it, and
  records what the measurement said.

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
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`High`**: the method's section 4 gives that level one obligation beyond a child task — *the release does not go out while it is open*. |
