---
id: T-045
title: Sweep the nine stale claims the audit found across the live documents
type: fix
status: proposed
phase: specify
parent: T-042
blocked_by: [T-043]
related: [T-044, T-047, T-028, T-037]
work_package: none
owner: the project owner
created: 2026-08-09
updated: 2026-08-09
deliverables:
  - CLAUDE.md
  - docs/BRIEF.md
  - docs/DESIGN-SYSTEM.md
  - docs/DESIGN-RATIONALE.md
  - .handoff/config.md
---

# T-045 — Sweep the nine stale claims the audit found across the live documents

## 1. Specify

**Outcome**
Nine statements that were true when written and are false now are corrected in the documents a
reader acts on. None of them is a design change; every one is a fact that moved and a sentence that
did not.

**Why this one**
Each is individually trivial and the set is not: they are concentrated in the three files a new
session is told to read first — `CLAUDE.md`, `docs/BRIEF.md`, `.handoff/config.md` — and two of them
would send a reader to a rule the project has already met or a measurement that no longer exists.

**The nine, as ten rows — F-10 is one finding stated in two separate sentences**

| # | Where | Says | Measured / true now |
| :-- | :--- | :--- | :--- |
| F-9 | `DESIGN-SYSTEM.md` §9 | *"no deck in this repository yet satisfies the deliverable contract — the rules that matter most are the least exercised"* | [T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) met it 2026-08-07; `BRIEF.md` records the publishing gate as clear. The **second** half of the sentence is still true and worth keeping — the deliverable rules remain the least exercised — so this is a rewrite, not a deletion |
| F-10a | `CLAUDE.md` line 12 | *"WP1 research is complete but for one measurement"* | All ten WP1 tasks are `done`. The line never said which measurement, and it is not recoverable from the commit that added it |
| F-10b | `CLAUDE.md` line 15 | *"decides 79 of the 111 rules a gate owns and names the other 32"* | The corrected split comes from [T-043](T-043-make-the-gates-coverage-account-provable.md). Same figure appears in `BRIEF.md`, `EVALUATION.md` §2 and `skills/htmldeck/references/pipeline.md` |
| F-14 | `BRIEF.md` | *"`—` (49, every `judge` rule)"* | 49 is 43 `judge` **plus** the 6 rules whose `Check` is `—`. The parenthesis names the wrong set |
| F-15 | `DESIGN-RATIONALE.md` Sources | *"`R1`–`R6` in `research/`"* | R7 exists, and §2.1 and the printable-mode rules depend on it |
| F-16 | `BRIEF.md` / `EVALUATION.md` | 160 rules · 161 rules counting DS-000 | Both correct. Neither says why they differ where it is read, and they are read together |
| F-17 | `.handoff/config.md` | *"`reference/` holds proven prior art… read it for behaviour that is already verified, not for code to copy wholesale"* | `reference/` holds one 1.2 KB prompt file. The paragraph describes a codebase that is not there |
| F-19 | `DESIGN-SYSTEM.md` DS-063, `DESIGN-RATIONALE.md` §3, `examples/README.md` | 116 / 336 values · 40 / 84 values | Both are real: `contract.py` samples four slides by default (`SAMPLE = [0, 4, 7, 11]`) and `--all` sweeps twelve. Neither figure says which it is |
| F-20 | `DESIGN-RATIONALE.md` | §5 → §5.5 → §5.6 → §5.7 → §6 | There is no §5.1–§5.4. The numbering was chosen to avoid renumbering and reads as four missing sections |
| F-21 | `tasks/T-025-…-twelve-…md` | filename says *twelve* | Its title, its body and `DESIGN-RATIONALE.md` §2.1 all say **thirteen** |

**The 183 KB figure travels with this sweep.** `BRIEF.md`'s definition of done and T-008's log both
carry it; the measurement is [T-044](T-044-restore-the-seeded-defect-fixture-and-its-claims.md)'s and
the correction of these copies is here, so the deck is measured once.

**Scope**
- In: the ten rows above, and any further copy of the same fact found while making each edit —
  these figures travel, and F-10b already appears in five places.
- In: deciding whether §5.5–§5.7 renumber or the gap is stated. Renaming a section is cheap here
  because nothing loads `DESIGN-RATIONALE.md` at runtime, but §5.5 is cited from four task files
  and a rename makes those pointers wrong, which is the failure this audit is about.
- Out: any rule change, any measurement, any structural edit. If a correction turns out to need a
  ruling, it stops and becomes its own task rather than being decided inside a sweep.
- Out: `examples/README.md` — [T-044](T-044-restore-the-seeded-defect-fixture-and-its-claims.md) owns
  it and re-measures rather than corrects.
- Out: the `X-nn` rename, which touches `DESIGN-RATIONALE.md` in the same session —
  [T-047](T-047-give-the-rationale-conflicts-their-own-id-namespace.md). **Sequence it after this
  task or before it, never alongside**; both edit §2 and §5.

**Inputs**
- [T-042](T-042-audit-the-whole-repository-against-itself.md) §2 — F-9, F-10, F-14, F-15, F-16, F-17,
  F-19, F-20, F-21, and the 183 KB row of F-4
- [T-043](T-043-make-the-gates-coverage-account-provable.md) — the corrected coverage split
- `python tools/deck/ruleset.py` — every count these documents state

**Acceptance criteria**
- [ ] Each of the ten rows corrected, and the correction states the measured value rather than
      removing the claim
- [ ] Every other copy of each corrected fact found and fixed — searched for, not assumed absent
- [ ] The `Reach` and rule-count figures come from a `ruleset.py` run in this session, pasted
- [ ] The DS-063 sample size is stated wherever the figure is, in both documents
- [ ] `python tools/tasks/task.py check` passes, including after any file rename
- [ ] No rule text, no `DS-nnn`, and no acceptance criterion changed by this task

**Open questions**
- none

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
| 2026-08-09 | → proposed | Raised by [T-042](T-042-audit-the-whole-repository-against-itself.md) — findings F-9, F-10, F-14, F-15, F-16, F-17, F-19, F-20, F-21, and F-4's 183 KB row. Ten small corrections kept as one task because they share a failure mode rather than a location: **a figure stated in one document and copied into four**, which is why each criterion asks for the other copies to be hunted rather than assumed. `blocked_by` [T-043](T-043-make-the-gates-coverage-account-provable.md), which decides the coverage split five of these documents quote — correcting the prose first would write the wrong number twice. |
