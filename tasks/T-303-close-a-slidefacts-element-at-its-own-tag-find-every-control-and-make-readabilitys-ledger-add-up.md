---
id: T-303
title: Close a slidefacts element at its own tag, find every control on a slide, and make readability's ledger add up
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-299, T-258, T-259]
work_package: PH1
owner: the project owner
business_value: high
effort: m
created: 2026-09-13
updated: 2026-09-13
deliverables: []
---

# T-303 — Close a slidefacts element at its own tag, find every control on a slide, and make readability's ledger add up

## 1. Specify

**Outcome**
`slidefacts.py` reads the whole face of a slide, and `readability.py` reads all of the copy it says it
reads. Today `by_class` closes an element at the **first** matching close tag
(`tools/deck/slidefacts.py` `:97`, `section.find("</%s>" ...)`), so a `.body` whose first child is
the same tag stops at that child. `readability.py` takes its lines **and** its counted-out words
through `slidefacts.facts` (`tools/deck/readability.py` `:151` and `:162`), so the dropped words are on
neither side of a ledger that promises nothing goes missing quietly. And `controls()`
(`tools/deck/slidefacts.py` `:119`-`:130`) matches only `data-disc`, so a slide's real `<button>` is
reported as absent.

**From the adopter report** [`10`](../docs/adopter-reports/nextep/2026-09-07-slidefacts-reports-no-control-on-any-slide.md), [`13`](../docs/adopter-reports/nextep/2026-09-08-slidefacts-closes-an-element-at-the-first-matching-close-tag.md), [`14`](../docs/adopter-reports/nextep/2026-09-08-readability-inherits-slidefacts-truncation-so-a-third-of-the-copy-is-unread.md).

**Re-run in triage, 2026-09-13, on this tree.** `by_class` on a nested fixture returned `['FIRST']`
where `['FIRST SECOND THIRD']` was expected, and the unnested control returned both of its words.
`slidefacts.py` on slide 2 of a copy of the reference deck printed the disclosure and omitted the
`sources-btn` button on the same slide.

**Scope**
- In: `by_class` tracks tag depth to the balanced close
- In: `readability.py` asserts that the words read plus the words counted out equal the words the
  slide carries, so a truncation of this kind cannot pass quietly again
- In: `controls()` finds `<button>`, `role="button"`, `role="tab"`, `role="switch"` and `[tabindex]`,
  and prints each control's accessible name
- Out: anything the records above do not name. The report is a closed one-way hand-over, so a
  question this task cannot answer is settled here rather than asked

**Inputs**
- the three records above, each with its command, its version and its own proposed fix
- [T-299](T-299-triage-the-nextep-adopter-report.md) section 3, where the three were ruled together

**Acceptance criteria**
- [ ] records `10`, `13` and `14` are each closed with the remedy measured, or deferred with the reason
      recorded in this task
- [ ] each fix is proved by seeding the defect and watching it fire, in both directions (**L-125**)
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None. Each record carries its evidence and a proposed fix; the proposal is a hypothesis to measure
  before committing to it.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

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
| 2026-09-13 | -> proposed | Raised by T-299 from Nextep records `10`, `13` and `14`, which share `slidefacts.py`. `PH1`: an adopter met all three in the published `0.7.0`. |
