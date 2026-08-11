---
id: T-046
title: Extend task.py to the three things it cannot currently see
type: fix
status: done
phase: review
parent: T-042
blocked_by: []
related: [T-029, T-031, T-037, T-039, T-045]
work_package: none
shipped_in: 0.1.0
owner: the project owner
created: 2026-08-09
updated: 2026-08-12
deliverables:
  - tools/docs/refcheck.py
  - tasks/TASK-WORKFLOW.md
  - docs/EVALUATION.md
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
- `tools/tasks/task.py` — `check`, `deliverables`, `WORKING`
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
| 1 | Write both rules into `TASK-WORKFLOW.md` **before** the tool, per criterion 7 | §6.1 and §6.2, which the tool then implements rather than defines |
| 2 | Prototype the resolver outside the repository and **measure it against the whole corpus** before wiring it in | The naive binding was wrong a third of the time; measured, not assumed |
| 3 | Bind a reference to a document by **adjacency**, and skip code spans and fenced blocks | 426 resolved, 912 skipped as unbound, and a document can quote a dead pointer again |
| 4 | Wire it into `check` as a failure, reporting resolved and skipped counts on the success line | The line now says what it did *not* check, like the pointer line above it |
| 5 | Number `EVALUATION.md`'s preamble `## 0.` | Five citations resolve without any of them being edited |
| 6 | Fix the dead references the instrument found | Four live miscitations corrected; the phantom `§11` and `§9.n` mentions marked as tokens |
| 7 | Split `deliverables` into outstanding and delivered, and gate `specified`-or-later on declaring one | A report whose outstanding column can be non-zero |
| 8 | Make an absent `deliverables/_working/` its own answer rather than a silent pass | `--closing` fails; a normal run notes it |
| 9 | Apply `.gitignore` to the markdown-link scan, the inconsistency [T-045](T-045-sweep-the-stale-claims-across-the-live-documents.md) found | Both scans now answer the same question |
| 10 | Give `task.py` the `self_test()` it never had, constructing each failure | Every new check demonstrated failing, on purpose |

## 3. Implement

**Decisions & assumptions**
- **A reference binds to a document only when the name is *adjacent* to the mark**, separated by
  markdown punctuation and at most one space. This was measured, not chosen: the obvious rule —
  *the nearest document named before the mark* — reported **202 dead references, and a third of
  them were the rule's own fault**, binding `R4-prior-art.md` to a `§2.1` that meant the citing
  document's own section. Adjacency reports **28**, all real. — 2026-08-09
- **A `§` inside a code span or fence is literal text, not a pointer.** Without this rule the
  repository cannot record that a pointer is dead: the audit had to write `` `DESIGN-SYSTEM.md §11` ``
  a dozen times to say it never existed, and every one would have been a fresh failure. Adding it
  took the dead count from 28 to 5 — and **all five of those were genuine live miscitations**, which
  is the evidence that the rule separates mention from citation rather than just suppressing noise.
  — 2026-08-09
