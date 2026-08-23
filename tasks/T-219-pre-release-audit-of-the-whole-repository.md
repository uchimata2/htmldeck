---
id: T-219
title: Pre-release audit of the whole repository, project and product
type: audit
status: in_progress
phase: implement
parent: null
blocked_by: []
related: [T-218, T-042, T-119, T-130, T-153]
work_package: PH3
owner: the project owner
business_value: high
effort: xl
created: 2026-08-22
updated: 2026-08-23
deliverables:
  - docs/PRE-RELEASE-AUDIT.md
---

# T-219 — Pre-release audit of the whole repository, project and product

## 1. Specify

**Trigger**

The owner asked for one on 2026-08-22. **Reordered the same day: the release is cut first and the
audit follows it.** That release was `0.6.0` and it was cut on 2026-08-23, so **this run now precedes
the next release**, whichever digit it takes. The reason
for the audit is unchanged — the
project has accumulated features, generated files, changed documents, updated statuses and settled
decisions faster than any one pass has reconciled them, and that is the condition under which
contradictions survive unnoticed.

**Outcome**

A ranked register of every defect the method can see, a child task for every High and Medium, a
recorded decision against every Low, and a graded account of whether the ranking was worth obeying.

**Scope**

- In: all four aspects of [`../docs/AUDIT-METHOD.md`](../docs/AUDIT-METHOD.md) §2 — project method,
  project documentation, product documentation, and the product — plus the cross-cutting sweep.
- In: every tracked file, plus two surfaces outside git — the working directories `.gitignore` names,
  and this project's memory and handoff record.
- Out: nothing is out by subject. Cycle 17 is out by *method*: the five shipped decks are audited by
  rendering and measurement, not by reading, because `CLAUDE.md` rule 6 forbids reading a deck whole.
- Out: fixing what is found. Remedies are child tasks, and a remedy is a hypothesis until it is
  measured (**L-90**).

**Coverage grades** — [`../docs/AUDIT-METHOD.md`](../docs/AUDIT-METHOD.md) §2. **Both this table and
§2's are printed by `python tools/docs/cycles.py`, which assigns every tracked path to exactly one
cycle and fails when one belongs to none.** They are not kept by hand and are not reconciled against
each other: they have one source, so they cannot disagree. Re-run it rather than cite the cells — the
figures below are a dated snapshot for sizing sessions, taken 2026-08-23, and **L-95** point 4 is why
that is the honest form.

| Grade | What it applies to here | Files | Bytes |
| :--- | :--- | ---: | ---: |
| A — wide | the product, the human-facing set, the current plan, open and unreleased tasks, the deck specifications | 122 | 2,896,037 |
| B — narrow | closed task records, lessons, research, the design rationale, the upstream reports | 373 | 4,235,609 |
| C — instrument only | the shipped decks and the blindness fixture | 5 | 1,773,568 |
| | **read (A + B)** | **495** | **7,131,646** |
| | **the tree** | **500** | **8,905,214** |

*These were 140 / 347 / 5 against a tree of 492 when the plan was written, and the two tables did not
reconcile — `PR-06`. They are derived from one partition now:
[T-223](T-223-derive-the-audit-cycles-membership-instead-of-counting-it.md) §3 has what the derivation
found, including the file the old §2 counted twice. **One residual self-reference the command cannot
remove**: this file is itself in cycle 7, so writing a number here changes the number. The command is
right at the moment it runs and the table is right at the moment it was pasted, which is what makes
`--cycle 7` the thing to run rather than this row the thing to read.*

**Register**

