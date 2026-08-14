---
id: T-149
title: Prune the memory index of spent entries
type: admin
status: done
phase: review
parent: T-130
blocked_by: []
related: [T-130, T-134]
work_package: PH3
finding: CE-10
shipped_in: unreleased
owner: the project owner
business_value: low
effort: xs
created: 2026-08-14
updated: 2026-08-14
deliverables: []
---

# T-149 — Prune the memory index of spent entries

## 1. Specify

**Outcome**
The agent memory index stops paying, on every turn of every session, for entries that tell the reader
in their own text not to use them. **The finding is `CE-10`**, stated in
[`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.1; it is not restated here.

**It is tier 1 and it is not this repository's.** The index measured 6,134 bytes over 39 lines and 35
entries when `CE-10` was written, and **6,706 over 41 lines and 38 entries when this task opened it on
2026-08-14** — the subject grew 9% while the finding sat, which is why §6.2's first rule is to
re-measure. It is one of the three files [`../CLAUDE.md`](../CLAUDE.md) records as loaded on every
turn. The bound written there deliberately covers only the file this repository owns, because a
repository cannot edit the other two — **so this task is the owner acting on their own store, and the
repository's part is the check, not the edit.**

**Scope**
- In: which entries are spent, and which are project-shaped and belong in this repository instead,
  where they are shared rather than private.
- In: the check each removal owes — is this fact recorded in [`../docs/LESSONS.md`](../docs/LESSONS.md)
  or elsewhere in the tree?
- Out: any change this repository can make on its own. The store is the owner's.
- Out: memories from other projects. This is scoped to the index this project's sessions load.

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.2 — read before starting; §6.1 — `CE-10`
- [`../CLAUDE.md`](../CLAUDE.md) — *What loads every turn, and what bounds it*, which names this file
  as tier 1 and says why it is outside the bound
- [`../docs/LESSONS.md`](../docs/LESSONS.md) — what the repository already records, and therefore what
  a memory need not

**What specifying must settle**
- What *spent* means as a test somebody can apply twice and get the same answer, rather than as a
  judgement per entry.
- What happens to a memory that is still true but project-shaped: promoted into the repository, or
  left private.
- Who runs it, and how the result is recorded here when the artifact edited is not in this tree.

### 1a. What specifying settled — 2026-08-14

**What *spent* means, as a test two people apply and agree on.** It is per **facet**, not per entry.
A facet is spent when it is either **superseded** — a later verified fact overrode it, usually said in
the entry's own text — or **absorbed**, meaning a repository document states it and the memory adds
nothing that document lacks. **An entry is spent when every facet is.**

**The clause that decides the hard cases is the third one: a cross-project facet is neither.** No
repository here states it, so it has no other home. That is what separates two entries that look
identical from the index: `CLAUDE.md` rules out a co-author trailer *in htmldeck*, and the memory says
*check an established history before adding one in any of their repositories*. The first half is
absorbed; the second is the reason the entry stays.

**Absorption is verified by searching the tree, not from recollection**, and the strongest case is
absorption into [`../CLAUDE.md`](../CLAUDE.md): both files load on every turn, so the fact is charged
twice per turn and the repository's copy is the better one — shared, reviewed, and reachable by a gate.

**A still-true, project-shaped facet in no document is promoted before it is pruned**, not dropped.
None arose here; the rule is written because the test would otherwise lose facts by construction.

**Who runs it, and what is reversible.** The agent, in the owner's store, because the memory
instructions already make pruning its job — and **entries move to a `spent/` subfolder rather than
being deleted**. The index line is the whole tier-1 saving and the file costs nothing where nothing
loads it, so the reversible option gives up no part of the outcome. Deleting `spent/` is the owner's.

**Acceptance criteria**
- [x] *Spent* is written as a test, applied per facet, with the cross-project clause stated
- [x] Every removal is justified by naming the repository document that now holds the fact
- [x] Nothing is destroyed: spent entries move, and the move is stated to the owner
- [x] No link is left orphaned by the move
- [x] The index is re-measured before and after, dated
- [x] The test itself gets a durable home, so the next prune does not re-derive it

**Open questions**
- ~~**Whether a task in this tracker is the right instrument at all**~~ — **yes.**
  [T-135](T-135-cut-the-load-path-this-project-cannot-use.md) was the same shape, closed here, and its
  correction is the most cited thing it produced. The repository owes the test and the record; the
  edit is outside the tree and is named rather than committed.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Re-measure the index, then read every entry the index line marks as a candidate | The 2026-08-14 before-figure, and a shortlist |
| 2 | For each candidate, search the tree for the fact and record the document that holds it | An absorption verdict per facet, not per entry |
| 3 | Move the spent entries to `spent/`; repoint every `[[link]]` to them at the document that now owns the fact | Nothing destroyed, nothing orphaned |
| 4 | Rewrite the index, and cut any entry carrying another entry's history | The tier-1 saving |
| 5 | Write the test as its own memory, so the next prune reads it instead of re-deriving it | A durable home outside this task |

## 3. Implement

**Seven entries moved, and what now holds each fact.** Verified by searching the tree, 2026-08-14.

| Moved to `spent/` | The home that holds it |
| :--- | :--- |
| `corpus-is-not-publishable` | [`../CLAUDE.md`](../CLAUDE.md) *Publishing constraints*, operatively and with the one ruled exception |
| `one-parametric-theme` | [`../CLAUDE.md`](../CLAUDE.md) rule 4, near-verbatim including *do not build it yet* |
| `research-may-reshape-the-project` | [`../CLAUDE.md`](../CLAUDE.md) *The objectives are still being shaped* |
| `portability-not-minimalism` | [`../CLAUDE.md`](../CLAUDE.md) rules 1, 2, 3 and 5; the `file://` half is [`../docs/research/R6-portability-contract.md`](../docs/research/R6-portability-contract.md) |
| `htmldeck-purpose-and-scope` | [`../docs/BRIEF.md`](../docs/BRIEF.md), and the two-question interface is in the skill's own description |
| `progressive-disclosure-signature` | [`../docs/BRIEF.md`](../docs/BRIEF.md); its printing correction is [`../CLAUDE.md`](../CLAUDE.md) rule 5 |
| `phase-name-is-not-a-version-number` | [`../docs/lessons/L-69.md`](../docs/lessons/L-69.md), cited from tier 1 and gated by `tools/docs/lessons.py` |

**Six of the seven were absorbed into tier 1**, which is the sharpest form of the finding: the same
fact loaded twice on every turn, in two files the harness reads before the session starts.

**The index, before and after.**

| | Bytes | Lines | Entries |
| :--- | ---: | ---: | ---: |
| Before, 2026-08-14 | 6,706 | 41 | 38 |
| After | **5,818** | 37 | 32 |

**−888 bytes, −13.2%, paid on every turn of every session.** Seven entries left and one arrived —
the test itself, which had no home and would otherwise be re-derived by the next prune.

**Two things the pass found that the finding did not predict.**

- **Three `[[link]]`s were already dangling before this task touched anything**, and one of them —
  `evaluate-proposals-before-recording-them` — is a **typo for an entry that exists**. A pointer that
  looks live and resolves to nothing is worse than one the format declares legal, and nothing checks
  these. Repointed. The other two mark entries never written, which the format permits.
- **The first index rewrite grew tier 1 back by 380 bytes.** A preamble explaining why the index had
  shrunk is *content*, in a file whose first line says content lives in the linked file. Cut to a
  pointer at the new entry — the rule this task is about, caught applying to its own output.

**Decisions & assumptions**
- **Spent is per facet, and a cross-project facet is never spent** — otherwise the test deletes the
  half of an entry that is the reason it exists — 2026-08-14.
- **Move, do not delete.** The index line is the entire saving; the file costs nothing in `spent/`,
  and the owner can delete the folder once satisfied — 2026-08-14.
- **`check-rule-provenance` was a candidate and stays.** Its rule — give an extracted convention a
  provenance verdict, and read the tool rather than a document's account of it — is in no lesson and
  no document here; `L-20` and `L-56` are the nearest and neither says it. **It is also not spent by
  timing**: [T-119](T-119-audit-the-ruleset-for-rules-that-cost-more-than-they-return.md) may remove rules, and
  provenance is the question it asks — 2026-08-14.
- **`deck-corpus-location` stays and must never be absorbed.** It holds a machine path, which
  [`../CLAUDE.md`](../CLAUDE.md) *Publishing constraints* forbids the repository to carry. It is the
  clearest case in the store of a fact that belongs in memory and nowhere else — 2026-08-14.

**Outputs produced**
- The owner's store: seven entries in `spent/`, the index rewritten, eight files repointed, one
  entry trimmed of another entry's history, and one new entry carrying the test
- Nothing in this repository. The record is this task.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| *Spent* written as a test, per facet, with the cross-project clause | met | §1a; the clause is what saved `no-agent-coauthor-trailer` and `publishing-identity-and-history` |
| Every removal names the document that now holds the fact | met | the §3 table; six of seven are tier 1 |
| Nothing destroyed; the move is stated to the owner | met | `spent/`, seven files, reversible |
| No link orphaned | met | eight files repointed; the two still dangling pre-date this task and are legal |
| Index re-measured before and after, dated | met | 6,706 → 5,818, −13.2%, 2026-08-14 |
| The test gets a durable home | met | a new memory entry, so the next prune reads it |

**What this does not settle.** Whether the remaining 32 are all earning their line — the test was
applied to every index line, but only the fifteen it flagged were read in full. A second pass would
be a new task and there is no evidence it would pay.

**Child fix tasks raised**
- none. The dangling-link typo was fixed in place; nothing checks memory links and nothing here can,
  since the store is outside the tree.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-14 | → proposed | Raised at the owner's direction with the rest of the unraised findings; it ranked twelfth and was never a candidate. Scheduled to `plan` and no further. The one row of the six whose work is not a repository change, which is why its specification is mostly about the test for *spent* and about where the result is recorded. |
| 2026-08-14 | (unchanged) | **Removed from the decision batch the same day, with [T-148](T-148-give-a-measured-figure-a-durable-home.md), by the same argument**: `xs`, the instance already measured, and the entries that call themselves spent are named in `CE-10` — so a pass to decide whether it is worth doing costs what doing it costs. It takes the ordinary lifecycle in its turn. **The work itself is still the owner's**, because the store is not in this tree; what this repository owes is the test and the record. |
| 2026-08-14 | → specified → planned | §1a settled *spent* as a per-facet test with three clauses, and the third — a cross-project facet has no repository home and is therefore never spent — is what stopped the pass deleting the half of an entry that is the reason it exists. The finding's own figure had drifted 9% while it sat: 6,134 when written, 6,706 when opened. |
| 2026-08-14 | → in_progress → done | Seven entries moved to `spent/`, index **6,706 → 5,818, −13.2%**, and six of the seven were duplicating tier 1 — the same fact loaded twice on every turn. Two things the finding did not predict: three links were already dangling and one was a typo pointing at an entry that exists, and **the first rewrite grew the index back by 380 bytes** with a preamble explaining the shrink, which is content in a file whose first line forbids content. Nothing was deleted; `spent/` is the owner's to remove. |
