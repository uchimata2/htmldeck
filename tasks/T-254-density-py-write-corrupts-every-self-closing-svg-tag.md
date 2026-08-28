---
id: T-254
title: Fix set_var's self-closing tag insertion, and have write verify what it wrote
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-225]
work_package: PH1
owner: the project owner
business_value: critical
effort: s
created: 2026-08-29
updated: 2026-08-29
deliverables: []
---

# T-254 — Fix set_var's self-closing tag insertion, and have write verify what it wrote

## 1. Specify

**Outcome**
`density.py write` produces valid markup on a deck containing self-closing SVG tags. Today `set_var` assumes a tag's last character is `>` and everything before it is attribute space, so `<circle ... />` becomes `<circle ... /  style="--dp:0">` — **seven invalid tags on one slide**. The browser reparents the broken subtree and `DS-035` then reports three labels at `0.0 du`, which names neither the tool nor the tag. **It is intermittent** — `0, 3, 3` over three runs — so it reads as a race in the author's own motion.

**From the adopter report** [`015`](../docs/adopter-reports/claimai/015-density-py-write-corrupts-a-self-closing-svg-tag.md).

**Scope**
- In: the one-line guard in `set_var`: insert before `/>` when the tag is self-closing
- In: **`write` verifying what it wrote** — it already parses the deck to find the tags, so re-parsing and refusing to save a file that gained a malformed tag would have caught this in the run that caused it
- In: whether `DS-035` should say a CTM is degenerate: `0.0 du` is not small type, it is no type
- Out: anything the records above do not name. The report is a closed one-way hand-over — there is no
  channel back and none is expected, so a question this task cannot answer is settled here rather
  than asked.

**Inputs**
- the record above, [`015`](../docs/adopter-reports/claimai/015-density-py-write-corrupts-a-self-closing-svg-tag.md) — each carries its evidence, its version and its own proposed fix
- `tools/deck/density.py` `:179` — the branch that runs when the tag carries no `style=` yet
- the adopter's own repair, `re.subn(r'/ (style="[^"]*")>', r' \1/>', html)`, which is evidence of the shape rather than the fix to take

**Acceptance criteria**
- [ ] every record named above is **closed with its remedy measured**, or explicitly deferred with the
      reason recorded in this task
- [ ] each fix is proved by seeding the defect and watching the check fire, in both directions where
      the record's own evidence is a verdict (**L-125**)
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None yet. Every record carries its own evidence and its own proposed fix; the proposal is a
  hypothesis and whoever implements it measures before committing to it.

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
| 2026-08-29 | → proposed | Raised by [T-225](T-225-triage-the-claimai-adopter-report.md), the triage of the ClaimAI adopter report. **`PH1`**: a defect an adopter met in the published `0.6.0`, which is `CLAUDE.md`'s one condition for reopening the phase. Verified against this tree before the record was actioned — the report's `Version seen` was stamped rather than re-run on fourteen of the twenty-seven. |
