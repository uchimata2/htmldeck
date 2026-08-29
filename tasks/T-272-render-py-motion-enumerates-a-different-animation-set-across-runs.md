---
id: T-272
title: Make render.py motion enumerate the same animation set on every run of one deck
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-255]
work_package: PH1
owner: the project owner
business_value: high
effort: s
created: 2026-08-29
updated: 2026-08-29
shipped_in: unreleased
deliverables:
  - tools/deck/render.py
---

# T-272 — Make render.py motion enumerate the same animation set on every run of one deck

## 1. Specify

**Outcome**
`render.py motion` reports the same animations on the same deck every time it is run. Today it does
not: six consecutive runs of `python tools/deck/render.py motion examples/reference-deck.html
--into 3` on an unchanged tree returned **`17, 17, 18, 17, 17, 17`**. The eighteenth is
`(effect) on i#rulerRing.ruler-ring`, a 200 ms transition on the chrome, present in one run of six.

**Why it matters more than one row.** This is an instrument, and wave 1 of
[`../docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) exists because *work verified against
a lying instrument has to be verified again*. A before-and-after taken with this tool — which is
exactly what [T-232](T-232-two-entrance-motions-do-not-collapse-for-print.md) and
[T-268](T-268-three-chrome-and-timing-defects-in-deck-js.md) in B9 will do — can differ by an
animation for no reason in the deck. It is also the second intermittent instrument this batch has
met: [T-254](T-254-density-py-write-corrupts-every-self-closing-svg-tag.md)'s defect gave `0, 3, 3`
over three runs and cost the adopter the better part of a session for the same reason. **An
instrument that answers differently twice teaches a reader to distrust the deck rather than the
tool.**

**Scope**
- In: why the ruler ring's transition is in the set on some runs and not on others. The probe
  clicks `next` in a synchronous loop, so whether a CSS transition is created at all may depend on
  a style recalculation that the loop does not force — **that is a hypothesis and it is measured
  before anything is changed**
- In: whichever of *make it deterministic* or *report the variation honestly* the measurement
  supports. A count that is stated as stable and is not is worse than one that says it varies
- In: a run count high enough to say what the rate is, rather than one that saw it once
- Out: the seek arithmetic — [T-255](T-255-render-py-motion-seeks-past-the-delay.md) owns it and
  is closed
- Out: `--shots`, unless the measurement shows the same cause reaches it

**Inputs**
- [`tools/deck/render.py`](../tools/deck/render.py) — `MOTION_PROBE`, the click loop and the
  `before` set that decides which animations belong to the navigation
- the six runs above, taken 2026-08-29 on this tree while closing `T-255`
- [T-254](T-254-density-py-write-corrupts-every-self-closing-svg-tag.md) — the other intermittent
  instrument in this batch, and the record of what intermittency costs a reader

**Acceptance criteria**
- [ ] the rate is **measured over enough runs to state it**, before and after
- [ ] the set is stable across those runs, **or** the tool says which of its animations it cannot
      promise and why
- [ ] whichever it is, it is proved by seeding — the failing direction shown to fail (**L-125**)
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None yet. The hypothesis in the scope is a hypothesis; whoever implements it measures before
  committing to it.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Measure the rate over ten runs of the shipped code, recording the full animation set each time rather than its size | The rate, and **which** animation varies |
| 2 | Test hypothesis A — settle the page before taking the `before` set, so a load-time transition cannot be in it on one run and gone on the next | Ten more runs, and what the set became |
| 3 | Test hypothesis B — force a style flush after each click, so transition creation does not depend on when the browser last flushed | Ten more runs, then ten more |
| 4 | Take whichever branch of the acceptance criterion the measurement supports, and **ship nothing a measurement refused** | Either determinism or honest reporting |
| 5 | Seed the failing direction (**L-125**), at the comparator and at the printed line alike | The report shown to say it |
| 6 | `python tools/tasks/lint.py`, then `python tools/check_all.py`, separately | Both green |

## 3. Implement

**Decisions & assumptions**
- **Both remedies were measured and both were refused. Neither ships.** That is this project's own
  rule — a remedy is a hypothesis — and it is the whole result of the task — 2026-08-29.
  - *Settle before snapshotting* left the ruler ring appearing in **3 of 22** runs, no better than
    before, **and silently added a second `button` transition to every report**. A change that
    fixes nothing and moves the answer is strictly worse than the defect.
  - *Force a style flush after each click* looked clean over ten runs — **0 of 10** — and was
    **2 of 10** over the next ten. Ten runs against a one-in-ten event is a coin that came up
    heads; the first result was small-sample luck, and taking it would have shipped a fix proved
    by a run that was likely to be clean anyway.
- **So the tool stops claiming determinism it does not have, and reports the uncertainty.** That
  is the acceptance criterion's second branch, and it is reached by measurement rather than by
  preference — 2026-08-29.
- **It reads the page twice and compares.** One read cannot see a race; two can. It costs a second
  Chrome invocation, on a tool [`tools/check_all.py`](../tools/check_all.py) classifies as *an
  instrument, not a gate* — so no gate gets slower, and the cost falls where the answer is being
  read by a person — 2026-08-29.
- **The cause is object identity, not timing, and the tool now says so.** Membership is decided by
  whether an animation was in the `before` set, and Chrome re-targets one `CSSTransition` per
  property per element rather than creating a second. A chrome transition already live at load
  therefore stays on the page's side of the difference — unless it happened to have finished and
  left `getAnimations()` before the snapshot, which is the race. Saying that in the report is
  worth more than a number that is stable and wrong — 2026-08-29.

**Outputs produced**
- `tools/deck/render.py` — `animation_set`, `set_disagreement`, the second read in `cmd_motion`,
  the three verdict lines, and three `self_test` assertions

**What was measured**

| Measurement | Result |
| :--- | :--- |
| Ten runs of the shipped code, full set recorded each time | **1 of 10.** The one that varies is `(effect) on i#rulerRing.ruler-ring`, a 200 ms transition on the chrome; every other animation appeared in all ten. With the six informal runs that found it, **2 of 16** |
| Hypothesis A — settle the page, then take the `before` set | **3 of 22**, and the baseline moved from 17 to 18: a second `(effect) on button` transition entered every report. **Refused** |
| Hypothesis B — force a style flush after each click | **0 of 10**, then **2 of 10** on a second set. 2 of 20 overall. **Refused**, and the first ten are the reason the second ten were run |
| The shipped answer — two reads, compared | The report says *a second read of the same page agreed, animation for animation*, or names each animation the two reads disagree on and by how much |
| **Seeded, both directions (L-125)** | At the comparator: two identical reads report no disagreement, and an animation present in one and absent from the other is reported as `(label, 1, 0)`. At the printed line: a seeded second read produces `NOT PROMISED - a second read of the same page disagreed on 1 animation(s)` with the offender named |

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The rate is measured over enough runs to state it, before and after | met | 10 runs on the shipped code, 22 on hypothesis A, 20 on hypothesis B — 52 browser runs in all. **The rate is the finding**: at one in ten, ten runs cannot tell a fix from luck, which is what hypothesis B's first ten demonstrated |
| The set is stable across those runs, **or** the tool says which of its animations it cannot promise and why | met, by the second branch | Stability was attempted twice and measured as not achieved. The tool now reads twice, compares, and names what disagreed and why — object identity in the `before` set, stated in the output rather than left in a comment |
| Proved by seeding — the failing direction shown to fail (**L-125**) | met | Both the pure comparator and the printed line, row 5 of *What was measured* |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | met | `lint.py` all four steps green with the baselined **eleven** advisories. `check_all.py` **0 failures, 0 unclassified, 0 stale** |

**Kept beyond this task**
- **[L-138](../docs/lessons/L-138.md)** — *a run count is evidence about the fix only if it is large against the defect's rate*. The generic half of what happened here, and the half worth more than the ruler ring: this task nearly shipped a remedy proved by ten runs against a one-in-ten fault.

**Child fix tasks raised**
- none. **The attribution question is answered here rather than deferred**: whether the ruler
  ring's transition *ought* to count as the navigation's is a design question about a set
  difference, not a defect with a measured wrong answer, and the report now states the rule it
  applies. A task to change the rule would be work with no measurement behind it.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → specified | Ten runs of the shipped code put the rate at **1 of 10**, and named the animation: `(effect) on i#rulerRing.ruler-ring`. The scope's own hypothesis was written as a hypothesis, which is why it could be refused. |
| 2026-08-29 | → planned | Six steps, two of them hypotheses to be measured rather than applied. Step 4 is the one that matters: **ship nothing a measurement refused**. |
| 2026-08-29 | → in_progress | **Both hypotheses refused.** Settling before the snapshot was no better (3 of 22) and moved the baseline; the style flush was 0 of 10 and then 2 of 10, so its first ten were luck against a one-in-ten event. The tool now reads the page twice and names what the two reads disagree on — the acceptance criterion's second branch, taken because the measurement pointed there. |
| 2026-08-29 | → done | Every criterion met. **52 browser runs**, and the useful finding is about evidence rather than about the ruler ring: at one in ten, a ten-run green cannot tell a fix from a coin toss, and this task nearly shipped one. |
| 2026-08-29 | → proposed | Found while closing [T-255](T-255-render-py-motion-seeks-past-the-delay.md), by diffing two post-fix runs of one command on one unchanged deck. Raised under [`../docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) §4's *absorb what a batch finds* and **added to the running batch B1**, which is what that authority says to do rather than filing it for later. **`PH1`**: `render.py` ships in the published `0.6.0`, and `CLAUDE.md`'s condition is a defect in the published plugin rather than who found it. `parent: null` and `related:` — a task that raises another is not its parent, on the owner's `T-057`/`T-016` precedent. |
