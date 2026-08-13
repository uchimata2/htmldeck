---
id: T-136
title: Re-run the external research with a recorded search record
type: research
status: proposed
phase: specify
parent: T-130
blocked_by: []
related: [T-130, T-135]
work_package: PH3
owner: the project owner
business_value: high
effort: m
created: 2026-08-13
updated: 2026-08-13
deliverables:
  - docs/research/R8-context-economy-for-coding-agents.md
---

# T-136 — Re-run the external research with a recorded search record

## 1. Specify

**Outcome**
[T-130](T-130-audit-the-context-economy-of-an-agent-driven-repository.md)'s method step 5 runs again,
properly this time, and its output carries the search record the method now requires: the queries run,
the sources read, and an explicit statement that named tools in this space were searched for **by
name**. The catalogue in
[`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
§7 is rebuilt on that basis, and every screening verdict in
[`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §4 is re-derived.

**Why this exists**
The first pass was **two web searches and two fetched articles**, and it presented its result as a
catalogue. The owner asked whether one specific named tool had been checked. It had not — and
checking it produced a technique the catalogue had no entry for. A second gap surfaced in the same
question: an index-and-retrieve approach over the project's own documents, which the first pass had
folded into a general just-in-time row rather than listing as its own technique with its own cost and
assumption.

**Neither was excluded on principle, and it matters that this is said plainly.** There was no rule
against third-party tooling — the catalogue already carries techniques that depend on external
components. They were simply not found, and nothing in the method required looking.

**The screening partition is what made the gap invisible.** *Adopted + rejected + deferred = every
technique gathered* sums correctly whether the catalogue holds nineteen techniques or two. It is an
arithmetic check on step 7 that reads like a coverage claim for step 5, and this task exists because
the audit shipped with that ambiguity intact. The guard now written into the method — a recorded
search record — is deliberately weaker than the partition, because a survey cannot be proved
complete; it can only be shown.

**Scope**
- In: re-running step 5 with breadth, and recording what was searched so a reader can judge it.
- In: **searching for named tools and plugins by name**, not only for ideas and articles.
- In: rebuilding the §7 catalogue, and re-screening **every** row into the three verdicts — including
  the nineteen already there, because a row screened against a thin catalogue was screened against a
  different denominator.
- In: replacing the two provisional rows added 2026-08-13, `T20` and `T21`, with whatever the proper
  pass produces.
- Out: steps 1–4. Those are measurements of this repository and are unaffected by what the literature
  says.
- Out: re-ranking the `CE-nn` findings, unless a new technique produces a new one. The findings rest
  on the inventory, not on the catalogue.
- Out: adopting anything. This is research; the ranking and the owner's review are where work is
  bought.

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.2 — what a session working an audit finding owes beyond the finding: what to check, what to report, and where each thing goes. Read before starting
- [`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
  §3 step 5 — the coverage rule this task is the first to run under — and §7, §10
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §4 — the screening to re-derive
- The named tool the owner supplied, and whatever the by-name search finds beside it

**Acceptance criteria**
- [ ] §7 carries a search record: the queries run, the sources read, and a statement that named tools
      were searched for by name
- [ ] Every catalogue row has what it costs and what it assumes, on the same terms as the existing
      rows
- [ ] Every row is screened *adopted / rejected / deferred* against this project, the three sum to the
      catalogue, and the sum is stated
- [ ] A rejection names the constraint it collides with; a deferral names what would close it
- [ ] `T20` and `T21` are either confirmed, restated, or replaced — none is left as *provisional*
- [ ] The audit's two documents agree on the catalogue's size, in both places it is stated
- [ ] Any new `CE-nn` the research produces is added with all ten fields and ranked with the rest;
      **if it produces none, that is written down as a result**

**Open questions**
- **How wide is wide enough?** The method cannot prove a survey complete, so this task has to choose a
  stopping rule and record it rather than stop when it feels done. — the implementer, from the rule's
  own reason; the owner if the answer costs more than `m`.

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
| 2026-08-13 | → proposed | Raised by the owner the day [T-130](T-130-audit-the-context-economy-of-an-agent-driven-repository.md) closed, from one question: had a specific named tool been checked. **It had not, and it was not excluded on principle** — the first pass was two searches and two articles, and nothing in the method required looking for named tools at all. Checking it produced a technique with no entry in the catalogue, and the same question exposed a second: index-and-retrieve over the project's own documents, folded into a general row rather than listed. **The partition is what hid it** — *adopted + rejected + deferred = everything gathered* sums correctly over any catalogue, however short, so it reads like coverage while checking only the screening. The method now requires a recorded search record, and `R8` §10 carries the limit; this task is the first to run under both. Two provisional rows are in the catalogue meanwhile, marked as such. |
