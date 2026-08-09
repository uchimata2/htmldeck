---
id: T-051
title: A check whose subject is absent must not report a pass
type: fix
status: done
phase: review
parent: T-044
blocked_by: []
related: [T-005, T-038, T-043]
work_package: none
owner: the project owner
created: 2026-08-09
updated: 2026-08-09
deliverables:
  - tools/deck/audit.py
  - tools/deck/check.py
  - tools/deck/contrast.py
  - tools/deck/static_variants.py
  - tools/deck/deliverable_variants.py
  - docs/LESSONS.md
  - README.md
  - examples/README.md
---

# T-051 — A check whose subject is absent must not report a pass

## 1. Specify

**Outcome**
No verdict in `tools/deck/` reports `pass` for a rule whose subject the deck does not contain. A
check that finds nothing to judge reports that it found nothing, and the run treats it the way it
treats any other rule nothing decided.

**Why this one**
Found by [T-044](T-044-restore-the-seeded-defect-fixture-and-its-claims.md) while re-measuring the
seeded fixture, in the one place it could be found — a deck deliberately missing something:

```
good deck     DS-140  `Current` renders dashed: 7px, 6px            pass
seeded deck   DS-140  `Current` renders dashed: no dashed flow      pass
```

The S3 seed replaces the deck's only dashed flow with a card row, so DS-140's subject stops
existing — and `data.get("currentDasharray") != "none"` is `True` for `None`, so the rule passes on
its own absence.

**This is L-36 inside the instrument**, and the repository already treats the pattern as a defect
everywhere else: `check.py` excuses DS-087 in writing precisely because *"no deck in the repository
has an appendix, so the check would have no subject to run against and would pass on nothing"*, and
[T-038](T-038-the-gate-emits-verdicts-for-judge-rules-and-one-wrong-id.md) fixed exactly this shape
for DS-130, which landed on a slide with no disclosure control, reported `null`, and passed. So the
question is not whether DS-140 should be fixed but **why the same fault keeps being found one
instance at a time** — three now — when the gate is otherwise built around the principle that a
rule nothing decided fails the run.

**Scope**
- In: an audit of every verdict in `tools/deck/` for the same shape — a truthy-by-absence
  comparison, a `.get()` defaulting to something that passes, a filter over an empty list.
- In: deciding what a subjectless check reports. It is **not** obviously a failure: a deck with no
  flows is legitimate, and DS-140 does not require one. The candidate is a third state the account
  already has room for — the rule is *not decided by this run*, which is what `SILENT` means.
- In: whatever prevents the fourth instance, which is the point of the task.
- Out: adding subjects to the reference deck so the checks have something to bite on. That
  reverses the dependency — the instrument would be shaping the artifact.
- Out: `judge` rules, which no check decides by definition.

**Inputs**
- [`tools/deck/audit.py`](../tools/deck/audit.py) — `render_verdicts()`, and the DS-130 comment
  recording the same fault
- [`tools/deck/check.py`](../tools/deck/check.py) — the account, and DS-087's excusal wording
- [`docs/LESSONS.md`](../docs/LESSONS.md) — **L-36**
- [T-044](T-044-restore-the-seeded-defect-fixture-and-its-claims.md) §4 — where this was found

**Acceptance criteria**
- [ ] Every verdict that can be reached with its subject absent is identified, and the list is in
      the task rather than only in the fix
- [ ] A deck with no dashed flow does not produce a DS-140 `pass`
- [ ] Whatever the subjectless state is, the coverage account still partitions
- [ ] Demonstrated against the seeded fixture, which is the deck that exposed it (**L-04**)
- [ ] Something makes the fourth instance loud rather than requiring another audit to find it

**Open questions**
- none — the reporting question above is the implementer's, decided from what `SILENT` already
  means in the account.

## 2. Plan

**The approach, and why it is not "audit the predicates by eye".** `render_verdicts()` is pure by
construction — its docstring says so, and T-005 built it that way so a variant suite could seed a
break and ask the same code that gates the real deck. That makes the audit mechanical: capture one
real measurement, delete the subject, and ask what the gate says. Reading forty predicates and
judging each is how the first two instances were found, one at a time, and it is why neither
generalised.

