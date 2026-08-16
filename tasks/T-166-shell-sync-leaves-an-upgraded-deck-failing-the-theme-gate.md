---
id: T-166
title: shell.py sync leaves an upgraded deck failing the theme gate, and says nothing
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-124, T-106, T-128]
work_package: PH1
shipped_in: unreleased
owner: the project owner
business_value: high
effort: s
created: 2026-08-16
updated: 2026-08-16
deliverables:
  - tools/deck/shell.py
  - skills/htmldeck/references/build.md
  - shell/README.md
  - docs/lessons/L-108.md
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

**The open question is settled, and the recommendation was taken with one change.** Report, and
offer a write — but **not from `sync`**. `sync`'s whole claim is that every per-deck region comes
through untouched; it asserts that on the adopter's own file and refuses to write if one moved. The
theme region is a per-deck region, so a `sync --write` that inserted a declaration would be spending
the sentence the command is trusted for to buy one token. The write goes to a separate command with
a narrower promise. That reasoning is [`L-108`](../docs/lessons/L-108.md).

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | `undeclared_tokens(html)` — the contract's tokens the deck's theme region does not declare, read the same way `DS-013` reads it | one function, and what it reports cannot drift from what the gate fails on |
| 2 | `sync` reports them, from the **synced** deck, and still writes nothing into the theme | the adopter is told at the moment of upgrade |
| 3 | `check` reports them too | a deck synced before this existed is not silent either |
| 4 | `shell.py tokens <deck> [--write]` — reports, and on `--write` adds **only** what is missing, at the shipped theme's value, in one marked block | the fix an adopter can run |
| 5 | A fixture: a deck one release behind in exactly one token, and the tool shown failing on it before the change | **L-04**, **L-05** |
| 6 | The documented upgrade path gains the step | `build.md`, `shell/README.md` |

## 3. Implement

**Decisions & assumptions**
- **The open question, settled 2026-08-16: report from `sync`, write from a new `tokens` command.**
  The recommendation in §1 was *report, and offer `--write` to insert the contract's stated default*.
  Both halves stand; only the command changed, because `sync --write` cannot insert into a per-deck
  region without contradicting the guarantee it asserts three lines earlier. `tokens --write` only
  ever **adds**, so it needs no such guarantee.
- **The default value comes from the shipped theme, not from the contract.** The contract's *Legal*
  cell is a band, not a value — `--qv-measure` has no stated default there. `themes/quarto.css` is
  what `new()` builds every deck from, so its declaration is the default a deck would have had. A
  token the shipped theme has no value for is reported and **not** written: there is nothing to copy
  and inventing a number that fits one deck is **L-38**.
- **A token already declared is never read, let alone rewritten.** A value someone chose and a
  version gap are the same bytes — the same reason `sync` reports first.

**Outputs produced**
- [`tools/deck/shell.py`](../tools/deck/shell.py) — `undeclared_tokens`, `declare_tokens`,
  `token_report`, the `tokens` command, the report in `sync` and the `TOKENS` row in `check`, and
  eight fixtures.
- [`skills/htmldeck/references/build.md`](../skills/htmldeck/references/build.md) and
  [`shell/README.md`](../shell/README.md) — the upgrade path gains its missing step.
- [`docs/lessons/L-108.md`](../docs/lessons/L-108.md) and its index row.

**The tool shown failing before the fix.** `HEAD`'s `shell.py` and the working tree's were loaded
side by side and asked the same question about the same bytes — a deck built by `new()` with one
token declaration removed:

```
HEAD (before the fix)    shell.py check -> PASS - says nothing
working tree (after)     shell.py check -> 1 problem(s): TOKENS ... 1 token(s) THEME-CONTRACT.md
the gate, either way     theme.py       -> 1 problem(s): --qv-measure not declared
working tree (after)     tokens --write -> added [('--qv-measure', '80rem')]; check now clean
```

**And end to end, on a deck rather than a fixture.** A scratch copy of `measure-first` with the
hand-declared token removed — which is exactly the 0.2.2-era deck T-128 met:

| Step | Before this task | After |
| :--- | :--- | :--- |
| `shell.py sync` | *OK — already carries the installed shell* | names `--qv-measure`, gives `80rem`, writes nothing, exits 1 |
| `theme.py check` | `DS-013 FAIL … 1 problem(s)` | — |
| `shell.py tokens --write` | did not exist | *1 declaration(s) added* |
| `theme.py check` after | — | `DS-011 pass`, `DS-013 pass — 117 token(s) required, 0 problem(s)` |
| `shell.py check` after | — | OK |

No deck in this repository changed. `measure-first`'s hand declaration from T-128 stands: it is the
same value this command would write, and rewriting it to prove a point is not a reason to touch a
shipped file.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A deck at 0.2.2 synced to the current release either passes `theme.py check` afterwards, or is told by `sync` exactly which tokens to declare | met, second limb | `sync` names the token, gives the value and exits 1 rather than 0. It still does not write into the theme region, and that is the decision above rather than a shortfall |
| A fixture holds a deck missing a required token, and the tool is shown to fail without the fix | met | Eight fixtures in `self_test`, and the before/after run above: `HEAD` calls the seeded deck clean, the working tree names the token. 52 of 52 fixtures pass |
| The message names the token and a value, not just a count | met | `--qv-measure  shipped theme declares 80rem`, one line per token, from `token_report` — used verbatim by `sync`, `check` and `tokens`. A token the shipped theme has no value for says so instead of printing a blank |

**Nothing this task produced renders**, which is why it was in the unattended batch — the deliverable
is a report and a CSS declaration whose value every deck here already carries. The one thing that
*could* be looked at is a quick-view sheet on a deck that was missing the token, and there is no such
deck in this repository: the scratch copy was `measure-first`, whose sheet already rendered at
`80rem` because T-128 declared it by hand. `TASK-WORKFLOW.md` §7 step 3 is not owed here, and no
browser was launched.

**Regression surface.** `python tools/check_all.py`: **25 checkers ran, 1 failed** — `figures.py`,
which is [T-172](T-172-the-shell-sync-falsified-four-published-deck-figures.md) and predates this.
`shell.py check` on all three shipped decks: OK. The two files that already failed it —
the seeded-defects fixture and `shell/shell.html`, neither of which is a deck it applies to — fail
with the same rows as before and no `TOKENS` row.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-16 | → done | Specified, planned, implemented and reviewed in one unattended pass. **All three criteria met**, the second limb of the first one by decision rather than by shortfall. **The open question was settled here and not handed back**: report from `sync`, write from a new `tokens` command — the recommendation's substance, moved off the command whose guarantee it would have cost. That trade is the transferable half and is [`L-108`](../docs/lessons/L-108.md): a tool's refuses-to-touch rule defines a class of change it cannot complete, and the answer is to name the gap rather than weaken the rule. **§7 step 3 is not owed** — nothing here renders, and the one deck that could be looked at does not exist in this repository. |
| 2026-08-16 | → proposed | Found by [T-128](T-128-publish-the-adopter-deck-as-a-worked-example.md) step 5, running the upgrade path on a real adopter deck for the first time. Worked around there by declaring the token by hand; raised here because the workaround is not the fix and the next adopter hits it too. |
