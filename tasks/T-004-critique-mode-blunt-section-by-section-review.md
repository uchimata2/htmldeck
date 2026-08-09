---
id: T-004
title: Critique mode — blunt section-by-section review
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: [T-014, T-020]
related: [T-002, T-005]
work_package: WP3
owner: maintainer
created: 2026-08-04
updated: 2026-08-07
deliverables: []
---

# T-004 — Critique mode — blunt section-by-section review

## 1. Specify

**Outcome**
A mode that reviews a deck slide by slide, bottom line up front, with no diplomatic padding.

**Why this one**
The most useful artifact in the corpus is a critique, not a deck. It caught a structural gap in the argument, a two-column format that only landed on one side, a "Venn diagram" whose sets did not overlap, a metaphor used four times, a typo on the most important slide, and generator branding left in a corner. This is the part users cannot do for their own work.

**Acceptance criteria**
- [ ] Opens with a verdict, then grades each slide
- [ ] Names specific defects with the slide they are on — no general advice
- [ ] Run against a deck with known defects and found them
- [ ] Voice stays direct; no compliment sandwich
- [ ] **When sources are supplied, reconciles the deck against them** — and reconciles the sources
      against each other, because a deck inherits their disagreements
- [ ] Run against a deck built from sources that contradict each other, and found the contradiction
- [ ] States plainly when it reviewed the deck alone, so a clean report is not read as "the content
      is right"

**The second class of finding**

The corpus critique's findings are all inside one deck. `docs/BRIEF.md` § *The critique pass* records
a second class, from a five-document set audited before its deck was built: figures correct where
written and wrong where quoted, a summary contradicting the table above it, a count drifted from the
model it described. Each document had passed its own review. **All of them were found by counting,
not reading** — so this mode needs a counting pass, not only a reading pass.

The cheap technique that worked: one table of every figure in the material, its origin, and every
place it is reused.

**Open questions**
- ~~Should critique be able to apply its own fixes, or only report?~~ **Answered 2026-08-07 by the
  owner: report only, when the user invokes it as a mode.** Inside the convergence loop the fixes
  are the build step's, as [`EVALUATION.md`](../docs/EVALUATION.md) §6.2 already has them, with the
  fix ledger keeping them attributable. The reason to hold the line at the user-invoked mode is
  evidence, not purity: a reviewer that edits its own subject cannot be re-run to prove the fix
  landed, and two reports of the same deck stop being comparable.
