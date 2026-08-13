---
id: T-123
title: Nothing can see a print-only layout fault, and one reached two shipped decks
type: decision
status: done
phase: review
shipped_in: unreleased
parent: null
blocked_by: []
related: [T-034, T-036, T-084, T-116]
work_package: PH3
owner: the project owner
business_value: high
effort: l
created: 2026-08-13
updated: 2026-08-13
deliverables:
  - tools/deck/printgeom.py
  - tools/deck/check.py
  - tools/deck/contents_bound.py
  - tools/check_all.py
---

# T-123 — Nothing can see a print-only layout fault, and one reached two shipped decks

## 1. Specify

**Outcome**
A decision on whether this repository gates the printed *geometry* of a deck, and not only its page
count — taken with the cost of the instrument on the table, because the cost is the reason the
question is open rather than obvious.

**What happened**

[T-116](T-116-the-printed-contents-page-collides-at-thirteen-entries.md) was a collision on the
printed contents page that **no gate could see, and that the one tool aimed at that page reported as
clean**. The two readings, same deck, same day:

| | box height | rows 2→3 gap | verdict |
| :--- | ---: | ---: | :--- |
| `contents_bound.py`, print rules lifted onto screen | 175.7 du | +26.0 du | clean |
| the printed PDF | 200.2 pt = 267 du | −49.2 pt | rows print through each other |

The divergence is Chrome's paged layout giving a grid item its own content height rather than its
track, where the screen zeroes the item's automatic minimum because `overflow:hidden` says to. **No
screen measurement can see it**, whatever the fixture holds — T-116 verified that by re-running the
screen reading with the tall fixture and the CSS still broken, and it stayed clean.

It reached `examples/reference-deck.html`, which is 13 entries and printed with two overlapping row
pairs and its footnote inside a card, and it reached the first adopting project's presented deck.
Both were shipped. Every gate was green for both.

**What a second adopter deck adds, measured 2026-08-13**

The owner produced a deck outside this repository with the plugin and printed it on **2026-08-12,
the day before `0.2.3` shipped the fix**. Read out of that PDF, geometry only:

| | |
| :--- | :--- |
| contents sheet | 13 entries, 4 rows of 4 · 4 · 4 · 1 |
| row gaps | +19.5, **−12.0**, **−12.0** pt |
| card pairs actually intersecting | **4** |
| last card | ends 775.9 pt down a 810 pt page, printing through the footnote band |
| every other page | clean |

So the fault class reached **three** printed decks, not two, and the third belongs to somebody who
was not reading this repository's gates at all. It also says something the first two could not: the
fix ships in the **shell**, so an adopter only receives it by re-syncing and re-printing, and
nothing today tells them whether that worked on their own file. A gate that only ever runs over
`examples/` cannot answer that question for the population the fault actually lives in.

**And the same measurement priced one false-positive class before the instrument exists.** On a
slide carrying a decision diamond, a naive *do any two drawn boxes intersect* test reports a
collision: the diamond's bounding box overlaps its neighbour's while nothing visually touches. The
assertion has to be **rows of siblings in the contents grid**, not any two rectangles on any page —
which narrows the instrument, and is the difference between a gate and a nuisance.

**What the instrument costs, measured 2026-08-13 rather than inherited**

The owner's second ruling forced the dependency question into the open, so it was priced by building
the reader rather than by estimating it again. A pure-standard-library spike was run against
`examples/reference-deck.html`, printed through the same Chrome path `printpages.py` uses:

| | |
| :--- | :--- |
| content streams | `FlateDecode` — `zlib`, which is standard library |
| the nesting that defeated T-116's throwaway | `q`/`Q` depth **2**: one outer flip `cm`, one `3.125` scale |
| what a card is on paper | a **stroked** rounded rectangle — `m`/`l`/`c`/`h`, 101 points, one per entry |
| what the spike read | **13** card outlines on sheet 1, in rows of 4 · 4 · 4 · 1 |
| row gaps | **+19.5, +20.2, +19.5 pt** — clean |
| footnote | lowest text baseline **748.5 pt**, last card bottom **712.1 pt** |
| the reader | ~150 lines, standard library only |

