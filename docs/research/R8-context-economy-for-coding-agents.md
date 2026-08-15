# R8 — The context economy of an agent-driven repository

> **The operative method is now the `ecoctx` skill, and this is the research record it came from.**
> Packaged 2026-08-15 by [T-137](../../tasks/T-137-package-the-context-economy-method-as-a-skill.md)
> into its own repository, a sibling of this one. **A session that wants to *run* the method invokes
> the skill; this document is what to read to find out why a step says what it says.** The skill
> carries the sixteen steps, the rubric, the taxonomy and the eleven-field record; it does not carry
> §7's catalogue, §8's portable findings or §11's sources, which are evidence and stay here.
>
> **Declared rather than left inferred, because this method's own `F2` rule says so**: a rule with no
> declared home is copied by whoever needs it next, and two documents that both read as the method
> disagree the first time either changes. Where the two differ, **the skill is the method** and this
> document is a record of what it was on the day it was packaged.

**This document is portable and stands alone.** It carries the external research, the audit method as
numbered steps, the ranking rubric, and every finding that applies to any repository worked by a
coding agent. Copy it into another project and run it there; it names no file of the repository it
was written in as required reading, and it needs no companion document to be usable. The repository
it was first run on is called *the audited repository* throughout, and its figures appear only as
worked examples.

**What it is not.** It is not an executable procedure, and it does not implement anything. It ranks,
and someone else decides. Following it produces a list, not a change.

**It assumes no particular agent.** Where it needs a word for something an agent may or may not have,
it says what the thing *does* rather than what one product calls it — so a reader maps the term onto
their own harness instead of translating out of somebody else's. **The method and the findings name no
product. §7 and §11 do, deliberately, because they are the evidence** — a query is quoted as it was
run, a source is cited as it is published, and a technique is named where it has a name. Sanitizing
any of the three would leave a record that could no longer be checked, which is the defect §7.1 exists
to prevent.

**The line falls between *what you must do* and *what was found*.** If a sentence tells the reader to
act, it uses no product's vocabulary. If it tells them where something came from, it uses the name.

---

## 1. What is being audited

**Token efficiency, and nothing else.** Security, compliance, licensing, quality and correctness are
not searched for. What is noticed anyway goes in a byproduct register (§6.3) and is never ranked.

**The ranking axis is context runway** — how long a session runs before it compacts. Cost in money
follows from runway and is not the axis. Subject and axis are different questions: token efficiency
decides what may appear in the findings at all, runway decides the order once they are in. A finding
that saves tokens without lengthening the runway is still a finding, and it ranks below one that does
both.

**The written record is in scope, with one hard constraint: no fact loses its only home.** Layering
and load-on-demand are the instruments. Deletion is not. A finding whose gain depends on a rule
becoming unfindable, a gate weakening, or a lesson disappearing is recorded with that risk stated and
ranks below everything else.

---

## 2. The four cost surfaces, and the fifth thing that cuts across them

Every agent-driven repository has all four. An audit that skips one ranks the other three against an
unknown denominator.

| | Surface | What it holds | Why it is separate |
| :--- | :--- | :--- | :--- |
| **A** | **The load path** | What enters context without anyone asking — instruction files at every scope, any persistent store the agent recalls from, whatever is carried over from the last session, the catalogue of capabilities the agent is offered, the tool interface, and whatever the harness injects on its own | Paid on **every** turn of **every** session, so a saving here compounds against all the others. **Its items differ in who controls them** (§2.2) |
| **B** | **The read path** | What a session must read to do one unit of work — the specification, the conventions, the lessons, the board, the work item, its neighbours, the source it edits | Paid once per session, and it grows with the project's age |
| **C** | **Tool output** | What commands print back — gate reports, per-row verdict listings, test suites, search results | Paid per invocation, and the only surface where a tool's own default decides the cost |
| **D** | **Write volume** | What a session produces — work-item prose, log rows, commit messages, the reconcile edits a closure owes | Paid twice: once written, and again when the next session reads it as surface B |

**E — workflow and tooling** cuts across all four. When a gate must run rather than may, whether a
suite runs whole or targeted, whether exploration searches or reads, whether read-heavy work is
delegated, and how a session hands over. Its findings change *when* a cost is paid rather than how
large it is, so it is reported as its own section.

### 2.1 Tiers, and why surface A is the one with a budget

The most useful distinction this method inherited is **tiering**, and it comes with a membership rule
that is checkable rather than maintained:

| Tier | Loaded | Membership rule |
| :--- | :--- | :--- |
| 1 | every turn | **What the harness loads without being asked.** A property of the tree, not a list someone updates |
| 2 | when work of a kind starts | What a packaged procedure or workflow document pulls in when it activates |
| 3 | when a phase or mode begins | What tier 2 loads one at a time, for the branch actually taken |

**Only tier 1 gets a budget.** Tiers 2 and 3 are not paid on every turn, so a line limit there
measures the wrong cost; what constrains them is the load-one-at-a-time rule. Say this explicitly
rather than leaving it inferred — it is the visible cost of budgeting tier 1 alone, and it means the
tier-2 documents are allowed to grow.

**Express the budget as a relation, never as a constant.** A number and the arithmetic that justified
it are a pair that must be edited together, and the number always wins that argument by staying put
while the comparison drifts. Bound tier 1 against something else counted from the same tree — the
flat alternative the split replaced — so that re-measuring changes a measurement and leaves the rule
alone.

**A document that asserts a load discipline the harness does not implement is worse than one that is
over budget**, because it makes the budget unfalsifiable and content keeps being written into it on
the strength of a claim. Establish tier 1 by observation. Do not take a file's word for when it
loads.

### 2.2 Controllers — who can change a load-path item

**A tier says when an item is paid. A controller says who can stop paying it**, and they are
independent: the most expensive item on the load path can be the one nobody in the repository can
touch. Every item inventoried in step 1 gets one of three values.

| Controller | Who can change it | What a finding against it means |
| :--- | :--- | :--- |
| **project** | anyone who clones the repository | actionable work, rankable as it stands |
| **user** | the person running the agent, across all their projects | actionable, and **someone present can do it** — but the change lands outside the repository and no clone inherits it. Say so |
| **harness** | the agent, its vendor, or its account configuration | **may be unreachable, and that is a result rather than a low rank** |

**Why this is a field and not a remark.** Without it an audit converts *I cannot reach this* into
*this is not worth doing*, and those read identically in a ranking while being different facts. A
harness cost that is measured, attributed and marked unreachable is a **finding**: it tells a reader
where the budget goes and who to ask. One dropped to a low band tells them nothing and is never
revisited.

**Addressability is measured, never assumed — in both directions.** This method's own first run got it
wrong twice and in opposite directions on the same item: the largest single item on its load path was
first written off as untouchable by reasoning about where the files came from, then banded on the
whole of it once a setting was found, and the reachable share turned out to be about a ninth. **Write
a setting, restart, measure again.** A configuration schema documents what a key *means* and is silent
about which sources honour it at which scope.

**Two failed attempts is the signal to stop.** What survives is the boundary — which sources the
mechanism reached and which it did not — recorded so the next reader does not re-run the same tests.
That boundary is worth more than the tokens it failed to save.