- ~~Does the counting pass belong here or in the build check (T-005)? They overlap. Likely: T-005
  gates automatically, critique explains and prioritises.~~ **Answered 2026-08-07 by the owner:
  the hypothesis was right — [T-005](T-005-build-check-the-gate-the-deck-must-pass.md) counts, this
  mode explains and prioritises.** Counting is deterministic and has to *gate*, which is what T-005
  is; its three figure criteria already own it. What a count cannot produce is which wrong number
  matters, and that is this mode's half.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |

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
| 2026-08-09 | (no change) | **[T-005](T-005-build-check-the-gate-the-deck-must-pass.md) closed, and the report this mode consumes now exists.** `python tools/deck/check.py <deck> --json` emits the rows, the **coverage account** (owned, checked, failing, excused with a reason each, silent), the **figure ledger** this mode prioritises, which halves ran, and the five dimensions the gate is blind to. **Two things that bear on this mode's own scope.** The gate decides 77 of 111 owned rules and names the other 34 - so a critique that repeats a mechanical finding is repeating one the build already had, and the useful half is the 43 `judge` rules plus S1, S2, S4, D1 and D4. And **two rules are open questions for the owner** - DS-045's two readings, DS-219's *never* against its own reason - which a critique should not decide either. |
| 2026-08-07 | (no change) | **Both open questions answered by the owner; §1 now has none.** *Report, do not fix* — the user-invoked mode reports and nothing else, while the loop's fixes stay with the build step under [`EVALUATION.md`](../docs/EVALUATION.md) §6.2. *Counting belongs to [T-005](T-005-build-check-the-gate-the-deck-must-pass.md)* — this mode consumes the count and says which wrong figure matters. **The second answer removes work from here and adds a dependency**: the counting pass in §1 above is no longer this mode's to build, so what it needs from T-005 is the figure ledger in a form it can cite — which is one more reason this mode follows the check rather than preceding it. **The `related` edge this implies is now written on both files** — it existed in [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md)'s reasoning for the build order and in neither task's front-matter, and `related` is asymmetric, so it has to be stated twice or the task that needs the context cannot see it. |
| 2026-08-07 | (no change) | **[T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md) ruled: this mode takes two input types, and it is not split into two modes.** The **specification review** runs before any HTML exists and the **design audit** after the build; both are critiques over different inputs, and two modes would duplicate the reporting machinery for that one difference. **The scope growth is real and it is the cheap half.** T-020 §3.3 maps six of the ten dimensions onto a slide-by-slide spec — S1, S2, D1, D2, D3 and D4's source-reconciliation half — **three of them among the five no mechanical check can reach.** The two report formats are R1 §14's, not inventions: spec review as `ID · Severity · Slide · Finding · Fix` with Major/Minor/Note, then *"Open — needs a decision"*, then counts; design audit as headline verdict, coverage table, findings with the principle violated, then an explicit keep-vs-rebuild split. |
| 2026-08-07 | (no change) | **Blocked on [T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md), added by [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md).** T-020 decides whether the **specification review** — the second critique format R1 §14 proves, run before any HTML exists — belongs to this mode or becomes one of its own. That is a doubling of scope, not a detail: §1 above reviews a built deck only, and every acceptance criterion is written against a rendered artifact. A mode specified for one format and then handed two is respecified. |
| 2026-08-04 | → proposed | Seeded from `docs/BRIEF.md` when the project folder was prepared. |
| 2026-08-05 | (no change) | Added the cross-document class of finding and the counting pass, after a source-document audit found nine defects that five per-document reviews had all passed. Evidence in `docs/BRIEF.md`. |
| 2026-08-06 | (no change) | Owner answered BRIEF open question 6 — sources are supplied, so the cross-document reconciliation added above is now a **standing** part of this mode rather than a conditional one. Two further inputs landed: R3 §6's 12 anti-patterns are directly usable as named defect classes, and R2 §11 gives this mode a testable disclosure check — close every panel and read the deck; if a slide stops making its argument, the tier split is wrong. R4 §2 found the critique format has **zero prior art**, so R1 §14's severity scheme is the only source for it. |
| 2026-08-06 | (no change) | **T-014 closed.** [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) **§6 owns the twelve anti-patterns and the named defect classes; this mode consumes them and must not restate them** — a check and the standard it tests cannot be two documents. Kept there deliberately, and T-014 recorded it as the assumption to revisit if this task disagrees when planned. M3–M6, M8, M9 and M11 were **deferred to here** as the report's format. The severity scheme (M2) stays in the design system as shared vocabulary. §11 conditions 15 and 23 are explicitly **not machine-checkable** and belong to this mode. *(Corrected 2026-08-09 by [T-037](T-037-record-in-the-ruleset-which-rules-no-check-can-reach.md): **`DESIGN-SYSTEM.md` §11 never existed** — the document has ended at §9 in every commit, and which rules "15 and 23" meant is unrecoverable. The sentence is left standing because it is what was believed at the time; what this mode actually inherits is every rule whose new **`Reach`** column reads `—`, which is machine-readable and cannot go stale the same way.)* |
| 2026-08-06 | (no change) | **This mode is now the reporting face of a defined evaluator, not a free-standing review.** [`docs/EVALUATION.md`](../docs/EVALUATION.md) supplies the dimensions, anchors, threshold and the four stop outcomes; the design system supplies `DS-nnn` IDs so a finding can cite a rule and a fix can be verified against it. **Three consequences:** findings carry a rule ID and a dimension score, not just prose; the report must state **which passes ran** (auto / render / per-slide / whole-deck), since the whole-deck pass is where cross-slide defects live; and the four outcomes are **not interchangeable** — PASS, CAP, STALL and OSCILLATION need different reports, and OSCILLATION is a finding about the *ruleset* that belongs in `DESIGN-RATIONALE.md` §2. |
