---
tool: htmldeck
version: 0.7.0
date: 2026-09-07
severity: defect
---

# The reader's Motion control does not stop a motion the deck wrote

## Expected

`DS-218` obliges a looping content motion to be stoppable, and the chrome's Motion control is the
stop. A reader who turns motion off gets a still page.

## Actual

The control sets `:root[data-motion="off"]`, and the shell then applies that state to its **own
contracted classes by name** — `.current`, `.rise`, `.pulse`, `.opening`, `.turn`, `.arrow-pop`,
`.dot-pop`. A class the deck invented is in none of those selectors, so a deck-authored animation
keeps running with motion off, and `DS-218` still passes because the control exists.

This is the mirror of the finding already filed as
[a deck-authored content motion gets no motion gate](2026-09-07-a-deck-authored-content-motion-gets-no-motion-gate.md):
there a deck motion inherits no `--m-on` and runs for zero seconds; here it inherits no stop and
never ends. `--motion-density` and `data-motion` are two different switches, and a deck author who
wires the first reasonably believes the second is handled.

Measured on this project's own deck: a looping `offset-path` animation on a slide-authored class ran
unchanged under `data-motion="off"` until the deck wrote its own rule.

## Command that proves it

```bash
grep -n 'data-motion="off"' "$HTMLDECK/shell/deck.css"
```

Every hit names a shell class. Then, in a browser on any deck with a deck-authored animation:

```js
document.documentElement.setAttribute('data-motion','off');
getComputedStyle(document.querySelector('.your-animated-class')).animationName
```

Measured 2026-09-07 on nextep.html before the deck's own rule existed: `worbit`, still running.
After `:root[data-motion="off"] .wdot{animation:none;opacity:0}`: `none`, and opacity `0`.

## Suggested

Either a blanket `:root[data-motion="off"] *{animation:none !important}` inside the stage, or a
contracted marker — an element carrying `--motion-long` gets stopped whatever its class is — so the
obligation lands where the declaration already is. Failing that, `check.py` could fail a rule that
declares `--motion-long` and has no `data-motion="off"` counterpart, which is the cheapest fix and
turns a silent gap into a gate finding.
