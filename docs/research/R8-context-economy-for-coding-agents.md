# R8 — The context economy of an agent-driven repository

**This document is portable and stands alone.** It carries the external research, the audit method as
numbered steps, the ranking rubric, and every finding that applies to any repository worked by a
coding agent. Copy it into another project and run it there; it names no file of the repository it
was written in as required reading, and it needs no companion document to be usable. The repository
it was first run on is called *the audited repository* throughout, and its figures appear only as
worked examples.

**What it is not.** It is not a skill, and it does not implement anything. It ranks, and someone else
decides. Following it produces a list, not a change.

---

## 1. What is being audited

**Token efficiency, and nothing else.** Security, compliance, licensing, quality and correctness are
not searched for. What is noticed anyway goes in a byproduct register (§6.3) and is never ranked.

**The ranking axis is context runway** — how long a session runs before it compacts. Cost in money
follows from runway and is not the axis. Subject and axis are different questions: token efficiency
decides what may appear in the findings at all, runway decides the order once they are in. A finding
that saves tokens without lengthening the runway is still a finding, and it ranks below one that does
both.

**The written record is in scope, with one hard constraint: no fact loses its only home.** Layering
and load-on-demand are the instruments. Deletion is not. A finding whose gain depends on a rule
becoming unfindable, a gate weakening, or a lesson disappearing is recorded with that risk stated and
ranks below everything else.

---

## 2. The four cost surfaces, and the fifth thing that cuts across them

Every agent-driven repository has all four. An audit that skips one ranks the other three against an
unknown denominator.

| | Surface | What it holds | Why it is separate |
| :--- | :--- | :--- | :--- |
| **A** | **The load path** | What enters context without anyone asking — instruction files at every scope, the memory index and recalled memories, the handoff, the description block of every available skill, tool schemas, system reminders | Paid on **every** turn of **every** session, so a saving here compounds against all the others |
| **B** | **The read path** | What a session must read to do one unit of work — the specification, the conventions, the lessons, the board, the work item, its neighbours, the source it edits | Paid once per session, and it grows with the project's age |
| **C** | **Tool output** | What commands print back — gate reports, per-row verdict listings, test suites, search results | Paid per invocation, and the only surface where a tool's own default decides the cost |
| **D** | **Write volume** | What a session produces — work-item prose, log rows, commit messages, the reconcile edits a closure owes | Paid twice: once written, and again when the next session reads it as surface B |

**E — workflow and tooling** cuts across all four. When a gate must run rather than may, whether a
suite runs whole or targeted, whether exploration searches or reads, whether read-heavy work is
delegated, and how a session hands over. Its findings change *when* a cost is paid rather than how
large it is, so it is reported as its own section.

### 2.1 Tiers, and why surface A is the one with a budget

The most useful distinction this method inherited is **tiering**, and it comes with a membership rule
that is checkable rather than maintained:

| Tier | Loaded | Membership rule |
| :--- | :--- | :--- |
| 1 | every turn | **What the harness loads without being asked.** A property of the tree, not a list someone updates |
| 2 | when work of a kind starts | What a skill, plugin or workflow document pulls in on activation |
| 3 | when a phase or mode begins | What tier 2 loads one at a time, for the branch actually taken |

**Only tier 1 gets a budget.** Tiers 2 and 3 are not paid on every turn, so a line limit there
measures the wrong cost; what constrains them is the load-one-at-a-time rule. Say this explicitly
rather than leaving it inferred — it is the visible cost of budgeting tier 1 alone, and it means the
tier-2 documents are allowed to grow.

**Express the budget as a relation, never as a constant.** A number and the arithmetic that justified
it are a pair that must be edited together, and the number always wins that argument by staying put
while the comparison drifts. Bound tier 1 against something else counted from the same tree — the
flat alternative the split replaced — so that re-measuring changes a measurement and leaves the rule
alone.

**A document that asserts a load discipline the harness does not implement is worse than one that is
over budget**, because it makes the budget unfalsifiable and content keeps being written into it on
the strength of a claim. Establish tier 1 by observation. Do not take a file's word for when it
loads.

---

## 3. The method — eleven steps

Numbered because another project follows them verbatim. Steps 1–4 are inventory and are **measured**;
steps 7–9 are the gain and are **estimated**.

1. **Inventory the load path (A).** Everything that enters context unasked, with its size: the
   instruction files at every scope, the memory index, the handoff, the description block of every
   available skill, and which tool schemas are eager rather than deferred. Establish membership by
   observation (§2.1).