**Two instruments, three decks, and the same quantity.** The adopter's pre-fix print read its row
gaps as +19.5, −12.0, −12.0; the first of those agrees with the reading above to 0.1 pt, on a
different deck built outside this repository. T-116's pymupdf reading put the footnote band at
735.7–751.5 pt, and the baseline this reader finds at 748.5 falls inside it. The stdlib reader is
measuring what pymupdf measured.

**So the third obstacle below dissolves, and it was never the hard part.** The tens-of-thousands
coordinates were a missing CTM stack — twenty lines of `q` / `Q` / `cm` — not a property of Chrome's
writer. **No dependency is taken**, L-07 stands, and the gate an adopter has to run costs them
nothing to install. That is the ruling this task takes, and it is taken on the numbers above.

**What stops the reader passing a page it never read.** A parser that finds nothing reports no
overlaps, which is `printpages.py`'s zero-page problem one level up (**L-36**). So the count is
checked against the deck itself: the reader must find exactly as many card outlines on a sheet as the
deck says that sheet carries, asked of the DOM the way `printpages.py` asks for `k` rather than
recomputed here (**L-08**). A disagreement is a failure of the gate, reported as one.

**And `contents_bound.py` stays, with a smaller claim.** It measures the bands and the two caps —
the *inputs* to the split rule — which the printed reading does not, and it is seconds where a print
is a minute. What it may no longer do is imply the printed page is clean, which is what L-76 caught
it doing. The screen tool keeps its measurement and loses that sentence.

**Why this is not simply "add a check"**

Three things stand in the way, and they are the substance of the decision:

1. **The owner ruled the opposite on 2026-08-08.** `printpages.py` asserts the page count and only
   the count; DS-222 to DS-226 are left to the print a person does under `CLAUDE.md` rule 6, on the
   argument that a gate claiming those five would be claiming a judgement it cannot make
   ([T-038](T-038-the-gate-emits-verdicts-for-judge-rules-and-one-wrong-id.md)). T-116 is evidence against that ruling —
   *collision* is geometry, not judgement — but overturning it is the owner's call, which is why
   this is a `decision` and not a `fix`.
2. **The instrument is not cheap.** Reading card positions out of Chrome's PDF needs a graphics-state
   stack: the rounded cards are béziers, not `re` operators, and the content stream nests `q`/`cm`.
   A throwaway that ignored the nesting returned coordinates in the tens of thousands. It is a real
   parser, and it is pinned to what Chrome's PDF writer emits.
3. **The obvious shortcut is barred.** pymupdf reads this correctly in four lines and was used
   throughout T-116's diagnosis, but it is not a repository dependency and `contents_bound.py` is
   pure standard library by **L-07**. Taking a dependency for one gate is its own decision.

**Scope**
- In: whether the printed geometry is gated at all, and if so, what it asserts. The narrow useful
  assertion is *no card overlaps another and none reaches the footnote* — a `>` between numbers, not
  a judgement.
- In: what the instrument costs, decided against L-07 and against a new dependency.
- In: whether `contents_bound.py` keeps measuring on screen at all once something measures on paper.
- Out: the second contents sheet — [T-036](T-036-the-second-contents-page-for-long-decks.md).
- Out: DS-222 to DS-226 as judgements. This is about geometry only, which is what makes it
  answerable where T-038 was not.

**Inputs**
- [T-116](T-116-the-printed-contents-page-collides-at-thirteen-entries.md) §3 — the mechanism, the
  two readings, and the prototype that priced the parser.
- [T-038](T-038-the-gate-emits-verdicts-for-judge-rules-and-one-wrong-id.md) — the 2026-08-08 ruling this would revisit.
- [`tools/deck/printpages.py`](../tools/deck/printpages.py) — where a geometry assertion would go,
  and the existing pure-stdlib PDF reading to build on.
- [`tools/deck/contents_bound.py`](../tools/deck/contents_bound.py) — the tool that reported clean.

**Acceptance criteria**
- [ ] A decision is recorded, either way, with the cost that decided it.
- [ ] If the answer is yes: a seeded overlap is caught, and a correct page passes — measured against
      both, not against the correct one alone (**L-05**).
- [ ] If the answer is no: the limitation is stated where someone about to trust the screen numbers
      will read it, and the manual print step is named in the release gate rather than assumed.
