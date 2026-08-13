---
id: T-120
title: printpages.py's own entry point defaults the slide count to a hardcoded 12, so it fails a correct deck
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-096, T-116]
work_package: PH1
owner: maintainer
business_value: medium
effort: xs
created: 2026-08-13
updated: 2026-08-13
shipped_in: 0.2.3
deliverables:
  - tools/deck/printpages.py
  - tools/deck/render.py
  - tools/check_all.py
  - docs/PUBLISHING.md
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

- **The override argument was removed, not kept** — the open question's recommendation, taken. It
  existed only to correct the constant by hand, and a second way to state a fact the deck already
  states is a second way to be wrong about it.
- **`render.slide_count` is the derivation, and it had to be fixed to be one.** It matched
  `class="slide` as a *prefix*, where the DOM count it now has to agree with matches `slide` as a
  class *token*. Two live disagreements: `class="close slide"` is a slide the prefix match missed,
  and `class="slide-note"` is not one that it took. Splitting the attribute is what `.slide` does,
  so the two cannot disagree by construction rather than by inspection. Neither case exists in a
  shipped deck today, which is why it was a latent disagreement and not a second bug report —
  the fix is what makes acceptance criterion 4 mean anything.
- **The agreement is asserted on fixture markup, not by rendering.** `render.self_test` counts a
  six-section fixture holding both wrong cases and expects 4. A self-test that launched Chrome to
  prove a file-read matches a DOM read would make the harness's own self-test cost a browser.
- **The count is printed on every run** (`slides: 13, counted in the deck`). The failure this task
  fixes was silent because nothing said where the number came from.
- **`check_all.py` keeps `printpages.py` in `NOT_RUN`, and the reason changed rather than the
  classification.** It was "its entry point is red on a correct deck"; it is now "the per-deck
  `check.py` line already evaluates `PRINT-1`, so running this too would print the same verdict from
  a second Chrome launch". The tool being broken was never the reason it was skipped, and leaving
  the old wording would have left a fixed defect documented as current.

**Outputs produced**
- [`tools/deck/printpages.py`](../tools/deck/printpages.py) — `main(deck)` derives the count; the
  second positional argument and the `12` are gone, including from the usage line.
- [`tools/deck/render.py`](../tools/deck/render.py) — `slide_count` matches a class token, with the
  fixture that pins it.
- [`tools/check_all.py`](../tools/check_all.py) and
  [`docs/PUBLISHING.md`](../docs/PUBLISHING.md) — both described the defect as current.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| `printpages.py examples/reference-deck.html` passes, and its `wanted` line agrees with `check.py --print-pages` | met | `printed pages: 14 declared, 14 counted, wanted 14 (13 slides + contents) pass` — the identical line `check.py --print-pages` prints for that deck. It read `wanted 13` and `FAIL` before. |
| The same command on `sort-window.html` still passes | met | `printed pages: 13 declared, 13 counted, wanted 13 (12 slides + contents) pass`. This deck passed under the constant too, by coincidence: it has 12 slides. |
| No slide count is written as a literal anywhere in the file | met | The `12` is gone from `main`, from the `__main__` block and from the usage line. The only integer left is `+ 1` for the contents page, which is the rule rather than a count. |
| The self-test asserts the two callers agree, so this cannot drift back silently | met | Asserted where the two could actually diverge: `render.self_test` counts a fixture of six `<section>`s — `slide`, `slide close`, `close slide`, `id` before `class`, `slide-note`, `contents` — and requires 4. Both of the old prefix match's errors are in it, so the fixture fails if the derivation stops meaning what `.slide` means. |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-13 | (no change) | **The owner added it to `0.2.3`**, which is now five tasks rather than the four committed to on 2026-08-12. The alternative was deferring it to an unscheduled `0.2.4`; a one-line fix parked behind a release nobody has scheduled is one the next adopter reports. |
| 2026-08-13 | → proposed | Raised by T-096's first run of the checkers the gate list omits — the run that command exists to make possible. `PH1` rather than the `PH3` default: a shipped checker returning a false FAIL on a conforming deck is T-105's class, and this one is a stored constant against a rendered fact (**L-08**). `xs`; `medium` rather than `high` because `check.py --print-pages` already gets the right answer and T-096 now passes that flag, so the count is covered while this is open. |
| 2026-08-13 | → specified | §1 was already complete, including the recommendation on the override. |
| 2026-08-13 | → planned | §2 was already complete and unchanged. |
| 2026-08-13 | → in_progress | Step 1 needed `render.slide_count` fixed before it could be the derivation: it matched `class="slide` as a prefix where the DOM matches `slide` as a class token, so adopting it as-is would have made the two callers agree on today's decks and disagree on a deck writing `class="close slide"`. Latent rather than reported, and fixing it is what makes acceptance criterion 4 an assertion instead of a coincidence. |
| 2026-08-13 | → done | Four criteria met. Both shipped decks pass standalone and print the same `wanted` line as `check.py --print-pages`. Two documents that described the defect as current were corrected — `check_all.py`'s skip reason and `PUBLISHING.md` §8 — because a fixed defect left documented is the next reader's wrong fact. |
| 2026-08-13 | (no change) | **Shipped in `0.2.3`**, tagged `v0.2.3`. `python tools/check_all.py` green on the tagged tree: 19 ran, 1 skipped with its reason, 0 failed. |
