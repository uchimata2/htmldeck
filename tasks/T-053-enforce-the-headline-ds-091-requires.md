---
id: T-053
title: Enforce the headline DS-091 requires, and excuse the fragment count no check can reach
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-051, T-038, T-005, T-037]
work_package: none
shipped_in: 0.1.0
owner: the project owner
created: 2026-08-09
updated: 2026-08-12
deliverables:
  - tools/deck/audit.py
  - tools/deck/static_variants.py
---

# T-053 — Enforce the headline DS-091 requires, and excuse the fragment count no check can reach

## 1. Specify

**Outcome**
A slide with no headline fails the gate. DS-091's remaining clause — the fragment budget — is
excused **in writing** with what would close it, rather than left as an unstated hole inside a rule
the account reports as `checked`.

**Why this one**
[T-051](T-051-a-check-with-no-subject-must-not-report-a-pass.md) §4 recorded that a deck whose
slides carry no headline passes DS-091 and nothing objects, and attributed it to a **gap in the
ruleset**. *That attribution is wrong, and correcting it is part of this task.* DS-091 reads:

> Per slide: **one** headline ≤ 6 words plus ≤ 3 supporting fragments.

The rule requires the headline. **The gap is in the check**, and it is wider than one clause — the
rule has three and the gate decides one:

| Clause | Decided today | |
| :--- | :--- | :--- |
| one headline per slide | **no** | the vacuity T-051 found |
| headline ≤ 6 words | yes | `longHeadlines` |
| ≤ 3 supporting fragments | **no** | noticed by [T-038](T-038-the-gate-emits-verdicts-for-judge-rules-and-one-wrong-id.md) §3 and not closed |

**Measured on the reference deck before specifying** — all 12 slides carry exactly one headline of
3 to 5 words, so clause 1 is enforceable at no cost to the conforming deck.

**Clause 3 is a different matter, and the deck is what settles it.** A count of tier-one runs puts
three slides over budget, at 4, 5 and 9. Read, those runs are the **eyebrow** (`03 · The problem`),
a **stat figure and its label** (`11` / `minutes, average wait`) which is one thing and not two, the
**assumption marker** (`Illustrative model`) and the **provenance mark** — deck furniture that
DS-104 and DS-105 *require*. Counting them as supporting fragments would set three rules against
each other, so **the reading is wrong, not the deck** (**L-38**: a threshold invented to fit one
deck is not a measurement).

**Scope**
- In: a verdict for *one headline per slide*, and the DS-091 row's declaration in
  `ABSENCE_IS_A_PASS` updated to match what then guards it.
- In: the fragment clause excused in writing, naming what would close it — the argument above,
  where a reader will find it.
- In: correcting T-051 §4, which states the wrong diagnosis.
- Out: amending DS-091. The rule says what it means; nothing here is a case for changing it.
- Out: inventing a `.fragment` class so the count becomes measurable. That is a rule amendment and
  the owner's, and adopting markup to make a check work is backwards (the DS-026 precedent).
- Out: teaching the coverage account to report a partially-checked rule. Real, wider than DS-091,
  and raised as a child rather than absorbed here.

**Inputs**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §3.3 — DS-090 to DS-092
- [`tools/deck/audit.py`](../tools/deck/audit.py) — `PROBE`, `render_verdicts`, `ABSENCE_IS_A_PASS`
- [`tools/deck/check.py`](../tools/deck/check.py) — `DEFERRED`, and why an excusal is a candidate task
- [T-051](T-051-a-check-with-no-subject-must-not-report-a-pass.md) §3 — the audit this came out of
- [`docs/LESSONS.md`](../docs/LESSONS.md) — **L-36**, **L-38**, **L-44**

**Acceptance criteria**
- [ ] A deck with a headline-less slide fails DS-091, demonstrated on a variant rather than argued
- [ ] The reference deck still passes, and the coverage account is unmoved at 78 of 111
- [ ] The fragment clause's excusal is written where a reader of the check will find it, and says
      what would close it
- [ ] T-051 §4 no longer claims the ruleset requires no headline
- [ ] `ABSENCE_IS_A_PASS` still describes DS-091 truthfully, and the self-test verifies the guard

**Open questions**
- none — the fragment definition is settled above, against the deck, and the rest follows.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Probe every slide for its headline count, not only the word count of the first one | `audit.py` `PROBE` |
| 2 | A verdict for clause 1, and DS-091's declaration moved from `prohibition` to the guard that now holds | `audit.py` |
| 3 | The fragment clause excused in writing beside the row, with the eyebrow / stat-label / marker argument and what would close it | `audit.py` |
| 4 | A variant that deletes a headline, and the gate required to catch it | `static_variants.py` |
| 5 | Correct T-051 §4; raise the partial-coverage child | `tasks/` |

## 3. Implement

**Decisions & assumptions**

