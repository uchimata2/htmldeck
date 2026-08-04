# htmldeck — working conventions

Read this before doing anything in this folder.

## What this is

A publishable Claude Code plugin: **single-file HTML presentations that don't look generated**,
plus the prompt structure that briefs them and the critique pass that fixes them.

Grounded in a corpus of ~10 real decks produced across a training programme. `docs/BRIEF.md`
records what that evidence shows and what to build; `reference/` holds the source prompt.
**Status: not started.** Read the brief first.

## The rules that must survive

1. **Self-contained or it doesn't ship.** One `.html` that renders correctly with the network
   disabled. Every deck in the source corpus failed this — 2–7 external references each, mostly
   web fonts. Fixing it while keeping the typography is the plugin's main technical problem.
2. **Diagrams are inline SVG.** Never raster images, never an external chart library. They scale,
   they theme, they diff.
3. **Decks must not look like each other.** The corpus decks read as designed *because* they
   don't share a template. A plugin shipping one house style produces one house look — which is
   the problem it exists to solve.
4. **Look at the rendered deck.** A deck that validates is not a deck that reads well.
5. **Critique is a first-class mode**, not a footnote. It is what turns a first draft into
   something worth presenting, and it is the part users cannot do for their own work.

## Voice

The critique mode is blunt on purpose — bottom line up front, then section by section, no
diplomatic padding. A review that opens with three compliments is one nobody acts on. This is a
deliberate choice carried from the corpus, where the harshest review was the most useful
artifact in it.

That applies to the critique output. The **decks** themselves stay respectful, positive and
professional, and avoid the terminology that marks text as machine-written — ship that list and
enforce it at build time rather than hoping.

## Working method

1. **No work without a task file** in `tasks/`, from `tasks/_templates/task-template.md`.
2. Lifecycle: `specify → plan → implement → review`.
3. A task is `done` only when its deliverables exist, its log is current, and any deck it
   produced has been **opened and looked at** — offline.

## Publishing constraints

This repository goes to GitHub. Everything written here must be:

- **Free of personal, client and machine data.** The source corpus is training work for real
  named scenarios; **do not copy deck content into this repository.** Patterns, structure and
  measurements only. Any example deck shipped here must be written fresh on a neutral topic.
- **Out-of-the-box.** Clone and run, no path editing.
- **Font-licence aware.** If fonts are embedded, only ones whose licence permits redistribution.
  Record the licence next to each.

## Verifying

Test the generator on a **real 12-slide deck with diagrams**, not a three-slide toy — the corpus
decks are the target case, and that is the size where layout and pacing problems appear. State
results as what was actually produced, not as "works".
