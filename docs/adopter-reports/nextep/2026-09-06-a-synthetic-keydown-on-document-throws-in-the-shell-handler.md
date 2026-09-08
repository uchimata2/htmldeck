# A synthetic `keydown` dispatched on `document` throws inside the shell's handler

> **Found 2026-09-06**, wiring a `Start` item into the More menu of the Nextep deck, against
> htmldeck `0.7.0`.

## What happens

The shell binds `Home` to `go(0)`. A per-deck control that wants the same behaviour has no
function to call — `go` lives inside the shell's IIFE — so the obvious route is to raise the key
the shell already listens for:

```js
document.dispatchEvent(new KeyboardEvent('keydown', {key:'Home', bubbles:true}));
```

Nothing happens, and nothing is reported. The handler opens with:

```js
document.addEventListener('keydown', function(e){
  if (e.target.matches('input,textarea')) return;
```

For a synthetic event dispatched on `document`, `e.target` **is** `document`, which has no
`matches`. The listener throws on its first statement, the exception is swallowed by the event
system, and the key never reaches the branch that would act on it.

## Why it is worth a line rather than a shrug

The guard is correct for real events, where `e.target` is always an element. It is the *first*
statement in the deck's only keyboard entry point, so any caller reaching it with a non-element
target loses every shortcut at once rather than one — and the failure looks like a dead button.

## The fix, either way round

- `if (e.target && e.target.matches && e.target.matches('input,textarea')) return;` — one guard,
  and the same shape the handler already uses three lines later for
  `e.target.closest && e.target.closest('.ruler-ticks')`.
- Or expose the navigation the chrome already performs, so a per-deck control has something to
  call rather than a key to fake.

The second is the better answer if a deck is expected to add chrome items at all, which
`0.7.0` made possible by turning the tail into a per-deck region.

## What this project did instead

Dispatched on `document.body`. It has `matches`, `closest('.ruler-ticks')` returns null, and the
event bubbles to the same listener. Proven with `render.py state --click "#startBtn"
--watch ".slide[data-stage='front']"`: hidden before, visible after.
