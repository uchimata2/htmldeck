---
id: T-246
title: Correct what the cycle and figure instruments say they do
type: fix
status: done
phase: review
parent: T-219
blocked_by: []
related: []
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-29
updated: 2026-08-29
deliverables: []
---

# T-246 — Correct what the cycle and figure instruments say they do

## 1. Specify

**Outcome**
Two instruments in `tools/docs/` describe what they do. Today **four documents say the coverage partition reports its verdict before it answers**, including the tool's own docstring, where `main()` prints it last and prints nothing at all on a holding partition; and `figures.py` says adjacency is the whole of the binding where `bind()` pairs a command with the next fence.

**Closes** `PR-65`, `PR-67` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: `main()` and `complaint()` in `tools/docs/cycles.py` plus the three documents restating the claim, and `bind()` in `tools/docs/figures.py` with the docstring beside it
- In: **nothing else** - every finding this task closes is named above, and each statement stays in the register rather than being restated here (the method's umbrella condition 2)
- Out: any finding not in the list above
- Out: committing to a remedy before measuring it. A remedy is a hypothesis (the method's section 5); a fix that the measurement refuses is reported here and its finding stays open

**Inputs**
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3 - the rows for `PR-65`, `PR-67`
- `PR-96`, **withdrawn at cycle 40 as a second raising of `PR-65`** - its one added observation, that a holding partition prints no verdict line at all, is recorded on `PR-65`'s row

**Acceptance criteria**
- [ ] every finding above is **closed with its remedy measured**, or explicitly deferred with the reason recorded on its register row - the method's obligation for `Med`
- [ ] each register row's `Task` cell names this task and its `Status` cell says what happened
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None yet. The register's `Remedy` column carries a hypothesis for each finding, and the method's
  section 5 says it is a hypothesis: whoever implements this measures before committing to it, and
  records what the measurement said.

## 2. Plan

**Both remedies were measured before either was written, and both register rows carry a hypothesis
that the measurement answered.**

`PR-67`'s threshold is **derived rather than chosen.** Every tracked document was walked and the gap
between each command fence's close and the fence bound to it as output was counted:

| Gap, in lines | 2 | 73 | 113 |
| :--- | :---: | :---: | :---: |
| Pairs | **5** | 1 | 1 |

Two is the minimum a closing fence and a blank line allow, and there is **nothing between the five
and the two**. The two far pairs are a command shown in a plain fence in
[`docs/PUBLISHING.md`](../docs/PUBLISHING.md) and a `check.py` account in
[`examples/README.md`](../examples/README.md) — neither is the output of the command it was bound to,
and both were being compared against one.

`PR-65`'s hypothesis was *whether the exit code was ever the real guard*. It is not: nothing consumes
it. [`tools/check_all.py`](../tools/check_all.py) names this tool in its not-run table with the
reason, and every other consumer in the tree is a person or an agent reading the printed output at a
cycle's step 2. So the printed ordering is the whole of the guard, the ordering claim stays, and the
code moves.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Census the command-to-output gap across every tracked document; test whether anything consumes `cycles.py`'s exit code | The table above. **Done** |
| 2 | `bind()` measures adjacency against a derived `GAP`; a pair further apart is `UNDECLARED` | `figures.py` |
| 3 | Test `PR-67`'s own stated tell — remove each *no output is pasted under it* exclusion and re-run | one retires, one does not |
| 4 | `complaint()` prints a line on a holding partition; `verdict()` is extracted and every mode leads with it | `cycles.py` |
| 5 | Guard both, and seed each red before trusting it | two self-tests |
| 6 | Close `PR-65` and `PR-67` on their register rows | `PRE-RELEASE-AUDIT.md` |
| 7 | `python tools/tasks/lint.py`, then `python tools/check_all.py`, run separately | green |

## 3. Implement

**Decisions & assumptions**
- **`GAP = 2`, derived from the census — 2026-08-29.** Not a judgement: the distribution is bimodal
  with nothing in the middle, so any threshold from 2 to 72 gives the same partition and 2 is the one
  the document's own shape justifies.
- **`PR-67`'s tell was measured and holds for exactly one entry — 2026-08-29.** The row predicted
  that under real adjacency at least one *no output is pasted under it* exclusion stops being needed.
  Removing each and re-running: `python tools/deck/check.py examples/sort-window` leaves the run
  green and was deleted; `taskmd check` reddens it and stays. **One of two, which is what the row
  said and not more.**
- **`PR-65`'s hypothesis was refused in the direction that favoured the code move — 2026-08-29.** The
  row offered *if the exit code is what stops the reading, the ordering claim should go rather than
  the code*. Nothing reads the exit code, so the claim stays and the code moved.
- **The default mode leads with the verdict too — 2026-08-29.** Three modes would have been enough to
  fix what a reader meets, but the register's argument for moving code rather than correcting four
  sentences only works if all four documents become true, and one of them describes every mode.
- **A live breach was found by the fixed command on its first run, and fixed in place — 2026-08-29.**
  [`docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) belonged to no cycle at all. It is
  cycle 7's now — *the audit's own record*, beside the register it was derived from.
  [`AUDIT-METHOD.md`](../docs/AUDIT-METHOD.md) §2 is why that is a defect rather than a state to
  tolerate. Cycle 7's recorded figure in §2 is a **dated reading**, not a live claim, and B23
  re-reads every cycle a remedy touched; cycle 7 was already `OVERSIZED` before this and still is,
  on its open-task rule rather than on 18,272 bytes.
- **The structural guard is matched as code rather than as prose — 2026-08-29.** Written as a
  substring search for `return complaint(`, it was tripped by the comment above it explaining the
  fault. `render.py` carries the same lesson beside its own pin guard: a self-test that fails on its
  own documentation teaches the next reader to delete the documentation.

**Outputs produced**
- [`tools/docs/figures.py`](../tools/docs/figures.py) — `GAP`, `bind()`'s adjacency and its
  docstring, one exclusion removed, the adjacency guard
- [`tools/docs/cycles.py`](../tools/docs/cycles.py) — `complaint()`'s green line and docstring,
  `verdict()`, every mode's ordering, `docs/REMEDIATION-ORDER.md` in cycle 7, two guards
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) — `PR-65` and `PR-67` closed

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every finding closed with its remedy **measured**, or deferred with the reason on its row | **met** | Both closed, and both rows carry what their own hypothesis measured to — `PR-65`'s exit code was never the guard, `PR-67`'s tell holds for one exclusion of two |
| Each register row's `Task` cell names this task and its `Status` cell says what happened | **met** | Both struck through in `PR-70`'s form, statement kept, and `findings.py --check` reads *13 linked, 14 task(s), execution order consecutive* |
| Both guards seeded red before being trusted | **met** | Four seeds. *Verdict returned last again* — RED. *Holding partition goes silent* — RED. *`GAP` too wide, the old behaviour* — RED. *`GAP` too narrow, pairs nothing* — RED, caught by the README's own check. Each file restored and verified byte-for-byte by hash |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | **met** | In that order, never concurrently ([`TOOLING.md`](TOOLING.md) §1) |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | proposed → done | **B3.** `bind()` measures adjacency against a `GAP` derived from a census, not chosen; `cycles.py` prints its verdict before its answer in every mode and never prints it as nothing. **Both register rows carried a hypothesis and both were tested**: the exit code was never `PR-65`'s guard, and `PR-67`'s tell retired exactly one exclusion of the two it predicted. **The fixed command found a live breach on its first run** — `docs/REMEDIATION-ORDER.md` was in no cycle — absorbed in place under the order's §4. Four seeded proofs, all red, every file restored by hash. `lint.py` green; `check_all.py` green. |
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`Med`**, grouped: the owner ruled on 2026-08-29 that a severity obliges a disposition before the release rather than a file count, on the precedent that the method already accepts many findings to one task at `Low`. Every finding keeps its id and its statement in the register. |
