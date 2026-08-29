# DS-141's `request` licence cannot be used, because no rule lets a deck state the duration

| Field | Value |
| :--- | :--- |
| **Target** | `htmldeck` — Gábor's own repository, cloned under `C:\Work\AgentPlugins` |
| **Kind** | Defect |
| **Status** | `closed` — closed 2026-08-29 by [T-264](../../../tasks/T-264-ds-141s-request-licence-has-nowhere-to-put-its-number.md). **Both findings taken, and the first by the better of the two candidates the record offers.** The theme contract names a licensed long band — `--long-dur`, `--long-ease`, `--long-delay` — under a new `optional` kind, so a deck that runs such a motion declares them in its own theme region and a deck that does not declares nothing. **The easing token is this repository's addition**: §3.6 requires every named motion to carry a curve, and without it a `cubic-bezier()` outside the region would trip DS-010's other half, so the record's *1000 ms with an ease-in-out curve* would still have been unwritable. **The asymmetry is closed the other way round from the obvious one**: a custom property is now scanned like any other declaration and §5's exemption table decides it, rather than every custom property being skipped on a comment claiming another rule owned the defect — no rule did. All three routes this record names were re-run as fixtures and each reproduces its verdict: the literal fails DS-010 on the same declaration, the invented token fails DS-013 with the same message, and the band route passes DS-013, DS-010 and DS-141 while the same rule without `--motion-long` fails DS-141. |
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
