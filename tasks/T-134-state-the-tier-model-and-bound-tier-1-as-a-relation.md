---
id: T-134
title: State the tier model and bound tier 1 as a relation
type: decision
status: done
phase: review
parent: T-130
blocked_by: []
related: [T-130, T-133]
work_package: PH3
finding: CE-11
shipped_in: 0.2.4
owner: the project owner
business_value: high
effort: s
created: 2026-08-13
updated: 2026-08-13
deliverables:
  - CLAUDE.md
---

# T-134 — State the tier model and bound tier 1 as a relation

## 1. Specify

**Outcome**
This project states what its always-loaded set is, how membership is decided, and what bounds it —
so that every later cut to [`../CLAUDE.md`](../CLAUDE.md) is decided against a rule rather than
negotiated. **The finding is `CE-11`**, stated in
[`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.1; it is not restated here.

**This adopts a decision already taken upstream, and that is the point.** The taskmd project settled
this in its own audit: the membership rule is *what the harness loads without being asked* — a
property of the tree rather than a list someone maintains — with three tiers, a budget on tier 1
only, and the bound written as a **relation** to something counted from the same tree so that no
number and its justification can drift apart. It rejected, in writing, both alternatives an outsider
arrives with: widening the budget to cover every file, and budgeting each file separately. Nothing
here is being invented, and the audit that found this went looking for something to send upstream and
found the answer already there — see [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §7.2,
`O-T1`.

**Measured here, 2026-08-13:** tier 1 is **338 lines across three files** — the global preferences
(92), this project's `CLAUDE.md` (207), and the memory index (39) — or **27,633 bytes / ~6,908
estimated tokens**, before a skill-description block of a further ~5,200.

**It is an enabler and saves nothing by itself.** `CE-01` (split the release chronology out of
`CLAUDE.md`) and `CE-04` (one operative home per cumulative rule) are the cuts it makes decidable,
and it should land first so those cuts are not chosen to fit a number nobody agreed.

**Scope**
- In: the membership rule, the tiers, and the bound, written in the file they govern — which under
  this model is tier 1 itself, where a reader meets the boundary at the moment it binds them.
- In: **establishing tier 1 by observation, not by any file's claim about itself.** A document
  asserting a load discipline the harness does not implement is worse than one over budget, because
  it makes the bound unfalsifiable — that is the upstream finding's sharpest half.
- In: the measurement, dated, with the command that reproduces it.
- In: stating explicitly that tiers 2 and 3 carry no budget, and what that accepts.
- Out: moving any content. A budget that also chooses the cut is a cut chosen to fit a number; the
  moves are `CE-01` and `CE-04` and they are not this task.
- Out: a hand-set constant. It is the pair that has to be edited together, and it always loses.
- Out: the global preferences file, which is not this repository's.

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.2 — what a session working an audit finding owes beyond the finding: what to check, what to report, and where each thing goes. Read before starting
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §2.1 and §6.1 — the measurement and `CE-11`
- [`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
  §2.1 — the tier model, the membership rule and the relation-bound, stated portably
- The upstream precedent, read at execution rather than named here

**Acceptance criteria**
- [ ] The always-loaded set is named by a **rule**, not a list, and the rule is checkable against the
      tree
- [ ] Tier 1 was established by observation — what a session receives unasked — and the method is
      recorded, not just the answer
- [ ] The bound is a relation between two quantities both counted from the tree; **no constant is
      written anywhere**
- [ ] Tiers 2 and 3 are stated as carrying no budget, with what that accepts written down
- [ ] Today's measurement is recorded with its date and its command, in a place where being stale
      makes it evidence rather than a false rule
- [ ] If the project is over its own bound on the day it is set, that is stated as dated debt naming
      the task that closes it — **an unmet budget that reads as met is worse than no budget**
- [ ] No content moves

**Open questions**
- **Which relation?** taskmd bounds tier 1 against the flat, single-document alternative its split
  replaced. This project has no such alternative, so the second term has to be chosen. — the owner,
  or the implementer from the rule's own reason. **Answered 2026-08-13 by the implementer**: the
  smallest document this file defers to as an authority. The argument, and the two candidates it
  beats, are in §3.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Establish tier 1 by observation — what this session was given before its first tool call — and confirm the tree holds no second `CLAUDE.md` | the membership answer, and the method that produced it |
| 2 | Re-measure both candidate terms before writing anything (**§6.2**, rule 1), and again after the edit | dated figures, and the drift since the audit |
| 3 | Settle the open question: choose the relation's second term from the rule's own reason, and record the candidates that were rejected and why | the bound, and the argument for it |
| 4 | Write the tier model, the membership rule, the bound, the no-budget statement for tiers 2 and 3, and the debt into `../CLAUDE.md` | the deliverable |
| 5 | Fold the record — `BRIEF.md`'s row and execution order, `CONTEXT-AUDIT.md`'s rank row, and the one figure there this change moved | the record agrees with the tree |
| 6 | Write what the *method* learned where it survives: **L-88**, and a row in T-137 §1 | the general half, out of the task |
| 7 | Gates: `python tools/tasks/lint.py`, `python tools/docs/refcheck.py` | green |

## 3. Implement

**Decisions & assumptions**
- **The relation is `CLAUDE.md` < the smallest document it defers to** — `docs/BRIEF.md`,
  `docs/PUBLISHING.md`, `tasks/TASK-WORKFLOW.md`, `tasks/README.md`, `.taskmd/config.md`. This closes
  the open question, decided by the implementer from the rule's own reason rather than referred back.
  What the inequality asserts: once the file paid for on every turn costs more than any single
  document opened on demand, the split has inverted. — 2026-08-13
- **Two candidate second terms were rejected, and they fail in opposite directions.** A sum or mean of
  the deferred documents is slack — it would permit this file to triple. *The smallest file it links
  to at all* is unstable — the file cites fourteen task records as evidence, so an unrelated small
  document would tighten the budget by an order of magnitude. An **authority** set moves only when
  someone deliberately adds an authority. The general half is **L-88**. — 2026-08-13
- **Bytes, not lines.** `Measure-Object -Line` undercounts, `wc` is not everywhere, and the audit's
  own figures are bytes. The reproducing command is one line of Python and runs in both shells here.
  — 2026-08-13
- **The bound covers this repository's one tier-1 file.** The global preferences and the memory index
  are observed and named, and excluded from the bound because the repository cannot edit them; the
  memory index is `CE-10`'s subject. — 2026-08-13
- **The section went into `CLAUDE.md` rather than into a document it points at.** It is the file the
  rule governs and the only one guaranteed to be read before an edit to it, which is the whole
  argument of `CE-11`. The cost is stated rather than absorbed: the section is 2,690 bytes charged to
  every turn. — 2026-08-13
- **No task was raised for `CE-01` or `CE-04`.** Raising them is the owner's cut-off, unchanged since
  T-130's review; the debt names them so the next reader finds the fix without one. — 2026-08-13

**Outputs produced**
- [`../CLAUDE.md`](../CLAUDE.md) — the new section *What loads every turn, and what bounds it*: the
  membership rule, the three tiers, the observation and its method, the bound with its command, the
  no-budget statement for tiers 2 and 3, and the debt
- [`../docs/LESSONS.md`](../docs/LESSONS.md) — **L-88**, a budget written as a relation is only as
  good as what its second term is bound to
- [T-137](T-137-package-the-context-economy-method-as-a-skill.md) §1 — two rows in the
  implementation table: the design step the method has no word for, and what stating a budget costs
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) — §6's rank row struck, and §2.1's figure for
  this file re-measured with the drift stated
