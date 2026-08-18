---
id: T-179
title: A quick view cannot be refreshed after the renderer changes, so a renderer fix never reaches a deck that already carries one
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-070, T-107, T-121]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-18
updated: 2026-08-18
shipped_in: unreleased
deliverables: [tools/deck/quickview.py, docs/lessons/L-118.md]
---

# T-179 — A quick view cannot be refreshed after the renderer changes, so a renderer fix never reaches a deck that already carries one

## 1. Specify

**Outcome**
A deck that already carries a quick view can be re-rendered from the same source with the current
`markdown()`, without rebuilding the deck and without hand-editing its HTML.

**The mechanism, measured**
`wire()` finds where to put a quick view with `item_pattern(title)`, which matches a **bare**
provenance item:

```
<span class="sources-item">(ITEM_HEAD)<title></span>
```

Once wired, that span holds a `<button class="sources-open">` and a `<template class="qv-src">`, so
the pattern no longer matches and `add` refuses. Measured 2026-08-18 on a copy of the shipped
`measure-first` deck:

```
REFUSED  Current business process analysis  no provenance item reads 'Current business process
         analysis' in this deck.
```

The refusal is correct for its own question — it is the T-069 guard that stops a quick view being
attached to a source no slide cites. It is simply also the only answer available to *refresh*, which
is a different question nothing asks on this deck's behalf.

**What it cost, already spent.** [T-121](T-121-the-quick-view-renderer-flattens-nested-lists-and-drops-indented-code.md)
fixed the renderer and proved the fix against the shipped sources: **4 of the 8 embedded sources
render differently**, and the difference is not cosmetic — the old renderer broke a wrapped list
item into `<li>first line</li></ol><p>the rest of the sentence</p><ol>`, splitting one sentence
across an item and a paragraph and shattering one `<ol>` into three. Two shipped decks carry that
today, and T-121 could not reach them.

**Scope**
- In: a way to re-render the quick views a deck already carries, from the sources named on the
  command line, replacing the `<template>` contents in place.
- In: the refusal above keeps meaning what it means for a source no slide cites. Refresh is a
  different verb, not a relaxation of that guard.
- In: it reports what changed, in the terms `plan` already uses — bytes before and after, per
  source — because a refresh silently rewriting a shipped deck is the failure mode here.
- In: refreshing the two decks that carry the T-121 defect, and looking at the result offline.
- Out: rebuilding a deck from its specification. That is the build, and it is not this.
- Out: any change to what `markdown()` produces — T-121 settled that.
- Out: what a quick view looks like, which is
  [T-110](T-110-the-quick-view-styles-a-source-as-deck-copy-not-as-a-document.md)'s.

**Inputs**
- [`tools/deck/quickview.py`](../tools/deck/quickview.py) — `item_pattern`, `wire`, `carried`,
  `plan`.
- [`examples/measure-first/measure-first.html`](../examples/measure-first/measure-first.html) and
  its [`sources/`](../examples/measure-first/sources) — 5 quick views, 4 of them affected.
- [`examples/sort-window/sort-window.html`](../examples/sort-window/sort-window.html) — 3 quick
  views, none affected; the control case that proves a refresh is byte-identical when the renderer
  agrees with what is already embedded.

**Acceptance criteria**
- [ ] A deck already carrying a quick view can be re-rendered from its source without rebuilding it
- [ ] Refreshing `sort-window` changes nothing, byte for byte — the renderer agrees with what is
      embedded, so a refresh must be a no-op
- [ ] Refreshing `measure-first` replaces exactly the 4 affected templates and leaves the 5th alone
- [ ] A source no slide cites is still refused, with the T-069 wording unchanged
- [ ] The two shipped decks are refreshed, gated, and looked at offline

**Open questions**
- None. Whether this is a new subcommand or a flag on `add` is an implementation choice, and the
  criteria above hold either way.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | A pattern that matches an already-wired item, beside the bare one | `quickview.py` |
| 2 | The refresh path: re-render, swap the `<template>` body, report the byte delta | `quickview.py` |
| 3 | A self-test fixture per branch — refuses an uncited source, no-ops when nothing changed | self-test |
| 4 | Refresh both shipped decks; gates; open the changed quick views and look | the decks |