- [ ] The reader is standard library only, and runs against **any deck it is pointed at** — the
      owner's second ruling — not `examples/` alone.
- [ ] The reader refuses to return a clean verdict when the number of cards it finds disagrees with
      the number the deck says that sheet carries (**L-36**).
- [ ] `check_all.py` accounts for the new tool in one of its three states, and runs it over both
      shipped decks.
- [ ] `contents_bound.py` no longer implies the printed page is clean (**L-76**).
- [ ] Both shipped decks are printed and the contents sheet is **looked at**, not only measured
      (**L-01**, CLAUDE.md rule 6).

**Open questions**
- ~~Should the printed geometry be gated at all?~~ **Answered by the owner 2026-08-13: yes,
  narrowly.** The assertion is *no card overlaps another and none reaches the footnote*, and nothing
  wider. So the 2026-08-08 ruling stands where it was aimed — DS-222 to DS-226 as *judgements* stay
  with the person who prints — and it is narrowed only where the property is arithmetic. What is
  left for `specify` is the instrument, not the question.
- ~~**Is `examples/` the only surface this gates, or does an adopter's deck get it too?**~~
  **Answered 2026-08-13 by the owner: any deck it is pointed at**, with `check_all.py` running it
  over `examples/`. So the instrument is a per-deck gate and the dependency question below is
  settled against L-07 rather than around it — whatever it costs, an adopter has to be able to run
  it. What is left for `specify` is the instrument, on both counts.
  Evidence arrived 2026-08-13 and is in *What a second adopter deck adds* above. The reasoning was:
  any deck it is pointed at, with `check_all.py` running it over `examples/` — the shape every
  other per-deck gate already has (`check.py`, `shell.py check`, `theme.py check`), and the shape the
  evidence asks for, because the fix travels in the shell and only the deck's owner can confirm it
  landed. The argument the other way is the dependency: a gate an adopter runs is a gate whose
  instrument an adopter must install, where an `examples/`-only gate could stay a maintainer tool and
  keep **L-07** intact. That trade is the ruling.
- ~~**Is the instrument a stdlib parser or a new dependency?**~~ **Settled 2026-08-13 by building
  it: standard library, no dependency.** The reasoning is *What the instrument costs* above, and it
  is a measurement rather than a judgement — the spike read the printed reference deck's thirteen
  cards and agreed with pymupdf's numbers on two other decks. This was the one question the owner's
  second ruling made unavoidable, and it turned out to cost 150 lines.
- ~~**Does `contents_bound.py` keep measuring on screen?**~~ **Yes, with a smaller claim** — see
  §1 above. Recorded here rather than left to `implement`, because deleting a working measurement is
  not a decision an implementation should take quietly.

## 2. Plan

**The instrument is settled, so this is construction and proof.** The order puts the seeded-defect
proof before the wiring: a gate wired into `check_all.py` before it is known to catch anything is a
gate that will be trusted before it is measured (**L-05**).

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | `tools/deck/printgeom.py` — the stdlib reader: object table, page-tree walk in document order, content stream through a `q`/`Q`/`cm` stack, painted-path bounding boxes | the reader |
| 2 | Ask the deck what each contents sheet carries — entries per sheet, from the DOM, as `printpages.py` asks for `k` | the expected counts |
| 3 | `verdicts(deck, ...)` — `PRINT-2` no two cards in adjacent rows overlap, `PRINT-3` no card reaches the footnote band, and a loud failure when the card count disagrees with step 2 | the producer |
| 4 | **Prove it both ways**: seed the T-116 overlap by reverting the `min()` clamp in a scratch copy, and require `FAIL` there and `pass` on `HEAD` — the same page, the same command | the evidence |
| 5 | A self-test on a PDF built in memory, as `printpages.self_test` does (**L-04**), so a reader that has stopped reading says so before it reports on a deck | the guard |
| 6 | Wire it: `check.py` under the existing `--print-pages`, `audit.py`'s absent-subject sweep and its `exercised` set, `check_all.py`'s `NOT_RUN` reason | the account |
| 7 | Demote `contents_bound.py`'s claim, and say in it what only the printed reading can decide | the corrected tool |
| 8 | Run `python tools/check_all.py`, then **print both shipped decks and look at the contents sheet** | the verdict |

## 3. Implement

