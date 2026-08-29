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
