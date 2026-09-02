---
id: T-NNN
title: Audit — <scope>
type: audit
status: proposed
phase: specify
parent: null
blocked_by: []
related: []
work_package: PH3   # the release phase — see ../docs/RELEASE-PHASES.md
owner: the project owner
business_value: critical | high | medium | low
effort: xs | s | m | l | xl
created: YYYY-MM-DD
updated: YYYY-MM-DD
deliverables: []
---

<!--
The method is the taskmd skill's - METHOD.md section 5, audit.md, and pre-release-audit.md for an
audit of everything about to be released. ../docs/AUDIT-METHOD.md is this project's binding only.
Neither is restated here. Fill the four sections below in order; they are the four lifecycle phases
(TASK-WORKFLOW.md section 2). Child fixes are separate task files with `parent:` set to this id.
-->

# T-NNN — Audit: <scope>

## 1. Specify

**Trigger**
<Who asked, when, and in what words. An audit here runs on request and never automatically.>

**Outcome**
<What exists at the end that does not exist now — normally: a register with every finding ranked,
a child task for every High and Medium, and a decision recorded against every Low.>

**Scope**
- In: <which aspects of `docs/AUDIT-METHOD.md` §2, and which surfaces>
- Out: <what this run does not look at, and why>

**Coverage grades** — §1 of the method. State the split for this run and measure it.

| Grade | What it applies to here | Files | Bytes |
| :--- | :--- | ---: | ---: |
| A — wide | | | |
| B — narrow | | | |
| C — instrument only | | | |

**Register**
`<name>.md`, under `docs/` — id space `<XX>-nn`.

**Acceptance criteria**
- [ ] Every tracked file is read, skipped with a stated reason, or produced a finding, and the
      coverage ledger says which.
- [ ] Every finding carries the command that proves it.
- [ ] Every High and Medium finding has a child task; every Low is batched or accepted with a reason.
- [ ] Phase 2 is recorded after the remedies exist.

**Open questions**
- <question — who answers it>

## 2. Plan

**The cycle program.** One subject per cycle, ordered by expected finding density, each sized to
what one session can read and still judge (the skill's `pre-release-audit.md`). A cycle is a
session boundary: it may be run alone.

| # | Subject | Files | Bytes | Brief | Instrument | Status |
| :-- | :--- | :--- | ---: | :--- | :--- | :--- |
| 0 | Prepare the instruments | | | baseline gates green on a frozen tree | `python tools/check_all.py`, `python tools/tasks/lint.py` | pending |
| 1 | | | | | | pending |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Findings raised**
Counts only; the statements live in the register.

| Severity | Raised | Tasked | Accepted | Open |
| :--- | ---: | ---: | ---: | ---: |
| High | | | | |
| Medium | | | | |
| Low | | | | |

**Child tasks raised**
- <T-NNN — PR-nn — one line>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Phase 2**
<Where the grading is recorded, and the one sentence it reduces to.>

**What this run could not see**
- <a limit met in practice, beyond the method's §10 list>

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| YYYY-MM-DD | → proposed | Created. |