**`user` earns its own value rather than folding into `harness`.** They differ in whether anyone in
the room can act, which is the entire purpose of the field.

---

## 3. The method — sixteen steps in two phases

Numbered because another project follows them verbatim. **Phase 1, steps 1–11, is the audit**: steps
1–4 are inventory and are **measured**; steps 7–9 are the gain and are **estimated**. **Phase 2,
steps 12–16, is what turns the audit into standing practice** and is described in §3.1.

*Phase 2 was added 2026-08-14 at the owner's direction. The method stopped at step 11 until then,
which the first run had already found insufficient from the other side: implementing the findings
produced material the audit had not seen, and it took a separate task to collect it.*

1. **Inventory the load path (A).** Everything that enters context unasked, with its size and **its
   controller** (§2.2). Whatever your agent calls them, look for: instruction or rule files at every
   scope; any persistent store the agent recalls from by itself; anything carried over from a previous
   session; **the catalogue of capabilities the agent is offered** — the name-and-description listing
   of whatever it can invoke, which is paid whether or not the project could use one; and how much of
   the tool interface is present before a tool is chosen. Establish membership **by observation**
   (§2.1), and **measure addressability rather than assuming it** (§2.2) — the item you cannot change
   still belongs in the inventory, marked.
2. **Inventory the read path (B)** for one representative unit of work, **chosen before the audit
   starts and named in the report**. Record what was opened, how much of it was needed, and how much
   was history rather than operative rule.
3. **Inventory tool output (C).** For each gate or command a unit of work runs, the size of what it
   prints on a **green** run. The failing case is rare and its verbosity is usually earned.
4. **Inventory write volume (D)** for the same representative unit.
5. **Research externally.** How practitioners reduce context and token use with coding agents.
   Produce a catalogue of *techniques*, each with what it costs and what it assumes (§7).

   **Record what was searched, and screen named tools as well as ideas.** A catalogue with no search
   record cannot be told apart from a short one, and the screening partition in step 7 then proves
   only that every gathered technique was judged — never that the gathering was adequate. So the
   catalogue carries: the queries run, the sources read, and an explicit statement that named tools
   in this space were looked for by name. **Two searches and two articles is a start, not a survey**,
   and a step-5 output that does not say which it was is claiming the second while doing the first.
6. **Read the local precedent.** Repositories where the same owner has already done this work are an
   input the internet cannot supply: they are proof a technique survived contact with how this owner
   actually works. **Patterns, structures and measurements only** — nothing is copied across, and no
   path, machine name or personal datum from them enters the report.
7. **Screen for applicability.** For each technique: **adopted**, **rejected**, or **deferred**. A
   rejection names the constraint it collides with; a deferral names what would close it. **The three
   are a partition, and a technique in none of them fails the audit** — a silent fourth category is
   how an account that looks complete gets shipped.
8. **Estimate gain and effort.** Bands, not numbers (§5).
9. **Rank.** Gain per unit of effort, with risk as a veto rather than as a term.
10. **Split.** Mark every finding *any project* or *this project*, and write the portable half so it
    stands alone.
11. **Raise child work** for the top of the ranked list — **at the owner's review, not before.**

    **Re-measure the inventory figure when the work starts, not when the row was written.** The
    subjects keep growing between ranking and implementation, and a saving computed against a stale
    denominator is not a measurement. *Added 2026-08-14 by phase 2, from three of thirteen: one
    finding's board grew 33,676 → 36,559 before its task began, one's share had already fallen from
    45% to 37.9% with the section itself unchanged, and one's was 61% at the audit and 69.0% on the
    day it was cut.* **A share is a ratio and the denominator usually moves faster than the
    numerator** — which is the same error as measuring the wrong unit, arrived at from the other side.

**Measure with a program, not by reading.** Opening a file to find out how big it is spends the exact
budget under audit. Sizes come off the filesystem; gate output is captured to a file whose length is
measured without printing it. The script is throwaway and belongs outside the repository.

**State the token conversion once and apply it uniformly.** Bytes divided by four is close enough for
English prose and markdown, costs no dependency, and must be labelled as an estimate. Never use it to
separate two findings that a byte count does not already separate.

### 3.1 Phase 2 — establish standing operation

**An audit is a measurement taken at one moment, and a repository that has been cleaned resumes
growing at the rate that produced the findings.** Phase 1 ends with work raised and, later, done.
Nothing in it makes the *next* year cheaper: the rules that would prevent regrowth are still in the
auditor's head, the bands that turned out wrong still read as right, and the technique catalogue
starts ageing the day it is written. Phase 2 is what converts one cleanup into an operating
discipline, and it runs **after the raised work is implemented**, not at ranking.

**Its standing risk, named first.** This is the phase where an audit becomes a **second policy author**
for a project it is a guest in — one that writes rules beside the project's own, in its own vocabulary,
with its own priorities. That is the `F2` family at the level of documents rather than sentences, and
it is committed by a well-meaning closing pass more often than by anything in phase 1. Step 16 exists
mostly to prevent it.

12. **Close the loop on every finding: predicted against measured.** Not a re-read of the findings —
    for each one implemented, the band it carried set against what it actually bought, with the
    original kept and the correction marked. **This is the only evidence that improves the next
    audit's rubric, and it is rarely a match.** From the first run: one finding understated itself
    twenty-fold, one was 48% wrong as a forecast of bytes, one saved no bytes at all and bought a
    gate instead, and one measured a unit that did not exist. **A withdrawn finding is a result and
    is reported as one**, not as a gap in delivery.
13. **Report what the remedies cost, not only what they saved.** Every remedy has a bill: a document
    that did not exist, a gate to run, a rule somebody now reads. Splits move bytes off the load path
    and usually **increase** the repository — a closing report that shows only savings teaches its
    reader that the method is free, and the first person to check the total concludes it failed.
    **Name any remedy that manufactured new work of another family**, such as a split that created
    duplication by giving content a new home while leaving the old statement in place.
14. **Reconcile the method's own practices against what this run did to them.** The run is a test of
    the rubric, the checklist and the record format. For each: did it hold, did it stay silent where
    it should have fired, did it fire where nothing was wrong. **The output is a change to the
    method**, not to the project — and the two must not be confused, because a project-specific
    finding written into the method is how a portable method acquires one repository's habits.
15. **Refresh the technique catalogue for what changed, with a search record.** Techniques in this
    space move faster than any repository does, so the catalogue's date is part of it. **Step 5's
    recorded-search rule applies here unchanged and is restated nowhere** — the queries run, the
    sources read, and an explicit statement that named tools were looked for by name. **Bound it to
    the delta**: this is *what is new since the audit's step 5*, not a second survey. A closing phase
    that re-runs step 5 in full is another audit wearing a different number.
