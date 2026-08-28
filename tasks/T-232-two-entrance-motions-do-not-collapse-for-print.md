---
id: T-232
title: Collapse every content entrance motion for print, not one selector at a time
type: fix
status: proposed
phase: specify
parent: T-219
blocked_by: []
related: []
work_package: PH1
owner: the project owner
business_value: critical
effort: s
created: 2026-08-29
updated: 2026-08-29
deliverables: []
---

# T-232 — Collapse every content entrance motion for print, not one selector at a time

## 1. Specify

**Outcome**
What prints is what a reader sees. Today `.dot-pop circle` and `.arrow-pop marker path` animate from a zero scale with `animation-fill-mode:both`, and a print rendering never advances an animation - so the FROM keyframe is painted and **the marks are not on the paper**. Measured: `measure-first.html` slide 6 prints its six-dimension scale with all 30 dots gone, under a caption that describes them.

**Closes** `PR-80` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: the two declarations beside `.rise` in `@media print`, which the register states as measured rather than hypothesised
- In: **the wider half, which is a hypothesis**: the print block collapses entrance motion one selector at a time, and that shape is what let two of three be missed here and once before
- Out: the motion control and reduced motion, which already collapse all three

**Inputs**
- `PR-80` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3
- [`shell/components.css`](../shell/components.css) - the `@media print` block and its note
- `CLAUDE.md`'s verifying section - one thing here reads the paper, and it reads two numbers

**Acceptance criteria**
- [ ] both decks **printed and looked at**, per `CLAUDE.md` rule 6, with the marks present
- [ ] an entrance motion added outside the print block's list is caught by something, or the record says plainly that it is not and why
- [ ] `printgeom.py` PRINT-2 and PRINT-3 still pass

**Open questions**
- None yet. The register's `Remedy` column carries a hypothesis for each finding, and the method's
  section 5 says it is a hypothesis: whoever implements this measures before committing to it, and
  records what the measurement said.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <the files this task changed>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- <T-NNN or "none">

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`High`**: the method's section 4 gives that level one obligation beyond a child task — *the release does not go out while it is open*. |
