#!/usr/bin/env python3
"""Run the mechanical half of `docs/EVALUATION.md`'s pipeline over a deck.

Stage 1 is the **auto gate** — static analysis of the file. Stage 2 is the part of the **render
gate** a measurement can answer: the design-unit floor, continuous motion, the reflow view, tab
order, target size, and the 320 CSS px reflow requirement.

**This is necessary and nowhere near sufficient, and it says so.** Validating the rubric against a
seeded-defect deck showed that **five of the ten evaluation dimensions are invisible to any static
or measured check** — S1 Claim, S2 Evidence, S4 Density, D1 Spine and D4 Consistency are judgement,
and a pipeline stopping here ships a deck whose headline is a topic label and whose figures
contradict each other (**L-05**, DS-190, DS-191).

    python tools/deck/audit.py examples/reference-deck.html

Pure standard library (**L-07**), real Chrome offline via `render.py`.
"""

import json
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths                                                        # noqa: E402
import render                                                       # noqa: E402
import contrast                                                     # noqa: E402
import contract                                                     # noqa: E402
import theme                                                        # noqa: E402
import content                                                      # noqa: E402
# Imported for the absent-subject fixture, which holds every verdict producer in `tools/deck/` to
# the same bar since T-075 - not for anything this module's own rows measure.
import component                                                    # noqa: E402
import printgeom                                                    # noqa: E402
import figgrid                                                      # noqa: E402
import markhits                                                     # noqa: E402
import density                                                      # noqa: E402
import printpages                                                   # noqa: E402
import spec                                                         # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = render.ROOT

# ---------------------------------------------------------------------------- static helpers
# Named rather than inlined, because each one is a claim about what a rule means and the claim
# needs somewhere to be argued. T-038's discriminator governs all of them: the thing measured is
# the thing cited, or the check does not ship and the rule is excused in writing instead.

STYLE = re.compile(r"<style[^>]*>(.*?)</style>", re.S)
HEXLIT = re.compile(r"#[0-9A-Fa-f]{3}(?:[0-9A-Fa-f]{3}(?:[0-9A-Fa-f]{2})?)?\b")
FUNCLIT = re.compile(r"\b(?:rgb|rgba|hsl|hsla|oklch|color)\s*\(")


def css(h):
    """Every `<style>` block joined, with embedded font payloads removed.

    **The payloads have to go before anything scans this.** A base64 woff2 is a 100 KB run of
    random-looking characters, and `\\d+s` matches inside it: the first version of the DS-141
    duration check reported six animations over 500 ms, all of them fragments of a typeface."""
    return re.sub(r"url\(\s*data:[^)]*\)", "url(data:)", "\n".join(STYLE.findall(h)), flags=re.S)


def screen_css(h):
    """The CSS that governs the screen. `@media print` is a different medium with no theme and a
    paper ground, so the rules about theming and about stage units do not reach into it - DS-226
    requires a floor in POINTS there, which the stage's own rules forbid."""
    return re.split(r"@media\s+print\s*\{", css(h))[0]


def blocks(text, selector):
    """The bodies of every rule whose selector matches, non-nested. Custom-property blocks and
    component rules do not nest braces, so a non-greedy match is right here and a brace counter
    would only add a way to be wrong."""
    return re.findall(selector + r"\s*\{(.*?)\}", text, re.S)


def token_layer(h):
    """The theme's own declarations: `:root` plus the dark override. DS-010's *token layer*."""
    c = css(h)
    return "\n".join(blocks(c, r":root(?:\s*\[[^\]]*\])?"))


def outside_token_layer(h):
    """Screen CSS with the token layer removed, so a colour literal found here is one DS-010
    forbids. Print is excluded with the rest of `@media print`: `background:#fff` on paper is not
    a theme value that could differ between themes, it is the paper.

    **The degraded state goes with it, for the same shape of reason one storey down.** DS-009's
    block renders when a capability is missing and CSS custom properties are one of the
    capabilities it names, so a token there resolves to nothing in the one case the block exists
    for - `#f6f1e4` is not a theme value that could differ, it is the last legible thing a browser
    that lost the theme can still paint. Written in the same words in `THEME-CONTRACT.md` §5,
    which exempts the length half.
    """
    c = DEGRADED.sub("", screen_css(h))
    for body in blocks(c, r":root(?:\s*\[[^\]]*\])?"):
        c = c.replace(body, "")
    return re.sub(r"/\*.*?\*/", "", c, flags=re.S)


# Every rule scoped to the degraded state, matched on the marker rather than on a comment: a
# comment is stripped before this runs and would make the exemption depend on prose.
DEGRADED = re.compile(r"[^{}]*\[data-preflight\][^{}]*\{[^{}]*\}")


def ds010_colours_tokenised(h):
    """DS-010 - a value that could differ between themes is a custom property. Colour is the
    class of value that always could, and a literal outside the token layer is the observable
    form of the defect. `currentColor`, `transparent` and `none` are not literals in this sense.

    **The rule's full subject is wider than colour** - any theme-varying value - and deciding
    *which* values could differ needs the parametric layer T-007 owns. This check is the colour
    half, which is the half that has ever gone wrong."""
    out = outside_token_layer(h)
    return not HEXLIT.search(out) and not FUNCLIT.search(out)


def ds011_one_palette(h):
    """DS-011 - one fully-resolved theme, never a palette per topic. Observable: exactly one
    `:root` palette declaration and at most one theme override of it."""
    c = css(h)
    roots = re.findall(r":root(?:\s*\[[^\]]*\])?\s*\{", c)
    palettes = [b for b in blocks(c, r":root(?:\s*\[[^\]]*\])?")
                if HEXLIT.search(b) or FUNCLIT.search(b)]
    return len(roots) <= 3 and len(palettes) <= 2


def ds012_dark_is_overrides(h):
    """DS-012 - dark mode is one block of custom-property overrides, never a redesign. So the
    dark block declares custom properties and nothing else: a `display`, a `margin` or a
    `grid-template` in there is the redesign the rule forbids."""
    dark = blocks(css(h), r':root\s*\[data-theme\s*=\s*"dark"\]')
    if not dark:
        return True                    # a deck with no dark theme has nothing to redesign
    body = re.sub(r"/\*.*?\*/", "", "\n".join(dark), flags=re.S)
    decls = [d.strip() for d in body.split(";") if d.strip()]
    return all(d.startswith("--") for d in decls)


def _hue(hexstr):
    h = hexstr.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) < 6:
        return None
    r, g, b = (int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    mx, mn = max(r, g, b), min(r, g, b)
    if mx - mn < 0.04:
        return None                    # a neutral has no hue to compare
    if mx == r:
        deg = 60 * (((g - b) / (mx - mn)) % 6)
    elif mx == g:
        deg = 60 * (((b - r) / (mx - mn)) + 2)
    else:
        deg = 60 * (((r - g) / (mx - mn)) + 4)
    return deg


def _hue_gap(a, b):
    d = abs(a - b) % 360
    return min(d, 360 - d)


def ds020_one_accent(h):
    """DS-020 - neutral ground plus **exactly one** accent.

    Counted as hue families, not as tokens: an accent wash and an accent ink are shades of one
    accent, and the rule is about the accent rather than about how many variables carry it. The
    three semantic roles are a separate vocabulary DS-026 fixes deck-wide, and are excluded by
    name.

    **The ground is what defines *neutral*, and it is not achromatic here.** DS-023 requires a
    warm paper ground and warm-charcoal ink, so the neutrals carry a real hue - measured on this
    deck, 38 to 46 degrees. Saturation was tried as the discriminator first and the margin was
    thin enough to be luck: the darkest neutral sits at 0.21 against the accent's 0.31. Grouping
    by distance from the ground's own hue has no such constant in it."""
    toks = dict(re.findall(r"--([a-z0-9-]+)\s*:\s*(#[0-9A-Fa-f]{3,8})\s*;", token_layer(h)))
    roles = ("pos", "neg", "caution")
    ground = None
    for name in ("paper", "bg", "ink"):
        if name in toks:
            ground = _hue(toks[name])
            if ground is not None:
                break
    families = []
    for name, value in sorted(toks.items()):
        if name.startswith(roles):
            continue
        d = _hue(value)
        if d is None:
            continue                             # achromatic: part of the ground by definition
        if ground is not None and _hue_gap(d, ground) <= 30:
            continue                             # the neutral family
        if not any(_hue_gap(d, f) <= 30 for f in families):
            families.append(d)
    return len(families) == 1


def ds023_no_pure_black_or_white(h):
    toks = re.findall(r"--[a-z0-9-]+\s*:\s*(#[0-9A-Fa-f]{3,8})\s*;", token_layer(h))
    bad = {"#fff", "#ffffff", "#000", "#000000"}
    return not [t for t in toks if t.lower() in bad]


def ds024_light_by_default(h):
    """DS-024 - light by default. The default is what `:root` declares; dark is the override, so
    the unqualified block must be the lighter of the two."""
    plain = blocks(css(h), r":root")
    dark = blocks(css(h), r':root\s*\[data-theme\s*=\s*"dark"\]')
    if not plain or not dark:
        return bool(plain)
    def lum(block):
        m = re.search(r"--paper\s*:\s*(#[0-9A-Fa-f]{3,8})|--bg\s*:\s*(#[0-9A-Fa-f]{3,8})", block)
        if not m:
            return None
        v = (m.group(1) or m.group(2)).lstrip("#")
        if len(v) == 3:
            v = "".join(c * 2 for c in v)
        return sum(int(v[i:i + 2], 16) for i in (0, 2, 4))
    a, b = lum(plain[0]), lum(dark[0])
    return a is not None and b is not None and a > b


def ds034_body_type(h):
    """DS-034 as amended by T-007 - body 24-28 design units at line-height 1.40-1.70.

    **The value is resolved, not pattern-matched.** The old check read
    `--fs-body:calc(N*var(--du))` with a regex and pinned the line height to 1.55 +/- 0.01, which
    was fine while there was one hand-built theme and wrong the moment `--fs-body` derived from a
    dial: a conforming deck failed because its body size was `calc(var(--fs-base)*var(--du))`.
    A rule about a NUMBER has to read the number, whatever expression carries it.
    """
    c = css(h)
    decls = theme.declarations(c)
    size = theme.number(decls.get("--fs-body", ""), decls)
    lh = theme.number(decls.get("--lh-body", ""), decls)
    return (size is not None and 24 <= size <= 28
            and lh is not None and 1.40 - 1e-9 <= lh <= 1.70 + 1e-9)


def ds006_module_specifiers(h):
    """DS-006 - a relative specifier cannot resolve from a `blob:` base, so an inline module may
    not carry one. Vacuously true in a deck with no modules, which is the common case and is
    reported as such rather than as a pass over nothing."""
    mods = re.findall(r'<script\b[^>]*type=["\']module["\'][^>]*>(.*?)</script>', h, re.S)
    for body in mods:
        for spec in re.findall(r'\b(?:from|import)\s+["\']([^"\']+)["\']', body):
            if not spec.startswith(("data:", "blob:")):
                return False
    return True


def ds044_headings_reset(h):
    """DS-044 - reset every heading level, `h4` and `h5` included; a partial reset is worse than
    none. Checked against the levels the deck actually uses: a reset for `h6` in a deck with no
    `h6` proves nothing, and a missing one for a level in use is the defect."""
    used = set(re.findall(r"<(h[1-6])\b", h))
    c = css(h)
    reset = set()
    for sel in re.findall(r"([^{}]+)\{", c):
        for lvl in re.findall(r"\bh[1-6]\b", sel):
            reset.add(lvl)
    return used.issubset(reset)


def ds045_no_bare_b(h):
    """DS-045 as clarified 2026-08-09 - never style the bare `b` ELEMENT SELECTOR.

    The banned shape is a selector whose rightmost compound is `b` and which carries no class, id
    or attribute anywhere: `b`, `p b`, `section b`. Those reach every `<b>` in the deck, so one
    component's look becomes a default nothing declared.

    `.bottom-line b` is allowed and is how the deliverable is set - the scope is precisely what
    stops the leak. The wide reading was tried first, failed the reference deck four times over a
    pattern twelve slides use, and lost to the harm the rule actually describes.
    """
    for sel in re.findall(r"([^{}]+)\{", css(h)):
        if "@" in sel:
            continue                             # an at-rule prelude, not a selector list
        for part in sel.split(","):
            part = part.strip()
            if not part or not re.search(r"(^|\s)b$", part):
                continue
            if re.search(r"[.#\[:]", part):
                continue                         # scoped by a class, id, attribute or pseudo
            return False
    return True


NON_TRANSFORM_UNITS = re.compile(r"[:\s(]\d[\d.]*(vw|vh|vmin|vmax|pt|cm|in|mm|pc)\b")


def ds065_units_ride_the_transform(h):
    """DS-065 as reworded by T-021 - no element positioned in a unit resolved against the
    VIEWPORT or the physical page rather than the design space. Print CSS is exempt by
    construction: DS-226 requires a floor in points, so `pt` inside an `@media print` block is
    the ruleset asking for it.

    This is the check `contract.py`'s tail said could not be built. It could not be built against
    the rule's OLD wording, which named a distinction that does not exist inside the stage; T-021
    reworded the rule and the check has been owed since."""
    return not NON_TRANSFORM_UNITS.search(screen_css(h))


def ds028_no_full_page_gradient(h):
    """DS-028 - no full-page gradients, no gradient blobs. The mechanical half is the ground:
    a gradient on `html`, `body`, the stage or a slide's own background."""
    for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css(h)):
        if "gradient(" not in body:
            continue
        s = sel.strip()
        if re.search(r"(^|,)\s*(html|body|\.stage|#stage|\.slide)\s*(,|$)", s):
            return False
    return True


def ds037_display_headings_balanced(h):
    return "text-wrap:balance" in css(h).replace(" ", "") or \
           "text-wrap: balance" in css(h)


def ds040_grid_and_flex(h):
    c = css(h).replace(" ", "")
    return "display:grid" in c and "display:flex" in c


def ds111_figures_are_drawn(h):
    """DS-111 - diagrams are inline SVG, with `<canvas>` and WebGL where they render better. The
    checkable content is what a figure is MADE OF: an embedded object is neither, and no deck may
    ship one. T-038 removed the previous verdict here, which passed on `svg.fig` count > 0 and so
    failed an all-canvas deck the rule permits."""
    return not re.search(r"<(object|embed|iframe)\b", h, re.I)


def ds118_svg_colour_from_css(h):
    """DS-118 - every SVG is theme-aware; no hard-coded fill or stroke. A literal colour in a
    presentation attribute is the hard-coding. `none`, `currentColor` and a `url(#...)` paint
    server are not colours in this sense, and `var(...)` is the tokenised form the rule wants -
    DS-214 is what catches a `var()` attribute that CSS then overrides."""
    for m in re.finditer(r'\b(?:fill|stroke)="([^"]+)"', h):
        v = m.group(1).strip()
        if v.startswith(("var(", "url(", "#")) and not HEXLIT.fullmatch(v):
            continue
        if v.lower() in ("none", "currentcolor", "transparent", "inherit"):
            continue
        return False
    return True


def ds119_canvas_dimensions(h):
    for tag in re.findall(r"<canvas\b([^>]*)>", h, re.I):
        if not (re.search(r'\bwidth="\d+"', tag) and re.search(r'\bheight="\d+"', tag)):
            return False
    return True


# DS-141's licence to exceed the 500 ms cap, **declared on the rule that starts the motion**.
#
# The history is worth keeping, because each version failed differently. Until T-007 the licence was
# a pair of exact seconds, 1.2 and 4.5, and the check admitted any duration matching one of them;
# banding those numbers broke it in a way the variant suite caught immediately, since a 900 ms slide
# transition falls inside Pulse-once's 0.8-1.6 s band and a scan over durations cannot tell which
# motion a number belongs to. T-007 replaced the numbers with the two token NAMES that carry them,
# which worked only for as long as DS-140 fixed the vocabulary at four.
#
# **T-187 opened DS-140, so the name stopped being a test.** A licence that reads `--pulse-dur` says
# nothing about a motion nobody has named. So the licence is now declared - `--motion-long`, on the
# rule itself, carrying WHY - and this check reads that the declaration is there. Whether the reason
# is TRUE is DS-243's business and a reader's; that split is the same one DS-237 makes with
# `--motion-kind` and DS-230 with `data-disc`.
DS141_REASONS = ("loop", "illustration", "emphasis", "request")
MOTION_LONG = re.compile(r"--motion-long\s*:\s*(?:%s)\b" % "|".join(DS141_REASONS))


def _custom_properties(c):
    return dict(re.findall(r"--([a-z0-9-]+)\s*:\s*([^;{}]+);", c))


def _expand_vars(value, toks, depth=4):
    """Resolve `var(--x)` from the deck's own token declarations.

    **Without this the check reads nothing**, and the variant suite is how that was found: DS-033
    requires every value inside the stage to come from a token, so a duration is written
    `transition: transform var(--slide-dur)` and the number lives one indirection away. Seeding
    `--slide-dur:900ms` broke DS-141 and the check saw only `var(--slide-dur)` and passed."""
    for _ in range(depth):
        if "var(" not in value:
            break
        value = re.sub(r"var\(\s*--([a-z0-9-]+)[^)]*\)",
                       lambda m: toks.get(m.group(1), ""), value)
    return value


def ds141_durations(h):
    """DS-141 - entry and transition animations max 500 ms, and a motion running longer declares
    `--motion-long` on the rule that starts it. So: every duration over the cap sits in a rule
    carrying the licence, which is what the rule's own sentence now grants.

    **Read per rule, not over the file.** The licence is a sibling declaration, so the block is the
    unit; scanning declaration values flat cannot see what else the rule said. `density.CSS_RULE`
    is the same parser DS-237 and DS-238 read `--motion-kind` with - one shape for one job.

    **Only duration-bearing declarations are read.** `animation-delay:600ms` is not a duration and
    scanning the file for `\\d+s` counted one, alongside six fragments of an embedded typeface."""
    c = css(h)
    toks = _custom_properties(c)
    for rule in density.CSS_RULE.finditer(c):
        body = rule.group(2)
        if MOTION_LONG.search(body):
            continue                     # licensed, and DS-243 judges whether the reason is true
        for value in re.findall(r"\b(?:animation|transition)(?:-duration)?\s*:\s*([^;{}]+)", body):
            for m in re.finditer(r"(\d+(?:\.\d+)?)(ms|s)\b", _expand_vars(value, toks)):
                if float(m.group(1)) / (1000.0 if m.group(2) == "ms" else 1.0) > 0.5:
                    return False
    return True


def _naming(items, keep=3):
    """` - a, b, c and 4 more`, or nothing at all when there is nothing to name.

    **A failing row names what failed** (T-193). Several rows here reported a *count* while the
    probe that produced it still held the subjects - `DS-113` printed `len(unusedSymbols)` with the
    ids in hand - so an author was told two icons were dead and not which two, and the only way on
    was to read this file. The first outside build did exactly that, seven times.

    Bounded on purpose: a row listing forty elements is a different failure of the same kind.
    """
    items = list(items or [])
    if not items:
        return ""
    shown = ", ".join(_name_of(i) for i in items[:keep])
    return " - %s%s" % (shown, " and %d more" % (len(items) - keep) if len(items) > keep else "")


def _name_of(item):
    """The identifying part of one measured item, whatever shape the probe emitted it in.

    The probe returns a bare string for some rows, a `[name, ...]` pair for others and a dict for
    the newest. A row should not have to know which - what an author needs is the same thing in
    every case, which is the name they can go and look at.
    """
    if isinstance(item, dict):
        for key in ("sel", "name", "slide", "id"):
            if item.get(key):
                return str(item[key])
        return str(sorted(item.items())[:1])
    if isinstance(item, (list, tuple)) and item:
        return str(item[0])
    return str(item)


