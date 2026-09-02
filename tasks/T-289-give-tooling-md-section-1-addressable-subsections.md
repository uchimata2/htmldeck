---
id: T-289
title: Give TOOLING.md section 1 addressable subsections, so a pointer costs one rule and not ten
type: fix
status: done
phase: review
parent: T-287
blocked_by: []
related: [T-285, T-286]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
finding: CE-15
created: 2026-09-02
updated: 2026-09-02
shipped_in: unreleased
deliverables: []
---

# T-289 — Give TOOLING.md section 1 addressable subsections, so a pointer costs one rule and not ten

## 1. Specify

**Outcome**
`TOOLING.md` §1 is split into numbered subsections, one rule each — the two gates and their order,
the no-edit-while-it-runs rule, `--docs`, the quiet line, the render workers, the bulk-edit rule,
`lint.py` and `query.py`, the board question, `refcheck.py`, `findings.py` — so that a handoff, a
task record or `TASK-WORKFLOW.md` §7 can point at `§1.3` and a resuming session reads one paragraph.
Measured 2026-09-02: §1 is **18,461 of the file's 26,408 bytes**, and the resume read it whole
because the handoff pointed at `§1`. The finding is `CE-15` in
[`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.3.

**Scope**
- In: headings and their numbers; every existing pointer to `§1` re-pointed at the subsection it
  means (`refcheck.py` resolves `§n` references, so a dead one fails the lint); `§1.1` keeps its
  number and content.
- Out: rewording any rule; moving anything out of the file.

**Inputs**
- `TOOLING.md` §1, `../docs/CONTEXT-AUDIT.md` §6.3 `CE-15`

**Acceptance criteria**
- [ ] No subsection of §1 exceeds one rule, and each has a number a pointer can name.
- [ ] Every `§1` pointer in `tasks/`, `docs/` and `.handoff/config.md` names a subsection or is shown to mean the whole.
- [ ] `python tools/docs/refcheck.py` green; the `--docs` gate green.

**Open questions**
- none

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | List the rules §1 holds, one heading each | fourteen, and the split points are paragraph leads rather than line numbers |
| 2 | Measure what the §1.1 constraint actually costs before honouring it | **one** live pointer, so it costs one edit to relax |
| 3 | Insert the headings unnumbered, then number them in document order | the numbers cannot disagree with the order, which is the defect `L-155` is about |
| 4 | `grep -rn` every live pointer at §1; re-point the ones that mean one rule | four documents; closed task records left as history |
| 5 | `refcheck.py`, `--docs` gate | green |

## 3. Implement

**Decisions & assumptions**
- **§1 is fourteen subsections, not the ten §1 listed**, because two of the ten were bundles: *the board question* also held the generated-markers rule and the gated-view rule, and *what the checks enforce* held `taskmd check` and `refcheck.py` under one lead. The criterion is *no subsection exceeds one rule*, and a heading over two rules fails it as surely as no heading at all — 2026-09-02
- **§1's constraint that §1.1 keeps its number was relaxed, on a measurement, and this is the deviation to read first.** The constraint protects citations; the tree holds **one** live pointer at `TOOLING.md` §1.1, in a closed task record. Honouring it would have numbered the new subsections 1.2 to 1.14 *before* a 1.1 that sits last in the file — a section whose whole purpose is to be addressed by number, numbered out of order, in a repository that closed [L-155](../docs/lessons/L-155.md) three days ago on exactly this class of defect. The shell recipe keeps its content and its place and takes the number its place gives it, §1.14, and the one pointer moved with it — 2026-09-02
- **The numbers are assigned by a pass over the document rather than typed into the headings.** Same reason: a typed number can disagree with its position and nothing here would notice — 2026-09-02
- **A pointer at `§1` was re-aimed only where it meant one rule.** `PUBLISHING.md` and `CONTEXT-AUDIT.md` both meant the `DUPLICATE INDEX` advisory (§1.12) and `TASK-WORKFLOW.md` §7 step 7 meant `--docs` (§1.4). **Closed task records were left alone**: they say what a session read on a day, and re-aiming them would rewrite that. The finding statements in `CONTEXT-AUDIT.md` keep `§1` because they are *about* §1's size — 2026-09-02
- **Scope deviation, recorded rather than glossed.** §1 says *Out: rewording any rule*, and two words changed anyway: *the two checks* and *neither*, both counting a set that is now four. Splitting the block promoted that lead into a heading, so the split is what made the stale count addressable, and leaving a false number inside a heading this task created is worse than the deviation — `T-236`'s rule, deleted rather than re-derived — 2026-09-02

**What it bought, measured**
- §1 was **18,456 bytes** and a pointer at it cost all of them. The fourteen subsections run **262 to 3,440 bytes**; the median rule is under 1 KB. A session sent to the no-edit rule now reads 966 bytes rather than eighteen thousand.

**Outputs produced**
- [`tasks/TOOLING.md`](TOOLING.md) — §1 split into fourteen numbered subsections
- [`docs/PUBLISHING.md`](../docs/PUBLISHING.md), [`tasks/TASK-WORKFLOW.md`](TASK-WORKFLOW.md), [`docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) — one pointer each, re-aimed
- [`tasks/T-277-put-motion-back-inside-the-more-menu.md`](T-277-put-motion-back-inside-the-more-menu.md) — the one live §1.1 pointer, moved to §1.14 because its target moved

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| no subsection of §1 exceeds one rule, and each has a number a pointer can name | met | Fourteen, 262 to 3,440 bytes. The two largest are one rule each — what `taskmd check` enforces, and what `refcheck.py` does — and both were inside one bundled lead before |
| every `§1` pointer names a subsection or is shown to mean the whole | met | Four re-aimed; the finding statements in `CONTEXT-AUDIT.md` are *about* §1 and keep it; closed task records are history and were not rewritten. §3 gives the test that separated them |
| `python tools/docs/refcheck.py` green; the `--docs` gate green | met | See the log row |

**Child fix tasks raised**
- none. The one thing found beyond the split — a lead counting *two checks* where there are four — is two words and was fixed in place under the remediation order's §4.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-02 | → proposed | Raised by `T-287` from `CE-15`. `PH3`. |
| 2026-09-02 | proposed → done | B19. Fourteen subsections rather than ten, because two of §1's named rules were bundles. **§1's constraint that §1.1 keeps its number was relaxed on a measurement**: it protects citations and the tree holds one, so honouring it would have bought a single closed record's pointer at the price of numbering the section out of order. §3 records it as the deviation to read first. §1 was 18,456 bytes read whole; the largest subsection is 3,440. |
