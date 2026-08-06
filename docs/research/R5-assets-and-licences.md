# R5 — Offline-safe assets, licences, and what self-containment actually costs

Deliverable of [T-013](../../tasks/T-013-research-offline-safe-assets-and-licences.md), and it
absorbs [T-012](../../tasks/T-012-research-existing-html-deck-skills-and-libraries.md) plan steps
4–6, which asked the same licence-and-size question about frameworks and libraries. Companion to
[R4](R4-prior-art.md).

Every figure below was produced by [`tools/assets/measure.py`](../../tools/assets/measure.py) and
[`tools/assets/build_probe_deck.py`](../../tools/assets/build_probe_deck.py), which run their own
self-test first and refuse to measure if it fails (**L-04**). Reproduce with:

```
python tools/assets/measure.py all
python tools/assets/build_probe_deck.py
```

Sources are the ones a browser really uses — the Google Fonts CSS API for the per-script woff2 a
browser downloads, jsDelivr for the minified build a `<script>` tag resolves to — so these are
production bytes, not repository bytes. Measured 2026-08-06.

---

## Bottom line

**Self-containment is nearly free, and the measurement is not close.** A complete 12-slide deck
with three embedded typefaces, twelve icons, a motion library and four hand-written SVG diagrams
is **191.8 KB in one file with zero external references**. It renders correctly from `file://`
with the network off; all three embedded faces report `loaded`.

That number reframes the question the owner asked. The delivery mode was proposed as
CDN-by-default with embedding on request, on the reasonable assumption that embedding is
expensive. It is not. **192 KB is smaller than one mid-sized photograph**, and it is the whole
deck, not the overhead.

Three findings follow from that, and one of them contradicts the brief:

**1. Fonts are the cheapest part of the problem, not the dear part.** Every deck in the corpus
failed self-containment mostly on web fonts, which framed fonts as the hard case. The dearest
family measured — Newsreader — costs 75.6 KB inlined. A three-face identity costs **97 KB**. The
corpus decks were not defeated by size; they were defeated by nobody trying.

**2. The heavy things are libraries, and only one is genuinely heavy.** Mermaid's runtime is
**3.48 MB** — on its own, eighteen times the entire probe deck, and more than three times every
other library measured *combined*. That single figure decides the diagram strategy (§5).

**3. The recommendation is the opposite of the proposed default.** Embed by default; make CDN the
opt-in. §4 sets out why, and what the configuration parameter should actually be.

---

## 1. Typefaces

All fifteen are **SIL Open Font License 1.1**, which permits redistribution and embedding provided
the licence text travels with the font. Verified per family from the Google Fonts source, not from
a summary page.

Measured as the **latin-subset woff2** — the file a browser downloads, not the full family. The
`b64` column is what it costs inside the HTML: a `data:` URI pays a base64 surcharge of exactly
one third, and there is no way around it for a binary in a single file.

| Family | raw KB | inlined KB | axes | Role |
| :--- | ---: | ---: | :--- | :--- |
| IBM Plex Mono | 14.4 | 19.2 | static | mono |
| Figtree | 19.7 | 26.2 | variable | text sans, geometric |
| **Instrument Serif** | 20.5 | **27.4** | static | display serif |
| **Space Grotesk** | 21.8 | **29.0** | variable | display grotesque |
| Public Sans | 26.2 | 34.9 | variable | text sans, plain by design |
| Source Sans 3 | 28.1 | 37.4 | variable | text sans, wide coverage |
| Libre Franklin | 28.6 | 38.1 | variable | text sans |
| Instrument Sans | 29.4 | 39.2 | variable | text sans |
| **JetBrains Mono** | 30.7 | **40.9** | variable | mono |
| Fraunces | 35.8 | 47.7 | variable | display serif, characterful |
| Bricolage Grotesque | 40.4 | 53.8 | variable | display grotesque |
| IBM Plex Sans | 44.6 | 59.5 | static | text sans |
| Inter | 47.1 | 62.8 | variable | text sans, the default everywhere |
| Source Serif 4 | 49.6 | 66.2 | variable | serif |
| Newsreader | 56.7 | 75.6 | variable | serif, optical sizes |

**Three things this table settles.**

- **A variable font is one file for the whole weight range.** Space Grotesk covers 400–700 in
  29 KB inlined. IBM Plex Sans, static, needs one file per weight and costs 59.5 KB for two.
  Prefer variable, and the size argument for a single-weight design disappears.
