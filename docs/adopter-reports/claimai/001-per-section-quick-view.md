# htmldeck — a quick view scoped to a document section

| Field | Value |
| :--- | :--- |
| **Target** | `htmldeck` — Gábor's own repository, cloned under `C:\Work\AgentPlugins` |
| **Kind** | Feature |
| **Status** | `open` |
| **Found while** | Specifying the ClaimAI board deck, on 2026-08-24 — `E15 — Build the Executive Board Presentation with htmldeck` |
| **Version seen** | `0.6.0` |

## What exists today

A quick view hangs off a source item and shows the whole file in a scrollable sheet.

**Evidence.** `docs/COMPONENT-CONTRACT.md` §3 lists `.qv-src` as a `template` whose parent is
`.sources-item`, cardinality `0-1`, authored. `docs/DESIGN-SYSTEM.md` DS-085 names a colophon
carrying the deck's sources as the one thing allowed to follow the closing slide, which is where
that list of source items lives.

## What is missing

No way to open a quick view scoped to the **section** a slide argues from. A slide citing one risk
row, one finding or one clause makes the reader open the whole document and scroll to find it.

The whole-file view is right for the colophon, where the reader is browsing sources. It is wrong on
an argument slide, where the reader is checking one claim.

## Proposed fix

Not settled. The shape the deck wanted was a second, slide-local quick view carrying a named
fragment of a source, with the whole-file view still reachable from the colophon. Whether that is a
new component, an anchor into the existing sheet, or a `data-` attribute selecting a range is the
repository's decision, not this project's.

## What was done instead

The ClaimAI deck keeps whole-file quick views on the colophon and builds any per-section panel by
hand on the slide that needs it. Recorded in `E15 — Build the Executive Board Presentation with
htmldeck` §1, Scope and Decisions.
