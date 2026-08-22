---
id: T-218
title: Record the pre-release audit method, and the machinery a run needs
type: deliverable
status: done
phase: review
parent: null
blocked_by: []
related: [T-042, T-119, T-130, T-153]
work_package: PH3
owner: the project owner
business_value: high
effort: m
created: 2026-08-22
updated: 2026-08-22
shipped_in: unreleased
deliverables:
  - docs/AUDIT-METHOD.md
  - tasks/_audit-umbrella-template.md
---

# T-218 — Record the pre-release audit method, and the machinery a run needs

## 1. Specify

**Trigger**

The owner asked for a pre-release audit of the whole repository and, in the same request, asked
whether this project's audit requirements could be improved so that a later request needs no
detailed prompt. Four audits have run here — [T-042](T-042-audit-the-whole-repository-against-itself.md),
[T-119](T-119-audit-the-ruleset-for-rules-that-cost-more-than-they-return.md),
[T-130](T-130-audit-the-context-economy-of-an-agent-driven-repository.md) and its phase 2
[T-153](T-153-run-the-audit-methods-phase-2-over-this-repositorys-own-audit.md) — and none of them
left a reusable statement of *how to audit this repository*. What existed was a 1,334-byte umbrella
template with six unweighted checkboxes, and a method inside `R8` §3 that is written for one subject.

**Outcome**

A reusable audit method, an umbrella template that implements it, and one entry point in the task
workflow — so that *run a pre-release audit* is a complete instruction.

**Scope**

- In: the method document, the umbrella template, a `TASK-WORKFLOW.md` subsection, the register
  scaffold the run writes into, and one paragraph in `PUBLISHING.md` §8 saying the audit is not a
  release step.
- Out: running the audit. That is [T-219](T-219-pre-release-audit-of-the-whole-repository.md), and it
  is deliberately a separate task with a separate lifespan — this machinery outlives every run.
- Out: generalising `tools/docs/findings.py` to a second register. It is cycle 0 of the run, because
  it is only needed once findings exist.

**Inputs**

