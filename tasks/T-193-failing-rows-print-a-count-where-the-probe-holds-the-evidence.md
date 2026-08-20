---
id: T-193
title: A failing row prints a count where the probe already holds the evidence that names the fault
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-066]
work_package: PH3
shipped_in: unreleased
owner: the project owner
business_value: high
effort: s
created: 2026-08-20
updated: 2026-08-20
deliverables: []
---

# T-193 - A failing row prints a count where the probe already holds the evidence that names the fault

## 1. Specify

**Outcome**
A failing verdict row names what failed. Today several print how many, and the author has to read
the checker's source to find out which.

**Two instances, both in [`../tools/deck/audit.py`](../tools/deck/audit.py)**

- Line 2114, DS-113: `"sprite icons never used: %d of %d" % (len(data["unusedSymbols"]), ...)`. The
  **ids are in `unusedSymbols`** and only the length is printed. An author is told two icons are
  dead and not which two.
- Line 2093, DS-075: the browser-side probe filters `#docBody *` for elements wider than 321 px and
  keeps `.length`. The elements are discarded inside the probe, so the row *cannot* name the wide
  one however the message is written. `reflow scrollWidth at 320 CSS px: 859 (overflowing: 1)` is
  everything the author gets about a rule that is hard to satisfy.

**What it costs.** The adopter build of 2026-08-19 hit DS-075 twice and DS-113 twice, and spent
**seven tool calls reading `audit.py` and `render.py` source** to work out what the messages meant.
That is the whole diagnosis cost this task removes, and it recurs for every adopter, because reading
the checker's source is not something an adopter should ever be doing.

**Scope**
- In: DS-113 and DS-075 first, since both are measured failures on a real deck.
- In: a sweep of every row whose message is a bare count, asking in each case whether the probe still
  holds the subject at the point the row is written.
- In: a bound on how much a row may name - a row listing forty elements is a different failure.
  My proposal is three, then `and N more`.
- Out: rules whose subject genuinely is a count, `DS-092`'s sentence lengths among them.

**Acceptance criteria**
- [ ] DS-113 names the dead symbol ids.
- [ ] DS-075 names the widest offending element, or states plainly that it cannot and why.
- [ ] The sweep is recorded with its result, including the rows it decided to leave alone.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Name the evidence in DS-113 and DS-075 | `_naming`, `_widest` |
| 2 | Keep the wide elements inside the DS-075 probe | `at320Widest` |
| 3 | Sweep every count-only row | ten more rows widened |

## 3. Implement

**Decisions & assumptions**
- **Bounded at three, then `and N more`** - a row listing forty elements is a different failure of the same kind.
- **`_name_of` handles a string, a pair and a dict**, because the probe emits all three and a row should not have to know which.
- **Left alone: `DS-219`'s mark pairs and `DS-092`'s counts of counts** - the first holds objects whose identifying part is a colour pair rather than a name, the second is a row whose subject genuinely is a count. Both recorded here rather than silently skipped.
- **The absent-subject fixture caught the omission**: `at320Widest` was in neither `ALWAYS_MEASURED` nor `CONDITIONALLY_MEASURED`, and the run refused to start.

**Outputs produced**
- `tools/deck/audit.py`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| DS-113 names the dead symbol ids | **pass** | seeded two unused symbols: `sprite icons never used: 2 of 13 - i-decoy-one, i-decoy-two` |
| DS-075 names the widest offending element | **pass** | seeded a 900 px div: `reflow scrollWidth at 320 CSS px: 920 (overflowing: 1) - widest: div.wide-decoy 900px` |
| The sweep is recorded, including what was left alone | **pass** | ten rows widened, two named above with the reason |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-20 | -> proposed | Created. |
| 2026-08-20 | -> in_progress | Two rows, then the sweep. |
| 2026-08-20 | -> done | Three criteria met. |
