---
id: T-070
title: The quick view — a source document rendered inside the deck
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: [T-069]
related: [T-019]
work_package: v0.2
owner: the project owner
business_value: medium
effort: l
created: 2026-08-10
updated: 2026-08-10
deliverables: []
---

# T-070 — The quick view: a source document rendered inside the deck

## 1. Specify

**Outcome**
A source cited by [`DS-105`](../docs/DESIGN-SYSTEM.md)'s provenance mark can open **inside the
deck** — a reading view of the source's content, carried in the file, needing no network and no
access to the author's filesystem.

**Why this one**
Requested by the owner on 2026-08-10 as the third of three link behaviours, alongside a local file
and an external URL. [T-069](T-069-extend-the-provenance-mark-to-multiple-sources.md) settles those
two on rule 1's existing precedent: a local-file link is an authoring form and a defect in a
delivered deck, and an external URL is legal because it needs network to follow rather than to
render. **That leaves the quick view as the only target that works unconditionally**, which is what
makes it worth building rather than a convenience on top of the other two.

**It is also the only one of the three that is not a rule change.** Local and external are decisions
about what DS-105 permits. This is a build-mode capability: something has to read a source document
and produce a displayable rendering of it, and nothing in this repository does that today.

**What makes it hard, stated before the work rather than discovered in it**
- **Size.** `docs/research/R5-assets-and-licences.md` measured a full 12-slide deck with three
  embedded faces, icons, a motion library and SVG diagrams at **192 KB**, and the shipping reference
  deck is 221 KB. Embedding is cheap for *fonts*; a set of source documents is a different order of
  magnitude and has no measured bound. **A measurement comes before a design here**, or the feature
  ships a deck nobody can email.
- **Fidelity is a claim, and the request already concedes it** — *"as it interpreted the original
  content to make it displayable"*. An interpreted rendering is a **derived artifact that asserts it
  represents a source**, which is DS-102's problem in a new place: a misrepresented source is a
  fabricated citation wearing a quick view. What the quick view promises about fidelity has to be
  written down and visible to the reader.
- **The reading view already exists and is not this.** `shell/` carries a reading view of the *deck*
  (`.doc`), which is the deck's own content re-laid-out. A source quick view is a second reading
  surface with a different subject, and **DS-136** says patterns are built once and reused — so
  whether these are one component or two is a design decision, not an implementation detail.
- **Licence and confidentiality.** Embedding a source copies it into a file that gets emailed. A
  deck built from a client's internal document would carry that document to everyone who receives
  the deck. **This is the one failure mode that is worse than not having the feature**, and the
  default has to be the safe one.

**Scope**
- In: reading a source into a displayable form, carrying it in the deck, and the surface that shows
  it.
- In: a measured size bound, on real source documents, before the design is fixed.
- In: what the deck tells a reader about fidelity, and what it tells an author about what they are
  about to embed.
- Out: DS-105's text and the provenance component — [T-069](T-069-extend-the-provenance-mark-to-multiple-sources.md),
  which this is blocked by, because there is no point building a target for a mark whose form is
  undecided.
- Out: source formats nobody in the corpus uses. Which formats are in scope is an open question
  below, not an assumption.

**Inputs**
- [T-069](T-069-extend-the-provenance-mark-to-multiple-sources.md) — the mark, its component, and
  which link targets are legal.
- [`docs/research/R5-assets-and-licences.md`](../docs/research/R5-assets-and-licences.md) — the
  192 KB measurement and the method that produced it, which is the method to reuse.
- [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) §4 — the existing reading view.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-102 on sourcing, DS-136 on building a
  pattern once, DS-001 on the one-file constraint the whole feature has to survive.

**Acceptance criteria**
- [ ] A deck carrying quick views for its sources **opens offline by double-click and renders
      glitch-free** — the constraint the feature exists inside, checked rather than assumed
- [ ] A measured size cost, on a real 12-slide deck with real source documents, stated as a number
      and a method someone else could re-run
- [ ] The reader can tell a quick view from the source: what it promises about fidelity is on the
      surface, not in documentation
- [ ] Embedding is **opt-in per source**, and an author is told what a deck will carry before it
      carries it — the confidentiality failure is the one that must not be reachable by default
- [ ] The quick view and the deck's own reading view are one component or two, with the reason
      recorded (**DS-136**)
- [ ] Every class it styles has a `COMPONENT-CONTRACT.md` row (**DS-229**)

**Open questions**
- **Settled 2026-08-10 by the owner — Markdown and plain text, and no other format in this task.**
  Both are readable with the standard library, which **L-07** requires of every tool here, and
  neither needs a parser this repository would have to acquire and then keep correct. `.docx` and
  `.pdf` are what real source material usually is, and that is a reason to raise a **second** task
  with a measured case behind it, not a reason to bring a dependency into the first. **The honest
  consequence, recorded rather than smoothed over:** for a while the quick view will not open the
  documents most decks are actually built from, so the provenance mark will fall back to plain text
  or an external URL more often than not. Whether that is worth building is a judgement the size
  measurement below should inform.
- **Settled 2026-08-10 by the owner — an overlay over the current slide, not a page.** Returning to
  the argument costs one dismissal, and the deck's slide count stops depending on how many sources
  it cites — which matters because slide count is a pacing decision and citation count is not.
  A `.doc`-style page would reuse more of what exists; it also interrupts more, and the thing being
  interrupted is the argument the source is supporting.

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
| 2026-08-10 | (specify) | **Both open questions settled by the owner**, as recommended: Markdown and plain text only, and an overlay rather than a page. The cost of the format decision is recorded rather than smoothed over — for a while the quick view will not open the formats most real source material uses, so the mark falls back to plain text or a URL more often than not. Still blocked by T-069. |
| 2026-08-10 | → proposed | Split from the owner's provenance request as the part that is a **capability rather than a rule**. Blocked by [T-069](T-069-extend-the-provenance-mark-to-multiple-sources.md): the mark's form decides what a quick view is a target *of*. Four hazards written down before any work — unmeasured size against a 221 KB shipping deck, fidelity as a DS-102-shaped claim, a second reading surface against DS-136, and **embedding a confidential source into a file that gets emailed**, which is the one outcome worse than not building this. `l` and `medium`: the largest thing on the v0.2 board and the least certain to be worth it, which is exactly the pair that should not be started before T-069 answers what it is for. |
