# Handoff config — htmldeck

Read by the `handoff` skill. Plain Markdown, read by the agent — no parser.

**Keys only, and only keys the binding reads.** Everything a resuming session needs to *know* lives
in the homes named below, not here: a second copy in this file goes stale silently, and did — it
carried a released version number, a task-schema rule and a publishing rule, each of which already
had an owner.

## Core keys

- `handoff_file`: .handoff/HANDOFF.md
- `tracker`: local-markdown-dir
- `project_docs`: CLAUDE.md, docs/ (start with `docs/BRIEF.md` — it is the specification)
- `reconcile_targets`: `tasks/`, `docs/**/*.md`, `*.md` (repo root), `.handoff/config.md` (this file)
- `language`: (omitted — match the source; this project is English)

> **`reconcile_targets` is a pattern, not a list — keep it that way.** It previously enumerated
> `docs/RELEASE-PHASES.md`, `docs/CONTEXT-AUDIT.md` and `docs/upstream/`. Measured 2026-08-23,
> `docs/` held fifteen top-level documents and four subdirectories, so thirteen documents and three
> subdirectories were outside every Create and Close sweep — including
> `docs/PRE-RELEASE-AUDIT.md`, the register this project's audit cycles write into, and
> `docs/AUDIT-METHOD.md`, which went stale that day and was repaired by hand rather than by a
> sweep. An enumerated list of homes is a second copy of *what the durable homes are*, and it goes
> stale exactly when a home is added, which is the moment the sweep matters most.
>
> **`docs/**/*.md`, not `docs/*.md`.** A single `*` stops at the top level, which is a derived-looking
> glob still enumerating one directory. Resolve the patterns against the working tree at sweep time;
> never hand-maintain the membership. Copied from
> [taskmd's own handoff config](https://github.com/uchimata2/taskmd/blob/master/.handoff/config.md),
> which carries three dated notes recording this same failure three times.
>
> This is a **floor, never a ceiling** (the skill's core §3a): a sweep still covers whatever else the
> session touched. [T-222](../tasks/T-222-derive-the-reconcile-sweeps-membership-instead-of-enumerating-it.md).

## Tracker keys — `local-markdown-dir`

- `tracker_dir`: tasks/
- `tracker_id_prefix`: T-
- `tracker_template`: tasks/_task-template.md
- `tracker_closed_dir`: (not set — done tasks stay in `tasks/` so links keep resolving)
- `tracker_lint`: `python tools/tasks/lint.py` — the checks a task edit owes, in order,
  stopping at the first failure and exiting with its code. Runs from any working directory.