- **DS-091 is not amended** — 2026-08-09. The rule already requires the headline; only the check was
  short. Amending a rule to match what its check happens to do is the inversion this repository has
  refused twice ([T-052](T-052-two-hard-judge-failures-in-the-reference-deck.md), DS-026's excusal).
- **A headline is `.headline`, and exactly one per slide** — the class is what every other rule and
  the probe already treat as the headline, so nothing new is invented. `!== 1` rather than `< 1`,
  because *one* is what the rule says and two headlines is the same defect as none.
- **The fragment clause is excused in writing, beside the row rather than in `DEFERRED`** —
  2026-08-09. `DEFERRED` is keyed by rule, and DS-091 *is* checked; an entry there would make the
  account report a stale excusal for a rule two of whose clauses the gate decides. That the excusal
  therefore has nowhere proper to live is a real defect in the account and is
  [T-054](T-054-record-which-clauses-of-a-rule-the-gate-decides.md), not something to work around
  quietly here.
- **The fragment count is not measured at all**, not even reported. A number nothing consumes, whose
  definition the task has just argued is wrong, is worse than an absence — it would be re-used.

**Outputs produced**
- [`tools/deck/audit.py`](../tools/deck/audit.py) — `headlineCounts` in the probe, the clause-1
  verdict, the excusal argument, and DS-091's corrected `ABSENCE_IS_A_PASS` entry
- [`tools/deck/static_variants.py`](../tools/deck/static_variants.py) — `slide-with-no-headline`
- [T-051](T-051-a-check-with-no-subject-must-not-report-a-pass.md) §4 — the wrong diagnosis corrected

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A deck with a headline-less slide fails DS-091, demonstrated on a variant | **met** | `slide-with-no-headline  breaks DS-091 -> CAUGHT`, reporting `slides without exactly one headline: 1  The window shuts i...`. Suite at 7 of 7 rendered |
| The reference deck still passes, and the account is unmoved at 78 of 111 | **met** | `checked 78 · failing 0 · SILENT 0 · buckets sum to 111 = owned`. DS-091 now carries two rows, both passing; a rule's row count does not move the account |
| The fragment clause's excusal is written where a reader of the check will find it, and says what would close it | **met** | Beside the DS-091 rows in `render_verdicts`, with the measured argument — 4, 5 and 9 tier-one runs on three conforming slides, all eyebrow, stat label, assumption marker and provenance mark. **Partly met in placement**: it is a comment rather than something `check.py` reports, which is T-054 |
| T-051 §4 no longer claims the ruleset requires no headline | **met** | Struck through and corrected in place, so the wrong diagnosis stays visible rather than being erased |
| `ABSENCE_IS_A_PASS` still describes DS-091 truthfully, and the self-test verifies the guard | **met** | Moved `prohibition` → `guarded by DS-081`, and `audit.self_test()` requires DS-081 to be failing on the nothing-was-found measurement, which it is |

**What the fragment clause cost to decide, since the answer was *no*.** The reference deck's three
over-budget slides run to 4, 5 and 9 tier-one runs, and reading them is what settled it: `03 · The
problem` is the eyebrow, `11` and `minutes, average wait` are one stat and its label, and
`Illustrative model` is the assumption marker DS-104 requires. **A fragment count would have made
DS-104 and DS-105 force a DS-091 failure** — three rules against each other over markup no rule
asks for. The rule is right, the deck is right, and the DOM does not carry the distinction.

**Child fix tasks raised**
- [T-054](T-054-record-which-clauses-of-a-rule-the-gate-decides.md) — the account counts rules, not
  clauses, so an unreachable clause hides inside a `checked` rule and its excusal has nowhere to go
- [T-055](T-055-a-variant-that-leaves-malformed-markup.md) — the new check fired on
  `slide-is-not-a-section`, whose slide does have a headline; that variant never closes its own tag,
  so it has been testing parser repair

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-09 | → done | Clause 1 checked, clause 3 excused with the argument, and the reference deck unmoved at 78 of 111 — DS-091 carries two rows now and a rule's row count does not move the account. Two children raised rather than absorbed: the excusal has **nowhere proper to live** because the account is keyed by rule and DS-091 is `checked` ([T-054](T-054-record-which-clauses-of-a-rule-the-gate-decides.md)), and the new check fired on a variant whose slide does have a headline, which turned out to be a variant that never closes its own tag ([T-055](T-055-a-variant-that-leaves-malformed-markup.md)). |
| 2026-08-09 | → proposed | Raised from [T-051](T-051-a-check-with-no-subject-must-not-report-a-pass.md) §4, whose diagnosis was wrong: DS-091 does require a headline, in its own first clause, so this is a check gap and not a ruleset one. Measuring the reference deck before specifying settled both halves — clause 1 is free, all 12 slides already conform; clause 3 cannot be counted without counting the eyebrow, the stat label and the assumption marker as supporting fragments, which would set DS-091 against DS-104 and DS-105. |
