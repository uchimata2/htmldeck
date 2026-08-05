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

The project is in its **research phase (WP1)**. Read `CLAUDE.md` first — its rules were rewritten
2026-08-06 and supersede anything older. Then `docs/BRIEF.md`, whose **"Decisions taken"** section
overrides the older material above it in the same file.

**Objectives are deliberately still open.** Research is expected to be able to overturn scope, not
just fill it in; findings that contradict the brief are surfaced as candidate changes of direction.

Corpus research (T-009) is done. Its measurements are in `docs/research/R1-*.md`; the full-fidelity
extraction sits in a local, gitignored knowledgebase so the private source folder should not need
reopening. `tools/kb/extract.py` reproduces the measurements and self-tests first.

`reference/` holds proven prior art. It is **not** the plugin: it works, but it is written
around one project's assumptions. Read it for behaviour that is already verified, not for code
to copy wholesale.

This repository will be published. Nothing personal, client-specific or machine-specific goes
in — see `CLAUDE.md`.
