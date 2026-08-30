---
name: htmldeck
description: Build or critique a single-file HTML presentation that does not look generated — one .html that opens by double-clicking, renders with the network disabled, and carries real diagrams, progressive disclosure and considered typography. Use when the user asks for a presentation, slide deck, pitch deck, slides, or an HTML deck; when they want an existing deck reviewed, critiqued or scored; or when they point at a .html deck and ask for changes. Asks exactly two questions.
---

# htmldeck

One pipeline. **Two questions up front, both specification files written every time, two gates the
user can decline.**

## 0. Resolve `$HTMLDECK` first, before any command below

Every path in this skill is written from `$HTMLDECK`, the plugin's own directory — a bare path would
resolve against the user's project, which may well have a `docs/` of its own.

**Read it off this file's own location.** A harness that loads a skill names the directory it loaded
it from. This file is `$HTMLDECK/skills/htmldeck/SKILL.md`, so `$HTMLDECK` is two directories above
it. That answer is already version-correct, and it is the only one that works for a copy of this
plugin published under another name.

**If your harness does not name it**, resolve it once, in your first shell call:

```
ls -d "$HOME"/.claude/plugins/cache/*/htmldeck/*/ | sort -V | tail -1
```

**`sort -V` is load-bearing.** The cache keeps every version ever installed, so a first-match glob
picks the oldest and the failure reads as *tool not found*. In a clone of the repository,
`$HTMLDECK` is the clone.

Then **substitute the printed path literally** into every later command. Shell state does not
persist between calls, so an assignment made in one is gone in the next.

**Never write a plugin-root placeholder into a command.** Claude Code substitutes its own into a
plugin's files *before you read them* — this file included, which is why this paragraph does not
spell it out. The value is **not exported into the shell**, so a command written from it arrives
with no base at all and runs against the drive root. This skill used to spell every command that
way. The first outside build read these documents in full, never used the placeholder once, and
hardcoded a version-pinned cache path **87 times** instead — one plugin update away from being
wrong, in a session that had updated the plugin an hour earlier (T-189).

**Re-resolve after a plugin update**, and never carry a version number in a path you keep.

## Ask exactly two questions

Ask both together, before anything else, and ask nothing else:

1. **How long should it be?** A maximum and/or a minimum.
2. **Anything to align to?** An existing brand, a deck, or source documents. Optional.

**Unanswered is a valid answer to both.** Defaults: **8–12 slides**, no alignment material, both
gates on. These produce a good deck — that is what the defaults are for.

**Never ask a third question.** Every other decision is already made in the design system, and
asking is the failure this plugin exists to prevent. If something seems to need asking, it is
either already decided in `$HTMLDECK/docs/DESIGN-SYSTEM.md` or it is yours to decide.

**Never ask whether to skip the gates.** Unprompted, both gates are on. If the user volunteers
"no gates", "just build it", or names one of the two, honour exactly that. Asking would be a
third question.

## Then run the pipeline

Load `$HTMLDECK/skills/htmldeck/references/pipeline.md` and follow it. Seven stages,
two gates:

```
governing idea → requirements → foundation spec (with the outline) → OUTLINE SIGN-OFF
    → slide-by-slide spec → spec review → DETAILED-SPEC SIGN-OFF
        → build, in batches → build review → owner review → fix
```

**Both `.md` specification files are written on every run**, gates or no gates, beside the deck and
named after it. They are the trace of what was decided.

## What to load, and when

Load on demand — **none of it belongs in this file**, and paraphrasing any of it here is how the two
copies drift apart. Every path is written from `$HTMLDECK`, because a bare path would
resolve against the user's project, which may well have a documentation folder of its own.

| Load | When |
| :--- | :--- |
| `$HTMLDECK/skills/htmldeck/references/pipeline.md` | First, on every build run |
| `$HTMLDECK/skills/htmldeck/references/artifacts.md` | At stage 3, before writing either specification file |
| `$HTMLDECK/skills/htmldeck/references/build.md` | At stage 6, before any HTML |
| `$HTMLDECK/skills/htmldeck/references/critique.md` | At either review stage, and for a review with no build |
| `$HTMLDECK/docs/DESIGN-SYSTEM.md` | Before the outline (§3.2 archetypes, §3.4 the deliverable) and before any HTML (all of it) |
| `$HTMLDECK/docs/EVALUATION.md` | At either review stage |
| `$HTMLDECK/examples/reference-deck.html` | When writing HTML — the structural reference, not a template to fill |

**Never load `$HTMLDECK/docs/DESIGN-RATIONALE.md`** — it explains why the rules are what
they are, and nothing at runtime needs that. Nor `$HTMLDECK/docs/BRIEF.md`,
`$HTMLDECK/docs/research/` or `$HTMLDECK/tasks/`: those are how the plugin
was built, not how a deck is.

## The rules that decide the rest

`$HTMLDECK/docs/DESIGN-SYSTEM.md` §0 carries nine. Four shape a run before any rule
is looked up:

- **Every slide delivers one thing and says it on the slide.** The audience must never wait for the
  presenter to reach the point.
- **Portable or it does not ship.** One file, zero external references, opens from `file://`. Not a
  size problem — embedding is cheap. Measured 2026-08-30, the four decks this repository
  ships run 316 to 427 KB, every one of them with three embedded faces and zero external
  references.
- **The headline is a claim, not a topic.**
- **Motion must encode something.** *What does this animation encode?* If the answer is "it looks
  good", remove it.

## Critique without building

When the user wants an existing deck reviewed rather than a new one built, the two questions do not
apply — there is nothing to size and nothing to align. Load
`$HTMLDECK/skills/htmldeck/references/critique.md` and run the design audit: headline
verdict first, then the coverage table, then findings naming the principle each one violates, then
an explicit keep-versus-rebuild split.

**The critique voice is blunt — bottom line up front, no diplomatic padding.** A review that opens
with three compliments is one nobody acts on. **The deck's own voice is the opposite**: respectful,
positive, professional.

## Say which half was checked

When sources were supplied, reconcile the deck against them *and* the sources against each other —
every figure on a slide appears in a source with the same value, and every figure used twice agrees
with itself.

When they were not, the run is presentation-only. **Say so in the output.** A presentation-only
check presented as a clean pass is a false one.
