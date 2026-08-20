---
id: T-189
title: Every documented command interpolates CLAUDE_PLUGIN_ROOT, which is empty in the shell
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-064, T-074]
work_package: PH1
owner: the project owner
business_value: critical
effort: s
created: 2026-08-20
updated: 2026-08-20
deliverables: []
---

# T-189 - Every documented command interpolates CLAUDE_PLUGIN_ROOT, which is empty in the shell

## 1. Specify

**Outcome**
A command copied out of `build.md` or `pipeline.md` runs. Today it does not: every one of them is
written `python ${CLAUDE_PLUGIN_ROOT}/tools/deck/check.py <deck>`, and that variable is not exported
into the shell the model drives. It expands to nothing, so the command becomes
`python /tools/deck/check.py` and fails on a path that does not exist.

**Evidence, measured 2026-08-20**
In a Bash tool call: `echo "CLAUDE_PLUGIN_ROOT=[${CLAUDE_PLUGIN_ROOT}]"` prints `[]`, and
`env | grep -c CLAUDE_PLUGIN` prints `0`. The variable is interpolated by Claude Code into plugin
*manifest* files - hooks, commands, MCP configuration - not into a shell environment.

**What it costs, measured on a real build**
The first outside adoption of 0.4.0 built a 16-slide deck on 2026-08-19. That session read
`build.md` in full, and then never used the documented form once. It substituted
`P="C:/Users/<user>/.claude/plugins/cache/htmldeck/htmldeck/0.4.0"` and repeated that string **87
times**. Two costs follow. The path pins a version - and the session immediately before it had just
migrated that install from 0.2.2 to 0.4.0, so the pin was one update away from being wrong. And it
is an absolute path into another user's home directory, which is exactly the *out-of-the-box* clause
`CLAUDE.md` puts on everything published here.

**Scope**
- In: every command line in `skills/htmldeck/references/build.md`, `pipeline.md`, `critique.md` and
  `artifacts.md` that interpolates the variable.
- In: one resolution the documents can state once and every command can reuse - a shell line the
  agent runs, or a launcher the plugin ships, argued either way rather than assumed.
- In: whether `SKILL.md` should carry the resolution, since it is the file an adopter's session loads
  without asking.
- Out: the plugin manifest, where the variable does work and must stay.

**Precedent.** [T-074](T-074-the-documented-render-command-does-not-exist.md) shipped in `0.1.4`
and is the same family one step back: a documented command that did not exist. This one exists and
cannot be reached.

**Inputs**
- [`../skills/htmldeck/references/build.md`](../skills/htmldeck/references/build.md)
- [`../skills/htmldeck/references/pipeline.md`](../skills/htmldeck/references/pipeline.md)

**Acceptance criteria**
- [ ] No document under `skills/htmldeck/` gives a shell command that depends on
      `CLAUDE_PLUGIN_ROOT` being exported.
- [ ] The replacement is **run**, from a directory that is not the plugin's own and on a drive that
      is not `C:`, and the run is recorded with its output.
- [ ] The replacement survives a version change: it is shown resolving after the installed version
      directory is renamed, or it does not name a version at all.

**Open questions**
- Ship a launcher, or document a one-line resolution? My recommendation is the resolution line: a
  launcher is a second thing to keep in step with the tools, and the failure this fixes is a
  documentation failure.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision - rationale - date>

**Outputs produced**
- <path>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-20 | -> proposed | Created. |