- **Inter is among the most expensive and the least distinctive.** It is 62.8 KB — more than twice
  Instrument Serif — and it is the face every generated deck already uses. It buys ubiquity, which
  is the one thing this project is explicitly trying not to have. This matters because R4 found
  the corpus's named faces were rows of the source skill's pairing table, not the owner's choice;
  **T-014 has to decide what carries the identity, and "Inter" is the answer that costs most and
  says least**.
- **Subsetting further is possible but not needed.** These are Google's latin subsets (~200
  glyphs). A deck-specific subset would cut them again, at the price of a font-tooling dependency
  that violates L-07. At 97 KB for three faces, that trade is not worth making yet.

**Recommended default set** — measured in the probe deck at **97.3 KB** total:
Instrument Serif (display) · Space Grotesk (text) · JetBrains Mono (figures and code). Not
because they are cheapest, but because they are cheap *and* the pairing does not read as a
default. Fallback if a lighter identity is wanted: Figtree + Instrument Serif at 53.6 KB.

**Licence obligation.** OFL 1.1 requires the licence to accompany the font. For an embedded
`data:` URI that means an HTML comment carrying the copyright line and licence reference next to
the `@font-face` block. This is cheap and non-negotiable; the build must emit it, not the author
remember it. CLAUDE.md already requires recording the licence next to each embedded font.

## 2. Icons

| Set | one icon, B | minified B | ×24, KB | Licence | Redistribution |
| :--- | ---: | ---: | ---: | :--- | :--- |
| Phosphor | 245 | 245 | 5.7 | MIT | clean |
| Heroicons | 254 | 249 | 5.8 | MIT | clean |
| Bootstrap Icons | 311 | 307 | 7.2 | MIT | clean |
| Feather | 314 | 314 | 7.4 | MIT | clean |
| **Lucide** | 343 | 314 | 7.4 | ISC (+ MIT for Feather-derived) | clean |
| Tabler | 412 | 379 | 8.9 | MIT | clean |

**Icons are a rounding error.** Twenty-four of them cost 5.7–8.9 KB. Any argument that trades
design quality for icon bytes is arguing about 0.3% of the file.

**Two licences needed reading rather than trusting.** GitHub's classifier reports both as
"Other":

- **Lucide** is ISC, with the ~110 Feather-derived icons additionally under MIT. Both permissive;
  redistribution and embedding are unambiguous.
- **RemixIcon changed licence in January 2026** — from Apache-2.0 to a custom "Remix Icon License
  v1.0". Most third-party references still say Apache. The new terms permit inclusion in a larger
  work but prohibit distributing the icons "as a standalone product" or as "an independent icon
  pack… for sale". Using them inside a generated deck is permitted; **vendoring the whole set into
  a published plugin repository sits close enough to the prohibited case to not be worth the
  argument.** Excluded on that basis, not on quality.

**Recommendation: Lucide.** ISC, 314 B minified, a large and coherent set, and its stroke-based
geometry themes cleanly. Phosphor is the pick if a lighter visual weight is wanted — it is also
the smallest.

**Inline `<svg>`, never a `data:` URI.** Two reasons, and the second is the real one: there is no
base64 surcharge, and an inlined glyph inherits `currentColor`, so one icon themes with the deck
instead of being a picture of an icon in a fixed colour. Verified in the probe deck — the accent
colour reaches the icons through CSS alone.

## 3. Libraries — frameworks, motion, 3D

Minified production build, the file a CDN tag resolves to. JavaScript inlines as text, so **raw KB
is what it adds to the deck**; the gzip column matters only if the deck is ever served rather than
opened from disk.

| Library | raw KB | gzip KB | Licence | Verdict |
| :--- | ---: | ---: | :--- | :--- |
| GSAP 3 | 71.2 | 27.6 | **no-charge, not OSI** | usable, but see below |
| **anime.js 4** | 82.0 | 28.4 | MIT | **vendor — recommended** |
| reveal.js 5 | 109.5 | 28.3 | MIT | borrow ideas, do not vendor |
| Motion 12 | 136.6 | 45.4 | MIT | viable alternative to anime.js |
| impress.js 1 | 157.3 | 36.2 | MIT | avoid |
| Chart.js 4 | 203.6 | 68.9 | MIT | avoid — SVG is enough (§5) |
| d3 7 | 273.2 | 90.3 | ISC | avoid whole; borrow scale maths |
| three.js | 331.0 | 76.9 | MIT | opt-in only |
| **mermaid 11** | **3482.5** | 948.8 | MIT | **never ship the runtime** |

