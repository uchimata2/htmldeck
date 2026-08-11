---
id: T-062
title: Retire the pre-split task tool and repoint what points at it
type: admin
status: done
phase: review
parent: null
blocked_by: []
related: [T-046, T-061]
work_package: PH2
shipped_in: 0.1.2
owner: the project owner
business_value: high
effort: m
created: 2026-08-09
updated: 2026-08-12
deliverables:
  - tools/docs/refcheck.py
  - tasks/TASK-WORKFLOW.md
---

# T-062 — Retire the pre-split task tool and repoint what points at it

## 1. Specify

**Outcome**
`tools/tasks/` is gone, taskmd is the only task tool, and **no gate is lost in the move**. Every live
reference points at something that exists.

**The premise that turned out to be wrong**
The migration brief said *"nothing is lost by deleting it, this was checked, not assumed"*, comparing
the two tools' **commands**: `context`, `index`, `check` have taskmd equivalents, `deliverables`
survives inside taskmd's `check`, and `decisions` is dead code here. All of that is correct.

It compared command names and not **what `check` checks**. Measured against seeded defects in a
throwaway clone:

| Seeded defect | `task.py check` | `taskmd check` |
| :--- | :--- | :--- |
| A markdown link whose target does not exist | BROKEN LINK | BROKEN LINK |
| A dead **bare path in prose** — a `.md` under a real directory, written without link syntax | DEAD POINTER | **not reported** |
| A dead **section reference** — `DESIGN-SYSTEM.md` cited at a section number it has no heading for | DEAD SECTION | **not reported** |

*The three are described rather than written out, because writing one here would make this file carry
the defect it reports. That is the same reason §6.1 treats a mark inside a code span as literal.*

taskmd's link check matches markdown link syntax only, so a path written as prose or printed by a tool is
invisible to it, and it has no notion of `§n` at all. Deleting the tool outright would have dropped
**497 section references and the prose half of 1005 document pointers** out of validation, silently,
which is the exact failure **L-05** and **L-44** are about. It would also have undone
[T-046](T-046-extend-task-py-to-what-it-cannot-see.md) and falsified three live claims: `README.md`
says *"every `<named document> §n` reference in the repository, including the ones on this page"*,
`PUBLISHING.md` §6 leans on it, and **L-39** records it.

**Decided by the owner, 2026-08-09:** keep the checker, drop the task half.

**Scope**
- In: `tools/docs/refcheck.py`, carrying **only** DEAD POINTER, DEAD SECTION and BROKEN LINK, with the
  self-test that already proves the section resolver (**L-04**).
- In: delete `tools/tasks/`. The other six directories under `tools/` survive.
- In: repoint the 16 live references. Task commands go to taskmd; document-reference commands go to
  `refcheck.py`.
- In: **merge `TASK-WORKFLOW.md` with taskmd's METHOD.md** — owner's decision, 2026-08-09: *"Taskmd
  process is a bit more mature, but lacks htmldeck specifics. Try to keep all useful and more
  efficient/up-to-date instructions."* So the document keeps what METHOD.md has no home for and
  points at METHOD.md for the method itself, rather than carrying a second, older copy of it.
- In: repoint the three pointers at the superseded template and delete it.
- Out: **18 closed task records and `.handoff/processed_*`.** A dated account of what was done is not
  kept in step with the present.
- Out: `.claude/settings.local.json`, local machine config.
- Out: taskmd's own defects and gaps. Those go upstream as
  [T-063](T-063-improvements-to-propose-upstream-to-taskmd.md).

**Acceptance criteria**
- [ ] `refcheck.py` reports all three seeded defects, its self-test passes, and it runs from a clean
      clone
- [ ] `tools/` holds exactly `assets`, `deck`, `docs`, `examples`, `kb`, `plugin`, `portability`
- [ ] `grep -rn "tools/tasks/task.py"` returns nothing outside the excluded history
- [ ] `taskmd check` is clean, and the index is not stale
- [ ] `TASK-WORKFLOW.md` carries no rule that METHOD.md now owns, and loses no htmldeck-specific rule
- [ ] Nothing points at the retired template

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Measure the coverage gap against seeded defects rather than trusting the brief | The table in §1 |
| 2 | Extract the reference machinery into `tools/docs/refcheck.py`, self-test included | The tool |
| 3 | Prove it catches all three defects and that its self-test fails when broken | The runs, in §3 |
| 4 | Delete `tools/tasks/`, confirm the six survivors | The listing |
| 5 | Repoint README, LESSONS, PUBLISHING, the template pointer | Four edited documents |
| 6 | Merge `TASK-WORKFLOW.md` against METHOD.md | The rewritten document |
| 7 | Repoint the three template pointers, delete the superseded template | Three edits, one deletion |
| 8 | `taskmd index`, `taskmd check`, `refcheck.py`, and re-derive the README figures | The output of each |

## 3. Implement

**Decisions & assumptions**

- **The coverage gap was measured before anything was deleted — 2026-08-09.** A throwaway clone, two
  seeded defects, both checkers run over it. Had the brief been taken at its word the gates would
  have gone silently, and the first evidence would have been a stale reference nobody caught.

