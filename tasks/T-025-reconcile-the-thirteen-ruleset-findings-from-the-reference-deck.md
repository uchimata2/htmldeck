---
id: T-025
title: Reconcile the thirteen ruleset findings the reference deck produced
type: fix
status: done
phase: review
parent: T-024
blocked_by: []
related: [T-005, T-014, T-021, T-022, T-023]
work_package: WP2
owner: maintainer
created: 2026-08-06
updated: 2026-08-06
deliverables:
  - docs/DESIGN-SYSTEM.md
  - docs/DESIGN-RATIONALE.md
  - docs/EVALUATION.md
---

# T-025 — Reconcile the thirteen ruleset findings the reference deck produced

## 1. Specify

**Outcome**
`docs/DESIGN-SYSTEM.md` and `docs/DESIGN-RATIONALE.md` corrected against the thirteen findings
[T-024](T-024-build-the-reference-deck-and-validate-the-ruleset.md) §3.3 recorded while building to
them, plus `docs/EVALUATION.md` corrected against F-13. Every finding either changes a rule, or is
recorded as considered and rejected with a reason.

**Why this is a separate task, and not part of T-024**
**A test that edits the thing it is testing is not a test.** T-024's job was to build strictly to
the ruleset and record where it broke; changing the rules mid-build would have hidden exactly the
evidence the task existed to produce. The findings are therefore recorded but unapplied, and this
task applies them.

**Scope**
- In: F-01 to F-13, each resolved and the resolution recorded under its rule ID.
- In: the four conflicts between two `hard` rules (F-01, F-03, F-04, F-05) — these are the ones
  where a deck cannot comply with both, so **one of each pair must yield explicitly**.
- In: `DESIGN-RATIONALE.md` §2, which is where the project says conflicts live.
- In: **DS-102 has no provision for an illustrative deck.** "Every figure sourced" cannot be met by a
  deck about a place that does not exist, and the plugin's own example deck is exactly that case.
  T-024 resolved it by making the model the source and saying so on the deck — recorded there as a
  decision rather than a finding, because it did not break the build. The rule should say so, since
  the alternative a builder reaches for is quoting real research from memory, which is a fabricated
  metric wearing a citation.
- In: EVALUATION §6.2/§6.4 (F-13), and EVALUATION §8's cap question, which F-13 answers with
  evidence rather than reasoning.
- Out: rebuilding the reference deck. Where a rule changes, the deck is re-checked against it, not
  rewritten to suit it.
- Out: `T-005`'s build check. This task decides what the rules say; T-005 decides how they are
  tested.