**GSAP needs a paragraph, because "free" is not "open source".** Since April 2025 (Webflow's
acquisition of GreenSock) GSAP is free for commercial use including the former members-only
plugins. But the repository carries **no LICENSE file** — GitHub's API returns no licence at all —
and the terms live on a web page as a "Standard 'no charge' license", which is what the npm
`license` field points to rather than an SPDX identifier. The Prohibited Uses clause targets
"tools that allow users to build visual animations without code" that compete with Webflow, and
the FAQ states plainly that AI-generated code is not a prohibited use. So htmldeck generating GSAP
code is permitted. **The problem is not permission, it is the absence of a redistribution grant**:
vendoring a third party's minified file into a published GitHub repository wants an explicit
licence, and there isn't one. anime.js is MIT, 11 KB larger, and raises none of this. Take the
MIT one.

**Deck frameworks: borrow, do not vendor — and the measurement says why.** The probe deck's entire
navigation, stage scaling, keyboard and click handling, and slide transitions came to **9.1 KB
including all four diagrams, the CSS and the markup**. reveal.js alone is 109.5 KB, and it brings
a plugin architecture, a DOM contract and a theming system that would have to be fought rather
than used. Marp and Spectacle were checked and are out of scope by construction: Marp's core is a
build-time Markdown renderer and Spectacle is a React component library — both require a build
step, which T-012's scope excludes. The framework question is settled: **htmldeck writes its own
~9 KB deck shell.**

**Motion: anime.js 4, vendored, MIT.** 82 KB is 43% of the probe deck, which is the single largest
line in its budget — worth stating plainly. It is justified only if the deck uses orchestrated
motion; for staggered entrances below roughly ten elements, CSS `animation-delay` is sufficient
and costs nothing. R4 recorded that the source deck skill says exactly this. **So motion should be
a build-time decision, not a constant**: no motion library unless the deck asks for one.

**three.js: opt-in, never default.** 331 KB, MIT. It is 1.7× the whole probe deck, so it belongs
behind an explicit request on size alone.

> **Correction, same day: this section originally said three.js "initialises fine from `file://`".
> That was not tested, and it should not have been written.** The probe deck exercised fonts,
> icons, anime.js and inline SVG from `file://` — never three.js, WebGL or module scripts. Worse,
> the file measured above is `three.module.min.js`, an **ES module**, and module loading is one of
> the specific things a restricted origin is expected to break.
>
> An attempt to settle it in the preview pane failed for a reason worth recording: the pane
> reports `location.origin` as `"file://"` and allows `fetch()` of a local file, both of which are
> inconsistent with a genuinely restricted origin. **It is not a faithful `file://` environment**,
> so nothing it reports about this can be trusted — the third time in this session that pane has
> given a confident wrong answer (**L-06**).
>
> **This is T-017's question, and T-017's method is the only one that answers it: double-click on
> a clean profile and record what happens.** The 331 KB figure and the MIT licence stand; the
> runtime claim is withdrawn until tested.

## 4. The delivery-mode question — the recommendation you asked for

The owner's answer to T-013's open question set the default as **CDN references, with embedding
available on request**, and asked for a measured recommendation on how a user of the plugin should
face this choice. This section is that recommendation, and it disagrees.

