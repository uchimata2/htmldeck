---
id: T-157
title: Hand the upstream registers to their owners
type: admin
status: proposed
phase: specify
parent: null
blocked_by: [T-153]
related: [T-140, T-141, T-130, T-137]
work_package: PH3
owner: the project owner
business_value: medium
effort: xs
created: 2026-08-14
updated: 2026-08-14
deliverables: []
---

# T-157 — Hand the upstream registers to their owners

## 1. Specify

**Outcome**
The observations this repository collected about tools it uses reach the people who own those tools,
and **what came back is recorded**. The three documents under
[`../docs/upstream/`](../docs/upstream) stop being a register that is filling and become a register
that was sent, with a date, a route and a response against each owner.

**Why this exists**
[`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §7 held everything back on a condition — *nothing
is sent until the audit's findings are worked and their fixes land* — because four out of four
implementation sessions had added rows, and sending early would mean sending three times. **The
condition is met.** The owner set the moment on 2026-08-14: after phase 2, before
[T-137](T-137-package-the-context-economy-method-as-a-skill.md).

**And the act had no home, which is why this exists as a task rather than as a step.** §7 says the
handover is *"one deliberate act, later, and not a step in anyone's task"* — written when it had no
schedule. A scheduled act with no task file has nowhere to put what it produces: who was told, by what
route, on what date, and what they said. **The rows are the input; the responses are the output, and
they were homeless.**

**Scope**
- In: sending [`../docs/upstream/handoff-skill.md`](../docs/upstream/handoff-skill.md) and
  [`../docs/upstream/taskmd.md`](../docs/upstream/taskmd.md) to their owners — the two the owner named.
- In: **recording the route, the date and the response** against each document.
- In: a decision on [`../docs/upstream/harness.md`](../docs/upstream/harness.md) — see the open
  question. It is the third document and it was not named.
- In: updating §7 from *nothing has been sent* to what was actually sent, since that paragraph is the
  operative statement and will otherwise be false the moment this task closes.
- Out: **implementing anything for them.** The register's own rule is that an observation carries no
  priority, because that is a guess about someone else's project.
- Out: re-reading anyone's backlog. The *audit* rows were written with it read; the *implementation*
  rows were not, and each is stamped so the recipient can tell.
- Out: adding new observations. A session that finds one adds it to the owner's document — that is §7's
  standing rule and it does not stop when this task closes.

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §7 — the rules that travel with the rows, the
  hold, and the 2026-08-14 ruling that set the moment. Read before starting
- The three documents under [`../docs/upstream/`](../docs/upstream)
- [T-141](T-141-extract-the-upstream-register-into-one-document-per-owner.md) — why there is one
  document per owner, and what each was written to stand alone as

**Acceptance criteria**
- [ ] Each document that is sent records **route, date and response** — including *no response yet*
- [ ] `../docs/CONTEXT-AUDIT.md` §7's *nothing has been sent* paragraph states what was sent instead
- [ ] No observation acquired a priority, a severity or a deadline on the way out
- [ ] The *audit* / *implementation* stamps survive the handover, so a recipient can tell which rows
      were written with their backlog read
- [ ] `harness.md` is sent, or its lack of a route is written down as a result

**Open questions**
- **Does `harness.md` go, and by what route?** The owner named the handoff skill and taskmd. The third
  document's owner is a vendor rather than a person with an issue tracker, and **an observation with no
  route is not the same as one withheld** — the difference has to be recorded either way. Recommended:
  send the two named, and record for `harness.md` that no route was identified, which leaves it
  findable rather than dropped. — the owner.

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
| 2026-08-14 | → proposed | Raised at the owner's direction, settling the open point `CONTEXT-AUDIT.md` §7 recorded the same day. The 2026-08-13 hold had a condition and no moment; the owner supplied the moment — **after phase 2, before T-137** — and a scheduled act with no task file has nowhere to record what it produces. `blocked_by: T-153`, because phase 2 is the session most likely to add rows and sending before it would mean sending twice, which is the argument the hold rests on. `xs`, `PH3` because PH2 has shipped and this is not a defect in the published plugin. |
