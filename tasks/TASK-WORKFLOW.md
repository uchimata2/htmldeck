# Task workflow — htmldeck

**What is specific to this project.** The method itself — the lifecycle, the conduct rules, which
edge to use, where a fact lives — is the **taskmd skill's `METHOD.md`**, and this document does not
restate it. The schema is `.taskmd/config.md`. What is left here is the part neither of those owns:
this project's conventions, its section-reference rule, and what its tools do.

The *rules of the project* are in [`../CLAUDE.md`](../CLAUDE.md). *What to build and why* is in
[`../docs/BRIEF.md`](../docs/BRIEF.md). The reusable lessons behind several of the conventions below
are in [`../docs/LESSONS.md`](../docs/LESSONS.md), cited as **L-nn**.

*Merged with METHOD.md on 2026-08-09 (T-062). The section numbers are unchanged on purpose: they are
cited from a dozen task records, and renumbering would falsify every one of those citations — which
is the failure §6.1 exists to catch.*

---

## 1. What a task is

**No work without a task** is METHOD §1 rule 1, not this file's. What this project adds:

One file per task in `tasks/`, created from [`_task-template.md`](_task-template.md). Name it
`T-NNN-<slug of the title>.md` — lower case, hyphenated, truncated where it gets silly. The filename
is a convenience; `id:` is the identity, and the tooling reads only the front-matter. `taskmd index`
prints the next free number.

An audit that will raise child fixes starts from
[`_audit-umbrella-template.md`](_audit-umbrella-template.md); METHOD §5 is the rule it follows.
*It lived in `_templates/` until 2026-08-10. taskmd 0.3.0's `check` reports it as unreachable there:
`create` lists `_`-prefixed files directly in `tasks/`, so a template one directory down is one
nothing offers. Moved rather than argued with — a template nobody is shown is not a template.*

**The front-matter is the only place a fact about a task is stored.** Child lists, "blocks" lists and
the index are computed from it. A stored copy of a derivable fact drifts; a derived one cannot
(**L-08**).

---

## 2. The lifecycle

`specify → plan → implement → review`, mandatory however small. **METHOD §2 defines the phases and
their exit criteria** — in particular that verification belongs to `implement` and not to `review`.
The four numbered sections of the template are the four phases, in order.

What this project adds is which status each phase earns:

| Phase | Section | Status it earns |
| :--- | :--- | :--- |
| `specify` | 1. Specify | `specified` |
| `plan` | 2. Plan | `planned` |
| `implement` | 3. Implement | `in_progress` throughout |
| `review` | 4. Review | `done` |

Three rules that are not obvious from the template:

- **Acceptance criteria are written before the work, not after it.** A criterion invented at review
  time is a description of what happened.
- **`not met` is a legitimate way to close.** A criterion recorded as unmet, with a reason and a gap
  or child task raised against it, closes a task honestly. A criterion quietly reworded to match the
  output does not.
- **Verify against the real case, and look at what was produced** (**L-01**, **L-02**). For anything
  that renders, CLAUDE.md sets the bar: a task is `done` only when its deliverables exist, its log is
  current, and any deck it produced has been opened and looked at, offline.

---

## 3. The front-matter schema

**The schema is [`../.taskmd/config.md`](../.taskmd/config.md), and it is not repeated here.** Field
names, their allowed values, which vocabulary means open, and how `list` orders tasks are all
configuration — `taskmd check` reports every violation of it by name, so there is nothing to carry in
your head and nothing to keep in step.

*This section used to hold a second copy of the schema. It was deleted on 2026-08-09 rather than
updated: two descriptions of one vocabulary disagree the first time either changes, which is **L-13**
and the reason the config exists.*

Two things about this project's use of it that the config does not say:

- **`work_package` is a grouping key, and its values are a release phase.** Open tasks use `v0.1`,
  `v0.2` or `v0.3`; closed tasks keep the `WP1`–`WP3` packages they were worked under, which are
  history rather than the current plan. `docs/BRIEF.md` *Release phases* is the decision behind the
  split, and which phase a new task takes is `../CLAUDE.md`'s rule: `v0.1` only when a defect in the
  published plugin reopens it, `v0.3` for anything `l` or `xl`, and — since v0.2 shipped — for
  everything else that is not such a defect.
- **`deliverables:` is the only place an unproduced output is written as a path.** Front-matter is not
  prose, so `tools/docs/refcheck.py` does not scan it; in §2 and §3 of a task, name a not-yet-existing
  output rather than pointing at it (`` `R7-printable-mode.md`, under `docs/research/` ``), or the
  reference check reports it as a dead pointer, correctly.

### 3.1 Status vocabulary

Enumerated in the config, with `open_statuses` naming the subset that counts as open. `done` and
`cancelled` are the closed statuses. That split is what the index divides on and what decides whether
a blocker still gates its downstream tasks.

`blocked` is the one value that asserts the work is held up, and `taskmd check` reports a task
carrying it with no dependency recorded.

**A task withdrawn because its premise proved false is `cancelled`, and its file is kept. It is never
deleted.** The reason is one clause: a deleted ID resolves to nothing, so the next reader cannot tell
withdrawn from lost, and the record gives them no way to find out. A `cancelled` file answers at its
own ID in one read — what was raised, and why it does not stand.

