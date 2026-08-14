---
id: T-160
title: Correct the three errors the recipients found in the delivered registers
type: admin
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-157, T-141, T-130]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-15
updated: 2026-08-15
deliverables: []
---

# T-160 — Correct the three errors the recipients found in the delivered registers

## 1. Specify

**Outcome**
The two registers [T-157](T-157-hand-the-upstream-registers-to-their-owners.md) delivered are correct
where they are wrong, at the source and on the threads. Both recipients invited corrections on the
terms this register offered — *a row that turns out to be wrong gets corrected here rather than
quietly dropped* — and **three errors are now known**, one found by each recipient and one found here
while reading their replies.

**Why this exists**
A register that promises corrections and does not make them is worse than one that promised nothing.
Two of the three errors are **live misinformation in someone else's backlog**: taskmd is carrying an
item on our word that the version sort is broken here, and it is not. That is the failure mode the
whole *no priority* discipline exists to avoid — an observation that costs the receiving project work
it did not need to do.

**The three errors**

| | What is wrong | Found by | Where the fix goes |
| :--- | :--- | :--- | :--- |
| **1** | **`O-T2` reports the version text-sort as live. It is fixed.** `tools/tasks/lint.py`'s `version_key` sorts on the parsed version and a self-test in the same file asserts `0.10.0` beats `0.5.0`. The row described a real defect and never said it had been repaired, so the recipient read it as outstanding and told us to fix it | here, reading their reply | the register and the thread |
| **2** | **`O-T6` cites the wrong id of theirs.** It points at *their* `T-063` for *an open task at `specified` or later declaring no deliverable*; their `T-063` is the character-count task. The preamble warned that their id could be read as ours and did not guard the harder direction — **a wrong id of theirs resolves to a real task, so it reads as evidence the work is already covered** | taskmd | the register and the thread |
| **3** | **The delivered issue body lost the *before* quote in the O-H4 patch section.** The transformation that replaced the sender-facing banner replaced **every** blockquote in the document, so the quote of the old §4 bullet became a second copy of the report's own banner. The committed document is intact; only what was delivered is wrong | the handoff skill | the thread, and the transformation |

**Scope**
- In: correcting the two register documents under [`../docs/upstream/`](../docs/upstream)
- In: a correction on each thread, since the delivered copy is what the recipient is working from
- In: **auditing the register's remaining cross-references to foreign ids**, which taskmd explicitly
  recommended after finding error 2. `O-T1`, `O-T3`, `O-T5` and `O-T6` all cite ids of theirs
- Out: **acting on their advice to delete the two wrappers.** It does not apply and that is error-adjacent
  rather than an error: the shipped fallback locates the launcher in *the skill directory the harness
  named when it served the skill*, which is available to an agent in a session and not to
  `python tools/tasks/lint.py` run by the gate from any working directory. Worth telling them, because
  an adopter running a tool outside a served skill is a case their fallback does not cover
- Out: re-triaging their verdicts. Five of six and six of seven rows landed; that is their call and it
  is made
- Out: adding new observations. `../docs/CONTEXT-AUDIT.md` §7's standing rule is unchanged, and a row
  added after a handover date is unsent by construction

**Inputs**
- The two threads: `uchimata2/handoff-skill#75` and `uchimata2/taskmd#1`
- [`../docs/upstream/taskmd.md`](../docs/upstream/taskmd.md) and
  [`../docs/upstream/handoff-skill.md`](../docs/upstream/handoff-skill.md) — the sources to correct
- [`../tools/tasks/lint.py`](../tools/tasks/lint.py) — `version_key` and its self-test, the evidence for error 1

**Acceptance criteria**
- [ ] `O-T2` states that the text sort was found and fixed here, with what fixes it, so the recipient
      can close whatever they raised on it
- [ ] `O-T6` cites the right id, or no id, and says which
- [ ] Every remaining foreign id in both registers has been checked against the project it names, and
      the count checked is written down — **a spot check is not an audit**
- [ ] Each thread carries the corrections, so the delivered copy and the source agree
- [ ] The O-H4 section reads correctly wherever the recipient looks at it
- [ ] The transformation that caused error 3 cannot silently do it again

**Open questions**
- **Does the delivered issue body get edited, or corrected in a comment?** Editing makes the artifact
  right for a later reader and quietly rewrites what the recipient replied to; a comment leaves the
  damage visible and the thread honest. **Recommend the comment**, with the missing quote in it — the
  thread is already the record of the exchange, and the recipient reconstructed the rule from
  behaviour rather than being blocked. *The owner answers this, because it edits public content.*

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
| 2026-08-15 | → proposed | Raised from what came back on the two threads T-157 opened. **Three errors, one found by each recipient and one found here**, and two of them are live in someone else's backlog. The one this project found is the worst of the three: `O-T2` reported a defect that had already been repaired, so taskmd's reply tells us to fix something that is fixed. A register that reports a repaired defect as open spends the recipient's attention on nothing, which is the same currency the *no priority* rule was protecting. `s` rather than `xs` because the cross-reference audit is a real pass over two documents, not a lookup. **`PH3` and `admin`**, following T-157: this is not a defect in the published plugin. |