2. **Inventory the read path (B)** for one representative unit of work, **chosen before the audit
   starts and named in the report**. Record what was opened, how much of it was needed, and how much
   was history rather than operative rule.
3. **Inventory tool output (C).** For each gate or command a unit of work runs, the size of what it
   prints on a **green** run. The failing case is rare and its verbosity is usually earned.
4. **Inventory write volume (D)** for the same representative unit.
5. **Research externally.** How practitioners reduce context and token use with coding agents.
   Produce a catalogue of *techniques*, each with what it costs and what it assumes (§7).
6. **Read the local precedent.** Repositories where the same owner has already done this work are an
   input the internet cannot supply: they are proof a technique survived contact with how this owner
   actually works. **Patterns, structures and measurements only** — nothing is copied across, and no
   path, machine name or personal datum from them enters the report.
7. **Screen for applicability.** For each technique: **adopted**, **rejected**, or **deferred**. A
   rejection names the constraint it collides with; a deferral names what would close it. **The three
   are a partition, and a technique in none of them fails the audit** — a silent fourth category is
   how an account that looks complete gets shipped.
8. **Estimate gain and effort.** Bands, not numbers (§5).
9. **Rank.** Gain per unit of effort, with risk as a veto rather than as a term.
10. **Split.** Mark every finding *any project* or *this project*, and write the portable half so it
    stands alone.
11. **Raise child work** for the top of the ranked list — **at the owner's review, not before.**

**Measure with a program, not by reading.** Opening a file to find out how big it is spends the exact
budget under audit. Sizes come off the filesystem; gate output is captured to a file whose length is
measured without printing it. The script is throwaway and belongs outside the repository.

**State the token conversion once and apply it uniformly.** Bytes divided by four is close enough for
English prose and markdown, costs no dependency, and must be labelled as an estimate. Never use it to
separate two findings that a byte count does not already separate.

---

## 4. The finding taxonomy — five families

A walkable checklist with stable ids. **Walk it; do not skim it. A family with no finding against it
is a result and is reported as one.**

| | Family | What it looks for |
| :--- | :--- | :--- |
| **F1** | **What loads, and when** | Anything paid every turn that is needed on few of them. Dynamic and on-demand loading; separating operative instruction from historical narrative |
| **F2** | **Redundancy and contradiction in the record** | The same fact in several homes, or two statements that cannot both be current. Cumulative rules and their history consolidated into one consistent statement with no detail lost; stale and deprecated information; records the project does not own |
| **F3** | **Prose that is not doing work** | Text that neither states a fact nor decides a future question |
| **F4** | **Model work that should be deterministic** | Anything the model does per session that a program could do once. A script that lists or processes instead of the model reading and reasoning; installing an existing third-party component rather than re-deriving its behaviour; simplifying input and output structures **wherever no human reads them** |
| **F5** | **Tool and workflow economics** | When a cost is paid, rather than how large it is. Gate output volume on a green run; a gate that must run per task against one that may run per release; targeted runs against whole suites; delegating read-heavy exploration |

### 4.1 F3 needs a line drawn, and drawing it is part of the work

A project may keep rationale on purpose — a rule whose reason is lost gets undone by the next person
who finds it inconvenient. So the test is not *is this justification* but **does it decide anything
future**.

- **Decides something:** why a rule exists; what it cost to learn; what would close an excusal; what
  was rejected and why; the constraint a later change will collide with.
- **Decides nothing:** a defence of a choice nobody is contesting; the same reason restated in a third
  place; an account of how carefully the author worked.

**An F3 finding that cannot name what the prose would stop deciding is not a finding, and is recorded
as rejected.** F3 is the family that can damage a record, and this is the whole of its guard rail.

**Relocation beats deletion.** The strongest F3 result is usually an F1 move: rationale keeps its
home, in a document the operative path does not load.

---

## 5. The ranking rubric

**Estimate the gain; do not measure it.** Measuring a saving requires building it, which is the work
the ranking exists to decide on.

| Band | Meaning |
| :--- | :--- |
| `XL` | removes more than about a third of a session's cost **on the surface it names** |
| `L` | roughly a tenth to a third |
| `M` | a few per cent |
| `S` | under a per cent, or unquantifiable but real |

A band is always read against its own surface: `L` on the load path and `L` on the read path are
different quantities, and the finding record says which.

