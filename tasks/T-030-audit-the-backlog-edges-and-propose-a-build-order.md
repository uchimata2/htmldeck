---
id: T-030
title: Audit the dependency edges across the open backlog and propose a build order
type: analysis
status: done
phase: review
parent: null
blocked_by: []
related: [T-008, T-020, T-028]
work_package: none
shipped_in: 0.1.0
owner: maintainer
created: 2026-08-07
updated: 2026-08-12
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
- ~~**Does the recommended order belong anywhere durable, or only in this task?**~~ **Answered
  2026-08-07 by the owner: only in this task.** The order lives in §3 with its tie-break rule and
  goes nowhere else — not `README.md`, and not a derived `task.py order` command. The edges are the
  durable record; the order is derivable from them plus a stated rule, and **L-08** says a stored
  copy of a derivable fact drifts where a derived one cannot. A closed task is also the one place a
  dated judgement cannot masquerade as current truth.

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

- **`blocked_by` is read as gating the *specification*, not only the first keystroke — 2026-08-07.**
  The vocabulary in [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §4 says *"must land before this one can
  start"*, which taken literally would delete most of the edges below: work can always *begin*.
  The reading that makes the edge useful is the one the backlog already uses — a task is gated when
  landing the upstream one later would make this task's §1 **wrong rather than incomplete**. Every
  `blocked_by` added here meets that test; everything that only wants reading became `related`.
- **`related` is asymmetric, and `context` prints only the outgoing side — 2026-08-07.** Eight tasks
  listed T-002 as `related` while T-002 listed nothing at all, so nobody opening T-002 saw them.
  Four of the additions below exist purely to make an edge visible from the task that needs to read
  it. This is a property of the schema, not a defect in it, but it means `related` has to be written
  on **both** files when both need the context.
- **The order is not a derivation, and the tie-break is stated rather than implied — 2026-08-07.**
  The graph fixes only a partial order; after it, seven tasks are simultaneously startable. The rule
  used below, in order: **(a)** unblocks the most, **(b)** converts an open criterion in
  [`BRIEF.md`](../docs/BRIEF.md)'s definition of done, **(c)** its output is consumed by another
  task's *first* step. Anyone re-deriving the order with a different rule gets a different answer,
  which is the point of writing the rule down.

**The thirteen verdicts**

| Task | Verdict | Reason |
| :--- | :--- | :--- |
| **T-002** | **three added** — `blocked_by` gains T-007, T-016, T-020; `related` gains T-021, T-028 | T-020 fixes the input contract; T-007 and T-016 are the token layer and the component set two acceptance criteria already require it to compose. A generator built before either exists can only hard-code, which `DESIGN-SYSTEM.md` §1.2 calls `hard`. |
| **T-003** | **one added** — `related` gains T-020 | Its gate arrives transitively through T-015; a direct edge would duplicate it. The `related` edge exists because T-003 is the task most likely to be **cancelled** — see §4. |
| **T-004** | **one added** — `blocked_by` gains T-020 | T-020 decides whether the specification review is this mode or a mode of its own. Every criterion here is written against a rendered artifact; being handed a second format afterwards is a respecification. |
| **T-005** | **one removed** — `blocked_by` T-002 deleted; `related` gains T-002, T-018, T-021 | **The edge was false.** The check runs on an HTML file and two exist, one of them the seeded-defect fixture its own criteria demand. `tools/deck/` already runs 30 checks against them. It was gating a task a third built. |
| **T-007** | **two added** — `related` gains T-016, T-021 | Edges unchanged otherwise and that is right: nothing gates it. But it is **not greenfield** — `examples/reference-deck.html` carries 57 custom properties. The instance exists; the contract and the swap demonstration do not. |
| **T-008** | **two added** — `blocked_by` gains T-005, T-028 | Both are open criteria in BRIEF's definition of done and both gate publishing only. T-028 is the *Release gate* the owner settled 2026-08-06, which existed **in prose with no edge**. This is the finding the audit was raised for. |
| **T-015** | **one added** — `blocked_by` gains T-020 | T-020 may reword *"asks exactly two questions"* into *"two questions, then shows its work at three points"*. That does not extend this task's central criterion, it contradicts it. |
| **T-016** | **one added** — `related` gains T-021 | Its own log already said to settle the tier-two question *with* T-021; the edge was never written. Like T-007, it is not greenfield: a disclosure component used ten times and a `rise` entrance used fifty-three already exist. |
| **T-018** | **one added** — `related` gains T-021 | No gate; deliberately so, and that still holds. But its measurement is the only thing that answers T-021's shared-rendering question, and the reference deck already couples the two without either task having ruled that it should. |
| **T-019** | **unchanged, and right** | `blocked_by: [T-002]` is a considered gate its own log explains: the preflight is emitted **by** build mode. The note that steps 1–2 could be pulled forward is a scheduling remark, not a reason to drop the edge. |
| **T-020** | **unchanged, and right** | No blockers, correctly — it is a decision taken from documents that all exist. Its own open question *"should this be a hard `blocked_by` on T-002 and T-015?"* is answered by this audit: **yes**, and the deadlock it feared cannot occur, because T-020 is gated by nothing. |
| **T-021** | **one added** — `related` gains T-018 | Edges otherwise right. **Specification partly satisfied** — flagged in §4, not rewritten. |
| **T-028** | **unchanged, and right** | No blockers is correct; it needs only the ruleset and the deck, both of which exist. What was missing was the edge on its **downstream** side, now added at T-008. |

**Recommended order, and why each position**

| # | Task | Reason for this position |
| :-- | :--- | :--- |
| 1 | **T-020** | Gates three tasks and is blocked by none. A decision, not a build — the cheapest thing in the backlog that unblocks the most. |
| 2 | **T-015** | Unblocks two, and its own §1 argues for standing the scaffold up early to have a working v1 to test against. |
| 3 | **T-018** | Cheap, unblocked, and the last open WP1 item — it closes the research phase. Its measurement is what T-021 needs at **step 1**. |
| 4 | **T-021** | Half built already; finishing it produces §11 conditions 13–19 as checks, which T-005 then absorbs in one pass instead of being reopened. *(Corrected 2026-08-09 by [T-037](T-037-record-in-the-ruleset-which-rules-no-check-can-reach.md): **`DESIGN-SYSTEM.md` §11 never existed**, so this position was argued from a section nobody had opened. The ordering still held — T-021 did produce the resolution-contract checks, as **DS-060 to DS-076** — but the reason cited a document that was not there.)* |
| 5 | **T-028** | The release gate — definition-of-done criterion 7, and the only one the owner made a condition of shipping. Unblocked since it was raised. |
| 6 | **T-005** | Definition-of-done criterion 2, unblocked as of this audit, a third built, both fixtures already in the repository. Takes T-021's conditions with it. |
| 7 | **T-007** | Gates T-002. Extraction from a working instance rather than authorship, so cheaper than its §1 reads. |
| 8 | **T-016** | Gates T-002, consumes T-007's tokens, and settles the tier-two question T-021 left it. |
| 9 | **T-004** | Definition-of-done criterion 3. Consumes T-005's report format, so it follows it; the seeded-defect deck it needs already exists. |
| 10 | **T-002** | The largest task and the one with the most inputs. Everything above is either its input contract, its tokens, its components, or the reference output it is judged against. |
| 11 | **T-019** | Emitted **by** build mode, so it cannot precede it. |
| 12 | **T-003** | Last of the modes because it may not survive — T-015 and T-020 between them decide whether it exists at all. |
| 13 | **T-008** | Publishing. All four of its blockers are above it, by construction. |

**One known cost in this order, stated rather than smoothed:** T-005 sits at 6 and T-007 at 7, so
the criterion *"fails on a theme value hard-coded outside the token layer"* cannot be built when
T-005 is worked. That is **one criterion of roughly thirty-three**, and re-entering for it is
cheaper than delaying the whole check behind the token layer. It is a re-entry, not an oversight.

**Outputs produced**
- Edited front-matter: **T-002, T-003, T-004, T-005, T-007, T-008, T-015, T-016, T-018, T-021** —
  ten of the thirteen. T-019, T-020 and T-028 were examined and left alone.
- A `(no change)` log row on each of those ten, per [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §5.
- [`README.md`](README.md) regenerated: six tasks now carry an open blocker, against four before.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| All thirteen examined, §3 records a verdict for each | met | The verdict table in §3. Three are *"unchanged, and right"* with the reason — T-019, T-020, T-028. |
| Every candidate edge resolved: added, rejected or re-typed | met | T-008←T-028 **added**; T-002←T-020 and T-004←T-020 **added**, and T-015←T-020 with them; T-002←T-007 and T-002←T-016 **added**; T-005←T-002 **removed and re-typed to `related`**; T-021 **flagged partly satisfied**. |
| No `blocked_by` that is really "read that first" | met | One found and deleted (T-005←T-002). Six of the eight `related` additions exist because the context was real and the gate was not. |
| A recommended order for all thirteen, one line per position | met | §3. The tie-break rule is stated because the graph alone leaves seven tasks simultaneously startable. |
| The order is consistent with the edges | met | Checked against the regenerated board: T-002 at 10 follows T-007/T-015/T-016/T-020; T-003 at 12 follows T-015; T-004 at 9 follows T-020; T-019 at 11 follows T-002; T-008 at 13 follows all four of its blockers. |
| Stale specifications flagged, not rewritten | met | Three flagged below. None edited. |
| `python tools/tasks/task.py check` passes | met | `OK - 30 tasks, vocabulary valid, task references resolve, 365 document pointer(s) checked, 0 broken`. No cycles, including through the four new gates. |

**Three specifications flagged as stale or partly satisfied — flagged only, per scope**

1. **T-021 is partly satisfied.** A working reflow view exists in the reference deck with all
   tier-two content, `scrollWidth` 320 at 320 CSS px, and position preserved both ways — three of
   its nine acceptance criteria, demonstrated on one deck. What remains is the fullscreen
   suppression, the auto-engage threshold, condition 17, the 720p measurement, the conformance
   wording, and the **enforcement**, which is the half its title names and the half that does not
   exist. Its §1 reads as though none of it were built.
2. **T-007 and T-016 read as greenfield and are not.** `examples/reference-deck.html` carries **57
   custom properties** across colour, type, spacing, radii, stroke, shadow, motion and disclosure,
   plus a disclosure component used ten times and a `rise` entrance used fifty-three. Neither task's
   §1 mentions this; only T-005's and T-021's logs record the equivalent for themselves. **The
   pattern is the finding**: T-024 built the reference deck by hand and, to make it comply, had to
   build a first instance of four separate downstream tasks. Four specifications describe authoring
   work that is actually extraction work, and the backlog cannot see the difference.
3. **T-003 may not survive.** Its existence is an open question held in T-015 §1 and settled by
   T-020. It is specified as a standalone mode; both of the tasks above it may fold it into an
   internal structure. Left open — cancelling it is the owner's call, and §1 puts status changes on
   other tasks out of scope.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-07 | → done | **Open question answered by the owner: the order lives in §3 and nowhere else** — not `README.md`, not a derived `task.py order` command. The edges are the record; the order is derivable from them plus the stated tie-break, and **L-08** rules that a stored copy of a derivable fact drifts. Two findings generalised beyond this task and went to [`LESSONS.md`](../docs/LESSONS.md): **L-31**, a dependency edge is a dated claim nothing re-checks — and it can be invalidated by work touching neither endpoint, which is exactly how T-005 came to be gated while a third built; **L-32**, building one artifact by hand does the first pass of every task downstream of it, so four specifications here describe authorship where only extraction remains. |
| 2026-08-07 | → review | Worked in one pass. **All five candidate edges resolved, and the suspected one was right**: BRIEF's *Release gate* had no edge, and T-008 is now `blocked_by` T-028 — plus T-005, which is the same document's criterion 2 and was only `related`. Two edges nobody had proposed: T-020 gates **T-015** as well (its own open question named it), and T-007/T-016 gate T-002 because the criteria there already require composing from contracts that do not exist. **One `blocked_by` was false and is deleted** — T-005 was gated on build mode while running 30 checks against two decks already in the repository. Ten of thirteen tasks edited; six now carry an open blocker, against four before, so the index distinguishes *unblocked* from *unrevisited* for the first time. The order is in §3 with the tie-break rule stated, because the graph alone leaves seven tasks simultaneously startable. **The open question — where the order lives — is not answered here.** |
| 2026-08-07 | → proposed | Raised at the owner's request when WP1's research work went quiet. The backlog's edges were mostly set before the research that has since landed, and **nine of thirteen open tasks carry no `blocked_by` at all** — which is either correct or an artifact of nobody revisiting them, and the index cannot tell those apart. The known-missing edge is the publishing gate: BRIEF rules that T-028 precedes the first published version, and no edge says so. |
