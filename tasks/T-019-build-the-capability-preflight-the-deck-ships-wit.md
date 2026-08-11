---
id: T-019
title: Build the capability preflight every deck ships with
type: deliverable
status: done
phase: review
parent: null
blocked_by: [T-002]
related: [T-005, T-017]
work_package: v0.3
owner: maintainer
business_value: high
effort: l
created: 2026-08-06
updated: 2026-08-11
deliverables:
  - tools/deck/preflight.py
  - shell/shell.html
  - shell/components.css
  - shell/deck.js
  - docs/DESIGN-SYSTEM.md
---

# T-019 — Build the capability preflight every deck ships with

## 1. Specify

**Outcome**
Every generated deck carries a short feature-detection block that runs before it renders, names
precisely which capability is missing when one is, and leaves the recipient with a legible document
instead of a blank page. This is the mechanism that makes
[R6](../docs/research/R6-portability-contract.md)'s version-floor position real: the deck's floor
is *whatever browser passes the preflight*, and without the preflight that position is just a
refusal to name a number.

**Why this one**
T-017 measured Chrome 151 and Edge 151 and nothing else, so it declined to invent a floor like
"Chrome 125+" — that would have been reading rather than testing (**L-05**). R6 §7 argues the
preflight is the better contract regardless of what testing old builds would have shown, for three
reasons worth restating in one line each: a version number is a lossy proxy for the capability you
actually care about; **a recipient cannot act on a version number** in a deck that has already
failed to render; and asking a browser what it can do fails in the safe direction for browsers
nobody tested.

The deck is delivered by double-click to someone who did not build it and cannot debug it. A blank
slide is the worst possible failure for that recipient. This task is what stands between them and
one.

**Scope**
- In: the preflight itself — what it checks, when it runs, and how little it costs.
- In: **emitting only the checks the deck actually uses.** A deck with no 3D must not fail on a
  missing WebGL context; a deck that inlines no ESM library must not test `import(blob:)`.
- In: the degraded state. What a recipient sees when a check fails, which must be the deck's
  content in a legible static form, never a diagnostic screen with no content behind it.
- In: proving the preflight fails when it should (**L-04**) — a preflight that has only ever been
  seen passing is not evidence of anything.
- Out: choosing a numeric version floor. R6 §7 settled that this should not be done, and this task
  implements that ruling rather than reopening it.
- Out: the rest of the build check. T-005 gates the deck **at build time**, on the author's
  machine; this runs **at open time**, on the recipient's. Different moment, different audience,
  different failure. Neither replaces the other.

**Inputs**
- [`docs/research/R6-portability-contract.md`](../docs/research/R6-portability-contract.md) §7 —
  the position, the reasoning, and a first list of load-bearing checks.
- [`docs/research/R6-portability-contract.md`](../docs/research/R6-portability-contract.md) §2 —
  which capabilities are actually load-bearing, measured.

**What the shell measures, and what it costs R6 §7's list** *(2026-08-11)*

R6 §7 proposed six rows. Counted across `shell/components.css`, `shell/deck.js`,
`themes/quarto.css` and both shipped decks, **four of them have no subject in any deck this project
can build today**, and the fifth was already ruled out:

| R6 §7 row | Uses in the shell + both decks |
| :--- | :--- |
| `isSecureContext` | ruled out 2026-08-07 — a build-check row, true for `file://` |
| `container-type: inline-size` | **0** |
| `selector(:has(*))` | **0** |
| `document.fonts` | **0** — `render.py`'s probe uses it, the deck does not |
| `import(blob:)` | **0** — no build path emits an ESM library |
| `WebGLRenderingContext` | **0** — no deck renders 3D |

What the shell *does* rest on is older and duller: 454 custom-property references, `display:grid` on
`.slide` with explicit `grid-row`, `transform:scale()` on the stage, `<template>` for the quick view,
and `Element.closest` in the delegated quick-view handler. **So the selection rule already agreed
(§1, *Open questions*) bites harder than R6 expected: applied honestly it empties most of R6's list
and replaces it with a shorter one nobody would have guessed.** That is the finding, not a
disappointment — the floor this deck actually has is low, and the preflight's job is to turn the
blank page below it into a legible one.

