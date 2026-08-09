---
id: T-046
title: Extend task.py to the three things it cannot currently see
type: fix
status: proposed
phase: specify
parent: T-042
blocked_by: []
related: [T-029, T-031, T-037, T-039]
work_package: none
owner: the project owner
created: 2026-08-09
updated: 2026-08-09
deliverables:
  - tools/tasks/task.py
  - tasks/TASK-WORKFLOW.md
---

# T-046 — Extend task.py to the three things it cannot currently see

## 1. Specify

**Outcome**
`python tools/tasks/task.py check` resolves `§` references as well as links and paths;
`task.py deliverables` reports outstanding work as well as delivered work; and the `--closing`
working-directory check stops being a silent no-op in a fresh clone. All three are the same defect
class the tool already names in its own output — **a report that looks complete** (**L-05**).

**Why this one**
`check` prints *"614 document pointer(s) checked, 0 broken"*, which is true and is read as a verdict
on the repository's references. It is not. Three gaps, each measured:

**1 · Section references — 1141 of them, none validated (F-5).** This is the mechanism **L-39** was
written for, and [T-037](T-037-record-in-the-ruleset-which-rules-no-check-can-reach.md) swept only
the `§11` instance. Still dead, in live prose:

- `docs/BRIEF.md:243` → `DESIGN-SYSTEM.md §9.4` for the semantic-heading rule; §9 is *"What is not
  covered"* and has no subsections. The rule is DS-090 in §3.3.
- `docs/BRIEF.md:324` → `DESIGN-SYSTEM.md §9.2`. The reasoning is in `DESIGN-RATIONALE.md` §4.
- `§9.1`, `§9.3`, `§9.5` cited the same way from T-002, T-007, T-014 and T-016 — all of them
  T-014's old re-scoping section, which **no commit of `DESIGN-SYSTEM.md` has ever contained.** The
  same failure as `§11`, in a family nobody swept.
- `EVALUATION.md §0` cited **five times** — `BRIEF.md:304`, `EVALUATION.md:369`, T-023, T-024,
  T-026 — and `EVALUATION.md` has no §0.
- `R3 §5.2`, `§5.3`, `§9.2` from T-016:131 resolve to nothing.

**2 · The deliverables report can only measure closed work (F-7).** All eight open tasks declare
`deliverables: []`, so the report reads:

```
59 declared output(s); 0 not on disk yet.
```

Every one of the 59 belongs to a `done` task. A report whose "not on disk yet" column is
structurally always zero is the failure `check`'s own success line was rewritten to avoid.

**3 · `--closing` cannot see an absent directory (F-18).** `leftovers = os.listdir(WORKING) if
os.path.isdir(WORKING) else []` — git carries no empty directory, so in a fresh clone
`deliverables/_working/` does not exist, the leftover check finds nothing, and `--closing` reports
the stricter pass having run one fewer test than it claims.

**Scope**
- In: resolving `<named document> §n[.m]` in prose, and failing on a miss like a dead link.
- In: the rule that makes the resolution decidable, written into `TASK-WORKFLOW.md` — see the
  answered question below.
- In: giving `EVALUATION.md`'s preamble a `## 0.` heading, since five documents already cite it that
  way, `DESIGN-SYSTEM.md` already numbers its own preamble §0, and editing one heading is cheaper
  and more honest than editing five citations.
- In: `deliverables` reporting open tasks separately, and a `check` rule for what an open task owes
  — see the answered question below.
- In: `--closing` failing, or saying so, when `deliverables/_working/` is absent.
- Out: back-filling `deliverables:` on the eight open tasks. That is content, and it belongs to
  whoever specifies each task; this task makes the absence visible.
- Out: correcting the dead `§` references it finds. They are
  [T-045](T-045-sweep-the-stale-claims-across-the-live-documents.md)'s and the task files' own; this
  task supplies the instrument. **The check ships red if it must** — a red run naming real dead
  pointers is the correct state to hand over.

**Inputs**
- [`tools/tasks/task.py`](../tools/tasks/task.py) — `check`, `deliverables`, `WORKING`
- [`tasks/TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §6 — *What `check` enforces*, which this extends
- [`docs/LESSONS.md`](../docs/LESSONS.md) — **L-05**, **L-09**, **L-39**
- [T-042](T-042-audit-the-whole-repository-against-itself.md) §2, F-5, F-7 and F-18

**Acceptance criteria**
- [ ] A `§` reference to a heading that does not exist is a `check` failure, and the self-test
      demonstrates it on a seeded miss (**L-04**)
- [ ] The resolver is shown to **pass** `R7 §5.3` and `DESIGN-SYSTEM §0.8` and **fail**
      `DESIGN-SYSTEM §9.4` and `EVALUATION §0` — the four cases that decide the rule
- [ ] `EVALUATION.md` carries a `## 0.` heading and the five citations resolve unchanged
- [ ] `check`'s success line states how many `§` references were resolved and how many were skipped,
      the way it already does for pointers
- [ ] `deliverables` distinguishes open from closed and names any open task declaring none
- [ ] `--closing` does not pass silently when `deliverables/_working/` is absent
- [ ] Every rule this adds is in `TASK-WORKFLOW.md` §6 before it is in the tool, and the two agree —
      *"where the two disagree, one of them is a bug"*

**Open questions**
- ~~How is `§5.3` distinguished from a dead subsection reference, given that `R7 §5.3` means item 3
  of section 5 and `DESIGN-SYSTEM §9.4` means nothing at all?~~ **Answered 2026-08-09, from L-39's
  own reason — *cite the content, not the address*, and an address is only citable if the document
  carries it.** The rule: **a `§n.m` reference resolves when `n.m` is a heading, or when `n` is a
  heading and `m` is an ordinal in a numbered list directly under it.** Both existing conventions
  survive and neither is ambiguous, because in both cases **the number is printed in the target
  document** and a reader can verify it. A number that exists only as the reader's own count of an
  unnumbered list is not an address and may not be cited. Checked against the four cases above: it
  passes `R7 §5.3` and `DESIGN-SYSTEM §0.8`, and fails `DESIGN-SYSTEM §9.4` and `EVALUATION §0` —
  which is exactly the live/dead split, so the rule needs no exception list.
- ~~What does an open task owe the deliverables report?~~ **Answered 2026-08-09 from
  `TASK-WORKFLOW.md` §3's own wording** — `deliverables:` is *"the only place an unproduced output is
  written as a path"*, so a task with a known output and an empty list is withholding the one fact
  the field exists for. **A task at `specified` or later must declare at least one deliverable**;
  `proposed` may be empty, because a proposal need not yet know what it produces. That makes the
  rule a gate on the transition rather than on the file, which is where the information actually
  becomes available.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <path>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-09 | → proposed | Raised by [T-042](T-042-audit-the-whole-repository-against-itself.md), findings F-5, F-7 and F-18. Three gaps in one file, all of them **L-05**: a pointer check that validates 614 references and cannot see 1141 more, a deliverables report whose outstanding column is structurally always zero, and a `--closing` test that is a no-op in every fresh clone. **F-5 is L-39 unswept** — T-037 chased `§11` and the `§9.1`–`§9.5` family survived, two of them in `BRIEF.md`'s live prose. The resolution rule is settled in §1 against the four cases that decide it, so `plan` starts from a testable definition rather than from the ambiguity. |
