---
id: T-162
title: Run the packaged skill end to end against a third repository
type: deliverable
status: proposed
phase: specify
parent: T-137
blocked_by: []
related: [T-130, T-136, T-137, T-153]
work_package: PH3
owner: the project owner
business_value: high
effort: l
created: 2026-08-15
updated: 2026-08-15
deliverables: []
---

# T-162 — Run the packaged skill end to end against a third repository

## 1. Specify

**Outcome**
The `ecoctx` skill runs **all sixteen steps** against a repository that is neither the one the method
was invented in nor the one the skill ships from, and produces the two documents. The subject is
`taskmd`, chosen by the owner on 2026-08-15.

**Why this is the product test and not a loose end**
[T-137](T-137-package-the-context-economy-method-as-a-skill.md) closed with one criterion unmet, and
it is this one. **The method's rule that part 1 names no file of any one repository was a discipline
until the skill was published; it is now the thing that makes the skill installable at all.** A search
proved the *text* carries no such name — 238 distinctive names, zero hits — and that is a weaker claim
than it looks. **A search proves nothing is named. A run proves nothing is assumed.** The gap between
those two is where a portable method turns out to have one repository's habits in it, and no static
check reaches it.

**What the partial run already found, and why it is not enough**
T-137 exercised steps 1–4 against `taskmd` and got real figures: tier 1 at **6,619 bytes**, the board
at **36,393** on the read path, and a green test run printing **344 bytes** for 261 tests. Those are
measurements, and they are the half of the method that has never failed. **The half that fails is
steps 7–9**, where a technique is screened, a mechanism is named and a band is written, and none of
that was touched. Eleven of thirteen bands missed in the one graded run; a method whose measured half
has been exercised twice and whose estimated half has been exercised once is not tested.

**Scope**
- In: steps 1–11 in full, against `taskmd`, producing a ranked register and a report **in that
  repository**, not here.
- In: the search record step 5 owes, across all three axes, with saturation declared per axis and the
  empty rounds listed. **Expect the catalogue to be a delta against the existing one** rather than a
  fresh survey, and say which it was.
- In: **a written answer to *did anything have to be explained that the skill should have said*.** That
  is the output this task exists for, and it is a change to the skill rather than to `taskmd`.
- Out: implementing any finding it raises. That is `taskmd`'s decision and its own work.
- Out: phase 2. It runs after the raised work is done, and there will be none for months.
- Out: any finding about `ecoctx` itself. A skill auditing the repository it ships from is a
  different task and would not test portability at all.

**Inputs**
- The `ecoctx` skill, in its own repository, at the commit T-137 closed on.
- [T-137](T-137-package-the-context-economy-method-as-a-skill.md) §3 — the partial run's figures, so
  steps 1–4 are re-measured rather than re-derived, and the dates are compared.

**Acceptance criteria**
- [ ] All sixteen steps are accounted for: run, or **not run with a stated reason**. A step in
      neither fails this task, which is the skill's own partition rule applied to the skill
- [ ] Both documents exist in `taskmd`, and the portable half names no file of `taskmd` either
- [ ] Every finding carries all eleven fields, `Controller` included — **it has never been reported on
      by a real run**, because it was added on the last day of the first one
- [ ] The search record covers three axes with saturation declared per axis and the empty rounds listed
- [ ] **Every place the skill had to be explained, worked around or ignored is written down** as a
      change to the skill, separately from anything about `taskmd`
- [ ] `findings.py` runs green against the result, configured for whatever `taskmd` uses, **with no
      change to the tool** — or the change it needed is the finding
- [ ] The run's own cost is stated: what was loaded, and how much

**Open questions**
- ~~**Does the owner want findings raised as work items in `taskmd`, or only reported?**~~ **Answered
  2026-08-15 — report only.** The run produces the two documents and stops; nothing is placed on
  `taskmd`'s board by this task. **The owner owning both projects makes the objection weaker, not
  absent** — the method's upstream rule is that a handed-over item carries the sender's guess about
  someone else's priorities, and a first real run that ignores its own rule because the two owners
  happen to be the same person teaches the skill the wrong habit at the exact moment it is being
  tested for portability.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |

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
| 2026-08-15 | → proposed | **T-137's one unmet criterion, raised as its own task because it is the product test rather than a remainder.** A search proved the skill's text names no file of the repository it came from; a run is what proves nothing is *assumed*, and no static check reaches the gap between those two. Steps 1–4 already ran against `taskmd` during T-137 and produced figures, so what is untested is precisely the half that fails: screening, naming a mechanism, and writing a band, where eleven of thirteen missed in the one graded run. `l` rather than `m` because a full sixteen-step audit is the same size as the audit that produced the method, and T-137 was scoped as packaging. **`Controller` has never been reported on by a real run** — it was added on the last day of the first one — which makes this the first test of an eleventh field as well. Publication is gated on it. |
