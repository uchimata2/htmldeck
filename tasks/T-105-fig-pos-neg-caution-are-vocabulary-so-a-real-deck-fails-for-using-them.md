---
id: T-105
title: The figure's pos, neg and caution roles are vocabulary, so the first deck to use them fails component.py
type: admin
status: done
phase: review
shipped_in: unreleased
parent: null
blocked_by: []
related: [T-092]
work_package: PH1
owner: the project owner
business_value: medium
effort: xs
created: 2026-08-12
updated: 2026-08-12
deliverables:
  - docs/COMPONENT-CONTRACT.md
---

# T-105 — The figure's pos, neg and caution roles are vocabulary, so the first deck to use them fails component.py

## 1. Specify

**Where this came from.** The adopting project, re-authoring its deck on v0.2.1. It is `N-9` in that
project's feedback document. **Filed as feedback, not as a defect** — the classification is documented
behaviour working exactly as written.

**What happens.** `COMPONENT-CONTRACT.md` §3.6 lists `.fig .pos`, `.fig .neg` and `.fig .caution` with
source `vocabulary` and count `0+`. A deck that draws a red mark inside a figure — the ordinary way to
show a loss — uses the contract's own class and **fails `component.py` for it**, because `vocabulary`
rows are ones the contract defines and a deck is not expected to author.

## Why it is worth a task rather than a shrug

§3.6 anticipated this in writing:

> a figure encoding a loss is the obvious next deck, which is why the rows stay

**That deck has now been built.** The anticipated case arrived, and the classification that was
correct while it was hypothetical is the thing standing in its way. The adopter's deck encodes a
shortfall in a figure and has to choose between drawing it correctly and passing the gate.

**Still present at `master`:** all three rows read `vocabulary` with count `0+`.

## The need

Move the three rows from `vocabulary` to `author`, keeping `0+`. The count is already right; only the
source column is describing the world as it was before any deck used them.

**Scope**
- In: the three `.fig` role rows in §3.6, and whatever `component.py` derives from the source column.
- In: checking whether any other `vocabulary` row is in the same position — a role the contract
  defines for a deck to use, classified as one the contract owns.
- Out: the `.ledger .pos` rows, which are a different rule and are used by the reference deck as
  intended.

**Acceptance criteria**
- [ ] A deck using `.fig .pos`, `.fig .neg` or `.fig .caution` passes `component.py`
- [ ] The reference deck's own use of `.ledger .pos` is unaffected
- [ ] Any other row in the same position is named, or it is recorded that none is

**Open questions**
- none.

## 2. Plan

**Phase: `PH1`, against the filer's classification, and the owner ruled on it.** Filed as feedback
because §3.6 behaves as documented. But a published gate fails a deck for using classes the contract
defines, which is what an adopter meets, and a check that forbids a legal design choice is a defect
in the check. The effect is identical to T-102's, which nobody filed as feedback.

| # | Step | Where |
| :--- | :--- | :--- |
| 1 | Move the three `.fig` role rows to `author`, keeping `0+` | `COMPONENT-CONTRACT.md` §3.6 |
| 2 | Examine every other `vocabulary` row for the same position | §3.6, §3.7 |
| 3 | Rewrite the two notes that explain the classification | §2.1, §3.6, §3.7 |
| 4 | Confirm the reference deck's `.ledger .pos` is untouched | `component.py` |

**Nothing in `component.py` needs changing.** It reads the source column out of the document, which
is the design working: the row moves and the check follows.

## 3. Implement

**All five `vocabulary` rows moved, not three.** Step 2's sweep is the reason, and it is the finding
worth more than the fix:

| Row | In | Same position? |
| :--- | :--- | :--- |
| `.pos` `.neg` `.caution` | `.fig` | Yes — the deck §3.6 predicted arrived |
| `.t-ink` | `.fig` | **Yes.** The sibling of five `author` text roles (`.t-accent`, `.t-soft`, `.t-faint`, `.t-paper`, `.t-caution`), styled `.fig text.t-ink{fill:var(--ink)}`. The next deck to colour figure text explicitly fails for it |
| `.mono` | — | **Yes.** §3.7 called it *the same treatment as a standalone utility*, which is a description of a class a deck may write. A deck needing a mono run fails for it |

**So the source was empty of anything it was for.** Every row carrying `vocabulary` turned out to be
a class this contract defines *for a deck to use* — the classification was a true statement about the
reference deck being enforced against everybody else's.

**The source stays defined, with no members.** It is still the right answer for a class the shared
block styles that a deck must **not** author; §2.1 now says a row earns it by being that, never by
being unused so far. The fifth verdict reads `0 declared, 0 now in the deck`, which is honest — the
claim it makes is about rows that exist, and none does.

**The `.ledger .pos` case is protected by machinery that was already there.** `is_scoped()` derives
*meaningless outside its part* from the CSS: `.pos` is styled only as `.fig .pos`, so a `<b
class="pos">` in a ledger is a different class `#slides` owns. Its docstring names this exact case.

## 4. Review

| Criterion | Verdict | Evidence |
| :--- | :--- | :--- |
| A deck using `.fig .pos`, `.fig .neg` or `.fig .caution` passes `component.py` | **met** | The reference deck with a `.pos` seeded inside a `.fig`: all five rows pass, where the same deck failed row 5 before |
| The reference deck's own use of `.ledger .pos` is unaffected | **met** | Both example decks: five rows pass, `0 problem(s)` on placement. 82 authored parts, up from 77 |
| Any other row in the same position is named, or it is recorded that none is | **met** | The table in §3 names both, with the evidence for each. Both moved |

**Moving `.t-ink` and `.mono` is beyond the acceptance criteria**, which asked only that they be
named. Recorded here as the deviation it is: leaving them would have shipped two known instances of
the defect this task fixes, and the argument that closed them is the same argument in the same
words.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-12 | → proposed | Filed from the adopting project's feedback document, `N-9`. Kept as feedback: §3.6 says what it does and says why, and the only thing that changed is that the deck it was waiting for exists. Re-verified against §3.6 on `master` before filing. |
| 2026-08-12 | → done | Phase set to `PH1` by the owner, against the filer's *feedback* classification: a published gate failing a deck for using a documented class is a defect in the check. The sweep the criteria asked for found `.t-ink` and `.mono` in the same position, so all five rows moved and the `vocabulary` source now has no members. |
