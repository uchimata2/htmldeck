---
id: T-009
title: Analyse the corpus — extract the deck conventions already in use
type: research
status: done
phase: review
parent: null
blocked_by: []
related: [T-014]
work_package: WP1
shipped_in: 0.1.0
owner: maintainer
created: 2026-08-06
updated: 2026-08-12
deliverables: [docs/research/R1-corpus-conventions.md, docs/research/R1-rules-candidate.md, tools/kb/extract.py]
---

# T-009 — Analyse the corpus — extract the deck conventions already in use

## 1. Specify

**Outcome**
A detailed, evidence-backed analysis of the rules the owner already applies when building HTML
decks, covering every dimension the plugin must span, with each rule traced to the files that
show it and marked as **dominant** (most decks), **variant** (some) or **one-off**.

**Why this one**
This is the project's first task by the owner's direction: the plugin exists to encode *their*
taste, so the conventions must be read off their own work rather than invented. The corpus already
contains explicit written conventions — style guides, presentation specs, audit and consistency
documents, feedback prompts — not just artefacts, which makes this cheaper and far more reliable
than inferring from HTML alone.

**Scope**
- In: the ~14 real decks, the written spec/style/audit/feedback documents, the SVG assets, the
  helper scripts, and the deck-related task files. Both the *stated* conventions and the *actual*
  ones, with disagreements between them called out.
- In: all thirteen dimensions the plugin must cover — writing style · UX · UI controls · colour
  scheme · design language · structure · content practice · headings and subtitles · illustration
  graphics · icons · diagrams · layout · external tooling and skills relied on.
- In: **the progressive-disclosure patterns specifically** — every turning card, toggle, tab,
  floating layer and tooltip in the corpus, how each is implemented, whether it survives printing,
  and what kind of content the owner puts behind interaction versus on the face of the slide.
  This is the owner's signature technique and it feeds T-016 directly.
- Out: deciding anything. This task measures; T-001, T-006 and T-007 decide.
- Out: Notion exports, the EU-AI-Act source page, and other third-party HTML — they are not the
  owner's design work.

**Inputs**
- The corpus root and its high-value files — see the `deck-corpus-location` project memory.
- `docs/BRIEF.md` (the earlier ~10-deck sample; this task supersedes and extends its measurements)

**Method**
Count, don't read — per the carried lesson in the brief. Deduplicate `_export/LocalWorkFiles/`
and `- Backup/` copies before counting anything, or every measurement is inflated.

**Acceptance criteria**
- [ ] Every deck in scope listed with slide count, inline-SVG count, external-reference count,
      script count, font stack, palette (hex), and file size
- [ ] Each of the thirteen dimensions has a section stating the rule, its evidence, and its
      frequency label
- [ ] The written style guides and specs are summarised, and every place the decks *contradict*
      them is listed
- [ ] The banned/AI-tell terminology list is extracted verbatim from the corpus
- [ ] Recurring slide archetypes catalogued (title, agenda, comparison, matrix, timeline, close…)
      with how often each appears
- [ ] Contains no client names, personal data, machine paths, or copied slide copy

**Open questions**
- Where the corpus disagrees with itself, does the most recent deck win, or the one the owner
  rates highest? — owner

## 2. Plan

**Approach — a knowledgebase first, rules second.** Set by the owner 2026-08-06: extract once, at
full fidelity, so no later task has to reopen the private notes folder. Three refinements on that:

1. **Two tiers, because scrubbing and fidelity conflict.** `.kb/` holds the full-fidelity
   extraction — real palettes, real CSS, real prose samples, real file provenance — and is
   **gitignored**, since it necessarily carries client and personal data. `docs/research/R1-*.md`
   holds the scrubbed, publishable analysis. A single scrubbed artefact would lose exactly the
   detail whose absence forces a return to the private source folder — the thing this is meant to
   prevent.
2. **Mechanical before interpretive.** A script emits the counts and inventories as JSON so the
   numbers are reproducible rather than remembered — the brief's "count, don't read". The script
   ships with a self-test on a deck whose answer is known by hand, per "verify the checker on a
   known case"; the corpus already contains one scan that was believed and wrong by 15×.
3. **A gaps register.** Where the corpus has no convention for a dimension, that silence is a
   finding, not a blank. It is the handoff to T-010 and T-011, and it is what "answering questions
   nobody asked" means in practice.

