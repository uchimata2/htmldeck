---
id: T-049
title: Reconcile the session memory with what the research settled and the owner last said
type: admin
status: proposed
phase: specify
parent: T-042
blocked_by: []
related: [T-014, T-017]
work_package: none
owner: the project owner
created: 2026-08-09
updated: 2026-08-09
deliverables: []
---

# T-049 — Reconcile the session memory with what the research settled and the owner last said

## 1. Specify

**Outcome**
The four stale or self-contradicting memories are corrected, so a session that reads any one of them
first reaches the same working method as a session that reads them all.

**Why this one**
Memory is loaded at the start of every session and is not read in order. Two entries close on *ask
the owner*; the newest closes on *decide it yourself*; one still lists `file://` restrictions this
project measured and retired. **A memory that is wrong is worse than one that is missing**, because
it is stated with the authority of something the owner said, and nothing in the repository
contradicts it where a session would look.

**Note on where the deliverable lands.** This task's outputs are **outside the repository** —
`~/.claude/projects/C--Work-AgentPlugins-htmldeck/memory/`, which is machine-local and never
published. `deliverables:` is therefore empty by intent rather than by omission, and the review
records what changed instead of a path.

**The four**

| Memory | What is wrong | What it should say |
| :--- | :--- | :--- |
| `research-before-building.md` · `research-may-reshape-the-project.md` | Both close on *the owner answers readily — ask rather than guess*. `decide-detailed-questions-yourself.md`, written 2026-08-09 from the owner's own words (*"pick the right choice for the questions — these are too detailed for me"*), says the opposite and is newer. Neither links to it | The two are not simply wrong — **asking was right during WP1's shaping window and is wrong now**. Each should scope its advice to that window and link `[[decide-detailed-questions-yourself]]` for what replaced it |
| `portability-not-minimalism.md` | Still names *"ES modules, `fetch`, XHR, some worker and WebGL texture paths fail"* as **the gotcha to design around**, and points at T-017 as unfinished | [R6](../docs/research/R6-portability-contract.md) measured 95 rows: the boundary is **fetch-like versus element-like access**, `file://` is a secure context, and **no refused capability costs the deck anything**. `DESIGN-RATIONALE.md` §6 says it in terms — *"Do not design around fears this research retired"* |
| `research-may-reshape-the-project.md` | *"Keep WP2 and WP3 tasks lightly specified until T-014 lands"*; *"expect T-014 to end with a re-scoping proposal"* | T-014 closed 2026-08-06 and all ten WP1 tasks are `done`. The durable half — *findings that contradict the brief are candidate changes of direction* — is still `CLAUDE.md`'s position and is what should survive |
| `one-parametric-theme.md` | *"this sits in tension with the brief's rule 3 ('decks must not look like each other')"* | `CLAUDE.md` rule 3 is now *Use whatever renders best*; one parametric theme is rule 4. The tension was resolved by the rewrite this memory predates |

**Scope**
- In: the four entries above, and `MEMORY.md`'s one-line hooks where a correction changes what the
  entry is for.
- In: linking the pairs that disagree, in both directions. An entry that has been superseded on one
  point and is right on the rest should say which is which, not be deleted.
- Out: writing new memories. This reconciles what is there.
- Out: anything in the repository. Every fact these entries get wrong is already correct in
  `docs/`; the memory is what disagrees.
- Out: `deck-corpus-location.md` and `browserless-instance.md`, which carry a private path and a LAN
  address. Both are correct, both are machine-local by design, and **neither may ever be copied into
  the repository** — noted here so the next audit does not re-raise them as a leak.

**Inputs**
- `~/.claude/projects/C--Work-AgentPlugins-htmldeck/memory/` — the entries and `MEMORY.md`
- [`docs/research/R6-portability-contract.md`](../docs/research/R6-portability-contract.md) §2, §8
- [`docs/DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) §6 — DS-005
- [`CLAUDE.md`](../CLAUDE.md) — the rewritten rules 1–7
- [T-042](T-042-audit-the-whole-repository-against-itself.md) §2, F-8

**Acceptance criteria**
- [ ] No two memories give contradictory instructions on when to ask the owner
- [ ] `portability-not-minimalism.md` states R6's measured boundary, and names what it retired
- [ ] No memory refers to WP1 or T-014 as pending
- [ ] Every superseded claim is corrected **in place with its supersession visible**, not deleted —
      the reason a position changed is the part that stops it coming back
- [ ] `MEMORY.md` has one line per file and no orphan on either side
- [ ] Read cold afterwards: any single entry read alone leads to the same working method

**Open questions**
- none

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <machine-local; recorded here rather than as a repository path>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-09 | → proposed | Raised by [T-042](T-042-audit-the-whole-repository-against-itself.md), finding F-8. **Four entries, and the contradiction is the one that matters**: two memories say *ask the owner*, the newest says *decide it yourself from the rule's own reason*, and memory is not read in order — so which instruction a session follows depends on which file it reads first. One memory also still carries the `file://` fears R6 retired, against a rationale that says in terms not to design around them. The deliverable is machine-local, which is why `deliverables:` is empty by intent; the review records what changed. |