*Written down 2026-08-11 by [T-089](T-089-a-withdrawn-task-was-deleted-rather-than-cancelled.md),
which found the hole this rule closes: `T-072` was deleted before it was ever committed, so it is
absent from the working tree and from git history alike, and what survived was two sentences in
another task's log. [T-072](T-072-a-corrupted-comment-opener-in-shell-components-css.md) is a stub
reconstructed from those, and [T-003](T-003-brief-mode-elicit-the-six-section-prompt.md) is the
precedent that was already right.*

---

## 4. Which edge to use

**METHOD §4 is the rule** — three kinds, store the forward edge, derive the rest. This project's
fields are in the config's *Edges* table: `parent`, `blocked_by`, `related`.

Two things worth repeating because they cost this project real time:

- **`blocked_by` is expensive.** It stops work and it propagates. Use it for a genuine gate;
  `related` costs nothing and carries most of the value.
- **Every reference must resolve.** A `parent`, `blocked_by` or `related` entry pointing at something
  that does not exist is a `taskmd check` failure (**L-09**).

*A fourth edge, `decisions`, pointed at a decisions register. It was removed on 2026-08-09: no task
here ever carried the field and the register was never created, so it was documentation of a feature
this project did not use.*

### 4.1 A foreign tracker's id is written with its owner's name

`T-nnn` means *this* board. Where a task record names an id belonging to another project — taskmd's,
an adopter's — **write whose it is every time**: `taskmd's T-112`, `their T-111`. Never a bare
`T-112`.

**Because the two numbering lines collide, and the collision arrives without warning.** This
repository's records already name taskmd's `T-095`, `T-102`, `T-111` and `T-112` from
[T-079](T-079-the-boards-dependency-columns-list-closed-tasks.md),
[T-080](T-080-check-resolves-a-markdown-link-inside-a-code-fence.md) and
[T-081](T-081-the-installed-taskmd-is-two-minor-versions-behind.md), and `T-095` was the next free
number here on 2026-08-11. Every one of those mentions is already written with its owner's name,
which is why nothing broke; the rule exists so that stays true rather than staying lucky. Nothing
mechanical can catch it — `check` resolves markdown links and front-matter edges, and a bare id in
prose is neither, so a reader is the only instrument.

*Two more ids in the record belong to nobody: `T-900` and `T-901` are fixtures inside
[T-031](T-031-stop-the-index-blocks-column-listing-closed-tasks.md)'s evidence. Deliberately far outside
the allocated range, which is the same rule solving the same problem.*

---

## 5. The log

The table at the bottom of every task file. **One row per status change**, with a note saying what
changed and why — not that it changed.

The generated views tell you where a task is. The log is the only record of how it got there, and it
is the first thing a later session reads. Where direction changed without a status change, write a
`(no change)` row for it.

---

## 6. The tooling

Two tools, and the split between them is what they are about:

```
taskmd list --open --limit 1     # what to work on next, by the config's ordering rule
taskmd context T-NNN             # everything needed to start one task
taskmd index                     # regenerate the tables in tasks/README.md
taskmd check                     # validate the task record

python tools/docs/refcheck.py    # validate every reference in every document
```

**The bare `taskmd` command does not resolve in an agent shell**, which is a property of how the
plugin is put on `PATH` rather than of the plugin — so the four `taskmd` lines above are what to
type at a terminal, and not what an agent can run. For the three that a task edit owes, there is one
command that finds the installed skill itself:

```
python tools/tasks/lint.py
```

It runs `index`, then `check`, then `refcheck.py`, stops at the first failure and exits with that
failure's code. It is `tracker_lint` in [`../.handoff/config.md`](../.handoff/config.md), and it
exists so that the incantation for locating the skill has one home rather than one per document
(**L-13**).

`taskmd` owns tasks. `refcheck.py` owns **documents**, and exists because taskmd's check sees
markdown-link syntax only: a path written as prose, a path printed by a tool into a fenced block, and
every `§n` reference are all invisible to it. Measured against seeded defects, not assumed — the
comparison is in [T-062](T-062-retire-the-pre-split-task-tool-and-repoint-what-points-at-it.md) §1.

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
- `refcheck.py` — every markdown link, **every repo-relative `.md` path written in prose or printed by
  a tool**, and **every `<named document> §n` reference** (§6.1). Two things are skipped and it prints
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

### 6.1 Section references

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

**This is why the headings in this document were not renumbered when it was merged with METHOD.md.**
Twelve task records cite `TASK-WORKFLOW.md` at §2 through §6.2. A renumbering is a silent falsification
of all of them, and the check would have caught it — which is the rule working on the document that
defines it.

### 6.2 What an open task owes the deliverables report

`deliverables:` is the only place an unproduced output is written as a path (§3), so a task that knows
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

---

## 7. The two checklists

**Opening a task**

1. Copy [`_task-template.md`](_task-template.md), take the next ID from `taskmd index`, name the file
   after the title.
2. Fill §1 and the front-matter. Set `related` and `blocked_by` deliberately; default to `related`.
3. `taskmd index` — the task appears in the tables.
4. `taskmd check` — it passes before any work starts.

**Closing a task**

1. Every acceptance criterion has a verdict and a note in §4.
2. Every deliverable exists at the path the front-matter declares; `taskmd check` confirms it.
3. Anything the task produced that renders has been opened and looked at, offline.
4. Findings worth keeping beyond this task are in [`../docs/LESSONS.md`](../docs/LESSONS.md), not only
   in the task file.
5. `status: done`, `updated:` today, a final log row.
6. `python tools/tasks/lint.py` — §6's three checks, chained with `&&` rather than `;` (**L-40**)
   inside the one command, so a failure stops the chain instead of scrolling past.
