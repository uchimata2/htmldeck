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
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render                                                       # noqa: E402
import contrast                                                     # noqa: E402
import contract                                                     # noqa: E402
import theme                                                        # noqa: E402

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
    a theme value that could differ between themes, it is the paper."""
    c = screen_css(h)
    for body in blocks(c, r":root(?:\s*\[[^\]]*\])?"):
        c = c.replace(body, "")
    return re.sub(r"/\*.*?\*/", "", c, flags=re.S)


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


# DS-140's two long motions, **by the token that carries each**. Until T-007 this was a pair of
# exact seconds, 1.2 and 4.5, and the check admitted any duration matching one of them. Banding
# those numbers broke the check in a way the variant suite caught immediately: a 900 ms slide
# transition falls inside Pulse-once's 0.8-1.6 s band and was waved through, because a scan over
# durations cannot tell which motion a number belongs to.
#
# **DS-141's own words are the fix** - Pulse-once and Current are conformant *by name*. So a
# duration over the cap is licensed when the declaration reads it out of one of these two tokens,
# and the band each token must sit in is the contract's business (`theme.py`, DS-140).
DS140_LONG_TOKENS = ("--pulse-dur", "--current-dur")


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
    """DS-141 - entry and transition animations max 500 ms, with DS-140's named vocabulary as the
    specific override. So: every duration over 500 ms is read out of one of DS-140's two long
    motions **by name**, which is the licence the rule's own sentence grants.

    **Only duration-bearing declarations are read.** `animation-delay:600ms` is not a duration and
    scanning the file for `\\d+s` counted one, alongside six fragments of an embedded typeface."""
    c = css(h)
    toks = _custom_properties(c)
    for value in re.findall(r"\b(?:animation|transition)(?:-duration)?\s*:\s*([^;{}]+)", c):
        if any(t in value for t in DS140_LONG_TOKENS):
            continue                     # named, so DS-140 governs it and DS-141 yields (F-04)
        for m in re.finditer(r"(\d+(?:\.\d+)?)(ms|s)\b", _expand_vars(value, toks)):
            if float(m.group(1)) / (1000.0 if m.group(2) == "ms" else 1.0) > 0.5:
                return False
    return True


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
STATIC = [
    ("DS-001", "zero external references",
     lambda h: not [u for u in re.findall(
         r'(?:src|href|xlink:href)\s*=\s*["\']([^"\']+)["\']', h)
         if not u.startswith(("data:", "#", "blob:"))]),
    ("DS-003", "meta charset present",
     lambda h: '<meta charset="utf-8">' in h.lower()),
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
    ("DS-110", "no raster images",
     lambda h: not re.search(r"<img\b", h) and "data:image/png" not in h
     and "data:image/jpeg" not in h),
    ("DS-122", "no chart library",
     lambda h: not any(x in h.lower() for x in
                       ("chart.js", "d3.min", "plotly", "highcharts", "echarts"))),
    ("DS-100", "no rhetorical questions in slide copy",
     lambda h: not re.search(r"\?\s*<", h)),
    ("DS-106", "no banned terminology",
     lambda h: not re.search(r"\b(crucial|pivotal|seamless|leverage|synerg\w*|friction|"
                             r"genuinely|arguably|precisely|delve)\b", h, re.I)),
    # ---- added by T-005, closing rules that were labelled `auto` and checked by nothing (L-36)
    ("DS-002", "no CDN host referenced - `linked` is not a shipping mode",
     lambda h: not re.search(r"cdn\.|unpkg\.com|jsdelivr|cdnjs|googleapis\.com", h, re.I)),
    ("DS-005", "no fetch, XHR or dynamic import - element access, not file reads",
     lambda h: not re.search(r"\bfetch\s*\(|XMLHttpRequest|\bimport\s*\(", h)),
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
    ("DS-141", "no duration over 500 ms outside DS-140's vocabulary", ds141_durations),
    ("DS-144", "no 3D transform on a slide transition", ds144_no_3d_between_slides),
    ("DS-163", "no :hover rule revealing content", ds163_no_hover_only),
    ("DS-165", "the disclosure mark is not restyled per slide", ds165_one_disclosure_mark),
]

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

    // DS-140/142 - DS-140 sanctions exactly one looping motion, `Current`, for flows. Anything
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
    out.motionControl = !!document.getElementById('motion');

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
      // DS-135 - the page title and the nav-bar name for that page must match. Read AFTER a
      // navigation, because on slide one the deck's own title collapses to the deck name and the
      // check would be true of any title at all.
      out.titleCarriesSlide = document.title.indexOf(slides[at()].dataset.name) >= 0;
      out.titleSample = [document.title, slides[at()].dataset.name];
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
      out.at320Overflowing = Array.prototype.filter.call(doc.querySelectorAll('#docBody *'),
        function(el){ return el.getBoundingClientRect().width > 321; }).length;
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
            ("DS-143", "risen elements hidden under reduced motion: %d of %d on the current slide"
             % (data.get("risenHidden", 0), data.get("risen", 0)),
             data.get("risen", 0) > 0 and data.get("risenHidden", 0) == 0)]
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
    "DS-035": ("prohibition", "no text run under 16 design units; the subject is the deck's text"),
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
    "DS-132": ("prohibition", "nothing tabbable on an off-screen slide"),
    "DS-142": ("prohibition", "no looping motion on static content"),
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
}

# The keys the probe emits unconditionally, so a measurement without them is malformed rather than
# empty. `self_test` builds its nothing-was-found measurement from exactly these; if a verdict grows
# a `data[...]` access to something outside the set, the self-test says so by name.
ALWAYS_MEASURED = ("slideCount", "underFloor", "longHeadlines", "tabbablesOffscreen",
                   "smallTargets", "panelsOpenInitially", "motionControl", "infinite")


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
        # **The third, `<= 3 supporting fragments`, is excused and this is the argument.** Nothing
        # in the DOM marks a run as a supporting fragment, and counting tier-one runs instead puts
        # three slides of the conforming deck over budget at 4, 5 and 9 - on the eyebrow
        # (`03 · The problem`), a stat figure and its label (`11` / `minutes, average wait`, which
        # is one thing and not two), the assumption marker and the provenance mark. Those are
        # required by DS-104 and DS-105, so the count would set three rules against each other, and
        # any threshold that spared them would be a number chosen to fit this deck (**L-38**).
        # CLOSES WHEN: a supporting fragment is structurally identifiable - a class, a container, a
        # list - which is a rule amendment and the owner's. Adopting markup to make a check work is
        # backwards, which is the DS-026 precedent.
        ("DS-091", "slides without exactly one headline: %d%s"
         % (len(data.get("headlineCounts", [])),
            "" if not data.get("headlineCounts")
            else "  %s" % ", ".join("%s has %d" % (n, c) for n, c in data["headlineCounts"][:3])),
         not data.get("headlineCounts")),
        ("DS-091", "headlines over six words: %d" % len(data["longHeadlines"]),
         not data["longHeadlines"]),
        ("DS-202", "slides with no bottom line: %d" % len(data.get("noBottomLine", [])),
         not data.get("noBottomLine")),
        ("DS-202", "bottom lines that are not one sentence: %d"
         % len(data.get("multiSentence", [])), not data.get("multiSentence")),
        ("DS-205", "bottom lines behind a disclosure: %d" % len(data.get("bottomLineHidden", [])),
         not data.get("bottomLineHidden")),
        ("DS-203", "prose outranking the bottom line: %d" % len(data.get("outranked", [])),
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
        # `is True`, not `is not False`: a null means the probe never found a control to measure,
        # and a gate must fail on "nothing measured" rather than pass on it (L-36).
        ("DS-130", "disclosure control in the tab order: %s" % data.get("currentDiscReachable"),
         data.get("currentDiscReachable") is True),
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
        ("DS-142", "looping motion on static content: %d" % len(data.get("ambient", [])),
         not data.get("ambient")),
        ("DS-218", "control for motion over 5s: %s (%d looping)"
         % (data["motionControl"], len(data["infinite"])),
         len(data["infinite"]) == 0 or data["motionControl"]),
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
        ("DS-073", "sections carrying less text than their slide: %d"
         % len(data.get("docShorterThanSlide", [])), not data.get("docShorterThanSlide")),
        # Two nulls compare equal, so a deck with no reflow view reported a pass here on
        # `None == None`. DS-070 goes red in that case, so no deck escaped the run - but the row
        # itself was still claiming a rule it had not decided (T-051).
        ("DS-073", "tier-two panels open in the reflow view: %s/%s"
         % (data.get("docPanelsOpen"), data.get("docPanelsTotal")),
         None if data.get("docPanelsTotal") is None
         else data["docPanelsOpen"] == data["docPanelsTotal"]),
        ("DS-075", "reflow scrollWidth at 320 CSS px: %s (overflowing: %s)"
         % (data.get("at320ScrollWidth"), data.get("at320Overflowing")),
         data.get("at320ScrollWidth", 999) <= 321 and data.get("at320Overflowing") == 0),
        ("DS-076", "position preserved returning from the reflow view: left %r, back on %r"
         % (data.get("leftFrom"), data.get("backOnSlide")),
         bool(data.get("backOnSlide")) and data.get("backOnSlide") == data.get("leftFrom")),
        ("DS-214", "dead fill= attributes overridden by CSS: %d"
         % len(data.get("deadFillAttributes", [])), not data.get("deadFillAttributes")),
        ("DS-215", "text runs rendering under 4.5:1: %d"
         % len(data.get("renderedLowContrast", [])), not data.get("renderedLowContrast")),
        # ---- added by T-005
        ("DS-080", "slides that are not a <section>: %d" % len(data.get("notSections", [])),
         not data.get("notSections")),
        ("DS-092", "sentences over 20 words: %d, paragraphs over 4 sentences: %d"
         % (len(data.get("longSentences", [])), len(data.get("longParagraphs", []))),
         not data.get("longSentences") and not data.get("longParagraphs")),
        ("DS-113", "sprite icons never used: %d of %d"
         % (len(data.get("unusedSymbols", [])), data.get("symbolCount", 0)),
         not data.get("unusedSymbols") and data.get("symbolCount", 0) > 0),
        ("DS-135", "the page title carries the slide's name: %s (%r)"
         % (data.get("titleCarriesSlide"), data.get("titleSample")),
         data.get("titleCarriesSlide") is True),
        ("DS-164", "disclosure controls with no real label: %d of %d"
         % (len(data.get("unlabelledDiscControls", [])), data.get("discControls", 0)),
         not data.get("unlabelledDiscControls") and data.get("discControls", 0) > 0),
        ("DS-166", "arrow advances with everything closed: %s; the toggle does not advance: %s"
         % (data.get("arrowAdvancesClosed"), data.get("toggleDoesNotAdvance")),
         data.get("arrowAdvancesClosed") is True and data.get("toggleDoesNotAdvance") is True),
        ("DS-146", "the played mark survives navigating away and back: %s"
         % data.get("playedSurvivesReturn"), data.get("playedSurvivesReturn") is True),
        # DS-026 is measured (`rolesWithoutLegend`) and NOT emitted as a verdict: the rule wants a
        # *visible* legend and the tripwire slide draws one as two unmarked SVG swatches, which a
        # class-based check reports as missing. Excused in `check.py`, with the argument.
        ("DS-043", "boxes nested in a box that has its own text: %d"
         % len(data.get("nestedTextBoxes", [])), not data.get("nestedTextBoxes")),
        ("DS-160", "third-tier disclosure inside a panel: %d, over %d panel(s)"
         % (data.get("thirdTier", 0), data.get("panelCount", 0)),
         not data.get("thirdTier") and data.get("panelCount", 0) > 0),
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

    `render_verdicts` is pure, so the fourth instance costs one dictionary and no browser: build the
    measurement a probe returns when it finds nothing, run every row against it, and require each
    row that still passes to be declared in `ABSENCE_IS_A_PASS` with its shape and its subject. A
    row added tomorrow with a `.get()` default that passes has to be argued for in writing before
    the gate will run at all.
    """
    empty = dict.fromkeys(ALWAYS_MEASURED, 0)
    empty.update({"underFloor": [], "longHeadlines": [], "infinite": [], "motionControl": None})
    try:
        rows = render_verdicts(empty)
    except KeyError as exc:
        sys.exit("SELF-TEST FAILED: a verdict reads data[%s] unconditionally, so it is not in "
                 "ALWAYS_MEASURED and the nothing-was-found measurement cannot be built. Add the "
                 "key there if the probe always emits it, or read it with .get()" % exc)

    passing = sorted({r for r, _w, ok in rows if ok is True})
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

    # A `guarded by` claim is a testable statement about another row, so it is tested. Without this
    # the table would be a set of comments, and a comment is what three previous fixes left behind.
    failing = {r for r, _w, ok in rows if ok is False}
    for rid, (shape, why) in sorted(ABSENCE_IS_A_PASS.items()):
        if not shape.startswith("guarded by"):
            if shape not in ("prohibition", "conditional"):
                sys.exit("SELF-TEST FAILED: %s declares shape %r, which is not one of "
                         "prohibition, conditional, guarded by <rule>" % (rid, shape))
            continue
        guards = [g.strip() for g in shape[len("guarded by"):].split("/")]
        if not any(g in failing for g in guards):
            sys.exit("SELF-TEST FAILED: %s claims to be guarded by %s, and none of them fails on a "
                     "measurement in which nothing was found. The guard has stopped guarding"
                     % (rid, " or ".join(guards)))
        if len(why) < 20:
            sys.exit("SELF-TEST FAILED: %s names its subject in a phrase, not in writing" % rid)

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
    return True


def main(deck, skip_contract=False):
    render.self_test()
    contrast.self_test()
    contract.self_test()
    html = open(deck, "r", encoding="utf-8").read()
    print("browser: %s" % render.CHROME)
    print("deck:    %s" % os.path.relpath(deck, ROOT))

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
