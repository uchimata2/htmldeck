---
tool: htmldeck
version: 0.6.0
date: 2026-09-01
severity: suggestion
---

# The nav chrome offers no clickable first-page or last-page control

## Expected

The presenter can jump to the first and the last page from the on-screen navigation — the
owner's request while reviewing a deck specification: a lobby and a colophon are the two pages
a presenter returns to on purpose, before the room fills and during questions.

## Actual

The keyboard already has both jumps; the pointer chrome has neither. The shell's key handler
maps `Home` to page 0 and handles `End` beside it, and the ruler's own key handler does the
same — but the visible chrome offers prev/next and the per-stage ruler ticks only, so a
presenter on a mouse or a presenter remote has no first/last control.

## Command that proves it

```bash
grep -n "'Home'" "$HTMLDECK/shell/deck.js"
```

Output measured on 0.6.0: hits at deck.js:280 (ruler keydown) and deck.js:534 (document
keydown, `go(0)`), with `End` handled beside each. No corresponding button or click target
exists in the shell's nav markup.

## Workaround used in this project

None needed yet — the deck is at specification. The presenter can use the keyboard's `Home`
and `End`.

## Suggested fix

Two small click targets at the ends of the ruler (or on the page counter), wired to the same
`go(0)` / `go(last)` the key handler already calls. The keyboard path shows the navigation
model already supports it; only the pointer affordance is missing.
