---
id: T-054
title: Record which clauses of a rule the gate decides, not only which rules it reaches
type: fix
status: done
phase: review
parent: T-053
blocked_by: []
related: [T-037, T-043, T-051, T-005]
work_package: PH3
owner: the project owner
business_value: medium
effort: l
created: 2026-08-09
updated: 2026-08-18
shipped_in: unreleased
deliverables: [tools/deck/check.py]
---

# T-054 — Record which clauses of a rule the gate decides, not only which rules it reaches

## 1. Specify

**Outcome**
The coverage account can say that a rule is **partly** decided, and where the rest of it went. A
clause no check reaches is recorded the way an unreached *rule* already is — with a reason and what
would close it — instead of disappearing inside a rule the account reports as `checked`.

**Why this one**
The account is per rule, and several rules are conjunctions. DS-091 is the case that exposed it:

> Per slide: one headline ≤ 6 words plus ≤ 3 supporting fragments.

Three clauses. [T-053](T-053-enforce-the-headline-ds-091-requires.md) closed the first and the
second is long-standing; **the third cannot be reached and the account still counts DS-091 as
`checked`**, because one satisfied row is enough to move a rule into that bucket. The excusal for
the fragment clause is a comment in `audit.py` — the one place `check.py`'s own rule says an excusal
must not live, since `DEFERRED` is keyed by rule and cannot express *clause 3 of DS-091*.

**This is L-43's shape one level down.** T-037 recorded which *rules* no check can reach; the same
argument applies to clauses, and the device that guarantees rule-level coverage is what stops the
clause-level question being asked. `render_verdicts`' docstring already sanctions partial checks —
*"a row deciding one clause of its rule is a partial check and belongs here"* — so the design admits
them and nothing counts them.

**How many there are is not known, and finding out is most of the task.** DS-091 is one. DS-092
(*sentence under 20 words · paragraph 3–4 sentences · table cell one line*) is a likely second — the
cell clause is not measured. DS-100 and DS-105 are candidates.

**Scope**
- In: a sweep for `hard` rules whose text is a conjunction, and which clauses each gate decides.
- In: somewhere for a clause-level excusal to live, that `check.py` can report and a self-test can
  hold to the same standard as `DEFERRED` — a reason, and what would close it.
- Out: building the missing checks. This task makes the hole visible; closing each is its own work.
- Out: rewriting rules into one clause each. Splitting DS-091 into three IDs is a ruleset change
  with a renumbering cost, and it is the owner's call, not a consequence of this task.

**Inputs**
- [`tools/deck/check.py`](../tools/deck/check.py) — `DEFERRED`, `account()`
- [`tools/deck/audit.py`](../tools/deck/audit.py) — the DS-091 rows and their excusal comment
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §3.3
- [`docs/LESSONS.md`](../docs/LESSONS.md) — **L-43**, **L-36**
- [T-037](T-037-record-in-the-ruleset-which-rules-no-check-can-reach.md) — the same move at rule level

**Acceptance criteria**
- [ ] Every `hard` rule with more than one checkable clause is listed, with which clauses are decided
- [ ] A clause no check reaches is excused where `check.py` reports it, not only in a code comment
- [ ] The run says how many rules are partly decided, so the number cannot sit at zero unnoticed
- [ ] The reference deck's account still partitions

**Open questions**
- none yet — the sweep decides the shape.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Sweep all 120 `hard` rules for statements that are conjunctions of separately checkable clauses | the candidate list |
| 2 | For each candidate, read the rows the gate actually emits and decide which clause each one settles | the clause census |
| 3 | A `CLAUSES` table in `check.py`, sharing `DEFERRED`'s entry shape so one validator serves both | `check.py` |
| 4 | `clause_account()`, reported on every run including at zero, and never touching the rule-level partition | `check.py` |
| 5 | Self-test: the live table is sound, and each way of writing a bad entry is watched failing | `check.py` |

**Three decisions the plan takes.**

- **A clause excusal is written in `DEFERRED`'s exact shape** — `(why, (kind, subject))` — so
  `closing_faults` validates it unchanged. A second validator for the same obligation is the drift
  **L-08** describes, and this table exists because one record was keyed too coarsely already.
- **`account()` is not touched, and the partition is the reason.** Rule-level coverage answers *did
  any check decide this rule*, which stays true of a partly-decided rule. Folding clauses into it
  would either break the partition or redefine `checked` for every published figure that quotes it.
- **A second sentence restating the first is rationale, not a clause.** DS-081's *under 6 is a memo*
  restates the rule; counting it would inflate the account instead of sharpening it. This is the
  judgement step 1 cannot make mechanically, and it is why step 2 reads rows rather than trusting
  the sweep.

## 3. Implement

**Decisions & assumptions**
- **The sweep needed a second instrument, and that is not a footnote** — 2026-08-18. The first pass
  read each rule's leading bold run and found 7 conjunctions. It missed DS-092 and DS-100, whose
  clauses are written as separate sentences rather than with the middot the other rules use —
  **the two the task itself had named as candidates.** A statement-shape sweep measures the shape
  the ruleset happens to use, so the list below comes from reading all 120 `hard` rules with the
  emitted rows beside them.
