---
id: T-287
title: Audit — what a session pays per turn, and why it grows
type: audit
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-130, T-153, T-285, T-286]
work_package: PH3
owner: the project owner
business_value: high
effort: m
created: 2026-09-02
updated: 2026-09-02
deliverables: []
---

<!--
The method is the taskmd skill's - METHOD.md section 5, audit.md, and pre-release-audit.md for an
audit of everything about to be released. ../docs/AUDIT-METHOD.md is this project's binding only.
Neither is restated here. Fill the four sections below in order; they are the four lifecycle phases
(TASK-WORKFLOW.md section 2). Child fixes are separate task files with `parent:` set to this id.
-->

# T-287 — Audit: what a session pays per turn, and why it grows

## 1. Specify

**Trigger**
The owner, 2026-09-02, after B17, in these words: *exponentially increasing token consumption is a
real problem. We should address that too.* [`../docs/AUDIT-METHOD.md`](../docs/AUDIT-METHOD.md) §1
names the context-economy audit's trigger as *request, or a change to tier 1*, and both hold: the
request above, and [T-236](T-236-tier-1-and-the-brief-against-what-they-measure.md) changed tier 1
in the same batch.

**Outcome**
The **second run** of the context-economy audit, whose first run was
[T-130](T-130-audit-the-context-economy-of-an-agent-driven-repository.md) and whose grading pass was
[T-153](T-153-run-the-audit-methods-phase-2-over-this-repositorys-own-audit.md). The first run
measured what a session loads **without asking** — tier 1, and the plugin as an adopter loads it.
This run measures what a session **accumulates by working**: what each turn adds to the context,
which of those additions are paid again on every later turn, and which can be changed. Its findings
join [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6's ranking under the next free ids after
`CE-13`, in a section of their own for this subject; every `High` and `Medium` becomes a child task
carrying `finding: CE-nn`, which `tools/docs/findings.py` binds for this register and no other
(the binding's §3); every `Low` is batched or accepted with a reason. **Phase 2 is recorded after the
remedies exist**, as the ecoctx skill requires, and it grades each prediction against what it
bought — the first run's grading found two of thirteen bands held as written.

**Scope**
- In: the four costs B17 met and could name. (1) What the gates print on a green run and how often
  they run — [T-285](T-285-let-a-documentation-task-run-the-gates-its-change-can-reach.md) and
  [T-286](T-286-print-the-verdict-on-a-green-run-and-the-report-only-when-asked.md) are the two
  measured cuts, already specified, and this audit takes its baseline **after** they land so their
  saving is not counted twice. (2) What a resume reads before its first edit: the handoff's pointed
  homes, and how much of each a task actually needs — B17's first task spent about thirty minutes
  reading and its second and third about five each. (3) What a finding costs to close: the register's
  rows run to one or two kilobytes each and the tool a finding is about can be a hundred kilobytes,
  of which a session reads what it must to change it. (4) Tier 1 as it stands after T-236, since a
  change to it is this audit's own trigger.
- In: the method as packaged — the `ecoctx` skill, which is T-130's method made reusable
  ([T-137](T-137-package-the-context-economy-method-as-a-skill.md)); this run is also its second
  use here and reports what the skill could not measure.
- In: **an instrument for the session's own consumption**, which is grade C below and was not
  available to the first run: the harness's own usage breakdown, which the `explain-usage` skill
  reads for one session. Whether that reading is evidence or illustration is an open question.
- Out: the plugin as an adopter loads it — the first run's subject 2, unchanged since, and audited
  again only if a session shows it moved.
- Out: implementing anything. An audit ranks; the owner reviews the ranking, and the top of it
  becomes child tasks then — the first run's rule, kept.

**Coverage grades** — §3 of the method. The split for this run; the sizes are measured at cycle 0
and not typed here, except tier 1, which is measured today because it is the trigger.

| Grade | What it applies to here | Files | Bytes |
| :--- | :--- | ---: | ---: |
| A — wide | tier 1: this repository's `CLAUDE.md`, the owner's global preferences, and the memory index — 15,581, 5,489 and 8,760 bytes on 2026-09-02, every turn | 3 | 29,830 |
| B — narrow | what a resume reads and what a finding costs to close, sampled over B17's three tasks and the audit's own; what the gates print, taken from T-286's table | cycle 0 | cycle 0 |
| C — instrument only | the session's own token accounting, which only the harness holds; read through `explain-usage` and reported as what that reading can and cannot say | — | — |

**Register**
[`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md), continuing the `CE-nn` id space after `CE-13`.

**Acceptance criteria**
- [ ] Every cost in scope is measured, skipped with a stated reason, or produced a finding, and the
      coverage ledger says which.
- [ ] Every finding carries the command that proves it, or names the reading that does and why no
      command can.
- [ ] Every High and Medium finding has a child task; every Low is batched or accepted with a reason.
- [ ] The baseline is taken on a tree where `T-285` and `T-286` have landed, and says so.
- [ ] Phase 2 is recorded after the remedies exist, and names at least one prediction the
      measurement refused — or it was not run honestly.

**Open questions**
- Whether the harness's usage breakdown counts as an instrument for grade C, or only as
  illustration, since it reads one session's transcript rather than the tree — the owner. Recommended:
  an instrument for the session it reads and nothing wider, stated as such on every figure it yields.
- Whether this run waits for `T-285` and `T-286` — the owner. Recommended: yes, third in the order,
  so its baseline is the quieter gates; the cost if wrong is a baseline a few thousand tokens too high.

## 2. Plan

**The cycle program.** One subject per cycle, ordered by expected finding density, each sized to
what one session can read and still judge (the skill's `pre-release-audit.md`). A cycle is a
session boundary: it may be run alone.

| # | Subject | Files | Bytes | Brief | Instrument | Status |
| :-- | :--- | :--- | ---: | :--- | :--- | :--- |
| 0 | Prepare the instruments | | | baseline gates green on a frozen tree, with `T-285` and `T-286` landed; measure grade B | `python tools/check_all.py`, `python tools/tasks/lint.py` | pending |
| 1 | | | | | | pending |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Findings raised**
Counts only; the statements live in the register.

| Severity | Raised | Tasked | Accepted | Open |
| :--- | ---: | ---: | ---: | ---: |
| High | | | | |
| Medium | | | | |
| Low | | | | |

**Child tasks raised**
- <T-NNN — CE-nn — one line>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Phase 2**
<Where the grading is recorded, and the one sentence it reduces to.>

**What this run could not see**
- <a limit met in practice, beyond the method's §10 list>

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-02 | → proposed | Asked for by the owner after B17, as the third task of one exchange: `T-285` cuts how often the gates run, `T-286` what they print, and this measures everything else a session pays per turn and why it grows. Filed as the second run of the context-economy audit rather than a new one, because `AUDIT-METHOD.md` §1 already names it, its register and id space exist, and `findings.py` binds this register's ids. `PH3`. To be run in a session of its own, after the two cuts land. |