16. **Write the standing policy into the documents that already govern, and nowhere else.** The
    output of phase 2 is a small number of durable rules. Four constraints on writing them, each of
    which this method has already paid for:
    - **Decide which document governs each policy before writing it.** A rule with no governing home
      is copied by whoever needs it next, and the copies are all written by people acting correctly.
      Where no document governs the act, *that* is the finding, and creating the home is the work.
    - **Price every policy against the load path the audit just cleaned.** A rule placed where it is
      read on every turn is paid on every turn — and that surface is usually the one phase 1 emptied.
      **An audit that closes by writing governance into the file it just cut has undone itself**, and
      the report will still show a saving.
    - **Check non-contradiction; do not intend it.** For each proposed policy, name the nearest
      existing rule and state whether it **extends**, **narrows** or **replaces** it. A replacement
      names its predecessor and edits it. An unmarked replacement leaves two live rules that disagree,
      which is precisely the defect the audit was measuring.
    - **The project's own policies win, and a collision is reported rather than resolved.** The method
      is a guest. Where a proposed policy collides with a rule the project has already settled, the
      project's rule stands and the collision goes in the report for its owner to rule on.

    **Leave at least one thing that re-measures without being asked** — a check that runs on an
    existing trigger the project already has, or an explicit statement that none is possible and why.
    A standing operation that depends on somebody remembering to look is not standing, and *review
    this annually* is that dependency with a date attached.

---

## 4. The finding taxonomy — five families

A walkable checklist with stable ids. **Walk it; do not skim it. A family with no finding against it
is a result and is reported as one.**

| | Family | What it looks for |
| :--- | :--- | :--- |
| **F1** | **What loads, and when** | Anything paid every turn that is needed on few of them. Dynamic and on-demand loading; separating operative instruction from historical narrative |
| **F2** | **Redundancy and contradiction in the record** | The same fact in several homes, or two statements that cannot both be current. Cumulative rules and their history consolidated into one consistent statement with no detail lost; stale and deprecated information; records the project does not own |
| **F3** | **Prose that is not doing work** | Text that neither states a fact nor decides a future question |
| **F4** | **Model work that should be deterministic** | Anything the model does per session that a program could do once. A script that lists or processes instead of the model reading and reasoning; installing an existing third-party component rather than re-deriving its behaviour; simplifying input and output structures **wherever no human reads them** |
| **F5** | **Tool and workflow economics** | When a cost is paid, rather than how large it is. Gate output volume on a green run; a gate that must run per task against one that may run per release; targeted runs against whole suites; delegating read-heavy exploration |

### 4.1 F3 needs a line drawn, and drawing it is part of the work

A project may keep rationale on purpose — a rule whose reason is lost gets undone by the next person
who finds it inconvenient. So the test is not *is this justification* but **does it decide anything
future**.

- **Decides something:** why a rule exists; what it cost to learn; what would close an excusal; what
  was rejected and why; the constraint a later change will collide with.
- **Decides nothing:** a defence of a choice nobody is contesting; the same reason restated in a third
  place; an account of how carefully the author worked.

**An F3 finding that cannot name what the prose would stop deciding is not a finding, and is recorded
as rejected.** F3 is the family that can damage a record, and this is the guard rail against
declining to draw the line.

**There is a second guard rail, and it comes first: prove the bytes you counted are prose.** The test
above assumes that much, and a share-of-file figure does not establish it. Comment markers, quote
styles and block delimiters are proxies for *kind*, and each one holds until a file uses that syntax
for something else — a template, a fixture, an embedded payload. **Count by the structure that
defines the unit** (a parser's own notion of a docstring or comment, not a regular expression over
quotes), **name that unit in the sentence reporting the share**, and check the counter against a
small case whose answer is known by construction before reading its output as a finding. *Written
2026-08-14, after this method's own F3 finding survived ranking, publication and citation in five
documents on a count of triple-quoted string tokens: the file it named as 85% prose is 3.2% prose and
the lowest in its tree, and the relocation it proposed would have deleted a tool's payload. An F3
finding is the one most likely to be acted on destructively, which is why its measurement gets the
strictest reading rather than the loosest.*

**Relocation beats deletion.** The strongest F3 result is usually an F1 move: rationale keeps its
home, in a document the operative path does not load.

---

## 5. The ranking rubric

**Estimate the gain; do not measure it.** Measuring a saving requires building it, which is the work
the ranking exists to decide on.

| Band | Meaning |
| :--- | :--- |
| `XL` | removes more than about a third of a session's cost **on the surface it names** |
| `L` | roughly a tenth to a third |
| `M` | a few per cent |
| `S` | under a per cent, or unquantifiable but real |
| `enabler` | it saves nothing and makes a later saving decidable. **Its gain is the finding it unblocks, named** |
| `bimodal` | it costs one surface to save another. **Both figures are stated, and the trade is argued rather than netted** |

*The last two were added 2026-08-14 by phase 2. The table had four values and the first run used six —
`CE-11` was banded `enabler` and `CE-13` `bimodal` at ranking time, because no listed band can express
a finding whose gain is not a saving. **Two of thirteen findings carried a band this table did not
define**, which is a rubric staying silent where it should have fired.*

A band is always read against its own surface: `L` on the load path and `L` on the read path are
different quantities, and the finding record says which.

**The band prices the finding. It does not price the remedy, and the remedy is where a ranking goes
wrong.** In the first run, eleven of thirteen bands missed — four on magnitude, three on the *shape*
of the change, one on its direction, one on a false premise. **Every error was in the `Change` cell,
never in the `Finding` cell**: the inventory said where the weight was and was right each time; the
proposed remedy said what removing it was worth and was wrong more often than not.

Two rules follow, and they are the first run's whole return on this section:

- **`Change` is a hypothesis and is read as one.** It is written with the same authority as `Finding`
  and does not deserve it. **Re-measure a remedy before carrying it out, and let the measurement
  refuse it** — four rows were refused exactly this way, and a ranking obeyed instead would have
  deleted two tools' payloads, rebuilt one finding on a timer, and split a small document into four
  smaller ones.
- **The inventory is what survives.** *Only the saving is banded* already said this; what the run adds
  is that it is the load-bearing half of the rubric rather than a caveat on it. A finding whose
  inventory figure is sound and whose remedy is refused is **still a good finding**.

Effort uses whatever scale the project already has for work items. **Inventory figures from steps 1–4
are measurements and are stated as measurements; only the saving is banded.** A band with no
inventory behind it is a guess wearing a table.

**Risk is a veto, not a term.** A finding that costs a fact its only home does not get ranked higher
by being cheap.

---

## 6. The finding record

Operative or it is decoration. Every finding carries all eleven fields, and a reader must be able to
act on it without the audit's author present.

*It was ten until 2026-08-14, when `Controller` was added. Records written before that date say ten
and are correct about themselves.*

| Field | What it holds |
| :--- | :--- |
| `CE-nn` | the id — stable, cited from child work and from other projects reusing this method |
| Surface | A, B, C, D or E |
| Family | F1–F5 |
| Finding | what is costing, stated as a fact about the repository |
| Change | what to do |
| Gain | a band, with the inventory figure it rests on |
| Effort | the project's own scale |
| Risk | what it could cost. **`none` is a legitimate value and must be written** |
| Applies to | `any`, `this project`, or `upstream: <component>` — **who implements the change.** `<component>` may be the **harness itself**, when the fix has to be made by the agent's own vendor |
| Controller | `project`, `user` or `harness` (§2.2) — **who can reach the cost.** A different question from `Applies to`, and the pair is not redundant: a finding can be `any` and `harness` at once — every project pays it and no project can change it |
| Source | external research, local precedent, or this audit |