Effort uses whatever scale the project already has for work items. **Inventory figures from steps 1–4
are measurements and are stated as measurements; only the saving is banded.** A band with no
inventory behind it is a guess wearing a table.

**Risk is a veto, not a term.** A finding that costs a fact its only home does not get ranked higher
by being cheap.

---

## 6. The finding record

Operative or it is decoration. Every finding carries all ten fields, and a reader must be able to act
on it without the audit's author present.

| Field | What it holds |
| :--- | :--- |
| `CE-nn` | the id — stable, cited from child work and from other projects reusing this method |
| Surface | A, B, C, D or E |
| Family | F1–F5 |
| Finding | what is costing, stated as a fact about the repository |
| Change | what to do |
| Gain | a band, with the inventory figure it rests on |
| Effort | the project's own scale |
| Risk | what it could cost. **`none` is a legitimate value and must be written** |
| Applies to | `any`, `this project`, or `upstream: <component>` |
| Source | external research, local precedent, or this audit |

### 6.1 One numbering space, one statement per finding

`CE-nn` ids are allocated once across both halves of the audit. **Each finding is stated in full in
exactly one document** — here if it is `any`, in the project's own report if it is `this project` —
and the project's ranked table lists every id wherever it is stated. An audit about redundancy that
prints its findings twice has answered its own question.

### 6.2 Three audiences, because a finding is implemented where its subject lives

The split is by **who can act on it**, not by what it is about.

| Audience | Where it is reported |
| :--- | :--- |
| **Any project** | The portable half — this document |
| **This project** | The project's own report, ranked |
| **Upstream** | The project's own report, in its own section: components the project *uses* but does not own |

**The upstream section is written to be handed over and is not implemented locally.** Two things it
owes: **read the upstream backlog before proposing**, because their own precedent outranks the
argument that arrived with the finding; and remember that a handed-over item carries the sender's
labels — its priority is a guess about someone else's project, so state the observation and let them
place it. Say in each entry whether their backlog was read.

### 6.3 The byproduct register

Checking every file for one thing means seeing other things. Record them; keep them out of the
ranking.

- Anything noticed that is not token efficiency — a defect, a stale claim, an inefficiency of another
  kind — goes in a register at the end of the project's report, with the file and what was seen.
- It is **never ranked, never banded, and never becomes a `CE-nn`.** Mixing them would put an unranked
  observation into a list someone is using to buy work.
- A register entry that is really a defect is raised as its own work item at review, and the register
  row then points at it.

---

## 7. The technique catalogue

Gathered in step 5. Each row is a *technique*, with what it costs and what it assumes — screening it
is step 7 and belongs to the project doing the audit, not to this catalogue.

