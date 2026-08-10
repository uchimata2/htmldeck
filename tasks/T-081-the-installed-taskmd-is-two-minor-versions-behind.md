---
id: T-081
title: The installed taskmd is two minor versions behind, so the gates run rules that have been superseded
type: admin
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-062, T-073, T-079, T-080]
work_package: v0.2
owner: the project owner
business_value: medium
effort: xs
created: 2026-08-10
updated: 2026-08-10
deliverables: []
---

# T-081 — The installed taskmd is two minor versions behind, so the gates run rules that have been superseded

## 1. Specify

**Outcome**
`python tools/tasks/lint.py` runs the taskmd its maintainer currently ships, and this project knows
what changed in the two releases it skipped — in particular whether anything it has written down about
`check`'s behaviour stopped being true.

**Why this one**
Found 2026-08-10 while closing
[T-073](T-073-decide-whether-to-keep-refcheck-now-that-upstream-has-ruled.md). The plugin cache holds
`0.1.0` and `0.1.1`, and `lint.py` deliberately takes the newest rather than pinning one, so every gate
this project runs is **0.1.1**. Upstream's repository is at **0.3.0**.

That gap is not idle. T-073 §1 anticipated a `Scope` line in `check`'s output from upstream's T-094 —
*"a run of this project's tracker at v0.2.0 is clean, with 31 documents excluded"* — and it is not in
the output here, because the release carrying it was never installed. A prediction that cannot be
observed is indistinguishable from one that failed.

**The risk this is really about is the reverse of the usual one.** A stale tool does not usually break
anything; it quietly keeps enforcing a rule that has been replaced, and the project writes down what it
observes as though it were current. This repository has now done that once —
[TASK-WORKFLOW.md](TASK-WORKFLOW.md) §6 asserted `task.py`'s filtering behaviour for a month after
T-062 swapped the tool, which is **L-59**. The same shape, one version boundary over.

**Scope**
- In: update the installed plugin, and re-run all three gates.
- In: read upstream's changelog or task record for `0.2.0` and `0.3.0`, and check each behaviour change
  against what this repository asserts about `check` — chiefly [TASK-WORKFLOW.md](TASK-WORKFLOW.md) §6
  and `tools/docs/refcheck.py`'s docstring.
- In: if the update changes what a gate reports, record the new figures where the old ones are quoted.
- Out: `lint.py`'s glob, which is working exactly as its comment says — it found the newest of what was
  installed. Nothing was pinned and nothing needs unpinning.
- Out: [T-079](T-079-the-boards-dependency-columns-list-closed-tasks.md) and
  [T-080](T-080-check-resolves-a-markdown-link-inside-a-code-fence.md). Both were checked upstream on
  2026-08-10 and are `proposed` there, so no release can carry their fix yet and updating will not
  close either.

**Inputs**
- Upstream taskmd's own tracker and README, for what `0.2.0` and `0.3.0` changed.
- [T-073](T-073-decide-whether-to-keep-refcheck-now-that-upstream-has-ruled.md) §3 — where the gap was
  found and what it invalidated there.
- [`../tools/tasks/lint.py`](../tools/tasks/lint.py) — how the version in use is selected.

**Acceptance criteria**
- [ ] The installed plugin is the current release, and `python tools/tasks/lint.py` is green on it
- [ ] Every behaviour change in the skipped releases has been checked against what this repository
      asserts about `check`, and anything now false is corrected rather than left to be noticed
- [ ] Any gate figure quoted in a document matches what the updated tool prints

**Open questions**
- none

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <path>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- <T-NNN or "none">

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-10 | → proposed | Raised from [T-073](T-073-decide-whether-to-keep-refcheck-now-that-upstream-has-ruled.md), which needed the version to explain why a predicted output line was absent. `medium` rather than low because the failure mode is silent: the gates pass, and the project records superseded behaviour as current — which it has already done once and called **L-59**. `xs` because the update is one command and the reading after it is bounded by two releases. `v0.2` under the release split: a minor fix. |