**The record has no field for what the finding actually bought, and it should not gain one.** Phase 2
had to reconstruct thirteen outcomes from **80,721 bytes** across fourteen closed task records, which
is the most expensive step in the method. A twelfth field would be paid by every finding to serve one
step that runs once. **What the closure owes instead is one line** — the measured outcome, in the
record that already exists, written on the day it is known. The rest is derivable: id, band, task and
status all come out of the project's own tracker. *Added 2026-08-14 by phase 2.*

*`Controller` is the one field this run cannot report on: it was added on the last day, after every
finding had closed. It is untested rather than held.*

**`Applies to` and `Controller` are deliberately two fields.** Merging them was considered and
rejected: one says who does the work, the other says whether the work is possible from here, and a
single field forces the answer to one of them to be a guess. **The failure this pair prevents** is a
real one from this method's first run — an unreachable cost was silently re-read as an unimportant
one, and a low band is where a finding goes to be forgotten.

### 6.1 One numbering space, one statement per finding

`CE-nn` ids are allocated once across both halves of the audit. **Each finding is stated in full in
exactly one document** — here if it is `any`, in the project's own report if it is `this project` —
and the project's ranked table lists every id wherever it is stated. An audit about redundancy that
prints its findings twice has answered its own question.

### 6.2 Three audiences, because a finding is implemented where its subject lives

The split is by **who can act on it**, not by what it is about.

| Audience | Where it is reported |
| :--- | :--- |
| **Any project** | The portable half — this document |
| **This project** | The project's own report, ranked |
| **Upstream** | The project's own report, in its own section: components the project *uses* but does not own |

**The upstream section is written to be handed over and is not implemented locally.** Two things it
owes: **read the upstream backlog before proposing**, because their own precedent outranks the
argument that arrived with the finding; and remember that a handed-over item carries the sender's
labels — its priority is a guess about someone else's project, so state the observation and let them
place it. Say in each entry whether their backlog was read.

### 6.3 The byproduct register

Checking every file for one thing means seeing other things. Record them; keep them out of the
ranking.

- Anything noticed that is not token efficiency — a defect, a stale claim, an inefficiency of another
  kind — goes in a register at the end of the project's report, with the file and what was seen.
- It is **never ranked, never banded, and never becomes a `CE-nn`.** Mixing them would put an unranked
  observation into a list someone is using to buy work.
- A register entry that is really a defect is raised as its own work item at review, and the register
  row then points at it.

**Read the register for a shape, not only row by row — at step 12, once the run is over.** *Added
2026-08-14 by phase 2, and it is the register's largest return in the first run.* Eight defects
surfaced in passing, each recorded as an unrelated row, and **six of the eight are one class: text a
reader follows and no checker reads** — a link label stating a wrong path beside a working target, a
bare `§n` cross-reference left behind by an extraction, a citation of an id that was never allocated,
a dangling pointer in a store outside the tree. Row by row they are eight small defects. As a class
they are a gap in what the project's gates can see at all, which is worth a work item and no single
row was. **The register is where a whole-repository sweep leaves its evidence; nothing else in the
method ever reads it back.**

---

## 7. The technique catalogue

Gathered in step 5. Each row is a *technique*, with what it costs and what it assumes — screening it
is step 7 and belongs to the project doing the audit, not to this catalogue.

### 7.1 The search record

**Step 15, 2026-08-14 — the delta window is empty, and no search was run.** Phase 2 owes *what is new
since step 5*, bounded to the delta. Step 5 was re-run to declared saturation on **2026-08-14**, the
same day, so the window between the baseline and this refresh is **zero days** and there is nothing in
it. Running the queries again would return the rows below and would be the third full survey of a
catalogue that has had two — which step 15 names and forbids: *a closing phase that re-runs step 5 in
full is another audit wearing a different number.*

**This is a null result with a reason, not a step skipped.** The distinction matters because the two
are indistinguishable from outside a year later, and only one of them means the catalogue is current.
**What would make step 15 real work is elapsed time and nothing else** — the next phase 2 over this
catalogue searches the window from 2026-08-14 to its own date, on the three axes below and under the
same stopping rule. *The catalogue's date is part of the catalogue*, which is this step's own premise,
and today that date and this refresh's date are the same.

**Re-run 2026-08-14 under step 5's coverage rule, which this is the first pass to satisfy.** The
first pass was two searches and two articles; this one is 23 searches and one fetched page, along
three axes, and **named tools were searched for by name** — that is the statement step 5 requires, and
the queries below are what makes it checkable rather than assertable.

**The stopping rule is declared saturation, per axis**: an axis stops when a full round of queries on
it returns no technique the catalogue does not already carry. **The rounds that returned nothing new
are listed too** — they are the evidence an axis stopped for a reason rather than at a budget. A
survey cannot be proved complete (§10), so the rule is deliberately of the weaker kind.

| Axis | Round | Queries | New techniques |
| :--- | :--- | :--- | :---: |
| **A — ideas, articles, papers** | A1 | `context engineering techniques reduce token usage coding agents 2026` · `agent context window management compaction sub-agent memory research paper` | 3 |
| | A2 | `code execution with MCP agents write code instead of tool calls token savings` · `MCP server tool schema token bloat reduce number of tools loaded` | 3 |
| | A3 | `TOON token-oriented object notation compact serialization vs JSON tokens` · `llms.txt AGENTS.md repository map for AI agents convention` | 2 |
| | A4 | `context rot long context degradation agent accuracy shorter context better` · `semantic code search vs grep for coding agents retrieval effectiveness` | **0 — saturated** |
| **B — named tools, by name** | B1 | `Repomix gitingest code2prompt pack repository into single file for LLM token count` · `Serena MCP server semantic code tools LSP symbol level editing token efficient` · `Aider repo map tree-sitter token budget Cursor codebase indexing Cline memory bank` | 3 |
| | B2 | `agent rule before writing code "already in the standard library" decision ladder plugin token reduction measured` · `Claude Code skills plugins subagents context cost ccusage measure token usage per session` · `Cline Roo Code context condensing memory bank token optimization named tool` | 1 |
| | B3 | *fetched*: the independent Ponytail benchmark · `Amp Sourcegraph Goose OpenHands opencode agent context management token efficiency` · `SpecKit BMAD claude-task-master spec-driven development context files token cost` | 1 |
| | B4 | `"Claude Context" MCP semantic search codebase Zilliz context7 library docs on demand` · `Continue.dev Windsurf Cascade Augment Code context engine token efficiency named` | **0 — saturated** |
| **C — the harness's own mechanisms** | C1 | `Claude Code documentation context editing microcompact tool search skills progressive disclosure official` | 1 |
| | C2 | `Anthropic context editing memory tool API clear tool uses automatic context management` · `Claude Code /usage command attributes usage to skills subagents plugins MCP servers percentage` | 3 |
| | C3 | `Claude Code OpenTelemetry metrics token usage per session monitoring instrumentation` · `enforce agent rules with deterministic linters hooks instead of prompt instructions token cost` | **0 — saturated** |

**Axis B is the one the first pass never ran at all**, and it is where the two known gaps came from.
It is also where the largest correction came from: the tool behind `T20` is **Ponytail**, and its own
figures and an independent benchmark's disagree by about four times — see the row.

