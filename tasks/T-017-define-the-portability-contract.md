---
id: T-017
title: Define the portability contract — what "opens anywhere and works" actually permits
type: research
status: done
phase: review
parent: null
blocked_by: []
related: [T-002, T-005, T-013, T-016]
work_package: WP1
shipped_in: 0.1.0
owner: maintainer
created: 2026-08-06
updated: 2026-08-12
deliverables: [docs/research/R6-portability-contract.md, tools/portability/build_probes.py, tools/portability/run_probes.py]
---

# T-017 — Define the portability contract — what "opens anywhere and works" actually permits

## 1. Specify

**Outcome**
A tested statement of exactly which web platform features a single self-contained HTML file can use
when it is **double-clicked** rather than served — and therefore which interaction, animation and
3D techniques the build mode is allowed to emit.

**Why this one**
Portability is now the binding constraint, and it is not the same thing as restraint. The hazard is
specific: **`file://` is a restricted origin.** ES modules, `fetch`, XHR, some worker
registrations and several WebGL and `<canvas>` texture paths fail on a double-clicked file while
working perfectly over HTTP — which means they also work perfectly in every local preview, and the
breakage only appears on the recipient's machine. "Rich JavaScript" and "no installation" collide
exactly here. Every other task in WP3 builds on the answer, so it belongs in research, before them.

**Scope**
- In: an empirically tested feature matrix for `file://` — module scripts vs classic scripts,
  inline vs external, `fetch` and XHR, data and blob URIs, workers, WebGL context creation and
  texture sources, Web Audio, fullscreen, clipboard, `localStorage`, CSS 3D and filters,
  `<canvas>` tainting rules.
- In: naming the **target browser** and version floor, and what "no glitch" means as a testable
  statement.
- In: how far mobile degrades, given it is explicitly secondary — degrade gracefully or not care.
- In: the vendoring question — inlining a 3D or animation library into the file, and the size cost
  measured rather than guessed. Feeds T-013.
- In: the optional printable mode — what it costs to support, given it is no longer a gate.
- Out: choosing the libraries. This says what is *possible*; T-013 and T-016 choose.

**Method**
Test, do not read. Documentation and memory both describe the HTTP behaviour of these features;
the `file://` behaviour differs per browser and changes between versions. Build a probe deck, open
it by double-click on a clean profile, and record what actually happens.

**Acceptance criteria**
- [ ] Feature matrix produced from **actual double-click testing**, not documentation, with browser
      and version recorded against every row
- [ ] Target browser and version floor named, with the reason
- [ ] "Glitch-free" defined as something a check can test — see T-005
- [ ] Every failure mode paired with the workaround that keeps the feature usable, or an explicit
      "do not use"
- [ ] Verified with the network disabled, on a profile with no extensions
- [ ] Mobile degradation position stated, not left implicit
- [ ] The probe deck kept as the self-test, per the brief's "verify the checker on a known case"

**Decided 2026-08-06 — recent Chrome/Edge.** One engine, and the one to test against. Firefox and
Safari degrade gracefully but do not set the bar, and mobile is secondary. Probe the others only
far enough to know what breaks, not to support them.

**Open questions**
- ~~Is a single-file deck still the requirement if it costs a large inlined 3D library, or is a
  folder-plus-file acceptable for the heaviest decks?~~ **Answered 2026-08-06 by the delivery-mode
  ruling** (BRIEF.md *Decisions taken*): **no folder-plus-file mode.** Two modes only — `portable`
  (everything inlined, the only shipping mode) and `linked` (CDN, authoring loop only). A deck plus
  an asset folder is the format that breaks when emailed, and it fails the double-click rule. So
  if a 3D library is too heavy to inline, the answer is not to ship it, not to unbundle the deck.
- ~~What is the version floor? "Recent" needs a number before a check can test it.~~
  **Answered 2026-08-06, and the answer is that it should not be a number** — see
  [R6](../docs/research/R6-portability-contract.md) §7. Only Chrome/Edge 151 were tested, so
  naming an older floor would be reading rather than testing, which is the one thing this task's
  method forbids. Instead the deck ships a **capability preflight** and the floor is whatever
  passes it. That is also the better contract on its own merits: a recipient cannot act on a
  version number, but can act on "this browser has no container queries".