def _widest(rows, keep=3):
    """` - widest: div.x 859px, table 604px`, for DS-075's offenders."""
    rows = list(rows or [])
    if not rows:
        return ""
    return " - widest: " + ", ".join("%s %dpx" % (r.get("sel", "?"), r.get("w", 0))
                                     for r in rows[:keep])


BAND_TOKEN = re.compile(r"var\(\s*--(?:afford|press)-(?:dur|ease)\s*\)")
TRANSFORM_DECL = re.compile(r"[;{]\s*transform\s*:")


def _specificity(sel):
    """`(ids, classes, types)` for the simple selectors this ruleset writes.

    A pseudo-element is stripped first, so `::before` cannot be read as a pseudo-*class*; what is
    left counts classes, attribute selectors and pseudo-classes together, which is what CSS does.
    """
    s = re.sub(r"::[a-zA-Z-]+", " ", sel.strip())
    ids = len(re.findall(r"#[\w-]+", s))
    cls = (len(re.findall(r"\.[\w-]+", s))
           + len(re.findall(r"\[[^\]]*\]", s))
           + len(re.findall(r":[a-zA-Z-]+(?:\([^)]*\))?", s)))
    rest = re.sub(r"[#.][\w-]+|\[[^\]]*\]|:[a-zA-Z-]+(?:\([^)]*\))?", " ", s)
    return (ids, cls, len(re.findall(r"[a-zA-Z][\w-]*", rest)))


def _rules(h):
    """`[(selector, body)]` for the deck's CSS, **with comments removed first**.

    `re.findall(r"([^{}]+)\\{([^{}]*)\\}", css(h))` is the house pattern and it reads everything
    between the previous `}` and the next `{` as the selector - which includes any comment written
    above the rule. This ruleset comments almost every rule, so a test like `selector.endswith(
    ":active")` silently matches nothing. Found 2026-08-20 by seeding T-199's defect back into the
    reference deck and watching DS-240 report it clean.
    """
    return re.findall(r"([^{}]+)\{([^{}]*)\}", re.sub(r"/\*.*?\*/", " ", css(h), flags=re.S))


def _compound(base):
    """The simple selectors of one compound as a set, or None where a combinator makes it two.

    `.btn.btn--pager` -> `{'.btn', '.btn--pager'}`. A base carrying a descendant, child or sibling
    combinator describes a relationship between two elements and is not something this compares.
    """
    base = base.strip()
    if not base or re.search(r"[\s>+~]", base):
        return None
    return frozenset(re.findall(r"\[[^\]]*\]|[#.][\w-]+|[a-zA-Z][\w-]*", base))


def ds240_band_is_closed(h):
    """DS-240 - `--afford-*` and `--press-*` appear only inside a rule declaring `affordance`.

    The short band exists because a control answers the hand faster than the argument moves. If a
    content motion may reach for it, it is not a band for controls - it is a way around DS-141's
    cap, and the rule that admits the exception is the rule that repeals the cap.
    """
    for _sel, body in _rules(h):
        if BAND_TOKEN.search(body) and "--motion-kind:affordance" not in body.replace(" ", ""):
            return False
    return True


def ds240_press_beats_hover(h):
    """DS-240 - where one element has both, the `:active` transform outranks the `:hover` one.

    **This is the check for a defect no render can see** (T-185, T-199). A press happens while the
    pointer is hovering, so both rules match and the cascade decides. The pager's back button
    carried `.btn.btn--pager.is-back:hover` at three classes against `.btn.btn--pager:active` at
    two, so it drew its lean and never its pinch - on every deck ever shipped here, with both
    declarations present and a screenshot unable to tell. The cascade is computable from the
    stylesheet, which is why this is `auto` rather than a look.

    Scoped to a selector **ending** in the pseudo-class: `.a:hover .b` is one element reacting to
    another and is not this rule's subject.

    **Matching bases by string is what the first draft of this check did, and it reported the very
    defect it was written for as clean.** The two rules do not share a base: the hover is
    `.btn.btn--pager.is-back` and the press is `.btn.btn--pager`, which is a *superset* relation
    rather than equality - the press rule matches the element the hover rule matches, with fewer
    classes and therefore less weight, which is the whole mechanism of the fault. So a press is a
    candidate for a hover when its compound is a **subset** of the hover's.
    """
    hovers, actives = [], []
    for i, (sel, body) in enumerate(_rules(h)):
        if not TRANSFORM_DECL.search(";" + body):
            continue
        for one in sel.split(","):
            one = one.strip()
            for pseudo, bucket in ((":hover", hovers), (":active", actives)):
                if not one.endswith(pseudo):
                    continue
                compound = _compound(one[:-len(pseudo)])
                if compound is not None:
                    bucket.append((compound, (_specificity(one), i)))
    for compound, hover_key in hovers:
        press = [k for c, k in actives if c <= compound]
        if press and max(press) < hover_key:
            return False
    return True


EYEBROW = re.compile(r'<p[^>]*\bclass="[^"]*\beyebrow\b[^"]*"[^>]*>(.*?)</p>', re.S | re.I)
TICK_SPAN = re.compile(r'<span[^>]*\bclass="[^"]*\btick\b[^"]*"[^>]*>.*?</span>', re.S | re.I)
HEADLINE_EL = re.compile(r'<h2[^>]*\bclass="[^"]*\bheadline\b[^"]*"[^>]*>(.*?)</h2>', re.S | re.I)
STAGES_VAR = re.compile(r"var\s+STAGES\s*=\s*\[(.*?)\]", re.S)
STARTS_WITH_POSITION = re.compile(r"^\d+\s*[·–—\-.|/:]")


def _stage_names(h):
    m = STAGES_VAR.search(h)
    if not m:
        return set()
    return set(x.strip("'\" ").lower() for x in re.findall(r"'[^']*'|\"[^\"]*\"", m.group(1)))


def _flat(fragment):
    """The fragment's text, **with HTML entities decoded** before anything reads it.

    **`&middot;` is how a build writes the separator, and it walked straight through DS-241 on the
    first day the rule shipped.** `runs()` decodes `&nbsp;` and `&amp;` and nothing else, so an
    eyebrow reading `07 &middot; Structure` arrived here as that literal string - and
    `STARTS_WITH_POSITION`, which looks for a digit then a separator, saw a digit then an
    ampersand and passed it. The deck the rule was written from is written that way, so the check
    missed the one deck it existed to catch. Found by rendering the slide and reading it (rule 6)
    after the gate had already said the deck was clean.
    """
    return " ".join(content.runs(html.unescape(fragment))).strip()


def _norm_words(text):
    return set(w for w in re.findall(r"[a-z0-9]+", text.lower()) if len(w) > 2)


def ds241_eyebrow_offenders(h):
    """`[slide-name]` for every eyebrow that does not name its slide's subject.

    **The eyebrow is the one place a presenter can learn what is on screen before speaking**, and
    two of the three decks shipped here spent it on `02 · Why now` - the position, which the ruler
    prints, beside the stage, which the ruler also prints. So the most prominent line after the
    headline said nothing that was not already on the screen twice, and a presenter had to read the
    whole slide to find out what it was about. Reported by the owner 2026-08-20 against a deck where
    a RACI chart and an AI policy were distinguishable only by reading them (T-197).

    Three mechanical failures, and the positive half - *is that the right name* - is a reading this
    cannot make and DS-241 hands to the critique pass.
    """
    stages = _stage_names(h)
    bad = []
    for m in SLIDE_BLOCK.finditer(content.strip_comments(h)):
        block, inner = m.group(0), m.group(1)
        name = re.search(r'data-name="([^"]*)"', block)
        name = name.group(1) if name else "?"
        em = EYEBROW.search(inner)
        if not em:
            continue                      # the part's presence is DS-229's, not this rule's
        text = _flat(TICK_SPAN.sub(" ", em.group(1)))
        head = HEADLINE_EL.search(inner)
        head = _flat(head.group(1)) if head else ""
        if (not text
                or STARTS_WITH_POSITION.match(text)
                or text.lower() in stages
                or (head and _norm_words(text) and _norm_words(text) <= _norm_words(head))):
            bad.append(name)
    return bad


def ds144_no_3d_between_slides(h):
    """DS-144 - no 3D transitions between slides. The 3D reveal of a card is permitted, so the
    check is scoped to rules that target a slide rather than to the file."""
    for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css(h)):
        if not re.search(r"rotateX|rotateY|rotate3d|translateZ|perspective", body):
            continue
        if re.search(r"\.slide\b", sel) and ".card" not in sel:
            return False
    return True


def ds163_no_hover_only(h):
    """DS-163 - never hover-only. A `:hover` rule that changes `display` or `visibility` is
    revealing content on hover; colour, border and transform changes are supplementary and are
    what the rule's *tooltips may supplement* clause allows."""
    for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css(h)):
        if ":hover" not in sel:
            continue
        if re.search(r"\b(display|visibility)\s*:", body):
            return False
    return True


def ds165_one_disclosure_mark(h):
    """DS-165 - the disclosure mark is a tokenised element of the theme, not a per-slide
    invention. Observable: no rule scoped to one slide restyles it."""
    for sel in re.findall(r"([^{}]+)\{", css(h)):
        if "disc-mark" not in sel:
            continue
        if re.search(r'\[data-name|\.slide-\d|#s\d', sel):
            return False
    return True


# ---------------------------------------------------------------------------- stage 1: static
# Each entry is (rule id, what it asserts, predicate). Only rules a file scan can actually
# decide - anything needing a render lives in stage 2, anything needing judgement is not here.
def ds001_no_external_references(h):
    """DS-001's sweep, with the provenance mark cut out of it first.

    **The rule enumerates what it means: every font, icon, script and style inlined.** Those are
    subresources - things the renderer fetches to draw the page - and this predicate swept every
    `href` in the file, so it also caught an `<a>`, which the renderer never fetches. That gap was
    load-bearing until 2026-08-10: DS-105 permits a source link where the sources are reachable, and
    the gate's own account excused the dead-link half on the ground that *DS-001 had banned links*.
    It had not; this check had, and only by reading wider than the rule it implements (T-069).

    **Cut narrowly, and the narrowness is the point.** Only `.sources-link` anchors are exempt,
    because that is the one class another rule takes over: DS-105 judges those, and
    `provenance_verdicts` fails a dead one. An `<a href>` anywhere else in a deck still fails here,
    so nothing has been let through - the exemption goes exactly as far as the rule that covers it.
    **It cuts by class rather than by place since T-109**, when the component gained a second home:
    the colophon's rows are the same component in `.body`, and a cut scoped to `<p class=
    "provenance">` failed an external URL DS-105 admits, on a fixture built to carry one.
    """
    swept = h
    for tag in source_link_tags(h):
        swept = swept.replace(tag, "<a>")
    return not [u for u in re.findall(
        r'(?:src|href|xlink:href)\s*=\s*["\']([^"\']+)["\']', swept)
        if not u.startswith(("data:", "#", "blob:"))]


# **The quick view is where a quoted source lives, and the only place DS-110 lets a raster be**
# (T-070). The cut itself moved to `content.py` when T-167 gave it a second caller there - one
# definition, in the module this one already imports. The reasoning travels with it.
QUICK_VIEW = content.QUICK_VIEW


def ds110_no_produced_raster(h):
    """DS-110 as narrowed by scope. A quick view's contents are removed, then nothing may remain."""
    outside = QUICK_VIEW.sub("", h)
    return (not re.search(r"<img\b", outside) and "data:image/png" not in outside
            and "data:image/jpeg" not in outside and "data:image/gif" not in outside
            and "data:image/webp" not in outside)


# **The same cut, for the two rules that judge what the deck SAYS** (T-167). DS-110 was given the
# quoted/produced distinction when T-070 landed and the rest of `STATIC` was not, so these two read
# the whole file - every rule below is a lambda over `h`, and `h` includes the sources the quick
# view carries. An adopter's deck was failed by both halves of that: DS-100 fired on section
# headings inside the quoted analysis (*Where are the delays?*), and the same file would have failed
# DS-106 the day a source used the word *leverage*.
#
# **Which rules this cut applies to is decided by what the rule judges, not by where it looks.**
# A rule about the deck's CONSTRUCTION keeps the whole file, because a quoted source that reaches
# the network, ships a second palette or breaks the charset is a real defect wherever it sits -
# DS-001, DS-002, DS-006 and the whole colour, type and unit family stay as they are. A rule about
# the deck's COPY takes the cut. Only two rules in `STATIC` are the second kind.
#
# Three rows are worth naming as deliberately left alone, because they read like candidates and are
# not: DS-008 (latin script) must see a quoted source, since the embedded faces are what render it;
# DS-044 (heading levels reset) and DS-118 (literal colour in fill=) would both be defensible either
# way, and neither has a case behind it - a rule moved on a hunch is the same defect facing the
# other direction.
def ds100_no_rhetorical_questions(h):
    """DS-100 over slide copy. A question a SOURCE asks is not a question the deck asks."""
    return not re.search(r"\?\s*<", QUICK_VIEW.sub("", h))


def ds106_no_banned_terminology(h):
    """DS-106 over slide copy, for the same reason. The deck does not choose a source's words."""
    return not re.search(r"\b(crucial|pivotal|seamless|leverage|synerg\w*|friction|"
                         r"genuinely|arguably|precisely|delve)\b",
                         QUICK_VIEW.sub("", h), re.I)


# --------------------------------------------------------------------------- DS-009, the preflight
# Three rows rather than one, because the rule has three separable halves and a single boolean
# would report *something about the preflight is wrong* - which is the shape of verdict this gate
# exists not to give. The third is the one that goes stale: a deck that grows a quick view needs a
# row it did not need yesterday, and nothing about the file announces that.


def ds009_preflight_present(h):
    """The block exists, is not empty, and sits where it runs before any slide is parsed."""
    found = re.search(r'<script id="preflight">(.*?)</script>', h, re.S)
    if not found or not found.group(1).strip():
        return False
    body = h.find("<body")
    stage = h.find('<main class="stage"')
    return body >= 0 and stage > found.start() > body


def ds009_degraded_ships_on(h):
    """The marker is authored, the fallback is in the stylesheet, and the script stands down."""
    tag = re.match(r"(?s).*?<html([^>]*)>", h)
    return bool(tag and "data-preflight" in tag.group(1)
                and ":root[data-preflight] .slide" in h
                and "if (root.hasAttribute('data-preflight')) return;" in h)


def ds009_rows_are_this_decks(h):
    """Only the rows this deck has a subject for - the clause `shell.py preflight` maintains."""
    import preflight                                                # noqa: E402 - a sibling tool
    found = re.search(r'<script id="preflight">(.*?)</script>', h, re.S)
    return bool(found) and found.group(1) == preflight.block(h)


# --------------------------------------------------------------------------- DS-005, fetch-like
# **The rule is about the ARGUMENT, not about the function name** (T-093). The predicate this
# replaced was `not re.search(r"\bfetch\s*\(|XMLHttpRequest|\bimport\s*\(", h)` - which forbids
# `import(blob:)`, the one route R6 §6 measured as working for an ESM library, and which DS-006
# exists for the sole purpose of making work. A check that forbids what two other rules assume is
# reading wider than the rule it implements, which is the shape T-069 found on DS-001.
#
# Two narrowings, and both are the rule's own words. *Script* may not read a local file's bytes, so
# only `<script>` bodies are scanned - a slide saying `import (see the appendix)` is prose, and
# matching vocabulary rather than structure is **L-67**. And a *local file* is named by a path, so a
# `data:` or `blob:` URL is not one: the bytes are already in the page.
SCRIPTS = re.compile(r"<script\b[^>]*>(.*?)</script>", re.S)
FETCH_LIKE = re.compile(r"\b(fetch|import)\s*\(")
WITH_LITERAL = re.compile(r"\b(fetch|import)\s*\(\s*(['\"])([^'\"]*)\2")
INLINE_URL = ("data:", "blob:")


def fetch_verdicts(h):
    """DS-005's two rows: XHR, and what every fetch-like call site names.

    **The count travels in the text**, for DS-105's reason: *0 naming a path, of 0 sites* and *0 of
    12* are the same boolean and are not the same fact, and a deck that fetches nothing must not
    read as a deck whose fetches were checked (**L-36**).

    A call site whose argument is not a string literal is reported and not failed. It cannot be
    decided here - the working ESM route builds its blob URL into a variable first - and guessing
    either way would be the check inventing a verdict. What catches a path arriving through a
    variable is the deck being one file with no siblings to read.
    """
    js = "\n".join(SCRIPTS.findall(h))
    sites, opaque, bad = 0, 0, []
    for found in FETCH_LIKE.finditer(js):
        sites += 1
        literal = WITH_LITERAL.match(js, found.start())
        if not literal:
            opaque += 1
            continue
        url = literal.group(3)
        if not url.startswith(INLINE_URL):
            bad.append("%s(%r)" % (literal.group(1), url[:40]))
    return [
        ("DS-005", "no XMLHttpRequest: script reads bytes the page already carries, never a file",
         "XMLHttpRequest" not in js),
        ("DS-005", "every fetch-like call names an inline URL: %d site(s), %d not a literal, "
         "%d naming a path%s"
         % (sites, opaque, len(bad), "" if not bad else " - " + "; ".join(bad[:3])),
         not bad),
    ]


STATIC = [
    ("DS-001", "zero external references, provenance links excepted (DS-105 judges those)",
     ds001_no_external_references),
    ("DS-003", "meta charset present",
     lambda h: '<meta charset="utf-8">' in h.lower()),
    ("DS-009", "a capability preflight, and it runs before the first slide is parsed",
     ds009_preflight_present),
    ("DS-009", "the degraded state ships on: authored marker, fallback block, script stands down",
     ds009_degraded_ships_on),
    ("DS-009", "the preflight holds only the rows this deck has a subject for",
     ds009_rows_are_this_decks),
    ("DS-008", "latin script only",
     lambda h: not re.search(r"[Ͱ-ϿЀ-ӿ一-鿿぀-ヿ]", h)),
    ("DS-030", "three named type roles",
     lambda h: all(t in h for t in ("--font-display", "--font-text", "--font-mono"))),
    ("DS-031", "no Inter, Roboto, Arial or system-ui",
     lambda h: not re.search(r"font-family:[^;]*(Inter|Roboto|Arial|system-ui)", h)),
    ("DS-032", "faces embedded base64, licence travelling with them",
     lambda h: h.count("data:font/woff2;base64,") >= 1 and "Open Font License" in h),
    ("DS-033", "no vw/vh/clamp inside the stage",
     lambda h: not re.search(r"[:\s]\d[\d.]*v[wh]\b", h) and "clamp(" not in h),
    ("DS-061", "no width media query reshaping the stage",
     lambda h: not re.search(r"@media[^{]*max-width", h)),
    ("DS-088", "no speaker notes in the shipped deck",
     lambda h: "speaker-note" not in h and 'class="notes' not in h),
    ("DS-110", "no raster the deck produces; a quoted source may be raster inside a quick view",
     lambda h: ds110_no_produced_raster(h)),
    ("DS-122", "no chart library",
     lambda h: not any(x in h.lower() for x in
                       ("chart.js", "d3.min", "plotly", "highcharts", "echarts"))),
    # The two rows that read slide copy rather than the file. See the note above the helpers.
    ("DS-100", "no rhetorical questions in slide copy", ds100_no_rhetorical_questions),
    ("DS-106", "no banned terminology", ds106_no_banned_terminology),
    # ---- added by T-005, closing rules that were labelled `auto` and checked by nothing (L-36)
    ("DS-002", "no CDN host referenced - `linked` is not a shipping mode",
     lambda h: not re.search(r"cdn\.|unpkg\.com|jsdelivr|cdnjs|googleapis\.com", h, re.I)),
    # DS-005 moved out of `STATIC` by T-093 and into `fetch_verdicts` below: it needs a count in its
    # text, which a boolean cannot carry, and the boolean it replaced forbade the one ESM route R6
    # measured as working.
    ("DS-006", "no relative module specifier in an inline module", ds006_module_specifiers),
    ("DS-010", "no colour literal outside the token layer", ds010_colours_tokenised),
    ("DS-011", "one resolved palette, not one per topic", ds011_one_palette),
    ("DS-012", "dark mode is custom-property overrides only", ds012_dark_is_overrides),
    ("DS-020", "exactly one accent hue, roles excluded", ds020_one_accent),
    ("DS-023", "never pure white, never pure black", ds023_no_pure_black_or_white),
    ("DS-024", "light is the default, dark is the override", ds024_light_by_default),
    ("DS-028", "no gradient on the ground, the stage or a slide", ds028_no_full_page_gradient),
    ("DS-034", "body 24-28 du at line-height 1.40-1.70", ds034_body_type),
    ("DS-037", "text-wrap: balance on display headings", ds037_display_headings_balanced),
    ("DS-040", "grid and flexbox both used", ds040_grid_and_flex),
    ("DS-044", "every heading level in use is reset", ds044_headings_reset),
    ("DS-045", "no unscoped rule on the bare b element", ds045_no_bare_b),
    ("DS-065", "no vw/vh/vmin/vmax/pt/cm/in outside print", ds065_units_ride_the_transform),
    ("DS-111", "no embedded object standing in for a diagram", ds111_figures_are_drawn),
    ("DS-118", "no literal colour in a fill= or stroke=", ds118_svg_colour_from_css),
    ("DS-119", "every <canvas> carries pixel dimensions", ds119_canvas_dimensions),
    ("DS-141", "no duration over 500 ms without a declared --motion-long licence", ds141_durations),
    ("DS-240", "the short band is reached only by affordance motion", ds240_band_is_closed),
    ("DS-240", "a control's press outranks its own hover", ds240_press_beats_hover),
    ("DS-144", "no 3D transform on a slide transition", ds144_no_3d_between_slides),
    ("DS-163", "no :hover rule revealing content", ds163_no_hover_only),
    ("DS-165", "the disclosure mark is not restyled per slide", ds165_one_disclosure_mark),
]


