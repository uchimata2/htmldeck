---
id: T-238
title: Fix the board header that routes work into a shipped phase, and two silent closures
type: fix
status: done
phase: review
parent: T-219
blocked_by: []
related: []
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-29
updated: 2026-09-02
shipped_in: unreleased
deliverables:
  - tools/tasks/shipped.py
---

# T-238 — Fix the board header that routes work into a shipped phase, and two silent closures

## 1. Specify

**Outcome**
The tracker's own documents agree with `CLAUDE.md`'s phase rule and with themselves. Today the board's hand-written header routes a new task into a shipped phase; the opening checklist's first step names a command an agent cannot run and the substitute refuses it; and [T-221](T-221-answer-the-three-defects-taskmd-0-6-0s-wider-check-set-found.md) and [T-222](T-222-derive-the-reconcile-sweeps-membership-instead-of-enumerating-it.md) are `done` with `shipped_in` **absent** - the third recurrence of a defect written down twice, which nothing gates because the field is deliberately outside the schema's vocabularies.

**Closes** `PR-19`, `PR-20`, `PR-27` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: `tasks/README.md`'s hand-written header, `TASK-WORKFLOW.md` sections 1 and 7, `tools/tasks/query.py`, and the two task records
- In: **nothing else** - every finding this task closes is named above, and each statement stays in the register rather than being restated here (the method's umbrella condition 2)
- Out: any finding not in the list above
- Out: committing to a remedy before measuring it. A remedy is a hypothesis (the method's section 5); a fix that the measurement refuses is reported here and its finding stays open

**Inputs**
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3 - the rows for `PR-19`, `PR-20`, `PR-27`
- `CLAUDE.md`'s phase rule, which the header contradicts
- [T-187](T-187-open-the-motion-vocabulary-into-a-style-guide.md)'s log, which records this same correction being made once already

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
| 1 | Measure all three before deciding — each `Remedy` is a hypothesis | `PR-19` and `PR-20` confirmed as stated; `PR-27` confirmed in kind, refuted in quantity and in where the gate goes |
| 2 | `PR-19` — delete the third copy of the routing rule, point at the two operative homes, then run `taskmd index` and confirm the header survives | `tasks/README.md`'s hand-written header |
| 3 | `PR-20` — decide the two candidates by where the question is asked, not by preference | `query.py next`, and the `index` refusal that names it |
| 4 | `PR-27` — settle whether the gate is upstream from the schema rather than from taste | `shipped_in` is a carried field here, so the rule is this project's; `tools/tasks/shipped.py` |
| 5 | Back-fill every closed record, under `TOOLING.md`'s front-matter rule, and read back | 44 records, `unreleased`, asserted once and in the front matter |
| 6 | Wire the fifth step, and stop the step count decaying in five places | `lint.py` derives its own verdict; four documents delete the number |
| 7 | Close the three rows, write the lesson, run both gates separately | `PRE-RELEASE-AUDIT.md` §3, `L-158`, `L-156`'s second instance |

## 3. Implement

**Decisions & assumptions**
- **`PR-27`'s two records are 44**, and every one of them closed after `0.6.0`, so `unreleased` is the correct value for all of them rather than a placeholder. The reported pair was a sample of a population, which is the second time in this batch — [L-156](../docs/lessons/L-156.md) — 2026-09-02
- **The upstream half of `PR-27`'s hypothesis is refused, and the schema is what refuses it.** `shipped_in` is a **carried** field in this project's own `.taskmd/config.md`, so *a closed task carries it* is this repository's rule and taskmd is right to be silent about it. The gate is local: `tools/tasks/shipped.py`, run as `lint.py`'s fifth step, because the rule says *at close* and `lint.py` is what a close runs — 2026-09-02
- **The step count is derived rather than re-typed.** Adding a fifth step falsified *all four passed* in the tool and *the four checks a task edit owes* in four documents. The tool now counts `steps()`; the documents say *the checks* and name no number — `T-236`'s rule again, and the third time this batch — 2026-09-02
- **`PR-20` is decided by where the question is asked, not by which tool is nearer.** The id is needed **before** the task file exists, and `taskmd index` earns its number by rewriting the board — a write inside a read. So `query.py` answers it locally, and the `index` refusal, which is where somebody asking is standing, points at it — 2026-09-02
- **Scope deviation, recorded rather than glossed.** §1 scoped this to `README.md`, `TASK-WORKFLOW.md`, `query.py` and two task records. The gate `PR-27` asks for lives in `lint.py` and `check_all.py`'s manifest, and the count it falsifies lives in `TOOLING.md` and `.handoff/config.md`. The register's *Where the fix lives* says *and whatever ends up gating it*, and the finding governs — 2026-09-02

**Outputs produced**
- `tools/tasks/shipped.py` — new, `lint.py`'s fifth step, declared in `check_all.py`'s manifest
- [`tools/tasks/query.py`](../tools/tasks/query.py) — `next`, its self-test, and the `index` refusal
- [`tools/tasks/lint.py`](../tools/tasks/lint.py) — the fifth step and a derived verdict
- [`tasks/README.md`](README.md) — the hand-written header
- [`tasks/TASK-WORKFLOW.md`](TASK-WORKFLOW.md) — §1, §6's pointer, §7 steps 1 and 6
- [`tasks/TOOLING.md`](TOOLING.md) — §1's sentence about `lint.py`
- `.handoff/config.md` — `tracker_lint`'s description
- 44 task records — `shipped_in: unreleased`
- [`docs/lessons/L-158.md`](../docs/lessons/L-158.md), [`docs/lessons/L-156.md`](../docs/lessons/L-156.md), and the regenerated index
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) — the three rows closed

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| every finding closed with its remedy measured, or deferred with the reason on its row | met | All three closed. `PR-27`'s remedy changed twice under measurement — two records to 44, and upstream to local — and both changes are on the row |
| each register row's `Task` cell names this task and its `Status` cell says what happened | met | `python tools/docs/findings.py --check` runs inside `lint.py` and exits 0 |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | met | See the log row |

**Child fix tasks raised**
- none. The one thing found beyond the three rows — a step count typed into five places — is a small fix in place under the remediation order's §4, and it is fixed rather than filed.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`Med`**, grouped: the owner ruled on 2026-08-29 that a severity obliges a disposition before the release rather than a file count, on the precedent that the method already accepts many findings to one task at `Low`. Every finding keeps its id and its statement in the register. |
| 2026-09-02 | proposed → done | B19. Three findings closed, one of them against both halves of its stated remedy: `PR-27`'s two records were **44**, and the gate it asks for is this project's rather than taskmd's, because `shipped_in` is a carried field in this repository's own schema. `lint.py` has a fifth step and a verdict that counts its own steps, which is what stops the next one falsifying five documents ([L-158](../docs/lessons/L-158.md)). |
