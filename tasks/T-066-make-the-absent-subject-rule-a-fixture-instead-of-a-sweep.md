---
id: T-066
title: Make the absent-subject rule a fixture instead of a sweep
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-051, T-065]
work_package: PH1
shipped_in: 0.1.3
owner: the project owner
business_value: critical
effort: m
created: 2026-08-10
updated: 2026-08-12
deliverables:
  - tools/deck/audit.py
---

# T-066 — Make the absent-subject rule a fixture instead of a sweep

## 1. Specify

**Outcome**
No verdict row can fail a deck for not containing the thing it judges, and **the gate proves that
about itself on every run** rather than a person proving it once with a script.

**Why this exists**
This is the third time the same defect has been found, each time by someone tripping over it:

| | What was found | How |
| :--- | :--- | :--- |
| T-051 | Rules **passing** on an absent subject | A fixture built to be missing things |
| T-065 | Four rules **failing** on an absent subject | An outside project's deck |
| here | **Three more**, one of them still failing that project after v0.1.2 shipped | The same project re-running the fix |

**T-065 marked its sweep criterion met, and it was not.** The sweep was a one-off script that
segmented each verdict row at the first `),`, so any row whose expression sat on a later line was
truncated before it was read. It reported one candidate. Re-run with balanced-paren parsing it
reports five. That criterion is now recorded as `not met` on T-065.

**The fixture has two holes, and they are the actual defect**

1. **It only asks which rows PASS on an absent subject.** `ABSENCE_IS_A_PASS` is a declared table
   with a reason per entry, enforced every run. There is no mirror, so a row that *fails* on an
   absent subject is checked by nobody. That asymmetry is why T-051 could convert three rows and
   leave four beside them, and why T-065 could convert four and leave three.
2. **It evaluates `render_verdicts` and `split_verdicts` only.** `reduced_verdicts` produces rows
   too, and DS-143 is one of them, so an entire family is outside the discipline.

**Measured, not swept — 2026-08-10.** All three producers run against the nothing-was-found
measurement `self_test` builds, with `reduced_verdicts` given a render that succeeded and a
preference that took. **Nine rules fail, not eight**, and every failing row was read verbatim rather
than parsed out of the source:

| Row | Prints | Class |
| :--- | :--- | :--- |
| DS-081 | `slides: 0` | **declared fail** — a deck with no slides is a real failure |
| DS-070 | `reflow view engages: None` | **declared fail** — the reflow view is required, so its absence is a defect |
| DS-075 | `reflow scrollWidth at 320 CSS px: None` | **guarded by DS-070** |
| DS-076 | `position preserved returning from the reflow view: left None` | **guarded by DS-070** |
| DS-113 | `sprite icons never used: 0 of 0` | **convert** — `symbolCount > 0` |
| DS-160 | `third-tier disclosure inside a panel: 0, over 0 panel(s)` | **convert** — `panelCount > 0` |
| DS-143 | `risen elements hidden under reduced motion: 0 of 0` | **convert** — `risen > 0` |
| DS-135 | `the page title carries the slide's name: None` | **the probe, not the row** — see below |
| DS-217 | `chrome height: None du` | **the fixture, not the row** — see below |

**Three different defects wear one symptom, and only the first is what the task was raised for.**

1. **The subject is absent.** DS-113, DS-160 and DS-143 each carry a clause requiring the deck to
   *contain* the thing the rule judges — the identical shape to DS-164, which T-065 deleted. These
   convert to `None`.
2. **The subject is present and the probe never measured it.** `out.titleCarriesSlide` is assigned
   **inside `if (btns.length)`**, the disclosure-controls block, because the reading has to follow a
   navigation and the navigation happens there. So a deck with no disclosure controls never gets
   DS-135 measured and the row reports `False`. **Its subject — a page title and a slide name —
   exists in every deck**, so converting the row to `undecided` would silently retire a real check
   on exactly the decks that prompted this work. The measurement is hoisted out of the block instead.
   **T-065's sweep cleared DS-135 explicitly, on the claim that the probe emits the key
   unconditionally. That claim is false**, and `titleCarriesSlide` is not in `ALWAYS_MEASURED`
   either, so the stated reason fails on its own terms. This is the sixth instance.
