---
id: T-164
title: Retire the cross-repo register in favour of a branch against the repository that has the defect
type: decision
status: done
phase: review
parent: null
blocked_by: []
related: [T-163, T-161, T-160, T-157, T-141, T-130]
work_package: PH3
owner: the project owner
business_value: high
effort: s
created: 2026-08-15
updated: 2026-08-15
shipped_in: 0.3.0
deliverables: []
---

# T-164 — Retire the cross-repo register in favour of a branch against the repository that has the defect

## 1. Specify

**Outcome**
Every project the owner holds works to one rule for a defect found in another of them: **fix it there,
as a branch with a failing test and a three-line pull request.** The rule has exactly one operative
home, it loads in all five projects without being copied into any of them, and this repository's
register-and-issue ritual is retired with its two sent documents left standing as history.

**Why this exists**
The ritual worked and cost more than it returned. One thread ran to completion —
[`uchimata2/taskmd#1`](https://github.com/uchimata2/taskmd/issues/1) — and it is measurable:

| | |
| :--- | :--- |
| Issue comments, both sides | **33,881 bytes** over 7 comments |
| Task records here | **65,506 bytes** — T-157, T-160, T-161, T-163 |
| The register document | **11,816 bytes** |
| Tasks raised here that changed a line of behaviour | **0 of 4** |
| Tasks raised upstream | 7, of which one gate ships |

Three of the four local tasks were **prose about prose**: deliver the register, correct the register,
correct the correction. The two most expensive disputes in the thread — whether `check` reads
`skills/` and `examples/`, and whether this repository's version sort was broken — were each settled
here by **one command**, after both sides had argued them in paragraphs.

**Why it is not a verdict that the exchange was worthless.** `O-T4` found a row wider than its header
in a closed task record, destroying evidence for six days with `check` green. That single row repaid
its own report. The rule is therefore **not** *stop reporting*; it is *report by patch, prove
behaviour by running it, and cap the prose*.

**Scope**
- In: the practice, written once, where every project on this machine loads it
- In: retiring the route in [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §7, which is this
  repository's operative home for the register
- In: one line in each sent register's handover record, so a reader of the delivered document is not
  led into a practice that no longer exists
- In: checking the other four projects for instruction text that contradicts the new rule
- Out: **deleting the registers or their rows.** They were delivered under correction terms that still
  hold; a document that promised corrections and then vanished is worse than one never sent
- Out: `../CLAUDE.md`. It is over its own tier-1 bound already, and the register practice has never
  lived there
- Out: re-opening any verdict on the thread. Five of six rows landed; that is the recipient's call and
  it is made

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §7 — the route, the rules that travel with the
  rows, and the hold that preceded them
- [`../docs/upstream/taskmd.md`](../docs/upstream/taskmd.md) and
  [`../docs/upstream/handoff-skill.md`](../docs/upstream/handoff-skill.md) — the two sent registers
- [T-163](T-163-correct-the-coverage-claim-that-carried-the-wide-row-refusal.md) — the last correction
  the old route produced, and the measurement of what it cost

**Acceptance criteria**
- [x] The practice is stated in exactly one operative place, and that place loads in all five projects
- [x] No project carries a second copy of the rule
- [x] Each of the other four projects is checked for instruction text that contradicts it, with the
      result recorded
- [x] This repository's §7 records the retirement, dated, with the measurement that decided it
- [x] Both sent registers say the route is retired, without losing what they promised
- [x] `python tools/tasks/lint.py` green

**Open questions**
- ~~**A second comment, on the handoff thread.**~~ **Answered by the owner 2026-08-15: post it.** Both
  live threads now carry the process note, so neither recipient answers the next finding with an essay.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Write the practice into the owner's global working preferences — machine-local, loaded on every turn of every project | One operative home, five projects covered, nothing duplicated |
| 2 | Retire the route in `../docs/CONTEXT-AUDIT.md` §7 with the measurement behind it | The ruling where the ritual lives |
| 3 | One line in each register's handover record | A delivered document that does not send its reader down a retired route |
| 4 | Check the other four projects' instruction files for contradicting text | Either edits or a recorded negative |
| 5 | Gates, commit | `python tools/tasks/lint.py`, one commit |

## 3. Implement

**Decisions & assumptions**
- **The operative home is the owner's global working preferences, outside every repository** —
  2026-08-15. Five projects sit side by side under `C:\Work\AgentPlugins` and that file is loaded on
  every turn of every session in all of them, so one statement covers all five and any project created
  later. A copy per repository would be five copies of a rule about not duplicating things (**L-13**).
- **The bound of that choice, stated rather than discovered later** — 2026-08-15. The global file is
  machine-local and version-controlled nowhere, so a different machine or a different Claude surface
  does not have it. `../docs/CONTEXT-AUDIT.md` §7 therefore carries a full copy of the *ruling* — what
  was decided, when, and on what measurement — and names the global file as the operative statement.
  A ruling that survives and a rule that binds are different jobs.
- **`../CLAUDE.md` was not touched** — 2026-08-15. It is over its own tier-1 bound, the register
  practice has never been stated there, and adding a cross-project rule to a per-project file is the
  wrong tier as well as the wrong file.
- **The other four projects needed no edit, and that is a measurement rather than an assumption** —
  2026-08-15. `bpmn`, `Handoff` and `taskmd` carry a `CLAUDE.md`; `ecoctx` carries none. Searched all
  three for register, upstream, issue and report ritual: **no match contradicts the new rule.** taskmd's
  own file governs how it answers phases, not how it answers adopters. So the global statement is the
  whole change, and nothing was written into a repository that did not need it.
- **The registers stay exactly as delivered** — 2026-08-15. Only the handover records gained a line.
  Their rows were sent under a promise that a wrong row gets corrected rather than quietly dropped, and
  retiring the route does not retire that promise.
- **Both threads carry the process note** — 2026-08-15. taskmd's says we are switching to running the
  tool rather than describing it; the handoff skill's says the next finding arrives as a pull request.
  The second was a separate outward act in a second repository and went out on the owner's word, not
  on the first authorisation.

**Outputs produced**
- The owner's global working preferences — *Working across my own repositories*, five rules
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §7 — the retirement, the measurement, and what
  the two sent registers now are
- [`../docs/upstream/taskmd.md`](../docs/upstream/taskmd.md),
  [`../docs/upstream/handoff-skill.md`](../docs/upstream/handoff-skill.md) — one line each
- [`uchimata2/taskmd#1`](https://github.com/uchimata2/taskmd/issues/1) and
  [`uchimata2/handoff-skill#75`](https://github.com/uchimata2/handoff-skill/issues/75) — the process
  note, posted on both

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| One operative place, loading in all five projects | met | The owner's global preferences, ~1.2 KB, between the token-budget section and the machine notes. Loaded on every turn of every session, so `bpmn`, `ecoctx`, `Handoff`, `htmldeck` and `taskmd` all receive it without a line being added to any of them. |
| No second copy of the rule | met | §7 carries the **ruling** — date, measurement, what changes — and names the global file as the operative statement. That is a record of a decision, not a competing authority. |
| The other four checked, result recorded | met | Three have a `CLAUDE.md`, one has none; no ritual text in any of them contradicts the rule. Recorded in §3 as a negative, since a check that finds nothing is worth the same as one that finds something only if it is written down. |
| §7 records the retirement with its measurement | met | 34 KB of comments, 111 KB of records, 0 of 4 tasks changing behaviour, and `O-T4` named as the reason the rule is *report by patch* rather than *stop reporting*. |
| Both registers say the route is retired | met | One line in each handover record, pointing here, and both state that the correction terms they were sent under still hold. |
| `python tools/tasks/lint.py` green | met | Four steps: index, `check`, `refcheck`, `findings`. |

**On what this actually changes for the next session**
The next defect this repository finds in taskmd or the handoff skill does not produce a task file, a
register row, an issue, or a reply to a reply. It produces a branch in the repository that has the
defect. **The saving is not the prose — it is that a diff cannot be argued with in paragraphs**, which
is what the 34 KB was.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-15 | → done | **The register-and-issue route is retired the day the last correction it produced was closed.** Measured: 33,881 bytes of issue comments, 65,506 bytes of task records here, 11,816 bytes of register, and **0 of 4 local tasks changed a line of behaviour**. Replaced by five rules in the owner's global preferences — send a branch not a report, never assert another tool's behaviour without the command that proves it, one round trip, report only what breaks a gate or destroys data, never mirror the exchange into task records. One operative home outside all five repositories, because a copy per project is the duplication the rule itself forbids. The other four projects were checked and needed no edit. `O-T4` is why this is *report by patch*, not *stop reporting*. |
| 2026-08-15 | → proposed | Raised by the owner after reading the correction thread: informing two repositories by hand and asking both to send messages through GitHub does not scale, and the cost of one completed exchange was asked for and measured. `s`, `decision`, `PH3`. |
