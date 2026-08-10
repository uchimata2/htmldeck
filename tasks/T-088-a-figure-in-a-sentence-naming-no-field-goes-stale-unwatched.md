---
id: T-088
title: A figure in a sentence that names no field goes stale unwatched, and two just did
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-060, T-068, T-077, T-082]
work_package: v0.3
owner: the project owner
business_value: medium
effort: l
created: 2026-08-11
updated: 2026-08-11
deliverables: []
---

# T-088 — A figure in a sentence that names no field goes stale unwatched, and two just did

## 1. Specify

**Outcome**

`figures.py` reports `unanchored 432` across the five documents it reads beyond the README, and an
unanchored numeral is one the gate has decided it cannot judge. That bucket is not empty of defects:
the `v0.2.0` release found **two stale figures inside it**, in
[`../examples/README.md`](../examples/README.md), describing the deck this repository ships as its
generated example. At the end of this task the gate can decide a figure that restates a **measurable
property of a named artifact** — a file's size, a count of its parts — without widening back into the
false-alarm rate [T-068](T-068-bind-a-prose-figure-to-a-field-not-to-the-whole-output.md) measured
and rejected.

**The two, and why each was invisible.** `examples/README.md` gave the built deck as *"212 KB in one
file — 217 050 bytes — 12 slides, five hand-written SVG figures"*. It is 225 639 bytes and carries
six `class="fig"` figures. Both numerals sit in a sentence naming no field any command prints, so the
gate skipped them, correctly by its own rule. The front `README.md` states the same two properties
**four lines of prose apart in another document** and was right about both, because there they are
bound. So the repository held a right answer and a wrong answer to the same question, and the gate
compared neither to the other.

**Why this is not simply T-068 reopened.** T-068 rejected binding by *vocabulary* after measuring 30
false alarms against 5 true hits, and that measurement stands. The proposal here is narrower and
structural: the subject is a **named artifact in the repository** (`sort-window.html`) and the
predicate is a property of that file which a tool can compute. That is the same shape as the figures
already `compared` — *printed by the deck files themselves* — differing only in that the sentence
names the artifact rather than the field. Whether that difference is bridgeable at an acceptable
false-alarm rate is this task's question, and it is answered by measurement, not by argument.

**Scope**
- In: a binding rule for *property of a named artifact*, measured against the whole corpus of
  documents `figures.py` reads, with its true-hit and false-alarm counts recorded the way T-068
  recorded its own
- In: the two figures already corrected stay corrected; this task is the rule, not the instance
- Out: widening the `unanchored` bucket generally. A rule that decides more of 432 by guessing is
  the failure T-068 already paid for
- Out: `volatile` figures, which are declared and reported rather than failed on purpose

**Inputs**
- [`../tools/docs/figures.py`](../tools/docs/figures.py) — the partition, and the `unanchored` bucket
- [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) §6 — what a figure is bound to, and what the check
  still cannot see
- [T-068](T-068-bind-a-prose-figure-to-a-field-not-to-the-whole-output.md) — the rejected rule and
  the 30-against-5 measurement that rejected it
- [T-060](T-060-check-that-the-readmes-pasted-figures-still-match-their-commands.md) — the gate

**Acceptance criteria**
- [ ] The two figures corrected in `v0.2.0` are **re-seeded and go red**, naming the document, the
      numeral and the artifact property behind it
- [ ] The false-alarm count over every document `figures.py` reads is measured and recorded, against
      the true-hit count, in the shape T-068 used
- [ ] If the rate is worse than T-068's threshold the rule is **rejected and the measurement kept** —
      a recorded rejection is a result, and this criterion is met either way
- [ ] `unanchored` remains a declared bucket with a reason, not a silent remainder

**Open questions**
- Whether *property of a named artifact* is decidable at all without a manifest of which artifacts
  have computable properties. A manifest is a list kept by hand, which is the failure mode
  [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) §2 argues against — but a list of two decks is not
  the same risk as a list of every document. The project owner answers.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- `deliverables/...`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-11 | → proposed | Raised while running [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) §8's step 4 for the `v0.2.0` release, which is the step no gate covers and the third release running in which it has found something. `v0.3` rather than `v0.2`: the effort is `l` by the rule in [`../CLAUDE.md`](../CLAUDE.md), because the deliverable is a measurement over every document the gate reads and a rule that survives it, not a patch to one binding. Not `v0.1`: no adopter's deck can hit this, it is a defect in this project's own record. |
