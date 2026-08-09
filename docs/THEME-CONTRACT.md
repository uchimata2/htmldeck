# htmldeck — the theme contract

**What a theme must supply, and what a deck may not contain outside it.** The rules that decide
whether a *look* is any good are [`DESIGN-SYSTEM.md`](DESIGN-SYSTEM.md)'s; this file says only where
the values live and which of them a theme is allowed to choose.

It exists because CLAUDE.md defers the template generator and asks for the layer that makes one
cheap to add. **A generator needs a contract to satisfy.** Until there is one, "every layer
parametric" is a claim about a single hand-built deck, and the measurement that opened
[T-007](../tasks/T-007-define-the-parametric-theme-layer.md) is what that claim was worth: 57
custom properties, and 62 design-unit literals sitting outside them.

```
python tools/deck/theme.py tokens                       # this table, as data
python tools/deck/theme.py validate themes/quarto.css   # a theme against it
python tools/deck/theme.py swap <deck> themes/<name>.css -o <out.html>
python tools/deck/theme.py check <deck>                 # what the gate asks
```

---

## 1. A theme is a file

**The region.** Every deck carries exactly one `<style id="theme">`, and it holds the whole theme:
the `@font-face` declarations and the `:root` blocks, and nothing else. Everything else the deck
styles lives in another `<style>`. Swapping a theme replaces that element's contents; **no rule
outside it is edited, ever.**

**The faces travel with it.** Face pairing is one of the five axes, and a face that is not embedded
is not a face a deck can swap to — so the region carries the fonts, not just their names. In the
*source* form of a theme that is one directive line:

```css
/* htmldeck-faces: instrument-serif, space-grotesk, jetbrains-mono */
```

`theme.py` resolves each slug against `themes/faces/<slug>.css`, which holds one `@font-face` and
the licence notice that DS-032 requires to travel with it. The **resolved** form — faces inlined as
base64 — is what sits in the deck, so DS-001 still holds: one file, zero external references. Two
themes that share a face therefore share one copy of it in the repository and still produce
self-contained decks.

**The demonstration deck is built, not committed.** `examples/` carries the reference deck; a
themed copy of it is an output of `theme.py swap` and belongs in `.assets-cache/`, beside the
seeded variants.

## 2. Primitive, derived, fixed

| Kind | Means | A theme may |
| :--- | :--- | :--- |
| **primitive** | A dial. The value is a choice this theme makes. | set it freely, inside the *Legal* column |
| **derived** | `calc()` over primitives. Its value is a consequence of the dials. | copy it unchanged; editing one is departing from the scale, which `validate` reports |
| **fixed** | Declared in the region but not the theme's to vary — a rule owns the number. | declare it and leave it |

**Derivation is used where a scale exists, and nowhere else.** Two places qualify: the **text
scale**, from `--fs-base` and `--type-ratio`, and the **spacing scale**, from `--sp-unit` and
`--sp-ratio`. Those are where a literal silently breaks the family — a size that is nearly on the
scale reads as a mistake rather than as a choice. Colour, faces, shape and motion are set directly,
because a *derived* colour is a generator's job and the generator is deliberately not built yet.

**What the display sizes say about that.** `--fs-display`, `--fs-title` and `--fs-figure` are
primitives, not steps. The shipping theme's are 67, 96 and 190 design units and no ratio joins
them: each is composed against the 1920-unit stage. Forcing them onto the text scale would be a
redesign dressed as a parameterisation, so the contract says they are dials and says why.

## 3. The tokens

`Axis` is one of **colour · type · geometry · shape · motion**. `Legal` is checked by
`theme.py validate`; **every range cites the rule it comes from**, because a threshold invented to
fit one deck is worse than no threshold (**L-38**).

### 3.1 Fixed

| Token | Axis | Kind | Governs | Legal |
| :--- | :--- | :--- | :--- | :--- |
| `--du` | geometry | fixed | The design unit. One CSS pixel before the transform. DS-060 fixes the stage at 1920×1080 of them; a theme that changes this changes the resolution contract, not the look. | `1px` |

### 3.2 Colour

