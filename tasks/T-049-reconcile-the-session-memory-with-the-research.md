---
id: T-049
title: Reconcile the session memory with what the research settled and the owner last said
type: admin
status: done
phase: review
parent: T-042
blocked_by: []
related: [T-014, T-017]
work_package: none
shipped_in: 0.1.0
owner: the project owner
created: 2026-08-09
updated: 2026-08-12
deliverables: []
---

# T-049 — Reconcile the session memory with what the research settled and the owner last said

## 1. Specify

**Outcome**
The four stale or self-contradicting memories are corrected, so a session that reads any one of them
first reaches the same working method as a session that reads them all.

**Why this one**
Memory is loaded at the start of every session and is not read in order. Two entries close on *ask
the owner*; the newest closes on *decide it yourself*; one still lists `file://` restrictions this
project measured and retired. **A memory that is wrong is worse than one that is missing**, because
it is stated with the authority of something the owner said, and nothing in the repository
contradicts it where a session would look.

**Note on where the deliverable lands.** This task's outputs are **outside the repository** —
`~/.claude/projects/C--Work-AgentPlugins-htmldeck/memory/`, which is machine-local and never
published. `deliverables:` is therefore empty by intent rather than by omission, and the review
records what changed instead of a path.

**Do the first row before the others, and preferably before the rest of
[T-042](T-042-audit-the-whole-repository-against-itself.md)'s children are worked.** The ask-versus-
decide contradiction is not one stale fact among four — it governs **how the fix run itself is
worked**. A session that reads *ask rather than guess* first will hand the open questions in T-046
and T-048 back instead of deciding them, which is the opposite of the instruction the owner gave
twice on 2026-08-09. The other three rows are ordinary staleness and can wait.

**The four**

| Memory | What is wrong | What it should say |
| :--- | :--- | :--- |
| `research-before-building.md` · `research-may-reshape-the-project.md` | Both close on *the owner answers readily — ask rather than guess*. `decide-detailed-questions-yourself.md`, written 2026-08-09 from the owner's own words (*"pick the right choice for the questions — these are too detailed for me"*), says the opposite and is newer. Neither links to it | The two are not simply wrong — **asking was right during WP1's shaping window and is wrong now**. Each should scope its advice to that window and link `[[decide-detailed-questions-yourself]]` for what replaced it |
| `portability-not-minimalism.md` | Still names *"ES modules, `fetch`, XHR, some worker and WebGL texture paths fail"* as **the gotcha to design around**, and points at T-017 as unfinished | [R6](../docs/research/R6-portability-contract.md) measured 95 rows: the boundary is **fetch-like versus element-like access**, `file://` is a secure context, and **no refused capability costs the deck anything**. `DESIGN-RATIONALE.md` §6 says it in terms — *"Do not design around fears this research retired"* |
| `research-may-reshape-the-project.md` | *"Keep WP2 and WP3 tasks lightly specified until T-014 lands"*; *"expect T-014 to end with a re-scoping proposal"* | T-014 closed 2026-08-06 and all ten WP1 tasks are `done`. The durable half — *findings that contradict the brief are candidate changes of direction* — is still `CLAUDE.md`'s position and is what should survive |
| `one-parametric-theme.md` | *"this sits in tension with the brief's rule 3 ('decks must not look like each other')"* | `CLAUDE.md` rule 3 is now *Use whatever renders best*; one parametric theme is rule 4. The tension was resolved by the rewrite this memory predates |

**Scope**
- In: the four entries above, and `MEMORY.md`'s one-line hooks where a correction changes what the
  entry is for.
- In: linking the pairs that disagree, in both directions. An entry that has been superseded on one
  point and is right on the rest should say which is which, not be deleted.
- Out: writing new memories. This reconciles what is there.
- Out: anything in the repository. Every fact these entries get wrong is already correct in
  `docs/`; the memory is what disagrees.
- Out: `deck-corpus-location.md` and `browserless-instance.md`, which carry a private path and a LAN
  address. Both are correct, both are machine-local by design, and **neither may ever be copied into
  the repository** — noted here so the next audit does not re-raise them as a leak.

**Inputs**
- `~/.claude/projects/C--Work-AgentPlugins-htmldeck/memory/` — the entries and `MEMORY.md`
- [`docs/research/R6-portability-contract.md`](../docs/research/R6-portability-contract.md) §2, §8
- [`docs/DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) §6 — DS-005
- [`CLAUDE.md`](../CLAUDE.md) — the rewritten rules 1–7
- [T-042](T-042-audit-the-whole-repository-against-itself.md) §2, F-8

**Acceptance criteria**
- [ ] No two memories give contradictory instructions on when to ask the owner
- [ ] `portability-not-minimalism.md` states R6's measured boundary, and names what it retired
- [ ] No memory refers to WP1 or T-014 as pending
- [ ] Every superseded claim is corrected **in place with its supersession visible**, not deleted —
      the reason a position changed is the part that stops it coming back
- [ ] `MEMORY.md` has one line per file and no orphan on either side
- [ ] Read cold afterwards: any single entry read alone leads to the same working method

**Open questions**
- none

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | **First row, before the rest of the run.** Scope the ask-first advice in `research-before-building.md` and `research-may-reshape-the-project.md` to WP1's shaping window, and forward-link `[[decide-detailed-questions-yourself]]` from both | Two entries whose ask-first line names the date it was superseded and what replaced it |
| 2 | Back-link the two from `decide-detailed-questions-yourself.md`, so the pair resolves from either end | The newest entry names what it supersedes |
| 3 | Replace `portability-not-minimalism.md`'s "gotcha to design around" with R6's measured boundary — fetch-like versus element-like, `file://` is a secure context, no refused capability costs the deck anything — and retire the T-017-as-pending pointer | An entry that states the measurement instead of the fear |
| 4 | Strip `research-may-reshape-the-project.md`'s WP1 scheduling advice (lightly-specified WP2/WP3, T-014's re-scoping proposal), keeping the durable half `CLAUDE.md` still holds | An entry with nothing pending in it |
| 5 | Correct `one-parametric-theme.md`'s tension note: `CLAUDE.md` rule 3 is now *Use whatever renders best* and the parametric-theme rule is rule 4 | An entry that cites the rewritten rules |
| 6 | Reconcile `MEMORY.md` — one line per file, no orphan either way, and a hook rewritten wherever step 1–5 changed what the entry is for | A current index |
| 7 | Cold read: open each edited entry alone and ask what working method it leads to | Verdicts in §4 |