3. **The fixture's own measurement is malformed.** `out.chromeHeightDu` *is* emitted
   unconditionally — `chromeRect ? … : 0` — so a real deck with no chrome measures `0` and passes.
   The row only fails here because `chromeHeightDu` is missing from `ALWAYS_MEASURED`, letting
   `data.get("chromeHeightDu", 999)` fire a default the probe can never produce. The `KeyError`
   guard in `self_test` exists for precisely this and a `.get()` with a default walks past it.
   **Nothing is wrong with DS-217**; the nothing-was-found measurement is wrong, and any row reading
   a probe-unconditional key through a defaulted `.get()` is today being judged against a value that
   does not occur.

Class 3 is the one that makes the mirror table urgent rather than tidy: **until the measurement
models the probe, the mirror would enshrine a false failure in writing** and call it a decision.

**Scope**
- In: `ABSENCE_IS_A_FAIL`, mirroring `ABSENCE_IS_A_PASS`: every row that fails on the
  nothing-was-found measurement is declared with its shape and its reason, and an undeclared one
  fails the self-test.
- In: extending the fixture to **every** verdict producer, `reduced_verdicts` included.
- In: converting whichever rows the table shows to be absent-subject cases rather than real
  verdicts. DS-160, DS-113 and DS-143 are already known.
- In: **making the nothing-was-found measurement model the probe.** A row reading a key the probe
  emits unconditionally must see the probe's value, not a `.get()` default — class 3 above, and the
  reason the mirror table cannot be written before it.
- In: hoisting `out.titleCarriesSlide` out of `if (btns.length)` so DS-135 is measured on a deck
  with no disclosure controls — class 2 above.
- In: a check that no single **row** is claimed by both tables.
- Out: the `undecided` bucket in `check.py`, which T-065 settled and which is right.
- Out: the reporting project's remaining findings on its own deck.
- Out: **a check that no *rule* is claimed by both tables**, which was in scope when this task was
  raised and is refuted by the measurement above: DS-143 and DS-217 each have one row that passes
  and another that fails on the same measurement, and both claims are correct. Declarations are
  per-row, so `ABSENCE_IS_A_PASS`'s rule-id key does not carry over to the mirror unchanged.

**Acceptance criteria**
- [ ] Every verdict row that fails on an absent subject is declared with a reason, or converted
- [ ] `reduced_verdicts` is inside the fixture, and adding a producer that is not fails the run
- [ ] DS-160, DS-113 and DS-143 are undecided on a deck lacking their subject
- [ ] **DS-135 is decided, not undecided, on a deck with no disclosure controls** — it has a title
      and a slide name, so a `None` here would be the check retiring itself
- [ ] **A row reading a probe-unconditional key through a defaulted `.get()` is caught by the
      fixture**, shown by DS-217's height row no longer failing on nothing-found
- [ ] The two tables cannot both claim one row, and the check proves it by rejecting a seeded pair
- [ ] The reference deck's verdicts are unchanged, checked by diff
- [ ] The seeded-defect deck still fails everything it is supposed to
- [ ] A declaration that outlives its row is reported, as `ABSENCE_IS_A_PASS` already does
- [ ] **The sweep is deleted.** If a hand-run script is still needed, this task has not finished