| Token | Axis | Kind | Governs | Legal |
| :--- | :--- | :--- | :--- | :--- |
| `--paper` | colour | primitive | The ground. Never pure white (DS-023). | colour |
| `--paper-sunk` | colour | primitive | A panel set into the ground. | colour |
| `--ink` | colour | primitive | Body text. Never pure black (DS-023). | colour |
| `--ink-soft` | colour | primitive | Secondary text. | colour |
| `--ink-faint` | colour | primitive | Mono labels and marginalia. | colour |
| `--line` | colour | primitive | Decorative hairline. Exempt from 1.4.11 — it separates, it does not mean. | colour |
| `--line-firm` | colour | primitive | A structural edge. | colour |
| `--ui-line` | colour | primitive | An interactive border. Carries 1.4.11's 3:1, which is why DS-013 keeps it off `--line`. | colour |
| `--data-quiet` | colour | primitive | A neutral data mark. Carries 1.4.11's 3:1 for the same reason. | colour |
| `--field` | colour | primitive | The darker field the stage floats on (DS-050). | colour |
| `--shadow` | colour | primitive | The stage's shadow colour. | colour |
| `--shadow-soft` | colour | primitive | A panel's shadow colour. | colour |
| `--accent` | colour | primitive | The one accent (DS-020). It means something wherever it appears. | colour |
| `--accent-ink` | colour | primitive | The accent as text on the ground. | colour |
| `--accent-wash` | colour | primitive | The accent as a ground. | colour |
| `--pos` | colour | primitive | The positive role, deck-wide (DS-026). | colour |
| `--neg` | colour | primitive | The negative role. | colour |
| `--caution` | colour | primitive | The caution role. | colour |

### 3.3 Type

| Token | Axis | Kind | Governs | Legal |
| :--- | :--- | :--- | :--- | :--- |
| `--font-display` | type | primitive | The display face (DS-030). Never Inter, Roboto, Arial or `system-ui` (DS-031). | — |
| `--font-text` | type | primitive | The text face. | — |
| `--font-mono` | type | primitive | The mono face, which carries the domain vocabulary (DS-038). | — |
| `--fs-base` | type | primitive | Body size in design units — the dial the whole text scale turns on. DS-034 fixes the band. | n 24-28 |
| `--type-ratio` | type | primitive | One step of the text scale, and of the reading view's. | — |
| `--fs-small` | type | derived | One step below body: control labels and panel text. | — |
| `--fs-body` | type | derived | Body text (DS-034). | — |
| `--fs-lead` | type | derived | One step above body: a lead paragraph. | — |
| `--fs-subhead` | type | derived | Two steps above body (DS-034). | — |
| `--fs-bottom` | type | derived | Three steps above body — the bottom line, second only to the headline (DS-203). | — |
| `--fs-mono` | type | primitive | Mono labels. DS-036 fixes the band, and 16–17 is marginalia that never carries meaning. | du 16-18 |
| `--fs-display` | type | primitive | The slide headline. Composed against the stage, not stepped. | — |
| `--fs-display-lg` | type | primitive | A closing or full-bleed headline, between display and title. | — |
| `--fs-title` | type | primitive | The title slide's headline. | — |
| `--fs-figure` | type | primitive | A headline statistic. | — |
| `--lh-body` | type | primitive | Body line height (DS-034). | n 1.40-1.70 |
| `--track-display` | type | primitive | Negative tracking on display headings (DS-037). | — |
| `--track-mono` | type | primitive | Tracking on mono labels (DS-036). | — |
| `--measure` | type | primitive | Line length (DS-039), inside 45–75 characters. | — |
| `--doc-fs` | type | primitive | The reading view's body size, in `rem` so it honours the reader (DS-074). | — |
| `--doc-fs-mono` | type | primitive | Mono labels in the reading view. A floor, like `--fs-mono`. | — |
| `--doc-fs-sm` | type | derived | One step below body, in the reading view. | — |
| `--doc-fs-lead` | type | derived | One step above body. | — |
| `--doc-fs-head` | type | derived | The reading view's headline, four steps up the same ratio. | — |
| `--doc-fs-title` | type | derived | The reading view's document title. | — |
| `--doc-fs-figure` | type | primitive | A headline statistic in the reading view. Composed, like the stage's. | — |
| `--doc-track-mono` | type | primitive | Tracking on mono labels in the reading view. | — |

### 3.4 Geometry

