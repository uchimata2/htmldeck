---
id: T-226
title: Give the portfolio-review deck a home in both human-facing documents
type: fix
status: proposed
phase: specify
parent: T-219
blocked_by: []
related: []
work_package: PH3
owner: the project owner
business_value: high
effort: s
created: 2026-08-29
updated: 2026-08-29
deliverables: []
---

# T-226 — Give the portfolio-review deck a home in both human-facing documents

## 1. Specify

**Outcome**
`examples/portfolio-review/` is described where a reader is sent to find it. Today [`examples/README.md`](../examples/README.md) opens *Four decks* and lists three plus the seeded-defects fixture, and the front page sends a reader there for *every shipped deck*, which is a completeness claim the tree does not support and `0.6.0` shipped already false.

**Closes** `PR-02` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: the deck's section in `examples/README.md`, its artifact-manifest entry, and the front page's row
- In: **writing the section from the feature's end**, which is the register's hypothesis: the deck is `0.6.0`'s chart-engine example and the front page describes that feature without pointing at it
- Out: the other three decks' sections, which are correct
- Out: anything about the fixture's own row, which already says what it is

**Inputs**
- `PR-02` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3
- [T-113](T-113-evaluate-an-embeddable-chart-library-against-hand-authored-svg.md) - what the deck was built to demonstrate

**Acceptance criteria**
- [ ] `examples/README.md` describes four decks and its count agrees with `check_all.py`'s `DECKS`, derived rather than typed
- [ ] the front page's *every shipped deck* row resolves to a page that has them all
- [ ] `python tools/check_all.py` green, and the figure watcher reports no new stale figure

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
