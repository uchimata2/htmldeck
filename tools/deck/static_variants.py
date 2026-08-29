#!/usr/bin/env python3
"""Break the rules T-005 closed, one at a time, and require the gate to notice.

Fourth sibling of `deliverable_variants.py`, `contract_variants.py` and `content_variants.py`, and
the reason has not changed: **a check that has never been seen to fail is a claim about the
instrument, not about the deck** (**L-36**). T-005 took the gate from 44 checked rules to 77, which
is 33 checks nobody had watched fail — and T-038 had just finished proving that a green row can
mean the check cannot fire at all.

Two halves, because they cost different amounts:

- **static** — a string edit and a predicate, no browser. Every one of these runs in milliseconds,
  so there is no reason to sample rather than cover.
- **rendered** — one real Chrome render each, so this half covers the rules where the measurement
  itself was the new thing rather than the threshold.

    python tools/deck/static_variants.py
    python tools/deck/static_variants.py --static-only

Each variant derives from `examples/reference-deck.html`, so everything except the seeded break is
held constant, and every edit asserts that it matched (**L-04**). Pure standard library (**L-07**).
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths                                                        # noqa: E402
import render                                                        # noqa: E402
import audit                                                         # noqa: E402
import check                                                         # noqa: E402
import glitchfree                                                    # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = render.ROOT
SRC = os.path.join(ROOT, "examples", "reference-deck.html")
OUT = os.path.join(render.OUT, "variants")

# (name, rule it must break, [(old, new), ...]) - the edit is the smallest one that breaks the
# rule and nothing else, because a variant that breaks three rules proves nothing about any of them.
STATIC_VARIANTS = [
    # ---- added by T-202, which re-bound DS-122 from five vendor names onto when the marks exist.
    # The engine is invented on purpose: a check that has to know a library's name is a check the
    # next library walks past, which is what the blocklist did to four of them (**L-125**).
    ("chart-engine-undeclared", "DS-122", [
        ("</body>",
         "<script>var e=document.createElementNS('http://www.w3.org/2000/svg','path');"
         "</script></body>")]),
    ("chart-canvas-undeclared", "DS-122", [
        ("</body>", "<canvas id=\"chart\"></canvas></body>")]),
    ("cdn-reference", "DS-002", [
        ('<meta charset="utf-8">',
         '<meta charset="utf-8"><link rel="stylesheet" href="https://cdn.example.com/x.css">')]),
    ("script-reads-a-file", "DS-005", [
        ("var DECK = 'Buy frequency before bikes';",
         "var DECK = 'Buy frequency before bikes';\n  fetch('data.json');")]),
    ("colour-outside-the-tokens", "DS-010", [
        (".legend i{width:var(--swatch)",
         ".legend i{background:#C43B2A;width:var(--swatch)")]),
    # ---- added by T-007, which made the theme a region and the token set a contract
    ("type-scale-outside-the-region", "DS-010", [
        # A slide setting its own type size is the defect the composition/look line exists to
        # catch: the geometry around it may be this deck's, the type scale never is.
        (".close-h{font-size:var(--fs-display-lg)", ".close-h{font-size:calc(81*var(--du))")]),
    ("derived-token-pinned-to-a-literal", "DS-013", [
        # The whole point of `derived`: a theme may set the dial, never the step. Pinned, the
        # family silently stops moving with `--type-ratio` and every individual value still
        # looks like a token.
        ("--fs-lead:calc(var(--fs-base)*var(--type-ratio)*var(--du));",
         "--fs-lead:calc(30*var(--du));")]),
    ("two-theme-regions", "DS-011", [
        ('<style id="slides">',
         '<style id="theme">:root{--accent:#1E7A4C}</style>\n<style id="slides">')]),
    ("motion-outside-its-band", "DS-140", [
        # 2.4 s is neither a reveal under DS-141's cap nor inside either long motion's band. It
        # breaks **DS-140**, not DS-141: DS-141 yields to the vocabulary by name (F-04), so the
        # rule that still has something to say is the one that states the band.
        ("--pulse-dur:1.2s;", "--pulse-dur:2.4s;")]),
    ("a-second-accent", "DS-020", [
        ("--accent-wash:#EBE7F5;", "--accent-wash:#EBE7F5;\n  --accent-two:#1E7A4C;")]),
    ("pure-white-ground", "DS-023", [
        ("--paper:#F3F0E8;", "--paper:#FFFFFF;")]),
    ("body-type-off-the-band", "DS-034", [
        # The dial, not the step. Since T-007 `--fs-body` derives from `--fs-base`, so seeding
        # the derived token would break the contract as well as the band and prove neither.
        ("--fs-base:26;", "--fs-base:21;")]),
    ("viewport-unit-decoration", "DS-065", [
        (".legend{display:flex", ".legend{margin-top:2vh;display:flex")]),
    ("hard-coded-svg-colour", "DS-118", [
        ('<line class="axis" x1="150" y1="420" x2="1660" y2="420"/>',
         '<line class="axis" x1="150" y1="420" x2="1660" y2="420" stroke="#8D8572"/>')]),
    ("animation-over-the-cap", "DS-141", [
        ("--slide-dur:420ms;", "--slide-dur:900ms;")]),
    ("styled-bare-b", "DS-045", [
        # The narrow reading, which is the rule as clarified 2026-08-09: a rule on the ELEMENT
        # reaches every `<b>` in the deck, so the deliverable's weight becomes a global default.
        # `.bottom-line b` is deliberately NOT this, and the deck keeps four such selectors.
        # No length in the seeded rule: a `letter-spacing` literal here would break DS-010's
        # region check as well, and a variant that breaks two rules proves nothing about either.
        ("</nav>\n", "</nav>\n<style>b{font-weight:800}</style>\n")]),
    ("hover-only-reveal", "DS-163", [
        (".disc-btn:hover{border-color:var(--accent);color:var(--ink)}",
         ".disc-btn:hover{border-color:var(--accent);color:var(--ink)}\n"
         ".disc:hover .disc-panel{display:block}")]),
    # ---- added by T-069, which stopped excusing *never a dead link*
    ("provenance-link-into-the-authors-disk", "DS-105", [
        # The defect the rule has always named and nothing has ever caught: a link that resolves
        # perfectly on the machine the deck was written on and is dead the moment it is emailed.
        # `file://` is the honest form of it; a relative path is the same defect wearing a shorter
        # string, and the check treats them alike for that reason.
        # *Re-anchored 2026-08-12 by T-103*: a one-source mark is the `.sources--one` shape now,
        # so the link is seeded where a link actually goes - inside the item.
        ('<span class="sources-box" id="src20"><span class="sources-item">Ridership model</span>',
         '<span class="sources-box" id="src20"><span class="sources-item">'
         '<a class="sources-link" href="file:///C:/sources/ridership-model.md">Ridership '
         'model</a></span>')]),
    ("provenance-link-to-a-fragment-that-is-not-there", "DS-105", [
        # The other half, and the one a person cannot see by reading: an in-document anchor whose
        # target was renamed. It looks like a working link and behaves like a dead one.
        # *Re-anchored 2026-08-12 by T-103*, for the reason above.
        ('<span class="sources-box" id="src25"><span class="sources-item">Cost model</span>',
         '<span class="sources-box" id="src25"><span class="sources-item">'
         '<a class="sources-link" href="#src-cost-model">Cost model</a></span>')]),
    # ---- added by T-016, which made the markup a contract
    ("control-with-no-aria-controls", "DS-229", [
        # The defect a generator produces and a person does not: the tenth disclosure looks
        # identical to the other nine and its panel is wired to nothing. Nothing in the render
        # gate sees it either - the panel still opens, because the script pairs them by DOM
        # position, and only a reader on a screen reader loses the association.
        ('<button class="disc-btn" aria-expanded="false" aria-controls="p11">',
         '<button class="disc-btn" aria-expanded="false">')]),
    ("panel-outside-its-disclosure", "DS-229", [
        # The place half. The panel is still in the slide and still styled, so it renders where it
        # always did; what it has stopped being is part of a component.
        ('<div class="disc" data-disc="instances">\n    <button class="disc-btn" '
         'aria-expanded="false" aria-controls="p10">',
         '<div class="disc" data-disc="instances"></div>\n  <div>\n    <button class="disc-btn" '
         'aria-expanded="false" aria-controls="p10">')]),
    ("component-nobody-contracted", "DS-229", [
        # A shared component added the way components are actually added - by writing a rule in
        # the shared block. The contract cannot know about it, which is the whole point: the row
        # is what makes it emittable, and the gate is what makes the row get written.
        (".icon{width:var(--icon)", ".callout{color:var(--accent)}\n.icon{width:var(--icon)")]),
    # **The form the rule was written from, and the form that walked through it** (T-197, and the
    # hole found the day 0.5.0 shipped). A build writes the separator as `&middot;`, so the eyebrow
    # never reached the check as text - `runs()` decoded `&nbsp;` and `&amp;` and nothing else, and
    # a digit followed by an ampersand is not a digit followed by a separator. Both forms are
    # seeded, because a rule that catches only the decoded one catches only decks nobody built.
    ("eyebrow-that-repeats-the-position-and-stage", "DS-241", [
        ('<span class="tick"></span>The two proposals',
         '<span class="tick"></span>05 &middot; The choice')]),
    ("eyebrow-that-repeats-the-position-decoded", "DS-241", [
        ('<span class="tick"></span>Corridor by corridor',
         '<span class="tick"></span>06 · The choice')]),
    ("motion-that-stopped-reading-its-token", "DS-229", [
        # **The half `theme.py`'s literal scan cannot state, and the seed has to avoid writing a
        # literal or it proves the wrong thing.** Turn reads the slide transition's dials instead
        # of its own: every token is still declared, still inside its band, and there is no literal
        # anywhere for the scan to find. What has gone is the tokenisation itself - a theme moving
        # Turn now moves everything except the disclosure mark.
        # T-112 added `--motion-kind` to this rule, so the seed carries it through both
        # halves: the defect being seeded is the tokenisation, and a variant that also
        # dropped the kind declaration would be caught by DS-237 and prove the wrong thing.
        # **The rule moved onto the affordance band on 2026-08-20** (DS-240, T-198): the mark is a
        # control answering the hand, not a reveal, and it read Turn's pair until then. The variant
        # follows the deck rather than being deleted - what it seeds is the tokenisation going away,
        # and that defect is the same whichever band the rule reads.
        (".disc-mark::after{width:var(--disc-mark-stroke);height:var(--disc-mark-bar);\n"
         "  transition:transform var(--afford-dur) var(--afford-ease);--motion-kind:affordance}",
         ".disc-mark::after{width:var(--disc-mark-stroke);height:var(--disc-mark-bar);\n"
         "  transition:transform var(--slide-dur) var(--slide-ease);--motion-kind:affordance}")]),
    ("easing-curve-in-a-component", "DS-010", [
        # §5's line, and the one the scan could not see until T-016: a curve is a choice about how
        # a motion FEELS, so a component writing one has taken a decision the theme owns.
        #
        # **It seeds a NEW transition rather than rewriting a tokenised one**, and that is the
        # point rather than convenience: rewriting an existing motion would also drop the token
        # its contract row names, so DS-229 would fail as well and the variant would prove nothing
        # about either rule. The duration is a token here for the same reason - a literal would be
        # caught by the length half of the same scan.
        (".legend{display:flex;gap:var(--sp-3);align-items:center}",
         ".legend{display:flex;gap:var(--sp-3);align-items:center;"
         "transition:opacity var(--scale-dur) cubic-bezier(.34,1.56,.64,1)}")]),
    # ---- added by T-016 step 4, which made the editorial split a rule
    ("a-fifth-editorial-kind", "DS-229", [
        # DS-230's vocabulary is closed, and `appendix` is the exact value the closure exists to
        # refuse - the name a generator reaches for when the content did not fit anywhere else.
        # The markup is otherwise untouched: the panel opens, reads and closes as it always did,
        # which is why nothing but the contract can see this.
        ('<div class="disc" data-disc="condition">\n    <button class="disc-btn" '
         'aria-expanded="false" aria-controls="p8">',
         '<div class="disc" data-disc="appendix">\n    <button class="disc-btn" '
         'aria-expanded="false" aria-controls="p8">')]),
    ("marker-defined-in-another-slide", "DS-232", [
        # **The defect that shipped four blank arrowheads** (T-104). The reference deck defines a
        # marker per slide, correctly; this points one slide's arrow at another slide's marker.
        # Nothing else moves - the connector is still directional, still labelled, still meets its
        # target - and it draws no arrowhead anywhere but the slide holding the definition.
        ("url(#ar4)", "url(#ar9)")]),
    ("bottom-line-supported-only-behind-the-click", "DS-231", [
        # **The failure a generator writes and a reader meets closed.** The deliverable is rewritten
        # to quote the gate's 26%, which lives in the panel and nowhere on the slide - so the slide
        # asserts a figure it does not show, and looks entirely fine until someone asks where the
        # number came from. The face is untouched, so no other row moves.
        ("<b>Nothing before month 18 is irreversible, and the\n"
         "    $1.5M reserve buys 16 Old Quarter stations if the gate fails.</b>",
         "<b>The gate clears at 26%, so nothing before month 18 is irreversible.</b>")]),
]

# One render each. These are the rules where T-005 added the MEASUREMENT and not just a threshold,
# so a string edit alone would prove nothing about whether the probe can see the defect.
# The one-source provenance mark, written once: two anchors below quote it (T-103).
MARK21 = ('<p class="provenance"><span class="sources sources--one"><svg class="sources-mark" aria-hidden="true"><use href="#i-source"/></svg><span class="sources-box" id="src21"><span class="sources-item">Ridership model</span></span></span></p>')

# The anchor T-214's two element-injecting seeds hang off - the one headline in the deck whose
# text is unique, so the injection lands in a slide (the probe walks `.stage` only) and lands
# once. Named rather than repeated because both directions must inject at the SAME place: a
# pass seed and a fail seed differing in where they sit would not be a pair.
SEED_HEAD = '<h2 class="headline rise" style="--i:1">The window shuts in March</h2>'

RENDER_VARIANTS = [
    ("slide-is-not-a-section", "DS-080", [
        ('<section class="slide" data-name="Waiting is the trip"',
         '<div class="slide" data-name="Waiting is the trip"'),
        # **The closing tag, which this variant left behind until T-055.** Without it the document
        # is malformed, Chrome repairs it, and what the run measures is the repair rather than the
        # rule - the same variant failed DS-091, DS-130 and DS-075 as collateral, reporting a slide
        # with no headline whose headline the parser had lifted out of it. The anchor is the
        # slide's own bottom line: `</section>` is not unique and neither is the provenance mark
        # above it.
        # *Re-anchored 2026-08-12 by T-103*: the mark this anchors past is the one-source
        # shape now. Still the slide's own bottom line plus its mark, for the reason above.
        ('is half the headway.</b></p>\n  ' + MARK21 + '\n</section>',
         'is half the headway.</b></p>\n  ' + MARK21 + '\n</div>')]),
    ("sentence-over-twenty-words", "DS-092", [
        # Re-anchored 2026-08-30: T-248 corrected this line, which asserted $5.6M spent plus
        # $1.5M held out of a $5.6M grant. The seeded break is unchanged - a sentence past DS-092's
        # twenty words - and it is still made out of the deck's own claim sentence.
        ("<b>Spend $4.1M of the $5.6M grant on bus frequency,",
         "<b>Spend the whole of the $5.6M state corridor grant on bus frequency across the six "
         "trunk routes, and hold $1.5M back,")]),
    ("icon-nobody-uses", "DS-113", [
        ('<symbol id="i-ask"',
         '<symbol id="i-unused" viewBox="0 0 24 24"><path d="M4 4h16v16H4z"/></symbol>\n '
         '<symbol id="i-ask"')]),
    ("a-third-tier", "DS-160", [
        ('<div class="disc-panel" id="p2" hidden>',
         '<div class="disc-panel" id="p2" hidden><button class="disc-btn" '
         'aria-expanded="false">More still</button>')]),
    ("mark-too-pale-to-clear-the-ground", "DS-219", [
        # **The half the old blanket ban never looked at.** The mark is washed out until it fails
        # 1.4.11 against the paper, and the label is darkened so it still reads perfectly well on
        # it - so DS-215 passes, the slide looks fine in a screenshot, and the chart's bars have
        # stopped being distinguishable from the page. Only DS-219 has anything to say about it.
        ("</nav>\n",
         "</nav>\n<style>svg.fig rect.accent{fill:#EBE7F5}\n"
         "svg.fig text.t-paper{fill:#23211D}</style>\n")]),
    ("slide-with-no-headline", "DS-091", [
        # The class is what carries the rule's subject, so dropping it is how one slide loses its
        # headline without losing its text - which is the shape that used to pass. Until T-053 the
        # word-count check ran over an empty set and reported 0 headlines over six words.
        ('<h2 class="headline rise" style="--i:1">The window shuts in March</h2>',
         '<h2 class="was-headline rise" style="--i:1">The window shuts in March</h2>')]),
    ("chevron-with-no-label", "DS-164", [
        ('<button class="disc-btn" aria-expanded="false" aria-controls="p2">',
         '<button class="disc-btn" aria-expanded="false" aria-controls="p2"><i></i></button>'
         '<button class="disc-btn" aria-expanded="false" hidden aria-controls="p2x">')]),
    ("motion-stop-behind-an-unreachable-opener", "DS-218", [
        # **The seed took `#motion` out of the chrome and shut it in the menu until 2026-08-29.**
        # That was the failing branch DS-218 had then, and the owner's reversal (T-277) made it a
        # PASSING deck - so the variant went on running and stopped catching anything, which is
        # the state L-145 was written about one batch earlier. Re-seeded here against the rule as
        # it now reads.
        #
        # **One attribute moves, and it is the one the new clause names.** DS-218's predicate is
        # `no looping motion OR the control is reachable`, so the lazy seed - drop the deck's
        # `Current` - satisfies the first disjunct and passes, reading as a catch while being the
        # opposite of one (T-051's trap in this rule's shape). So the motion is untouched and the
        # control is neither moved nor deleted: `motionControl` stays True, `infinite` stays 1, and
        # what flips is whether the menu's opener can be reached from the keyboard.
        #
        # `tabindex="-1"` rather than deleting `#moreBtn`, because deleting it also moves
        # `component.py`'s counts and `PR-78`'s preflight crash - and a variant that fails three
        # ways proves nothing about which rule was watching.
        ('<button class="btn" id="moreBtn" aria-expanded="false" '
         'aria-controls="moreMenu">More</button>',
         '<button class="btn" id="moreBtn" aria-expanded="false" '
         'aria-controls="moreMenu" tabindex="-1">More</button>')]),
    # ---- DS-142, both directions (T-214) ------------------------------------------------------
    # **This rule had no seed at all until T-214**, in either direction, so its green on four
    # shipped decks was the absence of a subject rather than a verdict - T-051's reading, and
    # **L-36** and **L-129** at once. The pass direction is `RENDER_PASS_VARIANTS` below.
    #
    # **Every seed here declares `--motion-kind:affordance`, and that is deliberate.** A glow on a
    # headline is not an affordance and the declaration is a false claim - but DS-237 checks that a
    # motion declares a kind, not that the claim is true (DS-243 and DS-150 judge that, and both are
    # `judge`). Declaring `content` instead would gate the seed on `--m-on` and demand an `--m-rank`,
    # so DS-238 and DS-239 would break alongside DS-142 and the seed would prove nothing about any
    # of the three. The smallest edit that breaks one rule is the whole convention of this file.
    ("ambient-glow-on-static-content", "DS-142", [
        # The direction the checker already caught, kept so the fix cannot quietly lose it. A
        # headline is static content by construction: it is the slide's claim, it does not change,
        # and nothing about it is in flight.
        ("</nav>\n",
         "</nav>\n<style>.slide .headline{animation:seedglow 3s ease-in-out infinite;"
         "--motion-kind:affordance;--motion-long:loop}\n"
         "@keyframes seedglow{50%{opacity:.55}}</style>\n")]),
    ("ambient-glow-inheriting-a-live-subject", "DS-142", [
        # **The seed that guards the mechanism rather than the rule.** `--motion-subject` is a
        # custom property, and custom properties inherit - so a glow nested inside an element that
        # declares `live` would read `live` off `getComputedStyle` and be exempted by descent. That
        # turns an allow-list of one class name into an exemption one SUBTREE wide, which is the
        # same defect one shape along and exactly what T-214's scope forbids.
        #
        # `shell/components.css` registers the property `inherits:false` to close it. Delete that
        # registration and this seed stops being caught while every other row stays green, which is
        # what makes it worth a render: the child declares nothing and must be judged on that.
        ("</nav>\n",
         "</nav>\n<style>.seed-live{display:inline-block;width:10px;height:10px;"
         "animation:seedspin 3s linear infinite;"
         "--motion-kind:affordance;--motion-long:loop;--motion-subject:live}\n"
         ".seed-glow{display:inline-block;width:6px;height:6px;"
         "animation:seedglow 3s ease-in-out infinite;--motion-kind:affordance;--motion-long:loop}\n"
         "@keyframes seedspin{to{transform:rotate(360deg)}}\n"
         "@keyframes seedglow{50%{opacity:.55}}</style>\n"),
        (SEED_HEAD, SEED_HEAD + '<span class="seed-live"><i class="seed-glow"></i></span>')]),
]


# **The rendered half's pass direction, which did not exist until T-214.** `run_must_pass` was built
# by T-041 for GF-7 and had exactly one caller; this is the second. The rendered suite could prove
# only that a row FAILS, and DS-142's pass had never been observed on anything but `.current` -
# which is the whole of what T-214 was raised for.
RENDER_PASS_VARIANTS = [
    ("looping-motion-declaring-a-live-subject", "DS-142", [
        # A looping motion that is **not** `.current`, on an element that carries no class the
        # checker has ever heard of, declaring its subject. Before T-214 this failed DS-142 for the
        # only reason that ever mattered: the element was not called `current`.
        ("</nav>\n",
         "</nav>\n<style>.seed-live{display:inline-block;width:10px;height:10px;"
         "animation:seedspin 3s linear infinite;"
         "--motion-kind:affordance;--motion-long:loop;--motion-subject:live}\n"
         "@keyframes seedspin{to{transform:rotate(360deg)}}</style>\n"),
        (SEED_HEAD, SEED_HEAD + '<span class="seed-live"></span>')]),
]


# One render each, with `prefers-reduced-motion` forced. Separate from RENDER_VARIANTS because the
# measurement is a different render, not a different threshold - and because a check nobody has
# watched fail is a claim about the instrument (**L-36**), which is exactly what DS-143 was while
# it sat excused.
REDUCED_VARIANTS = [
    ("reduced-motion-leaves-the-slide-blank", "DS-143", [
        # **The failure the second clause exists to see.** Stopping the animation is not enough:
        # `.rise` holds opacity 0 until it plays, so a deck that only sets `animation:none` shows
        # the reader an empty slide and reports motion dutifully disabled. Same shape as DS-224
        # on paper.
        #
        # **Both paths have to be seeded, and finding that out is what this variant was for.**
        # The deck disables motion twice over: an `@media (prefers-reduced-motion:reduce)` block
        # that applies at parse time, and `:root[data-motion="off"]`, which the script sets from
        # `matchMedia` on load. Seeding only the media query changed nothing measurable - the
        # attribute rules carry higher specificity and put the opacity back. A variant that
        # breaks one of two redundant paths proves the check cannot see the OTHER path.
        # **Both anchors gained `.turn` when T-274 built the card reveal**, and the suite caught
        # it: an anchor is a literal, so a component joining a collapse list moves it. That is the
        # variant working - a seeded defect that stopped matching is a suite reporting on a deck it
        # no longer describes, which is exactly what its own failure message says.
        (":root[data-motion=\"off\"] .opening,\n:root[data-motion=\"off\"] .turn"
         "{animation:none;opacity:1;transform:none}",
         ":root[data-motion=\"off\"] .opening,\n:root[data-motion=\"off\"] .turn"
         "{animation:none}"),
        (".rise,.pulse,.opening,.turn{animation:none;opacity:1;transform:none}",
         ".rise,.pulse,.opening,.turn{animation:none}")]),
    ("reduced-motion-solidifies-the-flow", "DS-143", [
        # The semantics half. The arrows stop moving AND stop being dashed, so the diagram no
        # longer says *flow* - motion removed, and meaning with it.
        # **Anchored on the enclosing selector, so it names which path it seeds** (`PR-57`).
        # `.current{animation:none}` alone occurs twice in the reference deck - under the
        # `[data-motion="off"]` attribute rule and again inside the `prefers-reduced-motion`
        # media query - and the seed silently took the first. That is the path that wins on
        # specificity, so the variant was correct by accident.
        (':root[data-motion="off"] .current{animation:none}',
         ':root[data-motion="off"] .current{animation:none;stroke-dasharray:none}')]),
]


# **The glitch-free half** (T-041). One seed per condition R6 section 8 numbers 2 to 8, and each
# breaks its own condition rather than a `DS-nnn` rule - these are a decomposition of CLAUDE.md
# rule 2, not new design law. Six of the seven need a browser and the seventh would be dishonest
# without one, so they are a fourth suite rather than rows in the static half.
#
# **GF-7's seed is the interesting one.** The unbroken deck returns NO SUBJECT for it, so this is
# the only condition whose variant has to CREATE the subject before it can break it - a blank
# canvas is both. That is R6's reason for the condition in one object: a renderer that silently
# draws nothing passes every other check.
GF_VARIANTS = [
    ("console-throws-on-load", "GF-2", [
        ("</head>", "<script>document.__gfSeed.boom();</script></head>")]),
    ("a-declared-face-never-loads", "GF-3", [
        ("</head>", "<style>@font-face{font-family:'GF3 Seed';"
                    "src:url(data:font/woff2;base64,AAAA) format(\"woff2\")}</style></head>")]),
    ("headings-fall-back-to-georgia", "GF-4", [
        ("</head>", "<style>.slide h1,.slide h2{font-family:Georgia,serif !important}"
                    "</style></head>")]),
    ("a-slide-outgrows-the-stage", "GF-5", [
        ("</head>", "<style>#stage{overflow:hidden}.slide[data-current]{min-height:4000px}"
                    "</style></head>")]),
    # **Upward, and small.** The first seed here moved the slide DOWN 40 px and broke GF-5 as well,
    # on 10 of 13 slides: content pushed below the stage grows `scrollHeight`, and a variant that
    # breaks two conditions proves nothing about either. A negative offset moves every box by more
    # than GF-6's 0.5 px tolerance without adding anything below the fold to scroll to.
    ("layout-moves-after-the-fonts-settle", "GF-6", [
        ("</head>", "<script>document.fonts.ready.then(function(){"
                    "var s=document.querySelector('.slide[data-current]');"
                    "if(s)s.style.transform='translateY(-8px)';});</script></head>")]),
    ("a-canvas-that-draws-nothing", "GF-7", [
        ("</body>", "<canvas id=\"gf7-seed\" width=\"80\" height=\"80\"></canvas></body>")]),
    # **A slide the navigation cannot reach, not a deck that fails to start.** Renaming `id="next"`
    # was the first seed and it broke the deck's own init: GF-8 came back *0 of 13, no slide carries
    # data-current*, GF-2 failed on the resulting throw, and GF-4 and GF-6 lost their subject
    # entirely. That proves the gate notices a broken deck, which was never in question. This one
    # leaves the deck working and adds a fourteenth slide outside the stage, so the walk reaches 13
    # of 14 and nothing else changes.
    ("a-slide-the-walk-cannot-reach", "GF-8", [
        ("</body>", "<section class=\"slide\" data-name=\"orphan\" "
                    "style=\"display:none\"></section></body>")]),
]


# **The other direction, and GF-7 is the only condition that needs it here.** Every variant above
# proves a check can fail. GF-7 is the one whose PASS has never been observed on any deck in this
# repository, because none of the four draws a canvas - so `a-canvas-that-draws-nothing` proves the
# FAIL and nothing at all proved that the pixel scan can see ink. **A check only ever seen to fail
# is L-36 with the sign flipped**, and a scan that returned *blank* for every input would look
# exactly like a working one against a corpus with no canvas in it.
GF_PASS_VARIANTS = [
    ("a-canvas-that-draws", "GF-7", [
        ("</body>", "<canvas id=\"gf7-ink\" width=\"80\" height=\"80\"></canvas>"
                    "<script>var g=document.getElementById('gf7-ink').getContext('2d');"
                    "g.fillStyle='#3b2f7a';g.fillRect(8,8,40,40);</script></body>")]),
]


def build(name, edits):
    html = open(SRC, "r", encoding="utf-8").read()
    for edit in edits:
        # **A third element declares how many occurrences the edit expects. Declared, never
        # defaulted to "all"** - the form `contract_variants.py` and `deliverable_variants.py`
        # have carried since they were written, and the reason they wrote down: a rename that
        # silently hit a different number of elements than the variant's author believed would
        # make the variant test something nobody wrote down. This suite tested `count < 1`
        # instead, so `str.replace(old, new, 1)` decided which of two redundant paths a seeded
        # defect landed in and nothing said so (`PR-57`).
        old, new, want = edit if len(edit) == 3 else (edit[0], edit[1], 1)
        n = html.count(old)
        if n != want:
            sys.exit("VARIANT %s: expected %d occurrence(s), found %d\n  %.140s"
                     % (name, want, n, old))
        html = html.replace(old, new)
    os.makedirs(OUT, exist_ok=True)
    dest = os.path.join(OUT, name + ".html")
    with open(dest, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html)
    return dest


def static_failures(path):
    """The gate's browserless half, run on one seeded deck.

    **Imported, never restated** (T-095). This composed its own copy by naming the producers until
    2026-08-13, and `check.py:gather` composed the same half in its own order from its own list -
    two descriptions of one thing, which is **L-13**'s subject and **L-08**'s. They disagreed the
    first time either changed: T-093 moved DS-005 out of `STATIC` into a producer, `check.py` picked
    it up, and this suite reported `MISSED` for a rule that was being checked. **It was loud by
    luck**, because a seeded variant for DS-005 happened to exist; a producer added for a rule with
    no variant left no trace at all, since the rules it has no variant for are not in its denominator
    either. A gate's static half is whatever `check.py` gathers without a browser, and now that is
    the only place it is written down.
    """
    html = open(path, "r", encoding="utf-8").read()
    rows = check.static_rows(html)
    return {r for r, _w, ok in rows if not ok}, rows


def render_failures(path):
    data, err = render.read_result(
        render.file_url(render.make_probe(path, name="variant.html", extra=audit.PROBE)),
        1622, 1054)
    if not data:
        return None, [("PROBE", (err or "")[:120], False)]
    rows = audit.render_verdicts(data)
    # `is False`: a row reporting `None` decided nothing, and counting that as a catch would let a
    # variant look caught because the seed removed the rule's subject rather than broke it (T-051).
    return {r for r, _w, ok in rows if ok is False}, rows


def glitchfree_failures(path):
    """The same shape as `render_failures`, from the glitch-free walk (T-041).

    **A fourth collector rather than a fourth entry in the third.** `render_failures` reaches
    `audit.render_verdicts` and nothing else, so a variant seeded against `GF-n` run through it
    would come back MISSED for a condition that is checked - which is exactly the drift T-093
    caused and T-095 closed one level up.
    """
    rows = glitchfree.verdicts(path)
    # `is False`, for `render_failures`' reason: a row reporting `None` decided nothing, and
    # counting that as a catch would let a variant look caught because the seed removed the
    # condition's subject rather than broke it (T-051).
    return {r for r, _w, ok in rows if ok is False}, rows


def reduced_failures(path):
    """The same shape as `render_failures`, from the reduced-motion render."""
    data, err = audit.reduced_motion_data(path)
    if not data:
        return None, [("PROBE", (err or "")[:120], False)]
    rows = audit.reduced_verdicts(data)
    return {r for r, _w, ok in rows if ok is False}, rows


def self_test():
    """The suite must be able to tell a broken deck from a good one (**L-04**), and the baseline
    must be green or a caught variant proves nothing."""
    if not os.path.exists(SRC):
        sys.exit("SELF-TEST FAILED: no reference deck at %s" % SRC)
    src = open(SRC, "r", encoding="utf-8").read()
    for name, _rule, edits in (STATIC_VARIANTS + RENDER_VARIANTS + REDUCED_VARIANTS
                              + GF_VARIANTS + GF_PASS_VARIANTS):
        for edit in edits:
            # The same exact-count test `build` applies, so the suite refuses at self-test
            # time rather than seeding one of several redundant paths (`PR-57`).
            old, want = edit[0], (edit[2] if len(edit) == 3 else 1)
            if src.count(old) != want:
                sys.exit("SELF-TEST FAILED: variant %r no longer matches the deck.\n"
                         "  The deck changed under the suite; fix the variant, do not delete it.\n"
                         "  wanted %d occurrence(s), found %d\n  %.160s"
                         % (name, want, src.count(old), old))
    base, _rows = static_failures(SRC)
    if base:
        sys.exit("SELF-TEST FAILED: the UNBROKEN deck already fails %s - a seeded break cannot be "
                 "shown caught against a red baseline" % sorted(base))

    # **Every verdict producer is inside this suite or declared outside it with a reason.** Importing
    # the composition stops the two halves drifting; it does not notice a producer that joined the
    # gate and reached neither half. Run here as well as in `check.py` because this is the suite the
    # answer is about, and a run of it must not depend on somebody having run the other.
    check.producer_split()
    return True


def run_must_pass(variants, failures_of, label):
    """The mirror of `run`: a seeded SUBJECT the check has to accept.

    **`True`, not merely *not caught*.** NO SUBJECT is also not caught, and it is what the unbroken
    deck already reports for GF-7 - so an assertion phrased as absence from the failure set would be
    satisfied by the seed never being seen at all, which is the thing being tested.
    """
    bad = []
    for name, rule, edits in variants:
        deck = build(name, edits)
        _caught, rows = failures_of(deck)
        got = [ok for r, _w, ok in (rows or []) if r == rule]
        good = got == [True]
        if not good:
            bad.append((name, rule, got))
        print("  %-28s must pass %-7s -> %s" % (name, rule, "PASSED" if good else "DID NOT"))
        for r, what, ok in (rows or []):
            if r == rule or ok is False:
                print("      %-8s %-58s %s"
                      % (r, what[:58], "NO SUBJECT" if ok is None else "pass" if ok else "FAIL"))
    print("  %d of %d %s variants passed.\n" % (len(variants) - len(bad), len(variants), label))
    return bad


def run(variants, failures_of, label):
    bad = []
    for name, rule, edits in variants:
        deck = build(name, edits)
        caught, rows = failures_of(deck)
        good = caught is not None and rule in caught
        if not good:
            bad.append((name, rule, caught))
        print("  %-28s breaks %-7s -> %s" % (name, rule, "CAUGHT" if good else "MISSED"))
        for r, what, ok in rows:
            if ok is not True:
                print("      %-8s %-58s %s"
                      % (r, what[:58], "NO SUBJECT" if ok is None else "FAIL"))
    print("  %d of %d %s variants caught.\n" % (len(variants) - len(bad), len(variants), label))
    return bad


def main(argv):
    self_test()
    print("source:  %s\n" % paths.display_path(SRC, ROOT))
    print("=== static (no browser)")
    # **What the denominator is over.** *n of n caught* says nothing until a reader can see which
    # producers were run: the count is over the variants, and a rule with no variant is absent from
    # numerator and denominator alike. Printing the producers is what makes the gap visible instead
    # of arithmetically invisible.
    static, elsewhere = check.producer_split()
    print("  producers run:  %s" % ", ".join(static))
    print("  outside this half, with a reason in check.NOT_STATIC:\n    %s\n"
          % "\n    ".join(elsewhere))
    bad = run(STATIC_VARIANTS, static_failures, "static")
    if "--static-only" not in argv:
        render.self_test()
        print("=== rendered (one real Chrome render each)")
        bad += run(RENDER_VARIANTS, render_failures, "rendered")
        print("=== rendered, the pass direction")
        bad += run_must_pass(RENDER_PASS_VARIANTS, render_failures, "rendered pass")
        print("=== rendered with prefers-reduced-motion forced")
        bad += run(REDUCED_VARIANTS, reduced_failures, "reduced-motion")
        # T-041. Last because it is the most expensive half - each variant walks every slide.
        print("=== glitch-free (R6 section 8, conditions 2 to 8)")
        bad += run(GF_VARIANTS, glitchfree_failures, "glitch-free")
        print("=== glitch-free, the pass direction")
        bad += run_must_pass(GF_PASS_VARIANTS, glitchfree_failures, "glitch-free pass")
    if bad:
        print("MISSED - the gate does not check what it says it checks:")
        for name, rule, caught in bad:
            print("  %-28s %s not among %s" % (name, rule, sorted(caught or [])))
        return 1
    print("Variants are written to %s and are not committed - the suite regenerates them."
          % paths.display_path(OUT, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
