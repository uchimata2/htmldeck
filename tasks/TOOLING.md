# Tooling — htmldeck

**What validates the work here, what each check enforces, and the two writing rules the checkers
implement.** Split out of [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) on 2026-08-14 by
[T-147](T-147-one-workflow-file-per-lifecycle-phase.md), for finding `CE-09`: it was **55% of a
document every task reads**, and it grows with every tooling change while the workflow around it does
not. No rule was rewritten in the move.

**The old addresses still work.** `TASK-WORKFLOW.md` §6, §6.1 and §6.2 are cited 65 times across the
record and keep their numbers and titles there as pointer sections — a heading removed is a citation
falsified, with nothing to say so (**L-39**). Sections 1, 2 and 3 below are those three, in order,
and are new addresses that nothing cites yet.

---

## 1. The tooling

Two tools, and the split between them is what they are about:

```
taskmd list --open --limit 1     # what to work on next, by the config's ordering rule
taskmd context T-NNN             # everything needed to start one task
taskmd index                     # regenerate the tables in tasks/README.md
taskmd check                     # validate the task record

python tools/docs/refcheck.py    # validate every reference in every document
python tools/docs/findings.py    # which audit finding is which task, and what state is it in
```

**The bare `taskmd` command does not resolve in an agent shell**, which is a property of how the
plugin is put on `PATH` rather than of the plugin — **measured 2026-08-13 and it is neither the
plugin's fault nor this project's**: taskmd ships `bin/taskmd`, it runs when invoked directly, and
the harness does emit its directory into the shell snapshot, whose `PATH` line is then truncated
mid-value and loses every plugin (**L-87**, `O-C1`). So the four `taskmd` lines above are what to
type at a terminal, and not what an agent can run. Two commands here run them, and between them they
cover all four:

```
python tools/tasks/lint.py                  # index, check, refcheck.py, then findings.py --check
python tools/tasks/query.py list --open     # what to work on next
python tools/tasks/query.py context T-NNN   # everything needed to start one task
```

**Never run `lint.py` and `tools/check_all.py` at the same time.** `lint.py`'s first step is
`taskmd index`, which **rewrites `tasks/README.md`**, and the release gate reads that file — so a gate
started beside the lint reads a board mid-write and fails on it. **Observed 2026-08-15: two failures
from a concurrent pair, and zero from the same tree run alone**, 172 s against 157 s. The failure names
were lost to a tail, so the mechanism is inferred from the write rather than proven from the output;
what is certain is that the two runs disagreed about one tree. The trap is that both commands are slow
enough to want to overlap and the gate is the one told to run in the background. **Lint first, let it
finish, then gate.**

`lint.py` is the four checks a task edit owes: it stops at the first failure and exits with that
failure's code, and it is `tracker_lint` in [`../.handoff/config.md`](../.handoff/config.md).
**It is also the only name tier 1 gives**: [`../CLAUDE.md`](../CLAUDE.md) enumerated the checkers
until 2026-08-14 and the list went stale both times the set changed, so it points here and this
section carries the count.
`query.py` is the two questions: everything after the command name goes to taskmd untouched, and it
refuses `index` and `check` by name because `lint.py` owns those. Both find the installed skill
through one locator, in `lint.py`, so the incantation has one home rather than one per document
(**L-13**).

**An agent asks the board a question; it does not read the board.** [`README.md`](README.md) is
generated for people, and answers *what next* only by being read whole — **36,559 bytes on
2026-08-13, against 94 for `query.py list --open --limit 1` and 716 for one task's `context`**.
Reading it whole to find the next task is the finding `CE-02` names and
[T-131](T-131-expose-the-trackers-query-commands-so-the-board-is-not-read-whole.md) closed.

`taskmd` owns tasks. `refcheck.py` owns **documents**, and exists because taskmd's check sees
markdown-link syntax only: a path written as prose, a path printed by a tool into a fenced block, and
every `§n` reference are all invisible to it. Measured against seeded defects, not assumed — the
comparison is in [T-062](T-062-retire-the-pre-split-task-tool-and-repoint-what-points-at-it.md) §1.

