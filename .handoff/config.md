# Handoff config — htmldeck

Read by the `handoff` skill. Plain Markdown, read by the agent — no parser.

## Core keys

- `handoff_file`: .handoff/HANDOFF.md
- `tracker`: local-markdown-dir
- `project_docs`: CLAUDE.md, docs/ (start with `docs/BRIEF.md` — it is the specification)
- `reconcile_targets`: tasks/, docs/BRIEF.md
- `language`: (omitted — match the source; this project is English)

## Tracker keys — `local-markdown-dir`

- `tracker_dir`: tasks/
- `tracker_id_prefix`: T-
- `tracker_template`: tasks/_templates/task-template.md
- `tracker_closed_dir`: (not set — done tasks stay in `tasks/` so links keep resolving)

## Notes for whoever resumes

This project is **not started**. `docs/BRIEF.md` holds the specification, the evidence behind
it, the lessons carried from the implementation it was extracted from, and the open questions.
Answer the open questions before writing code — the first one shapes everything else.

`reference/` holds proven prior art. It is **not** the plugin: it works, but it is written
around one project's assumptions. Read it for behaviour that is already verified, not for code
to copy wholesale.

This repository will be published. Nothing personal, client-specific or machine-specific goes
in — see `CLAUDE.md`.