**Inputs**
- [`T-024`](T-024-build-the-reference-deck-and-validate-the-ruleset.md) §3.3 — the findings, each
  with the moment it was found
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) · [`docs/DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) · [`docs/EVALUATION.md`](../docs/EVALUATION.md)
- [`examples/README.md`](../examples/README.md) — the measurements the findings rest on

**Acceptance criteria**
- [ ] Each of F-01 to F-13 has a recorded resolution: rule changed, rule clarified, or rejected with a reason
- [ ] The four `hard`×`hard` conflicts each name which rule yields, in the rule text itself
- [ ] DS-063 carries a stated tolerance, and it is the measured one rather than a guess
- [ ] DS-013's token list covers the data-series and interactive-border roles the deck needed
- [ ] EVALUATION §8's cap question is closed against T-024's evidence
- [ ] `python tools/tasks/task.py check` passes

**Open questions**
- ~~**Does DS-036's mono range move, or does DS-035's floor stop being absolute?**~~ **Settled by the
  owner, 2026-08-06**, reviewing the reference deck: *"If it's min 18 now, I would accept a 16 too."*
  **The floor moved to 16**, which makes DS-036's range reachable and closes F-01. Applied by
  [T-027](T-027-specify-the-slide-deliverable-and-the-outline-contract.md); the reasoning and the
  caveat — 16 units is 11 px in a 720p screen share, so this widens what is permitted, not what is
  readable — are in `DESIGN-RATIONALE.md` §3. **F-01 needs no further work here.**
- ~~**Should the Motion control (F-03) become a rule of its own?**~~ **Settled by the owner,
  2026-08-06: yes.** Now **DS-218**. The alternatives — amending DS-140 inline, or leaving it to §7
  where 2.2.2 already sits — were rejected for the reason in `DESIGN-RATIONALE.md` §2.1: the
  reference deck only built a control because the build happened to notice, and a floor that reaches
  the builder as a criterion rather than an instruction produces non-conformant decks by default.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Sort F-01 to F-13 into: conflict, unimplementable, silence, and check-impossible | four groups, each with a resolution shape |
| 2 | Settle the two owner questions before touching the conflicts | two decisions |
| 3 | Apply rule changes to `DESIGN-SYSTEM.md`, keeping every ID stable | the corrected ruleset |
| 4 | Record every "why" under its ID in `DESIGN-RATIONALE.md` §2 | the rationale |
| 5 | Apply F-13 to `EVALUATION.md` and close §8's cap question | the corrected loop |
| 6 | Re-check the reference deck against every changed rule | a pass, or a new finding |

## 3. Implement

### 3.1 What changed, by finding

**Nine rules amended, four added.** Every resolution and its reasoning is in
[`DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) §2.1, keyed by finding; the table below is the
routing only, so the two do not drift.

| Finding | Class | Landed as |
| :--- | :--- | :--- |
| F-01 | conflict | DS-035 (already amended by [T-027](T-027-specify-the-slide-deliverable-and-the-outline-contract.md)) — **DS-035 yields**, the number not the principle |
| F-02 | unbuildable | DS-033 rewritten — the ban is on *bare* `px`; `--du` is declared once |
| F-03 | silence | **DS-218, new** — looping or >5 s motion ships a persistent keyboard control |
| F-04 | conflict | DS-141 rewritten — **DS-141 yields by scope**; DS-140's vocabulary is the specific override |
| F-05 | conflict | DS-146 rewritten — **DS-140 wins**, the draw-in is Rise on the marks |
| F-06 | silence | DS-168 amended — ≥ **48 × 48 design units** inside the stage |
| F-07 | unbuildable | DS-117 split — labels universal, arrowheads directional only |
| F-08 | check impossible | DS-063 amended — tolerance **0.25 du** non-text, **2 du** text runs |
| F-09 | silence | DS-013 extended — data-series and UI-line roles, separate from `--line` |
| F-10 | conflict | **DS-219, new** — text never goes on a data mark |
| F-11 | unbuildable | DS-138 extended — the panel's height decides the control's row |
| F-12 | measurement | **DS-220 and DS-221, new** — `scrollHeight` vs `clientHeight`; pin motion before capturing |
| F-13 | conflict | `EVALUATION.md` §6.2/§6.4 — **the cap counts measurement rounds, not fixes**; §8 closed |
| *(in scope, not a finding)* | — | DS-102 gains the illustrative-deck provision |

### 3.2 Decisions & assumptions

- **F-03 becomes its own rule, DS-218 — owner, 2026-08-06.** §1's open question, with the two
  rejected alternatives recorded there and the reasoning in `DESIGN-RATIONALE.md` §2.1.
- **Three of the four `hard`×`hard` conflicts were not real impossibilities — 2026-08-06.** F-04 and
  F-05 are a general rule and its own specific case with no precedence stated; F-01 was a number.
  Only F-10 is a genuine joint-unsatisfiability. **This is the task's own finding**, generalised as
  **L-28**, and it changed the work: the fix for two of the four is a scope clause, and no rule was
  softened to buy it.
- **Every ruling is written into the rule text, not only the rationale — 2026-08-06.** Nothing loads
  `DESIGN-RATIONALE.md` at build time, so a precedence recorded only there gets re-derived by guess
  on the next build. That is how T-024 came to implement DS-141 and DS-146 correctly *by inference*.
