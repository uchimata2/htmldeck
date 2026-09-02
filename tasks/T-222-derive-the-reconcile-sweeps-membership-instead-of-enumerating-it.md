---
id: T-222
title: Derive the reconcile sweep's membership instead of enumerating it
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-219, T-218]
work_package: PH3
owner: the project owner
business_value: medium
effort: xs
created: 2026-08-23
updated: 2026-08-23
shipped_in: unreleased
deliverables:
  - .handoff/config.md
  - docs/lessons/L-135.md
---

# T-222 — Derive the reconcile sweep's membership instead of enumerating it

## 1. Specify

**Trigger**

Reported from the taskmd side on 2026-08-23, by handoff, and confirmed here before this file was
written. The handoff is archived at `.handoff/processed_20260823-151921_HANDOFF.md`; it is gitignored
and is evidence rather than a home.

**Outcome**

`reconcile_targets` in `.handoff/config.md` names patterns and directories, so that a document added
to this project is inside the Create and Close staleness sweep the day it is added, without anyone
editing the config.

**The defect**

`reconcile_targets` is an enumeration: `tasks/`, `docs/RELEASE-PHASES.md`, `docs/CONTEXT-AUDIT.md`,
`docs/upstream/`. It names two documents and one subdirectory. Measured 2026-08-23:

```bash
find docs -maxdepth 1 -type f | wc -l; find docs -maxdepth 1 -mindepth 1 -type d | wc -l
```

15 top-level documents and 4 subdirectories. So **thirteen documents and three subdirectories sit
outside every Create and Close sweep**, and `CLAUDE.md` and `README.md` are outside it as well. The
handoff that reported this said *twelve documents*; the count above is the correction, and the
finding is unchanged by it.

Three of the unswept homes matter now:

- `docs/PRE-RELEASE-AUDIT.md` — the register. [T-219](T-219-pre-release-audit-of-the-whole-repository.md)
  §2 ends every cycle at a commit with the register written, and there are forty-three of them.
- `docs/AUDIT-METHOD.md` — went stale when taskmd `0.6.0` shipped and was repaired by hand. That the
  repair happened at all is the evidence; nothing swept it.
- `docs/lessons/` — 134 files, `L-134` added the same day.

**Why a pattern and not a longer list**

An enumerated list of homes is a second copy of *what the project's durable homes are*, and it goes
stale at the moment a home is added — which is the moment the sweep matters most.
[taskmd's own handoff config](https://github.com/uchimata2/taskmd/blob/master/.handoff/config.md)
carries three dated notes recording this same failure three times: an enumerated brief document
missed a scope document added later; a gitignored control folder was outside every sweep; and a
single-star glob over its docs folder stopped at one directory level the moment documents appeared
in a subfolder of it. The third is the one to learn from here — a depth-limited glob looks derived
and is still enumerating folders.

**Scope**

- In: the `reconcile_targets` value in `.handoff/config.md`, and a note beside it recording why it
  is a pattern.
- Out: the handoff skill itself. Its Check mode reports a config, it does not correct one, and the
  skill is not this repository's.
- Out: `reconcile_targets` is a **floor, never a ceiling** (the skill's core §3a). Widening it does
  not narrow the obligation to sweep whatever else a session touched.

**Acceptance criteria**

- [ ] `reconcile_targets` names no individual document under `docs/`.
- [ ] A document added anywhere under `docs/`, at any depth, is matched without editing the config.
- [ ] `CLAUDE.md` and `README.md` are matched.
- [ ] `.handoff/config.md` is matched by itself.
- [ ] A note beside the value says why it is a pattern, so the next editor does not enumerate it back.
- [ ] `python tools/tasks/lint.py` exits 0.

**Open questions**

- None. The shape is settled by taskmd's three recorded failures and the count above.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Replace the value with `tasks/`, `docs/**/*.md`, `*.md` (repo root), `.handoff/config.md` | `.handoff/config.md` |
| 2 | Add the note: pattern not list, and the three upstream failures it is copied from | `.handoff/config.md` |
| 3 | Run `python tools/tasks/lint.py` | exit 0 |

## 3. Implement

**Decisions & assumptions**
- `*.md` at the repo root rather than naming `CLAUDE.md` and `README.md` — the root holds exactly
  those two today, and a pattern keeps the membership derived when a third arrives — 2026-08-23.
- No `themes/`, `shell/`, `tools/` or `skills/` entry. Those hold code, which goes stale as a defect
  a gate catches, not as a statement contradicting another home — 2026-08-23.

**Outputs produced**
- `.handoff/config.md`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| `reconcile_targets` names no individual document under `docs/` | pass | The three named entries are gone; `docs/**/*.md` replaces them. |
| A document added anywhere under `docs/`, at any depth, is matched | pass | `docs/**/*.md`. The `**` is deliberate and the note says why. |
| `CLAUDE.md` and `README.md` are matched | pass | By `*.md` at the repo root, which holds exactly those two — measured 2026-08-23. |
| `.handoff/config.md` is matched by itself | pass | Named, and marked *(this file)*. |
| A note beside the value says why it is a pattern | pass | Three paragraphs: the count, the depth trap, and the floor-not-ceiling rule. |
| `python tools/tasks/lint.py` exits 0 | pass | Green after two corrections, both recorded below. |

**Findings kept beyond this task**
- [L-135](../docs/lessons/L-135.md) — a list of the homes to check is a second copy of what the homes
  are, and it goes stale on the day one is added. Fourth recurrence of the shape across two projects.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-23 | → proposed | Reported by handoff from the taskmd side; the counts re-measured here before filing, and one corrected. |
| 2026-08-23 | → done | Value replaced, note written, [L-135](../docs/lessons/L-135.md) raised, `lint.py` green. **Two corrections during the work, both worth the row:** the note first landed between `reconcile_targets` and `language`, splitting the key list — a config is parsed by a reader, so a broken list is a real defect, not a cosmetic one. And the prose cited taskmd's own document paths in backticks; `refcheck` resolved them against *this* tree and failed on the scope document that project has and this one does not. **A sibling project's path is not a pointer, and writing it as one makes a false local reference that happens to resolve** — the brief document names a real file in both trees, so that half passed the gate while naming the wrong repository's document. This row deliberately names neither path: quoting the offending path is how the second failure was reproduced. Both citations now link upstream by URL. |