| Token | Axis | Kind | Governs | Legal |
| :--- | :--- | :--- | :--- | :--- |
| `--sp-unit` | geometry | primitive | The rhythm's step, in design units — the density dial. | — |
| `--sp-ratio` | geometry | primitive | One step of the spacing scale. | — |
| `--sp-0` | geometry | derived | Half a step below the base: the gap inside a row. | — |
| `--sp-1` | geometry | derived | The gap inside a control. | — |
| `--sp-2` | geometry | derived | The base gap. | — |
| `--sp-3` | geometry | derived | One step up. | — |
| `--sp-4` | geometry | derived | Two steps up. | — |
| `--sp-5` | geometry | derived | Three steps up: the gap between blocks. | — |
| `--pad-x` | geometry | primitive | The slide's side padding. | — |
| `--pad-y` | geometry | primitive | The slide's top padding. | — |
| `--pad-bottom` | geometry | primitive | Clearance under a slide for the chrome row (DS-217). | — |
| `--chrome-inset` | geometry | derived | How far the chrome row sits off the stage floor. | — |
| `--bottom-measure` | geometry | primitive | The bottom line's maximum width (DS-211). | — |
| `--rule-len` | geometry | primitive | The accent rule above the bottom line. | — |
| `--tick-len` | geometry | primitive | The eyebrow's tick. | — |
| `--disc-panel-w` | geometry | primitive | A disclosure panel's width (DS-138 places it below its control). | — |
| `--disc-key-w` | geometry | primitive | The key column inside a disclosure panel. | — |
| `--doc-sp` | geometry | primitive | The reading view's base gap, in `rem`. | — |
| `--doc-sp-2xs` | geometry | derived | Four spacing steps down: the gap under a label. | — |
| `--doc-sp-xs` | geometry | derived | Two steps down. | — |
| `--doc-sp-sm` | geometry | derived | One step down. | — |
| `--doc-sp-lg` | geometry | derived | One spacing step up, in the reading view. | — |
| `--doc-pad-b` | geometry | primitive | Trailing space under the reading view. | — |
| `--doc-measure` | geometry | primitive | The reading view's column width. | — |
| `--doc-tick` | geometry | primitive | The eyebrow's tick in the reading view. | — |
| `--doc-hit` | geometry | primitive | The view switch's target height. ≥ 44 CSS px is the floor DS-168 sets in a `rem` rendering. | rem 2.75- |

### 3.5 Shape

| Token | Axis | Kind | Governs | Legal |
| :--- | :--- | :--- | :--- | :--- |
| `--radius` | shape | primitive | A card's corner (DS-049). Zero is a legitimate theme. | — |
| `--radius-sm` | shape | primitive | A small control's corner. | — |
| `--radius-xs` | shape | primitive | A mark's corner. | — |
| `--hair` | shape | primitive | A hairline's weight. | — |
| `--rule` | shape | primitive | A structural rule's weight. | — |
| `--focus-w` | shape | primitive | The focus indicator's weight (2.4.7, 2.4.13). | — |
| `--focus-offset` | shape | primitive | The focus indicator's offset. | — |
| `--chev-stroke` | shape | primitive | The chevron's stroke. | — |
| `--shadow-y` | shape | primitive | The stage's shadow drop (DS-050). | — |
| `--shadow-blur` | shape | primitive | The stage's shadow blur. | — |
| `--shadow-y-sm` | shape | primitive | A panel's shadow drop. | — |
| `--shadow-blur-sm` | shape | primitive | A panel's shadow blur. | — |
| `--icon` | shape | primitive | A feature icon (DS-113). | — |
| `--icon-sm` | shape | primitive | An icon set inline with body text. | — |
| `--icon-ui` | shape | primitive | An icon inside a control. | — |
| `--chev` | shape | primitive | The chevron's box. | — |
| `--swatch` | shape | primitive | A legend chip (DS-026). | — |
| `--disc-mark-size` | shape | primitive | The disclosure mark's box (DS-165). | — |
| `--disc-mark-bar` | shape | primitive | The bar inside the disclosure mark. | — |
| `--disc-mark-stroke` | shape | primitive | That bar's weight. | — |
| `--disc-hit` | shape | primitive | The disclosure control's target. DS-168 requires ≥ 48 design units, because the stage bottoms out at half scale. | du 48- |
| `--doc-hair` | shape | primitive | A hairline in the reading view, in `rem`. | — |
| `--doc-radius` | shape | primitive | A control's corner in the reading view, in `rem`. | — |

### 3.6 Motion

Durations are bounded by DS-141's 500 ms cap, with DS-140's two long motions banded rather than
pinned — see §4.

| Token | Axis | Kind | Governs | Legal |
| :--- | :--- | :--- | :--- | :--- |
| `--rise-dur` | motion | primitive | Rise: entry (DS-140), inside the cap (DS-141). | ms 0-500 |
| `--rise-ease` | motion | primitive | Rise's easing. | — |
| `--rise-stagger` | motion | primitive | The gap between staggered entries. | — |
| `--rise-dist` | motion | primitive | How far a risen element travels. The distance dial. | — |
| `--current-dash` | motion | primitive | Current: the flow dash pattern (DS-140). | — |
| `--current-dur` | motion | primitive | Current's period. It loops, so DS-218's stop control is required — and the band is DS-140's. | ms 3000-6000 |
| `--open-dur` | motion | primitive | Open: a disclosure reveal (DS-140), inside the cap (DS-141). | ms 0-500 |
| `--open-rise` | motion | primitive | How far an opening panel travels. | — |
| `--open-squash` | motion | primitive | The scale an opening panel starts at. | — |
| `--turn-dur` | motion | primitive | Turn: a card reveal (DS-140), inside the cap (DS-141). | ms 0-500 |
| `--scale-dur` | motion | primitive | Scale: a reveal (DS-140), inside the cap (DS-141). | ms 0-500 |
| `--pulse-dur` | motion | primitive | Pulse-once. Never loops (DS-140). | ms 800-1600 |
| `--pulse-delay` | motion | primitive | How long Pulse-once waits for the slide to settle. | — |
| `--slide-dur` | motion | primitive | The inter-slide transition, which DS-141 puts at 400–500 ms. | ms 400-500 |