# ------------------------------------------------------------------ stage 1b: the editorial split
# **DS-230 is `judge` and this is not it.** What tier two is *for* needs someone to read the slide;
# what a program can settle is the one thing DS-161 leaves decidable — whether the deliverable
# quotes a number the closed slide does not show (DS-231).
#
# It sits here rather than in `STATIC` because the count has to travel in the row's text: *0
# problems over 6 cited figures* and *0 problems over none* read identically otherwise (**L-36**),
# and this deck's bottom lines carry six figures between them, one of which the panel repeats.
#
# The two sides are read with **different instruments on purpose**. A figure is `content.FIGURE` —
# a quantity a reader repeats, so a bottom line citing one is making a claim — while support is any
# number visible with the slide closed. Reading support strictly failed slide 3 of the reference
# deck, where `11` and `minutes, average wait` are two elements and so never one figure: the deck
# was right and the instrument was wrong, which is the direction a gate row cannot afford.

SLIDE_BLOCK = re.compile(r'<section[^>]*class="[^"]*\bslide\b[^"]*"[^>]*>(.*?)</section>',
                         re.S | re.I)
DISC_PANEL = re.compile(r'<div class="disc-panel"[^>]*>.*?</div>\s*</div>', re.S)
BOTTOM_LINE = re.compile(r'<p class="bottom-line[^"]*"[^>]*>.*?</p>', re.S)
ANY_NUMBER = re.compile(r"\d[\d,]*(?:\.\d+)?\s?[MKB]?", re.I)


def magnitude(value):
    """A figure reduced to what makes it the same figure. `$5.6M` and `5.6 m` are one; `11 minutes`
    and a bare `11` are one, because the unit is how the face happens to be written and not what
    the bottom line is claiming. **The magnitude suffix is only taken when it stands alone** — `M`
    in `5.6M` is millions, and the `m` in `11 minutes` is the start of a word.

    **The reversed form is turned round first** (T-169). `content.FIGURE` reads `Month 18` as a
    figure, and without `unreverse` this reduced it to the whole string rather than to `18` — so it
    matched nothing on the slide face and DS-231 reported the reference deck citing behind a click
    a number the face shows three times."""
    v = content.unreverse(value).lower().replace(",", "").replace("$", "").strip()
    m = re.match(r"^([\d.]+)\s*([mkb])(?![a-z])", v)
    num, mag = (m.group(1), m.group(2)) if m else (re.match(r"^([\d.]*)", v).group(1), "")
    num = num.rstrip(".")
    if "." in num:
        num = num.rstrip("0").rstrip(".")
    return (num + mag) if num else v


def _figures(fragment):
    return {magnitude(f.group(1)) for run in content.runs(fragment)
            for f in content.FIGURE.finditer(run)}


def _numbers(fragment):
    return {magnitude(n.group(0)) for run in content.runs(fragment)
            for n in ANY_NUMBER.finditer(run)}


def split_data(html):
    """`(cited, unsupported)` — figures the deck's bottom lines cite, and those of them a reader
    with every panel closed cannot see anywhere on the slide."""
    cited, unsupported = 0, []
    for m in SLIDE_BLOCK.finditer(content.strip_comments(html)):
        block, panels = m.group(1), DISC_PANEL.findall(m.group(1))
        if not panels:
            continue
        bl = BOTTOM_LINE.search(block)
        if not bl:
            continue                      # DS-202's subject, and its row already fails on it
        # **The bottom line is not its own support**, and leaving it in the face made the row
        # vacuous: every figure it cites appears in it, so nothing could ever be unsupported. What
        # the reader needs closed is the slide showing the number, not the sentence claiming it.
        face = block.replace(bl.group(0), " ")
        for p in panels:
            face = face.replace(p, " ")
        quoted = _figures(bl.group(0))
        hidden = set().union(*[_figures(p) for p in panels])
        cited += len(quoted)
        name = re.search(r'data-name="([^"]*)"', m.group(0))
        for fig in sorted((quoted & hidden) - _numbers(face)):
            unsupported.append(((name.group(1) if name else "?"), fig))
    return cited, unsupported


def split_verdicts(html):
    """DS-231's row. A prohibition over the deck's bottom lines — see `ABSENCE_IS_A_PASS`."""
    cited, bad = split_data(html)
    return [("DS-231", "figures a bottom line cites that live only behind the click: %d of %d%s"
             % (len(bad), cited,
                "" if not bad else " - " + "; ".join("%s: %s" % b for b in bad[:3])),
             not bad)]


# ------------------------------------------------------- stage 1d: references across the slides
# **DS-232**, added 2026-08-12 (T-104). A `<marker>` defined in one slide and referenced from
# another paints nothing: `.slide` is `visibility:hidden` except `[data-current]`, and a hidden
# subtree has nothing for a visible one to point at. It works on exactly one slide — whichever
# happened to be open when the author looked — and an adopting deck shipped four of five diagrams
# with no arrowheads at all, past every gate here.
#
# **Only paint references count.** `url(#id)` and `<use href="#id">` are the two ways an SVG names
# something to draw with; an `<a href="#x">` is navigation and resolves whatever is hidden, which
# is why matching every `#` would report a defect the reader does not have.
#
# **An id defined nowhere is not this rule's subject.** The sprite, the quick view and the chrome
# all sit outside every slide and are legitimate targets, so the test is *defined in a DIFFERENT
# slide* rather than *not defined here* — the second would fail every `<use href="#i-source">` in
# the deck.
PAINT_REF = re.compile(r'url\(\s*#([A-Za-z][-\w.:]*)\s*\)|<use\b[^>]*?href="#([^"]+)"')
ELEMENT_ID = re.compile(r'\bid="([^"]+)"')


def marker_data(html):
    """`(examined, [(slide, id)])` — paint references resolving inside a *different* slide."""
    slides = []
    for m in SLIDE_BLOCK.finditer(content.strip_comments(html)):
        name = re.search(r'data-name="([^"]*)"', m.group(0))
        slides.append(((name.group(1) if name else "?"), m.group(0)))
    owned = [set(ELEMENT_ID.findall(body)) for _n, body in slides]
    elsewhere = [set().union(*(owned[:i] + owned[i + 1:])) if len(slides) > 1 else set()
                 for i in range(len(slides))]
    examined, bad = 0, []
    for i, (name, body) in enumerate(slides):
        for a, b in PAINT_REF.findall(body):
            ref = a or b
            examined += 1
            if ref in elsewhere[i] and ref not in owned[i]:
                bad.append((name, ref))
    return examined, bad


def marker_verdicts(html):
    """DS-232's row. A prohibition over the deck's SVG references — see `ABSENCE_IS_A_PASS`."""
    examined, bad = marker_data(html)
    return [("DS-232", "SVG paint references defined in another slide, which never render: "
             "%d of %d%s"
             % (len(bad), examined,
                "" if not bad else " - " + "; ".join("%s: #%s" % b for b in bad[:3])),
             not bad)]


def front_matter_verdicts(html):
    """DS-242's row. The lobby is optional, so absence is a pass; what is checked is its shape.

    Three mechanical clauses and no more. *Nothing from the argument* is the clause that matters
    most and it is a reading, so it stays with the critique pass - the same division DS-241 and
    DS-090 make. What a program settles is that there is at most one, that it is first, and that
    the deck still has an argument to be in front of.
    """
    stages = [m.group(1).strip().lower()
              for m in re.finditer(r'<section[^>]*class="[^"]*\bslide\b[^"]*"[^>]*'
                                   r'data-stage="([^"]*)"', content.strip_comments(html), re.I)]
    if not stages:
        return [("DS-242", "front matter: no slides to judge", None)]
    front = [i for i, v in enumerate(stages) if v == "front"]
    argument = [v for v in stages if v not in ("front", "back")]
    bad = []
    if len(front) > 1:
        bad.append("%d lobby slides" % len(front))
    if front and front[0] != 0:
        bad.append("the lobby is slide %d, not the first" % (front[0] + 1))
    if front and not argument:
        bad.append("a lobby in front of no argument")
    return [("DS-242", "a lobby, if any, is single, first and in front of an argument: %s"
             % ("; ".join(bad) if bad else
                "%d lobby, %d argument slide(s)" % (len(front), len(argument))),
             not bad)]


def eyebrow_verdicts(html):
    """DS-241's row. The offending slides travel in the text, per T-193."""
    bad = ds241_eyebrow_offenders(html)
    return [("DS-241",
             "eyebrows naming the position, the stage or the headline instead of the subject: "
             "%d%s" % (len(bad), _naming(bad)), not bad)]



# ------------------------------------------------------------- stage 1c: the provenance mark
# **DS-105's *never a dead link* half**, checked from 2026-08-10 (T-069). It sat excused on the
# stated ground that *there are no links to test, DS-001 having banned them* — which is a misreading
# twice over. DS-001 governs what the file must **render** with the network down, and an anchor
# renders offline; and what the excuse actually described was a repository in which no deck cited
# anything, which is a fact about the decks and not about the rule.
#
# Its own row rather than a `STATIC` predicate for DS-231's reason: *0 dead of 4 examined* and *0
# dead of none* read identically as a bare boolean (**L-36**), and a deck that cites nothing must
# not come out of here looking checked.
#
# What a static read settles, and the one thing it cannot:
#   - **empty, `#` alone, `file://`, or any relative target — dead.** The deck is one file the
#     recipient double-clicks (CLAUDE.md rule 1); nothing sitting beside it on the author's disk
#     travels with it, so a link into that folder is dead on arrival, exactly as DS-002 treats a
#     CDN reference. This is the clause T-069 settled.
#   - **`#frag` — decidable exactly.** The id is in this document or it is not.
#   - **`http(s)://` — not decidable here, and named rather than excused.** Whether the far end
#     answers needs the network, which is the one thing a portable deck is defined against. The row
#     prints how many it did not follow, so the unchecked part is visible on every run.

PROVENANCE_MARK = re.compile(
    r'<p[^>]*class="[^"]*\bprovenance\b[^"]*"[^>]*>(.*?)</p>', re.S | re.I)
# Anchors only. A bare `href=` sweep would count the `<use href="#i-source">` that draws the mark's
# own glyph as a link and report `1 of 1 examined` on a deck with no links in it at all - the
# denominator this row exists to make honest, made dishonest by the instrument.
MARK_HREF = re.compile(r'<a\b[^>]*\bhref\s*=\s*["\']([^"\']*)["\']', re.I)

# **The class, not the place, and T-109 is why.** These two used to sweep the region inside
# `<p class="provenance">`, which was the only place the component could sit. It sits in `.body`
# too now - the colophon renders the same rows - and a region sweep silently stopped seeing them:
# the four-kind fixture reported `0 of 0 examined` with an external URL in it, and DS-001 failed
# the same URL because the exemption did not reach it either. Binding to `.sources-link` is also
# tighter than what it replaces: an `<a>` inside a provenance mark that is not part of the
# component was never DS-105's to judge, and is not exempt from DS-001 now.
ANCHOR = re.compile(r'<a\b[^>]*>', re.I)
HREF_ATTR = re.compile(r'\bhref\s*=\s*["\']([^"\']*)["\']', re.I)
CLASS_ATTR = re.compile(r'\bclass\s*=\s*["\']([^"\']*)["\']', re.I)


def source_link_tags(html):
    """Every `<a class="sources-link">` opening tag in the deck, wherever the component sits."""
    out = []
    for m in ANCHOR.finditer(html):
        cls = CLASS_ATTR.search(m.group(0))
        if cls and "sources-link" in cls.group(1).split():
            out.append(m.group(0))
    return out


def provenance_links(html):
    """`(examined, dead, unfollowed)` — every href on a `.sources-link`, judged."""
    ids = set(re.findall(r'\bid\s*=\s*["\']([^"\']+)["\']', html))
    examined, dead, unfollowed = 0, [], 0
    for tag in source_link_tags(html):
        for href in HREF_ATTR.findall(tag):
            examined += 1
            u = href.strip()
            if u.lower().startswith(("http://", "https://")):
                unfollowed += 1
            elif u.startswith("#"):
                if u[1:] not in ids:
                    dead.append(u)
            else:
                dead.append(u or "(empty)")
    return examined, dead, unfollowed


# The identifier bound, and the glyph the multi-source mark must wear. Both are the contract's
# (COMPONENT-CONTRACT.md 3.2.1) rather than this file's - it reads them, it does not set them.
SOURCE_ID_MAX = 6
KNOWLEDGEBASE_GLYPH = "library"

SOURCE_ID = re.compile(r'<span class="sources-id">([^<]*)</span>')
SPRITE_SYMBOL = re.compile(r'<symbol id="(i-[^"]+)"[^>]*\bdata-icon="([^"]*)"')
SOURCES_WRAPPER = re.compile(r'<span class="sources((?: sources--\w+)*)">(.*?)</span></span></span>',
                             re.S)
MARK_USE = re.compile(r'<svg class="sources-mark"[^>]*><use href="#([^"]+)"')
OPEN_KEY = re.compile(r'<button class="sources-open"[^>]*\bdata-qv="([^"]*)"')
TEMPLATE_KEY = re.compile(r'<template class="qv-src" data-qv="([^"]*)"')


def source_component(html):
    """T-109's decidable clauses of DS-105: `(long_ids, wrong_glyphs, unresolved, counts)`.

    Three prohibitions, each over something the file records rather than something a reader judges:
    an identifier past the contract's bound, a many-source mark wearing a one-source glyph, and a
    control that opens nothing. What this cannot reach is written at the call site.
    """
    glyph = dict(SPRITE_SYMBOL.findall(html))
    long_ids = [i.strip() for i in SOURCE_ID.findall(html)
                if len(i.strip()) > SOURCE_ID_MAX]

    wrong_glyphs, marks = [], 0
    for m in SOURCES_WRAPPER.finditer(html):
        body = m.group(2)
        many = 'class="sources-btn"' in body
        use = MARK_USE.search(body)
        if not use:
            continue                       # `.sources--list` carries no mark, by the contract
        marks += 1
        drawn = glyph.get(use.group(1))
        if drawn is None:
            continue                       # a sprite entry with no provenance is DS-112's, not this
        if many and drawn != KNOWLEDGEBASE_GLYPH:
            wrong_glyphs.append("%s marks %d sources" % (use.group(1), body.count("sources-item")))
        elif not many and drawn == KNOWLEDGEBASE_GLYPH:
            wrong_glyphs.append("%s marks one source" % use.group(1))

    carried = set(TEMPLATE_KEY.findall(html))
    keys = OPEN_KEY.findall(html)
    unresolved = sorted({k for k in keys if k not in carried})
    return long_ids, wrong_glyphs, unresolved, (len(SOURCE_ID.findall(html)), marks, len(keys))


def provenance_verdicts(html):
    """DS-105, in four rows: the link half and T-109's three.

    **What none of these can decide is the colophon's prose.** *This deck carries no instruction to
    find its sources on earlier slides* is a reading of a sentence, and the sentence that provoked
    the clause - *open any of the five from the mark in the corner of the slide that cites it* -
    contains no word a pattern could bind to without also failing honest copy. It is a person's,
    like DS-105's *reachable from where the deck is presented* beside it: whether a URL resolves
    for the audience is not a fact the file records either.
    """
    examined, dead, unfollowed = provenance_links(html)
    what = "dead links in a provenance mark: %d of %d examined" % (len(dead), examined)
    if unfollowed:
        what += "; %d external URL(s) present and not followed" % unfollowed
    if dead:
        what += " - " + "; ".join(dead[:3])
    rows = [("DS-105", what, not dead)]

    long_ids, wrong_glyphs, unresolved, (ids, marks, keys) = source_component(html)
    rows.append(("DS-105", "source identifiers past the contract's %d-character bound: %d of %d"
                 % (SOURCE_ID_MAX, len(long_ids), ids)
                 + (" - " + "; ".join(long_ids[:3]) if long_ids else ""), not long_ids))
    rows.append(("DS-105", "marks wearing the wrong kind's glyph: %d of %d"
                 % (len(wrong_glyphs), marks)
                 + (" - " + "; ".join(wrong_glyphs[:3]) if wrong_glyphs else ""), not wrong_glyphs))
    rows.append(("DS-105", "source controls that open nothing: %d of %d"
                 % (len(unresolved), keys)
                 + (" - " + "; ".join(unresolved[:3]) if unresolved else ""), not unresolved))
    return rows


