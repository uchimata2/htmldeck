---
id: T-288
title: Move the rules that bind only deck or release work out of tier 1, under path-scoped rules
type: fix
status: done
phase: review
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
shipped_in: unreleased
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
| 1 | Measure addressability **before** moving anything — the first criterion, and the whole gate | `.claude/rules/` does not exist here; the harness has an `InstructionsLoaded` hook and it logs a `load_reason` |
| 2 | Read the log rather than the documentation: what load reasons has this machine ever recorded | 1,814 `session_start`, 1 `compact`, **1 `path_glob_match`** |
| 3 | Read the one `path_glob_match` line for the format that fired and what it carries | `paths:` front matter, delivered with `prompt_id`, `globs` and `trigger_file_path` |
| 4 | Plant a probe here and read a matching file, to get the reading on **this** repository | Did not fire — the boundary in §3 |
| 5 | Read the sibling project's decision before proposing this one | taskmd declined the same move; its `.claude/rules/` is empty |
| 6 | Close on the first criterion as the task instructs, move nothing, and leave the instrument in place for the session that can finish it | `not met`, and `T-295` |

## 3. Implement

**Nothing moved. The first criterion is not met, and it is the one §1 made the gate.**

**What was established, and it is most of the question**
- **The mechanism is real on this harness, and the instrument that proves it is a log rather than a document.** `~/.claude/instructions-loaded.log` is an `InstructionsLoaded` hook record of every instruction file this machine has loaded, one JSON line each, carrying a `load_reason`. Across 1,814 loads it holds three values: `session_start` (1,814), `compact` (1), and **`path_glob_match`** (1). So a path-scoped rule has fired here, once, and the claim is observed rather than read — 2026-09-02
- **The one firing was the sibling project's own probe**, 2026-08-17, a rule file under `taskmd`'s `.claude/rules/`. The line carries `prompt_id`, `globs` and `trigger_file_path`, so a rule load is self-identifying and arrives on a **prompt** rather than at launch — which is the second half of §1's first criterion, observed on this harness and in another repository — 2026-09-02
- **The front-matter key is `paths:`, and the hook reports it back as `globs`.** §1's scope named `paths:` and is right; a probe written with `globs:` is written against the payload rather than against the file — 2026-09-02

**The boundary, which is why this closes `not met`**
- **A rule file created mid-session does not fire.** A probe was planted here and a matching file read in the next turn; nothing arrived in context and the hook logged nothing for this session. `.claude/rules/` is enumerated at session start, so the observation §1 requires needs a session **started after the file exists** — which no session can perform on itself. That is the boundary, and it is a property of the harness rather than a gap in the attempt — 2026-09-02
- The probe is left in place, rewritten with `paths:`, carrying a marker and no rule content. It is **untracked** and reaches no clone. [T-295](T-295-complete-t-288s-observation-and-decide-the-move.md) is what deletes it.

**Two findings the next session needs, and neither is in `CE-14`**
- **`.claude/` is entirely untracked in this repository** — `git ls-files .claude/` returns nothing and `.gitignore` says nothing about it, so the one file there is untracked by accumulation rather than by rule. **This repository is a published plugin.** A rule left untracked deletes the deck and publishing rules from what a clone receives, which is not a context saving but a loss of the document. So the move owes a **tracked** rules directory, and whether a clone should receive a machine-shaped instruction file is a decision rather than a step — 2026-09-02
- **The sibling project took this decision and declined it.** taskmd's `T-169` decided whether its tier-1 prose moved into a path-scoped rule, and its rules directory is empty today. Its §3 names the **margin** as the evidence that moved it, and it took the decision against the *worse* branch — assuming the rule does not re-fire after a compaction — on the reasoning that a remedy which fails to pay under that assumption cannot be rescued by the better one. That is precedent this project has to read before proposing the same move, not after — 2026-09-02

**Outputs produced**
- `.claude/rules/t-288-probe.md` — the instrument, untracked, deleted by `T-295`
- [T-295](T-295-complete-t-288s-observation-and-decide-the-move.md)
- **No change to [`../CLAUDE.md`](../CLAUDE.md).** Its measured pair was re-measured anyway: 15,742 bytes against `docs/AUDIT-METHOD.md`'s 6,675, debt 9,067 — unmoved, so the paragraph there is still right and owed no edit

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| a rule with `paths:` shown by observation absent at session start and present after a matching file is read | **not met** | Both halves are observed on this harness — but the second in another repository, on 2026-08-17, and not here. A rule added mid-session does not fire, so the reading needs a session started after the file exists. §3 records the boundary |
| every moved rule has one home, and `refcheck.py` resolves every reference to it | n/a | Nothing moved, which is what the first criterion instructs |
| `CLAUDE.md`'s measured pair re-measured in the same edit, and the debt written there | n/a | There was no edit. Re-measured regardless and unchanged at 15,742 / 6,675, debt 9,067, so the paragraph is still true |
| rule 6 still in `CLAUDE.md`, with one sentence saying why it did not move | n/a | Every rule is still there. The sentence belongs to the move and is `T-295`'s to write |

**Child fix tasks raised**
- [T-295](T-295-complete-t-288s-observation-and-decide-the-move.md) — this task closes on its own instruction and the move is then unowned, which is a gap rather than a conclusion. `T-295` carries the observation, the two findings above, and the decision itself. Unbatched, for the owner, like the rest of `T-287`'s children.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-02 | → proposed | Raised by `T-287` from `CE-14`, the highest-ranked finding of the second context-economy run. `PH3` by `CLAUDE.md`'s rule. |
| 2026-09-02 | proposed → done | B19, closing **`not met`** on the first criterion as §1 instructs. The mechanism is proven on this harness — `path_glob_match` is in the hook log, once in 1,814 loads — but not here, and a rule added mid-session does not fire, so no session can take this reading on itself. Nothing moved. Two findings the ranking did not have: `.claude/` is untracked in a repository that is published, and the sibling project declined the same move. [T-295](T-295-complete-t-288s-observation-and-decide-the-move.md) carries all of it. |
