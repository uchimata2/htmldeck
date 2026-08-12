---
id: T-103
title: build.md drops DS-105's link clause for a single-source slide, so the mark does not read as provenance
type: fix
status: done
phase: review
shipped_in: unreleased
parent: null
blocked_by: []
related: [T-069, T-070, T-092]
work_package: PH1
owner: the project owner
business_value: high
effort: s
created: 2026-08-12
updated: 2026-08-12
deliverables:
  - skills/htmldeck/references/build.md
  - docs/COMPONENT-CONTRACT.md
  - shell/components.css
  - shell/deck.js
  - examples/sort-window/sort-window.html
  - examples/reference-deck.html
  - tools/deck/static_variants.py
---

# T-103 — build.md drops DS-105's link clause for a single-source slide, so the mark does not read as provenance

## 1. Specify

**Where this came from.** The owner of the adopting project, reviewing the finished deck. He did not
recognise the provenance mark as provenance, and said so in his own words:

> the "subtitle" in the upper right corner is the source. It has no icon (file for local sources,
> link for URLs, …), and it has no link to access it or show it. So I thought it is a subtitle.

**This is not a new request.** It is `N-1` in that project's feedback document — *a source line a
reader can actually use* — which was accepted here and closed as `T-069` and `T-070`. The need was
agreed. What follows is where the implementation stopped.

## What happens

A slide resting on **one** source shows the source's title as bare uppercase text: no icon, no
control, nothing to click. A slide resting on **two** gets an icon, a labelled button and a list that
opens. Nothing tells the reader these are the same thing, so the first kind reads as a subtitle.

## The cause — two documents disagree, and an author follows the narrower one

**DS-105 sets no count condition on the link:**

> A working link where sources are reachable from where the deck is presented; plain text where they
> are not. **Never a dead link.** A slide resting on more than one source puts them behind a control
> that opens a list, one line per source.

The *control* is required at two or more. The **link clause is unconditional** and applies at one.

**`build.md` §2 cites DS-105 and then states the single-source case flatly:**

> The provenance mark is rendered from the slide's `Sources` field, never invented here (DS-105).
> One named source is the source's own title as plain text; more than one is the `.sources` control.

*Plain text*, with no *where they are not reachable* condition carried across. An author following
`build.md` — which is what `build.md` is for — produces a bare-text mark for every single-source
slide, reachable source or not.

## Why 0.2.1 made the gap wider

`T-070` shipped the **quick view**, which is the answer for a source that cannot be linked because it
is a local file. `COMPONENT-CONTRACT.md` §3.2 puts `.sources-open` and `.qv-src` **inside
`.sources-item`**, inside `.sources-box`, inside `.sources`.

So the quick view is reachable only through the `.sources` control, and `build.md` says a
single-source slide does not get one. **A deck whose sources are local files, one per slide, has no
route to the feature built for exactly that case.** §3.2 already notices the seam and says so:
*`.sources-item` is `1+` and DS-105 says two.*

## Why it is filed as a defect

The adopting project keeps defects and product feedback in separate documents on purpose, and this
one is filed here because **the tool does not do what it says**: DS-105 requires a working link where
the source is reachable, and `build.md` instructs plain text unconditionally. The owner classified it
himself, on the ground that the need had already been agreed.

**Scope**
- In: `build.md` carrying DS-105's condition rather than the count — a link where the source is
  reachable, the `.sources` control where it is not and a quick view is available, plain text only
  when neither applies.
- In: **the icon at one source.** What made this unrecognisable was not the missing link but the
  missing mark: a source with no icon and no affordance does not look like a source at any count.
- Out: changing `COMPONENT-CONTRACT.md` §3.2. `.sources-item` is already `1+`, so the structure
  permits one item today.
- Out: re-opening `T-070`. The quick view works; what is missing is the route to it at `n = 1`.

**Acceptance criteria**
- [ ] `build.md` states the single-source case as a condition on reachability, not on count
- [ ] A slide resting on one unreachable source can carry the quick view
- [ ] A one-source provenance mark carries the same glyph the multi-source control does, so it reads
      as provenance without being opened
- [ ] A deck with one local-file source per slide is walked through the ruleset and comes out with a
      mark a reader recognises

**Open questions**
- **Whether the one-source mark gets the full `.sources` control or only the glyph.** The control
  costs an interaction the adopter values not spending; the glyph alone would have prevented the
  misreading. — the project owner

## 2. Plan

**Phase: `PH1`.** `build.md` ships in the plugin and contradicts DS-105, so a deck built by the
published tool does not do what the ruleset says. Derived here; the task arrived with
`work_package: none`.

**The open question is answered: the glyph is the affordance.** Not the full `.sources` control at
one source — that costs the interaction the adopter objected to spending, and *2 sources* is a
disclosure label with nothing to disclose when there is one. So at `n = 1` there is no button and no
panel: the mark is the glyph and the title, on the line, and the title itself is the route.

