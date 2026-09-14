---
id: T-320
title: Remove what the repository says about other projects
type: deliverable
status: done
phase: review
parent: null
blocked_by: []
related: [T-319, T-225, T-299, T-128]
work_package: PH3
shipped_in: unreleased
owner: the project owner
business_value: medium
effort: m
created: 2026-09-15
updated: 2026-09-15
deliverables: [tools/docs/cycles.py, shell/deck.js, docs/DESIGN-SYSTEM.md, tools/deck/check.py]
---

# T-320 — Remove what the repository says about other projects

## 1. Specify

**Outcome**
No tracked file names or describes another project that adopted htmldeck. What such a passage taught
this repository survives, stated without the project it came from.

**Scope**
- In: every tracked file that names an adopter project: the adopter report folder under `docs/`, and
  the documents, tasks, lessons, tools, shell and decks that cite or name them.
- Out: `README.md` and the repository description, which [T-319](T-319-rewrite-the-readme-for-a-reader-choosing-whether-to-install.md) covers.
  Tools the project itself uses, named as tooling. `examples/measure-first/`'s invented client,
  which is fictional and sanitized under the owner's 2026-08-13 exception. Git history.

**Inputs**
- The owner's request, 2026-09-14, recorded in T-319: "if the repository tells info about other
  projects, remove them". Split out of T-319 on the owner's agreement, 2026-09-15, and batched into
  B29 before 1.0.0 by the owner's ruling the same day.

**Acceptance criteria**
- [x] A search for each adopter project's name over tracked files returns nothing.
- [x] Every link into a removed file is rewritten or removed; `python tools/tasks/lint.py` is green.
- [x] `examples/measure-first/` keeps its sanitized content (the owner's 2026-08-13 exception in `CLAUDE.md`).

**Open questions**
- Does a closed task keep an adopter's name in its own record? — decided 2026-09-15: no. A closed
  record is a tracked file a stranger can read, which is the request's test.
- Does this block the 1.0.0 release? — the owner, 2026-09-15: yes, B29 before T-300.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Inventory every tracked mention and every link into the report folder | The file list and the forms the names take |
| 2 | Rewrite by rule: a link keeps its label and loses its target; a path into the folder becomes prose; each name becomes an ordinal label | 49 files |
| 3 | Rename the two task files whose names carried a project name, and delete the report folder | `T-225`, `T-299` renamed |
| 4 | Sync the decks, since `shell/deck.js` carried a name in a comment | `TOOLING.md` §1.14 |
| 5 | Search again, lint, full gate | Criteria 1 and 2 |

## 3. Implement

**Decisions & assumptions**
- Each project name became an ordinal, "the second adopter" or "the third adopter", counted from the adopter whose deck is `measure-first`, so a record still tells two adopters apart. Reversible. — 2026-09-15
- The report folder is deleted, not rewritten: every report was another project's content, and what each one found is already in the task it raised. A link into it keeps its label; a path to it reads "the adopter reports T-320 removed". Reversible from git. — 2026-09-15
- Git history is not rewritten. The repository is public and cloned, and a history rewrite is the owner's call on terms `CLAUDE.md`'s publishing section already set. Not reversible once pushed. — 2026-09-15
- `tools/docs/cycles.py` loses the folder's glob from audit cycle 24, rather than keeping a pattern that matches nothing. Reversible. — 2026-09-15
- Eleven `hard` rows in `docs/DESIGN-SYSTEM.md` changed, so the clause sweep reported each `CHANGED` and every deck gate went red. Each row was re-read as a character diff against `HEAD`: the only change in all eleven is the provenance note (a name to an ordinal, a link to its label), and no statement moved. Their digests in `check.py`'s `SWEPT` were re-recorded on that reading. Reversible. — 2026-09-15

**Outputs produced**
- 49 files rewritten, including `shell/deck.js`, `tools/deck/shell.py` and `tools/deck/quickview.py` comments; `tasks/T-225-triage-the-second-adopters-report.md` and `tasks/T-299-triage-the-third-adopters-report.md` renamed; the report folder removed; decks synced and sizes repasted in `examples/README.md`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| No name in tracked files | pass | `git grep -i` for both names over every tracked file, this record excluded because it has none |
| Links rewritten; lint green | pass | `refcheck.py` 0 broken; lint and full gate run separately after the last edit |
| `measure-first` unchanged in content | pass | Its sources name an invented client; only its shell comments moved with the sync |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-15 | → proposed | Created from T-319's open question, on the owner's agreement. |
| 2026-09-15 | → done | Batched into B29 by the owner; names removed by rule, folder deleted, decks synced. |
