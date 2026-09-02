---
id: T-258
title: Report a readability measurement over drawn slide copy, and name the hardest lines
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-225]
work_package: PH3
owner: the project owner
business_value: high
effort: m
created: 2026-08-29
updated: 2026-08-30
shipped_in: 0.7.0
deliverables:
  - tools/deck/readability.py
---

# T-258 — Report a readability measurement over drawn slide copy, and name the hardest lines

## 1. Specify

**Outcome**
An author learns from the gate that copy is hard to read. Today the two rules over copy measure **length** (`DS-092`) and a **banned list** (`DS-106`), both were green on a deck its own author called difficult, and the difficulty was vocabulary, noun stacks and abstraction. Measured afterwards with an instrument the adopter had to write: Flesch 64.6, Fog 10.3, **18% three-syllable words and 129 nominalisations** — and no rule looks at either.

**From the adopter report** [`025`](../docs/adopter-reports/claimai/025-the-gate-passes-copy-its-own-reader-calls-difficult.md).

**Scope**
- In: a readability verdict over drawn slide copy — Flesch, Fog and a three-syllable share, standard library, reading the deck's own text nodes
- In: **reporting rather than gating.** A threshold on prose invites writing to the threshold, and the adopter's own record is that the numbers *located* the hard lines and did not judge them
- In: **saying what a green copy run means.** The gate already says a clean run is never *reads as human-written*; it should say the same about *reads easily*
- Out: anything the records above do not name. The report is a closed one-way hand-over — there is no
  channel back and none is expected, so a question this task cannot answer is settled here rather
  than asked.

**Inputs**
- the record above, [`025`](../docs/adopter-reports/claimai/025-the-gate-passes-copy-its-own-reader-calls-difficult.md) — each carries its evidence, its version and its own proposed fix
- the record's second half — six AI tells `DS-106` does not gate (rule-of-three cadence, negative parallelism, superficial `-ing` analyses, vague attribution, em-dash overuse, reflex bullet lists), read by hand once. **That half is [T-229](T-229-ds-106s-check-omits-a-word-the-rule-names.md)'s**, which already proposes deriving the fallback list from the rule's own row
- `DS-107`, which is where a category nobody has built yet is recorded

**Acceptance criteria**
- [x] every record named above is **closed with its remedy measured**, or explicitly deferred with the
      reason recorded in this task
- [x] each fix is proved by seeding the defect and watching the check fire, in both directions where
      the record's own evidence is a verdict (**L-125**)
- [x] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None yet. Every record carries its own evidence and its own proposed fix; the proposal is a
  hypothesis and whoever implements it measures before committing to it.

## 2. Plan

**The remedy's own note is the design, and a measurement confirmed it.** Report `025` says the
numbers *located* the hard lines and did not judge them — its author scored Flesch 64.6, which reads
as plain English, on copy their reader called difficult. So the deliverable is **a ranking of the
hardest lines**, with the aggregate as context rather than as the answer. An aggregate that agrees
with a reader who found the deck hard would still not say *which sentence*.

**And the subject had to be decided by measurement, because the two candidates disagree.** Report
`025` says *the deck's own text nodes*; §1's outcome says *drawn slide copy*. Scored both ways on
the four tracked decks:

| Deck | Every text node | Contracted prose |
| :--- | :--- | :--- |
| `sort-window` | Flesch 66.8, Fog 10.0, 8.7% | Flesch 69.0, Fog 10.4, 7.7% |
| `measure-first` | Flesch 56.5, Fog 11.4, 15.6% | Flesch 64.6, Fog 10.4, 13.1% |
| `portfolio-review` | Flesch 50.3, Fog 12.7, 18.9% | Flesch 57.1, Fog 11.6, 14.4% |
| `reference-deck` | Flesch 55.6, Fog 12.5, 16.0% | Flesch 57.2, Fog 13.1, 16.7% |