| # | Step | Where |
| :--- | :--- | :--- |
| 1 | The one-source shape, and the link form DS-105 has never had | `COMPONENT-CONTRACT.md` §3.2 |
| 2 | Style it: inline box, no panel, hit-height matching the button | `shell/components.css` |
| 3 | Stop the script wiring a mark that has no button | `shell/deck.js` |
| 4 | Restate the rule as reachability, not count | `build.md` §2 |
| 5 | Carry it into both example decks and re-sync the shell | `examples/` |
| 6 | Re-anchor the two DS-105 variants and the DS-080 one, which quote the old mark | `static_variants.py` |

**Step 1 is a deviation from the scope**, which put §3.2 out on the ground that `.sources-item` is
already `1+`. That is true of the *rival* answer. The one the owner took needs the mark to exist
without a button, which is three cells and two new rows.

## 3. Implement

**Four rows changed or added in §3.2**, and the shape is otherwise the one that was already there:

| Row | Change | Why |
| :--- | :--- | :--- |
| `.sources-btn` | `1` → `0-1` | A one-source mark has no control |
| `.sources-mark` | sits in `.sources-btn` → `.sources` | The glyph outlives the button. Both shapes still have exactly one, per `.sources` |
| `.sources--one` | new, `on .sources` | Names which shape, so the CSS can select it without `:has()` |
| `.sources-link` | new, `a` in `.sources-item`, `href` | DS-105's link clause had **no form in the contract at all**, which is why T-069 found it had no instance anywhere |

**The box survives at one source, and that is what makes the quick view reachable.**
`.sources-open` and `.qv-src` live inside `.sources-item`, inside the box — so keeping the box and
dropping the button gives a single local source the route it never had. `.sources--one .sources-box`
is static, unpadded and inherits the provenance line's own type; the disclosure box's panel styling
belongs to a panel.

**`deck.js` selects the disclosures, not the marks.** `srcs` now filters `.sources` down to those
carrying a `.sources-btn`. Without it the first one-source mark throws on
`s.querySelector('.sources-btn').addEventListener`, and a deck's whole script dies at load.

**`build.md` §2 no longer reads the route off the count.** Two tables: one mapping the count to the
*mark*, one mapping reachability to what the *title* is — a `.sources-link` where the source is
reachable, a `.sources-open` beside its template where it is a local document, plain text where
neither. DS-105's `file://` clause is restated where an author meets it.

**Both example decks carry it.** `sort-window` had four slides resting on one local source each —
the adopter's case exactly, in our own shipped example — and each is now the glyph plus a
`.sources-open` onto the existing template. The reference deck's six are the glyph plus the title,
its sources being notional. Shell re-synced into all three decks; `shell.py check` clean on both
gated ones.

## 4. Review

| Criterion | Verdict | Evidence |
| :--- | :--- | :--- |
| `build.md` states the single-source case as a condition on reachability, not on count | **met** | §2's second table is keyed on *the source is*, and the first on the count. The old sentence conditioned both on the count |
| A slide resting on one unreachable source can carry the quick view | **met** | `sort-window` slide 2, in the browser: the mark's `.sources-open` opens the quick view with 1024 characters of *Service calendar* |
| A one-source provenance mark carries the same glyph the multi-source control does | **met** | Both are `<svg class="sources-mark"><use href="#i-source"/></svg>`. Rendered shots of slides 2 and 4 put them at the same height and the same right edge |
| A deck with one local-file source per slide comes out with a mark a reader recognises | **met** | Slide 2 rendered offline: document glyph, underlined title, upper right. The complaint it answers was *no icon, no link, so I thought it is a subtitle* |

**Looked at, not inferred, and it found two defects no gate here can see.**

| Found by looking | Fix |
| :--- | :--- |
| The one-source mark sat 12px above the multi-source one, which reads as a jitter when paging | `.sources--one` carries the button's `min-height` and inset |
| The same title rendered **sentence-case in `sort-window` and uppercase in the reference deck** — a UA stylesheet sets `text-transform:none` on form controls, `font:inherit` does not carry it, and only one of the two shapes puts the title in a `<button>` | `.sources-open` re-inherits `text-transform` and `letter-spacing`, the way `.sources-btn` already had to |

Four real-Chrome shots offline across three passes. Both are DS-191's case exactly: every gate was
green at each step.

**One thing this does not do.** `.sources-link` ships with no instance: neither example deck cites a
reachable URL, both resting on local documents. The row is `0-1` and `author`, so that is legal and
no longer a `vocabulary` question (T-105) — but DS-105's link clause is still uninstantiated in this
repository, which is the state T-069 found it in.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-12 | → proposed | Filed from the adopting project's defect report, `Report 5`, written the same day. **The mechanism was corrected while writing it up**: the finding was first recorded there as *DS-105 specifies exactly this*, and reading DS-105 on `master` showed the rule is wider than the behaviour and the narrowing happens in `build.md`. That makes the report a contradiction between two documents rather than a rule someone dislikes. |
| 2026-08-12 | → done | Phase derived as `PH1`. The open question was answered *the glyph alone*, which needed §3.2 to describe a mark with no button — a deviation from the scope's *out: changing §3.2*, recorded in §2. Both example decks carry the new mark and were rendered and looked at offline. |