| # | Technique | What it does | What it costs | What it assumes |
| :--- | :--- | :--- | :--- | :--- |
| T1 | **Right-altitude system prompts** | Keeps always-loaded instruction specific enough to guide and short enough not to spend the attention budget | Tokens proportional to detail; verbose instruction competes with the task | Clear direct language guides behaviour without enumerating every edge case |
| T2 | **Just-in-time retrieval over preloading** | The agent holds lightweight identifiers and loads content at runtime | Slower than pre-computed retrieval; needs tool design good enough to stop the agent chasing dead ends | Metadata — paths, names, conventions — carries enough signal to choose well |
| T3 | **Progressive disclosure in three stages** | Discovery loads a name and description; activation loads the body; execution loads referenced files | A structure to maintain, and a description good enough to route on | The unit of knowledge can be split so the common case stops at stage one |
| T4 | **Tool-set curation** | Removes tools the project does not use from the turn cost | Judgement about what is needed; a wanted tool may be absent | If a human engineer cannot say which tool applies, the agent cannot either |
| T5 | **Deferred tool schemas** | Tool *names* load; schemas load on demand | An extra round trip when a schema is needed | The name is enough to decide relevance |
| T6 | **Tool-result clearing** | Drops tool output from history once it has served its purpose | Minimal; described as the lightest form of compaction | Historical output is not needed for later reasoning |
| T7 | **Compaction** | Summarizes history at the context limit and reinitializes | Can lose subtle context whose importance appears later | Summarization preserves decisions and open threads |
| T8 | **Structured note-taking / external memory** | Persistent notes outside the window, retrieved when needed | Discipline to structure notes; they must be consulted | The agent reliably reads its own notes across resets |
| T9 | **Sub-agent delegation** | Isolated context windows for focused work, returning a condensed summary | Orchestration complexity and latency; the summary is lossy | The work decomposes into independent exploration |
| T10 | **Scoped requests over broad retrieval** | Naming the files instead of describing the need | The requester must know which files | The relevant set is knowable up front |
| T11 | **Prompt caching** | Static content first, so repeats hit cache | Ordering discipline | The prefix is genuinely stable |
| T12 | **Output discipline — diffs not files** | Asks for the change, not the artifact | Diffs are harder to read wrong-in-place | Output tokens cost several times input |
| T13 | **Module summaries** | A short summary at the head of a unit, read instead of the unit | Must be kept true, or it lies cheaply | A summary answers the common question |
| T14 | **Code minification for agent input** | Strips non-essential lexical elements, preserving semantics | Breaks line references and human readability | No human reads that copy |
| T15 | **Adaptive context pruning** | Drops low-relevance context as the session runs | Needs a relevance signal; can drop something needed | Relevance is estimable in flight |
| T16 | **Model routing** | Cheaper model first, escalate on need | Escalation costs a retry | The cheap model can recognise its own limit |
| T17 | **Planner → implementer → reviewer** | Splits a task across phases so the expensive model runs briefly | Handover overhead; each phase must record enough for the next | The phases can hand over in writing |
| T18 | **Fresh context per checklist item** | A loop restarts context for each item | Loses cross-item learning | The items are genuinely independent |
| T19 | **Evidence quoted forward** | An earlier phase records verbatim quotes and `path:line` refs so a later phase greps instead of re-reading | The earlier phase writes more | The later phase would otherwise re-read whole files |

**T19 came from local precedent rather than the literature**, and it is the one most easily missed: it
does not reduce a document, it moves a cost from an expensive phase to a cheap one.

---

## 8. Findings that apply to any repository

Stated in full here; ranked in the auditing project's own report. Figures name *the audited
repository* — the first project this method was run on — and are illustrations, not required reading.

### CE-01 — The always-loaded instruction file carries the project's narrative history

| | |
| :--- | :--- |
| **Surface / Family** | A / F1 |
| **Finding** | The file the harness loads unasked accumulates a chronological record — what shipped when, which release carried which fix, which task found which defect. In the audited repository that narrative was **6,980 of 15,630 bytes, 45% of a tier-1 file paid on every turn of every session**. It grows by a paragraph per release and never shrinks |
| **Change** | Split the section. Operative rules that must bind before the agent knows what kind of work this is stay in tier 1; the chronology moves to a dated history document nothing loads by default. **Extract the rules first** — narrative paragraphs written over time embed real rules, and moving the section wholesale loses them |
| **Gain** | `L` on the load path — the audited repository's tier 1 measured 27,633 bytes (~6,900 estimated tokens) across three files, and the chronology is roughly a fifth of it |
| **Effort** | `s` for the move; the extraction is the work |
| **Risk** | A rule that lived only inside a narrative paragraph loses its home. Mitigated by moving rather than deleting, and by reading the section for rules before cutting it |
| **Applies to** | `any` |
| **Source** | this audit; local precedent (§9, P1) |

### CE-02 — The generated board is read whole because the tool that answers the query is unreachable

| | |
| :--- | :--- |
| **Surface / Family** | B / F4 |
| **Finding** | A tracker that generates a full index into the repository also ships commands that answer the two questions a session actually asks — *what next* and *what does this item point at*. When those commands do not resolve in an agent shell, sessions read the generated index instead. Measured in the audited repository: the index **33,676 bytes** against **1,901 bytes** for the open-item listing and **790 bytes** for one item's context — **17.7× and 42×** |
| **Change** | Ship a wrapper that locates the installed tool and exposes those commands, and point the workflow document at it. Where a project already has such a wrapper for its validators, this is one more entry point in a file that already solves the locating problem |
| **Gain** | `L` on the read path — ~7,900 estimated tokens per session that consults the board, which is most of them |
| **Effort** | `xs` |
| **Risk** | `none` — the wrapper adds an entry point and changes no data |
| **Applies to** | `any` |
| **Source** | this audit |

### CE-03 — A gate prints its whole verdict listing on a green run

