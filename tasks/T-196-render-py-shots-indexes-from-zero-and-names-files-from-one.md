---
id: T-196
title: render.py shots indexes slides from zero and names its files from one
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: []
work_package: PH3
owner: the project owner
business_value: low
effort: xs
created: 2026-08-20
updated: 2026-08-20
deliverables: []
---

# T-196 - render.py shots indexes slides from zero and names its files from one

## 1. Specify

**Outcome**
`render.py shots <deck> 12` produces the picture of slide 12.

**The defect, reproduced 2026-08-20**

    python tools/deck/render.py shots <deck> 1,12,14
    ->  slide-02.png  slide-13.png  slide-15.png

The argument is a zero-based index and the filename is a one-based number. The usage line shows
`0,4,6` so the base is documented by example, but a caller who reads the filenames back - which is
the whole point of the command - is reading a different numbering from the one they typed.

**Scope**
- In: one base for both, chosen and stated. My recommendation is one-based on the argument, because
  the filename, the ruler, the eyebrow and every conversation about a deck already count from one,
  and the argument is the only thing that does not.
- In: the migration cost. Any caller passing indices today changes, so the decision needs stating
  even though the fix is small.

**Acceptance criteria**
- [ ] `shots <deck> 12` writes `slide-12.png` and it is slide 12.
- [ ] Every call site and every document using the old base is updated in the same commit.

**Open questions**
- One-based argument, or keep zero-based and rename the file? Renaming the file is worse: it breaks
  the sort order a human reads and every existing reference to a shot by name.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision - rationale - date>

**Outputs produced**
- <path>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-20 | -> proposed | Created. |
