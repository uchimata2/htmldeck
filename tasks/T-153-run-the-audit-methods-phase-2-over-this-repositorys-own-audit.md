---
id: T-153
title: Run the audit method's phase 2 over this repository's own audit
type: audit
status: done
phase: review
parent: T-130
blocked_by: []
related: [T-130, T-137, T-157]
work_package: PH3
owner: the project owner
business_value: medium
effort: l
created: 2026-08-14
updated: 2026-08-14
shipped_in: 0.3.0
deliverables: []
---

# T-153 — Run the audit method's phase 2 over this repository's own audit

## 1. Specify

**Outcome**
The context-economy audit stops at its own last closure and instead **grades itself**: every finding's
predicted band paired against what it actually bought, what the remedies cost, the method's rubric fed
from how it behaved, and standing policy written into the documents that already govern. **The method
is [`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
§3.1, steps 12–16**; it is not restated here.

**Why it exists as a task at all.** Phase 2 runs **once**, after the raised work is implemented, and
until 2026-08-14 nothing scheduled it — the obligation was a paragraph in
[`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §9 depending on the next session reading §9.
That is the shape that became [T-152](T-152-give-look-at-the-rendered-deck-one-operative-home.md) the
day before, and this project does no work without a task file.

**The trigger fired on 2026-08-14: every finding in §6 now has a closed task.**
[T-148](T-148-give-a-measured-figure-a-durable-home.md),
[T-149](T-149-prune-the-memory-index-of-spent-entries.md) and T-152 closed in one session, and
`python tools/docs/findings.py` is what reports it rather than a count anyone keeps.

**What it is blocked on, and what it is deliberately not blocked on.** `T-136` re-runs the external
research with a recorded search record and **can still raise a finding**, which would change the
ranking phase 2 grades; `T-138` repairs the portable half phase 2 reasons from. Those two, and nothing
else. **The rest of the execution order is ordinary backlog** — the ruler, the source cluster, the
motion tasks — and reading it as the condition would park this behind eighteen tasks it has no
relation to. *§9 said "blocked behind six" against the old, wider reading; corrected the same day.*

**Scope**
- In: the five things `R8` §3.1 steps 12–16 name. That document is the operative statement.
- In: the correction record. Four findings in this audit had their band or shape refused by the
  measurement — `CE-07` `L`→`S`, `CE-02` understated twentyfold, `CE-06` saved no bytes and bought a
  gate, `CE-12` measured a unit that did not exist — and phase 2 is where that becomes rubric input
  rather than four separate notes.
- In: what the remedies **cost**, including the case this audit has already met twice: the repository
  ends *larger* while the load path ends smaller.
- Out: raising new findings. `CE-nn` closed at thirteen; anything phase 2 turns up is an ordinary task
  or a `T-136` finding, not a fourteenth row.
- Out: T-137's packaging. Phase 2 produces the evidence; that task carries it outward — and what this
  teaches the *method* goes to [T-137](T-137-package-the-context-economy-method-as-a-skill.md) §1,
  which is the only home that survives these sessions.
- Out: step 16's temptation. **An audit is a guest**: a policy names its governing document, carries an
  extends/narrows/replaces verdict, and yields to the project's own with the collision reported. `R8`
  §3.1 says so and this task does not soften it.

**Inputs**
- `R8` §3.1 — the five steps, which are the specification
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.2 — read before starting, as every audit
  task does; it is the **per-closure** half of this phase rather than a substitute for it
- `python tools/docs/findings.py` — the ranking and its outcomes, derived; do not re-assemble it
- The fourteen closed task records' §3 and §4 — where each band met its measurement

**Settled at `specify`, 2026-08-14**

**Five outputs, four homes, and step 14 is the reason they are not one home.** The temptation is to
write the whole phase into `CONTEXT-AUDIT.md` because that is where the audit lives. Steps 14 and 15
grade the **method**, not this repository, and a method finding written into this repository's audit
is how a portable method acquires one repository's habits — which is the defect step 14 names in its
own text.

| Step | Output | Home |
| :-- | :--- | :--- |
| 12 | every finding's band against what it bought | `CONTEXT-AUDIT.md` — a new section |
| 13 | what the remedies cost, including where the repository grew | same section |
| 14 | what the run taught the rubric, the checklist and the record format | `R8` §3.1/§5/§6, and [T-137](T-137-package-the-context-economy-method-as-a-skill.md) §1 |
| 15 | the catalogue delta since step 5, with a search record | `R8` §7 and §7.1 |
| 16 | standing policy | the documents that already govern, and nowhere else |

**Steps 12 and 13 go in `CONTEXT-AUDIT.md`, not in a new document.** A separate file would be reachable
only through a pointer from §6, which is one more statement to keep true, and the grade belongs beside
the ranking it grades. The growth objection stands but names the wrong surface: `CONTEXT-AUDIT.md` is
**tier 3, loaded by nothing** ([`../CLAUDE.md`](../CLAUDE.md), *What loads every turn*), and tier 3
carries no budget by that document's explicit ruling. The cost is paid by whoever opens it — surface B
in `R8` §2, not surface A — and that is the trade being made rather than one being overlooked.

**The band is `l`, and it moved on a measurement rather than on a re-reading** (**L-90**).

- Step 12's input is §3 and §4 of the fourteen finding records: **80,721 bytes**, measured 2026-08-14.
  Reading those records whole would be 210,783 — **the sections are 38% of them, and the whole record
  is not the unit.**
- `R8` and `CONTEXT-AUDIT.md` are **64,242** and **64,638** bytes and both are read in part. Step 14
  adds `T-136` and `T-138`, which are not finding records and are not in the 80,721.
- Step 15 is a **live search with a recorded search record**, bounded to the delta. Step 16 writes into
  at least three governing documents and owes **a check that re-measures without being asked**.
- The comparison that decides it: [T-154](T-154-bind-the-measurements-that-five-live-documents-state-in-prose.md)
  was `m` and moved five documents and one tool, with no search pass and no new gate. This is that plus
  a search pass, plus a new gate, plus 80 KB of reading before the first edit.

*`m` was a first estimate from the step count, made when the task was raised. It is kept legible here
because §6.2's correction rule applies to a band this task carries as much as to one it grades.*

**Acceptance criteria**
- [ ] Written at `specify`, from `R8` §3.1 rather than from this section
- [ ] Every finding's band is paired against what it bought, **with the original band kept legible**
      (§6.2's correction rule)
- [ ] The remedies' cost is stated, including where the repository grew
- [ ] The catalogue refresh is **bounded to the delta** since step 5 and carries a search record — the
      queries run, the sources read, and the statement that named tools were looked for by name
- [ ] Any standing policy names its governing document and carries an extends/narrows/replaces verdict
- [ ] No standing policy lands on surface A. A rule written into the file phase 1 cut is the audit
      undoing itself, and the report would still show a saving
- [ ] **Something re-measures without being asked**, on a trigger the project already has — or an
      explicit statement that none is possible, and why. *Review this annually* is not one
- [ ] What the method learned is in T-137 §1, not only here

**Open questions**
- **Does step 16 earn a new gate, or a statement that none is possible?** — the implementer, at
  `plan`. A gate is a standing cost on every release and this project holds that a check forbidding a
  design choice is a defect in the check; `R8` §3.1 allows either answer and requires the reason
  either way.
- *Answered at `specify`:* the `m` band did not survive — see **Settled at `specify`** above.

## 2. Plan

**Steps 1–3 are step 12–13, 4 is step 14, 5 is step 15, 6–7 are step 16.** The numbering is this
task's; `R8` §3.1 keeps its own and is the specification.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Read **§3 and §4 only** of the fourteen finding records — 80,721 bytes, not the 210,783 the whole records are — and record per finding: the band it carried, what it measurably bought, and the correction where they differ. `python tools/docs/findings.py` supplies the band and the outcome; the *bought* column is the part no tool has | a working table, input to steps 2 and 4 |
| 2 | Write the pairing into `CONTEXT-AUDIT.md` as a new section, **original bands kept legible** and each correction marked. A withdrawn finding is a result, not a gap — `CE-12`/`T-150` is the one | `R8` step 12 |
| 3 | Price the remedies in the same section: bytes off the load path against bytes added to the repository, plus every gate, document and rule the run created. **Name any remedy that manufactured work of another family** | `R8` step 13 |
| 4 | Reconcile the method against this run — the rubric, the checklist, the record format — one verdict each: held, stayed silent where it should have fired, or fired where nothing was wrong. Four bands were refused by measurement (`CE-07`, `CE-02`, `CE-06`, `CE-12`) and that is rubric input, not four notes | edits to `R8` §3/§5/§6, and T-137 §1 |
| 5 | Refresh the catalogue **for the delta since step 5 only**, with the search record step 5's rule requires — queries run, sources read, named tools looked for by name, and the rounds that returned nothing. T-136 set the form on 2026-08-14 and it is the baseline, not a thing to redo | `R8` §7 and §7.1 |
| 6 | Draft each standing policy with three things attached: the document that governs it, its price on the load path, and an **extends / narrows / replaces** verdict against the nearest existing rule. Collisions go to the owner unresolved | `R8` step 16 |
| 7 | Answer §1's open question — a check on a trigger the project already has, or the written reason none is possible | a tool, or a recorded refusal |
| 8 | Close per [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §7: §4 verdicts, the `RELEASE-PHASES.md` row folded to two cells, the execution order renumbered so T-157 takes `next`, lessons as `L-nn`, `lint.py` | closure |

**What is deliberately not a step.** Re-reading `CONTEXT-AUDIT.md` §6 for findings — the ranking is
closed and step 12 grades it rather than revisiting it. Raising a fourteenth `CE-nn` — §1's Out scope.
Sending anything upstream — that is [T-157](T-157-hand-the-upstream-registers-to-their-owners.md),
which this task unblocks.

## 3. Implement

### Steps 1–3 — `R8` steps 12 and 13, done 2026-08-14

**Two of thirteen findings held as written.** Four were wrong about magnitude, three about shape, one
about its premise, two were costs by design, and one undercounted the subject it measured. The table
is [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §10.1 and is not repeated here.

**Decisions & assumptions**
- **The pattern is one sentence and it is `T-147`'s, not a new one** — 2026-08-14. *A finding says
  where the weight is; it does not know what removing it is worth.* It was written after three
  consecutive shape refusals and it holds across all thirteen: **every row that was wrong was wrong
  about the value or form of the remedy, never about the location of the cost.** The inventory was
  sound; the forecasting was not, and it was not close. Writing a second formulation of it would be
  `CE-04` in the audit's own report.
- **The corollary is the part with teeth** — 2026-08-14. Four rows were refused by a measurement taken
  *while implementing them*. A ranking obeyed rather than re-measured would have deleted two tools'
  payloads, rebuilt `CE-05` on a timer, and split one small document into four smaller ones. **The
  rank was useful and obeying it would have done damage** — that is a statement about how a ranking
  should be *used*, and it belongs to the method (step 4).
- **The tier-1 arc is stated net, and the peak is kept** — 2026-08-14. 15,630 at the audit, **19,035**
  at its peak, 15,208 now: **−422 bytes, −2.7% net, after a peak 21.8% above where the audit found
  it.** Reporting only the −4,118 that `CE-01` and `CE-04` cut would be true and would teach the
  reader that the method is free, which is exactly what step 13 exists to stop.
- **The audit's own remedies are most of the growth it then had to cut** — 2026-08-14. `CE-11` +2,690
  and `CE-13` +322 are 3,012 of the 3,405 bytes tier 1 gained. That is `R8` step 16's warning
  committed **before step 16 existed to name it**, and it is legible only because both records priced
  it at the time.
- **The 96-byte disagreement is recorded, not resolved** — 2026-08-14. §9 says the pair took
  `CLAUDE.md` to 14,821; T-144's record measures 14,917 the same day. Neither is reproducible now.
  **L-97**'s rule is that a figure nothing owns drifts, and inventing a winner here would be a third
  unowned figure.

### Steps 4–6 — `R8` steps 14, 15 and 16, done 2026-08-14

**Decisions & assumptions**
- **Step 14's output went to `R8` and to T-137 §1, and none of it came here** — 2026-08-14. That is
  the step's own rule and it is the easiest one to break: a method finding written into this
  repository's audit is how a portable method acquires one repository's habits.
- **The rubric was under-specified and the first run proved it in the field** — 2026-08-14. `enabler`
  and `bimodal` were invented at ranking time because the four-value table cannot express a gain that
  is not a saving. **Two of thirteen findings carried a band the rubric did not define.** Both are in
  `R8` §5 now, with the reason.
- **The record does *not* gain a twelfth field** — 2026-08-14. Step 12 reconstructed thirteen outcomes
  from 80,721 bytes and the obvious fix is an `Outcome` field, paid by every finding to serve one step
  that runs once. **The closure owes one line instead**, in the record that already exists. The cheap
  answer and the tidy answer disagree here, which is why it is written down.
- **Step 15 ran and found an empty window, which is a result rather than a skipped step** —
  2026-08-14. Step 5 was re-run to declared saturation the same day by `T-136`, so the delta is **zero
  days**. Re-searching would be the third full survey of this catalogue, which step 15 forbids by
  name. `R8` §7.1 records the null with the condition that makes it real work next time: elapsed time
  and nothing else.
- **Step 16 produced one local policy, and it collides** — 2026-08-14. Almost everything belongs to
  the method; **an audit is a guest and a guest leaving ten house rules has misread the job.** The one
  local rule — the tier-1 bound should be measured rather than remembered — cannot be implemented
  without breaking either step 16's *do not write governance into the file you just cut* or
  `CLAUDE.md`'s *a figure about this file cannot be corrected anywhere else*. **Both are the project's
  own, both are right, and step 16 says the collision goes to the owner unresolved.**
- **The standing re-measure is therefore not delivered, and it is written down as not delivered** —
  2026-08-14. *Review this annually* is the failure step 16 names; a policy blocked on one decision is
  not an improvement on it. Recorded in `CONTEXT-AUDIT.md` §10.4 rather than softened.

**The closing pass wrote a duplicate lesson, and caught it by checking rather than by remembering.**
The ranking result was drafted as a new `L-100` — *a ranking is right about where the cost is and
wrong about what removing it is worth* — which is **`L-90`'s title almost word for word**. `L-90` was
written by the three tasks whose shapes were refused and already carries *treat the proposed change as
a hypothesis and the finding as an observation*. **What phase 2 adds is the population, not the
rule**: 2 of 13 rather than 3 of 3. Deleted, and `L-90` gained the measurement instead. *This is
`CE-04`'s mechanism — a rule with no declared home is copied by whoever needs it next — operating on
the audit's own closing pass, which is the second time in this audit a duplicate was created inside a
pass raised to remove them.* The category set is three and the draft invented a fourth; `lessons.py`
refused both problems in one run.

**Two observations, neither a finding.** `figures.py` reports the tier-1 figures as **unanchored**,
among 413 — the number governing what every session pays is checked by nobody. And it reports a live
drift in `README.md`'s pasted `refcheck` output (2,485 → 2,562 pointers) at **exit 0**, which reads as
deliberate: those counts move on every commit and failing on them would block every release.

**Outputs produced**
- [`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
  — §5 gains `enabler` and `bimodal` plus the two rules the run returns (`Change` is a hypothesis; the
  inventory is what survives); §3 step 11 gains the re-measure obligation; §6 rules out a twelfth
  field and marks `Controller` untested; §6.3 gains *read the register for a shape*; §7.1 records
  step 15's null delta
- [T-137](T-137-package-the-context-economy-method-as-a-skill.md) §1 — a sixth row set, six rows,
  written with every outcome known
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §10 — §10.1 the pairing, §10.2 the pattern and
  its corollary, §10.3 the cost: the tier-1 arc, the five remedies that grew the repository, the four
  standing gates, the price of a withdrawal, the `F2` duplicate one remedy manufactured, and the eight
  defects found in passing that no row could have forecast, and §10.4 the one local policy with its
  collision reported unresolved

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Written at `specify`, from `R8` §3.1 rather than from this section | met | §1's *Settled at `specify`* is built from the five steps and their four homes, and it changed the band |
| Every finding's band is paired against what it bought, **with the original band kept legible** | met | [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §10.1, thirteen rows. `CE-07` shows ~~L~~ → S, `CE-04` shows `xs` **each** |
| The remedies' cost is stated, including where the repository grew | met | §10.3 — the tier-1 arc net **−422 bytes after a peak 21.8% above the start**, five remedies that grew the repository with their byte counts, four standing gates, and the price of the one withdrawal |
| The catalogue refresh is **bounded to the delta** and carries a search record | met | `R8` §7.1. **The window is zero days** — step 5 was re-run to saturation the same day — so the record is a null with its reason and the condition that makes it real next time |
| Any standing policy names its governing document and carries an extends/narrows/replaces verdict | met | One policy, one governing document (`CLAUDE.md`, *What loads every turn*), verdict **extends**. §10.4 |
| No standing policy lands on surface A | met | None landed anywhere. The one that would have is the collision, and refusing to write it is the criterion doing its job rather than an omission |
| **Something re-measures without being asked**, or an explicit statement that none is possible and why | **not met** | The statement that can honestly be written is *blocked on one owner decision*, which is **not** *none is possible*. Recorded unsoftened in §10.4 and raised as [T-158](T-158-measure-the-tier-1-bound-instead-of-remembering-it.md) |
| What the method learned is in T-137 §1, not only here | met | A sixth row set, six rows — the only one written with every outcome known |

**Seven of eight met, and the eighth is the interesting one.** Phase 2 was supposed to end by leaving
a check that runs by itself. It could not, and the reason is worth more than the check: **every route
is cheap and each is forbidden by a different rule this project has already settled** (**L-100**). The
subject is the one number governing what every session pays, it drifted 174 bytes since the previous
task closed, and nothing noticed — so the gap is real and the fix is one decision wide.

**What this task did not do, deliberately.** It raised no `CE-nn` — §1's Out scope, and `CE-nn` closed
at thirteen. It sent nothing upstream, which is
[T-157](T-157-hand-the-upstream-registers-to-their-owners.md), now unblocked. It did not re-run step 5.

**Rule 6 and the close gate.** Nothing this task produced renders — the outputs are five documents and
a task record — so [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §7 step 3 has no subject here. Said
explicitly rather than left unmentioned, because a closure that is silent about it looks like one that
skipped it.

**Child fix tasks raised**
- [T-158](T-158-measure-the-tier-1-bound-instead-of-remembering-it.md) — the standing re-measure this
  task owed and could not deliver. `s`, and its open question is the collision, which is the owner's.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-14 | → done | **Phase 2 ran once and the audit is closed.** Seven acceptance criteria met, one **not met** and raised as [T-158](T-158-measure-the-tier-1-bound-instead-of-remembering-it.md). The headline is §10.1: **two of thirteen bands held as written**, and every error was in the `Change` cell rather than the `Finding` cell — the inventory was right thirteen times out of thirteen. Four rows were refused by a measurement taken while implementing them, so **the rank was useful and obeying it would have done damage**, which is **L-90**, now carrying the measurement over all thirteen. Step 13 is stated net rather than gross: tier 1 ended **−422 bytes, −2.7%** against a peak **21.8% above** where the audit found it, and `CE-11` and `CE-13` — the audit's own remedies — are 3,012 of the 3,405 bytes it then had to cut. Step 15 found an empty window and recorded it as a result. Step 16 produced one local policy and reported its collision unresolved, which is **L-100**. `T-157` is unblocked and takes `next`. |
| 2026-08-14 | → planned | **Eight steps, and the ordering constraint is that step 1 feeds two later steps rather than one.** The per-finding table built for the pairing is also the rubric's input, so reading the records twice is the thing the plan is shaped to avoid. Steps 5 and 6–7 are separable from 1–4 and from each other, which matters because this is an `l` and the phase does not have to land in one session. **One consequence of the band move worth recording:** the generated board sorts by value against effort, so `l` puts T-153 below tasks the execution order places behind it. The board is not the execution order — [`../docs/RELEASE-PHASES.md`](../docs/RELEASE-PHASES.md) is — and this is the second time that gap has had to be said out loud. |
| 2026-08-14 | → specified | **Both questions §1 posed are answered, and one of them changed the band.** The pairing goes in `CONTEXT-AUDIT.md` rather than a new document — it is tier 3, loaded by nothing, so the growth is surface B and paid by whoever opens it; a separate file would be reachable only through a pointer that has to be kept true. **`m` → `l`, on a measurement**: step 12's input is §3 and §4 of the fourteen finding records, **80,721 bytes** against 210,783 for the whole records, and on top of it a live search with a record, three governing documents, and a check that has to re-measure by itself. The deciding comparison is T-154 — an `m` that moved five documents and one tool with no search pass and no new gate. **What `specify` added beyond the band** is that the five steps have four homes and not one: steps 14 and 15 grade the *method*, and writing them into this repository's audit is the exact defect step 14 is about. Three acceptance criteria added — the search record, the *no policy on surface A* constraint, and the standing re-measure — because §1 as raised covered steps 12, 13 and half of 16. One open question left, and it is the implementer's at `plan`: whether step 16 earns a gate or a written reason there can be none. |
| 2026-08-14 | (unblocked) | **`T-138` closed. `blocked_by` is empty and this task is now runnable** — both repairs to the method have landed. What phase 2 will grade has changed shape since the condition was written: the catalogue it prices is 35 rather than 21, and the finding record it feeds gained an eleventh field, `Controller`, which is the rubric's first way of saying *nobody here can reach this cost*. `CE-07` is the row to check that against, since it is the reason the field exists. |
| 2026-08-14 | (blocker cleared) | **`T-136` closed and raised no finding**, so the ranking this task grades has stopped moving — the exact condition §1 named. `blocked_by` is `T-138` alone now. The catalogue it will price is larger than the one that was ranked: 21 → 35, with fourteen techniques screened for the first time, so phase 2 grades a screening whose denominator moved even though no band did. `CONTEXT-AUDIT.md` §4.1 is the argument for the null result. |
| 2026-08-14 | → proposed | Raised at the owner's direction once the trigger fired: the last three findings closed in one session, so every row in `CONTEXT-AUDIT.md` §6 has a closed task. **Not a finding** — `CE-nn` closed at thirteen and this is the method's own phase, so it takes an ordinary task id. Blocked on `T-136` and `T-138` alone; the wider reading in §9, *blocked behind six*, counted ordinary backlog as the condition and was corrected the same day. It sorts last while blocked, so raising it changes nothing about what to work on next — it stops the obligation depending on a paragraph being re-read. |
