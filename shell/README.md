# shell — the half of a deck nobody rewrites

A deck is ~225 KB and roughly 170 KB of it is the same in every deck built here: three embedded
faces, the shared component block, the script, the chrome, the reading view. **That half cannot be
authored per run**, and a copy of it is a second home for a fact that already has one. So it lives
here, and [`tools/deck/shell.py`](../tools/deck/shell.py) puts it back.

```
python tools/deck/shell.py new <out.html> --title "..." --subtitle "..."
python tools/deck/shell.py preflight <deck> [--check]
python tools/deck/shell.py sync <deck> [--write]
python tools/deck/shell.py tokens <deck> [--write]
python tools/deck/shell.py check <deck>
python tools/deck/shell.py parts
```

**`sync` is the other direction of `check`, and it is the reason a release may touch this folder.**
The comparison below is byte for byte, so any change here fails every deck already built through no
fault of its author; `sync` cuts the deck's eleven regions out and fills the *installed* shell with
them, which is the same lossless operation that made `shell.html` in the first place. It reports
before it writes — a deck one release behind and a deck whose shell someone edited on purpose are
the same bytes, and nothing in a deck records which release built it. **T-124.**

**`tokens` is the half `sync` cannot carry.** Add a token to `components.css` and the block installs
cleanly while the *declaration* stays missing, because that lives in the deck's theme region and a
sync must not touch it — so the upgrade reports success and DS-013 fails afterwards on a token the
author never saw. `sync` and `check` now name them; `tokens --write` adds exactly the missing ones at
the shipped theme's values and never rewrites one already declared. **T-166.**

**It carries each band separately, and declines what it cannot carry. T-177.** A colour is
declared twice — once light, once dark — and reading the theme as one flat map kept whichever came
last, so the first new dual-band token since `tokens` shipped put the **dark** value in a deck's
light band and nothing in its dark one. `theme.py` passed it, because DS-013 asks whether a token
is declared and not whether it is declared at the right value in the right band. Both values are
written now, into this deck's own bands; a deck with no dark band to receive the second is told
which token was declined and why, rather than given half of it.

| File | What it is | Contracted by |
| :--- | :--- | :--- |
| `shell.html` | The structure — head, sprite, stage, chrome, reading view — with `{{SLOT}}` where a deck differs | [`../docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) |
| `components.css` | The shared component block: every element more than one slide can use | the same |
| `deck.js` | The deck script — scaling, navigation, disclosure, the ruler, the reading view | the same, §4 |
| `icons.svg` | 40 Lucide glyphs, ids by Lucide name. **DS-112 forbids hand-drawn icons and this is what makes that satisfiable** | DS-112, DS-113 |

The theme is not here. It has its own home in [`../themes/`](../themes) and its own contract, and
`shell.py new` resolves it in exactly as `theme.py swap` does.

## How it was made, and why that matters

`shell.html` was **cut out of [`../examples/reference-deck.html`](../examples/reference-deck.html)
losslessly** — ten regions replaced by slots, and putting them back reproduces the deck byte for
byte. It is not a description of that deck, it is that deck with the content removed, which is why
`shell.py check` can hold any deck to it:

```
python tools/deck/shell.py check examples/reference-deck.html
```

**That is the check worth running after every build batch.** It is the one that notices an edit
which strayed out of the slides and into the shared block — the failure a rules gate cannot see,
because a component block with one extra rule breaks no rule.

## The slots

Twelve, and nowhere else may a deck differ:

`TITLE` · `NOTE` · `THEME` · `COMPONENTS` · `PREFLIGHT` · `ICONS` · `SLIDES` · `CHROME_TAIL` ·
`DOC_TITLE` · `DOC_SUB` · `COMPOSITION` · `SCRIPT`

**`CHROME_TAIL` is the twelfth and the odd one (T-114).** The others hold what a deck *says*; this
one holds the chrome row's tail — `More`, its menu, and `Read` and `Motion` inside it. It is a
region rather than an element because it was built to hold a control whose **parent** varied:
DS-218 read *persistent* as forbidding a stop one click inside a shut menu, so a looping deck
lifted `Motion` out beside `.more`.

**The parent stopped varying on 2026-08-29** ([T-277](../tasks/T-277-put-motion-back-inside-the-more-menu.md)),
when the owner reversed that clause — 2.2.2 asks the stop be reachable while the motion runs, not
that it be zero clicks. **The slot stays, and the reason is now a different one**: a deck may reword
these three labels, so this is the one region `shell.py check`'s byte comparison must not own. What
guards it instead is `component.py`'s table and DS-218's surviving half, that the control and its
opener are present and reachable.

**Three of them nest inside `SCRIPT`**, and finding them is what this cut was worth: `DECK_NAME`,
`STAGES` and `STAGE_ICON` are per-deck facts that had been sitting in the middle of 560 invariant
lines, where nothing could see they were content.

## Two of them are derived, never declared

DS-113 wants only the icons a deck uses, which is a fact about the file rather than a thing to
remember, so `shell.py icons` reads the deck and rewrites the sprite to match. **Both kinds of
reference count** — `<use href="#i-x">` in the markup and `'i-x'` in the script — because the
reference deck names four of its nine icons only in a script array, and a markup-only scan deletes
them. Each symbol records the glyph it is in `data-icon`, so DS-112's *Lucide primary* is a claim
`check` can settle rather than a hope.

**`PREFLIGHT` is the same sentence about a different region** (DS-009). Which capability checks a
deck needs is a fact about its own bytes, so `shell.py preflight` reads the deck and emits the rows
it finds a subject for — the reference deck emits two and `sort-window` three, the difference being
the `<template>` row that its quick views need. [`tools/deck/preflight.py`](../tools/deck/preflight.py)
owns the table and `preflight.py rows` says why each row is a row; `check` reports a stale block the
way it reports a stale sprite.

**The degraded state is the other half of it and lives in the shell proper**, not in a slot: the
banner markup, `<html data-preflight>` authored on, the baseline-CSS block in `components.css`, and
the line in `deck.js` that stands the script down while the marker survives. That is what a browser
paints when the preflight names something missing, when no script runs, or when boot throws.
