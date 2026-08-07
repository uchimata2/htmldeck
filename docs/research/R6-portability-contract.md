# R6 — The portability contract: what a double-clicked HTML file is actually allowed to do

Deliverable of [T-017](../../tasks/T-017-define-the-portability-contract.md). This is the note the
build work in WP3 depends on: it says which web platform features a single self-contained deck may
use when the recipient **double-clicks the file** rather than serving it, and what to do about the
ones it may not.

Every row below was produced by
[`tools/portability/build_probes.py`](../../tools/portability/build_probes.py) and
[`tools/portability/run_probes.py`](../../tools/portability/run_probes.py), which self-test before
they will build or measure anything (**L-04**). Reproduce with:

```
python tools/portability/build_probes.py
python tools/portability/run_probes.py --screenshot
python tools/portability/run_probes.py --browser edge
python tools/portability/run_probes.py --shell
python tools/portability/run_probes.py --page probe-3d.html --screenshot
```

Measured 2026-08-06 on **Chrome 151.0.7922.71** and **Edge 151.0.4129.59**, Windows, from a
dedicated empty profile with no extensions and every DNS lookup black-holed for the launch. The
gesture rows need five real clicks from whoever runs it; the runner asks and waits.

---

## Bottom line

**The restricted origin takes away one thing, and it is narrower than the brief assumed.** You
cannot **read a local file's bytes into script**. That is the whole of it. `fetch`, XHR, a worker
from a sibling file, a canvas texture from a sibling file, a scriptable `<iframe>` — every refusal
in 95 measured rows is a variant of that one sentence.

Everything else the brief listed as an expected casualty is available. `file://` is a **secure
context**, so `crypto.subtle`, `registerProperty`, view transitions, container queries, popover,
WebGL1, WebGL2 and a WebGPU adapter are all present. Fullscreen, clipboard write, audio-context
resume and file download all work. Storage works. Fonts, stylesheets, images, SVG and audio load
from `data:` URIs **and from sibling files**.

**The line does not fall where the brief drew it.** It is not "inline is fine, external is not" —
sibling files load perfectly well as *elements*. It falls between **fetch-like access** and
**element-like access**: the renderer may consume a local file, script may not read it.

Three consequences decide the build mode, and one of them is a correction to this project's own
prior work:

**1. ES modules are usable, by exactly one route, and it needs a build step.** `<script
type="module" src>` and relative `import` are dead. `import()` of a **blob:** or **data:** URL
works. But a library that ships as more than one file cannot be inlined verbatim — a relative
specifier cannot be resolved from a `blob:` base at all, and an import map does not rescue it
because resolution fails before the map is consulted (§6).

**2. Nothing needed a workaround that costs the deck anything.** Every refused capability has a
permitted substitute already in the matrix — `data:`/`blob:` for every fetch-like need, `srcdoc`
for iframes, inline everything. There is no feature in this contract the deck wants and cannot
have.

**3. Three of the four capabilities this note nearly reported as forbidden were forbidden by my
own test harness.** Fullscreen, clipboard and audio-resume were measured against a spent user
activation and reported `NotAllowedError` — the same words a real refusal uses. Given one click
each, all four pass. Recorded as **L-17**, and it is the single most important thing in this note's
provenance: a contract is only as good as the harness that produced it, and this one lied in the
pessimistic direction until it was caught.

---

## 1. Method, and which half of it is load-bearing

**Test, do not read** — the task's own instruction, because `file://` behaviour differs per browser
and per version, and documentation describes the HTTP case. So: build probe pages, open them in a
real browser by launching the executable and by handing the file to the Windows shell, and record
what the page itself reports.

Results come back **three ways**, which is not redundancy for its own sake (**L-16**):

| Channel | What it is for |
| :--- | :--- |
| a downloaded JSON file | exact, machine-readable, complete |
| a rotating window title | survives a blocked download — *a probe that can only report by downloading cannot report that downloading is blocked* |
| an on-screen table | so the result can be **looked at** (**L-01**) |

**What is prohibited, and why it is stated this loudly.** Nothing in this note may be answered from
an in-tool preview pane. Loaded with a `file://` URL such a pane permits `fetch()` of a local file,
which a genuinely restricted origin refuses. It fails **in the optimistic direction** — reporting
capabilities as available that a recipient's browser denies — which is the failure mode that ships
a broken deck instead of a caught bug (**L-15**). Note also what does *not* discriminate: real
Chrome reports `location.origin === "file://"`, exactly as the pane does. That observation proves
nothing; the `fetch()` behaviour is the real test.

