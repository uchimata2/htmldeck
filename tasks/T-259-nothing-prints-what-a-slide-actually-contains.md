---
id: T-259
title: Ship a per-slide fact printer, so a specification and its deck stop drifting silently
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
shipped_in: unreleased
deliverables:
  - tools/deck/slidefacts.py
---

# T-259 — Ship a per-slide fact printer, so a specification and its deck stop drifting silently

## 1. Specify

**Outcome**
A reader can ask what a slide actually contains. Today a deck is built from a specification pair and then edited in place — the supported way to work — and from that moment the specification is a claim about the deck that nothing checks. The adopter swept theirs: **twenty-three of twenty-five entries had drifted**, and `check` was green throughout.

**From the adopter report** [`026`](../docs/adopter-reports/claimai/026-nothing-prints-what-a-slide-actually-contains.md).

**Scope**
- In: the printer: one slide's own answer for every field an entry claims — eyebrow, headline, standfirst, bottom line, drawn labels, body copy, controls, motion classes, quick views and sources. `render.py` already parses the deck for `measure` and `motion`
- In: **making no judgement**, which is what made the adopter's ~250-line version usable: a differ would produce noise on every intentional difference and there are many
- In: **saying in the docs that in-place editing forks the specification.** The workflow is supported and the consequence is not written down
- Out: anything the records above do not name. The report is a closed one-way hand-over — there is no
  channel back and none is expected, so a question this task cannot answer is settled here rather
  than asked.

**Inputs**
- the record above, [`026`](../docs/adopter-reports/claimai/026-nothing-prints-what-a-slide-actually-contains.md) — each carries its evidence, its version and its own proposed fix
- a verdict is **out of scope here** and worth considering only once the printer exists and its shape is known — the record says so and it is right
- `tools/deck/spec.py`, which reads the specification and never holds it against the output

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

**The remedy was measured before it was adopted, and it did not survive intact.** Report 026's step 1
proposes reusing `render.py`'s parse. `render.py` reads the DOM out of a real Chrome; every field an
entry claims is in the static markup, so the browser buys nothing a printer needs and costs a launch
per invocation. Step 1 below is that measurement; steps 2 onward are what it decided.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | **Measure the remedy's mechanism before adopting it.** Extract slide 4 of [`../examples/sort-window/sort-window.html`](../examples/sort-window/sort-window.html) statically and hold it against that slide's entry in [`../examples/sort-window/sort-window.slides.md`](../examples/sort-window/sort-window.slides.md) | **Done, and it refused the browser.** All ten claimed field groups are reachable from the static markup — eyebrow, headline, standfirst, bottom line, drawn labels (`.lab`/`.val`/`.tick`), body copy, controls (`data-disc`), motion classes, quick views (`data-qv`/`data-file`) and sources (`.sources-item`). It also found the trap: **59% of that section is `<template>` payload** — 9,826 bytes raw against 4,056 with templates removed — so a printer that does not exclude it prints the quick views' source documents as the slide's own copy |
| 2 | Write `tools/deck/slidefacts.py` — one slide's own answer for every field an entry claims, standard library (**L-07**), **and no verdict**, which is what made the adopter's version usable. Motion classes read from the deck's own `--motion-kind` declarations through [`../tools/deck/density.py`](../tools/deck/density.py) rather than a copied list; slide sections located by the deck's declared numbers, the way [`../tools/deck/spec.py`](../tools/deck/spec.py) locates them; `<template>` content excluded per step 1 | The printer |
| 3 | Prove it in **both directions** (**L-125**): seed a field into a slide and watch the printed line carry it, remove one and watch the line say the slide does not | `self_test()`, run on every invocation |
| 4 | Wire it into [`../tools/check_all.py`](../tools/check_all.py)'s `WIDE` as a self-test — the precedent is `tools/examples/portfolio_charts.py selftest`. **A tracked tool no table names is `unclassified` and fails the run**, so this is not optional | One `WIDE` row |
| 5 | **Say that in-place editing forks the specification**, in [`../skills/htmldeck/references/build.md`](../skills/htmldeck/references/build.md) §4 — which already tells a build to write a deviation back, and is silent on the edit made after the build that never becomes one. Point it at the printer | The consequence written down where the workflow that causes it lives |
| 6 | Close [`026`](../docs/adopter-reports/claimai/026-nothing-prints-what-a-slide-actually-contains.md) with its remedy measured, and record here that its step 2 — a verdict — stays out of scope, which the record itself argues for | The closed record |

## 3. Implement