**One query returned a negative result, and it is recorded because negatives are results.** C2's
second query tested a secondary source's claim that the harness attributes recent usage to individual
skills, subagents, plugins and MCP servers. **It did not confirm against primary documentation.** The
claim is therefore *unverified* and no row rests on it; what would close it is the harness's own
documentation or a run of the command. The mechanism that *is* documented by several independent
sources is `T31`.

**What this record cannot do** is prove the survey complete — only show what it covered, so a reader
who thinks an axis stopped early can see the queries and judge. That asymmetry is the whole reason
step 5 asks for a record rather than a coverage claim (§10, fifth limit).

### 7.2 The catalogue

| # | Technique | What it does | What it costs | What it assumes |
| :--- | :--- | :--- | :--- | :--- |
| T1 | **Right-altitude system prompts** | Keeps always-loaded instruction specific enough to guide and short enough not to spend the attention budget | Tokens proportional to detail; verbose instruction competes with the task | Clear direct language guides behaviour without enumerating every edge case |
| T2 | **Just-in-time retrieval over preloading** | The agent holds lightweight identifiers and loads content at runtime | Slower than pre-computed retrieval; needs tool design good enough to stop the agent chasing dead ends | Metadata — paths, names, conventions — carries enough signal to choose well |
| T3 | **Progressive disclosure in three stages** | Discovery loads a name and description; activation loads the body; execution loads referenced files | A structure to maintain, and a description good enough to route on | The unit of knowledge can be split so the common case stops at stage one |
| T4 | **Tool-set curation** | Removes tools the project does not use from the turn cost | Judgement about what is needed; a wanted tool may be absent | If a human engineer cannot say which tool applies, the agent cannot either |
| T5 | **Deferred tool schemas** | Tool *names* load; schemas load on demand | An extra round trip when a schema is needed | The name is enough to decide relevance |
| T6 | **Tool-result clearing** | Drops tool output from history once it has served its purpose | Minimal; described as the lightest form of compaction | Historical output is not needed for later reasoning |
| T7 | **Compaction, in tiers** | Summarizes history at the context limit and reinitializes. **Restated 2026-08-14:** production harnesses tier it — clearing stale tool results with *no* model call, a full summarizing call, and a call skipped entirely by reusing notes already extracted | Can lose subtle context whose importance appears later; the cheap tier can only drop, not summarize | Summarization preserves decisions and open threads, and the cheapest tier is tried first |
| T8 | **Structured note-taking / external memory** | Persistent notes outside the window, retrieved when needed | Discipline to structure notes; they must be consulted | The agent reliably reads its own notes across resets |
| T9 | **Sub-agent delegation** | Isolated context windows for focused work, returning a condensed summary | Orchestration complexity and latency; the summary is lossy | The work decomposes into independent exploration |
| T10 | **Scoped requests over broad retrieval** | Naming the files instead of describing the need | The requester must know which files | The relevant set is knowable up front |
| T11 | **Prompt caching** | Static content first, so repeats hit cache | Ordering discipline | The prefix is genuinely stable |
| T12 | **Output discipline — diffs not files** | Asks for the change, not the artifact | Diffs are harder to read wrong-in-place | Output tokens cost several times input |
| T13 | **Module summaries** | A short summary at the head of a unit, read instead of the unit | Must be kept true, or it lies cheaply | A summary answers the common question |
| T14 | **Code minification for agent input** | Strips non-essential lexical elements, preserving semantics | Breaks line references and human readability | No human reads that copy |
| T15 | **Adaptive context pruning** | Drops low-relevance context as the session runs | Needs a relevance signal; can drop something needed | Relevance is estimable in flight |
| T16 | **Model routing** | Cheaper model first, escalate on need | Escalation costs a retry | The cheap model can recognise its own limit |
| T17 | **Planner → implementer → reviewer** | Splits a task across phases so the expensive model runs briefly | Handover overhead; each phase must record enough for the next. **Measured 2026-08-14 and it is not small**: the spec-driven frameworks in this genre re-read spec, plan and task files every turn, and one comparison budgets **20–40% higher spend** than working without them, another ~31,700 tokens per workflow run | The phases can hand over in writing, and the correctness bought exceeds the re-reading paid |
| T18 | **Fresh context per checklist item** | A loop restarts context for each item | Loses cross-item learning | The items are genuinely independent |
| T19 | **Evidence quoted forward** | An earlier phase records verbatim quotes and `path:line` refs so a later phase greps instead of re-reading | The earlier phase writes more | The later phase would otherwise re-read whole files |
| T20 | **Generation restraint — a decision ladder before writing code** | A rule set the agent applies before generating: does this need to exist, is it already in the codebase, in the standard library, a native platform feature, an installed dependency, a one-liner — and only then, write it. **Named 2026-08-14: this is Ponytail**, an installable skill with adapters for some fourteen agents | Its own instructions are a permanent load-path cost; a minimalism rule pointed at output that is *meant* to be rich fights the brief. **And the effect is about four times smaller than advertised** — see below | The saving is in what the agent does not write, and the domain rewards less code |
| T21 | **Semantic index over the repository** | A vector or embedding index of the project's own documents and code, queried for the few relevant passages instead of loading files. Named instances: hybrid BM25-plus-dense-vector code search shipped as an MCP server | An index to build, host and keep fresh; a stale index answers confidently and wrongly. **Measured 2026-08-14**: about **+12.5% answer accuracy** and roughly **40% fewer tokens at equal retrieval quality** — but *on large, heterogeneous corpora*; on a small plain-text corpus lexical search is reported faster and more precise | A service or library dependency is acceptable, and **the corpus is large enough that retrieval beats naming files** — which is the assumption that decides it, not the accuracy figure |
| T22 | **Code execution over tool calls** | The agent writes code that imports and calls tools in a sandbox; loops, retries and intermediate data stay there, and only the result enters context | A sandbox, a code-generation surface and a security boundary; a failure is now a program's failure | The tools are expressible as an importable API, and the caller controls the tool layer |
| T23 | **On-demand tool retrieval** | One search tool replaces N schemas: the agent queries for the few tools it needs and their definitions arrive then | An extra round trip, and a relevance miss is a tool the agent never learns exists | Tool descriptions are searchable, and the name alone does not have to carry the decision |
| T24 | **Token-oriented serialization** | A compact encoding of the same data — indentation and tabular rows instead of braces, brackets and repeated keys | A translation layer, and a format fewer readers know | The payload is uniform enough to tabulate, and no human reads that copy |
| T25 | **A compression proxy in the path** | A component between agent and model that shrinks tool output, logs and file contents before they arrive | Another component that can drop the one line that mattered; the saving is lossy by construction | A proxy may sit in the path, and the agent's inputs are redundant enough to compress |
| T26 | **Server-side context editing** | The API clears stale tool results and thinking blocks itself, **after the cache lookup**, so the saving does not cost the cache prefix that `T11` depends on | Beta surface; the decision of what is stale is not the caller's | You control the API call, and a cleared result will not be needed verbatim later |
| T27 | **Symbol-level retrieval** | A language server answers at symbol granularity: a read returns one function body, an overview returns signatures rather than implementations | A language server per language, and a dependency the project must accept | The artifact has a symbol graph — which prose does not |
| T28 | **A ranked repository map on a token budget** | A generated map of the repository's public surface, ranked by how often each symbol is referenced elsewhere, serialized to a fixed token budget | A parser and a build step; the ranking is approximate and a wrong map misdirects cheaply | The corpus has a reference graph, and a fixed budget of map is worth more than the same budget of file |
| T29 | **Whole-repository packing with a token report** | A tool concatenates the filtered repository into one model-ready file and reports the token count per file and in total | It maximizes load rather than reducing it; the report is the part that survives contact with a budget | The corpus fits, or only the measurement is wanted |
| T30 | **Deterministic enforcement instead of instruction** | A rule that can be checked mechanically moves out of the always-loaded prompt into a hook, linter or gate the harness runs | The rule must be mechanically checkable; a check that needs judgement costs tokens wherever it lives | The harness exposes lifecycle points, and the rule's cost in the prompt is paid every turn |
| T31 | **Session telemetry as the instrument** | The harness exports per-session tokens, cost and cache hit rate over OpenTelemetry, so what a session *paid* is measured rather than inferred from file sizes | A collector and a backend to run; it measures, it does not reduce | Telemetry may be enabled, and the question worth answering is what was spent, not what was available |
| T32 | **Addressable recall** | Tool observations go to an append-only, ID-addressable log and are replaced in context by compact citations the agent can dereference | A store and an addressing scheme; the agent must actually re-fetch | The citation carries enough to decide whether the body is needed |
| T33 | **A curated entry index for machine readers** | One published, hierarchical map of what to read — a root instruction file, a base layer, and a task-active layer — so the reader spends its budget on content rather than on discovery | Keeping the index true; an index that lies costs more than the discovery it saved | Readers honour the index instead of crawling |
| T34 | **A capped reasoning budget** | The thinking allowance is bounded per turn or per task | Hard problems lose the depth that would have solved them | The budget is settable, and the cap is above what the work needs |
| T35 | **Version-pinned documentation retrieval** | Library documentation for the exact version in use is fetched on demand instead of carried, vendored or recalled from training | An external service in the loop at authoring time | The project has third-party dependencies whose documentation it would otherwise carry |

