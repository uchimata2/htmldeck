---
id: T-166
title: shell.py sync leaves an upgraded deck failing the theme gate, and says nothing
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-124, T-106, T-128]
work_package: PH1
owner: the project owner
business_value: high
effort: s
created: 2026-08-16
updated: 2026-08-16
deliverables:
  - tools/deck/shell.py
---

# T-166 — shell.py sync leaves an upgraded deck failing the theme gate, and says nothing

## 1. Specify

**What happened, on the first real adopter upgrade this repository has ever performed.**
[T-128](T-128-publish-the-adopter-deck-as-a-worked-example.md) step 5 ran
`shell.py sync <deck> --write` on a deck built against **0.2.2**. The sync reported success — two
regions synced, twelve per-deck regions untouched — and `shell.py check` then passed. The next gate
did not:

```
DS-013  FAIL  every token THEME-CONTRACT.md names is declared and derives as it says:
              117 token(s) required, 1 problem(s) - --qv-measure not declared
```

**The mechanism.** `--qv-measure` was introduced by
[T-106](T-106-the-quick-view-sheet-is-sized-to-the-prose-measure.md). The shipped
[`shell/components.css`](../shell/components.css) **uses** it, and every deck **declares** it in its
own theme block — `examples/reference-deck.html` and `examples/sort-window/sort-window.html` each
carry `--qv-measure:80rem;` beside `--doc-measure`. The theme block is a per-deck region, so `sync`
correctly refuses to touch it — and therefore installs a shell that reads a token the older deck
never declared. Neither command that an adopter is told to run can see it.

**Why this is `PH1`.** It is a defect in the published plugin reachable by an adopter following the
documented upgrade path, which `CLAUDE.md` places in `PH1` regardless of size. T-124 shipped `sync`
precisely so an adopter could catch up after a release; a sync that reports success and leaves the
deck failing a gate is that feature not finishing its job.

**The general shape, which is what the fix must address.** This is not about one token. Any release
that adds a token to the shared block and expects it declared per deck creates the same gap, and the
gap widens silently with every release an adopter skips. `sync` knows both halves — the shell it is
installing and the deck it is installing into — so it is the one command that can see it.

**Scope**
- In: `sync` detects tokens the incoming shell reads and the deck does not declare, and reports
  them. Whether it also **writes** a default is the open question below.
- In: the same detection on `check`, so an already-synced deck is not silent either.
- Out: changing the theme contract, or moving `--qv-measure` into the shared block. The per-deck
  home is deliberate — the token is a theme value.

**Acceptance criteria**
- [ ] A deck at 0.2.2 synced to the current release either passes `theme.py check` afterwards, or
      is told by `sync` exactly which tokens to declare
- [ ] A fixture holds a deck missing a required token, and the tool is shown to fail without the fix
      (**L-04**, **L-05**)
- [ ] The message names the token and a value, not just a count

**Open questions**
- **Report only, or write a default?** Recommendation: **report, and offer `--write` to insert the
  contract's stated default.** `sync` already inverts the report/write posture for exactly this
  reason — it cannot tell a version gap from a deliberate edit — and a theme value someone chose
  differently must not be overwritten. A missing declaration, though, is not a choice.

## 2. Plan

_Not planned._

## 3. Implement

_Not started._

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-16 | → proposed | Found by [T-128](T-128-publish-the-adopter-deck-as-a-worked-example.md) step 5, running the upgrade path on a real adopter deck for the first time. Worked around there by declaring the token by hand; raised here because the workaround is not the fix and the next adopter hits it too. |
