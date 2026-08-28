# DS-141's `request` licence cannot be used, because no rule lets a deck state the duration

| Field | Value |
| :--- | :--- |
| **Target** | `htmldeck` — Gábor's own repository, cloned under `C:\Work\AgentPlugins` |
| **Kind** | Defect |
| **Status** | `open` |
| **Found while** | Building the slide 2 entrance on `D4 — Executive Board Presentation`, on 2026-08-24 |
| **Version seen** | `0.6.0` |

## What happens

DS-141 caps an entry animation at 500 ms and grants four licences to exceed it, one of which is
**`request` — the deck's author asked for it**. The owner of this deck asked for a 1000 ms entrance
with an ease-in-out curve. There is no legal way to write it.

Three rules close every route:

| Route | Rule that closes it |
| :--- | :--- |
| Declare `--ground-dur:1000ms` in the theme region | **DS-013** — every token the theme contract names must be declared, and a token it does not name may not be. `theme.py` reports: *`--ground-dur` is declared and the contract does not name it — add a row or drop the token* |
| Write `animation: … 1000ms …` in `<style id="slides">` | **DS-010** — no theme-varying length outside the region. `theme.py` reports the whole declaration as the one offending literal |
| Reuse a declared dial | The nearest is `--pulse-dur`, 1.2 s, which is Pulse-once's dial and is paced for an emphasis mark rather than for an entrance. T-198 already recorded borrowing a neighbouring band as a defect |

The deck shipped the third route and recorded the deviation. The author's number is not what runs.

## Evidence

```
python tools/deck/theme.py check <deck>
```

with the token declared:

```
DS-013  every token THEME-CONTRACT.md names is declared and derives as it says:
        133 token(s) required, 2 problem(s)
        - --ground-dur is declared and the contract does not name it - add a row or drop the token;
          an undocumented dial is one a generator cannot set
```

and with the literal instead:

```
DS-010  no theme-varying length or easing curve outside the region:
        45 literal(s) scanned, 44 exempt, 1 offending
        - #slides .fig .verdict-no {animation:ground 1000ms var(--pulse-ease) var(--no-delay,0ms) both}
```

A custom property holding the same value — `--no-delay:120ms` — is exempt from DS-010 and passes.
That asymmetry is a second finding: the loophole is open for a delay and shut for a duration, and
neither is a decision anyone took.

## What is missing

A licensed motion needs somewhere to put its number. DS-141 says an author may ask for a longer
motion; nothing lets the author say **how long**.

## Proposed fix

Either add a **per-deck motion band** the theme contract names — one duration and one delay token
reserved for `--motion-long` rules, unset by default — or state in DS-010 that a duration inside a
rule declaring `--motion-long:request` is exempt, in the same sentence that exempts a custom
property. The first is better: it keeps the value where a generator can find it, which is the whole
argument DS-013 rests on.
