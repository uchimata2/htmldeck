---
id: T-141
title: Extract the upstream register into one document per owner
type: deliverable
status: done
phase: review
shipped_in: unreleased
parent: null
blocked_by: []
related: [T-130, T-140]
work_package: PH3
owner: the project owner
business_value: high
effort: s
created: 2026-08-13
updated: 2026-08-13
deliverables:
  - docs/upstream/handoff-skill.md
  - docs/upstream/taskmd.md
  - docs/upstream/harness.md
---

# T-141 — Extract the upstream register into one document per owner

## 1. Specify

**Outcome**
Each project this repository has observations for receives **one document that is entirely theirs**,
readable by someone who has never seen this repository, and reachable as a link rather than as a
section of somebody else's audit.

**Why**
[`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §7 holds eleven observations for three
different owners inside a 30 KB audit of this project's own context economy. **A recipient has to
read an audit of somebody else's repository to find three paragraphs addressed to them**, and every
future observation lands in the same place. The register was always meant to be handed over; §7 is
where it was assembled, not where it should arrive. Decided by the owner 2026-08-13.

**Scope**
- In: one document per owner under `docs/upstream/`, each self-contained.
- In: §7 kept as a section **with all three subsections**, each reduced to a pointer. `§7`, `§7.1`,
  `§7.2` and `§7.3` are cited from five task records and from §6.2, and a `§n` is a pointer like any
  other — removing the headings falsifies every one of those citations (**L-39**).
- In: §6.2's routing table, which currently says an observation goes to §7.
- In: writing this repository's own task ids with their owner named, from the recipient's side. `T-139`
  means nothing to a reader of the taskmd document, and **collides with their own numbering**
  (**TASK-WORKFLOW §4.1**).
- Out: changing any observation's content. This is a move plus the framing a standalone document
  needs; a correction pretending to be an extraction is how a record loses its history.
- Out: ranking, prioritising, or recommending. §7's rule travels with the content
  ([`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md) §6).