**T19 came from local precedent rather than the literature**, and it is the one most easily missed: it
does not reduce a document, it moves a cost from an expensive phase to a cheap one.

**T20 and T21 were added 2026-08-13, after the first pass missed both**, and they are no longer
provisional: the 2026-08-14 re-run confirmed both and restated both. They are recorded here with
their provenance because *how* they were missed matters more than that they were: T20 is a named,
installable tool that reports its own measurements, and T21 is a mainstream technique the first pass
folded into T2 rather than listing. **A reader found both by asking one question.** See §3 step 5's
coverage rule, which exists because of this, and §10's fourth limit.

**T20's own figures and an independent benchmark's disagree by about four times, and the gap is the
lesson.** The skill advertises **−54% code, −22% tokens, −20% cost, −27% time**. A paired benchmark
of **80 tasks**, inside a programme of 251 billed trials, measured **−15% code** (p = 0.088, which is
not significant), **−10.3% cost** (p = 0.004, which is) and **−11% time**; quality was unchanged on 65
of 80, slightly worse on 9 and slightly better on 6. **The effect is not spread evenly**: it reaches
**−31% on big builds** and is **zero where the plain agent already wrote almost nothing**. So the
technique is real, is smaller than claimed, and pays only where a lot of code was going to be written
— which is a different question from whether it is worth its permanent load-path cost. **A tool that
publishes its own measurements is still publishing its own measurements** (**L-98**).

**T22 to T35 were gathered 2026-08-14 by the axes in §7.1.** Six of the fourteen came from the
by-name axis and would not have been found by searching for ideas: the technique has a product name
before it has a literature.

---

## 8. Findings that apply to any repository

Stated in full here; ranked in the auditing project's own report. Figures name *the audited
repository* — the first project this method was run on — and are illustrations, not required reading.

### CE-01 — The always-loaded instruction file carries the project's narrative history

| | |
| :--- | :--- |
| **Surface / Family** | A / F1 |
| **Finding** | The file the harness loads unasked accumulates a chronological record — what shipped when, which release carried which fix, which task found which defect. In the audited repository that narrative was **6,980 of 15,630 bytes, 45% of a tier-1 file paid on every turn of every session**. It grows by a paragraph per release and never shrinks |
| **Change** | Split the section. Operative rules that must bind before the agent knows what kind of work this is stay in tier 1; the chronology moves to a dated history document nothing loads by default. **Extract the rules first** — narrative paragraphs written over time embed real rules, and moving the section wholesale loses them |
| **Gain** | `L` on the load path — the audited repository's tier 1 measured 27,633 bytes (~6,900 estimated tokens) across three files, and the chronology is roughly a fifth of it |
| **Effort** | `s` for the move; the extraction is the work |
| **Risk** | A rule that lived only inside a narrative paragraph loses its home. Mitigated by moving rather than deleting, and by reading the section for rules before cutting it |
| **Applies to** | `any` |
| **Controller** | `project` - The repository's own files and tools |
| **Source** | this audit; local precedent (§9, P1) |

### CE-02 — The generated board is read whole because the tool that answers the query is unreachable

| | |
| :--- | :--- |
| **Surface / Family** | B / F4 |
| **Finding** | A tracker that generates a full index into the repository also ships commands that answer the two questions a session actually asks — *what next* and *what does this item point at*. When those commands do not resolve in an agent shell, sessions read the generated index instead. Measured in the audited repository: the index **33,676 bytes** against **1,901 bytes** for the open-item listing and **790 bytes** for one item's context — **17.7× and 42×** |
| **Change** | Ship a wrapper that locates the installed tool and exposes those commands, and point the workflow document at it. Where a project already has such a wrapper for its validators, this is one more entry point in a file that already solves the locating problem |
| **Gain** | `L` on the read path — ~7,900 estimated tokens per session that consults the board, which is most of them |
| **Effort** | `xs` |
| **Risk** | `none` — the wrapper adds an entry point and changes no data |
| **Applies to** | `any` |
| **Controller** | `project` - The repository's own files and tools |
| **Source** | this audit |

### CE-03 — A gate prints its whole verdict listing on a green run

| | |
| :--- | :--- |
| **Surface / Family** | C / F5 |
| **Finding** | Per-rule gates default to printing one row per rule whether or not anything failed. Measured in the audited repository: **17,391 bytes (~4,300 estimated tokens), 169 lines, on a passing run** of the deck gate — more output than the whole-repository release gate produces (8,233 bytes), and a session runs it repeatedly |
| **Change** | Add a quiet mode printing failures plus a one-line summary. **Keep the full listing as the default** — a person reading a green run is why it exists — and let the agent pass the flag |
| **Gain** | `L` on tool output, per invocation |
| **Effort** | `xs` |
| **Risk** | A quiet green run hides a rule that silently stopped being checked. Mitigated by keeping the count of rules evaluated in the summary line |
| **Applies to** | `any` |
| **Controller** | `project` - The repository's own files and tools |
| **Source** | this audit |

### CE-04 — One cumulative rule, five homes, one of them tier 1

