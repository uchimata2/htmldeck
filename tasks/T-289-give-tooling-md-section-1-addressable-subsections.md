---
id: T-289
title: Give TOOLING.md section 1 addressable subsections, so a pointer costs one rule and not ten
type: fix
status: proposed
phase: specify
parent: T-287
blocked_by: []
related: [T-285, T-286]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
finding: CE-15
created: 2026-09-02
updated: 2026-09-02
deliverables: []
---

# T-289 — Give TOOLING.md section 1 addressable subsections, so a pointer costs one rule and not ten

## 1. Specify

**Outcome**
`TOOLING.md` §1 is split into numbered subsections, one rule each — the two gates and their order,
the no-edit-while-it-runs rule, `--docs`, the quiet line, the render workers, the bulk-edit rule,
`lint.py` and `query.py`, the board question, `refcheck.py`, `findings.py` — so that a handoff, a
task record or `TASK-WORKFLOW.md` §7 can point at `§1.3` and a resuming session reads one paragraph.
Measured 2026-09-02: §1 is **18,461 of the file's 26,408 bytes**, and the resume read it whole
because the handoff pointed at `§1`. The finding is `CE-15` in
[`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.3.

**Scope**
- In: headings and their numbers; every existing pointer to `§1` re-pointed at the subsection it
  means (`refcheck.py` resolves `§n` references, so a dead one fails the lint); `§1.1` keeps its
  number and content.
- Out: rewording any rule; moving anything out of the file.

**Inputs**
- `TOOLING.md` §1, `../docs/CONTEXT-AUDIT.md` §6.3 `CE-15`

**Acceptance criteria**
- [ ] No subsection of §1 exceeds one rule, and each has a number a pointer can name.
- [ ] Every `§1` pointer in `tasks/`, `docs/` and `.handoff/config.md` names a subsection or is shown to mean the whole.
- [ ] `python tools/docs/refcheck.py` green; the `--docs` gate green.

**Open questions**
- none

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | List the rules §1 holds, one heading each | the subsection list |
| 2 | `grep -rn "§1\b"` across the tree; re-point each | pointers naming a subsection |
| 3 | `refcheck.py`, `--docs` gate | green |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- `TOOLING.md`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-02 | → proposed | Raised by `T-287` from `CE-15`. `PH3`. |