The rule set is *candidate* output here. Choosing what to keep and drop is T-014's job; this task
must not pre-empt it, only supply evidence good enough to decide on.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Deduplicate, classify, and fix the corpus inventory | `.kb/inventory/files.json` |
| 2 | Build and self-test the measurement script | `tools/kb/extract.py` + self-test |
| 3 | Measure every deck mechanically (refs, SVG, fonts, palette, structure, interaction) | `.kb/inventory/decks.json` |
| 4 | Extract the written specs, style guides, audits and feedback prompts with provenance | `.kb/sources/` |
| 5 | Diff stated conventions against actual practice | `.kb/analysis/contradictions.md` |
| 6 | Write up by dimension, scrubbed | `docs/research/R1-corpus-conventions.md` |
| 7 | Emit candidate rules with IDs, frequency labels and evidence, plus the gaps register | `docs/research/R1-rules-candidate.md` |

## 3. Implement

**Decisions & assumptions**
- **Stated conventions beat observed practice where they conflict** — 2026-08-06. The written specs
  consistently run ahead of the artefacts; they read as refined intent, the older decks as work that
  predates them. Flagged to the owner as R1's one open question, because it is load-bearing for
  `prefers-reduced-motion` (stated absolute, delivered 5/12).
- **Deck IDs D1–D12 assigned by slide count**, mapped in the gitignored `.kb/analysis/deck-index.md`
  — 2026-08-06. Lets the published analysis stay anonymous without losing traceability.
- **Corpus path moved out of `tools/kb/extract.py` into gitignored `.kb/config.json`** — 2026-08-06.
  The script publishes; the path names a person and a client tree. Caught by the scrub check, not by
  design.
- **11 HTML files excluded as non-decks** (<4 slide containers or <4 KB) — diagram fragments and
  document exports, not design work.
- **Library fingerprints were wrong on first run** — a blanket case-insensitive flag made `THREE.`
  match the word "three." in prose and reported three.js in two decks that never referenced it.
  Caught by checking every detection against the verbatim URL list. Flags are now scoped.

**Outputs produced**
- `tools/kb/extract.py` — measurement, 20-assertion self-test on a hand-counted case
- `.kb/inventory/files.json` — 346 unique files classified, 3 content duplicates collapsed
- `.kb/inventory/decks.json` — 12 decks fully measured
- `.kb/analysis/deck-index.md` — the scrub key
- `.kb/sources/written-conventions.md` — sources S1–S4
- `.kb/sources/written-conventions-2.md` — sources S5–S10, the second sweep
- `.kb/analysis/libraries.json` — library and CDN usage per deck
- `docs/research/R1-corpus-conventions.md` — scrubbed analysis
- `docs/research/R1-rules-candidate.md` — **154 candidate rules in 14 categories**, 5 gaps closed
  and 9 open, 11 contradictions

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every deck listed with slide count, SVG, external refs, scripts, fonts, palette, size | met | `.kb/inventory/decks.json`; summarised in R1 §2–6 |
| Each of the thirteen dimensions has a rule, evidence and frequency label | met | R1-rules-candidate §A–K, 60 rules |
| Written guides summarised and contradictions with the decks listed | met | R1 §7, five contradictions |
| Banned-terminology list extracted verbatim | **not met** | The corpus contains one example, "friction, etc". Raised as gap G-8 — the list must be built, not extracted |
| Recurring slide archetypes catalogued with frequency | met | Initially judged unmet. Two foundation specs name and reuse archetype sets; catalogued as rule L3. G-2 closed |
| No client names, personal data, machine paths or copied slide copy | met | Automated scrub over `docs/` and `tools/` returns clean; `.kb/` confirmed gitignored |
| Progressive-disclosure patterns catalogued | met | R1 §6 signal table plus the stated rules; feeds T-016 |

**All seven criteria met after the second sweep.** Two were reported unmet on the first pass, and
both were wrong: the material existed in documents not yet read, not in a silent corpus. Five of the
twelve original gaps closed the same way. **The lesson is the corpus's own** — reviewing the
convenient source rather than the authoritative one is how a whole business case went missing in the
audit this task extracted (rule M11).

**Child fix tasks raised**
- none — the two unmet criteria are gaps G-2 and G-8, owned by T-011 and the owner respectively

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-06 | → proposed | Created from the owner's direction to open the project with corpus research. |
| 2026-08-06 | → in_progress | Started. Approach set: full-fidelity gitignored `.kb/` plus scrubbed repo analysis, mechanical extraction before interpretation, and a gaps register. |
| 2026-08-06 | → done | KB built and both R1 deliverables written. 12 decks measured, 60 candidate rules, 12 gaps, 6 contradictions. Two acceptance criteria unmet because the corpus is silent; both recorded as gaps. |
| 2026-08-06 | (no change) | Second sweep at the owner's direction: six more written sources plus library/CDN extraction. Rules 60 to 154, five gaps closed, two acceptance criteria moved from unmet to met. |
