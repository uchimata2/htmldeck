---
id: T-056
title: Humanize the human-facing documents before publishing
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-050, T-052, T-042]
work_package: v0.1
owner: the project owner
created: 2026-08-09
updated: 2026-08-09
deliverables: []
---

# T-056 — Humanize the human-facing documents before publishing

*Adapted from `T-079` in the **taskmd** project, 2026-08-09, at the owner's request — the same rule
is wanted across every repository that gets published. What carried over unchanged is the owner's
exception, quoted verbatim below, and the shape of the deliverable: **a standing rule, not a pass
over today's tree**. What changed is recorded under [Where this differs from
T-079](#where-this-differs-from-t-079), because a task copied without its differences named is a
task that will be worked against the wrong repository.*

## 1. Specify

**Outcome**
A standing rule, at a home that publication reaches, saying which text gets humanized and under what
exception — plus one use of it on real text, because a rule nobody has run is a claim. **The rule is
the deliverable, not a sweep**: a sweep covers the files that exist on the day it runs, and every
document written afterwards is uncovered.

**Raised to a deployment rule by the owner, 2026-08-09.** *"No release can be published without
humanizing human-facing information. Plugin files are not human facing and must be kept AI
optimized."* Two consequences, and neither is cosmetic:

- **It binds every release, not this one.** A `blocked_by` edge on
  [T-008](T-008-package-document-and-publish.md) is spent the moment T-008 closes, so the edge
  cannot carry a standing rule and was never going to. The constraint now lives in
  [`CLAUDE.md`](../CLAUDE.md) *Publishing constraints*, beside the three rules of the same kind, and
  the edge stays as the gate on the **first** release.
- **The agent-facing exclusion is a rule, not a scope note.** It was already listed under *Out*
  below as a boundary this task would not cross. The owner has made it a positive requirement:
  plugin files **must be kept** AI-optimized, so a humanizer pass over `SKILL.md` is now a defect
  rather than merely out of scope, and this task's job includes saying so where a later reader
  looks.

What that leaves for this task is the **detail and the use**: the covered-set test, the verbatim
exception, the DS-106 boundary, and one run against real text. The decision itself is taken.

**Why this one**
Every document here was drafted in an agent session, and the tell is uniform prose rather than any
one sentence. A reader who bounces off the README never reaches the plugin. This repository already
holds *decks* to that standard — DS-106 bans five categories of terminology and `check.py` gates it —
and holds its own documents to nothing.

**The exception, as given by the owner on 2026-08-09 — verbatim**

> When humanizing docs: preserve tables, code blocks, heading hierarchy, and **Label:** value
> bullets. Skip patterns 15, 16, 18. Apply the rest.

The three skipped patterns are numbered sections of the skill, and they are named here as well as
numbered so the instruction survives the skill being renumbered — **verified against the installed
copy**, `humanizer@humanizer` **2.9.1**, where they are **15 Overuse of Boldface**, **16
Inline-Header Vertical Lists** and **18 Emojis**. Each is load-bearing in a technical document: this
project's prose carries its decisions in bolded labels and its rules in inline-header lists, and
stripping them would flatten the structure that makes a document skimmable rather than remove a tell.

**Scope**
- In: the rule, written where publication reaches it.
- In: what the rule covers, stated as a test rather than a list — *what a stranger reads before they
  have installed anything*. Today that is [`README.md`](../README.md) and any repository or
  marketplace description; a list would go stale the first time a document is added, and silently.
- In: one application of the rule to text that exists today, as the evidence it works.
- Out: **everything agent-facing** — [`CLAUDE.md`](../CLAUDE.md),
  [`skills/htmldeck/SKILL.md`](../skills/htmldeck/SKILL.md) and its `references/`, and the tool
  docstrings. The owner's words: keep them efficient for AI parsing. The compression that reads as
  machine-written is the feature there, and `SKILL.md` is under a byte budget on purpose.
- Out: commit messages, for the same reason.
- Out: task files. Fifty-odd records of work already done are an audit trail; rewriting their prose
  edits the history rather than the product.
- Out: **the ruleset and the research notes** — `docs/DESIGN-SYSTEM.md`, `docs/DESIGN-RATIONALE.md`,
  `docs/EVALUATION.md`, `docs/LESSONS.md`, `docs/research/`. A stranger does not read them before
  installing, they are cited by ID from code, and their density is what makes them usable.
- Out: **deck copy**, which DS-106 and DS-107 already govern and `check.py` already gates. Two
  instruments over one text would disagree, and the gated one wins.
- Out: anything the humanizer would have to invent a fact to improve. **Every figure in the README
  is pasted from a run** ([T-050](T-050-write-the-repository-readme.md)), so a rewrite that rounds,
  rephrases or re-derives one is a defect and not a style improvement.

**Inputs**
- The installed skill: `humanizer@humanizer` 2.9.1, from the `blader/humanizer` marketplace.
  **Not currently enabled for this project** — see the open question below.
- [`CLAUDE.md`](../CLAUDE.md) *Publishing constraints*, where the other publish-time rules live, and
  *Voice*, which already states the machine-written-terminology position for decks.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §3.3 — DS-106 and DS-107, the deck-side rule
  this one sits beside without overlapping.
- The owner's exception of 2026-08-09, quoted verbatim above.

**Acceptance criteria**
- [ ] The rule exists in one home, states what it covers and what it excludes, and carries the
      exception verbatim
- [ ] ~~`CLAUDE.md` gains a pointer to it~~ — **done ahead of this task, 2026-08-09**, when the owner
      raised it to a deployment rule. What remains is that the pointer still resolves to the written
      rule once it exists, and that the summary in `CLAUDE.md` and the rule do not disagree
- [ ] **The rule binds releases, not this release** — stated so that closing T-008 does not retire it,
      and so a second release is covered by the same words
- [ ] **Keeping plugin files AI-optimized is written as a requirement**, not only as this task's
      *Out* list, since the owner made it one
- [ ] The rule's covered set is stated as a test a future document can be held against, not as a
      list of today's files
- [ ] The rule says how it relates to DS-106, so a later reader does not apply both to one text
- [ ] The rule has been **used** on real text, with the before and after both recorded
- [ ] Every figure and every code block in the touched text is byte-identical afterwards, checked
      rather than assumed
- [ ] Nothing agent-facing is rewritten, and `check_scaffold.py` still passes

**Open questions**
- **Is the humanizer skill to be enabled for this project, or run from the other one?** It is
  installed at user level and this project's session does not list it. Whoever works this task
  answers it in the first five minutes; it is recorded because it is the one thing that can stop
  the task dead.
- ~~**Which documents count as human-facing?**~~ **Answered by the owner, 2026-08-09** (on T-079,
  and it transfers): the README definitely, and any repository description. Everything agent-facing
  is explicitly out, because it should stay efficient for AI parsing.
- ~~**Does pattern 14 apply — cutting em dashes?**~~ **Answered by the owner, 2026-08-09: yes.**
  Worth recording that the skill offers an escape and it is not being taken: its *Voice Calibration*
  section says a supplied writing sample outranks §14, so this repository's existing prose could
  have been handed over as a sample to keep its em dashes. The answer forecloses that, and the rule
  must say so, because the next person to read §14 will find that escape too.

## Where this differs from T-079

Four differences, each of which changes what the task does rather than only what it names.

| | taskmd T-079 | here |
| :--- | :--- | :--- |
| **The README** | Does not exist; T-006 step 5 writes it, so T-079 is scoped *away* from it to avoid writing one document twice | **Exists**, written from a clean clone by [T-050](T-050-write-the-repository-readme.md). It is the primary subject, and the ordering problem does not arise |
| **A rule already governs machine-written prose** | No analogue | **DS-106 and DS-107 do, for decks, and `check.py` gates DS-106.** The new rule must say where its jurisdiction ends, or two instruments end up over one text |
| **Where the rule lives** | A `PUBLISHING.md` under `docs/`, pointed to from tier 1 | No such file here. The same shape is the leading candidate, on this project's own precedent — `SKILL.md` keeps substance in `references/` for exactly this reason — but it is step 1, not a decision taken in advance |
| **What must survive verbatim** | Tables, code blocks, headings, label bullets | Those, **plus every figure in the README**, each of which is pasted from a run and re-derived by `ruleset.py --counts` rather than typed |

The publish task is **[T-008](T-008-package-document-and-publish.md)** here, not T-006, and this task
gates it on the same reasoning T-079 used: after publishing, the first impression has been made.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 0 | ~~Settle whether the constraint binds at all~~ — **taken by the owner, 2026-08-09**, and already in `CLAUDE.md` *Publishing constraints* | The bullet, and this row as its record |
| 1 | Answer the enablement question, then settle where the rule's **detail** lives against the cost of `CLAUDE.md` being read every turn | The decision and its rejections, in §3 |
| 2 | Write the rule: the covered set as a test, the exclusions with the owner's reason, the exception verbatim, the DS-106 boundary, and the *Voice Calibration* escape that is not being taken | `PUBLISHING.md` under `docs/`, or wherever step 1 lands it |
| 3 | Add the pointer from `CLAUDE.md`, and measure what it costs there | The edited section, and the character count before and after |
| 4 | Use the rule on real text: draft the repository description a stranger reads, run the skill's draft / audit / final loop on it, and record all three | The before, the audit answers, and the final text, in §3 |
| 5 | Run the rule over `README.md` and record the verdict per section, **including the sections it changes nothing in** | A verdict list, in §4 |
| 6 | Prove the figures survived: re-derive every count the README states and diff the code blocks | The output of `ruleset.py --counts` against the edited README |
| 7 | Point T-008's publication step at where the drafted description lives | The edited T-008 |
| 8 | `task.py index`, `task.py check --closing`, `check_scaffold.py` | The output of each |

**Step 4 is what makes this a task rather than a note**, and **step 6 is what makes it safe.** A rule
written and never run is the unverified claim this project exists to avoid (**L-05**); a humanizer
pass over a document whose every figure is evidence is how a correct number quietly becomes a
plausible one (**L-03**).

**Decisions — shape**

- **The rule is written as a test, not as a list of files.** A list goes stale the first time a
  document is added, and it would go stale silently. *Rejected: enumerating `README.md` and the
  description.* This project has already paid for that once — `reconcile_targets` in
  [`.handoff/config.md`](../.handoff/config.md) is an enumeration, and the audit
  ([T-042](T-042-audit-the-whole-repository-against-itself.md)) is what found what it had stopped
  covering.

**Not in this plan:** rewriting the ruleset or the research notes, which are out of scope above; and
enabling the humanizer skill repository-wide, which is a tooling decision the owner takes once for
every project rather than inside this task.

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <path>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-09 | (no change) | **Raised to a deployment rule by the owner** — *"no release can be published without humanizing human-facing information; plugin files are not human facing and must be kept AI optimized."* The important half is that it binds **every** release: a `blocked_by` edge on [T-008](T-008-package-document-and-publish.md) is spent when T-008 closes, so the constraint could never have lived there and now sits in [`CLAUDE.md`](../CLAUDE.md) *Publishing constraints* beside the three rules of its kind. The edge stays as the gate on the first release. The second half turns this task's *Out* list into a positive requirement: a humanizer pass over `SKILL.md` is now a **defect**, not merely out of scope. Step 3 was therefore done ahead of the task and step 0 records it; what is left here is the detail and one use of it, which is what the task was always for. |
| 2026-08-09 | → proposed | Adapted from `T-079` in the **taskmd** project at the owner's request, who wants the rule applied across every repository that gets published. The owner's exception is carried **verbatim** and its three pattern numbers were **re-verified against the installed skill** rather than trusted from the copy — `humanizer@humanizer` 2.9.1 does have 15 Overuse of Boldface, 16 Inline-Header Vertical Lists and 18 Emojis, and 14 is the em-dash rule with the *Voice Calibration* escape. Four differences from the source are named in their own section rather than absorbed: **the README already exists here**, so it is the subject rather than something to route around; **DS-106 already governs machine-written terminology for decks and is gated**, so the new rule has to state where its jurisdiction ends; there is no `PUBLISHING.md` under `docs/` to write into; and **every figure in this README is pasted from a run**, which makes "preserve code blocks" a stronger obligation than it was in the source. Made a blocker on [T-008](T-008-package-document-and-publish.md) on the source's reasoning: after publishing, the first impression has been made. |
