---
id: T-144
title: Give each cumulative rule one operative home
type: deliverable
status: done
phase: review
shipped_in: unreleased
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
  - docs/PUBLISHING.md
  - docs/RELEASE-PHASES.md
  - docs/RELEASE-HISTORY.md
  - tasks/README.md
  - tasks/TASK-WORKFLOW.md
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

## 1a. The survey

**Three candidates were checked and one qualifies.** Measured 2026-08-14, before any edit.

**Out — *write LF everywhere* (`L-11`) has one home.** It appears in `docs/lessons/L-11.md` and in
two task records that cite it. A citation is not an operative statement, and a pointer added to a
rule nobody duplicated saves nothing.

**Out for now — *look at the rendered deck* (`L-01`, `L-02`).** 34 occurrences across 23 files, but
20 of those files are task records citing it, which is the system working. The live-document copies
are `../CLAUDE.md` rule 6, [`../docs/EVALUATION.md`](../docs/EVALUATION.md),
[`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §2 and a research note. Three operative homes, none of them
long, and each is the rule stated *for a different act* — building, scoring, and closing a task.
**This is the stated remainder**, per the open question below: it is a real instance and it is a
second `xs`, not part of this one.

**In — *a phase name is not a version number*, and it is `CE-04`'s own measured instance.** The
finding describes five homes with the tier-1 copy longest because it carries the incident. Counted
here: **six live homes plus the lesson**, and the tier-1 copy is the longest of the six.

| Home | Bytes | What it states | Kind |
| :--- | ---: | :--- | :--- |
| [`../docs/lessons/L-69.md`](../docs/lessons/L-69.md) | 2,927 | The incident, the reason, and four applications | **the lesson — already the right home** |
| [`../CLAUDE.md`](../CLAUDE.md), two paragraphs | **1,024** | Both limbs of the rule **and the whole incident**, retold | tier 1 — paid every turn |
| [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §3 | 651 | The field limb, plus what `shipped_in` means and when it is set | operative |
| [`README.md`](README.md) *(the board)* | 501 | Both limbs, restated for a board reader | operative |
| [`../docs/RELEASE-PHASES.md`](../docs/RELEASE-PHASES.md) head | 339 | The field limb, as an instruction for reading its own tables | operative |
| [`../docs/RELEASE-HISTORY.md`](../docs/RELEASE-HISTORY.md) §2 | 98 | The field limb again | operative — **created this morning** by [T-143](T-143-split-the-release-chronology-out-of-claude-md.md) |
| [`../README.md`](../README.md) *(public)* | 60 | *a phase is not a version*, one clause | human-facing |
| `../docs/RELEASE-PHASES.md`, the `0.2.1` row | 544 | The incident, retold in a completed task row | record, not a rule |

**2,613 bytes of operative restatement across five documents**, none of which is the lesson that
holds the incident. `CE-04` predicted the shape and undercounted the homes by one — and the sixth
was written **today, by the sibling task**, which is the finding demonstrating itself inside the pass
meant to fix it.

**It is two rules, not one, and that is why nothing could hold it.** They bind at different moments
and neither moment is tier 1's:

- **`A` — a patch takes the next patch number on the published line, whatever phase its tasks belong
  to.** Binds when somebody picks a version, which is
  [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) §8. **That document does not state it at all
  today** — step 2 says *bump the version* and never says to what. The rule went to tier 1 in 2026-08-11
  because tier 1 was *near* the release status, which `L-69` §4 records as the cheap fix it knew was
  a compromise.
- **`B` — `work_package` is the phase, `shipped_in` is the version; never write a phase with a `v`.**
  Binds when somebody edits a task's front-matter, which is `TASK-WORKFLOW.md` §3 — where it is
  already stated best, with `shipped_in`'s semantics attached.

**What tier 1 keeps.** Acceptance criterion 3 says the rule stays where tier 1 governs it, and tier 1
governs one thing here: **never write a phase with a `v`**, because every turn's prose uses phase
names. The distinction itself stays as one sentence, since tier 1's own text puts `PH3` and `0.2.1`
in the same paragraph and a reader who conflates them there is the failure. The incident does not.

**Open questions**
- **How many rules to take.** — **One**, the phase rule, with *look at the rendered deck* left as the
  stated remainder above. The band is `xs` per rule and the survey found the instance `CE-04` was
  written from; taking the second would double the task and answer nothing the first does not.

## 2. Plan

**Five steps. The operative homes are written before the copies are cut**, so no moment exists in
which the rule is stated nowhere.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Give rule `A` its operative home: state it in [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) §8, where a version gets picked, and make step 2 say to *what* | The rule's first statement in the document that governs it |
| 2 | Confirm rule `B`'s home in [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §3 is complete on its own, and add the `L-69` pointer if it is not | `B` stated once, operatively |
| 3 | Cut the tier-1 copy to the two clauses tier 1 governs plus pointers to `A`'s home, `B`'s home and `L-69` | `../CLAUDE.md`, ~800 bytes lighter |
| 4 | Replace the three remaining operative restatements with pointers — the board preamble, `RELEASE-PHASES.md`'s head, and `RELEASE-HISTORY.md` §2 — keeping each document's local application of the rule | Three pointers |
| 5 | Re-measure `../CLAUDE.md` against its bound; `python tools/docs/refcheck.py` and `python tools/tasks/lint.py` | Before and after, dated, with the command; both gates green |

**Not touched, and why.** The public `../README.md`'s clause is 60 bytes of human-facing prose under
the humanizer rule, and `RELEASE-PHASES.md`'s `0.2.1` row is a completed record that document keeps
on purpose. Neither is an operative statement, and the scope excludes rules with one home for the
same reason.

## 3. Implement

**Every copy, before and after.** Measured 2026-08-14 with the same spans as §1a's survey.

| Home | Before | After | It now |
| :--- | ---: | ---: | :--- |
| [`../CLAUDE.md`](../CLAUDE.md), the rule's copy | 1,024 | **428** | states the distinction and points twice; the incident is gone |
| [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §3 | 651 | **778** | **is rule `B`'s operative home**, and says so |
| [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) §8 | **0** | **945** | **is rule `A`'s operative home** — it did not state it at all |
| [`README.md`](README.md) *(board)* | 501 | 453 | keeps its own column's meaning and points for the rule |
| [`../docs/RELEASE-PHASES.md`](../docs/RELEASE-PHASES.md) head | 339 | 353 | keeps its reading instruction and points for the rule |
| [`../docs/RELEASE-HISTORY.md`](../docs/RELEASE-HISTORY.md) §2 | 98 | 61 | points |

**Operative statements of this rule: five before, two after** — one per rule, each in the document
that governs the moment it binds. Tier 1 keeps a compressed statement of the distinction, which is
acceptance criterion 3 and is why criterion 2 is not fully met; §4 says so rather than rewording it.

**The bound, and the pair's total.** `../CLAUDE.md` with `CE-01` and `CE-04` both cut:

| | Before T-143 | After T-143 | After T-144 |
| :--- | ---: | ---: | ---: |
| `../CLAUDE.md` | 19,035 | 15,416 | **14,917** |
| The bound — `TASK-WORKFLOW.md` | 11,407 | 11,407 | 11,579 |
| Over by | 7,628 | 4,009 | **3,338** |

**−4,118 bytes off the load path, −21.6%, and the file is still over its bound.** The two cuts T-134
was raised to make decidable are both spent and they close 57% of the debt.

**The finding does not reduce bytes; it moves them off the load path.** `PUBLISHING.md` grew 945
and `TASK-WORKFLOW.md` 172 to hold what tier 1 gave up, and T-143 added a 10,047-byte document. The
repository is **larger** after both tasks. That is the trade the tier model was written for and it is
worth stating once, plainly: a byte in tier 2 is paid when work of its kind starts, a byte in tier 1
is paid on every turn of every session, and only the second is what `CE-01` and `CE-04` measure.

**Decisions & assumptions**
- **It is two rules, not one, and splitting them is what made a single home possible.** Every
  previous attempt kept them together, so no one document could govern both — one binds at release
  time and one at task-edit time. `A` to `PUBLISHING.md` §8, `B` to `TASK-WORKFLOW.md` §3 —
  2026-08-14.
- **`PUBLISHING.md` §8 never stated rule `A`.** The release sequence said *bump the version* and not
  to what, which is the document whose own step the failure broke. Five documents restated the rule
  and the one that governs it was not among them — 2026-08-14.
- **Tier 1 keeps the distinction and loses the incident**, which is `CE-04`'s prescription exactly and
  its stated risk read the other way: a pointer replacing a rule leaves a reader acting without it,
  so what stays is the rule and what goes is the story — 2026-08-14.
- **The public `README.md` and `RELEASE-PHASES.md`'s `0.2.1` row were left alone.** One is 60 bytes
  of human-facing prose under the humanizer rule, the other is a completed record that document keeps
  on purpose. Neither is an operative statement — 2026-08-14.
- **`L-11` and *look at the rendered deck* were surveyed and not taken**, the first because it has one
  home and the second as the stated remainder. §1a carries both — 2026-08-14.

**Outputs produced**
- [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) — §8 gains rule `A`, and step 2 says what to bump to
- [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) — §3 declares itself rule `B`'s operative home
- [`../CLAUDE.md`](../CLAUDE.md) — two paragraphs to one, 1,024 bytes to 428
- [`README.md`](README.md), [`../docs/RELEASE-PHASES.md`](../docs/RELEASE-PHASES.md),
  [`../docs/RELEASE-HISTORY.md`](../docs/RELEASE-HISTORY.md) — three restatements to three pointers

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The survey exists and is recorded in the task: every duplicated rule, every copy, every byte count, before any edit | **met** | §1a. Three candidates checked, one taken, one rejected for having a single home, one left as a stated remainder. Seven copies of the rule taken, each sized |
| For each rule taken, exactly one document states it operatively and every other mention points there | **partly met** | Five operative statements became two — one per rule, each in the document that governs it. **Tier 1 is a third**, deliberately: see the row below. Everything else points |
| **The rule stays in tier 1 where tier 1 is what governs it** — only the incident moves | **met**, and it is why the row above is not | The two criteria conflict on this rule and this one wins, because `CE-04`'s stated risk is a pointer replacing a rule a reader then acts without. Tier 1 keeps the distinction in one sentence — its own prose puts `PH3` and `0.2.1` in the same paragraph — and loses the 596 bytes of incident |
| Each rule taken has its incident in one lesson entry, with no copy of the incident left behind | **met** | `L-69` holds it and always did. Tier 1's retelling is gone. `RELEASE-PHASES.md`'s `0.2.1` row keeps its own account, which is a completed record that document keeps on purpose, not a rule |
| `CLAUDE.md` re-measured against its bound, before and after, dated, with the command | **met** | §3. 15,416 → 14,917 for this task; 19,035 → 14,917 across the pair, −21.6%, still 3,338 over |
| `python tools/docs/refcheck.py` green, and `python tools/tasks/lint.py` green | **met** | `2273 document pointer(s) checked, 0 broken`; `751 section reference(s) resolved, 0 dead`; `taskmd check` OK on 151 tasks |

**The finding undercounted its own homes, and the sixth was written the same morning.**
[T-143](T-143-split-the-release-chronology-out-of-claude-md.md) put a fresh copy of the field limb
into `RELEASE-HISTORY.md` while moving the chronology — a duplicate created by the sibling task, in
the pass raised to remove duplicates, hours before the survey that caught it. **A rule with no
declared home gets copied by whoever needs it next**, and that is the mechanism `CE-04` describes
rather than an oversight by anyone.

**And the document that governs the behaviour was the one document not stating it.** Five documents
restated the rule; `PUBLISHING.md` §8 — the release sequence, whose own step 2 the original failure
broke — said *bump the version* and never said to what. The rule had gone to tier 1 in 2026-08-11
because tier 1 sat *near* the release status, which `L-69` §4 already recorded as a compromise.
**Restatement spreads where the governing home is missing**, so the first question is not *which
copies to delete* but *which document should have had it*. **L-93** is the general form and the
place it is stated; it is cited here rather than repeated.

**Child fix tasks raised**
- [T-152](T-152-give-look-at-the-rendered-deck-one-operative-home.md) — *look at the rendered deck*,
  the second instance §1a surveyed and this task did not take. **Raised at the owner's direction on
  review**, against this task's own answer of *leave it as a stated remainder*: `CE-04` is closed, so
  nothing schedules a remainder living inside a closed task. `xs`, and it may correctly take nothing.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-14 | → done | **Five operative statements became two, and the document that governs the behaviour was the one not stating it.** `PUBLISHING.md` §8 said *bump the version* and never said to what, while five other documents restated the rule — so the fix was not deleting copies but giving `A` a home for the first time, and splitting it from `B`, which binds at a different moment and lives in `TASK-WORKFLOW.md` §3. `../CLAUDE.md` 15,416 → 14,917; across the pair 19,035 → 14,917, **−21.6%**, still 3,338 over the bound. **The finding undercounted its own homes and the sixth was written the same morning** by T-143, in the pass raised to remove duplicates — which is the mechanism rather than an oversight. **And this does not reduce bytes**: `PUBLISHING.md` grew 945 and `TASK-WORKFLOW.md` 172 to hold what tier 1 gave up. It moves bytes off the load path, which is the only thing the finding ever measured. |
| 2026-08-14 | → in_progress | Built in the planned order, and writing the operative homes first meant the rule was never stated nowhere. Criterion 2 came out **partly met** rather than reworded: tier 1 keeps the distinction because criterion 3 requires it and `CE-04`'s own risk is a pointer replacing a rule a reader then acts without. |
| 2026-08-14 | → planned | Five steps, homes before cuts. |
| 2026-08-14 | → specified | **The survey found `CE-04`'s own instance and one more home than the finding counted** — six live homes plus the lesson, 2,613 bytes of operative restatement across five documents, tier-1 copy longest at 1,024 because it carries the incident. Two of the three candidates were rejected on measurement: `L-11` has one home, and *look at the rendered deck* is a real second instance kept as a stated remainder rather than folded in, which is the open question's answer. **The unlock was seeing it as two rules**: a release-numbering rule and a task-field rule, binding at different moments, which is why no single document had ever been able to own it. |
| 2026-08-14 | → proposed | Raised at the owner's direction, with [T-143](T-143-split-the-release-chronology-out-of-claude-md.md). `CE-04` was **never one of T-130's seven candidates** — it was ranked tenth and not put up — so this is the owner extending the cut-off rather than accepting a candidate. It is the second cut T-134's bound was written to make decidable, and the survey is deliberately the first step: the finding names the shape of the duplication and not which rule here has it. |
