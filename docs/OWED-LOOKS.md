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

Empty. Nothing outstanding.

| # | Deck | Where | What to look for | Owed by |
| :-- | :--- | :--- | :--- | :--- |

## What has already been looked at

A look that has happened stops being owed **without its row being deleted** — a deleted row is a
look nobody can show was taken.

| # | Deck | Where | The question, and the answer | Owed by | Looked |
| :-- | :--- | :--- | :--- | :--- | :--- |
| 1 | [`examples/measure-first/measure-first.html`](../examples/measure-first/measure-first.html) | slide 4, *The loop that never closes* — the four-node cycle diagram, the node at the left | Its label became **one line**, `What sold`, where it was two, `What` / `actually sold`, set at the midpoint of the two old lines where its three sibling nodes' single lines sit. *Does the single line read as well as the pair did, and does the node still balance against its three siblings?* — **Yes.** The owner looked and confirmed it reads correctly | [T-229](../tasks/T-229-ds-106s-check-omits-a-word-the-rule-names.md) | 2026-08-29, by the owner |
| 2 | [`examples/measure-first/measure-first.html`](../examples/measure-first/measure-first.html) | slide 5, *Poor exactly where we decide* — the six-dimension scale | The thirty dots printed **absent** before the fix: they animate from `scale(0)` with `fill:both`, print never advances an animation, and the print block did not switch them off. *Are all thirty on the paper, at their right size?* — **Yes.** The owner printed it: all 30 dots visible, and they read well | [T-232](../tasks/T-232-two-entrance-motions-do-not-collapse-for-print.md) | 2026-08-29, by the owner |
| 3 | [`examples/reference-deck.html`](../examples/reference-deck.html) | slide 9, *Month eighteen stays reversible* — the flow's arrowheads | The same defect on the other motion: `.arrow-pop marker path` scales from `scaleX(0)`, so the arrowheads printed as nothing. *Is every arrowhead there?* — **Yes.** The owner printed it and saw one highlighted head and one plain one, **which is every arrowhead the slide has**: it defines two markers, `ar9` and `ar9q`, and uses each once. Counted after the look rather than assumed, because *two* would read as a shortfall against a flow diagram anyone would expect to carry more | [T-232](../tasks/T-232-two-entrance-motions-do-not-collapse-for-print.md) | 2026-08-29, by the owner |
| 4 | [`examples/reference-deck.html`](../examples/reference-deck.html) | slide 12, *Approve the frequency package* — the ask itself | The first card reveal. Turn replaced Rise on the closing headline: it scales up from its own centre line over 420 ms instead of rising. *Does turning the ask face-up land the deck, or read as a flourish on the slide that should be plainest?* — **It reads correctly.** The owner looked and passed it, so the placement stands | [T-274](../tasks/T-274-build-the-card-reveal-so-turns-two-dials-have-a-reader.md) | 2026-08-29, by the owner |
