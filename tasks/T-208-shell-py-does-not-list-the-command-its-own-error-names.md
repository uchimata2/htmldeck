---
id: T-208
title: shell.py does not list the preflight command its own error message tells you to run
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-203]
work_package: PH1
owner: the project owner
business_value: low
effort: xs
created: 2026-08-21
updated: 2026-08-21
shipped_in: unreleased
deliverables: [tools/deck/shell.py]
---

# T-208 — shell.py does not list the preflight command its own error message tells you to run

## 1. Specify

**Outcome**
`python tools/deck/shell.py` with no arguments lists `preflight` among its commands. It does not
today, and it is the command the tool's own failure message tells the reader to run.

**How it was found**
Rebuilding the portfolio-review deck on 2026-08-21 under
[T-203](T-203-four-chart-defects-the-decks-look-missed.md). The generator printed a third step of
`preflight.py <deck> --write`, which exited with `unknown command`. Finding the working command took
three tool reads: `preflight.py`'s docstring says emission lives in `shell.py`; `shell.py`'s usage
block lists `new`, `icons`, `sync`, `tokens`, `check` and `parts` and **not** `preflight`; and
`shell.py`'s own DS-009 failure message reads *"run `shell.py preflight`"* — a command that exists,
works, and is listed nowhere. The generator's stale line was corrected under T-203, since that chain
had to run; this half is the tool's own and is left here.

**Why it is worth a record at this size.** The command is undiscoverable by the two routes a reader
has — the usage block and the sibling tool's pointer — and discoverable only by reading the source
of the error you are trying to fix. That is a published tool telling the truth in one place and not
the other, which is the same fault class as a stale reference, at a smaller size.

**Scope**
- In: the usage block gains the `preflight` line.
- Out: renaming or moving the command, and anything about `preflight.py`'s own split between
  reading and writing. If that split is wrong it is a bigger question than this record.

**Inputs**
- [`tools/deck/shell.py`](../tools/deck/shell.py) — the module docstring's usage list, and the
  DS-009 message that names the command.
- [`tools/deck/preflight.py`](../tools/deck/preflight.py) — the docstring that points at `shell.py`.

**Acceptance criteria**
- [ ] `python tools/deck/shell.py` with no arguments lists `preflight <deck>` with the others.
- [ ] Every command the tool accepts appears in that list — checked by comparing the list against
      the dispatch, not by reading it.

**Open questions**
- None.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Read the dispatch and compare it to the usage list, rather than adding the one line the report named | the true size of the gap |
| 2 | Add every missing command to the docstring's usage block and to `USAGE` | the list a reader gets with no arguments |
| 3 | Make the comparison a fixture, deriving both sets from this file rather than keeping a third list | a self-test row |
| 4 | Seed each defect the fixture claims to catch and prove it goes red | evidence, not a green run |

## 3. Implement

**Decisions & assumptions**
- **The gap was twice the size of the report, and step 1 is why that was visible.** The dispatch
  accepts eight commands: `parts`, `new`, `icons`, `preflight`, `sync`, `tail`, `tokens`, `check`.
  The docstring listed six. `preflight` was missing, as reported — and so was **`tail`**, which was
  named in **no** usage list, in **no** `USAGE` entry, and only inside its own argument error at
  [`tools/deck/shell.py`](../tools/deck/shell.py) `:1254`. Nobody had reported it. Adding the one
  line the task asked for would have left it exactly as undiscoverable as `preflight` was. —
  2026-08-21
- **The fixture derives both sets from this file rather than holding a third list**, which is
  **L-08**: `dispatched` is read from the `if cmd == "..."` branches and `listed` from the
  docstring's own `shell.py <cmd>` lines. A command added tomorrow fails the self-test rather than a
  reader's terminal. A hand-kept list of expected commands would have been the same defect one
  level up. — 2026-08-21
- **Three assertions, not one.** A dispatched command missing from the list is the reported fault;
  a dispatched command with no `--help` entry is the same fault on the other route a reader has;
  and a *listed* command the tool will not run is the mirror defect, which the first two cannot
  see. — 2026-08-21
- **`preflight` also gained a description line**, which the six other entries had and it did not.
  Outside the letter of the scope and inside its reason: the task is about a command a reader
  cannot find, and a bare `usage:` line with no sentence is the same problem one step later. —
  2026-08-21

**Outputs produced**
- [`tools/deck/shell.py`](../tools/deck/shell.py) — the docstring usage block gains `preflight` and
  `tail`; `USAGE` gains `tail` and a description for `preflight`; `self_test` gains three fixtures.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| `python tools/deck/shell.py` with no arguments lists `preflight <deck>` with the others | **met** | Confirmed by running it: the block now prints nine lines, with `preflight` fourth and `tail` seventh. Exit code is unchanged at 2. |
| Every command the tool accepts appears in that list, checked against the dispatch rather than by reading | **met** | Three fixtures in `self_test`, both sets derived from the file. **69 of 69 fixtures pass.** |
| *(evidence, not a criterion)* | — | Each of the four defects the fixtures claim to catch was **seeded and proved red**: `preflight` dropped from the list, `tail` dropped from the list, `tail` dropped from `USAGE`, and a listed command the tool will not run. Each failed the right assertion and named the right command; the file was restored and verified byte-identical. |
| *(closing checklist step 3)* | **n/a** | This task produced nothing that renders. The output is a terminal usage block, and it was read in a terminal. |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-21 | → proposed | Raised from T-203's rebuild, where the printed chain's third step failed and the working command turned out to be named only inside an error message. The generator's stale line was fixed under T-203; this is the tool's own usage block. |
| 2026-08-21 | proposed → done | Fixed, and **the gap was twice the size of the report**. The dispatch accepts eight commands and the usage list named six: `preflight` as reported, and `tail`, which was named in no list, no `USAGE` entry, and only inside its own argument error. Deriving the list from the dispatch is what found it — adding the one reported line would have left it as undiscoverable as `preflight` was. Three fixtures now derive both sets from the file itself (**L-08**), and all four defects they claim to catch were seeded and proved red. 69 of 69 fixtures pass. L-08 gains the instance, because the rule already existed and what was new is the measurement of what a stored copy hides. |