---

## 4. What this contract changed in the ruleset

Two `hard` rules stated the shipping theme's own numbers as the rule, and their checks enforced the
pin. A second theme moving the density axis or the motion axis therefore failed the gate **for
being a second theme** — the exact failure the parametric layer exists to prevent. Both were
amended on [T-033](../tasks/T-033-reconcile-ds-131-with-the-chrome-budget.md)'s precedent, and both
amendments are faithful to the rule's own recorded reason.

| Rule | Was | Is | Why the change is faithful |
| :--- | :--- | :--- | :--- |
| DS-034 | body 24–28 du **at line-height 1.55** | body 24–28 du at line-height **1.40–1.70**, this theme's being 1.55 | [`DESIGN-RATIONALE.md`](DESIGN-RATIONALE.md) §3 argues the type **floor** and computes it; line-height is not argued there at all. |
| DS-140 | four motions at 340 / 380 / 420 / 300 ms, 1.2 s, 4.5 s | the same four motions, **banded**: reveals and entries inside DS-141's cap, Pulse-once 0.8–1.6 s, Current 3–6 s | [`DESIGN-RATIONALE.md`](DESIGN-RATIONALE.md) §4 argues that *a named vocabulary is what stops animation becoming decoration*. **The names and the closure carry that; the milliseconds are one theme's instance of it.** |

## 5. What may still be a literal

A length or a duration written outside the region is a defect unless it is on this list. **The list
is data, not prose** — `theme.py check` reads these four rows and prints how many literals each
covers, so an exemption that silently starts covering half the deck shows up as a number that moved
(**L-36**).

**Easing is on the same test and needs no table, because it has no exceptions.** A component may
write an easing **keyword** and may never write an easing **curve**. The keywords are the rules'
own words: DS-141 fixes entry and transition at *max 500 ms, ease-in-out*, so a component writing
`ease-in-out` is quoting the rule rather than choosing a feel, and `linear` is the only easing that
leaves a looping dash and a zero-duration step undistorted — which is the whole of what `.current`
and the slide's `visibility` transition need it for. **A `cubic-bezier()` or a `steps()` is a
choice about how a motion feels.** It belongs to the theme, this deck has exactly one — `--rise-ease`
— and one written outside the region is a component that a theme cannot reach. *Added 2026-08-09 by
[T-016](../tasks/T-016-the-interaction-and-motion-layer.md): the scan below has covered lengths and
durations since T-007 and easing was never in its subject, so `no component hard-codes a duration or
an easing` was half true and read as settled.*

**The line the middle rows draw is the one that matters: composition versus look, inside two named
scopes and nowhere else.** A slide may compose its own geometry — a ledger's three tracks, a note's
measure, a tick's height — because those exist to fit *this deck's content*, and a generated deck
would emit different ones. What it may **never** do is choose its own type size, tracking, corner,
shadow or timing: those are the look, they belong to every slide at once, and a theme that cannot
reach them is not a theme. **Outside those two scopes nothing is exempt by property** — a shared
component's icon size is a value a denser theme has to be able to shrink.

| Where | Property | Value | Why |
| :--- | :--- | :--- | :--- |
| `.stage` | any | `1920` `1080` | DS-060 fixes the stage at 1920 × 1080 design units. A resolution contract, not a look. |
| `.sr` | any | `1px` `-1px` | The visually-hidden clip. A rendering idiom with no visible size. |
| `#slides` | not `font-size` `letter-spacing` `line-height` `border-radius` `box-shadow` `animation` `transition` `outline` | any | The rules that exist because *this* deck has a ledger with three columns. Composition; a generated deck emits its own. |
| `.ruler` | not `font-size` `letter-spacing` `line-height` `border-radius` `box-shadow` `animation` `transition` `outline` | any | Proportions internal to one component: a section tick is taller than a slide tick because it ranks above it, at every density. DS-217's 4-unit mark floor is a *rule's* number and sits here for the same reason. |
| any | any | `0` | No unit to vary. |

Anything not covered here is a token. That is the whole test, and it is why the list is short.
