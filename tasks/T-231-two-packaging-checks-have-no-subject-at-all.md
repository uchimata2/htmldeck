---
id: T-231
title: Teach the scaffold gate the placeholder the skill actually writes
type: fix
status: done
phase: review
parent: T-219
blocked_by: []
related: []
work_package: PH1
owner: the project owner
business_value: critical
effort: s
created: 2026-08-29
updated: 2026-08-29
shipped_in: unreleased
deliverables:
  - tools/plugin/check_scaffold.py
  - README.md
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
| 1 | Measure the subject before touching the check: how many `python <base>/tools/….py` commands and how many based paths the skill's five markdown files actually carry, and under which base | The denominator, from the tree rather than from the register |
| 2 | Learn the base from `SKILL.md`'s own section-0 heading — `placeholder()` — falling back to `${CLAUDE_PLUGIN_ROOT}`, which stays valid for a plugin that uses it | The name has one home, and it is the skill's |
| 3 | Bind checks 4, 5 and 7 on that base, accepting the manifest placeholder alongside it | `check_paths` and `check_commands` take `var` |
| 4 | **Report a base neither of those** — `UNBOUND BASE` for a path, `UNBOUND CMD` for a command. That is the fault itself, so it must be a problem rather than a note | The check can no longer go blind quietly |
| 5 | Print the denominator per skill, on `static_variants.py`'s precedent, and fail outright when the subject is non-empty and nothing was read | `EMPTY SUBJECT`, and a note read before the `OK` |
| 6 | Seed, both directions (**L-125**): four new fixtures, and **the real 2026-08-20 state reproduced against this repository** by holding the placeholder in the tool again | The check shown to fail where it used to pass |
| 7 | `python tools/tasks/lint.py`, then `python tools/check_all.py` at the end of the batch | Both green |

## 3. Implement

**Decisions & assumptions**
- **The base is read from the skill, not held in the tool.** That is the register's hypothesis and
  the measurement supports it: the tool's copy of the name is what survived commit `2e31c20`
  unchanged, and any copy would have. `placeholder()` reads the section-0 heading that declares it
  — the same heading an adopter reads — so the two cannot part again — 2026-08-29.
- **`${CLAUDE_PLUGIN_ROOT}` is accepted alongside the declared base, never instead of it.** It
  stays valid for a plugin that uses it, which is this task's stated scope, and this skill's own
  §0 quotes it to explain why it must not appear in a command. Without the exemption the check
  would report its own documentation — 2026-08-29.
- **An unknown base is a problem, not a note.** A path or command written from something the skill
  never declared is precisely the state that went green for nine days. Printing the denominator
  makes it *visible*; refusing makes it *stop* — 2026-08-29.
- **The new fixtures are about the check's subject, not about a plugin.** Every fixture before
  them describes a malformed plugin, and no number of those can catch a check that has stopped
  reading. That is the general form cycle 40 asked for, and it is why there are four — 2026-08-29.

**Outputs produced**
- `tools/plugin/check_scaffold.py` — `placeholder`, `command_re`, `ANY_BASE_RE`, `ANY_COMMAND_RE`,
  the rebound `check_paths` and `check_commands`, the per-skill denominator note, `EMPTY SUBJECT`,
  and four fixtures
- `README.md` — the quoted output of that command, which `figures.py` checks against a live run

**What was measured**

| Measurement | Result |
| :--- | :--- |
| The subject, counted from the tree before any change | **18 documented commands and 48 `$HTMLDECK` paths** across the skill's five markdown files, plus the one `${CLAUDE_PLUGIN_ROOT}` mention in `SKILL.md` §0. All 18 commands use `$HTMLDECK`; none is bare |
| What the checks read before the change | Check 7: **0 of 18**. Check 5: **1 of 49**. `OK - manifest valid` |
| What they read after | Check 7: **18 of 18**. Checks 4–5: **49 paths**. Still `OK`, and now the `OK` has a denominator beside it |
| **Seeded, both directions (L-125)** — four new fixtures | 23 of 23 behave as specified, including a command written from an undeclared base (`UNBOUND CMD`), a path from one (`UNBOUND BASE`), and the declared base being the one check 7 binds on, proved by an unknown flag firing under it |
| **The real 2026-08-20 state, reproduced against this repository** by holding the placeholder in the tool again | The note reads *base `${CLAUDE_PLUGIN_ROOT}` — checks 4-5 read 1 path(s), check 7 read 0 of 18 documented command(s)* and the run raises **24 problems**. It raised none and printed `OK` for the nine days the defect was live |

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Check 7 reads all eighteen documented commands and check 5 all forty-eight paths, **stated as numbers** | met | `18 of 18` and `49` — forty-eight from `$HTMLDECK` plus the one `${CLAUDE_PLUGIN_ROOT}` pointer §0 quotes, which resolves and is counted rather than ignored |
| A command naming a tool that does not exist fails the check, seeded | met | The pre-existing *an invoked tool that is not there* fixture now runs under a declared base as well — *a base declared in section 0 is the one the command check binds on* fires `UNKNOWN FLAG`, which the old binding could not have reached |
| The denominator is printed, so an empty subject is visible rather than green | met | One note per skill, before the `OK`, and `EMPTY SUBJECT` refuses outright when the subject is non-empty and nothing was read |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | met | `lint.py` all four steps green with the baselined **eleven** advisories and no more. `check_all.py` **0 failures, 0 unclassified, 0 stale** over 37 commands and all 50 tracked tools, 278 s, run separately and after the last edit |
| `PR-70` closed | met | The register's `Remedy` hypothesis — *learn `$HTMLDECK` from `SKILL.md` section 0 rather than hold a second copy* — was measured and taken as written |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | (no change) | **`check_all.py` caught the README.** `figures.py` compares the front page's pasted output against a live run, and this task changed both lines it quotes — the fixture count and the closing sentence. Repaired in place under [`../docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) §4, and the denominator line was added while there: it is the point of the change, and `figures.py` is what keeps it true. |
| 2026-08-29 | → done | Every criterion met and `PR-70` closed in the register. Check 7 **0 of 18 → 18 of 18**, check 5 **1 → 49**, the denominator printed. Seeded by reproducing 2026-08-20 against this tree: **24 problems** where the run printed `OK`. |
| 2026-08-29 | → specified | Batch B1 of [`../docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md). The subject was counted from the tree before the scope was closed: **18 commands and 48 paths**, which is the register's figure re-derived rather than quoted. |
| 2026-08-29 | → planned | Seven steps. Step 4 is the one the register did not ask for: printing the denominator makes a blind check *visible*, and refusing on an undeclared base makes it *stop*. |
| 2026-08-29 | → in_progress | The base is learned from `SKILL.md` §0 and checks 4, 5 and 7 bind on it. Check 7 went **0 of 18 → 18 of 18**, check 5 **1 → 49**. The proof is the seeded one: holding the placeholder in the tool again reproduces 2026-08-20 exactly — same note, same numbers — and the run raises **24 problems** where it printed `OK`. |
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`High`**: the method's section 4 gives that level one obligation beyond a child task — *the release does not go out while it is open*. |
