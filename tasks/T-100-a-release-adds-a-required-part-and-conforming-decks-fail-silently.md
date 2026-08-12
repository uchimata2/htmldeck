---
id: T-100
title: A release adds a required part, and every conforming deck becomes non-conforming in silence
type: admin
status: done
phase: review
shipped_in: unreleased
parent: null
blocked_by: []
related: [T-092]
work_package: PH3
owner: the project owner
business_value: medium
effort: xs
created: 2026-08-12
updated: 2026-08-12
deliverables:
  - docs/PUBLISHING.md
---

# T-100 — A release adds a required part, and every conforming deck becomes non-conforming in silence

## 1. Specify

**Where this came from.** The adopting project, upgrading 0.2.0 → 0.2.1. It is `N-7` in that
project's own `HTMLDECK-FEEDBACK.md`, filed here because a recommendation that never leaves the
adopter's document has not been filed.

**What happened.** A deck that passed every gate on 0.2.0 — `check.py` clean, `shell.py check` `OK`,
`theme.py check` nine verdicts all passing — was **not edited at all**. The plugin was upgraded. The
same three gates then returned:

| Gate | 0.2.0 | 0.2.1 |
| :--- | :--- | :--- |
| `check.py` | 0 failures | **5 failures** — `DS-009` ×3, `DS-013`, `DS-229` |
| `shell.py check` | `OK`, carries the shipped shell unchanged | **`NOT A SHELL`** — no `<script id="preflight">` anchor |
| `theme.py check` | 9 verdicts, all pass; 115 tokens required | **`DS-013` FAIL**; 116 required — `--scrim` not declared |

**All six are one feature.** 0.2.1's capability preflight: `DS-009` wants the preflight and the
degraded state, `DS-229` wants `.preflight` and `.qv` at one per deck and finds none, `DS-013` wants
the `--scrim` token the scrim uses, and `shell.py` will not call the file a shell without the anchor.

**This is not a defect and is not filed as one.** The preflight is documented in `DESIGN-SYSTEM.md`,
`THEME-CONTRACT.md` and `COMPONENT-CONTRACT.md` before any gate enforces it. htmldeck does exactly
what it says.

**It is the second release in a row to do it, which is what makes it worth a task.** 0.2.0 added the
per-slide `Sources` field and failed all twelve slides of a deck written the week before — the
adopter hit that one too, and worked through it the same way. Both times: the adopter met the
contract, the contract moved, and the first news of it was a wall of failures against an artefact
nobody had touched.

**The need.** One line per release naming **which existing decks stop conforming, and what the
smallest edit is**. The maintainer knows this at the moment of the change. The adopter reconstructs
it from failure output, by reading rules until five failures and a refusal collapse into one
feature.

**The expensive half is not the hour of reading.** It is that an adopter who has not baselined the
old build **cannot tell a new requirement from a regression**. The first instinct on seeing six
failures after an upgrade is that the upgrade broke something. This adopter could tell the
difference only because it ran every gate on the untouched deck *before* upgrading — a habit it
holds because an earlier htmldeck rebuild taught it. A first-time adopter has no such habit and will
read a documented new requirement as a broken release.

**Scope**
- In: deciding whether a release note carries a *what stops conforming* line, and where it lives.
- Out: changing the preflight requirement or any gate. The requirement is fine; its arrival is the
  subject.
- Out: the adopter's own migration. That is their task and is already in hand.

**Acceptance criteria**
- [ ] A release that adds or tightens a required part says so in a place an upgrader reads, naming
      the rule ids that will newly fail and the smallest edit that satisfies them
- [ ] The two releases that have already done this are covered retrospectively, or a deliberate
      decision not to is recorded — 0.2.0's `Sources` field and 0.2.1's preflight
- [ ] The guidance says to baseline before upgrading, or the release note makes baselining
      unnecessary by naming the expected new failures

