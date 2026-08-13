---
id: T-138
title: Make the portable half agent-agnostic, and classify the load path by who controls it
type: fix
status: proposed
phase: specify
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
- **Does `user` earn its own controller value, or fold into `harness`?** They differ in who can act,
  which is the whole point of the field — but a two-value split is simpler and this project has one
  user. — the implementer, from the rule's own reason.

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
| 2026-08-13 | → proposed | Raised by the owner minutes after the audit was pushed, on the observation that **the skill will be run by other agents and on machines with other things installed**. Part 1 passes its extraction test and fails the spirit of it: `CE-07` and §10 carry one harness's mechanism — an override key form, a connector switch, three nulls against one product's settings files — which is noise to an agent with no such concepts and wrong to an agent with different ones. The fix is larger than a rewrite of two sections: the method never asked **who controls each load-path item**, and that omission is what let `CE-07` be banded `L` on a cost no project could reach. A controller field turns *unreachable* into a reportable result instead of a low rank, which is a different fact that currently reads the same. `s`, and it lands before [T-137](T-137-package-the-context-economy-method-as-a-skill.md) — packaging a method that assumes one agent would publish that assumption. |
