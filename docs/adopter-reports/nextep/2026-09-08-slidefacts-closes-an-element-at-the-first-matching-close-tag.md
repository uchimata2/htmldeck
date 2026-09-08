---
tool: htmldeck
version: 0.7.0
date: 2026-09-08
severity: defect
---

# `slidefacts.py` closes an element at the first matching close tag, so most of a page's face is invisible

## Expected

`slidefacts.py <deck> <n>` prints what a slide itself says. Its own header calls it *what the deck
itself says*, and `deck/build/README.md` and this project's audit both use it as the cheap text read
that answers *does the deck say it*. `Body copy` should carry every word of the slide's `.body`.

## Actual

`by_class(section, name)` takes the **first** matching close tag rather than its own:

```python
end = section.find("</%s>" % m.group(1), m.end())
```

So a `<div class="body">` whose first child is itself a `<div>` reports only that child's text.
Every sibling after it is dropped, silently, with no marker in the output.

The bug is in a shared helper, so `eyebrow`, `headline`, `standfirst`, `bottom line` and `sources`
inherit it wherever those elements wrap another element of the same tag.

## The reproduction

```python
import sys; sys.path.insert(0, r"<htmldeck>/tools/deck")
import slidefacts as sf
sf.by_class('<div class="body"><div class="a">FIRST</div><p>SECOND</p><p>THIRD</p></div>', 'body')
```

Run on 0.7.0, 2026-09-08:

```
['FIRST']                          # actual
['FIRST SECOND THIRD']             # expected
```

And the control, which isolates the cause to nesting rather than to siblings:

```python
sf.by_class('<div class="body"><p>FIRST</p><p>SECOND</p></div>', 'body')
['FIRST SECOND']                   # correct - no nested div, nothing dropped
```

## What it costs, measured on a real deck

**Page 23, *What you read decides the rate*.** The resting face carries `63%`, `43%`, `32%`, `0%`,
`145 issues declared done` and `308 issues declared done`. `slidefacts.py` prints its body copy as
`Every channel The platform's own link only` and nothing else — the two band buttons, which are the
first child `<div>`. The page's whole result is invisible.

**Across the 32 argument pages, `slidefacts.py` printed every word of the rendered face on 4.**

**A second witness, 2026-09-08.** Page 19, *It predicts links, not outcomes*, has the same shape:
its `.body` opens with a `<div class="predwrap">`, so `Body copy` stops at the column grid and drops
the footer paragraph entirely. The truncation reproduces on the deck as it stood before that page
was edited, so it is the helper rather than anything the deck did that day.

## Why it matters

An audit that trusts this section reports a gap where the deck has content. The failure is silent:
there is no marker, no warning and no exit code, so the only way to notice is to read the built
parts and compare — which is what the tool exists to save.

## Suggested fix

Balance the tag. Count opens of `m.group(1)` between `m.end()` and each candidate close, and take
the close where the depth returns to zero. Void and self-closing elements never open a depth.

## Not the same as the `Controls` finding

[2026-09-07-slidefacts-reports-no-control-on-any-slide.md](2026-09-07-slidefacts-reports-no-control-on-any-slide.md)
is about the `Controls` section and a different cause. This one is `Body copy`, and it is a
tag-balance bug in a shared helper.

Found while auditing a deck against its training material, 2026-09-08.