- **`refcheck.py` is the old machinery moved, not rewritten — 2026-08-09.** The regexes, the
  adjacency rule, `points_into_repo`, the `.gitignore` handling and the self-test are carried across
  verbatim. Rewriting them would have re-derived, badly, decisions that took T-046 a whole task to
  reach: adjacency versus proximity was **measured** and proximity picked the wrong target for a
  third of the misses it reported.

- **Its self-test gained two assertions rather than inheriting only the old ones.** A prose pointer
  must match and a bare filename must not, because that is the specific check taskmd lacks and the
  reason this file exists. A tool whose self-test does not cover its reason for existing is the
  L-04 defect one level up.

- **`§` numbering in `TASK-WORKFLOW.md` was preserved through the merge — 2026-08-09.** Twelve task
  records cite it at §2 through §6.2. Renumbering while merging would have silently falsified all
  twelve, and `refcheck.py` would have reported it — the rule catching a change to the document that
  defines the rule. The merge therefore replaces *content* under fixed headings: §3's duplicate
  schema became a pointer to `.taskmd/config.md`, §2 and §4 point at METHOD.md, and §5, §6.1 and
  §6.2 stayed because nothing else owns them.

- **The brief's "leave the closed records alone" could not be satisfied as written — 2026-08-09.**
  It counted 18 records that *mention* the tool, from a grep that cannot tell a mention from a link.
  Two closed records **declared `tools/tasks/task.py` as a deliverable** and two carried **markdown
  links** to it; both fail a check the moment the file goes. The distinction taken: **a prose mention
  is history and was left untouched**, while **a link is a promise a reader can follow** and was
  demoted to a code span. The two declared deliverables were **repointed rather than dropped**,
  because what T-029 and T-046 built is in `refcheck.py` verbatim. Each of the three records carries
  a `(no change)` log row saying so, and T-046's says plainly that its `--closing` leftover check did
  **not** survive.

- **`decisions` was removed from the workflow, not ported — 2026-08-09.** No task here ever carried
  the field and the register was never created, so it was documentation of an unused feature. This
  also cleared the last dead pointer to a file that does not exist.

**Outputs produced**
- `tools/docs/refcheck.py`
- `tasks/TASK-WORKFLOW.md` (merged)
- `README.md`, `CLAUDE.md`, `docs/PUBLISHING.md`, `docs/LESSONS.md`, `.handoff/config.md` (repointed)
- deleted: `tools/tasks/`, and the superseded `task-template.md` under `_templates/`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| `refcheck.py` reports all three seeded defects, self-test passes, runs from a clean clone | **met** | Verified against the seeded clone and the live tree. `--self-test` passes; the resolver rejects §9.4, §0.9 and §11 while accepting §5.1 and §0.8 |
| `tools/` holds exactly the six survivors plus `docs` | **met** | `assets deck docs examples kb plugin portability` — the six named in the brief, plus the new `docs/` |
| The grep returns nothing outside the excluded history | **met** | Returns only `.claude/settings.local.json`, which the brief excludes as local machine config |
| `taskmd check` clean, index not stale | **met** | `OK - 63 task(s), vocabulary valid, references resolve, no broken links` |
| `TASK-WORKFLOW.md` carries no rule METHOD.md owns, loses no htmldeck-specific rule | **met** | §3's schema became a pointer; §2 and §4 point at METHOD.md; §5, §6.1 and §6.2 kept in full. §6.2 is now marked a convention rather than a gate, which is the one thing that genuinely changed |
| Nothing points at the retired template | **met** | `CLAUDE.md`, `.handoff/config.md` and `TASK-WORKFLOW.md` §1 and §7 all point at `tasks/_task-template.md` |

**Child fix tasks raised**
- [T-063](T-063-improvements-to-propose-upstream-to-taskmd.md)

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-09 | → done | **Every gate that existed before still exists, which was the point.** `tools/tasks/` is gone, the six other tool directories are untouched, and the reference checking it carried is `tools/docs/refcheck.py` with its machinery moved verbatim rather than rewritten. `taskmd check` and `refcheck.py` are both clean. The brief's *leave the closed records alone* could not be met as written and the distinction drawn is recorded in §3: a prose mention is history and stayed, a markdown link is a promise and was demoted, and two declared deliverables were repointed because what those tasks built survives in the new file. One capability genuinely did not survive and is written down rather than glossed: the `--closing` leftover-file check, noted in T-046's log and proposed upstream in [T-063](T-063-improvements-to-propose-upstream-to-taskmd.md). |
| 2026-08-09 | → in_progress | Raised for the migration. **The brief's central premise was measured and found wrong**, which changed the task before it started: comparing the two tools' command names says nothing about what their `check` commands cover, and taskmd reports `OK` on a repository carrying a dead bare path and a dead section reference. Owner's decisions, all three taken 2026-08-09: keep the checker and drop the task half; merge `TASK-WORKFLOW.md` with METHOD.md rather than repointing or retiring it; repoint all three template pointers and delete the superseded template. |