**The discriminator, decided here.** Absence of a subject is not uniformly a defect, and treating it
as one would fail decks the ruleset permits. Two shapes are *correct* and stay:

- a **prohibition** — *never X*, *at most n X*. Its subject is the deck, which exists. Zero X is a
  genuine pass.
- a **conditional** — *if X then Y*. DS-218 is one: no looping motion, no obligation to control it.

The defect is a **requirement over an optional construct** — *every X is Y* — where the row cannot
tell *nothing wrong* from *nothing there*. Three rules already carry the fix (`symbolCount > 0`,
`discControls > 0`, `panelCount > 0`), which is what makes it a pattern rather than a bug.

**What a subjectless check reports — settled.** It goes to `silent`, and the run fails, which is what
`SILENT` already means and what every published description of the account says. It does **not** get
a fourth, non-failing bucket: that would let coverage erode quietly as rules drift into it, which is
**L-36 re-created one level up**. What the account gains is the *reason* — a rule silent because no
check exists needs a different fix from one silent because the check ran and found nothing, and the
report now says which.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Capture one real measurement, then delete each **construct** the probe emits under a guard and re-run the pure verdicts. A key at a time is the wrong model: a deck with no reflow view loses ten keys together and a sibling row goes red | The finding list, in §3, classified A/B/C |
| 2 | Sweep the other four verdict sources by hand — `contrast.py`, `contract.py`, `content.py`, `printpages.py` — since none of them is pure enough to drive | Their rows in the same list |
| 3 | Fix the Class A rows: DS-140's `!= "none"`, and `contrast.py`'s fabricated dark theme | `audit.py`, `contrast.py` |
| 4 | Fix the Class B rows, whose shape is the same even though a sibling makes the run red today: `is not False`, `None == None`, and a `.get()` default that passes | `audit.py` |
| 5 | Give `audit.py` a self-test that drives every verdict against a measurement in which nothing was found, and requires each passing row to be **declared in writing** as a prohibition or a conditional. Wire it into `check.py.run()` so it fires on every gate run, not when someone remembers a suite | `audit.py`, `check.py` |
| 6 | Carry the reason into the account: `silent` reports *no check exists* separately from *the check found no subject* | `check.py` |
| 7 | Demonstrate against the seeded fixture — the S3 seed removes the deck's only dashed flow, which is the deck that exposed this | A run, in §4 |
| 8 | Write the generalised lesson, which is the deliverable the previous two instances did not produce | `docs/LESSONS.md` |

## 3. Implement

### The audit — every verdict that can be reached with its subject absent

**How it was taken, since it decides how much the list is worth.** `render_verdicts()` is pure, so
the sweep is mechanical rather than a reading: capture one real measurement from the reference deck,
delete a whole **construct** the probe emits under a guard, and re-run. A key at a time is the wrong
model — a deck with no reflow view loses ten keys together, and a sibling row goes red. The other
four verdict sources are not pure enough to drive and were read.

**36 rendered rows. 24 pass against a measurement in which nothing was found**, which is the
candidate list, not the defect list — most of them are prohibitions whose subject is the deck.

**Class A — the run stays green and a rule reports a pass on a subject the deck does not contain.**

| Rule | Where | The expression | The deck that exposes it |
| :--- | :--- | :--- | :--- |
| **DS-140** | `audit.py` | `data.get("currentDasharray") != "none"` — `None != "none"` is `True` | no dashed flow. **The reported instance** |
| **DS-027** | `contrast.py` | `read_tokens` returned `dark or dict(light)`, so the fallback theme *is* the light theme | no dark theme. Deleting the whole dark block from the reference deck produced **zero failures** and a row reading *dark 17 pairs / 0 failing* |

**Class B — the row claims a rule it did not decide, but a sibling row fails, so no deck reaches a
clean run.** Same shape, no escape today; each one is a sibling edit away from becoming Class A.

