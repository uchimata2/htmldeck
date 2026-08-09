# shell — the half of a deck nobody rewrites

A deck is ~225 KB and roughly 170 KB of it is the same in every deck built here: three embedded
faces, the shared component block, the script, the chrome, the reading view. **That half cannot be
authored per run**, and a copy of it is a second home for a fact that already has one. So it lives
here, and [`tools/deck/shell.py`](../tools/deck/shell.py) puts it back.

```
python tools/deck/shell.py new <out.html> --title "..." --subtitle "..."
python tools/deck/shell.py check <deck>
python tools/deck/shell.py parts
```

| File | What it is | Contracted by |
| :--- | :--- | :--- |
| `shell.html` | The structure — head, sprite, stage, chrome, reading view — with `{{SLOT}}` where a deck differs | [`../docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) |
| `components.css` | The shared component block: every element more than one slide can use | the same |
| `deck.js` | The deck script — scaling, navigation, disclosure, the ruler, the reading view | the same, §4 |
| `icons.svg` | 38 Lucide glyphs, ids by Lucide name. **DS-112 forbids hand-drawn icons and this is what makes that satisfiable** | DS-112, DS-113 |

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

Ten, and nowhere else may a deck differ:

`TITLE` · `NOTE` · `THEME` · `COMPONENTS` · `ICONS` · `SLIDES` · `DOC_TITLE` · `DOC_SUB` ·
`COMPOSITION` · `SCRIPT`

**Three of them nest inside `SCRIPT`**, and finding them is what this cut was worth: `DECK_NAME`,
`STAGES` and `STAGE_ICON` are per-deck facts that had been sitting in the middle of 560 invariant
lines, where nothing could see they were content.

## The sprite is derived, never declared

DS-113 wants only the icons a deck uses, which is a fact about the file rather than a thing to
remember, so `shell.py icons` reads the deck and rewrites the sprite to match. **Both kinds of
reference count** — `<use href="#i-x">` in the markup and `'i-x'` in the script — because the
reference deck names four of its nine icons only in a script array, and a markup-only scan deletes
them. Each symbol records the glyph it is in `data-icon`, so DS-112's *Lucide primary* is a claim
`check` can settle rather than a hope.
