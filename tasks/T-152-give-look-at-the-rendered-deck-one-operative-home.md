---
id: T-152
title: Give "look at the rendered deck" one operative home
type: deliverable
status: done
phase: review
parent: T-130
blocked_by: []
related: [T-130, T-134, T-143, T-144]
work_package: PH3
finding: CE-04
owner: the project owner
business_value: medium
effort: xs
created: 2026-08-14
updated: 2026-08-14
shipped_in: unreleased
deliverables:
  - CLAUDE.md
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

### 1a. What the re-measurement changed — 2026-08-14

**The survey named the wrong third document, and re-measuring is what found it.**
[`../docs/EVALUATION.md`](../docs/EVALUATION.md) **states no operative form of this rule.** Searched
for `look`, `opened`, `offline`, `browser`, `Chrome` and `a person`: its only hits are a table cell
*describing* what the render gate does, and a rubric row about progressive disclosure — *"the slide
only resolves … once something is opened"* — which is the word in a different sense entirely.

**The third copy was inside [`../CLAUDE.md`](../CLAUDE.md) all along.** *Working method* 3 stated the
close gate in full, and [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) restated it in §2 **while saying
`CLAUDE.md` sets the bar** — a document pointing and restating in the same sentence — and again in §7
step 3. So the real count was **three copies of the close gate across two documents**, two of them in
tier 1's own file, and nothing in the third document at all.

**It is two rules, and they bind at different moments** — T-144's finding, a second time (**L-93**):