| Rule | The expression | Subject absent when | Guarded by |
| :--- | :--- | :--- | :--- |
| **DS-138** | `is not False` on a null | no panel opened | DS-160, DS-164, DS-166 |
| **DS-228** | `.get("panelsOpenAfterTwo", 0) <= 1` | no disclosure control | the same three |
| **DS-073** | `docPanelsOpen == docPanelsTotal`, `None == None` | no reflow view | DS-070, DS-075, DS-076 |
| **DS-168** | `smallTargets == 0` with nothing measured | no tabbable found | DS-130 — **and this one is not hypothetical**: the `slide-is-not-a-section` variant breaks the deck badly enough that `smallestTarget` is null, and DS-168 reported a pass on it until this task |
| **DS-012**, **DS-024** | `return True` with no dark block | no dark theme | DS-027, once Class A above is fixed |

**Class C — absence is a genuine pass and the row stays.** Declared in `ABSENCE_IS_A_PASS` with the
shape and the subject, 18 rules: DS-035 · DS-043 · DS-073 · DS-080 · DS-091 · DS-092 · DS-132 ·
DS-142 · DS-202 · DS-203 · DS-205 · DS-214 · DS-215 · DS-216 · DS-217 · DS-218 · DS-219 · DS-227.

**The four other verdict sources are clean, and three of them cite L-36 for why.** `contract.py`
fails on *no result*, *NO NON-TEXT ELEMENT MEASURED* and *no body run measured at 720p*;
`printpages.py` requires two independent page counts to agree so a parse that found nothing cannot
read as zero; `content.py` guards FIG-1 with `deckFigures > 0`, which covers FIG-2 and FIG-3.
`contrast.py` had the guard and it was **on the wrong quantity** — see Class A. `chrome_row.py` and
`contents_bound.py` are standalone sweeps the gate does not import and are out of scope.

**So the fault is concentrated in one file, and the reason is structural.** The four clean modules
each have a single place that emits rows, written once by one person. `audit.py` has 36 rows written
across four tasks, and the guard is per row — which is why a general fix had to be a **forcing
function** rather than another correct row.

### Decisions & assumptions

- **A subjectless check reports `None`, the rule falls to `silent`, and the run fails** — not a
  fourth forgiving bucket — 2026-08-09. A non-failing bucket would let coverage drain into it deck
  by deck while the gate reported green, which is L-36 one storey up. It also preserves every
  published description of the account: the three states are intact, `bucketSum` arithmetic is
  untouched, and no figure in any document moved.
- **`silent` gains a reason, not a sibling.** `silentNoSubject` separates *no check exists* from
  *the check ran and found no subject*; the two need opposite fixes and the account could not tell
  them apart because the second used to report `pass` and never reached the account at all.
- **DS-027 fails rather than going undecided** — 2026-08-09. It is `hard` and states a property of
  *both* themes, so a deck with one theme fails it; the second theme is the rule's stated subject,
  not an optional construct. This is the opposite side of the same discriminator from DS-140, and
  the pair is why the discriminator had to be written down rather than applied by feel.
- **`ok is False` replaces `not ok` in all five consumers.** Left alone, a row that decided nothing
  would have counted as a caught variant in two suites and as a deck defect in the gate.

### Outputs produced

- [`tools/deck/audit.py`](../tools/deck/audit.py) — `ABSENCE_IS_A_PASS`, the three-valued verdict,
  five predicates fixed, and `self_test()`
- [`tools/deck/check.py`](../tools/deck/check.py) — the account reads three values; `silentNoSubject`
- [`tools/deck/contrast.py`](../tools/deck/contrast.py) — `darkDeclared`, and a self-test on strings
- [`tools/deck/static_variants.py`](../tools/deck/static_variants.py),
  [`tools/deck/deliverable_variants.py`](../tools/deck/deliverable_variants.py) — `ok is False`
