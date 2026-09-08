---
tool: htmldeck
version: 0.7.0
date: 2026-09-07
severity: suggestion
---

# `density.py write` ranks only the rule that starts the motion, and says nothing when it finds none

## Expected

A deck declares `--motion-kind: content` on the class it animates, and `density.py write` gives that
class's elements a `--m-rank` so `--m-on` can resolve.

## Actual

`density.py` reads the declarations off **the rule that starts the motion** — the one carrying
`animation` or `transition` — and ignores a `--motion-kind` sitting on any other rule for the same
class. That is defensible, and it is invisible: an author who declares the motion vars on a base
rule (`.dot{fill:…;--motion-kind:content}`) and the animation on a state rule
(`.stage[data-state="active"] .dot{animation:…}`) gets **no rank written and no message**.

An unranked element takes `--m-rank`'s fallback of `101`, so
`--m-on: max(0,min(1,calc(var(--motion-density) - 101 + 1)))` computes to `0` at every density. The
motion then runs for zero seconds and, where the author also gated visibility on `--m-on`, the
element is invisible in a deck whose motion is fully on. Nothing fails.

The only signal is the summary count, and it only helps an author who already knows what it should
be: the deck went from `8 content motion(s) ranked` to `13` when the three declarations moved onto
the animating rule. Five elements had silently had none.

## Command that proves it

```bash
python tools/deck/density.py write deck/nextep.html
grep -o -- '--m-rank:[0-9]*' deck/nextep.html | sort -u
```

Measured 2026-09-07: with `--motion-kind` on the base rule, `8 content motion(s) ranked` and no rank
on any `.wdot` element. With the same three declarations moved onto the rule carrying `animation`,
`13 content motion(s) ranked` and the five dots at ranks 62 to 93.

## Suggested

Print a line per class that declares `--motion-kind` and receives no rank — one sentence naming the
class and the rule it was found on. The information is already in hand at that point, and it turns a
silent zero-duration motion into a build message.
