---
id: T-287
title: Audit — what a session pays per turn, and why it grows
type: audit
status: in_progress
phase: review
parent: null
blocked_by: []
related: [T-130, T-153, T-285, T-286]
work_package: PH3
owner: the project owner
business_value: high
effort: m
created: 2026-09-02
updated: 2026-09-02
deliverables: [docs/CONTEXT-AUDIT.md, docs/lessons/L-154.md]
---

<!--
The method is the taskmd skill's - METHOD.md section 5, audit.md, and pre-release-audit.md for an
audit of everything about to be released. ../docs/AUDIT-METHOD.md is this project's binding only.
Neither is restated here. Fill the four sections below in order; they are the four lifecycle phases
(TASK-WORKFLOW.md section 2). Child fixes are separate task files with `parent:` set to this id.
-->

# T-287 — Audit: what a session pays per turn, and why it grows

## 1. Specify

**Trigger**
The owner, 2026-09-02, after B17, in these words: *exponentially increasing token consumption is a
real problem. We should address that too.* [`../docs/AUDIT-METHOD.md`](../docs/AUDIT-METHOD.md) §1
names the context-economy audit's trigger as *request, or a change to tier 1*, and both hold: the
request above, and [T-236](T-236-tier-1-and-the-brief-against-what-they-measure.md) changed tier 1
in the same batch.