**Decisions & assumptions**
- 2026-08-13 — **the reader lives in its own module, `printgeom.py`, not inside `printpages.py`.**
  That file's docstring is emphatic that it asserts the count and only the count, and it is right to
  be; geometry is a second subject with its own rule IDs. They share the print machinery, not the
  file.
- 2026-08-13 — **it rides the existing `--print-pages` flag rather than earning its own.** Both need
  a real Chrome print, so a second flag would only let a caller ask for the count and skip the
  layout, which is the run T-116 shipped through.
- 2026-08-13 — **`PRINT-2` and `PRINT-3` are separate IDs**, so a failure names which of the two
  things went wrong without being read. The seeded run below fails both, and they fail for different
  reasons.
- 2026-08-13 — **the footnote is identified as the last text run painted, not the lowest one.** Paint
  order follows DOM order and the deck appends `.contents-foot` after the grid, so the last run is
  the footnote by construction. Lowest-on-the-page would pick the wrong element on precisely the
  broken sheet this gate exists for: the card that has overflowed its row is the one printing text
  furthest down.

**Outputs produced**

`tools/deck/printgeom.py`, ~330 lines, standard library only. Object table, page tree walked from
`/Root` in document order, content stream through a `q`/`Q`/`cm` stack, bounding box per painted
path, text runs from `Tm`. Cards are the large stroked paths on a contents sheet; the deck is asked
how many each sheet carries and a disagreement fails the gate rather than passing it (**L-36**).

**Measured both ways, on the same page and the same command (L-05)**

| | cards read | `PRINT-2` | `PRINT-3` |
| :--- | ---: | :--- | :--- |
| `examples/reference-deck.html` at `HEAD` | 13 over 1 sheet | pass — no two intersect | pass — every card ends above it |
| the same deck with T-116 seeded back in | 13 over 1 sheet | **FAIL** — cards 5/9, 6/10, 7/11 intersect | **FAIL** — card 13 ends at 798.4 pt, footnote starts at 732.7 pt |

**The seeded numbers agree with T-116's pymupdf reading of the same fault**, which is the
cross-check that matters: that record has the footnote block at 735.7–751.5 pt inside card 13 at
636.0–798.8 pt. This reader, standard library only, puts card 13's bottom at 798.4 and the footnote
top at 732.7 — 0.4 pt on the card, and 3 pt high on the footnote because the band top is taken as
baseline minus font size, which errs towards flagging early rather than late.

**Reverting the `min()` clamp alone did not reproduce the fault, and that is a finding.** The first
seeding attempt changed only `.cbox`'s `max-height` and the deck printed clean, gate green. T-116
was two edits, and the second — clamping a four-row band's description to one line — is what makes
the box tall enough to overhang. So the collision needs both, which is what that task's analysis
says and what nothing had tested. A one-edit revert would have "proved" the gate blind.

**Two more things the work found**

- **`audit.py` described `PRINT-1` as `n + 1`.** T-036 made the printed count `n` + `k` on
  2026-08-13 and the arithmetic in `printpages.py` moved with it; only this absent-subject
  description stayed behind. Corrected in place, dated.
- **`DS-226`'s excusal said a person printing is its only instrument.** It has had a second since
  T-034 and a third since this task. Rewritten to say what each of the three reaches, and what is
  still left to the person — which is the judgement half, not the geometry.

**Where it is wired**

