---
id: T-045
title: Sweep the nine stale claims the audit found across the live documents
type: fix
status: done
phase: review
parent: T-042
blocked_by: [T-043]
related: [T-044, T-047, T-028, T-037]
work_package: none
shipped_in: 0.1.0
owner: the project owner
created: 2026-08-09
updated: 2026-08-12
deliverables:
  - CLAUDE.md
  - docs/BRIEF.md
  - docs/DESIGN-SYSTEM.md
  - docs/DESIGN-RATIONALE.md
  - docs/EVALUATION.md
  - .handoff/config.md
  - skills/htmldeck/references/pipeline.md
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
| 1 | Take the authoritative figures from a run in this session — `ruleset.py --counts` and `check.py` — before touching any prose | 78 / 111 / 33, and the full count set, pasted rather than recalled |
| 2 | Search for every copy of each travelling figure, then correct all of them in one pass | The coverage split in 5 files, 183 KB in 2, `R1`–`R6` in 1 |
| 3 | Correct the two claims that would mislead a reader into acting — `CLAUDE.md`'s phantom measurement, `DESIGN-SYSTEM.md` §9's met contract — keeping the half of each that is still true | Two rewrites, no deletions |
| 4 | Explain the two disagreements rather than picking a side: 160 vs 161, and 116/336 vs 40/84 | Both stated with the reason they differ, in both documents that carry them |
| 5 | Decide the §5.1–§5.4 gap from its own cost | Stated, not renumbered — §5.5 is cited from four task files |
| 6 | Rename T-025's file and repoint every link, found by search | 13 links across 10 files, plus one archived handoff |
| 7 | Re-run both gates | Clean, and one further `task.py` inconsistency found on the way |

## 3. Implement

**Decisions & assumptions**
- **Nothing was corrected by deletion.** Every row's fix states the measured value or the reason two
  values differ, because a claim that vanishes leaves a reader who remembers it with no way to find
  out what replaced it — which is how several of these survived. — 2026-08-09
- **The §5.1–§5.4 gap is stated, not renumbered.** §1 left the choice open. Renumbering is cheap in
  the file and expensive outside it: §5.5 is cited from four task files, so a rename trades a
  cosmetic oddity for four dead pointers — the exact defect class
  [T-042](T-042-audit-the-whole-repository-against-itself.md) exists to remove. — 2026-08-09
- **Dated log rows are annotated, never rewritten.** T-008's two 2026-08-07 rows state 183 KB, which
  was true when written; editing them would make the log claim a measurement that did not exist.
  A new `(no change)` row carries the current figure, per **TASK-WORKFLOW.md** §5. The same
  reasoning left `DESIGN-SYSTEM.md`'s and `EVALUATION.md`'s historical *"it went stale again"*
  passages intact — they are the evidence for the instruction beside them. — 2026-08-09
- **Two disagreements were explained rather than resolved**, because in both cases both figures are
  correct and the defect is the silence. 160 vs 161 is DS-000, stated as prose in §0 and therefore
  invisible to a row count — it moves `guidance` from 5 to 6 and nothing else. 116/336 vs 40/84 is a
  twelve-slide sweep against `contract.py`'s four-slide default. — 2026-08-09
- **A fourth `task.py` blind spot was found and left for
  [T-046](T-046-extend-task-py-to-what-it-cannot-see.md).** `check` applies `.gitignore` to its prose
  scan and **not** to its markdown-link scan, so an archived, gitignored handoff is link-checked as
  though it shipped. The rename made it fail. Fixed the pointer to unblock; the inconsistency is
  recorded in §4 and belongs to the task that owns `task.py`'s reach. — 2026-08-09