**Say which half was checked (L-05).** Measured here: Chrome 151 and Edge 151, on Windows,
current versions only. **Not measured:** Firefox, Safari, any mobile browser, any older version,
and macOS or Linux `file://` behaviour, which is not guaranteed to match. §7 says what follows
from that and what does not.

---

## 2. The matrix — 91 automatic rows

Chrome 151 and Edge 151 returned **identical codes on all 91 rows**. 70 pass, 14 fail, 7
informational. The full result set is written to `.assets-cache/portability/results/` — gitignored
by design: the repository keeps the script and the numbers, never the artefacts.

### Origin

| Row | Result |
| :--- | :--- |
| `location.origin` | `file://` — *informational, and it distinguishes nothing* |
| `isSecureContext` | **true** |
| `crossOriginIsolated` | false |
| `document.fullscreenEnabled` | true |
| cookies | **refused** — not stored |

**`file://` is a secure context.** This single row explains most of the surprises below. Everything
gated on secure context — `crypto.subtle`, `registerProperty`, view transitions, clipboard — is
present, and the assumption that a restricted origin loses them is wrong.

The origin is nonetheless genuinely **opaque**: a worker constructed from a sibling file fails with
an error naming the origin as `'null'`, and service-worker registration fails on the same grounds.
`location.origin` simply does not report it.

### Script and modules

| Route | Result |
| :--- | :--- |
| inline classic `<script>` | PASS |
| classic `<script src="./x.js">` | PASS |
| inline `<script type="module">` | PASS |
| `<script type="module" src="./x.mjs">` | **FAIL** — did not run |
| `import('./x.mjs')` | **FAIL** — failed to fetch dynamically imported module |
| `import(blob:)` | PASS |
| `import(data:)` | PASS |
| classic `<script>` tag pointing at a blob: URL | PASS |
| `new Function(...)` | PASS |

### Fetch-like access — the one hard boundary

| Row | Result |
| :--- | :--- |
| `fetch('./sibling.txt')` | **FAIL** — TypeError: Failed to fetch |
| `fetch(own file)` | **FAIL** — TypeError: Failed to fetch |
| `XMLHttpRequest` on a sibling file | **FAIL** — refused |
| `fetch('data:...')` | PASS |
| `fetch('blob:...')` | PASS |

A deck cannot read its own source at runtime. Anything that would have been loaded by `fetch` must
be present as a JavaScript value, a `data:` URI, or a `blob:` built from one.

### Workers

| Row | Result |
| :--- | :--- |
| classic worker from `blob:` | PASS |
| classic worker from `data:` | PASS |
| **module** worker from `data:` | PASS |
| **module** worker from `blob:` | **FAIL** — load refused before execution |
| worker from a sibling file | **FAIL** — SecurityError, origin `'null'` |
| `OffscreenCanvas` in a worker | PASS |
| service worker — available | true |
| service worker — register | **FAIL** — protocol of origin `'null'` unsupported |

**The module-worker asymmetry is worth naming**, because it is the one place the `blob:` escape
hatch does *not* work while `data:` does. If a deck wants a module worker, build it as a `data:`
URL.

### Storage

`localStorage`, `sessionStorage`, IndexedDB and CacheStorage all work; `navigator.storage.estimate`
reports a real quota. Cookies do not. A deck that wants to remember the slide you were on can.

### Canvas, WebGL and WebGPU

| Row | Result |
| :--- | :--- |
| 2D context, `toDataURL` | PASS |
| image from `data:` — canvas stays **clean** | PASS |
| image from `blob:` — canvas stays **clean** | PASS |
| image from a **sibling file** — canvas is **tainted** | **FAIL** on `getImageData` |
| WebGL1 / WebGL2 context, shader compile, `readPixels` | PASS |
| WebGL texture from `data:` | PASS |
| WebGL texture from a **sibling file** | **FAIL** — SecurityError on `texImage2D` |
| WebGPU adapter | PASS |

A hardware-accelerated renderer was identified through ANGLE on Direct3D 11; the specific GPU is
recorded in the local result file and deliberately not reproduced here. **These rows are
driver-dependent** — that is the caveat that matters, not the card.

### Elements that load local files perfectly well

