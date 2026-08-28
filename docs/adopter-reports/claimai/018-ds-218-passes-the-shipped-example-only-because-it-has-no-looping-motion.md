# DS-218 passes htmldeck's own example only because that example has no looping motion

| Field | Value |
| :--- | :--- |
| **Target** | `htmldeck` — Gábor's own repository, cloned under `C:\Work\AgentPlugins` |
| **Kind** | Defect |
| **Status** | `open` |
| **Severity** | High — an author who copies the shipped chrome and later adds one looping motion turns a passing deck into a failing one, and nothing points at the chrome |
| **Found while** | Moving the motion control into the More menu on `D4 — Executive Board Presentation`, on 2026-08-24 — `E39`. Re-measured 2026-08-28 |
| **Version seen** | 0.6.0 |

## What happens

`DS-218` asks for *a persistent, keyboard-operable control* that stops motion which loops or runs
over 5 s. `COMPONENT-CONTRACT.md` is explicit about what that excludes:

> a control one click inside a shut menu is not

**The shipped `portfolio-review` example puts the control inside the shut menu, and passes.** Both
verdicts, taken 2026-08-28 on `0.6.0`:

```
examples/portfolio-review/portfolio-review.html
  DS-218   persistent control for motion over 5s: False (present: True, 0 looping)   pass
  0 failure(s): none

D4-executive-board-deck.html
  DS-218   persistent control for motion over 5s: False (present: True, 8 looping)   FAIL
  4 failure(s): DS-110, DS-217, DS-218, DS-219
```

The `False` is identical. The chrome is in the same place. The only difference is the looping count,
which gates whether the rule applies at all.

## Why it costs more than a failing rule

**The example teaches a placement that is only safe by accident.** An author reads
`portfolio-review`, copies its chrome, and has a passing deck. The first looping motion they add
fails `DS-218` — and the failure names a rule about motion, on a deck whose motion is fine. The
defect is in chrome they inherited and never chose.

That is exactly the path this project took. The control was moved into the menu on the author's
instruction, the example was checked and found to agree, and the rule failed anyway. The deck ships
with `DS-218` failing by decision.

## What to change

1. **Make `portfolio-review` pass for a reason, not for want of a subject.** Either move its motion
   control out of the menu, or give the example one looping motion so the rule is actually exercised.
   An example that satisfies a rule vacuously is worse than one that fails it.
2. **Say so in the failure.** When `present: True` and the control is inside the shut menu, the
   verdict should say *the control exists but is not persistent*, not merely `False`. The contract
   already has the sentence; the gate does not print it.
3. **Consider whether the menu is genuinely disqualifying.** The author here wanted a clean chrome
   bar and chose the menu twice. If a one-click-deep control is acceptable when the menu button
   itself is persistent and keyboard-reachable, the rule should say so; if it is not, the shipped
   example should not model it.

## Related

- [`002-ruler-scale-claim-breaks-past-eighteen-sections.md`](002-ruler-scale-claim-breaks-past-eighteen-sections.md)
  — `DS-217`, the other rule this deck fails permanently.