- Out: sending anything to anyone. This produces the documents; the handover is a separate act.

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §7 — the register, its preamble and the
  vintage rule
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.2 — the routing table that names §7
- [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §4.1 — a foreign tracker's id is written with its owner's name

**Acceptance criteria**
- [ ] Three documents, each readable with no knowledge of this repository: what it is, who wrote it,
      what the rules of the register are, and what to do with it
- [ ] Every observation appears exactly once across the three, and none lost its vintage stamp
- [ ] No bare task id anywhere: this repository's are named as the reporting project's, the
      recipient's are named as theirs
- [ ] `§7`, `§7.1`, `§7.2` and `§7.3` still exist and still resolve; §6.2 points at the documents
- [ ] Nothing is ranked, banded or prioritised
- [ ] `python tools/check_all.py` stays green

**Open questions**
- None.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Find every citation of `§7` and `§7.n` before moving anything | Five task records, `BRIEF.md`, §6.2 — so the headings stay |
| 2 | Write the three documents, each with its own *how to read this*: the no-priority rule, the vintage stamps, and how ids are named | `docs/upstream/` |
| 3 | Rewrite every row from the recipient's side — *your* `T-085`, *the reporting project's* `T-139` — and drop the ids that only meant something here | Rows a stranger can read |
| 4 | Reduce §7 to a pointer plus three pointer subsections, keeping every cited heading | §7 as an index |
| 5 | Repoint §6.2's routing table, including the *new owner* row | `upstream/`, not §7 |
| 6 | Re-run the gates and the cell-width scan | Every pointer resolves |

## 3. Implement

**Decisions & assumptions**
- **§7 keeps all three subsections as pointers rather than being deleted** — 2026-08-13. `§7`,
  `§7.1`, `§7.2` and `§7.3` are cited from five task records, from `BRIEF.md` and from §6.2 inside
  the same document. A `§n` is a pointer like any other, and removing the headings would have
  falsified every one of those silently — the check would have caught it, which is the rule working
  on the document that defines it (**L-39**). A pointer subsection is not a second copy.
- **The rules are restated in each document, deliberately, and that is not an L-13 violation** —
  2026-08-13. A standalone document that omits *no observation carries a priority* and *an
  implementation row is not a claim that you do not already know this* is a document that will be
  misread. The operative home for the rule is `R8` §6 and each document cites it; what is repeated
  is the reader-facing consequence, not the rule's justification.
- **Every row was rewritten from the recipient's side, and the content was not changed** —
  2026-08-13. *Their* `T-085` became *your* `T-085`; this repository's ids are named as the reporting
  project's or dropped where they carried nothing; measurements kept their figures. The one exception
  is `O-H4`, which gained a patch section — that belongs to
  [T-142](T-142-fix-o-h4-the-handoff-spine-routes-a-mode-word-with-a-qualifier-to-the-opposite-mode.md)
  and is recorded there rather than smuggled into an extraction.
- **The harness document leads with its scope limit** — 2026-08-13. One machine and two shells is
  enough to correct an attribution and not enough to describe a surface; a reader who takes the first
  paragraph and stops should still have that (**L-75**).
- **The audit shrank by 10,149 bytes** — 44,350 → 34,563, and it is a read-path document that two
  open findings exist to shorten. That was not the reason for the move and it is not claimed as one;
  the bytes went to the three documents rather than away.

**Outputs produced**
- [`../docs/upstream/handoff-skill.md`](../docs/upstream/handoff-skill.md) — `O-H1` to `O-H6`
- [`../docs/upstream/taskmd.md`](../docs/upstream/taskmd.md) — `O-T1` to `O-T6`
- [`../docs/upstream/harness.md`](../docs/upstream/harness.md) — `O-C1`, `O-C2`
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §7 as an index, and §6.2's routing table

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Three documents readable with no knowledge of this repository | met | 7,057 / 7,819 / 3,492 bytes. Each opens with what it is and who wrote it, carries its own *how to read this*, and ends with provenance and an invitation to correct it |
| Every observation appears exactly once, none lost its vintage stamp | met | 6 + 6 + 2 = 14 rows against §7's 14, every one stamped. The harness document states its vintage in the provenance instead of per row, because both rows share it |
| No bare task id | met | *your* `T-085`, `T-087`, `T-063`, `T-028`; *the reporting project's* where one was needed; the rest dropped as meaningless to the reader |
| `§7`, `§7.1`, `§7.2`, `§7.3` still resolve; §6.2 points at the documents | met | `696 section reference(s) resolved, 0 dead` over `1,848 document pointer(s), 0 broken`. §6.2's routing table names `upstream/`, and its *new owner* row now says *a new document* |
| Nothing ranked, banded or prioritised | met | No rank, band, effort or priority in any of the three; each says so in its own words in the first paragraph |
| `python tools/check_all.py` stays green | met | `0 failure(s), 0 unclassified, 0 stale` |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-13 | → done | Fourteen observations into three documents, each standing alone. **§7 keeps all four of its headings and became an index**: `§7`, `§7.1`, `§7.2` and `§7.3` are cited from seven places, and a heading removed is a citation falsified with nothing to say so. The rewrite was from the recipient's side — *your* `T-085`, not *their* — which is the half an extraction usually skips and the half that decides whether the document is readable at all. |
| 2026-08-13 | → in_progress | Built in the planned order. Step 1 paid for itself immediately: the citation sweep is what turned *delete §7* into *reduce §7*. |
| 2026-08-13 | → planned | Six steps, and the first is *find every citation before moving anything*. |
| 2026-08-13 | → specified | Specified in one sitting; the open question it came from had already been argued both ways at the previous handoff, so there was nothing left to decide. |
| 2026-08-13 | → proposed | Raised at the owner's decision, from the open question left by [T-140](T-140-correct-and-extend-the-upstream-register-from-what-implementing-the-audit-found.md). The argument that settled it: a recipient should not have to read an audit of another project to find the three paragraphs addressed to them, and every future observation would land in the same place. |
