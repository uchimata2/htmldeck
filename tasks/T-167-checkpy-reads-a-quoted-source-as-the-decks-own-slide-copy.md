---
id: T-167
title: check.py's content half reads a quoted source as the deck's own slide copy
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-070, T-128, T-106]
work_package: PH1
owner: the project owner
business_value: high
effort: m
created: 2026-08-16
updated: 2026-08-16
deliverables:
  - tools/deck/check.py
---

# T-167 — check.py's content half reads a quoted source as the deck's own slide copy

## 1. Specify

**A deck that embeds its sources is failed for what the sources say.** DS-100 is *no rhetorical
questions in **slide copy***; FIG-3 is *figures appearing twice in **the deck** with different
values*. Both are evaluated over text that includes every `<template class="qv-src">` region — the
quoted source documents the quick view carries (T-070). A source document is evidence the deck
shows, not a claim the deck makes.

**Measured on [T-128](T-128-publish-the-adopter-deck-as-a-worked-example.md)'s deck, 2026-08-16.**
The experiment emptied the five `qv-src` regions on a scratch copy and re-ran the same gate:

| | with quick views | with them emptied |
| :--- | ---: | ---: |
| `DS-100 no rhetorical questions` | **FAIL** | **pass** |
| `FIG-3 figures appearing twice with different values` | **FAIL** (4) | **pass** (0) |
| figures the gate attributes to the deck | 152 | 30 |

**122 of the 152 figures it was reasoning about were quotations.** Nothing in the slide copy proper
carries a question mark — the only question-shaped strings left after stripping are JavaScript
ternaries in the shell's own script.

**What the deck was actually failed for.** The DS-100 hits are section headings and table headers
inside the quoted analysis: *Where are the delays?*, *Which measurements already exist?*, *Is the
data historically correct and factually reliable?*. The FIG-3 hits compare a figure on a slide with
a different figure inside a source the slide quotes — `87%` on the face against `78%` in a table of
the quoted D1, which are two different measures and disagree only because they were put in one bag.

**Why this is `PH1`.** It is a published gate failing a deck for using a feature this repository
ships and documents — `quickview.py` exists to put sources inside the deck, and `check.py` then
charges the deck for their contents. `CLAUDE.md` classes that as a defect regardless of who filed
it and regardless of size.

**Why neither shipped deck caught it.** `examples/reference-deck.html` and
`examples/sort-window/sort-window.html` both carry quick views and both pass, because the sources
written in this repository happen to contain no question headings and no figure that differs from
the slide quoting it. The rule was never exercised against a source document written by somebody
else — which is exactly the value T-128 was raised to get.

**The mechanism, located 2026-08-16 in [`tools/deck/audit.py`](../tools/deck/audit.py) §`STATIC`.**
Every static verdict is a lambda over `h`, and **`h` is the whole file** — slide copy, the shell's
CSS and script comments, and the `qv-src` templates alike. DS-100 is one line:

```python
("DS-100", "no rhetorical questions in slide copy",
 lambda h: not re.search(r"\?\s*<", h)),
```

Nothing in it is scoped to a slide. **DS-106 has the same shape and the same exposure** — a quoted
source that happens to use *leverage* or *seamless* fails the deck for terminology the deck did not
write. That is the second rule this task must cover, and it has not fired yet only by luck.

**The repository already knows quick views are a different context**, which is what makes this a
defect rather than a design choice: DS-110's own row reads *no raster the deck produces; **a quoted
source may be raster inside a quick view***. One rule was given the distinction when T-070 landed and
the rest were not.

**So the work is classification, not invention.** Each rule in `STATIC` reads either *what the deck
says* or *what the file contains*, and the two need different inputs. DS-001, DS-002 and the
external-reference family must keep seeing everything — a quoted source that reaches the network is
a real defect. DS-100 and DS-106 must see slide copy only. That sweep is why this is `m` and not
`s`.

**Scope**
- In: the content half excludes `<template class="qv-src">` regions when it decides what the deck
  *says* — DS-100, DS-106 and the FIG rules that speak of "the deck" or "a slide".
- In: a fixture deck whose quoted source carries a question and a conflicting figure, so the fix
  is shown to fail without it (**L-04**, **L-05**).
- Open: whether any rule *should* still read the quoted text. A source that reaches the network or
  carries a banned term is `quickview.py`'s admission problem, not slide copy's.

**Acceptance criteria**
- [ ] `check.py` on T-128's deck reports DS-100 pass and FIG-3 pass, with the quick views intact
- [ ] The figure count the gate attributes to the deck counts slide copy only
- [ ] A fixture proves the old behaviour failed and the new one does not
- [ ] Every rule whose wording says *slide copy*, *a slide* or *the deck* is checked against what it
      now reads, and any rule deliberately left reading the quotation says so in its own row

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Build the second input beside `h`: the file with every `<template class="qv-src">…</template>` region emptied | one helper |
| 2 | **Classify every row of `STATIC`** — reads the deck's own copy, or reads the whole file — and record the verdict per row rather than per family | the classification |
| 3 | Feed each row the input its classification names. DS-100 and DS-106 take the stripped text; DS-001, DS-002 and the reference family keep `h` | the change |
| 4 | Do the same for the FIG rules in `content.py`, whose figure set is the same mistake one layer down (152 → 30 on T-128's deck) | the change |
| 5 | A fixture deck whose quoted source carries a question, a banned term and a conflicting figure — red before, green after (**L-04**, **L-05**) | the proof |
| 6 | Re-run every shipped deck: none of them may move | the regression |

**Do not fix this by stripping in one place and hoping.** The classification in step 2 is the
deliverable; the code change is small and follows from it. A rule quietly given the wrong input is
the same defect pointing the other way — a deck that reaches the network inside a quoted source and
passes.

## 3. Implement

_Not started._

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-16 | → proposed | Found by [T-128](T-128-publish-the-adopter-deck-as-a-worked-example.md) step 6 on the first deck here whose sources were written outside this repository. Diagnosed by stripping the `qv-src` regions and re-running rather than by reading the checker, so the mechanism is measured and not inferred. |
