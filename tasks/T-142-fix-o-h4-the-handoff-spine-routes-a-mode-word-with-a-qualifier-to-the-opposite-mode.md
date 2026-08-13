---
id: T-142
title: Fix O-H4 — the handoff spine routes a mode word with a qualifier to the opposite mode
type: fix
status: done
phase: review
shipped_in: unreleased
parent: null
blocked_by: []
related: [T-140, T-141]
work_package: PH3
owner: the project owner
business_value: medium
effort: xs
created: 2026-08-13
updated: 2026-08-13
deliverables:
  - docs/upstream/handoff-skill.md
---

# T-142 — Fix O-H4 — the handoff spine routes a mode word with a qualifier to the opposite mode

## 1. Specify

**Outcome**
`handoff resume, full lifecycle` selects **Resume** and treats the rest as an instruction for that
run, and the fix reaches the repository that owns the skill rather than only the copy installed here.

**The defect**
The spine's §4 *Explicit invocation and its argument* said trailing text that **is just a mode word**
selects that mode, and that **otherwise the whole argument is the subject of a handoff to create**. A
parenthesis then granted `create <text>` the mode-plus-subject reading and explicitly denied it to
`resume` / `status` / `close`. So a mode word with a qualifier after it — ordinary phrasing — selected
Create and recorded the user's own words as the next session's task. It happened here on 2026-08-13;
Resume was obviously meant and Resume was run, by reading intent against the written rule.

**Why this project fixes it at all**
The skill's author is this project's owner, and an adopter's report normally stops at the
observation ([`../docs/upstream/handoff-skill.md`](../docs/upstream/handoff-skill.md), `O-H4`). The
fix was directed 2026-08-13. **The installed copy is not a repository** — it is an unversioned
install under the user profile — so editing it makes the behaviour right today and reaches nothing
else. The patch therefore has to exist as text in a place the owner keeps.

**Scope**
- In: the corrected rule, applied to the installed copy so the behaviour is right now.
- In: the same change written out in the observation document, precisely enough to apply to the
  source, and with the one part worth arguing about named as such.
- In: saying in that document that the installed copy is not the source and why that matters.
- Out: any other section of the spine, either flow file, or the bindings. One rule, one fix.
- Out: treating the installed copy as the fix. It will be overwritten by the next install, and a
  change that survives only in an unversioned directory is not a change.
- Out: rewriting `O-H4` to read as though it were never a defect. The observation stays, with the
  fix attached to it.

**Inputs**
- [`../docs/upstream/handoff-skill.md`](../docs/upstream/handoff-skill.md) — `O-H4` as reported
- The skill's own §4 ambiguity rule, which already prefers asking over guessing for a bare *wrap up*

**Acceptance criteria**
- [ ] A leading mode word selects its mode whatever follows it, and the three non-`create` modes have
      a stated meaning for the remainder
- [ ] The genuinely ambiguous phrasing — a qualifier that describes work for a *later* session — is
      resolved by asking, not by a rule that has to guess
- [ ] The old behaviour is recorded where the change is, so a reader can see what was wrong rather
      than only what is right
- [ ] The patch is applicable to the source repository by someone who has only the document

**Open questions**
- None.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Re-read §4 and find where the asymmetry actually is | It is the parenthesis, not the bullet |
| 2 | Rewrite the rule as three cases keyed on the leading word, plus an ask for the one that is genuinely ambiguous | The corrected §4 |
| 3 | Apply it to the installed copy, and date the correction inside the text | Right behaviour today |
| 4 | Write the patch and its argument into the observation document, flagging the debatable part | A fix that can reach the source |

## 3. Implement

**Decisions & assumptions**
- **A leading mode word wins, and the remainder's meaning depends on which mode it opened** —
  2026-08-13. After `create` it is a subject, because Create writes a handoff about future work.
  After `resume` / `status` / `close` it is a qualifier on this run, because those act on a handoff
  that already exists and have no subject to take. The old rule had the `create` half right and had
  no path at all for the other three.
- **The one ambiguous case is resolved by asking, and that is the debatable part** — 2026-08-13.
  `resume the migration next week` fits both readings honestly. Adding a question puts a prompt where
  the flow currently never asks; the simpler alternative — always a qualifier — is cleaner and wrong
  about a real phrasing. §4 already asks rather than guesses when a bare *wrap up* is ambiguous, so
  the precedent is the section's own. **Flagged in the document as the part to argue with**, rather
  than presented as settled.
- **The correction is dated inside the spine text** — 2026-08-13, and it states the old rule. A
  reader of a changed rule cannot tell a fix from a preference unless the thing it replaced is
  visible.
- **The installed copy was edited and that is not the deliverable.** It is unversioned and under the
  user profile; the next install overwrites it. The deliverable is the patch text, which is why this
  task's only declared output is in this repository.

**Outputs produced**
- [`../docs/upstream/handoff-skill.md`](../docs/upstream/handoff-skill.md) — *The O-H4 patch, as
  applied here*, and the note that the installed copy is not the source
- The installed skill's `handoff.core.md` §4 — corrected, outside this repository and not tracked
  by it

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A leading mode word selects its mode whatever follows it, and the non-`create` modes have a stated meaning for the remainder | met | Three bullets keyed on the leading word: subject after `create`, qualifier after the other three, subject when there is no mode word at all |
| The genuinely ambiguous phrasing is resolved by asking | met | A named case — text describing work for a later session — with the instruction to ask, and the §4 precedent cited |
| The old behaviour is recorded where the change is | met | A dated paragraph inside §4 quoting what the rule said and what it did to `resume, full lifecycle` |
| The patch is applicable by someone who has only the document | met | The document quotes the sentence being replaced, names the parenthesis as the actual fault, and lists the four numbered changes. **Not verified by anyone applying it** — that is the owner's repository and no clone of it was available |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-13 | → done | The asymmetry was in a parenthesis, not in the rule everyone reads: `create <text>` already meant mode-plus-subject, and the same reading was explicitly denied to the other three modes. Fixed as three cases plus one question. **The installed copy is not the source and the patch is the deliverable** — an unversioned directory under a user profile is not where a fix lives, and the next install would take it back. |
| 2026-08-13 | → in_progress | Applied to the installed copy so the behaviour is right today, and written out for the source. |
| 2026-08-13 | → planned | Four steps. Step 1 is *find where the asymmetry actually is*, because the reported symptom pointed at the bullet and the fault was in the clause after it. |
| 2026-08-13 | → specified | Raised and specified at the owner's direction, from `O-H4` in the document [T-141](T-141-extract-the-upstream-register-into-one-document-per-owner.md) had just created. Normally an adopter's report stops at the observation; this one is fixed because the owner of the skill directed it. |
| 2026-08-13 | → proposed | Created. |
