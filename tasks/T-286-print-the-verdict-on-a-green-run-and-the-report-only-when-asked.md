---
id: T-286
title: Print the verdict on a green run, and the report only when asked or when it fails
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-285, T-279]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-09-02
updated: 2026-09-02
deliverables: []
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
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <path>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- <T-NNN or "none">

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-02 | → proposed | Asked for by the owner after B17, in the same exchange as `T-285`, from the question *is there anything to save in the scripts' output*. Measured first: a green gate prints about 6,000 tokens between the tools, almost all of it report rather than verdict, and a session pays it again on every later turn. `PH3` per `CLAUDE.md`: this repository's own tooling. To be implemented in a session of its own, by the owner's instruction. |
