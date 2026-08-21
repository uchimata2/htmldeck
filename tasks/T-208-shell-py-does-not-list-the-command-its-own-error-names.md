---
id: T-208
title: shell.py does not list the preflight command its own error message tells you to run
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-203]
work_package: PH1
owner: the project owner
business_value: low
effort: xs
created: 2026-08-21
updated: 2026-08-21
deliverables: []
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

*Not started.*

## 3. Implement

**Decisions & assumptions**
-

**Outputs produced**
-

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :--- | :--- |
|  |  |  |

**Child fix tasks raised**
-

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-21 | → proposed | Raised from T-203's rebuild, where the printed chain's third step failed and the working command turned out to be named only inside an error message. The generator's stale line was fixed under T-203; this is the tool's own usage block. |
