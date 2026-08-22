---
id: T-216
title: The PH1 reopening count contradicts the prose below it, and T-214 made it a tenth
type: audit
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-214, T-143, T-105]
work_package: PH3
owner: the project owner
business_value: low
effort: s
created: 2026-08-22
updated: 2026-08-22
deliverables: []
---

# T-216 — The PH1 reopening count contradicts the prose below it, and T-214 made it a tenth

## 1. Specify

**Outcome**
[`docs/RELEASE-PHASES.md`](../docs/RELEASE-PHASES.md)'s account of how many times `PH1` has reopened
is one number, derived from the document's own rows, and the prose below it agrees with it.

**Why this one**
**The document states a count and then narrates past it.** Its `PH1` section says *the phase has
reopened eight times*, and two paragraphs later says *the ninth reopening is three tasks, also from
the adopting project*. Both sentences are in the same section, four screens apart, and neither is
marked as superseding the other. A reader takes the first as the total and the second as a detail of
it, which is the one reading that cannot be true.

**This was already drift, and this session added to it.**
[T-214](T-214-ds-142s-checker-is-an-allow-list-of-one-class-name.md) closed 2026-08-22 as a `PH1`
task — a defect in the published gate, reopening the phase again — so whatever the correct figure
was, it is now one higher. **Two sessions have now looked at this and declined to fix it**, each
recording it as *worth an audit, not a guess*, which is the right call twice and the wrong outcome
the second time: a finding that survives being noticed twice has stopped being a note and become
work.

**Why it is an audit and not a fix.** The number cannot be read off the prose, because the prose is
what disagrees. It has to be **derived from the document's own tables** — which `PH1` rows exist,
which of them were raised after the phase first closed, and which arrived together as one reopening
rather than separately. That last part is the whole difficulty: the document already groups tasks
into reopenings (*the eighth reopening is four tasks*, *the ninth is three*), so the count is over
**events**, not over tasks, and nothing records which event a row belongs to except the prose that
is wrong.

**Scope**
- In: derive the reopening count from the `PH1` tables, event by event, and state what defines an
  event — same report, same day, same source is the shape the existing prose already uses.
- In: reconcile every sentence in that section that states or implies a count.
- In: decide whether tasks from `T-203` onward count as reopenings for this purpose. **They have no
  row in this document by settled precedent**, so a count derived from the tables will silently omit
  them — which is how T-214 would go missing from the very figure it increments.
- Out: **adding rows for T-203 onward.** That precedent is not reopened here; if the count needs them
  and the tables must not have them, the answer is a sentence saying so, not a table change.
- Out: any other document. `tasks/README.md` is generated and states no such count.

**Inputs**
- [`docs/RELEASE-PHASES.md`](../docs/RELEASE-PHASES.md) — the `PH1` section, its tables and the
  three sentences that state a count.
- [T-214](T-214-ds-142s-checker-is-an-allow-list-of-one-class-name.md) — the newest `PH1` task, and
  the one that has no row by precedent.
- `CLAUDE.md` — what makes a task `PH1`, which is what makes a reopening a reopening.

**Acceptance criteria**
- [ ] One count, stated once, derived from the tables rather than from any earlier sentence
- [ ] What counts as one reopening is written down, and the existing groupings satisfy it
- [ ] Every other sentence in the section agrees with that count
- [ ] Tasks from `T-203` onward are either counted with a stated reason or excluded with one — not
      omitted silently
- [ ] `python tools/tasks/lint.py` green

**Open questions**
- **Is the count worth keeping at all?** It is narrative rather than operative: nothing reads it, no
  gate checks it, and it has now been wrong for at least ten days. **Deleting it is a legitimate
  outcome of this audit** and may be the better one — a figure with no consumer that two sessions
  have declined to correct is exactly what `CLAUDE.md`'s *deliverables must operate* argument is
  about. Decide during specify, from whether any sentence elsewhere depends on it.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |

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
| 2026-08-22 | → proposed | **Raised on the second sighting, not the first.** The 2026-08-21 session found the count inconsistent, judged it pre-existing rather than caused by its own work, and recorded it as *worth an audit, not a guess* — correctly, since guessing is what produced the disagreement. The 2026-08-22 session found the same thing while reconciling after [T-214](T-214-ds-142s-checker-is-an-allow-list-of-one-class-name.md), which is itself a `PH1` reopening and therefore makes the figure one further out of date. `s` because the work is reading one section and deriving one number; `low` because nothing consumes it, which is also the open question. |
