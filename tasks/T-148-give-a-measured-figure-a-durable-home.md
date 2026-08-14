---
id: T-148
title: Give a measured figure a durable home
type: deliverable
status: done
phase: review
parent: T-130
blocked_by: []
related: [T-130]
work_package: PH3
finding: CE-08
shipped_in: unreleased
owner: the project owner
business_value: medium
effort: xs
created: 2026-08-14
updated: 2026-08-14
deliverables:
  - tools/check_all.py
  - docs/PUBLISHING.md
  - docs/lessons/L-95.md
---

# T-148 — Give a measured figure a durable home

## 1. Specify

**Outcome**
A figure this project measures once stops living only in the chain of session handovers, where it
propagates without anything able to check it. **The finding is `CE-08`**, stated in
[`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
§8; it is not restated here.

**The instance is measured and recorded** in [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md)
§8, `BP-2`: five successive handoffs carried *"the release gate takes 7–11 minutes"*; it is **154
seconds**. No committed document was wrong, because **no committed document stated it at all** — the
figure had no durable home, so nothing could be stale and nothing could be checked.

**This repository already has the mechanism**: `tools/docs/figures.py` binds a pasted figure to the
command that produces it and reports drift. A figure with a home is a figure that mechanism can
reach; a figure in a handoff is outside every gate this project owns.

**Scope**
- In: where a measured figure of this kind belongs, and the run-time figure as the first instance.
- In: whether it is bound as a checked figure or written as a dated measurement, which are different
  contracts.
- Out: the handoff format, which belongs to a skill this project does not own — observations about it
  go to [`../docs/upstream/handoff-skill.md`](../docs/upstream/handoff-skill.md).

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.2 — read before starting; §8 `BP-2` — the
  instance
- `R8` §8 — `CE-08` in full
- **L-74** in [`../docs/LESSONS.md`](../docs/LESSONS.md) — make a stored copy fail loudly in both
  directions

**What specifying must settle**
- Which figures qualify. *Everything measured* is a rule nobody keeps; *the release gate's run time*
  is one figure and not a rule at all.
- Whether the home is a checked figure under `figures.py` or a dated line in
  [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md), and what each costs when it goes stale.

### 1a. What specifying settled — 2026-08-14

**The figure had already drifted again before this task opened it.** `BP-2` records 154 seconds; a run
on 2026-08-14 took **164**. Ten seconds is nothing and that is the point — the number moves on every
run, on every machine, under every load, and any document stating it is wrong by the next one.

**So the home is not a checked figure, and it is not a dated line either.** `figures.py` binds a
figure to the command that prints it and fails on drift; bound that way this one fails the gate for
*load*. Written as prose in [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) it goes stale exactly as
**L-94** point 4 says — self-measurement is not self-updating.

**What the figure was carried for was never its value.** Every session repeating it answered one
question: *foreground or background?* That answer does not change between 154 and 164 seconds. It
changes between seconds and minutes. **The decision is coarser than the figure**, and the coarse fact
is the one that keeps.

**So: write the decision, print the figure, state no number.** `PUBLISHING.md` §8 step 1 says the gate
takes minutes and must be backgrounded; `check_all.py` prints its own elapsed seconds on every run.
**No document holds the number, so no document can hold a stale one** — which is the rule
[`../CLAUDE.md`](../CLAUDE.md) already applies to the tier-1 bound, *no constant is written anywhere*,
generalised instead of repeated.

**Which figures qualify**, since *everything measured* is a rule nobody keeps. A figure is owed a
durable home when something is **done differently** at different values. Then: if the decision is
coarser than the figure, write the decision and let the command print the value; if the decision needs
the value, bind it with `figures.py` and declare it `volatile` when it counts the repository rather
than a decision. A figure that decides nothing gets a dated record and no home at all.

**A dated record is not a stated figure**, and the distinction is what lets this task record 164 s
without violating its own rule. *Measured 164 s on 2026-08-14* stays true forever; *the gate takes
164 s* decays. `figures.py` already draws that line when it skips a struck-through done row.

**Acceptance criteria**
- [x] Which figures qualify is written as a test, not as *everything measured*
- [x] The run-time figure has a home, and no live document states a number for it
- [x] `check_all.py` reports its own elapsed time on every run
- [x] The rule outlives the task, so the next figure is not re-argued
- [x] `python tools/tasks/lint.py` green

**Open questions**
- ~~**Whether this needs a specify pass at all.**~~ **Answered 2026-08-14 by the owner: it does not
  need a decision pass.** It is `xs` with a known instance and a mechanism that already ships, so a
  specification written only to decide whether to spend the hour costs about what the hour costs.
  **This left the decision batch and takes the ordinary lifecycle in its turn** — `specify → plan →
  implement → review` in one pass, which is mandatory however small
  ([`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §2). What was dropped is the parking, not the phases.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Re-measure the gate, so the decision rests on a reading rather than on `BP-2`'s | The 2026-08-14 figure |
