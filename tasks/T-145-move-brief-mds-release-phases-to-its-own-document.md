---
id: T-145
title: Move BRIEF.md's Release phases to its own document
type: deliverable
status: done
phase: review
parent: T-130
blocked_by: []
related: [T-130, T-146, T-147, T-098, T-141]
work_package: PH3
shipped_in: unreleased
owner: the project owner
business_value: high
effort: m
created: 2026-08-14
updated: 2026-08-14
deliverables:
  - docs/RELEASE-PHASES.md
  - docs/BRIEF.md
  - docs/LESSONS.md
  - tasks/TASK-WORKFLOW.md
  - docs/PUBLISHING.md
---

# T-145 — Move BRIEF.md's Release phases to its own document

## 1. Specify

**Outcome**
[`../docs/BRIEF.md`](../docs/BRIEF.md) is the size of a specification again, and the per-task decision
record it grew lives in its own document. **The finding is `CE-05`**, stated in
[`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
§8; it is not restated here.

**Re-measured 2026-08-14, first, and the finding grew.** *Release phases* is **92,894 of 134,596
bytes — 69.0%**, in 134 content rows of which 76 are struck through. The audit read 66,461 of 108,163
— 61% — one day earlier ([`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.2, rule 1), so the
section gained 26,433 bytes in a day and the share moved eight points. **All of the growth is in
PH3** — 52,894 bytes over 86 rows, 58 of them still open — which is the fact that decides the shape
below, not a detail about size.

**It is worth doing, and the growth rate is the argument rather than the ratio.** `../CLAUDE.md`
tells a session to *read the brief first*, and 69% of what it then reads is a per-task decision table
it did not ask for. Every PH3 closure adds a row, so the share climbs on its own; a finding that
worsens without anyone touching it does not get cheaper by waiting.

**One collision is already ruled**: `TASK-WORKFLOW.md` §6 excuses the `DUPLICATE INDEX` advisory **by
file name**, so the excusal moves with the content **inside this task**. Splitting the two would
leave the advisory firing correctly against a document no rule covers.

**[T-098](T-098-check-reports-briefs-phase-tables-as-a-second-index.md) considered this split and
rejected it, on a different question.** It asked how to answer the advisory, and refused the split
because it *"moves the count rather than lowering it"* — which is true, and is not an argument about
the read path. `CE-05` is the read-path argument and T-098 never weighed it. **T-098's prediction is
this task's instrument**: the count is expected to move intact, and that is measurable rather than
hoped for. Distinct known ids named outside the generated markers, 2026-08-14: **105 inside the
section, 22 outside it, against a known set of 151** — so after the move `BRIEF.md` holds 22 against
a threshold of 76 and stops firing, and the new document holds 105 and starts. **One named file
before, one named file after**, so T-098's stated reopening condition — a *second* document
legitimately tripping it — is not met and no upstream exclusion becomes due.

