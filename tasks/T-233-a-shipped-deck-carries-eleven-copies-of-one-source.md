---
id: T-233
title: Remove the ten dead quick-view payloads, and fix the verb that writes them
type: fix
status: done
phase: review
parent: T-219
blocked_by: []
related: []
work_package: PH1
owner: the project owner
business_value: critical
effort: s
created: 2026-08-29
updated: 2026-08-30
shipped_in: 0.7.0
deliverables: [examples/portfolio-review/portfolio-review.html, tools/deck/quickview.py]
---

# T-233 — Remove the ten dead quick-view payloads, and fix the verb that writes them

## 1. Specify

**Outcome**
A deck carries one copy of each source it quotes, and the verb that repairs a drifted quick view writes the copy the deck reads. Today `portfolio-review.html` carries 12 templates and 2 distinct payloads - `Portfolio model` eleven times at 8,451 bytes each, **84,510 bytes and 21.3% of the deck** - and `deck.js` keys on `data-qv` so the last wins and ten are dead. `rewire()` substitutes with `count=1`, so the repair writes the copy nobody reads.

**Closes** `PR-83` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: the ten copies, which are byte-identical to the eleventh so removing them is a deletion
- In: **which of the three sites is the defect** - the register's hypothesis names `wire()`, `rewire()`'s `count=1` and the gate's dedupe, and says each is right on a deck with one copy per source and wrong on this one
- Out: the quick view's design, which is correct and is what the docstrings state

**Inputs**
- `PR-83` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3
- [`tools/deck/quickview.py`](../tools/deck/quickview.py) - `wire()` and `rewire()`
- [`shell/deck.js`](../shell/deck.js) - the `qvSrc` lookup

**Acceptance criteria**
- [ ] the deck carries one template per distinct payload, and its byte count is stated before and after
- [ ] `rewire()` repairs the copy the deck actually reads, proved by drifting one and repairing it
- [ ] the quick view **opened and looked at** on the rebuilt deck, per `CLAUDE.md` rule 6

**Open questions**
- None yet. The register's `Remedy` column carries a hypothesis for each finding, and the method's
  section 5 says it is a hypothesis: whoever implements this measures before committing to it, and
  records what the measurement said.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Prove the ten copies are byte-identical before deleting anything, so the removal is a deletion rather than a choice | one distinct body across eleven templates |
| 2 | Read each of the three candidate sites against what it is for, rather than against the deck | `wire()` and `deck.js` cleared; the deck and `rewire()` named |
| 3 | Remove the copies, keeping the first — which is what `wire` writes and what `wired_pattern` finds | the deck's byte count, before and after |
| 4 | Make `rewire` reach the copy the deck renders, and prove it by drifting one on **both** deck shapes | the repair run against the current deck and against `HEAD`'s eleven-copy one |
| 5 | Answer the row's last question — should `check` fail on a repeated `data-qv`? | the duplicate named and the check failing |

## 3. Implement

**Decisions & assumptions**
- **`wire()` is not the defect** — 2026-08-30. Its `first[0]` guard emits the control on every mark
  and the `<template>` on the first, which is exactly what its docstring claims and what its own
  self-test asserts. Read rather than assumed.
- **`deck.js` is not the defect** — 2026-08-30. Keying `qvSrc` by `data-qv` implements the stated
  contract; on a deck with one template per source, last-wins and first-wins are the same template.
- **The deck is the defect, and so is `rewire()`'s `count=1`** — 2026-08-30. `count=1` is *correct*
  on a conformant deck and wrong on this one, because it repaired the **first** template while
  `deck.js` renders the **last**. `rewire` now substitutes every copy, returns how many, and
  `refresh` prints a line when it repaired more than one — a verb that quietly fixed eleven copies
  would hide the finding that produced it.
- **The first copy is the one kept** — 2026-08-30. All eleven bodies hash the same, so the choice is
  free today; the first is what `wire` would have written and what `wired_pattern` finds, so keeping
  it makes the deck what the tool would produce.
- **A fourth site the register did not name** — 2026-08-30, and it was found by seeding rather than
  by reading. `check`'s drift comparison reads `wired_pattern(title).search(html)` — the **first**
  template. Drifting the copy `deck.js` actually renders and running `check` on `HEAD`'s deck
  reported `match` and exited 0: **the drift detection T-181 shipped was defeated in a second way**,
  independent of `rewire`. So the row's open question is answered **yes** — `check` now names a
  repeated `data-qv` and **fails** on it, which is the one rule that catches every part of this.

