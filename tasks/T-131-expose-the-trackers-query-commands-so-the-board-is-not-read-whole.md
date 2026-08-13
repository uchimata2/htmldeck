---
id: T-131
title: Expose the tracker's query commands so the board is not read whole
type: deliverable
status: done
phase: review
shipped_in: unreleased
parent: T-130
blocked_by: []
related: [T-130]
work_package: PH3
owner: the project owner
business_value: high
effort: xs
created: 2026-08-13
updated: 2026-08-13
deliverables:
  - tools/tasks/query.py
---

# T-131 — Expose the tracker's query commands so the board is not read whole

## 1. Specify

**Outcome**
A session can ask *what next* and *what does this task point at* with one command, instead of reading
[`README.md`](README.md) whole. **The finding is `CE-02`**, stated in full in
[`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
§8 and ranked first in [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6; it is not restated
here.

**Why it is first on the ranked list**
Measured 2026-08-13: the generated board is **33,676 bytes** and `taskmd list --open` answers the
same question in **1,901** — 17.7× — while `taskmd context T-130` answers one task in **790**. The
hard part is already solved: [`lint.py`](../tools/tasks/lint.py) locates the installed skill by
globbing the version directory, so a plugin update cannot break it silently. This adds an entry
point beside it and changes no data.

**Scope**
- In: a tool exposing at least `list` and `context`, using the same locator as `lint.py`.
- In: [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §6 pointing at it, beside the four commands it already
  states are not what an agent can run.
- In: a line saying an agent asks rather than reads the board.
- Out: changing the generated board, which is for people.
- Out: duplicating the locator. If two files would carry it, it moves to one (**L-13**).
- Out: wrapping `index` or `check` — [`lint.py`](../tools/tasks/lint.py) owns those and chains them.

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6, `CE-02`, and §7.2 `O-T2` — the same
  finding written as an observation for taskmd, whose backlog was read
- [`../tools/tasks/lint.py`](../tools/tasks/lint.py) — the locator, and the precedent for the shape
- [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §6

**Acceptance criteria**
- [ ] One command returns the open board, and one returns a single task's context, from any working
      directory, standard library only (**L-07**)
- [ ] The locator has exactly one home across the repository, and a plugin version bump does not
      break either tool
- [ ] `TASK-WORKFLOW.md` §6 names it where it currently says the bare `taskmd` command does not
      resolve, so a reader meets the answer at the sentence that states the problem
- [ ] Measured after the change: the bytes a session pays to learn what to work on next, against
      33,676
- [ ] `python tools/check_all.py` stays green — a new tool under `tools/` that no manifest table
      names is `UNCLASSIFIED` and **fails the run**, so the manifest entry is part of this task

**Open questions**
- None.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Write `tools/tasks/query.py`. It takes `list` or `context` and passes the rest through to the installed skill, run with the project root as its working directory so it answers from anywhere | The tool |
| 2 | Import the locator from [`lint.py`](../tools/tasks/lint.py) rather than copying it, so it keeps exactly one home (**L-13**) | One `find_taskmd` in the repository |
| 3 | Refuse `index` and `check` by name, pointing at `lint.py`, which chains them. Two entry points that both offer the same command is the second home arriving through the back door | A refusal that names the right tool |
| 4 | Add `tools/tasks/query.py` to `check_all.py`'s `NOT_RUN` with what it is instead. A tracked tool no table names fails the release run | The manifest entry |
| 5 | Measure: bytes to learn what to work on next, before and after, against the 33,676 in §1 | A number in §4 |
| 6 | Point [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §6 at it, at the sentence saying the bare `taskmd` command does not resolve, and say there that an agent asks rather than reads the board | The two lines §1 asks for |

## 3. Implement

**Decisions & assumptions**
- **The locator is imported from [`lint.py`](../tools/tasks/lint.py), and its refusal moved there
  too** — 2026-08-13. `find_taskmd` was already one function; what was not shared was the *"no
  installed skill"* exit, which sat inside `steps()` and would have been retyped here. It is now
  `require_taskmd()` and both entry points call it, so the locating and the refusal have one home
  between them rather than one each (**L-13**).
- **The locator sorted versions as text and was fixed while it had one caller** — 2026-08-13.
  `sorted(glob(...))[-1]` picks `0.5.0` over `0.10.0`, so the next minor bump past `9` would have
  pointed both tools at an older installed skill, silently. Out of the written scope and inside the
  acceptance criterion that says a version bump breaks neither tool; fixed with a numeric key and
  **asserted in `lint.py`'s self-test against three fabricated versions**, because a fixture built
  from the one install present passes while the defect is dormant. Kept as **L-85**.
- **`index` and `check` are refused by name, not merely absent** — 2026-08-13. Leaving them out
  quietly would send the next reader to `python -m taskmd` directly, which is how the chain acquires
  a second home; the refusal names `lint.py` instead.
- **A new tool must be tracked before the release gate can see it.** `check_all.py` discovers through
  `git ls-files`, so an untracked `query.py` reported as **`STALE`** — an entry naming a file that is
  gone — which is the opposite of the truth and reads that way. `git add` fixed it. The rule is
  right: a checker a clone does not receive is a checker no adopter has.

**Outputs produced**
- [`tools/tasks/query.py`](../tools/tasks/query.py) — `list` and `context`, arguments passed through,
  `index` and `check` refused
- [`tools/tasks/lint.py`](../tools/tasks/lint.py) — `version_key`, `require_taskmd`, and the
  self-test assertion for both
- [`tools/check_all.py`](../tools/check_all.py) — the `NOT_RUN` entry
- [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §6 — the two commands, and *an agent asks the board a
  question; it does not read the board*
- [`../docs/LESSONS.md`](../docs/LESSONS.md) — **L-85**

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| One command returns the open board, one returns a single task's context, from any working directory, standard library only | met | Both run, and both were measured from `C:\` rather than from the project root. `os`, `subprocess`, `sys` and the sibling import |
| The locator has exactly one home, and a plugin version bump does not break either tool | met | One `find_taskmd`, reached through `require_taskmd`. The bump half was **not** true when the task started — see §3 and **L-85** — and is now asserted on every invocation of `lint.py`, which is the release run's first gate |
| `TASK-WORKFLOW.md` §6 names it where it says the bare `taskmd` command does not resolve | met | Same paragraph, and the four terminal commands now have two runnable answers covering all four |
| Measured after the change, against 33,676 | met | The board has grown to **36,559** bytes since the audit measured it. Against that: `list --open` **2,451** (14.9×), `context T-131` **716** (51×), and `list --open --limit 1` — the literal *what next* — **94** bytes, **389×**. Exact byte counts of stdout and stderr, taken through `subprocess`, not through the shell |
| `python tools/check_all.py` stays green | met | `0 failure(s), 0 unclassified, 0 stale` over 37 tools and 20 commands. It went red first, correctly, on the untracked file |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-13 | (no change) | **The reason this task exists has been re-attributed, and the deliverable is unaffected.** [T-140](T-140-correct-and-extend-the-upstream-register-from-what-implementing-the-audit-found.md) measured why the bare command does not resolve: taskmd ships a working launcher and the harness does put it on `PATH`, into a shell snapshot whose `PATH` line is truncated mid-value. `query.py` and `lint.py` are right either way — a locator that does not depend on `PATH` is the correct answer to a `PATH` that cannot be relied on — but `CE-02`'s upstream twin `O-T2` was pointing taskmd at somebody else's defect. **L-87.** |
| 2026-08-13 | → done | All five criteria met. **The saving is larger than the audit priced it**: `CE-02` compared the whole board against `list --open`, 17.7×, but the question a session actually asks is *what next*, and `list --open --limit 1` answers that in **94 bytes against 36,559** — 389×. **One thing found on the way was not in scope and is kept as L-85**: the locator sorted version directories as text, so the next minor bump past `9` would have pointed both tools at an older installed skill with nothing to say so. |
| 2026-08-13 | → in_progress | Built in the planned order. The one surprise was the release gate reporting the new tool as `STALE` rather than `UNCLASSIFIED` — discovery is by `git ls-files`, so an untracked file looks like a deleted one; §3 records it. |
| 2026-08-13 | → planned | Six steps. The two that are not obvious: the locator is **imported** from `lint.py` rather than copied, because a second copy is the defect this task's own scope forbids; and `index` and `check` are refused **by name**, since a query tool that also offered them would be that second copy of the chain. |
| 2026-08-13 | → specified | §1 arrived written, with the deliverable declared and no open question, so the specify phase closed on the first read rather than on new work. |
| 2026-08-13 | → proposed | Raised from [T-130](T-130-audit-the-context-economy-of-an-agent-driven-repository.md)'s ranking at the owner's review, first of four. `CE-02`, and the highest measured saving per unit of effort in that audit: 33,676 bytes against 1,901, with no risk and the locating problem already solved by a file that ships. **Its manifest entry in `check_all.py` is inside the task rather than after it** — a tracked tool no table names fails the release run, which is the gate working as designed and a trap if it is met at release time. |
