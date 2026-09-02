---
id: T-291
title: Measure whether the desktop app's skill catalogue can be scoped, and disable what no project uses
type: fix
status: proposed
phase: specify
parent: T-287
blocked_by: []
related: [T-135]
work_package: PH3
owner: the project owner
business_value: medium
effort: xs
finding: CE-17
created: 2026-09-02
updated: 2026-09-02
deliverables: []
---

# T-291 — Measure whether the desktop app's skill catalogue can be scoped, and disable what no project uses

## 1. Specify

**Outcome**
The catalogue of skills a session here is offered on every turn is measured as **60 entries,
15,024 bytes of name and description, about 3,800 estimated tokens per turn**, of which five serve
this repository. Forty-one come from the desktop app's own skill store under the user's roaming
profile and fourteen are the harness's built-ins; `CE-07`'s per-project enabling reached the
`~/.claude` plugins and none of these. This task finds whether the app's store can be scoped or
disabled per skill, does so for what no project on this machine uses, and records the boundary where
it cannot. The finding is `CE-17` in [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.3.

**The change lands outside the repository.** The controller is the user; no clone inherits it. The
task exists so the measurement and the boundary have a home, which is the ecoctx rule for a
user-controlled item.

**Scope**
- In: the app's skill settings; one setting written, one restart, one re-measurement — the ecoctx
  rule, and *two failed attempts is the signal to stop*.
- Out: anything under `~/.claude/plugins`, which `T-135` already scoped; the built-ins.

**Inputs**
- `../docs/CONTEXT-AUDIT.md` §11.1, `CE-17`

**Acceptance criteria**
- [ ] The catalogue re-measured after the change, by the same script, with the before and after figures in §3.
- [ ] Where a skill could not be scoped, the boundary is one line here rather than a retry.

**Open questions**
- none

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Find the app's per-skill or per-project control | the setting, or its absence |
| 2 | Write it, restart, re-measure | the after figure |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- none in the tree

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-02 | → proposed | Raised by `T-287` from `CE-17`. User-controlled; the task holds the measurement. `PH3`. |
