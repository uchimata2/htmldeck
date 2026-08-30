# Owed looks — what a person still has to see before the release is cut

**Tier 3. Loaded by nothing**; opened twice — once by a session closing a task that changed what a
deck renders, and once by the owner running the pass.

[`REMEDIATION-ORDER.md`](REMEDIATION-ORDER.md) §4 rules that **the one thing an unattended session
may not do is look**. A task owing a look does everything measurable, records the look as **owed**,
and closes; the owed looks accumulate here; the owner runs **one pass** over them, and that pass
happens **before the release is cut**. That last clause is what keeps
[`../CLAUDE.md`](../CLAUDE.md) rule 6 true rather than merely deferred.

**This file is the queue that sentence describes.** It did not exist until 2026-08-29, so the record
lived in whichever of 273 task files wrote it and the pass had nothing to run
([T-273](../tasks/T-273-the-owed-looks-have-no-queue-to-accumulate-in.md)).

## How to write a row

**Name the deck, the slide and the question — never the diff.** A diff says what moved; a look
answers whether it reads, and the two need different sentences. *One SVG label is now one line where
it was two: does it read as well against its three siblings?* is answerable in ten seconds. *Changed
a text element* is not answerable at all.

**Nothing here is checked by a program, and that is deliberate.** The only thing a gate could decide
is whether this file was edited, which is not whether anybody looked. A row nobody wrote is a look
nobody owed, and the honesty of the queue is the discipline rather than a green verdict.

**A task that changes nothing a reader sees writes no row**, and says so in its own record instead —
six of B5, B6 and B7's seven tasks did exactly that. An empty queue after a batch of checker work is
the correct answer, not a gap.

**Name the slide, and give its number the way the deck numbers itself.** The first row written here
said *slide 7* for a slide the deck calls 4, and the owner corrected it. Counting `<section>`
elements would have given 5 — a lobby (`data-stage="front"`) is front matter and is counted in no
stage, so the element index and the reader's number differ by one from the first lobby onwards. **A
`data-name` cannot be off by one**, so lead with it and let the number follow.

## The queue

Two outstanding.

| # | Deck | Where | What to look for | Owed by |
| :-- | :--- | :--- | :--- | :--- |
| 10 | [`examples/portfolio-review/portfolio-review.html`](../examples/portfolio-review/portfolio-review.html) | *Three tranches, one gate*, slide 11 - the timeline's **first** segment, the one running into the gate | It is now a flowing dashed line (`Current`) where it was a plain rule, and the segment **after** the gate is deliberately left plain. The asymmetry is the encoding: what the gate measures accrues before it and not after it. *Does the moving segment read as the realised discount accruing into the gate, or as decoration on a schedule - and does the plain second segment read as deliberate rather than as a line somebody forgot?* Also worth a glance with `Motion` off, where both segments should read as dashed and still. | [T-257](../tasks/T-257-ds-218-passes-the-shipped-example-vacuously.md) |
| 11 | [`examples/reference-deck.html`](../examples/reference-deck.html) | the chrome row, on any slide - the `More` menu **open**, in a picture rather than in a browser | This is the first capture of a state that only exists after a click, so the question is about the PICTURE and not about the deck. Run `python tools/deck/render.py state examples/reference-deck.html --click "#moreBtn" --watch "#moreMenu" --shot` and open the PNG. *Is the open menu wholly inside the frame, fully painted, and legible enough to review the menu from - or is it clipped at the window edge, or caught half-drawn?* Measurement says the state is in the file - the shot is 250 KB against 69 KB at rest, and a no-op `state --shot` is byte-identical to `shots` - but no measurement here says the picture is USABLE, which is the whole point of the command. | [T-267](../tasks/T-267-render-py-cannot-capture-a-decks-interactive-states.md) |

## What has already been looked at

A look that has happened stops being owed **without its row being deleted** — a deleted row is a
look nobody can show was taken.

