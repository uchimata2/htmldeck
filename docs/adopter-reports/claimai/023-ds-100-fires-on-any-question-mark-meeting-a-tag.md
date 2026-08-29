# DS-100 fires on any `?` that meets a tag, including a question the slide answers

| Field | Value |
| :--- | :--- |
| **Target** | `htmldeck` — Gábor's own repository, cloned under `C:\Work\AgentPlugins` |
| **Kind** | Defect |
| **Status** | `deferred` — read 2026-08-29 by [T-270](../../../tasks/T-270-two-rules-whose-escape-hatch-teaches-the-wrong-habit.md), and **`DS-100` is unchanged**. The finding is accepted: the escape hatch this report names — draw the word as a shape — is a real cost and worse than the rule. **Proposal 1 was ruled and then refused by measurement.** Its condition, *a `?` followed within the slide by a declarative bottom line*, holds on **38 of 38** slides across htmldeck's three decks: the component contract puts exactly one `.bottom-line` on every slide and `DS-202` requires it to be one factual sentence, so the guard is true by construction. Written as proposed it is not a narrowing but an off switch, and it would have taken a `hard` rule to zero findings behind a green verdict. Proposal 2, *make the rule reviewable*, was refused by the owner: `reviewable` is how a rule quietly stops being enforced. **What `DS-100` should measure instead is now an open question with the owner**, recorded in [`REMEDIATION-ORDER.md`](../../REMEDIATION-ORDER.md) §3 with a recommendation — narrow by where the question sits, so a `?` in a slide's `<header>` fails and one in body copy passes, which admits both cases in this report — and with that recommendation's own limit stated: all three decks carry zero `?` in copy, so there is no firing rate to calibrate against. |
| **Severity** | Low — one word, but the author asked for it twice and it had to be drawn as a shape to get past the check |
| **Found while** | Sharpening slide 1's copy on 2026-08-24 — `E40`; again building round 2's motion on 2026-08-26 — `E66` |
| **Version seen** | 0.6.0 |

## What happens

`DS-100` forbids rhetorical questions. Its check fires on any `?` immediately preceding a tag — which
is where a question mark lands whenever the question is the last thing in an element.

Two questions in this deck are not rhetorical. One is the board's own question, which the slide
answers on the same face. The other is the word *Why?*, which the author asked for by name. Both
failed.

**The rule's own code already draws the distinction it needs.** It exempts a question a *source*
asks. It has the concept; it just does not extend it to a question the deck itself puts and then
answers.

## The workarounds, and what they cost

- The board's question was **quoted**, which the check reads correctly. That is honest here, because
  it really is a quotation — but quoting to satisfy a checker is a bad habit to teach.
- *Why?* was **drawn as a shape** rather than written as text, so no `?` meets a tag. The word is now
  invisible to every text instrument in the toolchain — the readability check, the copy audit and any
  future translation pass.

The second is the real cost: a rule about rhetoric pushed content out of the text layer entirely.

## What to change

1. **Extend the existing source-question exemption** to a question the same slide answers — the
   condition is checkable: a `?` followed, within the slide, by a declarative bottom line.
2. **Or make the rule reviewable rather than fatal.** A rhetorical question is a judgement. A build
   that refuses one is stronger than the judgement warrants, and the escape hatch it leaves is
   *draw the word as a picture*.
