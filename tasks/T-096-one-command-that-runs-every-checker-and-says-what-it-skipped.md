---
id: T-096
title: One command that runs every checker under tools/ and reports what it skipped, with a reason
type: deliverable
status: done
phase: review
parent: null
blocked_by: []
related: [T-078, T-083, T-084, T-095]
work_package: PH3
owner: maintainer
business_value: high
effort: m
created: 2026-08-11
updated: 2026-08-13
shipped_in: unreleased
deliverables: [tools/check_all.py]
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

**Open questions** — *both settled 2026-08-13, as recommended; see §3.*
- ~~Does it live at `tools/check_all.py`, or as a mode of an existing tool?~~ **Its own file**: it
  composes tools from six directories and belongs to none of them.
- ~~Does a green run of this command replace step 1 of the release sequence, or sit inside it?~~
  **It replaces step 1 outright** — a step whose evidence is sixteen exit codes read by a person is
  the thing being fixed.

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
- **Its own file, `tools/check_all.py`** — it composes tools from six directories under `tools/` and
  belongs to none of them — 2026-08-13.
- **It replaces step 1 of the release sequence outright**, rather than sitting inside it. A step
  whose evidence is sixteen exit codes read by a person is the thing being fixed — 2026-08-13.
- **The discovery rule is `git ls-files`, not a directory walk.** `control/`, `dist/` and `.kb/` are
  machine-local by design, and a checker discovered in one of them is a checker no adopter has. Same
  rule `refcheck.py` reaches through `.gitignore` and `taskmd check` adopted in 0.3.0: only what a
  clone receives — 2026-08-13.
- **The manifest is four tables inside the tool, checked against the filesystem in both
  directions** — a tracked tool no table names is `UNCLASSIFIED`, an entry naming a file that is gone
  is `STALE`, and both fail. That is what stops it being a list: `figures.py`'s rule for an exclusion
  whose subject has left the page, applied to checkers (**L-08**, **L-13**) — 2026-08-13.
- **It does not stop at the first failure**, which is the opposite of `tools/tasks/lint.py` and is
  stated in both files. A release run needs every verdict, or the next run finds the second defect
  after fixing the first — 2026-08-13.
- **Child output is captured and printed only for a failure**, with `--verbose` to restore the
  inherited stream. Sixteen accounts is thousands of lines, and a wall of green is where the three
  red checks of 2026-08-10 hid — 2026-08-13.

**Two deviations from the sixteen, both additions rather than changes**

1. **Three sibling variant suites are now gates.** `deliverable_variants.py`, `contract_variants.py`
   and `content_variants.py` were never in the list while `static_variants.py`, their fourth sibling
   and the one with the same purpose, was. All three are green, and were run standalone to confirm
   it before wiring. The partition forced the question; nothing else had.
2. **The per-deck `check.py` line now passes `--print-pages`.** `PRINT-1`, the printed page count,
   was reached by nothing: `check.py` evaluates it only under that flag and the list never passed it,
   and `printpages.py`'s own entry point is red on a correct deck. Both shipped decks pass with the
   flag. The defect behind the red is
   [T-120](T-120-printpages-standalone-defaults-the-slide-count-to-a-hardcoded-twelve.md).

Neither changes a verdict the sixteen produced; both add one the sixteen never asked for.

**Outputs produced**
- [`tools/check_all.py`](../tools/check_all.py) — the command, its manifest and its self-test.
- [`docs/PUBLISHING.md`](../docs/PUBLISHING.md) §8 — step 1 is the command, the enumeration is gone,
  and the excusal is struck through with what closed it.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every checker under `tools/` ends the run in exactly one of ran / skipped-with-a-reason / failed | met | `35 tools(s)`, partitioned `10` gate + `5` per-deck gate + `20` not run, `0` unclassified, `0` stale. The commands partition too: `19 ran`, `1 skipped`, `0 FAILED`, `total 20`. Both totals are printed as `= so the account is a partition` and both are arithmetic on the run, not a claim |
| A checker in none of the three **fails the run**, demonstrated by adding one and not wiring it | met | `tools/deck/unwired_check.py` added and `git add -N`'d, nothing wired. Full run: `0 failure(s), 1 unclassified, 0 stale`, **exit 1**, and `This is step 1 of docs/PUBLISHING.md section 8, and it is red.` Every checker was still green — the red came from the partition alone, which is the point. `--list` fails on it too, in a second rather than six minutes, because `--list` is what someone runs after adding a tool |
| Every deck the repository ships gets the per-deck set, discovered rather than named | met | Decks come from `git ls-files -- '*.html'`, not a list. All four tracked `.html` are classified: two decks, and `reference-deck-seeded-defects.html` and `shell/shell.html` declared as not-decks with what each is. An undeclared `.html` refuses the run before any checker starts |
| A wrong or missing `--sources` is refused, not run against a guess | met | Declared per deck in `DECKS`; a deck absent from both tables returns exit 2 with what to add and why guessing is worse than stopping. The self-test asserts the reference deck's entry exists, so the file cannot ship without one |
| The permanent `spec.py` exception is skipped **with its reason printed**, not silently omitted | met | `skip python tools/deck/spec.py <examples/reference-deck.html>` followed by five lines naming T-087's ruling and pointing at `PUBLISHING.md` §8 for the argument. It is the only skip in the run |
| `PUBLISHING.md` §8 points at the command instead of enumerating, and its excusal is struck out | met | Step 1 of the table is `python tools/check_all.py` with its own last line as the evidence; the thirteen-line code block is one line; the excusal is struck through with what closed it and kept visible, because it is the specification this was built to |
| Run against this repository, it reproduces the sixteen verdicts `0.2.1` was cut on | met | All sixteen appear and all sixteen pass — the by-hand baseline was re-run first on 2026-08-13 and was `EXIT 0` sixteen times. Two of the sixteen now carry `--print-pages` in addition, and three commands are new. **No verdict changed; three were added** |

**Child fix tasks raised**
- [T-120](T-120-printpages-standalone-defaults-the-slide-count-to-a-hardcoded-twelve.md) —
  `printpages.py`'s own entry point defaults the slide count to a hardcoded 12 and fails a deck that
  prints correctly. `PH1`, so it joins `0.2.3`.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-13 | → done | `tools/check_all.py`, and `PUBLISHING.md` §8 step 1 is now that command. Every criterion met. **The run that mattered was the first one**: it found three variant suites nobody had wired — `deliverable_variants.py`, `contract_variants.py`, `content_variants.py`, siblings of the `static_variants.py` that was in the list — all three green, and `PRINT-1` reached by no command at all, with the checker behind it red on a correct deck (**T-120**, raised `PH1`). That is the argument for the whole task, made by the thing itself on its first use rather than by anyone's prediction. |
| 2026-08-13 | proposed → planned | Both open questions settled as recommended: its own file, and it replaces step 1 outright. The design question the specification did not ask turned out to be the load-bearing one — what stops a manifest being the list it replaces — and the answer is `figures.py`'s: check it against the filesystem in **both** directions, so an unwired tool and a deleted one both go red (**L-08**). |
| 2026-08-11 | → proposed | Raised from the closed-record sweep after `0.2.1`, which was cut by running the sixteen commands by hand. The specification is [`PUBLISHING.md`](../docs/PUBLISHING.md) §8's own excusal, written 2026-08-10 and unclaimed since; this task is that paragraph with a number. `high` because the list has already missed three red checks once, and `m` rather than `s` because discovering the decks and their unguessable arguments is most of the work. `PH3` by [`../CLAUDE.md`](../CLAUDE.md)'s rule. |
