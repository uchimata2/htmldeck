---
id: T-181
title: Nothing detects that a deck's embedded quick view has drifted from its source
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-069, T-070, T-107, T-121, T-179]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-18
updated: 2026-08-22
shipped_in: 0.5.0
deliverables: [tools/deck/quickview.py, tools/check_all.py]
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
- ~~How the check locates a source from a title.~~ **Settled by the owner, 2026-08-19: the check
  accepts the same `--source <title>=<path>` list the other verbs already take, and is therefore run
  per deck.** It needs no build change, so it ships without touching what every future deck emits,
  and it keeps every verb in this tool on one argument shape. The alternative — the deck recording
  enough to locate its own sources — is better in the long run and costs a build change; it is **not
  folded in here**, so detection lands now and recording provenance paths in the deck can be argued
  on its own merits when somebody raises it. Nothing is open on this task.

## 2. Plan

**A fourth verb, `check`, beside `plan` / `add` / `refresh`.** `refresh` already computes the exact
comparison this needs — it renders the source and asks `body == was` — and then offers to
write. `check` asks the same question, writes nothing ever, and **exits non-zero on drift**. It is a
verb rather than a flag on `refresh` for the reason `refresh` is a verb rather than a flag on `add`:
it answers a different question and refuses on different grounds.

**What it prints has to separate the two causes**, because §1's three findings were two renderer
fixes and one document edit and a byte count cannot tell them apart:

- a **tag histogram** of both renderings, differenced — `<p> 42 -> 0`, `<ol> 0 -> 7` is a
  renderer that moved;
- the **first differing word** of the text with the tags stripped — that is a document that was
  edited;
- and where both are equal, *attributes or whitespace*, so the row is never silent about a
  difference it detected.

**The denominator travels in the line.** A deck carries *n* quick views and a run names *m* sources;
*compared 2 of 5* and *compared 5 of 5* must not read alike, which is **L-36** and the shape DS-231,
DS-232 and DS-236 all take here.

