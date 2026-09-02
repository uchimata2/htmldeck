---
id: T-223
title: Derive each audit cycle's membership instead of counting it
type: fix
status: done
phase: review
parent: T-219
blocked_by: []
related: [T-218, T-222, T-220]
work_package: PH3
owner: the project owner
business_value: high
effort: s
created: 2026-08-23
updated: 2026-08-23
shipped_in: 0.7.0
deliverables:
  - tools/docs/cycles.py
---

# T-223 — Derive each audit cycle's membership instead of counting it

## 1. Specify

**Trigger**

`PR-06`, raised between cycles 1 and 2 of
[T-219](T-219-pre-release-audit-of-the-whole-repository.md) and recorded in
[`../docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3. The owner asked on
2026-08-23 that it be settled before the remaining cycles run, if it reached them.

**It reaches every one of them.** T-219 section 2's step 2 is *re-measure the cycle's file list*,
and there is no list to re-measure: section 2 states a **count** per cycle and never a
**membership**. So each of the forty-one remaining cycles re-derives its own subject by reading a
phrase, which is what cycles 0 and 1 did by hand and is the mechanism behind the finding. The
acceptance criterion *every tracked file is read, skipped with a stated reason, or produced a
finding* is a claim about a partition the document cannot express.

**Outcome**

A command that assigns every tracked path to exactly one audit cycle by rule, fails when a path
belongs to none, and fails when a rule names a path that is gone. T-219's two tables stop being
hand-kept and are regenerated from it.

**Scope**

- In: the partition, both failure directions, and the two tables in T-219 that restated it.
- In: re-cutting a cycle boundary where the derived membership shows a cycle too large to read in
  one sitting.
- Out: running any cycle. This makes the plan measurable; it reads nothing on the plan's behalf.
- Out: `PR-01`'s question of whether cycle 17 should hold the blindness fixture. That is a separate
  open finding with its own remedy, and encoding an answer here would settle by tooling what it
  says to settle by measurement.

**Inputs**

- [`../docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) — `PR-06`, its evidence and its
  proposed remedy.
- [`../tools/check_all.py`](../tools/check_all.py) — the partition this one is modelled on, one
  subject over.
- [`../docs/AUDIT-METHOD.md`](../docs/AUDIT-METHOD.md) section 2 — the coverage grades and the rule
  that an item in none of the three states is a gap.

**Acceptance criteria**

- [ ] Every tracked file is assigned to exactly one cycle, by a rule rather than by a list.
- [ ] A tracked file no rule claims fails the command, and a rule matching nothing fails it —
      both proven against the real rule set, not only in a fixture.
- [ ] T-219 section 1's grade table and section 2's Files and Bytes columns are regenerated from
      the command, and the two agree because they have one source.
- [ ] The two figures `PR-06` could not reconcile are either located or shown to be unlocatable,
      with the command that decides which.
- [ ] No cycle carrying tracked files is left far above the size a cycle is read at.

**Open questions**

- **Does this outlive the audit?** A partition over cycles nobody will run again charges every later
  file a decision it does not need. Left to cycle 42 and written into the tool's own docstring, so
  the answer is taken rather than inherited. Owner answers, at cycle 42.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Write the rule per cycle from that cycle's own subject line, ordered, first match winning | `tools/docs/cycles.py` |
| 2 | Run it against the tree and drive the unassigned list to zero | a partition covering every tracked path |
| 3 | Compare the derived counts against the plan's stated ones, cycle by cycle, and account for every difference | the located and the unlocatable halves of `PR-06` |
| 4 | Re-cut any boundary the comparison shows is now oversized | balanced bands |
| 5 | Regenerate T-219's two tables from the command; record the outcome in the register | T-219 sections 1 and 2, `PR-06` closed |

## 3. Implement

**Decisions & assumptions**

- **Derived membership, declared boundaries** — the id ceilings on the `PH1`, `PH2`, `PH3` and `WP2`
  bands are written down and the membership under them is a query. A ceiling that rebalanced itself
  would move a *finished* cycle's membership after the fact, and that cycle's coverage-ledger row
  would stop describing what the session read. So the tool reports an oversized cycle and a person
  cuts it, which is `tools/check_all.py`'s shape exactly: the manifest is declared, discovery is
  derived, and disagreement between them fails — 2026-08-23