- **A fifth site, and it was three gates deep** — 2026-08-30. Removing the payloads turned
  `spec.py`'s `SPEC-5` **red on two ledger rows**, and the cause is the same one: a quick view's
  `<template>` sits **inside its slide's own `<section>`**, and `SPEC-5` searched that section's
  text for the ledger's value. The payload is the *source document*, so a figure the source states
  and the slide never prints read as *shown*. **Isolated to one variable**: with `HEAD`'s deck and
  nothing changed but the deduplication, `SPEC-5` fails on exactly the two rows the batch's gate
  named. A `<template>` is markup nobody sees, so `slide_text` now strips it.
- **And the first form of that strip was wrong, which is worth more than the fix** — 2026-08-30.
  `<template\b.*?</template>` looks obviously right and is not: this deck holds **eight** `<template`
  openings against **two** closings, six of them the quick-view contract quoted in the shell's own
  prose. The pattern ran from one of those to the first real closing tag, swallowed slide 1's
  `<section>` opening, and `SPEC-5` reported *slide 1 does not exist* about a deck that has one — a
  checker made **more** blind by a fix meant to sharpen it. It now matches the exact form
  `quickview.py` writes, and the self-test seeds an unclosed prose mention ahead of a slide.
- **What the newly-sighted rule then found is a real defect in a shipped deck** — 2026-08-30, and it
  is [T-282](T-282-the-opening-slide-carries-one-of-the-two-figures-its-specification-names.md).
  `65%` appears **nowhere a reader can see** in `portfolio-review.html`, while the slides
  specification, the foundation's opening paragraph and the source all call it half the deck's
  argument. B12 corrected the ledger to what the deck does show and recorded the deviation beside
  slide 1; building the missing figure is a title-slide composition change and wants an eye, which
  §4 forbids an unattended session.

**Outputs produced**
- [`examples/portfolio-review/portfolio-review.html`](../examples/portfolio-review/portfolio-review.html)
  — ten templates removed
- [`tools/deck/quickview.py`](../tools/deck/quickview.py) — `rewire` over every copy, `refresh`'s
  report, `check`'s duplicate row and its failure, and a self-test fixture built by duplicating what
  `wire` emits
- [`tools/deck/spec.py`](../tools/deck/spec.py) — `INERT`, `slide_text`'s strip, and two self-test
  cases: a value carried only by a template, and a prose mention that must not swallow a slide
- [`tools/deck/static_variants.py`](../tools/deck/static_variants.py),
  [`tools/deck/content_variants.py`](../tools/deck/content_variants.py) — re-anchored on the claim
  line `T-248` corrected, seeded breaks unchanged

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The deck carries one template per distinct payload, and its byte count is stated before and after | pass | **407,546 → 322,796 bytes, −84,750, −20.8%.** Twelve controls kept, two templates left, and `check` went from `compared 2 of 12 carried` to `compared 2 of 2` |
| `rewire()` repairs the copy the deck actually reads, proved by drifting one and repairing it | pass | Run on **both** shapes. On the current deck: drift seen, repaired, re-check clean. On `HEAD`'s eleven-copy deck: `11 templates carried this title - all 11 replaced`, no stale copy left — and `check` did **not** see that drift beforehand, which is the fourth site above |
| The quick view **opened and looked at** on the rebuilt deck, per `CLAUDE.md` rule 6 | pass | **The owner looked, 2026-08-30**, and confirmed the same document displays from more than one page — which is the property eleven copies were paying for and one template now provides. [`docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md) row 6 |

**Child fix tasks raised**
- [T-282](T-282-the-opening-slide-carries-one-of-the-two-figures-its-specification-names.md) — the
  figure the newly-sighted `SPEC-5` found missing from the opening slide

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`High`**: the method's section 4 gives that level one obligation beyond a child task — *the release does not go out while it is open*. |
| 2026-08-30 | proposed → done | Closed in **B12**. The register's three candidate sites were read against what each is for: `wire()` and `deck.js` are correct, the deck and `rewire()`'s `count=1` are not. **A fourth site was found by seeding** — `check`'s own comparison read the first template too, so a drift in the rendered copy reported `match`. `check` now fails a repeated `data-qv`, which is the one rule the row hoped for. **A fifth site turned up while the batch's gate ran**: `spec.py`'s `SPEC-5` was reading the dead payloads too, because a quick view sits inside its slide's own section — and the newly-sighted rule found a figure the specification calls half the deck's argument missing from the opening slide, which is [T-282](T-282-the-opening-slide-carries-one-of-the-two-figures-its-specification-names.md). `PR-83` closed; one look owed. |
| 2026-08-30 | (no change) | **The owed look came back the same day and it passed.** The owner opened the quick view from more than one slide: the same document displays on multiple pages. That is the whole of what the ten dead copies were buying, and it is now bought by one template and `data-qv`. |