Two design consequences follow, and both are decided here rather than in §3:

1. **The degraded state is the deck's *initial* state, not a reaction to a failed check.** `<html>`
   ships carrying the marker and the preflight **removes** it when every check passes. A blank page
   then cannot happen by a check running too late, only by the fallback CSS being wrong — and it
   costs nothing, because the same marker covers the case no preflight can catch: **the deck is
   blank with JavaScript off**, since `.slide` is `opacity:0` until the script sets `data-current`.
   One mechanism, three triggers: a failed check, no script, a script that throws before it boots.
2. **The fallback block may use no custom property, no grid and no modern selector**, because the
   capability it is compensating for may be exactly one of those. It is baseline CSS with literal
   values, and it is the one block in `shell/components.css` under that rule.

**Acceptance criteria**
- [ ] A deck built by build mode carries a preflight, and it runs before first paint
- [ ] The preflight contains **only** the checks that deck's content needs — demonstrated by
      building two decks with different feature use and diffing what each emits
- [ ] Demonstrated **failing on a known case** (**L-04**) — a capability is suppressed and the
      preflight names it, rather than the deck rendering blank or rendering wrong
- [ ] On failure the recipient still gets the deck's content in a legible static form
- [ ] Zero false positives on the tested browsers — a deck that works must never show the warning
- [ ] Size cost measured, not estimated
- [ ] The failure state **looked at** (**L-01**), offline, in a real browser
- [ ] **The same degraded state with the script suppressed entirely** — added 2026-08-11 from the
      measurement above. A recipient whose browser runs no script is the extreme of the case this
      task exists for, and it reaches the identical mechanism rather than a second one

**Open questions**
- ~~Should a failed preflight be silent for the *author* and loud for the *recipient*, or the same
  for both?~~ **Answered 2026-08-07 by the owner: the same for both, always visible.** A deck
  opened by double-click cannot know who opened it, so "silent for the author" would have to be
  compiled in — and the shipped file would then differ from the file that was tested, which is the
  one thing a portability contract cannot afford. The author's separate signal already exists and
  runs at a different moment on a different machine:
  [T-005](T-005-build-check-the-gate-the-deck-must-pass.md)'s build check.
- ~~Does `isSecureContext` belong in the emitted preflight at all, given that every route by which a
  deck is opened satisfies it? It may be a build-check row rather than a runtime one.~~ **Answered
  2026-08-07 by the owner: no — make it a build-check row.** `file://` is already a secure context
  in Chrome, so a runtime test can only ever pass: bytes in every deck, plus the false reassurance
  that something was verified. **This is the general rule this task should apply to the whole check
  set, not a one-off** — a preflight row earns its place only if there is a real opening route on
  which it fails, and the scope line above already forbids emitting checks the deck does not use.

## 2. Plan

**The shape.** The preflight is an eleventh shell region, and it is **derived, never declared** —
the same mechanism `shell.py icons` already uses for the sprite, for the same reason: which checks a
deck needs is a fact about the deck's own bytes, not a thing for an author to remember. A row is
emitted when a scan of the built deck finds the feature it guards; the probe code for a row nothing
uses is not in the file at all.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | The row table — `(id, name, probe, used(deck), why)`, one row per capability the design system permits a deck to reach for, ordered as they would bite | `preflight.py` |
| 2 | The degraded state: `<html data-preflight>` shipped on, the marker removed by a passing preflight, and a baseline-CSS fallback that flows the slides as a document | `shell.html`, `components.css` |
| 3 | Emit from `shell.py new`, keep it in sync with `preflight --check`, and stand the deck script down when the marker survives | `shell.py`, `deck.js` |
| 4 | Two decks with different feature use, built and diffed — what each emits and what neither does | evidence in §3 |
| 5 | Suppress a capability in a copy of a real deck and confirm the preflight names *it* (**L-04**); suppress the script too | evidence in §3 |
| 6 | DS-009 in the ruleset with a check behind it, or the gate goes red for a rule nothing decides | `DESIGN-SYSTEM.md`, `audit.py` |
| 7 | Size cost measured on both shipped decks; the failure state and the no-script state **looked at** offline | figures + a look |

