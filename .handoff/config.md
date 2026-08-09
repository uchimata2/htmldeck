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
- `tracker_template`: tasks/_task-template.md
- `tracker_closed_dir`: (not set — done tasks stay in `tasks/` so links keep resolving)

**The tracker is the `taskmd` plugin as of 2026-08-09**, and the schema is `.taskmd/config.md`,
which is authoritative over anything about fields written here or in `tasks/TASK-WORKFLOW.md`.
`tasks/TASK-WORKFLOW.md` keeps only what taskmd's METHOD.md has no home for. The bare `taskmd`
command does not resolve in agent shells; from the project root:

```
P=$(ls -d ~/.claude/plugins/cache/taskmd/taskmd/*/skills/taskmd | tail -1); PYTHONPATH="$P" python -m taskmd check
```

**`taskmd check` is not the whole gate.** It validates the task record and markdown links only.
`python tools/docs/refcheck.py` is the other half and checks what taskmd cannot see: repo-relative
paths written in prose or printed by a tool, and every `<named document> §n` reference. Run both.

## Notes for whoever resumes

**The research is complete as of 2026-08-07**, and the plugin exists: `.claude-plugin/` and
`skills/htmldeck/`, standing up the seven-stage pipeline. The work from here is building, against
research already written up in `docs/research/R1`–`R7`. Read `CLAUDE.md` first — its rules were
rewritten 2026-08-06 and supersede anything older. Then `docs/BRIEF.md`, whose **"Decisions taken"**
section overrides the older material above it in the same file.

**The backlog is two release phases as of 2026-08-09 — `v0.1` and `v0.2`** — and `tasks/README.md`
is grouped by them. **v0.1 shipped 2026-08-09**: the repository is public at
`github.com/uchimata2/htmldeck`, released as `v0.1.0`, `master` is the published branch and `origin`
now exists. **Resume from v0.2 unless told otherwise**; `docs/BRIEF.md` *Release phases* says what is
in each and why. Task front-matter carries the phase in `work_package`; closed tasks keep the
`WP1`–`WP3` packages they were worked under, which are history rather than the current plan.

**Every release from here runs the humanizing rule again** — `docs/PUBLISHING.md`, which owns the
covered-set test and outlives the task that wrote it. Commits are authored as
`uchimata2 <112070643+uchimata2@users.noreply.github.com>`, set in the repository's local git config;
the personal address was scrubbed from the history before the first push and must not come back.

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
