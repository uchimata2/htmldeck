# A deck-authored content motion gets no `--m-on`, so it runs for 0s and only ever snaps

**Found** 2026-09-07 building `deck/nextep.html` on htmldeck `0.7.0`.
**Severity** silent wrong result. Every animation a deck writes for itself plays for zero seconds,
lands on its end state, and looks like a snap. No check fails.

## What the shell contracts

The shared block gates a content motion by multiplying its duration, and defines the multiplier on
the contracted components only:

```css
.pulse,.arrow-pop,.dot-pop,.turn{
  --m-on:max(0,min(1,calc(var(--motion-density) - var(--m-rank,101) + 1)))}
```

`--m-on` is not inherited from anywhere else, and `build.md` shows the duration idiom
`animation-duration:calc(var(--m-on,0) * var(--long-dur))` without saying that a deck-authored rule
must declare `--m-on` itself. A deck that copies the idiom onto its own class takes the `var()`
fallback of `0` on every frame.

## The command that proves it

With the deck open, and the arrival mark forced so the rule matches:

```js
document.querySelectorAll('.slide').forEach(s => s.setAttribute('data-arrived',''));
const c = getComputedStyle(document.querySelector('<your animated class>'));
[c.animationName, c.animationDuration, c.getPropertyValue('--m-on')]
```

Measured before the fix, on three deck-authored rules: `["scanfade", "0s", ""]`,
`["zerowiggle", "0s", ""]`, `["decayrise", "0s", ""]`. `--m-on` is the empty string — the property
is not set on the element — so `var(--m-on,0)` resolves to `0` and the duration to `0s`.

## Why it is invisible

A zero-duration animation still applies its fill state, which is the behaviour the shared block's
own comment relies on. So the element lands correctly and nothing looks broken enough to
investigate: with `animation-fill-mode: both` and a delay, the element holds its FROM state for the
delay and then snaps. Three separate readings of that snap were reported by the deck's owner as
three different defects - a colour changing back and forth, a wiggle that never happened, and marks
that blinked in order instead of rising.

## The fix on the deck side

Declare the same expression on the deck's own animated classes:

```css
.scanfound,.scanzero-num,.decaymark,.decaycall{
  --m-on:max(0,min(1,calc(var(--motion-density) - var(--m-rank,101) + 1)))}
```

## The fix worth making upstream

Either `build.md` states the requirement beside the duration idiom, or the shared block sets
`--m-on` on `.slide` so every descendant inherits a gate derived from its own `--m-rank`. The second
costs nothing: an element with no rank already falls back to `101`, which outranks every density,
so an unranked motion still does not move.
