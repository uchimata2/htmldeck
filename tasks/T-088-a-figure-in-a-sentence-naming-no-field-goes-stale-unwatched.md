---
id: T-088
title: A figure in a sentence that names no field goes stale unwatched, and two just did
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-060, T-068, T-077, T-082]
work_package: v0.3
owner: the project owner
business_value: medium
effort: l
created: 2026-08-11
updated: 2026-08-11
deliverables:
  - tools/docs/figures.py
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
- [x] The two figures corrected in `v0.2.0` are **re-seeded and go red**, naming the document, the
      numeral and the artifact property behind it
- [x] The false-alarm count over every document `figures.py` reads is measured and recorded, against
      the true-hit count, in the shape T-068 used
- [x] If the rate is worse than T-068's threshold the rule is **rejected and the measurement kept** —
      a recorded rejection is a result, and this criterion is met either way
- [x] `unanchored` remains a declared bucket with a reason, not a silent remainder
- [x] **A manifest entry naming an artifact that is absent or has moved fails the run**, rather than
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

**The mechanism, found before planning anything.** `audit()` binds a README numeral with
`bound(n, said, table)` — the sentence must name the label the command printed beside the value —
and `deck_facts()` already prints two artifact properties per deck under a label that *is* the
artifact's path. `words()` even documents the case: *path separators split, so the label
`examples/sort-window/sort-window.html` reaches a sentence that names `examples/sort-window`*.
**`declared()` never calls `bound()` at all.** It judges a numeral only through `claimed()`'s
*part of whole* shape and counts everything else as unanchored. So the binding this task is asked to
build already exists, is already tested, and is simply not reached from the five documents — which is
why two figures about a named file went stale in the one document that describes it.

That changes the shape of the work: the question is no longer *can a rule decide this* but *what does
the existing rule decide when it is pointed at these five pages*, and that is measurable rather than
arguable.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Promote `deck_facts()`'s hard-coded pair to a declared `ARTIFACTS` manifest, one reason per entry, and make an entry whose file is absent or moved **fail the run** rather than emit nothing | `tools/docs/figures.py` |
| 2 | In `declared()`, bind a numeral against the manifest's fields only — never the whole table, so no gate label re-enters by the door T-068 closed | `tools/docs/figures.py` |
| 3 | **Measure before keeping it.** Enumerate every numeral the new rule newly judges across all five documents, classify each by hand as a true hit or a false alarm, and record both counts against T-068's 30-to-5 | The measurement, in §3 |
| 4 | Re-seed the two figures `v0.2.0` corrected as self-test fixtures, judged by the message each produces | `tools/docs/figures.py` `self_test` |
| 5 | Keep `unanchored` a declared bucket with its reason, and say in the report what the manifest now covers | the report's wording |
| 6 | `figures.py`, `lint.py`, `check_scaffold.py` | three green runs, in §4 |

## 3. Implement

**Decisions & assumptions**
- **The binding is a link, not a name** — 2026-08-11. Three conditions have to hold together: the
  scope **links** the artifact, the numeral is followed within three words by a unit naming a
  property this tool computes, and the artifact is in the manifest. The link is what answers T-068:
  its 30 false alarms came from binding on words that are ordinary English elsewhere, and a markdown
  link to a path is the one reference a paragraph makes that cannot be a coincidence of vocabulary.
- **The scope is a list item, not a paragraph** — 2026-08-11, and this was a measurement rather than
  a preference. `sentences()` splits *"It is 220 KB in one file"* off from the sentence naming what
  *it* is, so a sentence-level scope cannot see the subject and the rule catches nothing. With the
  whole block as the scope it caught everything — including `BRIEF.md`'s *"all twelve slides carry a
  bottom line"*, bound to a link **thirty lines above it in a different bullet**. Right answer, and
  right by luck. Splitting the block at list-item boundaries dropped that judgement and kept every
  other one.
- **A spelled-out number counts inside this rule and nowhere else** — 2026-08-11. The file's standing
  rule is that a figure is a numeral, because in free prose *"two days"* outnumbers measurements six
  to one. Both figures `v0.2.0` corrected were **`five` / `six` hand-written SVG figures**, written
  as words, so a numeral-only rule would have missed half of exactly what this task was raised for.
  Inside the three conditions the unit has already said the number is a count.
- **`bytes` became a field of its own beside `KB`** — 2026-08-11. `examples/README.md` states the
  same size twice in one sentence, and only the rounded half was derivable here: the exact figure sat
  unwatched *beside* a watched one, and at `v0.2.0` both were wrong. A space-grouped byte count is
  two numerals to `PROSE_NUMERAL`, so this rule reads its own digit runs and lets the unit say where
  the number ends.
