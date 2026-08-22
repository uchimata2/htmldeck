---
id: T-220
title: Derive the release chronology's task count instead of typing it
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-216, T-096, T-145, T-042]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-22
updated: 2026-08-22
deliverables: []
---

# T-220 — Derive the release chronology's task count instead of typing it

## 1. Specify

**Outcome**
[`docs/RELEASE-HISTORY.md`](../docs/RELEASE-HISTORY.md)'s third column is held to the command that
produces it, by a checker [`tools/check_all.py`](../tools/check_all.py) runs. A row whose count
disagrees fails the run, the way a stale pasted figure does today. The document already names the
command two paragraphs above the table; nothing connects the two, so the column is seventeen numbers
typed by hand and re-derived by nobody.

**Measured 2026-08-22, while cutting `0.6.0`.** The `0.5.0` row read **14** where
`grep -h "^shipped_in:" tasks/*.md | sort | uniq -c` answered **22**, and `0.2.4` read **1** against
**2**. Both had been wrong for days with every gate green and `figures.py` reporting
`0 stale figure(s)`. Eight of `0.5.0`'s shortfall were tasks that carried no `shipped_in` at all and
were back-filled the same day; **the other eight were the row simply never being recounted**, which
is the half no back-fill fixes and the reason for this task.

**Why the existing instrument does not reach it.** [`tools/docs/figures.py`](../tools/docs/figures.py)
watches a **fence holding what a command printed**. This column is a number lifted out of a
command's output and typed into a table cell, which is the same claim in a shape no fence can hold.
The tool already carries a mechanism for exactly this case and it is one row wide — *the declared
accounts*, where `the gate's coverage of the ruleset — 92 of 122` is held to
`python tools/deck/check.py`. One number, one command. What is missing is the plural of it.

**Scope**
- In: a check that re-derives every row's task count from the task records and fails on disagreement.
- In: **a seeded proof in both directions** — a wrong number must fail and the corrected table must
  pass. A check only ever seen green is **L-36**.
- In: the decision of where it lives: extend `figures.py`'s declared accounts to hold a table
  column, or a checker of its own. The first is recommended — the mechanism is already written and
  the second copy of it is the drift this repository keeps finding.
- Out: **the fourth column**, *what it is remembered for*. It is prose and no tool can decide it.
- In: **the date column too**, on the same pass. Settled 2026-08-22 by measurement rather than by argument: all seventeen rows already agree with `%(creatordate:short)`, so binding it cannot fail a row today and the *a person may state it* case has no instance behind it in the whole history. The document names the tag command in the same fence as the count command, so it already treats both columns as derived.
- In: **the comparison is against `%(creatordate:short)` and nothing better.** Not a publication timestamp, not `gh release view`, not a UTC normalisation. The tag set is **mixed** — seventeen tags, some annotated and some lightweight — and `creatordate` means the tag's date for one and the commit's for the other. Binding to the command the document names tests the claim the document makes; binding to anything better tests a claim nobody made, and would move a near-midnight release by a day the first time a timezone differs.
- Out: back-filling the records. Done 2026-08-22, and this task must not need it repeated.
- Out: `figures.py`'s **floor blocks**, where growth above the pasted value is reported rather than
  failed by design. This column is not a floor: a row that disagrees is wrong in either direction.

**Inputs**
- [`docs/RELEASE-HISTORY.md`](../docs/RELEASE-HISTORY.md) — the table, and the recount note beside it
- [`tools/docs/figures.py`](../tools/docs/figures.py) — the declared-accounts mechanism
- [`tools/check_all.py`](../tools/check_all.py) — the partition a new checker must land in
- [`docs/PUBLISHING.md`](../docs/PUBLISHING.md) §8 step 8, which is the step that writes the row

**Acceptance criteria**
- [ ] A row whose count disagrees with the derived count **fails**, proved by seeding one of the two
      2026-08-22 errors back and watching it go red.
- [ ] The corrected table **passes**, and every one of the seventeen rows is compared rather than a
      subset.
- [ ] It runs from `check_all.py` and lands in that command's **ran / skipped / failed** partition,
      so an unwired checker goes red rather than unnoticed.
- [ ] A release that adds a row satisfies it **without editing the checker**.
- [ ] A row whose **date** disagrees with its tag fails, and a row with **no tag at all** fails rather than passing quietly.

**Open questions**
- None. The date column was the one open question and it is answered above. **If the owner wants the column to mean the publication date rather than the tag date, that is an edit to `RELEASE-HISTORY.md`'s stated command, not to this checker** — the check enforces whatever the document says derives it.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Read `figures.py`'s declared-accounts code and decide whether a table column fits it or needs its own checker | The decision, recorded in §3 with what made it |
| 2 | Implement the comparison over every row of the table | The checker |
| 3 | Seed each of the two 2026-08-22 errors back and confirm each goes red | Two red runs, quoted |
| 4 | Wire it into `check_all.py` and confirm the partition still accounts for every tool | `0 failure(s), 0 unclassified, 0 stale` |

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
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-22 | (no status change) | **The one open question is answered and the date column is in scope.** Decided by measuring rather than by weighing the argument: all seventeen rows already agree with `%(creatordate:short)`, so the *a person may state it* case has no instance behind it, and binding the column cannot fail a row today. The condition is that the comparison uses the command the document names and not a better one — the tag set is mixed, annotated and lightweight, and `creatordate` means different things across it. |
| 2026-08-22 | → proposed | **Created from a figure found wrong while cutting `0.6.0`.** Two rows of the chronology disagreed with the command the document itself names, and one of them had been eight short since `0.5.0` shipped. The back-fill that closed half of it is done; this is the half that recurs, because the column is derived by a command and maintained by hand. `PH3` per `CLAUDE.md`: it is this repository's own tooling and not a defect in the published plugin, so it does not reopen `PH1`. |
