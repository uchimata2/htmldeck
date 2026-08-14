---
id: T-158
title: Measure the tier-1 bound instead of remembering it
type: fix
status: proposed
phase: specify
parent: T-130
blocked_by: []
related: [T-130, T-134, T-143, T-144, T-152, T-153]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-14
updated: 2026-08-14
deliverables: []
---

# T-158 — Measure the tier-1 bound instead of remembering it

## 1. Specify

**Outcome**
The two figures in [`../CLAUDE.md`](../CLAUDE.md)'s tier-1 bound are checked by something that runs on
a trigger this project already has, so a drift is reported rather than discovered by the next session
that happens to re-measure.

**Why it exists**
Raised at [T-153](T-153-run-the-audit-methods-phase-2-over-this-repositorys-own-audit.md)'s review, as
the acceptance criterion that task closed **not met**. `R8` §3.1 step 16 requires phase 2 to leave at
least one thing that re-measures without being asked; phase 2 could not, and the reason is a collision
rather than a difficulty. [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §10.4 is the report.

**The evidence, and it is about this repository's most-paid number.**
- Tier 1 measured **15,034** when T-152 closed and **15,208** hours later. **174 bytes drifted and
  nothing reported it.**
- `CLAUDE.md`'s own debt statement records that it *has now been wrong in both terms twice*.
- `python tools/docs/figures.py` reads both figures as **unanchored** — *in a sentence naming no
  field* — among 413 others. The file carries the measuring command in a fence and pastes no output,
  which is the one shape that tool cannot bind.

**Scope**
- In: a mechanism that compares the stated pair against the measured pair, on an existing trigger —
  `tools/tasks/lint.py` or `tools/check_all.py`, not a new entry point.
- In: **the reporting level.** `CLAUDE.md` is knowingly over its bound, so a check that fails on the
  inequality blocks every release until a debt this project has chosen to carry is paid. What must
  fail is the **stated figure disagreeing with the measured one**, which is a fact about the page and
  not a design choice (`CLAUDE.md`, *a check that forbids a design choice is a defect in the check*).
- In: a self-test on a synthetic fixture, not on the current contents of a tracked file (**L-78**,
  **L-85**) — the fixture rule matters more than usual here, because the subject *is* a tracked file
  whose size this task will change.
- Out: changing the bound, its comparison set, or which document owns the figures. **This task makes
  an existing rule enforceable; it does not re-open it.**
- Out: picking a side in the collision below. That is the open question and it is the owner's.

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §10.4 — the collision, both routes, and why
  neither is takeable without a ruling
- [`../CLAUDE.md`](../CLAUDE.md) *What loads every turn* — the bound, the command, and the rule that a
  figure about that file cannot be corrected anywhere else
- [`../tools/docs/figures.py`](../tools/docs/figures.py) — the mechanism that exists for this shape,
  and the reason it cannot see this instance

**Acceptance criteria**
- [ ] The stated pair is compared against the measured pair on a trigger that already runs
- [ ] A seeded drift in either term fails, in both directions, demonstrated rather than asserted
- [ ] The inequality being unmet does **not** fail anything — only a stated figure disagreeing with the
      measured one does
- [ ] The self-test builds its own instance and does not read the live `CLAUDE.md`
- [ ] `CLAUDE.md`'s byte cost of this change is stated, and it is zero or argued

**Open questions**
- **Which rule yields?** Two routes, each blocked by a rule this project has settled: pasting the
  command's output into `CLAUDE.md` puts new bytes on surface A — the file the audit was cutting —
  while moving the figures out contradicts *a figure about this file cannot be corrected anywhere
  else*. **Recommended: neither — teach `figures.py` to run a fenced command whose output is not
  pasted, and compare against prose in the same document.** That is a change to a tool rather than to
  a policy, it costs tier 1 nothing, and it leaves both rules standing. The alternative is for the
  owner to rule that one of the two rules yields, which is cheaper to implement and spends a
  settled rule. — the owner.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <none yet>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-14 | → proposed | Raised at T-153's review against the one acceptance criterion that closed **not met**: `R8` step 16 requires phase 2 to leave something that re-measures unasked, and it could not. **The blocker is a collision, not a difficulty** — every route is cheap and each is forbidden by a different settled rule, which is **L-100**. The evidence is 174 bytes of undetected drift in the number that governs what every session pays, plus a debt statement that has been wrong in both terms twice, plus `figures.py` reading both figures as unanchored among 413. `s`, `PH3` because PH2 has shipped and this is not a defect in the published plugin. |
