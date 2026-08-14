---
id: T-152
title: Give "look at the rendered deck" one operative home
type: deliverable
status: proposed
phase: specify
parent: T-130
blocked_by: []
related: [T-130, T-134, T-143, T-144]
work_package: PH3
owner: the project owner
business_value: medium
effort: xs
created: 2026-08-14
updated: 2026-08-14
deliverables:
  - CLAUDE.md
  - docs/EVALUATION.md
  - tasks/TASK-WORKFLOW.md
---

# T-152 — Give "look at the rendered deck" one operative home

## 1. Specify

**Outcome**
*Look at the rendered deck* has one operative statement, its incident in one lesson entry, and
pointers everywhere else — the same three-way split
[T-144](T-144-give-each-cumulative-rule-one-operative-home.md) applied to *a phase is not a version*.
**The finding is `CE-04`**, stated in
[`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
§8; it is not restated here.

**This is the remainder T-144 surveyed and did not take**, raised at the owner's direction 2026-08-14
rather than left recorded in a closed task. `CE-04` is banded `xs` per rule and is itself closed, so
this task carries the second instance on its own.

**What the survey already found**, in T-144 §1a and not to be re-derived: 34 occurrences across 23
files, of which **20 are task records citing the rule**, which is the system working and not a
defect. The live-document copies are three:

| Home | It states the rule for |
| :--- | :--- |
| [`../CLAUDE.md`](../CLAUDE.md) rule 6 | building — and it also carries `CE-13`'s *never read one whole* |
| [`../docs/EVALUATION.md`](../docs/EVALUATION.md) | scoring |
| [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §2 | closing a task |

**Whether this is one rule or three is the whole question, and T-144 is the precedent for both
answers.** There the rule turned out to be two rules binding at different moments, and splitting them
is what made a single home possible for each (**L-93**). Three acts appear here — build, score,
close — and if each is a distinct rule then all three copies are correct and **the right outcome is
to take nothing**, which is a legitimate close. Re-measure the copies before deciding: T-144's
figures are dated 2026-08-14 and three of those documents changed that day.

**Scope**
- In: deciding how many rules there are, from what each copy actually constrains, before any edit.
- In: for each rule taken, the three-way split — operative statement, lesson entry, pointers.
- In: re-measuring `CLAUDE.md` against its bound afterwards and correcting the debt statement.
- Out: the 20 task-record citations. A citation is not an operative statement.
- Out: `CE-13`'s *never read one whole*, which shares rule 6's sentence and has its own history
  ([T-133](T-133-write-down-that-a-deck-is-never-read-whole.md)). Do not cut it by accident.
- Out: closing with nothing taken counted as failure. If the three acts are three rules, say so and
  close `done` with that finding, per **L-93**'s test.

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.2 — what a session working an audit
  finding owes beyond the finding. Read before starting
- [T-144](T-144-give-each-cumulative-rule-one-operative-home.md) §1a and §4 — the survey, and what
  the first instance cost
- **L-93** in [`../docs/LESSONS.md`](../docs/LESSONS.md) — a rule in five documents is a rule with no
  home, and how to tell one rule from two

**Acceptance criteria**
- [ ] Each of the three copies is re-measured and the act it constrains is named, before any edit
- [ ] The one-rule-or-three question is answered from what the copies constrain, with the answer and
      its reason recorded — including the answer *three rules, take nothing*
- [ ] For each rule taken, exactly one document states it operatively and every other mention points
      there; **the rule stays in tier 1 where tier 1 is what governs it**, and only the incident moves
- [ ] `CE-13`'s clause in rule 6 is intact, checked by reading it
- [ ] `CLAUDE.md` re-measured against its bound, before and after, dated, with the command
- [ ] `python tools/tasks/lint.py` green

**Open questions**
- **One rule or three?** — the implementer, from what each copy constrains, per the scope above. The
  survey did not answer it and the answer decides whether this task edits anything at all.

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
| 2026-08-14 | → proposed | Raised at the owner's direction, from [T-144](T-144-give-each-cumulative-rule-one-operative-home.md) §1a's stated remainder. **The argument for raising it rather than leaving it recorded**: `CE-04` closed, so a remainder inside a closed task has nothing scheduling it, and this project does no work without a task file. It is the second instance of a finding whose band is per rule, so the finding closing does not close the work. **It may correctly take nothing** — three copies, three acts, and T-144's own lesson says a rule that resists one home is more than one rule. |
