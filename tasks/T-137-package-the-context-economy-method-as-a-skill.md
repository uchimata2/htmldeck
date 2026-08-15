---
id: T-137
title: Package the context-economy method as a skill
type: deliverable
status: done
phase: review
shipped_in: unreleased
parent: T-130
blocked_by: []
related: [T-130, T-131, T-132, T-133, T-135, T-136, T-139, T-140]
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-08-13
updated: 2026-08-15
deliverables: [docs/research/R8-context-economy-for-coding-agents.md]
---

# T-137 — Package the context-economy method as a skill

## 1. Specify

**Outcome**
The audit method in
[`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
becomes something another project invokes rather than reads: a skill that runs the sixteen steps in
two phases, walks the `F1`–`F5` checklist, and produces the two documents. **Packaging, not rewriting** — if it turns
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

**What building the three `F1` splits then said — added 2026-08-14, and it is one finding, not eight**

`CE-05`, `CE-06` and `CE-09` were the method's three largest recommendations and were implemented in
one session. **Every one of them named a remedy the measurement changed, and every one was still
worth doing.** That is the row the skill most needs, because it is a property of how a finding is
produced rather than of who wrote these three.

| | What happened | What it means for the skill |
| :--- | :--- | :--- |
| **Three findings, three refused shapes** | `CE-05` would have left the growing half in place; `CE-06` led with a ratio describing a read nothing performs; `CE-09` asked for four files where everything outside the target was smaller than the target | The rubric must **separate the observation from the remedy** and mark only the observation as carried. A finding is generated by looking at sizes, and a size cannot price a change (**L-90**) |
| **Two of the three were worth doing for reasons the row never named** | `CE-06` saved no bytes at all and closed an interface that **983 citations** depended on with no gate resolving one of them | The closure step owes *what this actually bought*, and permission to correct the band downward while keeping the task. Without it the record teaches the next reader a number the project disproved |
| **The by-unit / by-kind question was one question in three tasks** | Specifying them independently would have produced three inconsistent answers; the first specified settled it as **L-89** and the other two cited it | Where a batch shares a policy question, the method should say so and name which task settles it — an ordering rule, not a note |
| **A byte-identity assertion passed while the references lied** | Both extractions shipped link labels and bare `§n` marks still pointing at the file they had left; both gates were silent and right to be (**L-91**) | The extraction step owes a **read** pass after the mechanical one, and its checklist is the checker's own list of what it declines to resolve |
| **The verification hid the defect it was written to catch** | A shape report bucketed `../../../` under `startswith("../../")` and called a doubled rewrite clean | Already **L-62**; what is new is that it happened to the session that was citing L-62. The step needs to be in the procedure, not in the reader's memory |
| **A gate went red because the tool was untracked** | The manifest names every tracked tool exactly once, so a new checker is `STALE` until it is staged | Worth shipping as a shape: the manifest partition turns *clone-and-run* from a principle into a failing test |
| **The last finding on the board was measuring the wrong unit** | `CE-12` ranked 13 of 13 on three docstring shares that were counts of triple-quoted string tokens. Re-measured by AST role the "85%" file is **3.2%** and the lowest in the tree, and the relocation the row proposed would have deleted two tools' payloads. Withdrawn ([T-150](T-150-relocate-the-research-prose-in-the-two-docstring-outliers.md), **L-92**) | **The step before *does this prose decide anything* is *are these bytes prose*.** The rubric gets a unit field, and the method owes a **known-answer check on the counter** before a share is written down. Note where it landed: **L-90 says a band cannot price a change; this says a band's own subject can be wrong**, and neither is visible from inside a number that is precise and reproducible. The cheap rows are where it survives, because nobody re-measures rank 13 |

**What the two tier-1 cuts then said — added 2026-08-14, and it is about what a finding can and
cannot price**

`CE-01` and `CE-04` are the two cuts `CE-11`'s bound was written to make decidable, worked in that
order ([T-143](T-143-split-the-release-chronology-out-of-claude-md.md),
[T-144](T-144-give-each-cumulative-rule-one-operative-home.md)).

| | What happened | What it means for the skill |
| :--- | :--- | :--- |
| **The finding's byte count was 48% wrong as a forecast** | `CE-01` measured a 6,980-byte chronology; **3,619 came out**, because the rest was fourteen operative rules that had to stay. The row said *the extraction is the work* and could not say what fraction that was | The rubric needs a **carve-out estimate** for any F1 split: what share of the named region is load-bearing. `L-90` says a size cannot price a change; this says the *region* named by a size is not the change either. A one-line answer — *what fraction of this is rules?* — would have moved the band |
| **The share had already moved before the task started** | `CE-01`'s 45% was 37.9% a day later. The section had **grown** 228 bytes; the file around it grew 3,405 | A share is two measurements and the denominator usually moves faster. The record field should be **absolute bytes plus the date**, with the share derived — the reverse of how it was written |
| **Three paragraphs in scope needed no new home** | Their content was already in two other documents. Copying them would have built `CE-04`'s defect while fixing `CE-01`'s | The split step owes a **sweep for existing homes before writing the destination**, or an F1 split manufactures F2 duplication. The two findings are adjacent and the method treats them as independent |
| **The duplicate-removal task found a duplicate its sibling had created that morning** | T-143 wrote a fresh copy of the rule into the document it created, hours before T-144's survey caught it | Not an oversight — **a rule with no declared home gets copied by whoever needs it next**. The `F2` remedy is therefore *declare the home*, and deleting copies without doing that regenerates them |
| **The document that governs the behaviour was the only one not stating it** | Five documents restated *a phase is not a version*; the release sequence, whose own step the failure broke, said *bump the version* and never said to what | The `F2` step's first question is **which document should have had it**, not which copies to delete. Restatement spreads where the governing home is missing, so the count of copies is a symptom |
| **It was two rules wearing one sentence** | They bind at different moments — picking a release number, and setting a task field — which is why no single document had ever been able to own it | Before assigning a home, **ask how many rules there are**. A cumulative rule that resists a single home is usually two, and the survey is what surfaces that |
| **Neither finding reduces bytes** | Tier 1 fell 4,214; the destinations gained 1,117 and a new 10 KB document | Say it in the band's definition. `A` and `B` surfaces measure **what is paid per turn**, not repository size, and a reader who checks the total will think the method failed |
| **A bound that a split cannot satisfy** | Any document split out of tier 1 is smaller than tier 1, so a relation over *the smallest document it defers to* ratchets down with every remedy it prompts, unless the comparison set is fixed | `L-88` chose the second term; this is its missing test. **The relation's set must be closed and stated** — here, tier 2 — or the budget is unsatisfiable by the one action it exists to cause |

**What emptying the ranking said — added 2026-08-14, and it is about the register the method never
told anyone to keep**

The last three findings closed in one session
([T-148](T-148-give-a-measured-figure-a-durable-home.md),
[T-149](T-149-prune-the-memory-index-of-spent-entries.md),
[T-152](T-152-give-look-at-the-rendered-deck-one-operative-home.md)), preceded by the tooling that
made the closing legible ([T-151](T-151-generate-the-finding-to-task-listing-instead-of-keeping-it-by-hand.md)).

| | What happened | What it means for the skill |
| :--- | :--- | :--- |
| **Nothing joined a finding to its task, and by thirteen findings that cost 325,695 bytes to answer** | *Which finding is which task* had to be assembled from six sources, and the answer was stale at the next closure. The link now lives in one field in the task's front matter and the listing is computed in **1,317 bytes** | The method ranks findings and never says **where the link lives**. Every adopting project will re-derive it, and the shape that works needs no new file: put the link on the *task*, parse the ranking table where it stands, and check the two against each other |
| **The register and the tracker could disagree with nothing to notice** | A finding's row read closed while its task was open, and vice versa, invisibly. The check fails in **both** directions now, and it caught the session that wrote it — closing the task left it in a live row | `L-74` applied to the audit's own bookkeeping. **The method owes a closure gate, not a closure checklist**: §6.2 lists what a closure owes and a list is what goes unread. Wire it where a closure actually happens, not into the release gate |
| **A per-item band was already declared and nothing read it** | `CE-04`'s Effort cell had read `xs` **each** since the row was written, while the prose one section away said nothing in the table marked per-item bands. A closed row with open work is legal for exactly those findings | **The rubric needs a per-item band as a first-class value**, because a finding that closes per instance breaks *closed means finished* — the assumption every status check makes. The marker existed; the schema for reading it did not |
| **An inherited survey was wrong in both directions** | T-144's survey named a document that had never stated the rule, and missed a copy inside the file the rule was being cut from — found only because T-152's criteria forced a re-measure before editing | **A survey is evidence about the day it was taken** (**L-96**). The method's F2 step should carry its own re-measure clause, the way §6.2 carries one for figures; a remainder handed from a closed task inherits its staleness with it |
| **A finding's remedy was refused and the refusal was the deliverable** | `CE-08` said *give a measured figure a durable home*; the figure now has none, because the decision it drove was coarser than the number (**L-95**). Third refused shape in this audit, and the first where refusing *was* the work | `L-90` says a band cannot price a change. This says the **remedy field is a hypothesis**, and the rubric should mark it as one — an outcome of *shape refused, still worth doing* has now happened four times out of thirteen and has no place to be recorded |
| **The obligation after the last closure had nothing scheduling it** | Phase 2 existed as a paragraph saying a session should notice. It became [T-153](T-153-run-the-audit-methods-phase-2-over-this-repositorys-own-audit.md), blocked on two tasks — and the recorded condition, *blocked behind six*, had counted unrelated backlog | The method gained phase 2 and did not say **who raises it**. A phase that runs once, later, on a trigger nobody watches, is a phase that does not run. It should ship as a task the adopter creates when the ranking is raised, blocked on the audit's own repairs |

**What re-running step 5 under its own new rule said — added 2026-08-14, and it is about the
gathering step rather than the ranking**

The coverage rule written after `T-130` closed was run for the first time by
[T-136](T-136-re-run-the-external-research-with-a-recorded-search-record.md). It worked, and what it
cost and found is the input this task wants.

| What happened | Detail | What the method owes |
| :--- | :--- | :--- |
| **The first pass had found 54% of the catalogue and the partition read as complete over it** | Nineteen entries, then twenty-one, then **35** under a recorded search record. Every earlier sum was internally correct | **The method should state the expected order of magnitude of step 5**, because *two searches and two articles* did not read as thin at the time. A catalogue that fits on one screen after a survey of a live tool space is the signal, and nothing in the method said so |
| **Six of fourteen new techniques came only from the by-name axis** | Searching for *ideas* never reaches a technique whose name is a product. The by-name axis also produced the single largest correction in the catalogue | **Step 5's three axes should be named in the method, not left to the auditor**: ideas, named tools, and *the harness's own documented mechanisms* — the third found three techniques and had never been treated as a source at all |
| **A stopping rule had to be invented, and the useful part was recording the empty rounds** | Declared saturation per axis: an axis stops when a full round adds nothing, and **the round that added nothing is listed**. That row is what lets a reader judge whether the axis stopped early | The method asks for a search record and does not say **when to stop searching**. Without a rule the record documents an arbitrary stop; with one, the negative rounds carry the argument. Ship the rule with the record |
| **A named tool's own figures were four times its measured effect** | Advertised −54% code / −20% cost; an 80-task independent benchmark measured −15% and −10.3%, concentrated on big builds and zero elsewhere (**L-98**) | **Step 7 should require the source of every figure it screens on.** A verdict resting on a vendor's number is a verdict resting on their best case, and the shape of the effect — where it concentrates — decides more screenings than its size |
| **Re-running the research changed no finding, and that had to be written down** | `CONTEXT-AUDIT.md` §4.1. Ten of fourteen new techniques were addressed to the harness or the API, and the one real local candidate was unmeasured | **A step that can produce nothing needs a place to say so.** `T-153` was blocked on this answer, and *no new finding* is only an answer if it is recorded as one. The method's step 5 should say that a null result is an output |

**What grading the whole ranking said — added 2026-08-14, and it is the only row set written with
every outcome known**

Phase 2's steps 12 and 13, by [T-153](T-153-run-the-audit-methods-phase-2-over-this-repositorys-own-audit.md).
Thirteen findings paired against what they bought:
[`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §10. **This is the row set that cost the most
to produce and is the least likely to be reproducible** — it needed fourteen closed records at 80,721
bytes and a year of nobody having thrown them away.

| What happened | Detail | What the method owes |
| :--- | :--- | :--- |
| **Two of thirteen bands held as written** | Four wrong on magnitude, three on shape, one on premise, two costs by design, one undercounting its own subject | **The band is not a forecast and the method should stop implying it is.** `R8` §5 now says `Change` is a hypothesis; the skill has to carry that at the point a user writes a band, not in a paragraph they read afterwards |
| **Every error was in the `Change` cell and none in the `Finding` cell** | The inventory said where the weight was and was right thirteen times out of thirteen | **Split the record's reliability, visibly.** A user who trusts both halves equally will obey a ranking; four rows here were refused by measurement during implementation, and obeying them would have deleted two tools' payloads |
| **Two findings carried a band the rubric did not define** | `enabler` and `bimodal`, invented at ranking time because nothing in the four-value table fits a gain that is not a saving | **A rubric that gets extended in the field is under-specified.** Both are in `R8` §5 now. The skill should ask *is this a saving?* before it asks *how big?* |
| **The audit's own remedies were most of the growth it then had to cut** | 3,012 of 3,405 bytes onto tier 1, from the two findings written to govern tier 1 | **This is step 16's warning, and this run committed it before step 16 existed.** The skill must price a governance rule against the surface it lands on, at the moment it is written |
| **The method has no cheap way to know what a finding bought** | Step 12 reconstructed it from 80,721 bytes; a twelfth field would be paid by every finding to serve one step | **The closure owes one line, in the record that already exists.** Not a field. `R8` §6 now says so, and this is the clearest case in the method of the cheap answer and the tidy answer disagreeing |
| **Six of eight byproducts were one class, and no row could show it** | Text a reader follows and no checker reads: link labels, bare `§n`, unallocated citations, a dangling pointer outside the tree | **Read the register for a shape at step 12.** `R8` §6.3 now says so. As rows they are eight small defects; as a class they are a gap in what a project's gates can see |

**Where the rest of it is.** [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.2 is the
operative version of the first four rows — what to check, what to report, where each thing goes —
written for a session working a finding. **L-85**, **L-86** and **L-87** in
[`../docs/LESSONS.md`](../docs/LESSONS.md) are the general halves, and **L-89** to **L-96** are the
2026-08-14 batch's. The portable half of the last row is already in
[`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
§4.1, as a second F3 guard rail ahead of the first. §7's preamble carries the
*audit* / *implementation* vintage rule and why it exists.

**Scope**
- In: the skill package — the sixteen steps in two phases, the checklist, the rubric, the ten-field
  record, the three audiences, the byproduct register.
- In: **phase 2, `R8` §3.1 — establish standing operation**, added there 2026-08-14 at the owner's
  direction and **not restated here**. It is the closing half the method lacked: an audit is a
  measurement at one moment, and a cleaned repository resumes growing at the rate that produced the
  findings. **It changes what this skill is** — from an instrument that reports, to one that leaves a
  discipline behind — and its own step 16 is written mostly to stop the skill becoming a second policy
  author for a project it is a guest in.
- In: **progressive disclosure**, on the evidence of this repository's own plugin: a description that
  routes, a body that activates, and references loaded per phase. `skills/htmldeck/` is the shape that
  measured best in the very audit being packaged, and it is the local model to copy.
- In: the four shaping rules T-130 followed — numbered imperative steps, a walkable checklist with
  stable ids, stable `CE-nn` ids, and no file of any one repository named as required reading.
- In: **a listing that answers *which finding is which task, and where is it* without reading the
  audit.** Requested by the owner 2026-08-14, from the cost of doing it by hand: assembling that
  picture here meant reading the ranking table, the two blocks of finding statements, the candidate
  table, the per-owner upstream documents and thirteen task files, and the result was a fourteenth
  hand-kept copy of facts that already existed. **The finding's prose is not the target** — the
  argument in a row is why the row survives. The index is: `id`, one-line title, subject or owner,
  band, effort, the task it became, and that task's status. See the criteria below for what
  *efficient* has to mean.
- In: **bootstrapping the repository the skill ships from — added 2026-08-15, when the owner supplied
  it.** It is a sibling of this one, empty, named `ecoctx`, and not yet a git repository. That answers
  the third open question below and it enlarges the task by a whole half: identity, licence, README,
  a gate list, and a release rule, none of which travel from here. **`PUBLISHING.md` §8 is written for
  this repository and is evidence rather than a template** — what carries across is that step 1 is one
  command which partitions every checker into *ran*, *skipped with a reason*, or *failed*, and the
  contents of that command are the new repository's to discover.
- In: **declaring where the operative method now lives.** Once the skill exists, `R8` is a research
  record and the skill is the method, and nothing in the tree says so. That is the method's own `F2`
  remedy applied to itself — *declare the home*, in the document that should have had it — and it is
  this task's only deliverable inside this repository.
- Out: changing the method. Corrections belong to T-136 and to whoever runs it next; this task moves
  it into a package.
- Out: **mirroring the skill's source here.** The package ships from `ecoctx` and its files are
  recorded in §3 rather than declared as paths in the front-matter. A tracker gates what it can see; a
  declared path that cannot resolve is a red gate forever, and a hand-kept list of another tree's
  files is the second copy this project's own audit exists to prevent.
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
- [ ] The skill runs all sixteen steps and produces both documents, on a repository that is not this one
- [ ] **Phase 2 runs after the raised work is implemented, and the skill says so** rather than
      offering it at ranking, where there is nothing yet to measure against
- [ ] Step 12 pairs every implemented finding's **band against its measured outcome**, keeps the
      original, and treats a withdrawn finding as a result rather than a gap
- [ ] Step 13's report states what the remedies **cost** as well as what they saved, including the case
      where the repository ends larger
- [ ] Step 14's output changes the **method**, and the skill keeps it separate from anything
      project-specific — a repository's habit written into a portable skill is the failure this shaping
      exists to prevent
- [ ] Step 15 inherits step 5's search-record refusal and is **bounded to the delta** since the audit
- [ ] Step 16 will not emit a policy without a named governing document, a load-path price, and an
      **extends / narrows / replaces** verdict against the nearest existing rule
- [ ] Step 16 reports a collision with a project's own policy rather than resolving it, and leaves at
      least one check that re-measures on a trigger the project already has — or states why none can
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
- [ ] **A command answers *every finding, its task and its state* in one output**, and the output is
      small enough to read whole — the tracker's own `list --open --limit 1` at 94 bytes is the bar
      that already exists here, not a new idea
- [ ] **The listing is derived, never maintained.** Each finding's key fields live in exactly one
      place, and every table that shows them — the ranking, the candidate record, the per-owner
      upstream documents — is generated from that place or checked against it. A hand-kept second
      table is the defect this criterion exists to prevent
- [ ] **A finding's link to its task is structured, not prose.** Today it is a sentence inside §1 of a
      task file, which no tool can follow; whatever replaces it must be readable by a command without
      parsing English
- [ ] **The check fails loudly in both directions** (**L-74**): a finding whose task has closed and
      still reads open, and a task naming a finding that does not exist, both stop the run. A
      generator without that check moves the inconsistency rather than removing it
- [ ] **The listing does not become a second board.** This repository's `DUPLICATE INDEX` advisory
      exists because a table of task ids outside the tracker's markers is exactly that, and it is
      excused for one file by name — so the skill's index must key on findings and reference tasks,
      never mirror them
- [ ] **`ecoctx` is a repository a stranger can clone and run**: a licence, a README that says what the
      skill does before it says how it is built, and no path that only resolves on the machine it was
      written on
- [ ] **It carries no personal, client or machine data**, and the human-facing text has been through
      the humanizer while the skill's own files have not — the same split
      [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) makes here, for the same reason
- [ ] **`ecoctx` has its own step-1 command**, and it partitions every checker into *ran*, *skipped
      with a stated reason*, or *failed*. A checker in none of the three fails the run
- [ ] **This repository states where the operative method now lives** — in `R8`, the document that
      would otherwise be read as the method — and `docs/CONTEXT-AUDIT.md` still reads as the worked
      example rather than as a second copy of the procedure
- [ ] **Nothing in `ecoctx` names a file of this repository.** The extraction test, run as a search
      rather than asserted

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
- ~~**One skill or two?**~~ **Answered 2026-08-15 — one skill, two phases.** Settled by the method's
  own `F1` rule rather than by preference: a second skill is a second description every adopter pays
  on every session, and the two halves are never wanted apart, because screening has nothing to screen
  until the measurement has run. The measurement half stays deterministic by being **tools the skill
  calls**, not a skill of its own — which is also what keeps *its own load cost* answerable, since a
  script costs nothing until it is run and a description costs on every session.
- ~~**Which repository does it live in?**~~ **Answered 2026-08-15 — its own, a sibling named
  `ecoctx`, supplied empty by the owner.** Recorded in the scope above, which is where its
  consequences are. It is not yet a git repository, so *bootstrap* is part of the work rather than a
  precondition of it.
- ~~**Does `ecoctx` track its own work, and if so with what?**~~ **Answered 2026-08-15 by the owner —
  taskmd, and on GitHub once taskmd can do that. It is scheduled and not ready, so the interim is two
  homes split by who writes:**
  - **GitHub Issues is the public inbox**, on from publication. It is the only channel a stranger will
    use — nobody clones a repository to add a markdown file to `tasks/` — and this owner already runs
    one that way, as the route for htmldeck's whole upstream register. An issue is a **report**: its
    phase, type and severity are `ecoctx`'s to derive, on this project's *a task's classification is
    not its filer's* rule.
  - **`tasks/` with taskmd in-repo is the backlog**, owner-side, exactly as this repository does it in
    public today. A task cites the issue it came from.

  **This is not undone when taskmd learns GitHub.** What that feature syncs is `tasks/` against
  Issues, so having both in the shapes they would take anyway is what gives the sync something to
  sync. **What must not be built now is the triage or sync tool** — that is the scheduled work, and a
  local version of it is the trap this task's own §1 names: a workaround that sidesteps a broken
  mechanism keeps working while the attribution stays wrong, so nothing forces the question. Manual
  triage until it ships.

  **And the loop that actually improves the method is runs, not reports.** Step 14 already says so;
  what the owner's answer adds is that the tracker is insurance rather than the mechanism, because a
  graded finding table is the evidence a method improvement needs and an issue is not one. Just-committed
  is right for the first weeks and wrong permanently: before there are adopters the commit log **is**
  the record, and the second run is when that stops being true.
- **When may `ecoctx` be published?** Not before step 10 has run the skill against a repository that
  is neither this one nor its own — the acceptance criterion is the product test, and publishing first
  makes the first stranger the first test. Publication itself is out of scope here; this records what
  gates it. — the owner, after review.

## 2. Plan

**Order, and the one thing it is built around.** The extraction test is step 10 and not step 1,
because it is the only step that can fail for a reason the others cannot see — a sentence naming this
repository reads perfectly inside `ecoctx` and is wrong there. It runs as a **search over the finished
tree**, after everything is written, and it is why the writing steps below never copy prose across:
what moves is the method, and every worked example is rewritten or dropped.

**Where the two halves meet.** Steps 1 and 11 are the only ones that touch this repository. Everything
between them is `ecoctx`, and none of it is mirrored back — see the scope's last bullet.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | **Bootstrap the repository.** `git init`, the publishing identity, `.gitignore`, a licence, and a README that says what the skill does before it says how it is built. No trailer, on this repository's ruling | `ecoctx` is a git repository with a first commit |
| 2 | **Write the routing description alone, and stop.** It is the only part every adopter pays on every session, and the criterion is that it is enough to decide whether to activate. Write it before the body so it is not a summary of one | The description block, and its measured byte cost |
| 3 | **Write the body**: what the method is, the two phases, the three audiences, and where each reference is loaded. It activates; it does not teach | `SKILL.md`, at the root of `ecoctx` |
| 4 | **Phase 1 reference — the measurement half**, steps 1–4 plus step 5's three axes, its saturation rule and its refusal to present a catalogue without a search record | A phase-1 reference file, under `references/` in `ecoctx` |
| 5 | **Phase 1 reference — the judgement half**, steps 6–11: the rubric with the mechanism named before a band, the *is this a saving* question ahead of *how big*, `enabler` and `bimodal` as defined values, the `F1`–`F5` checklist with §4.1 verbatim, the eleven-field record, and the byproduct register with a home for an owner it has no subsection for | A second phase-1 reference file, under `references/` |
| 6 | **Phase 2 reference**, steps 12–16: pair every band against what it bought, report cost as well as saving, treat a withdrawn finding as a result, bound the delta research, and refuse a policy without a governing document, a load-path price and an *extends / narrows / replaces* verdict | A phase-2 reference file, under `references/` |
| 7 | **The finding-to-task link, and the command that reads it.** Structured on the task, parsed where the ranking stands, and failing in **both** directions. This is the one piece with a working local original — `tools/docs/findings.py` here — and what travels is its shape, not its code, because it is bound to one tracker's front-matter | A findings tool, under `tools/` in `ecoctx`, tracker-agnostic |
| 8 | **The step-1 command**: discover every checker, run it, and end with a partition of *ran* / *skipped with a stated reason* / *failed*, with no fourth outcome | A check-all tool, under `tools/` in `ecoctx` |
| 9 | **Measure the skill's own load cost** — description, body, and each reference separately — and write the figures with their date into the README, as the promise they now are | A load-cost section in the README |
| 10 | **Run the extraction test as a search**, not as a claim: no file, tool or document of this repository named anywhere in `ecoctx`. Then run the skill's phase 1 against a repository that is neither | A recorded search, and one phase-1 run on a third tree |
| 11 | **Declare the home here.** `R8` states that the operative method is the skill and that it is the research record; `docs/CONTEXT-AUDIT.md` is checked for the same confusion and left as the worked example | The declared deliverable |
| 12 | **Humanize what a stranger reads before installing** — the README and the repository description, and nothing else. The skill's own files stay AI-optimized | A humanizer pass, README only |

## 3. Implement

**Decisions & assumptions**
- **`ecoctx` keeps its backlog in `tasks/` and its inbox in GitHub Issues** — the owner, 2026-08-15.
  Recorded in §1's third open question with the reason and with what it forbids.
- **`m` is unchanged and is measured, not re-guessed, once steps 1–2 are done** — the owner,
  2026-08-15, answering the band question directly.

**Outputs produced**
- **Plan step 1 — the repository exists.** `ecoctx` is a git repository under the publishing identity
  with no trailer, MIT, `eol=lf` pinned because this project publishes measured byte counts, and a
  README leading with the grading table rather than with the steps. Two commits.
- **Plan step 2 — the routing description, measured 2026-08-15.** **497 bytes**, front matter block
  **532**. The comparison is this repository's own deck skill at **474 bytes** of description, measured
  the same day and the same way, so `ecoctx` costs **+4.9%** of a description to have installed.
  **The first draft was 610 and that is the finding**: 29% over the comparison, on a skill whose whole
  argument is that this number matters. What came out was duplication and not trigger surface — two
  pairs of phrases each saying one thing twice — so **−18.5% with every trigger kept**. The width that
  remains is deliberate: nobody guesses that *why is my session expensive* routes here, where *make me
  a slide deck* routes itself.

- **Plan steps 3–9 — the package.** A three-stage skill in `ecoctx`: a routing description, a body
  that routes and never teaches, and three references, one per span of steps, with a run loading
  exactly one. **The four refusals live on the body rather than in a reference**, because a refusal
  kept in a file the session may not load is not a refusal. Two tools: a findings register that reads
  the finding-to-task link off the task's front matter and fails in both directions, and a check-all
  that partitions into *ran* / *skipped with a stated reason* / *failed*, with a tool on disk and
  absent from the manifest failing the run. A self-test exists because this repository is the skill
  and holds no report of its own, so the register would otherwise ship untested.
- **The known-answer run found a defect in the instrument, not in the target.** Pointed at a
  repository whose finding-to-task answer was already established by other means, the first scanner
  reported **twelve disagreements out of thirteen** where there were none: a finding is stated in
  prose before it is ranked, so the first line naming an id is never the row carrying the closure
  marker, and a project with three tables naming the same id compounds it. Restricted to table rows
  and OR-ed across them it reproduces the independent answer exactly — **13 findings, 14 tasks linked,
  0 disagreeing.** This is the method's own *a scanning step owes a known-good case* rule catching the
  session that was packaging it.
- **Plan step 10 — the extraction test, run as a search.** 238 distinctive filenames of this
  repository, plus its own name, searched across every file of `ecoctx`: **0 hits.** *The first
  instrument was useless and that is worth keeping*: matching all 451 names produced **89 false
  alarms** — `faces` inside *surfaces*, plus `tools`, `reference`, `research`, `sources` and `tasks` as
  ordinary English. Bound on structure instead (a real extension, long enough not to be a word, and
  not a name `ecoctx` itself uses), it went to zero. Convergent tool names in both trees are not a
  leak; a pointer at the source tree is.
- **Plan step 10, second half — phase 1 against a third repository**, `taskmd`, chosen by the owner.
  Surfaces A, B and C measured: tier 1 is **6,619 bytes**, less than half this repository's; the board
  is **36,393** on the read path, which is the same shape as the finding this repository closed with a
  query command, and that tool is already shipped there; the green test run prints **344 bytes** for
  261 tests, which is a null result for `F5` and is reported as one. **Steps 5–11 were not run and the
  two documents were not produced** — see §4.
- **Plan step 11 — the home is declared.** `R8` now opens by saying the operative method is the skill
  and that it is the research record, with what the skill does and does not carry. That is this
  method's own `F2` remedy applied to itself.
- **Plan step 12 — the README went through the humanizer**, and nothing else did. **0 em dashes, 0 en
  dashes, 0 curly quotes, 0 bold runs**, every figure preserved. The skill's own files stay
  AI-optimized, which is the rule rather than an omission.

**What steps 1–2 say about the `m` band**
The owner deferred the re-band to this measurement, so here it is. **Nothing in the first two steps
argues for moving it.** Both were cheap and neither surprised: the repository skeleton is boilerplate
and the description is one paragraph that took one trim pass. **The band's risk was never here** — it
is steps 4 to 8, three reference files and two tools, and step 10, which is a run against a third
repository that nothing has sized. The honest statement is that `m` is untested rather than confirmed,
and the next measurement that can move it is step 4.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Runs all sixteen steps and produces both documents, on a repository that is not this one | **not met** | Steps 1–4 ran against `taskmd` and produced real figures; 5–11 did not, and no document was produced. **A full audit of a third repository is itself `l`-sized work and packaging it is not the same act as running it.** Raised as [T-162](T-162-run-the-packaged-skill-end-to-end-against-a-third-repository.md), which is the product test and gates publication |
| Phase 2 runs after the raised work is implemented, and the skill says so | met | On the body and again at the head of the phase-2 reference, which refuses a run from memory |
| Step 12 pairs band against measured outcome, keeps the original, treats a withdrawal as a result | met | Including *the refusal was the deliverable* |
| Step 13 states what remedies cost, including a repository that ends larger | met | With the 4,214 / 1,117 figures and the audit's own 3,012-of-3,405 growth |
| Step 14 changes the method and keeps it separate from anything project-specific | met | Stated as the failure the step exists to prevent |
| Step 15 inherits step 5's refusal and is bounded to the delta | met | *A closing phase that re-runs step 5 in full is another audit wearing a different number* |
| Step 16 refuses a policy without a governing document, a load-path price, and an extends/narrows/replaces verdict | met | All four constraints carried, plus the 2,690-byte worked example of writing a budget into the file it bounds |
| Step 16 reports a collision rather than resolving it, and leaves a re-measuring check or says why none can exist | met | Both, plus *wire the closure gate where a closure happens* |
| Three-stage, and the description alone decides activation | met | Measured: 497 / 5,074 / three references loaded one at a time |
| Step 5's search record is required and a catalogue without one is refused | met | Refusal 1 on the body, so it cannot be missed by a session that never loads the reference |
| The rubric requires the mechanism named before a gain band | met | And *is this a saving at all* placed ahead of *how big* |
| §4.1's F3 line is carried verbatim | met | *An F3 finding that cannot name what the prose would stop deciding is not a finding, and is recorded as rejected*, plus the prove-the-bytes-are-prose guard ahead of it |
| The upstream step keeps *read their backlog first* as a step with its reason | met | With *say in each entry whether their backlog was read* |
| The byproduct register survives, outside the ranking and with no gain band | met | Including the record-everything rule and the home for an owner you have no section for |
| It was packaging: what changed is stated, and a rewrite is reported as a shaping defect | met | **Nothing was rewritten.** Three things were *added* and each is a shaping gap rather than a method change: the reference boundaries, the four refusals hoisted onto the body, and the load-one-at-a-time table. The method's prose transferred as written |
| Its own load cost is measured, per stage | met | The README table, dated |
| A command answers every finding, its task and its state in one output | met | `findings.py`, and the output is one line per finding |
| The listing is derived, never maintained | met | Nothing is written down; both sides are parsed where they stand |
| A finding's link to its task is structured, not prose | met | A front-matter field, read without parsing English |
| The check fails loudly in both directions | met | **Tested, not asserted**: ten fixture checks, both directions plus the dangling task and the prose-mention regression |
| The listing does not become a second board | met | Keys on findings, references tasks, mirrors nothing |
| `ecoctx` is a repository a stranger can clone and run | met | MIT, README, no machine-specific path; the tools take `--root` and discover the repository themselves |
| No personal, client or machine data; humanizer on the human-facing text only | met | 0 em dashes, 0 en dashes, 0 bold in the README; the skill's files untouched |
| `ecoctx` has its own step-1 command with a three-way partition | met | `check_all.py`, green at 1 ran / 2 skipped with reasons / 0 failed / 0 unpartitioned |
| This repository states where the operative method now lives | met | `R8`'s opening block |
| Nothing in `ecoctx` names a file of this repository | met | Searched, 238 distinctive names, 0 hits |

**Child fix tasks raised**
- [T-162](T-162-run-the-packaged-skill-end-to-end-against-a-third-repository.md) — the one unmet
  criterion, and it is the product test rather than a loose end.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-15 | → done | **Twenty-six criteria, twenty-five met, and the unmet one is the product test rather than a loose end.** The skill exists in its own repository as three stages measured at 497 / 5,074 / three references loaded one at a time, with two tools and a self-test. **It was packaging and nothing was rewritten** — the method's prose transferred as written, and the three things added are shaping gaps rather than method changes: reference boundaries, the four refusals hoisted onto the body where a session cannot miss them, and the load-one-at-a-time table. **The session's own instruments failed twice and both are recorded because they are the method's rules catching the person applying them.** The finding register's first scanner reported twelve disagreements out of thirteen against a known answer, because a finding is stated in prose before it is ranked and the first mention of an id is never the ranked row; restricted to table rows it reproduces the independent answer exactly. The extraction test's first instrument produced 89 false alarms by matching ordinary English inside longer words, and bound on structure it produced zero across 238 distinctive names. **Steps 1–4 ran against a third repository and produced real figures**, which is the half of the method that has never failed; steps 5–11 did not, and that is [T-162](T-162-run-the-packaged-skill-end-to-end-against-a-third-repository.md), `l`, gating publication. A search proves nothing is *named*; only a run proves nothing is *assumed*. **`m` was the right band for what this task turned out to be** and the repository half did not blow it, because the bootstrap was boilerplate and the writing was transfer rather than invention. `shipped_in: unreleased` — the skill is in a different repository and nothing was released here. |
| 2026-08-15 | → in_progress | **Steps 1 and 2 done, and step 2 caught this project failing its own subject on the first draft.** The repository exists — MIT, publishing identity, no trailer, `eol=lf` pinned because a project that publishes byte counts cannot let them depend on who checked it out. The README leads with the grading table rather than the steps, on the argument that two of thirteen bands holding is the part a stranger cannot get elsewhere. **The description was written alone and before the body**, so that it is a routing decision rather than a summary, and it came out at **610 bytes against a comparable skill's 474**. Trimmed to **497** by deleting two pairs of phrases that each said one thing twice, with every trigger kept: **−18.5%**, and **+4.9%** against the comparison, which the extra trigger surface earns because nobody guesses that *why is my session expensive* routes to an audit. **The remaining width is not slack and the figure is dated in §3, not here.** *On the band:* the owner deferred the re-band to this measurement and the measurement does not move it. Both steps were cheap and neither surprised; the risk was always steps 4 to 8 and step 10, and none of those has been touched. `m` is **untested rather than confirmed**, and step 4 is the next thing that can move it. **The third open question is closed by the owner's ruling** — `tasks/` and Issues, split by who writes, with no triage tool built here because that is taskmd's scheduled work — and a fourth was raised in its place: publication is gated on step 10, since otherwise the first stranger to run this is also its first test. |
| 2026-08-15 | → planned | **Twelve steps, and the order is built around the one that can fail invisibly.** The extraction test is step 10 rather than step 1: a sentence naming this repository reads perfectly from inside `ecoctx`, so it has to be a search over the finished tree, and it is why no writing step copies prose across. Two steps touch this repository — the bootstrap's sibling and the home declaration — and nothing between them is mirrored back. **The description is written before the body and alone**, because it is the only part charged on every session and a description written afterwards is a summary of the body rather than a routing decision. **One step has a working local original and it does not travel as code**: `tools/docs/findings.py` is bound to this tracker's front-matter, so what moves is the shape — the link on the task, the ranking parsed where it stands, and a check failing in both directions. **The band still reads `m` and the plan says why that is now doubtful**: twelve steps, of which four are the packaging the band was set for and eight are the repository, and the honest re-band waits for the first two steps to be measured rather than being guessed here. |
| 2026-08-15 | → specified | **The owner supplied the repository and it closed the question that gated everything else.** A sibling folder named `ecoctx`, empty and not yet a git repository — so the skill ships from its own project rather than from here, and *bootstrap* is inside the task instead of behind it. That adds a half nobody had sized: identity, licence, README, a gate list and a release rule, none of which travel, because `PUBLISHING.md` §8 is written against this tree's checkers and decks. What does travel is its **shape** — one command, and a partition with no fourth outcome. **Two of the three open questions closed and one was replaced.** *One skill or two* is settled at one, by the method's own `F1` rule rather than by taste: a second skill is a second description charged to every adopter on every session, and the halves are never wanted apart, since screening has nothing to work on until the measurement has run — so the deterministic half ships as tools the skill calls, which cost nothing until invoked. *Which repository* is answered above. What replaced them is whether `ecoctx` tracks its own work, which is the implementer's at plan and reversible. **One deliverable is declared and it is the small one**: `R8` gains the statement of where the operative method now lives, because a research record that reads as the method is the `F2` defect this method names — *declare the home, in the document that should have had it*. The skill's own files are not declared as paths, and the reason is in the scope: this tracker cannot resolve another tree, and a hand-kept mirror of one is the second copy `L-74` is about. Five acceptance criteria added for the repository half; the twenty for the package are untouched. **The `m` band is left alone and is now probably wrong** — it was set for packaging, and bootstrapping a publishable repository is not packaging. It is not re-banded here because `L-90` is exactly this: a band moved without a measurement, and plan is where the measurement comes from. |
| 2026-08-14 | (no change) | **The owner added phase 2 to the method — `R8` §3.1, steps 12–16 — so this task's subject grew a closing half.** The method ended at *raise child work* and the gap was already visible from the other side: the third table's last-but-two row says implementing is a measurement pass and the loop back belongs in the method. Phase 2 is that loop plus four things it does not do — pair every band against what it bought, report what remedies cost, feed the method's own rubric, and write standing policy only into documents that already govern. **It changes what the skill is**, from an instrument that reports to one that leaves a discipline behind. Recorded in `R8` §3.1 as the one operative home and cited from the scope here, not restated. **The `m` band is left alone rather than guessed at**: this task is still `proposed`, its own `specify` pass sizes it, and a band moved without a measurement is what `L-90` is about. |
| 2026-08-13 | (no change) | **The ship question is answered and it enlarges the task: published on GitHub as a token-saver audit skill, in its own right rather than inside the htmldeck plugin.** Three consequences are written into §1 rather than left to be met at review. The extraction test stops being a discipline and becomes the product test — a skill naming another repository's files is not installable. Its own load cost stops being self-discipline and becomes a promise every adopter pays on every session. And the publishing rules apply in full: no personal, client or machine data, the humanizer pass on what a stranger reads before installing, a licence, and out-of-the-box operation. A new question replaces the closed one: **it needs a repository, and that repository needs its own gate list** — `PUBLISHING.md` §8 is written for this one and does not travel. The effort stays `m` for the packaging; the repository is not sized here. |
| 2026-08-13 | → proposed | Raised at the owner's request, ahead of a session they have already planned, so the one run's evidence is not lost with the session that produced it. [T-130](T-130-audit-the-context-economy-of-an-agent-driven-repository.md)'s condition — *if and when the method survives being used once* — **is met**: it ran end to end and produced findings, a ranking, five child tasks and three corrections to itself. §1 records what the run says about the method rather than only that it ran, because that is the input a packaging task actually needs: steps 1–4 held, step 5 was thin, one band was wrong by four times, and the F3 line held under pressure. **Blocked on [T-136](T-136-re-run-the-external-research-with-a-recorded-search-record.md)** — packaging a method whose research half is known to be thin would set that defect in a form other projects copy, and T-136 is the fix already scheduled. `m`, and its own load cost is an acceptance criterion. |
