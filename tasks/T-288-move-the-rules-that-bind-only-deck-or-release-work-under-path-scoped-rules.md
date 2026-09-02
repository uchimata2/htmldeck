---
id: T-288
title: Move the rules that bind only deck or release work out of tier 1, under path-scoped rules
type: fix
status: proposed
phase: specify
parent: T-287
blocked_by: []
related: [T-236, T-143]
work_package: PH3
owner: the project owner
business_value: high
effort: s
finding: CE-14
created: 2026-09-02
updated: 2026-09-02
deliverables: []
---

# T-288 — Move the rules that bind only deck or release work out of tier 1, under path-scoped rules

## 1. Specify

**Outcome**
`CLAUDE.md` holds only what binds every turn. The rules that bind deck work — *The rules that must
survive* 1–5 and 7, *Voice*, *Verifying* — and the release-only publishing constraints load when a
session touches the trees they govern, through the harness's documented `.claude/rules/` mechanism
with `paths:` front matter. **Rule 6 stays in tier 1**: a path-scoped rule fires when a matching file
is *read*, which is one read too late for the rule that forbids reading a deck whole. The finding is
`CE-14` in [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.3; the section sizes it rests on
are in §11.1 there.

**Scope**
- In: a rule file `decks.md` under `.claude/rules/`, scoped to `examples/**`, `tools/deck/**`, `shell/**`, `themes/**`,
  `skills/htmldeck/**`; a rule file `release.md` there, scoped to `README.md` and `docs/PUBLISHING.md`;
  the moved paragraphs deleted from `CLAUDE.md`, not copied; `CLAUDE.md`'s measured pair re-measured
  in the same edit (`tools/docs/figures.py` holds it to the fence).
- In: **addressability measured before the move**, the ecoctx rule — write one small rule, start a
  session, confirm it loads only when a matching file is read and not at launch. The harness
  documents the mechanism; this desktop harness is not the one the document describes, and a claim
  about what loads is established by observation (`CLAUDE.md`'s own first section).
- Out: the publishing identity and the co-author rule, which bind every commit; `T-236`'s tier-2
  ruling, which this does not touch; any rule whose reason would be lost by the move.

**Inputs**
- `../docs/CONTEXT-AUDIT.md` §6.3 `CE-14`, §11.1
- `../CLAUDE.md` — the section sizes: rules 2,556, Voice 540, Verifying 1,568, Publishing 3,107 bytes on 2026-09-02

**Acceptance criteria**
- [ ] A one-line rule under `.claude/rules/` with `paths:` is shown, by observation, to be absent at
      session start and present after a matching file is read — or the task closes `not met` with the
      boundary recorded, and nothing moves.
- [ ] Every moved rule has exactly one home afterwards, and `refcheck.py` resolves every reference to it.
- [ ] `CLAUDE.md`'s measured pair is re-measured in the same edit and the debt figure written there.
- [ ] Rule 6 is still in `CLAUDE.md`, with one sentence saying why it did not move.

**Open questions**
- Whether the desktop harness honours `paths:` at all — measured, never assumed; the first criterion.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Write a one-line probe rule, restart, observe | the boundary: loads at launch, on read, or never |
| 2 | Move the deck-only and release-only sections; delete at the source | two rule files, a smaller `CLAUDE.md` |
| 3 | Re-measure the pair; `figures.py`; `refcheck.py`; `--docs` gate | the debt figure, green |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- `.claude/rules/...`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-02 | → proposed | Raised by `T-287` from `CE-14`, the highest-ranked finding of the second context-economy run. `PH3` by `CLAUDE.md`'s rule. |
