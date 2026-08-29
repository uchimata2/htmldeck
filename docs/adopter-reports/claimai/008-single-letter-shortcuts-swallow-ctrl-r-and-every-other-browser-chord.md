# The single-letter shortcuts have no modifier guard, so Ctrl-R toggles the view instead of reloading

| Field | Value |
| :--- | :--- |
| **Target** | `htmldeck` — Gábor's own repository, cloned under `C:\Work\AgentPlugins` |
| **Kind** | Defect |
| **Status** | `closed` — closed 2026-08-29 by [T-268](../../../tasks/T-268-three-chrome-and-timing-defects-in-deck-js.md). **Taken as proposed.** The keydown handler returns on `ctrlKey`, `metaKey` or `altKey` before it reads the key, so every browser chord built on the six letters reaches the browser. **Shift is deliberately not one of the three**: the handler accepts `R` as well as `r`, so Shift is part of how these shortcuts are typed and guarding on it would break the capital form of all six. `DS-131` now says the shortcuts are unmodified keys, so the rule carries the reason rather than the code alone. Measured in a browser on a deck built from the edited shell: Ctrl-R neither entered the reading view nor was `preventDefault`ed, Ctrl-F neither went fullscreen nor was prevented, and bare `r` still enters the reading view and still leaves it. |
| **Found while** | Round 2 of the deck review on `D4 — Executive Board Presentation`, on 2026-08-25. Reported by the presenter, who uses Ctrl-R to refresh while building |
| **Version seen** | `0.6.0` |

## What happens

`shell/deck.js` binds six single-letter shortcuts on `keydown`. The handler reads `e.key` and never
looks at the modifiers:

```js
document.addEventListener('keydown', function(e){
  if (e.target.matches('input,textarea')) return;
  var k = e.key;
  ...
  else if (k === 'r' || k === 'R')  { setView(true); e.preventDefault(); }
  else if (k === 'm' || k === 'M')  { setMotion(root.dataset.motion === 'off'); }
  else if (k === 't' || k === 'T')  { setTheme(...); }
  else if (k === 'f' || k === 'F')  { ... requestFullscreen() ... }
});
```

`shell/deck.js:519–547`, and the same shape at `:529` for the reading view's own Escape / `r` branch.

Pressing **Ctrl-R** sets `e.key` to `'r'`. The branch matches, the deck switches into the reading
view, and `e.preventDefault()` cancels the reload the user asked for. The user's own words: *htmldeck
binds Ctrl-R to the read / presentation toggle. Remove it; I use it to refresh.*

It is not only Ctrl-R. Every browser chord built on one of these six letters is captured the same way:

| Chord | What the user wanted | What the deck does |
| :--- | :--- | :--- |
| Ctrl-R / Cmd-R | Reload | Enters the reading view, reload cancelled |
| Ctrl-F / Cmd-F | Find on page | Goes fullscreen |
| Ctrl-D / Cmd-D | Bookmark | Toggles the current slide's disclosure |
| Ctrl-T, Ctrl-M | New tab, minimise | Toggles theme, toggles motion |

`Ctrl-F` is the worst of them for a reader: the browser's find bar is how anyone searches a long
reading view, and it silently becomes a fullscreen toggle instead.

## Evidence

Open any built deck, put focus anywhere outside an input, and press Ctrl-R. The view toggles and the
page does not reload. The handler above is the whole of it — there is no modifier test anywhere in
the file:

```
grep -n "ctrlKey\|metaKey\|altKey" shell/deck.js
```

returns nothing.

## What is missing

A shortcut that spells `r` should fire on `r`, not on every chord that happens to contain `r`. The
browser's own chords must reach the browser.

## Proposed fix

One line, beside the guard that is already there:

```js
if (e.target.matches('input,textarea')) return;
if (e.ctrlKey || e.metaKey || e.altKey) return;      /* browser chords are the browser's */
```

Shift is deliberately not in that list — the handler already accepts `R` as well as `r`, so a
capital letter must keep working.

`DESIGN-SYSTEM.md`'s keyboard section should also say that the single-letter shortcuts are
unmodified only. As written, a reader would not expect Ctrl-F to be swallowed.
