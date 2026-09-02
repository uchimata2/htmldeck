---
id: T-286
title: Print the verdict on a green run, and the report only when asked or when it fails
type: deliverable
status: done
phase: review
parent: null
blocked_by: []
related: [T-285, T-279]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-09-02
updated: 2026-09-02
deliverables: [tools/check_all.py, tools/docs/figures.py, tools/docs/chronology.py, tools/tasks/lint.py, docs/lessons/L-153.md]
---

# T-286 — Print the verdict on a green run, and the report only when asked or when it fails

## 1. Specify

**Outcome**
A passing run of each repository gate prints its partition in one line and nothing else when its
stdout is not a terminal or when `--quiet` is passed — *40 ran, 1 skipped with a reason, 0 failed,
209 s* — and a failing run prints every failure in full, exactly as today. The reference tables, the
timing table and the closing paragraphs print on a terminal or under `--report`. What a run *decides*
does not change by a byte.

**Why it is worth a task.** An agent pays a tool's output once when it reads it and again on every
later turn of the session, so the cost of a report compounds with the number of runs — which is what
the owner named on 2026-09-02 as *exponentially increasing token consumption*. Measured on B17's last
green runs:

| Tool | Bytes | Lines | Tokens, about | What the bytes are |
| :--- | ---: | ---: | ---: | :--- |
| `tools/check_all.py` | 18,480 | 244 | 4,600 | forty `pass` lines each carrying its whole command, the per-command timing table, a four-line closing paragraph |
| `tools/docs/figures.py` | 3,043 | 59 | 760 | eight reference tables and a three-line closing paragraph; the verdict is one line |
| `tools/tasks/lint.py` | 2,222 | 34 | 555 | four headings, one long counts line, and taskmd's six standing advisories |
| `tools/docs/chronology.py` | 611 | 10 | 150 | the partition and a two-line closing paragraph |

A three-task batch runs the first four times and the second about eight, so a session that reads them
unfiltered carries some 25,000 tokens of green reports forward — filtering with `grep`, as B17 did,
is discipline rather than design.

**Scope**
- In: `check_all.py`, `figures.py`, `chronology.py` and `lint.py`'s own lines. The one-line form
  keeps the partition's counts, because **L-05**'s *say which half you checked* is the reason the
  closing paragraphs exist and the counts are that sentence in numbers
- In: the default. Recommended: quiet when stdout is not a terminal, since an agent never has one
  and a flag nobody passes saves nothing; a person at a terminal keeps the report, and a person
  piping to a file adds `--report`
- In: `figures.py --values` unchanged — it is the paste helper, not the report
- In: the self-tests assert that a failing fixture **still prints its failure under `--quiet`**. A
  quiet mode that hides a failure is the one outcome worse than today
- In: `check_all.py` passes the quiet form to the children it runs, or keeps capturing them — whichever
  a measurement shows is what it already does
- Out: taskmd's six advisories printed by `lint.py`'s second step. They are upstream's, expected
  forever, and quieting them is a pull request to the owner's taskmd repository — named here so the
  next session does not re-derive that
- Out: any change to a verdict, to `--verbose`, or to what a red run prints

**Inputs**
- [`../tools/check_all.py`](../tools/check_all.py) — `report()`, and T-279's timing table
- [`../tools/docs/figures.py`](../tools/docs/figures.py) — `report()`, and the epilogue its
  docstring justifies
- [`../tools/docs/chronology.py`](../tools/docs/chronology.py) and
  [`../tools/tasks/lint.py`](../tools/tasks/lint.py)
- [T-285](T-285-let-a-documentation-task-run-the-gates-its-change-can-reach.md) — the other half of
  the same question, and the one that decides how often a run happens at all

**Acceptance criteria**
- [ ] A green `check_all.py` run with stdout not a terminal prints under 300 bytes, and a green
      `figures.py` run under 200, each measured and recorded before and after
- [ ] A seeded failure under `--quiet` prints the failure in full, asserted by each tool's self-test
- [ ] `--report` prints today's output byte for byte on a green run
- [ ] The one-line form carries the partition's counts, not only the word *pass*

**Open questions**
- Whether quiet is the non-terminal default or an explicit flag — the owner. The recommendation is
  the default; the cost if wrong is one `--report` typed by a person who piped a run to a file

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Baseline the four green outputs on the frozen tree, captured to files | 18,480, 3,043, 2,222 and 611 bytes — §1's table, re-measured to the byte |
| 2 | Put the decision in one function per tool and buffer the account so the decision comes **after** the verdict: `finish()` in `check_all.py`, `emit()` in `figures.py` and `chronology.py`, `verdict()` in `lint.py`; the default from `isatty`, `--report` and `--quiet` overriding it, `--values` always printing | The four tools |
| 3 | Self-test each: a seeded failure under quiet prints in full; a green quiet run is one line under the byte target; the default follows the terminal and the two flags | The four self-tests |
| 4 | Measure after, piped and with `--report`, and diff the `--report` forms against the baselines | §4 |

## 3. Implement

**Decisions & assumptions**
- **Quiet is the non-terminal default** — 2026-09-02. The spec's recommendation, adopted rather
  than asked: an agent never has a terminal and a flag nobody passes saves nothing; a person at a
  terminal keeps the account; a person piping to a file adds `--report`. Reversible by flag on every
  run, and by one function per tool.