- `docs/research/R8-context-economy-for-coding-agents.md` §3, §5, §6 — the sixteen-step method, the
  ranking rubric and the finding record, all written for one subject and generalised here.
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6, §10 — the worked instance and its phase 2.
- [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §2, §7 — the lifecycle the umbrella must follow, and the bar
  it closes on.

**Acceptance criteria**

- [ ] A method document exists that answers, without a prompt: what is audited, at what grade, what
      counts as a finding, what each severity obliges, and when phase 2 runs.
- [ ] The umbrella template's four sections are the four lifecycle phases.
- [ ] `TASK-WORKFLOW.md` has one entry point, and it says an audit runs on request only.
- [ ] `PUBLISHING.md` §8 says the audit is not one of its steps, and why.
- [ ] The method is not tier 1 and does not enter the tier-2 bound; the claim is established by
      observation, not asserted.
- [ ] `python tools/tasks/lint.py` green.

**Open questions**

- None outstanding. Four were put to the owner before any file was written, and their answers are in
  §3.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Establish what audit machinery already exists, and measure it | the four prior audits, the 1,334-byte template, `R8` §3–§6, `findings.py`'s hardcoded register |
| 2 | Put the four decisions the owner owns to the owner | method home, stop line, coverage depth, finding granularity |
| 3 | Write the method, generalised from one subject to four aspects | `AUDIT-METHOD.md`, under `docs/` |
| 4 | Rewrite the umbrella template against it, onto the four phases | [`_audit-umbrella-template.md`](_audit-umbrella-template.md) |
| 5 | Add the entry point and the release-sequence exclusion | [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §8, [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) §8 |
| 6 | Scaffold the register the run writes into | `PRE-RELEASE-AUDIT.md`, under `docs/`, owned by T-219 |
| 7 | Re-measure the tier-1 pair and correct `CLAUDE.md` in the same edit | the measured figures, in the one file that may hold them |

## 3. Implement

**Decisions & assumptions**

- **The method is tier 3, not tier 2 — 2026-08-22.** `CLAUDE.md` gives two tests for tier 3 and they
  disagree: *what tier 2 loads one at a time, for the branch actually taken* admits it, and *never to
  start work of a kind* excludes it. The precedent settles it — `RELEASE-PHASES.md` and
  `RELEASE-HISTORY.md` are both reached through a link and both declared tier 3, and this document is
  reached the same way, through [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §8. **The conflict itself is a
  candidate finding for T-219**, recorded in its cycle 3 brief rather than settled here.
  **The ruling is not moot in size, and an earlier draft of this line said it was.** The method
  measures **12,302** bytes and `TASK-WORKFLOW.md` measures **13,530** once §8 is in it, so the method
  is *below* the floor: called tier 2 it becomes the new smallest member and `CLAUDE.md`'s debt goes
  from **1,696** bytes to **2,924**. Called tier 3 it does not enter the bound at all. The draft
  claimed the opposite from a figure taken before §8 was written — which is the family of defect
  T-219 exists to find, met while writing the task that opens it.
- **The generic half went upstream the same day — 2026-08-22.** Reading taskmd's `audit.md` after this
  task closed showed most of the method either already lived there or contradicted a rule in it: its
  *Procedure* refuses a standing checklist, and taskmd's `SCOPE.md` R-9 forbids method content that
  assumes code or version control. The owner ruled the pre-release audit should be a taskmd feature so
  every adopter gets it. `docs/AUDIT-METHOD.md` is now the **local binding** — which audits run here,
  what the decks are exempt from reading, and the one tool gap — and is 3,450 bytes rather than 12,302.
  What went up is on taskmd's branch `audit/pre-release-audit-method` as their T-223.
- **Two tasks, not one — 2026-08-22.** The machinery outlives the run. Merging them would leave a
  `done` audit whose method is only recoverable by reading a closed record.
- **The register is scaffolded here and owned by T-219 — 2026-08-22.** It has to exist before the
  method may link it, and `taskmd check` reports a declared deliverable that does not exist. It says
  *not started* in its own text rather than reading as an audit that found nothing.
- **`R8` §3's sixteen steps were not copied.** They are a context-economy procedure — surfaces,
  controllers, tiers — and generalising them literally would have produced a method about the wrong
  subject. What was taken is the machinery that is subject-free: the finding record, the two-phase
  shape, the byproduct discipline, and *the remedy is a hypothesis* (**L-90**).

**The owner's four decisions, put before any file was written — 2026-08-22**

| Question | Answer | Consequence |
| :--- | :--- | :--- |
| Where the method lives | an updated umbrella template, a workflow subsection, **and** a method document | three artifacts, not one; the workflow subsection is the entry point that makes the method tier 3 |
| How far this session goes | specify and plan only — **do not execute the audit** | T-219 is left at `planned` with a full cycle program and no findings |
| How coverage is bought | **deep read everything**, batched so a session can stop | 43 cycles, sized to about 300 KB of source each |
| Findings to tasks | task for High and Medium, **batch the Low** | now the taskmd skill's `pre-release-audit.md` |

**What was argued against, and how it was resolved**

- **"Scan all project files" cannot mean the decks.** `CLAUDE.md` rule 6 forbids reading a deck whole,
  and the five tracked `.html` files are 1,773,568 bytes — 20% of the tree. Resolved with a third
  coverage grade: the decks are rendered and measured, their specifications are read.
- **The audit must not become a release step.** The owner had already ruled this; `PUBLISHING.md` §8
  now carries it, because a rule with no discoverable surface is one the next session re-derives.
- **`findings.py` reads one register.** `docs/CONTEXT-AUDIT.md` and the `CE-nn` pattern are hardcoded,
  and `lint.py`'s fourth check runs it — so a child task carrying `finding: PR-nn` fails the lint
  today. Recorded in the method §6 and made cycle 0 of the run, with `parent:` as the stated fallback.

**Outputs produced**

- `docs/AUDIT-METHOD.md` — the method, 12,302 bytes as written.
- `docs/PRE-RELEASE-AUDIT.md` — the register scaffold, owned by T-219.
- [`_audit-umbrella-template.md`](_audit-umbrella-template.md) — rewritten onto the four phases.
- [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §8 — the entry point.
- [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) §8 — the release-sequence exclusion.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Method answers the six questions without a prompt | met | §2, §3, §5, §7, §8, §9 of the method |
| Template's four sections are the four phases | met | it was `Specify / Findings / Resolution / Log` and did not follow §2 |
| One entry point, request-only | met | [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §8 |
| §8 says the audit is not a release step | met | stated with its reason, under the step table |
| Tier claim established by observation | met | nothing in the harness loads it; the only route is a link from a tier-2 document |
| `lint.py` green | met | run after the tier-1 re-measure |

**Child fix tasks raised**

- none. [T-219](T-219-pre-release-audit-of-the-whole-repository.md) is the run, not a fix.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-22 | → proposed | Created, from a request to run a pre-release audit and to improve the audit requirements behind it. |
| 2026-08-22 | → specified | Four decisions put to the owner and answered before any file was written. |
| 2026-08-22 | → planned | Seven steps. Step 7 exists because adding to `TASK-WORKFLOW.md` moves one term of the tier-1 bound. |
| 2026-08-22 | → in_progress | Method, register scaffold, template, entry point and the §8 exclusion written. |
| 2026-08-22 | → done | Every criterion met. The run is T-219 and is deliberately left unstarted. |
| 2026-08-22 | (no change) | The generic half handed to taskmd; this document thinned to the local binding. The criteria are unchanged and still met — a binding that defers is still an entry point — but the outcome above overstates what stayed here. |
