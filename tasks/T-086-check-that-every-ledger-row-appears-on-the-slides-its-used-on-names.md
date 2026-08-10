---
id: T-086
title: Check that every figure ledger row appears on the slides its Used on names
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-082, T-071]
work_package: v0.2
owner: the project owner
business_value: medium
effort: m
created: 2026-08-10
updated: 2026-08-10
deliverables: [tools/deck/spec.py, examples/sort-window/sort-window.foundation.md]
---

# T-086 — Check that every figure ledger row appears on the slides its Used on names

## 1. Specify

**Outcome**
A gate reads a foundation's figure ledger against the built deck and fails a row whose `Used on`
names a slide that does not show the value. The check is exact rather than heuristic, because it
searches for a known string on a known slide instead of deciding what a figure is.

**Why this one**
[T-082](T-082-the-worked-examples-figure-ledger-omits-figures-that-reach-slides.md) §3 decided the
ledger's two directions are not equally checkable, and this is the half that is. Its sweep found
four rows over-claiming — `12.4%` named slides 4 and 9, `2.4%` named 11 and 12, `84%` named 7, `16%`
named 5 — and the deck shows none of them there. SPEC-4 reads `Used on` to decide whether a slide's
`Sources` field is right, so a cell naming a slide the figure never reached mis-calibrates the one
check built on the ledger.

**The other direction stays a judge rule, and T-082 §3 records why.** Completeness needs something
that can enumerate every figure on a slide; `content.py`'s `FIGURE` pattern cannot see `6 rounds`,
`04:10`, `27 of 31` or `31 peak working days`, and widening it to any digit makes every axis tick a
figure. A completeness gate built on that instrument would pass a ledger missing exactly what this
sweep found missing.

**Scope**
- In: a new rule, over `foundation.md` plus the built `.html`, that every `Used on` slide shows the
  row's value.
- In: where it lives. `spec.py` compares two specifications and takes no deck; `content.py` takes a
  deck and sources and builds its own ledger rather than reading the hand-written one. Neither
  signature fits, and picking one over a third tool is the first decision.
- In: how a row that legitimately renders differently is handled — `4.1 / 11.2 / 15.9 / 18.7%` is
  one row and four marks, and `first working week of January` is prose. A rule that cannot express
  those will be switched off rather than fixed.
- Out: ledger completeness, which T-082 §3 decided stays `judge`.
- Out: the reference deck's ledger, until this runs on `sort-window` first.

**Inputs**
- [`tools/deck/spec.py`](../tools/deck/spec.py) — SPEC-4 and the `used_on` parser to reuse.
- [`tools/deck/content.py`](../tools/deck/content.py) — `runs()` and the per-slide split, which
  already solve reading a deck's text per slide.
- [`examples/sort-window/sort-window.foundation.md`](../examples/sort-window/sort-window.foundation.md)
  — 58 rows, complete and corrected, which is the calibration case.

**Acceptance criteria**
- [ ] The rule exists, and names the row and the slide when it fails
- [ ] It is green on `sort-window` as T-082 left it
- [ ] It is red on a seeded defect — a `Used on` cell given a slide that does not show the value —
      and the seed asserts it landed
- [ ] The multi-value and prose row forms are handled, or explicitly excluded with a recorded reason
- [ ] `docs/PUBLISHING.md` §8's gate list names it, if it is a gate a release runs

**Open questions**
- Which tool owns it — a third input to `spec.py`, a second reader in `content.py`, or its own file.
  Decide at `plan`, from which one already reads the deck per slide.

## 2. Plan

**The open question is closed first, because every other step depends on it.** `spec.py` takes the
built deck as an **optional third argument** and gains a fifth verdict, `SPEC-5`. §3 records why the
other two candidates lost.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Settle which tool owns the rule | The decision and its two rejected rivals, in §3 |
| 2 | Read the deck per slide by the number it already declares, reusing `content.runs()` for the text | A slide-number to text map in `spec.py`, and no second copy of the run splitter |
| 3 | Match the whole `Value` cell word-bounded, run it over `sort-window` unfiltered, and print every row it cannot decide | The measurement step 4 is drawn from, rather than a rule guessed at from four examples |
| 4 | From that list, express the multi-value and prose forms or exclude them **by shape**, reporting how many were excluded | `SPEC-5` green on `sort-window` as T-082 left it, with any exclusion visible in the verdict line |
| 5 | Seed the defect — a `Used on` cell given a slide that does not show the value — into `self_test()` | A red run asserted, alongside the four seeds already there |
| 6 | Hold it to the absent-subject bar `audit.py` already applies to this module | `spec.verdicts("", "")` reports `SPEC-5` as `None`, and the fixture stays green |
| 7 | Name the deck argument in the gate list, and correct every document that says `spec.py` has four verdicts | `PUBLISHING.md` §8 runs the rule; no stale count survives |
| 8 | Run the gate list against both shipped decks | The verdict lines, pasted into §4 |

## 3. Implement

