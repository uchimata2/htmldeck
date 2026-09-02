---
id: T-227
title: Correct the copy-into-your-own-plugin route, or withdraw it
type: decision
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
updated: 2026-08-30
deliverables: []
shipped_in: 0.7.0
---

# T-227 — Correct the copy-into-your-own-plugin route, or withdraw it

## 1. Specify

**Outcome**
An adopter following the front page's second adoption route either succeeds or is told plainly that the route does not exist. Today [`README.md`](../README.md) rests it on `${CLAUDE_PLUGIN_ROOT}`, and **no path in the skill goes through that variable** - all 22 go through `$HTMLDECK`, whose two resolution branches are an installed plugin or a clone, and a copy inside somebody else's plugin is neither.

**Closes** `PR-07` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: the front page's install section, and `SKILL.md` section 0's resolution branches
- In: **measuring whether a run can locate a skill file from its own path** before writing a third branch - the register's hypothesis, and the thing that decides which fix is honest
- In: **from the ClaimAI adopter report, [`027`](../docs/adopter-reports/claimai/027-the-tools-are-unreachable-when-htmldeck-is-installed-as-a-plugin.md)** — Installed as a plugin the tools are **not on `PATH`** and there is no documented invocation, so every adopter writes a 70-line launcher. **The line worth the report on its own**: the plugin cache keeps *every* version — seven here, `0.1.1` to `0.6.0` — so a first-match glob picks `0.1.1` and the failure reads as *tool not found*. This is the same root as `PR-07`: what `$HTMLDECK` resolves to, and for whom
- Out: `$HTMLDECK` itself, and [T-189](T-189-resolve-the-plugin-root-in-every-documented-command.md)'s ruling that the variable is not written into a command
- Out: the two routes that work

**Inputs**
- `PR-07` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3
- [`skills/htmldeck/SKILL.md`](../skills/htmldeck/SKILL.md) section 0
- [T-189](T-189-resolve-the-plugin-root-in-every-documented-command.md)
- [`027`](../docs/adopter-reports/claimai/027-the-tools-are-unreachable-when-htmldeck-is-installed-as-a-plugin.md) — the adopter record merged into this task by [T-225](T-225-triage-the-claimai-adopter-report.md), because this task already owns the class. Each carries its own evidence and version.

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
| 1 | Measure whether a run can locate a skill file from its own path — the register's hypothesis, and the thing that decides which fix is honest | A yes or no, with the observation behind it |
| 2 | Measure what a copied `skills/htmldeck/` can actually reach, and prove both halves by running a documented command from a copy | The route stands or falls here, not on which variable resolves it |
| 3 | Correct the front page to what the measurement supports, or withdraw the route | `README.md`'s install section |
| 4 | Give section 0 the branch the measurement licenses | `SKILL.md` section 0 |
| 5 | Run `check_scaffold.py`, `figures.py` and `refcheck.py`, figures before the gate | Three green |

## 3. Implement

**Decisions & assumptions**

- **The hypothesis holds: a skill can locate itself.** Measured 2026-08-30. A harness that loads a
  skill prints `Base directory for this skill: <absolute path>` ahead of the body — observed for a
  user-level skill and for this plugin's own skill, where it named the installed
  `0.6.0` skill directory. The phrase is authored in **no** file in either tree, so it is injected
  rather than written. `$HTMLDECK` is that path's grandparent. Section 0 now leads with it and keeps
  the glob as the fallback, which is the order the register predicted.
- **The stated remedy is refused, on a fact the row does not contain.** The register asks for the
  discovery command on the front page **and** a third resolution branch. Neither reaches the defect:
  of the 23 `$HTMLDECK` targets the skill writes, **19 sit outside `skills/htmldeck/`** — the design
  system, every deck tool, the shell and the reference deck. A copy of that one directory reaches
  four of twenty-three whatever resolves the variable, because the other nineteen files are not
  there. The route is false for a reason no resolver can fix.
- **So the route is corrected rather than withdrawn, and the correction is proved both ways.** Copied
  whole into a plugin directory named `acme-plugin` — a name the discovery glob cannot match — the
  documented `check.py` invocation exits **0**, run from a third working directory against a deck
  outside the copy. Copied as `skills/htmldeck/` alone, the same command dies with *No such file or
  directory* and 19 of 23 targets are absent. Self-location is what carries the working case; the
  glob cannot, because the adopter's plugin is not called `htmldeck`.
