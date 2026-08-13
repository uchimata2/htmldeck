---
id: T-144
title: Give each cumulative rule one operative home
type: deliverable
status: proposed
phase: specify
parent: T-130
blocked_by: []
related: [T-130, T-134, T-143]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-14
updated: 2026-08-14
deliverables:
  - CLAUDE.md
  - docs/LESSONS.md
---

# T-144 — Give each cumulative rule one operative home

## 1. Specify

**Outcome**
A rule this project learned the hard way has **one operative statement** in the document that governs
the behaviour, **one lesson entry** holding the incident and the reason, and **pointers** everywhere
else — instead of a copy in each place it might be needed, with the longest copy in the file paid for
on every turn. **The finding is `CE-04`**, stated in
[`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
§8; it is not restated here.

**This is the second of the two cuts
[T-134](T-134-state-the-tier-model-and-bound-tier-1-as-a-relation.md) enables**, and the cheaper one.
`CE-04` is banded `xs` **per rule**, so the task's size is the survey plus however many rules the
survey finds worth taking.

**Which rules qualify is a survey, not a given.** The finding names the shape — five homes, the
tier-1 copy the longest because it carries the incident — without naming which rule in this
repository was measured that way. Three candidates are worth checking first and none is the answer
until counted: *look at the rendered deck* (34 occurrences across 23 files), *write LF everywhere*
(**L-11**), and *a phase name is not a version number* (**L-69**), which tier 1 carries at the length
of its story.

**Scope**
- In: the survey — every rule with more than one operative home, each copy with its byte count and
  its document, before anything is edited.
- In: for each rule taken, the three-way split: operative statement, lesson entry, pointers.
- In: re-measuring `CLAUDE.md` against its bound afterwards and correcting the debt statement.
- Out: rules with exactly one home. A pointer added to a rule nobody duplicated is work that saves
  nothing.
- Out: deleting a lesson. The incident is the reason the rule survives contact with someone in a
  hurry; it moves, it does not go.
- Out: `CLAUDE.md`'s release chronology, which is [T-143](T-143-split-the-release-chronology-out-of-claude-md.md).

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.2 — what a session working an audit
  finding owes beyond the finding. Read before starting
- [`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
  §8 — `CE-04` in full, including its risk
- **L-13** in [`../docs/LESSONS.md`](../docs/LESSONS.md) — point at the source, do not restate it,
  which is this finding's rule stated generally and already owned

**Acceptance criteria**
- [ ] The survey exists and is recorded in the task: every duplicated rule, every copy, every byte
      count, before any edit
- [ ] For each rule taken, exactly one document states it operatively and every other mention points
      there
- [ ] **The rule stays in tier 1 where tier 1 is what governs it** — only the incident moves. The
      finding's own risk is a pointer replacing a rule a reader then acts without
- [ ] Each rule taken has its incident in one lesson entry, with no copy of the incident left behind
- [ ] `CLAUDE.md` re-measured against its bound, before and after, dated, with the command
- [ ] `python tools/docs/refcheck.py` green, and `python tools/tasks/lint.py` green

**Open questions**
- **How many rules to take.** The band is per rule and the survey decides the count; a task that
  takes every duplicated rule in one pass is no longer `s`. — the implementer, from the survey, with
  the remainder left as a stated remainder rather than silently dropped.

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
| 2026-08-14 | → proposed | Raised at the owner's direction, with [T-143](T-143-split-the-release-chronology-out-of-claude-md.md). `CE-04` was **never one of T-130's seven candidates** — it was ranked tenth and not put up — so this is the owner extending the cut-off rather than accepting a candidate. It is the second cut T-134's bound was written to make decidable, and the survey is deliberately the first step: the finding names the shape of the duplication and not which rule here has it. |