**This contradicts CLAUDE.md rule 1** ("Self-contained or it doesn't ship... renders correctly
with the network disabled") and it reverses the position R4 identified as the owner's sharpest
departure from the source deck skill — J1, where *the skill means one file and the owner means no
network*. CLAUDE.md requires findings that contradict the brief to be raised as candidate changes
of direction rather than worked around, so it is raised here rather than implemented quietly.

**Recommendation: embed by default; make CDN the opt-in; drop the local-files mode entirely.**

> **Accepted by the owner, 2026-08-06.** This is now the project's decision, recorded under
> *Delivery mode* in [BRIEF.md](../BRIEF.md) "Decisions taken". CLAUDE.md rule 1 stands unchanged
> and `linked` is a development mode only. The rest of this section is the argument that was made,
> kept as the rationale behind the decision.

The case, in the order the evidence supports it:

1. **Cost is not a reason.** The premise for defaulting to CDN is that embedding is expensive.
   Measured, a full deck is 192 KB. There is no budget being protected.

   **A second, independent measurement agrees.** R1 found that three corpus decks are already
   fully self-contained, and one of them carries **seven** faces as base64 `@font-face`, zero
   external references and 22 inline SVGs, at **282 KB** — recorded in
   [BRIEF.md](../BRIEF.md) as *"the font problem is solved precedent, not an open problem"*. Two
   measurements taken from different artefacts by different methods land in the same place: a
   lavish self-contained deck is under 300 KB. Nothing about the size argument survives this.
2. **The default is the one that gets shipped.** Every deck in the source corpus failed offline
   rendering with 2–7 external references. Nobody chose that; it was the default. A CDN default
   reproduces the exact failure the project exists to fix, and it will be discovered by a
   recipient, in a meeting, offline — which is the one moment it cannot be fixed.
3. **CDN failures are silent and delayed.** A missing font does not error; it silently falls back
   and the deck's identity — the thing this plugin is for — is what disappears. Link rot, a
   corporate proxy, an air-gapped laptop and a plane all produce the same result months after the
   author last looked.
4. **"Local file references" should not exist.** A deck plus a folder of assets is the format that
   breaks when emailed, and it fails CLAUDE.md rule 2 — the recipient double-clicks *the file*.
   Two delivery modes are enough.

**What the configuration parameter should be.** Not "CDN or embedded" — that asks the author to
reason about the recipient's network, which they cannot know. Make it a statement about the
audience:

| Setting | Behaviour | When |
| :--- | :--- | :--- |
| `portable` (**default**) | Everything inlined. Zero external references. ~190 KB typical. | Anything sent to anyone. |
| `linked` | Fonts and libraries from CDN. ~15 KB. | Authoring loop only — fast rebuilds while iterating. |

`linked` earns its place as a **development** mode, not a delivery mode, and the build check should
say which one produced the file. A deck built `linked` should carry a visible warning in the build
report, and the critique mode should flag it as a defect — because for a deck that is about to be
sent, it is one.

**If the owner still wants CDN as the shipped default**, the honest way to do it is to keep rule 1
as the definition of done and make `linked` an explicit per-deck override — so the failure mode is
a choice someone made, not a default someone inherited.

## 5. Diagrams and illustration

**Mermaid's 3.48 MB runtime settles this.** Shipping it is out of the question — it is 18× the
entire probe deck. But the ban is on the *runtime*, not the tool:

- **Mermaid as an authoring convenience, pre-rendered to SVG at build time** — the author writes
  Mermaid, the build emits static SVG, the deck ships no Mermaid. This keeps the ergonomics and
  pays none of the cost. It needs a render step at build time (Node), so it is an optional
  enhancement under R4 §7's capability-first contract, never a requirement.
- **Hand-written SVG** — what the probe deck used. Four diagrams, part of the 9.1 KB that covered
  markup, CSS and script together. It themes through CSS variables, scales without blurring, and
  diffs as text.

**Verified in the probe deck, and worth recording:** hand-written SVG at fixed viewBox coordinates
renders correctly inside a scaled stage, and its text inherits the deck's embedded font and accent
colour through CSS. The measured box centres matched the measured text centres exactly.

**A methodology warning that cost time here.** The preview pane renders `file://` pages as static
snapshots, and the snapshot renderer mis-draws SVG `text-anchor`. It produced a convincing picture
of a broken diagram that was not broken — the DOM geometry was correct to the pixel. This is
**L-06** again, in its third costume: *check a visual verdict against a second view before
recording it as a defect.*

**Charts: no library.** The probe deck's line chart is hand-written SVG inside the same 9.1 KB.
Chart.js is 203.6 KB and d3 is 273.2 KB, and neither is needed for the chart types a deck actually
uses — a line, some bars, a share. Borrow d3's scale arithmetic as a dozen lines of code; do not
vendor d3. This is an input to T-006.

**Illustration: geometric SVG, generated from the theme tokens.** No clip art, no raster (already
banned), no illustration library exists that is licence-clean *and* does not look like stock. The
probe deck's rules, accent bar and diagram strokes all draw from the same `--accent`/`--line`
tokens, which is what keeps a deck looking authored rather than assembled.

## 6. Plugin packaging — T-012 step 6

Surveyed from the first-party `plugin-dev` plugin installed in this environment, which is a worked
example rather than documentation about one. What htmldeck's repository must contain:

- **`.claude-plugin/plugin.json`** is required and must be in that directory. Component
  directories (`commands/`, `agents/`, `skills/`, `hooks/`) go at the **plugin root**, never
  inside `.claude-plugin/`. Only `name` is mandatory; kebab-case, matching
  `^[a-z][a-z0-9]*(-[a-z0-9]+)*$`.
- **Auto-discovery does the work.** `skills/<name>/SKILL.md` is found without registration; custom
  paths in the manifest *supplement* the defaults rather than replacing them, so the lean manifest
  is the right one.
- **`${CLAUDE_PLUGIN_ROOT}`** for every intra-plugin path. Never absolute paths, never `~`, never
  working-directory-relative. This is the packaging equivalent of L-09.
- **For distribution**: `version` (semver), `description`, `author`, `repository`, `license`
  (SPDX), `keywords`, and a LICENSE file at the plugin root.
- **Skill layout matches what R4 §1 found the hard way**: `SKILL.md` routes, and the substance
  belongs in `references/` loaded on demand. That is L-12 as a packaging convention, and it is
  what the design-system reference should be.

This feeds T-015 and T-008 and closes T-012's last unmet criterion.

## 7. What was verified, and how

The probe deck is a **measurement vehicle, not a product**. It is written to `.assets-cache/`
(gitignored) and never committed; the repository keeps the script and the numbers. Topic is
neutral, per CLAUDE.md's publishing constraints.

**Probe deck budget** — 12 slides, four SVG diagrams, embedded fonts and icons:

| Component | KB | Share |
| :--- | ---: | ---: |
| anime.js 4 (motion) | 82.0 | 42.7% |
| JetBrains Mono | 40.9 | 21.3% |
| Space Grotesk | 29.0 | 15.1% |
| Instrument Serif | 27.4 | 14.3% |
| Markup, CSS, four diagrams, deck script | 9.1 | 4.7% |
| Lucide icons ×12 | 3.4 | 1.8% |
| **Total, one self-contained file** | **191.8** | |

**Offline verification.** Opened from `file://` with no server:

- **0 external references** — every `src`, `href` and `url()` is `data:`, `#`, or absent. The only
  `http` strings in the file are the SVG namespace URI and a comment inside anime.js; neither is a
  fetch.
- `document.fonts.size === 3` and `document.fonts.status === "loaded"` — all three embedded faces
  resolved from the `data:` URIs.
- All 12 slides render; diagrams, chart, icons, two-column layouts and the stage scaling all
  behave. Looked at, not just validated (**L-01**).

**Honest defects seen in the probe** — design issues in the probe itself, not asset findings, but
recorded because L-01 means reporting what was actually seen: slides run bottom-heavy with dead
space at the lower right, the chart's x-axis labels collide with the axis line, and the cycle
diagram's return-path label sits on its own connector. All three are the layout-and-pacing class
of problem that only appears at real size, which is the whole reason L-02 asks for twelve slides.

**Not measured:** deck-specific font subsetting below Google's latin subset (needs a font-tooling
dependency, and at 97 KB for three faces the incentive is absent); `three.js` inside a real deck;
and Mermaid's build-time render path, which needs Node and belongs with the enhancement work.

