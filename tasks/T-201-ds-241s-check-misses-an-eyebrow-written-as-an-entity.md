---
id: T-201
title: DS-241's check misses an eyebrow whose separator is written as an entity
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-197]
work_package: PH1
shipped_in: 0.5.1
owner: the project owner
business_value: high
effort: xs
created: 2026-08-20
updated: 2026-08-20
deliverables: []
---

# T-201 - DS-241's check misses an eyebrow whose separator is written as an entity

## 1. Specify

**Outcome**
DS-241 catches `07 &middot; Structure`, which is how a build actually writes the defect it was
written for. Today it catches only the decoded form.

**The defect, found the day `0.5.0` shipped**
`audit._flat` reads an eyebrow through `content.runs()`, which decodes `&nbsp;` and `&amp;` and
nothing else. So `07 &middot; Structure` arrives as that literal string, and
`STARTS_WITH_POSITION` - a digit followed by a separator - sees a digit followed by an **ampersand**
and passes it.

**The deck the rule was written from is written that way.** Running `0.5.0`'s gate against it
reported `eyebrows ... : 0` on a deck where **all fifteen** eyebrows were the defect. The three
decks in this repository are clean because they were re-cut by hand, not because the check saw
anything.

**How it was found: by looking, after the gate had already said the deck was clean** - rendering
slide 8 and reading the top strip (`CLAUDE.md` rule 6). No instrument here would have found it.

**This is the fourth check in one day that found nothing on its first run**, after two in T-198 and
one in T-190. Three were caught by seeding the defect before believing the green; this one was not
seeded, which is the whole difference.

**Scope**
- In: decoding HTML entities before DS-241 reads an eyebrow.
- In: **both** forms seeded into `static_variants.py`, since a rule catching only the decoded one
  catches only decks nobody built.
- Out: `content.runs()`'s own entity handling. It affects figure harvesting and is a wider change
  than this defect justifies on a patch.

**Acceptance criteria**
- [ ] The entity form is caught, and the decoded form still is.
- [ ] Both are seeded in the variants suite and watched failing.
- [ ] The deck that exposed it reports its real count.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Decode entities in `audit._flat` | one call |
| 2 | Seed both forms | `static_variants.py` |
| 3 | Re-run against the deck that exposed it | its real count |

## 3. Implement

**Decisions & assumptions**
- **Decoded in `_flat`, not in `runs()`** - 2026-08-20. `_flat` exists only for this rule, so the
  change is scoped to it. `runs()` feeds the figure ledger, and widening its entity handling on a
  patch release would move a measurement nobody asked to move.
- **Both forms seeded, not one.** The decoded form is what a person types and the entity form is
  what a build writes; a suite holding only the first is the suite that let this through.

**Outputs produced**
- `tools/deck/audit.py`
- `tools/deck/static_variants.py`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The entity form is caught, and the decoded form still is | **pass** | `27 of 27 static variants caught`, the two new ones among them |
| Both are seeded and watched failing | **pass** | `eyebrow-that-repeats-the-position-and-stage` and `...-decoded`, both CAUGHT |
| The deck that exposed it reports its real count | **pass** | `15 - AI runs. Governance does not., ... and 12 more`, against `0` before |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-20 | -> proposed | Created. |
| 2026-08-20 | -> in_progress | One call, and two variants. |
| 2026-08-20 | -> done | Three criteria met. |