- [`../docs/BRIEF.md`](../docs/BRIEF.md) — the row folded to two cells, the execution order renumbered
  and its two internal row references moved with it

**Measurements, 2026-08-13**

| | Bytes | Lines |
| :--- | ---: | ---: |
| `CLAUDE.md` at the audit | 15,630 | 207 |
| `CLAUDE.md` before this edit | 15,952 | 211 |
| `CLAUDE.md` after | **18,642** | 249 |
| `.taskmd/config.md` — the smallest deferred document | 14,087 | 238 |
| Over the bound | **4,555** | |

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The always-loaded set is named by a rule, not a list, and the rule is checkable against the tree | met | *What the harness loads without being asked* — a property of the tree. The five documents named in the bound are the second term, not the membership rule |
| Tier 1 established by observation, and the method recorded | met | What the session received before its first tool call, then a check that the tree holds no second `CLAUDE.md`. Both the answer and the method are in the section |
| The bound is a relation between two quantities counted from the tree; no constant written | met | `CLAUDE.md` < the smallest document it defers to. No coefficient. The figures that appear are dated measurements, which criterion 5 requires |
| Tiers 2 and 3 stated as carrying no budget, with what that accepts | met | They are not paid every turn, so a size limit measures the wrong cost; it accepts that `BRIEF.md` and `LESSONS.md` grow without limit, and a tier-2 document loaded every turn has become tier 1 |
| Today's measurement recorded with its date and its command | met | In the section, with a one-line command that measures both terms and runs in either shell here |
| Over the bound on the day it is set — stated as dated debt naming what closes it | met | 18,642 against 14,087, over by 4,555, naming `CE-01` and `CE-04`. Neither is raised as a task, and the section says so |
| No content moves | met | Nothing was cut from `CLAUDE.md` or relocated. The file grew by 2,690 bytes, which is the honest cost of the criterion above it |

