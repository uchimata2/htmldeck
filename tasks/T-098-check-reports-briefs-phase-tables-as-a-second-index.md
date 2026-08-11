---
id: T-098
title: taskmd check reports BRIEF.md's phase tables as a second index, and will on every run
type: decision
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-063, T-080]
work_package: PH3
owner: the project owner
business_value: low
effort: xs
created: 2026-08-12
updated: 2026-08-12
deliverables: []
---

# T-098 — taskmd check reports BRIEF.md's phase tables as a second index, and will on every run

## 1. Specify

**Outcome**
`taskmd check` prints one advisory this project has decided about, rather than one it has learned to
skip past. Either the line stops firing, or the reason it is permanently correct-and-ignored is
written where the next person meets it.

**Why this one**
taskmd 0.5.0 added a `DUPLICATE INDEX` advisory and it fires here on the first run:

```
DUPLICATE INDEX  docs/BRIEF.md: a second table of 70 known task ids sits outside the taskmd markers
```

**The mechanism, read rather than inferred.** `check_duplicate_index` counts the **distinct** known
ids a document names outside taskmd's own markers, discounts the ids a *task file* is entitled to
carry — its own and its edges' — and reports when `len(seen) * 2 > len(known)`. A majority of the
known set, chosen upstream so the threshold scales instead of needing a number. `docs/BRIEF.md` is
not a task file, so nothing is discounted: **70 of 97 when this was raised**, and both numbers move
with the backlog — the block above is what the command printed that morning, not a current reading.
The count is deliberately absent from this task's row in `BRIEF.md`: it sits in a sentence naming no
field, so `figures.py` cannot watch it, and it had already gone 70 to 72 within the day.

**It is a true reading of a document that is not a duplicate index.** [`../docs/BRIEF.md`](../docs/BRIEF.md)
*Release phases* is the decision record — three tables, one row per task, each carrying a *why it is
in this phase* the generated board does not hold and never will. Struck-through rows stay on purpose:
"what a release phase contained is a fact about the decision, and an item that vanishes is one nobody
can check was delivered." So the content is right and the count is right at the same time.

**What it costs is the advisory, not the document.** The line is unconditional and grows with the
backlog, so from now on every run of the gate ends with a warning that means nothing. The next
genuine second board — a real index pasted into a document, which is exactly what upstream's T-121
found in an adopting project — arrives as a second line in a place someone already reads past. An
advisory nobody reads is worse than one that is absent, for the reason a validator is believed.

**The recommendation is to accept it and record why**, not to change the document. Splitting the
phase tables into a document of their own moves the count rather than lowering it; pruning the
struck-through rows destroys the record the section exists to keep.

**Scope**
- In: where the acceptance is written — [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) §8's gate
  list is where a red-looking line gets read during a release, so it is the candidate.
- In: whether an exclusion is worth proposing upstream, this project having the channel already
  ([T-063](T-063-improvements-to-propose-upstream-to-taskmd.md),
  [T-080](T-080-check-resolves-a-markdown-link-inside-a-code-fence.md)).
- Out: editing `docs/BRIEF.md`'s phase tables. The advisory is advisory because quoting your own task
  table is legitimate, and this is that case.
- Out: any change to `tools/tasks/lint.py`. It reports what the three tools print; suppressing a line
  there would hide it from the one command that runs them.

**Inputs**
- [`../docs/BRIEF.md`](../docs/BRIEF.md) *Release phases* — the tables that trip it.
- [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) §8 — the gate list, and the candidate home.

**Acceptance criteria**
- [ ] The decision is taken and written in one place, naming the file, the count and why both are
      correct.
- [ ] A release run of §8's gate list meets the line with something that tells the reader it is
      expected.
- [ ] If an upstream exclusion is proposed, it is named here by id and title.

**Open questions**
- Accept and record, or propose an upstream exclusion — the project owner. §1 recommends the first.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- none yet

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-12 | → proposed | Raised on the first run of **taskmd 0.5.0**, installed the same day over 0.4.0. Not a defect in either tool: the advisory is new, the count is right, and the document it names is right too. `PH3` by the rule in [`../CLAUDE.md`](../CLAUDE.md) — PH2 has shipped and this is not a defect in the published plugin, so it is not PH1 work whatever its size. `low`/`xs`: nothing is broken, and what is owed is one written decision. |