Stylesheets (`data:` and sibling), `@font-face` (`data:` **and sibling**, both reporting
`FontFace.status === 'loaded'`), `<img>` (`data:` and sibling), SVG (`<img>` from both, inline
`<use>` with an internal reference, `foreignObject`), `<audio>` (`data:` and sibling, metadata and
duration correct), and `AudioContext.decodeAudioData` from a `data:` URI.

This is the "element-like access" half of the boundary, and it is why the single-file rule is about
*script's* access to bytes, not about whether the browser will render a neighbouring file.

### Iframes

Only `srcdoc` is scriptable. `data:`, `blob:` and sibling-file iframes all return a null
`contentDocument`. A deck that wants an isolated sub-document has exactly one route.

### CSS and platform APIs — 27 rows, all passing

`:has()`, nesting, container queries, subgrid, `aspect-ratio`, `text-wrap-balance`, `color-mix`,
`oklch`, `mask-image`, `backdrop-filter`, `filter`, `perspective`, `preserve-3d`,
`scroll-timeline`, anchor positioning; `adoptedStyleSheets`, `customElements`, `dialog.showModal`,
popover, view transitions, `structuredClone`, `ResizeObserver`, `history.pushState`,
`registerProperty`, `matchMedia('print')`, `crypto.randomUUID`, `crypto.subtle.digest`.

**Nothing in the modern CSS toolkit is lost.** The design layer is unconstrained by portability.

---

## 3. The four gesture-gated rows — and the harness that nearly libelled them

Fullscreen, clipboard write, audio-context resume and blob download are gated on a **user
activation**, not on the origin. All four **PASS**, on Chrome and on Edge.

They did not pass at first, and the story is the contract's most important provenance note.

| Attempt | Result | Cause |
| :--- | :--- | :--- |
| four rows chained off one click | 3 of 4 "refused" | a transient activation is **consumed** by the first gated call; rows 2–4 measured a spent grant |
| one click per row | fullscreen still "refused" | the **first** click on a newly opened window is spent focusing it |
| one unmeasured arming click, then one click per row | **all four pass** | — |

Both faults reported `NotAllowedError` / `TypeError: Permissions check failed` — **the exact
vocabulary a genuine origin refusal uses**. Nothing in the output distinguished "the origin said
no" from "my harness never validly asked". Had this note been written from the first run, it would
have told WP3 that a deck cannot go fullscreen, which is false and would have removed a feature the
deck plainly wants.

Generalised as **L-17**. The attribution row that settles it is `document.fullscreenEnabled ===
true`, which needs no activation to read and says the capability was never policy-blocked.

**A note on how the activation is obtained.** It is a real human click. An earlier version of the
runner synthesised one with OS-level keystroke injection and foreground-window stealing; it worked
and it was withdrawn, because it is indistinguishable from input hijacking and this repository
publishes. One click costs seconds and asks nothing of whoever clones it. **Do not reintroduce
it** — if gesture rows are ever hard to collect, collect them by hand.

---

## 4. Two cross-checks, and neither moved a row

**Edge 151 against Chrome 151:** identical codes on all 91 rows, and the informational details
match too. One engine, as decided; the second browser confirms rather than extends.

**The literal double-click against the arranged run:** the probe was opened through the Windows
file association into the **real default browser** — real profile, extensions loaded, network
up — and compared against the dedicated empty profile with DNS black-holed. **Zero disagreements
across all 91 rows.**

This is the check that matters most. The arranged environment is the one a critic would suspect of
flattering the results, and it did not: the matrix describes what a recipient actually gets.

*A caveat found while running it, and it is now a lesson.* The first double-click run harvested a
complete, well-formed, entirely wrong payload — from a probe window left open by the **previous**
run. The window-title channel is global to the desktop, so a stale producer is indistinguishable
from the current one and answers first. The runner now snapshots existing probe windows **by
handle** before launching and ignores them (**L-18**).

---

## 5. What is refused, and what to do instead

Every refusal, paired with the workaround. **There is no row here where the substitute costs the
deck a capability.**

