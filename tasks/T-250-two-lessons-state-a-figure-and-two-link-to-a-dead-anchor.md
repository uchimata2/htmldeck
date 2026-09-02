---
id: T-250
title: Fix four lessons in the folder whose own rule is that a lesson outlives its instance
type: fix
status: done
phase: review
parent: T-219
blocked_by: []
related: []
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-29
updated: 2026-09-02
shipped_in: 0.7.0
deliverables: []
---

# T-250 — Fix four lessons in the folder whose own rule is that a lesson outlives its instance

## 1. Specify

**Outcome**
The lessons folder holds no statement its own tree contradicts. Today `L-39` and `L-43` state a figure about the tree in the present tense and both have drifted, in the folder whose rule is that a lesson outlives its instance; and `L-38` and `L-42` link to an in-page anchor the one-file-per-lesson split removed, which **every gate reports as resolving**.

**Closes** `PR-103`, `PR-104` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: `docs/lessons/L-38.md`, `L-39.md`, `L-42.md` and `L-43.md`, and whichever gate should take the dead-anchor class
- In: **nothing else** - every finding this task closes is named above, and each statement stays in the register rather than being restated here (the method's umbrella condition 2)
- Out: any finding not in the list above
- Out: committing to a remedy before measuring it. A remedy is a hypothesis (the method's section 5); a fix that the measurement refuses is reported here and its finding stays open

**Inputs**
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3 - the rows for `PR-103`, `PR-104`
- `PR-104`'s evidence, which is that the anchors resolve to the file and not to the section

**Acceptance criteria**
- [ ] every finding above is **closed with its remedy measured**, or explicitly deferred with the reason recorded on its register row - the method's obligation for `Med`
- [ ] each register row's `Task` cell names this task and its `Status` cell says what happened
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None yet. The register's `Remedy` column carries a hypothesis for each finding, and the method's
  section 5 says it is a hypothesis: whoever implements this measures before committing to it, and
  records what the measurement said.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Re-derive both figures and list every in-page anchor in the tree before editing | `65` commits, not the register's `54`; `130` hard rules; three `](#` links, two of them dead |
| 2 | `PR-103` — delete the two figures rather than refresh them, and date the one that carries a case | `docs/lessons/L-39.md`, `docs/lessons/L-43.md` |
| 3 | `PR-104` — point both anchors at `L-36.md` | `docs/lessons/L-38.md`, `docs/lessons/L-42.md` |
| 4 | Decide the gate question on the measured class, then build it if it earns its place | `tools/docs/refcheck.py` check 5, `DEAD ANCHOR` |
| 5 | Seed the check both ways — the honest tree, and a slug rule that would clear the defect | Self-test asserts both |
| 6 | Close the two register rows, then `lint.py` and `check_all.py --docs`, run separately | Both green |

## 3. Implement

**Decisions & assumptions**
- **Both figures are deleted rather than corrected**, which is the remedy's harder half. The register offered `54` for `L-39` on 2026-08-29 and `git rev-list --count` returns **65** today: the replacement had itself decayed inside the four days between raising the finding and fixing it, which settles the argument better than the lesson beside it does — 2026-09-02
- **One figure is kept and its tense dated instead.** `L-43`'s *`EVALUATION.md` §1 declares **114 `hard`** rules* is the case's own evidence — 25 of them `judge`, 11 named nowhere — so deleting it would cost the lesson its subject. `declares` became `declared`. What that document says *today* is `PR-32`'s, not this task's — 2026-09-02
- **The gate question is answered yes and the check is built.** `refcheck.py` check 5, `DEAD ANCHOR`. **L-75** cautions against a check built on a thin population and the population is three links tree-wide; what carries it is that **two of the three were dead**, that the class was created wholesale by one refactor ([T-146](T-146-one-file-per-lesson-with-a-generated-index.md)), and that `LINK`'s pattern requires a path before the fragment — so these matched **nothing** and were never resolved, rather than being resolved wrongly — 2026-09-02
- **No new lesson.** The mechanism — a checker's pattern bounding its own population, invisibly from inside — is [L-57](../docs/lessons/L-57.md), and L-75, L-114 and L-05 sit beside it. A fifth statement of one idea is what `docs/lessons/`'s own rule is against, so the code comment cites L-57 instead — 2026-09-02

**Outputs produced**
- [`../docs/lessons/L-39.md`](../docs/lessons/L-39.md), [`../docs/lessons/L-43.md`](../docs/lessons/L-43.md) — the two figures
- [`../docs/lessons/L-38.md`](../docs/lessons/L-38.md), [`../docs/lessons/L-42.md`](../docs/lessons/L-42.md) — the two anchors
- [`../tools/docs/refcheck.py`](../tools/docs/refcheck.py) — check 5 `DEAD ANCHOR`, `INPAGE_LINK`, `anchor_slug`, `anchors_in`, and the self-test that seeds both directions
- [`../docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) — the `PR-103` and `PR-104` status cells

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| every finding closed with its remedy **measured**, or deferred with the reason on its row | pass | Both closed. `PR-103`'s figures were re-derived first, and the re-derivation is what chose the harder remedy: the register's own replacement was already stale. `PR-104`'s open half — whether a gate takes the class — was decided by counting the class, not by preference |
| each register row's `Task` cell names this task and its `Status` cell says what happened | pass | Both. The `Task` cells already named it |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | pass | `lint.py` green; `check_all.py --docs` green — the diff reaches `tools/docs/` and four documents, none of the paths `--docs` refuses. **The batch's landing owes the full run** |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-02 | proposed → done | B20. **The measurement chose the remedy in both rows.** `PR-103` offered a refresh or a deletion; re-deriving `L-39`'s figure returned **65** against the register's own **54**, written four days earlier, so the number had decayed between the finding and the fix and the deletion argued itself. `PR-104`'s open question — whether `refcheck.py` should resolve an in-page anchor — is answered **yes** on the population rather than against it: three links tree-wide, **two dead**, a class created wholesale by one refactor, and a `LINK` pattern that could not match them at all. Check 5 is seeded both ways, including against the slug rule that would clear the defect and report the live anchor. No new lesson: this is **L-57** inside the instrument that hunts the class. |
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`Med`**, grouped: the owner ruled on 2026-08-29 that a severity obliges a disposition before the release rather than a file count, on the precedent that the method already accepts many findings to one task at `Low`. Every finding keeps its id and its statement in the register. |