| 2 | Make `check_all.py` print its own elapsed seconds beside the verdict | The figure, where it cannot go stale |
| 3 | State the *decision* in [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) §8 step 1 — minutes, background it — and no number | The durable half |
| 4 | Write the rule as a lesson, since the next figure will not be this one | `L-95` |
| 5 | Close `BP-2` in [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §8 with the dated reading | The register current |

## 3. Implement

**The gate, measured 2026-08-14: 164 s.** `BP-2` recorded 154 on 2026-08-13 and five handoffs before
it carried *7–11 minutes*, which is four times the truth. **The drift between the two real readings is
6%, and between the carried figure and the truth it is 300%** — the gap is not measurement noise, it
is what happens to a number nothing owns.

**One line of code and one sentence of prose.** `check_all.py`'s verdict line now ends with its own
elapsed seconds, and `PUBLISHING.md` §8 step 1 says the gate takes minutes and must be run in the
background. Neither states a number that can decay. The comment in `check_all.py` says why, because a
`time.time()` around `main` looks like instrumentation and is a remedy.

**What was rejected, and why it is worth recording.** Binding the figure with `figures.py` was the
obvious move — T-148 was raised naming that mechanism, and this repository already uses it for exactly
this shape of problem. It fails on a property the mechanism cannot see: `figures.py` distinguishes a
figure that describes a *decision* from one that counts the *repository*, and a run time is neither.
It describes **the machine**, and the gate would go red for load. The `volatile` category would have
demoted it to *reported*, which is a figure nobody acts on — the state it was already in.

**Decisions & assumptions**
- **No live document states the run time.** The decision it drives is coarser than the figure, so the
  decision is written and the figure is printed — `L-95` — 2026-08-14.
- **A dated record is not a stated figure**, which is how this task and `BP-2` can both hold `164 s`
  without re-creating the defect — 2026-08-14.
- **The qualifying test is *does anything act differently at different values*.** *Everything
  measured* was rejected as unkeepable, and the task said so before the work started — 2026-08-14.

**Outputs produced**
- `tools/check_all.py` — its own elapsed time on every run
- [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) §8 step 1 — the decision, no number
- [`../docs/lessons/L-95.md`](../docs/lessons/L-95.md) — the rule, and the test for the next figure
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §8 — `BP-2` closed with the dated reading

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Which figures qualify is written as a test | met | §1a, and `L-95` carries it out of this task |
| The figure has a home, and no live document states a number | met | printed by the command; `PUBLISHING.md` states minutes |
| `check_all.py` reports its own elapsed time | met | on the verdict line, both green and red |
| The rule outlives the task | met | `L-95`, indexed and resolving — `lessons.py` reports 95 lessons, 95 rows |
| `python tools/tasks/lint.py` green | met | four checks |

**The band held and the shape did not.** `CE-08` is `xs` and this was `xs`; what the row proposed —
give the figure a home — is the opposite of what the work did, which was to make sure no document
holds it. That is the third finding in this audit whose stated remedy the measurement refused
(**L-90**), and the first where the refusal is the deliverable rather than a note beside it.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-14 | → proposed | Raised at the owner's direction with the rest of the unraised findings; it ranked eleventh and was never a candidate. Scheduled to `plan` and no further, with one argument against that for this row in particular: it is `xs`, its instance is already measured, and the mechanism it would use ships — so the specification may be the expensive half. |
| 2026-08-14 | (unchanged) | **Removed from the decision batch the same day, the argument above accepted.** It sits in the execution order as ordinary work and runs the whole lifecycle when its turn comes. A task whose worth is not in doubt does not need a pass to establish it. |
| 2026-08-14 | → specified → planned | §1a refused the mechanism the task was raised naming. `figures.py` sorts a figure into *describes a decision* or *counts the repository*; a run time is neither, it describes the machine, so binding it fails the gate for load and `volatile` demotes it to the reported-and-ignored state it was already in. Re-measured first: 164 s against `BP-2`'s 154. |
| 2026-08-14 | → in_progress → done | **The deliverable is that no live document states the figure.** The decision it drives — background it — is coarser than the number, so `PUBLISHING.md` §8 states minutes and `check_all.py` prints its own seconds. `L-95` carries the test out of this task. Third finding in this audit whose stated remedy the measurement refused (**L-90**), and the first where the refusal *is* the deliverable. |