| | |
| :--- | :--- |
| **Surface / Family** | C / F5 |
| **Finding** | Per-rule gates default to printing one row per rule whether or not anything failed. Measured in the audited repository: **17,391 bytes (~4,300 estimated tokens), 169 lines, on a passing run** of the deck gate — more output than the whole-repository release gate produces (8,233 bytes), and a session runs it repeatedly |
| **Change** | Add a quiet mode printing failures plus a one-line summary. **Keep the full listing as the default** — a person reading a green run is why it exists — and let the agent pass the flag |
| **Gain** | `L` on tool output, per invocation |
| **Effort** | `xs` |
| **Risk** | A quiet green run hides a rule that silently stopped being checked. Mitigated by keeping the count of rules evaluated in the summary line |
| **Applies to** | `any` |
| **Source** | this audit |

### CE-04 — One cumulative rule, five homes, one of them tier 1

| | |
| :--- | :--- |
| **Surface / Family** | A+B / F2 |
| **Finding** | A rule learned the hard way gets written where it was learned, then restated wherever it might be needed. In the audited repository one such rule occupied five documents — the always-loaded instructions, the workflow document, the board preamble, the public readme, and the lessons file — with the tier-1 copy the longest of the five, because it carried the incident that produced it |
| **Change** | One operative statement in the document that governs the behaviour, one lesson entry holding the incident and the reason, and **pointers everywhere else**. The tier-1 copy is the one to shorten first: it is the copy paid on every turn, and it is usually the one carrying the story |
| **Gain** | `M` on the load path per rule, and rules of this kind accumulate |
| **Effort** | `xs` per rule |
| **Risk** | A pointer is weaker than a statement — a reader who does not follow it acts without the rule. Keep the *rule* in tier 1 and move only the incident |
| **Applies to** | `any` |
| **Source** | this audit |

### CE-05 — A large appendix inside the document everyone is told to read first

| | |
| :--- | :--- |
| **Surface / Family** | B / F1 |
| **Finding** | The specification a project points new sessions at grows a per-work-item decision table, and the table outgrows the specification. Measured in the audited repository: **66,461 of 108,163 bytes — 61% — in one section, 112 rows of which 68 were struck through as completed** |
| **Change** | Move the decision table to its own document, leaving the specification the size of a specification. Completed rows go to a history file; the open phase stays where a planner will meet it |
| **Gain** | `XL` on the read path for any session that reads the specification |
| **Effort** | `m` |
| **Risk** | The per-row rationale is a real decision record and must keep its home. Check what else keys on the document — a duplicate-index check pinned to that file by name will follow the content to its new home and fire there, correctly, unless the rule that excuses it moves too |
| **Applies to** | `any` |
| **Source** | this audit |

### CE-06 — A citable unit of knowledge kept in one growing file

| | |
| :--- | :--- |
| **Surface / Family** | B / F1 |
| **Finding** | Lessons, rules or decisions cited individually by id but stored in one document force a session that needs one of them to load all of them. Measured in the audited repository: **152,444 bytes (~38,000 estimated tokens) in 81 entries, mean 1,873 bytes** — a session needing one entry pays 81× |
| **Change** | One file per citable unit, plus a generated one-line index. The id stays the address; only its storage changes |
| **Gain** | `XL` on the read path when an entry is cited, which is most sessions |
| **Effort** | `m`–`l` — every existing citation must still resolve, and any reference checker must be taught the new shape |
| **Risk** | Cross-entry reading gets harder: a person browsing for a pattern loses the single scroll. Mitigated by the generated index carrying each entry's one-line hook |
| **Applies to** | `any` |
| **Source** | this audit |

### CE-07 — The skill-description block is paid every session for skills a project never uses

| | |
| :--- | :--- |
| **Surface / Family** | A / F5 |
| **Finding** | Every available skill contributes its name and description to every session, whether or not the project could ever use it. Measured on the audited machine: **55 skills, 20,941 bytes of description, ~5,200 estimated tokens per session** — comparable to the whole always-loaded instruction set, and mostly for skills irrelevant to the repository at hand |
| **Change** | Enable per project rather than globally. This is a harness setting, not a repository change, so it is the owner's action and not a work item in any one project |
| **Gain** | `L` on the load path |
| **Effort** | `xs` |
| **Risk** | A skill that would have helped is silently absent. Mitigated because the mechanism that lists skills also allows adding one back |
| **Applies to** | `any` |
| **Source** | external research (T4); this audit |

### CE-08 — A measured figure that lives only in the handover chain

