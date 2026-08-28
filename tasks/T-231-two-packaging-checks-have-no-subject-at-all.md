---
id: T-231
title: Teach the scaffold gate the placeholder the skill actually writes
type: fix
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

# T-231 — Teach the scaffold gate the placeholder the skill actually writes

## 1. Specify

**Outcome**
`check_scaffold.py`'s command and path checks read the skill this repository ships. Today **check 7 reads nought of the skill's eighteen documented commands** and check 5 resolves one path against forty-eight, because both bind on `${CLAUDE_PLUGIN_ROOT}` and commit `2e31c20` moved the whole skill onto `$HTMLDECK`. A check whose subject emptied out silently has read nothing since 2026-08-20 and reported green throughout.

**Closes** `PR-70` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: `COMMAND_RE`, `check_paths` and `BARE_RE`, and a fixture written the way the skill is written
- In: **where the placeholder is declared** - the register's hypothesis is that the check must learn `$HTMLDECK` from `SKILL.md` section 0 rather than hold a second copy of the name
- In: **printing the denominator**, which is the general form cycle 40 was asked to look at: an instrument whose subject can empty out needs to say how big its subject was
- Out: the manifest placeholder, which stays valid for a plugin that uses it

**Inputs**
- `PR-70` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3
- [`tools/plugin/check_scaffold.py`](../tools/plugin/check_scaffold.py)
- `tools/deck/static_variants.py` - the precedent for printing a denominator

**Acceptance criteria**
- [ ] check 7 reads all eighteen documented commands and check 5 all forty-eight paths, **stated as numbers**
- [ ] a command naming a tool that does not exist fails the check, seeded
- [ ] the denominator is printed, so an empty subject is visible rather than green

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