- **DS-063's tolerances differ per mechanism, and are the measurement rounded up — 2026-08-06.** Box
  geometry rounds once (measured 0.09 → 0.25); a text run accumulates glyph-advance rounding along
  its length (measured 1.17 → 2), so the text figure carries headroom for runs longer than this
  deck's. Assumed rather than measured: that no realistic run exceeds 2 du. A second deck tests it.
- **DS-168's 48-unit floor assumes viewport width binds the scale — 2026-08-06.** A short, wide
  viewport can scale below 0.5, and DS-071 is `default`, so a deck moving the reflow threshold moves
  this floor with it. Recorded in the rationale rather than complicating the rule.
- **The evaluation counts were re-derived, not adjusted — 2026-08-06.** They were already wrong by
  six before this task (written before T-027's additions). Corrected by measurement, and
  `EVALUATION.md` §1 now says they are derived and must be re-derived (**L-08**).

### 3.3 Outputs produced

- `docs/DESIGN-SYSTEM.md` — 9 rules amended, 4 added (DS-218 · DS-219 · DS-220 · DS-221), §0.8
  corrected against the DS-035 amendment, §9 updated
- `docs/DESIGN-RATIONALE.md` — §2.1, the thirteen findings and how each was closed
- `docs/EVALUATION.md` — §6.2 scoped, §6.4 and the §6 diagram corrected, §8's cap question closed,
  counts re-derived
- `docs/LESSONS.md` — **L-28**; L-22's stale "nothing under 18" corrected to 16
- `tools/deck/audit.py` — the motion-control check now cites `DS-218` rather than the bare criterion

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Each of F-01 to F-13 has a recorded resolution | **met** | `DESIGN-RATIONALE.md` §2.1 — thirteen rows, each naming the class and the reasoning. None was rejected; all thirteen changed a rule. |
| The four `hard`×`hard` conflicts each name which rule yields, **in the rule text** | **met, with the premise corrected** | F-01 (DS-035), F-04 (DS-141 yields by scope) and F-05 (DS-146 defers to DS-140) each carry the ruling in the rule. **F-03 is not a conflict** — it is a silence, and nothing yields; it is closed by adding DS-218. The criterion assumed four rules in tension where there were three. |
| DS-063 carries a stated tolerance, and it is the measured one | **met** | 0.25 du non-text, 2 du text runs, from 384 measured values worst-casing at 0.09 and 1.17. The derivation and the headroom argument are in the rule and the rationale. |
| DS-013's token list covers the data-series and interactive-border roles | **met** | Both added, and the rule now states *why* — a hairline token carries no 3:1 obligation and a chart mark does. |
| EVALUATION §8's cap question is closed against T-024's evidence | **met** | Closed at **2 measurement rounds measured, cap stays 3**. The entry states what the evidence does *not* settle: one deck, one author. |
| `python tools/tasks/task.py check` passes | **met** | 28 tasks, 0 broken pointers. |

### 4.1 Plan step 6 — the reference deck re-checked against every changed rule

**No rule change broke the deck, and none needed it rewritten.** Re-checked rather than rebuilt, per
§1's scope.

| Rule | How re-checked | Result |
| :--- | :--- | :--- |
| DS-013 | `--data-quiet` and `--ui-line` present as separate tokens | pass |
| DS-033 | `--du:1px` declared exactly once; gate confirms no `vw`/`vh`/`clamp()` | pass |
| DS-063 | T-024's 384-value diff, now against a stated tolerance | pass — 0.09 and 1.17 inside 0.25 / 2 |
| DS-102 | "ILLUSTRATIVE MODEL" per slide; "MODELLED, NOT OBSERVED" on the trajectory | pass |
| DS-117 | **Looked at slide 8.** Four route edges undirected, labelled, no arrowheads; the one timed-connection edge directional, arrowhead meeting its target | pass |
| DS-138 | Gate: panel drops below its control | pass |
| DS-140/141 | Exactly four keyframes; durations 340/380/420/300 ms, 1.2 s, 4.5 s — the vocabulary exactly | pass |
| DS-146 | Chart marks carry Rise; no stroke-dash draw | pass |
| DS-168 | `--disc-hit: calc(52*var(--du))` — 52 ≥ 48 | pass |
| DS-218 | `<button id="motion" aria-pressed>`, persistent in the chrome; gate confirms | pass |
| DS-219 | **Looked at slide 7.** Every label outside its mark — series labels beside the end points, "DOCKS FULL" on a leader | pass |

`python tools/deck/audit.py examples/reference-deck.html` → **0 mechanical failures**, 0 contrast
failures.

### 4.2 What the re-check could not see, and it is not nothing

**Two of the new rules have no mechanical check, and one of them needs none.**

- **DS-219 is already covered by DS-215.** DS-215 compares every text run's computed fill against its
  computed backdrop and reports zero failures; text on a mark dark enough for 1.4.11 would fail
  4.5:1 and be caught there. **DS-219 states the consequence so a builder stops before drawing it**,
  which is a different job from catching it afterwards.
- **DS-168's design-unit floor is not checked.** The gate measures targets in CSS pixels at viewport
  1600, where the stage scale is ~0.83 — so a control sized at 24 design units would pass there and
  fail at the 0.5 the rule is derived from. **The rule is now right and the check does not test it.**
  Handed to [T-005](T-005-build-check-the-gate-the-deck-must-pass.md), which owns check mechanics.
- **DS-220 and DS-221 are claims about the harness, not about a deck.** `tools/deck/render.py`
  already implements both; they are now stated as rules so the next harness cannot omit them.

**And the standing limitation is unchanged.** Thirteen findings came from **one deck, one topic, one
author**. Every amendment here is a correction from a single build, and L-24's own arithmetic —
roughly one finding per ten rules — says a second deck would find more. `DESIGN-SYSTEM.md` §9 says
so in the document itself.

**Child fix tasks raised**
- none. Two follow-ons were routed to existing tasks rather than raised as new ones: DS-168's
  unchecked design-unit floor to [T-005](T-005-build-check-the-gate-the-deck-must-pass.md), and the
  reference deck's three simultaneous position encodings (DS-216/DS-217, visible in every capture) to
  [T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md), which already owns it.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-06 | → done | Nine rules amended, four added, `EVALUATION.md`'s loop corrected and its cap question closed. The reference deck re-checked against all eleven changed rules it can exercise — **0 mechanical failures**, and slides 7 and 8 looked at for the two changes that are visual judgements (DS-219, DS-117). **Two gaps recorded rather than closed:** DS-168's design-unit floor has no check (handed to T-005), and every finding here still comes from one deck by one author. |
| 2026-08-06 | → in_progress | **The task's own finding, and it changed the work: three of the four `hard`×`hard` conflicts were not real impossibilities.** F-04 and F-05 are a general rule and its own specific case with no precedence stated; F-01 was a number in a rule whose principle was never in doubt. Only F-10 is genuinely jointly-unsatisfiable. So the fix for two of the four is a scope clause and **no rule was softened** — where the instinct on opening was to arbitrate. Generalised as **L-28**. |
| 2026-08-06 | → planned | §2 was written at creation. Order held: the owner question first, then the conflicts. |
| 2026-08-06 | → specified | The one live open question settled by the owner — **F-03 becomes DS-218**, a rule of its own, rather than an inline amendment to DS-140 or a pointer at §7's criterion. |
| 2026-08-06 | → proposed | Raised by T-024, which built a real 12-slide deck strictly to the ruleset and produced **thirteen findings** — four of them conflicts between two `hard` rules, three rules unimplementable as written. Kept separate from T-024 on purpose: a test that edits the thing it tests is not a test, so the findings were recorded unapplied. |