- **`ARTIFACT_UNITS` is keyed by `stem()`'s output, and finding that out was the only real trap.**
  `stem` strips the plural and then a trailing `e` unconditionally, so `bytes` arrives as `byt` and
  `slides` as `slid`. Keyed by the readable word, two of the four units silently never matched and
  the run went green having judged half of what it claimed to — the exact shape of defect this file
  exists to catch, in the file itself.

**The measurement, in the shape T-068 recorded its own**

| | T-068's rejected rule | This rule |
| :--- | ---: | ---: |
| True hits | 5 | **1** |
| False alarms | 30 | **0** |
| Figures judged | — | 6 |

The one true hit is a **third stale figure**, found on the rule's first run and known to nobody:
[`../docs/BRIEF.md`](../docs/BRIEF.md) *Definition of done* gave the reference deck as `214 KB`
against 231, written 2026-08-09 and stale ever since T-069's colophon and T-085's shell sync grew the
file. Corrected here — the bullet names a live file and states three present-tense properties of it,
which is not the struck-through dated record `DONE_ROW` already excuses.

The other five judgements are all correct and were all previously unanchored: `12 slides` of the
reference deck, and the built deck's `220 KB`, `225 639 bytes`, `12 slides` and `six figures`.
`unanchored` fell from 437 to 433 and remains a declared bucket with its reason printed.

**Outputs produced**
- [`../tools/docs/figures.py`](../tools/docs/figures.py) — `ARTIFACTS` and `missing_artifacts()`;
  `artifact_facts()` beside `deck_facts()`; `blocks()` under `sentences()`; `claim_scopes()`,
  `artifact_claims()` and `scope_claims()`; the manifest section in the report; two fixtures.
- [`../docs/BRIEF.md`](../docs/BRIEF.md) — the third stale figure, corrected.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The two figures corrected in `v0.2.0` are re-seeded and go red, naming document, numeral and property | met | Fixture 9 seeds the page's real wording. Three rows, not two — the exact byte count travels with the rounded one: `examples/README.md states 212 - claims 212 KB of examples/sort-window/sort-window.html, which is 220`, and the same for `217 050 bytes` and `five figures`. The fixture exits loudly if the page stops using that wording, rather than seeding nothing. |
| The false-alarm count over every document is measured and recorded against the true-hit count | met | The table above. Six figures judged across the five documents, **1 true hit and 0 false alarms**, against T-068's 5 and 30. Enumerated one at a time and read, not counted from a summary. |
| If the rate is worse than T-068's, the rule is rejected and the measurement kept | met, and the rule stands | It is better by both terms. The measurement also rejected one *version* of the rule: block-scope bound a correct figure by luck, and that is recorded above rather than left out because the verdict happened to be right. |
| `unanchored` remains a declared bucket with a reason | met | 433, and the report now states both halves of why: *in a sentence naming no field and in no block linking an artifact, so not judged.* The manifest is printed with every property it computes, so what the rule can reach is on the page rather than in the source. |
| A manifest entry naming an absent or moved artifact fails the run | met | `missing_artifacts()` takes a manifest so the fixture can hand it a file that is not there without touching the module; fixture 10 asserts both directions — a bogus entry is reported, and the live manifest is clean. `report()` counts it into `fails`, so it is a red run and not a note. |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-11 | → done | All five criteria met, and **the rule found a third stale figure on its first run** - `BRIEF.md` gave the reference deck as 214 KB against 231, stale since 2026-08-09 and reported by nobody. Measured 1 true hit against 0 false alarms, where T-068's rejected rule measured 5 against 30. Three things are worth carrying. The binding that works is a **link**, not a name: it is the one reference a paragraph makes that cannot be a coincidence of vocabulary, which is the whole of T-068's objection. The scope is a **list item**, decided by measurement after block-scope bound a correct figure to a link thirty lines away - right by luck, and a rule that is right by luck is the one T-068 rejected. And `ARTIFACT_UNITS` is keyed by `stem()`'s output, because `stem` takes `bytes` to `byt` and `slides` to `slid`: keyed by the readable word, two of four units never matched and the run went green having judged half of what it claimed - this file's own defect class, in this file. |
| 2026-08-11 | (no change) | Owner answered the open question the day it was raised: **allow a manifest**. §1 records what that buys (the rule declares which artifacts have measurable properties instead of inferring it) and what it owes: an entry whose artifact is gone must fail, since a hand-kept list is only acceptable here because §8's cadence re-reads it. Added as a fifth acceptance criterion so the condition is checkable rather than remembered. |
| 2026-08-11 | → proposed | Raised while running [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) §8's step 4 for the `v0.2.0` release, which is the step no gate covers and the third release running in which it has found something. `v0.3` rather than `v0.2`: the effort is `l` by the rule in [`../CLAUDE.md`](../CLAUDE.md), because the deliverable is a measurement over every document the gate reads and a rule that survives it, not a patch to one binding. Not `v0.1`: no adopter's deck can hit this, it is a defect in this project's own record. |
