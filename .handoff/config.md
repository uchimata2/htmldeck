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
- `reconcile_targets`: tasks/, docs/BRIEF.md
- `language`: (omitted — match the source; this project is English)

## Tracker keys — `local-markdown-dir`

- `tracker_dir`: tasks/
- `tracker_id_prefix`: T-
- `tracker_template`: tasks/_task-template.md
- `tracker_closed_dir`: (not set — done tasks stay in `tasks/` so links keep resolving)
- `tracker_lint`: `python tools/tasks/lint.py` — the three checks a task edit owes, in order,
  stopping at the first failure and exiting with its code. Runs from any working directory.