**Child fix tasks raised**
- none. `CE-01` and `CE-04` are the cuts this enables and remain the owner's to raise.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-14 | (no change) | `shipped_in` set to `0.2.4`, which it had been missing since it closed — the only closed task in the record without one. Found by [T-144](T-144-give-each-cumulative-rule-one-operative-home.md) while checking the release table it had just written. `60a82bb` is the closing commit and `v0.2.4` is the first tag containing it; `PUBLISHING.md` §8 step 8 owes this and no gate reads it. |
| 2026-08-13 | → proposed | Raised from [T-130](T-130-audit-the-context-economy-of-an-agent-driven-repository.md)'s ranking at the owner's review, fourth of four and the only one above `xs`. `CE-11`, and **the direction of travel is upstream to here**: the audit went looking for something to send taskmd about context budgeting and found they had settled it first, in more detail, with both alternatives rejected in writing. It saves nothing by itself — it decides what `CE-01` and `CE-04` are allowed to cut, which is why it is ranked with them rather than after them. One question is left open on purpose: taskmd's bound has a natural second term and this project's does not, so which relation to use is a choice rather than a copy. |
| 2026-08-13 | → specified | §1 arrived written from the owner's review, with the deliverable declared and the one open question named as the implementer's to settle. Nothing re-derived. |
| 2026-08-13 | → planned | Seven steps, and two of them exist only because §6.2 says so: measure before and after, and write what the *method* learned somewhere that outlives the task. |
| 2026-08-13 | → in_progress | The open question was the task. The relation is `CLAUDE.md` < the smallest document it defers to; the sum of the deferred set is slack and the smallest file it merely links to is unstable, so the second term is the **authority** set, which moves only by a deliberate act (**L-88**). |
| 2026-08-13 | → done | Seven criteria, all met, and the one that matters is the last: **the file is 4,555 bytes over the bound it just set**, written as dated debt naming `CE-01` and `CE-04` rather than as a rule already kept. 2,690 of those bytes are the section itself — stating a budget in the file it governs is charged to the budget, and that trade is argued rather than hidden. The audit's figure for this file had drifted 322 bytes in a day, which is §6.2's first rule earning itself. Neither cut is raised as a task: that cut-off is the owner's. |
