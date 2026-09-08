# `quickview.py` cannot wire a source item whose icon comes before its id

> **Found 2026-09-06**, building the Nextep deck against htmldeck `0.7.0`. Cost two build rounds
> and one wrong report to the owner. Filed here rather than fixed in place: htmldeck is a separate
> repository and the capstone ships tomorrow.

## What happens

`.sources-item` may carry a short identifier and a kind glyph in front of the title. The contract
fixes no order between them — §3.2.1 lists `.sources-icon`, `.sources-id`, `.sources-link` and
`.sources-open` as author-owned parts of `.sources-item` and says nothing about sequence.

`quickview.py` does fix one. `ITEM_HEAD` is:

```python
ITEM_HEAD = (r'(?:<span class="sources-id">[^<]*</span>)?'
             r'(?:<svg class="sources-icon"[^>]*>.*?</svg>)?')
```

Both groups are optional, and they are in a fixed order: **id, then icon**. A deck that writes the
icon first — which reads faster at projector distance, and is the order this project's owner
specified on 2026-09-04 — matches nothing.

## Why it costs a round rather than a minute

**The failure is silent in the direction that matters.** `plan` and `add` refuse a title no item
cites, with a clear message. But an item that *is* cited and simply ordered the other way is not a
refusal — it is a `0 hits` that reads as *this source is not cited*:

```
REFUSED  service-landscape.md   no provenance item reads 'service-landscape.md' in this deck.
                                A quick view is attached to a source a slide already cites - if
                                the slide does not cite it, that is a specification question and
                                not this tool's (T-069)
```

The message sends the author to the specification, which is correct. The specification says the
source *is* cited, which is also correct. Nothing points at the order.

## The measurement

| The item | `quickview.py plan` |
| :--- | :--- |
| `<span class="sources-id">S-29</span><svg class="sources-icon">…</svg>service-landscape.md` | `markdown service-landscape.md → 9188 bytes` |
| `<svg class="sources-icon">…</svg><span class="sources-id">S-29</span>service-landscape.md` | `REFUSED … no provenance item reads 'service-landscape.md'` |

Same deck, same slide, same title. The only difference is the two elements' order.

## The fix

`ITEM_HEAD` accepts either order, which is one alternation:

```python
ITEM_HEAD = (r'(?:(?:<span class="sources-id">[^<]*</span>)?'
             r'(?:<svg class="sources-icon"[^>]*>.*?</svg>)?'
             r'|(?:<svg class="sources-icon"[^>]*>.*?</svg>)?'
             r'(?:<span class="sources-id">[^<]*</span>)?)')
```

`wire()` already carries `m.group(1)` through unchanged, so nothing downstream needs to know which
order it found. A fixture per order would keep it honest.

## What this project did instead

Authored the wired markup directly — icon, id, then `.sources-open`, with the rendered document in
a `<template class="qv-src">` inside the same `.sources-item`, which is where the contract puts it.
`quickview.py list`, `check` and `refresh` all read it correctly afterwards; only the wiring step
could not produce it.