| Refused | Use instead |
| :--- | :--- |
| `fetch` / XHR of any local file, including the deck's own source | inline the data as a JS value, a `data:` URI, or a `blob:` built from one |
| `<script type="module" src>` and relative `import` | `import()` a `blob:` or `data:` URL built from inlined source (§6) |
| module worker from `blob:` | module worker from `data:` — measured working |
| worker from a sibling file | worker from `blob:` or `data:` |
| service worker registration | nothing — a deck has no offline-caching problem; it *is* the file |
| cookies | `localStorage` / `sessionStorage` / IndexedDB, all working |
| canvas & WebGL textures from a sibling file (taints) | `data:` or `blob:` image sources — both keep the canvas clean |
| scriptable `data:` / `blob:` / sibling `<iframe>` | `srcdoc` |

The single-file rule is not softened by any of this. What the matrix adds is *precision about which
half of it bites*: sibling files render but cannot be read, so a deck shipped as a folder would
fail in ways that are invisible until script touches an asset.

---

## 6. 3D and ESM libraries — three.js, tested

**Verdict: usable, at 703 KB, conditional on a one-line build step. Opt-in, never default.**

Measured on Chrome 151, clean profile, DNS black-holed. Both halves of the package inlined into the
page as non-executing `<script type="text/plain">` source — 720,032 characters.

| Row | Result |
| :--- | :--- |
| unmodified package + import map redirecting the specifier | **FAIL** — `Failed to resolve module specifier "./three.core.min.js". Invalid relative url or base scheme isn't hierarchical.` |
| specifier rewritten to the core's `blob:` URL before blobbing the entry | **PASS** — 422 exports |
| `THREE.WebGLRenderer` | PASS — r180 |
| scene built, framebuffer read | PASS — centre pixel `rgba=165,132,71` |
| looked at (**L-01**) | a correctly shaded, lit box; three faces at distinct luminance |

**The finding is the first row.** three@0.180 ships as an entry module that re-exports plus a core
it imports by the relative specifier `./three.core.min.js`. From a `blob:` URL there is no
hierarchical base to resolve that against, so **resolution fails before an import map is
consulted** — the map never gets the chance to redirect it. An ESM library of more than one file
therefore **cannot be inlined verbatim**; its internal specifiers must be rewritten to blob URLs at
build time. For three.js that is one string replacement, and then it renders.

**A correction this produced.** [R5](R5-assets-and-licences.md) recorded three.js at 331 KB. That
was `three.module.min.js` alone — the shim, not the library. With `three.core.min.js` (372.2 KB)
the real inlined cost is **703.2 KB**: 3.7× the entire 192 KB probe deck, not 1.7×.
`tools/assets/measure.py` now measures both halves so the figure cannot drift back. R5's "opt-in,
never default" ruling is unchanged and better supported.

---

## 7. The version floor — and why it is a preflight, not a number

The task asked for a version floor with a reason. The honest answer has two parts.

**What was tested: Chrome 151 and Edge 151, and nothing else.** No older build was run. Naming
"Chrome 125" or any other number would be reading, not testing, and this task's whole method is the
refusal to do that (**L-05**: say which half you checked).

**So the floor is defined operationally.** The deck ships a **capability preflight** — a short
feature-detection block that runs before the deck renders and names what is missing. The floor is
*whatever version passes it*, and the tested-good version is 151.

This is the better contract regardless of what testing old builds would have shown, for three
reasons:

1. **A version number is a proxy for the thing you actually care about**, and a lossy one — vendors
   ship features behind flags, enterprise builds lag, and forks diverge.
2. **The recipient cannot act on a version number.** "Requires Chrome 125+" in a deck that has
   already failed to render is not a diagnosis. A preflight that says *which* capability is absent
   is.
3. **It fails in the safe direction.** An unknown browser is asked what it can do rather than
   assumed broken or assumed fine.

**What the preflight must check** — the load-bearing rows, in the order they would bite:

```
isSecureContext                      the whole matrix rests on it
CSS.supports('container-type: inline-size')
CSS.supports('selector(:has(*))')
document.fonts && document.fonts.status
import(blob:)                        only if the deck inlines an ESM library
WebGLRenderingContext                only if the deck renders 3D
```

**Recommended for T-005 and WP3:** the build emits only the checks the deck actually uses, and the
deck degrades to a legible static state rather than a blank page when one fails. **Raised as
[T-019](../../tasks/T-019-build-the-capability-preflight-the-deck-ships-wit.md)**, blocked on build
mode, since the preflight is emitted by it. Note the distinction that task turns on: T-005 gates
the deck at **build** time on the author's machine, the preflight runs at **open** time on the
recipient's. Neither replaces the other.

---

## 8. "Glitch-free", defined so a check can test it

