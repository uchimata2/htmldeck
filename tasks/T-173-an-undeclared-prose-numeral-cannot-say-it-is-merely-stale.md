---
id: T-173
title: An UNDECLARED prose numeral cannot say it is merely stale, and that misled the task raised about it
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-172, T-129, T-154]
work_package: PH3
shipped_in: unreleased
owner: the project owner
business_value: medium
effort: xs
created: 2026-08-16
updated: 2026-08-16
deliverables:
  - tools/docs/figures.py
---

# T-173 — An UNDECLARED prose numeral cannot say it is merely stale, and that misled the task raised about it

## 1. Specify

**Outcome**
When a prose numeral fails to bind **because its value is wrong**, `figures.py` says so and names the
value the sentence's own subject carries — instead of reporting the same sentence it uses for a
numeral nothing watches at all.

**What is wrong.** `bound()` requires the value **and** the label to agree. A figure that has gone
stale fails both halves at once, so the report falls through to:

```
UNDECLARED prose numeral 262 - no command prints it under a label this sentence names, and it is excused nowhere
```

Every word of that is true and it describes the wrong failure. The sentence *does* name a subject
this tool measures — `examples/reference-deck.html` — and that subject's `KB` is `263`. The numeral
is not unwatched; it is **wrong**. Two lines below it in the same report, the same drift on the same
property of the same file reads:

```
STALE  examples/README.md states 262 - claims 262 KB of examples/reference-deck.html, which is 263
```

**The cost is measured, not hypothetical.**
[T-172](T-172-the-shell-sync-falsified-four-published-deck-figures.md) was specified against this
message and got it wrong: its scope proposed *bind it to the artifact manifest, or excuse it by
name*, and the recommendation was to bind. Neither was needed — the numeral was already bound and
correcting the value settled it. A report that names the wrong failure buys a wrong plan from
whoever reads it, and this one did.

**Scope**
- In: when a numeral does not bind, look for fields whose label the sentence **does** name, and put
  the nearest of them in the message.
- In: the message stays one line, and the verdict is unchanged — this is what `UNDECLARED` says, not
  which rows are `UNDECLARED`.
- Out: making it a `STALE` verdict. `UNDECLARED` is the honest kind — the tool cannot know the
  sentence means that field rather than an unrelated number that happens to sit near it, and a
  verdict claiming otherwise is the coincidence-matching **L-36** and **L-44** already refused here.
- Out: the `STALE` message on the linked-artifact path, which is the one that reads correctly.

**Inputs**
- [`tools/docs/figures.py`](../tools/docs/figures.py) — `bound`, `fields`, `audit`'s prose loop
- [T-172](T-172-the-shell-sync-falsified-four-published-deck-figures.md) §4 — the finding, recorded
  there when the message misled its own specification

**Acceptance criteria**
- [ ] A stale prose numeral whose sentence names its subject is reported with the value that subject
      carries, and with the word *stale*
- [ ] A numeral nothing watches keeps the message it has now — the two cases read differently
- [ ] No verdict moves: the same rows are `UNDECLARED` before and after, on the live page and on
      every fixture
- [ ] Both cases are fixtures that build their own text (**L-78**)

**Open questions**
- none

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | `near_miss(numeral, said, table)` — `bound`'s mirror: fields whose label the sentence names and whose **value differs**, nearest first | the information the message never had |
| 2 | `unbound_why()` — the one line an `UNDECLARED` row carries, near miss when there is one, today's sentence when there is not | one call site, one line, no verdict touched |
| 3 | Two fixtures on their own table (**L-78**): the stale case says *STALE* and names the value, the unwatched case says neither | the two cases are shown reading differently, not asserted to |
| 4 | Every count in the report diffed against the pre-change run | the verdict must not move — this is a message |

**Why `UNDECLARED` stays the verdict.** Nothing here knows the sentence means that field rather than
an unrelated number sitting near it — which is exactly why `bound()` needs both halves. A kind that
claimed otherwise is the coincidence-matching **L-36** and **L-44** already refused. The report can
say *if this is that figure, it is stale*; it cannot say *it is stale*.

## 3. Implement

**Decisions & assumptions**
- **Nearest first, by absolute difference** — 2026-08-16. A subject carries four properties, so a
  sentence naming `examples/reference-deck.html` near-misses `KB`, `bytes`, `slides` and `figures`
  at once. Distance puts the one the author got wrong first: `262` against `263` is 1, against
  `269083` is 268,821. A value that does not parse sorts last rather than raising.
- **Only the first near miss is printed.** The list is what a caller gets; the message is one line,
  because a report that prints four candidates is one a reader skips.
- **The message names the verdict it is NOT.** `if that is this figure it is STALE rather than
  unwatched` — the word `STALE` in the line is what makes the two cases greppable apart, and it is
  the word T-172's specification needed and did not get.

**Outputs produced**
- [`tools/docs/figures.py`](../tools/docs/figures.py) — `near_miss`, `unbound_why`, the call site,
  and three assertions.

**The exact figure that misled [T-172](T-172-the-shell-sync-falsified-four-published-deck-figures.md),
seeded back onto `README.md` and re-run:**

```
before  UNDECLARED prose numeral 262 - no command prints it under a label this sentence names,
                                       and it is excused nowhere

after   UNDECLARED prose numeral 262 - no command prints 262 under a label this sentence names.
                                       The sentence DOES name 'examples/reference-deck.html',
                                       whose nearest value is 263, printed by the deck files
                                       themselves - if that is this figure it is STALE rather
                                       than unwatched, and correcting it binds it
```

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A stale prose numeral whose sentence names its subject is reported with the value that subject carries, and with the word *stale* | met | Shown on the real case in §3 — `262` seeded back onto `README.md` — and asserted on a fixture that builds its own table |
| A numeral nothing watches keeps the message it has now | met | `4242` against the same table gets neither the word `STALE` nor a value, asserted. The two lines are greppable apart |
| No verdict moves: the same rows are `UNDECLARED` before and after | met | Every count in the report diffed against the run taken before the change — `compared 9, total 9` for prose numerals, and every other bucket identical. `figures.py` exits 0 either side |
| Both cases are fixtures that build their own text (**L-78**) | met | A two-row table written in the fixture. The one earlier draft that reached for the live `table` clobbered it and took down an unrelated assertion, which is the failure L-78 is about, met while writing the test for it |

**A third assertion nobody asked for, and it earns its line.** The near miss is checked to be ordered
by distance. Without it the byte count can be offered ahead of the rounded size — `269083` is a field
of the same subject and a perfectly valid near miss — and the message would name a number the author
never wrote.

**Nothing here renders**, and no verdict changed on any page. `TASK-WORKFLOW.md` §7 step 3 is not
owed.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-16 | → done | Raised and closed the same night. **A message change and nothing else** — every count in the report is identical either side of it, which is the property that had to hold. The line now names the value the sentence's own subject carries and the verdict it would be if the reader means that field. `UNDECLARED` stays the kind: the tool cannot know the sentence means that field, and a kind that claimed to is the coincidence-matching `bound()` needs both halves to refuse. |
| 2026-08-16 | → proposed | Raised on the owner's instruction, out of [T-172](T-172-the-shell-sync-falsified-four-published-deck-figures.md)'s review. The finding was recorded there as an observation and left unraised; the owner asked for the text sharpened. |
