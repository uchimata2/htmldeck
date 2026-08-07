---
name: htmldeck
description: Build or critique a single-file HTML presentation that does not look generated — one .html that opens by double-clicking, renders with the network disabled, and carries real diagrams, progressive disclosure and considered typography. Use when the user asks for a presentation, slide deck, pitch deck, slides, or an HTML deck; when they want an existing deck reviewed, critiqued or scored; or when they point at a .html deck and ask for changes. Asks exactly two questions.
---

# htmldeck

One pipeline. **Two questions up front, both specification files written every time, two gates the
user can decline.**

## Ask exactly two questions

Ask both together, before anything else, and ask nothing else:

1. **How long should it be?** A maximum and/or a minimum.
2. **Anything to align to?** An existing brand, a deck, or source documents. Optional.

**Unanswered is a valid answer to both.** Defaults: **8–12 slides**, no alignment material, both
gates on. These produce a good deck — that is what the defaults are for.

**Never ask a third question.** Every other decision is already made in the design system, and
asking is the failure this plugin exists to prevent. If something seems to need asking, it is
either already decided in `${CLAUDE_PLUGIN_ROOT}/docs/DESIGN-SYSTEM.md` or it is yours to decide.

**Never ask whether to skip the gates.** Unprompted, both gates are on. If the user volunteers
"no gates", "just build it", or names one of the two, honour exactly that. Asking would be a
third question.

## Then run the pipeline

Load `${CLAUDE_PLUGIN_ROOT}/skills/htmldeck/references/pipeline.md` and follow it. Seven stages,
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
copies drift apart. Every path is written from `${CLAUDE_PLUGIN_ROOT}`, because a bare path would
resolve against the user's project, which may well have a documentation folder of its own.

| Load | When |
| :--- | :--- |
| `${CLAUDE_PLUGIN_ROOT}/skills/htmldeck/references/pipeline.md` | First, on every build run |
| `${CLAUDE_PLUGIN_ROOT}/skills/htmldeck/references/artifacts.md` | At stage 3, before writing either specification file |
| `${CLAUDE_PLUGIN_ROOT}/docs/DESIGN-SYSTEM.md` | Before the outline (§3.2 archetypes, §3.4 the deliverable) and before any HTML (all of it) |
| `${CLAUDE_PLUGIN_ROOT}/docs/EVALUATION.md` | At either review stage |
| `${CLAUDE_PLUGIN_ROOT}/examples/reference-deck.html` | When writing HTML — the structural reference, not a template to fill |

**Never load `${CLAUDE_PLUGIN_ROOT}/docs/DESIGN-RATIONALE.md`** — it explains why the rules are what
they are, and nothing at runtime needs that. Nor `${CLAUDE_PLUGIN_ROOT}/docs/BRIEF.md`,
`${CLAUDE_PLUGIN_ROOT}/docs/research/` or `${CLAUDE_PLUGIN_ROOT}/tasks/`: those are how the plugin
was built, not how a deck is.

## The rules that decide the rest

`${CLAUDE_PLUGIN_ROOT}/docs/DESIGN-SYSTEM.md` §0 carries nine. Four shape a run before any rule
is looked up:

- **Every slide delivers one thing and says it on the slide.** The audience must never wait for the
  presenter to reach the point.
- **Portable or it does not ship.** One file, zero external references, opens from `file://`. Not a
  size problem — a full deck with three embedded faces is under 200 KB.
- **The headline is a claim, not a topic.**
- **Motion must encode something.** *What does this animation encode?* If the answer is "it looks
  good", remove it.

## Critique without building

When the user wants an existing deck reviewed rather than a new one built, the two questions do not
apply — there is nothing to size and nothing to align. Load
`${CLAUDE_PLUGIN_ROOT}/docs/EVALUATION.md` and run the design audit: headline verdict first, then
the coverage table, then findings naming the principle each one violates, then an explicit
keep-versus-rebuild split.

**The critique voice is blunt — bottom line up front, no diplomatic padding.** A review that opens
with three compliments is one nobody acts on. **The deck's own voice is the opposite**: respectful,
positive, professional.

## Say which half was checked

When sources were supplied, reconcile the deck against them *and* the sources against each other —
every figure on a slide appears in a source with the same value, and every figure used twice agrees
with itself.

When they were not, the run is presentation-only. **Say so in the output.** A presentation-only
check presented as a clean pass is a false one.
