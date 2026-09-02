---
id: T-235
title: Reconcile the skill's documents with the tools and rules they describe
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
updated: 2026-08-30
deliverables: []
shipped_in: 0.7.0
---

# T-235 — Reconcile the skill's documents with the tools and rules they describe

## 1. Specify

**Outcome**
An adopter reading the skill meets figures and commands the tree supports. Today two bare `python tools/...` commands survive where a check exists to catch them and cannot see them; three documents disagree how many fields a slide has and the gate takes the larger side; the critique document states the hard-rule count twice, ten lines apart, and both are wrong; and the skill tells an adopter a deck is under 200 KB when no deck this repository ships is.

**Closes** `PR-08`, `PR-09`, `PR-10`, `PR-13` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: the four skill documents, `SKILL.md`, `BRIEF.md`'s *Delivery mode* row, and `check_scaffold.py`'s command check
- In: **nothing else** - every finding this task closes is named above, and each statement stays in the register rather than being restated here (the method's umbrella condition 2)
- Out: any finding not in the list above
- Out: committing to a remedy before measuring it. A remedy is a hypothesis (the method's section 5); a fix that the measurement refuses is reported here and its finding stays open

**Inputs**
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3 - the rows for `PR-08`, `PR-09`, `PR-10`, `PR-13`
- [`skills/htmldeck/SKILL.md`](../skills/htmldeck/SKILL.md)
- [T-231](T-231-two-packaging-checks-have-no-subject-at-all.md) - why the command check sees nothing today, which has to land first or this task's proof is vacuous

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
| 1 | `PR-08` — find why the check that exists for this class cannot see either instance, before writing a line | The mechanism, not the two edits |
| 2 | `PR-08` — widen the check to the places a command actually lives, seed both on the real tree, add fixtures | `check_scaffold.py`, and the two commands |
| 3 | `PR-09` — settle whether *seven* is a miscount or a stale subset, then remove the restated list | `pipeline.md` |
| 4 | `PR-10` — replace both counts with the sheet that holds them, then **test** whether declaring the four documents would have caught either | `critique.md`, and a verdict on the durable half |
| 5 | `PR-13` — restate both as dated measurements of named artifacts, the form `CLAUDE.md` already uses | `SKILL.md`, `BRIEF.md`'s *Delivery mode* row |
| 6 | `check_scaffold.py`, `figures.py`, `refcheck.py`, `lint.py` | Green, figures before the gate |

## 3. Implement

**Decisions & assumptions**

- **`PR-08`: the register names one of two mechanisms, and fixing only it leaves both instances
  unseen.** The two bare commands hide for different reasons. `artifacts.md`'s `presenter.py` sits
  **inside a fenced template**, where check 7 does look — but written as an inline span, so the line
  begins with a backtick and the pattern's `^\s*python` anchor never reaches it. `build.md`'s
  `figgrid.py` sits in **ordinary prose, in no fence at all**, where check 7 never looked, and
  `check_paths`'s bare-path rule cannot see it either because that rule needs the backtick followed
  by the path rather than by `python`. Only the second is the mechanism the row states. A comment in
  the tool carried the false premise in as many words — *a command line the skill tells a build to
  run lives only inside fences* — and it is now corrected rather than left as folklore.
- **So the check is keyed the way the row's own hypothesis proposes**, on a command naming a
  repository tool without a base, and its subject is widened to where commands live: `command_units`
  yields fenced blocks **and** the inline spans of the prose outside them, which partition the file.
  The anchor accepts a line start **or** a backtick, and a command now ends at the closing backtick
  rather than at the end of the line — without that, the flag check would read the sentence after a
  span as arguments.
- **Seeded on the real tree, which is the proof a fixture cannot give.** Before the change the gate
  read **23 of 23** documented commands and printed `OK`; after it, **27 of 29**, naming both bare
  commands. Widening found six commands the check had never counted, two of them defective. With
  the two commands based, **29 of 29** and green. Three fixtures added — a span inside a fence, a
  span in prose, and the direction that must not fire, a **based** command in prose read normally —
  taking the self-test from 23 to 26.
- **`PR-09`: the hypothesis holds, and the fix is to stop restating the list.** *Seven* is a stale
  subset rather than a miscount: the template carries nine fields and an optional tenth, and the two
  missing are `Archetype` and `Sources` — and `Sources` is the one `spec.py`'s `SPEC-1` gates on
  every slide. `pipeline.md` now names the template as the list's home, two lines below where it
  already pointed at it, so there is no second copy to drift.
- **`PR-10`: the cheap half taken, the durable half refused by measurement.** Both counts are gone —
  the worksheet carries them, and it is 29 rather than the 25 and 26 the page stated ten lines apart.
  The row's durable half asks for the four unwatched skill documents to be declared in `figures.py`'s
  `DECLARED_DOCS`. **Tested rather than assumed**: with all four declared and `25` seeded back into
  `critique.md`, `figures.py` reports **0 stale figures**. `DECLARED_DOCS` holds a document to a
  **part-of-whole coverage claim**, and these are plain counts naming no field, so the declaration
  would have watched nothing — 56 more numerals seen, **0 more compared** — while printing four more
  documents as covered. That is a vacuous pass of exactly the shape `T-231` was, so it is not made.
  The class the row names is real and stays open; what is refused is the mechanism proposed for it.
- **`PR-13`: a wrong number under a right decision, and the row says so.** `SKILL.md`'s *under
  200 KB* and `BRIEF.md`'s *~190 KB typical* are both restated as dated measurements of named
  artifacts, which is the form [`../CLAUDE.md`](../CLAUDE.md) rule 1 already uses and the reason that
  sentence is still true. The four shipped decks measured **316 to 427 KB on 2026-08-30**. The
  *Delivery mode* decision rests on *embedding is cheap* and survives untouched.
- **The register's own figures for `PR-13` had drifted before this task read them** — it records
  314,405 / 312,384 / 426,655 / 397,867, and `B12` and `B13` rebuilt three of the four since. The
  finding is right and its evidence decayed inside one release, which is the finding's own argument
  arriving a second time.
- **And a third time, inside this batch.** `T-227` corrected the front page's fixture count to
  *sixteen broken and seven good*; step 2 above added three fixtures, so the same sentence was wrong
  again four commits later and now reads eighteen and eight. A pasted count is a liability whoever
  writes it.

**Outputs produced**

- [`tools/plugin/check_scaffold.py`](../tools/plugin/check_scaffold.py) — `command_units`, the two
  patterns, the corrected premise, and three fixtures
- [`skills/htmldeck/references/artifacts.md`](../skills/htmldeck/references/artifacts.md) and
  [`skills/htmldeck/references/build.md`](../skills/htmldeck/references/build.md) — the two commands
- [`skills/htmldeck/references/pipeline.md`](../skills/htmldeck/references/pipeline.md) — the field
  list, replaced by its home
- [`skills/htmldeck/references/critique.md`](../skills/htmldeck/references/critique.md) — both counts
- [`skills/htmldeck/SKILL.md`](../skills/htmldeck/SKILL.md) and
  [`docs/BRIEF.md`](../docs/BRIEF.md) — the size claims
- [`README.md`](../README.md) — the pasted gate output and the fixture count, both moved by step 2

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every finding closed with its remedy measured, or deferred with the reason recorded | pass | `PR-08`, `PR-09`, `PR-13` closed with the remedy measured. `PR-10` closed on the figures; **its durable half refused on a seeded test** and the reason is on the row |
| Each register row's `Task` cell names this task and its `Status` cell says what happened | pass | Four rows updated |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | pass | Lint's four checks pass. Scaffold 26 of 26 fixtures, 50 paths, 29 of 29 commands, body 7,005 of 8,192; `figures.py` 0 stale; `refcheck.py` 4,976 pointers 0 broken |

**No look is owed.** This task changed six markdown documents and one checker, and no deck.

**Child fix tasks raised**
- none. `PR-10`'s class stays open on its own row with the measurement that refuses the proposed
  mechanism; nothing here is blocked on it.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-30 | → done | Four findings closed. `PR-08`'s stated mechanism is **one of two** — one command hid inside a fence behind a line anchor, the other in prose where the command check never looked — and the widened check took the gate's subject from 23 documented commands to 29, seeded on the real tree before any fixture was written. `PR-10`'s durable half is **refused**: declaring the four documents and seeding the wrong count back leaves `figures.py` green, because `DECLARED_DOCS` holds part-of-whole claims and these are plain counts |
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`Med`**, grouped: the owner ruled on 2026-08-29 that a severity obliges a disposition before the release rather than a file count, on the precedent that the method already accepts many findings to one task at `Low`. Every finding keeps its id and its statement in the register. |
