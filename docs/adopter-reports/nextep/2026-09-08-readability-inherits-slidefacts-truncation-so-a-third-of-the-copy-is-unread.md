---
tool: htmldeck
version: 0.7.0
date: 2026-09-08
severity: defect
---

# `readability.py` reads its lines through `slidefacts.py`, so a third of the copy is neither read nor named

## Expected

`readability.py`'s own contract is that nothing goes missing quietly. Its docstring says the words
it leaves out are **counted and named** rather than dropped in silence (`L-149`), and the report
prints that ledger:

```
Not read: 863 word(s) - drawn labels 789, sources 74.
```

So a reader can trust two numbers: what was measured, and what was deliberately not.

## Actual

`lines_of()` takes every line from `slidefacts.facts`, on the stated ground that *what text is on a
slide* should have one implementation. That is the right instinct, and it inherits the truncation
recorded the same day in
[2026-09-08-slidefacts-closes-an-element-at-the-first-matching-close-tag.md](2026-09-08-slidefacts-closes-an-element-at-the-first-matching-close-tag.md):
a `.body` whose first child is an element of the same tag reports that child only, and every
sibling after it is dropped.

**The dropped words are on neither side of the ledger.** They are not measured, and they are not
in *Not read*, because `counted_out()` reads the same truncated facts. The report is confident and
short by a third.

## The command that proves it

On this project's delivered 33-page deck, 0.7.0, 2026-09-08:

```bash
python <htmldeck>/tools/deck/readability.py deck/nextep.html
```

```
Over 132 line(s) of prose, 2985 word(s), 215 sentence(s):
  Flesch Reading Ease    60.8   (plain)
Not read: 863 word(s) - drawn labels 789, sources 74.
```

Against the same deck's body copy, counted by closing each `.body` at its **own** close tag and
dropping `script`, `style`, `template` and `svg`:

```python
import sys; sys.path.insert(0, r"<htmldeck>/tools/deck")
import density, slidefacts
# per slide: words in slidefacts.facts(html, i)["body copy"]  vs  words in the whole .body subtree
```

```
slides: 33
body-copy words slidefacts reports : 2247
body-copy words the slides carry   : 3284
neither read nor named as not-read : 1037  (32%)
slides losing words: 11 of 33
  slide 14  reported   66  carries  351  lost  285
  slide 19  reported  105  carries  252  lost  147
  slide 22  reported   87  carries  226  lost  139
  slide 12  reported   99  carries  202  lost  103
  slide 23  reported    7  carries  108  lost  101
```

The full script is 60 lines of standard library and can be sent if it is wanted; the loop above is
the whole of it.

## Why it matters more here than in `slidefacts.py` itself

`slidefacts.py` prints a page and a person reads it, so a short answer invites a second look.
`readability.py` prints **aggregates and a ranking**, and both look complete. Slide 14 contributes
66 of its 351 words to a Fog score; the ranked *hardest lines* list cannot name a line it never
read. This project's own reader — the deck's owner — flagged sentences by hand that the instrument
had no chance of ranking, on a deck whose readability run was green and plausible.

## Workaround used in this project

The copy pass was done by reading the rendered pages, with the readability report as one input
rather than the measurement. No tooling change was made here.

## Suggested fix

Fix `by_class` in `slidefacts.py` — closing at tag depth rather than at the first matching close
tag repairs both tools at once. Then **make the ledger prove itself**: have `readability.py` count
the words in each slide's `.body` subtree and assert that *read + counted-out = carried*, printing
the difference when it is not zero. A ledger that cannot be short is worth more than one that
promises not to be.
