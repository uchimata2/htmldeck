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
- [ ] **A manifest entry naming an artifact that is absent or has moved fails the run**, rather than
      covering nothing in silence — the condition the owner's 2026-08-11 answer rests on

**Open questions**
- ~~Whether *property of a named artifact* is decidable at all without a manifest of which artifacts
  have computable properties.~~ **Answered by the owner 2026-08-11: allow a manifest.** So the rule
  does not have to infer which nouns name a measurable artifact, which was the hard half and the
  half most likely to reproduce T-068's false-alarm rate. It declares them.

  **What the manifest owes, given it is a list kept by hand.**
  [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) §2 is the argument against enumerations, and it is
  not withdrawn: a hand-kept list goes stale *silently*. What makes this one acceptable is that it
  cannot. §8's per-deck five already run against both shipped decks every release, so a manifest of
  those two is re-read on the same cadence as the decks themselves, and an entry naming a file that
  has moved fails the run rather than quietly covering nothing. **That property is a requirement on
  the implementation, not an observation about it** — a manifest entry whose artifact is absent must
  fail, in the same shape as [T-051](T-051-a-check-with-no-subject-must-not-report-a-pass.md)'s rule
  that a check with no subject may not report a pass. An entry that can go stale without a red run
  is this task's own defect, not a compromise it accepted.

**N-5, from the first external deck — the pattern recurred in a deck this project never touched.**
Routed here 2026-08-11 by [T-092](T-092-product-feedback-from-the-first-external-deck.md). The
ledger omission [T-082](T-082-the-worked-examples-figure-ledger-omits-figures-that-reach-slides.md)
found in the worked example, and T-087 then looked for in the reference deck, appeared again
**independently, in an unrelated twelve-slide deck built by an adopter**. That does not change this
task's deliverable; it changes what the deliverable is worth. Two instances in decks this repository
wrote could be one house habit — the same hand making the same omission twice — and a third in a deck
written by someone who had read only the shipped skill is the evidence that separates *our habit*
from *a gap in what the tool asks for*. Worth stating in this record because the false-alarm
measurement §1 requires is the expensive half, and its justification rests on how general the defect
is.

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
| 2026-08-11 | (no change) | Owner answered the open question the day it was raised: **allow a manifest**. §1 records what that buys (the rule declares which artifacts have measurable properties instead of inferring it) and what it owes: an entry whose artifact is gone must fail, since a hand-kept list is only acceptable here because §8's cadence re-reads it. Added as a fifth acceptance criterion so the condition is checkable rather than remembered. |
| 2026-08-11 | → proposed | Raised while running [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) §8's step 4 for the `v0.2.0` release, which is the step no gate covers and the third release running in which it has found something. `v0.3` rather than `v0.2`: the effort is `l` by the rule in [`../CLAUDE.md`](../CLAUDE.md), because the deliverable is a measurement over every document the gate reads and a rule that survives it, not a patch to one binding. Not `v0.1`: no adopter's deck can hit this, it is a defect in this project's own record. |
