---
id: T-295
title: Complete T-288's observation in a session that can take it, then decide the move on the evidence
type: decision
status: done
phase: review
parent: T-287
blocked_by: []
related: [T-288, T-236]
work_package: PH3
owner: the project owner
business_value: high
effort: s
finding: CE-14
created: 2026-09-02
updated: 2026-09-14
shipped_in: unreleased
deliverables: [docs/lessons/L-164.md]
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
- In: the observation — the probe, `t-288-probe.md` under `.claude/rules/`, is already planted with `paths:`
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
  **Answered by the owner 2026-09-13: carry, if the observation shows the marker arriving.** The
  objection does not separate the two files — `CLAUDE.md` is also read by one harness only — and
  taskmd's `T-169` declined the same move on its margin under budget, where this repository's
  `CLAUDE.md` is over its own bound.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Read `docs/BRIEF.md` in the main context before any other matching file, first in part and then whole, and read the log after each | Observation 1: not delivered, not logged |
| 2 | Name what differs between this probe and the only firing on record, taskmd's, and read the harness documentation for the front-matter form | Three candidate causes: an inline array, a separator in the glob, a rule ignored by name |
| 3 | Plant marker-only probes that vary one of those at a time, and have a context that starts after they exist read the trigger files. A headless session could not authenticate, so a subagent of this session is that context | Observation 2: every form loads in a subagent |
| 4 | Put the planted probe itself to the same subagent test | Observation 3: delivered and logged in the subagent |
| 5 | Take the decision against the owner's condition, read by its reason, and write the reversal | §3 |
| 6 | Delete every probe and the `.gitignore` line naming the first; reconcile `CLAUDE.md`, `CONTEXT-AUDIT.md` §6's row and the lesson | The outputs below |

## 3. Implement

**Observation 1 — the main context. Not delivered, not logged.** This session started 2026-09-14,
twelve days after the probe was last written, and its main context read `docs/BRIEF.md` before any
other file the probe matches: once with a 60-line limit and once whole. Neither result had a block
appended, and the log holds one line for this session across both reads — its start:

```
2026-09-14T00:20:15 {"session_id":"d732d326-…","hook_event_name":"InstructionsLoaded",
"file_path":"…\\CLAUDE.md","memory_type":"Project","load_reason":"session_start"}
```

**Observation 2 — what does not stop a load.** The probe differed from the one firing on record in
three ways: `paths: ["docs/BRIEF.md"]` is an inline array where the documentation shows only a block
list, its glob holds a separator where taskmd's was `CLAUDE.md`, and `.gitignore` names it. Seven
marker-only probes, written mid-session, varied these one at a time — two front-matter forms on
`LICENSE`, two on `docs/AUDIT-METHOD.md`, a block list on `tools/deck/**`, and a block list on
`LICENSE` ignored by name beside one that was not. **Every form loaded in a subagent**, each line
timed at that subagent's read and carrying its `prompt_id`: both forms, both glob shapes, the
directory glob, and the ignored file. The non-ignored control wrote **no** line although the subagent
reported its marker in context — the log's loss under concurrency, recorded by taskmd's `T-169`,
seen again. **A main-context read of `LICENSE` after the probes existed delivered nothing and logged
nothing**, which agrees with taskmd's `T-171`: a rule added mid-session does not reach the main
context.

**Observation 3 — the planted probe. Delivered and logged, in a subagent only.** A subagent of the
same session read `docs/BRIEF.md` whole and reported `T288-PROBE-9F3A2C` in its context, and the log
wrote, at that read:

```
2026-09-14T00:27:01 {"session_id":"d732d326-…","prompt_id":"8e641ce8-…",
"hook_event_name":"InstructionsLoaded","file_path":"…\\.claude\\rules\\t-288-probe.md",
"memory_type":"Project","load_reason":"path_glob_match","globs":["docs/BRIEF.md"],
"trigger_file_path":"…\\docs\\BRIEF.md"}
```

Its `prompt_id` is the subagent's; the main context made no read of that file then. **So the line
is this session's and the delivery is not the main context's** — a distinction the log does not draw,
which is [L-164](../docs/lessons/L-164.md).