**Eight Flesch points separate the two readings of `measure-first`**, which is a reading-grade
apart, so this is not a rounding choice. Every text node scores harder on three decks and easier on
the fourth, so the difference is not even a constant offset to correct for: an axis tick and a
legend key are terse noun phrases with no verb and no sentence end, and scoring them measures label
style rather than reading. **Contracted prose is the subject**, and the words left out are counted
and named rather than dropped in silence (**L-149**).

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | **Score both candidate subjects on all four tracked decks before choosing one** | **Done** — the table above. It decided the subject and refused the record's own wording |
| 2 | Write `tools/deck/readability.py` — Flesch, Flesch–Kincaid, Fog and a three-syllable share over the deck's contracted prose, **and the hardest lines named, ranked**. Standard library (**L-07**). The subject reuses an existing extractor rather than adding a second one (**L-08**) | The reporter. *Planned against [`../tools/deck/audit.py`](../tools/deck/audit.py)'s `copy_of`, which is what `DS-106` reads; built on [`../tools/deck/slidefacts.py`](../tools/deck/slidefacts.py)'s `facts` instead, because naming the hardest **lines** needs the slide and field each line came from and `copy_of` returns one string. `facts` is a subset of `copy_of`'s subject — it reads inside slide sections with `<template>` already cut — so the reuse argument holds and the attribution comes free* |
| 3 | **It reports and never gates.** A threshold on prose invites writing to the threshold, and this instrument cannot tell a hard sentence from a precise one. Exit 0 on any deck it can read | No verdict, stated in the tool |
| 4 | Prove it in **both directions** (**L-125**): a fixture of deliberately hard copy ranks above a fixture of plain copy on every measure, and the plain one is not reported as hard | `self_test()`, run on every invocation |
| 5 | **Say what a green copy run means**, where [`../tools/deck/check.py`](../tools/deck/check.py) already says `DS-106` is never *reads as human-written* — `DS-107`'s obligation, which binds whoever builds the check. Green over `DS-092` and `DS-106` is not *reads easily* either: one measures length and one a word list | The account extended, and pointed at the reporter |
| 6 | Wire it into [`../tools/check_all.py`](../tools/check_all.py)'s `WIDE` as a self-test — a tracked tool no table names is `unclassified` and fails the run | One `WIDE` row |
| 7 | Close [`025`](../docs/adopter-reports/claimai/025-the-gate-passes-copy-its-own-reader-calls-difficult.md), recording that its **second half is not this task's** — the six AI tells are [T-229](T-229-ds-106s-check-omits-a-word-the-rule-names.md)'s, which has already derived `DS-106`'s list from the rule's own row | The closed record |

## 3. Implement

**Decisions & assumptions**
- **The ranking is the output; the aggregate is context — 2026-08-30.** Report `025`'s own note
  settles it: its author measured Flesch 64.6 — plain English — on copy their reader called
  difficult. A number that agrees with nobody cannot be the deliverable.
- **The subject is contracted prose, decided by the §2 measurement — 2026-08-30.** The record asked
  for *the deck's own text nodes*; that reading and this one differ by 8 Flesch points on one deck
  and the sign is not constant. The excluded words are counted and named in the report itself, so
  nothing is dropped in silence (**L-149**).
- **Nominalisations are counted, though §1's scope lists only Flesch, Fog and a three-syllable
  share — 2026-08-30.** The record's evidence sentence is *18% three-syllable words and 129
  nominalisations is where the difficulty lived*, so the record does name them. The count is a
  suffix heuristic that over-counts — `moment`, `city` — and is reported as a rate to compare
  against rather than as a defect count, which the tool says where the list is.
- **It never gates, and every exit code is 0 — 2026-08-30.** A threshold on prose invites writing
  to the threshold, and this instrument cannot tell a hard sentence from a precise one.
- **Lines come from [`../tools/deck/slidefacts.py`](../tools/deck/slidefacts.py), not a second
  extractor — 2026-08-30.** *What text is on a slide* now has one implementation, so this tool
  inherits its two cuts — the `<template>` payload and the drawn-label partition — rather than
  re-deriving them (**L-08**, **L-149**).