- **Not a gate in [`../tools/check_all.py`](../tools/check_all.py), and this was the one real
  choice here.** `PR-06`'s proposed remedy cites that file's failing partition, so wiring this into
  it is the obvious reading. It is wrong: this command fails when a tracked file belongs to no audit
  cycle, which is a defect in T-219's coverage and not in the release, and
  [`../docs/AUDIT-METHOD.md`](../docs/AUDIT-METHOD.md) section 1 states that no audit is a release
  step. A new project document would have blocked a release it has nothing to do with. **So the
  failing half rides on the command a cycle already runs**: `--cycle <n>` answers which files that
  cycle reads and reports the partition's verdict before it answers. Forty-one cycles remain, so it
  is asked forty-one more times — more coverage than a release gate would have given it, on a
  project that releases every few days. `NOT_RUN` carries the reason — 2026-08-23
- **The open/closed vocabulary is read from [`../.taskmd/config.md`](../.taskmd/config.md), not
  copied** — cycle 7 is *the unreleased work*, which is a question about status, and a second copy
  of a vocabulary disagrees with the first the day either changes (**L-13**) — 2026-08-23
- **Cycle 17 keeps the blindness fixture.** `PR-01` proposes cutting it out and that remedy is a
  hypothesis its implementer measures. Encoding the answer in the partition would settle it by
  tooling — 2026-08-23
- **A third failure direction was added during implementation, and it replaced a wrong one.** The
  plan asked for two: an unassigned file, and a rule matching nothing. The second is right for a
  **path claim** — a filename that matches nothing has moved or was mistyped — and wrong for a
  **query**: `Task(shipped_in="unreleased")` is empty the day after a release and full the day a
  task closes, and failing on that teaches a reader to ignore every verdict the file prints. It
  fired that way within a minute of being written. So a query no longer reports stale, and what that
  check was standing in for is caught directly: **a cycle that owns no tracked file and gives no
  reason for owning none**. Six own none and say why. The case worth having is subtler than either —
  a cycle emptied because an earlier cycle's rule took its only file, which is a subject nobody reads
  and which shows in the table as a row of zeroes — and the self-test asserts exactly that one, after
  its own first fixture failed on it — 2026-08-23

**What the derivation found**

Three things, and the middle one is the finding `PR-06` could only state in aggregate.

- **Every tracked file is now in exactly one cycle**, and `python tools/docs/cycles.py` is what says
  so. It read 500 files and 8,902,955 bytes on 2026-08-23, against the plan's 492 and 8,786,384
  measured 2026-08-22 — the tree grew by this task's own record, its tool, its lesson and the edits
  they caused. **Re-run rather than cite**: this file is itself in cycle 7, so any figure written
  here moves when the file does.
- **Half the discrepancy is located, to the byte.** `shell/README.md` is 6,380 bytes and was counted
  in **both** cycle 1 and cycle 16. Cycle 1 stated seven files and derives seven; cycle 16 stated
  ten and derives nine, and the residue is 278,973 − 272,593 = **6,380**, which is that file exactly.
