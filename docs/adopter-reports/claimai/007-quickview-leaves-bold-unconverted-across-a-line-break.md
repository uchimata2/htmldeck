# A quick view leaves `**bold**` unconverted when the emphasis spans a line break

| Field | Value |
| :--- | :--- |
| **Target** | `htmldeck` — Gábor's own repository, cloned under `C:\Work\AgentPlugins` |
| **Kind** | Defect |
| **Status** | `closed` |
| **Found while** | Reading the sources markup of `D4 — Executive Board Presentation` on 2026-08-24, for an unrelated wrapping change |
| **Version seen** | `0.6.0` |

## What happens

`quickview.py` renders a Markdown source section into the deck. Strong emphasis is converted when
the whole `**…**` sits on one line, and left as literal asterisks when it wraps. Backticks in the
same sentence convert correctly, so the failure is specific to the multi-line case rather than to
the renderer being off.

The source, from `D4 — Governance Decision Record` §3.1:

```
  when it is written. So SecureLife's residual risk today is its inherent risk: **four CRITICAL and
  eight HIGH** (`D1 §8 — Residual risk`).
```

What the deck carries:

```html
its inherent risk: **four CRITICAL and eight HIGH** (<code>D1 §8 — Residual risk</code>).
```

The `<code>` is right; the asterisks are on screen.

## Evidence

Three occurrences in one deck, in two distinct passages, both of which wrap in the source. Found by
stripping every `<style>` and `<script>` block and scanning what is left:

```
python -c "import re; h=open(DECK,encoding='utf-8').read(); \
  b=re.sub(r'<style.*?</style>','',h,flags=re.S); b=re.sub(r'<script.*?</script>','',b,flags=re.S); \
  print(re.findall(r'\*\*[^*\n]{1,90}\*\*', b))"
```

```
['**four CRITICAL and eight HIGH**', '**It equals the inherent score for all twelve risks**',
 '**four CRITICAL and eight HIGH**']
```

The `[^*\n]` in that pattern is the point: the leaked text has already been joined into one line by
the renderer, so the break that defeated the conversion is not visible in the output. It has to be
found in the source.

## What is missing

Emphasis is converted or it is not. A reader of a quick view sees raw Markdown, and nothing in the
build gate says so — `check.py`, `component.py`, `theme.py` and `spec.py` all pass on a deck
carrying it.

## Proposed fix

Normalise the paragraph before the inline pass — collapse the run of whitespace that a soft wrap
leaves, then match `\*\*(.+?)\*\*` without the newline exclusion. **And add a gate**: a scan for
unconverted `**`, `__` or a leading `#` inside rendered quick-view content, run where `spec.py`
runs. The renderer will keep meeting constructs it does not handle; the gate is what makes the next
one cost a minute instead of a shipped deck.

## Closed

**2026-08-29 by [T-269](../../../tasks/T-269-three-build-path-defects-the-adopter-worked-around.md),
both halves - and the record named the wrong site.**

The proposed fix was to normalise the paragraph before the inline pass. **`flush_para` already does
exactly that** - it joins the paragraph's lines and converts once - which is why the same sentence
written as a paragraph converts correctly and was never the failing case. The site is the **list
item**: its first line was converted the moment it was read and each wrapped continuation converted
separately, so `**four CRITICAL and` / `eight HIGH**` met the inline pass as two halves and neither
matched. An item now accumulates its raw text run and converts once, which is the order the
paragraph path already used. The source passage in this record is indented two spaces under a list
marker, so it is a continuation - the reason a paragraph-shaped diagnosis fitted the symptom.

**And the gate**, as the record asked, run where `spec.py` runs: `quickview.py check` scans every
carried rendering for unconverted `**`, `__` or a leading `#` and exits non-zero. It scans **every**
view the deck carries rather than only the ones `--source` named, because a leak is a property of
the rendering and needs no source file - the unnamed views are exactly the ones nothing else there
reads. Measured across the tracked decks: **20 quick views, 0 leaking**. Seven self-test fixtures
hold it in both directions, three of them false-alarm cases the first draft got wrong - an
attribute, a snake_case identifier and an inline `#`.