- [`docs/LESSONS.md`](../docs/LESSONS.md) — **L-44**
- [`README.md`](../README.md), [`examples/README.md`](../examples/README.md) — the stale caveat
  replaced by what the fixture now reports

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every verdict reachable with its subject absent is identified, and the list is in the task | **met** | §3, classified A/B/C. Derived by a construct sweep over a captured measurement, not by reading predicates — which is how the first three were found, one at a time |
| A deck with no dashed flow does not produce a DS-140 `pass` | **met** | On the seeded fixture: `` DS-140  `Current` renders dashed: no dashed flow in this deck  NO SUBJECT ``, and `SILENT 1 DS-140` |
| Whatever the subjectless state is, the coverage account still partitions | **met** | Seeded deck `checked 77`, `SILENT 1`, `buckets sum to 111 = owned`. Reference deck unchanged at 78 / 0 / 111 |
| Demonstrated against the seeded fixture, which is the deck that exposed it (**L-04**) | **met** | Both decks run. `seed_defects.py --check` first, so the fixture is what regenerating produces |
| Something makes the fourth instance loud rather than requiring another audit | **met** | `audit.self_test()`, called from `check.py.run()`, so it fires on every gate run. Shown to fail five ways: a declaration removed, a declaration for a row that decides, a guard that no longer guards, an invented shape, and DS-140 reverted to the original fault |

**Two things worth stating that no criterion asked for.**

- **No published figure moved.** The reference deck contains every subject, so `checked` stays 78
  and `SILENT` stays 0. `CLAUDE.md`, `README.md`, `BRIEF.md`, `DESIGN-RATIONALE.md`,
  `examples/README.md` and `pipeline.md` all state *78 of 111* and all remain correct — which was
  not a given, and was as much of the argument against a fourth bucket as the L-36 reasoning.
- **A deck whose slides carry no headline passed DS-091**, the only unowned subject the sweep turned
  up. ~~A gap in the ruleset, not in the gate: no rule requires a slide to carry a headline at
  all.~~ **That diagnosis was wrong** — corrected 2026-08-09 by
  [T-053](T-053-enforce-the-headline-ds-091-requires.md), which read the rule: *"Per slide: **one**
  headline ≤ 6 words plus ≤ 3 supporting fragments"* requires the headline in its own first clause.
  The gap was in the check, and wider than one clause — DS-091 has three and the gate decided one.
  T-053 closed the first, excused the fragment count in writing, and DS-091's entry in
  `ABSENCE_IS_A_PASS` is now `guarded by DS-081` rather than a prohibition.

**Child fix tasks raised**
- none. Class B was fixed here rather than deferred — it is four expressions, and leaving the shape
  in place while writing a lesson about the shape would have repeated the mistake of the first two
  instances.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-09 | → done | Six rules fixed, not one. The sweep found a **second Class A instance nobody had suspected**: deleting the entire dark theme from the reference deck produced zero failures, because `contrast.py`'s token reader falls back to a copy of the light theme and DS-027 then reports *dark 17 pairs / 0 failing* about a theme that does not exist. That file is the one place that had already learned this lesson and cites L-36 for its pair count — **the guard was on the wrong quantity**, counting pairs when the absent subject was a theme. The general fix is a forcing function rather than a correct row: `audit.self_test()` drives every verdict against a measurement in which nothing was found, requires each row that still passes to be declared a prohibition or a conditional in writing, and **tests every `guarded by` claim** rather than trusting it. Wired into `check.py.run()`, so it fires on every gate run. Reference deck unchanged at 78 / 0 / 111, so no published figure moved. |
| 2026-08-09 | → planned | §1 accepted unchanged and planned in eight steps. Two decisions taken before any code: the **discriminator** — a prohibition and a conditional pass legitimately on absence, a requirement over an optional construct does not — and **what a subjectless check reports**, which is `silent` and a red run rather than a fourth bucket, because a non-failing bucket lets coverage erode into it and that is L-36 one level up. |
| 2026-08-09 | → proposed | Raised by [T-044](T-044-restore-the-seeded-defect-fixture-and-its-claims.md), which found it by running the gate over a deck built to be missing things — the only kind of deck that can expose it. DS-140 passes on a deck with no dashed flow because `None != "none"`. **The reason this is worth its own task rather than a one-line fix is that it is the third instance**: DS-130 was the same fault and was fixed in place by T-038, DS-087 is excused in `check.py` for exactly this reason, and nothing generalised either. The gate's whole design is that a rule nothing decided fails the run; a rule decided *vacuously* is the same claim wearing a pass. |
