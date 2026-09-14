---
id: T-313
title: Keep a pager press that starts on the button's edge a click
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-307, T-199]
work_package: PH1
owner: the project owner
business_value: medium
effort: s
created: 2026-09-14
updated: 2026-09-14
deliverables: []
---

# T-313 — Keep a pager press that starts on the button's edge a click

## 1. Specify

**Outcome**
A press anywhere on a pager button pages. Today a press that starts near the button's edge animates
and does not page. The hypothesis is the pinch: `.btn.btn--pager:active` scales the button to
`--pager-pinch` while it is held, so the release lands outside the shrunken box and the browser fires
no click.

**Found by** the owner's look at [`OWED-LOOKS.md`](../docs/OWED-LOOKS.md) row 14, 2026-09-14, on all
four pager buttons.

**Scope**
- In: measure the mechanism, then keep the press a click without removing the pinch
- Out: the pinch's look and its tokens

**Acceptance criteria**
- [ ] measured in Chrome: a point just inside the edge falls outside the pinched button before the
      change and inside it after (**L-125**)
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |

## 3. Implement

**Decisions & assumptions**
- <what was decided>: <why, in one sentence>. <Reversible | Not reversible>. — YYYY-MM-DD

**Outputs produced**
- `deliverables/...`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- <T-NNN or "none">

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-14 | -> proposed | Raised from the owner's look at row 14. `PH1`: the published pager animates a press and does not page. Batched into B28 first by the owner's ruling. |
