# Nothing prints what a slide actually contains, so a specification and its deck drift silently

| Field | Value |
| :--- | :--- |
| **Target** | `htmldeck` — Gábor's own repository, cloned under `C:\Work\AgentPlugins` |
| **Kind** | Feature |
| **Status** | `closed` — closed 2026-08-30 by [T-259](../../../tasks/T-259-nothing-prints-what-a-slide-actually-contains.md). **Step 1 taken, its mechanism refused; step 3 taken; step 2 deferred on the record's own argument.** [`../../../tools/deck/slidefacts.py`](../../../tools/deck/slidefacts.py) prints one slide's answer for every claimed field and makes no judgement. **The mechanism is not `render.py`'s parse**, which is a Chrome DOM read: every claimed field is in the static markup, so the printer is standard library and costs no browser launch. The static read then exposed the trap a DOM read would have hidden — **a `<template>`'s text is inside its slide's `<section>`**, and on slide 4 of `examples/sort-window/sort-window.html` the quick-view payloads are **59% of the section** (9,826 bytes against 4,056 with templates cut), so an unguarded printer answers for the slide with the documents it cites. **One field pair was re-cut for the same reason**: a figure sits inside a `.body` wrapper, so body copy is read with the SVG removed and the eleven chart labels are printed once, as drawn labels, rather than twice. Step 2's verdict stays out of scope, which this record argues for and T-259 §1 records. Step 3 is [`../../../skills/htmldeck/references/build.md`](../../../skills/htmldeck/references/build.md) §4, beside the deviation obligation that already exists for the build-time half of the same problem. |
| **Severity** | High — twenty-three of twenty-five entries had drifted before anyone looked, and the gate was green throughout |
| **Found while** | Sweeping every slide entry in the specification against the built deck, on 2026-08-27 — `E75` |
| **Version seen** | 0.6.0 |

## What happens

A deck is built from a specification pair and then **edited in place** — which is the supported way to
work once a slide carries anything the build cannot reproduce. From that moment the specification is a
claim about the deck, and nothing checks it.

Four entries were read closely against the deck, one at a time, and all four had drifted. A full sweep
followed:

> **Twenty-three of twenty-five entries had drifted**

`check` was green for every one of them. A stale specification is valid input; the gate has no opinion
about whether it describes the deck it sits beside.

## Why the gate cannot catch it

The gate reads the deck. The drift is between the deck and a *second document*, and no verdict spans
the two. `spec.py` reads the specification but does not hold it against the built output.

## The workaround, and its shape

This project wrote a ~250-line script that prints the deck's own answer for every field an entry
claims — eyebrow, headline, standfirst, bottom line, drawn labels, body copy, controls, motion
classes, quick views and sources — for one slide:

```
python tools/slidefacts.py D4-executive-board-deck.html 13
```

**It makes no judgement.** It says what is there, and a reader says whether the entry matches. That
division is what made it usable: a differ would have produced noise on every intentional difference,
and there are many.

## What to change

1. **Ship the printer.** `render.py` already parses the deck for `measure` and `motion`; the same
   parse can emit a per-slide fact sheet. It is the cheapest useful thing here.
2. **Then consider a verdict**, once the printer exists and its shape is known — an entry whose
   headline does not appear on its slide is a defect with no judgement in it, and could be a rule.
3. **Say in the docs that in-place editing forks the specification.** The workflow is supported and
   the consequence is not written down. This project found it after twenty-three entries.