| # | Deck | Where | The question, and the answer | Owed by | Looked |
| :-- | :--- | :--- | :--- | :--- | :--- |
| 1 | [`examples/measure-first/measure-first.html`](../examples/measure-first/measure-first.html) | slide 4, *The loop that never closes* — the four-node cycle diagram, the node at the left | Its label became **one line**, `What sold`, where it was two, `What` / `actually sold`, set at the midpoint of the two old lines where its three sibling nodes' single lines sit. *Does the single line read as well as the pair did, and does the node still balance against its three siblings?* — **Yes.** The owner looked and confirmed it reads correctly | [T-229](../tasks/T-229-ds-106s-check-omits-a-word-the-rule-names.md) | 2026-08-29, by the owner |
| 2 | [`examples/measure-first/measure-first.html`](../examples/measure-first/measure-first.html) | slide 5, *Poor exactly where we decide* — the six-dimension scale | The thirty dots printed **absent** before the fix: they animate from `scale(0)` with `fill:both`, print never advances an animation, and the print block did not switch them off. *Are all thirty on the paper, at their right size?* — **Yes.** The owner printed it: all 30 dots visible, and they read well | [T-232](../tasks/T-232-two-entrance-motions-do-not-collapse-for-print.md) | 2026-08-29, by the owner |
| 3 | [`examples/reference-deck.html`](../examples/reference-deck.html) | slide 9, *Month eighteen stays reversible* — the flow's arrowheads | The same defect on the other motion: `.arrow-pop marker path` scales from `scaleX(0)`, so the arrowheads printed as nothing. *Is every arrowhead there?* — **Yes.** The owner printed it and saw one highlighted head and one plain one, **which is every arrowhead the slide has**: it defines two markers, `ar9` and `ar9q`, and uses each once. Counted after the look rather than assumed, because *two* would read as a shortfall against a flow diagram anyone would expect to carry more | [T-232](../tasks/T-232-two-entrance-motions-do-not-collapse-for-print.md) | 2026-08-29, by the owner |
| 4 | [`examples/reference-deck.html`](../examples/reference-deck.html) | slide 12, *Approve the frequency package* — the ask itself | The first card reveal. Turn replaced Rise on the closing headline: it scales up from its own centre line over 420 ms instead of rising. *Does turning the ask face-up land the deck, or read as a flourish on the slide that should be plainest?* — **It reads correctly.** The owner looked and passed it, so the placement stands | [T-274](../tasks/T-274-build-the-card-reveal-so-turns-two-dials-have-a-reader.md) | 2026-08-29, by the owner |
| 5 | [`examples/reference-deck.html`](../examples/reference-deck.html), and the same row on `sort-window` and `measure-first` | the chrome row, on any slide — the `More` menu open, and the row with it shut | *Motion* moved back inside the menu, so the row lost a button and the menu gained a second item. *Does the open menu read with two rows where it had one, and does the row still balance with only `More` outside the navigation box?* — **Yes, both.** The owner looked: *exactly how I wanted, perfect like this*. **And they ruled the wider point in the same breath — this is not an exception, it is how it should be**, which is the menu form as the norm rather than a tolerated placement | [T-277](../tasks/T-277-put-motion-back-inside-the-more-menu.md) | 2026-08-29, by the owner |
| 6 | [`examples/portfolio-review/portfolio-review.html`](../examples/portfolio-review/portfolio-review.html) | any slide carrying a provenance mark — the `Portfolio model` control, on more than one slide | The deck carried **eleven** copies of that source and now carries one, shared by all eleven controls through `data-qv`. *Open the quick view from two different slides and confirm both show the document, and that closing one does not leave the other empty.* — **Yes.** The owner opened it from more than one slide and confirmed **the same document displays on multiple pages**, which is the property the eleven copies were paying for and one template now provides | [T-233](../tasks/T-233-a-shipped-deck-carries-eleven-copies-of-one-source.md) | 2026-08-30, by the owner |
| 7 | [`examples/reference-deck.html`](../examples/reference-deck.html) | slide 1, *Waiting is the trip*, the bottom line — and slide 10, *Holding is not the cheap option*, the third cost | The claim slide now reads *Spend $4.1M of the $5.6M grant on bus frequency, and hold $1.5M for bike-share until month 18*, one word-group longer than before, and slide 10's third cost became *The whole $5.6M is committed now or it lapses, so the $1.5M is locked to the gate.* *Does the longer bottom line still sit as the layout intends, does the contents entry still read as a sentence, and does slide 10's cost still read as a cost?* — **Yes, all three.** The owner confirmed it | [T-248](../tasks/T-248-four-content-errors-in-three-shipped-decks.md) | 2026-08-30, by the owner |
| 8 | [`examples/portfolio-review/portfolio-review.html`](../examples/portfolio-review/portfolio-review.html) | slide 6, *The best year is a mark* — the annotation, the bottom line and the disclosure's heading | `$131M` became `$102M` in three places and the disclosure heading changed from *What the $131M is* to *The three largest lines*, because the third asset in that table is transmission and not renewables. *Does the heading still say what the panel contains now that it names no figure, and does the slide still read as a concentration argument at $102M of $172M?* — **Yes.** The owner confirmed it | [T-248](../tasks/T-248-four-content-errors-in-three-shipped-decks.md) | 2026-08-30, by the owner |
| 9 | [`examples/sort-window/sort-window.html`](../examples/sort-window/sort-window.html) | slide 5, *The night the window closes* — the night-flow figure's **first** lane | The first trunk now clears at **22:57** instead of 00:14, so its bar is shorter: 674 px became **485**, its mid label reads `6,200/hr` where it read `sort at 3,100/hr`, and `clears 22:57` sits at the new bar end. **The geometry was recomputed from the lane's own scale — 2.46 px a minute — and never rendered**, which is what this row was for. *Do the first lane's three labels sit clear of each other, and is the gap to the second trunk's 23:40 legible as the 43 minutes of headroom the deck now argues from?* — **Yes, both.** The owner looked and confirmed the labels read clear and the headroom is legible | [T-281](../tasks/T-281-the-sort-windows-capacity-story-cannot-hold-its-own-failure-table.md) | 2026-08-30, by the owner |
