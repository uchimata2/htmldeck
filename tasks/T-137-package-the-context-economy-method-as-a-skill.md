---
id: T-137
title: Package the context-economy method as a skill
type: deliverable
status: proposed
phase: specify
parent: T-130
blocked_by: [T-136]
related: [T-130, T-131, T-132, T-133, T-135, T-136, T-139, T-140]
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-08-13
updated: 2026-08-13
deliverables: []
---

# T-137 — Package the context-economy method as a skill

## 1. Specify

**Outcome**
The audit method in
[`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
becomes something another project invokes rather than reads: a skill that runs the eleven steps, walks
the `F1`–`F5` checklist, and produces the two documents. **Packaging, not rewriting** — if it turns
into a rewrite, the shaping rules failed and that is the finding.

**Why now, and why not before**
[T-130](T-130-audit-the-context-economy-of-an-agent-driven-repository.md) ruled: *this task produces
no skill, and it is shaped so one is cheap later. A second task does it if and when the method
survives being used once.* **It has now been used once, end to end**, on this repository, and the run
produced findings, a ranking, five child tasks and three corrections to itself. The trigger condition
is met.

**What the one run says about the method — the input this task exists to use**

| | What happened | What it means for the skill |
| :--- | :--- | :--- |
| **Steps 1–4 held** | The inventory ran as scripts and produced measurements nobody disputed | The measurement half is ready to package as written |
| **Step 5 was thin and said so only afterwards** | Two searches and two articles, presented as a catalogue; a reader named a tool it had missed | The skill must carry step 5's **coverage rule** — the search record — as a required output, not advice (**L-84**, [T-136](T-136-re-run-the-external-research-with-a-recorded-search-record.md)) |
| **A band was wrong by four times** | `CE-07` was banded on the surface's size, not on what could be changed | The rubric needs the *name the mechanism* step before a band is written (**L-82**) |
| **The F3 line held under pressure** | The general sweep over rationale prose was rejected, on the method's own test | Keep §4.1 verbatim; it is the part most likely to be softened by someone in a hurry |
| **The upstream rule paid for itself** | Reading the upstream backlog first turned a proposal into an adoption | Keep *read their backlog before proposing* as a step, not a note |
| **The byproduct register caught five things** | None of them token efficiency; one a real defect | It works. Keep it outside the ranking, as ruled |

**What implementing four of the findings then said — added 2026-08-13, and this is the half that decays**

The table above is what the *audit* run taught. Below is what came out of **building** four of its
findings in one session, which is a different instrument: every one of the four produced something
the finding had not predicted. **This section is the recall point.** A session starting the skill
reads it first and follows the pointers; the sessions themselves are gone.

| | What happened | What it means for the skill |
| :--- | :--- | :--- |
| **A finding understated itself by twenty times** | `CE-02` banded the board against a full listing — 17.7×. The question a session actually issues is *what next*, answered in **94 bytes against 36,813 — 389×** | The estimator must measure **the query the agent will issue**, not the pair of surfaces the finding names. Both are honest measurements of different things, and only one is the saving |
| **A filed observation had the wrong owner** | `O-T2` reported the unreachable command surface to taskmd. Measured later: taskmd ships a working launcher, the harness emits it onto `PATH`, and the shell snapshot's `PATH` line is truncated mid-value (**L-87**, `O-C1`) | The method needs a *prove which component failed* step **before** an observation is filed, not after. A local workaround that sidesteps the broken mechanism keeps working while the attribution stays wrong, so nothing forces the question |
| **The register's shape caused it** | §7 had one subsection per tool this project uses, so the only homes available for a harness defect were wrong ones | The skill's register template ships with a home for **an owner you have no subsection for**. A missing slot is where a wrong owner comes from |
| **Three of nine new observations would have been dropped** | They looked marginal or had no obvious action. The owner's ruling: record everything; what an observation is worth is the receiving project's call | State it as a rule, with the reason. A filter that asks *can I see what they would do with this* is the reporter deciding with less information than the reader has |
| **A throwaway scan's first output was a claim about its own tuning** | A twenty-line scan named three defective rows; one was its own regex (**L-86**) | Any scanning step owes a known-good case before its output is read as a finding. The scan was still the right move — one step was missing, not the tool |
| **Implementations feed the register, and nothing said so** | All four closures produced upstream-relevant material the audit had not seen; it took a separate task ([T-140](T-140-correct-and-extend-the-upstream-register-from-what-implementing-the-audit-found.md)) to collect it | The method's last step is not *rank and stop*. Implementing is a measurement pass, and the loop back into the register belongs in the method rather than in someone's memory |
| **The relation-bound needed a design step the method has no word for** | `CE-11` said *bound tier 1 as a relation* and taskmd had settled the shape already. Choosing the relation's **second term** was the whole of the work: a sum of what the file defers to is slack, and the smallest file it merely mentions is unstable, so an unrelated 2 KB note would tighten the budget tenfold (**L-88**) | *Write it as a relation* is guidance, not a procedure. The step owes its test — the second term moves only by a deliberate act, and the inequality is restatable in one sentence — or every project reinvents this argument |
| **Stating the budget cost 2,690 bytes of the budget** | The tier section went into the file it bounds, which is where a reader meets it at the moment it binds them, and that pushed the file 4,555 bytes over its own bound — more than half of it the section's own text | The skill has to say where the budget is written and price both answers. Outside the file it governs it goes unread; inside it is charged to every turn, and the first thing it reports is itself |

**Where the rest of it is.** [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.2 is the
operative version of the first four rows — what to check, what to report, where each thing goes —
written for a session working a finding. **L-85**, **L-86** and **L-87** in
[`../docs/LESSONS.md`](../docs/LESSONS.md) are the general halves. §7's preamble carries the
*audit* / *implementation* vintage rule and why it exists.

**Scope**
- In: the skill package — the eleven steps, the checklist, the rubric, the ten-field record, the three
  audiences, the byproduct register.
- In: **progressive disclosure**, on the evidence of this repository's own plugin: a description that
  routes, a body that activates, and references loaded per phase. `skills/htmldeck/` is the shape that
  measured best in the very audit being packaged, and it is the local model to copy.
- In: the four shaping rules T-130 followed — numbered imperative steps, a walkable checklist with
  stable ids, stable `CE-nn` ids, and no file of any one repository named as required reading.
- Out: changing the method. Corrections belong to T-136 and to whoever runs it next; this task moves
  it into a package.
- Out: shipping it in the htmldeck plugin. **This is a different product from a deck builder**, and
  bolting an audit onto a presentation skill would confuse both descriptions — which is itself an
  `F1` cost for every adopter who wanted neither.
- Out: publishing or releasing. That is a separate decision with its own gate list.

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.2 — what a session working an audit finding owes beyond the finding: what to check, what to report, and where each thing goes. Read before starting
- [`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
  — the whole method, and §10's four limits, which the skill must carry rather than drop
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) — the worked example, and the only evidence
  the method produces anything