**Open questions**
- **Whether this belongs in a release note, in `build.md`, or in the gate output itself.** The third
  is the strongest and the most work: a gate that knows a rule is new in this version could say
  *new in 0.2.1* beside the failure, and no adopter would ever need the baseline. — the project owner

## 2. Plan

**Phase: `PH3`.** Not a defect in the published plugin — the requirement is documented before it is
enforced, and the task says so — and PH2 is shipped, so everything that is not such a defect goes
here. Derived; the task arrived with `work_package: none`.

**The open question is answered: a step in the release sequence, not the gate output.** *New in
0.2.1* beside a failing verdict is the stronger answer and was the rival; it needs every gate to
carry a rule-to-version table, which is `m`-sized work and a second copy of a fact the release
already knows. `PUBLISHING.md` §8 is the enumeration a release runs anyway, it has already caught
two red checks nobody would have run, and a row there costs one sentence per release.

| # | Step | Where |
| :--- | :--- | :--- |
| 1 | A step: name what stops conforming, before tagging | §8, new step 5 |
| 2 | Make the release note carry it, so an upgrader reads it | §8, step 7 |
| 3 | The table, and the two releases that already did this | §8.1 |

## 3. Implement

**§8 is eight steps now.** Step 5 — *name what stops conforming* — sits before the tag, because the
maintainer knows the answer at that moment and reconstructs it later from nothing. Step 7 carries
§8.1's row verbatim into the release note, which is where an upgrader is standing: §2's own test is
*what does a stranger read before they have installed anything*, and a release note passes it.

**§8.1 is the table, with all three releases in it.** `0.2.0`'s `Sources` field and `0.2.1`'s
preflight are entered retrospectively, each naming the gates that newly bite and the smallest edit
— for the preflight, one `shell.py preflight` run and one token. `0.2.2`'s row is written in
advance, from this batch, and says explicitly which of its four changes newly fail a conforming deck
and which two cannot.

**Baselining is answered by the second half of the criterion rather than the first.** The guidance
does not tell adopters to baseline; the row makes it unnecessary, and §8.1 says so in those terms.
Telling every adopter to snapshot before every upgrade is a cost paid by everyone to save the
maintainer a sentence.

**A release with nothing to say writes that.** An absent row and a forgotten one are the same shape,
which is the failure mode this whole section exists for.

## 4. Review

| Criterion | Verdict | Evidence |
| :--- | :--- | :--- |
| A release that adds or tightens a required part says so where an upgrader reads, naming the rule ids and the smallest edit | **met** | §8 step 5 requires the row; step 7 puts it in the release note. §8.1's columns are exactly *what newly fails* and *the smallest edit* |
| The two releases that already did this are covered retrospectively | **met** | §8.1 rows for `0.2.0` and `0.2.1`. The `0.2.1` row carries all six failures the adopter met, named as one feature |
| The guidance says to baseline before upgrading, or the release note makes baselining unnecessary | **met, by the second half** | §8.1's opening states it: naming the failures here and in the note is what makes baselining unnecessary. No baselining instruction was added |

**What this does not fix.** The two releases already published cannot gain the line — their notes
are on the forge as written. §8.1 is where an adopter upgrading from either finds it now, and that
is the whole of the retrospective half.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-12 | → proposed | Filed from the adopting project's `HTMLDECK-FEEDBACK.md` `N-7`, written the same day it was found. The adopter upgraded, ran the same gates on an untouched deck, and compared against a pre-upgrade baseline — which is the only reason the report can say *these six failures are one documented feature* rather than *the upgrade broke our deck*. Filed as feedback rather than as a defect because the requirement is documented before it is enforced; the subject is how it arrives, not what it asks for. |
| 2026-08-12 | → done | Phase derived as `PH3`. The open question was answered *a step in `PUBLISHING.md` §8*, over the stronger *new in 0.2.1* in gate output, which is `m`-sized and a second copy of what the release knows. §8 gained step 5 and §8.1; three releases are in the table, two of them retrospective. |
