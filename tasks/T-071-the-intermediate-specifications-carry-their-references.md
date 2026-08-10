---
id: T-071
title: The intermediate specifications carry the sources they rest on
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: [T-069]
related: [T-070]
work_package: v0.2
owner: the project owner
business_value: high
effort: m
created: 2026-08-10
updated: 2026-08-10
deliverables: []
---

# T-071 — The intermediate specifications carry the sources they rest on

## 1. Specify

**Outcome**
The two documents build mode produces before any HTML exists — `<slug>.foundation.md` and
`<slug>.slides.md` — **name the source documents the deck rests on**: the foundation carries the
full list once, and each slide names the ones it used. Today neither does, so the provenance mark
the build emits cannot be true of the slide it sits on, and it is not: both example decks say
`Illustrative model` on every slide while three real source documents sit beside each of them.

**Why this one**
Requested by the owner on 2026-08-10. It is the **upstream** of
[T-069](T-069-extend-the-provenance-mark-to-multiple-sources.md): that task makes the reference deck
cite its three source documents, and a build that has never been told which slide rests on which
document can only invent a uniform mark or reverse-engineer one. **What is measured today:**

- **`<slug>.foundation.md` names a count and a folder.** `examples/sort-window/`'s reads *"Three
  source documents, in `sources/`"* and then a **figure ledger** — `Figure | Value | Origin | Used
  on` — where `Origin` is a bare slug. There is no list of the documents themselves: no title, no
  path, nothing saying what each carries. That list exists for the reference deck only, as
  [`examples/sources/README.md`](../examples/sources/README.md), **hand-written outside the
  pipeline.**
- **`<slug>.slides.md` has eight fields per slide and none of them is a source.** Archetype, Title,
  Bottom line, Structure, Text, Visuals, Animations, Interactive elements. A slide says what it
  claims and never what it rests on.

**The objection this has to answer**
The figure ledger already maps origin to slide, so a per-slide source list looks like **a second
copy of a fact that has a home** — which METHOD rule 3 forbids and this project enforces. The
argument that it is not: **the ledger covers figures, and a slide can rest on a source without
quoting a number.** A date, a definition, a threshold, a quoted phrase, a diagram redrawn from a
source document — none of those is a ledger row, and all of them are things DS-105's mark is
supposed to be true about. Where the two overlap the ledger stays authoritative and the slide field
is checked **against** it rather than trusted, which is the difference between a derived fact and a
duplicated one.

**Scope**
- In: the reference list in `<slug>.foundation.md` — one row per source document, with whatever
  identifies it, where it lives and what it carries.
- In: a source field per slide in `<slug>.slides.md`, and what an **empty** one means — a title or a
  close slide rests on nothing external and that is a legitimate answer, not an omission.
- In: [`skills/htmldeck/references/build.md`](../skills/htmldeck/references/build.md), which is
  where both document shapes are defined, and whatever in `shell/` emits the mark from them.
- In: a check — every slug a slide names resolves to a row in the foundation's list, and every
  listed document is used by at least one slide. **An unused source is either a missing citation or
  a stale file**, and both are findings.
- Out: the mark's own form, its multi-source disclosure and the colophon —
  [T-069](T-069-extend-the-provenance-mark-to-multiple-sources.md) decides all three, which is why
  this task is blocked by it.
- Out: the quick view — [T-070](T-070-the-quick-view-for-a-source-document.md).
- Out: regenerating `examples/sort-window/`, unless the review finds the new fields change what the
  pipeline would have produced. Then it is in, because a worked example that predates the format is
  the format's first counter-example.

**Inputs**
- [`skills/htmldeck/references/build.md`](../skills/htmldeck/references/build.md) — the definition
  of both intermediate documents, and the deviation rule that says a build writes a departure back
  into them — so the format has to hold what a deviation would be written *as*.
- [`examples/sort-window/sort-window.foundation.md`](../examples/sort-window/sort-window.foundation.md)
  and [`sort-window.slides.md`](../examples/sort-window/sort-window.slides.md) — the only worked pair
  in the repository, and the case any format change has to keep working.
- [`examples/sources/README.md`](../examples/sources/README.md) — the reference list this task moves
  into the pipeline, written by hand for the deck that has no foundation document.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-105 on the mark, DS-102 on every figure
  being sourced.

**Acceptance criteria**
- [ ] `<slug>.foundation.md` carries a reference list, and `build.md` defines it — a reader of the
      foundation alone can say what the deck rests on without opening `sources/`
- [ ] Every slide in `<slug>.slides.md` names its sources, and an empty answer is **defined** rather
      than absent
- [ ] The build emits each slide's provenance mark **from that field**, so a deck resting on two
      documents does not say what a deck resting on one says
- [ ] A slug a slide names and the foundation does not list is **reported**; so is a listed document
      no slide uses
- [ ] Where a slide's sources and the figure ledger's `Origin` disagree, the ledger wins and the
      disagreement is reported — the field is checked against it, never a second copy of it
- [ ] `examples/sort-window/` is regenerated or explicitly ruled unchanged, with the reason recorded

**Open questions**
- **Does the reference list replace [`examples/sources/README.md`](../examples/sources/README.md),
  or coexist with it?** Recommended: coexist for now and revisit. The README explains *why* those
  documents exist and what DS-102 requires of an illustrative deck, which is prose a generated
  reference list has no place for; but the three-row table inside it becomes a second copy the day
  the foundation carries one. The reference deck has no foundation document at all, which is what
  makes this awkward rather than obvious. **The project owner decides.**

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |

## 3. Implement

**Decisions & assumptions**
- none yet

**Outputs produced**
- none yet

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-10 | → proposed | Raised from an owner request that the intermediate specifications list the references used. **Recorded as the gap that was measured, not as the request**: the foundation names a count and a folder and carries a figure ledger whose `Origin` is a bare slug, and the slide specification's eight fields include nothing about sources at all. The reference list that does exist — `examples/sources/README.md` — is hand-written outside the pipeline for the one deck that has no foundation document. **The one-home objection is answered in §1 rather than left for review to find**: the ledger covers figures, a slide can rest on a source it quotes no number from, and where the two overlap the ledger stays authoritative and the slide field is checked against it. Blocked by T-069, which decides the mark's form — this task is what makes that form reproducible from a specification rather than hand-authored. `v0.2`: nothing shipped is wrong. |
