# DS-229 keys the component contract's motion rows to exact selector text, so any prefix silently breaks them

| Field | Value |
| :--- | :--- |
| **Target** | `htmldeck` — Gábor's own repository, cloned under `C:\Work\AgentPlugins` |
| **Kind** | Defect |
| **Status** | `open` |
| **Severity** | Medium — the correct CSS for a common need takes the gate from four failures to five, and the failure names the wrong thing |
| **Found while** | Deciding whether figure motion should play on arrival, on 2026-08-26 — `E68` |
| **Version seen** | 0.6.0 |

## What happens

The component contract carries one row per motion, keyed on the selector **as written** — for
example `` `.pulse` ``, which owes `--pulse-dur`, `--pulse-ease` and `--pulse-delay`.

`DS-229` finds that row by matching the selector text. A deck that scopes the same rule to a state:

```css
:where(.slide[data-played]) .pulse { ... }
```

no longer has a selector the contract can find. The tokens are still declared, the motion still
works, and the gate reports the contract row as unsatisfied. Building it that way took this deck
from four failing rules to **five**.

**The workaround is not obvious and had to be found by bisection.** Keep the contracted selector
exactly as written, then add a separate `:where()` rule *later in the file* that switches the motion
off. Same result, opposite construction, and nothing in the failure suggests it.

## Why it matters

Scoping a motion to a state is the ordinary way to express *this plays on arrival*, which is what the
author asked for. A rule that makes the natural construction fail, and the awkward one pass, teaches
the awkward one.

## What to change

1. **Match the contract row on the compound selector, not the selector text** — `.pulse` should be
   found inside `:where(...) .pulse` and inside `.slide[data-played] .pulse`.
2. **If exact-text matching is deliberate, say so in the failure.** The verdict should read *the
   contract's `.pulse` row matched no rule; `.pulse` appears prefixed at line N* rather than reporting
   missing tokens that are in fact declared.

## Related

- [`014-a-deck-cannot-name-a-repeated-figure-treatment-once.md`](014-a-deck-cannot-name-a-repeated-figure-treatment-once.md)
  — the other `DS-229` finding. That one is the rule refusing a class the deck needed; this one is
  the rule failing to find a class the deck kept.