- **A defect nobody was looking for, in the published `0.6.0`: the prohibition destroyed itself on
  delivery.** Claude Code substitutes its plugin-root placeholder into a plugin's **skill body**, not
  only into manifest files — so the sentence forbidding the placeholder arrived naming a
  version-pinned absolute cache path instead, twice, in bold, and asserted that a correct absolute
  path *becomes* a command rooted at the drive, which is false. The paragraph written to prevent
  T-189's 87 hardcoded version-pinned paths was the skill's most prominent source of one. Rewritten
  to state the rule without spelling the token, because spelling it is what breaks it. Kept as
  [L-151](../docs/lessons/L-151.md). It also corrects the paragraph's own claim about *manifest*
  files.
- **Not measured, and the fix does not depend on it:** whether the placeholder's unbraced form also
  interpolates. Both observed occurrences were braced. The rewrite names no token at all, so the
  answer cannot change it.
- **The adopter's record [`027`](../docs/adopter-reports/claimai/027-the-tools-are-unreachable-when-htmldeck-is-installed-as-a-plugin.md)
  is answered in part.** Its version-sorting point was already correct in section 0 — the glob sorts
  as versions — but nothing said **why**, so the line read as a flourish and an adopter rewriting the
  glob would drop it. Section 0 now says it is load-bearing and what the failure looks like. Its
  first point, *ship a launcher*, is a packaging decision this task does not own and stays open on
  the record.
- **In place under section 4:** `README.md`'s *nineteen deliberately broken packages* is wrong —
  `check_scaffold.py` carries **23** fixtures, **16** deliberately broken and 7 good, read out of
  `FIXTURES` rather than counted by eye, which is what corrected a hand count of 14. It is in the
  install section this task owns, so it was fixed here rather than left standing for
  [T-234](T-234-the-front-pages-own-figures-and-claims.md).
- **The count went into the front page and came straight back out.** `figures.py` flagged *19* and
  *23* as prose numerals bound to no command, which is right: they are this task's measurement, not
  the front page's subject. The figure now lives here and on the register row, and the README names
  the six directories to copy — the actionable half, which does not decay. That is `PR-103`'s
  proposed remedy applied on arrival instead of after the drift.

**Outputs produced**

- [`README.md`](../README.md) — the install section's vendoring paragraph, and the fixture count
- [`skills/htmldeck/SKILL.md`](../skills/htmldeck/SKILL.md) — section 0's resolution branches and the
  placeholder rule; 6,291 to 6,885 bytes of the 8,192 budget
- [`docs/lessons/L-151.md`](../docs/lessons/L-151.md)

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The route is **proved by running it from a copied directory**, or removed with the reason recorded | pass | Proved both ways — the whole payload under `acme-plugin` exits 0; `skills/htmldeck/` alone fails with *No such file or directory*, 19 of 23 targets absent. The front page states the working form |
| No document names the placeholder as a mechanism the skill uses, unless it does | pass | Zero occurrences remain in `README.md` and `SKILL.md`. Section 0 states the rule without spelling the token, because spelling it is what broke it |
| `python tools/plugin/check_scaffold.py` green, and `python tools/check_all.py` green | pass | Scaffold: 23 of 23 fixtures, base `$HTMLDECK`, 49 paths read, 23 of 23 documented commands, body 6,885 of 8,192. `figures.py` 0 stale and `refcheck.py` 4,960 pointers 0 broken, both after the pasted block was updated |

**No look is owed.** This task changed two markdown documents and no deck, which is
[`../docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md)'s stated case for writing no row.

**Child fix tasks raised**
- none. The one finding worth keeping is [L-151](../docs/lessons/L-151.md); the adopter's *ship a
  launcher* stays open on its own record.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-30 | → done | `PR-07` closed, and its stated remedy **refused**: 19 of the 23 paths the skill writes sit outside `skills/htmldeck/`, so no resolver saves a copy of that directory. The route is corrected to the whole payload and proved by running it, both ways. Found in passing that the placeholder prohibition is destroyed by the harness that delivers it ([L-151](../docs/lessons/L-151.md)) — a defect in the published `0.6.0` |
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`High`**: the method's section 4 gives that level one obligation beyond a child task — *the release does not go out while it is open*. |