- **The clause table shares `DEFERRED`'s entry shape** — 2026-08-18, so `closing_faults` validates
  both and the standard cannot diverge.
- **`account()` is untouched** — 2026-08-18. 114 owned, 84 checked, buckets sum to 114, exactly as
  before; every published coverage figure is unaffected.
- **The missing checks are not built here** — 2026-08-18, which is §1's scope. Each excusal names
  what would close it, and two of the six are `work` with the measurement already named.

**Outputs produced**
- [`tools/deck/check.py`](../tools/deck/check.py) — `CLAUSES`, `clause_account()`, the clause
  section of the printed account, clause faults folded into `coverage_faults`, and 6 self-test
  fixtures.

**The census — 5 rules, 14 clauses, 6 of them unreached.** All 120 `hard` rules were read; these are
the ones whose statement is a conjunction of separately checkable clauses.

| Rule | Clauses | Decided | Unreached |
| :--- | :---: | :---: | :--- |
| DS-020 | 2 | 2 | — |
| DS-034 | 3 | 1 | *display ~67 du*, *subhead ~34 du* — `ds034_body_type` resolves `--fs-body` and `--lh-body` and nothing else |
| DS-091 | 3 | 2 | *at most three supporting fragments* — the clause T-053 could not close and had nowhere to record |
| DS-092 | 3 | 2 | *table cell one line* — a rendered fact the static half cannot see and the rendered half does not measure |
| DS-100 | 3 | 1 | *active voice*, *one dash per paragraph* |

**DS-100 is the sharpest instance and the task did not predict it.** §1 listed DS-091 as the case and
DS-092, DS-100 and DS-105 as candidates. DS-100 turns out to decide **one clause of three** —
`ds100_no_rhetorical_questions` is its only check — and the account has been reporting it `checked`
throughout. DS-105 was examined and is not a conjunction of checkable clauses in the sense this table
means; it is not listed, which is the judgement step 2 exists to make.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :--- | :--- |
| Every `hard` rule with more than one checkable clause is listed, with which clauses are decided | met | 5 rules, 14 clauses, in `CLAUSES`. Swept across all 120 `hard` rules, with the emitted rows read beside each — the statement-shape pass alone missed two of them |
| A clause no check reaches is excused where `check.py` reports it, not only in a code comment | met | All 6 are entries in `CLAUSES` with a reason and a closing condition, validated by `closing_faults` — the same validator the rule-level excusals use. DS-091's excusal has moved out of `audit.py`'s comment |
| The run says how many rules are partly decided, so the number cannot sit at zero unnoticed | met | Four lines printed on every run, at zero or not: clauses declared, decided, UNREACHED, partly decided. Currently `6` and `DS-034 DS-091 DS-092 DS-100` |
| The reference deck's account still partitions | met | `owned 114, checked 84, buckets sum to 114 = owned, so the account is a partition`. Unchanged, because `account()` was not touched |

**Child fix tasks raised**
- none, and that is §1's scope: *building the missing checks* is explicitly out, and each of the six
  carries the condition that would close it. Two are `work` with the measurement already named —
  resolving `--fs-display`, and counting em dashes per paragraph — and are the cheapest places to
  start.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-10 | (specify) | **Estimated `medium`/`l`, and moved to `PH3`.** `medium` because the account it corrects is sharper rather than missing — no rule is unreported today, only under-reported; `l` because a clause-level record changes the shape of `DEFERRED`, which is keyed by rule ID, and every producer that writes into it. `PH3` under the release split set by the owner 2026-08-10, on size. |
| 2026-08-09 | → proposed | Raised by [T-053](T-053-enforce-the-headline-ds-091-requires.md), which could close two of DS-091's three clauses and had nowhere to record the third except a comment. Deliberately not absorbed there: DS-091 is one instance and the question is general, which is the mistake the same file made three times before [T-051](T-051-a-check-with-no-subject-must-not-report-a-pass.md). |
| 2026-08-18 | proposed → specified | §1's instance re-derived rather than trusted: `account()` buckets by rule id, `decided` is any row with `ok is not None`, so one satisfied row carries a conjunction into `checked` — DS-091 emits two rows and the fragment clause has none. Scope and the four criteria stand. |
| 2026-08-18 | specified → planned | §2 was empty and is now five steps. The shape was settled by reading `DEFERRED`: a clause excusal takes its exact `(why, (kind, subject))` form so `closing_faults` validates both, and `account()` is left alone so the partition and every published coverage figure survive. |
| 2026-08-18 | planned → in_progress → done | The sweep needed a second instrument and that is the finding worth keeping: reading each rule's leading bold run found 7 conjunctions and missed DS-092 and DS-100, the two §1 had itself named. Reading all 120 with the emitted rows beside them gives 5 rules and 14 clauses, **6 unreached**. **DS-100 decides one clause of three** and has been reported `checked` throughout, which §1 did not predict. `account()` untouched — 114 owned, 84 checked, buckets sum to 114. |