**Outputs produced**
- [`CLAUDE.md`](../CLAUDE.md) · [`docs/BRIEF.md`](../docs/BRIEF.md) ·
  [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) ·
  [`docs/DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) ·
  [`docs/EVALUATION.md`](../docs/EVALUATION.md) · `.handoff/config.md` ·
  `skills/htmldeck/references/pipeline.md`
- [T-008](T-008-package-document-and-publish.md) — one `(no change)` log row
- `tasks/T-025-…` renamed to `…-thirteen-…`, with 13 links repointed across 10 files

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Each of the ten rows corrected, stating the measured value rather than removing the claim | **met** | All ten, plus the 183 KB row. Two are rewrites that keep the true half: `DESIGN-SYSTEM.md` §9 now records the contract as met **and** keeps *the rules that matter most are the least exercised*; `CLAUDE.md` drops the phantom measurement and keeps the status |
| Every other copy of each corrected fact found and fixed — searched for, not assumed absent | **met** | The coverage split was in **five** places (`CLAUDE.md`, `BRIEF.md`, `EVALUATION.md`, `pipeline.md`, `DESIGN-RATIONALE.md`), 183 KB in **three** (`BRIEF.md` and twice in T-008's log), `R1`–`R6` in one. A closing scan for all four patterns returns only T-037's *"the other 32"*, which is about §11's conditions and not the gate |
| The `Reach` and rule-count figures come from a `ruleset.py` run in this session, pasted | **met** | `by Reach yes 107 never 1 off-gate 3 — 49`; `by Label, rows only hard 114 default 41 guidance 5 = 160`; `by Label, declared … guidance 6 = 161`. The gate's split from `check.py`: `checked 78 … excused in the rules 4 … excused here 29 … buckets sum to 111` |
| The DS-063 sample size stated wherever the figure is, in both documents | **met** | DS-063's own row names both the twelve-slide sweep and the four-slide default; `DESIGN-RATIONALE.md` §3 gains a paragraph naming which run each set comes from and that they do not contradict |
| `task.py check` passes, including after the file rename | **met** | `OK - 51 tasks, … 701 document pointer(s) checked, 0 broken` |
| No rule text, no `DS-nnn`, and no acceptance criterion changed by this task | **met** | The only `DS-nnn` edit is DS-063's trailing *measured* note, which is provenance rather than rule text; the rule's tolerances and wording are untouched |

**One finding, handed to the task that owns it.** `task.py check` applies `.gitignore` to its prose
scan and **not** to its markdown-link scan, so a gitignored, archived handoff is link-checked as
though a fresh clone contained it — which is the opposite of the question the prose scan says it is
answering. The T-025 rename made it fail on a file nobody publishes. Recorded for
[T-046](T-046-extend-task-py-to-what-it-cannot-see.md), whose §1 already covers `task.py`'s reach;
raising a separate task for a fourth item in a list of three would be worse than adding it to that
list.

**Child fix tasks raised**
- none — the `task.py` inconsistency above goes to
  [T-046](T-046-extend-task-py-to-what-it-cannot-see.md) rather than a new task

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-09 | → done | **Ten rows, and the count that matters is how far each one had travelled.** The coverage split was in five documents, 183 KB in three, and no single edit would have been wrong on its own — which is the failure mode the set was grouped around and the reason every criterion says *search, do not assume*. **Two corrections needed a rewrite rather than a replacement**, because half of each sentence was still true: `DESIGN-SYSTEM.md` §9 said no deck here satisfies the deliverable contract *and* that those rules are the least exercised — the first is false since T-028, the second is still the sharpest thing in the section and is now the point of the paragraph. **Two disagreements were explained rather than settled**, because in both cases both figures are right and the silence was the defect: 160 against 161 is DS-000, stated in §0's prose and so invisible to a row count, and it moves the `guidance` figure and nothing else; 116/336 against 40/84 is a twelve-slide sweep against `contract.py`'s four-slide default. **The §5 gap was stated, not renumbered** — §5.5 is cited from four task files, so renumbering would trade an appearance for four dead pointers, which is the class of defect this audit exists to remove. And **dated log rows were annotated, never rewritten**: T-008's two 183 KB rows were true on 2026-08-07 and a new row carries the current figure. The rename of T-025 turned up a fourth `task.py` inconsistency — `.gitignore` governs the prose scan and not the link scan — which went to [T-046](T-046-extend-task-py-to-what-it-cannot-see.md) rather than to a new task. |
| 2026-08-09 | → planned | §1 accepted as written. Unblocked by [T-043](T-043-make-the-gates-coverage-account-provable.md), whose corrected split — **78 of 111, the other 33** — is the figure five of these documents quote; taking the number from a run in this session rather than from T-043's prose is step 1 for the same reason the task was ordered second. Worked in a separate session from [T-047](T-047-give-the-rationale-conflicts-their-own-id-namespace.md) as both tasks require, since both edit `DESIGN-RATIONALE.md`. |
| 2026-08-09 | → proposed | Raised by [T-042](T-042-audit-the-whole-repository-against-itself.md) — findings F-9, F-10, F-14, F-15, F-16, F-17, F-19, F-20, F-21, and F-4's 183 KB row. Ten small corrections kept as one task because they share a failure mode rather than a location: **a figure stated in one document and copied into four**, which is why each criterion asks for the other copies to be hunted rather than assumed. `blocked_by` [T-043](T-043-make-the-gates-coverage-account-provable.md), which decides the coverage split five of these documents quote — correcting the prose first would write the wrong number twice. |