| | |
| :--- | :--- |
| **Surface / Family** | A+B / F2 |
| **Finding** | A rule learned the hard way gets written where it was learned, then restated wherever it might be needed. In the audited repository one such rule occupied five documents — the always-loaded instructions, the workflow document, the board preamble, the public readme, and the lessons file — with the tier-1 copy the longest of the five, because it carried the incident that produced it |
| **Change** | One operative statement in the document that governs the behaviour, one lesson entry holding the incident and the reason, and **pointers everywhere else**. The tier-1 copy is the one to shorten first: it is the copy paid on every turn, and it is usually the one carrying the story |
| **Gain** | `M` on the load path per rule, and rules of this kind accumulate |
| **Effort** | `xs` per rule |
| **Risk** | A pointer is weaker than a statement — a reader who does not follow it acts without the rule. Keep the *rule* in tier 1 and move only the incident |
| **Applies to** | `any` |
| **Controller** | `project` - The repository's own files and tools |
| **Source** | this audit |

### CE-05 — A large appendix inside the document everyone is told to read first

| | |
| :--- | :--- |
| **Surface / Family** | B / F1 |
| **Finding** | The specification a project points new sessions at grows a per-work-item decision table, and the table outgrows the specification. Measured in the audited repository: **66,461 of 108,163 bytes — 61% — in one section, 112 rows of which 68 were struck through as completed** |
| **Change** | Move the decision table to its own document, leaving the specification the size of a specification. Completed rows go to a history file; the open phase stays where a planner will meet it |
| **Gain** | `XL` on the read path for any session that reads the specification |
| **Effort** | `m` |
| **Risk** | The per-row rationale is a real decision record and must keep its home. Check what else keys on the document — a duplicate-index check pinned to that file by name will follow the content to its new home and fire there, correctly, unless the rule that excuses it moves too |
| **Applies to** | `any` |
| **Controller** | `project` - The repository's own files and tools |
| **Source** | this audit |

### CE-06 — A citable unit of knowledge kept in one growing file

| | |
| :--- | :--- |
| **Surface / Family** | B / F1 |
| **Finding** | Lessons, rules or decisions cited individually by id but stored in one document force a session that needs one of them to load all of them. Measured in the audited repository: **152,444 bytes (~38,000 estimated tokens) in 81 entries, mean 1,873 bytes** — a session needing one entry pays 81× |
| **Change** | One file per citable unit, plus a generated one-line index. The id stays the address; only its storage changes |
| **Gain** | `XL` on the read path when an entry is cited, which is most sessions |
| **Effort** | `m`–`l` — every existing citation must still resolve, and any reference checker must be taught the new shape |
| **Risk** | Cross-entry reading gets harder: a person browsing for a pattern loses the single scroll. Mitigated by the generated index carrying each entry's one-line hook |
| **Applies to** | `any` |
| **Controller** | `project` - The repository's own files and tools |
| **Source** | this audit |

### CE-07 — The capability catalogue is paid every session for capabilities a project never uses

| | |
| :--- | :--- |
| **Surface / Family** | A / F5 |
| **Finding** | Agents are offered a catalogue of what they can invoke, and its name-and-description listing enters context every session whether or not the project could ever use an entry. Measured on the audited machine: **55 entries, 20,941 bytes, ~5,200 estimated tokens per session** — comparable to the whole always-loaded instruction set, and mostly for capabilities irrelevant to the repository at hand |
| **Change** | Narrow the catalogue to what the project can use. **Look for the mechanism that keys on an entry's own name rather than on where it was served from** — the two are different questions and an audit that reasons from where the files live answers the wrong one |
| **Gain** | **`S`, corrected from `L` after measurement.** The listing is large; the *addressable* part was about a ninth of it. **Band the reachable share, never the surface** |
| **Effort** | `xs` to attempt, and it may take more than one attempt |
| **Risk** | A capability that would have helped is silently absent. Mitigated because the same mechanism adds one back, and because a setting that keeps the name and drops the description may cost about a tenth while staying discoverable |
| **Applies to** | `any` |
| **Controller** | `harness` - The listing is supplied by the harness. Three mechanisms at three scopes reached about a ninth of it and nothing else moved — measured, attributed, and not addressable by the project paying for it |
| **Source** | external research (T4); this audit |

**This is the finding the controller field was built for**, and it is stated here as a shape rather
than as one product's settings. *The key names, the scopes tried and the three null results were in
this document until 2026-08-14; they are evidence about one machine, so they moved to the audited
repository's own report, where the agent and the machine are known.*

**The shape, which any agent's reader can act on.**

1. **The listing is paid per session and is usually the largest single item on the load path** that
   the project did not write.
2. **Its addressability is harness-dependent and must be measured, not assumed** (§2.2). Two readings
   of the same item were both wrong here — first *untouchable*, then *all of it* — and the truth was
   about a ninth.
3. **The mechanism, where one exists, keys on what an entry is called and not on where it came from.**
   Reasoning from where the files live is what produced the first wrong answer.
4. **A configuration schema says what a key means and is silent about which sources honour it at which
   scope.** Write the setting, restart, measure again.
5. **After two failed attempts, stop and record the boundary** — which sources the mechanism reached
   and which it did not. That is the finding when the saving is not.

Three lessons, and the third is the one that costs most to learn late:

- **An entry's delivery mechanism and its listing cost are different questions.**
- **Estimate the addressable share, not the surface.** A gain band is a claim about *reachable*
  saving; `L` was an honest reading of the listing's size and a careless one of what could change.
- **Two failed experiments is the signal to stop, not to try a third.** Each attempt cost a restart of
  someone else's environment, and the boundary that survives is worth more than the tokens were.

### CE-08 — A measured figure that lives only in the handover chain

| | |
| :--- | :--- |
| **Surface / Family** | A / F2 |
| **Finding** | A handover document is written to be consumed once, so a fact placed in it is copied to the next one rather than re-derived. Measured in the audited repository: a run-time figure for the release gate appeared in **five successive handover files, none of which had a durable home for it**; measuring it took 154 seconds and returned **a third of the figure being carried** |
| **Change** | A figure that will be quoted belongs in the durable document that owns the subject, dated, with the command that reproduces it. A handover may point at it. **This is the handover discipline that already exists — the handover points, it does not store — applied to numbers, which is where it is easiest to break** |
| **Gain** | `S` in tokens, and its value is accuracy rather than size |
| **Effort** | `xs` |
| **Risk** | `none` |
| **Applies to** | `any` |
| **Controller** | `project` - The repository's own files and tools |
| **Source** | this audit |

---

## 9. Local precedent — what to look for in a repository that already did this

Step 6 reads repositories where the same owner has already optimised for context. Six patterns
carried over, each stated as a structure rather than as a file.

