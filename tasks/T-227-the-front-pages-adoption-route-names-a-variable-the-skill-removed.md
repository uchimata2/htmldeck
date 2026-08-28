---
id: T-227
title: Correct the copy-into-your-own-plugin route, or withdraw it
type: decision
status: proposed
phase: specify
parent: T-219
blocked_by: []
related: []
work_package: PH1
owner: the project owner
business_value: critical
effort: s
created: 2026-08-29
updated: 2026-08-29
deliverables: []
---

# T-227 — Correct the copy-into-your-own-plugin route, or withdraw it

## 1. Specify

**Outcome**
An adopter following the front page's second adoption route either succeeds or is told plainly that the route does not exist. Today [`README.md`](../README.md) rests it on `${CLAUDE_PLUGIN_ROOT}`, and **no path in the skill goes through that variable** - all 22 go through `$HTMLDECK`, whose two resolution branches are an installed plugin or a clone, and a copy inside somebody else's plugin is neither.

**Closes** `PR-07` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: the front page's install section, and `SKILL.md` section 0's resolution branches
- In: **measuring whether a run can locate a skill file from its own path** before writing a third branch - the register's hypothesis, and the thing that decides which fix is honest
- Out: `$HTMLDECK` itself, and [T-189](T-189-resolve-the-plugin-root-in-every-documented-command.md)'s ruling that the variable is not written into a command
- Out: the two routes that work

**Inputs**
- `PR-07` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3
- [`skills/htmldeck/SKILL.md`](../skills/htmldeck/SKILL.md) section 0
- [T-189](T-189-resolve-the-plugin-root-in-every-documented-command.md)

**Acceptance criteria**
- [ ] the route is either **proved by running it from a copied directory**, or removed from the front page with the reason recorded - a third state, documented harder, is the failure
- [ ] no document names `${CLAUDE_PLUGIN_ROOT}` as a mechanism the skill uses, unless it does
- [ ] `python tools/plugin/check_scaffold.py` green, and `python tools/check_all.py` green

**Open questions**
- None yet. The register's `Remedy` column carries a hypothesis for each finding, and the method's
  section 5 says it is a hypothesis: whoever implements this measures before committing to it, and
  records what the measurement said.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <the files this task changed>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- <T-NNN or "none">

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`High`**: the method's section 4 gives that level one obligation beyond a child task — *the release does not go out while it is open*. |