**Step 6 is not optional and not last by accident.** `check.py` fails any run where a ruleset rule
lands in no bucket, so adding DS-009 without its check is a red gate the same afternoon — which is
the discipline working, and the reason the rule and the check land together.

## 3. Implement

**Decisions & assumptions**

- **The preflight is an eleventh shell region, derived like the sprite** — 2026-08-11. `shell.py
  preflight` reads the deck and emits the rows it finds a subject for, and `shell.py check` reports a
  stale block exactly as it reports a stale sprite. The alternative was invariant probe code plus a
  per-deck `var NEEDS=[...]`, which is smaller to build and ships the WebGL probe to every deck that
  has no 3D — the scope line forbids that, so the region won.
- **`<html data-preflight="pending">` ships in the source and a passing preflight removes it** —
  2026-08-11. Progressive enhancement rather than progressive degradation: the blank stage is never
  what an unsupported browser paints, so a check that runs late cannot cost the recipient anything.
- **The deck script stands down while the marker survives**, one line at the top of the IIFE, and
  **an `error` listener puts the marker back if boot throws** — scoped to boot by a `booted` flag set
  on the last line. A check set cannot be complete; this is the net under the rows nobody wrote. A
  chart that throws on slide nine must not collapse a deck somebody is already reading, which is why
  the flag is there rather than a bare handler.
- **The fallback block is baseline CSS with literal values**, and it is exempted from DS-010 in both
  halves — `THEME-CONTRACT.md` §5 for lengths, `audit.outside_token_layer` for colour. A token there
  resolves to nothing in the one case the block exists for.
- **Printing is unchanged by the degraded state.** The print block is `!important` throughout and
  paginates the stage; a browser that failed the preflight prints what that block says. Printing is a
  mode the user forces on and never a constraint on the design, so it was not made this block's
  subject.

**What was built**

