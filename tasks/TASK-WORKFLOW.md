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

- **`work_package` is a grouping key, and its values are a release phase.** Tasks use `PH1`, `PH2` or
  `PH3`; the `WP1`–`WP3` packages belong to tasks worked under the research and design phases, which
  are history rather than the current plan. [`../docs/RELEASE-PHASES.md`](../docs/RELEASE-PHASES.md)
  is the decision behind
  the split, and which phase a new task takes is `../CLAUDE.md`'s rule: `PH1` only when a defect in
  the published plugin reopens it, `PH3` for anything `l` or `xl`, and — since PH2 shipped — for
  everything else that is not such a defect.
- **`work_package` is the phase; `shipped_in` is the version.** They are different questions and they
  give different answers: `PH3` work shipping in `0.2.1` is the rule working, since a patch takes the
  next number on the published line whatever phase its tasks belong to. The phases were named `v0.1`
  to `v0.3` until 2026-08-12, which made that sentence unreadable (**L-69**, **T-099**). **Never
  write a phase with a `v`.** `shipped_in` is set at close, holds a bare version with no `v`, and is
  the first release tag containing the commit that closed the task — `unreleased` until there is one.
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

**Moved to [`TOOLING.md`](TOOLING.md) on 2026-08-14** — the two commands and what to run, what each
check enforces, the one advisory that is expected forever, and the two rules below. This heading and
its two subsections keep their numbers because 65 citations use them.

**What to run**, so this pointer is not a dead end for the commonest question: `python
tools/tasks/lint.py` is the three checks a task edit owes. Everything else is one file away.

*It was 55% of this document and grew with every tooling change, while the workflow around it did
not — finding `CE-09`, [T-147](T-147-one-workflow-file-per-lifecycle-phase.md).*

### 6.1 Section references

**[`TOOLING.md`](TOOLING.md) §2.** The rule for writing and resolving a `§` citation — when one is
checked, when it resolves, and why quoting a dead reference must not create one.

### 6.2 What an open task owes the deliverables report

**[`TOOLING.md`](TOOLING.md) §3.** A task at `specified` or later declares at least one deliverable.

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
