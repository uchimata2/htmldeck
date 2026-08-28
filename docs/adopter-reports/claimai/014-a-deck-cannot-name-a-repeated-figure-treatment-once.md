# A deck cannot name a repeated figure treatment once, and DS-229 does not say so

| Field | Value |
| :--- | :--- |
| **Target** | `htmldeck` — Gábor's own repository, cloned under `C:\Work\AgentPlugins` |
| **Kind** | Feature |
| **Status** | `open` |
| **Found while** | Drawing fifteen inline marks across four slides of `D4 — Executive Board Presentation`, on 2026-08-25 — `E62 — Draw round 2's new icons as one set` |
| **Version seen** | `0.6.0` |

## What happens

Fifteen marks were drawn into four slides. Eleven of them share one stroke width, one cap and one
join, so they were given a class holding those three properties:

```css
.fig .ico{stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
```

DS-229 failed it:

```
DS-229   every class the shared block styles has a row: 101 styled, 1 uncontracted - .ico   FAIL
```

`component.py` reads every class in the unnamed `<style>` block and holds it against
`docs/COMPONENT-CONTRACT.md`. The contract is the plugin's, so **a deck may not add a class at all.**

## What is missing

Two things, and they are separable.

**1. The message names the failure and not the remedy.** It says `.ico` is uncontracted. It does not
say that no deck-authored class can ever be contracted, nor that presentation attributes are the
route. A builder reads *uncontracted* as *not yet in the contract* and goes looking for where to add
the row — the contract lives in the plugin, so the search ends nowhere. That cost one full check
cycle here, and it will cost every deck the same one.

**2. A deck has no way to name a repeated figure treatment once.** The route that works is
attributes on each element:

```html
<g class="quiet-s" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" transform="…">
```

That is correct and it is what the sprite's own `<symbol>` elements do. But it is stated eleven
times here, and a twelfth mark would state it a twelfth. The deck's *own* repeated treatments are
exactly the thing a class is for, and the one mechanism for them is closed.

Note the interaction that makes the workaround safe, because it is not obvious: `.quiet-s` and
`.accent-s` set only `stroke` and `fill`, so an attribute setting `stroke-width` does not lose to
them. `deck.html:3073` already carries a comment about the opposite case — *"a class rule beats a
presentation attribute"* — so the safety here is a property of these two classes, not a general one.

## Proposed fix

In increasing order of cost.

1. **Say what to do, in the message.** Where a class fails the contract, add one clause:
   *"a deck may not add a class; carry the properties as presentation attributes on the element."*
   This is a string change and it removes the whole dead-end search.
2. **Reserve a deck-local prefix.** Let a deck declare classes under an agreed prefix — `d-`, say —
   and have DS-229 skip them while still holding every contracted class to its row. The rule keeps
   its real job, which is stopping a deck from redefining a *component*, and stops policing a deck's
   own figure internals, which no component contract can anticipate.
3. **Extend the contract with a figure-internals section.** Most expensive, and probably wrong: the
   set of treatments a hand-built figure needs is open, so the contract would chase it forever.

The first is worth doing whatever happens to the second. The second is the real gap.

## What this is not

Not a request to weaken DS-229 over components. Holding `.slide`, `.headline` or `.sources-box` to a
contract is the rule earning its keep — a deck that redefines one of those breaks the shell. The
argument here is only that a mark drawn inside `svg.fig` is not a component, and today the rule
cannot tell the two apart.
