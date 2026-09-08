---
id: T-299
title: Triage the Nextep adopter report and decide each of its eighteen findings
type: analysis
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-225]
work_package: PH3
owner: the project owner
business_value: high
effort: m
created: 2026-09-08
updated: 2026-09-08
deliverables: []
---

# T-299 — Triage the Nextep adopter report and decide each of its eighteen findings

## 1. Specify

**Outcome**
Every finding in [`docs/adopter-reports/nextep/`](../docs/adopter-reports/nextep/README.md) has a
decision against it — accepted and raised as a fix, accepted and deferred, or rejected with a
reason. Nothing in the set is left unjudged. This task produces the judgement; the fixes it accepts
become tasks of their own.

**Where it came from**

A second outside project used htmldeck to build its presentation: a thirty-three page argument deck
for a training capstone, built between 2026-09-01 and 2026-09-08 against a date that did not move,
and delivered. Seventeen findings were measured on `0.7.0` and one on `0.6.0`. Each was written the
day it was met, with the command that proves it, and the batch was held back so the project's own
deadline paid nothing for a context switch into this repository.

**The adopting project's repository is private, and the records were written to stand without it.**
Every piece of evidence is quoted inside the record. Paths such as `deck/nextep.html` and
`tools/deck.ps1` are that project's own and resolve nowhere here; nothing links out.

**What is different from [T-225](T-225-triage-the-claimai-adopter-report.md)**

- **Four records are `request` rather than `defect`** — places where the design system has no
  vocabulary for a decision the deck's owner made, not places where a rule misfires. `17` is the
  general case: three owner-ruled deviations leave the gate red on every run, so the adopter wrote a
  forty-line wrapper to hold the ruling. ClaimAI's `011`, `023` and `024` each asked for one escape
  hatch; this one asks for the mechanism.
- **One defect arrives with its downstream consumer attached.** `13` truncates a slide's body at the
  first matching close tag; `14` is `readability.py` inheriting it through `slidefacts.facts` and
  reporting aggregates over two thirds of the copy, with a ledger that promises nothing goes missing
  quietly. Deciding `13` decides most of `14`.
- **Five records say no instrument can see an interaction** — `06`, `08`, `09`, `10`, and `12` from
  the other side. `016` and `017` of the ClaimAI set are the same complaint one release earlier, so
  the triage has a before and an after to compare.

**In scope.** Each of the eighteen: a verdict, and where accepted, a task. Re-deriving each one's
phase and type by this repository's rules rather than by what the filer called it — CLAUDE.md is
explicit that classification is this project's to make, and the report's `severity` is what it cost
the author who hit it.

**Out of scope.** Fixing anything here. Any change to the report's own files: an evidence record is
not edited after it arrives, and a verdict that disagrees with one says so in this task.

**Acceptance.** Eighteen verdicts, each with a reason. Every accepted finding names the task that
carries it. Every rejected one names why, in a sentence somebody who did not sit in this triage can
weigh.

## 2. Plan

1. Read [`docs/adopter-reports/nextep/README.md`](../docs/adopter-reports/nextep/README.md) whole —
   the covering note carries four themes and they cut across the individual records.
2. For each of the eighteen, in the index's order: reproduce or accept the record's own command,
   then rule.
3. Cross-check against the ClaimAI set before ruling on `11`, `16`, `17` and `18` — `011`, `023`,
   `024` and `025` touch the same rules, and `023` was already answered by narrowing `DS-100`, which
   is why `17` is not a re-run of it.
4. Cross-check `01` against what shipped in `0.7.0`: it is the one record measured on `0.6.0`.
5. Raise a task per accepted finding, phase and type re-derived here, and record in section 3 where
   each verdict differs from what arrived and why.

## 3. Implement

<!-- Not run. -->

## 4. Review

<!-- Not run. -->

## Log

- 2026-09-08 — Raised on delivery of the report. The batch arrived as a pull request from the
  adopting project; no verdict has been taken on any record yet.