[`../docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) — id space `PR-nn`, scaffolded by
[T-218](T-218-record-the-pre-release-audit-method-and-its-machinery.md) and owned here.

**Acceptance criteria**

- [ ] Every tracked file is read, skipped with a stated reason, or produced a finding, and the
      register's coverage ledger says which for every cycle.
- [ ] Every finding carries the command that proves it.
- [ ] Every High and Medium finding has a child task; every Low is batched or accepted with a reason
      and a date.
- [ ] No High finding is open when the release is tagged.
- [ ] Cycles 1, 3 and 5 are re-run after the last remedy lands, and what the remedies broke is
      recorded.
- [ ] Phase 2 is written, and it names at least one prediction the measurement refused.

**Open questions**

- **`CLAUDE.md` gives two tests for tier 3 and they disagree** — *what tier 2 loads one at a time*
  admits a method document, *never to start work of a kind* excludes it. T-218 ruled on precedent so
  the work could proceed; cycle 3 decides whether the definition is the defect. Owner answers.
- **Stage 7 is 3,366,873 bytes of closed record across twelve cycles — 47% of the reading for the
  least current subject.** The program is ordered so that stopping after cycle 26 leaves the audit
  complete over everything a reader, an adopter or the next release touches. Whether to spend
  stage 7 is a checkpoint decision, not a planning one. Owner answers, at cycle 26. *It read
  3,046,859 and 44% when the plan was written; `0.6.0` closed eighteen tasks into it on 2026-08-23,
  which is the share growing while nobody decided anything.*
- **Which release this precedes.** `0.6.0` is published; the digit the next one takes is
  [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) §8's rule and is not this audit's to set.

## 2. Plan

**The cycle program.** Forty-three cycles in nine stages, ordered by expected finding density rather
than by directory, each sized to about 300 KB of source
(the taskmd skill's `pre-release-audit.md`). **A cycle is a session boundary**: it may
be run alone, and it ends at a commit with the register written.

**The Files and Bytes columns are printed, not typed.** `python tools/docs/cycles.py --plan` emits
them; the rule that decides which files a cycle owns lives in that file, one rule per cycle, and a
tracked path belonging to no cycle fails the command. **The Subject column is the input to those
rules and the Brief and Status columns are this table's own** — so a re-cut boundary is edited here
*and* there, in one change, and nowhere else.
[T-223](T-223-derive-the-audit-cycles-membership-instead-of-counting-it.md) is why, and `PR-06` is
what it cost to find out.

| # | Subject | Files | Bytes | Brief | Status |
| :-- | :--- | ---: | ---: | :--- | :--- |
| **0** | **Instruments and baseline** | **4** | **62,058** | Freeze the tree. `check_all.py` and `lint.py` green, both recorded with their elapsed time. Generalise `findings.py` to discover registers, or record `parent:` as the fallback and why. | **done** |
| | *Stage 1 — what an adopter receives.* Highest density: it is the oldest text about the fastest-moving tree. | | | | |
| 1 | The human-facing set | 7 | 55,103 | Every claim in `README.md` against the tree — it says *two decks* and three are shipped. The install lines run. The humanizer test of `PUBLISHING.md` §2 still holds. `LICENSE` and the marketplace manifest agree with the plugin manifest. | **done** |
| 2 | The skill and the prompt | 6 | 58,890 | What an adopter's tier 1 receives through the skill description. Every `${CLAUDE_PLUGIN_ROOT}` path resolves in a copied directory. The four reference documents agree with the tools they describe. | **done** |
| | *Stage 2 — how this project governs itself.* | | | | |
| 3 | Tier 1 and the brief | 2 | 60,449 | The tier definitions against each other and against what a session is actually given. The bound's two terms re-measured. `BRIEF.md`'s *Decisions taken* against what shipped. | **done** |
| 4 | The release machinery | 4 | 60,607 | `PUBLISHING.md` §8's eight steps against how `0.5.0`, `0.5.1` and `0.6.0` actually ran. §8.1's `*next*` row. `RELEASE-HISTORY.md` against the tags. What `.gitignore` hides that should ship, and what it fails to hide. | pending |
| 5 | The tracker's own rules | 7 | 112,267 | `TASK-WORKFLOW.md`, `TOOLING.md`, the two templates and the schema against each other and against 219 task files. Which conventions are gated and which are only written down. | pending |
| 6 | The release plan | 1 | 179,575 | 177 KB of phase decision against the phases as they ran. Rows for tasks that changed shape, counts that moved, and the PH3-takes-everything rule against what PH3 now holds. | pending |
| 7 | The unreleased work, and this audit's own record | 6 | 97,443 | What the next release contains, read as an adopter would meet it. Every open record against the code that will close it, plus `AUDIT-METHOD.md` and the register. *It was 18 files when the plan was written and is 6 now: `0.6.0` shipped on 2026-08-23 and took the other 13 into cycle 34, [T-218](T-218-record-the-pre-release-audit-method-and-its-machinery.md) among them. The cycle did not shrink — its subject moved, which is what a membership derived from `status` does and a count could not.* | pending |
| | *Stage 3 — the product.* | | | | |
| 8 | The design system and the evaluation | 2 | 146,650 | Every `DS-nnn` against `check.py`'s coverage: decided, named-with-a-reason, or neither. The ten evaluation dimensions against what any instrument can reach. | pending |
| 9 | The three contracts | 3 | 76,319 | Component, theme and motion contracts against the shell that implements them and the checkers that decide them. A contracted part nothing enforces. | pending |
| 10 | The gate's code | 9 | 240,446 | 122 rules, 92 decided. Whether each undecided rule's stated reason is still true, and whether any decided rule decides something other than what it says. | pending |
| 11 | `audit.py` and `critique.py` | 2 | 198,718 | 182 KB in one file. What is dead, what is duplicated from `check.py`, and whether the stage-1/stage-2 split still matches `EVALUATION.md`. | pending |
| 12 | The build path | 7 | 268,414 | Spec to shell to render to deck. Where a failure is silent, where a path is assumed, and what the presenter build shares with the deck build. | pending |
| 13 | The rest of `tools/deck/` | 14 | 270,560 | Fourteen tools. Which are reachable from a documented command, which are only reachable from a task record, and which are neither. | pending |
| 14 | `tools/docs/` | 5 | 187,164 | The four checkers that read documents. `figures.py` is 99 KB and every pasted figure in the tree depends on it. `refcheck.py`'s skip list. | pending |
| 15 | The remaining tools | 9 | 265,632 | Assets, portability, examples, kb, plugin scaffold. `check_all.py`'s partition says every one of these is classified — verify that against what each actually does. | pending |
| 16 | The shell and the themes | 9 | 272,593 | 85 KB of CSS and 51 KB of JavaScript that every shipped deck embeds. Dead selectors, tokens nothing reads, a theme value that is not parametric. | pending |
| | *Stage 4 — the decks.* | | | | |
| 17 | The five shipped decks | 5 | 1,773,568 | **Grade C.** Render each offline and look at it. `check.py`, `audit.py`, `printgeom.py`, `glitchfree.py`. Print two and read the paper. No deck is opened as a file. | pending |
| 18 | The deck specifications and sources | 25 | 301,861 | Each specification against the deck built from it, and each source against what the deck claims it says. The sanitisation rule on the adopter deck. | pending |
| | *Stage 5 — the record.* | | | | |
| 19 | The prior audits | 2 | 119,302 | `CONTEXT-AUDIT.md` and `RULESET-AUDIT.md`: is every row that reads closed actually closed, and does every open row still describe the tree? `findings.py --check` decides part of this and not all of it. | pending |
| 20 | The design rationale | 1 | 69,194 | **Grade B.** A decision recorded here that the product no longer implements. | pending |
| 21 | Lessons `L-01`–`L-77`, and the index | 78 | 167,650 | **Grade B.** A lesson whose mechanism the tree no longer has. The index against the files. | pending |
| 22 | Lessons `L-78`–`L-133` | 59 | 158,429 | **Grade B.** As cycle 21. | pending |
| 23 | Research `R1`–`R4` | 5 | 153,311 | **Grade B.** A finding the build later contradicted, and a candidate rule that never became one. | pending |
| 24 | Research `R5`–`R9`, upstream, sketches | 9 | 200,850 | **Grade B.** `R8` against `AUDIT-METHOD.md`. The three upstream reports against what those projects did. An orphan sketch. | pending |
| | *Stage 6 — outside git.* | | | | |
| 25 | Memory and the handoff record | - | - | Every memory entry against the tree it describes — a named file, function or flag that no longer exists. The index against its entries. The handoff config, and whether the processed chain still holds anything unreconciled. | pending |
| 26 | The untracked surface | - | - | What `.gitignore` hides: anything that should be tracked, anything that must never publish, and anything left behind by a tool that no longer runs. `.claude/settings.local.json`. **Checkpoint: the owner decides here whether stage 7 runs.** | pending |
| | *Stage 7 — the closed record, Grade B.* One question per file: does anything written here contradict the tree today? | | | | |
| 27 | `PH1` closed, `T-002`–`T-085` | 14 | 273,368 | | pending |
| 28 | `PH1` closed, `T-086` onward | 30 | 277,369 | | pending |
| 29 | `PH2` closed | 21 | 293,976 | | pending |
| 30 | `PH3` closed, up to `T-113` | 20 | 326,610 | | pending |
| 31 | `PH3` closed, `T-114`–`T-135` | 19 | 339,137 | | pending |
| 32 | `PH3` closed, `T-136`–`T-153` | 18 | 327,529 | | pending |
| 33 | `PH3` closed, `T-154`–`T-186` | 24 | 326,197 | | pending |
| 34 | `PH3` closed, `T-187` onward | 25 | 301,841 | | pending |
| 35 | `WP2` closed, up to `T-032` | 11 | 215,435 | | pending |
| 36 | `WP2` closed, `T-033` onward | 6 | 181,144 | | pending |
| 37 | `WP1` closed | 11 | 181,895 | | pending |
| 38 | `WP3`, `final`, `none`, and the two cancelled stubs | 20 | 322,372 | | pending |
| | *Stage 8 — synthesis.* | | | | |
| 39 | The figure and version sweep | - | - | Every number, count and version string in the tree against what the tree is. Scripted first, then read: `figures.py` decides the fenced ones and **L-05** is the family it cannot see. | pending |
| 40 | Triage, rank, raise the tasks | - | - | Severity and its obligations per the taskmd skill's `pre-release-audit.md`. Child tasks for High and Medium; one batch task or an accepted row for each Low. | pending |
| 41 | Re-read what the remedies changed | - | - | Cycles 1, 3 and 5 again, plus every cycle a remedy touched. **This is where an audit's own damage shows.** | pending |
| 42 | Phase 2 | - | - | Predicted against measured, per finding. It has to name at least one prediction the measurement refused, or it was not run honestly. | pending |

**How to run one cycle in a fresh session**

1. Read [`../docs/AUDIT-METHOD.md`](../docs/AUDIT-METHOD.md), this section, and the register.
2. `python tools/docs/cycles.py --cycle <n>` — the file list, with its bytes. **It reports the whole
   partition's verdict before it answers**, so a tracked file that has fallen outside every cycle
   stops the reading rather than surviving it. Read what it names.
3. Append rows to the register, and one row to its coverage ledger — including *no finding*, with
   what was checked.
4. Set the cycle's status here, commit, stop. **Never leave a cycle half-read and unwritten.**

## 3. Implement

**Decisions & assumptions**

- **`parent:` is the fallback for the finding-to-task link, and no task may carry `finding: PR-nn`** — `tools/docs/findings.py` is bound to [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md)'s table *shape*, not merely its path: closure is a struck-through rank cell and the bands are read from fixed column positions, where [`../docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3 signals closure in a `Status` column and carries different columns entirely. Generalising is a second reader, and it would be written against a table that has never held a row. Proven rather than assumed — a task carrying `finding: PR-01` yields exactly one problem and `lint.py`'s fourth step exits 1:
  `python -c "import importlib.util;s=importlib.util.spec_from_file_location('f','tools/docs/findings.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);print(m.link(m.findings(m.read(m.AUDIT)),{'T-900':('proposed','PR-01')},m.open_statuses())[1])"`.
  The cost is the one [`../docs/AUDIT-METHOD.md`](../docs/AUDIT-METHOD.md) section 3 already states: the register's `Task` column stays hand-kept and drifts. Revisit at cycle 40, where the child tasks are actually raised and the table's shape is settled by real rows — 2026-08-23
- **The gate timings are a dated record, not a stated figure** — section 2's brief for cycle 0 asks for the elapsed time, and `check_all.py` prints its own seconds precisely so that no document holds them (**L-95**, `CE-08`). [`../docs/lessons/L-95.md`](../docs/lessons/L-95.md) point 4 resolves it: a dated measurement in a byproduct register is history and stays true, where *the gate takes N s* in a live document decays. So the register's baseline row names the commit and the date and says to re-run rather than cite. Measured 294.5 s today against the 154 s L-95 records for 2026-08-14 — the drift is the rule working — 2026-08-23
- **`taskmd check`'s eleven advisories are baselined, not raised** — it exits 0 and still prints a duplicate-index line for [`../docs/RELEASE-PHASES.md`](../docs/RELEASE-PHASES.md) and ten unresolved section references. By subject they are cycles 5 and 6's; recording them in the baseline is what lets a later cycle tell a new advisory from an old one — 2026-08-23

**Findings raised**

Counts only; the statements live in the register.

| Severity | Raised | Tasked | Accepted | Open |
| :--- | ---: | ---: | ---: | ---: |
| High | 2 | 0 | 0 | 2 |
| Medium | 11 | 1 | 0 | 10 |
| Low | 1 | 0 | 0 | 1 |

**Child tasks raised**

- [T-223](T-223-derive-the-audit-cycles-membership-instead-of-counting-it.md) — `PR-06`, raised and closed ahead of cycle 40 on the owner's instruction of 2026-08-23. **The rule that triage waits for cycle 40 is unchanged**; what makes this one an exception is the same clause `PR-01` carries, that the finding gates cycles rather than only the run's closing claim. `PR-06` gated *every* remaining cycle, because section 2's step 2 asks for a file list the document did not hold.
- Everything else waits for cycle 40, which is where section 2 puts the triage. `PR-01` is the remaining exception in waiting: its remedy has to land before cycle 17 runs.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Phase 2**

<Where the grading is recorded, and the one sentence it reduces to.>

**What this run could not see**

- <a limit met in practice, beyond the method's §10 list>

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-22 | → proposed | Requested by the owner before the next release after `0.5.1`. |
| 2026-08-22 | → specified | Scope, grades and the register fixed against [T-218](T-218-record-the-pre-release-audit-method-and-its-machinery.md)'s method. Three questions left open, each with who answers it. |
| 2026-08-22 | → planned | Forty-three cycles in nine stages, measured from the tree. **Left here deliberately**: the owner asked for the audit to be specified and planned, and not executed. |
| 2026-08-22 | (no change) | The method moved to taskmd ([T-218](T-218-record-the-pre-release-audit-method-and-its-machinery.md)); §2's cycle programme stays here, because taskmd's `audit.md` puts a given audit's procedure in its own plan. |
| 2026-08-22 | (no change) | **The owner reordered it: cut the release first, run the audit after.** So this task no longer gates the next release, and its findings are expected to carry the one after — the owner's expectation is a **minor**, which [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) §8's digit rule decides at the time and §8.1's row is the evidence for. The side effect is welcome: the run now starts after taskmd [PR #2](https://github.com/uchimata2/taskmd/pull/2) is settled, so it reads one method rather than a local draft. |
| 2026-08-23 | (no change) | **That precondition is settled.** [PR #2](https://github.com/uchimata2/taskmd/pull/2) merged 2026-08-22 and its `pre-release-audit.md` shipped in taskmd `0.6.0` on 2026-08-23, at 11,371 bytes — so a run reads one method, upstream, and the six rules §2's programme was written against are now fixed text rather than a draft. **Still not started; the owner's request opens it.** Two things a session must check first: the installed taskmd must be `0.6.0` or later, and the `finding:` tool gap was **not** closed upstream, so cycle 0 still owns it. |
| 2026-08-23 | (no change) | **The release position moved, because the release it was reordered behind has been cut.** §1 read *the release after next*, written when `0.6.0` was next; `0.6.0` shipped 2026-08-23, so §1 and [`../docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) §1 now both say **the next one**, and §1's open question names `0.6.0` as what is published. Cycle 4 gained `0.6.0` to its list: a cycle auditing the release machinery against every release but the newest one is a gap the plan would have carried in silently. The dated rows above keep their words. |
| 2026-08-23 | — in_progress | **Cycle 0 is done and the run is open.** Tree frozen at `62c3ab3`; `check_all.py` and `tools/tasks/lint.py` both green and recorded in [`../docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 1. The cycle re-measured its own four files and they came to the planned 61,356 bytes exactly, so the count the handoff warned might have moved did not move here. The `finding:` gap is settled locally rather than upstream — [taskmd T-247](https://github.com/uchimata2/taskmd/blob/master/tasks/T-247-decide-whether-taskmd-validates-a-finding-field-against-a-register.md) is still `proposed` — and section 3 carries the decision, its proof and the trigger to revisit. One Medium finding, `PR-01`, and its subject is this task's own section 2. |
| 2026-08-23 | (no change) | **Cycle 1 done: the human-facing set.** Four findings, and the one that matters is `PR-02` — `examples/portfolio-review/` is a tracked, gated, 397,867-byte deck that appears in neither `README.md` nor `examples/README.md`, while the front page's table promises *every shipped deck* and sends the reader to the second. `0.6.0` shipped with that claim already false, which is why it is the run's first High. `PR-03` and `PR-04` are the front page's other stale numbers, `PR-05` a Low batched from [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) section 2 while it was being applied as the authority for the covered set. **The cycle's own subject moved**: 54,585 bytes at the plan's commit against 55,103 today, because both READMEs grew on 2026-08-22 after the plan was measured — the re-measure section 2 requires is what caught it, and cycle 0's list had not moved at all. |
| 2026-08-23 | (no change) | **`PR-06`: this task's own two tables do not reconcile.** Section 1's grade table says the tree is 492 files and 8,786,384 bytes; section 2's thirty-seven sized cycles sum to 491 and 8,769,356, and the six unsized cycles cannot absorb the difference. No tracked file is 17,028 bytes, then or now, so it is one unreconciled measurement and not one omitted file — and section 2 states a count per cycle without a membership, so the document cannot locate it. Raised between cycles 1 and 2 by summing this file, so no coverage-ledger row carries it. The remedy proposed is **L-135**'s: derive the boundaries and let a command decide the partition, rather than hand-reconcile two tables. |
| 2026-08-23 | (no change) | **`PR-06` is settled, and the plan's coverage is now derived.** [T-223](T-223-derive-the-audit-cycles-membership-instead-of-counting-it.md) assigns every tracked path to exactly one cycle by rule; `python tools/docs/cycles.py` covers 499 of 499 and fails on a file no cycle claims. **Half the discrepancy is located to the byte** - `shell/README.md`, 6,380 bytes, counted in cycles 1 and 16 - and half is shown unlocatable, which was the finding's sharper claim. The plan's 491 covered at most **488 distinct** files, so four were unread rather than one. Section 1's grade table and section 2's Files and Bytes columns are printed by that command now. **Two boundaries moved**: cycle 7 fell from 18 files to 6 because `0.6.0` released its subject, and the five `PH3` bands were re-cut off a worst case of 465,531 bytes. None of the five had run. |
| 2026-08-23 | (no change) | **Cycle 2 done: the skill and the prompt.** Four findings, and the one that matters is `PR-07` — [`../README.md`](../README.md) tells an adopter that copying `skills/htmldeck/` works because every path goes through `${CLAUDE_PLUGIN_ROOT}`, and **not one does**: all 22 go through `$HTMLDECK`, which [`../skills/htmldeck/SKILL.md`](../skills/htmldeck/SKILL.md) section 0 resolves by a glob that only finds an installed htmldeck or a clone. The route the front page offers has no resolver. `PR-08` is two bare `python tools/...` commands that survived T-189, in documents a build loads, past a check written for exactly that and keyed on the variable the skill now forbids. `PR-09` and `PR-10` are the same shape as `PR-04`: three documents disagreeing on how many fields a slide has, and two wrong hard-rule counts ten lines apart — both in files `figures.py` does not watch. **The subject re-measured to the planned 58,890 bytes exactly**, the first cycle whose figure has not moved, and the first taken from `cycles.py --cycle 2` rather than by hand. |
| 2026-08-23 | (no change) | **Cycle 3 done: tier 1 and the brief.** Four findings, and `PR-14` is section 1's own open question answered: [`../CLAUDE.md`](../CLAUDE.md)'s two tests for tier 3 disagree on [`../docs/AUDIT-METHOD.md`](../docs/AUDIT-METHOD.md), and the disagreement is arithmetic — as a tier-2 term it takes the bound's floor from 13,324 to 4,430 and the stated debt from 2,248 to **11,142**. The owner decides which test governs. `PR-11` is tier 1's own figure for the shipped decks, wrong by one deck and 640,565 bytes; `PR-12` is seven stale ruleset counts sitting inside the sentence that says to re-derive them; `PR-13` is *under 200 KB* in the shipped skill against four decks averaging 363 KB. **Four claims were checked and hold exactly**, which is worth recording as loudly as the failures: the three files a session receives unasked, the bound's two terms and its 2,248-byte debt, the gate's 92 of 122 with 30 named, and `0.6.0` as published. |
