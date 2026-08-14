---
id: T-147
title: One workflow file per lifecycle phase
type: deliverable
status: done
phase: review
parent: T-130
blocked_by: []
related: [T-130, T-145, T-146, T-141]
work_package: PH3
finding: CE-09
shipped_in: unreleased
owner: the project owner
business_value: medium
effort: m
created: 2026-08-14
updated: 2026-08-14
deliverables:
  - tasks/TOOLING.md
  - tasks/TASK-WORKFLOW.md
---

# T-147 — One workflow file per lifecycle phase

## 1. Specify

**Outcome**
A session at one phase of the lifecycle reads that phase's rules, not the history of which checker
resolved what. **The finding is `CE-09`**, stated in
[`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.1; it is not restated here.

**Re-measured 2026-08-14: 23,210 bytes, and §6 *The tooling* is 12,836 of them — 55.3%**, counting
its two subsections. The audit read 22,190 and 11,842 — 53% — the day before. **The section grew
again while this batch was running**: [T-145](T-145-move-brief-mds-release-phases-to-its-own-document.md)
repointed the duplicate-index excusal and added 727 bytes to §6, which is the third time in two days
that this finding has described itself.

**Every other section is small, and that is the measurement that settles the shape.** §1 1,097, §2
1,291, §3 2,229 + §3.1 1,309, §4 817 + §4.1 1,312, §5 388, §7 1,003 — **10,374 bytes for the entire
document once §6 is out of it**, which is less than §6 alone.

**Section numbers must survive, and the count is larger than the document says.** It claims a dozen
records cite §2 through §6.2. Measured across every tracked document: **104 citations in 42 files**,
covering all ten headings — §1×2, §2×7, §3×12, §3.1×4, §4×6, §4.1×5, §5×3, **§6×49**, §6.1×14,
§6.2×2. `refcheck.py` resolves every one, so a renumbering falsifies a hundred pointers and the
checker says so.

**Scope**
- In: the split, the numbering that survives it, and the entry point that says which file to open.
- Out: rewriting a rule while moving it.
- Out: deleting the tooling history. It is the record of why each check exists; it moves.

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.2 — read before starting; §6.1 — `CE-09`
- `R8` §9, P2 — the four-part shape this finding proposes: preflight, do, do-not, close
- [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §6.1 — the section-reference rule this task is bound by

**What specifying must settle**
- ~~**The shared policy question**, with [T-145](T-145-move-brief-mds-release-phases-to-its-own-document.md)
  and [T-146](T-146-one-file-per-lesson-with-a-generated-index.md): does this project split large
  documents by unit? **The first of the three specified settles it**; the other two adopt or argue.~~
  **Settled 2026-08-14 by T-145 as `L-89`.** Both limbs bear on this task and they point different
  ways, which is the second bullet below: `§n` is an address and a planner wants one phase at a time,
  which argues the by-unit limb; but the weight is in one section, which argues the by-kind limb and
  a single extraction. **`L-89`'s rule 2 decides it — move the part that grows.** Adopt that or argue
  against it; do not re-decide the policy.
- **Whether the four-part shape fits, or whether extracting the one section is the whole change.**
  **It is the whole change, and the four-part shape is refused.** `R8` §9's P2 — preflight, do,
  do-not, close — describes a document whose weight is spread across its phases. This one's is not:
  §6 is 55.3% and everything else together is 10,374 bytes. Splitting that remainder four ways gives
  a session at `plan` three or four files to open instead of one document smaller than the section
  being removed. **`L-89` rule 2 is the deciding rule — move the part that grows** — and what grows
  here is named in the finding itself: every tooling change lands in §6, three times in two days.
- **How `§n` citations survive — the constraint that decides the rest.** §6, §6.1 and §6.2 are cited
  **65 times between them**. They keep their numbers and their titles and become pointer sections,
  which is [T-141](T-141-extract-the-upstream-register-into-one-document-per-owner.md)'s worked
  precedent in this repository and **L-39**'s rule: a heading removed is a citation falsified, with
  nothing to say so. A pointer subsection is not a second copy.

**The shape, settled**

- **`TOOLING.md`, under `tasks/`, beside its host** — the same choice T-145 made and for the same
  reason: the moved text carries relative links, and a document at the same depth keeps every one of
  them correct untouched. T-146 paid for the alternative.
- **All of §6 moves, including §6.1 and §6.2.** §6.1 is the section-reference rule and reads as a
  writing rule rather than a tooling one, which is an argument for leaving it — **refused**, because
  it is written as the rule `refcheck.py` implements, opens on the checker that had not existed, and
  is unreadable apart from it. Splitting a rule from the thing that enforces it to satisfy a
  filing category is the trade **L-39** warns about, one level up.
- **The new document renumbers from §1**, and the old numbers stay where they are cited. Its own
  headings are new addresses that nothing cites yet.
- **The commands move with it, and that is a real cost, stated rather than hidden.** A session at
  `implement` runs `python tools/tasks/lint.py` and will now open one more file to find it. The
  alternative — leaving a copy behind — is **L-13**, and the copy is what goes stale.

**Acceptance criteria**
- [ ] §6, §6.1 and §6.2 exist in `TASK-WORKFLOW.md` as pointer sections, keeping their numbers and
      titles, and all **104** section citations still resolve
- [ ] The moved text is byte-identical to what was removed, asserted rather than reviewed, with no
      rule rewritten and none deleted
- [ ] `TASK-WORKFLOW.md` is under 13,000 bytes, stated as measured
- [ ] The new document is reachable: `TASK-WORKFLOW.md` §6 names it, and so does the one other
      document that sends a reader to the tooling
- [ ] `python tools/check_all.py` green; `python tools/tasks/lint.py` ends with its one known advisory

**Open questions**
- ~~**Is it worth doing at all?**~~ **Yes, and the cheaper alternative named in this bullet is the
  one being taken** — *move §6 out and leave the rest* was written here as the lesser option and the
  measurement makes it the whole task. Nothing is left for the four-part shape to do.

## 2. Plan

**Sliced, with the bytes asserted equal** — T-145's method and T-146's, for the third time. The
difference from T-146 is that the new document sits beside its host, so there is no depth rewrite and
no chance of the defect that cost T-146 a redo.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Sweep every citation of §6, §6.1 and §6.2, and every document that sends a reader to the tooling | The list step 4 repoints, and the proof the headings stay |
| 2 | Slice §6 through the end of §6.2 into the new document, renumbered from §1, with its own *what this is* | `TOOLING.md`, under `tasks/` |
| 3 | Reduce §6, §6.1 and §6.2 to pointer sections keeping their numbers and titles | `TASK-WORKFLOW.md` at workflow size |
| 4 | Repoint what named §6 for its content rather than its address | The sweep's list |
| 5 | Run the gates; re-measure both documents and re-count the citations | The review table's figures, taken after |

**What step 1 must catch that a link check will not.** A citation resolves to a *heading*, so every
one of the 104 keeps resolving whether or not the content behind it moved. **The check cannot tell a
pointer from the rule it points at** — so a reference that meant *read the rule here* has to be found
by reading, not by running anything. That is the failure mode this step exists for, and `§6×49` is
the reason it is worth the pass.

## 3. Implement

**Decisions & assumptions**
- **The finding's shape was refused on a measurement, and this is the third time in three tasks —
  2026-08-14.** `CE-09` proposed four files, one per lifecycle phase. Everything in this document
  except §6 is **10,374 bytes together**, less than the section being removed, so four files would
  give a session at `plan` several to open instead of one that is already small. The pattern across
  the batch is now worth naming: **a finding says where the weight is; it does not know what removing
  it is worth**, and all three of `CE-05`, `CE-06` and `CE-09` named a shape the measurement changed.
- **All three headings stay in place as pointer sections — 2026-08-14.** §6, §6.1 and §6.2 are cited
  65 times; T-141's precedent and **L-39**. The alternative — delete them and repoint the citations —
  means editing closed task records, which are dated statements of what was true when written.
- **§6.1 moved with the rest, against the argument for keeping it — 2026-08-14.** It is the
  section-reference rule and reads as a writing rule, so filing it under *tooling* is arguable. It
  moved because it is written as the rule `refcheck.py` implements and opens on the checker that did
  not exist before it; separating a rule from the thing that enforces it, to satisfy a category, is
  the trade **L-39** warns about one level up. `TASK-WORKFLOW.md` §6.1 still carries the reader there.
- **The new document sits beside its host — 2026-08-14.** No relative reference inside the moved text
  changes, which is exactly the trap that cost T-146 a redo. Only the three heading lines were
  rewritten, and the body between them is asserted identical to what was removed.
- **Three internal cross-references were repaired, and no gate would have caught them —
  2026-08-14.** The moved text said *(§6.1)*, *(§3)* and *"the headings in this document"*, all
  meaning `TASK-WORKFLOW.md` and all now sitting in a different file. A bare `§n` is not bound to a
  document, so `refcheck.py` counts it as unbound and skips it — correctly, by its own adjacency
  rule. **The class this belongs to is the one T-146 found in link labels**: text a reader follows
  and no checker reads. It is worth looking for after every extraction.
- **The commands went with the section, and the pointer names the one that matters — 2026-08-14.**
  A session at `implement` runs `python tools/tasks/lint.py`, so §6 states that one line and sends the
  reader on for the rest. That is a pointer doing its job rather than a second copy of the rules
  (**L-13**).
- **Six live references were repointed; the rest were left — 2026-08-14.** Of 75 lines naming this
  document with a section-6 mark, most sit in **closed task records** and say what was written where
  at the time. Those are correct dated statements and editing them would rewrite history to match the
  present, which is the same reasoning `TOOLING.md` §1 already applies to `task.py`.

**Outputs produced**
- [`TOOLING.md`](TOOLING.md) — the tooling, the two checks and the two rules they implement
- [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) — **23,210 → 11,407 bytes**, with §6, §6.1 and §6.2 as pointers
- Repointed: [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) (two),
  [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) (§2.2 twice, §6's rank row, §9),
  [`../docs/lessons/L-70.md`](../docs/lessons/L-70.md)

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| §6, §6.1 and §6.2 remain as pointer sections keeping their numbers and titles, and all citations resolve | **met** | `728 section reference(s) resolved, 0 dead`. Re-counted after: **103 citations in 41 files**, all ten headings still cited. It was 104 in 42; the one that moved is `L-70`'s, repointed because it cited §6.1 *for the rule* rather than for the address — which is the distinction step 1 existed to draw |
| The moved text is byte-identical to what was removed, no rule rewritten or deleted | **met** | Asserted: undo the three heading lines and the 12,829 bytes come back exactly. Three internal cross-references were repaired **after** that assertion, and they are listed in §3 rather than folded into the move |
| `TASK-WORKFLOW.md` under 13,000 bytes, stated as measured | **met** | **11,407**, from 23,210. `TOOLING.md` is 13,885 — larger than the section, by its own preamble |
| The new document is reachable from §6 and from the other document that sends a reader to the tooling | **met** | `TASK-WORKFLOW.md` §6, §6.1 and §6.2 each name it; `PUBLISHING.md` in two places; `CONTEXT-AUDIT.md` §9; `L-70` |
| `check_all.py` green; `lint.py` ends with its one known advisory | **met** | `lint.py`: three passed, `2174 document pointer(s), 0 broken`, one advisory naming `RELEASE-PHASES.md`. `check_all.py`: `0 failure(s), 0 unclassified, 0 stale` over 38 tracked tools, green on the first run |

**What the review does not claim.** No bytes were saved — 12,829 moved out of a document every task
reads and into one it opens when it needs the checkers. **And the four-part shape was never tried**,
so nothing here is evidence against it; it was refused on the measurement in §1, which is a different
thing from having been measured and lost.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-14 | → done | **23,210 → 11,407 bytes, and the finding's shape was refused for the third time in three tasks.** `CE-09` asked for four files, one per lifecycle phase; everything except §6 is 10,374 bytes together, so four files would cost a planner more openings than the whole document costs today. **The batch's real result is that pattern**: `CE-05`, `CE-06` and `CE-09` each named a shape, and the measurement changed all three. A finding says where the weight is and cannot say what removing it is worth. |
| 2026-08-14 | → in_progress | Sliced beside the host, so no relative reference moved and T-146's depth trap could not recur. **The defects that remained were the ones no gate reads**: three internal cross-references inside the moved text — `(§6.1)`, `(§3)` and *"the headings in this document"* — each still pointing at the file they had left. A bare `§n` is unbound, so `refcheck.py` skips it correctly and sees nothing. Same class as T-146's link labels. |
| 2026-08-14 | → planned | Five steps, sweep first. The sweep's purpose was not the links — a citation resolves to a heading whether or not the content behind it moved — but to separate the references that meant *the rule* from the ones that meant *the address*. Six of 75 were the former. |
| 2026-08-14 | → specified | Re-measured 23,210 with §6 at 55.3%, against the audit's 22,190 and 53% one day earlier; the section had grown again, 727 bytes of it from [T-145](T-145-move-brief-mds-release-phases-to-its-own-document.md) two tasks ago. **The citation count was larger than the document's own claim**: it said a dozen records cite §2 through §6.2, and the measurement found 104 in 42 files. `L-89` rule 2 settled the shape. |
| 2026-08-14 | (no change) | The shared policy question was struck out rather than answered here: T-145 settled it as **L-89** and both its limbs bear on this task, which is why rule 2 — *move the part that grows* — had to be the tie-break rather than rule 1. |
| 2026-08-14 | → proposed | Raised at the owner's direction with the rest of the unraised findings. It was **never a candidate** — it ranked ninth in T-130's §6 and was not put up — so this is the cut-off moving, not a proposal accepted. **Scheduled to `plan` and no further.** |
