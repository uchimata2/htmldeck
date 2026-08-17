---
id: T-157
title: Hand the upstream registers to their owners
type: admin
status: done
phase: review
parent: null
blocked_by: []
related: [T-140, T-141, T-130, T-137]
work_package: PH3
owner: the project owner
business_value: medium
effort: xs
created: 2026-08-14
updated: 2026-08-14
shipped_in: 0.3.0
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
- In: recording, against [`../docs/upstream/harness.md`](../docs/upstream/harness.md), that **no route
  was identified** and what would change that. **Settled 2026-08-14** — it is not sent, and it is not
  withheld.
- In: updating §7 from *nothing has been sent* to what was actually sent, since that paragraph is the
  operative statement and will otherwise be false the moment this task closes.
- Out: **implementing anything for them.** The register's own rule is that an observation carries no
  priority, because that is a guess about someone else's project.
- Out: re-reading anyone's backlog. The *audit* rows were written with it read; the *implementation*
  rows were not, and each is stamped so the recipient can tell.
- Out: adding new observations. A session that finds one adds it to the owner's document — that is §7's
  standing rule and it does not stop when this task closes.
  > **Superseded 2026-08-15 by [T-164](T-164-retire-the-cross-repo-register-in-favour-of-a-branch.md).**
  > The standing rule this bullet relies on is retired: a session that finds a defect in one of the
  > owner's other projects now fixes it there, as a branch with a failing test and a three-line pull
  > request, and adds nothing to any register. The bullet is left standing because it describes what
  > this task was scoped against.

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
- [ ] `harness.md` records that no route was identified, and **what would change that** — so it reads
      as pending rather than as sent or as dropped

**Open questions**
- ~~**Does `harness.md` go, and by what route?**~~ **Settled by the owner 2026-08-14: send the two
  named — the handoff skill and taskmd — and record for
  [`../docs/upstream/harness.md`](../docs/upstream/harness.md) that no route was identified.**

  **The recording is the deliverable for that document, not a consolation for one.** An observation
  with no route and an observation withheld look identical from outside, and only one of them is
  waiting for something. Write which it is, and what would change it — a vendor channel, an issue
  tracker, a support path — so a later session can send it without re-deciding whether it should be
  sent. **Do not leave `harness.md` looking sent, and do not leave it looking rejected.**

## 2. Plan

**The route is settled: one GitHub issue per register, on the owner's own repositories.** Ruled by
the owner 2026-08-14, from three candidates — an issue, a file committed into the receiving repository,
or a direct handover with no outward action. The issue wins on the one thing the outcome asks for:
*what came back* needs somewhere to land, and only a thread has one. The documents were already
written for it — they cite the receiving projects' issue numbers and invite corrections.

**The response is recorded as handed over rather than waited for.** Also the owner's ruling: the
sending is done on this side, and a reply is the receiving project's business, not this task's. So
this task closes on delivery, not on an answer.

**Two things the route changes that sending did not obviously imply.** A register's relative links
resolve inside this repository and nowhere else, so an issue body needs them absolute or it arrives
broken. And an issue is a notification only to whoever watches the repository — the owner asked for a
**copy-paste prompt per project**, so a session started in the receiving repository can pick the work
up without any of this context.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Build an issue body per register: the document as it stands, with every repository-relative link rewritten to an absolute `github.com/uchimata2/htmldeck` URL. The committed copies keep their relative links | Two issue bodies that resolve from another repository |
| 2 | Create one issue on `uchimata2/handoff-skill` and one on `uchimata2/taskmd`, titled as an adopter's report rather than as a request, so the title does not smuggle in the priority the rows refuse to carry | Two issue URLs |
| 3 | Add a **Handover record** to all three documents — route, date, response. `harness.md`'s says *no route identified* and what would change that, in the same shape, so it reads as pending rather than as sent or dropped | Three documents that state their own disposition |
| 4 | Replace `../docs/CONTEXT-AUDIT.md` §7's *nothing has been sent* with what was sent, and correct §7.1's `O-H1` to `O-H6` — `O-H7` was added after that line was written | §7 true at the moment this task closes |
| 5 | Write one copy-paste prompt per receiving project, naming the issue and what to do with it, and carrying the *no priority* rule across so it survives the trip | Prompts in §3, and handed to the owner |
| 6 | Gates and commit | `lint`, `check_all`, one commit |

## 3. Implement

**Decisions & assumptions**
- **The issue body is the document with its links made absolute, and nothing else changed** — 2026-08-14.
  A register's relative links resolve inside this repository and nowhere else, so an issue carrying them
  arrives broken. The committed copies keep their relative form; the rewrite happens on the way out, by a
  throwaway script that asserts no `../` survives. The rows are byte-identical either side.
