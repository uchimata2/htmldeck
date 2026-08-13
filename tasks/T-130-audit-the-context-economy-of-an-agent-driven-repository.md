---
id: T-130
title: Audit the context economy of an agent-driven repository, and rank the savings
type: audit
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-096, T-128]
work_package: PH3
owner: the project owner
business_value: high
effort: l
created: 2026-08-13
updated: 2026-08-13
deliverables:
  - docs/research/R8-context-economy-for-coding-agents.md
  - docs/CONTEXT-AUDIT.md
---

# T-130 — Audit the context economy of an agent-driven repository, and rank the savings

## 1. Specify

**Outcome**
Two documents. **Part 1 is portable**: the external research, the audit *method* as numbered steps,
the ranking rubric, and every finding that applies to any repository worked by a coding agent — it
can be copied into another project and run there without reading part 2. **Part 2 is this
repository**: the same method applied here, with findings ranked and the top of the list ready to
become child tasks. Neither implements anything; the owner reviews the ranking first.

**Why this task exists**
A single task here spends a large share of a session's context before any work happens, and the
share is growing. That is a claim about the *load path* rather than about any one file, and nobody
has ever inventoried it. **The saving is unknown, which is the first thing this fixes** — an audit
that names what is loaded, what is read, what is printed and what is written is worth having even
if it recommends nothing.

**The four answers that set this scope**, given by the owner 2026-08-13:

| Question | Answer |
| :--- | :--- |
| Optimise for what? | **Context runway first** — how long a session runs before compaction. Cost follows from it and is not the ranking axis |
| Is the written record in scope? | **Yes, with single-source-of-truth preserved.** Layering and load-on-demand, never deleting a fact's only home |
| What is the portable half? | **A playbook plus findings** — the method, so another project re-runs it rather than re-deriving it |
| Which surfaces? | **Both, reported separately** — this repository's own workflow, *and* `skills/htmldeck/` as loaded into an adopter's context |

### The four cost surfaces

Generic. Any agent-driven repository has all four, and an audit that skips one will rank the other
three against an unknown denominator.

| | Surface | What it holds | Why it is separate |
| :--- | :--- | :--- | :--- |
| **A** | **The load path** | What enters context without anyone asking — instruction files, the memory index and recalled memories, the handoff, every available skill's description, tool schemas, system reminders | Paid on **every** turn of **every** session, so a saving here compounds against all the others |
| **B** | **The read path** | What a session must read to do one unit of work — the specification, the conventions, the lessons file, the board, the work item, its neighbours, the source it edits | Paid once per session but grows with the project's age, which is the growth the owner is describing |
| **C** | **Tool output** | What commands print back — gate reports, per-row verdict listings, test suites, search results | Paid per invocation, and the only surface where a tool's own default decides the cost |
| **D** | **Write volume** | What a session produces — work-item prose, log rows, commit messages, the reconcile edits a closure owes | Paid twice: once written, and again when the next session reads it as surface B |

**E — workflow and tooling** cuts across all four: when a gate must run rather than may, whether a
suite runs whole or targeted, whether exploration searches or reads, whether read-heavy work is
delegated, and how a session hands over. It is audited as its own section because its findings
change *when* a cost is paid rather than how large it is.

### Method — the playbook, and part 1's core

Numbered because another project follows it verbatim. Steps 1–4 are inventory and are **measured**;
steps 7–9 are the gain and are **estimated** (see *The estimate is a band*).

1. **Inventory the load path (A).** Everything that enters context unasked, with its size. Include
   the instruction files at every scope, the memory index, the handoff, the description block of
   every available skill, and which tool schemas are eager rather than deferred.
2. **Inventory the read path (B)** for one representative unit of work, chosen before the audit
   starts and named in the report. Record what was opened, how much of it was needed, and how much
   was history rather than operative rule.
3. **Inventory tool output (C).** For each gate or command a unit of work runs, the size of what it
   prints on a *green* run — the failing case is rare and its verbosity is usually earned.
4. **Inventory write volume (D)** for the same representative unit.
5. **Research externally.** How practitioners reduce context and token use with coding agents.
   Produce a catalogue of *techniques*, each with what it costs and what it assumes.
6. **Read the local precedent.** Repositories where this owner has already done such work are an
   input the internet cannot supply: they are proof a technique survived contact with this owner's
   way of working. **Patterns, structures and measurements only** — nothing is copied across.
7. **Screen for applicability.** For each technique: adopted, rejected, or deferred. A rejection
   names the constraint it collides with; a deferral names what would close it. **The three are a
   partition and a technique in none of them fails the audit** — a silent fourth category is how
   this repository has twice shipped an account that looked complete.
8. **Estimate gain and effort.** Bands, not numbers.
9. **Rank.** Gain per unit of effort, with risk as a veto rather than a term.
10. **Split.** Every finding is marked *any project* or *this project*, and part 1 is written so it
    stands alone.
11. **Raise child tasks** for the top of the ranked list — at the owner's review, not before.

### The estimate is a band