# ---------------------------------------------------------------------------- stage 2: rendered
PROBE = r"""
<script>
(function(){
  function tabbables(root){
    return Array.prototype.filter.call(
      root.querySelectorAll('a[href],button,input,select,textarea,[tabindex]'),
      function(el){
        if (el.disabled || el.closest('[inert]') || el.closest('[hidden]')) return false;
        var r = el.getBoundingClientRect();
        return r.width > 0 && r.height > 0;
      });
  }
  /* Jump to a slide without depending on any one piece of chrome.
     This used to be `getElementById('dots').children[i].click()`. T-028 deleted the twelve dots
     under DS-216, and stage 3 then reported NO RESULT - a null dereference that read as an
     infrastructure failure rather than as "the gate is calling something that no longer exists".
     Next and previous are controls rather than position encodings, so a chrome redesign does not
     take them; and walking from the current slide means the helper never assumes where it is. */
  function goTo(i){
    var slides = document.querySelectorAll('.stage .slide');
    var prev = document.getElementById('prev'), next = document.getElementById('next');
    if (!prev || !next) throw new Error('no prev/next control to drive the deck with');
    var guard = 0;
    while (guard++ < slides.length + 2){
      var cur = document.querySelector('.slide[data-current]');
      var at = Array.prototype.indexOf.call(slides, cur);
      if (at === i || at < 0) return;
      (at < i ? next : prev).click();
    }
  }
  function run(){
    var out = {};
    var stage = document.getElementById('stage');
    var doc = document.getElementById('doc');
    var slides = stage.querySelectorAll('.slide');
    var k = parseFloat(getComputedStyle(stage).getPropertyValue('--k')) || 1;
    out.slideCount = slides.length;

    // DS-035 - nothing below 16 design units, anywhere (amended from 18, 2026-08-06)
    out.underFloor = [];
    var all = stage.querySelectorAll('*');
    for (var i=0;i<all.length;i++){
      var el = all[i];
      if (el.children.length || !el.textContent || !el.textContent.trim()) continue;
      var fs = parseFloat(getComputedStyle(el).fontSize), du = fs;
      if (el.namespaceURI === 'http://www.w3.org/2000/svg'){
        var m = el.getScreenCTM(); if (!m) continue;
        du = fs * (Math.sqrt(Math.abs(m.a*m.d - m.b*m.c)) / k);
      }
      if (du < 15.5) out.underFloor.push([+du.toFixed(1),
        el.textContent.replace(/\s+/g,' ').trim().slice(0,32),
        (el.closest('.slide')||{dataset:{}}).dataset.name || '']);
    }

    // DS-140/142 - a flow may loop, and the shipped theme's `Current` is the instance every deck
    // carries. (This read `DS-140 sanctions exactly one looping motion` until T-187 opened the
    // vocabulary; what decides the rows below is whether a looping thing is a flow or static
    // content, which was always the actual test.) Anything
    // else looping is continuous motion on static content, which DS-142 bans outright. DS-218
    // additionally requires a control for whatever does loop (WCAG 2.2.2 is the criterion behind
    // it; DS-218 is the rule that makes building the control an obligation rather than an
    // inference).
    out.infinite = []; out.ambient = [];
    for (var j=0;j<all.length;j++){
      var c = getComputedStyle(all[j]);
      if ((c.animationIterationCount||'').indexOf('infinite') < 0) continue;
      var row = [c.animationName, (all[j].closest('.slide')||{dataset:{}}).dataset.name || ''];
      out.infinite.push(row);
      if (!all[j].classList.contains('current')) out.ambient.push(row);
    }
    // DS-218 asks for a PERSISTENT control, and T-114 put a `More` menu on the chrome row -
    // so existence stopped being the test. A stop button one click inside a shut menu is not
    // reachable while the motion runs, which is the thing the rule is for. Placement is a static
    // fact about the built markup, decided by `shell.py`'s CHROME_TAIL slot at build time, which
    // is exactly why this can be read here rather than inferred.
    var motionEl = document.getElementById('motion');
    out.motionControl = !!motionEl;
    out.motionPersistent = !!motionEl && !motionEl.closest('.more-menu');

    // DS-091 - **one** headline of six words or fewer. DS-085 - the last slide is a close.
    // The count is measured as well as the length, because the rule's first clause is that the
    // headline EXISTS: a slide carrying none passed the word bound on an empty set, which is L-36
    // in the shape T-051 swept the file for and T-053 closed here.
    out.longHeadlines = []; out.headlineCounts = [];
    for (var s=0;s<slides.length;s++){
      var hs = slides[s].querySelectorAll('.headline');
      if (hs.length !== 1) out.headlineCounts.push([slides[s].dataset.name, hs.length]);
      var h = hs[0];
      if (h && h.textContent.trim().split(/\s+/).length > 6)
        out.longHeadlines.push([slides[s].dataset.name, h.textContent.trim().split(/\s+/).length]);
    }
    out.lastSlide = slides[slides.length-1].dataset.name;

    // DS-111 / DS-123 - figures present, and card rows standing in for a diagram
    out.figures = stage.querySelectorAll('svg.fig').length;

    // ---- T-005 -------------------------------------------------------------------------
    // DS-080 - a <section> per slide. Counted by TAG, because the probe finds slides by class
    // and a `div.slide` would satisfy every other measurement here while breaking this rule.
    out.notSections = [];
    for (var s=0;s<slides.length;s++)
      if (slides[s].tagName.toLowerCase() !== 'section')
        out.notSections.push([slides[s].dataset.name, slides[s].tagName.toLowerCase()]);

    // DS-092 - sentence under 20 words, paragraph 3-4 sentences. Measured on rendered prose, so
    // a sentence broken across two elements is two runs, which is what a reader sees.
    // A terminator only ends a sentence when whitespace or the end follows it. **A decimal point
    // is not a full stop**, and splitting on the bare character cut `$5.6M` in half: a 28-word
    // sentence read as three short ones and the variant suite caught DS-092 missing its own seed.
    // Same rule the DS-202 bottom-line check already uses, and now the same expression.
    function sentences(t){
      var s = t.replace(/\s+/g,' ').trim();
      if (!s) return [];
      return s.split(/(?<=[.!?])\s+/).filter(function(x){ return x.trim().length > 1; });
    }
    out.longSentences = []; out.longParagraphs = [];
    var proseRuns = stage.querySelectorAll('.slide p, .slide li, .slide td');
    for (var p=0;p<proseRuns.length;p++){
      var el = proseRuns[p];
      if (el.querySelector('p,li,td')) continue;
      var txt = (el.textContent||'').replace(/\s+/g,' ').trim();
      if (!txt) continue;
      var ss = sentences(txt);
      if (el.tagName.toLowerCase() === 'p' && ss.length > 4)
        out.longParagraphs.push([(el.closest('.slide')||{dataset:{}}).dataset.name, ss.length]);
      for (var q=0;q<ss.length;q++){
        var w = ss[q].trim().split(/\s+/).filter(Boolean).length;
        if (w > 20) out.longSentences.push(
          [(el.closest('.slide')||{dataset:{}}).dataset.name, w, ss[q].trim().slice(0,48)]);
      }
    }

    // DS-101 / DS-209 - emphasis. Counted as rendered weight rather than as tag, since a class
    // can bold anything and `<b>` can be reset. Recorded per slide, and separately for the runs
    // OUTSIDE the deliverable, which is the distinction DS-209 turns on.
    out.boldRuns = []; out.emphasisOutsideBottomLine = [];
    for (var s=0;s<slides.length;s++){
      var nm = slides[s].dataset.name, n = 0, outside = [];
      var runs = slides[s].querySelectorAll('p,h1,h2,h3,h4,li,td,span,b,strong,text,div');
      for (var r=0;r<runs.length;r++){
        var el = runs[r];
        if (el.children.length || !(el.textContent||'').trim()) continue;
        if (el.closest('.disc-panel') || el.closest('.eyebrow')) continue;
        var wgt = parseInt(getComputedStyle(el).fontWeight, 10) || 400;
        if (wgt < 600) continue;
        n++;
        if (!el.closest('.bottom-line') && !el.closest('.headline'))
          outside.push((el.textContent||'').trim().slice(0,28));
      }
      out.boldRuns.push([nm, n]);
      if (outside.length) out.emphasisOutsideBottomLine.push([nm, outside.length, outside[0]]);
    }

    // DS-113 - the sprite carries ONLY the icons used. Read after start-up, because the printed
    // contents page builds its own `<use>` set from the manifest and a source scan sees none of
    // them - four of this deck's ten symbols are referenced only from there.
    out.unusedSymbols = [];
    var used = {};
    var uses = document.querySelectorAll('use');
    for (var u=0;u<uses.length;u++){
      var href = uses[u].getAttribute('href') || uses[u].getAttribute('xlink:href') || '';
      if (href.charAt(0) === '#') used[href.slice(1)] = 1;
    }
    var syms = document.querySelectorAll('symbol[id]');
    for (var y=0;y<syms.length;y++)
      if (!used[syms[y].id]) out.unusedSymbols.push(syms[y].id);
    out.symbolCount = syms.length;

    // DS-117 - connectors are labelled, always. Distance from the connector's own midpoint to
    // the nearest text in the same figure, in design units, so the number is comparable across
    // figures drawn at different viewBox scales.
    out.connectorLabelGap = [];
    var figs = stage.querySelectorAll('svg.fig');
    for (var f=0;f<figs.length;f++){
      var conns = figs[f].querySelectorAll('[marker-end]');
      var labels = figs[f].querySelectorAll('text');
      for (var c=0;c<conns.length;c++){
        var cr = conns[c].getBoundingClientRect();
        var cx = cr.left + cr.width/2, cy = cr.top + cr.height/2, best = 1e9;
        for (var l=0;l<labels.length;l++){
          var lr = labels[l].getBoundingClientRect();
          var dx = (lr.left + lr.width/2) - cx, dy = (lr.top + lr.height/2) - cy;
          best = Math.min(best, Math.sqrt(dx*dx + dy*dy) / k);
        }
        out.connectorLabelGap.push([+best.toFixed(0),
          (conns[c].closest('.slide')||{dataset:{}}).dataset.name || '']);
      }
    }

    // DS-219 - never set text on a data mark. A text run whose nearest painted background is an
    // SVG shape rather than the page is sitting on a mark; `paintedBehind` below already does
    // exactly this geometry for DS-215, so the two share one definition of "behind".
    // (measured further down, where paintedBehind is defined)

    // DS-135 - the page title and the nav-bar name for that page must match.
    var brand = document.querySelector('.chrome .deck, .chrome .brand, .chrome h1, .ruler-label');
    out.chromeName = brand ? (brand.textContent||'').trim() : null;
    out.docTitle = document.title;

    // DS-164 - a visible affordance with a REAL LABEL; a bare chevron does not qualify.
    out.unlabelledDiscControls = [];
    var dbtns = stage.querySelectorAll('.disc-btn');
    for (var d=0;d<dbtns.length;d++){
      var words = (dbtns[d].textContent||'').replace(/\s+/g,' ').trim();
      if (words.replace(/[^A-Za-z0-9]/g,'').length < 3)
        out.unlabelledDiscControls.push([(dbtns[d].closest('.slide')||{dataset:{}}).dataset.name,
                                         words.slice(0,20)]);
    }
    out.discControls = dbtns.length;

    // DS-026 - semantic roles ship WITH A VISIBLE LEGEND. Only slides that actually use a role
    // colour owe one, so the subject is found before it is judged.
    out.rolesWithoutLegend = []; out.slidesUsingRoles = 0;
    function cls(el){
      var c = el.className;
      return (c && c.baseVal !== undefined) ? c.baseVal : (c || '');
    }
    for (var s=0;s<slides.length;s++){
      var usesRole = false;
      var kids = slides[s].querySelectorAll('*');
      for (var r=0;r<kids.length && !usesRole;r++)
        usesRole = /(^|[\s-])(pos|neg|caution)($|[\s-])/.test(cls(kids[r]));
      if (!usesRole) continue;
      out.slidesUsingRoles++;
      if (!slides[s].querySelector('.legend, .sm-legend'))
        out.rolesWithoutLegend.push(slides[s].dataset.name);
    }

    // DS-043 - no box nested in a box with its own text. A "box" is what a reader sees as one:
    // a painted background or a real border. Nesting alone is not the defect - the outer box
    // carrying its own text is, because that is when the two read as one thing and are two.
    function isBox(el){
      var st = getComputedStyle(el);
      if (st.backgroundColor && st.backgroundColor !== 'rgba(0, 0, 0, 0)'){
        var pr = el.parentElement ? getComputedStyle(el.parentElement).backgroundColor : '';
        if (st.backgroundColor !== pr) return true;
      }
      return parseFloat(st.borderTopWidth) > 0.4 || parseFloat(st.borderLeftWidth) > 0.4;
    }
    function ownText(el){
      for (var i=0;i<el.childNodes.length;i++)
        if (el.childNodes[i].nodeType === 3 && el.childNodes[i].nodeValue.trim()) return true;
      return false;
    }
    out.nestedTextBoxes = [];
    var boxy = stage.querySelectorAll('.slide *');
    for (var b=0;b<boxy.length;b++){
      var el = boxy[b];
      if (el.ownerSVGElement || !isBox(el)) continue;
      var up = el.parentElement;
      while (up && up !== stage){
        if (!up.ownerSVGElement && isBox(up) && ownText(up)){
          out.nestedTextBoxes.push([(el.closest('.slide')||{dataset:{}}).dataset.name,
            (up.className||'') + ' > ' + (el.className||'')]);
          break;
        }
        up = up.parentElement;
      }
    }

    // ---- DS-202/203/205 - the deliverable. T-027 wrote these rules and labelled them auto and
    // render; nothing enforced them until T-028, which is how a deck with a bottom line on none
    // of its twelve slides passed a 43-check gate. L-36: a rule with no coverage is a claim about
    // the instrument, not about the deck.
    out.noBottomLine = [];      // DS-202 - present at all
    out.multiSentence = [];     // DS-202 - one sentence, not a paragraph
    out.bottomLineHidden = [];  // DS-205 - never behind a disclosure
    out.outranked = [];         // DS-203 - second only to the headline
    for (var s=0;s<slides.length;s++){
      var sl = slides[s], nm = sl.dataset.name;
      var bl = sl.querySelector('.bottom-line');
      if (!bl || !bl.textContent.trim()){ out.noBottomLine.push(nm); continue; }
      var txt = bl.textContent.trim().replace(/\s+/g,' ');
      // terminal punctuation followed by space-or-end, so $4.1M and 1.5M are not sentence ends
      var ends = txt.match(/[.!?](\s|$)/g) || [];
      if (ends.length !== 1) out.multiSentence.push([nm, ends.length, txt.slice(0,60)]);
      if (bl.closest('.disc-panel')) out.bottomLineHidden.push(nm);

      // DS-203 is a claim about RANK, so it needs every competing prose run, measured as rendered.
      // Prose only: a stat figure ('11') and a chart label ('Bus') are marks, not sentences, and
      // a word-count floor is what separates them without naming every class by hand.
      var blSize = parseFloat(getComputedStyle(bl.querySelector('b') || bl).fontSize);
      var runs = sl.querySelectorAll('p,h3,h4,li,td,text,div');
      for (var r=0;r<runs.length;r++){
        var el = runs[r];
        if (el.closest('.disc-panel') || el.closest('.bottom-line') || el.closest('.headline')) continue;
        if (el.querySelector('p,h3,h4,li,td,text,div')) continue;   // leaf runs only, no wrappers
        var words = (el.textContent || '').trim().split(/\s+/).filter(Boolean);
        if (words.length < 4) continue;
        var fs = parseFloat(getComputedStyle(el).fontSize);
        if (el.namespaceURI === 'http://www.w3.org/2000/svg'){
          var m = el.getScreenCTM(), sc = m ? Math.sqrt(Math.abs(m.a*m.d - m.b*m.c)) : k;
          fs = fs * (sc / k);
        }
        if (fs >= blSize)
          out.outranked.push([nm, +fs.toFixed(1), +blSize.toFixed(1), words.slice(0,6).join(' ')]);
      }
    }

    // ---- DS-216/217 - one encoding of position, and a chrome budget
    var chrome = document.querySelector('.chrome');
    out.chromeItems = chrome ? tabbables(chrome).length : 0;
    // buttons, plus labelled items that are not merely wrappers around one - counting `li` and
    // `button` separately scored every ribbon stage twice and reported 24 for an 11-item chrome.
    // DS-217 as amended by T-035: a REGULAR REPEATING SCALE counts as one item rather than n,
    // because the budget counts items to bound how noisy the frame reads and a scale is perceived
    // as one object. The claim is verified, never trusted - otherwise `data-scale` is a loophole
    // any evenly spaced row of controls could use to escape the budget entirely.
    // The owner's definition, 2026-08-08: uniform mark, uniform pitch, no per-item label at rest.
    // Two pitch/width clusters are allowed, because major and minor graduations are what makes a
    // ruler a ruler - but a labelled item disqualifies it outright.
    function regularScale(el){
      var kids = Array.prototype.slice.call(el.children);
      if (kids.length < 3) return false;
      var gaps = [], widths = [], prev = null;
      for (var s=0;s<kids.length;s++){
        var r = kids[s].getBoundingClientRect();
        if ((kids[s].textContent || '').trim()) return false;   // a label at rest
        widths.push(Math.round(r.width * 2) / 2);
        var c = r.left + r.width / 2;
        if (prev !== null) gaps.push(Math.round((c - prev) * 2) / 2);
        prev = c;
      }
      function clusters(a){
        var u = []; for (var t=0;t<a.length;t++) if (u.indexOf(a[t]) < 0) u.push(a[t]); return u;
      }
      return clusters(gaps).length <= 2 && clusters(widths).length <= 2;
    }
    out.chromeLabelled = 0;
    out.scaleVerdict = null;
    if (chrome){
      var scaleEl = chrome.querySelector('[data-scale]');
      var scaleOk = scaleEl ? regularScale(scaleEl) : false;
      if (scaleEl) out.scaleVerdict = scaleOk
        ? 'regular scale, counted as 1'
        : 'claims data-scale but is not regular - counted as n';
      var items = chrome.querySelectorAll('button,[aria-label]');
      for (var q=0;q<items.length;q++){
        if (items[q].querySelector('button')) continue;   // a wrapper, not an item
        if (scaleEl && scaleOk && scaleEl.contains(items[q])) continue;   // counted once, below
        out.chromeLabelled++;
      }
      if (scaleEl && scaleOk) out.chromeLabelled++;
    }
    var chromeRect = chrome ? chrome.getBoundingClientRect() : null;
    var progRect = document.querySelector('.progress');
    progRect = progRect ? progRect.getBoundingClientRect() : null;
    out.chromeHeightDu = chromeRect ? +((chromeRect.height +
      (progRect ? progRect.height : 0)) / k).toFixed(1) : 0;
    // the encodings of position that exist, by the marker each one draws
    out.positionEncodings = [];
    if (document.querySelector('.ruler-ticks li')) out.positionEncodings.push('ruler');
    if (document.querySelector('.ribbon li'))    out.positionEncodings.push('stage ribbon');
    if (document.querySelector('.dots button'))  out.positionEncodings.push('per-slide dots');
    if (document.querySelector('.progress'))     out.positionEncodings.push('progress bar');
    if (document.querySelector('.count'))        out.positionEncodings.push('slide counter');

    // DS-132 - off-screen slides leave the tab order. DS-130 - the current one stays in it.
    var t = tabbables(document);
    out.tabbables = t.length;
    out.tabbablesOffscreen = t.filter(function(el){
      var sl = el.closest('.slide'); return sl && !sl.hasAttribute('data-current'); }).length;
    // DS-130 is measured further down, on a slide that HAS a disclosure control. Taken here it
    // landed on slide 1, which has none, so it reported `null` and the verdict passed on nothing
    // measured - L-36's failure inside the instrument rather than in the deck (T-038).

    // DS-168 / 2.5.8 - every target at least 24 CSS px. The MINIMUM is reported as well as the
    // count, because a threshold comparison alone tells a reader whether the deck passes and not
    // by how much - and `examples/README.md` quoted a smallest-target figure that no command here
    // printed, so it could only ever be re-measured by hand (T-044).
    out.smallTargets = t.filter(function(el){
      var r = el.getBoundingClientRect(); return r.width < 24 || r.height < 24; }).length;
    out.smallestTarget = t.length ? Math.round(Math.min.apply(null, t.map(function(el){
      var r = el.getBoundingClientRect(); return Math.min(r.width, r.height); })) * 10) / 10 : null;

    // DS-227 - every panel closed at load. DS-228 - at most one open at a time, which is the
    // precedence rule DS-137 requires and does not itself supply. DS-138 - the open one drops below
    // its control. This comment read `DS-160/161 - closed by default` until T-038: DS-161 is the
    // judgement about whether the slide's point survives closure, DS-160 is "two tiers, never
    // three", and neither is what these three lines measure. Both rules the probe used to name are
    // `judge`, so the ruleset says no check should be deciding them at all.
    out.panelsOpenInitially = document.querySelectorAll('.stage .disc-panel:not([hidden])').length;
    // DS-160 - two tiers, never three. A third tier is a disclosure control or panel living
    // INSIDE a panel, which is the only shape slide -> detail -> further detail can take.
    out.thirdTier = document.querySelectorAll(
      '.stage .disc-panel .disc-panel, .stage .disc-panel .disc-btn').length;
    out.panelCount = document.querySelectorAll('.stage .disc-panel').length;
    var btns = document.querySelectorAll('.stage .disc-btn');
    if (btns.length){
      btns[0].click();
      goTo(4);
      var b2 = document.querySelector('.slide[data-current] .disc-btn');
      if (b2) out.currentDiscReachable = tabbables(document).indexOf(b2) >= 0;   // DS-130
      if (b2) b2.click();
      out.panelsOpenAfterTwo = document.querySelectorAll('.stage .disc-panel:not([hidden])').length;
      var p = document.querySelector('.slide[data-current] .disc-panel:not([hidden])');
      if (p) out.panelBelowControl =
        p.getBoundingClientRect().top >= p.parentNode.querySelector('.disc-btn').getBoundingClientRect().bottom - 1;
      // Dispatched on BODY, never on `document`. The deck's handler opens with
      // `e.target.matches('input,textarea')`, and `document` has no `matches` - so an event
      // dispatched on the document throws inside the deck's own listener and the key does
      // nothing, silently. Found by DS-166 reporting that an arrow did not advance the deck.
      document.body.dispatchEvent(new KeyboardEvent('keydown', {key:'Escape', bubbles:true}));

      // DS-166 - disclosure state is never required to advance, and the two do not interact.
      // Both halves are observed: an arrow with everything closed must move the deck, and the
      // disclosure toggle must not. Driven through the keyboard rather than the buttons, because
      // the rule is written about keys.
      function at(){
        var cur = document.querySelector('.slide[data-current]');
        return Array.prototype.indexOf.call(slides, cur);
      }
      var before = at();
      document.body.dispatchEvent(new KeyboardEvent('keydown', {key:'ArrowRight', bubbles:true}));
      out.arrowAdvancesClosed = at() === before + 1;
      var afterArrow = at();
      document.body.dispatchEvent(new KeyboardEvent('keydown', {key:'d', bubbles:true}));
      out.toggleDoesNotAdvance = at() === afterArrow;
      // Dispatched on BODY, never on `document`. The deck's handler opens with
      // `e.target.matches('input,textarea')`, and `document` has no `matches` - so an event
      // dispatched on the document throws inside the deck's own listener and the key does
      // nothing, silently. Found by DS-166 reporting that an arrow did not advance the deck.
      document.body.dispatchEvent(new KeyboardEvent('keydown', {key:'Escape', bubbles:true}));

      // DS-146 - charts draw in ONCE, never again on the way back. The deck marks a slide played
      // and the mark is what must survive the round trip; an animation that re-ran would have
      // needed the mark cleared.
      var playedAt = at();
      var wasPlayed = slides[playedAt].hasAttribute('data-played');
      goTo(playedAt > 0 ? playedAt - 1 : playedAt + 1);
      goTo(playedAt);
      out.playedSurvivesReturn = wasPlayed && slides[playedAt].hasAttribute('data-played');
    }

    // DS-135 - the page title and the nav-bar name for that page must match. Read AFTER a
    // navigation, because on slide one the deck's own title collapses to the deck name and the
    // check would be true of any title at all.
    //
    // **Hoisted out of `if (btns.length)` by T-066, and that placement was the whole defect.** It
    // sat in the disclosure block only because the navigation it needs happened to be there, so a
    // deck with no disclosure control never had the key measured and DS-135 reported `False` - for
    // want of a subject every deck has. The navigation is made here instead. What remains
    // conditional is real and much narrower: a deck of one slide has nowhere to navigate to, so
    // there is no second title to compare and the rule is undecided rather than failed.
    if (slides.length > 1){
      goTo(1);
      var cur135 = document.querySelector('.slide[data-current]');
      if (cur135){
        out.titleCarriesSlide = document.title.indexOf(cur135.dataset.name) >= 0;
        out.titleSample = [document.title, cur135.dataset.name];
      }
    }

    // DS-070..076 - the reflow view
    if (doc){
      goTo(6);
      // DS-076 is "position preserved in BOTH directions", so the verdict needs the slide we left
      // as well as the one we came back to. Without it the check asserted only that some slide was
      // current afterwards, which every deck satisfies - it named DS-076 and tested nothing (T-038).
      out.leftFrom = (document.querySelector('.slide[data-current]') || {dataset:{}}).dataset.name;
      document.getElementById('toDoc').click();
      out.docOn = doc.hasAttribute('data-on');
      out.docSections = doc.querySelectorAll('#docBody > section').length;
      var panels = doc.querySelectorAll('.disc-panel');
      out.docPanelsOpen = doc.querySelectorAll('.disc-panel:not([hidden])').length;
      out.docPanelsTotal = panels.length;
      // DS-073 - all content travels, tier two included. Compare text, not element counts.
      function norm(s){ return s.replace(/\s+/g,' ').trim(); }
      out.docShorterThanSlide = [];
      var secs = doc.querySelectorAll('#docBody > section');
      for (var q=0;q<slides.length && q<secs.length;q++){
        var a = norm(slides[q].textContent), b = norm(secs[q].textContent);
        if (b.length < a.length - 2) out.docShorterThanSlide.push([slides[q].dataset.name, a.length, b.length]);
      }
      // DS-075 / 1.4.10 - no two-dimensional scrolling at 320 CSS px
      var prev = doc.style.width;
      doc.style.width = '320px';
      doc.getBoundingClientRect();
      out.at320ScrollWidth = doc.scrollWidth;
      // **The elements, not just how many** (T-193). This kept `.length` and threw the elements
      // away inside the probe, so the verdict row could not name the wide one however it was
      // worded - and DS-075 is the rule an author is most likely to hit and least able to act on.
      var wide = Array.prototype.filter.call(doc.querySelectorAll('#docBody *'),
        function(el){ return el.getBoundingClientRect().width > 321; })
        .map(function(el){
          var cls = (typeof el.className === 'string' && el.className.trim())
            ? '.' + el.className.trim().split(/\s+/).join('.') : '';
          return { sel: el.tagName.toLowerCase() + cls,
                   w: Math.round(el.getBoundingClientRect().width) };
        })
        .sort(function(a, b){ return b.w - a.w; });
      out.at320Overflowing = wide.length;
      out.at320Widest = wide.slice(0, 3);
      doc.style.width = prev;
      out.switchVisibleInDoc = document.getElementById('toStage').getBoundingClientRect().width > 0;
      document.getElementById('toStage').click();
      out.backOnSlide = document.querySelector('.slide[data-current]').dataset.name;
    }

    // DS-140 - `Current` is a dashed flow, and this render says whether it is dashed. It is NOT
    // DS-143: that rule is about what survives `prefers-reduced-motion`, and this render is taken
    // in the default state, so a deck dropping the dasharray under reduced motion passes here.
    // Deciding DS-143 needs a second render under the media feature - a new check, which is T-005's
    // (T-038).
    var cur = document.querySelector('.current');
    if (cur) out.currentDasharray = getComputedStyle(cur).strokeDasharray;

    // DS-214/215 - the colour that RENDERS, not the colour the palette intended. A palette audit
    // compares pairs an author nominates; it cannot see a pair nobody thought to nominate.
    function lum(c){
      var m = (c||'').match(/\d+(\.\d+)?/g); if (!m || m.length < 3) return null;
      var f = [m[0],m[1],m[2]].map(function(v){ v = v/255;
        return v <= 0.04045 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); });
      return 0.2126*f[0] + 0.7152*f[1] + 0.0722*f[2];
    }
    function contrastOf(a,b){
      var x = lum(a), y = lum(b); if (x === null || y === null) return null;
      return (Math.max(x,y)+0.05) / (Math.min(x,y)+0.05);
    }
    function paintedBehind(el){
      if (el.ownerSVGElement){
        var r = el.getBoundingClientRect();
        var cx = r.left + r.width/2, cy = r.top + r.height/2, found = null;
        var shapes = el.ownerSVGElement.querySelectorAll('rect,circle,path,polygon,ellipse');
        for (var i=0;i<shapes.length;i++){
          var sr = shapes[i].getBoundingClientRect();
          if (sr.width < 2 || sr.height < 2) continue;
          if (cx >= sr.left && cx <= sr.right && cy >= sr.top && cy <= sr.bottom){
            var f = getComputedStyle(shapes[i]).fill;
            if (f && f !== 'none' && f !== 'rgba(0, 0, 0, 0)') found = f;
          }
        }
        if (found) return found;
      }
      var n = el.nodeType === 1 ? el : el.parentElement;
      while (n && n !== document.documentElement){
        var bg = getComputedStyle(n).backgroundColor;
        if (bg && bg !== 'rgba(0, 0, 0, 0)') return bg;
        n = n.parentElement;
      }
      return getComputedStyle(document.body).backgroundColor;
    }
    // DS-219 as amended 2026-08-09 - a label may sit on a mark, and then the mark owes TWO
    // numbers: itself against the ground at 3:1 (1.4.11) and the label against it at 4.5:1
    // (1.4.3). The old blanket ban was wider than its own reason, which is about NEUTRALS - and
    // the amended rule is stricter in one direction the ban never looked at, because it also
    // catches a mark too PALE to clear the ground under a label that reads perfectly well.
    out.textOnDataMark = []; out.markPairsFailing = [];
    function groundOf(el){
      var n = el.ownerSVGElement || el;
      while (n && n !== document.documentElement){
        var bg = getComputedStyle(n).backgroundColor;
        if (bg && bg !== 'rgba(0, 0, 0, 0)') return bg;
        n = n.parentElement;
      }
      return getComputedStyle(document.body).backgroundColor;
    }
    var figs2 = stage.querySelectorAll('svg.fig');
    for (var f2=0; f2<figs2.length; f2++){
      var ftexts = figs2[f2].querySelectorAll('text');
      for (var t3=0; t3<ftexts.length; t3++){
        var te = ftexts[t3];
        if (!(te.textContent||'').trim()) continue;
        var r3 = te.getBoundingClientRect();
        var cx3 = r3.left + r3.width/2, cy3 = r3.top + r3.height/2, on = null, onFill = null;
        var shapes3 = figs2[f2].querySelectorAll('rect,circle,ellipse,polygon');
        for (var s3=0; s3<shapes3.length; s3++){
          var sr3 = shapes3[s3].getBoundingClientRect();
          if (sr3.width < 4 || sr3.height < 4) continue;
          var fill3 = getComputedStyle(shapes3[s3]).fill;
          if (!fill3 || fill3 === 'none' || fill3 === 'rgba(0, 0, 0, 0)') continue;
          if (cx3 >= sr3.left && cx3 <= sr3.right && cy3 >= sr3.top && cy3 <= sr3.bottom){
            on = shapes3[s3].getAttribute('class') || shapes3[s3].tagName;
            onFill = fill3;
          }
        }
        if (!on) continue;
        var name3 = (te.closest('.slide')||{dataset:{}}).dataset.name;
        var label3 = (te.textContent||'').trim().slice(0,20);
        var onText = contrastOf(getComputedStyle(te).fill, onFill);
        var onGround = contrastOf(onFill, groundOf(te));
        out.textOnDataMark.push([name3, label3, on,
                                 onText === null ? null : +onText.toFixed(2),
                                 onGround === null ? null : +onGround.toFixed(2)]);
        if (onText === null || onGround === null || onText < 4.5 || onGround < 3)
          out.markPairsFailing.push([name3, label3, on,
                                     onText === null ? null : +onText.toFixed(2),
                                     onGround === null ? null : +onGround.toFixed(2)]);
      }
    }

    out.renderedLowContrast = [];
    out.deadFillAttributes = [];
    for (var sl=0; sl<slides.length; sl++){
      var texts = slides[sl].querySelectorAll('text, p, h2, h3, h4, span, li');
      for (var t2=0; t2<texts.length; t2++){
        var el2 = texts[t2];
        if (el2.children.length || !(el2.textContent||'').trim()) continue;
        var cs2 = getComputedStyle(el2);
        var fg = el2.ownerSVGElement ? cs2.fill : cs2.color;
        var r2 = contrastOf(fg, paintedBehind(el2));
        if (r2 !== null && r2 < 4.5)
          out.renderedLowContrast.push([slides[sl].dataset.name,
            el2.textContent.trim().slice(0,24), fg, paintedBehind(el2), +r2.toFixed(2)]);
        // a fill= that the computed style disagrees with is dead markup (DS-214)
        var attr = el2.getAttribute && el2.getAttribute('fill');
        if (attr && el2.ownerSVGElement){
          var probe = document.createElement('span');
          if (attr.indexOf('var(') === 0){
            probe.style.color = attr; document.body.appendChild(probe);
            var want = getComputedStyle(probe).color; document.body.removeChild(probe);
            if (want && want !== cs2.fill)
              out.deadFillAttributes.push([slides[sl].dataset.name,
                el2.textContent.trim().slice(0,24), attr, cs2.fill]);
          }
        }
      }
    }

    out.vw = window.innerWidth;
    document.title = 'RESULT' + JSON.stringify(out) + 'ENDRESULT';
  }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function(){ setTimeout(run,250); });
  else window.addEventListener('load', run);
})();
</script>
"""