| | Pattern | What it is | What it buys |
| :--- | :--- | :--- | :--- |
| **P1** | **Stub, canon, depth** | A tiny per-agent instruction file points at one agent-neutral canonical document, which points at heavy references | One copy of the rules for several agents, and the heavy material out of the always-loaded path. **Note honestly**: the stub itself saves little — the layer below it is what saves |
| **P2** | **One file per lifecycle phase** | Workflow split into a small file per phase, each with preflight, do, do-not, close | A session in one phase loads that phase. Measured in precedent: 1.2–7 KB per phase against a single document several times larger |
| **P3** | **Rationale in its own document** | The *why* separated from the operative steps and cited from them | The F3 tension resolves without deleting anything: reasons keep a home the operative path never loads |
| **P4** | **Evidence quoted forward** | A planning phase records verbatim signatures and `path:line` refs so the audit phase greps instead of re-reading | The expensive re-read never happens. This is T19 |
| **P5** | **One body, thin per-agent front-ends** | The portable package lives once; each agent gets a ~1–2 KB adapter naming only what differs for it | No drift between agents, and no duplicated body |
| **P6** | **Spine plus one branch, never both** | A core document declares which branch file a mode loads, and a run loads exactly one | Confirmed by observation during this audit: resuming loaded the spine and one flow, and never touched the other flow or the tracker binding — **10 KB present, 7 KB of binding and 6 KB of the other flow not paid** |

**Nothing is copied across.** Patterns, structures and measurements only, and no path, machine name or
personal datum from a precedent repository enters the report.

---

## 10. What this method cannot see

Stated so a reader does not mistake the audit's silence for a clean bill.

- **It measures artifacts, not sessions.** File sizes are what a session *could* pay. What it actually
  paid needs harness instrumentation this method does not require. *Restated 2026-08-14: that
  instrumentation exists and is documented — per-session tokens, cost and cache hit rate over
  OpenTelemetry (`T31`). **So this limit is now a choice rather than an impossibility**, and a method
  that keeps it should say why. The reason to keep it is that artifact sizes are the thing a
  repository can change; a session total mixes them with how the session was driven.*
- **It cannot separate operative prose from narrative mechanically.** Section sizes are measured; the
  split inside a section is a reader's judgement, and every F1 or F3 finding resting on one says so.
- **It does not price attention.** A shorter context is assumed better. Where a cut would make the
  agent guess, that is a risk field, not a measurement.
- **A green gate proves the gate ran, not that the saving is safe.** Every finding here is a proposal
  for someone to review.
- **The screening partition says nothing about the catalogue's completeness.** *Adopted + rejected +
  deferred = every technique gathered* is an arithmetic check on step 7, and it reads like a coverage
  claim. It is not one. **Demonstrated on this document's first pass**: the partition summed
  correctly over nineteen techniques while two were missing, including a named tool that publishes
  its own measurements. Step 5's coverage rule is the guard, and it is weaker than the partition —
  a search record can be read and judged, but nothing can prove a survey complete.
  **And the size of the gap is now measured.** The re-run under the coverage rule, 2026-08-14, brought
  the catalogue to **35**. The partition summed correctly, and read as complete, over **nineteen of
  them** — *the arithmetic was right about a bit over half a catalogue.* A check that passes at 54%
  coverage while reading as a coverage claim is not a weak check; it is a check of something else.

---

## 11. Sources

**Grouped by the axis that found them (§7.1).** The first eight are the 2026-08-13 pass; everything
under the axis headings is the 2026-08-14 re-run.

### 11.1 The first pass

- [Effective context engineering for AI agents — Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Context is a budget: eight levers and three workflow patterns — foojay.io](https://foojay.io/today/context-is-a-budget-eight-levers-and-three-workflow-patterns/)
- [Context engineering: why AI coding agents spend most of their tokens reading, not writing — Moderne](https://www.moderne.ai/blog/context-engineering-why-ai-coding-agents-spend-most-of-their-tokens-reading-not-writing)
- [Just-in-time context for AI agents: a runtime discipline — TrueFoundry](https://www.truefoundry.com/blog/jit-context-just-in-time-context-agents)
- [Progressive disclosure in AI agents — MindStudio](https://www.mindstudio.ai/blog/progressive-disclosure-ai-agents-context-management)
- [Context engineering for coding agents: CLAUDE.md, AGENTS.md and token budgets — CodeSmith](https://www.codesmith.in/post/context-engineering-claude-md-agents-md)
- [Reducing token usage of state-in-context agents using minification](https://arxiv.org/pdf/2606.01326)
- [SWE-Pruner: self-adaptive context pruning for coding agents](https://arxiv.org/pdf/2601.16746)
- Local precedent: two repositories of the same owner, read for structure under step 6 and
  deliberately unnamed.

### 11.2 Axis A — ideas, articles, papers

- [Code execution with MCP: building more efficient agents — Model Context Protocol discussion](https://github.com/modelcontextprotocol/modelcontextprotocol/discussions/1780)
- [SEP-1576: mitigating token bloat in MCP — schema redundancy and tool selection](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1576)
- [MCP compression: preventing tool bloat in AI agents — Atlassian](https://www.atlassian.com/blog/development/mcp-compression-preventing-tool-bloat-in-ai-agents)
- [TOON — Token-Oriented Object Notation](https://toonformat.dev/), and its [benchmark against JSON](https://arxiv.org/abs/2603.03306)
- [Addressable recall compaction for long context-window control](https://arxiv.org/html/2607.25066)
- [Classifier context rot: performance degrades with context length](https://arxiv.org/html/2605.12366v1)
- [llms.txt — making a project discoverable to agents](https://www.agentpatterns.ai/standards/llms-txt/) and [the AGENTS.md hierarchical standard](https://agentsstandard.com/)
- [Improving the agent with semantic search — Cursor](https://cursor.com/blog/semsearch) and [grep vs. RAG for agents — LlamaIndex](https://www.llamaindex.ai/blog/is-grep-all-you-need-lexical-vs-sematic-search-for-agents)

### 11.3 Axis B — named tools, searched by name

- [Ponytail — the decision-ladder skill](https://mcpservers.org/agent-skills/dietrichgebert/ponytail), and **the independent benchmark that measured it**: [Ponytail skill for Claude Code, tested — JetBrains](https://blog.jetbrains.com/ai/2026/07/ponytail-skill-claude-tested/)
- [Serena — LSP-backed semantic code toolkit](https://github.com/oraios/serena)
- [Aider's repository map](https://aider.chat/docs/repomap.html)
- [Repomix — pack a repository into an AI-friendly file](https://repomix.com/)
- [Claude Context — code search MCP server](https://github.com/zilliztech/claude-context)
- [Cline's Memory Bank](https://docs.cline.bot/best-practices/memory-bank)
- [BMAD vs Spec Kit vs OpenSpec — the spend comparison](https://reenbit.com/bmad-vs-spec-kit-vs-openspec-choosing-your-spec-driven-ai-framework/)
- [A directory of terminal-native coding agents and harnesses](https://github.com/bradAGI/awesome-cli-coding-agents) — where the compression-proxy layer behind `T25` was found

### 11.4 Axis C — the harness's own mechanisms

- [Context editing — Claude Platform Docs](https://platform.claude.com/docs/en/build-with-claude/context-editing) and [Managing context on the Claude Developer Platform](https://claude.com/blog/context-management)
- [Agent Skills overview — Claude Platform Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Steering Claude Code: CLAUDE.md, skills, hooks, subagents](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more) and [output styles](https://code.claude.com/docs/en/output-styles)
- [Claude Code monitoring with OpenTelemetry — SigNoz](https://signoz.io/docs/claude-code-monitoring/) and [the same, via CloudWatch — AWS](https://aws.amazon.com/blogs/mt/analyzing-claude-code-usage-with-cloudwatch-and-opentelemetry/)
