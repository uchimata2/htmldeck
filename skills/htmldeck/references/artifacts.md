# The artifact contract

Load this at stage 3. It fixes where the two specification files go, what they are called, and what
shape they take. **What makes their content good is
`${CLAUDE_PLUGIN_ROOT}/docs/DESIGN-SYSTEM.md`'s job, not this file's.**

## Where they go, and what they are called

One slug per run, fixed at stage 3 and derived from the governing idea. All three files share it and
sit in one directory — **the directory the deck is delivered to**, which is the user's project
unless they named somewhere else.

```
<slug>.html            the deck
<slug>.foundation.md   the foundation spec, including the outline
<slug>.slides.md       the slide-by-slide specification
```

**Both `.md` files are written on every run**, including one where the user declines both gates.
They are not drafts and not scratch: they are what a reader opens when the deck turns out wrong,
which is the moment nobody remembers what was decided. Writing them into a temporary directory
forfeits the only reason they are unconditional.

Write each one **when its stage produces it**, not at the end. A run that stops halfway should leave
the file the stage before it completed.

---

## Template — `<slug>.foundation.md`

```markdown
# <Deck title>

**Governing idea.** <One sentence, written before anything else.>

**Audience and occasion.** <Who is in the room, and what happens after.>

## Narrative spine

<How the argument moves, in three or four sentences. Not a slide list — the reason the slides
are in this order. This and the governing idea are the only genuinely per-deck design content;
everything below is a selection from a standing catalogue.>

## Selections

| Layer | This deck uses | Catalogue |
| :--- | :--- | :--- |
| Archetypes | <A-nn, A-nn, …> | DESIGN-SYSTEM §3.2 |
| Disclosure | <where tier two lives, and why> | DESIGN-SYSTEM §5.3 |
| Motion | <which of the four, and what each encodes> | DESIGN-SYSTEM §5.2 |
| Visuals | <diagram kinds; charts if any> | DESIGN-SYSTEM §4 |

## Quality bar — additions only

<The standing bar is EVALUATION.md. List only what this deck adds to it, or "none".>

## Sources and the figure ledger

<Omit the table when no sources were supplied, and say so in one line — a presentation-only run
is a legitimate state, and it has to be visible as one.>

| Figure | Value | Origin | Used on |
| :--- | :--- | :--- | :--- |

## Outline

<One row per slide. This is what gate 1 shows. The bottom line here is the sentence that ships
on the slide, not a paraphrase of it (DS-211).>

| # | Archetype | Title — a claim, not a topic | Bottom line |
| :-- | :--- | :--- | :--- |
```

---

## Template — `<slug>.slides.md`

```markdown
# <Deck title> — slide-by-slide specification

Expanded from the outline in `<slug>.foundation.md`, page by page. Seven fields per slide.

## Slide <n> — <title>

- **Archetype.** <A-nn, carried from the outline.>
- **Title.** <The claim, as it ships.>
- **Bottom line.** <The one thing this slide delivers. Visually dominant, never behind a
  disclosure, stated factually — DESIGN-SYSTEM §3.4.>
- **Structure.** <The layout: what sits where, and what is tier one versus tier two.>
- **Text.** <Every string that ships, or the rule that generates it.>
- **Visuals.** <The diagram or chart, and what it encodes. "None" is an answer.>
- **Animations.** <What each one encodes. If the answer is "it looks good", remove it.>
- **Interactive elements.** <What opens, and what it reveals. Tier one must read with everything
  closed.>

## Open — needs a decision

<From the specification review. Anything the review could not settle stays here, unresolved and
named. Do not guess one closed; an unanswered question recorded as answered is the defect this
section exists to prevent.>

| # | The question | Why it matters | Proposed |
| :-- | :--- | :--- | :--- |
```
