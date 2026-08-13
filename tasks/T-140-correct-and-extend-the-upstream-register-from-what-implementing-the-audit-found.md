---
id: T-140
title: Correct and extend the upstream register from what implementing the audit found
type: fix
status: done
phase: review
shipped_in: unreleased
parent: null
blocked_by: []
related: [T-130, T-131, T-139]
work_package: PH3
owner: the project owner
business_value: high
effort: s
created: 2026-08-13
updated: 2026-08-13
deliverables:
  - docs/CONTEXT-AUDIT.md
  - docs/LESSONS.md
---

# T-140 — Correct and extend the upstream register from what implementing the audit found

## 1. Specify

**Outcome**
[`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §7 carries everything the implementing
sessions saw that belongs to somebody else — **including one row that is currently wrong about whose
defect it is** — so the register can be handed over as it stands.

**Why now**
§7 was written from the audit alone. Four of its findings have since been implemented
([T-131](T-131-expose-the-trackers-query-commands-so-the-board-is-not-read-whole.md),
[T-132](T-132-give-the-deck-gate-a-quiet-mode-for-its-green-run.md),
[T-133](T-133-write-down-that-a-deck-is-never-read-whole.md),
[T-139](T-139-two-rows-in-brief-md-carry-a-cell-the-table-cannot-render.md)), and **building a thing
is a different instrument from auditing it**. Implementing `CE-02` turned up the cause of the symptom
`O-T2` reports, and it is not taskmd's.

**The correction, because it is the reason this task exists**
`O-T2` reports that taskmd's command surface is unreachable in an agent shell and points at *their*
`T-085`, which is about installing the plugin on a fresh machine. Measured 2026-08-13:

- taskmd **ships** `bin/taskmd` and `bin/taskmd.cmd`, and the launcher **works** when invoked
  directly — `sh <cache>/taskmd/0.5.0/bin/taskmd list --open --limit 1` returns the right row, exit 0.
- The harness **does** emit that `bin/` into the shell snapshot's `export PATH`, at entry 47.
- **The snapshot's `PATH` line is 5,551 characters, holds 67 entries, and is cut mid-path with the
  closing quote missing.** The live shell then has 37 entries and **zero** plugin `bin/` directories.
- **20 of the 67 are session-scoped `local-agent-mode-sessions/.../rpm/plugin_<id>/bin` paths**,
  around 200 characters each, which is where the length comes from.
- In PowerShell no plugin `bin/` is present at all, by a different route.

So the symptom is real, the saving is real, and **the owner of the defect is the harness**. Sent as
filed, it asks taskmd to fix an install path that is not broken.

**Scope**
- In: correcting `O-T2` to report the measured cause, and keeping its saving figures current.
- In: a **third subsection for the harness**, since §7 has homes only for the handoff skill and
  taskmd and this belongs to neither.
- In: every other observation the four implementations produced, for both existing owners.
- In: saying, per row, whether the owner's backlog was read for it. The §7 preamble asserts both
  backlogs were read; rows added later have not been checked that way and must not inherit the claim.
- In: a `(no change)` log row on T-131, whose stated reason for existing is re-attributed by this.
- Out: changing anything in `tools/`. `query.py` and `lint.py` are correct either way — a locator
  that does not depend on `PATH` is the right answer to a `PATH` that cannot be relied on.
- Out: ranking, banding or prioritising any observation. §7's own rule, and it is not ours to guess.
- Out: reporting anything to anyone. This produces the register; the handover is a separate act.

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §7 — the register and its preamble
- [`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
  §6 — the byproduct rule: recorded, never ranked, never a `CE-nn`
- The four closed tasks above, and [`../docs/LESSONS.md`](../docs/LESSONS.md) **L-85** and **L-86**

**Acceptance criteria**
- [ ] `O-T2` states the measured cause and no longer directs taskmd at an install-path task
- [ ] Every observation carries an owner, and no observation sits under the wrong one
- [ ] Each row says whether the owner's backlog was read for it, and the preamble no longer claims
      what it cannot claim for the later rows
- [ ] Nothing in §7 is ranked or banded
- [ ] The register is legible to a reader who has never seen this repository — no bare `T-nnn`
      without its owner (**TASK-WORKFLOW §4.1**)

**Open questions**
- None.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Establish the cause before writing anything: run the shipped launcher directly, then read the snapshot the shell sources | Launcher works; `PATH` line truncated at 5,551 chars |
| 2 | Rewrite §7's preamble — two vintages, what *implementation* rows have not been checked against, and why §7.3 exists | A register that does not overclaim |
| 3 | Correct `O-T2`: the measured cause, the current figures, and what is genuinely still taskmd's | The row that had the wrong owner |
| 4 | Add §7.3 and `O-C1`, `O-C2` | A home for the harness |
| 5 | Add `O-T4`, `O-T5`, `O-T6`, `O-H4`, `O-H5`, `O-H6`; datum rows on `O-T3`, `O-H2`, `O-H3` | Everything the four implementations saw |
| 6 | Repoint the two live statements of the cause — [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §6 and [`query.py`](../tools/tasks/query.py)'s docstring — and log the re-attribution on T-131 | No stale statement of the cause |
| 7 | Keep the general half as **L-87** | The lesson, not the instance |

## 3. Implement

**Decisions & assumptions**
- **The register records everything seen and judges nothing** — 2026-08-13, the owner's direction.
  Three of the nine rows added here would have been dropped under the earlier standard for looking
  marginal or for having no obvious action: `O-T5` (a `--help` that prints the wrong usage), `O-H5`
  (a stale board count in one handoff), `O-C2` (PowerShell, where the mechanism is not even the same).
  Whether an observation is worth acting on is the owner's call, and withholding it makes that call
  for them with less information than they have.
- **Rows are stamped with their vintage instead of the preamble being weakened** — 2026-08-13. §7
  opened by asserting both backlogs were read; rows added after four implementations cannot inherit
  that, and dropping the claim would have thrown away what was true of the audit's own rows. *audit*
  and *implementation* keeps both facts, and tells the reader which rows may already be known to them.
- **§7.3 was added rather than forcing `O-C1` into an existing subsection** — 2026-08-13. The
  register had one subsection per tool this project uses, which assumed every outside defect belongs
  to one of them. `O-C1` had only wrong homes available, and a wrong home is where a wrong owner
  comes from (**L-87**).
- **Nothing in `tools/` changed except a docstring** — 2026-08-13. `query.py` and `lint.py` locate
  the skill themselves and never consult `PATH`, so the correction does not touch them; the docstring
  now names the cause so the next reader does not re-derive it.
- **The measurement is one machine and says so** — 2026-08-13. Windows 11, Git Bash and PowerShell 7.
  Enough to correct an attribution; not enough to characterise the surface, and §7.3 states that
  rather than leaving the reader to infer it (**L-75**).
- **`O-T4` reports a trade this project took the other way**, deliberately. T-139 decided against
  building the equivalent gate here; the row says so, because an observation that hides the reporter's
  own decision is worth less to the person reading it.

**Outputs produced**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §7 — the preamble, the corrected `O-T2`, the
  new §7.3, six new observations and three datum additions
- [`../docs/LESSONS.md`](../docs/LESSONS.md) — **L-87**
- [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §6 and [`../tools/tasks/query.py`](../tools/tasks/query.py)
  — the cause, where it was stated as unknown
- [T-131](T-131-expose-the-trackers-query-commands-so-the-board-is-not-read-whole.md) — a
  `(no change)` log row for the re-attribution

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| `O-T2` states the measured cause and no longer directs taskmd at an install-path task | met | It now names `O-C1` as the cause, drops the pointer to *their* `T-085`, and keeps the one question that is genuinely taskmd's — a documented fallback for *the command is not on `PATH`*, since `bin/taskmd`'s own comment states that mechanism as given |
| Every observation carries an owner, and none sits under the wrong one | met | 3 handoff + 3 new, 3 taskmd + 3 new, 2 harness. The one that was misfiled is the reason §7.3 exists |
| Each row says whether the owner's backlog was read for it, and the preamble no longer overclaims | met | Every row is stamped *audit* or *implementation*; the preamble states that no backlog was re-read for the second kind and tells the reader how to read them |
| Nothing in §7 is ranked or banded | met | No rank, band, effort or priority anywhere in the section, per R8 §6 |
| Legible to a reader who has never seen this repository — no bare `T-nnn` without its owner | met | Foreign ids are written *their* `T-085`, *their* `T-063`, *their* `T-087` (**TASK-WORKFLOW §4.1**); this repository's are markdown links |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-13 | → done | Nine observations added, one corrected, three given a fresh datum, and a third subsection created for an owner the register had no home for. **The correction is the deliverable**: `O-T2` was sending taskmd after a defect in the harness, and it was found only because implementing the fix required chasing the cause the audit had not needed. Kept as **L-87**. The standard changed with it — everything seen is recorded, and whether an observation is worth acting on is the owner's call, not the reporter's. |
| 2026-08-13 | → in_progress | Step 1 changed the task. *Run the launcher directly* took one command and turned an addition into a correction. |
| 2026-08-13 | → planned | Seven steps, and the first is *establish the cause*, because the register cannot be extended honestly while one of its rows is wrong about whose defect it reports. |
| 2026-08-13 | → specified | Specified in one sitting from the four closed implementations and the owner's direction; no open question, because what to record was settled by *record everything* and what to correct was settled by measurement. |
| 2026-08-13 | → proposed | Raised at the owner's direction after four of the audit's findings were implemented: collect everything worth another project's consideration, including the assumptions worth double-checking, and let them decide — the value of an observation is not ours to judge. **It opened with a correction rather than an addition.** Chasing why the bare `taskmd` command does not resolve found a shipped launcher that works, a harness that does put it on `PATH`, and a shell snapshot whose `PATH` line is truncated mid-value — so `O-T2` currently sends taskmd after somebody else's defect. |
