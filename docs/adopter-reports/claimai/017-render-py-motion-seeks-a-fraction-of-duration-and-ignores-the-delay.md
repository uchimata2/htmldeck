# `render.py motion` seeks a fraction of duration and ignores the delay, so a working motion reads as dead

| Field | Value |
| :--- | :--- |
| **Target** | `htmldeck` — Gábor's own repository, cloned under `C:\Work\AgentPlugins` |
| **Kind** | Defect |
| **Status** | `open` |
| **Severity** | High — the tool states a conclusion about the deck in a sentence, and the conclusion is about its own seek |
| **Found while** | Reviewing `E68 — Decide whether figure motion should play on arrival` on `D4 — Executive Board Presentation`, on 2026-08-26. Reproduced 2026-08-28 |
| **Version seen** | htmldeck `0.6.0` |

## What happens

`render.py motion` reports every animation as dead when its delay is at least as long as its
duration. Reproduced 2026-08-28:

```
python tools/deck/render.py motion D4-executive-board-deck.html --into 3

  qpop on g.mark-q  [slide Deployer of a score nobody explains]
    300 ms, linear, fill both, delay 600, iterations 1
        seek     read state      opacity   transform
           0        0 paused     1         matrix(0, 0, 0, 0, 0, 0)
          75       75 paused     1         matrix(0, 0, 0, 0, 0, 0)
         150      150 paused     1         matrix(0, 0, 0, 0, 0, 0)
         225      225 paused     1         matrix(0, 0, 0, 0, 0, 0)
         300      300 paused     1         matrix(0, 0, 0, 0, 0, 0)
    the computed style DOES NOT MOVE - the seek reached nothing across the offsets
```

**The motion works.** Seeking the same animation past its delay, in the same Chrome, measured
2026-08-26:

| `currentTime` | transform |
| ---: | :--- |
| 600 ms | `matrix(0, 0, 0, 0, 0, 0)` |
| 750 ms | `matrix(1.0874, 0, 0, 1.0874, 0, 0)` — the overshoot |
| 900 ms | `matrix(1, 0, 0, 1, 0, 0)` — settled, 36 px wide |

## Where it comes from

`MOTION_PROBE` in `tools/deck/render.py`. Two branches write a seek, and both are off by the delay.

**The report branch**, line 602:

```javascript
want = offs.map(function(p){ return dur * (parseFloat(p) / 100); });
```

Its comment says the offsets stay *"a fraction of each one's own duration"*, and that is the right
unit. But `currentTime` is measured from the **start of the delay**, not from the start of the active
phase — so a fraction of the duration lands a delay too early. With `delay: 600, duration: 300` the
five offsets are `0, 75, 150, 225, 300`, and every one of them falls inside the 600 ms delay. With
`fill: both` the element sits at its FROM keyframe throughout, which is what the table above shows.

**The capture branch**, lines 597–598, used by `--shots`:

```javascript
var at = parseFloat(seek) - (tm.delay || 0);
want = [Math.max(0, Math.min(dur, at))];
```

This one starts from an absolute clock, which is right — `motion_span` runs it to `delay + duration`
— and then subtracts the delay before writing it to a property that already includes the delay. For
the same animation the span is 900 ms, the five capture moments are `0, 225, 450, 675, 900`, and
after the subtraction and the clamp they become `0, 0, 0, 75, 300`. All five are inside the delay
again, so every frame written shows the FROM keyframe.

**The two branches disagree with each other and both are wrong the same way.** One never adds the
delay; the other subtracts it after correctly adding it.

## Why it costs more than a wrong table row

**The verdict is a sentence, not a number.** *The computed style DOES NOT MOVE - the seek reached
nothing across the offsets* reads as a finding about the deck. It is a finding about the seek.
Nothing in the row points at the delay, and the delay is printed two lines above it.

**It is not confined to `delay >= duration`.** Any non-zero delay shifts the whole report, and the
shift is invisible because the row still says MOVES. From the same run, on a staggered entrance:

```
  rise on h2.headline.rise  [slide Not in six weeks]
    340 ms, linear, fill both, delay 60, iterations 1
        seek     read state      opacity   transform
           0        0 paused     0         matrix(1, 0, 0, 1, 0, 18)
          85       85 paused     0.306551  matrix(1, 0, 0, 1, 0, 12.4821)
         170      170 paused     0.857309  matrix(1, 0, 0, 1, 0, 2.56843)
         255      255 paused     0.979232  matrix(1, 0, 0, 1, 0, 0.373831)
         340      340 paused     0.99902   matrix(1, 0, 0, 1, 0, 0.0176368)
    the computed style MOVES across the offsets
```

**The last row is the tell.** The 100% offset reads opacity `0.99902` and a 0.0176 px offset. The
animation's real end is at `currentTime` 400 and the report stops at 340, so the frame labelled 100%
is not the settled state. A reader checking whether an entrance lands cannot tell that from an eased
curve that nearly arrives. `rise` at delays 0, 60, 120, 180 and 240 is htmldeck's own reference
stagger, so every deck built on it is being sampled this way.

This deck has two motions in the total-failure class, both reproduced on 2026-08-28 — slide 4's
question mark above, and slide 12's sway:

```
  sway on g  [slide Seven years is wrong twice]
    500 ms, linear, fill both, delay 1250, iterations 1
        seek     read state      opacity   transform
           0        0 paused     1         matrix(1, 0, 0, 1, 0, 0)
         125      125 paused     1         matrix(1, 0, 0, 1, 0, 0)
         250      250 paused     1         matrix(1, 0, 0, 1, 0, 0)
         375      375 paused     1         matrix(1, 0, 0, 1, 0, 0)
         500      500 paused     1         matrix(1, 0, 0, 1, 0, 0)
    the computed style DOES NOT MOVE - the seek reached nothing across the offsets
```

Both are motions a reviewer would go to this tool to check.

## What to change

1. **Add the delay in the report branch**: `tm.delay + dur * (p / 100)`. The comment's intent — a
   fraction of the animation's own life — is right; the arithmetic is missing one term.
2. **Drop the subtraction in the capture branch**: `want = [Math.max(0, Math.min(tm.delay + dur,
   parseFloat(seek)))]`. The absolute clock is already correct at the point it arrives.
3. **Make the verdict line say which it is.** *DOES NOT MOVE* should distinguish an animation that
   interpolates to nothing from one whose sampled range never left the delay. The second is the
   tool's own fault and should name itself, the way `motion_span` already names its clock.

Items 1 and 2 are the defect. Item 3 is why it was expensive.

## Related

- [`016-render-py-cannot-capture-a-decks-interactive-states.md`](016-render-py-cannot-capture-a-decks-interactive-states.md)
  — the other `render.py` finding from this project. That one is a state the tool cannot reach at
  all; this one is a motion it enumerates correctly and then samples in the wrong place.
- [`010-data-played-lands-at-transition-start-so-an-entrance-plays-under-the-outgoing-slide.md`](010-data-played-lands-at-transition-start-so-an-entrance-plays-under-the-outgoing-slide.md)
  — the other timing finding, on the shell rather than on the instrument.