**Decisions & assumptions**
- **Not carried. Nothing moves, and `CLAUDE.md` stays over its bound** — 2026-09-14. The owner's
  condition was *carry, if the observation shows the marker arriving*, and its reason is that the
  deck and release rules reach the agent doing that work. That agent is the main context, and there
  the marker did not arrive from a rule that existed before the session started. Carrying on the
  subagent's delivery would take the rules away from the main context if its null is real, which
  costs rules 1–5 and 7 on exactly the sessions they bind. Declining costs the tier-1 debt
  `CLAUDE.md` already records. *Rejected:* **carry on the subagent's line** — it is evidence about a
  different reader. *Rejected:* **keep a probe in place for the next session** — §1 requires deletion
  either way, and the recipe below is three lines to rebuild.
- **Neither of `T-288` §3's two findings moved it** — 2026-09-14. The owner's answer of 2026-09-13
  had settled both toward carry: tracking a rule file is no worse than tracking `CLAUDE.md`, and
  taskmd's `T-169` declined on a margin this repository does not have. The decision turned on the
  observation, which is the one input that answer left open.
- **The main-context null has one untested cause, and the reversal is built to remove it** —
  2026-09-14. The first main-context read of `docs/BRIEF.md` was partial. If the harness counts a
  file as seen on a partial read that did not trigger, the whole read after it would not trigger
  either. taskmd's `T-171` saw a main context receive a rule on 2026-08-17, so the mechanism has
  worked there before.

**What reverses this, in terms a later session can check.** All three, in one session:

1. A block-list probe — `paths:` with one entry naming a small file no start-up load reads — exists
   under `.claude/rules/` **before** the session starts.
2. The session's **first tool call** is a whole read of that file, from the main context, with no
   subagent running.
3. That read's result has the probe's body appended, **and** `~/.claude/instructions-loaded.log`
   gains a `path_glob_match` line naming the probe, timed at that read.

When all three hold, the owner's 2026-09-13 answer applies unchanged: carry, with `.claude/rules/`
tracked and the probe deleted. When the body arrives and no line does, the delivery still counts,
because the log loses lines.

**Outputs produced**
- This record, and [L-164](../docs/lessons/L-164.md)
- `.claude/rules/` — the planted probe and T-295's seven probes deleted, and the directory with them
- [`../.gitignore`](../.gitignore) — the line naming the probe removed, and the comment about
  `.claude/` restated as decided
- [`../CLAUDE.md`](../CLAUDE.md) — the debt paragraph pointed at this decline instead of at `T-288`,
  and its measured pair re-measured in the same edit
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) — §6's `CE-14` row reads declined

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The marker's arrival recorded as an observation of what was delivered, with the log's line quoted | met | Recorded per context, because the two disagree: the main context, no delivery and only the start line; a subagent of the same session, the marker reported and the `path_glob_match` line quoted in §3. Neither is inferred from the marker being in this record's author's context |
| The decision taken, its reasons named, including which `T-288` §3 finding moved it; a decline checkable | met | Not carried. Neither finding moved it — the owner's answer had settled both — and §3 says so. The reversal is three observable conditions in one session |
| If carry: tracked rules, one home each, rule 6 with its sentence, the pair re-measured | n/a | The decision was not to carry. `CLAUDE.md` was edited anyway, to point its debt paragraph here, and its pair re-measured in that edit |
| The probe deleted either way, `.claude/rules/` holding only what the decision put there | met | The decision put nothing there. `.claude/rules/` no longer exists, and the `.gitignore` line that named the probe is gone |
| `lint.py` and `check_all.py` green, run separately | met | Lint first, then the full gate, on the tree committed with this record |

**Child fix tasks raised**
- none. The reversal is an observation for the owner to ask for, not scheduled work.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-02 | → proposed | Raised in B19 while closing [T-288](T-288-move-the-rules-that-bind-only-deck-or-release-work-under-path-scoped-rules.md) `not met`. That task closes on its own instruction and the move is then unowned, which is a gap rather than a conclusion. **Unbatched, for the owner**, like the rest of [T-287](T-287-audit-what-a-session-pays-per-turn-and-why-it-grows.md)'s children — the audit's own rule. |
| 2026-09-13 | (no change) | The owner answered the open question: carry, on the observation. Still `proposed`. |
| 2026-09-14 | proposed → done | **Not carried.** The whole lifecycle ran in one session on the owner's instruction in the handoff. The planted probe never reached the main context of a session started twelve days after it, on a partial or a whole read, and reached a subagent of the same session at once. Probes varying the front-matter form, the glob shape and the ignore line all loaded in a subagent, so none of those explains the null. The owner's condition is read by its reason — the rules must reach the agent doing the work — and is unmet there. Every probe deleted; the reversal is three conditions in §3; [L-164](../docs/lessons/L-164.md). |
