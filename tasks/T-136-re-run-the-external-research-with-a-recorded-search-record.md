---
id: T-136
title: Re-run the external research with a recorded search record
type: research
status: done
phase: review
shipped_in: 0.3.0
parent: T-130
blocked_by: []
related: [T-130, T-135]
work_package: PH3
owner: the project owner
business_value: high
effort: m
created: 2026-08-13
updated: 2026-08-13
deliverables:
  - docs/research/R8-context-economy-for-coding-agents.md
---

# T-136 — Re-run the external research with a recorded search record

## 1. Specify

**Outcome**
[T-130](T-130-audit-the-context-economy-of-an-agent-driven-repository.md)'s method step 5 runs again,
properly this time, and its output carries the search record the method now requires: the queries run,
the sources read, and an explicit statement that named tools in this space were searched for **by
name**. The catalogue in
[`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
§7 is rebuilt on that basis, and every screening verdict in
[`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §4 is re-derived.

**Why this exists**
The first pass was **two web searches and two fetched articles**, and it presented its result as a
catalogue. The owner asked whether one specific named tool had been checked. It had not — and
checking it produced a technique the catalogue had no entry for. A second gap surfaced in the same
question: an index-and-retrieve approach over the project's own documents, which the first pass had
folded into a general just-in-time row rather than listing as its own technique with its own cost and
assumption.

**Neither was excluded on principle, and it matters that this is said plainly.** There was no rule
against third-party tooling — the catalogue already carries techniques that depend on external
components. They were simply not found, and nothing in the method required looking.

**The screening partition is what made the gap invisible.** *Adopted + rejected + deferred = every
technique gathered* sums correctly whether the catalogue holds nineteen techniques or two. It is an
arithmetic check on step 7 that reads like a coverage claim for step 5, and this task exists because
the audit shipped with that ambiguity intact. The guard now written into the method — a recorded
search record — is deliberately weaker than the partition, because a survey cannot be proved
complete; it can only be shown.

**Scope**
- In: re-running step 5 with breadth, and recording what was searched so a reader can judge it.
- In: **searching for named tools and plugins by name**, not only for ideas and articles.
- In: rebuilding the §7 catalogue, and re-screening **every** row into the three verdicts — including
  the nineteen already there, because a row screened against a thin catalogue was screened against a
  different denominator.
- In: replacing the two provisional rows added 2026-08-13, `T20` and `T21`, with whatever the proper
  pass produces.
- Out: steps 1–4. Those are measurements of this repository and are unaffected by what the literature
  says.
- Out: re-ranking the `CE-nn` findings, unless a new technique produces a new one. The findings rest
  on the inventory, not on the catalogue.
- Out: adopting anything. This is research; the ranking and the owner's review are where work is
  bought.

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.2 — what a session working an audit finding owes beyond the finding: what to check, what to report, and where each thing goes. Read before starting
- [`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
  §3 step 5 — the coverage rule this task is the first to run under — and §7, §10
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §4 — the screening to re-derive
- The named tool the owner supplied, and whatever the by-name search finds beside it

**Acceptance criteria**
- [ ] §7 carries a search record: the queries run, the sources read, and a statement that named tools
      were searched for by name
- [ ] Every catalogue row has what it costs and what it assumes, on the same terms as the existing
      rows
- [ ] Every row is screened *adopted / rejected / deferred* against this project, the three sum to the
      catalogue, and the sum is stated
- [ ] A rejection names the constraint it collides with; a deferral names what would close it
- [ ] `T20` and `T21` are either confirmed, restated, or replaced — none is left as *provisional*
- [ ] The audit's two documents agree on the catalogue's size, in both places it is stated
- [ ] Any new `CE-nn` the research produces is added with all ten fields and ranked with the rest;
      **if it produces none, that is written down as a result**

**Open questions**
- ~~**How wide is wide enough?**~~ **Settled 2026-08-14 by the implementer, from the rule's own
  reason.** The stopping rule is **declared saturation, per axis**: the search runs along three axes —
  *ideas and articles*, *named tools, plugins and MCP servers searched by name*, and *the harness's own
  documented mechanisms* — and an axis stops when a full round of queries on it yields **no technique
  the catalogue does not already carry**. **Every query is recorded, including the ones that returned
  nothing new**, because those are the evidence that the axis stopped for a reason rather than at a
  budget. A reader who thinks an axis stopped early can see exactly which queries were run and judge.
  This costs one extra round per axis and stays inside `m`.

  Saturation is what a survey can show; completeness is what it cannot (`R8` §10, fifth limit). The
  rule is deliberately of the weaker kind for the same reason the search record is.

## 2. Plan

**The three axes are the plan's spine**, and each runs to the saturation rule §1 settles. Queries are
recorded as they are run, not reconstructed afterwards — a reconstructed search record is the thing
this task exists to stop.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | **Axis A — ideas, articles, papers.** Context engineering, token budgets, retrieval discipline, agent memory. Run to saturation | Queries + sources, recorded |
| 2 | **Axis B — named tools, plugins, MCP servers and CLIs, searched by name.** The axis the first pass never ran. Includes the tool the owner supplied | Queries + sources, recorded; the owner's tool identified and screened by name |
| 3 | **Axis C — the harness's own documented mechanisms.** What Claude Code itself offers is a technique source the first pass treated as background | Queries + sources, recorded |
| 4 | **Rebuild `R8` §7.** Every surviving row keeps its cost and assumption; new rows get the same two columns; `T20` and `T21` are confirmed, restated or replaced against what the by-name axis found | A catalogue with a stated size |
| 5 | **Write the search record into `R8` §7**, above the table: the queries, the sources, and the by-name statement §3 step 5 requires | The guard, satisfied for the first time |
| 6 | **Re-screen every row in `CONTEXT-AUDIT.md` §4** — all of them, not only the new ones, because the denominator moved | Three verdicts, a stated sum, and a reason per rejection and deferral |
| 7 | **Reconcile the size in both documents**, and check whether `tools/docs/figures.py` binds either statement | Both places agree; the checker is green or gains a row |
| 8 | **Decide the finding question and write the answer down either way** — a new `CE-nn` with all ten fields and a rank, or the recorded result that the research produced none | What [T-153](T-153-run-the-audit-methods-phase-2-over-this-repositorys-own-audit.md) is waiting on |
| 9 | **Review.** §4 verdicts, `L-nn` for anything that outlives the task, [T-137](T-137-package-the-context-economy-method-as-a-skill.md) §1 for anything the *method* learned | Closure |

## 3. Implement

**Decisions & assumptions**
- **The stopping rule is declared saturation per axis, and the empty rounds are published** — a
  survey cannot be proved complete, so the record has to let a reader judge where it stopped instead
  of asserting it stopped in the right place — 2026-08-14. §1.
- **Three axes, not one.** *Ideas*, *named tools by name*, and **the harness's own documented
  mechanisms**. The third was not in the plan's original reasoning and earned its place: it produced
  three techniques and had never been treated as a source at all — 2026-08-14.
- **`T20` is Ponytail, and it is screened on an independent benchmark rather than on its own
  figures.** Advertised −54% code / −22% tokens / −20% cost / −27% time; measured across 80 paired
  tasks at −15% code (p = 0.088), −10.3% cost (p = 0.004), −11% time, concentrated at −31% on big
  builds and zero on small ones. The verdict stays *deferred* and the closing condition sharpens —
  **L-98** — 2026-08-14.
- **`T7` and `T17` were restated rather than split.** Tiered compaction is compaction, and the
  measured cost of the spec-driven genre is a cost of `T17`, not a new technique. Splitting either
  would have inflated the catalogue without adding a decision — 2026-08-14.
- **One secondary-source claim was tested and not confirmed, and it is recorded as unverified.** That
  the harness attributes recent usage to individual skills, subagents, plugins and MCP servers comes
  from one blog; a targeted second query did not confirm it against primary documentation, so no row
  rests on it. The documented instrument is `T31` — 2026-08-14.
- **No method text was edited.** What the run taught the *method* went to
  [T-137](T-137-package-the-context-economy-method-as-a-skill.md) §1, per
  [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.2. Adopting anything is out of scope, and
  that includes adopting an improvement to `R8` §3 — 2026-08-14.
- **Assumption worth double-checking:** the measurements quoted in the catalogue are each from a
  single source, and only the Ponytail benchmark was read at its origin rather than through search
  results. The rest are recorded with their claims attached to the row that uses them, so a reader who
  distrusts one can see exactly which verdict it moves.

**Outputs produced**
- [`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
  §7.1 — the search record: three axes, eleven rounds, 23 queries and one fetch, with the saturating
  rounds shown as such and one negative result recorded
- §7.2 — the catalogue rebuilt to **35** techniques; `T22`–`T35` new, `T7`, `T17`, `T20` and `T21`
  restated, `T20` and `T21` no longer provisional
- §10 — the first limit restated (session instrumentation exists, so the limit is a choice), and the
  fifth limit given the measured size of the gap
- §11 — sources regrouped by axis, with the 2026-08-13 pass kept as §11.1
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §4 — every row re-screened; **12 adopted, 10
  rejected, 13 deferred, summing to 35**
- §4.1 — **the finding question answered: no new `CE-nn`**, with the argument
- §6.2 — corrected: only `T-138` now stands between here and phase 2
- `docs/lessons/L-98.md` — a tool's own measurements are its best case; **L-84** amended with the
  measured size of the gap it describes
- [T-137](T-137-package-the-context-economy-method-as-a-skill.md) §1 — five rows on what the gathering
  step owes
- [T-156](T-156-make-the-screening-partition-a-figure-a-checker-can-count.md) — raised

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| §7 carries a search record: queries, sources, and a statement that named tools were searched by name | **met** | `R8` §7.1. 23 queries and one fetch across three axes, each round listed with how many techniques it added. The by-name statement is explicit and the axis has its own row |
| Every catalogue row has what it costs and what it assumes | **met** | All 35, on the same two columns as the original rows |
| Every row screened *adopted / rejected / deferred*, the three sum to the catalogue, and the sum is stated | **met** | `CONTEXT-AUDIT.md` §4: **12 + 10 + 13 = 35**, stated in the opening sentence. All 21 original rows re-derived; none changed verdict |
| A rejection names the constraint it collides with; a deferral names what would close it | **met** | Checked row by row across the 23 non-adopted verdicts. The new rejections name **L-07**, the out-of-the-box constraint, or the audit's own axis |
| `T20` and `T21` are confirmed, restated, or replaced — none left *provisional* | **met** | Both confirmed **and** restated, each now carrying an independent measurement. The word *provisional* is gone from both documents |
| The audit's two documents agree on the catalogue's size, in both places it is stated | **met** | 35 in `R8` §10 and in `CONTEXT-AUDIT.md` §4. **And the criterion is checked by nobody, which is the defect** — [T-156](T-156-make-the-screening-partition-a-figure-a-checker-can-count.md) |
| Any new `CE-nn` added with all ten fields and ranked; if none, that is written down as a result | **met — as the null branch** | `CONTEXT-AUDIT.md` §4.1 states it and argues it: the findings rest on the inventory, ten of fourteen new techniques belong to another owner, three were already in force, and the one local candidate is unmeasured |

**On the one criterion that reads oddly:** *the two documents agree on the size* passed, and passing it
taught more than failing would have. Nothing checks it. The sentence has been internally consistent and
externally wrong twice, and this task made it a third value without any gate being able to tell —
which is why T-156 exists rather than a note.

**Child fix tasks raised**
- [T-156](T-156-make-the-screening-partition-a-figure-a-checker-can-count.md) — make the screening
  partition a figure a checker can count

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-14 | → done | **21 → 35, and the first pass had found 54% of it.** Three axes, 23 queries and one fetch, every round recorded including the four that added nothing. **The by-name axis — the one the first pass never ran — produced six of the fourteen new rows and the largest correction**: `T20` is Ponytail, whose own figures are about four times its independently measured effect, which is **L-98**. A third axis nobody had counted as a source, the harness's own documented mechanisms, produced three more. **No new `CE-nn`**, written down as a result in `CONTEXT-AUDIT.md` §4.1 and unblocking `T-153`. Two rejections now rest on measurements instead of arguments, `R8` §10's first limit turns out to be a choice, and `T28` gained a route that does not break **L-07**. One defect found in passing and raised as `T-156`. |
| 2026-08-14 | → in_progress | Searching began under the plan's three axes. |
| 2026-08-14 | → planned | Nine steps, three of which are the search axes. **Queries are recorded as they run**, because a search record assembled after the fact is indistinguishable from the thing this task was raised to replace. |
| 2026-08-14 | → specified | The one open question is settled in §1 and struck rather than deleted: **declared saturation per axis**, with every query recorded including the ones that added nothing. A survey cannot be proved complete, so the stopping rule is of the same weaker kind as the search record it produces. |
| 2026-08-13 | → proposed | Raised by the owner the day [T-130](T-130-audit-the-context-economy-of-an-agent-driven-repository.md) closed, from one question: had a specific named tool been checked. **It had not, and it was not excluded on principle** — the first pass was two searches and two articles, and nothing in the method required looking for named tools at all. Checking it produced a technique with no entry in the catalogue, and the same question exposed a second: index-and-retrieve over the project's own documents, folded into a general row rather than listed. **The partition is what hid it** — *adopted + rejected + deferred = everything gathered* sums correctly over any catalogue, however short, so it reads like coverage while checking only the screening. The method now requires a recorded search record, and `R8` §10 carries the limit; this task is the first to run under both. Two provisional rows are in the catalogue meanwhile, marked as such. |
