---
id: T-271
title: Decide whether a slide can open a quick view scoped to the section it argues from
type: decision
status: done
phase: review
parent: null
blocked_by: []
related: [T-225]
work_package: PH3
shipped_in: unreleased
owner: the project owner
business_value: low
effort: m
created: 2026-08-29
updated: 2026-09-14
deliverables: [shell/deck.js, shell/components.css, tools/deck/audit.py, docs/COMPONENT-CONTRACT.md]
---

# T-271 — Decide whether a slide can open a quick view scoped to the section it argues from

## 1. Specify

**Outcome**
**Accepted and deferred.** A slide citing one risk row, one finding or one clause makes the reader open the whole source and scroll to find it. The whole-file view is right on the colophon, where a reader is browsing sources, and wrong on an argument slide, where they are checking one claim. The adopter built any per-section panel by hand on the slide that needed it.

**From the adopter report** [`001`](../docs/adopter-reports/claimai/001-per-section-quick-view.md).

**Scope**
- In: the decision, which the record explicitly leaves to this repository: a new component, an anchor into the existing sheet, or a `data-` attribute selecting a range
- In: **deferred rather than rejected**, and the reason is scheduling: it is the only record in the set that asks for a new component, and it competes with nothing else here
- Out: anything the records above do not name. The report is a closed one-way hand-over — there is no
  channel back and none is expected, so a question this task cannot answer is settled here rather
  than asked.

**Inputs**
- the record above, [`001`](../docs/adopter-reports/claimai/001-per-section-quick-view.md) — each carries its evidence, its version and its own proposed fix
- `COMPONENT-CONTRACT.md` section 3 — `.qv-src` as a `template` whose parent is `.sources-item`
- `DS-085`, which names the colophon as the one thing allowed to follow the closing slide

**Acceptance criteria**
- [x] every record named above is **closed with its remedy measured**, or explicitly deferred with the
      reason recorded in this task
- [x] each fix is proved by seeding the defect and watching the check fire, in both directions where
      the record's own evidence is a verdict (**L-125**)
- [x] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None yet. Every record carries its own evidence and its own proposed fix; the proposal is a
  hypothesis and whoever implements it measures before committing to it.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Decide between a component, an anchor and a range | §3 |
| 2 | Open the quick view at the named heading and mark it | `shell/deck.js`, `shell/components.css` |
| 3 | Count an anchor naming no heading as a control that opens nothing, and self-test both directions | `tools/deck/audit.py` |
| 4 | Contract the attribute | `docs/COMPONENT-CONTRACT.md` |
| 5 | Sync, measure on a copy of `sort-window`, record the look, lint, gate | §3 |

## 3. Implement

**Decisions & assumptions**
- Built now rather than deferred: the owner's wave 8 ruling of 2026-09-14 closes every open task
  before 1.0.0, which retires the scheduling reason in §1. Reversible. — 2026-09-14
- An anchor into the existing sheet: `data-qv-at` on `.sources-open` names a heading in the source,
  and the quick view opens scrolled to it and marks it. Reversible. — 2026-09-14
- A new slide-local component is rejected: it copies the fragment into the deck, which is the size
  cost T-233 removed, and it is a second surface to keep in step with the sheet. Reversible.
  — 2026-09-14
- A `data-` range is rejected: it cuts the clause away from the text a reader checks it against, and
  a Markdown source has no range boundary a deck can name except its headings. Reversible.
  — 2026-09-14
- The anchor is a heading's text, not an id: `quickview.py` writes headings with no ids, and adding
  them would re-render every deck's sources. Text is compared without case or extra space.
  Reversible. — 2026-09-14
- DS-105's *source controls that open nothing* counts an anchor that names no heading in its
  source. DS-105's text is unchanged, because the clause already covers it. Reversible. — 2026-09-14
- No seeded variant: `static_variants.py` seeds only the reference deck, which carries no quick view.
  Both directions are `audit.py`'s self-test, and the real case is measured on a copy of
  `sort-window`. Reversible. — 2026-09-14

On a copy of `examples/sort-window/sort-window.html` whose first *Throughput model* opener carries
`data-qv-at="Failure"`, in headless Chrome at 1920x1080:

| Case | Result |
| :--- | :--- |
| the anchored opener | `scrollTop` 1027, *Failure* marked, the heading 0.0 px from the top of the sheet, a solid rule down its edge |
| an opener with no anchor | `scrollTop` 0, nothing marked |
| DS-105 with `Failure` | `source controls that open nothing: 0 of 19`, pass |
| DS-105 with `Recovery` | `1 of 19 - Throughput model at 'Recovery', which is no heading in it`, fail |

The self-test adds four cases: an exact heading, the same heading with different case, spacing and an
entity, a heading the source does not have, and no anchor.

§1.14 after the shell edit: four decks synced, the fixture regenerated, `density.py check` `0 wrong`
on each, and the size figures corrected.

**Record `001` closed.** **The look is owed**: [`../docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md) row 16.

**Outputs produced**
- `shell/deck.js`: `openQuick` opens at the named heading and marks it
- `shell/components.css`: the mark
- `tools/deck/audit.py`: `section_name`, the anchor check, four self-test cases
- `docs/COMPONENT-CONTRACT.md`: `data-qv-at`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| every record named above closed with its remedy measured | **pass**, look owed | §3. The look is `OWED-LOOKS.md` row 16 |
| each fix proved by seeding the defect, in both directions | **pass** | §3's table and the self-test |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | **pass** | Lint, then the full gate on the finished tree |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-14 | → done | Decided and built: an anchor names a heading in the source, and the quick view opens at it. A component and a range are rejected in §3. Record `001` closed; the look is owed as `OWED-LOOKS.md` row 16. |
| 2026-08-29 | → proposed | Raised by [T-225](T-225-triage-the-claimai-adopter-report.md), the triage of the ClaimAI adopter report. **`PH3`**: not a defect in the published plugin's behaviour, so `CLAUDE.md`'s rule puts it in the main line rather than reopening a shipped phase. |