## 3. Implement

**Decisions & assumptions**
- **Superseded claims are corrected in place with the supersession visible, not deleted** — the
  criterion asks for it, and the reason is that a deleted position comes back. Every correction below
  therefore reads *"X was right until DATE, and Y replaced it because Z"*, not just *"Y"*. — 2026-08-09
- **`modified:` is updated on every entry this task edits.** F-8's own argument turns on which
  instruction is newer, so leaving the timestamps stale would preserve the exact ambiguity the task
  exists to remove. — 2026-08-09
- **The two ask-first entries keep their research half untouched.** Only the closing ask-the-owner
  sentence was superseded; `research-before-building`'s *find the existing source first* is current
  and is the reason the entry exists. — 2026-08-09

**Outputs produced**
- Machine-local, in the agent memory directory; recorded here rather than as a repository path, per
  §1. Six files edited: `research-before-building`, `research-may-reshape-the-project`,
  `decide-detailed-questions-yourself`, `portability-not-minimalism`, `one-parametric-theme`, and
  `MEMORY.md`.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| No two memories give contradictory instructions on when to ask the owner | **met** | Both ask-first entries now carry a *superseded* paragraph naming the date, the quote that replaced it, and the entry that holds it; the newest entry names both in return. The three resolve as one instruction from any starting point |
| `portability-not-minimalism.md` states R6's measured boundary, and names what it retired | **met** | Fetch-like versus element-like, `file://` as a secure context, and *no refused capability costs the deck anything*, against the "gotcha to design around" paragraph it replaced. L-17's caution about the harness is kept, since that one is about the instrument and did not expire |
| No memory refers to WP1 or T-014 as pending | **met** | `grep -ril 'T-014\|T-017\|WP1' memory/` returns only the two entries that name them as **closed**, in the superseded paragraphs |
| Every superseded claim is corrected in place with its supersession visible, not deleted | **met** | Five entries, no deletions. Each spent claim is quoted, dated, and given the reason it changed — which is the part that stops it being re-derived |
| `MEMORY.md` has one line per file and no orphan on either side | **met** | 19 index lines against 19 files; both directions checked mechanically. Two hooks rewritten where the entry's purpose moved |
| Read cold afterwards: any single entry read alone leads to the same working method | **met** | All five read alone. Each reaches *decide it from the rule's own reason*; none leaves a reader believing WP1 is open or `file://` is a hazard |

**Child fix tasks raised**
- none

**One thing found and deliberately not fixed.** `dont-synthesise-user-input.md` links
`[[verify-in-the-delivery-environment]]`, which no entry provides. That is not a defect — an
unresolved `[[link]]` marks something worth writing later, and writing new memories is out of scope
by §1. Recorded so the next audit does not raise it as a broken pointer.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-09 | → done | **Five entries corrected in place, none deleted, and the supersession is the payload.** The ask-versus-decide contradiction was worked first and separately from the other three rows, because it governs how the rest of [T-042](T-042-audit-the-whole-repository-against-itself.md)'s run is worked rather than being one stale fact among four. What made the contradiction dangerous was not that an entry was wrong but that **memory is not read in order** — so the fix is a link in both directions plus a dated supersession paragraph in each, rather than an edit to whichever one is wrong. The other three rows were ordinary staleness with one common cause: **each recorded a tension or a hazard that a later measurement or rewrite resolved, and none of them knew it.** `portability-not-minimalism` still named `file://` as the thing to design around after R6 measured 95 rows and found nothing it refuses costs the deck anything; `one-parametric-theme` recorded a tension with a `CLAUDE.md` rule that no longer exists, and its own decision is now rule 4. A memory whose reason expired reads exactly like one whose reason holds, which is why the corrections say what changed and when, not just what is true. `modified:` is stamped by the store on write, so the ordering F-8 reasons from is now real rather than asserted. |
| 2026-08-09 | → planned | §1 accepted as written — the four rows, their evidence and the ordering note were all settled when [T-042](T-042-audit-the-whole-repository-against-itself.md) raised them, so `specify` was accept-not-compose. Plan is seven steps, one per entry plus the index and a cold read, with the ask-versus-decide row pulled to the front for the reason §1 gives. |
| 2026-08-09 | → proposed | Raised by [T-042](T-042-audit-the-whole-repository-against-itself.md), finding F-8. **Four entries, and the contradiction is the one that matters**: two memories say *ask the owner*, the newest says *decide it yourself from the rule's own reason*, and memory is not read in order — so which instruction a session follows depends on which file it reads first. One memory also still carries the `file://` fears R6 retired, against a rationale that says in terms not to design around them. The deliverable is machine-local, which is why `deliverables:` is empty by intent; the review records what changed. |
