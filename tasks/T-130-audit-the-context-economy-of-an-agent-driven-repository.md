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
| What is being audited? | **Token efficiency and nothing else.** Security, compliance, quality and every other audit are out of scope |
| Optimise for what, *within* that? | **Context runway first** — how long a session runs before compaction. Cost follows from it and is not the ranking axis |
| Is the written record in scope? | **Yes, with single-source-of-truth preserved.** Layering and load-on-demand, never deleting a fact's only home |
| What is the portable half? | **A playbook plus findings** — the method, so another project re-runs it rather than re-deriving it |
| Which surfaces? | **Both, reported separately** — this repository's own workflow, *and* `skills/htmldeck/` as loaded into an adopter's context |
| Does it produce a skill? | **No, and it is shaped so one is cheap later.** See *Skill-ready, not a skill* |

**Subject and axis are different questions and both have answers.** The *subject* is what may appear
in the findings at all; the *axis* is how findings are ordered once they are in. Token efficiency
decides the first, context runway the second — a finding that saves tokens without lengthening the
runway is still a finding, and it ranks below one that does both.

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

### The finding taxonomy — five families, and the checklist part 1 ships

**Seeded by the owner 2026-08-13 and deliberately not closed.** The examples below are what is
already known to work; step 5's research extends the families and may add one. A family with no
finding against it is a result and is reported as one — the checklist is walked, not skimmed.

| | Family | What it looks for | Examples given |
| :--- | :--- | :--- | :--- |
| **F1** | **What loads, and when** | Anything paid every turn that is needed on few of them | Dynamic and on-demand loading; **separating operative instruction from historical narrative**, of which `docs/BRIEF.md` is the named case |
| **F2** | **Redundancy and contradiction in the record** | The same fact in several homes, or two statements that cannot both be current | Consolidating cumulative rules and their history into **one consistent statement with no detail lost**; eliminating duplication; removing contradicting pairs, and pairs where one strongly weakens the other; stale and deprecated information; records the project does not own |
| **F3** | **Prose that is not doing work** | Text that neither states a fact nor decides a future question | **Self-justification beyond useful reasoning** — see the line below, because this family is the one that can damage the record |
| **F4** | **Model work that should be deterministic** | Anything the model does per session that a program could do once | A script that lists or processes deterministically instead of the model reading and reasoning; **installing an existing third-party skill with no external dependencies** rather than re-deriving its behaviour; simplifying input and output structures **wherever no human reads them** |
| **F5** | **Tool and workflow economics** | When a cost is paid, rather than how large it is | Gate output volume on a *green* run; a gate that must run per task against one that may run per release; targeted runs against whole suites; delegating read-heavy exploration |

**F3 needs a line drawn, and drawing it is part of the work.** This project keeps rationale on
purpose: a rule whose reason is lost gets undone by the next person who finds it inconvenient. So
the test is not *is this justification* but **does it decide anything future**. Why a rule exists,
what it cost to learn, and what would close an excusal all decide something. A defence of a choice
nobody is contesting, a restatement of the same reason in a third place, and an account of how
carefully the author worked decide nothing. **A finding in F3 that cannot name what the prose would
stop deciding is not a finding**, and is recorded as rejected.

### Skill-ready, not a skill

The owner's ruling, 2026-08-13: **this task produces no skill.** It produces a document. But the
document is shaped so that packaging it later is a packaging job rather than a rewrite, at no extra
effort now:

- the method is **numbered, imperative steps**, each with its inputs and its output named;
- the taxonomy is a **walkable checklist** with stable `F1`–`F5` ids, not prose to interpret;
- findings carry stable `CE-nn` ids, so another document can cite one without quoting it;
- part 1 **names no file of this repository** as required reading (the extraction test, below).

That is the whole of the secondary target. Do not spend further effort on skill packaging here; a
second task does it if and when the method survives being used once.

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
| Family | F1–F5 |
| Finding | what is costing, stated as a fact about the repository |
| Change | what to do |
| Gain | a band, with the inventory figure it rests on |
| Effort | `xs`–`xl` |
| Risk | what it could cost — a fact losing its only home, a gate weakening, a rule becoming unfindable. `none` is a legitimate value and must be written |
| Applies to | `any`, `this project`, `upstream: handoff`, or `upstream: taskmd` |
| Source | external research, local precedent, or this audit |

### Three audiences, because a finding is implemented where its subject lives

The split the owner asked for is by **who can act on it**, not by what it is about.

| Audience | Where it is reported | Note |
| :--- | :--- | :--- |
| **Any project** | Part 1, `R8` | The portable half. This is what gets lifted into another repository |
| **This project** | Part 2, `CONTEXT-AUDIT.md` | Findings whose subject is htmldeck's own files, tooling or workflow |
| **Upstream** | Part 2, its own section | The **handoff skill** and the **taskmd plugin**. Both are the owner's, both are used here, and htmldeck is an *adopter* of them — so this audit sees real usage that their own repositories cannot show themselves |

**The upstream section is written to be handed over, and it is not implemented here.** Two things it
owes, both learned the hard way in this repository: **read the upstream backlog before proposing**,
because their own precedent outranks the argument that arrived with the finding; and remember that a
handed-over item carries the sender's labels — its priority here is a guess about their project, so
state the observation and let them place it.

### The byproduct register

Checking every file for one thing means seeing other things. The owner's instruction is to **report
them and not lose them**, while keeping them out of the ranking.

- Anything noticed that is not token efficiency — a compliance issue, a stale claim, a defect, an
  inefficiency of another kind — is recorded in a **byproduct register** at the end of part 2, with
  the file and what was seen.