The owner's instruction is to **estimate the gain, not measure it**, and the reason is that
measuring a saving requires building it. So:

| Band | Meaning |
| :--- | :--- |
| `XL` | removes more than about a third of a session's load-path or read-path cost |
| `L` | roughly a tenth to a third |
| `M` | a few per cent |
| `S` | under a per cent, or unquantifiable but real |

Effort reuses the project's own `xs`–`xl`. **Inventory figures in steps 1–4 are measured and are
stated as measurements**; only the saving is banded. A band with no inventory behind it is a guess
wearing a table, which is the failure **L-04** names.

### The finding record

Operative or it is decoration: every finding carries an ID and enough for a reader to act without
the audit's author present.

| Field | What it holds |
| :--- | :--- |
| `CE-nn` | the ID, stable, cited from child tasks and from the other project that reuses part 1 |
| Surface | A, B, C, D or E |
| Finding | what is costing, stated as a fact about the repository |
| Change | what to do |
| Gain | a band, with the inventory figure it rests on |
| Effort | `xs`–`xl` |
| Risk | what it could cost — a fact losing its only home, a gate weakening, a rule becoming unfindable. `none` is a legitimate value and must be written |
| Applies to | `any` or `this project` |
| Source | external research, local precedent, or this audit |

**Scope**
- In: all four surfaces plus workflow, on **two** subjects reported separately — this repository's
  development workflow, and the plugin as loaded into an adopter's context.
- In: the external research, and the local precedent the owner supplies.
- In: restructuring proposals for the written record — layering, load-on-demand, splitting an
  operative rule from its history — **provided no fact loses its only home**.
- Out: implementing anything. The ranking is reviewed first, and that is the whole point of the
  umbrella.
- Out: measuring a saving by building it.
- Out: anything that weakens a gate, deletes a lesson, or makes a rule harder to find. A finding
  whose gain depends on that is recorded with the risk stated and ranked below everything else.
- Out: the local repositories' contents. They are read; nothing is copied, and **no path, machine
  name or personal datum from them enters this repository** — the publishing constraint in
  [`../CLAUDE.md`](../CLAUDE.md), and **L-81**.

**Inputs**
- [`../CLAUDE.md`](../CLAUDE.md) — the working rules, and itself a load-path item.
- [`../docs/BRIEF.md`](../docs/BRIEF.md), [`../docs/LESSONS.md`](../docs/LESSONS.md),
  [`../tasks/README.md`](../tasks/README.md), [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) — the read path.
- [`../skills/htmldeck/`](../skills/htmldeck) — the second subject.
- [`../tools/check_all.py`](../tools/check_all.py) — the gate whose output is surface C's largest
  single item, and whose run time is surface E's.
- **The owner's repositories carrying prior optimisation of this kind.** Deliberately unnamed here:
  this repository is public and a local path is machine data. Ask the owner at execution, exactly as
  [T-128](T-128-publish-the-adopter-deck-as-a-worked-example.md) does.
- External sources, gathered in step 5.

**Acceptance criteria**
- [ ] `R8-context-economy-for-coding-agents.md` under `docs/research/` carries the external research,
      the method as numbered steps, the ranking rubric, and every `any`-marked finding
- [ ] **The extraction test passes**: part 1 names no htmldeck file as required reading, and a
      reader with only that document can run steps 1–11 in another repository
- [ ] `CONTEXT-AUDIT.md` under `docs/` carries this repository's findings, ranked, with the two
      subjects reported separately
- [ ] Every finding carries all nine fields, and every `Risk` is written rather than left blank
- [ ] Every technique from the external research is adopted, rejected with the constraint it
      collides with, or deferred with what would close it — and the three sum to the catalogue
- [ ] Steps 1–4's inventory figures are measurements and are stated as such; every gain is a band
- [ ] The local precedent is credited on each finding it produced, without naming its location
- [ ] No path, machine name, or personal datum from any local repository appears in either document
- [ ] The ranked list's top entries are named as candidate child tasks, and none is raised before
      the owner's review

**Open questions**
- **How many of the ranked findings become child tasks, and at what cut-off?** Recommended: the
  owner picks at review from a list already ordered, rather than the audit proposing a line. A cut-off
  chosen by the auditor is a second ranking hidden inside the first. — the owner, at review
- **Does part 1 later become a skill?** Recommended: not now. Write the playbook as a document, and
  let a second task package it if it survives being used once. Packaging a method that has run
  exactly once ships the first draft as the interface. — the owner, after the first reuse

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <none yet>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-13 | → proposed | Raised by the owner, who put it at the top of the execution order ahead of T-128. The four scope questions were asked and answered before the specification was written: **context runway** is the ranking axis, the **written record is in scope** provided no fact loses its only home, the portable half is a **playbook plus findings**, and **both surfaces** are audited and reported separately. `l` and `PH3` by [`../CLAUDE.md`](../CLAUDE.md)'s rule. It is an umbrella: it implements nothing, and the ranked findings become child tasks at the owner's review. |