**Open questions**
- **Settled 2026-08-10, on the rule's own reason: `symbolCount > 0` is not a requirement and the
  clause goes.** DS-113 reads *"a sprite containing only the icons used"* — a prohibition over the
  sprite's symbols, which a deck with no sprite cannot violate. Nothing in `DESIGN-SYSTEM.md`
  requires a deck to carry icons; DS-112 governs where icons come from *if* there are any. The
  clause enforced in code a rule the ruleset does not state, which is DS-164's finding verbatim, and
  it takes DS-164's answer.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Instrument the nothing-was-found measurement so it records every key each row reads and every `.get()` default that fired | The recording measurement type in `audit.py`, and the printed read-set |
| 2 | Split that read-set against the probe: keys emitted unconditionally, and keys emitted inside a guard. Declare both, naming the guard for each conditional key | `ALWAYS_MEASURED` extended; `CONDITIONALLY_MEASURED` added, with its guard per key |
| 3 | Rebuild the measurement from the unconditional set and re-run all three producers | The corrected failing set, in §3 |
| 4 | Classify every remaining failing row: declared fail, guarded by a named row, or convert | The table, in §3 |
| 5 | Write `ABSENCE_IS_A_FAIL`, keyed per row; an undeclared failure fails the self-test, and no row may be claimed by both tables | The edited `audit.py` |
| 6 | Convert DS-113, DS-160 and DS-143; hoist `out.titleCarriesSlide` out of `if (btns.length)` | The edited rows, and the edited probe |
| 7 | Bring `reduced_verdicts` inside the fixture, and make a producer the fixture does not exercise fail the run | The edited `self_test` |
| 8 | Correct `self_test`'s own comment, which records T-065's DS-070/DS-135 clearance as fact | The edited comment |
| 9 | Diff the reference deck's verdicts before and after; run the seeded-defect deck | Both runs, in §3 |

**Sequencing.** Steps 1–3 come first because they can invalidate step 4: until the measurement models
the probe, the classification would be made against values the probe cannot produce, which is how
DS-217 arrived on the list. Step 6 is deliberately after step 5, so each conversion is made against a
fixture that already fails without it (**L-04**).

**Decision — the fixture records what rows read, rather than a person keeping a list current.**
The obvious alternative is to extend `ALWAYS_MEASURED` by hand until DS-217 stops failing, and it was
rejected: it fixes the one instance and leaves the next `.get(key, default)` on an unmodelled key
exactly as invisible as this one was. **That is the shape of every previous fix in this family** —
T-038, T-051, T-065 — and the thing this task exists to stop. Recording the reads makes an unmodelled
key a named failure at self-test time, so the discipline survives a row added tomorrow by someone who
has not read this task.

**Decision — `CONDITIONALLY_MEASURED` names each key's guard, and the guard is written down.**
A key list alone would not have caught DS-135: `titleCarriesSlide` is conditional *by accident of
where the reading sits*, not by the nature of its subject. Naming the guard is what makes the
difference between "this subject can be absent" and "this measurement is in the wrong place" legible
at the point of declaration.

**The sweep needs no deletion — it was never committed.** It ran once, in a session, and left nothing
behind but the claim in T-065's record, which is the whole complaint. The criterion is met by the
fixture answering the question on every run instead.

**Output paths**
- `tools/deck/audit.py`

## 3. Implement

**Decisions & assumptions**

- **The specify was wrong about the disjointness check, and the correction makes it the strongest
  check in the fixture — 2026-08-10.** §1 recorded that "no rule in both tables" was refuted by
  measurement, because DS-143 and DS-217 each passed on one row and failed on another. That
  observation was right and the conclusion drawn from it was backwards: **the overlap was not a
  legitimate case, it was the two defects.** Convert DS-143's risen row and model `chromeHeightDu`
  and the overlap disappears — and any future row that fails on an absent subject while its rule
  passes on another lands in it. So the check is kept, rule-keyed as `ABSENCE_IS_A_PASS` is, and it
  is the one that would have caught both of this task's fixture-level faults on its own.