| | |
| :--- | :--- |
| `check.py` | under `--print-pages`, beside `printpages.verdicts` |
| `audit.py` | the absent-subject sweep, its `exercised` set, and `PRINT-2` / `PRINT-3` descriptions |
| `check_all.py` | `NOT_RUN`, with the reason it runs inside `check.py` |
| `contents_bound.py` | claim demoted — it sizes the rule, `printgeom.py` decides the page |

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A decision is recorded, either way, with the cost that decided it | met | §1 *What the instrument costs*. The cost is ~330 lines of standard library, and it is a measurement rather than an estimate — the reader was built before the decision was written down |
| If yes: a seeded overlap is caught and a correct page passes (**L-05**) | met | §3's table. Clean deck passes, seeded deck fails both rows and names five intersecting pairs |
| If no: the limitation is stated where someone about to trust the screen numbers reads it | n/a | The answer was yes. The clause is left standing rather than reworded — `contents_bound.py` got the statement anyway, because a screen tool beside a printed one still needs to say which is which |
| Standard library only, and runs against any deck it is pointed at | met | No import outside the standard library. Measured on a deck outside the repository — the seeded copy lives in a scratch directory with no `.git`, and the tool resolved its output there rather than into the repository (T-074) |
| Refuses a clean verdict when the card count disagrees with the deck's | met | `sheet_problem`, exercised directly by the self-test in both directions. It also fired for real: the first fixture had no `/Root`, read as nought pages, and the run said so instead of passing |
| `check_all.py` accounts for the tool and runs it over both decks | met | `NOT_RUN` with its reason; it runs inside `check.py --print-pages`, which the per-deck line passes for both decks |
| `contents_bound.py` no longer implies the printed page is clean | met | Docstring and closing line both rewritten: it sizes the rule, `printgeom.py` decides the page |
| Both shipped decks printed and **looked at** | met | Reference deck 13 entries over 4 rows, sort-window 12 over 3, footnote clear on both. The seeded sheet was looked at too, which is what confirmed the seed before any verdict was read |

**What the gate now decides that nothing did**

| | reference deck | sort-window |
| :--- | ---: | ---: |
| cards read on the contents sheet | 13 | 12 |
| intersecting pairs | 0 | 0 |
| footnote clearance | clear | clear |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-13 | → done | `printgeom.py` gates the printed geometry of the contents sheet on any deck it is pointed at, standard library only. Both shipped decks pass and were printed and looked at; the seeded T-116 fault fails both rows and names five intersecting pairs. **The seeding is the part worth remembering** — reverting the headline edit alone printed a clean page, so a one-edit revert would have read as a blind instrument, and that is **L-79**. Two stale statements were corrected on the way past: `audit.py` still described `PRINT-1` as `n + 1`, and DS-226's excusal still said a person printing was its only instrument. |
| 2026-08-13 | (no change) | `check_all.py` refused the run with `STALE tools/deck/printgeom.py` — the tool was named in `NOT_RUN` and not tracked by git. The account is doing exactly what it was built for: a checker a clone would not receive is not a checker. Staged, and the re-run is green. |
| 2026-08-13 | → specified, → planned | **The dependency question was answered by building the reader instead of estimating it a third time: standard library, no dependency.** A ~150-line spike read the printed reference deck's thirteen card outlines, its three row gaps and its footnote baseline, and agreed with pymupdf's numbers on two other decks — so the obstacle §1 listed third was a missing CTM stack rather than a property of Chrome's writer. Specified and planned in one pass because the decision the task was raised to take is now taken, and what remains is construction. `contents_bound.py` keeps its measurement and loses its claim about paper. |
| 2026-08-13 | (no change) | **The owner ruled the second open question the same day: any deck the gate is pointed at, not `examples/` alone.** That settles scope and hands `specify` a harder instrument problem than it had — an adopter must be able to run it, so the pure-stdlib question can no longer be dodged by keeping the tool internal. |
| 2026-08-13 | (no change) | The owner supplied a deck built with the plugin outside this repository, printed the day before `0.2.3`. It carries the T-116 collision — four intersecting card pairs and the last card through the footnote — which makes three printed decks with this fault and the first that no gate here would ever have run over. Measured geometry only; nothing from that document is recorded anywhere in this repository. Recorded in §1, with a recommendation against the second open question and one false-positive class the measurement found for free. |
| 2026-08-13 | → proposed | Raised out of T-116, which found a printed collision that the screen measurement reported as clean and that reached two shipped decks. `PH3` and `l`: the instrument is a PDF graphics-state parser or a new dependency, and either way it revisits the owner's 2026-08-08 ruling on what the print gate asserts. |
| 2026-08-13 | (no change) | **The owner answered the same day: yes, narrowly.** Gate *no card overlaps another and none reaches the footnote*, and nothing else. The type stays `decision` because the decision is what was asked for and it is now recorded; the remaining work is the instrument, and this task carries it under its second acceptance criterion. **Stays `PH3` and out of `0.2.3`** — `l` puts it there by the rule in [`../CLAUDE.md`](../CLAUDE.md), and the release it would protect is three tasks that are nearly done. Not `blocked_by` anything. |