- [`../skills/htmldeck/`](../skills/htmldeck) — the local model for a three-stage skill, measured in
  the audit at 472 bytes to discover and 5,206 to activate
- **L-82**, **L-83**, **L-84** in [`../docs/LESSONS.md`](../docs/LESSONS.md) — the three the one run
  produced; **L-85**, **L-86** and **L-87** are the three that implementing it produced

**Acceptance criteria**
- [ ] The skill runs the eleven steps and produces both documents, on a repository that is not this one
- [ ] It is three-stage: a routing description, a body on activation, references per phase — and the
      description alone is enough to decide whether to activate
- [ ] Step 5's search record is a **required output**, and the skill refuses to present a catalogue
      without one
- [ ] The rubric requires the mechanism to be named before a gain band is written
- [ ] §4.1's F3 line is carried verbatim, including *a finding that cannot name what the prose would
      stop deciding is not a finding*
- [ ] The upstream step keeps *read their backlog first* as a step with its reason
- [ ] The byproduct register survives, outside the ranking and with no gain band
- [ ] **It was packaging**: what changed is stated, and anything that had to be rewritten is reported
      as a defect in the shaping rules rather than quietly fixed
- [ ] Its own load cost is measured — description, body, and each reference — because a skill that
      audits context economy and is expensive to have installed is the joke that writes itself

**Open questions**
- ~~**Does it ship, and to whom?**~~ **Answered 2026-08-13 — it is published on GitHub as a token-saver
  audit skill, in its own right.** Not inside the htmldeck plugin, which settles the scope line above
  and adds three things this task now owes, because a published skill is a different artifact from an
  internal one:
  - **The extraction test becomes the product test.** `R8`'s rule that part 1 names no file of any one
    repository was a discipline; it is now the thing that makes the skill installable at all. It is
    verified by running the skill against a repository that is not this one, which is already a
    criterion.
  - **Its own load cost is a published cost.** Every adopter pays the description on every session,
    the way this project's deck skill costs 472 bytes to discover. That criterion stops being
    self-discipline and becomes a promise.
  - **The publishing rules apply**: no personal, client or machine data; the humanizer pass over
    whatever a stranger reads before installing; a licence; and out-of-the-box operation. See
    [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) — its §8 gate list is written for this repository
    and a new repository needs its own equivalent, which is work this task should size rather than
    discover.
- **One skill or two?** The measurement half is deterministic and scriptable; the screening and
  ranking half is judgement. They may want different shapes. — the implementer, from the rule's own
  reason.
- **Which repository does it live in?** Its own, by the answer above — but that is a new repository
  with its own gates, identity and release process, and none of that exists yet. — the owner, at plan.

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
| 2026-08-13 | (no change) | **The ship question is answered and it enlarges the task: published on GitHub as a token-saver audit skill, in its own right rather than inside the htmldeck plugin.** Three consequences are written into §1 rather than left to be met at review. The extraction test stops being a discipline and becomes the product test — a skill naming another repository's files is not installable. Its own load cost stops being self-discipline and becomes a promise every adopter pays on every session. And the publishing rules apply in full: no personal, client or machine data, the humanizer pass on what a stranger reads before installing, a licence, and out-of-the-box operation. A new question replaces the closed one: **it needs a repository, and that repository needs its own gate list** — `PUBLISHING.md` §8 is written for this one and does not travel. The effort stays `m` for the packaging; the repository is not sized here. |
| 2026-08-13 | → proposed | Raised at the owner's request, ahead of a session they have already planned, so the one run's evidence is not lost with the session that produced it. [T-130](T-130-audit-the-context-economy-of-an-agent-driven-repository.md)'s condition — *if and when the method survives being used once* — **is met**: it ran end to end and produced findings, a ranking, five child tasks and three corrections to itself. §1 records what the run says about the method rather than only that it ran, because that is the input a packaging task actually needs: steps 1–4 held, step 5 was thin, one band was wrong by four times, and the F3 line held under pressure. **Blocked on [T-136](T-136-re-run-the-external-research-with-a-recorded-search-record.md)** — packaging a method whose research half is known to be thin would set that defect in a form other projects copy, and T-136 is the fix already scheduled. `m`, and its own load cost is an acceptance criterion. |