**Three decisions the plan takes, so implementation does not re-take them.**

- **A third verb, `refresh`, not a flag on `add`.** `add`'s refusal is the T-069 guard and its
  posture is *plan first, write on the exception*. A flag would make one command answer two
  questions whose refusals differ, and the guard is the thing most worth not blurring.
- **The swap target is the `<template>`, not the item.** `carried()` already locates every quick
  view by `<template class="qv-src" data-qv="…">`, which is exact and unambiguous; the button and
  the `ITEM_HEAD` identifier beside it are untouched, so T-109's carry-through cannot regress
  through this path at all.
- **`refresh` reports and writes nothing by default, `--write` writes.** Same posture as `plan`,
  for the reason §1 gives: the failure mode is a shipped deck rewritten silently.

**The refusals, which are two and not one.** A title the deck does not carry splits by whether a
slide cites it: cited-but-unwired is an `add` job and says so; not cited at all is the T-069
refusal. To keep §1's "wording unchanged" true mechanically rather than by care, that sentence
becomes one constant used by both `wire` and `refresh` — the same string, not a copy of it.

## 3. Implement

**Decisions & assumptions**
- **`refresh` is a third verb, not a flag on `add`** — 2026-08-18. The two refuse on different
  grounds and the difference is the T-069 guard, which is the last thing worth blurring.
- **The swap target is the `<template>` body, via `wired_pattern`** — 2026-08-18. `carried()`
  already locates every quick view by `data-qv`, so the control, the `sources-id` and the kind
  glyph are outside the substitution by construction rather than by care. T-109 cannot regress
  through this path.
- **`rewire()` is pure and separate from `refresh()`** — 2026-08-18. Both refusals live in it, so
  the self-test can watch each one fail; a branch reachable only through a file on disk is a branch
  **L-04** does not actually cover.
- **The T-069 sentence is now one constant, `UNCITED`, used by `wire` and `rewire`** — 2026-08-18.
  §1 required the wording unchanged between the two verbs; a shared string makes that mechanical
  instead of careful.
- **`--write` rather than write-by-default** — 2026-08-18, from §1: the failure mode here is a
  shipped deck rewritten silently, so the reporting posture is `plan`'s.

**Outputs produced**
- [`tools/deck/quickview.py`](../tools/deck/quickview.py) — `refresh` verb, `rewire()`,
  `wired_pattern()`, the `UNCITED` constant, and 8 self-test assertions covering both refusals, the
  replacement, the byte report, the carry-through and the no-op.
- [`examples/measure-first/measure-first.html`](../examples/measure-first/measure-first.html) —
  refreshed, 399 607 → 398 940 bytes.
- [`docs/lessons/L-118.md`](../docs/lessons/L-118.md) — the general rule the run produced.
- [T-181](T-181-nothing-detects-that-a-decks-embedded-quick-view-has-drifted-from-its-source.md) —
  the detection half, raised rather than absorbed.

**What the refresh actually found, which is more than the task expected.** Re-rendering
`measure-first` changed **all five** embedded sources, not the four §1 predicted, and the surplus is
not a defect in the refresh:

| Stranded correction | Sources affected | Evidence |
| :--- | :---: | :--- |
| **T-107** — thematic break as a paragraph of hyphens | 5 of 5 | 42 × `<p>---</p>` → 42 × `<hr>` |
| **T-121** — list continuation and ordered lists | 4 of 5 | 19 shattered lists → 3 genuine; 0 `<ol>` → 7 |
| **A source-document edit** (`745f6b8`) | 1 (D1) | link targets gained `../`; a dropped file entry |

The 5th source, *Management decision matrix*, changed by exactly −48 bytes = 8 × the 6 bytes
`<p>---</p>` → `<hr>` saves, and by nothing else — which is how the three were told apart.

