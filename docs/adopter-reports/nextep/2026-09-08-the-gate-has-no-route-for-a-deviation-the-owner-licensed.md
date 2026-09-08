---
tool: htmldeck
version: 0.7.0
date: 2026-09-08
severity: request
---

# The gate has no route for a deviation the deck's owner licensed, so every adopter wraps it

## Expected

A deck's owner sometimes rules that a rule does not apply to this deck — a drawing that *is* the
content, a question that is the deck's own topic, a demonstration that has to reach a service. The
ruling is an editorial act, and `check.py` is the instrument that should record it: the deck states
what it deviates from and why, the gate reports those deviations as licensed, and **anything else
still fails**. What a gate is for is telling a licensed deviation from an unnoticed one.

## Actual

`check.py` has one exit code and no waiver. A deck with three ruled deviations is red forever, so
the gate stops being a signal and the adopter builds a second gate around it.

Run on 0.7.0, 2026-09-08, against this project's delivered deck:

```bash
python <htmldeck>/tools/deck/check.py deck/nextep.html --quiet
```

```
3 failure(s): DS-110, DS-100, DS-005
    DS-110  no raster the deck produces; a quoted source may be raster inside a quick view,
            and decoration may be raster outside a slide's `.body` if it carries no role=img
    DS-100  no rhetorical questions in slide copy
    DS-005  every fetch-like call names an inline URL: 1 site(s), 0 not a literal,
            1 naming a path - fetch('http://127.0.0.1:8642/run')
```

Exit 1. Each of the three is a ruling, not a defect:

| Rule | What the deck does | Who ruled it |
| :--- | :--- | :--- |
| `DS-110` | The lobby carries the owner's own pencil drawing as a raster on the slide's face | the deck's owner, in the approved specification |
| `DS-100` | The deck's topic is a question — *Where is the truth?* — quoted on the lobby and at the close | the same specification's title line |
| `DS-005` | One slide re-derives the project's own result from a local service on `127.0.0.1`, and replays a recorded run when it is absent | a project agreement licensing local scripts for this deck |

## What it costs, measured

The adopter writes the missing mechanism. This project's `tools/deck.ps1` holds a list of three
rule ids and a regular expression over `check.py`'s prose:

```powershell
$exceptions = @('DS-110', 'DS-100', 'DS-005')
$m = [regex]::Match($text, '(\d+) failure\(s\): ([^\r\n]+)')
```

It re-implements three behaviours the gate should own: a deviation passes only if it is on the
list, **a rule outside the list still fails**, and **a listed rule that stops failing is reported as
retired** so the list cannot quietly overstate the deck. That wrapper is 40 lines, it parses a
human-readable summary line that no contract fixes, and every adopter writes its own version.

## Prior art in the reports htmldeck already holds

Three ClaimAI records ask for the escape hatch one rule at a time —
`011` (DS-110 cannot tell a rasterised diagram from a drawing), `023` (DS-100 fires on any `?`
meeting a tag) and `024` (DS-202 refuses a two-sentence bottom line the author chose). `023` was
answered by narrowing the rule, which was the right answer for that rule and does not generalise:
this deck still fails DS-100 **after** the narrowing, because its question is in the headline, which
is exactly where the narrowed rule means to fire. **The rule is right and the deck is right.** What
is missing is the place to write that down.

## Suggested fix

A deck-side declaration the gate reads, so the ruling travels with the deck rather than with one
project's PowerShell:

```html
<!-- deviations: DS-110 the owner's drawing is the lobby's content
                 DS-100 the deck's topic is a question, quoted
                 DS-005 the demo reads a project-licensed local service -->
```

and `check.py --deviations` (or a `DEVIATIONS` shell region) that prints three lines and exits 0:

```
3 licensed: DS-110, DS-100, DS-005
0 unlicensed
retired: none          # a licensed rule that no longer fails is named, never dropped in silence
```

Two properties matter more than the syntax. **A licensed deviation is named in the output every
time**, so a reader of the gate sees the deck's whole shape rather than a green line. **A licensed
rule that stops failing is reported as retired**, so the list cannot rot into a blanket.

## What it buys

The gate goes back to being the signal. Today a deck with three rulings is red on every run, and a
fourth failure — a real one — arrives inside a wall of red the team has learned to read past. That
is the failure mode the wrapper exists to prevent, and it should not need a wrapper.