**What this note is *not* evidence about, stated plainly.** The offline verification in this
section covers exactly what the probe deck contains: `data:` fonts, inline SVG, inline icons, and
one classic (non-module) script. It says **nothing** about ES modules, WebGL, workers, `fetch`,
`localStorage`, canvas tainting or Web Audio from a restricted origin. Those are
[T-017](../../tasks/T-017-define-the-portability-contract.md)'s matrix, they must be tested by
double-click rather than in any preview tool (see §3's correction), and **T-017 could still narrow
what this note treats as available.**

This is an ordering inversion worth naming: T-013's own scope says the `file://` envelope "comes
from T-017", and T-017's says it "feeds T-013" — but T-013 ran first. Where the two meet, T-013
measured **size and licence**, which are facts that do not depend on T-017, and **assumed**
runtime availability, which does. The assumption is now marked everywhere it was made.

## 8. What this hands to other tasks

| Task | What R5 gives it |
| :--- | :--- |
| **T-001** font strategy | Embedded subsets win outright: 27–76 KB per face, OFL-clean, verified offline. The recommendation and its fallback are in §1. Blocker cleared. |
| **T-006** chart strategy | No chart library. Hand-written SVG; borrow scale maths from d3 without vendoring it. §5. |
| **T-014** design-system synthesis | The typography that carries the identity — and the argument that Inter is the expensive, least distinctive answer. Feeds directly into the R4 typography contradiction. |
| **T-016** motion | anime.js 4, MIT, 82 KB, opt-in rather than constant; CSS staggering below ~10 elements. GSAP rejected on redistribution, not capability. §3. |
| **T-015 / T-008** packaging | §6. |

**Settled 2026-08-06:** §4's recommendation reversed the stated CDN-by-default direction and the
owner accepted it. T-014 can assume every shipped deck is self-contained. Recorded under *Delivery
mode* in [BRIEF.md](../BRIEF.md) "Decisions taken".
