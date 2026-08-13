---
id: T-099
title: Rename the release phases to PH1-PH3 and record which version shipped each task
type: admin
status: done
phase: review
shipped_in: 0.2.2
parent: null
blocked_by: []
related: [T-078, T-092, T-098]
work_package: PH3
owner: the project owner
business_value: high
effort: m
created: 2026-08-12
updated: 2026-08-12
deliverables:
  - .taskmd/config.md
  - tasks/README.md
---

# T-099 — Rename the release phases to PH1-PH3 and record which version shipped each task

## 1. Specify

**Outcome**
No label in this repository can be read as both a phase and a version. The three release phases are
`PH1`, `PH2` and `PH3`; the version a task's work reached an installed copy in is a field on the
task, shown on the board. A reader asking *what shipped in 0.2.1* gets an answer from the board
instead of from six task logs.

**Why this one**
[`../docs/LESSONS.md`](../docs/LESSONS.md) **L-69** already records the failure: a backlog phase
called `v0.1` is not a version anyone can install, and tagging the phase name would have shipped
three fixes to nobody. L-69 weighed this rename and declined it — *"renaming the phases would end the
ambiguity and costs a rewrite of the whole backlog"* — and put a sentence where a version gets picked
instead.

**That was the right call once and is the wrong one now.** The sentence protects the release
sequence, which is where the cost was measured. It does nothing for the *reading* cost, which has
kept accruing: six closed tasks carry `PH3` and shipped in `0.2.1`, and the board shows the first and
not the second, so the page cannot answer the question a reader actually asks. The owner reported
mistaking one for the other repeatedly in conversation, which is the symptom L-69 predicted at the
release and did not predict in prose.

**The two facts, and why one column could never carry both**

| | What it says | Where it lives now |
| :--- | :--- | :--- |
| Phase | What *kind* of work this is, and which release it was planned into | `work_package` |
| Version | What an installed copy compares itself against to decide whether to update | a sentence in the task log, or nowhere |

They diverge by design. A release takes the next patch number on the published line whatever phase
its tasks belong to, so `PH3` work shipping in `0.2.1` is the rule working, not a mistake.

**Scope**
- In: `v0.1` → `PH1`, `v0.2` → `PH2`, `v0.3` → `PH3`, one-to-one, in the schema vocabulary and in all
  51 tasks that carry one — **closed tasks included**, since the task that exposed this
  ([T-092](T-092-product-feedback-from-the-first-external-deck.md)) is closed.
- In: every phase mention in project documents and task prose. Counted before starting: **282 in 60
  tracked files**.
- In: a `shipped_in` field, and a column for it on the board.
- Out: `WP1`–`WP3`. Those are research and design packages, they were never version-shaped, and
  renumbering them would rewrite what happened.
- Out: renaming any actual version. `0.1.5` and `v0.2.1` stay exactly as written.
- Out: the released artifacts. No tag moves and `plugin.json` does not change.

**Inputs**
- [`../.taskmd/config.md`](../.taskmd/config.md) — the vocabulary, which outranks any prose about it.
- [`../docs/BRIEF.md`](../docs/BRIEF.md) *Release phases* — the decision the names belong to.
- [`../CLAUDE.md`](../CLAUDE.md) — the phase rule, and the paragraph L-69 put beside it.

**Acceptance criteria**
- [ ] No tracked file contains a phase-shaped `v0.N`. Every remaining `v0.N.N` is a real version.
- [ ] `python tools/tasks/lint.py` is green, and the board shows a `Shipped In` column.
- [ ] `shipped_in` is derived the same way for every task and the derivation is written down.
- [ ] The phase rule in `CLAUDE.md`, the phase section in `BRIEF.md` and L-69 all read correctly
      under the new names, and L-69 records that the rename it declined was later taken.

**Open questions**
- none. Both were put to the owner and answered: `PH1`/`PH2`/`PH3`, and rename closed tasks too.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Vocabulary and the new column | `.taskmd/config.md` |
| 2 | `work_package` and `shipped_in` in all task front matter | 90 task files |
| 3 | Phase mentions in project documents | `CLAUDE.md`, `BRIEF.md`, `LESSONS.md`, `README.md`, `TASK-WORKFLOW.md`, both templates |
| 4 | Phase mentions in task prose | the rest |
| 5 | Prove no phase-shaped token survives and no version was touched | this file §4 |

## 3. Implement

**Decisions & assumptions**
- **`shipped_in` is the first release tag containing the commit that closed the task** — 2026-08-12,
  and it is derived from git rather than read from prose. The prose is not a reliable source: a scan
  for *shipped in `X`* returned two versions for one task, because the second was that task citing
  another task's release. The git derivation is uniform, verifiable after the fact, and answers the
  question actually asked — *when did this work first reach an installed copy* — rather than *which
  release was cut for it*, which for pre-publication work has no answer.