**A tooling constraint that will otherwise cost this task a session** — recorded 2026-08-06.
**The in-app preview pane cannot answer this task's question and will appear to.** Loaded with a
`file://` URL it allows `fetch()` of a local file, which a genuinely restricted origin refuses. It
also renders `file://` pages as static snapshots that mis-draw SVG `text-anchor`. It produced three
confident wrong answers in the session that closed T-013, one of which reached a research note
before being caught (R5 §3's withdrawn three.js claim).

> **Amended 2026-08-06, by this task's own measurements.** This paragraph also claimed the pane
> reporting `location.origin` as `"file://"` was inconsistent with a restricted origin. **Real
> Chrome 151 reports exactly the same value**, so that half was wrong and is removed; the `fetch()`
> half is the real discriminator and the prohibition below is unchanged. Detail in §3, lesson in
> **L-15**.

The Method above already says "double-click on a clean profile". Read it as a prohibition on every
in-tool shortcut, not just on reading documentation — **the shortcut here is not merely
unreliable, it fails in the optimistic direction**, reporting capabilities as available that a
real restricted origin denies. That is the failure mode that ships a broken deck.

## 2. Plan

| # | Step | Output | State |
| :-- | :--- | :--- | :--- |
| 1 | Build the probe pages covering every feature in scope | `tools/portability/build_probes.py` | done |
| 2 | Build the runner: clean profile, network black-holed, and a literal shell double-click | `tools/portability/run_probes.py` | done |
| 3 | Run the matrix, Chrome, offline, clean profile | 90-row result set | done |
| 4 | Run the four gesture-gated rows (fullscreen, clipboard, audio resume, download) | 4 rows | done — all four pass |
| 5 | Run the same matrix on Edge, and via a literal double-click, and reconcile | cross-check | done — zero disagreements |
| 6 | Run the 3D probe: three.js inlined, imported as a blob module, rendering | 3D verdict + size | done — renders, with one condition |
| 7 | Name the version floor and define "glitch-free" testably | contract sections | done — R6 §7, §8 |
| 8 | Write the contract | `docs/research/R6-portability-contract.md` | done |

Steps 4–6 were blocked on the environment in the previous session, not on the work; command
execution returned and they were run unchanged in method. **Three of the four things that failed
when they were finally run were faults in this task's own harness, not in `file://`** — recorded
below, and generalised as **L-17** and **L-18**.

## 3. Implement

**Decisions & assumptions**

- **Results come back three ways, not one — 2026-08-06.** A downloaded JSON file (exact), a
  rotating window title (compact), and an on-screen table (so it can be looked at, L-01). The
  title channel is not redundancy for its own sake: *a probe that can only report by downloading
  cannot report that downloading is blocked*, and downloads are one of the things under test. It
  earned its place immediately — the second download in a run makes Chrome raise a permission
  dialog, so the gesture rows had to move off the download channel entirely.
- **"Network off" is per-launch, not machine-wide — 2026-08-06.** Implemented as
  `--host-resolver-rules=MAP * ~NOTFOUND` plus `--disable-background-networking`. Disabling the
  machine's network adapter is a system-wide change to someone else's computer and is not needed
  to prove the point: nothing may resolve, for this browser, for this run. Zero external
  references is additionally provable statically, as R5 did.
- **The user activation is a human click, not injected input — 2026-08-06.** Fullscreen, clipboard
  and audio-resume are gated on a real activation, and a synthetic DOM event does not carry one —
  it would report every gated row as blocked, writing a false negative into the contract as if the
  origin had refused. The first implementation synthesised the activation with OS-level keystroke
  injection and foreground-window stealing. It worked, and it was withdrawn: it is
  indistinguishable from input hijacking, and this repository publishes. One human click costs
  seconds and asks nothing of whoever clones it.
- **Two rows initially failed on my own fixtures, not on the origin — 2026-08-06.** The `<audio>`
  row used a 2 ms WAV that no element ever fires `loadedmetadata` for, and a video row used a
  36-byte fragment of an mp4 header that is not a decodable video. Both read as "the origin
  refused this" and both were wrong. Fixed (a real half-second WAV) and dropped (the video row)
  respectively. **L-04 in its exact shape:** the check was believed because it printed a verdict.
- **`document.fonts.load()` resolving is not proof a face loaded.** It reports the faces that
  *matched the query*, whatever became of their fetches. The row now asserts
  `FontFace.status === 'loaded'`. A font row that says PASS while the deck renders in Arial is the
  optimistic failure this whole task exists to prevent.

**Decisions & assumptions — added 2026-08-06, second session**

- **All four gesture-gated features work from `file://`. The failures were mine.** Fullscreen,
  clipboard write, audio-context resume and blob download all pass, on Chrome *and* Edge. The
  first run reported three of them as refused because all four were chained off one click, and a
  transient activation is consumed by the first gated call that reaches it; the fourth then failed
  too, because the very first click on a newly opened window is spent focusing it. Both faults
  produce `NotAllowedError` / `TypeError: Permissions check failed` — **the exact vocabulary a
  genuine origin refusal uses**, which is why neither was visible in the result. Fixed by one
  click per row plus an unmeasured arming click. Generalised as **L-17**; this is the failure mode
  the task's own *Specify* section warns about, arriving from the harness instead of the tool.
- **A stale probe window answered for a fresh run.** The literal-double-click run harvested a
  complete, correctly-reassembled payload containing *gesture rows the page had not yet run* — the
  window title channel is global to the desktop and an earlier run's window was still open. The
  runner now snapshots existing probe windows by handle before launching and ignores them.
  Generalised as **L-18**. Related to L-16 but distinct: L-16 is about the channel colliding with
  the *subject*, this is about it colliding with *another run*.
- **The title channel now terminates its payload with `¬`.** Suffix-stripping a known list of
  browser titles silently glued `" - Personal"` onto the last chunk of every Edge run: Edge puts
  the *profile name* in the title, and a profile can be called anything. A terminator the page
  controls does not have to guess what the browser appended.
- **Screenshots are scoped to the probe window, not the screen.** The first capture took the whole
  virtual desktop and swept up unrelated windows. The probe window is the only part that is
  evidence; capturing the rest is someone's private screen. Capture only — nothing is clicked or
  typed, per the ruling above.
- **`three.js` costs 703 KB inlined, not 331 KB.** The measured file was `three.module.min.js`,
  which is a re-export shim; the library itself is in `three.core.min.js` (372.2 KB), imported by
  a relative specifier. R5's table recorded only the shim. Corrected there, and the correction
  strengthens rather than changes that note's "opt-in, never default" ruling.

**Outputs produced**
- `tools/portability/build_probes.py` — builds the probes; self-tests the chunker and the PNG
  generator before it will build anything (L-04).
- `tools/portability/run_probes.py` — clean-profile and literal-double-click runners.
- `.assets-cache/portability/results/chrome-offline/probe-results.json` — 91 rows, Chrome
  151.0.7922.71, clean profile, no extensions, DNS black-holed. Gitignored by design; the
  repository keeps the script and the numbers, never the artefacts.

  **One row of that JSON must not be copied into R6 as it stands.** `webgl.unmasked-renderer`
  records the actual GPU model of the machine it ran on. It is a useful row — WebGL behaviour is
  driver-dependent, so the contract should say *a* renderer was identified and that the results are
  from hardware-accelerated ANGLE/D3D11 — but naming the card is machine data, which CLAUDE.md's
  publishing constraints forbid. Generalise it when the note is written.

**What the rows say so far** — Chrome 151.0.7922.71, `file://`, clean profile, DNS black-holed.
**91 automatic rows** (70 pass, 14 fail, 7 info) **plus 4 gesture rows, all passing** — 95 in
total. Interim; R6 is where these become the contract.

**Two cross-checks, and neither moved a row.**

- **Edge 151.0.4129.59 agrees with Chrome on all 91 rows** — same codes, and the informational
  details match too. One engine, as decided; the second browser confirms rather than extends.
- **The literal double-click agrees with the clean-profile run on all 91 rows.** Opened through
  the Windows file association into the real default browser — real profile, extensions loaded,
  network up — against a dedicated empty profile with DNS black-holed. **Zero disagreements.**
  This is the check that matters most: it says the arranged environment did not flatter the
  results, and the matrix describes what a recipient gets.

**Step 6 — three.js from `file://`: yes, with one condition that belongs in the contract.**
Measured on Chrome 151, offline, clean profile; the render was looked at, not just counted (L-01).

| Row | Result |
| :--- | :--- |
| both halves inlined | 720,032 chars of source in the page |
| unmodified package + import map | **FAIL** — `Failed to resolve module specifier "./three.core.min.js"` |
| specifier rewritten to the core's blob URL | **PASS** — 422 exports |
| WebGL renderer | PASS — r180 |
| rendered pixels | PASS — centre `rgba=165,132,71` |

The condition is the second row. **A relative specifier cannot be resolved from a `blob:` module
at all** — the base scheme is not hierarchical, so resolution fails *before* an import map is
consulted, and the map never gets a chance to redirect it. So an ESM library that ships as more
than one file cannot be inlined verbatim; its internal specifiers must be rewritten to blob URLs
at build time. For three.js that is one string replacement, and then it renders.

This also disposes of the shape of the question R5 left open. It is not "is three.js allowed" —
it is allowed. It is "what does the build step have to do first", and the answer is small but
non-optional.

*The line is not where the brief assumed.* It does not fall between "inline" and "external" — it
falls between **fetch-like access** and **element-like access**, and several things the brief
listed as expected casualties are not casualties at all.

| Works | Refused |
| :--- | :--- |
| classic `<script src="./x.js">` | `<script type="module" src>` and `import('./x.mjs')` |
| `import()` of a **blob:** or **data:** URL | `fetch`/XHR of *any* local file, including its own file |
| workers from blob: and data: (incl. module workers from data:) | workers from a sibling file (SecurityError) |
| `localStorage`, `sessionStorage`, IndexedDB, CacheStorage | cookies, service worker registration |
| WebGL1, WebGL2, WebGPU adapter, shader compile, `readPixels` | canvas/WebGL textures from a **sibling file** — taints |
| canvas clean from **data:** and **blob:** images | scriptable access to any `<iframe>` except `srcdoc` |
| `@font-face` from data: **and from a sibling file** | — |
| stylesheets, images, SVG and audio from data: **and sibling files** | — |

Four consequences worth stating before the note is written:

1. **ES modules are usable, via one specific route.** `<script type="module" src>` and relative
   `import` are dead on `file://`, but `import()` of a blob: URL built from an inlined string
   works. That is the route a single-file deck would have to take for any ESM-only library, and it
   is what the three.js question in step 6 turns on.
2. **`file://` is a secure context** (`isSecureContext === true`), which is why `crypto.subtle`,
   `registerProperty`, view transitions and the rest are all present. Several capabilities assumed
   lost are simply there.
3. **Sibling files load as elements but not as data.** An image, stylesheet, font, script or audio
   file next to the deck loads; the same image taints a canvas, and no local file can be `fetch`ed.
   This does not soften the single-file rule — it explains precisely which half of it bites.
4. **The one hard boundary is reading bytes.** Everything refused above is a variant of "read a
   local file's contents into script". Everything permitted is "let the renderer consume it".

**A correction to this task's own warning, and to L-15 — 2026-08-06.** The paragraph under
*Specify* says the preview pane "reports `location.origin` as `\"file://\"` … neither consistent
with a genuinely restricted origin, where the origin is opaque". **Half of that is wrong, and it is
now measured:** real Chrome 151, on a real double-clicked file, also reports `location.origin` as
`"file://"`. It is what Chrome does; it is not evidence of anything. The *other* half stands and is
the real discriminator — real Chrome refuses `fetch()` of a local file with `TypeError: Failed to
fetch`, and refuses a worker from a sibling file with an error naming the origin as **`'null'`**.
So the origin genuinely is opaque; `location.origin` just does not say so. **L-15's conclusion
survives intact on the `fetch` evidence; one of its two stated proofs does not.** Corrected at its
home in [`docs/LESSONS.md`](../docs/LESSONS.md) and noted in R5 §3.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Feature matrix from actual double-click testing, browser and version on every row | met | 91 automatic + 4 gesture rows, Chrome 151.0.7922.71 and Edge 151.0.4129.59. [R6](../docs/research/R6-portability-contract.md) §2–§3 |
| Target browser and version floor named, with the reason | met, **not as a number** | R6 §7. Only 151 was tested, so naming an older floor would be reading, not testing (L-05). The floor is a capability preflight; the reasons are given |
| "Glitch-free" defined as something a check can test | met | R6 §8 — nine checks, written for T-005 to implement |
| Every failure mode paired with a workaround or an explicit "do not use" | met | R6 §5. No refusal costs the deck a capability |
| Verified with the network disabled, on a profile with no extensions | met | DNS black-holed per launch; **and** cross-checked against a literal double-click into the real default browser with network up — zero disagreements (R6 §4) |
| Mobile degradation position stated, not left implicit | met | R6 §9 — stated as a design position, and explicitly **not measured** |
| The probe deck kept as the self-test | met | both scripts self-test before they will build or measure (L-04) |

**Child fix tasks raised**
- none. Two follow-ups are named in R6 rather than raised as tasks, because both belong to work
  that is not specified yet: the **printing mode** needs its own small task once T-005 exists
  (R6 §9), and the **capability preflight** is an output of WP3's build mode, not of research
  (R6 §7).

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-06 | → proposed | Created after the owner replaced the minimal-JavaScript constraint with a portability constraint, making the `file://` envelope the thing WP3 depends on. |
| 2026-08-06 | → specified | §1 accepted as written. The folder-plus-file open question was already answered by the delivery-mode ruling; the version-floor question stays open and is answered by the work, not before it. |
| 2026-08-06 | → planned | Plan rewritten from 5 steps to 8: the original had no step for *getting results out of* a browser that cannot be scripted from outside, which turned out to be the hard part of the method rather than a detail of it. |
| 2026-08-06 | → in_progress | Probes and runner built and self-testing. Matrix run on Chrome 151, clean profile, DNS black-holed: 90 rows, 70 pass, 14 fail, 6 info. Three of my own rows failed on bad fixtures before they failed honestly — recorded in §3, because a probe that lies optimistically is the exact thing this task exists to catch. |
| 2026-08-06 | (no change) | **Blocked on the environment, not the work.** Python execution stopped being permitted in this session after the runner briefly contained OS-level keystroke injection (since removed in favour of a human click). Steps 4–6 — gesture rows, Edge, literal double-click, and the three.js blob-module test — are built and unrun. |
| 2026-08-06 | → done | All seven acceptance criteria have a verdict; deliverables exist; the probe pages were opened offline and looked at, not merely counted (L-01). The version-floor criterion is met by refusing to invent a number — R6 §7 defines the floor as a capability preflight and says why, since only 151 was tested. |
| 2026-08-06 | → review | Unblocked; steps 4–8 run and R6 written. Three of the four gesture rows and the whole first 3D result were **faults in this task's own harness**, each failing in the vocabulary of a genuine refusal: one activation shared across four gated calls, an arming click spent on a measurement, a stale window answering for a fresh run, and a two-file ESM package inlined as one file. All four fixed and re-measured. Cross-checks added nothing and that is the point — Edge matches Chrome on all 91 rows, and a literal double-click into the real browser matches the clean-profile run on all 91. New lessons **L-17**, **L-18**; corrections to R5's three.js size (331 → 703 KB) and to its withdrawn runtime claim, now settled. |
