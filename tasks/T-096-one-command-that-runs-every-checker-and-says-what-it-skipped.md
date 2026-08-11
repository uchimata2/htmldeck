---
id: T-096
title: One command that runs every checker under tools/ and reports what it skipped, with a reason
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-078, T-083, T-084, T-095]
work_package: PH3
owner: maintainer
business_value: high
effort: m
created: 2026-08-11
updated: 2026-08-12
deliverables: []
---

# T-096 — One command that runs every checker under tools/ and reports what it skipped, with a reason

## 1. Specify

**Outcome**
One command runs every checker in the repository and ends with the partition this project already
applies to rules and to figures: each checker **ran**, **was skipped with a stated reason**, or
**failed**, and a checker in none of those three states fails the run.

**Why this one**
**[`docs/PUBLISHING.md`](../docs/PUBLISHING.md) §8 has already specified it, as its own excusal:**

> **What closes the excusal:** one command that runs every checker under `tools/` and reports which
> it ran and which it skipped **with a reason** — the partition `figures.py` already applies to
> fences and `check.py` to rules. Until that exists, a list kept by hand is what there is, and a
> list kept by hand goes stale silently.

The list is sixteen commands today, five of them per deck against two decks, and one of the five
runs against one deck **permanently** for a reason a reader has to know. It was written down on
2026-08-10 because four releases had each re-derived the sequence from the last one's commits, and
**it had already missed three red checks** the day it was written
([T-083](T-083-the-generated-example-deck-fails-a-hard-rule-and-nothing-recorded-it.md),
[T-084](T-084-the-contents-bound-fixture-counts-a-deck-that-no-longer-exists.md), and a stale shell
on `examples/sort-window/`).

**Writing the list down did not stop it being a list.** `0.2.1` was cut by running those sixteen by
hand on 2026-08-11 and reading sixteen exit codes, which is the failure mode one step slower rather
than one step gone. The argument is the same one §2 of that document makes about the humanizer's
covered set: *a list of filenames goes stale the first time a document is added, and it goes stale
silently.*

**Scope**
- In: discovering the checkers rather than listing them — every `tools/**/*.py` that is a checker.
- In: the per-deck five, run against **every** deck the repository ships, discovered the same way.
- In: the arguments that cannot be guessed. `--sources` is the case that already exists: guessing
  wrong does not error, it reports a content failure that reads exactly like a defect in the deck.
- In: a **stated reason** for anything skipped — `spec.py` against `examples/reference-deck.html` is
  the permanent one, and [`PUBLISHING.md`](../docs/PUBLISHING.md) §8 says why in a paragraph that
  should not have to be re-read to interpret a run.
- Out: replacing `check.py`'s rule account or `figures.py`'s figure account. This is one altitude up:
  a partition over **checkers**, not over rules or figures.
- Out: making the checkers uniform. They print what they found and that is deliberate; this composes
  them, it does not rewrite them.

**Inputs**
- [`docs/PUBLISHING.md`](../docs/PUBLISHING.md) §8 — the list, the arguments that cannot be guessed,
  the permanent exception, and the excusal this closes.
- [`tools/deck/check.py`](../tools/deck/check.py) — `account`, the partition shape to copy.
- [`tools/docs/figures.py`](../tools/docs/figures.py) — the same partition over fences, including
  `volatile`, which is the precedent for *reported rather than failed*.

**Acceptance criteria**
- [ ] Every checker under `tools/` ends the run in exactly one of ran / skipped-with-a-reason / failed
- [ ] A checker in none of the three **fails the run**, demonstrated by adding one and not wiring it
- [ ] Every deck the repository ships gets the per-deck set, discovered rather than named
- [ ] A wrong or missing `--sources` is refused, not run against a guess
- [ ] The permanent `spec.py` exception is skipped **with its reason printed**, not silently omitted
- [ ] `PUBLISHING.md` §8 points at the command instead of enumerating, and its excusal is struck out
- [ ] Run against this repository, it reproduces the sixteen verdicts `0.2.1` was cut on

**Open questions**
- Does it live at `tools/check_all.py`, or as a mode of an existing tool? *Recommend its own file:
  it composes tools from three directories and belongs to none of them.*
- Does a green run of this command replace step 1 of the release sequence, or sit inside it?
  *Recommend it replaces step 1 outright — a step whose evidence is sixteen exit codes read by a
  person is the thing being fixed.*

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Enumerate what a checker is, mechanically, and what a deck is | the discovery rule |
| 2 | The partition and its report, in `check.py`'s shape | `check_all.py` |
| 3 | The unguessable arguments, declared per deck rather than inferred | a small manifest |
| 4 | Break it: add a checker, wire nothing, watch the run go red (**L-04**) | evidence |
| 5 | Reproduce the sixteen verdicts, then repoint `PUBLISHING.md` §8 | evidence + the doc |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <none yet>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-11 | → proposed | Raised from the closed-record sweep after `0.2.1`, which was cut by running the sixteen commands by hand. The specification is [`PUBLISHING.md`](../docs/PUBLISHING.md) §8's own excusal, written 2026-08-10 and unclaimed since; this task is that paragraph with a number. `high` because the list has already missed three red checks once, and `m` rather than `s` because discovering the decks and their unguessable arguments is most of the work. `PH3` by [`../CLAUDE.md`](../CLAUDE.md)'s rule. |
