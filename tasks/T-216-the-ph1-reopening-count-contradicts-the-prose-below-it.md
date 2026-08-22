---
id: T-216
title: The PH1 reopening count contradicts the prose below it
type: audit
status: done
phase: review
parent: null
blocked_by: []
related: [T-214, T-143, T-105]
work_package: PH3
owner: the project owner
business_value: low
effort: s
created: 2026-08-22
updated: 2026-08-22
shipped_in: unreleased
deliverables: []
---

# T-216 — The PH1 reopening count contradicts the prose below it

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

**Open questions — both answered 2026-08-22, by the owner**
- **Is the count worth keeping at all? No, and neither are the ordinals.** Ruled after the specify
  pass put four things in front of it. **Nothing consumes the figure** — the one tool that reads this
  document, `tools/docs/findings.py`, reads its *execution order* table and not this prose. **The
  groupings satisfy no single event rule**: `0.2.1` holds two reopenings split by origin, `0.2.3`
  holds one made of six tasks across two days and two sources, so the criterion *the existing
  groupings satisfy it* could not be met without rewriting the section's narrative spine, which is
  not `s`. **The same defect was already fixed in this document once** — `findings.py`'s docstring
  records that five execution-order notes cited row numbers until an insertion cascaded into the
  prose, four hand renumbering passes in two days, and the notes cite task ids now. **And a count of
  this kind was already deleted once**: `CLAUDE.md` carried *nine reopenings* and *seven PH1 patches*
  until 2026-08-14 and neither was carried over, because neither was re-derivable. An ordinal is an
  index into a set that grows; a release, a date and a source are facts about the item.
- **Scope widened to [`docs/RELEASE-HISTORY.md`](../docs/RELEASE-HISTORY.md) §2, against this task's
  own *Out* clause.** That section states its own total — *has reopened nine times* — written before
  `0.5.0` and `0.5.1` each reopened the phase again. Removing the figure from `RELEASE-PHASES.md`
  while leaving that one would have made `RELEASE-HISTORY.md` the **sole** home for a wrong number,
  which moves the defect rather than closing it.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Derive the reopening events from the tables and from `work_package: PH1`, and test whether one rule fits the existing groupings | It does not — recorded in §1 above, and it is what settles the open question |
| 2 | Delete the total and every ordinal index from the `PH1` prose, replacing each with the release, the date or the task id it stood for | Nine replacements in `RELEASE-PHASES.md` |
| 3 | Write the omission down, so a later session does not restore the figure | The *states no reopening total* paragraph, naming what is countable instead |
| 4 | Fix the three sentences `0.2.3` shipping left behind — *Open `PH1` is therefore*, *Three of the six are closed*, *Four of the five came from looking* | All six are `done`; five of the six came from looking |
| 5 | Do the same to `RELEASE-HISTORY.md` §2's own total, under the widened scope | One replacement |
| 6 | `python tools/tasks/lint.py`, then `python tools/check_all.py` — never together | Two green runs |

## 3. Implement

**Decisions & assumptions**
- **The ordinals go with the total, because they are the total** — *the eighth reopening*, *the ninth
  reopening* and *the sixth was the first from outside* are one running index in different
  grammatical dress. Leaving them would have left the figure decaying under another name. Each was
  replaced by the release it shipped in — 2026-08-22.
- **`A fourth / A sixth / A fifth joined` counted tasks within `0.2.3`, not reopenings, and ran out
  of order in the document.** All three now name their task — T-116, T-122, T-120 — which is the
  fact each sentence was reaching for anyway — 2026-08-22.
- **The `0.2.3` group is left as one reopening of six tasks**, not split to satisfy a rule. Splitting
  it belonged to the branch this audit declined; with no total stated, nothing depends on that
  grouping agreeing with `0.2.1`'s — 2026-08-22.
- **No row was added to or removed from any table.** The *Out* clause on `T-203` onward stands, and
  with no count derived from the tables there is nothing for those rows' absence to distort —
  2026-08-22.
- Patched with a Python script written to a file, `newline=''` on read and write, every replacement
  asserted to match exactly once. Both documents are `eol=lf` under `.gitattributes` and both read
  back with zero `CR` — 2026-08-22.

**Outputs produced**
- [`docs/lessons/L-133.md`](../docs/lessons/L-133.md) — an ordinal cited in prose is a running total
  in disguise, and fixing one numbering in a document does not fix the other
- `docs/RELEASE-PHASES.md` — the `PH1` section: nine ordinal or total statements replaced, three
  stale sentences corrected, one paragraph added recording why no total is stated
- `docs/RELEASE-HISTORY.md` — §2's own total replaced, by the same reasoning

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| One count, stated once, derived from the tables rather than from any earlier sentence | **n/a** | **Superseded by the answered open question** — no count is stated at all, which the owner ruled the better outcome. The criterion assumed the figure survives the audit |
| What counts as one reopening is written down, and the existing groupings satisfy it | **n/a** | Same ruling, and **it was unsatisfiable as written**: `0.2.1`'s two events and `0.2.3`'s single six-task one cannot both follow one rule. That is the evidence which settled the question |
| Every other sentence in the section agrees with that count | **met** | Read as *no sentence states or implies a total*. Nine replaced; a grep for the six surviving forms returns nothing in either document — the one hit left is T-077's row in `PH2`, about figure exclusions |
| Tasks from `T-203` onward are either counted with a stated reason or excluded with one — not omitted silently | **met** | With no count there is nothing to omit them from. The new paragraph names `work_package: PH1` in the task front matter as what is countable, which reaches T-208 and T-214 with no row existing for either |
| `python tools/tasks/lint.py` green | **met** | See the log |

**Three further defects were in the same section, none of them in T-216's statement of the problem.**
*A fourth / A sixth / A fifth* ran out of order; *These six are `0.2.3`* contradicted *Four of the
five came from looking*; and *Open `PH1` is therefore exactly the release's contents* with *Three of
the six are closed* were both left behind by `0.2.3` shipping. A section that stated one figure twice
turned out to state four things twice.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-22 | → proposed | **Raised on the second sighting, not the first.** The 2026-08-21 session found the count inconsistent, judged it pre-existing rather than caused by its own work, and recorded it as *worth an audit, not a guess* — correctly, since guessing is what produced the disagreement. The 2026-08-22 session found the same thing while reconciling after [T-214](T-214-ds-142s-checker-is-an-allow-list-of-one-class-name.md), which is itself a `PH1` reopening and therefore makes the figure one further out of date. `s` because the work is reading one section and deriving one number; `low` because nothing consumes it, which is also the open question. |
| 2026-08-22 | → done | **The audit ended by deleting its subject, which its own §1 named as a legitimate outcome.** Two owner rulings: the count and the ordinals both go, and the scope widens to `RELEASE-HISTORY.md` §2's own copy of the same figure. What settled the first is that **the existing groupings satisfy no single event rule** — `0.2.1` holds two reopenings split by origin and `0.2.3` holds one of six tasks across two days and two sources — so *derive the correct number* had no correct number to reach. Two precedents pointed the same way: `findings.py` records this document's execution-order notes already losing their row numbers to task ids after an insertion cascaded, and `CLAUDE.md` already losing two counts on 2026-08-14 for not being re-derivable. Three defects beyond the reported one turned up in the same section. **The title lost its own figure in the same pass** — it read *and T-214 made it a tenth*, which is the claim this audit found undecidable, and it was the one place a reader meets the task without the correction. The filename never carried the clause, so nothing was renamed. |