- It is **never ranked**, never given a gain band, and never becomes a `CE-nn`. Mixing them would
  put an unranked observation into a list the owner is using to buy work.
- A register entry that is really a defect is raised as its own task at review, by the ordinary
  rule, and the register row then points at it.

**Scope**
- In: all four surfaces plus workflow, on **two** subjects reported separately — this repository's
  development workflow, and the plugin as loaded into an adopter's context.
- In: the external research, and the local precedent the owner supplies.
- In: restructuring proposals for the written record — layering, load-on-demand, splitting an
  operative rule from its history — **provided no fact loses its only home**.
- In: **the handoff skill and the taskmd plugin**, as this repository experiences them. Observed
  here, reported for their owner, implemented there.
- In: **the byproduct register** — everything seen in passing that is not token efficiency.
- Out: implementing anything. The ranking is reviewed first, and that is the whole point of the
  umbrella.
- Out: every other kind of audit as a *goal*. Security, compliance, licensing, quality and
  correctness are not searched for; what is noticed anyway goes in the register.
- Out: producing a skill, or spending effort on skill packaging beyond the four shaping rules above.
- Out: measuring a saving by building it.
- Out: anything that weakens a gate, deletes a lesson, or makes a rule harder to find. A finding
  whose gain depends on that is recorded with the risk stated and ranked below everything else.
- Out: the local repositories' contents. They are read; nothing is copied, and **no path, machine
  name or personal datum from them enters this repository** — the publishing constraint in
  [`../CLAUDE.md`](../CLAUDE.md), and **L-81**.
- Out: changing anything inside the handoff skill or the taskmd plugin. They are not this
  repository's to edit.

**Inputs**
- [`../CLAUDE.md`](../CLAUDE.md) — the working rules, and itself a load-path item.
- [`../docs/BRIEF.md`](../docs/BRIEF.md), [`../docs/LESSONS.md`](../docs/LESSONS.md),
  [`../tasks/README.md`](../tasks/README.md), [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) — the read path.
- [`../skills/htmldeck/`](../skills/htmldeck) — the second subject.
- [`../tools/check_all.py`](../tools/check_all.py) — the gate whose output is surface C's largest
  single item, and whose run time is surface E's.
- **The handoff skill and the taskmd plugin**, as installed. Their in-repository halves —
  [`../.handoff/config.md`](../.handoff/config.md) and [`../.taskmd/config.md`](../.taskmd/config.md)
  — are readable from here; the skill and plugin bodies live under the owner's Claude configuration
  and are located at execution rather than written down, for the same reason as the line below.
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
- [ ] Every finding carries all ten fields, and every `Risk` is written rather than left blank
- [ ] Every technique from the external research is adopted, rejected with the constraint it
      collides with, or deferred with what would close it — and the three sum to the catalogue
- [ ] **Every family F1–F5 is walked and reported on, including any that yielded nothing**
- [ ] Each F3 finding names what the prose would stop deciding, or is recorded as rejected
- [ ] The handoff and taskmd findings sit in their own section, phrased as observations for their
      owner rather than as work planned here, and each says whether their backlog was read
- [ ] The byproduct register exists, is separate from the ranking, and carries no gain band
- [ ] Steps 1–4's inventory figures are measurements and are stated as such; every gain is a band
- [ ] No skill, plugin or package is produced; part 1 satisfies the four shaping rules
- [ ] The local precedent is credited on each finding it produced, without naming its location
- [ ] No path, machine name, or personal datum from any local repository appears in either document
- [ ] The ranked list's top entries are named as candidate child tasks, and none is raised before
      the owner's review

**Open questions**
- ~~**How many of the ranked findings become child tasks, and at what cut-off?**~~ **Answered
  2026-08-13 — the owner picks at review, from a list already ordered.** The audit proposes no line.
- ~~**Does part 1 later become a skill?**~~ **Answered 2026-08-13 — not here, and shaped so it is
  cheap later.** The four rules in *Skill-ready, not a skill* are the whole of the secondary target,
  and they cost nothing to follow from the start. A second task packages it if the method survives
  being used once.
- **None open.** The specification is complete; the one thing execution still needs from the owner
  is the location of the local repositories, which cannot be written here.

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
| 2026-08-13 | (no change) | **Both open questions answered and the scope widened three ways, all by the owner the same day.** The audit's *subject* is token efficiency and nothing else, which is a different question from its ranking axis and now says so. A **finding taxonomy** of five families was seeded — F3 is the delicate one and the specification draws its line, because this project keeps rationale on purpose and *decides something future* is the test. A **third audience** was added: the handoff skill and the taskmd plugin are the owner's, are used here, and this repository is the adopter whose real usage their own repositories cannot show — observed here, handed over, implemented there. And a **byproduct register** takes everything seen in passing that is not token efficiency, deliberately outside the ranking so an unranked observation cannot enter a list the owner is buying work from. The skill question resolved to *not here, and shaped so it is cheap later*: four structural rules that cost nothing to follow, and no further packaging effort. |
| 2026-08-13 | → proposed | Raised by the owner, who put it at the top of the execution order ahead of T-128. The four scope questions were asked and answered before the specification was written: **context runway** is the ranking axis, the **written record is in scope** provided no fact loses its only home, the portable half is a **playbook plus findings**, and **both surfaces** are audited and reported separately. `l` and `PH3` by [`../CLAUDE.md`](../CLAUDE.md)'s rule. It is an umbrella: it implements nothing, and the ranked findings become child tasks at the owner's review. |