def ok(flag):
    """`None` is neither. A row that found no subject decided nothing, and printing it as either
    answer is the claim T-051 removed (**L-36**)."""
    return "NO SUBJECT" if flag is None else "pass" if flag else "FAIL"


def render_data(deck):
    """Run the stage-3 probe once. Returns (measurements, error) - the browser half."""
    probe = render.make_probe(deck, name="audit.html", extra=PROBE)
    return render.read_result(render.file_url(probe), 1622, 1054)


# --------------------------------------------------------------- stage 2b: reduced motion
# **DS-143 has two clauses and the second is the one that costs something.** *Honoured* is a media
# query anyone can read out of the file; *the semantics survive it* is a claim about what the deck
# still says once the motion is off - the dashed arrows stay dashed, and a slide the reader never
# advanced to is not a blank rectangle.
#
# It was excused in `check.py` until T-016, on the accurate ground that the one render this gate
# takes is in the default state. So this is a SECOND render with the preference forced, and it is
# the whole of the fix: the deck already honoured the query, and nothing had ever looked.
REDUCED_PROBE = r"""
<script>
(function(){
  function run(){
    var out = {};
    var flow = document.querySelector('.current');
    out.hasFlow = !!flow;
    /* The dasharray is DS-143's own example of a semantic that must survive: a dashed arrow
       encodes *this is a flow*, and a reduced-motion pass that solidifies it has removed
       meaning rather than movement. Read the COMPUTED value - the attribute is not the truth. */
    out.flowDash = flow ? (getComputedStyle(flow).strokeDasharray || '') : '';

    /* Every risen element must be at rest AND visible. `.rise` holds opacity 0 until it plays,
       so a deck that merely stops the animation prints the slide blank - which is DS-224 on a
       different medium and the exact failure this row exists to see. */
    var risen = document.querySelectorAll('.slide[data-current] .rise');
    out.risen = risen.length;
    out.risenHidden = 0;
    Array.prototype.forEach.call(risen, function(el){
      var cs = getComputedStyle(el);
      if (parseFloat(cs.opacity) < 0.99) out.risenHidden++;
    });

    /* Anything still animating after the preference is set. `animation-name: none` is the
       resting value; a running name here is motion the reader asked not to see. */
    var moving = [];
    Array.prototype.forEach.call(document.querySelectorAll('.stage *'), function(el){
      var n = getComputedStyle(el).animationName;
      if (n && n !== 'none') moving.push(n);
    });
    out.stillAnimating = moving.slice(0, 8);
    out.stillAnimatingCount = moving.length;
    out.mediaMatches = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    document.title = 'RESULT' + JSON.stringify(out) + 'ENDRESULT';
  }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function(){ setTimeout(run,200); });
  else window.addEventListener('load', run);
})();
</script>
"""


def reduced_motion_data(deck):
    """Run the deck once more with `prefers-reduced-motion: reduce` forced in Chrome."""
    probe = render.make_probe(deck, name="reduced.html", extra=REDUCED_PROBE)
    return render.read_result(render.file_url(probe), 1622, 1054,
                              ["--force-prefers-reduced-motion"])


def reduced_verdicts(data):
    """DS-143's rows. Counts travel in the text, because a pass over nothing reads identically to
    a pass over everything (**L-36**)."""
    if not data:
        return [("DS-143", "the reduced-motion render produced no result", False)]
    if not data.get("mediaMatches"):
        # Not a pass. The flag did not take, so nothing below was measured under the preference -
        # and every row would report the default state while claiming to report the reduced one.
        return [("DS-143", "the reduced-motion render did not enter reduced motion: "
                 "prefers-reduced-motion did not match", False)]
    rows = [("DS-143", "still animating under reduced motion: %d%s"
             % (data.get("stillAnimatingCount", 0),
                "" if not data.get("stillAnimating") else " (%s)"
                % ", ".join(data["stillAnimating"])),
             data.get("stillAnimatingCount", 0) == 0),
            # `risen > 0` required the current slide to CARRY a risen element. A deck that animates
            # nothing in hides nothing, and the rule is about what becomes of what rises - so with
            # no risen element there is no subject. Invisible until T-066 because the fixture
            # evaluated `render_verdicts` and `split_verdicts` and never this function.
            ("DS-143", "risen elements hidden under reduced motion: %d of %d on the current slide"
             % (data.get("risenHidden", 0), data.get("risen", 0)),
             None if not data.get("risen") else data.get("risenHidden", 0) == 0)]
    # The dash is a `conditional`: a deck with no flow diagram owes nothing here. Declared rather
    # than left to the expression, per ABSENCE_IS_A_PASS.
    rows.append(("DS-143", "the flow stays dashed with motion off: %s"
                 % (data.get("flowDash") or "NO FLOW DIAGRAM IN THIS DECK"),
                 (not data.get("hasFlow")) or bool((data.get("flowDash") or "").strip()
                                                   not in ("", "none"))))
    return rows


