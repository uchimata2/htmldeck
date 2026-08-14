# Observations for the taskmd plugin

> **Handover record — sent 2026-08-14.**
> **Route:** one issue on this project's own repository,
> [`uchimata2/taskmd#1`](https://github.com/uchimata2/taskmd/issues/1). The body is this document with
> its links made absolute; the rows are identical.
> **Response: triaged against a 143-file backlog, and five of the six were real there.** `O-T4` is the
> row that repaid the report — the scan it prompted found **one row wider than its header in 2,797**,
> in the very task that answered `O-T2`, and the excess cell had been rendering as nothing since
> 2026-08-10; it is repaired. `O-T5`'s 2026-08-07 ruling was narrowed on the argument this register
> supplied. `O-T1` and `O-T3` were agreed with nothing to add. Their tasks and reasoning are on the
> thread; this register points at it rather than copying it.
>
> **Three corrections travelled back the other way and were posted 2026-08-15** by
> [T-160](../../tasks/T-160-correct-the-three-errors-the-recipients-found-in-the-delivered-registers.md):
> `O-T6` cited the wrong id of theirs; `O-T2`'s text-sort defect is fixed here and was reported as
> though live, which put work on their disposition that they do not owe; and their advice to delete
> both wrappers assumes a caller that was served the skill, which the release gate is not. **The
> cross-reference audit they asked for is done — seven citations across both registers, one wrong**,
> the `T-063` they found.
>
> Sent by [T-157](../../tasks/T-157-hand-the-upstream-registers-to-their-owners.md) after the hold in
> [`../CONTEXT-AUDIT.md`](../CONTEXT-AUDIT.md) §7 came off: the closing review landed 2026-08-14 and
> **added no rows here**, which is the condition the hold was waiting on rather than a lucky outcome.

**From the htmldeck project, which uses it to track 141 tasks.** Six observations, none of them
ranked and none of them a request. They come from one adopting repository, and they are written down
because an adopter sees usage the author's own repositories cannot show.

**One of them is a correction of an earlier report, and it matters more than the rest.** `O-T2` was
originally going to send you after a defect that is not yours. It is kept, corrected in place, with
what it got wrong visible — see below.

## How to read this

- **Nothing here carries a priority.** Assigning one would be a guess about your project. What an
  observation is worth is your call, not the reporter's — which is also why the marginal-looking
  ones are here rather than filtered out.
- **Each row is stamped with how it was found.** *audit* rows came from a deliberate context-economy
  audit that **read your backlog first** — 138 task files, the 8 then open, and every closed title
  touching context, size or output. *implementation* rows came later, from sessions building things,
  and **no backlog was re-read for them** — so read an *implementation* row as *this was observed*,
  never as *this is not already known or already decided*.
- **Ids collide, so every one is named.** A `T-nnn` written as *your* `T-085` is yours. One written
  as *the reporting project's* is htmldeck's. The two numbering lines overlap heavily and a bare id
  is unsafe in either direction.
- The version observed is **0.5.0**, on Windows 11 with Git Bash and PowerShell 7.

## The observations

| | Observation |
| :--- | :--- |
| **O-T1** *audit* | **Nothing to propose about tiering — you did it first, and the adopting project should follow you.** *Your* `T-028` established the membership rule, the three tiers, and the budget-as-a-relation, and rejected both the alternatives an outsider would arrive with. The audit went looking for something to send you about context budgeting and found the question already settled, so the finding became *adopt what they settled*; the direction of travel is upstream→adopter |
| **O-T2** *audit, corrected* | **The command surface is unreachable in an agent shell, and it causes the adopting project's largest read-path cost — but the defect is not taskmd's.** The saving is real and larger than first stated: `list --open` answers in 2,451 bytes what reading the generated index costs 36,813, and `list --open --limit 1` — the form that actually answers *what next* — answers in **94 bytes, 389×**. **The cause was measured and it is the harness**, not your packaging: taskmd ships `bin/taskmd`, the launcher runs correctly when invoked directly, and the harness does emit its directory into the shell snapshot — where the `PATH` line is truncated mid-value, at 5,551 characters, losing every plugin's `bin/`. That is a separate report, filed against the harness. **This row previously pointed at *your* `T-085`** (*install the published plugin on a machine that has never seen it*) and would have been a hunt for a defect that is not there. **What is left for you** is smaller and still real: the design comment in `bin/taskmd` states the `PATH` mechanism as given — *no install step, no PYTHONPATH to set, no path to a cache directory anyone has to know* — and one environment breaks it silently, so a documented fallback for *the command is not on `PATH`* may be worth having. Every adopter otherwise re-derives a locator, and re-deriving it is error-prone: this one globbed the version directory and **sorted it as text**, which would have selected `0.5.0` over `0.10.0` at your next minor bump. **Corrected 2026-08-15: that defect was found and fixed here before this row was ever sent, and the row failed to say so.** `version_key` parses the version and a self-test in the same file asserts `0.10.0` beats `0.5.0` and `0.9.1`. The row is evidence that re-deriving a locator is error-prone — it is **not** an outstanding defect, and reading it as one costs you work. This is the reporting project's error, not a change of mind |
| **O-T3** *audit* | **A generated index grows without bound and has no cheap form.** 134 rows and 33,676 bytes when measured; five task closures in one session took it to 139 rows and 36,813 bytes, **+9.3% in a day**, while `list --open` moved only from 1,901 to 2,451. The index grows with the whole board; the query grows only with what is open. *Your* `T-087` let `list` filter on a field the index shows, which is the same problem approached from the query side. Stated as an observation only: the index is for people, and the fix may simply be that agents should never read it — which is what `O-T2` makes possible |
| **O-T4** *implementation* | **A markdown table row with more cells than its header loses the excess silently, and nothing in a markdown-native tracker can see it.** Two rows of a document here carried a whole paragraph in a third cell against a two-column header; GitHub-flavoured markdown drops it, so the text existed in the file and rendered nowhere, for weeks, with `check` green. `check` already reads documents and resolves markdown links, so it is the only tool in the neighbourhood — **and the reporting project decided against building the equivalent gate for itself**, on the grounds that a cell past the header is not a broken pointer and a checker for two rows would outlive the fault. Recorded because that trade may come out differently for a tool whose whole subject is markdown records, and because the failure mode is invisible by construction: the only instrument is counting cells against the header |
| **O-T5** *implementation* | **`--help` on a subcommand prints the top-level usage, so the options cannot be discovered from the CLI.** `python -m taskmd list --help` and `... context --help` both print `usage: taskmd {check,context,index,list} [args] [--root PATH]` and nothing else. `--open`, `--closed`, `--limit`, `--json` and the `--<field> V` form are in `SKILL.md` and in `cli.py`'s module docstring; an agent that has the command but not the skill file has to read the source. This is a context-economy point as well as a usability one — it is the case where a caller reads a whole file to learn what a flag is called |
| **O-T6** *implementation* | **A field a project requires at a status transition has no gate, and three tasks closed without it.** This project's convention is that `shipped_in` is set when a task closes; `check` validates the *value* of a declared field but nothing ties a field's presence to a status. 113 of 138 files carried it and three closed tasks did not, found by hand. ~~The adjacent case is already filed as *your* `T-063` — an open task at `specified` or later declaring no deliverable — which is the same shape: *this field becomes required at this point in the lifecycle*.~~ **Corrected 2026-08-15, and the correction is the point of the row rather than a footnote to it: that citation was wrong.** Your `T-063` is *Measure the tier-1 member the rule declares*, and it is closed. **Nothing in your backlog covered this class**, which you established independently and raised as your `T-146`. The preamble guarded against your id being read as ours and not against the harder direction — **a wrong id of yours resolves to a real task, so it reads as evidence the work is already covered rather than as a dangling pointer**, and a reader who trusts it stops looking. Recorded as one observation rather than two because the general form may be cheaper than either instance. **A third instance, 2026-08-14, and it is about two fields agreeing rather than one being present:** `status` and `phase` move together through the lifecycle, and **two sessions in this project chose differently on the same day** — one wrote `status: specified, phase: specify`, the other `status: specified, phase: plan`, and **`check` passes both**. Neither is obviously wrong: *the phase just completed* and *the phase to do next* are both readable from a table that pairs them. The reporting project owns which reading is right, and states it in its own workflow document — but nothing enforces the pair, so the two live side by side in the same tracker. **If the general form is worth building, this is the shape that argues for a relation between fields rather than a required-field rule** |

## What this project runs instead, and why it is not a complaint

Because the bare command does not resolve here, two small wrappers locate the installed skill by
globbing the version directory and put it on `PYTHONPATH`: one chains `index`, `check` and a
reference checker for a task edit, the other exposes `list` and `context`. They are not a workaround
for anything taskmd does — a locator that never consults `PATH` is simply the right answer to a
`PATH` that cannot be relied on, whatever broke it. They are mentioned only as evidence for `O-T2`'s
last clause: every adopter writes this, and the obvious implementation of it is wrong.

## Provenance

Assembled by the htmldeck project as part of a context-economy audit of its own development
workflow, and extracted here so it arrives as its own document. The audit that produced the *audit*
rows is [`../CONTEXT-AUDIT.md`](../CONTEXT-AUDIT.md) §7.2; the rules the register follows are in
[`../research/R8-context-economy-for-coding-agents.md`](../research/R8-context-economy-for-coding-agents.md)
§6. Replies, corrections and *already knew that* are all useful; `O-T2` is what happens to a row that
turns out to be wrong — corrected in place, with the error visible, rather than quietly dropped.