Rule 2 in [`CLAUDE.md`](../../CLAUDE.md) requires a deck to render **glitch-free in recent
Chrome/Edge**. That is a testable statement only if it is decomposed. Proposed definition, for
T-005 to implement — a deck is glitch-free when, opened from `file://` with the network disabled,
**all** of the following hold:

| # | Check | How it is tested |
| :--- | :--- | :--- |
| 1 | **Zero external references** | static scan: every `src`, `href` and `url()` is `data:`, `blob:`, `#`, or absent |
| 2 | **No console errors and no unhandled rejections** | collected over the full load and one pass through every slide |
| 3 | **Every declared face actually loaded** | `document.fonts.status === 'loaded'` *and* every `FontFace.status === 'loaded'` — **not** that `document.fonts.load()` resolved, which reports only that faces matched the query |
| 4 | **No text rendered in a fallback family** | computed `font-family` of every text node resolves to an embedded face |
| 5 | **Nothing overflows its stage** | for every slide, `scrollWidth <= clientWidth` and `scrollHeight <= clientHeight` on the stage element |
| 6 | **Layout is stable after fonts settle** | no layout shift between first paint and `document.fonts.ready` |
| 7 | **Every canvas/WebGL surface drew something** | framebuffer read returns a non-background pixel — a renderer that silently draws nothing passes every other check |
| 8 | **Every slide reached** | the deck can be advanced from first to last without a script error |
| 9 | **Looked at** (**L-01**) | a human opens it offline; checks 1–8 do not replace this and never will |

Checks 3 and 7 exist because this task watched both fail in the optimistic direction:
`document.fonts.load()` resolving says nothing about whether a fetch succeeded, and a WebGL context
that reports PASS on every API call can still render a black frame.

---

## 9. Mobile, other browsers, and printing — stated, not left implicit

**Mobile: degrade gracefully, do not chase.** Mobile is secondary by decision. Not measured here —
no mobile browser was tested, and nothing in this note should be read as a claim about one. The
position: the deck must remain **legible and advanceable** on a small screen, and may drop motion,
3D and hover-dependent progressive disclosure. That is a design constraint for WP3, not a
portability finding, and it should be verified when there is a deck worth verifying.

**Firefox and Safari: not measured.** They degrade gracefully by decision and do not set the bar.
`file://` policy is known to differ between engines — Firefox historically treats sibling files
differently from Chrome — so **the sibling-file rows in §2 must not be assumed to carry over**. The
deck's own rules make this mostly moot: a `portable` deck has no siblings.

**Printing: optional, and cheap so far.** `matchMedia('print')` is available, so a print stylesheet
can be authored and detected. What was **not** tested is whether `window.print()` behaves from
`file://` and whether a print stylesheet reproduces the deck faithfully at page size. Printing is
"a mode the user can force on, never a constraint on the design" — nothing in this matrix threatens
it, and nothing here confirms it either. **Raised as
[T-018](../../tasks/T-018-measure-the-printable-mode-what-printing-from-fi.md)**, which also has to
say plainly what a printed deck cannot preserve: anything behind interaction, motion or 3D.

> **Closed by [R7](R7-printable-mode.md), 2026-08-07.** `window.print()` works and needs **no user
> activation**; `beforeprint`/`afterprint` both fire. One correction to the paragraph above: this
> note calls `matchMedia('print')` *available*, which is true and misleading — inside the
> `beforeprint` handler it still reads **`false`**, so a deck must use the **events**, not the
> query. R7 also found that printing changes the layout viewport, which makes a width-responsive
> deck switch its own view mid-print — a portability behaviour this matrix had no row for.

---

## 10. What this note is *not* evidence about

Stated plainly, because the largest risk in a document like this is a reader taking the confident
parts as covering the untested ones:

- **Any browser other than Chrome 151 and Edge 151 on Windows.** No Firefox, no Safari, no mobile,
  no older version, no macOS or Linux.
- **Performance.** Nothing here measures frame rate, memory, or how a 12-slide deck with 3D behaves
  on a modest machine. The WebGL rows say a feature exists, not that it is fast.
- **Whether a real deck built this way reads well.** That is L-01's territory and T-005's, and it
  is the thing no matrix can answer.
- **The specific GPU, driver or machine anything ran on** — deliberately generalised out, per the
  publishing constraints in [`CLAUDE.md`](../../CLAUDE.md).
