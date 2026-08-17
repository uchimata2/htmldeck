---
id: T-138
title: Make the portable half agent-agnostic, and classify the load path by who controls it
type: fix
status: done
phase: review
shipped_in: 0.3.0
parent: T-130
blocked_by: []
related: [T-130, T-135, T-136, T-137]
work_package: PH3
owner: the project owner
business_value: high
effort: s
created: 2026-08-13
updated: 2026-08-13
deliverables:
  - docs/research/R8-context-economy-for-coding-agents.md
---

# T-138 — Make the portable half agent-agnostic, and classify the load path by who controls it

## 1. Specify

**Outcome**
[`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
stops assuming one agent's configuration model, and gains the distinction that would have made this
audit's biggest wrong answer impossible: **who controls each load-path item.** Every mechanism detail
moves to part 2, where the machine and the agent are known.

**Why this exists**
Part 1 passes its own extraction test — it names no file of this repository — and **fails the spirit
of it**. `CE-07` and §10 currently carry the mechanism of one harness: a per-skill listing override, a
cloud-connector switch, a `plugin:skill` key form, and three null results measured against one
product's settings files. **An agent with no concept of a skill, a plugin or a connector reads that as
noise**, and an agent with different concepts reads it as wrong. The audit is expected to be run by
other agents entirely, on machines with other things installed.

**The distinction the method is missing**
Every load-path item has a **controller**, and the audit never asked who it was:

| Controller | Who can change it | What a finding against it means |
| :--- | :--- | :--- |
| **project** | anyone who clones the repository | actionable work, rankable as it stands |
| **user** | the person running the agent, across all their projects | actionable, but the cost lands outside this project — say so |
| **harness** | the agent, its vendor, or its account configuration | **may be unreachable**, and that is a *result*, not a low rank |

**This is the fix for the failure mode `CE-07` demonstrated.** Banded `L`, corrected to `S`, three
mechanisms and three scopes tried, all null. Without a controller field an audit converts *I cannot
reach this* into *this is not worth doing* — which reads identically in a ranking and is a completely
different fact. **A harness cost that is measured, attributed and marked unreachable is a finding**;
it tells the reader where their budget goes and who to ask.

**Scope**
- In: a **controller** classification in method step 1, applied to every load-path item.
- In: a fourth value on the finding record's `Applies to` field — `harness` — since the existing three
  cannot express *nobody in any project can change this*.
- In: rewriting `CE-07` and §10's null-results paragraph so part 1 states the *shape* — capability
  listings are paid per session, their addressability is harness-dependent and **must be measured
  rather than assumed** — and part 2 carries the mechanism, the key forms and the three nulls.
- In: a sweep of the rest of part 1 for the same assumption. *Skill*, *plugin*, *connector*,
  *tool schema* and *memory* are one product's vocabulary; the portable text needs terms an agent
  without them can still map onto its own.
- Out: dropping the detail. It is evidence and it belongs in part 2, which is exactly what part 2 is
  for.
- Out: writing an inventory procedure per agent. The method says *find your harness's mechanism and
  measure whether it worked*; enumerating agents would go stale and is the surveying problem
  [T-136](T-136-re-run-the-external-research-with-a-recorded-search-record.md) already has.
- Out: re-ranking. A controller field changes how a finding is read, not what the inventory measured.

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.2 — what a session working an audit finding owes beyond the finding: what to check, what to report, and where each thing goes. Read before starting
- [`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
  §2.1, §3 step 1, §6, §8 `CE-07`, §10
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §2.1 — where the mechanism detail lands
- [T-135](T-135-cut-the-load-path-this-project-cannot-use.md) — the three null results, and the only
  evidence that addressability has to be measured

**Acceptance criteria**
- [ ] Method step 1 classifies every load-path item by controller — `project`, `user`, `harness`
- [ ] `Applies to` accepts `harness`, and the field's description says what it means for ranking
- [ ] Part 1 contains no configuration key, file name, or setting mechanism belonging to any one agent
- [ ] Part 1's vocabulary is mappable by an agent that has no skills, plugins or connectors — each
      such term is either defined generically or replaced
- [ ] `CE-07` states the portable shape; the mechanism, key forms and three nulls are in part 2
- [ ] **The method says addressability is measured, not assumed**, and that an unreachable cost is
      reported rather than dropped
- [ ] A reader running a different agent can execute steps 1–11 without translating anything

**Open questions**
- ~~**Does `user` earn its own controller value, or fold into `harness`?**~~ **Settled 2026-08-14 by
  the implementer: three values, `user` keeps its own.** Folding it into `harness` would put a
  *reachable* cost in the same bucket as an unreachable one, which is the exact confusion the field
  exists to end — `CE-07` was banded on it. **Two live instances decide it rather than the argument
  alone**: `CE-10`'s subject is the memory index, which is the user's store and no clone's, and `T31`
  in the technique catalogue is a telemetry export the user enables on their own machine. Both are
  *someone present can do this, and it is not the repository's to ship*. A two-value split has no way
  to say that.

**Deviation from this specification, decided during `specify` and reported rather than handed back**
- **`Applies to` does not gain a `harness` value, and the controller becomes the eleventh field
  instead.** The scope line asked for both, and they would half-say the same thing in two places.
  They answer different questions: `Applies to` says **who implements the change** — and
  `upstream: <component>` already covers a change the harness's own vendor must make, which is what
  `CONTEXT-AUDIT.md` §7.3 exists for — while the controller says **who can reach the cost**. `CE-07`
  is `Applies to: any` *and* controller `harness` at the same time: every project pays it and no
  project can change it. **A fourth `Applies to` value would re-merge exactly the two questions this
  task was raised to separate.** What §6 owes instead is a sentence saying `<component>` may be the
  harness. The acceptance criterion is recorded `not met, by decision` in §4.

## 2. Plan

**The sweep has a boundary, and stating it is half the task.** Part 1's *method* and *findings* must
name no product. **Its evidence may** — §7.1's search record quotes the queries verbatim and §11 cites
what was read, and a bibliography with the product names filed off is not a portable document, it is a
false one. A search record you sanitize stops being a record.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | **Define the controller** as a new §2.2, beside the tier model — both are properties of a load-path item, and neither is a property of a finding until step 1 assigns it | Three values, with what a finding against each one means |
| 2 | **Wire it into method step 1**, which is where the load path is inventoried, and say **addressability is measured rather than assumed** | The step that would have caught `CE-07`'s band |
| 3 | **Make the controller the eleventh field of the finding record** (§6), and say `<component>` may be the harness. **No fourth `Applies to` value** — §1's deviation | A ranking that can express *unreachable* |
| 4 | **Write the field onto every existing finding**, in both halves, with a script that asserts each insertion matched once (**L-78**, **L-85**) rather than by hand across thirteen tables | `CE-07` `harness`, `CE-10` `user`, the rest `project` |
| 5 | **Rewrite `CE-07` to the portable shape** — capability listings are paid per session and their addressability is harness-dependent — and move the key forms, the scopes and the three nulls to `CONTEXT-AUDIT.md` §2.1 | Part 1 free of one product's mechanism |
| 6 | **Sweep the rest of part 1** for the same assumption: surface A's item list, the tier-2 row, step 1's list, §9's `P5`, and §1's own description of what this document is | Terms an agent without those concepts can map |
| 7 | **Verify by grep**, not by reading: no product or configuration-key vocabulary outside §7.1, §11 and the evidence notes that cite them | The criterion made checkable |
| 8 | **Review**, and reconcile in passing: `CONTEXT-AUDIT.md` §2.1's last re-measure is stale in both terms against today's measurement | Closure |

## 3. Implement

**Decisions & assumptions**
- **Three controller values; `user` keeps its own** — §1, settled on two live instances rather than on
  the argument — 2026-08-14.
- **`Applies to` did not gain `harness`. The controller became the eleventh field instead** — §1's
  deviation. The two answer different questions and a fourth value would re-merge them — 2026-08-14.
- **The controller is written on every finding, not only surface-A ones.** An omitted field defaulting
  to `project` is how `Risk` went blank in the first place; this document's own rule is that a value
  is written even when it is the boring one — 2026-08-14.
- **The thirteen insertions were made by a script that asserts each one matched once** (**L-78**,
  **L-85**), not by thirteen hand edits. It also refuses to run twice and fails if an `Applies to` row
  sits under no `CE-nn` heading. **Verified afterwards that it changed no line endings**: the file
  receiving only new rows shows `5 insertions, 0 deletions` — 2026-08-14.
- **The sweep's boundary is stated in the document itself**, not only in this task: the method and the
  findings name no product, **§7 and §11 do**. A technique with a name is named, a query is quoted as
  run, a source is cited as published. The line falls between *what you must do* and *what was found*
  — 2026-08-14.
- **Assumption worth double-checking:** the criterion *a reader running a different agent can execute
  steps 1–11 without translating anything* was checked by grep and by re-reading, both by the author of
  the rewrite. **It has not been read by an agent that lacks these concepts**, which is the only real
  test and is not available here. Recorded rather than claimed.

**Outputs produced**
- [`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
  §2.2 — **Controllers**, the new section: three values, why the field exists, addressability measured
  in both directions, and the two-attempt stopping rule
- §1 preamble — the agent-agnostic statement and where its exception falls
- §2 surface A, §2.1 tier 2, §3 step 1, §3.1 step 14, §9 `P5` — one product's vocabulary replaced by
  what the thing does
- §3 step 1 — inventories the controller, and says addressability is measured rather than assumed
- §6 — `Controller` is the eleventh field; `Applies to` gains the sentence that `<component>` may be
  the harness; the two are stated as deliberately separate
- §8 `CE-07` — retitled and rewritten to five portable points; the key forms, the scopes and the three
  nulls are gone from part 1
- All thirteen findings across both halves carry `Controller`: `CE-07` `harness`, `CE-10` `user`, the
  rest `project`
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §2.1 — receives `CE-07`'s mechanism, scopes
  and three nulls, and gains a fourth re-measure of the tier-1 bound because the third was stale in
  both terms

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Method step 1 classifies every load-path item by controller — `project`, `user`, `harness` | **met** | `R8` §3 step 1 inventories it alongside size; §2.2 defines the three values and what a finding against each means |
| `Applies to` accepts `harness`, and the field's description says what it means for ranking | **not met, by decision** | §1's deviation, decided at `specify` and reported rather than handed back. `Applies to` says *who implements*; `upstream: <component>` already covers a harness-vendor fix, and §6 now says so explicitly. **The controller — the eleventh field — says who can reach the cost.** A fourth `Applies to` value would re-merge the two questions this task exists to separate, and `CE-07` is `any` and `harness` simultaneously |
| Part 1 contains no configuration key, file name, or setting mechanism belonging to any one agent | **met** | Verified by grep, not by reading. Every remaining product name is inside §7 or §11 — the search record, the catalogue's named instances, and the bibliography — which §1 declares as the deliberate exception |
| Part 1's vocabulary is mappable by an agent with no skills, plugins or connectors | **met, with a stated limit** | Each term replaced by what the thing does: *the catalogue of capabilities the agent is offered*, *a packaged procedure*, *any persistent store the agent recalls from*. **The limit is in §3**: no agent lacking these concepts has read it, and that is the only real test |
| `CE-07` states the portable shape; the mechanism, key forms and three nulls are in part 2 | **met** | Five numbered points in `R8` §8; the evidence is `CONTEXT-AUDIT.md` §2.1, marked with the date it moved and why |
| The method says addressability is measured, not assumed, and an unreachable cost is reported rather than dropped | **met** | `R8` §2.2, twice — as the rule, and as the failure that produced it: two readings of one item, both wrong, in opposite directions |
| A reader running a different agent can execute steps 1–11 without translating anything | **met, with the same limit** | Steps 1–11 re-read end to end against the question. Step 1 was the only one carrying a translation cost and it is the one rewritten |

**On the criterion recorded `not met`.** It is not a shortfall — it is the specification being wrong in
a way only implementation exposes, and the alternative was two fields half-answering one question each.
The task's own §1 carries the argument; this row exists so the closure does not read as if seven of
seven passed.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-14 | → done | **`R8` §2.2 is the new section and the controller is the eleventh field.** Six of seven criteria met; **one recorded `not met, by decision`** — `Applies to` did not gain `harness`, because *who implements* and *who can reach* are different questions and `CE-07` answers them differently at the same time. The thirteen field insertions were scripted with a one-match assertion rather than hand-edited, and checked afterwards for line-ending damage. `CE-07` is retitled and reduced to five portable points; its key forms, scopes and three null results are now `CONTEXT-AUDIT.md` §2.1, where the machine is known. **Reconciled in passing**: that section's tier-1 re-measure was stale in both terms and now carries a fourth, dated. The one thing not verifiable here is recorded rather than claimed — no agent lacking these concepts has read the result. |
| 2026-08-14 | → in_progress | Eight steps, and the sweep's boundary is stated in §2: the method and the findings name no product, **the evidence may**. §7.1's queries are quoted verbatim and §11 cites what was read — sanitizing either would turn a record into an assertion, which is the defect `T-136` was raised to fix. |
| 2026-08-14 | → planned | See §2. |
| 2026-08-14 | → specified | The open question is settled — **three controller values, `user` keeps its own** — on two live instances rather than on the argument: `CE-10`'s memory index and the catalogue's `T31` are both *reachable, but not by anything a clone receives*. **And the specification is deviated from once, in §1**: `Applies to` does not gain `harness`, because that would re-merge *who implements* with *who can reach*, which is the split this task exists to make. The controller becomes the eleventh field instead. |
| 2026-08-13 | → proposed | Raised by the owner minutes after the audit was pushed, on the observation that **the skill will be run by other agents and on machines with other things installed**. Part 1 passes its extraction test and fails the spirit of it: `CE-07` and §10 carry one harness's mechanism — an override key form, a connector switch, three nulls against one product's settings files — which is noise to an agent with no such concepts and wrong to an agent with different ones. The fix is larger than a rewrite of two sections: the method never asked **who controls each load-path item**, and that omission is what let `CE-07` be banded `L` on a cost no project could reach. A controller field turns *unreachable* into a reportable result instead of a low rank, which is a different fact that currently reads the same. `s`, and it lands before [T-137](T-137-package-the-context-economy-method-as-a-skill.md) — packaging a method that assumes one agent would publish that assumption. |