**Decisions & assumptions**
- **`spec.py` owns it, as a fifth verdict over an optional third argument** — 2026-08-10. The
  subject of the rule is the foundation's `Used on` column, which is `spec.py`'s column: `rows()`
  and `used_on()` already parse it, and SPEC-4 is the rule the defect mis-calibrates. Two rules over
  one column, in one tool, sharing one parser.
- **`content.py` was the rival the specification pointed at, and it lost on which ledger it holds** —
  2026-08-10. It does already read the deck per slide, which is what §1's open question asked for.
  But the ledger it holds is one it **builds** from the deck and the sources, and it builds its own
  precisely because the authored one cannot be trusted for completeness (**L-62**). Putting a rule
  about the *authored* ledger in the tool that exists to not depend on it would put two ledgers of
  opposite provenance in one file, and the next reader would have to work out which was which.
- **A third file lost on cost, not on fit** — 2026-08-10. It would be a fourth reader of the
  foundation and one more hand-kept line in a gate list that has already gone stale twice
  (`PUBLISHING.md` §8).
- **The deck argument is optional, and that is what makes the choice safe** — 2026-08-10. `spec.py`'s
  own docstring says to run it *before writing any slide*, so a required deck would break the tool's
  stated use. Absent, `SPEC-5` reports `None` — the absent-subject shape every producer in this
  directory is held to, and the one `audit.py`'s fixture already asserts through
  `spec.verdicts("", "")`.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The rule exists, and names the row and the slide when it fails | met | `SPEC-5` in [`spec.py`](../tools/deck/spec.py). Its message is `slide 4 does not show Off-peak miss rate (3.1%)` — row, slide and value, so the cell to correct is named rather than searched for |
| It is green on `sort-window` as T-082 left it | **not met, and the rule is right** | It was red, on one pair of the 89. Slide 4's chart labels its maximum and prints *3.4% or under* beneath it, so 3.1% is nowhere on the slide its `Used on` claimed. The ledger was corrected — a fifth over-claim of the four T-082 found by hand, and the first no sweep caught. Green after |
| It is red on a seeded defect, and the seed asserts it landed | met | Two seeds in `self_test`, because the row fails two ways: a slide showing another value, and a `Used on` naming a slide nobody built. The second was reachable by no other test |
| The multi-value and prose row forms are handled, or explicitly excluded with a recorded reason | met | Handled, none excluded. Three forms, each measured rather than assumed: as written (80 pairs), as one mark of a `/`-separated series (6), and as the leading quantity with the unit noun dropped (2). `canonical()` folds the two spellings the deck actually uses — a number as a word, a month abbreviated |
| `docs/PUBLISHING.md` §8's gate list names it, if it is a gate a release runs | met | The `spec.py` line takes the deck. It also gained the sentence that it is the one per-deck check that runs on `sort-window` alone, the reference deck shipping no specification pair |

**Child fix tasks raised**
- none. The reference deck having no pair to check is
  [T-087](T-087-sweep-the-reference-decks-figure-ledger-for-the-pattern-t-082-found.md)'s open
  question already, and was recorded in `PUBLISHING.md` rather than raised again.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-11 | (no change) | Shipped in **`v0.2.0`**, the release this task and [T-087](T-087-sweep-the-reference-decks-figure-ledger-for-the-pattern-t-082-found.md) close. |
| 2026-08-10 | → done | `SPEC-5` shipped, five acceptance criteria met and one **not met on purpose**: the rule was red on the deck it was calibrated against, because a fifth `Used on` over-claim was there to find. The ledger was corrected rather than the rule relaxed. Calibrated by re-seeding T-082's four hand-found over-claims — all four go red and each names its row and slide. Every gate in `PUBLISHING.md` §8 green, both decks. Carried out as **L-64**: a literal comparison between two documents written by different hands left 19 of 89 pairs undecided, and exactly one of them was the defect. |
| 2026-08-10 | → planned | §2 written, and the open question closed with it: `spec.py`, optional third argument, `SPEC-5`. The specification pointed at `content.py` — *decide from which one already reads the deck per slide* — and that is the candidate the reasoning rejected, on which ledger each tool holds rather than on which one can read a slide. §3 carries all three. |
| 2026-08-10 | → specified | §1 was complete when the task was raised and the owner ratified its one contested question the same day, so the status was the only thing missing. `deliverables:` declared at the same time, per `TASK-WORKFLOW.md` §6.2. |
| 2026-08-10 | (no change) | Owner settled the scope on the day it was raised: **exact direction only**. Widening `content.py`'s figure pattern to gate completeness as well was put and declined, so the `Out:` line above is a decision rather than a proposal and is not to be re-argued at `plan`. |
| 2026-08-10 | → proposed | Raised from [T-082](T-082-the-worked-examples-figure-ledger-omits-figures-that-reach-slides.md) §3, which decided the checkable half of the ledger question and left the implementation here rather than growing a fix to a worked example into a tool change. `m` and not `s`: no existing tool takes both a foundation and a deck, so this adds an input to a signature rather than a rule to a list. `v0.2`, being under the `l` line. |