| | |
| :--- | :--- |
| **Surface / Family** | A / F2 |
| **Finding** | A handover document is written to be consumed once, so a fact placed in it is copied to the next one rather than re-derived. Measured in the audited repository: a run-time figure for the release gate appeared in **five successive handover files, none of which had a durable home for it**; measuring it took 154 seconds and returned **a third of the figure being carried** |
| **Change** | A figure that will be quoted belongs in the durable document that owns the subject, dated, with the command that reproduces it. A handover may point at it. **This is the handover discipline that already exists — the handover points, it does not store — applied to numbers, which is where it is easiest to break** |
| **Gain** | `S` in tokens, and its value is accuracy rather than size |
| **Effort** | `xs` |
| **Risk** | `none` |
| **Applies to** | `any` |
| **Source** | this audit |

---

## 9. Local precedent — what to look for in a repository that already did this

Step 6 reads repositories where the same owner has already optimised for context. Six patterns
carried over, each stated as a structure rather than as a file.

| | Pattern | What it is | What it buys |
| :--- | :--- | :--- | :--- |
| **P1** | **Stub, canon, depth** | A tiny per-agent instruction file points at one agent-neutral canonical document, which points at heavy references | One copy of the rules for several agents, and the heavy material out of the always-loaded path. **Note honestly**: the stub itself saves little — the layer below it is what saves |
| **P2** | **One file per lifecycle phase** | Workflow split into a small file per phase, each with preflight, do, do-not, close | A session in one phase loads that phase. Measured in precedent: 1.2–7 KB per phase against a single document several times larger |
| **P3** | **Rationale in its own document** | The *why* separated from the operative steps and cited from them | The F3 tension resolves without deleting anything: reasons keep a home the operative path never loads |
| **P4** | **Evidence quoted forward** | A planning phase records verbatim signatures and `path:line` refs so the audit phase greps instead of re-reading | The expensive re-read never happens. This is T19 |
| **P5** | **One skill body, thin agent front-ends** | The portable package lives once; each agent gets a ~1–2 KB adapter | No drift between agents, and no duplicated body |
| **P6** | **Spine plus one branch, never both** | A core document declares which branch file a mode loads, and a run loads exactly one | Confirmed by observation during this audit: resuming loaded the spine and one flow, and never touched the other flow or the tracker binding — **10 KB present, 7 KB of binding and 6 KB of the other flow not paid** |

**Nothing is copied across.** Patterns, structures and measurements only, and no path, machine name or
personal datum from a precedent repository enters the report.

---

## 10. What this method cannot see

Stated so a reader does not mistake the audit's silence for a clean bill.

- **It measures artifacts, not sessions.** File sizes are what a session *could* pay. What it actually
  paid needs harness instrumentation this method does not require.
- **It cannot separate operative prose from narrative mechanically.** Section sizes are measured; the
  split inside a section is a reader's judgement, and every F1 or F3 finding resting on one says so.
- **It does not price attention.** A shorter context is assumed better. Where a cut would make the
  agent guess, that is a risk field, not a measurement.
- **A green gate proves the gate ran, not that the saving is safe.** Every finding here is a proposal
  for someone to review.

---

## 11. Sources

- [Effective context engineering for AI agents — Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Context is a budget: eight levers and three workflow patterns — foojay.io](https://foojay.io/today/context-is-a-budget-eight-levers-and-three-workflow-patterns/)
- [Context engineering: why AI coding agents spend most of their tokens reading, not writing — Moderne](https://www.moderne.ai/blog/context-engineering-why-ai-coding-agents-spend-most-of-their-tokens-reading-not-writing)
- [Just-in-time context for AI agents: a runtime discipline — TrueFoundry](https://www.truefoundry.com/blog/jit-context-just-in-time-context-agents)
- [Progressive disclosure in AI agents — MindStudio](https://www.mindstudio.ai/blog/progressive-disclosure-ai-agents-context-management)
- [Context engineering for coding agents: CLAUDE.md, AGENTS.md and token budgets — CodeSmith](https://www.codesmith.in/post/context-engineering-claude-md-agents-md)
- [Reducing token usage of state-in-context agents using minification](https://arxiv.org/pdf/2606.01326)
- [SWE-Pruner: self-adaptive context pruning for coding agents](https://arxiv.org/pdf/2601.16746)
- Local precedent: two repositories of the same owner, read for structure under step 6 and
  deliberately unnamed.