**Scope**
- In: the split, the excusal's move, and every pointer into the moved rows.
- Out: rewriting a row while moving it.
- Out: the execution-order table's placement decisions, which are the owner's and move unchanged.
- Out: any change to the struck-through convention. T-098 ruled the completed rows stay, and this
  task moves them, it does not prune them.

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.2 — read before starting
- `R8` §8 — `CE-05` in full, including the collision it names
- [`../tasks/TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §6 — the excusal that moves
- [T-098](T-098-check-reports-briefs-phase-tables-as-a-second-index.md) — the same split, refused on
  the advisory question, and the prediction reused here
- [T-141](T-141-extract-the-upstream-register-into-one-document-per-owner.md) — this project's worked
  precedent for a section extraction: sweep the citations first, keep every cited heading as a
  pointer, and do not claim the bytes as a saving

**What specifying must settle**

**1. Whether this project splits large documents by unit at all — the policy the three tasks share.**
The answer is a rule with two limbs, and it settles all three without any of them being a precedent
for the wrong one:

> **Split to a document when a section is a different *kind* of document from its host. Split to one
> file per unit only when the unit is addressed by its own id and is wanted one at a time.**

- **This task takes the first limb and not the second.** *Release phases* is a decision record inside
  a specification — two kinds, one file. Its rows are read as a table, by phase; nothing cites a row
  by id, and 134 files holding one table row each would answer a question nobody asks.
- [T-146](T-146-one-file-per-lesson-with-a-generated-index.md) takes the second: `L-nn` is an
  address, lessons are cited singly, and a session that needs one pays for all of them.
- [T-147](T-147-one-workflow-file-per-lifecycle-phase.md) takes the second as well, with its own
  constraint — the `§n` numbers are the addresses and must survive the split.

**2. Where completed rows go, and whether a closed phase stays readable in place.** Both settled by
one measurement. `CE-05` proposes a three-way split — completed rows to a history file, the open
phase left in `BRIEF.md`. **That is refused, because the open phase is the growth.** PH3 is 52,894 of
the 92,894 bytes; leaving it behind cuts 40,000 and leaves the only table that still gains rows in
the document the finding is about, so the finding returns by itself. The whole section moves to one
document, and completed rows stay struck through where they are — the convention T-098 protected,
which already separates shipped from open without a second file.

**3. What still points into the moved section, and how the pointers survive.** Swept before anything
moves, per T-141 step 1. `## Release phases` stays in `BRIEF.md` as a pointer heading so that every
`BRIEF.md § *Release phases*` reference resolves unchanged; `refcheck.py` is the instrument, and it
reports a dead `§` as a failure.

**Acceptance criteria**
- [ ] *Release phases* lives in `RELEASE-PHASES.md`, under `docs/`, whole — head, PH1, PH2 and PH3 —
      with no row rewritten and none pruned
- [ ] `BRIEF.md` keeps `## Release phases` as a pointer heading, and every existing
      `§ *Release phases*` reference still resolves
- [ ] `BRIEF.md` is under 45,000 bytes, and the figure is stated as measured rather than as the
      arithmetic predicted
- [ ] The `DUPLICATE INDEX` advisory names the new document and no longer names `BRIEF.md`;
      `TASK-WORKFLOW.md` §6 and `PUBLISHING.md` §8 name the file the advisory now names, and say the
      count moved rather than fell
- [ ] The policy above is written where the other two tasks will meet it, not only in this file
- [ ] `python tools/check_all.py` is green, and `python tools/tasks/lint.py` ends with exactly one
      advisory

**Open questions**
- None. *Is it worth doing at all* is answered above and the answer is yes; the shape `CE-05`
  proposed is refused with a measurement rather than deferred.

## 2. Plan

**The new document is `RELEASE-PHASES.md`, under `docs/`** — beside its host, which is what keeps
every `../tasks/…` link in the moved rows correct without being touched. 134 rows carry one such link
each; a move that changed the depth would rewrite all of them, and a rewrite of 134 links is where a
transcription error hides.

**Step 1 is the citation sweep, before anything moves.** T-141 recorded that as the step that paid
for itself, and it is what turns *delete the section* into *reduce the section*.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Find every reference to the section and every id-bearing pointer into it, before moving a byte | The list the later steps repoint, and the proof the heading must stay |
| 2 | Write the new document: its own *what this is*, then the head paragraphs, PH1, PH2 and PH3 moved verbatim | `RELEASE-PHASES.md`, under `docs/` |
| 3 | Reduce `BRIEF.md`'s section to a pointer heading — the heading survives, the table does not | `BRIEF.md` at specification size |
| 4 | Repoint the excusal to the file the advisory now names, in both places that carry it | `TASK-WORKFLOW.md` §6, `PUBLISHING.md` §8 |
| 5 | Write the split policy where the next two tasks meet it, and cite it from all three | `LESSONS.md` **L-89**, cited from T-145, T-146, T-147 |
| 6 | Re-measure both documents and the advisory's two counts; run the gates | The review table's figures, taken after rather than predicted |

**What step 1 must not miss.** Three reference forms resolve to this section and only one of them is
a markdown link: the `§ *Release phases*` form that `refcheck.py` checks, a bare mention in prose,
and the pointer `../CLAUDE.md` carries. The heading stays for the first; the second and third are
repointed by hand.

**What this task owes the record at closure lands in the moved document, not in `BRIEF.md`.**
`CONTEXT-AUDIT.md` §6.2 requires a two-cell row above the PH3 table and a renumbered execution order;
after step 3 both live in `RELEASE-PHASES.md`. Writing them into `BRIEF.md` would re-create the
section this task removed, one row at a time, which is the failure mode worth naming in advance.

## 3. Implement

**Decisions & assumptions**
- **The whole section moved; `CE-05`'s three-way shape was refused — 2026-08-14.** The finding
  proposed leaving the open phase in `BRIEF.md` and extracting only the completed rows. PH3 is
  **52,894 of the section's 92,894 bytes**, it is the only table that still gains rows, and it gains
  one per closure — so that shape cuts 40,000 bytes once and rebuilds the finding on a timer. The
  measurement is the argument; the alternative was not rejected on taste.
- **The new document sits beside its host, and that is load-bearing — 2026-08-14.** 134 rows carry
  one `../tasks/…` link each. `docs/RELEASE-PHASES.md` keeps every one of them correct without being
  touched; any other location rewrites 134 links, and a 134-link rewrite is where a silent
  transcription error lives.
- **Moved by slicing, with the bytes asserted equal — 2026-08-14.** The section is ~93 KB, which is
  too large to read into a session (`../CLAUDE.md` rule 6's reasoning, applied to a document rather
  than a deck). A script sliced it between the two headings, wrote both files, re-read the new one
  and asserted the moved text identical to the removed text — `sha256:b414d344735a3c42` both sides.
  Written with explicit `newline=""` because the repository is pinned to `eol=lf`.
- **`## Release phases` stays in `BRIEF.md` as a pointer heading — 2026-08-14.** T-141's precedent
  and **L-39**: a heading removed is a citation falsified, and `§ *Release phases*` is written from
  several closed task records whose text is history and should not be edited.
- **T-098's refusal was reused as the instrument rather than argued with — 2026-08-14.** It refused
  this split as a way to silence the `DUPLICATE INDEX` advisory, on the ground that the split *moves
  the count rather than lowering it*. That is correct and it is not an argument about the read path,
  which is `CE-05`'s and which T-098 never weighed. Its prediction was checked instead of assumed:
  **105 ids moved, 22 stayed, threshold 76** — `BRIEF.md` stopped firing and the new file started, in
  the same run. **One named file before, one after**, so T-098's own reopening condition is unmet.
- **The advisory's excusal was repointed, not duplicated — 2026-08-14.** `TASK-WORKFLOW.md` §6 is the
  operative home and `PUBLISHING.md` §8 keeps its pointer to it (**L-13**, and T-098's own ruling on
  which of the two is primary). Both now name the new file and say the count *moved* rather than fell.
- **The policy went to `LESSONS.md` as `L-89`, not into this file — 2026-08-14.** `CONTEXT-AUDIT.md`
  §6.2 routes a rule that outlives its task there, cited rather than restated. T-146 and T-147 cite
  it in place of the shared question, which is struck through in both rather than deleted.
- **`../CLAUDE.md` gained 18 bytes and is still over its bound — 2026-08-14.** 18,807 → 18,825
  against `.taskmd/config.md`'s 14,087. One pointer was repointed and nothing else; `BRIEF.md` at
  42,485 does not become the binding term, so **L-88**'s relation is unmoved and T-143 and T-144 are
  still the cuts that close it. Recorded because a task that shrinks one document should say what it
  did to the one that is over budget.

**Outputs produced**
- [`../docs/RELEASE-PHASES.md`](../docs/RELEASE-PHASES.md) — the decision record, standing alone
- [`../docs/BRIEF.md`](../docs/BRIEF.md) — 134,596 → **42,485 bytes**, with the heading kept as a pointer
- [`../docs/LESSONS.md`](../docs/LESSONS.md) **L-89** — the splitting policy, cited from three tasks
- [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §6 and [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) §8 —
  the excusal repointed
- Repointed pointers: `../CLAUDE.md`, [`README.md`](README.md),
  [`_audit-umbrella-template.md`](_audit-umbrella-template.md),
  [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.2, §9, §2.2 and `BP-3`,
  [`../docs/LESSONS.md`](../docs/LESSONS.md) **L-25**
- [T-146](T-146-one-file-per-lesson-with-a-generated-index.md) and
  [T-147](T-147-one-workflow-file-per-lifecycle-phase.md) — the shared question struck and replaced
  by the answer

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| *Release phases* lives in `RELEASE-PHASES.md`, whole, with no row rewritten and none pruned | **met** | Asserted rather than reviewed: the moved text was re-read from the new file and compared to the removed text, `sha256:b414d344735a3c42` on both sides. Head, PH1, PH2 and PH3, 134 rows, 76 struck through |
| `BRIEF.md` keeps `## Release phases` as a pointer heading, and every `§ *Release phases*` reference still resolves | **met** | `720 section reference(s) resolved, 0 dead` over `2034 document pointer(s), 0 broken`. Six closed task records cite the section and none was edited |
| `BRIEF.md` under 45,000 bytes, stated as measured | **met** | **42,485**, measured after the move. It was 134,596 before, and the section was 92,894 of that — **69.0%**, not the audit's 61%, because 26,433 bytes of rows landed the previous day |
| The advisory names the new document and not `BRIEF.md`; both records name the file it now names and say the count moved | **met** | `DUPLICATE INDEX  docs/RELEASE-PHASES.md: a second table of 105 known task ids`. Predicted 105 moved / 22 left / threshold 76 before the move, and the run returned 105 |
| The policy is written where the other two tasks meet it | **met** | **L-89** in `LESSONS.md`. T-146 and T-147 have the shared question struck through and replaced by a citation, so neither can answer it a second time |
| `check_all.py` green, `lint.py` ends with exactly one advisory | **met** | `lint.py`: all three passed, one advisory, naming the new file. `check_all.py`: `0 failure(s), 0 unclassified, 0 stale` — 19 commands ran, 1 skipped with its reason, 0 failed, over 37 tracked tools |

**What the review does not claim.** The bytes were not saved, they moved — 92,894 of them, from a
document a session is told to read first into one it opens when it wants the decision. `BRIEF.md`
costs 31.6% of what it did; the total on disk grew by the preamble and this row.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-14 | → done | **The document is 42,485 bytes and the advisory moved with the tables, both measured rather than predicted.** Two things are worth carrying forward. **The finding's own shape was wrong**: `CE-05` proposed leaving the open phase behind, and the open phase is the growth — 52,894 of 92,894 bytes and a row per closure — so that split would have rebuilt the finding by itself. **And [T-098](T-098-check-reports-briefs-phase-tables-as-a-second-index.md) had already refused this split**, on the advisory question rather than the read path; reading what it actually decided turned a contradiction into the instrument that checked this one, because its refusal *was* the prediction. Both went to **L-89**. |
| 2026-08-14 | → in_progress | Built in the planned order, and step 1 paid the same way it paid T-141: the citation sweep is what proved the heading had to stay rather than be deleted. Six live pointers repointed, six historical ones in closed records left alone. The move itself was a slice with the bytes asserted equal — 93 KB is too much to retype and too much to read. |
| 2026-08-14 | → planned | Six steps, sweep first. The new document goes **beside** its host so that 134 `../tasks/…` links stay correct untouched — the cheapest decision in the plan and the one that removes the only real risk. |
| 2026-08-14 | → specified | **The measurement was re-taken first and moved the finding**: 92,894 of 134,596 — 69.0% — against the audit's 66,461 of 108,163 at 61%, one day apart. The open question *is it worth doing* is answered yes, and the argument is the growth rate rather than the ratio. The shared policy is settled as two limbs, so that T-146 and T-147 adopt one each instead of three tasks answering one question three ways. |
| 2026-08-14 | (no change) | **The `specify → plan` scope limit was lifted by the owner**, so this ran the whole lifecycle. What the limit protected is unchanged and recorded in `RELEASE-PHASES.md`: `cancelled` stays available to the three tasks left in the batch, and authorising the lifecycle is not a reason to implement something that specifies into *not worth it*. |
| 2026-08-14 | → proposed | Raised at the owner's direction with the rest of the unraised findings. It was the fifth of T-130's seven candidates and stood as a candidate for a day. **Scheduled to `plan` and no further**: the next session takes it through `specify → plan` to decide whether it is worth implementing, which is the owner's instruction and not this task's judgement. |