- **The value is written bare, `0.2.1`, not `v0.2.1`** — 2026-08-12. It matches
  [`../.claude-plugin/plugin.json`](../.claude-plugin/plugin.json) and the existing log prose. The
  `v` prefix belongs to the git tag and nowhere else; keeping it here would re-import the shape this
  task exists to remove.
- **A task closed but not yet in any tag reads `unreleased`** — 2026-08-12. Blank would be
  indistinguishable from *not closed*, and this is a state that lasts only until the next release.
- **The rename is done by reading, not by substitution** — 2026-08-12. `v0.1` is a prefix of
  `v0.1.5`, so any pattern that catches the phase also catches five real versions. Telling them apart
  is the ambiguity being removed, which means no tool can do it. Measured first so the two
  populations were known: 282 phase-shaped against 213 version-shaped.

- **A guard, not a review, is what made the substitution safe** — 2026-08-12. The rewriter records
  every `v?N.N.N` token in a file, substitutes, records them again, and **exits without writing if the
  two lists differ**. So the claim *no version was touched* is enforced per file rather than asserted
  after the fact. It ran over 49 files and never aborted.
- **The 80 phase mentions in task prose were read before any of them were substituted** — 2026-08-12.
  Every one sits in a phrase like *`PH1` patch*, *moved to `PH3`*, *under the release split*; where a
  release is meant the record already writes `v0.1.3` or `v0.1.5`, which the pattern excludes. The
  reading is what licensed the tool, and it is the step §3's previous decision says cannot be skipped.

**Outputs produced**
- [`../.taskmd/config.md`](../.taskmd/config.md) — the vocabulary, `shipped_in` in both views, and
  what each of the two fields answers.
- 99 task files — `work_package` renamed in 51, `shipped_in` added to all 90 closed ones.
- [`../CLAUDE.md`](../CLAUDE.md), [`../docs/BRIEF.md`](../docs/BRIEF.md),
  [`../docs/LESSONS.md`](../docs/LESSONS.md) **L-69**, [`../README.md`](../README.md),
  [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §3, [`README.md`](README.md), and both templates.

**What the guard could not catch, and a reader did.** Three sentences written *during* this task
deliberately quote the old names — *"the phases were named `v0.1` to `v0.3` until 2026-08-12"* — and
the sweep rewrote all three into *"named `PH1` to `PH3` until 2026-08-12"*, which says nothing. The
guard protects versions; nothing protects a sentence whose subject is the old name itself. Found by
reading the three files back, and the two documents excluded from the sweep by hand
([`../CLAUDE.md`](../CLAUDE.md) and **L-69**) are the ones that were never at risk — **the exclusion
list was right and incomplete**, which is the failure mode of every exclusion list.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| No tracked file contains a phase-shaped `v0.N`; every remaining `v0.N.N` is a real version | met | 22 survive, each read individually: six sentences that quote the old names on purpose, plus this file's own scope and mapping lines. Everything else is `v0.N.N`. |
| `lint.py` green, and the board shows a `Shipped In` column | met | `OK - 99 task(s)`, 0 broken pointers, 0 dead sections. The board carries `Work Package` and `Shipped In` side by side, which is the whole point. |
| `shipped_in` is derived the same way for every task and the derivation is written down | met | First release tag containing the commit that closed the task, from git. §3, and again in `TASK-WORKFLOW.md` §3 where a task author meets it. 90 values, one `unreleased`. |
| `CLAUDE.md`, `BRIEF.md` and L-69 read correctly, and L-69 records the reversal | met | L-69 point 4 now carries both answers and why the first one was wrong: it priced the edit and not the reading. |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-12 | → done | **282 phase mentions across 60 files, and the guard held on every one.** The substitution refuses to write a file whose `v?N.N.N` tokens changed, so *no version was touched* is enforced rather than claimed; the 80 phase mentions in task prose were read first, which is what licensed using a tool at all. **The one thing it got wrong was mine, not the tool's**: three sentences written this session to quote the old names were rewritten into nonsense by the sweep that followed them, and the two documents I had excluded by hand were the two that never needed excluding. The board now answers the question that started this — `Work Package` beside `Shipped In`, so `PH3` work shipping in `0.2.1` reads as the rule working instead of as a mistake. |
| 2026-08-12 | → in_progress | Raised and started on the owner's word, after they asked why closed tasks show a phase that looks like a version they had already shipped. **L-69 declined this rename and was right to at the time**: it priced the rewrite and bought protection for the release sequence, which is where the failure had actually happened. What it could not price was the reading cost, and that is what came due. Both naming questions went to the owner rather than being settled here — the label is what everyone reads, and `WP1`–`WP3` already occupy the shape. |
| 2026-08-13 | (no change) | **Shipped in `0.2.2`.** `shipped_in` read `unreleased` until this sweep: the closing commit `e636698` is contained in `v0.2.2`, which is what the field holds (TASK-WORKFLOW.md §3). Found by reconciling the board after the `0.2.3` release rather than by a check - nothing validates the field against the tags. |
