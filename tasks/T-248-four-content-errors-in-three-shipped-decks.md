---
id: T-248
title: Correct four numbers a shipped deck asserts and its own source contradicts
type: fix
status: done
phase: review
parent: T-219
blocked_by: []
related: [T-281]
work_package: PH3
owner: the project owner
business_value: high
effort: m
created: 2026-08-29
updated: 2026-08-30
shipped_in: unreleased
deliverables: [examples/sources/cost-model.md, examples/portfolio-review/sources/portfolio-model.md, examples/measure-first/sources/D5-management-decision-matrix.md]
---

# T-248 — Correct four numbers a shipped deck asserts and its own source contradicts

## 1. Specify

**Outcome**
Every number a shipped deck states agrees with the source model beside it. Today the reference deck's claim slide spends $5.6M on a package its own ask prices at $4.1M; `sort-window` prints a sort finish its stated rate contradicts by two hours, and the tripwire that should have caught it does not; `portfolio-review` attributes a transmission asset's $29M to renewables **on the slide that is its concentration argument**; and the adopter deck's sanitisation left the source project's own names in the documents beside it.

**Closes** `PR-81`, `PR-84`, `PR-85`, `PR-86` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: the three source models, the slide copy quoting them, and the sanitisation pass on the adopter deck's documents
- In: **nothing else** - every finding this task closes is named above, and each statement stays in the register rather than being restated here (the method's umbrella condition 2)
- Out: any finding not in the list above
- Out: committing to a remedy before measuring it. A remedy is a hypothesis (the method's section 5); a fix that the measurement refuses is reported here and its finding stays open

**Inputs**
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3 - the rows for `PR-81`, `PR-84`, `PR-85`, `PR-86`
- `CLAUDE.md`'s publishing rule, which the adopter deck's remaining names are measured against
- **L-127** - a figure can be arithmetically right and relationally wrong

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
| 1 | For each finding, settle the question **in the source** before touching a slide — every row asks for this and two of them turn on it | one answer per finding, and the reason it beats the alternatives |
| 2 | Rewrite the source, then let the derived things be derived rather than edited | the decks' embedded quick views refreshed from the corrected sources |
| 3 | Where the deck states the same fact twice, count the statements before choosing which one is wrong | six of seven statements agreed on `PR-81`; one did not |
| 4 | Where no answer survives the deck's own evidence, say so with the arithmetic and stop | `PR-84` deferred to [T-281](T-281-the-sort-windows-capacity-story-cannot-hold-its-own-failure-table.md) |

## 3. Implement

**Three closed, one deferred — and the deferral is the one that needed the most measuring.**

**Decisions & assumptions**
- **`PR-81`: the $1.5M is committed at approval and drawn at the month-18 gate** — 2026-08-30, and
  decided by counting rather than by taste. The deck states it **seven** times; six already read
  *held*, *reserve*, or *held for the gate* — slides 1, 5, 9 (three times) and 12 — and only slide
  10's cost line read *forgone*. The source settles it outright: the grant *lapses if it is not
  committed*, so money forgone at the state cannot buy 16 stations eighteen months later. The wide
  half went into `cost-model.md` first, as the row requires: *leaves $1.5M of the grant uncommitted*
  became committed-and-drawn-later, and *What the city forgoes* now says what is actually forgone —
  **46 stations and eighteen months**, since $1.5M buys 16 at the vendor's per-station price against
  the 62 the bike-share proposal would have built at once. The narrow half is one line, and slide 1
  now says what slide 12 says.
- **`PR-85`: renewables is $102M** — 2026-08-30, the first of the row's three candidates. The
  source's own top-three table already calls Aldis *Transmission. The only one of the three outside
  renewables*, so the **label** was wrong and the parts were right; the third candidate, a lost
  fourth renewable asset, would invent data the document does not have. The three-asset total stays
  **$131M**, relabelled *the three largest revaluation lines* with an *of which renewables $102M*
  row under it, so the sum a reader checks on the slide still closes.
- **`PR-86`: `D-004` gets a home rather than a deletion** — 2026-08-30. The row is right that
  deleting the mark loses a citation that is load-bearing four times, so it is defined in
  `D5-management-decision-matrix.md` — the document whose subject is decisions — in a *Decisions
  referenced by mark* table. **Nothing was invented**: the definition is the sentence D3 and D4
  already state beside every mark. The five paths were mechanical; the *Generated with* line took the
  row's second option and says plainly that the diagrams were laid out elsewhere, because naming a
  tool an adopter has would be inventing one.
- **`PR-84` is deferred, and all three of the row's candidate answers were refused as number fixes**
  — 2026-08-30. The arithmetic is on the register row in full. In short: one line at 3,100/hr sorts
  at most **16,533** parcels before the 01:00 cut-off against a peak night of **27,600**, so a
  **12.4%** miss is unreachable at the stated capacity under any finish time; changing the parcel
  split does not help, because the second trunk cannot start until the first is done; and the failure
  table and the tripwire **pull opposite ways at every constant rate**. One arrangement was found
  that reproduces the deck's own working exactly — two lines until the evening shift ends, one
  through the night — and it costs the deck's headline, *One depot, one sorter line*. That is a
  content decision the copy cannot take for itself, so it goes to the owner as
  [T-281](T-281-the-sort-windows-capacity-story-cannot-hold-its-own-failure-table.md) and the
  register row stays open.
- **Every deck's embedded sources were refreshed rather than edited** — 2026-08-30. Three of the
  four sources this task changed are quoted inside a deck's quick view. Editing both copies is how
  they drift; `quickview.py refresh --write` makes the deck's copy a function of the source. The
  refresh also exercised `T-233`'s repaired `rewire` on a real deck.

**Outputs produced**
- [`examples/sources/cost-model.md`](../examples/sources/cost-model.md) and
  [`examples/reference-deck.html`](../examples/reference-deck.html) — `PR-81`
- [`examples/portfolio-review/sources/portfolio-model.md`](../examples/portfolio-review/sources/portfolio-model.md),
  the deck and its foundation — `PR-85`
- [`examples/measure-first/`](../examples/measure-first/) — the slides line, the foundation's source
  directory, both diagram YAML headers, and `D-004`'s definition in D5 — `PR-86`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every finding closed with its remedy **measured**, or explicitly deferred with the reason on its register row | pass | `PR-81`, `PR-85`, `PR-86` closed. `PR-84` deferred with the arithmetic that refused all three of its candidate answers, and carried by [T-281](T-281-the-sort-windows-capacity-story-cannot-hold-its-own-failure-table.md) |
| Each register row's `Task` cell names this task and its `Status` cell says what happened | pass | Three struck and written; `PR-84` left open, its `Task` cell repointed to `T-281`, which is what keeps the register and the board telling the same story |
| `lint.py` and `check_all.py` green, run separately | pass | Run separately, on the batch's tree |

**Child fix tasks raised**
- [T-281](T-281-the-sort-windows-capacity-story-cannot-hold-its-own-failure-table.md) — the
  sort-window deck's capacity story, which no number fix reaches

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`Med`**, grouped: the owner ruled on 2026-08-29 that a severity obliges a disposition before the release rather than a file count, on the precedent that the method already accepts many findings to one task at `Low`. Every finding keeps its id and its statement in the register. |
| 2026-08-30 | proposed → done | Closed in **B12**, three of four findings closed and `PR-84` deferred. `PR-81` and `PR-85` were both *which number is wrong* questions and both were settled by counting what the documents already say rather than by choosing: six of seven statements agreed on the $1.5M, and the source's own table already called Aldis transmission. `PR-86`'s judgement half kept the citation and gave it a home. `PR-84` refused all three candidate answers with the arithmetic — the deck's failure table and its tripwire cannot both hold at any constant sort rate — and became [T-281](T-281-the-sort-windows-capacity-story-cannot-hold-its-own-failure-table.md), because the settlement changes the deck's headline. |
| 2026-08-30 | (no change) | **Both owed looks came back the same day and both passed**, rows 7 and 8 of [`../docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md). The reference deck's longer claim line and its rewritten slide-10 cost read as intended, and slide 6 still reads as a concentration argument at $102M of $172M with a disclosure heading that names no figure. Neither was checkable by anything here: they are D1 Spine and D4 Consistency, which is why the register's own rows for them say so. |