- **Deviation: the dead references were fixed here, not left.** §1 puts correcting them out of
  scope and assigns them to [T-045](T-045-sweep-the-stale-claims-across-the-live-documents.md) —
  which closed before this task ran, without them, so the alternative was a **permanently red gate**,
  and a gate that is always red is one nobody reads. Four were live miscitations and were corrected
  (`BRIEF.md` §9.4 → §3.3 and DS-090; T-016's `§9.3`; T-021's `§9.1`; T-005's three `§11`s). The
  phantom-family mentions became code spans, which is what the rule they now violate says a mention
  is. — 2026-08-09
- **`self_test()` asserts both directions of every rule.** A resolver that returns `True` for
  everything satisfies *"§5.3 resolves"*; only *"§9.4 does not"* catches it. The same shape for
  adjacency — the negative case is the heuristic this task rejected, kept as a regression. — 2026-08-09

**Outputs produced**
- `tools/tasks/task.py` — the section resolver, `doc_aliases`,
  `section_index`, `strip_code`, the split `deliverables` report, the `--closing` fix, the
  `.gitignore` fix in the link scan, and `self_test()`
- [`tasks/TASK-WORKFLOW.md`](TASK-WORKFLOW.md) — §6.1 and §6.2, plus three lines in *What `check`
  enforces*
- [`docs/EVALUATION.md`](../docs/EVALUATION.md) — `## 0.` heading
- Corrections in [`docs/BRIEF.md`](../docs/BRIEF.md),
  [T-005](T-005-build-check-the-gate-the-deck-must-pass.md),
  [T-016](T-016-the-interaction-and-motion-layer.md),
  [T-021](T-021-the-reflow-view-and-the-resolution-contract.md)

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A `§` to a heading that does not exist is a `check` failure, demonstrated on a seeded miss (**L-04**) | **met** | Reverting `BRIEF.md`'s one correction gives `DEAD SECTION docs\BRIEF.md -> docs\DESIGN-SYSTEM.md has no §9.4`, exit 1. `self_test()` seeds the same miss on every invocation and exits if it is not reported |
| The resolver **passes** `R7 §5.3` and `DESIGN-SYSTEM §0.8` and **fails** `DESIGN-SYSTEM §9.4` and `EVALUATION §0` | **met** | Run against the real documents: `R7 §5.3 RESOLVES` · `DESIGN-SYSTEM §0.8 RESOLVES` · `DESIGN-SYSTEM §9.4 DEAD` · `EVALUATION §0 DEAD (as it stood before T-046)`, and `RESOLVES` now that the heading exists |
| `EVALUATION.md` carries a `## 0.` heading and the five citations resolve unchanged | **met** | `## 0. What the score is, and what it is not`. None of the five citing sites was edited — which is the reason §1 chose this over rewriting them |
| `check`'s success line states how many `§` were resolved and how many skipped | **met** | `426 section reference(s) resolved, 0 dead; 912 not bound to a document and skipped.` The skipped figure is the honest half: most marks in this repository are bare `§3`s inside a task file, and the citation form does not bind them |
| `deliverables` distinguishes open from closed and names any open task declaring none | **met** | Two tables, two totals — `5 output(s) declared by open tasks, 1 of them not on disk yet` against `77 declared by closed tasks` — then `10 open task(s) declare no deliverable at all`, each marked correct-for-`proposed` or a `check` failure |
| `--closing` does not pass silently when `deliverables/_working/` is absent | **met** | With the directory moved aside: `NO WORKING DIR deliverables\_working does not exist, so the leftover-file check had nothing to run against`, exit 1; a normal run downgrades it to a note. `git ls-files deliverables/` is empty, which is F-18's premise confirmed |
| Every rule this adds is in `TASK-WORKFLOW.md` §6 before it is in the tool, and the two agree | **met** | §6.1 and §6.2 written first, and three lines added to *What `check` enforces*. The tool's docstrings cite the section rather than restating it |

**What the numbers say about the gap this closed**

```
before   614 document pointer(s) checked, 0 broken        1394 § references, none validated
after    713 document pointer(s) checked, 0 broken         426 resolved, 0 dead; 912 skipped
```

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-09 | (no change) | **Declared output relocated, and one part of it did not survive.** `tools/tasks/task.py` was retired by [T-062](T-062-retire-the-pre-split-task-tool-and-repoint-what-points-at-it.md). The section resolver, `doc_aliases` and the adjacency rule are in `tools/docs/refcheck.py` verbatim, so the deliverable points there. **The `--closing` leftover-file check did not move** — it was task-side and taskmd has no equivalent, so that third of this task's output is gone rather than relocated, which is worth knowing before anyone cites this record as evidence the check still runs. |
| 2026-08-09 | → done | **The binding rule was measured before it was written, and the first one was wrong.** *The nearest document named before the mark* is the obvious reading of "`<named doc> §n`", and against the whole corpus it reported **202 dead references** of which a large share were its own fault — binding `R4-prior-art.md` to a `§2.1` that meant the citing document's own section. Requiring the name to be **adjacent** to the mark took it to 28. **Then the rule that mattered most:** a `§` inside a code span or fence is literal text, which took 28 to **5** — and all five were genuine live miscitations. That rule is not noise suppression; without it a repository cannot record that a pointer is dead, and this one had to write `` `DESIGN-SYSTEM.md §11` `` a dozen times to say so. **A deviation, and it was the alternative to a permanently red gate.** §1 puts fixing the dead references out of scope and assigns them to [T-045](T-045-sweep-the-stale-claims-across-the-live-documents.md), which had already closed without them — so leaving them meant shipping a gate that is always red, and a gate nobody can act on is one nobody reads. Four live miscitations were corrected and the phantom-family mentions became code spans. **`task.py` had no `self_test()` at all**, which is the common root of all three findings: a section resolver that did not exist, a deliverables column that was structurally zero, and a `--closing` test that no-opped in every fresh clone are three reports that could not fail, in a tool with nothing asserting that any of them could. Each new check is now demonstrated failing on a seeded break, and the negative cases are kept as regressions — including the binding heuristic this task rejected. |
| 2026-08-09 | → planned | §1 accepted with both open questions already answered in it, so `specify` was accept-not-compose. Ten steps, and two orderings were deliberate: the rules go into `TASK-WORKFLOW.md` **before** the tool, because criterion 7 asks for it and because a tool that defines its own rule cannot disagree with the spec; and the resolver was prototyped and measured against the corpus outside the repository before being wired in, which is what caught the binding rule being wrong. |
| 2026-08-09 | → proposed | Raised by [T-042](T-042-audit-the-whole-repository-against-itself.md), findings F-5, F-7 and F-18. Three gaps in one file, all of them **L-05**: a pointer check that validates 614 references and cannot see 1141 more, a deliverables report whose outstanding column is structurally always zero, and a `--closing` test that is a no-op in every fresh clone. **F-5 is L-39 unswept** — T-037 chased `§11` and the `§9.1`–`§9.5` family survived, two of them in `BRIEF.md`'s live prose. The resolution rule is settled in §1 against the four cases that decide it, so `plan` starts from a testable definition rather than from the ambiguity. |