- **The account is buffered and the decision is a function, so the red path is today's output to
  the byte and the self-test can assert it without a red history.** `emit(full, code, line, quiet)`
  consults `code` before `quiet`; `check_all.py`'s `finish()` is the same shape over `Result`s and
  is exercised with a fake failing command whose captured output must appear. The live proof came
  unasked: a fixture path in `check_all.py`'s new self-test read as a dead pointer, `lint.py` and
  `figures.py` went red inside a piped `--docs` run, and the run printed 29,036 bytes with both
  failures in full.
- **`quiet_wanted` is written in each of the four files rather than shared** — 2026-09-02. Each
  tool is standalone standard library and runs from anywhere; a shared module would be a path hack
  in four files plus a `NOT_RUN` entry, for eight lines. **L-13** is about an incantation with two
  homes that drift apart; this is a rule each file's self-test asserts, so a drift fails. Reversible.
- **`lint.py` quiets only its own lines** — 2026-09-02. Its four headings and the closing paragraph
  become one line; the children keep writing to the console, because `taskmd check`'s eleven
  advisories are upstream's (the spec's *Out*) and `TOOLING.md` §1 counts them piped to tell a
  twelfth from the set. Measured: **2,222 → 1,969 bytes**. `refcheck.py`'s and `findings.py`'s green
  lines are this repository's and could follow, and are named for `T-287` rather than widened here.
- **`check_all.py` keeps capturing its children** — the spec's either/or, settled by reading
  `run_one`: output was already captured and printed only on failure, so a child's verbosity never
  reached the account. The 18,480 bytes were this file's own.
- **A green docs run closes with a different paragraph**, because *the whole gate set* would be
  false under `--docs`. The two are separate strings in `finish()`.

**Outputs produced**
- [`../tools/check_all.py`](../tools/check_all.py) — `quiet_wanted`, `finish`, the progress lines
  gated by quiet, and the self-test's two assertions
- [`../tools/docs/figures.py`](../tools/docs/figures.py) — `quiet_wanted`, `emit`, `report` over
  `account`, and the one-line form
- [`../tools/docs/chronology.py`](../tools/docs/chronology.py) — the same three
- [`../tools/tasks/lint.py`](../tools/tasks/lint.py) — `quiet_wanted`, `verdict`, `main(argv)`
- [`../docs/lessons/L-153.md`](../docs/lessons/L-153.md) — the rule, generalised past these four
- [`TOOLING.md`](TOOLING.md) §1 — the paragraph a session reads before running a gate

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A green `check_all.py` with stdout not a terminal prints under 300 bytes, a green `figures.py` under 200, measured before and after | pass | `check_all.py` 18,480 → **128** (the `--docs` line, which carries the base; a full run's line is shorter); `figures.py` 3,043 → **130**; `chronology.py` 611 → 93; `lint.py` 2,222 → 1,969, its children untouched by decision |
| A seeded failure under `--quiet` prints the failure in full, asserted by each tool's self-test | pass | `check_all.py`: a fake `failed` `Result` carrying `BOOM: the seeded failure` through `finish(quiet=True)` must print it and return 1; `figures.py` and `chronology.py`: `emit("FULL", 1, …, True)` must be `FULL`; `lint.py`: `verdict(3, "second", True)` must equal its `--report` form and name the step. And the live red above |
| `--report` prints today's output byte for byte on a green run | pass | `chronology.py`: identical to the baseline. `figures.py` and `lint.py`: identical except the counts this session's own document edits moved — `refcheck` 5,048 → 5,057 pointers, and the resulting *floor grew* line — which is the content changing, not the form. `check_all.py`: the closing full run's report against the baseline, same lines in the same order with the seconds differing |
| The one-line form carries the partition's counts, not only the word *pass* | pass | `check_all: 7 ran, 35 skipped with a reason, 0 failed, 0 unclassified, 0 stale  -  44 s  (--docs, against origin/master 746f8a2)`; `figures: 0 stale - 17 fence(s), 11 prose numeral(s), 33 in 5 document(s) pasting no output - 1 floor block(s) grew (see --values)`; `chronology: 17 row(s) agree with both commands, 17 tag(s), 17 version(s) in tasks, 0 FAILING`; `lint: all four passed - index, check, refcheck, findings` |

**Child fix tasks raised**
- none. `refcheck.py`'s and `findings.py`'s green lines are named for `T-287`.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-02 | → proposed | Asked for by the owner after B17, in the same exchange as `T-285`, from the question *is there anything to save in the scripts' output*. Measured first: a green gate prints about 6,000 tokens between the tools, almost all of it report rather than verdict, and a session pays it again on every later turn. `PH3` per `CLAUDE.md`: this repository's own tooling. To be implemented in a session of its own, by the owner's instruction. |
| 2026-09-02 | proposed → done | Quiet is the non-terminal default in all four tools, with `--report` and `--quiet` overriding it. A green `check_all.py` run went from 18,480 bytes to one line of 128; `figures.py` 3,043 → 130; `chronology.py` 611 → 93; `lint.py` 2,222 → 1,969 with its children deliberately untouched. Every red path is today's output and each self-test seeds a failure to prove it; a real one proved it too. **L-153** carries the rule. Landed in one commit with `T-285`, for the reason its §3 gives. Closed on a green `lint.py` and a green full gate. |
