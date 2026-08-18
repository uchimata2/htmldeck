---
id: T-181
title: Nothing detects that a deck's embedded quick view has drifted from its source
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-069, T-070, T-107, T-121, T-179]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-18
updated: 2026-08-18
deliverables: [tools/deck/quickview.py]
---

# T-181 — Nothing detects that a deck's embedded quick view has drifted from its source

## 1. Specify

**Outcome**
A gate reports when a deck's embedded quick view no longer matches a fresh render of the source it
names, so the drift is found by a run rather than by someone happening to look.

**The mechanism, measured**
A quick view is a *rendering* copied into the deck, so the deck holds an answer rather than a
reference. [T-179](T-179-a-quick-view-cannot-be-refreshed-after-the-renderer-changes.md) built the
verb that can re-render one; running it on `measure-first` for the first time found **three**
independent corrections stranded inside five embedded documents:

- 42 × `<p>---</p>` — **T-107**'s thematic break, in all 5 sources;
- 19 shattered lists and 0 `<ol>` where 7 belong — **T-121**'s list continuation, in 4 of the 5;
- stale link targets and a dropped file entry in D1 — **not a renderer fix at all**, but an edit to
  the source document made by `745f6b8`, which the deck never saw.

Every gate was green throughout. `check.py` reads the deck and the deck was valid; the reference
checks read documents and `<template>` contents are not documents; the renderer's self-test proves
what `markdown()` does now, never what an artifact captured earlier. The join between a source and
the copy of it inside a deck is watched by nothing. **L-118** is the general form.

**Scope**
- In: a check that, for each quick view a deck carries, re-renders the named source and reports
  whether the embedded copy still matches.
- In: it names the source and what differs, not merely that something does — a byte count alone
  does not tell a reader whether a renderer moved or the document was edited.
- In: reaching it from the run that already gates this repository, so it is not a command someone
  has to remember.
- Out: fixing the drift. `quickview.py refresh --write` is T-179's and already exists.
- Out: any change to `markdown()`, to what a quick view looks like, or to the T-069 admission guard.

**The question this has to answer, and it is the hard part.** A deck records the *title* of each
source, not its path — `data-qv` and `data-file` hold a title and a base name. So a check cannot
find the source on its own without a convention that binds one to the other. Settle that before
building: either the deck records enough to locate the source, or the check takes the same
`--source <title>=<path>` list the other verbs take and is therefore run per deck rather than
globally. The second is cheap and honest; the first is better and costs a build change.

**Inputs**
- [`tools/deck/quickview.py`](../tools/deck/quickview.py) — `carried`, `wired_pattern`, `render`.
- [`docs/lessons/L-118.md`](../docs/lessons/L-118.md) — why the refresh verb alone is not enough.
- [`tools/check_all.py`](../tools/check_all.py) — the run a new checker has to be discovered by.

**Acceptance criteria**
- [ ] A deck whose quick views match their sources passes, and says how many it compared
- [ ] A deck carrying a stale quick view fails, naming the source and what differs
- [ ] The check is watched failing on a seeded instance, not only passing on a clean tree
- [ ] It is reached by `python tools/check_all.py` rather than only by hand
- [ ] The two shipped decks with quick views pass it as they now stand

**Open questions**
- How the check locates a source from a title — the paragraph above frames it and does not settle
  it. It is the one decision worth taking before any code.

## 2. Plan

<not started>

## 3. Implement

**Decisions & assumptions**
- <none yet>

**Outputs produced**
- <none yet>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-18 | → proposed | Raised out of [T-179](T-179-a-quick-view-cannot-be-refreshed-after-the-renderer-changes.md), whose refresh verb found three stranded corrections in one deck and thereby proved that nothing reports the drift. `PH3` by [`../CLAUDE.md`](../CLAUDE.md)'s rule: the published plugin is not broken by this — a deck built today is correct from the start — so it does not reopen `PH1`. T-179 fixed the *unreachability*; this is the *undetectability*, which is the half a refresh verb cannot cover, and **L-118** says why they are owed together. |