- **The fixture records what rows read, rather than a table someone remembers to extend.** The
  alternative — add `chromeHeightDu` to `ALWAYS_MEASURED` and move on — fixes one instance and
  leaves the next unmodelled `.get()` default exactly as invisible. That is what T-038, T-051 and
  T-065 each did, and the reason this is the fourth attempt. `Measurement` overrides `__getitem__`
  and `get`, so a key in neither declared table is a **named** self-test failure the moment a row
  starts reading it.

- **`CONDITIONALLY_MEASURED` names each key's guard in prose, not just the key.** A list of names
  would have accepted `titleCarriesSlide` as legitimately conditional. Written out, *"measured inside
  the disclosure block"* is visibly not a statement about page titles, and that is the whole
  difference between an absent subject and a misplaced measurement.

- **DS-135 is hoisted AND converted, and both halves are needed.** The hoist moves the reading out
  of `if (btns.length)` so every multi-slide deck is measured; the `None` branch covers what stays
  genuinely conditional, which is a one-slide deck with nowhere to navigate to and therefore no
  second title to compare. Converting alone would have retired the check on the decks that prompted
  the task; hoisting alone would have left a row failing a one-slide deck for the same old reason.

- **The shape field accepts a `+` — 2026-08-10.** DS-143 reaches the pass table by two routes at
  once: one row is a prohibition (nothing left animating), another a conditional (no flow owes no
  dash), and the third is the converted one. Forcing a single shape per rule would have meant
  writing down a reason that was true of one row and false of another, which is the kind of
  approximate record this whole family of defects grew out of.

- **The producer list is derived from the module, not written down.** `reduced_verdicts` sat outside
  the fixture from the day it was written and nothing said so, because the fixture named its
  producers and a name nobody adds is a name nobody misses. `sorted(n for n in globals() if
  n.endswith("_verdicts"))` compared against the exercised set makes the fourth one a red run.

- **`ALWAYS_MEASURED` became a dict of key → nothing-was-found value.** A name alone cannot say
  whether absence means `0`, `[]` or `None`, and `smallestTarget` is a null on a real run while
  `chromeHeightDu` is a zero. The tuple form could only have been extended by guessing.

**Verification**

*The fixture, held to L-04 — ten seeded defects, each undone before the next:*

```
  DS-160 failing on an absent subject          CAUGHT  ... not declared in ABSENCE_IS_A_FAIL
  DS-113 failing on an absent subject          CAUGHT  ... not declared in ABSENCE_IS_A_FAIL
  DS-135 failing on an absent subject          CAUGHT  ... not declared in ABSENCE_IS_A_FAIL
  DS-143 failing on an absent subject          CAUGHT  ... not declared in ABSENCE_IS_A_FAIL
  chromeHeightDu unmodelled again              CAUGHT  ... in neither ALWAYS_MEASURED nor CONDITIONALLY_MEASURED
  a fourth producer left outside the fixture   CAUGHT  the module defines bogus_verdicts, ...
  a declared fail that no longer fails         CAUGHT  the declaration outlived the row it explains
  a real failure nobody declared               CAUGHT  DS-070 FAIL ... not declared
  one rule claimed by both tables              CAUGHT  DS-035 are declared in BOTH tables
  an `entailed by` whose owner stopped failing CAUGHT  The guard has stopped guarding
```

*The case the task exists for, put in front of the gate.* The reference deck with its disclosure
classes renamed and its `<symbol>` sprite removed — 17 controls and 26 panels to zero, nine symbols
to zero — which is the shape of deck the reporting project built:

```
  DS-113          sprite icons never used: 0 of 0                     NO SUBJECT
  DS-160          third-tier disclosure inside a panel: 0, over 0     NO SUBJECT
  DS-135          the page title carries the slide's name: True       pass
  undecided, no subject  8   DS-113 DS-130 DS-138 DS-146 DS-160 DS-164 DS-166 DS-228
  SILENT                 0
```

