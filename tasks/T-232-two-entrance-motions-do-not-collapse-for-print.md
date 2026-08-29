---
id: T-232
title: Collapse every content entrance motion for print, not one selector at a time
type: fix
status: done
phase: review
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
- [x] both decks **printed and looked at**, per `CLAUDE.md` rule 6, with the marks present
- [x] an entrance motion added outside the print block's list is caught by something, or the record says plainly that it is not and why
- [x] `printgeom.py` PRINT-2 and PRINT-3 still pass

**Open questions**
- None yet. The register's `Remedy` column carries a hypothesis for each finding, and the method's
  section 5 says it is a hypothesis: whoever implements this measures before committing to it, and
  records what the measurement said.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Add the two declarations beside `.rise` in `@media print` — the half the register measured | `shell/components.css` |
| 2 | **Decide the wider half by measuring it**, not by adopting it. The register's shape — *make the three collapse sites one list* — is a hypothesis | the measurement |
| 3 | Build whatever step 2 leaves standing, and prove it in both directions on a shipped deck | `tools/deck/component.py` |
| 4 | Account for what the gate now decides and what it still does not | `tools/deck/check.py`, `tools/deck/audit.py` |
| 5 | Queue the looks, which a session may not take (`REMEDIATION-ORDER.md` §4) | `docs/OWED-LOOKS.md` |

## 3. Implement

**Decisions & assumptions**

- **The wider half is a check, not one list — 2026-08-29.** *Make the three collapse sites one
  list* was measurable and was measured first. `uncollapsed_motions`' first form compared the
  motion control, reduced motion and print, on the theory that the three lists are the same list.
  On `measure-first.html` it reported **nine** selectors of which **two** were real: print hides the
  whole chrome, so it owes no collapse for the ruler or the pager, and a looping dash whose first
  frame is an ordinary dashed line prints correctly without one. **The theory was wrong rather than
  the code** (**L-142**), and a 7-to-2 false-alarm rate is a check nobody keeps
  ([`bind-on-structure-not-vocabulary`](../docs/LESSONS.md)).
- **So it binds on the hazard, which is DS-224's own sentence.** A motion whose *first painted
  frame* is empty — `opacity:0` or a zero scale, held there by `fill:both` in a medium that never
  advances an animation — and which `@media print` does not switch off. Derived from the deck's own
  `@keyframes`, so a motion added later carries its obligation without anyone editing the checker.
  Re-measured: **3 findings on the tracked deck, 0 after the fix.**
- **A third instance, found on the check's first run — 2026-08-29.** `.opening` is on a sources box
  while its open animation plays, `@keyframes open` starts at `opacity:0`, and the print block sets
  `.slide .sources-box{display:block!important}`. So a box the reader had opened printed as an
  empty space where the deck's sources should be. **`PR-80`'s own analysis says `.opening` is
  unaffected because *print hides the panels*, and that is wrong** — it hides the tier-two
  disclosure panels, not the sources box. Fixed with the other two and recorded on the row.
- **`DS-224` stops being only a look.** Its excusal in `check.py` is closed on DS-143's precedent
  and kept as a comment; the mechanical half is a verdict, declared in `ABSENCE_IS_A_PASS` as a
  prohibition. **The paper half is untouched and still a person** — a slide the reader never
  advanced to, and whether what printed reads as a page, which is `CLAUDE.md` rule 6 rather than an
  excusal.

**Outputs produced**
- [`shell/components.css`](../shell/components.css) — three declarations in the `@media print` block
- [`tools/deck/component.py`](../tools/deck/component.py) — `collapses`, `opening_state`,
  `uncollapsed_motions`, `at_rule_body`, and the `DS-224` verdict
- [`tools/deck/check.py`](../tools/deck/check.py) — `DS-224`'s excusal closed
- [`tools/deck/audit.py`](../tools/deck/audit.py) — `DS-224` in `ABSENCE_IS_A_PASS`
- [`docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md) — rows 2 and 3
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) — `PR-80` closed

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Both decks **printed and looked at**, with the marks present | **owed** | A session may not look ([`REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) §4), and here it could not anyway: the fix is in `shell/components.css` while the tracked decks still carry the old shell, so printing one today would show the defect. Queued as rows 2 and 3 of [`OWED-LOOKS.md`](../docs/OWED-LOOKS.md), **owed after B12 rebuilds the decks** |
| An entrance motion added outside the print block's list is caught by something, or the record says why not | pass | Caught. `component.uncollapsed_motions`, reported as a `DS-224` verdict. Proved both ways on a shipped deck: **3 findings before the fix, 0 after** |
| `printgeom.py` PRINT-2 and PRINT-3 still pass | pass | On the synced deck: `PRINT-2 printed contents cards: 14 over 1 sheet, no two intersect` pass; `PRINT-3 footnote clearance: every card ends above it` pass |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → done | Landed in **B9**, closing `PR-80`. The measured half is three declarations in the print block. **The wider half was refused in the shape the register proposed** - *make the three collapse sites one list* reported nine selectors of which two were real - and rebuilt to bind on the hazard DS-224 names, which reports three and then none. It found a third instance on its first run, `.opening`, which `PR-80` had reasoned was unaffected. `DS-224`'s excusal is closed; the paper half is two rows in [`../docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md), owed after B12. |
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`High`**: the method's section 4 gives that level one obligation beyond a child task — *the release does not go out while it is open*. |