| Rule | What it settles | Binds at | Home |
| :--- | :--- | :--- | :--- |
| **A** | what *looking* is, and what it excludes | build and verify | [`../CLAUDE.md`](../CLAUDE.md) rule 6 — tier 1 governs building |
| **B** | that a task does not close until it happened | task close | [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §7 step 3 — that document owns the lifecycle |

**Three acts, two rules.** Scoring looked like a third act and is not: `EVALUATION.md` assigns *who
runs which stage*, which is a different subject that happens to use the same verb. **The answer is
therefore not *take nothing*** — the scope allowed for that outcome, and the copies that made it wrong
were in the two documents nobody had counted twice.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Re-measure all three named copies before any edit, and search `EVALUATION.md` for an operative statement rather than assuming the survey | The correction above |
| 2 | Confirm rule A's home — [`../CLAUDE.md`](../CLAUDE.md) rule 6 — is complete on its own, and leave it alone | Rule A stated once, `CE-13`'s clause untouched |
| 3 | Make [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §7 step 3 rule B's operative home, saying what it blocks | Rule B stated once |
| 4 | Cut the two restatements: [`../CLAUDE.md`](../CLAUDE.md) *Working method* 3 and [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §2, each to a pointer | Two copies gone, one off tier 1 |
| 5 | Re-measure [`../CLAUDE.md`](../CLAUDE.md) against its bound, **both terms** (**L-94**) | Before and after, dated |

## 3. Implement

**Operative statements of the close gate: three before, one after.**

| Home | Before | After | It now |
| :--- | ---: | ---: | :--- |
| [`../CLAUDE.md`](../CLAUDE.md) *Working method* 3 | 146 | **85** | points at the checklist that owns the bar |
| [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §2 | 274 | **203** | points twice — to rule A for *what*, to §7 for *when* |
| [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §7 step 3 | 82 | **336** | **is rule B's operative home**, and says what it blocks |
| [`../CLAUDE.md`](../CLAUDE.md) rule 6 | 407 | 407 | unchanged — rule A's home, `CE-13`'s clause intact |
| [`../docs/EVALUATION.md`](../docs/EVALUATION.md) | **0** | **0** | never stated it |

**The bound, both terms, measured with `CLAUDE.md`'s own command.**

| | Before this session | After T-151 | After T-152 |
| :--- | ---: | ---: | ---: |
| [`../CLAUDE.md`](../CLAUDE.md) | 15,182 | 15,095 | **15,034** |
| The bound — [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) | 11,579 | 11,734 | **11,925** |
| Over by | 3,603 | 3,361 | **3,109** |

**−494 on the debt, and only 148 of it is tier 1 getting smaller.** The other 346 is the bound rising
because rule B's home had to state the rule properly. That is the trade working as designed and it is
worth saying plainly: **moving a rule out of tier 1 costs bytes in tier 2 and closes the gap twice as
fast**, because the relation has two moving terms (**L-94**).

**Decisions & assumptions**
- **Two rules, not three, and not one.** The three acts are build, close and score; the third is a
  different subject wearing the same verb, so `EVALUATION.md` is untouched — 2026-08-14.
- **Rule A stays in tier 1.** What *looking* is governs building, which is what tier 1 governs; only
  the close gate left. The scope required this and re-measuring confirmed it — 2026-08-14.
- **`EVALUATION.md` is removed from this task's declared deliverables**, because it was declared
  before the survey was checked and nothing in it changed — 2026-08-14.

**Outputs produced**
- [`../CLAUDE.md`](../CLAUDE.md) — *Working method* 3 is a pointer; rule 6 untouched
- [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) — §7 step 3 is rule B's home; §2 points

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Each of the three copies re-measured and its act named, before any edit | met | and one of the three was not a copy — §1a |
| The one-rule-or-three question answered from what the copies constrain | met | **two**, binding at build and at close; the third act is a different subject |
| One document states each rule operatively, every other mention points; the rule stays in tier 1 where tier 1 governs it | met | rule A in `CLAUDE.md` rule 6, rule B in `TASK-WORKFLOW.md` §7 step 3 |
| `CE-13`'s clause in rule 6 intact, checked by reading it | met | *never read one whole* present; rule 6 unchanged at 407 bytes |
| `CLAUDE.md` re-measured against its bound, before and after, dated, with the command | met | the table above, `CLAUDE.md`'s own command, 2026-08-14 |
| `python tools/tasks/lint.py` green | met | four checks |

**What the second instance taught that the first did not.** T-144 found a rule in five documents and
split it in two. Here the *survey inherited from that task* named a document that had never stated the
rule, and missed a copy sitting in the file the rule was being cut out of. **A survey is evidence
about the day it was taken** — **L-96** — and `CE-04`'s band is per rule precisely because each rule
has to be re-counted: the count is the work, not the preamble to it.

**Child fix tasks raised**
- none. `CE-04` has no third instance: the surveyed rules are now one-home each.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-14 | → proposed | Raised at the owner's direction, from [T-144](T-144-give-each-cumulative-rule-one-operative-home.md) §1a's stated remainder. **The argument for raising it rather than leaving it recorded**: `CE-04` closed, so a remainder inside a closed task has nothing scheduling it, and this project does no work without a task file. It is the second instance of a finding whose band is per rule, so the finding closing does not close the work. **It may correctly take nothing** — three copies, three acts, and T-144's own lesson says a rule that resists one home is more than one rule. |
| 2026-08-14 | → specified → planned | **The inherited survey was wrong in both directions.** `docs/EVALUATION.md` states no operative form of the rule — searched six ways — and the copy it was credited with was in `../CLAUDE.md`'s own *Working method* 3, inside the file the rule was to be cut out of. `TASK-WORKFLOW.md` §2 held a third, pointing at `CLAUDE.md` and restating it in the same sentence. Two rules, binding at build and at close. |
| 2026-08-14 | → in_progress → done | Close-gate statements **three → one**. `../CLAUDE.md` −61, `TASK-WORKFLOW.md` +191, and the debt against the bound **3,361 → 3,109** — only 148 of the session's 494 came from tier 1 shrinking, the rest from the bound rising as rule B's home stated it properly. `CE-13`'s clause read and intact. `EVALUATION.md` dropped from the declared deliverables: it was named before the survey was checked. |