**The instrument, and its control.** The preview pane reports a 0×0 viewport and would not
composite frames, so the look was taken in real Chrome through `render.py shots`, on a copy carrying
an injected opener. **L-110** warns that an injected opener can fail silently, so the control was to
shoot the deck shut and open and require the images to differ: 141 KB against 253 KB. They differ,
so the opener fired and the picture is of the state claimed.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A deck already carrying a quick view can be re-rendered from its source without rebuilding it | met | `quickview.py refresh <deck> --source <title>=<path> [--write]`. Both shipped decks re-rendered without a build |
| Refreshing `sort-window` changes nothing, byte for byte | met | Dry run: 0 changed, 3 unchanged, +0 bytes. Run again with `--write`: md5 `778f5404…` before and after, and `git status` reports the file unmodified |
| Refreshing `measure-first` replaces exactly the 4 affected templates and leaves the 5th alone | **not met** | All 5 were replaced. The 5th is affected too — by **T-107**'s stranded fix, not T-121's, at exactly −48 bytes and no other difference. The criterion was written from T-121's measurement, which counted only T-121's defect; it is wrong about the deck rather than about the tool. Not reworded — see the table in §3 and [T-181](T-181-nothing-detects-that-a-decks-embedded-quick-view-has-drifted-from-its-source.md) |
| A source no slide cites is still refused, with the T-069 wording unchanged | met | Same `UNCITED` constant serves both verbs, so the wording cannot drift. Self-test asserts `T-069` is in `rewire`'s refusal, and separately that a cited-but-unwired source is **not** refused in those words |
| The two shipped decks are refreshed, gated, and looked at offline | met | `check_all.py`, `lint.py` and `figures.py` green. Looked at in real Chrome, offline, with the shut/open control above: the `<hr>` rules render as rules, and the split sentence reads as one `<ol>` item |

**Child fix tasks raised**
- [T-181](T-181-nothing-detects-that-a-decks-embedded-quick-view-has-drifted-from-its-source.md) —
  nothing detects the drift this task made fixable. Raised rather than absorbed, because a refresh
  verb and a drift check are different work and only the first was specified here.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-18 | → proposed | Raised out of [T-121](T-121-the-quick-view-renderer-flattens-nested-lists-and-drops-indented-code.md), which fixed the renderer and then could not deliver the fix to the two decks that need it. `PH3` by [`../CLAUDE.md`](../CLAUDE.md)'s rule — the published plugin is not broken by this, and a deck built after T-121 renders correctly from the start, so it is not a defect that reopens `PH1`. What makes it worth its own record rather than a note is that the gap is in the *tool's verbs*, not in one deck: every future renderer change will hit it again. |
| 2026-08-18 | proposed → specified | §1 re-read against the code rather than taken on trust: `item_pattern` matches a bare `.sources-item`, and `wire` substitutes a `<button>` plus `<template>` into exactly that span, so once wired the pattern cannot match again and `add` has no path back. The refusal §1 quotes is `wire`'s only failure mode. Scope and criteria stand unchanged; the one open question was already answered as an implementation choice. |
| 2026-08-18 | specified → planned | Plan kept its four steps and gained the three decisions above, all settled by reading the tool rather than by choosing: a third verb because `add`'s refusal is a guard worth not blurring, the `<template>` as the swap target because `carried()` already locates it exactly, and `--write` because §1 names silent rewriting as the failure mode. Also split the refusal in two — cited-but-unwired is not the same answer as uncited — and made the T-069 sentence a shared constant so "wording unchanged" is mechanical. |
| 2026-08-18 | planned → in_progress → done | Built `refresh`, `rewire` and `wired_pattern`; the T-069 sentence became the shared `UNCITED` constant so §1's "wording unchanged" is mechanical. `sort-window` is byte-identical through a real `--write`, which is the control that makes the verb trustworthy on a shipped deck. `measure-first` changed in all five sources rather than four: T-107's thematic break was stranded in every one of them, T-121's list defect in four, and D1 additionally quoted a source edited after the deck was built. That criterion is recorded **not met** rather than reworded. Two things came out of it — **L-118**, and [T-181](T-181-nothing-detects-that-a-decks-embedded-quick-view-has-drifted-from-its-source.md) for the detection half, which this task's scope does not cover. Looked at in real Chrome offline, with a shut/open image pair as the **L-110** control. |