**Decisions & assumptions**
- **The printer is a static read, not `render.py`'s parse — 2026-08-30.** The record's remedy names
  that parse; it is a Chrome DOM read. Every claimed field is in the static markup, so a browser
  buys nothing and costs a launch per invocation. Standard library (**L-07**).
- **`<template>` content is cut before any field is read — 2026-08-30.** A quick view's source
  document ships inside the slide that cites it. Measured on slide 4 of
  [`../examples/sort-window/sort-window.html`](../examples/sort-window/sort-window.html): **9,826
  bytes raw against 4,056 with templates removed**, so 59% of that section belongs to another
  document. This was found by the step-1 measurement and would not have been visible from a DOM
  read, where the payload is inert. Generalised as [L-149](../docs/lessons/L-149.md).
- **Body copy and drawn labels partition the slide's text — 2026-08-30.** They overlapped on first
  run: a figure sits inside a `.body figwrap` wrapper, so slide 4's eleven chart labels printed
  twice, once as prose. Body copy is now read with the SVG removed. A reader holding the entry's
  `Text.` line against the deck was otherwise reading axis ticks as a paragraph.
- **The motion vocabulary is read from the deck, never listed in the tool — 2026-08-30.** Through
  [`../tools/deck/density.py`](../tools/deck/density.py)'s `motion_rules` and `ranked_classes`, the
  same `--motion-kind` idiom `DS-239` uses. A copied list is a second home and goes stale the first
  time a theme adds a class.
- **A verdict is still out of scope — 2026-08-30.** Report `026`'s step 2 says to consider one
  *once the printer exists and its shape is known*, and that is the right order. The shape is now
  known and the question is a later task's, not this one's.

**Outputs produced**
- [`../tools/deck/slidefacts.py`](../tools/deck/slidefacts.py) — the printer, new
- [`../tools/check_all.py`](../tools/check_all.py) — one `WIDE` row, `slidefacts.py --self-test`
- [`../skills/htmldeck/references/build.md`](../skills/htmldeck/references/build.md) §4 — the
  consequence of in-place editing, beside the deviation obligation for the build-time half
- [`../docs/adopter-reports/claimai/026-nothing-prints-what-a-slide-actually-contains.md`](../docs/adopter-reports/claimai/026-nothing-prints-what-a-slide-actually-contains.md)
  — closed, with what was taken and what was refused
- [`../docs/lessons/L-149.md`](../docs/lessons/L-149.md) — the generic half of the `<template>`
  finding, and the index regenerated

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every record closed with its remedy measured, or deferred with the reason recorded | **met** | `026` closed. Its step 1's *mechanism* refused on a measurement, its step 3 taken, its step 2 deferred on the record's own argument and the reason recorded in §3 |
| Each fix proved by seeding the defect and watching the check fire, in both directions | **met** | `self_test()` runs on every invocation and asserts both: a field the slide carries is printed and attributed to the right field, and a field removed from the fixture prints the *carries none* line rather than going quiet. It also asserts the two traps — no field answered by a `<template>` payload, and no drawn label printed as body copy — and that slide 2's headline cannot answer for slide 1 |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | **met** | Run in that order, never concurrently ([`TOOLING.md`](TOOLING.md)) |

**Child fix tasks raised**
- none. Report `026`'s step 2 — a verdict over the printed facts — is a candidate for a later task
  now that the printer's shape is settled, and is deliberately not raised here: the record asks for
  it to be *considered*, and considering it is not this task's scope.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → proposed | Raised by [T-225](T-225-triage-the-claimai-adopter-report.md), the triage of the ClaimAI adopter report. **`PH3`**: not a defect in the published plugin's behaviour, so `CLAUDE.md`'s rule puts it in the main line rather than reopening a shipped phase. |
| 2026-08-30 | → planned | B14's first task, per [`../docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) §2 — the fact printer before the readability printer, because a later verdict would rest on it. §1's specify section needed nothing added, so the two steps were taken in one edit. |
| 2026-08-30 | (no status change) | **The remedy's mechanism was refused before implementing it**, per the standing rule that a `Remedy` is a hypothesis: report 026 proposes reusing `render.py`'s parse, which is a Chrome DOM read, and the static markup answers every claimed field. §2 step 1 carries the measurement and the `<template>` finding it turned up. |
| 2026-08-30 | → done | The printer ships, `026` is closed, and `build.md` §4 now says what in-place editing costs. **No look is owed**: nothing here renders — no deck changed, and the output is text. The `<template>` trap became [L-149](../docs/lessons/L-149.md) rather than staying in this record, because it is a property of reading any container and the next rule that searches a slide will meet it too. |
