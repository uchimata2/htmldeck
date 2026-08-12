---
id: T-120
title: printpages.py's own entry point defaults the slide count to a hardcoded 12, so it fails a correct deck
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-096, T-116]
work_package: PH1
owner: maintainer
business_value: medium
effort: xs
created: 2026-08-13
updated: 2026-08-13
deliverables: [tools/deck/printpages.py]
---

# T-120 — printpages.py's own entry point defaults the slide count to a hardcoded 12, so it fails a correct deck

## 1. Specify

**Outcome**
`python tools/deck/printpages.py <deck>` derives the slide count from the deck in front of it, the
way `check.py` does when it calls the same function, instead of from a constant written in 2026.

**Why this one**
The two callers of `printpages.verdicts` disagree about the same deck, and only one of them is
right:

```
python tools/deck/printpages.py examples/reference-deck.html
  PRINT-1  printed pages: 14 declared, 14 counted, wanted 13 (12 slides + contents) FAIL

python tools/deck/check.py examples/reference-deck.html --sources examples/sources --print-pages
  PRINT-1  printed pages: 14 declared, 14 counted, wanted 14 (13 slides + contents) pass
```

`check.py` passes `data["slideCount"]` from the render. The standalone entry point passes
`int(a[1]) if len(a) > 1 else 12` — a **stored copy of a derivable fact**, which is **L-08**, and it
drifted the day the reference deck gained its `slide close` colophon. The deck prints 14 pages and
is correct at 14; the constant is what is wrong.

**It is a false FAIL on a conforming deck, from a file the plugin ships.** That is the class
[T-105](T-105-fig-pos-neg-caution-are-vocabulary-so-a-real-deck-fails-for-using-them.md) settled as
`PH1` — a published gate failing a deck that conforms is a defect in the check — so this takes `PH1`
by [`../CLAUDE.md`](../CLAUDE.md)'s rule rather than the `PH3` default, and adds a fifth task to
`0.2.3`.

**Found by [T-096](T-096-one-command-that-runs-every-checker-and-says-what-it-skipped.md)**, on the
first run of every checker the release gate list does not run. Nothing in the sixteen commands
`0.2.1` and `0.2.2` were cut on reaches it: `printpages.py` has no line of its own in
[`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) §8, and `check.py` evaluates `PRINT-1` only under
`--print-pages`, which that list never passed. **So the printed page count has been checked by
nothing since it was written.**

**Scope**
- In: the standalone entry point's slide count, derived from the deck.
- In: the second positional argument, which is now the only way to get a right answer and should
  become an override or go.
- Out: the page count's rule. `PRINT-1` is right, and T-116 records that it read `n` + 1 correctly
  throughout while the page it counted was broken.
- Out: what a "slide" is. `figures.py` counts `class="slide"` and gets 12, the render counts every
  `.slide` and gets 13, and the README's figure is the first of those. Both are defensible answers
  to different questions; this task only stops one file answering from memory.

**Inputs**
- [`../tools/deck/printpages.py`](../tools/deck/printpages.py) — `main` and the `__main__` block.
- [`../tools/deck/check.py`](../tools/deck/check.py) — the caller that gets it right, at the
  `printpages.verdicts` call.
- [`../tools/deck/render.py`](../tools/deck/render.py) — where `slideCount` comes from.

**Acceptance criteria**
- [ ] `python tools/deck/printpages.py examples/reference-deck.html` passes, and its `wanted` line
      agrees with `check.py --print-pages` on the same deck
- [ ] The same command on `examples/sort-window/sort-window.html` still passes
- [ ] No slide count is written as a literal anywhere in the file
- [ ] The self-test asserts the two callers agree, so this cannot drift back silently

**Open questions**
- Keep the second positional argument as an explicit override, or remove it? *Recommend removing it:
  the only reason it existed was to correct the constant, and an override is a second way to be
  wrong about a fact the deck states.*

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Read the slide count from the render in the `__main__` block, as `check.py` does | the fix |
| 2 | Assert both callers agree, in the self-test | evidence it cannot drift back |
| 3 | Run it against both shipped decks, and against `check.py --print-pages` | four verdicts |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

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
| 2026-08-13 | (no change) | **The owner added it to `0.2.3`**, which is now five tasks rather than the four committed to on 2026-08-12. The alternative was deferring it to an unscheduled `0.2.4`; a one-line fix parked behind a release nobody has scheduled is one the next adopter reports. |
| 2026-08-13 | → proposed | Raised by T-096's first run of the checkers the gate list omits — the run that command exists to make possible. `PH1` rather than the `PH3` default: a shipped checker returning a false FAIL on a conforming deck is T-105's class, and this one is a stored constant against a rendered fact (**L-08**). `xs`; `medium` rather than `high` because `check.py --print-pages` already gets the right answer and T-096 now passes that flag, so the count is covered while this is open. |
