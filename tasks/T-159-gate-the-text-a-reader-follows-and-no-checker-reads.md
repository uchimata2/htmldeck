---
id: T-159
title: Gate the text a reader follows and no checker reads
type: fix
status: proposed
phase: specify
parent: T-130
blocked_by: []
related: [T-130, T-146, T-147, T-149, T-153]
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-08-14
updated: 2026-08-14
deliverables: []
---

# T-159 — Gate the text a reader follows and no checker reads

## 1. Specify

**Outcome**
The class of defect that every gate here is blind to by construction becomes visible: text that a
reader acts on, sitting beside a pointer that resolves. **A link whose target is right and whose words
are wrong passes every check in this repository**, and so does a bare `§n` left behind by an
extraction.

**Why it exists**
Raised at [T-153](T-153-run-the-audit-methods-phase-2-over-this-repositorys-own-audit.md)'s review,
2026-08-14, from [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §10.3. Phase 2 read the
byproduct register for a shape rather than row by row — which is `R8` §6.3's new instruction — and
**six of the eight defects found in passing turned out to be one class.** No single row could show
that; each looked like a small unrelated defect at the time it was recorded.

**The six, and what each one is.**

| Found by | The instance |
| :--- | :--- |
| T-146 | A link **label** showing a one-level path beside a target carrying the new two-level one. The link works; the words beside it are wrong from the new depth, and **no checker reads a label** |
| T-146 | A citation of an `L-nn` that was never allocated — invisible to every gate in the repository until `lessons.py` existed |
| T-147 | Three internal cross-references — *(§6.1)*, *(§3)*, *"the headings in this document"* — left pointing at the host after the text moved. **A bare `§n` is not bound to a document**, so `refcheck.py` counts it unbound and skips it, correctly by its own rule |
| T-149 | Three dangling `[[link]]`s in the memory store, **one a typo for an entry that exists**. Nothing checks these and nothing here can — the store is outside the tree |
| T-144 | A survey that named a document which had never stated the rule it was surveying |
| T-152 | A survey that **missed a copy sitting in the file the rule was being cut out of** |

**The mechanism they share.** Every one is a statement a reader follows, whose correctness is not a
property any pointer-resolver can test. `refcheck.py` proves a target exists; it cannot prove the
sentence beside the target is true. **The last two are the same failure at a different altitude** — a
survey is prose about what the repository contains, and it goes stale the moment the repository moves
(**L-96**).

**Scope**
- In: deciding **which of the six are mechanically decidable** and which are irreducibly a person's.
  A bare `§n` in a file that moved is arithmetic. A link label that lies is close to arithmetic — the
  label and the target are both in the same string. A survey that missed a copy is not.
- In: the decidable subset, gated on a trigger that already runs.
- In: **a written refusal for the rest**, naming why. `R8` §10's limits are the precedent and this
  project has refused gates before with reasons that outlived the refusal
  ([T-139](T-139-two-rows-in-brief-md-carry-a-cell-the-table-cannot-render.md) is one).
- Out: the memory store. It is outside the tree, `CLAUDE.md` forbids the repository to carry its
  paths, and T-149 already established nothing here can reach it.
- Out: widening `refcheck.py`'s adjacency rule. That rule is correct and T-147 confirmed it; the gap
  is not that it is wrong but that nothing else covers what it deliberately skips.

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §10.3 — the eight, and the six that are one
  class
- [`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
  §6.3 — *read the register for a shape*, which is the instruction that produced this task
- T-146 §3 and T-147 §3 — the two extractions where the class was first seen, one each
- **L-96** on a survey being evidence about the day it was taken, **L-62** on the instrument that
  produced a change not being the one that clears it

**Acceptance criteria**
- [ ] Each of the six is classified **decidable** or **a person's**, with the reason
- [ ] The decidable subset fails on seeded instances, in each direction, demonstrated rather than
      asserted (**L-86**)
- [ ] The self-test builds synthetic fixtures and does not assert the current state of a tracked file
      (**L-78**, **L-85**)
- [ ] Anything refused has its refusal written where the next person meets the question, not only here
- [ ] No existing gate's rule is widened to cover this — a new check or none (`refcheck.py`'s
      adjacency rule is correct and stays)
- [ ] `python tools/check_all.py` green, and any new tool named in exactly one of its four tables

**Open questions**
- **Is the link-label case worth a gate on its own?** It is the most mechanical of the six — label and
  target sit in one string — and it is also the only one that has bitten twice. Recommended: yes, and
  size the rest against it, because a check that decides one instance cleanly is worth more than one
  that half-decides four. — the implementer, at `plan`, after the classification in step 1.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <none yet>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-14 | → proposed | Raised at the owner's acceptance on T-153's review. **Not a `CE-nn`** — the ranking closed at thirteen and phase 2 raises ordinary tasks, which is §1's Out scope in T-153. The evidence is that **six of eight byproducts are one class**, which no individual row could show and which only appeared once `R8` §6.3's *read the register for a shape* was applied. `m`, because the classification is most of the work and the gate may turn out to cover one instance rather than six. `PH3` because PH2 has shipped and this is not a defect in the published plugin. |
