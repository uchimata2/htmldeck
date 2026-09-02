---
id: T-293
title: The second context-economy run's three Low findings, in one pass
type: fix
status: proposed
phase: specify
parent: T-287
blocked_by: []
related: [T-286, T-132]
work_package: PH3
owner: the project owner
business_value: low
effort: xs
finding: CE-19
created: 2026-09-02
updated: 2026-09-02
deliverables: []
---

# T-293 — The second context-economy run's three Low findings, in one pass

## 1. Specify

**Outcome**
Three `Low` findings from [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.3 closed in one
pass, each `xs`. The front matter binds `CE-19`; `CE-20` and `CE-21` are batched here because
`findings.py` binds one id per task, and their rows in §6.3 name this task.

- **`CE-19`** — `tools/deck/check.py` prints **29,980 bytes** on a green run by default, up from
  17,391 on 2026-08-13, against **398** under `--quiet`. L-153's rule — quiet when stdout is not a
  terminal, the account on a terminal, everything on a red run — was applied to four document tools
  and not to the tool that prints most. Apply it; the self-test already asserts a red run is never
  swallowed.
- **`CE-20`** — five entries in the memory index duplicate a rule that has a home in `CLAUDE.md` or
  the owner's global preferences: the two publishing rules, the trailer rule, the PowerShell command
  rule, and the incoming-labels rule. About 930 of 9,014 bytes, paid every turn. Prune at the next
  consolidate pass; the test is the *memory with a repository home is spent* entry's own.
- **`CE-21`** — `refcheck.py` and `findings.py --check` print 384 and 62 bytes green inside every
  lint; `T-286` §3 named them. Apply L-153's one line.

**Scope**
- In: the three above. Out: any verdict, any rule.

**Inputs**
- `../docs/CONTEXT-AUDIT.md` §6.3, `../docs/lessons/L-153.md`

**Acceptance criteria**
- [ ] `check.py` on a green deck, piped, prints its one line; at a terminal, the account; red prints everything — self-test asserts all three.
- [ ] The memory index is smaller by the five entries and no fact lost its only home.
- [ ] `lint.py`'s green run, piped, is smaller than 1,976 bytes by the two tools' lines.

**Open questions**
- none

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | `check.py`: `quiet_wanted` as in the four tools | the change, self-test |
| 2 | Memory index: remove the five, read back | the index |
| 3 | `refcheck.py`, `findings.py`: one line green when piped | the change |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- `../tools/deck/check.py`, `../tools/docs/refcheck.py`, `../tools/docs/findings.py`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-02 | → proposed | Raised by `T-287`: the run's Lows, batched as the audit method asks. `PH3`. |
