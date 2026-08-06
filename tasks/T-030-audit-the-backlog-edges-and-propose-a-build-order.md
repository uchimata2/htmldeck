---
id: T-030
title: Audit the dependency edges across the open backlog and propose a build order
type: analysis
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-008, T-020, T-028]
work_package: none
owner: maintainer
created: 2026-08-07
updated: 2026-08-07
deliverables: []
---

# T-030 — Audit the dependency edges across the open backlog and propose a build order

## 1. Specify

**Outcome**
Every open task's `blocked_by` and `related` edges reflect what is actually true after WP1's
research closed, and **a recommended order for the thirteen open tasks** exists with a reason per
position. The edges are the durable output — they are what `task.py` derives `blocks` from and what
decides whether a task is startable. The order is the reasoning, recorded in §3.

**Why now**
The backlog's edges were set when the tasks were written, most of them before the research that has
since landed. Since then: the ruleset was built, validated against a real deck and reconciled
(T-014, T-024, T-025, T-027); the rubric was written and its two owner decisions settled (T-023,
T-026); and a publishing gate was added that **has no edge representing it**. Nine of the thirteen
open tasks carry no `blocked_by` at all, which is either correct or an artifact of nobody revisiting
them — and those two states are indistinguishable from the index.

**Scope**
- In: every task in the *Active* table of [`README.md`](README.md) — thirteen as of 2026-08-07.
- In: adding, removing and re-typing edges. `blocked_by` is the only edge that gates and it
  propagates, so **an edge that is really "read that first" must be `related`**, per
  [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §4.
- In: a recommended order, with the reason for each position stated in one line.
- In: flagging any open task whose **specification** is now stale or partly satisfied by work that
  has since landed — T-021 is the known candidate (see below). Flag it; do not rewrite it.
- Out: doing any of the work the tasks describe.
- Out: changing status or phase on any task other than this one. If a task looks done, say so in
  §3 and let the owner rule.
- Out: creating new tasks. If the audit implies one, name it in §4 rather than opening it.

**Candidate edges to verify — unverified, and listed so the audit starts warm rather than blank**

| Candidate | Why it is suspected | What to check |
| :--- | :--- | :--- |
| **T-008 `blocked_by` T-028** | [`../docs/BRIEF.md`](../docs/BRIEF.md) *Decisions taken* → **Release gate** rules that T-028 lands before the first published version, and T-008 *is* "package, document and publish". The ruling exists in prose with **no edge representing it** — the exact drift `blocked_by` is for. | Whether the gate is on T-008 specifically or on a later publish step. |
| **T-002 / T-004 `blocked_by` T-020** | T-020 decides *where the convergence loop runs* and whether build is batched. Build mode and critique mode both have to sit somewhere in that pipeline. | Whether either can be specified without the placement, or only implemented. |
| **T-002 `blocked_by` T-007, T-016** | Build mode emits the theme and the interaction layer those two tasks define. | Whether they are genuine gates or `related` — a generator can be specified against a token contract that does not exist yet. |
| **T-005 `blocked_by` T-002** *(exists)* | Still right? T-024 built a measurement layer under `tools/deck/` that the check will reuse. | Whether the check is now partly buildable ahead of build mode. |
| **T-021 partly satisfied** | T-024's round 1 fixed the reference deck's reflow below ~430 px, and `DESIGN-SYSTEM.md` §2.4–§2.5 already carry the rules. | What of T-021 remains: the rules exist and one deck complies; the *enforcement* may not. |

**Inputs**
- [`README.md`](README.md) — the generated board; `python tools/tasks/task.py index` regenerates it
- [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §4 — which edge to use, and why `blocked_by` is expensive
- [`../docs/BRIEF.md`](../docs/BRIEF.md) — *Decisions taken* and *Definition of done*; four of seven
  criteria are open and they are the strongest signal of what order the work wants
- `python tools/tasks/task.py context T-NNN` — per task, and it prints the derived `blocks` side

**Acceptance criteria**
- [ ] Every one of the thirteen open tasks has been examined, and §3 records a verdict for each —
      including "edges unchanged, and here is why that is right", which is the finding for most of them
- [ ] Every candidate edge above is resolved: added, rejected, or re-typed to `related`, with a reason
- [ ] No `blocked_by` edge exists that is really "read that first"
- [ ] A recommended order for all thirteen, each position carrying a one-line reason
- [ ] The order is consistent with the edges — nothing is recommended before something that gates it
- [ ] Any task whose specification is stale is flagged in §4, not silently rewritten
- [ ] `python tools/tasks/task.py check` passes — it walks the graph and rejects cycles

**Open questions**
- **Does the recommended order belong anywhere durable, or only in this task?** An order goes stale
  as soon as an edge changes, and the edges are the real record. Recording it in a hand-written
  section of `README.md` would put it where people look and where it can rot unnoticed. — maintainer

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Read the thirteen open tasks, and the derived `blocks` side of each | a picture of the graph as it stands |
| 2 | Resolve each candidate edge above, then look for edges nobody has proposed | verdicts with reasons |
| 3 | Apply the edge changes to front-matter, and re-run `index` and `check` | a graph that validates, no cycles |
| 4 | Derive the order from the corrected graph and the four open definition-of-done criteria | the recommended order, reason per position |
| 5 | Put the open question above to the owner | a decision on where the order lives |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <edited task front-matter, listed by ID>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-07 | → proposed | Raised at the owner's request when WP1's research work went quiet. The backlog's edges were mostly set before the research that has since landed, and **nine of thirteen open tasks carry no `blocked_by` at all** — which is either correct or an artifact of nobody revisiting them, and the index cannot tell those apart. The known-missing edge is the publishing gate: BRIEF rules that T-028 precedes the first published version, and no edge says so. |