- **The other half is not locatable, which is `PR-06`'s sharper claim proven rather than asserted.**
  Cycle 4 states six files and 69,189 bytes. Its subject names four —
  [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md), [`../docs/RELEASE-HISTORY.md`](../docs/RELEASE-HISTORY.md),
  `.gitignore`, `.gitattributes` — which came to 54,768 bytes at the plan's own commit. No pair of
  tracked files matches the remaining 14,421: the obvious candidates,
  [`../docs/AUDIT-METHOD.md`](../docs/AUDIT-METHOD.md) and
  [`../docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md), were 3,450 and 2,137 there.
  `git ls-tree -r -l 3d08f2b -- docs/PUBLISHING.md docs/RELEASE-HISTORY.md` prints the first two.

**So the aggregate understated it.** The plan's thirty-seven sized rows sum to 491 files while
covering at most **488 distinct** ones — one counted twice, two the document cannot name — against
492 tracked. **Four tracked files were in no cycle at all**, not one, and the two errors ran in
opposite directions and partly cancelled, which is why the total looked one short. Which four cannot
be recovered from the document; that is exactly why the remedy was a command and not a corrected
table. The reusable half is **L-136**: a count with no membership cannot be audited, and a small
discrepancy between two totals is the residue of the mistakes rather than their size.

**Two boundaries moved, and one of them had to**

- **`0.6.0` shipped the morning the plan was being read.** Eighteen `PH3` tasks that were unreleased
  when the plan was measured are now closed, all above `T-164`. Cycle 7 — *the unreleased work* —
  falls from 18 files to 5, and they land in the last `PH3` band, which reached **39 files and
  465,531 bytes** against the ~300 KB a cycle is sized to. The five `PH3` ceilings were re-cut to
  326,610 / 339,137 / 327,529 / 326,197 / 301,841 bytes. **None of the five had run**, so no
  coverage-ledger row describes a membership that has since changed.
- **Cycle 22 gained `L-134` and `L-135`**, written after the plan was measured. `L-135` is the
  lesson `PR-06`'s own remedy cites.

**Outputs produced**

- [`../tools/docs/cycles.py`](../tools/docs/cycles.py) — the partition, its self-test, and the two
  failure directions.
- [`../tools/check_all.py`](../tools/check_all.py) — one `NOT_RUN` entry, with why it is not a gate.
- [T-219](T-219-pre-release-audit-of-the-whole-repository.md) sections 1 and 2 — both tables
  regenerated from the command.
- [`../docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) — `PR-06` closed against this task.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every tracked file assigned to exactly one cycle, by rule | met | `python tools/docs/cycles.py` prints 498 of 498 assigned, 0 unassigned, 0 stale, exit 0. First match wins, so *exactly one* is structural rather than checked afterwards |
| Both failure directions proven against the real rule set | met, and there are three | Pointing cycle 3's rule at a name the tree does not carry reports **both** at once — the renamed rule as stale, and [`../docs/BRIEF.md`](../docs/BRIEF.md) as unassigned — which is one moved file producing both symptoms, the pair that has to fire together or neither is trustworthy. §3 records the third direction and why the second was too broad as written. The self-test asserts five states on a fixture of its own, so a green run is not a claim about the instrument (**L-04**) |
| T-219's two tables regenerated from the command | met | `--plan` emits section 2's Files and Bytes columns; the default run emits section 1's grade table. Both come from one partition, so they cannot disagree |
| The two figures located, or shown unlocatable | met | `shell/README.md` located to the byte in cycle 16; cycle 4's residue of 14,421 bytes matches no pair the subject can name, at the plan's commit or today. Section 3 carries both commands |
| No oversized cycle left | met | The `PH3` bands were re-cut from a worst case of 465,531 bytes to five between 301,841 and 339,137. `cycles.py` now reports any cycle over 350,000 bytes as `OVERSIZED` — an advisory, since the ~300 KB figure sizes a sitting rather than gating one |

**Child fix tasks raised**

- none. This is itself `PR-06`'s child fix.

**What this could not settle**

- **Which four tracked files the plan left unread.** The document states counts, so the membership
  was never written down and cannot be recovered — only re-derived, which is what now happens. The
  audit loses nothing by it: no cycle beyond 0 and 1 had run.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-23 | → proposed | Raised as `PR-06`'s child fix, ahead of cycle 40's triage, because the finding gates every remaining cycle rather than only the run's closing claim. |
| 2026-08-23 | → specified | Scope fixed against the finding's own remedy hypothesis: derive the membership, do not reconcile the tables. |
| 2026-08-23 | → planned | Five steps. Step 3 is the one that matters — the comparison is what turns a hypothesis into a measurement, per **L-90**. |
| 2026-08-23 | → in_progress | `tools/docs/cycles.py` covers every tracked file. Half of `PR-06` located to the byte — `shell/README.md`, counted in cycles 1 and 16 — and half shown unlocatable, which was the finding's sharper claim. The plan covered at most 488 distinct files, so **four** were unread rather than one. The five `PH3` bands were re-cut after `0.6.0` pushed one to 465,531 bytes. |
| 2026-08-23 | (no change) | **The stale check was too broad and its own first firing said so.** A query with an empty answer is not a moved file. Path claims still fail; queries no longer do, and a cycle empty *without a stated reason* fails instead — which is what the wrong check was reaching for. The self-test's first fixture failed on the sharpest case of it, a cycle emptied by an earlier cycle's precedence, and now asserts it. |
| 2026-08-23 | → done | All five criteria met, the third recorded as met with a correction rather than reworded to match the output (§2's rule). `PR-06` closed in the register with the first row of its phase-2 table: **the remedy's own prediction was refused** — the counts did not reconcile, and the finding had understated itself four to one. **L-136** carries the general shape. |
| 2026-08-23 | (no change) | **A defect in this tool, found by cycle 6 and fixed there.** Front matter was split on the substring `---`, and [T-107](T-107-quickviews-markdown-renderer-drops-thematic-breaks.md)’s title quotes it — so that record parsed with no `status` and no `work_package`, and a `PH1` task was assigned to the band for the two stubs that predate the field. **The partition stayed complete and one file was in the wrong cycle**, which is the failure mode a coverage count cannot show and which only a second reading of the same fact caught: cycle 6 cross-checked [`../docs/RELEASE-PHASES.md`](../docs/RELEASE-PHASES.md)’s rows against the records and got one answer it could not explain. The fence is now matched as a whole line, the case is asserted in the self-test, and `T-107` sits in cycle 28. |