`findings.py` owns the **join** between the two — which audit finding is which task. The link is a
`finding: CE-nn` field in task front matter, carried by the schema and never interpreted by it, so
the finding rows in [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6 stay where their
argument is and nothing is copied anywhere. Run bare it prints the listing; `--check` is the gate,
and it fails in both directions (**L-74**) — a row reading closed while open work names it, a row
reading open when every task on it is finished, and a task naming a finding that does not exist. It
also asserts [`../docs/RELEASE-PHASES.md`](../docs/RELEASE-PHASES.md)'s execution order is numbered
`1..n` with no gap. **Two markers in the documents drive it**: a struck-through rank cell means
closed, and an Effort cell ending in `each` means the band is per item, so a closed row is not a
finished subject — `CE-04` is the instance and it kept a task open after its row closed.
[T-151](T-151-generate-the-finding-to-task-listing-instead-of-keeping-it-by-hand.md).

**`index` rewrites only the block between its generated markers**; hand-written sections of
`README.md` survive it. `check` reports a stale index and does not fix it, so run `index` after any
task edit.

**Generated views count only open tasks as gated** — the rule, and it is currently observed by
`list` and `context` and **not** by `index`. Both directions of an edge should be filtered the same
way: a closed task neither gates anything nor waits on anything, so it belongs in neither a *Blocked
by* nor a *Blocks* column. `context` keeps them, with their status, because they are the trail
explaining why the task exists. Stated here because it was previously implied by two comprehensions
that disagreed with each other, which is how it survived being read repeatedly (**T-031**, **L-08**).

**It stopped being true on the day the tool changed, and was true again five weeks of releases
later — on 2026-08-10, both within a day.** This paragraph described `task.py`, which filtered both
columns; taskmd's `index` did not, so three rows named a closed blocker while `taskmd list --open`
ranked them free. [T-079](T-079-the-boards-dependency-columns-list-closed-tasks.md) sent that
upstream as their **T-111**, they accepted it, and **taskmd 0.3.0 filters both columns**: T-019's
*Blocked by* is empty where it read `T-002`, and T-084's *Blocks* names `T-036` and nothing closed.
Measured on this board, not taken from a release note. The whole episode is left visible because a
rule that survived a tool swap unnoticed is the thing to recognise faster next time (**L-59**).

**What the two checks enforce**

- `taskmd check` — the vocabularies in the config; every `parent`, `blocked_by` and `related`
  reference resolves; `blocked` implies a dependency; no dependency cycles; a declared deliverable
  exists; the generated index is not stale; and markdown links resolve. **Since 0.3.0 it also holds
  the templates to the schema** — a `_`-prefixed file offering a field value the config does not
  allow, or sitting where `create` will not find it, is a failure. All three of this project's were,
  on the day it was installed. It now reads **only the documents a clone would receive** and prints
  how many it skipped, so a gitignored working file can no longer fail the run.
- **One advisory is expected on every run, and is ignored by the file it names.** taskmd 0.5.0's
  `DUPLICATE INDEX` counts the distinct known task ids a non-task document names outside the generated
  markers, and fires when they are a majority of the board:
  [`../docs/RELEASE-PHASES.md`](../docs/RELEASE-PHASES.md), **105 of 151 on 2026-08-14**, both numbers
  climbing with every release. That document is the decision record — one row per task, each carrying
  a *why it is in this phase* the generated board does not hold, struck-through rows kept on purpose.
  The content is right and the count is right at the same time. **So the line is read by file name,
  not by rule: a `DUPLICATE INDEX` naming any other document is a real second board and is not covered
  by this.** [T-098](T-098-check-reports-briefs-phase-tables-as-a-second-index.md) took the decision
  and rejected both alternatives — splitting the tables out moves the count rather than lowering it,
  and no upstream exclusion was asked for, because a per-document opt-out is the one change that would
  make the advisory unbelievable everywhere it is right (**L-73**).
  **The named file changed on 2026-08-14 and the decision did not.** It read `docs/BRIEF.md`, **78 of
  105 on 2026-08-12**, until [T-145](T-145-move-brief-mds-release-phases-to-its-own-document.md) moved
  the tables to a document of their own for a read-path reason T-098 never weighed. T-098's refusal
  was the prediction that made this safe to check: the count **moved intact** — 105 ids to the new
  file, 22 left behind against a threshold of 76, so `BRIEF.md` stopped firing and the new file
  started. **Still one named file, so T-098's reopening condition — a *second* document legitimately
  tripping the advisory — is still not met** and no upstream exclusion is due.
- `refcheck.py` — every markdown link, **every repo-relative `.md` path written in prose or printed by
  a tool**, **every `<named document> §n` reference** (§2 below), and **every link *label* that names a
  `.md` file the link does not open** (§2.1). Two things are skipped and it prints
  how many: documents `.gitignore` excludes, which are machine-local by design and absent from a fresh
  clone; and front-matter, which is a structured record rather than prose.
- **A bare path that is not `.md` is checked by nothing, and now never will be.** `refcheck.py` matches
  `.md` only; taskmd's `check` sees markdown links and, as of upstream's answer to
  [T-063](T-063-improvements-to-propose-upstream-to-taskmd.md), will not resolve a bare path at all.
  So this repository names `tools/tasks/task.py` 46 times, in 22 task files, and the tool has not
  existed since T-062 — with all three gates green. **That is intended.** A task record naming a tool
  that was live when it was written is a correct dated statement, not a broken promise, and no path
  checker can tell the two apart; the alarm would be wrong every time.
  [T-073](T-073-decide-whether-to-keep-refcheck-now-that-upstream-has-ruled.md) §3 decided to leave
  them. What would be a real defect is a mention in **live instructional prose** — something telling a
  reader to run it — and there is none.
- **There is no exemption for declared deliverables.** Until T-029 there was: any path a task named in
  `deliverables:` was skipped *everywhere in the repository*, on the reasoning that a deliverable is a
  promise about the future. It was hiding **110 of 357 pointers**, because most declared outputs are
  long-existing documents that everything else cites (**L-05**).

**What neither does.** They validate structure and references. Neither can tell you a specification is
wrong, a plan is thin, or a deliverable is bad — and both say so in their own output rather than
reporting a clean pass (**L-05**).

## 2. Section references

A `§` is a pointer like any other, and until T-046 nothing resolved one — **1394 of them, against 614
links and paths that were all checked** (**L-39**). The rule has two halves, and both exist so that
the number a reference cites is **printed in the document it points at**, where a reader can verify it.

**When a reference is checked.** Only when the document is named **adjacent** to the mark —
`` `DESIGN-SYSTEM.md` §3.3 ``, a markdown link to a task followed by `§2`, or `R7 §5.3`. A bare `§4`
and a document named earlier in the paragraph are *not* a reference to that document: the citation
form does not bind them, and guessing produced wrong targets in every case tried. Unbound marks are
counted and reported as skipped, never silently dropped.

**When a reference resolves.** `§n` resolves when `n` is a heading. `§n.m` resolves when `n.m` is a
heading, **or** when `n` is a heading and `m` is an ordinal printed in a numbered list under it. That
admits both conventions already in use — `R7 §5.3` is item 3 of section 5, `DESIGN-SYSTEM §0.8` is
item 8 of section 0 — and needs no exception list, because it rejects `DESIGN-SYSTEM §9.4` and
`EVALUATION §0` exactly as it should. **A number that exists only as the reader's own count of an
unnumbered list is not an address and may not be cited.**

**Mentioning a section is not citing it.** A `§` inside a code span or a fenced block is literal text
and is not resolved — which is how a document quotes a reference that is *wrong*. The audit that found
this family had to write `` `DESIGN-SYSTEM.md §11` `` a dozen times to say it never existed; under any
other rule the record of a dead pointer is itself a dead pointer.

**Nor is showing a link following one**, and since 2026-08-12 both checkers agree. `[label](target)`
inside a code span or a fenced block renders as the characters typed: nobody can follow it, so nothing
can break it. taskmd stopped resolving it in 0.4.0 and `refcheck.py` in
[T-080](T-080-check-resolves-a-markdown-link-inside-a-code-fence.md), so a task file may now paste a
`taskmd index` row **verbatim, abridged filename and all**. Before that the checker did not find a
defect, it required the evidence to be edited — and a quotation adjusted to satisfy a link checker is
no longer a quotation, with nothing left to say it was adjusted.

**A bare path inside a fence is the opposite case and stays checked.** A tool printing
`docs/LESSONS.md` into a block makes the same promise a sentence does, and that check has caught real
defects — which is why blanket fence-skipping was never the ask, upstream or here. The two rules meet
at syntax, not at fences.

**This is why [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md)'s headings were not renumbered when it was
merged with METHOD.md**, and why they were not renumbered again when this section left it either.
Twelve task records cite `TASK-WORKFLOW.md` at §2 through §6.2 — **104 citations in 42 files when it
was counted on 2026-08-14**, which is the same argument with the real number in it. A renumbering is
a silent falsification
of all of them, and the check would have caught it — which is the rule working on the document that
defines it.

### 2.1 The label beside the pointer — and the mark that stays ungated

**Check 4 reads what the reader is told, not what the link opens.** Every other check in this
repository, and every check taskmd has, asks *does this file exist*; none asks whether the words
beside it are true. A link whose target is right and whose label names a different file passes all of
them. It was found twice by a person, the second time inside a pass raised to catch exactly that
class — the six instances, and what they share, are
[T-159](T-159-gate-the-text-a-reader-follows-and-no-checker-reads.md) §1.

The rule accepts **both** conventions in use here: a label written from the citing document's own
directory, and one written from the repository root. Either resolving to the target is honest. A
third answer is not. Accepting only one convention would turn a house style into hundreds of
failures, which is why the honest shapes are asserted in the self-test beside the defect one.

**Every run prints how many labels name a path, not only how many disagree, and the first number is
the check's liveness signal.** It is in the hundreds and it climbs with the documents; if it ever
drops to near zero the check has gone blind rather than the tree having gone clean. Read it from the
run rather than from here — a count written into prose is stale the next time anyone adds a link
(**L-114** is the failure it guards against, and **L-96** is why the number is not quoted).

**A bare `§n` that is not a heading in its own document is *not* gated, and this is the refusal
rather than an omission.** The obvious companion rule — resolve an unbound mark against the document
it sits in — was written and measured before it was rejected: **2,501 bare marks in the tree, 1,195
of which it would report.** The three real instances that raised the question are inside that 1,195,
so the rule buys **three true hits at the price of roughly 1,192 alarms**, over a tree its owners
believe is clean.

Almost every alarm is a correct reference to *another* document that §2's adjacency rule declined to
bind — `R8 §3.1`, a second mark in a sentence whose first mark named the document, a comparison of
two sections of a third file. **Adjacency is not the defect; it is the only thing keeping those 1,195
quiet.** Resolving a mark against its host instead is the *nearest document* heuristic §2 already
records having tried and rejected, applied to a different candidate, and it picks the wrong target at
the same scale.

**What would reverse it:** a convention that marks a self-reference as one, so the rule has something
to bind to other than proximity. Until then the class is a reader's, and saying so is worth more than
a check nobody can leave switched on.

## 3. What an open task owes the deliverables report

`deliverables:` is the only place an unproduced output is written as a path
([`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §3), so a task that knows
what it produces and declares nothing is withholding the one fact the field exists for. The symptom
was a report that could only ever measure finished work: every open task declared `[]`, so *"0 not on
disk yet"* was structurally true and told nobody anything (**L-05**).

**A task at `specified` or later declares at least one deliverable.** `proposed` may be empty, because
a proposal need not yet know what it produces — which puts the rule on the transition, where the
information becomes available, rather than on the file.

*This one is a convention rather than a gate.* The retired tool enforced it; `taskmd check` validates
that a **declared** path exists but does not require an open task to declare one. Losing the
enforcement was accepted rather than overlooked — it is the one check of the five the old tool had
that did not survive, and it is recorded in
[T-063](T-063-improvements-to-propose-upstream-to-taskmd.md) as a proposal upstream.