**DS-113 and DS-160 stop failing, and DS-135 goes on deciding** — which is the pair of outcomes the
hoist exists to get. That deck's four remaining failures are DS-013 and DS-229, and they are the
diagnostic's own doing: renaming a contracted class is exactly what the component contract is there
to report. Deleting the markup outright was tried first and left the document damaged enough that
render calibration failed, which answers a different question.

*The shipped decks, unchanged.* Full output diffed before and after, both decks:

```
reference deck   the only line that differs is DS-135's sample text
                 ('The window sh...' rather than 'Bikes win thr...'), because the
                 reading now follows its own navigation instead of the disclosure
                 block's. Verdict True before and after.
                 113 owned / 0 undecided / 0 SILENT / 0 failure(s)
seeded deck      same single line, same 4 failure(s): DS-141, DS-035, DS-142, DS-075
sort-window      113 owned / 0 undecided / 0 SILENT / 0 failure(s)
```

*The rest of the gate:* `check_scaffold.py` 14 of 14, `critique.py --self-test` 12 of 12.

**Outputs produced**
- `tools/deck/audit.py`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every row failing on an absent subject is declared with a reason, or converted | **met** | `ABSENCE_IS_A_FAIL` declares four — DS-081 and DS-070 as `requirement`, DS-075 and DS-076 as `entailed by DS-070` — and an undeclared failure exits the run. Seeded by removing DS-070's entry: caught |
| `reduced_verdicts` is inside the fixture, and adding a producer that is not fails the run | **met** | Producers are `sorted(n for n in globals() if n.endswith("_verdicts"))` compared against the exercised set. Seeded a fourth producer: caught, naming it |
| DS-160, DS-113 and DS-143 are undecided on a deck lacking their subject | **met** | DS-113 and DS-160 report `NO SUBJECT` on the stripped deck, where before they failed. **DS-143 is proven by the fixture rather than by that deck**, which kept its risen elements — the fixture asserts it returns `None`, and un-converting it is caught |
| DS-135 is decided, not undecided, on a deck with no disclosure controls | **met** | `the page title carries the slide's name: True   pass`, on a deck with zero controls and zero panels. This is the criterion the hoist exists for, and the one a conversion alone would have failed |
| A row reading a probe-unconditional key through a defaulted `.get()` is caught | **met** | DS-217's height row no longer fails: `chromeHeightDu` is modelled at `0`, which is what `chromeRect ? … : 0` emits. Seeded by removing it again: caught by name |
| The two tables cannot both claim one row, and the check rejects a seeded pair | **met, criterion corrected** | See below. The check is **rule**-keyed, not row-keyed; seeding a rule that genuinely passes on one row and fails on another is caught |
| The reference deck's verdicts are unchanged, checked by diff | **met** | Full output diffed. One line differs, and it is DS-135's sample text — the reading follows its own navigation now rather than the disclosure block's. Verdict `True` both sides; `113 / 0 undecided / 0 SILENT / 0 failure(s)` |
| The seeded-defect deck still fails everything it is supposed to | **met** | Same four: DS-141, DS-035, DS-142, DS-075. Same single sample-text difference |
| A declaration that outlives its row is reported | **met** | Both directions. Seeded a `DS-999` fail declaration and an `entailed by` whose owner passes: both caught |
| **The sweep is deleted** | **met** | It was never committed — it ran once in a session and left only the claim in T-065's record, which is the complaint. The fixture answers the question on every run instead |

