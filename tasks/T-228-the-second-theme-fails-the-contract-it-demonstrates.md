---
id: T-228
title: Bring lattice.css up to the theme contract, and put a theme in a gate's subject
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

# T-228 — Bring lattice.css up to the theme contract, and put a theme in a gate's subject

## 1. Specify

**Outcome**
`python tools/deck/theme.py validate themes/lattice.css` exits 0, and a tracked theme is inside some check's subject. Today it exits 1 with **fifteen tokens not declared** - the whole affordance and press band, most of the inter-slide transition, `--motion-density`, both pager tokens and the three pop tokens - every one of which arrived after the file did, because `check_all.py` runs `theme.py check <deck>` and never `theme.py validate <theme>`.

**Closes** `PR-37` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: the fifteen declarations in `themes/lattice.css`
- In: **the missing step**, which the register calls the larger half: `check_all.py` already discovers every checker and every deck, and discovering every *theme* is what would have caught this the day DS-240 landed
- Out: what the tokens' values should be for a second look - that is a design question and this is a conformance one
- Out: `themes/quarto.css`, which passes

**Inputs**
- `PR-37` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3
- [`docs/THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) section 5

**Acceptance criteria**
- [ ] `theme.py validate` exits 0 on every tracked theme
- [ ] a theme that drops a required token **fails a gate**, proved by seeding one rather than asserted
- [ ] `python tools/check_all.py` green with the new step classified

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