- **The "ready to send" banner was replaced for the recipient, not deleted** — 2026-08-14. A banner that
  says *ready to send* is addressed to the sender and reads as pre-delivery once it has arrived. The issue
  opens instead with what the reader needs: this is a report, nothing is ranked, no answer is being waited
  on.
- **The issue titles state the disclaimer** — 2026-08-14. *"Adopter report … no priorities attached"*. A
  title is the one line every recipient reads, and a title like *observations to address* would smuggle
  back exactly the priority the rows refuse to carry.
- **A row added after a document's handover date is unsent, and nothing marks it so** — 2026-08-14, and
  it is this task's ruling because sending created the question. The handover record carries a date and a
  row carries a position; the two answer it between them, and a per-row send-state would be a second
  register to keep in step (**L-13**). Written into `../docs/CONTEXT-AUDIT.md` §7, where the standing rule
  already lives.
- **`harness.md`'s record is written in the same shape as the two that went** — 2026-08-14. Route, what
  would change it, response. A document whose disposition is recorded in a different form from its
  siblings invites the reader to conclude it was forgotten, which is the exact misreading §1 raised.

**Outputs produced**
- [`uchimata2/handoff-skill#75`](https://github.com/uchimata2/handoff-skill/issues/75) — `O-H1` to `O-H7`
- [`uchimata2/taskmd#1`](https://github.com/uchimata2/taskmd/issues/1) — `O-T1` to `O-T6`
- A handover record in each of the three documents under [`../docs/upstream/`](../docs/upstream), two
  *sent* and one *no route identified*
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §7 — *nothing has been sent* replaced by what was
  sent; §7.1's row range corrected from `O-H6` to `O-H7`; the spent scheduling argument compressed to one
  line
- The two handover prompts below

**The handover prompts.** An issue notifies whoever watches the repository and nobody else, so each
receiving project gets a prompt that starts a session there with no access to any of this context. They
carry the *no priority* rule across, because that rule is the one most likely to be lost in transit — a
report that arrives without it reads as a list of demands.

For the handoff skill:

```text
Read https://github.com/uchimata2/handoff-skill/issues/75 — an adopter report from the htmldeck
project. Seven observations about this skill, from about a week of daily use in one repository.

Treat it as evidence, not as a backlog. Nothing in it is ranked and nothing is a request: the
reporter assigned no priority on purpose, because that would be a guess about this project. What
each row is worth is our call, and making that call is the job.

Two things that are easy to skim past. Every row is stamped audit or implementation — the audit
rows were written with our open issues and PROJECT_BOARD.md read first, the implementation rows
were not. Read an implementation row as "this was observed", never as "this is not already known".
And any T-nnn in it is htmldeck's id; it will collide with our numbering if quoted bare.

For each row, decide three things: is it real here, does an existing issue already cover it, and
does this project want to do anything about it. Raise what survives as our own issues, in our own
words. O-H4 carries a proposed patch to handoff.core.md §4 that the reporter already applied to
their installed copy — check it against the source before adopting it, since that copy is not ours.

Reply on the thread if anything is worth telling them, including "already knew that". They are not
waiting on an answer.
```

For taskmd:

```text
Read https://github.com/uchimata2/taskmd/issues/1 — an adopter report from the htmldeck project.
Six observations from a repository tracking 141 tasks, on version 0.5.0.

Treat it as evidence, not as a backlog. Nothing in it is ranked and nothing is a request: the
reporter assigned no priority on purpose, because that would be a guess about this project. What
each row is worth is our call, and making that call is the job.

Three things that are easy to skim past. Every row is stamped audit or implementation — the audit
rows were written with our backlog read first, 138 task files and the 8 then open; the
implementation rows were not, so read one as "this was observed", never as "this is not already
known". Ids collide in both directions: a T-nnn marked as ours is ours, one marked as the
reporting project's is htmldeck's. And O-T2 is a correction of an earlier row that blamed us for a
defect that turned out to be the harness's — what is left of it is small and specific, so read the
row rather than its opening clause.

For each row, decide three things: is it real here, does an existing task already cover it, and
does this project want to do anything about it. O-T1 asks for nothing — it says we settled the
question first and the adopter should follow us. Raise what survives as our own tasks, in our own
words.

Reply on the thread if anything is worth telling them, including "already knew that". They are not
waiting on an answer.
```

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Each document that is sent records **route, date and response** | met | Both carry a **Handover record** banner: route as the issue it went to, date `2026-08-14`, response as **handed over — no answer is being waited on**. That last form is the owner's ruling and is stronger than the *no response yet* the criterion allowed for: the register is not parked on a reply, so nothing has to come back for this to be complete. |
| §7's *nothing has been sent* paragraph states what was sent instead | met | Replaced by what went, by what route, and why that route was chosen over the two rivals. `harness.md`'s non-sending is stated in the same paragraph, so §7 is not silently about two documents out of three. |
| No observation acquired a priority, a severity or a deadline on the way out | met | Measured rather than asserted: the observation rows in each issue body are **byte-identical** to the committed document — 7 rows and 6 rows, `a == c` — and carry none of `urgent`, `severity`, `deadline`, `high priority`, `must fix`, `asap`. The titles disclaim it out loud: *"…no priorities attached"*. |
| The *audit* / *implementation* stamps survive the handover | met | Counted in the delivered bodies: **3 audit and 4 implementation** for the handoff skill, **3 and 3** for taskmd. Both prompts restate what the stamp means, since the stamp is worthless to a reader who does not know an *implementation* row had no backlog re-read. |
| `harness.md` records that no route was identified, and **what would change that** | met | Its record names the three things that would change it and adds the part §1 asked for in substance: **the question of whether it should be sent is settled and the answer is yes**, so a later session supplies a route and sends, rather than re-opening the decision. |

**What the criteria did not ask for, and the owner did**
The owner added one requirement at the route decision: an issue notifies a watcher and nobody else, so
each receiving project needs **a prompt that starts a session there cold**. Two are in §3. They were
written to carry the *no priority* rule across, because it is the rule most likely to be lost in
transit — a report that arrives without it reads as a list of demands, which is precisely what the
register spent seven months of rows refusing to be.

**One thing worth saying plainly.** This task sent observations to two repositories the owner also
owns. That made the route cheap, and it makes the *response* half of the outcome softer than it looks:
the reply will come from the same person who commissioned the report. The rows are still worth
sending — a written register read in the receiving project's own context is not the same artifact as a
memory of having noticed something — but *what came back* will not be an independent signal, and
nothing here should later be cited as though it were.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-15 | (response) | **Both recipients triaged within hours, and the *handed over rather than waited for* ruling is what let this task close before any of it arrived.** Six of seven rows landed at the handoff skill and five of six at taskmd; none was wrong. **`O-T4` repaid the whole report** — the scan it prompted found one table row wider than its header in 2,797, in the task that answered `O-T2`, silently destroying a record since 2026-08-10. The responses are recorded in the two documents, which own that field; the reasoning stays on the threads. **Three errors came back and are [T-160](T-160-correct-the-three-errors-the-recipients-found-in-the-delivered-registers.md)**, one of them this task's own delivery defect — the banner replacement matched every blockquote and overwrote a quotation, which §4's byte-identical row could not see because it compared the rows and the damage was not in the rows (**L-102**). |
| 2026-08-14 | → done | **Sent.** Two issues, [`handoff-skill#75`](https://github.com/uchimata2/handoff-skill/issues/75) and [`taskmd#1`](https://github.com/uchimata2/taskmd/issues/1); `harness.md` recorded as *no route identified*. All five criteria met, one of them measurably: the observation rows in each issue body are byte-identical to the committed documents, and the *audit* / *implementation* stamps came through 3+4 and 3+3. **Two defects were found by delivering rather than by any gate** — repository-relative links resolve nowhere else, and a *ready to send* banner is addressed to the sender and false on arrival. That is **L-101**, and it is the closing checklist's *look at what rendered* rule earning its keep on a text file. |
| 2026-08-14 | → planned | **The owner set the route: one GitHub issue per register, on their own repositories**, chosen over committing a file into each receiving repository and over a direct handover with no outward action. The deciding property is that *what came back* needs a home and only a thread has one. **The response is recorded as handed over rather than waited for** — the sending is complete on this side, and a reply is the receiving project's business. Two consequences the route carries that the act did not: relative links must be absolute in an issue body, and an issue notifies only a watcher, so the owner asked for a copy-paste prompt per project. |
| 2026-08-14 | (unblocked) | **`T-153` closed and phase 2 added no upstream rows**, which is the condition the hold rested on rather than a lucky outcome — the argument was that a review of what the findings bought is the session most likely to add rows. `blocked_by` is empty and this task is runnable. What it sends is unchanged: the three documents under `../docs/upstream/` are as T-141 left them. |
| 2026-08-14 | → specified | The one open question is settled by the owner: **send the two named, and record for `harness.md` that no route was identified.** The recording is that document's deliverable rather than a consolation — *no route found* and *withheld* are indistinguishable from outside, and only one of them is waiting for something. Struck rather than deleted, per §1. |
| 2026-08-14 | → proposed | Raised at the owner's direction, settling the open point `CONTEXT-AUDIT.md` §7 recorded the same day. The 2026-08-13 hold had a condition and no moment; the owner supplied the moment — **after phase 2, before T-137** — and a scheduled act with no task file has nowhere to record what it produces. `blocked_by: T-153`, because phase 2 is the session most likely to add rows and sending before it would mean sending twice, which is the argument the hold rests on. `xs`, `PH3` because PH2 has shipped and this is not a defect in the published plugin. |
