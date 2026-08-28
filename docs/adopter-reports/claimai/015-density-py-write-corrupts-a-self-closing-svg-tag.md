# `density.py write` corrupts every self-closing SVG tag it touches

| Field | Value |
| :--- | :--- |
| **Target** | `htmldeck` — Gábor's own repository, cloned under `C:\Work\AgentPlugins` |
| **Kind** | Defect |
| **Status** | `open` |
| **Severity** | High — it writes invalid markup into the deliverable, and the gate reports the damage under an unrelated rule |
| **Found while** | Building round 2's motion on `D4 — Executive Board Presentation`, on 2026-08-26 — `E66 — Build round 2's motion` |
| **Version seen** | `0.6.0` |

## What happens

`DS-239` requires `--m-rank` to be the value the rule derives, and the rule derives it from the deck
itself — so adding one content motion re-ranks every content motion already there. `density.py write`
exists to do that arithmetic, and it is the right answer to the rule. Run against a deck whose new
content motion is a `dot-pop` figure:

```
python tools/deck/density.py write deliverables/D4-executive-board-deck.html
wrote ... - 5 content motion(s) ranked
```

It also writes `--dp` onto each circle in a `dot-pop` figure. Those circles are self-closing, and
this is what came out:

```html
<circle class="accent" cx="120" cy="80" r="24"/ style="--dp:0"><text ...>Oversight</text>
```

The `style` attribute landed **after** the closing slash. Seven tags on one slide, every one invalid.

## Where it comes from

`set_var` in `tools/deck/density.py`, the branch that runs when the tag carries no `style=` yet:

```python
return tag[:-1] + ' style="%s:%s"' % (name, value) + tag[-1]
```

The assumption is that a tag's last character is `>` and everything before it is attribute space.
That holds for `<p ...>` and fails for `<circle ... />`, where the character before `>` is the slash
that closes the element. The function's own docstring is careful about the *other* hazard — it merges
rather than replaces so that an existing `--i` survives — which suggests self-closing tags were simply
not in view.

## Why it costs more than a malformed tag

**The gate reports it as something else entirely.** The browser reparents the broken subtree, and the
`<text>` siblings inside the same `<g>` come back with a degenerate screen CTM. `DS-035` measures SVG
text through that matrix, so it reported:

```
DS-035   text below 16 design units: 3
   0.0 du  Oversight    [Fifteen per cent is unverified]
   0.0 du  Fairness     [Fifteen per cent is unverified]
   0.0 du  Wellbeing    [Fifteen per cent is unverified]
```

Three labels at exactly `0.0 du`, on a slide whose type was never touched. Nothing in that row points
at `density.py`, at `--dp`, or at a malformed tag.

**And it is intermittent, which is worse than wrong.** The same file, unchanged, gave `0, 3, 3` over
three consecutive runs and `0, 3, 0, 0, 3` over five. A gate that passes two runs in five sends an
author looking for a race condition in their own motion. This one cost the better part of a session:
the failure was bisected across three deck variants, each variant passing or failing by luck, before
`audit.py` was run directly to get the offenders named and the tag was finally read.

## What to change

1. **Fix `set_var`** — insert before the closing `/>` when the tag is self-closing, not before `>`.
   A one-line guard.
2. **Have `write` verify what it wrote.** It already parses the deck to find the tags; re-parsing
   afterwards and refusing to save a file that gained a malformed tag would have caught this in the
   run that caused it.
3. **Consider whether `DS-035` should say when a CTM is degenerate.** `0.0 du` is not small type, it
   is no type — a distinct fault reported as a type-size failure. Naming it separately would have
   pointed at the markup immediately.

Item 1 is the defect. Items 2 and 3 are why it was expensive.

## Workaround in use here

The seven tags were repaired by hand after the run:

```python
re.subn(r'/ (style="[^"]*")>', r' \1/>', html)
```

`DS-035` has been stable at `0` across three runs since. Any future `density.py write` on this deck
needs the same repair, so the sequence is: run `write`, repair, then check.
