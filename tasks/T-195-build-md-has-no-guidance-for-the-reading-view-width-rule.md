---
id: T-195
title: build.md gives no guidance for the reading-view width rule, which is the rule wide tables fail
type: deliverable
status: done
phase: review
parent: null
blocked_by: []
related: []
work_package: PH3
shipped_in: unreleased
owner: the project owner
business_value: medium
effort: xs
created: 2026-08-20
updated: 2026-08-20
deliverables: []
---

# T-195 - build.md gives no guidance for the reading-view width rule, which is the rule wide tables fail

## 1. Specify

**Outcome**
An author who puts a wide table on a slide finds out, before the gate does, what satisfies DS-075.

**The gap, measured 2026-08-20**

    grep -n "DS-075\|scroll\|overflow" skills/htmldeck/references/build.md

returns nothing. The build guide says nothing at all about overflow, in either direction.

The natural fix an author reaches for is a horizontal scroll container. The DS-075 probe measures
`doc.scrollWidth` at 320 CSS px and counts elements wider than 321, so a container that scrolls its
own content does not necessarily move either number, and the author gets the same failure back with
no indication that the fix was the wrong shape.

**Scope**
- In: a short passage beside `build.md`'s reading-view rules - what DS-075 measures, what satisfies
  it, and what does not.
- In: the wide table specifically, since it is the case that produced the failure.
- Depends on [T-193](T-193-failing-rows-print-a-count-where-the-probe-holds-the-evidence.md): once
  the row names the wide element, the passage can be shorter.

**Acceptance criteria**
- [ ] The passage names at least one fix that is **verified** to move the probe's numbers, on a real
      deck carrying a real wide table.
- [ ] It says which shapes do not work, since that is the half an author cannot derive.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Measure what actually moves the DS-075 numbers | three renders of one deck |
| 2 | Write the passage beside the reading-view rules | `build.md` |

## 3. Implement

**Decisions & assumptions**
- **The scroll container is documented as failing, with its numbers** - it is the fix an author reaches for first and it moves the number that was not failing. Measured on `measure-first` with a six-column table added: untouched 538/4 FAIL, scroll container **320/3 still FAIL**, `display:block` on table, rows and cells 320/0 pass.

**Outputs produced**
- `skills/htmldeck/references/build.md`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The passage names a fix verified to move the probe's numbers | **pass** | the table above is three real runs, not an argument |
| It says which shapes do not work | **pass** | the middle row is the whole point of the passage |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-20 | -> proposed | Created. |
| 2026-08-20 | -> in_progress | Measured before written. |
| 2026-08-20 | -> done | Both criteria met. |