**Reaching `check_all.py`.** A per-deck gate whose argument builder reads the deck: the `data-qv`
title and `data-file` base name are already on every control, and `DECKS` already maps each deck to
its sources directory, so `title=<sources dir>/<data-file>` resolves — verified for all 8 quick
views across the two decks that carry any. The **tool** still takes the owner's `--source
<title>=<path>` list; the builder is what derives it, so nothing about the deck format changes and
the ruling holds exactly as given. A deck carrying no quick view is a **refusal with its reason**,
which is what `check_all` does with a gate that does not apply.

**Steps**
1. `check(deck, sources)` in `quickview.py`, and the verb in `main`.
2. Self-test fixtures: a match, a renderer-shaped drift, a text-shaped drift, and a title the deck
   does not carry — each asserted on what the row *says*, not only on the exit code.
3. `_quickview_args` in `check_all.py`, the `PER_DECK` row, and `quickview.py` out of `NOT_RUN`.
4. Watch it fail on a seeded instance, then pass on the tree as it stands.

## 3. Implement

**Decisions & assumptions**
- **A fourth verb, not a flag on `refresh`** — 2026-08-19. `refresh` already computes `body ==
  was`; what it does next is offer to write, and a checker that can write is a checker somebody
  eventually runs with the wrong flag. `check` writes nothing under any flag and returns 1 on drift.
  Same reasoning that made `refresh` a verb rather than a flag on `add`.
- **The row names the cause, not the fact** — 2026-08-19, and it is §1's requirement rather
  than a flourish. A **tag count that moved** is the renderer; a **word that differs** is the source
  document; both can be true at once and both print. Where the tags and the text both match and the
  strings do not, the row says *attributes or whitespace* — a comparison that failed must never
  print nothing.
- **The denominator is in the line** — 2026-08-19. *compared 2 of 5 carried* and *compared 5 of
  5* are the same verdict and not the same fact (**L-36**), and each quick view no `--source` named
  is printed by name. Without that, the honest way to make this check pass would be to name fewer
  sources.
- **`check_all` derives the `--source` list from the deck; the tool still takes it explicitly**
  — 2026-08-19. That is the owner's ruling implemented exactly: the argument shape every verb
  here uses is untouched, no deck format changes, and the derivation lives in the runner where a
  wrong guess is one file to fix. It works because `data-qv` and `data-file` are already on every
  wired control (T-109) and `DECKS` already maps each deck to its sources directory — verified
  for all 8 quick views across the two decks that carry any.
- **A deck with no quick view is a refusal with its reason, not a pass** — 2026-08-19.
  `reference-deck.html` carries none, so there is nothing embedded that can have drifted. It lands
  in `check_all`'s *skipped with a stated reason* bucket, which is what that bucket is for.
- **A named source file that is missing is a defect, not an exemption** — 2026-08-19. The
  builder refuses with the paths, rather than quietly comparing the rest.

**Watched failing, twice, one per cause.** §1 asks for a seeded instance rather than a clean
tree, and the two causes had to be told apart:

| Seeded | What the check said | Exit |
| :--- | :--- | :---: |
| a source document edited — one word, in a copy of `service-calendar.md` | `text differs at word 45: 'September Operations board…' -> 'Septembre Operations board…'`, and no tag movement at all | **1** |
| a deck aged to a pre-T-107, pre-T-121 renderer — `<hr>` back to `<p>---</p>`, three lists shattered | `<hr> 0 -> 8`, `<p> 42 -> 34`, `<ul> 5 -> 2` | **1** |
| a title the deck does not carry | `MISSING … this deck carries no quick view for that title` | **1** |
| both shipped decks as they stand | `compared 3 of 3` and `compared 5 of 5`, all match | **0** |

The second row reproduces T-179's original finding in the shape a reader can act on: those counts
say *the renderer moved and `refresh --write` is the repair*, where a byte count would have said
only that something did.

**Outputs produced**
- [`tools/deck/quickview.py`](../tools/deck/quickview.py) — `check`, `differences`, `profile`,
  the verb in `main`, and four self-test fixtures over what the row says rather than over its exit
  code.
- [`tools/check_all.py`](../tools/check_all.py) — `_quickview_args`, the `PER_DECK` row, and
  `quickview.py` out of `NOT_RUN`.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A deck whose quick views match their sources passes, and says how many it compared | **pass** | `compared 3 of 3 carried: 3 match` and `compared 5 of 5 carried: 5 match`, exit 0 |
| A deck carrying a stale quick view fails, naming the source and what differs | **pass** | Names the source path, and separates a renderer that moved from a document that was edited — §3's table |
| The check is watched failing on a seeded instance, not only passing on a clean tree | **pass** | Three seeded instances, one per failure mode, each watched at exit 1 — §3. Four self-test fixtures assert the wording rather than the code, so a row that stops naming the cause fails the tool's own start-up |
| It is reached by `python tools/check_all.py` rather than only by hand | **pass** | A `PER_DECK` gate. `reference-deck.html` is a refusal with its reason — it carries no quick view — and the run's partition holds |
| The two shipped decks with quick views pass it as they now stand | **pass** | Both, on the tree as committed |

**Child fix tasks raised**
- none. The wider option the open question named — a deck recording the path of each source it
  quotes, so the check needs no list at all — is deliberately not folded in here and is not
  raised as a task either: the owner ruled it *better in the long run* and argued it should be
  argued on its own merits when somebody raises it, which is not this session's call to pre-empt.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-22 | (shipped) | **`shipped_in` set to `0.5.0`, back-filled.** The field was never written, so this task read as belonging to no release while being closed. **Derived, not assumed**: the commit that set `status: done` is an ancestor of `v0.5.0`, which `git tag --contains` answers. Found while reading the unreleased set for `0.6.0` — eight tasks closed 2026-08-19 all carried an empty field, and a ninth ([T-187](T-187-open-the-motion-vocabulary-into-a-style-guide.md)) closed after the tag and belonged to `0.6.0` instead. |
| 2026-08-18 | → proposed | Raised out of [T-179](T-179-a-quick-view-cannot-be-refreshed-after-the-renderer-changes.md), whose refresh verb found three stranded corrections in one deck and thereby proved that nothing reports the drift. `PH3` by [`../CLAUDE.md`](../CLAUDE.md)'s rule: the published plugin is not broken by this — a deck built today is correct from the start — so it does not reopen `PH1`. T-179 fixed the *unreachability*; this is the *undetectability*, which is the half a refresh verb cannot cover, and **L-118** says why they are owed together. |
| 2026-08-19 | (no change) | **The one open question is closed by the owner**, on the recommendation written the day before: the check takes a per-deck `--source` list rather than teaching the deck to record its own source paths. That keeps this task `s` — the wider option would have reached the build and every deck it emits — and it means an unattended session can implement this without handing anything back. |
| 2026-08-19 | → done | `quickview.py check`, a fourth verb that writes nothing and returns 1 on drift, reached per deck by `check_all.py`. What it prints separates the two causes — a tag count that moved is the renderer, a differing word is the source document — because the three drifts that raised this task were two of one and one of the other, and a byte count names neither. Watched failing on three seeded instances and passing on both shipped decks. The owner's `--source` ruling implemented as given: the tool takes the list, the runner derives it, and no deck format changed. |