# --------------------------------------------------------------- passing on an absent subject
# **A row that cannot tell *nothing wrong* from *nothing there* is not a check.** Three shapes are
# legitimate and one is the defect, and the difference is the rule's own quantifier:
#
#   prohibition   never X, at most n X   - the subject is the deck, which exists. Zero X is a pass.
#   conditional   if X then Y            - no X, no obligation. Vacuous truth is the right answer.
#   guarded by R  every X is Y           - vacuous, but row R fails when the subject is absent, so
#                                          no deck reaches a clean run without one.
#   ------------- every X is Y, unguarded - THE DEFECT. Reports `None`, and the rule goes silent.
#
# Every rule whose row still passes against a measurement in which nothing was found is declared
# here, with the shape and the subject, and `self_test` refuses to run if one is missing. **A `guarded
# by` claim is verified rather than trusted**: the self-test requires one of the named rows to be
# failing on that measurement, so a guard that stops guarding is a red run and not a comment that
# quietly went out of date. Naming several is not hedging - a bottom-line rule is vacuous either
# because the deck has no slides or because its slides carry no bottom line, and those are two rows.
#
# This table is the answer to *why does the same fault keep being found one instance at a time* -
# three times before T-051, each fixed in place. It was never that the fix was hard; it was that
# nothing made the next one loud.
ABSENCE_IS_A_PASS = {
    "DS-005": ("prohibition", "no XHR, and no fetch-like call naming a path. A deck with no script "
                              "at all satisfies both, and the second row prints its own denominator "
                              "- *0 naming a path, of 0 sites* and *of 12* are the same boolean and "
                              "not the same fact (T-093)"),
    "DS-035": ("prohibition", "no text run under 16 design units; the subject is the deck's text"),
    "DS-241": ("prohibition", "no eyebrow spending itself on the position, the stage or the "
                              "headline's own words. **The row is written as the prohibition on "
                              "purpose**, and the choice is worth stating: the rule's positive "
                              "half - *is that the right name for what is on the slide* - is a "
                              "reading, so what is left for a program is the four things the name "
                              "must not be. A slide carrying no eyebrow at all is skipped rather "
                              "than failed; whether the part is present is DS-229's question and "
                              "answering it twice would put two rules on one subject"),
    "DS-043": ("prohibition", "no box nested in a box that carries its own text"),
    "DS-073": ("guarded by DS-070", "the reflow view's sections; DS-070 fails when it never "
                                    "engaged, so there is no run in which this is the only silence"),
    "DS-080": ("guarded by DS-081", "a filter over the slides"),
    "DS-091": ("guarded by DS-081", "one headline per slide, of six words or fewer - a filter over "
                                    "the slides. **It was a prohibition until T-053**, and wrongly: "
                                    "the rule's first clause requires the headline to exist, so a "
                                    "deck whose slides carried none passed the word bound over an "
                                    "empty set. Now only a deck with no slides at all reaches this "
                                    "vacuously, and DS-081 fails that"),
    "DS-092": ("prohibition", "no sentence over 20 words, no paragraph over 4 sentences"),
    "DS-105": ("prohibition", "no dead link inside a provenance mark; the subject is the hrefs the "
                              "marks carry, and the row prints its own denominator - a deck whose "
                              "sources are named in plain text has no link to be dead (T-069)"),
    "DS-132": ("prohibition", "nothing tabbable on an off-screen slide"),
    "DS-142": ("prohibition", "no looping motion on static content"),
    # The first rule to reach this table by two routes at once, and the reason the shape field
    # accepts a `+`. DS-143 emits three rows from `reduced_verdicts` - a family that was outside
    # this fixture until T-066, which is why none of them had ever been declared.
    "DS-143": ("prohibition + conditional", "nothing left animating once the preference is set, "
                                            "which a deck animating nothing satisfies; and a flow "
                                            "that is not there owes no dash. The third row - risen "
                                            "elements hidden - has a subject that CAN be absent, "
                                            "and reports None rather than sitting here"),
    "DS-202": ("guarded by DS-081", "a filter over the slides; the first row IS the presence "
                                    "check, and the second is guarded by the first"),
    "DS-203": ("guarded by DS-202/DS-081", "prose outranking a bottom line that exists"),
    "DS-205": ("guarded by DS-202/DS-081", "a bottom line that exists, hidden behind a disclosure"),
    "DS-214": ("prohibition", "no fill= attribute the computed style overrides"),
    "DS-215": ("prohibition", "no text run rendering under 4.5:1"),
    "DS-216": ("prohibition", "at most two encodings of position. Zero is a deck with no position "
                              "indicator, which is DS-133's subject and not this budget's"),
    "DS-217": ("prohibition", "a budget - at most 12 chrome items, at most 90 du tall. A deck with "
                              "no chrome is not over it"),
    "DS-218": ("conditional", "a control is owed for motion that loops; no looping motion, no "
                              "obligation. This is the shape DS-140's `Current` triggers"),
    "DS-219": ("conditional", "a label sitting on a data mark owes two ratios; no label on a mark, "
                              "no pair to measure. The row prints its own denominator, `0 of 0`"),
    "DS-227": ("prohibition", "no panel open at load"),
    "DS-237": ("prohibition", "no motion rule declares neither kind; the subject is the deck's "
                              "stylesheet, and a document with no stylesheet has none to classify. "
                              "The row prints its own denominator (T-112)"),
    "DS-238": ("prohibition", "no motion is governed by the wrong half of the split. Same subject "
                              "and same denominator as DS-237 above (T-112)"),
    "DS-232": ("prohibition", "no SVG paint reference pointing into another slide. The subject is "
                              "the deck's own `url(#id)` and `<use href=\"#id\">` references, and "
                              "the row prints its own denominator - a deck with one slide, or with "
                              "no SVG at all, has pointed nowhere"),
    "DS-231": ("prohibition", "no figure a bottom line cites living only behind a disclosure. The "
                              "subject is the deck's bottom lines, and the row prints its own "
                              "denominator - a deck with no panels, or none whose bottom line "
                              "quotes a figure, has hidden nothing"),
    # ---- `component.py`'s rows, inside the discipline since T-075. The first rule to be declared
    # in both tables: three of its five rows are prohibitions over the deck's own markup and two
    # are requirements the contract states, and an empty document splits them.
    "DS-229": ("prohibition", "three prohibitions over what the deck contains - no contracted class "
                              "outside the place the contract puts it, no class the shared block "
                              "styles without a row, no `vocabulary` row in use. A document with no "
                              "markup has put nothing anywhere and used nothing, and the rows print "
                              "their own denominators"),
}

# ---------------------------------------------------------------- failing on an absent subject
# **The mirror, and the reason the fault above kept coming back.** Everything in `ABSENCE_IS_A_PASS`
# asks which rows PASS when nothing was found. Nothing asked which rows FAIL on one, so a row that
# failed a deck for not containing the thing it judges was checked by nobody - and that asymmetry,
# not the difficulty of any single fix, is why the same defect was found four times: T-038 fixed
# DS-130 in place, T-051 converted three rows and left four beside them, T-065 converted four and
# left three, and v0.1.2 shipped claiming a sweep that had truncated every multi-line row unread.
#
# A failure on an absent subject is legitimate in exactly two shapes, and both are testable:
#
#   requirement   the rule requires the subject to EXIST, so its absence is the defect the row
#                 reports. A deck with no slides really does fail DS-081.
#   entailed by R the absence is a defect, and R is the row that says so. This row failing beside it
#                 is redundant rather than false - and the claim is verified, exactly as
#                 `guarded by` is: R must actually be failing on the same measurement.
#
# Anything else failing here is the defect. It is not declared, it is CONVERTED - the row returns
# `None`, the account calls it undecided, and the deck stops being failed for what it does not have.
ABSENCE_IS_A_FAIL = {
    "DS-081": ("requirement", "at least six slides. A deck with no slides is not a deck that "
                              "happens to lack a subject; it is the failure this row reports"),
    "DS-070": ("requirement", "the reflow view engages. DS-070 is what makes the reflow view "
                              "compulsory, so a deck without one is failing the rule and not "
                              "escaping it"),
    "DS-075": ("entailed by DS-070", "the reflow view's width at 320 CSS px, measured inside "
                                     "`if (doc)`. With no reflow view there is nothing to measure "
                                     "and DS-070 already reports why"),
    "DS-076": ("entailed by DS-070", "position preserved across the reflow view, measured inside "
                                     "`if (doc)`. Same absence, same owner"),
    # ---- `contract.py`'s rows, inside the discipline since T-075
    "DS-060": ("requirement", "the stage scales to min(vw/1920, vh/1080) and its design space "
                              "stays 1920x1080. A deck whose stage never scales and never appears "
                              "at any of four viewports has no design space to measure, and that "
                              "is the defect rather than an absent subject - every deck has a "
                              "stage by construction of the shell"),
    "DS-062": ("entailed by DS-060", "the rendered aspect stays 16:9, measured only where a stage "
                                     "is on screen. With none on screen at any viewport there is "
                                     "no rendered aspect, and DS-060's row above already reports "
                                     "why"),
    "DS-071": ("requirement", "the reflow view engages exactly when k < 0.5. Two of the four "
                              "viewports in the sweep require it to engage, so a deck with no "
                              "reflow view fails this rule rather than lacking its subject - the "
                              "same ruling T-066 recorded for DS-070, which is the static half of "
                              "the same requirement"),
    # ---- `theme.py`, `contrast.py`, `component.py` and `printpages.py`, inside the discipline
    # since T-075. Every one of them is a rule the ruleset states as something a deck must HAVE.
    "DS-011": ("requirement", "exactly one theme region. A document declaring none has not "
                              "satisfied the rule vacuously; the rule is what makes the region "
                              "compulsory, and the count it prints is zero"),
    "DS-013": ("requirement", "every token THEME-CONTRACT.md names is declared, and the data and "
                              "UI roles are distinct from --line. A document with no theme is "
                              "missing all 115 of them, which is the defect this row reports"),
    "DS-027": ("requirement", "both themes evaluated. The rule requires a light theme and a dark "
                              "one to exist before either can be judged, and the row names which "
                              "is missing"),
    "1.4.3": ("entailed by DS-027", "text pairs at 4.5:1, over the pairs the theme yields. With no "
                                    "theme there are no pairs, and DS-027 above is the row that "
                                    "says so - the count was made a failure deliberately, because "
                                    "`0 of 0` passing is how a missing theme reads as a clean one"),
    "1.4.11": ("entailed by DS-027", "non-text pairs at 3:1. Same absence, same owner"),
    "DS-229": ("requirement", "every authored part is the element, place and count the contract "
                              "names, and every rule the contract lists reads the motion tokens it "
                              "lists. Both require the parts to be there; a document with none is "
                              "missing 65 of them"),
    "PRINT-1": ("requirement", "the printed page count is n + k, for n slides and k contents "
                               "sheets. With no slide count from the render stage there is nothing "
                               "to compare, and that is a failure of the gate's own pipeline rather "
                               "than a deck lacking a subject. *Said n + 1 here until 2026-08-13, "
                               "which T-036 falsified the day it let the contents page continue "
                               "onto further sheets - the arithmetic in `printpages.py` was right "
                               "throughout and only this description was stale*"),
    "PRINT-2": ("requirement", "no two cards on a printed contents sheet intersect. With no deck "
                               "there is no sheet to print, and a geometry reader that reports an "
                               "unblemished page from nothing is the exact failure it exists to "
                               "catch (T-123, **L-36**)"),
    "PRINT-3": ("requirement", "no card reaches the footnote band on a printed contents sheet. "
                               "Same absent subject as PRINT-2, and the same reason it must fail "
                               "rather than pass"),
    "DS-239": ("requirement", "a deck to read. `density.verdicts` takes the deck itself, so its "
                              "absent subject is the empty path, and a ranking that was never read "
                              "is not a ranking that is right. A deck that WAS supplied and carries "
                              "no content motion is a different state and a pass - `kind_verdicts` "
                              "and `density.self_test` hold that one (T-112)"),
    "DS-236": ("requirement", "a deck to measure. `figgrid.verdicts` takes the deck itself, so "
                              "its absent subject is the empty path - and an unmeasured diagram is "
                              "not a placed one. A deck that WAS supplied and draws no diagram is a "
                              "different state and a pass; `figgrid.self_test` is what holds it to "
                              "that, with the denominator in the row (T-184)"),
    "DS-244": ("requirement", "a deck to measure. `markhits.verdicts` takes the deck itself, so "
                              "its absent subject is the empty path - and a diagram whose labels "
                              "were never measured is not a diagram whose labels are clear. A deck "
                              "that WAS supplied and draws no diagram is a different state and a "
                              "pass; `markhits.self_test` holds that one, denominator and "
                              "label-on-line count included (T-204)"),
}

# --------------------------------------------------------------- what the probe actually emits
# **The nothing-was-found measurement has to model the probe, or the fixture judges rows against
# values no deck can produce.** This was a tuple of eight names until T-066, and DS-217's height row
# was failing the fixture for that reason alone: `chromeHeightDu` was outside the set, so
# `data.get("chromeHeightDu", 999)` fell back to a sentinel the probe never emits - it writes
# `chromeRect ? … : 0`, and a deck with no chrome measures zero and passes. Nothing was wrong with
# the rule; the instrument was wrong about the instrument.
#
# So the key carries its **nothing-was-found value**, not merely its name: an empty list, a zero, a
# null where the probe emits one. `self_test` builds the measurement from exactly this, and
# `Measurement` below reports any key a row reads that is in neither this table nor
# `CONDITIONALLY_MEASURED`.
ALWAYS_MEASURED = {
    # ---- the deck, its text and its slides
    "slideCount": 0,
    "underFloor": [],
    "longHeadlines": [],
    "headlineCounts": [],
    "longSentences": [],
    "longParagraphs": [],
    "notSections": [],
    "nestedTextBoxes": [],
    "noBottomLine": [],
    "multiSentence": [],
    "bottomLineHidden": [],
    "outranked": [],
    # ---- motion
    "infinite": [],
    "ambient": [],
    "motionControl": False,          # `!!getElementById('motion')`
    # Placement, not existence: the shell builds the control into every deck, so what a
    # looping deck owes is a control NOT shut inside `.more-menu` (DS-218, T-114).
    "motionPersistent": False,
    # ---- chrome, targets and position
    "chromeLabelled": 0,
    "chromeHeightDu": 0,             # `chromeRect ? … : 0` - no chrome measures zero, not 999
    "scaleVerdict": None,
    "positionEncodings": [],
    "tabbablesOffscreen": 0,
    "smallTargets": 0,
    "smallestTarget": None,          # null when nothing tabbable was measured
    # ---- disclosure, counted rather than driven
    "panelsOpenInitially": 0,
    "panelCount": 0,
    "thirdTier": 0,
    "discControls": 0,
    "unlabelledDiscControls": [],
    # ---- graphics, colour and icons
    "symbolCount": 0,
    "unusedSymbols": [],
    "deadFillAttributes": [],
    "renderedLowContrast": [],
    "textOnDataMark": [],
    "markPairsFailing": [],
    # ---- the second render, with the motion preference forced. `mediaMatches` is True because the
    # nothing-was-found case is a render that SUCCEEDED and found nothing; a render where the
    # preference never took is a different failure and `reduced_verdicts` reports it as one.
    "mediaMatches": True,
    "hasFlow": False,
    "flowDash": "",
    "risen": 0,
    "risenHidden": 0,
    "stillAnimating": [],
    "stillAnimatingCount": 0,
}

# The other half of the same fact: keys the probe emits **only inside a guard**, with the guard
# named. Absence here is expected rather than malformed, so a row reading one of these has to say
# what it does when the key is missing - which is the absent-subject rule, and is why the guard is
# written down rather than implied.
#
# **Naming the guard is what distinguishes the two defects that look identical from the outside.**
# `titleCarriesSlide` was conditional on `if (btns.length)` until T-066 - not because DS-135's
# subject can be absent, but because the reading had been parked in the disclosure block for the
# navigation it needed. A bare list of key names would have recorded that as legitimate. Written
# out, "measured inside the disclosure block" is visibly not a statement about page titles.
CONDITIONALLY_MEASURED = {
    "currentDiscReachable": "if (btns.length) and the current slide carries a control",
    "panelsOpenAfterTwo": "if (btns.length) - two controls have been clicked",
    "panelBelowControl": "if (btns.length) and a panel is open on the current slide",
    "arrowAdvancesClosed": "if (btns.length) - the keyboard walk needs a control to close first",
    "toggleDoesNotAdvance": "if (btns.length)",
    "playedSurvivesReturn": "if (btns.length) - the round trip is made inside that block",
    "currentDasharray": "a `.current` flow element exists to compute a dasharray from",
    "titleCarriesSlide": "slides.length > 1 - a one-slide deck has nowhere to navigate to, so "
                         "there is no second title to compare",
    "titleSample": "slides.length > 1, with titleCarriesSlide",
    "docOn": "if (doc) - the reflow view exists",
    "docPanelsOpen": "if (doc)",
    "docPanelsTotal": "if (doc)",
    "docShorterThanSlide": "if (doc)",
    "at320ScrollWidth": "if (doc)",
    "at320Overflowing": "if (doc)",
    "at320Widest": "if (doc)",
    "leftFrom": "if (doc)",
    "backOnSlide": "if (doc)",
}


# A producer the fixture cannot call directly, with what it delegates to **first in the reason**,
# because the self-test parses that word and checks the delegation is real. Without this table the
# split T-075 made would look like an escape hatch; with it, a producer can only sit outside the
# fixture by naming a producer that is inside it and provably calling it.
DELEGATING_PRODUCERS = {
    "contract.scale_verdicts": "contract.scale_verdicts_from is what it delegates to, after a "
                               "render. A producer that needs a browser cannot be run against a "
                               "measurement in which nothing was found, so splitting the render "
                               "off is what makes its rows reachable by any fixture at all.",
}


