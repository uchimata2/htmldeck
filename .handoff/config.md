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

**The research is complete as of 2026-08-07**, and the plugin exists: `.claude-plugin/` and
`skills/htmldeck/`, standing up the seven-stage pipeline. The work from here is building, against
research already written up in `docs/research/R1`–`R7`. Read `CLAUDE.md` first — its rules were
rewritten 2026-08-06 and supersede anything older. Then `docs/BRIEF.md`, whose **"Decisions taken"**
section overrides the older material above it in the same file.

**The backlog is two release phases as of 2026-08-09 — `v0.1` and `v0.2`** — and `tasks/README.md`
is grouped by them. **Resume from v0.1 unless told otherwise**; `docs/BRIEF.md` *Release phases* says
what is in each and why. Task front-matter carries the phase in `work_package`; closed tasks keep the
`WP1`–`WP3` packages they were worked under, which are history rather than the current plan.

`skills/htmldeck/SKILL.md` is the always-loaded body and is kept under a byte budget on purpose;
substance goes in `references/` or in `docs/`, never in it. `tools/plugin/check_scaffold.py`
enforces that, and self-tests first.

**Objectives are deliberately still open.** Research is expected to be able to overturn scope, not
just fill it in; findings that contradict the brief are surfaced as candidate changes of direction.

Corpus research (T-009) is done. Its measurements are in `docs/research/R1-*.md`; the full-fidelity
extraction sits in a local, gitignored knowledgebase so the private source folder should not need
reopening. `tools/kb/extract.py` reproduces the measurements and self-tests first.

`reference/` holds **one file** — `example-prompt.md`, 1.2 KB, the source prompt this project was
briefed from. It is a prompt, not a codebase; nothing in it is code to copy or behaviour to verify.
*This paragraph described a working prior-art codebase until 2026-08-09, which was never what is
there.*

This repository will be published. Nothing personal, client-specific or machine-specific goes
in — see `CLAUDE.md`.