| Piece | Where |
| :--- | :--- |
| The row table, the emitter, and `prove` | [`tools/deck/preflight.py`](../tools/deck/preflight.py) — `rows`, `show`, `prove` |
| The eleventh slot, emission, and the staleness check | [`tools/deck/shell.py`](../tools/deck/shell.py) — `PREFLIGHT`, `apply_preflight`, `shell.py preflight` |
| The banner, and the marker authored on `<html>` | [`shell/shell.html`](../shell/shell.html) |
| The degraded state | [`shell/components.css`](../shell/components.css), the block above `@media print` |
| Standing down, and the net under boot | [`shell/deck.js`](../shell/deck.js) |
| The rule and its three verdicts | [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) DS-009; [`tools/deck/audit.py`](../tools/deck/audit.py) `STATIC` |
| The two new parts, and the exemption | [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) §3.1; [`docs/THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) §5 |

**Evidence**

*Only the rows this deck needs* — the two shipped decks, built and diffed:

```
examples/reference-deck.html            2 of 6 rows: custom-properties, grid
examples/sort-window/sort-window.html   3 of 6 rows: custom-properties, grid, template
```

The whole diff between the two emitted blocks is one line, and it is the row `sort-window`'s three
quick views need. The reference deck cites its sources as plain text and carries no `<template>`, so
it does not test for one.

*Failing on a known case* — `python tools/deck/preflight.py prove examples/sort-window/sort-window.html`:

```
  suppressed         marker    what the recipient reads
  none               (removed) This deck needs JavaScript to present itself. Every slide's content is bel
  custom-properties  fail      This browser is missing CSS custom properties. The deck cannot present her
  grid               fail      This browser is missing CSS grid. The deck cannot present here, so every s
  template           fail      This browser is missing the <template> element. The deck cannot present he
  no-script          pending   This deck needs JavaScript to present itself. Every slide's content is bel
```

**Two of the five suppressions are real and three of them are not, and the tool says which on every
run.** `delete HTMLTemplateElement.prototype.content` takes the capability away rather than the
answer about it, and the deck's own `tpl.content.cloneNode` breaks as it would on a browser that
never had it; stripping the scripts is the same kind of real. Chrome cannot be made to lack CSS grid
or custom properties, so those two suppress the **detector** — which proves the row's wiring and the
degraded state, and does not prove the capability's absence.

*Size cost*, measured on both decks rather than estimated:

```
  examples/reference-deck.html          245479 -> 252439   +6960 bytes (2.84%)
  examples/sort-window/sort-window.html 242699 -> 249747   +7048 bytes (2.90%)
      of which the fallback CSS   3769
      of which the preflight      1005 (2 rows) / 1093 (3 rows)
      of which the shell markup    728
      of which deck.js            1470
```

**The rows are the cheap part.** 84 bytes buys a row; the degraded state is 3.8 KB and is paid once
whether a deck emits two rows or six.

**Deviations and findings**

- **R6 §7's check list did not survive being measured**, and §1 records what replaced it. R6 §7 now
  carries the correction under its own recommendation.
- **One acceptance criterion was added before the work** (§1), for the script-suppressed case, on the
  measurement that the deck is blank with JavaScript off.
- **`audit`'s DS-005 predicate bans `import(` outright and would fail any deck emitting the `esm`
  row.** DS-005 is *script may not read a local file's bytes*, and R6 §6 measures `import(blob:)` as
  the one working route for an ESM library — DS-006 exists for it. So the check reads wider than the
  rule it implements, in the shape T-069 found for DS-001. Latent rather than live: no build path
  emits an ESM deck today. Raised as
  [T-093](T-093-ds-005s-check-bans-the-one-esm-route-r6-measured-as-working.md).
- **Two defects were found in tools this task depended on, and both are fixed here** rather than left
  for the deck that trips over them next: `component.shared_css` truncated the shared block at
  `@media print{` and reported *0 uncontracted* over two new classes (**L-68**), and the two scans
  that read prose about a construct as the construct (**L-67**).
- **`render.py shots --out <relative path>` silently produces no screenshots**, reporting `FAILED`
  with no cause — found while looking at the decks, in the flag T-074 made parse. Not this task's
  subject and not fixed here; raised as
  [T-094](T-094-render-py-shots-out-with-a-relative-path-writes-nothing.md).

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A deck built by build mode carries a preflight, and it runs before first paint | met | The block is the first script in `<body>`, so nothing of the deck below it has been parsed when it runs. `ds009_preflight_present` decides the position, not just the presence. And the guarantee does not rest on the timing at all: the marker is authored, so the degraded state is what paints if the preflight never runs. |
| The preflight contains **only** the checks that deck's content needs, demonstrated by diffing two decks | met | 2 rows against 3 on the two shipped decks, and the diff is the one line `sort-window`'s quick views need. `shell.py check` fails a block that stopped matching its deck. |
| Demonstrated **failing on a known case** (**L-04**) | met | Four suppressions, each naming its own row and nothing else. Two are real capability removals and two are detector-level; `prove` prints which on every run rather than letting the reader assume. |
| On failure the recipient still gets the deck's content in a legible static form | met | Looked at, offline: banner, then twelve slides flowed in order with figures at full width, disclosure panels open, ledgers and stat figures readable, source lists under each slide. The reading view's argument, built by CSS alone because the script may be one of the missing pieces. |
| Zero false positives on the tested browsers | met | The control removes the marker and shows no banner on both decks, and the full gate's render stage drives the real deck to 0 failures on each. |
| Size cost measured, not estimated | met | +6960 and +7048 bytes, 2.84% and 2.90%, broken down by piece in §3. |
| The failure state **looked at** (**L-01**), offline, in a real browser | met, with its half named | Real Chrome, headless, throwaway profile, every DNS lookup black-holed — this project's instrument, and five captures were read. **A literal double-click by a person is not something this session can observe**, and it is not claimed. |
| The same degraded state with the script suppressed entirely | met | The marker stays `pending`, the authored sentence is what the recipient reads, and the document below it is identical to the failed-row case. One mechanism, three triggers. |

**Child fix tasks raised**
- [T-093](T-093-ds-005s-check-bans-the-one-esm-route-r6-measured-as-working.md) — DS-005's predicate
  bans the `import(blob:)` route R6 §6 measured as working, so the `esm` row cannot ship.
- [T-094](T-094-render-py-shots-out-with-a-relative-path-writes-nothing.md) — `render.py shots --out`
  with a relative path writes nothing and says `FAILED`.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-11 | → done | **DS-009 ships, and the deck's floor is a question the browser answers.** Every criterion met; the one whose half is named is the look — real Chrome, offline, five captures read, and a literal double-click is not something this session can observe. Two decks emit two rows and three, and the diff between the blocks is the single line the quick views need. Four suppressions each name their own row, and `prove` prints on every run which two are real capability removals and which two only take the detector away. Cost: 2.84% and 2.90% of the two decks, of which the rows are 84 bytes each and the degraded state is 3.8 KB paid once. **Two defects in tools this task leaned on were found and fixed here** — a shared-block read that truncated at `@media print` and reported *0 uncontracted* over two new classes (**L-68**), and two scans that read prose about a construct as the construct (**L-67**, once in the emitter and once in the instrument built to prove the emitter right). Two more were found and left: [T-093](T-093-ds-005s-check-bans-the-one-esm-route-r6-measured-as-working.md) and [T-094](T-094-render-py-shots-out-with-a-relative-path-writes-nothing.md). |
| 2026-08-11 | → in_progress | **Built, and the first fixture written caught the emitter reading its own documentation.** `"<template" in html` fired on every deck, because the shared block and the deck script both explain the quick view in a comment naming the tag and both ship inside every deck. The instrument written to prove the emitter right had the same defect an hour later, and reported a passing control as degraded. Both are **L-67**. |
| 2026-08-11 | → planned | **Seven steps, and the shape decided: the preflight is a derived shell region, not an authored one.** The sprite is the precedent — `shell.py icons` reads the deck and rewrites the sprite to match, so DS-113 is true by construction rather than by memory — and *emit only the checks this deck uses* is the same sentence about a different region. Step 6 exists because `check.py` fails a run where a ruleset rule lands in no bucket, so DS-009 and its check are one step or the gate goes red. |
| 2026-08-11 | → specified | **R6 §7's proposed check list does not survive contact with the shell, and §1 now records what does.** Counted across the shell, the theme and both shipped decks: container queries 0, `:has()` 0, the fonts API 0, `import()` 0, WebGL 0 — four of R6's six rows have no subject in any deck this project can build, and `isSecureContext` was already ruled out in 2026-08-07. The selection rule the owner generalised that day is what empties the list, so this is the rule working rather than a gap. What the shell does rest on is custom properties, `display:grid`, `transform:scale()`, `<template>` and `Element.closest`. Two decisions came out of the same measurement and are recorded in §1: the degraded state ships **on** and a passing preflight removes it, which also covers the deck being blank with JavaScript off; and the fallback block may use no custom property, no grid and no modern selector. One acceptance criterion added for the script-suppressed case — the same mechanism, its extreme. |
| 2026-08-10 | (specify) | **Estimated `high`/`l`, and moved to `v0.3`.** `high` because the preflight is what makes CLAUDE.md rule 2's *degrade gracefully* real for a recipient who cannot debug a blank page; `l` because emitting only the checks a deck actually uses requires the builder to know what it emitted, which is not a property the deck can read off itself. `v0.3` under the release split set by the owner 2026-08-10 — a new capability of this size is neither a dependency nor a moderate fix. |
| 2026-08-07 | (no change) | **Both open questions answered by the owner; §1 has none left.** *One behaviour, always visible* — the file cannot know who opened it, and an author-silent build would ship a different artifact from the one that was tested. *`isSecureContext` becomes a build-check row* — it is true for `file://`, so at runtime it can only pass. **The second answer generalises into the design step this task starts with**: step 1 selects checks per deck feature, and the selection rule is now stated — a row earns its place only where a real opening route makes it fail. That is testable against [R6](../docs/research/R6-portability-contract.md) §2's load-bearing list, and it will remove more than one candidate. |
| 2026-08-06 | → proposed | Created. R6 §7 defines the deck's version floor as a capability preflight rather than a number; that position is only real if something emits the preflight. Blocked on T-002 because the preflight is emitted **by** build mode and cannot be built before it — the design work in steps 1–2 could start earlier if the owner wants it pulled forward. |