- **Ranking by Fog and by the three-syllable share name the same lines — 2026-08-30.** Measured on
  `measure-first` and `portfolio-review`: the two orderings agree on the top three of each and
  differ only at rank four. Fog is kept, because it is the measure the record asked for and the
  alternative buys nothing.
- **`RANK_MIN_WORDS` is 8, and it is a calibration — 2026-08-30.** Below it, Fog is arithmetic over
  a single unterminated fragment and the list fills with two-word eyebrows. At 8 every entry on the
  four tracked decks is a sentence somebody wrote.

**A defect in `slidefacts.py` was found and fixed in place**, per
[`../docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) §4's *a small fix in place is made
in place*: its `unescape` was a six-entry table of *the entities a deck writes*, and
`examples/measure-first/measure-first.html`'s title slide carries `&middot;` and `&rsquo;`. Both
reached the printed output as literal text and were **counted as words** here — with the byline
ranked third-hardest in the deck on the strength of it. It now calls `html.unescape`, and the
fixture asserts both characters decode. *A hand-kept table of the ones we use is a second home for
a list the standard library owns* — the same shape as **L-08**.

**Outputs produced**
- [`../tools/deck/readability.py`](../tools/deck/readability.py) — the reporter, new
- [`../tools/deck/slidefacts.py`](../tools/deck/slidefacts.py) — `unescape` through the standard
  library, and a fixture line that proves it
- [`../tools/deck/check.py`](../tools/deck/check.py) — the closing account now says a clean copy run
  is not *reads easily*, and points at the reporter (`DS-107`'s obligation)
- [`../tools/check_all.py`](../tools/check_all.py) — one `WIDE` row, `readability.py --self-test`
- [`../docs/adopter-reports/claimai/025-the-gate-passes-copy-its-own-reader-calls-difficult.md`](../docs/adopter-reports/claimai/025-the-gate-passes-copy-its-own-reader-calls-difficult.md)
  — closed, with what was taken and what was refused

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every record closed with its remedy measured, or deferred with the reason recorded | **met** | `025` closed. All three of its changes taken; its *text nodes* subject refused on the §2 measurement and the replacement recorded. Its second half was already [T-229](T-229-ds-106s-check-omits-a-word-the-rule-names.md)'s and is `done` |
| Each fix proved by seeding the defect and watching the check fire, in both directions | **met** | `self_test()` runs on every invocation. Both directions: a deliberately hard fixture scores worse than a deliberately plain one on **all five** measures and lands in a different Flesch band, and the ranking names the hard line while never naming the plain one. It also asserts what must stay out — a line under `RANK_MIN_WORDS`, a drawn label — that the excluded words are counted rather than dropped, and that empty copy answers `None` rather than 0, since 0 would sort a prose-free deck as the easiest in the tree |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | **met** | Run in that order, never concurrently ([`TOOLING.md`](TOOLING.md)) |

**Child fix tasks raised**
- none. The `slidefacts.py` entity defect was a small fix in place and was made in place, per
  [`../docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) §4 — it changes one function in a
  tool shipped the same day and has no impact on other work.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → proposed | Raised by [T-225](T-225-triage-the-claimai-adopter-report.md), the triage of the ClaimAI adopter report. **`PH3`**: not a defect in the published plugin's behaviour, so `CLAUDE.md`'s rule puts it in the main line rather than reopening a shipped phase. |
| 2026-08-30 | → planned | B14's second task. **The subject was decided by measurement before anything was written**, and the measurement refused the record's own wording — §2 carries the table and the eight-Flesch-point gap that settled it. |
| 2026-08-30 | → done | The reporter ships and never gates; `025` is closed; `check.py`'s account now says a clean copy run is not *reads easily*. **No look is owed**: nothing renders, no deck changed, and the output is text. **One defect was found and fixed in place** — `slidefacts.py` decoded six entities and a tracked deck writes more, which put a byline third in the hardest-lines ranking. |
