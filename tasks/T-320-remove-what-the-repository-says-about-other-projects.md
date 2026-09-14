---
id: T-320
title: Remove what the repository says about other projects
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-319, T-225, T-128]
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-09-15
updated: 2026-09-15
deliverables: []
---

# T-320 — Remove what the repository says about other projects

## 1. Specify

**Outcome**
No tracked document names or describes another project. What such a passage taught this repository
survives, stated without the project it came from.

**Scope**
- In: every tracked file that names an adopter project, starting with `docs/adopter-reports/claimai/`
  and the documents, tasks and lessons that cite it.
- Out: `README.md` and the repository description, which [T-319](T-319-rewrite-the-readme-for-a-reader-choosing-whether-to-install.md) already covers.
  Tools the project itself uses (`taskmd`, `handoff`) named as tooling.

**Inputs**
- The owner's request, 2026-09-14, recorded in T-319: "if the repository tells info about other
  projects, remove them". Scope split out of T-319 on the owner's agreement, 2026-09-15.

**Acceptance criteria**
- [ ] A search for each adopter project's name over tracked files returns nothing.
- [ ] Every link into a removed file is rewritten or removed; `python tools/tasks/lint.py` is green.
- [ ] `examples/measure-first/` keeps its sanitized content (the owner's 2026-08-13 exception in `CLAUDE.md`).

**Open questions**
- Does a closed task keep an adopter's name in its own record, or is history rewritten too? — the owner.
- Does this block the 1.0.0 release? — the owner.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |

## 3. Implement

**Decisions & assumptions**
- none yet

**Outputs produced**
- none yet

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-15 | → proposed | Created from T-319's open question, on the owner's agreement. |
