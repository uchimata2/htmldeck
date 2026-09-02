---
id: T-252
title: Put this repository's ignore rules where a clone receives them
type: fix
status: done
phase: review
parent: T-219
blocked_by: []
related: []
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-29
updated: 2026-09-02
shipped_in: 0.7.0
deliverables: []
---

# T-252 — Put this repository's ignore rules where a clone receives them

## 1. Specify

**Outcome**
What this repository ignores is stated where a clone can read it. Today `.gitignore` names ten things and `.claude/` is not among them - **one machine's global ignore file is what hides it** - and the effective rules come from three files of which a clone receives one.

**Closes** `PR-15`, `PR-122` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: `.gitignore`, and a statement of what the other two files were doing
- In: **nothing else** - every finding this task closes is named above, and each statement stays in the register rather than being restated here (the method's umbrella condition 2)
- Out: any finding not in the list above
- Out: committing to a remedy before measuring it. A remedy is a hypothesis (the method's section 5); a fix that the measurement refuses is reported here and its finding stays open

**Inputs**
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3 - the rows for `PR-15`, `PR-122`
- `PR-15`'s evidence, which is that the behaviour differs on a clone
- `PR-123`, in the Low batch, which is that nothing here ever looks at what `.gitignore` hides

**Acceptance criteria**
- [ ] every finding above is **closed with its remedy measured**, or explicitly deferred with the reason recorded on its register row - the method's obligation for `Med`
- [ ] each register row's `Task` cell names this task and its `Status` cell says what happened
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None yet. The register's `Remedy` column carries a hypothesis for each finding, and the method's
  section 5 says it is a hypothesis: whoever implements this measures before committing to it, and
  records what the measurement said.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Ask what the repository's **own** rules decide, with the machine's global excludes file emptied | Settings file already covered by B19; `.claude/worktrees/` still `.git/info/exclude`'s alone |
| 2 | Decide the hypothesis both rows offer — `.claude/` wholesale, or one path at a time | **Refused wholesale**, on `T-295`'s open decision |
| 3 | Ship the missing rule, and open the file with the rule that keeps the three sources from drifting apart again | `.gitignore` |
| 4 | Prove it both ways — both paths resolve here, and an unnamed file under `.claude/rules/` stays unignored | Measured with the global excludes emptied |
| 5 | Close the two register rows, then `lint.py` and `check_all.py --docs`, run separately | Both green |

## 3. Implement

**Decisions & assumptions**
- **`.claude/` is not ignored wholesale**, which both register rows offered as the likely answer. A directory rule forecloses `T-295`'s open question about whether this repository should track a rule file — and it would take that decision *silently*, which is the exact mechanism that published `T-288`'s probe. The rules are named one path at a time — 2026-09-02
- **Half of `PR-15` had already closed, by accident and four days early.** `.claude/settings.local.json` entered `.gitignore` on 2026-09-02 in B19's untracking commit, raised by `git add -A` publishing a probe rather than by this finding. Recorded rather than claimed: this task shipped `.claude/worktrees/` and the opening rule — 2026-09-02
- **The two other sources are described and never named.** `.git/info/exclude` is generic and safe to name; the global excludes file is a path in a home directory, and this repository publishes — the same reason the register gives for not writing it either — 2026-09-02
- **The proof that matters is the negative one.** With the machine's global excludes emptied, a second, unnamed file beside the probe is still unignored. A directory rule would have made that line green too, and passed for a fix — 2026-09-02

**Outputs produced**
- [`../.gitignore`](../.gitignore) — the opening rule, `.claude/worktrees/`, and the `.claude/` block restated
- [`../docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) — the `PR-15` and `PR-122` status cells

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| every finding closed with its remedy **measured**, or deferred with the reason on its row | pass | Both closed, and both rows' shared hypothesis refused on an argument the file already carried. Measured with `git -c core.excludesfile=` pointed at an empty file, which is the only way to ask what a clone receives |
| each register row's `Task` cell names this task and its `Status` cell says what happened | pass | Both. The `Task` cells already named it |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | pass | `lint.py` green; `check_all.py --docs` green — `.gitignore` and one register, no path `--docs` refuses. **The batch's landing owes the full run** |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-02 | proposed → done | B20. **Both rows proposed ignoring `.claude/` wholesale and both are refused**, on an argument `.gitignore` was already carrying: a directory rule decides `T-295`'s open question about tracking a rule file, and decides it quietly — the same mechanism that published `T-288`'s probe in the commit arguing a clone should not receive it. So the rules are named one path at a time. **Half of `PR-15` had closed itself four days early**, when B19 added the settings file for an unrelated reason; what this task shipped is `.claude/worktrees/`, which was `.git/info/exclude`'s alone and reached no clone, and an opening rule that says every rule this repository depends on lives in the one file a clone receives. The proof that decides it is the negative one: with the machine's global excludes emptied, a second, unnamed file beside the probe is still unignored, so the decision `T-295` owns is still open. |
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`Med`**, grouped: the owner ruled on 2026-08-29 that a severity obliges a disposition before the release rather than a file count, on the precedent that the method already accepts many findings to one task at `Low`. Every finding keeps its id and its statement in the register. |
