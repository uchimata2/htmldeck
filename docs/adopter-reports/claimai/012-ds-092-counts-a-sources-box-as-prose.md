# DS-092 counts the provenance sources box as a paragraph of prose, so a fourth source fails the slide

| Field | Value |
| :--- | :--- |
| **Target** | `htmldeck` — Gábor's own repository, cloned under `C:\Work\AgentPlugins` |
| **Kind** | Defect |
| **Status** | `open` |
| **Found while** | Adding repeated source controls to `D4 — Executive Board Presentation`, on 2026-08-25 |
| **Version seen** | `0.6.0` |

## What happens

DS-092 caps a paragraph at four sentences and a sentence at twenty words. The provenance mark is
authored as a `<p class="provenance">`, so the rule counts the **sources box** as prose:

```
DS-092   sentences over 20 words: 0, paragraphs over 4 sentences: 1 - Measured, not predicted   FAIL
```

That slide had six source items. Each item ends in a full stop — the deck's own house style, and the
style every existing slide uses — so six items read as six sentences and the slide fails.

Nothing about a source list is prose. It is a list of pointers, and the rule it trips is written for
body copy a reader reads in sequence.

## Why it matters more than it looks

The user's request was *repeat the source controls freely; it is very useful to look up the relevant
material*. htmldeck supports that well — one `<template>` serves every slide that cites it, which is
exactly the right design. But DS-092 then puts a hard ceiling of about **three sources plus one
verification line** on any slide, and the ceiling is invisible until it fires.

Two slides had to be trimmed to satisfy it, and one of the trims removed a source pointer that had
no other home on that slide.

## Evidence

```
python tools/deck/check.py <deck>
```

Add a fourth `<span class="sources-item">` to a slide that already has three, each ending in a full
stop. The rule fails on that slide and names it. Remove one item and it passes, with no other change.

## What is missing

The rule should read prose and skip provenance. A source list is not a paragraph, and the deck's own
component contract already distinguishes them by class.

## Proposed fix

Exclude `.provenance` — or, more precisely, `.sources-box` — from the paragraph-length half of
DS-092. The twenty-word sentence cap can stay: a source description that runs past twenty words is a
genuine defect and worth catching.

If some ceiling on source count is wanted, make it its own rule with its own number and its own
message, so a builder reads *this slide cites too many things* rather than *this slide's prose is too
long*.
