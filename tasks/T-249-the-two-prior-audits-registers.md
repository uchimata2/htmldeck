---
id: T-249
title: Correct three claims the ruleset and context audits make about their own coverage
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

# T-249 — Correct three claims the ruleset and context audits make about their own coverage

## 1. Specify

**Outcome**
The two earlier audit registers state their own coverage correctly. Today the ruleset audit is titled *Every rule, with its verdict* and holds 165 of the ruleset's 177; the context audit says the screening partition is checked by nobody and that no command exists for it; and the ruleset audit's ceiling on its own test 2 rests on a fixture that has not had that shape since [T-224](T-224-give-the-blindness-fixture-its-own-instrument-in-cycle-17.md).

**Closes** `PR-90`, `PR-91`, `PR-92` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: `RULESET-AUDIT.md` sections 1, 3 and 5, and `CONTEXT-AUDIT.md` section 4.1's final paragraph
- In: **nothing else** - every finding this task closes is named above, and each statement stays in the register rather than being restated here (the method's umbrella condition 2)
- Out: any finding not in the list above
- Out: committing to a remedy before measuring it. A remedy is a hypothesis (the method's section 5); a fix that the measurement refuses is reported here and its finding stays open

**Inputs**
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3 - the rows for `PR-90`, `PR-91`, `PR-92`
- `ruleset.py`, which derives the ruleset's true total

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
| 1 | Measure all three rows before touching anything — `ruleset.py`, `screening.py`, `seed_defects.py --check`, and section 5's ID column parsed against `DESIGN-SYSTEM.md`'s | All three claims confirmed; `PR-90`'s gap derived as `DS-233` to `DS-244` and **dated** |
| 2 | `PR-90` — state the denominator as a date and make the exclusion derivable, in the title, the snapshot caveat, section 1's headline and section 5's heading | `docs/RULESET-AUDIT.md` |
| 3 | `PR-92` — restate test 2's ceiling in the fixture's current terms, naming the instrument rather than five outputs | `docs/RULESET-AUDIT.md` section 3 |
| 4 | `PR-91` — write the closure note in section 10.4's form, then sweep both registers for the class the row feared | `docs/CONTEXT-AUDIT.md` section 4.1 |
| 5 | Close the three register rows with what happened, and with what was refused | `docs/PRE-RELEASE-AUDIT.md` section 3 |
| 6 | `lint.py`, then `check_all.py --docs`, run separately | Both green |

## 3. Implement

**Decisions & assumptions**
- **The audit's membership is dated, not short** — `git log -1 -S` puts all twelve of `DS-233` to `DS-244` at 2026-08-18 or later, against a 2026-08-17 run, so `PR-90` is a missing denominator and not twelve missing rows. The title, section 1 and section 5's heading say *examined* against a date instead of *every* — 2026-09-02
- **The excluded list is refused as a list** — the remedy hypothesis offered one, and a typed list of *rules added since* goes stale on the next rule, which is the class this finding is an instance of. The snapshot caveat names `python tools/deck/ruleset.py` and section 5's ID column as what answers it — 2026-09-02
- **`PR-92`'s denominator is pointed at rather than corrected** — writing 122 where the sentence implied 115 rebuilds the same defect one number later, and the paragraph now names `ruleset.py` — 2026-09-02
- **`PR-94`'s 29-against-30 is left untouched** although it sits in the paragraph rewritten here. It is `T-253`'s finding, and closing it would take a disposition this task's scope excludes — 2026-09-02
- **`PR-91`'s wider hypothesis is refused on the sweep** — it guessed *a stated gap whose remedy shipped* might be a wide class; reading both registers returned section 4.1 alone, because sections 10.3 and 10.4 already carry their notes — 2026-09-02

**Outputs produced**
- [`../docs/RULESET-AUDIT.md`](../docs/RULESET-AUDIT.md) — the title, the snapshot caveat, section 1's headline figure, section 3's test-2 ceiling, section 5's heading
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) — section 4.1's closure note
- [`../docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) — the `PR-90`, `PR-91`, `PR-92` status cells

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| every finding closed with its remedy **measured**, or deferred with the reason on its row | pass | Three closed. Each was measured before any edit, and **two remedy halves were refused on the measurement** — `PR-90`'s excluded list and `PR-92`'s corrected denominator — with the refusal recorded on the row rather than in this file |
| each register row's `Task` cell names this task and its `Status` cell says what happened | pass | All three. The `Task` cells already named it; the `Status` cells moved from `open` to a dated closure |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | pass | `lint.py` green; `check_all.py --docs` green, which is the gate this diff can reach — three documents and nothing under `tools/deck/`, `shell/`, `themes/` or `examples/`. **The batch's landing owes the full run**, per `TASK-WORKFLOW.md` section 7 step 7 |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-02 | proposed → done | B20. **All three claims held, and two of the three remedies did not.** `PR-90`'s twelve missing rows turn out to be rules added *after* the run — every one dated 2026-08-18 or later — so the audit examined its whole subject and the defect is an undated denominator; the excluded list its remedy offered is refused, because a typed list of *added since* is the same failure one turn later. `PR-92`'s corrected denominator is refused for the same reason and replaced by a pointer to `ruleset.py`, and the ceiling now names `seed_defects.py --check` rather than five rule ids the fixture has not seeded since `T-224`. `PR-91`'s closure note is written in section 10.4's form and **its wider hypothesis was measured and refused**: the sweep of both registers returned one live member, the one the row already named. |
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`Med`**, grouped: the owner ruled on 2026-08-29 that a severity obliges a disposition before the release rather than a file count, on the precedent that the method already accepts many findings to one task at `Low`. Every finding keeps its id and its statement in the register. |
