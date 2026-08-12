---
id: T-098
title: taskmd check reports BRIEF.md's phase tables as a second index, and will on every run
type: decision
status: done
phase: review
parent: null
blocked_by: []
related: [T-063, T-080]
work_package: PH3
shipped_in: unreleased
owner: the project owner
business_value: low
effort: xs
created: 2026-08-12
updated: 2026-08-12
deliverables:
  - tasks/TASK-WORKFLOW.md
  - docs/PUBLISHING.md
  - docs/LESSONS.md
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
field, so `figures.py` cannot watch it, and it had already gone 70 to 72 within the day. **78 on
2026-08-12**, after the `0.2.2` release added six rows — which is the argument, not a detail: the
number only ever climbs, and every release moves it.

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

**The open question is answered: accept and record.** §1's recommendation stands, and the rival —
propose an upstream exclusion — is rejected in §3 rather than deferred.

**The home is not the one §1 nominated.** [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) §8's gate
list is where a release meets the line, but `lint.py` runs on every task edit and a release happens a
few times a month, so the release checklist is the smaller readership. The decision lives where the
checker's own output is documented — [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §6, beside the two other
alarms this project has decided are permanently correct — and §8 carries a pointer to it.

| # | Step | Where |
| :--- | :--- | :--- |
| 1 | The decision: the file, the dated count, the mechanism, and why both are right | `TASK-WORKFLOW.md` §6 |
| 2 | A pointer, so a release run meets the line already answered | `PUBLISHING.md` §8, above the `--sources` note |
| 3 | The upstream question, decided rather than left open | §3 below |

## 3. Implement

**Decisions & assumptions**
- **Accept and record; the document is not edited — 2026-08-12.** Splitting the phase tables into a
  document of their own moves the count rather than lowering it, and pruning the struck-through rows
  destroys the record the section exists to keep.
- **The primary home is `TASK-WORKFLOW.md` §6, not `PUBLISHING.md` §8 — 2026-08-12.** The advisory
  fires on every `lint.py` run, not only at release, so it belongs with what `taskmd check` reports.
  §8 gets a pointer, not a second copy (**L-13**).
- **The line is ignored by the file it names, not by its rule — 2026-08-12.** Both records say
  `docs/BRIEF.md` explicitly, so a `DUPLICATE INDEX` naming any other document reads as new. That is
  what answers §1's stated cost — the next genuine second board arriving where someone already reads
  past — without an upstream change.
- **No upstream exclusion is proposed — 2026-08-12.** It was the rival worth taking seriously: this
  project has the channel and has used it twice ([T-063](T-063-improvements-to-propose-upstream-to-taskmd.md),
  [T-080](T-080-check-resolves-a-markdown-link-inside-a-code-fence.md)), and an opt-out marker in
  taskmd's own `<!-- taskmd: -->` vocabulary would be a small change. It is refused because of what it
  is: a per-document silencer for an advisory whose whole value is that it cannot be silenced. Every
  project that trips it has a document it believes is legitimate — that belief is exactly what
  upstream's T-121 found to be wrong in an adopting project. The cost here is one documented line;
  the cost of the marker is borne by everyone the advisory is right about.
- **What would reopen it — 2026-08-12.** A second document legitimately tripping the advisory. The
  record above works because the expected set is one named file; at two it is a rule again, and the
  case for an upstream exclusion is then made by this project's own experience rather than by
  anticipation.

**Outputs produced**
- [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §6 — the decision, in the *What the two checks enforce* list.
- [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) §8 — the pointer, above the `--sources` note.
- [`../docs/LESSONS.md`](../docs/LESSONS.md) **L-73** — the generic half: an advisory decided about is
  pinned to the subject that earns it, or the decision spends the rule.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The decision is taken and written in one place, naming the file, the count and why both are correct | **met** | `TASK-WORKFLOW.md` §6. The count is written as a dated reading — **78 of 105 on 2026-08-12** — because it sits in a sentence naming no field, so `figures.py` cannot watch it and every release moves it |
| A release run of §8's gate list meets the line with something that tells the reader it is expected | **met** | `PUBLISHING.md` §8, before the gate list's other notes. A pointer to §6, not a second copy of the decision |
| If an upstream exclusion is proposed, it is named here by id and title | **met, vacuously** | None is proposed, and §3 says why rather than leaving the option unmentioned |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-12 | → done | **Accepted and recorded, and the upstream rival refused on its merits rather than on its size.** Both moves are decisions this task existed to take, so it closes at `done` with nothing implemented and no document edited except the two that now carry the record. The home moved off the candidate §1 named: a release checklist is read a few times a month and `lint.py` runs on every task edit. |
| 2026-08-12 | → proposed | Raised on the first run of **taskmd 0.5.0**, installed the same day over 0.4.0. Not a defect in either tool: the advisory is new, the count is right, and the document it names is right too. `PH3` by the rule in [`../CLAUDE.md`](../CLAUDE.md) — PH2 has shipped and this is not a defect in the published plugin, so it is not PH1 work whatever its size. `low`/`xs`: nothing is broken, and what is owed is one written decision. |
