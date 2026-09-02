---
id: T-295
title: Complete T-288's observation in a session that can take it, then decide the move on the evidence
type: decision
status: proposed
phase: specify
parent: T-287
blocked_by: []
related: [T-288, T-236]
work_package: PH3
owner: the project owner
business_value: high
effort: s
finding: CE-14
created: 2026-09-02
updated: 2026-09-02
deliverables: []
---

# T-295 — Complete T-288's observation in a session that can take it, then decide the move on the evidence

## 1. Specify

**Outcome**
`CE-14` is decided rather than deferred: either the deck-only and release-only rules move out of
`CLAUDE.md` under `.claude/rules/`, or the move is declined with what would reverse it written down
checkably. [T-288](T-288-move-the-rules-that-bind-only-deck-or-release-work-under-path-scoped-rules.md)
closed `not met` on its first criterion — the mechanism is proven on this harness but was never
observed in this repository, because a rule file added mid-session does not fire and no session can
start itself. That is one turn of work for a session that starts with the probe already in place.

**Scope**
- In: the observation — the probe at `.claude/rules/t-288-probe.md` is already planted with `paths:`
  front matter and the marker `T288-PROBE-9F3A2C`; read `docs/BRIEF.md` and record whether the marker
  arrives, and what `~/.claude/instructions-loaded.log` says about this session
- In: **the decision**, which `T-288` never reached and which is not mechanical — two findings it
  raised bear on it, and both are in its §3: this repository publishes, and `.claude/` is untracked
- In: reading the sibling project's precedent **before** proposing the move, not after —
  taskmd's `T-169` took the same decision and declined it, and its §3 names the evidence that moved it
- In: deleting the probe, whichever way the decision goes
- Out: moving anything before the observation lands. That is `T-288`'s rule and it is unchanged
- Out: advising adopters to use `.claude/rules/`

**Inputs**
- [T-288](T-288-move-the-rules-that-bind-only-deck-or-release-work-under-path-scoped-rules.md) §3 —
  the log evidence, the format that fired, the boundary, and the two findings
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.3 `CE-14` and §11.1
- `~/.claude/instructions-loaded.log` — the standing instrument, machine-local
- taskmd's `T-169`, in the clone beside this one

**Acceptance criteria**
- [ ] The marker's arrival is recorded as an **observation of what was delivered**, and the hook
      log's line for the session is quoted — never inferred from the marker being in context
- [ ] The decision is taken and its reasons named, including which of `T-288` §3's two findings moved
      it. A decline is written in terms a later session can check, not as a mood
- [ ] If the decision is **carry**: `.claude/rules/` is tracked, every moved rule has exactly one
      home, rule 6 stays in `CLAUDE.md` with one sentence saying why, and `CLAUDE.md`'s measured pair
      is re-measured in the same edit
- [ ] The probe is deleted either way, and `.claude/rules/` is left holding only what the decision put
      there
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- **Should a published plugin ship a `.claude/rules/` file at all?** It is machine-shaped instruction
  for one harness, in a repository whose front page promises clone-and-run. Untracked, the move
  deletes rules from what an adopter receives; tracked, the repository starts carrying a file that
  only one tool reads. **The project owner answers**, and the answer decides the task rather than
  colouring it.

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
| 2026-09-02 | → proposed | Raised in B19 while closing [T-288](T-288-move-the-rules-that-bind-only-deck-or-release-work-under-path-scoped-rules.md) `not met`. That task closes on its own instruction and the move is then unowned, which is a gap rather than a conclusion. **Unbatched, for the owner**, like the rest of [T-287](T-287-audit-what-a-session-pays-per-turn-and-why-it-grows.md)'s children — the audit's own rule. |
