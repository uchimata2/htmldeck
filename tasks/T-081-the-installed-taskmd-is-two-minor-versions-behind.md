---
id: T-081
title: The installed taskmd is two minor versions behind, so the gates run rules that have been superseded
type: admin
status: done
phase: review
parent: null
blocked_by: []
related: [T-062, T-073, T-079, T-080]
work_package: PH2
shipped_in: 0.1.5
owner: the project owner
business_value: medium
effort: xs
created: 2026-08-10
updated: 2026-08-12
deliverables:
  - tasks/_task-template.md
  - tasks/_audit-umbrella-template.md
  - tasks/TASK-WORKFLOW.md
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
| 1 | Update the plugin and re-run the three gates | the run |
| 2 | Fix whatever the new checks find | the templates |
| 3 | Check every claim this repository makes about `check` against the tool that now runs | [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §6 |
| 4 | Re-measure the two upstream tasks this project is waiting on | T-079, T-080 |

## 3. Implement

**Decisions & assumptions**
- **Updated on the owner's instruction, 2026-08-10.** `0.1.1` → `0.3.0`, user scope. The cache keeps
  the older versions and `lint.py` globs for the newest, so nothing needed repointing.

**What the update found, immediately**

    3 problem(s) - 83 task(s), 498 field value(s), … 2 template(s), 12 template field value(s)

Three defects in this project's own templates, none of which any earlier release could see:

| Reported | What it was | Fix |
| :--- | :--- | :--- |
| `TEMPLATE UNREACHABLE` | the audit umbrella template sat one directory down, under a `_templates` folder, and `create` lists `_`-prefixed files directly in `tasks/` — so nothing would ever offer it | Moved to [`_audit-umbrella-template.md`](_audit-umbrella-template.md) |
| `TEMPLATE FIELD` | `_task-template.md` offered five `type` values; the schema allows seven — `decision` and `audit` were missing | Both added |
| `TEMPLATE FIELD` | the same template offered `WP<n> \| final \| none` for `work_package`, which predates the release split entirely | `PH1 \| PH2 \| PH3` added, `WP1`–`WP3` spelled out |

**A template is the one document that cannot be checked by using it**, which is why all three
survived: nothing reads a template except a person copying it, and a person copying it fixes the
field in their own file and moves on. The second and third are also the answer to a live worry —
this project kept the template's value lists deliberately thin because a second copy of the schema
drifts (**L-13**), and drift is exactly what happened. It is now gated, so the copy is safe to keep.

**What the skipped releases changed, checked against what this repository asserts**

- **`check` now reads only the documents a clone would receive** (upstream's T-094) and prints
  `Scope  35 document(s) not read`. [T-073](T-073-decide-whether-to-keep-refcheck-now-that-upstream-has-ruled.md)
  §1 predicted this line and could not observe it; **35, where that prediction said 31**. The
  difference is the documents this session added, not a disagreement.
- **`index` filters closed tasks out of both dependency columns.** That is
  [T-079](T-079-the-boards-dependency-columns-list-closed-tasks.md)'s proposal, accepted upstream as
  their T-111 and shipped — **so T-079 closes on this update.** Verified on this board rather than
  from a release note: T-019's *Blocked by* is empty where it read `T-002`, and T-084's *Blocks*
  names `T-036` and nothing closed.
- **The code-fence defect is not fixed.** Their T-112 is still `proposed`, and reproducing it against
  0.3.0 puts a link inside a fence in a task file and turns the run red exactly as before.
  [T-080](T-080-check-resolves-a-markdown-link-inside-a-code-fence.md) stays open on measurement.
- `TASK-WORKFLOW.md` §6's account of what `check` enforces was true and incomplete; it now names the
  template checks and the clone-scope rule. Its paragraph asserting that `index` does **not** filter
  was true when written and false as of this update — corrected, and the whole episode left visible,
  since it is **L-59**'s own case coming round twice in one day.

**Outputs produced**
- [`_task-template.md`](_task-template.md) — both field lists reconciled with the schema.
- [`_audit-umbrella-template.md`](_audit-umbrella-template.md) — moved where `create` will find it.
- [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §1 and §6 — the move, the new checks, and the corrected
  claim about `index`.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The installed plugin is the current release and `lint.py` is green on it | met | `Plugin "taskmd" updated from 0.1.1 to 0.3.0`, then `OK - 83 task(s), 498 field value(s), … 5 vocabulary row(s)` and all three checks passing. |
| Every behaviour change checked against what this repository asserts, and anything now false corrected | met | Four changes traced; one made a `TASK-WORKFLOW.md` paragraph false and it is corrected rather than left to be noticed. |
| Any gate figure quoted in a document matches what the updated tool prints | met | `python tools/docs/figures.py` is green; no document pastes `taskmd check`'s output, which is why its fence is declared excluded. |

**Child fix tasks raised**
- none. **T-079 closes on this update** and T-080 does not — both recorded in their own files.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-10 | → done | **The update paid for itself in one run**: three defects in this project's own templates, none visible to any earlier release, and one of them a template `create` would never have offered. It also settled both upstream tasks by measurement rather than by waiting — T-079's fix shipped and is verified on this board, T-080's has not and was reproduced against 0.3.0. The failure mode this task was raised for is the one it demonstrated: `TASK-WORKFLOW.md` asserted that `index` does not filter closed blockers, which was true when written and false the moment the plugin moved. |
| 2026-08-10 | → proposed | Raised from [T-073](T-073-decide-whether-to-keep-refcheck-now-that-upstream-has-ruled.md), which needed the version to explain why a predicted output line was absent. `medium` rather than low because the failure mode is silent: the gates pass, and the project records superseded behaviour as current — which it has already done once and called **L-59**. `xs` because the update is one command and the reading after it is bounded by two releases. `PH2` under the release split: a minor fix. |