**Outcome**
The **second run** of the context-economy audit, whose first run was
[T-130](T-130-audit-the-context-economy-of-an-agent-driven-repository.md) and whose grading pass was
[T-153](T-153-run-the-audit-methods-phase-2-over-this-repositorys-own-audit.md). The first run
measured what a session loads **without asking** — tier 1, and the plugin as an adopter loads it.
This run measures what a session **accumulates by working**: what each turn adds to the context,
which of those additions are paid again on every later turn, and which can be changed. Its findings
join [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6's ranking under the next free ids after
`CE-13`, in a section of their own for this subject; every `High` and `Medium` becomes a child task
carrying `finding: CE-nn`, which `tools/docs/findings.py` binds for this register and no other
(the binding's §3); every `Low` is batched or accepted with a reason. **Phase 2 is recorded after the
remedies exist**, as the ecoctx skill requires, and it grades each prediction against what it
bought — the first run's grading found two of thirteen bands held as written.

**Scope**
- In: the four costs B17 met and could name. (1) What the gates print on a green run and how often
  they run — [T-285](T-285-let-a-documentation-task-run-the-gates-its-change-can-reach.md) and
  [T-286](T-286-print-the-verdict-on-a-green-run-and-the-report-only-when-asked.md) are the two
  measured cuts, already specified, and this audit takes its baseline **after** they land so their
  saving is not counted twice. (2) What a resume reads before its first edit: the handoff's pointed
  homes, and how much of each a task actually needs — B17's first task spent about thirty minutes
  reading and its second and third about five each. (3) What a finding costs to close: the register's
  rows run to one or two kilobytes each and the tool a finding is about can be a hundred kilobytes,
  of which a session reads what it must to change it. (4) Tier 1 as it stands after T-236, since a
  change to it is this audit's own trigger.
- In: the method as packaged — the `ecoctx` skill, which is T-130's method made reusable
  ([T-137](T-137-package-the-context-economy-method-as-a-skill.md)); this run is also its second
  use here and reports what the skill could not measure.
- In: **an instrument for the session's own consumption**, which is grade C below and was not
  available to the first run: the harness's own usage breakdown, which the `explain-usage` skill
  reads for one session. Whether that reading is evidence or illustration is an open question.
- Out: the plugin as an adopter loads it — the first run's subject 2, unchanged since, and audited
  again only if a session shows it moved.
- Out: implementing anything. An audit ranks; the owner reviews the ranking, and the top of it
  becomes child tasks then — the first run's rule, kept.

**Coverage grades** — §3 of the method. The split for this run; the sizes are measured at cycle 0
and not typed here, except tier 1, which is measured today because it is the trigger.

| Grade | What it applies to here | Files | Bytes |
| :--- | :--- | ---: | ---: |
| A — wide | tier 1: this repository's `CLAUDE.md`, the owner's global preferences, and the memory index — 15,581, 5,489 and 8,760 bytes on 2026-09-02, every turn | 3 | 29,830 |
| B — narrow | what a resume reads and what a finding costs to close, sampled over B17's three tasks and the audit's own; what the gates print, taken from T-286's table | cycle 0 | cycle 0 |
| C — instrument only | the session's own token accounting, which only the harness holds; read through `explain-usage` and reported as what that reading can and cannot say | — | — |

**Register**
[`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md), continuing the `CE-nn` id space after `CE-13`.

**Acceptance criteria**
- [x] Every cost in scope is measured, skipped with a stated reason, or produced a finding, and the
      coverage ledger says which.
- [x] Every finding carries the command that proves it, or names the reading that does and why no
      command can.
- [x] Every High and Medium finding has a child task; every Low is batched or accepted with a reason.
- [x] The baseline is taken on a tree where `T-285` and `T-286` have landed, and says so.
- [ ] Phase 2 is recorded after the remedies exist, and names at least one prediction the
      measurement refused — or it was not run honestly.

**Open questions** — both decided at cycle 0, the recommendation adopted in each case, as `T-285`
and `T-286` did with theirs.
- Whether the harness's usage breakdown counts as an instrument for grade C, or only as
  illustration — **an instrument for the session it reads and nothing wider, stated as such on every
  figure it yields.** The register's §11 says so at its head, and the lesson repeats it.
- Whether this run waits for `T-285` and `T-286` — **moot: both landed in `807d2db` before this
  session began**, and the baseline is that commit.

## 2. Plan

**The cycle program.** One subject per cycle, ordered by expected finding density, each sized to
what one session can read and still judge (the skill's `pre-release-audit.md`). A cycle is a
session boundary: it may be run alone. **All seven ran in one session on 2026-09-02**, because the
instruments were three scripts and the subjects were small; the boundary was never needed.

| # | Subject | Files | Bytes | Brief | Instrument | Status |
| :-- | :--- | :--- | ---: | :--- | :--- | :--- |
| 0 | Prepare the instruments | 16 gates | — | baseline gates green on the frozen tree at `807d2db`; three throwaway scripts outside the repository | `lint.py` then `check_all.py`, in sequence, output captured to files | done — green, 226 s |
| 1 | Surface A — the load path | 3 + 60 | 30,084 + 15,024 | tier 1 by observation; the skill catalogue priced from its own files; the memory index against the harness's limit | the sizing script; the transcript's first call | done — `CE-14`, `CE-17`, `CE-20` |
| 2 | Surface B — the resume read path | 16 | 123,684 / 306,038 | this session's own resume, chosen before it started | the sizing script over the files and ranges read; the transcript's growth over the same calls | done — `CE-15` |
| 3 | Surface C — tool output green | 16 commands | 82,000 | every gate and query on the frozen tree | the sequential runner | done — `CE-18`, `CE-19`, `CE-21` |
| 4 | Surface D — write volume | 9 commits, 6 tasks | — | B17 and the two cuts | `git log --numstat`; file sizes | done — `CE-22` |
| 5 | Surface E and grade C — the per-turn model | 1 transcript | 525,451 | this session's own API calls | the transcript instrument, deduplicated by message id | done — `CE-16`, L-154 |
| 6 | Research and screening | — | — | three axes, saturation declared per axis | thirteen searches, three fetches | done — §11.3 |

## 3. Implement

**Decisions & assumptions**
- **The transcript is an instrument for the session it reads** — 2026-09-02. The spec's
  recommendation, adopted. Every figure from it is dated and named as one session's; none is written
  into a rule without that label. The first version of the instrument counted one API call per content
  block and reported 36 calls for 14; a known-good case before reading a scan as a finding is the
  method's own rule, re-learned.
- **The child tasks are raised now, `proposed`, and not after the owner's review** — 2026-09-02. The
  spec says both: *every High and Medium becomes a child task* and *the owner reviews the ranking, and
  the top of it becomes child tasks then*. A proposed task is the cheaper reversible form of the
  ranking — one file the owner strikes — and the first run's grading showed the ranking itself was
  where the errors were, so the owner reviews tasks that each carry their own measurement step.
- **`CE-16` and `CE-22` collide with settled policy and are not resolved here** — the ecoctx method's
  fourth refusal. `CE-16` gets a measurement task and no change; `CE-22` gets no task and a stated
  reason. Both are the owner's.
- **The Lows are one task with one `finding:` field** — `findings.py` binds one id per task, so
  `T-293` carries `CE-19` and names `CE-20` and `CE-21` in its body; the tool reports a finding with
  no task rather than failing on it.
- **Axis B of the search was stopped while still adding**, at five rounds, and the record says so
  rather than claiming saturation. Axis A saturated at three; axis C stopped at five with the fifth
  still adding, and is stated the same way.
- **The full gate ran once, before any edit, and the docs gate closes the commit** — `T-285`'s rule;
  this task changed documents and task records only, and the docs mode refuses if that stops being
  true.

**Findings raised**
Counts only; the statements live in the register.

| Severity | Raised | Tasked | Accepted | Open |
| :--- | ---: | ---: | ---: | ---: |
| High | 1 | 1 | 0 | 0 |
| Medium | 4 | 4 | 0 | 0 |
| Low | 4 | 3 (batched) | 1 | 0 |

**Child tasks raised**
- [T-288](T-288-move-the-rules-that-bind-only-deck-or-release-work-under-path-scoped-rules.md) — `CE-14` — deck and release rules out of tier 1, under path-scoped rules; addressability measured first
- [T-289](T-289-give-tooling-md-section-1-addressable-subsections.md) — `CE-15` — `TOOLING.md` §1 into addressable subsections
- [T-290](T-290-measure-one-batch-run-as-one-session-against-the-session-per-task-rhythm.md) — `CE-16` — one batch run both ways, measured, for the owner
- [T-291](T-291-measure-whether-the-desktop-apps-skill-catalogue-can-be-scoped-per-project.md) — `CE-17` — the app's skill catalogue, scoped or its boundary recorded
- [T-292](T-292-the-docs-gate-is-four-fifths-one-render.md) — `CE-18` — what `figures.py`'s coverage account binds to
- [T-293](T-293-the-second-runs-low-findings-in-one-pass.md) — `CE-19`, with `CE-20` and `CE-21` — the Lows in one pass
- [T-294](T-294-grade-the-second-context-economy-runs-bands-after-its-remedies-land.md) — phase 2, blocked on the six above

**Outputs produced**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) — rows `CE-14` to `CE-22` in §6's table, §6.3 the statements, §11 the measurement
- [`../docs/lessons/L-154.md`](../docs/lessons/L-154.md) — the per-byte cost line and the session-boundary arithmetic
- [`../docs/AUDIT-METHOD.md`](../docs/AUDIT-METHOD.md) §1 — one clause: this run in the *ran as* list
- `../CLAUDE.md` — one clause: the tier-1 debt now has a ranked finding behind it

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every cost in scope measured, skipped with a reason, or a finding | met | the four named costs: gates → §11.1 C and `CE-18`, `CE-19`, `CE-21`; the resume → §11.1 B and `CE-15`; a finding's closing cost → §11.1 D, and `CE-22` is what it produced; tier 1 → §11.1 A and `CE-14`, `CE-17`, `CE-20`. The method as packaged → §11.4. Nothing skipped |
| Every finding carries its proof | met | a command or a script for `CE-14`, `CE-15`, `CE-17`–`CE-21`; the transcript reading, named as one session's, for `CE-16` and `CE-22` |
| High and Medium tasked; Low batched or accepted | met | five tasks for five; `T-293` for three Lows; `CE-22` accepted with the collision stated |
| Baseline after `T-285` and `T-286`, and says so | met | `807d2db`, §11's first paragraph |
| Phase 2 recorded after the remedies, with a refused prediction | **not met** | the remedies do not exist yet; [T-294](T-294-grade-the-second-context-economy-runs-bands-after-its-remedies-land.md) is raised and blocked on them, which is how `T-130` closed with `T-153` still to run |

**Phase 2**
§11.5 of the register holds the placeholder and names `T-294`; the sentence it reduces to is not
written until the remedies are measured. What this run can already say is §10.2's sentence unchanged:
the inventory is what survives, and every `Change` cell is a hypothesis.

**What this run could not see**
- Inside the harness's shared prefix — 39,315 of the 70,788 tokens a session starts with. The
  repository controls about a tenth of the start context and no instrument here decomposes the rest.
- The catalogue's completeness on axis B, stopped while still adding.
- Thinking tokens apart from output; the transcript reports one output figure.
- Any session but this one. A second transcript is `T-294`'s first step.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-02 | → proposed | Asked for by the owner after B17, as the third task of one exchange: `T-285` cuts how often the gates run, `T-286` what they print, and this measures everything else a session pays per turn and why it grows. Filed as the second run of the context-economy audit rather than a new one, because `AUDIT-METHOD.md` §1 already names it, its register and id space exist, and `findings.py` binds this register's ids. `PH3`. To be run in a session of its own, after the two cuts land. |
| 2026-09-02 | → specified, planned | Both open questions decided by their recommendations; the cycle program written as seven cycles over the five surfaces plus research. |
| 2026-09-02 | → in_progress | Cycle 0 on the frozen tree at `807d2db`: full gate green in 226 s before any edit. Cycles 1–6 in the same session. |
| 2026-09-02 | → review | Nine findings, `CE-14`–`CE-22`; seven children raised, `T-288`–`T-294`; L-154. Four criteria met, the fifth carried by `T-294`. **Stays `in_progress` as the umbrella** — `taskmd check` refuses a `done` parent with open children, so this closes when `T-294` does, which is when phase 2 is recorded; the pre-release audit's umbrella rule, met the same way. Committed on the docs gate. |