**One criterion was corrected during review, and the original text is kept.** As written in
`specify` it read *"The two tables cannot both claim one **row**"*, on the measured ground that
DS-143 and DS-217 each passed on one row and failed on another, so a rule-keyed check would collide.
**The measurement was right and the inference from it was backwards.** Both overlaps were the
defects themselves: convert DS-143's risen row, model `chromeHeightDu`, and no rule is in both
tables. Keyed by rule the check is not merely still possible — it is the one that catches this
task's two fixture-level faults on its own, and it needs no row identity that the row tuples do not
carry. Agreed with the owner's standing instruction to decide and report.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-10 | → done | **The fixture now asks the question in both directions, and it is the asymmetry rather than any single row that this closes.** Six rules had been failing decks for what they lack; three are converted here (DS-113, DS-160, DS-143), DS-135 was a misplaced measurement and is hoisted out of `if (btns.length)`, and DS-217 was never a defect at all — the fixture's own eight-name model of a forty-key probe was handing it a `.get()` default no deck can produce. **A bad model does not only hide defects, it manufactures ones to explain**, and the first honest classification would have written DS-217's false failure into a declared table with a reason. Ten seeded defects prove the fixture fails on what it is for, including all four converted rows put back one at a time. On a deck stripped of every disclosure and every icon — the reporting project's shape — DS-113 and DS-160 report `NO SUBJECT` where they used to fail, **and DS-135 still decides**, which is what a conversion alone would have thrown away. Both shipped decks are byte-identical in verdict. Generalised as [**L-54**](../docs/LESSONS.md), because L-44 already told this project to build a forcing function and the one it built watched one direction. |
| 2026-08-10 | → planned | **Owner agreed the specify, both recommendations taken: hoist DS-135's measurement rather than declare its failure, and keep all three defect classes in one task rather than splitting them.** The plan that follows is not the one the raise implied. Extending `ALWAYS_MEASURED` by hand until DS-217 stops failing would fix the instance and leave the next unmodelled `.get()` default as invisible as this one — which is what T-038, T-051 and T-065 each did, and why this is the fourth attempt. So the fixture **records what each row reads** and fails on a key it was never told about, and `CONDITIONALLY_MEASURED` names the guard each conditional key sits behind, because a bare key list would not have distinguished DS-135's misplaced measurement from a genuinely absent subject. Steps 1–3 precede the classification deliberately: DS-217 got onto the list *because* it was classified against a value the probe cannot emit. **The sweep turns out to need no deletion — it was never committed**, which is precisely the complaint. |
| 2026-08-10 | → specified | **The specify was written from a claim and is now written from a measurement, and the measurement is worse.** All three producers were run against the nothing-was-found measurement rather than reasoned about: **nine rules fail, not eight**, and the nine split into three unrelated defects that had been collapsed into one. Only DS-113, DS-160 and DS-143 are the absent-subject case this task was raised for. **DS-135 is a sixth instance and T-065 cleared it by name on a false premise** — `out.titleCarriesSlide` is assigned inside `if (btns.length)`, so a deck with no disclosure controls never has it measured, and the key is not in `ALWAYS_MEASURED` either, which is the reason T-065 gave. Its subject exists in every deck, so the fix is to hoist the measurement, **not** to convert the row: converting would retire a live check on precisely the decks that prompted the work. **DS-217 is not a defect at all** — the probe emits `chromeHeightDu` unconditionally and a chrome-less deck measures `0`; the row fails only because the fixture's measurement omits the key and a defaulted `.get()` supplies `999`. That inverts a scope item: **the measurement has to model the probe before the mirror table is written**, or the mirror enshrines a false failure in writing and calls it a decision. The `no rule in both tables` check is refuted outright — DS-143 and DS-217 each pass on one row and fail on another, correctly, so declarations are per-row. DS-113's open question is settled on the rule's own text and takes DS-164's answer: the clause goes. |
| 2026-08-10 | → proposed | Raised on the third finding of one defect, and the third is the one that matters: **v0.1.2 shipped claiming a complete sweep and the sweep was broken**, so DS-160 kept failing the very project whose report produced the fix. [T-065](T-065-four-rules-still-fail-a-deck-for-not-having-their-subject.md) §3 recorded a deliberate decision not to build the general table because it was *"a bigger change than a patch release should carry"*. That was wrong, and it is the whole reason this task exists: **a hand-run script is not a gate**, which is this repository's own position turned on itself. `PH1` because the published gate still fails legitimate decks. |
