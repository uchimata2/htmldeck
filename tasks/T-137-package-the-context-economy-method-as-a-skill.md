---
id: T-137
title: Package the context-economy method as a skill
type: deliverable
status: proposed
phase: specify
parent: T-130
blocked_by: [T-136]
related: [T-130, T-135, T-136]
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-08-13
updated: 2026-08-13
deliverables: []
---

# T-137 — Package the context-economy method as a skill

## 1. Specify

**Outcome**
The audit method in
[`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
becomes something another project invokes rather than reads: a skill that runs the eleven steps, walks
the `F1`–`F5` checklist, and produces the two documents. **Packaging, not rewriting** — if it turns
into a rewrite, the shaping rules failed and that is the finding.

**Why now, and why not before**
[T-130](T-130-audit-the-context-economy-of-an-agent-driven-repository.md) ruled: *this task produces
no skill, and it is shaped so one is cheap later. A second task does it if and when the method
survives being used once.* **It has now been used once, end to end**, on this repository, and the run
produced findings, a ranking, five child tasks and three corrections to itself. The trigger condition
is met.

**What the one run says about the method — the input this task exists to use**

| | What happened | What it means for the skill |
| :--- | :--- | :--- |
| **Steps 1–4 held** | The inventory ran as scripts and produced measurements nobody disputed | The measurement half is ready to package as written |
| **Step 5 was thin and said so only afterwards** | Two searches and two articles, presented as a catalogue; a reader named a tool it had missed | The skill must carry step 5's **coverage rule** — the search record — as a required output, not advice (**L-84**, [T-136](T-136-re-run-the-external-research-with-a-recorded-search-record.md)) |
| **A band was wrong by four times** | `CE-07` was banded on the surface's size, not on what could be changed | The rubric needs the *name the mechanism* step before a band is written (**L-82**) |
| **The F3 line held under pressure** | The general sweep over rationale prose was rejected, on the method's own test | Keep §4.1 verbatim; it is the part most likely to be softened by someone in a hurry |
| **The upstream rule paid for itself** | Reading the upstream backlog first turned a proposal into an adoption | Keep *read their backlog before proposing* as a step, not a note |
| **The byproduct register caught five things** | None of them token efficiency; one a real defect | It works. Keep it outside the ranking, as ruled |

**Scope**
- In: the skill package — the eleven steps, the checklist, the rubric, the ten-field record, the three
  audiences, the byproduct register.
- In: **progressive disclosure**, on the evidence of this repository's own plugin: a description that
  routes, a body that activates, and references loaded per phase. `skills/htmldeck/` is the shape that
  measured best in the very audit being packaged, and it is the local model to copy.
- In: the four shaping rules T-130 followed — numbered imperative steps, a walkable checklist with
  stable ids, stable `CE-nn` ids, and no file of any one repository named as required reading.
- Out: changing the method. Corrections belong to T-136 and to whoever runs it next; this task moves
  it into a package.
- Out: shipping it in the htmldeck plugin. **This is a different product from a deck builder**, and
  bolting an audit onto a presentation skill would confuse both descriptions — which is itself an
  `F1` cost for every adopter who wanted neither.
- Out: publishing or releasing. That is a separate decision with its own gate list.

**Inputs**
- [`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
  — the whole method, and §10's four limits, which the skill must carry rather than drop
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) — the worked example, and the only evidence
  the method produces anything
- [`../skills/htmldeck/`](../skills/htmldeck) — the local model for a three-stage skill, measured in
  the audit at 472 bytes to discover and 5,206 to activate
- **L-82**, **L-83**, **L-84** in [`../docs/LESSONS.md`](../docs/LESSONS.md) — the three the one run
  produced

**Acceptance criteria**
- [ ] The skill runs the eleven steps and produces both documents, on a repository that is not this one
- [ ] It is three-stage: a routing description, a body on activation, references per phase — and the
      description alone is enough to decide whether to activate
- [ ] Step 5's search record is a **required output**, and the skill refuses to present a catalogue
      without one
- [ ] The rubric requires the mechanism to be named before a gain band is written
- [ ] §4.1's F3 line is carried verbatim, including *a finding that cannot name what the prose would
      stop deciding is not a finding*
- [ ] The upstream step keeps *read their backlog first* as a step with its reason
- [ ] The byproduct register survives, outside the ranking and with no gain band
- [ ] **It was packaging**: what changed is stated, and anything that had to be rewritten is reported
      as a defect in the shaping rules rather than quietly fixed
- [ ] Its own load cost is measured — description, body, and each reference — because a skill that
      audits context economy and is expensive to have installed is the joke that writes itself

**Open questions**
- **Does it ship, and to whom?** A skill useful to any agent-driven repository is not obviously this
  project's to publish, and htmldeck's marketplace entry is about decks. — the owner.
- **One skill or two?** The measurement half is deterministic and scriptable; the screening and
  ranking half is judgement. They may want different shapes. — the implementer, from the rule's own
  reason.

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
| 2026-08-13 | → proposed | Raised at the owner's request, ahead of a session they have already planned, so the one run's evidence is not lost with the session that produced it. [T-130](T-130-audit-the-context-economy-of-an-agent-driven-repository.md)'s condition — *if and when the method survives being used once* — **is met**: it ran end to end and produced findings, a ranking, five child tasks and three corrections to itself. §1 records what the run says about the method rather than only that it ran, because that is the input a packaging task actually needs: steps 1–4 held, step 5 was thin, one band was wrong by four times, and the F3 line held under pressure. **Blocked on [T-136](T-136-re-run-the-external-research-with-a-recorded-search-record.md)** — packaging a method whose research half is known to be thin would set that defect in a form other projects copy, and T-136 is the fix already scheduled. `m`, and its own load cost is an acceptance criterion. |
