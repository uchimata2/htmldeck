---
id: T-258
title: Report a readability measurement over drawn slide copy, and name the hardest lines
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-225]
work_package: PH3
owner: the project owner
business_value: high
effort: m
created: 2026-08-29
updated: 2026-08-29
deliverables: []
---

# T-258 — Report a readability measurement over drawn slide copy, and name the hardest lines

## 1. Specify

**Outcome**
An author learns from the gate that copy is hard to read. Today the two rules over copy measure **length** (`DS-092`) and a **banned list** (`DS-106`), both were green on a deck its own author called difficult, and the difficulty was vocabulary, noun stacks and abstraction. Measured afterwards with an instrument the adopter had to write: Flesch 64.6, Fog 10.3, **18% three-syllable words and 129 nominalisations** — and no rule looks at either.

**From the adopter report** [`025`](../docs/adopter-reports/claimai/025-the-gate-passes-copy-its-own-reader-calls-difficult.md).

**Scope**
- In: a readability verdict over drawn slide copy — Flesch, Fog and a three-syllable share, standard library, reading the deck's own text nodes
- In: **reporting rather than gating.** A threshold on prose invites writing to the threshold, and the adopter's own record is that the numbers *located* the hard lines and did not judge them
- In: **saying what a green copy run means.** The gate already says a clean run is never *reads as human-written*; it should say the same about *reads easily*
- Out: anything the records above do not name. The report is a closed one-way hand-over — there is no
  channel back and none is expected, so a question this task cannot answer is settled here rather
  than asked.

**Inputs**
- the record above, [`025`](../docs/adopter-reports/claimai/025-the-gate-passes-copy-its-own-reader-calls-difficult.md) — each carries its evidence, its version and its own proposed fix
- the record's second half — six AI tells `DS-106` does not gate (rule-of-three cadence, negative parallelism, superficial `-ing` analyses, vague attribution, em-dash overuse, reflex bullet lists), read by hand once. **That half is [T-229](T-229-ds-106s-check-omits-a-word-the-rule-names.md)'s**, which already proposes deriving the fallback list from the rule's own row
- `DS-107`, which is where a category nobody has built yet is recorded

**Acceptance criteria**
- [ ] every record named above is **closed with its remedy measured**, or explicitly deferred with the
      reason recorded in this task
- [ ] each fix is proved by seeding the defect and watching the check fire, in both directions where
      the record's own evidence is a verdict (**L-125**)
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None yet. Every record carries its own evidence and its own proposed fix; the proposal is a
  hypothesis and whoever implements it measures before committing to it.

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
| 2026-08-29 | → proposed | Raised by [T-225](T-225-triage-the-claimai-adopter-report.md), the triage of the ClaimAI adopter report. **`PH3`**: not a defect in the published plugin's behaviour, so `CLAUDE.md`'s rule puts it in the main line rather than reopening a shipped phase. |