def verdict_producers():
    """Every module-level verdict producer under `tools/deck/`, as {"<module>.<name>": source}.

    **Read from the source, not from `globals()` and not from imports.** T-066 derived this from the
    module's own namespace, which cannot see a producer in another file - and `contract.py` had two,
    consumed by `check.py`, outside the absent-subject discipline for as long as it existed. Reading
    the directory finds a producer in a module nothing imports as well.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    found = {}
    for fn in sorted(os.listdir(here)):
        if not fn.endswith(".py"):
            continue
        src = open(os.path.join(here, fn), encoding="utf-8").read()
        tops = [m.start() for m in re.finditer(r"^\S", src, re.M)] + [len(src)]
        for m in re.finditer(r"^def (\w*verdicts\w*)\(", src, re.M):
            end = min(t for t in tops if t > m.start())
            found["%s.%s" % (fn[:-3], m.group(1))] = src[m.start():end]
    return found


class Measurement(dict):
    """A measurement that records what was asked of it, so the fixture can check its own model.

    **The gap this closes is the one that put DS-217 on the failing list.** `ALWAYS_MEASURED` is a
    hand-kept table, and a row reading a key nobody added to it was judged against a `.get()`
    default instead - silently, because a default that fires looks exactly like a measurement. Three
    previous fixes in this family (T-038, T-051, T-065) each corrected the instances in front of them
    and left the next one just as invisible; extending the table by hand would have been the fourth.

    Recording the reads instead makes an unmodelled key a **named self-test failure** at the moment
    a row starts reading it, which is the difference between a discipline and a habit.
    """

    def __init__(self, *args, **kw):
        dict.__init__(self, *args, **kw)
        self.read = set()

    def __getitem__(self, key):
        self.read.add(key)
        return dict.__getitem__(self, key)

    def get(self, key, default=None):
        self.read.add(key)
        return dict.get(self, key, default)


def render_verdicts(data):
    """(rule, what, ok) for every rule stage 3 decides. Pure: no browser, so a variant suite can
    seed a break, take one measurement, and ask the same code that gates the real deck.

    **Every row names the rule it tests, and only that rule** - swept for the first time by T-038,
    which found the list claiming two `judge` rules the ruleset says no check should decide, and
    four IDs cited by verdicts that measured something else. The discriminator is subject identity,
    not completeness: a row deciding one clause of its rule is a partial check and belongs here; a
    row whose measurement is a precondition, a proxy or a different rule's subject does not.

    **`ok` has three values, not two.** `True` and `False` are the deck's answer; **`None` means the
    check ran and the deck contains no subject to judge**, which is not a pass and is not a defect
    either. It travels to `check.py`, where the rule lands in `silent` and the run fails - the same
    place a rule with no check at all lands, because both are the gate declining to make a claim
    (**L-36**). What the account adds is which of the two it was, since the fixes differ.
    """
    return [
        ("DS-081", "slides: %d" % data["slideCount"], 6 <= data["slideCount"]),
        ("DS-035", "text below 16 design units: %d" % len(data["underFloor"]),
         not data["underFloor"]),
        # DS-091 has three clauses and the gate reaches two. **The first is that the headline
        # exists** - checked here since T-053, because until then a slide carrying none satisfied
        # the word bound over an empty set and nothing else objected.
        #
        # **The third, `<= 3 supporting fragments`, is excused in `check.py`'s `CLAUSES`**, with
        # the argument and the closing condition. It lived here as a comment until T-054, which is
        # the one place `check.py`'s own rule says an excusal must not live: a comment cannot be
        # reported, so the account called DS-091 `checked` while a third of it went unmeasured.
        ("DS-091", "slides without exactly one headline: %d%s"
         % (len(data.get("headlineCounts", [])),
            "" if not data.get("headlineCounts")
            else "  %s" % ", ".join("%s has %d" % (n, c) for n, c in data["headlineCounts"][:3])),
         not data.get("headlineCounts")),
        ("DS-091", "headlines over six words: %d" % len(data["longHeadlines"]),
         not data["longHeadlines"]),
        ("DS-202", "slides with no bottom line: %d%s"
         % (len(data.get("noBottomLine", [])), _naming(data.get("noBottomLine"))),
         not data.get("noBottomLine")),
        ("DS-202", "bottom lines that are not one sentence: %d%s"
         % (len(data.get("multiSentence", [])), _naming(data.get("multiSentence"))),
         not data.get("multiSentence")),
        ("DS-205", "bottom lines behind a disclosure: %d%s"
         % (len(data.get("bottomLineHidden", [])), _naming(data.get("bottomLineHidden"))),
         not data.get("bottomLineHidden")),
        ("DS-203", "prose outranking the bottom line: %d%s"
         % (len(data.get("outranked", [])), _naming(data.get("outranked"))),
         not data.get("outranked")),
        ("DS-216", "encodings of position: %d (%s)"
         % (len(data.get("positionEncodings", [])), ", ".join(data.get("positionEncodings", []))),
         len(data.get("positionEncodings", [])) <= 2),
        ("DS-217", "labelled or interactive chrome items: %d%s"
         % (data.get("chromeLabelled", 0),
            ("  [%s]" % data["scaleVerdict"]) if data.get("scaleVerdict") else ""),
         data.get("chromeLabelled", 0) <= 12),
        ("DS-217", "chrome height: %s du" % data.get("chromeHeightDu"),
         data.get("chromeHeightDu", 999) <= 90),
        ("DS-132", "tabbables from off-screen slides: %d" % data["tabbablesOffscreen"],
         data["tabbablesOffscreen"] == 0),
        # A null means the probe found no control to measure. That is neither pass nor fail: it is
        # the subject being absent, which T-051 gave a third state and which this row was left out
        # of. Failing here made a deck specified without disclosures un-passable (T-065).
        ("DS-130", "disclosure control in the tab order: %s" % data.get("currentDiscReachable"),
         None if data.get("currentDiscReachable") is None
         else data["currentDiscReachable"] is True),
        # `smallestTarget` is null when nothing tabbable was measured, and a count of 0 then means
        # no target rather than no small one. The minimum is the denominator (T-051).
        ("DS-168", "targets under 24 CSS px: %d (smallest %s)"
         % (data["smallTargets"], data.get("smallestTarget")),
         None if data.get("smallestTarget") is None else data["smallTargets"] == 0),
        ("DS-227", "panels closed at load: %d open" % data["panelsOpenInitially"],
         data["panelsOpenInitially"] == 0),
        # Both keys exist only on a deck with a disclosure control - the probe emits them inside
        # `if (btns.length)`. A `.get()` default that passes, and `is not False` on a null, were the
        # same fault DS-140 had: absence read as conformance (T-051).
        ("DS-228", "panels open at once: %s" % data.get("panelsOpenAfterTwo"),
         None if data.get("panelsOpenAfterTwo") is None
         else data["panelsOpenAfterTwo"] <= 1),
        ("DS-138", "panel drops below its control: %s" % data.get("panelBelowControl"),
         None if data.get("panelBelowControl") is None
         else data["panelBelowControl"] is True),
        ("DS-142", "looping motion on static content: %d%s"
         % (len(data.get("ambient", [])), _naming(data.get("ambient"))),
         not data.get("ambient")),
        # `persistent` rather than `present`: the control exists in every deck the shell builds,
        # so existence decided nothing. What a looping deck owes is a control not shut inside the
        # chrome menu (T-114 step 7a).
        ("DS-218", "persistent control for motion over 5s: %s (present: %s, %d looping)"
         % (data["motionPersistent"], data["motionControl"], len(data["infinite"])),
         len(data["infinite"]) == 0 or data["motionPersistent"]),
        # **The instance T-051 was raised for.** `.current` is the only subject this row has, the
        # probe emits the key only when it finds one, and `None != "none"` is `True` - so the rule
        # passed on its own absence, and the seeded fixture that deletes the deck's only dashed flow
        # reported the same `pass` as the deck that has one. A deck with no flow is legitimate and
        # this is not a failure; it is the rule going undecided, which the account calls silent.
        ("DS-140", "`Current` renders dashed: %s"
         % (data.get("currentDasharray") or "no dashed flow in this deck"),
         None if data.get("currentDasharray") is None
         else data["currentDasharray"] != "none"),
        ("DS-070", "reflow view engages: %s" % data.get("docOn"), data.get("docOn") is True),
        ("DS-073", "sections carrying less text than their slide: %d%s"
         % (len(data.get("docShorterThanSlide", [])), _naming(data.get("docShorterThanSlide"))),
         not data.get("docShorterThanSlide")),
        # Two nulls compare equal, so a deck with no reflow view reported a pass here on
        # `None == None`. DS-070 goes red in that case, so no deck escaped the run - but the row
        # itself was still claiming a rule it had not decided (T-051).
        ("DS-073", "tier-two panels open in the reflow view: %s/%s"
         % (data.get("docPanelsOpen"), data.get("docPanelsTotal")),
         None if data.get("docPanelsTotal") is None
         else data["docPanelsOpen"] == data["docPanelsTotal"]),
        ("DS-075", "reflow scrollWidth at 320 CSS px: %s (overflowing: %s)%s"
         % (data.get("at320ScrollWidth"), data.get("at320Overflowing"),
            _widest(data.get("at320Widest"))),
         data.get("at320ScrollWidth", 999) <= 321 and data.get("at320Overflowing") == 0),
        ("DS-076", "position preserved returning from the reflow view: left %r, back on %r"
         % (data.get("leftFrom"), data.get("backOnSlide")),
         bool(data.get("backOnSlide")) and data.get("backOnSlide") == data.get("leftFrom")),
        ("DS-214", "dead fill= attributes overridden by CSS: %d%s"
         % (len(data.get("deadFillAttributes", [])), _naming(data.get("deadFillAttributes"))),
         not data.get("deadFillAttributes")),
        ("DS-215", "text runs rendering under 4.5:1: %d%s"
         % (len(data.get("renderedLowContrast", [])), _naming(data.get("renderedLowContrast"))),
         not data.get("renderedLowContrast")),
        # ---- added by T-005
        ("DS-080", "slides that are not a <section>: %d%s"
         % (len(data.get("notSections", [])), _naming(data.get("notSections"))),
         not data.get("notSections")),
        ("DS-092", "sentences over 20 words: %d%s, paragraphs over 4 sentences: %d%s"
         % (len(data.get("longSentences", [])), _naming(data.get("longSentences"), 2),
            len(data.get("longParagraphs", [])), _naming(data.get("longParagraphs"), 2)),
         not data.get("longSentences") and not data.get("longParagraphs")),
        # `symbolCount > 0` required the deck to CONTAIN icons, which DESIGN-SYSTEM.md nowhere
        # states: DS-113 is a prohibition over the sprite's symbols, and DS-112 governs where icons
        # come from IF a deck has any. The identical clause to DS-164's, and it takes DS-164's
        # answer - with no sprite the rule has no subject, with one it looks for dead symbols
        # (T-066).
        ("DS-113", "sprite icons never used: %d of %d%s"
         % (len(data.get("unusedSymbols", [])), data.get("symbolCount", 0),
            _naming(data.get("unusedSymbols"))),
         None if not data.get("symbolCount") else not data.get("unusedSymbols")),
        # Measured outside the disclosure block since T-066 - see the probe. The null that survives
        # is a one-slide deck, which has no second title to compare and is DS-081's failure anyway.
        ("DS-135", "the page title carries the slide's name: %s (%r)"
         % (data.get("titleCarriesSlide"), data.get("titleSample")),
         None if data.get("titleCarriesSlide") is None
         else data["titleCarriesSlide"] is True),
        # `discControls > 0` was a requirement that the deck CONTAIN a disclosure control, which
        # DESIGN-SYSTEM.md nowhere states - the gate enforcing a rule the ruleset does not have.
        # With no controls the rule has no subject; with controls it checks their labels (T-065).
        ("DS-164", "disclosure controls with no real label: %d of %d"
         % (len(data.get("unlabelledDiscControls", [])), data.get("discControls", 0)),
         None if not data.get("discControls")
         else not data.get("unlabelledDiscControls")),
        # Both keys exist only on a deck with a disclosure control, same as DS-228 (T-065).
        ("DS-166", "arrow advances with everything closed: %s; the toggle does not advance: %s"
         % (data.get("arrowAdvancesClosed"), data.get("toggleDoesNotAdvance")),
         None if data.get("arrowAdvancesClosed") is None
         else data["arrowAdvancesClosed"] is True and data["toggleDoesNotAdvance"] is True),
        # Null where the deck has no played mark to survive anything (T-065).
        ("DS-146", "the played mark survives navigating away and back: %s"
         % data.get("playedSurvivesReturn"),
         None if data.get("playedSurvivesReturn") is None
         else data["playedSurvivesReturn"] is True),
        # DS-026 is measured (`rolesWithoutLegend`) and NOT emitted as a verdict: the rule wants a
        # *visible* legend and the tripwire slide draws one as two unmarked SVG swatches, which a
        # class-based check reports as missing. Excused in `check.py`, with the argument.
        ("DS-043", "boxes nested in a box that has its own text: %d%s"
         % (len(data.get("nestedTextBoxes", [])), _naming(data.get("nestedTextBoxes"))),
         not data.get("nestedTextBoxes")),
        # `panelCount > 0` is DS-164's clause again, word for word in effect: it required a
        # conforming deck to CONTAIN a disclosure panel. DS-160 is "two tiers, never three", which a
        # deck with no panels cannot violate. **This is the row the adopting project was still
        # failing after v0.1.2 shipped a fix that claimed to have swept for it** (T-066).
        ("DS-160", "third-tier disclosure inside a panel: %d, over %d panel(s)"
         % (data.get("thirdTier", 0), data.get("panelCount", 0)),
         None if not data.get("panelCount") else not data.get("thirdTier")),
        ("DS-219", "labels on a data mark failing 3:1 to ground or 4.5:1 to text: %d of %d"
         % (len(data.get("markPairsFailing", [])), len(data.get("textOnDataMark", []))),
         not data.get("markPairsFailing")),
    ]


def self_test():
    """No verdict may report a pass against a measurement in which nothing was found (**L-36**).

    **This is the check that was missing for three instances.** DS-130 was fixed in place by T-038,
    DS-087 is excused in `check.py` for the same reason in its own words, and DS-140 was found a
    third time by a fixture built to be missing things - and after each one the gate went back to
    having no way to notice a fourth. Reading forty predicates by eye is what produced that record.

    The verdict producers are pure, so the fourth instance costs two dictionaries and no browser:
    build the measurement a probe returns when it finds nothing, run **every** row against it, and
    require each row that still passes to be declared in `ABSENCE_IS_A_PASS`, each row that fails to
    be declared in `ABSENCE_IS_A_FAIL`, and neither table to claim a rule the other does.

    **Three things were wrong with the version this replaces, and each shipped a false claim.**

      1. It asked only which rows PASS. A row failing a deck for not containing the thing it judges
         was checked by nobody - the asymmetry T-051 and T-065 both fell through (T-066).
      2. It evaluated `render_verdicts` and `split_verdicts` and never `reduced_verdicts`, so DS-143
         was outside the discipline entirely. The producers are enumerated from the module now, and
         one the fixture does not exercise fails the run.
      3. Its measurement was eight hand-kept names, so a row reading anything else got a `.get()`
         default instead - a value no deck can produce, indistinguishable from a measurement.
         `Measurement` records the reads and reports a key the fixture has no model of.
    """
    empty = Measurement(ALWAYS_MEASURED)
    reduced = Measurement(ALWAYS_MEASURED)
    try:
        # The static split row is held to the same bar against the same absent subject: a document
        # with no slides. The reduced-motion rows are held to it against a render that SUCCEEDED and
        # found nothing, which is a different thing from a render where the preference never took -
        # `reduced_verdicts` reports that one as its own failure and it is not an absent subject.
        rows = (render_verdicts(empty) + split_verdicts("") + provenance_verdicts("")
                + fetch_verdicts("") + marker_verdicts("") + eyebrow_verdicts("")
                + front_matter_verdicts("")
                + reduced_verdicts(reduced))
    except KeyError as exc:
        sys.exit("SELF-TEST FAILED: a verdict reads data[%s] unconditionally, so it is not in "
                 "ALWAYS_MEASURED and the nothing-was-found measurement cannot be built. Add the "
                 "key there if the probe always emits it, or read it with .get()" % exc)

    # **The resolution contract's rows, which were outside this fixture entirely until T-075.**
    # `contract.py` produces verdict rows that `check.py` consumes, and the derivation below used
    # to read `globals()` - one module. So the guarantee this file believes it makes held over
    # `audit.py` and said nothing about the file next door, where DS-064 was failing a conforming
    # deck for not containing the thing it judges and DS-200 was passing on an empty set. An
    # outside project found the first; nothing here could have found either.
    #
    # **It was six producers outside the fixture, not two.** The directory scan below was written
    # for `contract.py` and immediately named `contrast`, `theme`, `component` and `printpages` as
    # well - every one of them consumed by `check.py`, none of them ever run against a measurement
    # in which nothing was found. Three take the deck's markup, so their absent subject is the
    # empty document `split_verdicts` and `provenance_verdicts` already use; `printpages` takes the
    # slide count the render stage produced, and none is a count of zero.
    sweep_rows = [Measurement(r) for r in contract.nothing_found_rows()]
    rows += contract.verdicts(sweep_rows)
    rows += contract.scale_verdicts_from(contract.nothing_found_results())
    # `contrast.verdicts` used to refuse a document with no `:root` colour tokens outright - it
    # exited the process rather than returning a row - so it was handed a theme with nothing to
    # measure instead of the empty document every other producer is held to. T-076 moved the refusal
    # into `contrast.main`, where a tool declining to run belongs, and it now takes the same subject
    # as the rest. Its four rows fail on it, exactly as they did on the hand-built theme.
    rows += contrast.verdicts("")
    rows += theme.verdicts("") + component.verdicts("")
    rows += printpages.verdicts("", 0)
    # `printgeom` takes the deck itself, so its absent subject is the empty path - and it must
    # decline rather than report an unblemished page, which is the whole reason it exists.
    rows += printgeom.verdicts("")
    # `figgrid` takes the deck too, and the same distinction applies to it: no deck is an unmeasured
    # placement and must decline. Its OTHER absent subject - a render that succeeded and found no
    # diagram - is a pass, and `figgrid.self_test` holds the row to that one, denominator included.
    rows += figgrid.verdicts("")
    # `markhits` is the same shape as `figgrid` and for the same reason: no deck is an unmeasured
    # diagram, which must decline rather than pass. Its other absent subject - a render that found
    # no diagram at all - is a pass, and `markhits.self_test` holds the row to that one along with
    # the label-on-line count, which must survive into the text even when nothing gates (T-204).
    rows += markhits.verdicts("")
    # `density` has both shapes, and they have different absent subjects. `verdicts` takes the deck,
    # so no deck is an unmeasured ranking and it must decline. `kind_verdicts` takes the markup, and
    # a document with no stylesheet has classified nothing wrongly - it passes, with its own
    # denominator in the row so it cannot read like a document whose motions were checked.
    rows += density.verdicts("")
    rows += density.kind_verdicts("")
    # `spec.verdicts` reads the two specification documents rather than the deck, so its absent
    # subject is a pair of empty ones - no source list, no slide, no ledger. It is the first
    # producer here that `check.py` does not consume, and it is held to the same bar anyway: the
    # discipline is about rows nobody makes choose between undecided and satisfied, not about which
    # command happens to print them (T-071).
    rows += spec.verdicts("", "")
    # **An absent subject and an unreadable one are two states, and this is where they stay apart.**
    # The line above supplies no deck, which leaves SPEC-5 undecided and is correct. A deck that WAS
    # supplied and parsed to no slides reported that same `None` until T-090 - so a rule could skip
    # itself entirely and say so in the words for *not applicable*, on a deck whose other four rows
    # were passing. The assertion lives here as well as in `spec.py` because this is the file that
    # holds every producer to what an absent subject means, and the collapse is a claim about that.
    absent_deck = dict((r, ok) for r, _w, ok in spec.verdicts("", ""))
    unread_deck = dict((r, ok) for r, _w, ok in
                       spec.verdicts("", "", "<section class=\"slide\"><h2>a</h2></section>"))
    if absent_deck["SPEC-5"] is not None or unread_deck["SPEC-5"] is not False:
        sys.exit("SELF-TEST FAILED: SPEC-5 reports %r with no deck and %r for a deck it could not "
                 "read. Those are different states and only one of them is benign (T-090)"
                 % (absent_deck["SPEC-5"], unread_deck["SPEC-5"]))
    # **DS-005 reads the argument, and both directions are fixtures** (T-093, **L-04**). The
    # predicate this replaced was a name match, so `import(blob:)` - the one route R6 §6 measured as
    # working - could not be written in a conforming deck, and there was no fixture to say so
    # because a check that only ever refuses looks exactly like a check that is right.
    def ds005(js, markup=""):
        rows_ = fetch_verdicts("<script>%s</script>%s" % (js, markup))
        return [ok for _r, _w, ok in rows_]

    for js, want, why in (
            ("fetch('./sibling.txt')", [True, False], "a fetch of a sibling file"),
            ("import('./x.mjs')", [True, False], "a relative dynamic import"),
            ("var x = new XMLHttpRequest()", [False, True], "XHR"),
            ("import('data:text/javascript,export default 1')", [True, True], "a data: import"),
            ("import('blob:null/abc')", [True, True], "a blob: import"),
            ("var u = make(); import(u)", [True, True], "an import whose argument is a variable"),
            ("", [True, True], "a deck whose script does nothing of the kind")):
        if ds005(js) != want:
            sys.exit("SELF-TEST FAILED: DS-005 reports %s for %s, expected %s. The rule is about "
                     "the ARGUMENT - a `data:` or `blob:` URL is bytes the page already carries, "
                     "not a local file (T-093)" % (ds005(js), why, want))
    # And the subject is *script*, because that is the rule's own word. A slide that discusses one
    # of these is prose, and matching vocabulary rather than structure is L-67.
    if ds005("", "<p>Then import ('the appendix') and fetch ('the minutes').</p>") != [True, True]:
        sys.exit("SELF-TEST FAILED: DS-005 read slide prose as a call site")

    modelled_sweep = set(contract.PROBE_FOUND_NOTHING) | {"vw", "vh", "want"}
    unmodelled_sweep = sorted(set().union(*[r.read for r in sweep_rows]) - modelled_sweep)
    if unmodelled_sweep:
        sys.exit("SELF-TEST FAILED: contract's rows read %s, which contract.PROBE_FOUND_NOTHING "
                 "has no model of. Add the key there with the value the probe emits when it finds "
                 "nothing - a .get() default on an unmodelled key is a value no deck produces, "
                 "which is what put DS-217 on the failing list (T-066)."
                 % ", ".join(unmodelled_sweep))

    # **Derived from the source of every module, never listed by hand.** `reduced_verdicts` sat
    # outside this fixture from the day it was written, and nothing said so: the fixture named its
    # producers, and a name nobody adds is a name nobody misses. T-066 fixed that by reading
    # `globals()`, which is the same mistake one scope out - a producer in another module is
    # equally invisible. The source is read rather than imported so a module nothing imports is
    # still found.
    exercised = {"audit.render_verdicts", "audit.split_verdicts", "audit.provenance_verdicts",
                 "audit.fetch_verdicts", "audit.marker_verdicts", "audit.eyebrow_verdicts",
                 "audit.front_matter_verdicts",
                 "audit.reduced_verdicts", "contract.verdicts", "contract.scale_verdicts_from",
                 "contrast.verdicts", "theme.verdicts", "component.verdicts",
                 "printpages.verdicts", "printgeom.verdicts", "spec.verdicts",
                 "figgrid.verdicts", "markhits.verdicts", "density.verdicts",
                 "density.kind_verdicts"}
    producers = verdict_producers()
    undeclared_producers = sorted(set(producers) - exercised - set(DELEGATING_PRODUCERS))
    if undeclared_producers:
        sys.exit("SELF-TEST FAILED: %s produce verdict rows and this fixture does not exercise "
                 "them. A verdict producer outside the fixture is a family of rows nobody is "
                 "holding to the absent-subject rule, which is how DS-143 stayed invisible through "
                 "two fixes (T-066) and DS-064 through three (T-075)."
                 % ", ".join(undeclared_producers))
    gone = sorted((exercised | set(DELEGATING_PRODUCERS)) - set(producers))
    if gone:
        sys.exit("SELF-TEST FAILED: %s are named here and no module defines them - the fixture is "
                 "claiming to exercise a producer that does not exist" % ", ".join(gone))
    for name, why in sorted(DELEGATING_PRODUCERS.items()):
        target = why.split()[0]
        if target not in exercised or target.split(".")[-1] not in producers[name]:
            sys.exit("SELF-TEST FAILED: %s is declared to delegate to %s, and either that is not "
                     "an exercised producer or its source does not call it. A delegation nobody "
                     "checks is how a producer parks itself outside the fixture." % (name, target))

    # **What did the rows actually ask for?** A key in neither table is one the fixture has no model
    # of, so whatever a row reads it with is fiction. This is DS-217's whole story: `chromeHeightDu`
    # was unmodelled, `data.get("chromeHeightDu", 999)` supplied a sentinel against a probe that
    # writes `chromeRect ? … : 0`, and a rule with nothing wrong with it sat on the failing list.
    modelled = set(ALWAYS_MEASURED) | set(CONDITIONALLY_MEASURED)
    unmodelled = sorted((empty.read | reduced.read) - modelled)
    if unmodelled:
        sys.exit("SELF-TEST FAILED: rows read %s, which is in neither ALWAYS_MEASURED nor "
                 "CONDITIONALLY_MEASURED.\n  The fixture has no model of that key, so any .get() "
                 "default on it is a value no deck produces. Add it to ALWAYS_MEASURED with the "
                 "value the probe emits when it finds nothing, or to CONDITIONALLY_MEASURED naming "
                 "the guard it sits behind." % ", ".join(unmodelled))
    unread = sorted(modelled - (empty.read | reduced.read))
    if unread:
        sys.exit("SELF-TEST FAILED: %s are modelled and no row reads them - the declaration "
                 "outlived the row it was written for" % ", ".join(unread))

    states = {}
    for rid, _what, ok in rows:
        states.setdefault(rid, []).append(ok)
    passing = sorted(r for r, oks in states.items() if True in oks)
    failing = sorted(r for r, oks in states.items() if False in oks)

    undeclared = [r for r in passing if r not in ABSENCE_IS_A_PASS]
    if undeclared:
        sys.exit("SELF-TEST FAILED: %s pass against a measurement in which nothing was found and "
                 "are not declared in ABSENCE_IS_A_PASS.\n  A rule of the form *every X is Y* whose "
                 "X is absent is not passing - it is undecided, and reports None. A prohibition or "
                 "a conditional IS passing, and says so there in writing."
                 % ", ".join(undeclared))
    stale = [r for r in ABSENCE_IS_A_PASS if r not in passing]
    if stale:
        sys.exit("SELF-TEST FAILED: %s are declared to pass on an absent subject and do not - the "
                 "declaration outlived the row it excuses" % ", ".join(sorted(stale)))

    # **The same bar in the other direction, and it is the point of T-066.** A row that fails on a
    # measurement where nothing was found is either reporting a real requirement or failing a deck
    # for what it does not have, and until this ran nothing made anyone choose.
    undeclared_fail = [r for r in failing if r not in ABSENCE_IS_A_FAIL]
    if undeclared_fail:
        sys.exit("SELF-TEST FAILED: %s FAIL against a measurement in which nothing was found and "
                 "are not declared in ABSENCE_IS_A_FAIL.\n  Either the rule requires its subject to "
                 "exist - say so there, in writing - or the row is failing a deck for not "
                 "containing the thing it judges, and it must report None instead (T-066)."
                 % ", ".join(undeclared_fail))
    stale_fail = [r for r in ABSENCE_IS_A_FAIL if r not in failing]
    if stale_fail:
        sys.exit("SELF-TEST FAILED: %s are declared to fail on an absent subject and do not - the "
                 "declaration outlived the row it explains" % ", ".join(sorted(stale_fail)))
    # **A rule MAY reach both tables, and T-075 is the first time one did.** This forbade the
    # overlap outright, on the ground that no rule could honestly be excused in both directions -
    # which T-066 had already recorded as refuted and shipped the check anyway, because nothing had
    # yet had both states. DS-229 does: `component.verdicts` emits five rows under it, three
    # prohibitions that pass on an empty document and two requirements that fail on it, and all
    # five are correct. What the check was protecting against is a declaration in a table the rule
    # never reaches, and `stale` / `stale_fail` above already report exactly that - so the bar here
    # is that an overlap must be earned by rows in both directions rather than asserted.
    for rid in sorted(set(ABSENCE_IS_A_PASS) & set(ABSENCE_IS_A_FAIL)):
        if rid not in passing or rid not in failing:
            sys.exit("SELF-TEST FAILED: %s is declared in BOTH tables and only %s on a measurement "
                     "in which nothing was found. An overlap is legitimate only for a rule whose "
                     "rows genuinely split - one declaration is describing a row that does not "
                     "exist" % (rid, "passes" if rid in passing else "fails"))

    # The rows that were converted rather than declared, asserted by name. Six of the seven from
    # T-065 read keys the probe emits only inside `if (btns.length)`; the four added by T-066 are
    # DS-113 and DS-160 (a clause requiring the deck to CONTAIN the subject), DS-143 (the same, in
    # the producer this fixture could not see) and DS-135 (whose measurement moved - see the probe).
    # DS-064, DS-063, DS-200, DS-072 and DS-074 are T-075's, from `contract.py`. DS-064 is the row
    # an outside project's deck failed on; DS-200 is the same defect in the pass direction, found
    # only because this fixture finally reached that module.
    for rid in ("DS-130", "DS-164", "DS-166", "DS-146", "DS-168", "DS-228", "DS-138",
                "DS-113", "DS-160", "DS-143", "DS-135",
                "DS-064", "DS-063", "DS-200", "DS-072", "DS-074"):
        if rid not in states:
            sys.exit("SELF-TEST FAILED: %s is no longer emitted as a verdict row, so the "
                     "absent-subject assertion below is checking nothing" % rid)
        if None not in states[rid]:
            sys.exit("SELF-TEST FAILED: %s reported %s and no undecided row against a measurement "
                     "in which nothing was found. Its subject is absent, so it is undecided and "
                     "must report None - anything else decides a rule on a deck that contains "
                     "nothing for it to judge (T-065, T-066)."
                     % (rid, ", ".join(repr(o) for o in states[rid])))

    # A `guarded by` or `entailed by` claim is a testable statement about another row, so it is
    # tested. Without this the tables would be a set of comments, and a comment is what every
    # previous fix in this family left behind.
    for table, name, backing in ((ABSENCE_IS_A_PASS, "ABSENCE_IS_A_PASS", "guarded by"),
                                 (ABSENCE_IS_A_FAIL, "ABSENCE_IS_A_FAIL", "entailed by")):
        allowed = ("prohibition", "conditional") if backing == "guarded by" else ("requirement",)
        for rid, (shape, why) in sorted(table.items()):
            if len(why) < 20:
                sys.exit("SELF-TEST FAILED: %s names its subject in a phrase, not in writing" % rid)
            # A rule reaching the measurement by more than one route declares each, joined by `+`.
            # DS-143 is the case: one row is a prohibition, another a conditional, a third undecided.
            for part in [s.strip() for s in shape.split("+")]:
                if not part.startswith(backing):
                    if part not in allowed:
                        sys.exit("SELF-TEST FAILED: %s declares shape %r in %s, which is not one of "
                                 "%s, %s <rule>"
                                 % (rid, part, name, ", ".join(allowed), backing))
                    continue
                named = [g.strip() for g in part[len(backing):].split("/")]
                if not any(g in failing for g in named):
                    sys.exit("SELF-TEST FAILED: %s claims to be %s %s, and none of them fails on a "
                             "measurement in which nothing was found. The guard has stopped guarding"
                             % (rid, backing, " or ".join(named)))

    # All three states exercised on one row, because a `None` that is never contrasted with a real
    # pass and a real failure proves only that the row returns something. DS-140 is the row the task
    # was raised for, so it is the one held to it.
    def ds140(**kw):
        return {r: ok for r, _w, ok in render_verdicts(dict(empty, **kw))}["DS-140"]

    for want, state, kw in ((None, "undecided with no dashed flow", {}),
                            (True, "a pass on a dashed flow", {"currentDasharray": "7px, 6px"}),
                            (False, "a failure on a flow that is not dashed",
                             {"currentDasharray": "none"})):
        if ds140(**kw) is not want:
            sys.exit("SELF-TEST FAILED: DS-140 does not report %s - it gave %r. The fault T-051 "
                     "exists for is back, or the row has stopped deciding anything"
                     % (state, ds140(**kw)))

    # DS-231 has to be able to fail, and it has to fail for the stated reason rather than on any
    # figure the panel happens to repeat. The two documents differ in one place: whether the face
    # says the number the bottom line quotes.
    def one(face):
        return ('<section class="slide" data-name="x"><div class="body">%s</div>'
                '<div class="disc" data-disc="derivation"><div class="disc-panel">'
                '<div class="row"><span>the gate clears at 26%%</span></div></div></div>'
                '<p class="bottom-line"><b>the gate clears at 26%% and the package completes</b>'
                '</p></section>' % face)
    if split_verdicts(one("<p>26% against an 18% threshold</p>"))[0][2] is not True:
        sys.exit("SELF-TEST FAILED: DS-231 fired on a figure the face shows, which is a gate that "
                 "fails a conforming deck")
    if split_verdicts(one("<p>the committee reads it in public</p>"))[0][2] is not False:
        sys.exit("SELF-TEST FAILED: DS-231 passed a bottom line whose only support is behind the "
                 "click, which is the whole of the rule")
    # DS-232, and the pair matters more than either half: the failing case is the one that shipped
    # four blank arrowheads, and the passing case is every `<use href="#i-x">` in every deck here.
    def two(second_svg):
        return ('<section class="slide" data-name="a"><svg><defs>'
                '<marker id="m-arrow"><path d="M0 0"/></marker></defs>'
                '<path marker-end="url(#m-arrow)"/></svg></section>'
                '<section class="slide" data-name="b"><svg>%s</svg></section>' % second_svg)
    if marker_verdicts(two('<path marker-end="url(#m-arrow)"/>'))[0][2] is not False:
        sys.exit("SELF-TEST FAILED: DS-232 passed a marker defined in another slide, which is the "
                 "reference that paints nothing and the whole of the rule")
    if marker_verdicts(two('<use href="#i-source"/>'))[0][2] is not True:
        sys.exit("SELF-TEST FAILED: DS-232 fired on a sprite reference, which resolves outside "
                 "every slide and is what DS-113 requires")
    if marker_verdicts(two('<marker id="m-arrow"/><path marker-end="url(#m-arrow)"/>'))[0][2] \
            is not True:
        sys.exit("SELF-TEST FAILED: DS-232 fired on a slide carrying its own copy of the marker, "
                 "which is the fix the rule asks for")
    if magnitude("11 minutes") != magnitude("11"):
        sys.exit("SELF-TEST FAILED: a unit word changed a figure's identity, so a bottom line "
                 "citing `11 minutes` cannot be cleared by a face that shows `11`")
    if magnitude("$5.6M") == magnitude("5.6 minutes"):
        sys.exit("SELF-TEST FAILED: millions and minutes normalise to one figure")
    # T-169. `content.FIGURE` reads a time word before its numeral, and a bottom line citing
    # `month 18` has to be cleared by a face that shows `18`. Without `unreverse` this reduced to
    # the whole string and DS-231 failed the reference deck on a figure that slide shows.
    if magnitude("month 18") != magnitude("18") or magnitude("month-4") != magnitude("4"):
        sys.exit("SELF-TEST FAILED: a time word before its numeral is not the number the face "
                 "shows, so DS-231 cannot be cleared by a slide that shows it")

    # **DS-110's boundary, demonstrated on one document rather than asserted** (T-070). The same
    # raster twice: once as a slide's own figure, once as the source a quick view quotes. A rule
    # narrowed by scope is only narrowed if both halves are shown, and this is the assertion that
    # decides whether the narrowing was a narrowing or a loss.
    raster = '<img src="data:image/png;base64,iVBORw0KGgo=" alt="x">'
    produced = '<section class="slide"><div class="body">%s</div></section>' % raster
    quoted = ('<span class="sources-item"><template class="qv-src" data-qv="Survey">%s</template>'
              '</span>' % raster)
    if ds110_no_produced_raster(produced):
        sys.exit("SELF-TEST FAILED: a raster the deck produced passed DS-110. The amendment narrows "
                 "the rule by scope and does not relax it - a deck that rasterises its own content "
                 "is as much a defect after T-070 as before it")
    if not ds110_no_produced_raster(quoted):
        sys.exit("SELF-TEST FAILED: a raster inside a quick view failed DS-110, so the amendment "
                 "bought nothing: a screenshot is frequently the only form a source has")
    if ds110_no_produced_raster(produced + quoted) or not ds110_no_produced_raster(quoted + quoted):
        sys.exit("SELF-TEST FAILED: DS-110 cannot tell the two apart in one deck, which is the only "
                 "case that matters - a deck carries both")

    # **T-167's boundary, on the same pattern and for the same reason.** DS-110 was given the
    # quoted/produced distinction in T-070 and these two were not, so an adopter's deck was failed
    # for a question its SOURCE asks and would have been failed for a word its source chose. Both
    # halves are asserted here: a cut that stops the rule firing on the deck's own copy is not a
    # narrowing, it is a loss, and the last pair is the only case that matters because a real deck
    # carries both at once.
    asks = "<h3>Where are the delays?</h3>"
    banned = "<p>a seamless and pivotal result</p>"
    own = '<section class="slide"><div class="body">%s%s</div></section>' % (asks, banned)
    cited = ('<span class="sources-item"><template class="qv-src" data-qv="D1">%s%s</template>'
             '</span>' % (asks, banned))
    if ds100_no_rhetorical_questions(own):
        sys.exit("SELF-TEST FAILED: a question in the deck's own slide copy passed DS-100. T-167 "
                 "narrows the rule by scope and does not relax it")
    if not ds100_no_rhetorical_questions(cited):
        sys.exit("SELF-TEST FAILED: a question a quoted SOURCE asks failed DS-100, which is the "
                 "defect T-167 exists to fix - a deck does not write its sources' headings")
    if ds106_no_banned_terminology(own):
        sys.exit("SELF-TEST FAILED: banned terminology in the deck's own copy passed DS-106")
    if not ds106_no_banned_terminology(cited):
        sys.exit("SELF-TEST FAILED: banned terminology inside a quoted source failed DS-106 - the "
                 "deck did not choose that word, and DS-106 is a rule about the words it chose")
    if (ds100_no_rhetorical_questions(own + cited)
            or not ds100_no_rhetorical_questions(cited + cited)):
        sys.exit("SELF-TEST FAILED: DS-100 cannot tell the two apart in one deck, which is the only "
                 "case that matters - a deck carries both")
    return True


def main(deck, skip_contract=False):
    render.self_test()
    contrast.self_test()
    contract.self_test()
    html = open(deck, "r", encoding="utf-8").read()
    print("browser: %s" % render.CHROME)
    print("deck:    %s" % paths.display_path(deck, ROOT))

    print("\n=== stage 1  auto gate (static)")
    failures = []
    for rule, what, fn in STATIC:
        good = fn(html)
        if not good:
            failures.append(rule)
        print("  %-8s %-50s %s" % (rule, what, ok(good)))

    print("\n=== stage 2  contrast (WCAG 2.2 AA, DESIGN-SYSTEM §7)")
    cfails = contrast.audit(html, verbose=False)
    print("  %d failure(s)" % len(cfails))
    for theme, label, fg, bg, r, need in cfails:
        print("    %-6s %-32s %.2f:1 (needs %.1f)" % (theme, label, r, need))
        failures.append("contrast/%s" % label)

    data, err = render_data(deck)
    if not data:
        print("\n=== stage 3  render gate: NO RESULT\n%s" % err[:400])
        return 1

    print("\n=== stage 3  render gate (measured, viewport %d)" % data["vw"])
    rows = render_verdicts(data)
    for rule, what, good in rows:
        if good is False:
            failures.append(rule)
        print("  %-15s %-58s %s" % (rule, what, ok(good)))

    # Reported, not gated. No rule requires a deck to carry a figure at all, and DS-111 governs what
    # a diagram is MADE OF, which a count cannot decide. This was a DS-111 verdict passing on `> 0`
    # until T-038 - a check that fails the all-canvas deck DS-111 explicitly permits, and passes a
    # deck whose other eleven figures are card grids.
    print("      inline SVG figures: %d  (measured, not gated)" % data["figures"])
    for du, text, slide in data["underFloor"][:6]:
        print("      %5.1f du  %-32s  [%s]" % (du, text, slide))
    for slide, text, fg, bg, r in data.get("renderedLowContrast", [])[:8]:
        print("      %-30s %-24s %s on %s = %.2f:1" % (slide[:30], text, fg, bg, r))
    for slide, text, attr, actual in data.get("deadFillAttributes", [])[:8]:
        print("      %-30s %-24s wrote %s, renders %s" % (slide[:30], text, attr, actual))
    for name, slide in data["infinite"][:6]:
        tag = "ambient" if [name, slide] in data.get("ambient", []) else "flow (DS-140)"
        print("      looping %-14s %-14s [%s]" % (name, tag, slide))

    # Stage 4 is a second and a third pass of the browser, so it is opt-out: the resolution
    # contract is a claim about what happens BETWEEN viewports and one render cannot decide it.
    if not skip_contract:
        print("\n=== stage 4  resolution contract (DESIGN-SYSTEM §2.4, §2.5)")
        for rule, what, good in contract.audit(deck, quiet=True):
            if not good:
                failures.append(rule)
            print("  %-15s %-4s  %s" % (rule, ok(good), what))
        if contract.UNCHECKED:
            print(contract.UNCHECKED)

    print("\n%d mechanical failure(s): %s" % (len(failures), ", ".join(failures) or "none"))
    print("""
This gate covers the `auto` and `render` rules only. **Five of the ten evaluation dimensions -
S1 Claim, S2 Evidence, S4 Density, D1 Spine, D4 Consistency - are invisible to it**, and were
proven so against a seeded-defect deck. A clean run here is not a good deck; it is a deck with no
defect this gate was built to see (L-05, DS-191).""")
    return 1 if failures else 0


if __name__ == "__main__":
    deck = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(
        ROOT, "examples", "reference-deck.html")
    sys.exit(main(deck))
