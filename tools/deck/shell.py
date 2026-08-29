#!/usr/bin/env python3
"""The deck shell: instantiate it, keep the sprite honest, and prove a deck still matches it.

A deck is 225 KB of which roughly 170 KB is the same in every deck ever built here - the embedded
faces, the shared component block, the script, the chrome and the reading view. **That half cannot
be authored per run**, and copying it into a second file is how two copies of one fact start
disagreeing. So it lives in `shell/`, cut out of `examples/reference-deck.html` losslessly, and
this tool is what puts it back.

    python tools/deck/shell.py new <out.html> --title "..." --subtitle "..."
    python tools/deck/shell.py icons <deck> [--set concept=lucide,...] [--check]
    python tools/deck/shell.py icons --sheet <out.svg>
    python tools/deck/shell.py preflight <deck> [--check]
    python tools/deck/shell.py sync <deck> [--write]
    python tools/deck/shell.py tokens <deck> [--write]
    python tools/deck/shell.py tail <deck> [--write]
    python tools/deck/shell.py check <deck>
    python tools/deck/shell.py parts

**`check` is the reason the other commands are trustworthy.** It cuts the same regions `SLOTS` names out of
the deck and compares what is left with `shell/shell.html` byte for byte, so a batch edit that
strayed into the shared block is a red run rather than a discovery two decks later. The stale
fixture (**L-05**) is the same failure in a different file.

**`sync` is what `check` leaves you needing.** A release that touches `shell/` makes every deck
already built fail that comparison through no fault of its author, and for three releases running
there was no command to name (T-124). It reports by default and writes on `--write`, which inverts
`icons` and `preflight` deliberately: those derive a region from the deck's own content, while this
one overwrites the deck's shell with a foreign one and cannot tell a version gap from a deliberate
edit.

**`tokens` is what `sync` cannot do.** A release can add a token to the shared block, and the block
is shell while the declaration is a theme value in a per-deck region `sync` must not touch - so the
upgrade succeeds, `check` passes, and DS-013 fails on a token the adopter never had a chance to
declare (T-166). `sync` and `check` both name them now; `tokens --write` adds exactly the missing
ones, at the shipped theme's values, and never rewrites one already there.

Runs its own self-test first and refuses to report if it fails (**L-04**). Pure standard
library (**L-07**).
"""

import io
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths                                                        # noqa: E402
import preflight as preflight_mod  # noqa: E402  - a sibling tool, not a package
import theme as theme_mod  # noqa: E402  - a sibling tool, not a package

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SHELL = os.path.join(ROOT, "shell")
SHELL_HTML = os.path.join(SHELL, "shell.html")
COMPONENTS = os.path.join(SHELL, "components.css")
DECK_JS = os.path.join(SHELL, "deck.js")
ICONS = os.path.join(SHELL, "icons.svg")
DEFAULT_THEME = os.path.join(ROOT, "themes", "quarto.css")

# The regions a deck varies in. Everything else is the shell.
# **The count lives here and is derived everywhere it is read** (`PR-55`). It used to be
# written out in four other places and they disagreed: a docstring said ten, `parts` printed
# eleven directly above a list of twelve, and the SKELETON refusal an adopter reads said
# ten. Both additions labelled themselves at the definition - *Eleventh, added by T-019*,
# *Twelfth, added by T-114* - so the count moved here and nowhere a reader meets it.
#
# The delimiters are literals rather than patterns on purpose: they are compared, not merely
# found, so a deck whose chrome comment has drifted has to fail rather than be re-anchored around.
#   (slot, opening delimiter, closing delimiter, what it is)
SLOTS = (
    ("TITLE", "<title>", "</title>", "the browser tab and the deck's name"),
    ("NOTE", "<!--\n", "\n\n  EMBEDDED FONT LICENCES", "the head comment above the licences"),
    ("THEME", '<style id="theme">', "</style>", "the theme region (THEME-CONTRACT.md)"),
    ("COMPONENTS", "\n<style>", "</style>", "the shared component block"),
    # Eleventh, added by T-019. It is a region rather than shell for the same reason the sprite is:
    # what it holds is derived from the deck's own content, so two decks legitimately differ here.
    ("PREFLIGHT", '<script id="preflight">', "</script>",
     "the capability preflight, only the rows used (DS-009)"),
    ("ICONS", " </defs>\n", "\n</svg>", "the sprite, only the icons used (DS-113)"),
    ("SLIDES", '<main class="stage" id="stage" aria-label="Presentation">\n',
     "\n<!-- ============================================================ chrome -->",
     "every <section class=\"slide\">"),
    # Twelfth, added by T-114 for a control with a varying PARENT, and now carrying one form
    # (T-277). DS-218's placement clause was reversed on 2026-08-29: a control one click inside a
    # persistent, keyboard-operable menu button counts as reachable, so `Motion` sits inside
    # `.more-menu` on every deck and nothing about it varies. **The slot stays**, because it is the
    # region a deck may reword and `shell.py check`'s byte comparison must not own - which is what
    # T-114 spent to buy it, and is unrelated to the placement question that has since gone away.
    ("CHROME_TAIL", "<!-- chrome-tail -->\n", "\n</nav>",
     "the chrome row's tail: `More`, and `Motion` inside its menu (DS-218)"),
    ("DOC_TITLE", '<h1 class="t">', "</h1>", "the reading view's heading"),
    ("DOC_SUB", '<p class="s">', "</p>", "the reading view's standfirst"),
    ("COMPOSITION", '<style id="slides">', "</style>", "this deck's own layout"),
    ("SCRIPT", "<script>", "</script>", "the deck script"),
)

# Three of those regions turned out to nest. The script is not wholly shell: it names the deck,
# the stages of its argument and the icon that marks each - per-deck facts that were sitting in
# the middle of 560 invariant lines, which is why nothing had noticed them.
SCRIPT_SLOTS = (
    ("DECK_NAME", "var DECK = '", "';", "the deck's name, as the ruler says it"),
    ("STAGES", "var STAGES = [", "];", "the stages of the argument (DS-134)"),
    ("STAGE_ICON", "var STAGE_ICON = [", "];", "one icon per stage, `i-` names"),
)

SYMBOL = re.compile(r'<symbol\s+id="([^"]+)"([^>]*)>(.*?)</symbol>', re.S)

# **An icon reference is not always markup.** The reference deck's stage icons are named in a
# script array and put into the DOM at runtime - the `script` source the component contract
# names - so a scan reading only `<use>` concludes four of its nine icons are unused and deletes
# them. Both forms count, and neither pattern may be loosened to a bare `i-name`: that matches
# `--ui-line` five times in the deck it was first run on.
REFERENCE = re.compile(r'href="#i-([A-Za-z0-9_-]+)"'          # <use href="#i-wait">
                       r"|'i-([A-Za-z0-9_-]+)'"               # 'i-gate' in the script
                       r'|"i-([A-Za-z0-9_-]+)"')              # "i-gate", same thing
DATA_ICON = re.compile(r'\sdata-icon="([^"]+)"')
SYMBOL_ATTRS = ('viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
                'stroke-linecap="round" stroke-linejoin="round"')


def read(path):
    return io.open(path, encoding="utf-8", newline="").read()


def write(path, text):
    with io.open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


# ------------------------------------------------------------------------------- cut and fill


class NotAShell(Exception):
    """The file does not have the shell's structure, and says which anchor is missing."""


def cut(text, slots=SLOTS):
    """`(skeleton, parts)` - the shell with `{{SLOT}}` where the deck varies, and what was there.

    Filling the skeleton back in reproduces `text` exactly; that property is what the self-test
    asserts, and it is the whole basis for calling `shell/` the deck's one home rather than a
    description of it.
    """
    parts, out, pos = {}, [], 0
    for slot, opener, closer, _what in slots:
        start = text.find(opener, pos)
        if start < 0:
            raise NotAShell("no %s anchor - expected %r" % (slot, opener))
        a = start + len(opener)
        b = text.find(closer, a)
        if b < 0:
            raise NotAShell("%s opens at %d and never closes - expected %r" % (slot, a, closer))
        parts[slot] = text[a:b]
        out.append(text[pos:a])
        out.append("{{%s}}" % slot)
        pos = b
    out.append(text[pos:])
    return "".join(out), parts


def fill(skeleton, parts):
    for slot, body in parts.items():
        skeleton = skeleton.replace("{{%s}}" % slot, body, 1)
    return skeleton


# ------------------------------------------------------------------------------- new


NOTE_DEFAULT = """  Built by htmldeck. One self-contained file: every font, icon, script and style is
  inlined, and it renders with the network disabled (DS-001)."""


# The tail every deck gets, looping or not (T-277). There was a second form until 2026-08-29, for
# a deck with looping motion, which lifted `Motion` out to sit beside `.more` - DS-218's placement
# clause, added by T-114 step 7a on the reading that a stop one click inside a shut menu is not
# reachable. **The owner reversed that ruling the same day it was made**: WCAG 2.2.2 asks that the
# stop be reachable while the motion runs, not that it be zero clicks, and a persistent,
# keyboard-operable menu button satisfies it. So the parent stopped varying and the two forms
# collapsed here - a flag selecting between identical forms being worse than no flag.
#
# What DS-218 still decides about this markup is the other half, and it is not vacuous: the
# control must exist and its opener must be a real, reachable button. `PR-78` measured what a tail
# missing one of these does - the deck refuses to start - and neither `shell.py check` nor
# `component.py` catches it, because the tail is the one region a deck may reword.
CHROME_TAIL = """  <div class="more" id="more">
    <button class="btn" id="moreBtn" aria-expanded="false" aria-controls="moreMenu">More</button>
    <div class="more-menu" id="moreMenu" hidden>
      <button class="btn" id="toDoc">Read</button>
      <button class="btn" id="motion" aria-pressed="false">Motion on</button>
    </div>
  </div>"""


def tail(html):
    """The deck, with the chrome tail in the one form DS-218 now asks for.

    Takes no answer about the deck's motion any more. It used to: the placement depended on
    whether anything looped, which only `audit.py` can measure - and that dependency is what the
    2026-08-29 reversal removed (T-277). Idempotent: a deck already carrying the form is returned
    unchanged, which is what makes this safe to run over the tracked decks in a sweep.
    """
    skeleton, parts = cut(migrate(html))
    parts["CHROME_TAIL"] = CHROME_TAIL
    return fill(skeleton, parts)


def new(title, subtitle, note=None, theme_css=DEFAULT_THEME, stages=None, stage_icons=None):
    """A deck with the shell in place and no slides yet."""
    resolved = theme_mod.resolve(read(theme_css))
    stages = stages or ["Claim"]
    # `[(concept, lucide)]`. The concept is the deck's word for the idea and the glyph is what
    # draws it - DS-114 is about the first and DS-112 about the second, and conflating them is how
    # a deck ends up with `i-circle-check` twice under two names.
    stage_icons = stage_icons or [("info", "info")] * len(stages)
    script = fill(read(DECK_JS), {
        "DECK_NAME": title.replace("'", "\\'"),
        "STAGES": ",".join("'%s'" % s.replace("'", "\\'") for s in stages),
        "STAGE_ICON": ",".join("'i-%s'" % concept for concept, _glyph in stage_icons),
    })
    parts = {
        "TITLE": escape(title),
        "NOTE": note if note is not None else NOTE_DEFAULT,
        "THEME": "\n%s\n" % resolved.strip("\n"),
        "COMPONENTS": read(COMPONENTS),
        # Empty here and derived below, once there is a deck to read it off. It cannot be decided
        # before the components and the theme are in place: `var(--` is what puts the first row in.
        "PREFLIGHT": "",
        "ICONS": "",
        # The marker is a comment rather than a stub slide: a placeholder headline is copy nobody
        # wrote, and DS-090 wants a claim there.
        #
        # **And it writes no tag, which is T-191.** It used to spell the example out as
        # `<section class="slide">`, inside the comment - and four tools split a deck with a regex
        # over exactly that string, so the comment opened a phantom slide and `FIG-1` reported the
        # `3.2` after it as an unsourced figure on slide 1. `content.strip_comments` is the fix
        # that holds for any comment; this is the other half, so a deck built by an older copy of
        # this tool is not carrying the trap in the first place.
        "SLIDES": "\n<!-- slides go here, one section.slide each "
                  "(COMPONENT-CONTRACT.md 3.2) -->\n",
        # One form, whatever the deck goes on to animate (T-277). What `audit.py` still decides
        # about this region is that the control and its opener are there and reachable, not where
        # they sit.
        "CHROME_TAIL": CHROME_TAIL,
        "DOC_TITLE": escape(title),
        "DOC_SUB": escape(subtitle),
        "COMPOSITION": "\n/* this deck's own layout. The look is the theme region's; "
                       "the components are the shared block's. */\n",
        "SCRIPT": script,
    }
    # Neither derived region is left to be remembered: whatever the stages reach for is wired now,
    # and the preflight is read off the result.
    return apply_preflight(apply_icons(fill(read(SHELL_HTML), parts), dict(stage_icons)))


def escape(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ------------------------------------------------------------------------------- icons


def library(path=ICONS):
    """`{lucide name: inner markup}` for the shipped set."""
    return dict((m.group(1), m.group(3)) for m in SYMBOL.finditer(read(path)))


def deck_icons(html):
    """`[concept]` in first-use order - every icon the deck reaches for, markup or script.

    The sprite itself is excluded, or every symbol would count as its own reference and DS-113
    would be unfalsifiable.
    """
    try:
        _skeleton, parts = cut(html)
        body = html.replace(parts["ICONS"], "", 1) if parts["ICONS"] else html
    except NotAShell:
        body = html
    seen, order = set(), []
    for match in REFERENCE.finditer(body):
        name = match.group(1) or match.group(2) or match.group(3)
        if name not in seen:
            seen.add(name)
            order.append(name)
    return order


def declared(html):
    """`{concept: lucide}` from the sprite's own `data-icon` attributes."""
    _skeleton, parts = cut(html)
    out = {}
    for m in SYMBOL.finditer(parts["ICONS"]):
        ident, attrs = m.group(1), m.group(2)
        if ident.startswith("i-"):
            found = DATA_ICON.search(attrs)
            out[ident[2:]] = found.group(1) if found else None
    return out


def sprite(concepts, mapping, lib):
    """The ICONS region for exactly `concepts`, in order. DS-113 as an output rather than a rule."""
    lines = []
    for concept in concepts:
        glyph = mapping.get(concept)
        if not glyph:
            raise NotAShell("icon `i-%s` is used and nothing says which Lucide glyph it is - "
                            "pass --set %s=<lucide-name>" % (concept, concept))
        if glyph not in lib:
            raise NotAShell("`%s` is not in shell/icons.svg. Add it there once, with its licence, "
                            "rather than drawing it here (DS-112)" % glyph)
        lines.append(' <symbol id="i-%s" data-icon="%s" %s>%s</symbol>'
                     % (concept, glyph, SYMBOL_ATTRS, lib[glyph]))
    return "\n".join(lines)


def apply_icons(html, sets=None, lib=None):
    """`html` with its sprite rewritten to hold exactly the icons the slides use."""
    lib = lib if lib is not None else library()
    mapping = dict((k, v) for k, v in declared(html).items() if v)
    mapping.update(sets or {})
    skeleton, parts = cut(html)
    parts["ICONS"] = sprite(deck_icons(html), mapping, lib)
    return fill(skeleton, parts)


# ------------------------------------------------------------------------------- preflight


def apply_preflight(html):
    """`html` with its preflight rewritten to hold exactly the rows this deck needs (DS-009).

    The same sentence as `apply_icons`, one region along: what belongs in it is a fact about the
    deck's own bytes, so it is read off the deck rather than declared. `preflight.block` strips any
    block already present before it scans, or the probe source would be evidence about the deck.
    """
    skeleton, parts = cut(html)
    parts["PREFLIGHT"] = preflight_mod.block(html)
    return fill(skeleton, parts)


def sheet(lib=None):
    """A contact sheet, so the set can be looked at rather than trusted (**L-01**)."""
    lib = lib if lib is not None else library()
    names = sorted(lib)
    cols, cell = 6, 120
    rows = (len(names) + cols - 1) // cols
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
           'viewBox="0 0 %d %d" fill="none" stroke="#23211D" stroke-width="2" '
           'stroke-linecap="round" stroke-linejoin="round">'
           % (cols * cell, rows * cell, cols * cell, rows * cell),
           '<rect width="100%%" height="100%%" fill="#F3F0E8" stroke="none"/>']
    for i, name in enumerate(names):
        x, y = (i % cols) * cell, (i // cols) * cell
        out.append('<g transform="translate(%d,%d) scale(2)">%s</g>' % (x + 36, y + 24, lib[name]))
        out.append('<text x="%d" y="%d" text-anchor="middle" font-family="monospace" '
                   'font-size="11" fill="#5F594E" stroke="none">%s</text>'
                   % (x + cell // 2, y + 96, name))
    out.append("</svg>")
    return "\n".join(out)


# ------------------------------------------------------------------------------- sync


# **What `sync` cannot carry on its own, and why this is a table rather than a looser `cut`.**
# `cut` finds a slot by a literal delimiter, so the release that ADDS a slot leaves every existing
# deck with no anchor for it: `check` reports NOT A SHELL, and `sync` - the one command that
# repairs a deck - cannot read the deck in order to repair it. The tempting fix is to let a missing
# anchor default silently, and that spends the property the literals were chosen for: a deck whose
# markup had drifted would stop failing.
#
# So the anchor is INSTALLED instead, by an exact replacement that is itself checked. Each entry is
# `(what the previous shell shipped, what replaces it, the task that needed it)`. A deck already
# carrying the anchor matches nothing and is untouched; a deck carrying neither still fails `cut`,
# loudly, which is the case the literals exist for.
MIGRATIONS = (
    ("""    <button class="btn" id="toDoc">Read</button>
    <button class="btn" id="motion" aria-pressed="false">Motion on</button>
  </div>
</nav>""",
     """  </div>
  <!-- chrome-tail -->
%s
</nav>""",
     "T-114: the chrome row's tail became a slot, and `Read` and `Motion` left the "
     "navigation container"),
)


def migrate(html):
    """The deck, with any anchor a later release added installed at its literal old position.

    Ordered and idempotent: an entry whose old text is absent - because the deck is already
    current, or because it never had that shell - is skipped, and nothing else is touched. `sync`
    runs this before `cut`; `check` does NOT, so an un-migrated deck still reports rather than
    being quietly read as current.

    **The migrated tail puts `Read` and `Motion` both into the menu**, which since 2026-08-29 is
    the only form there is (T-277). It was the default of two until then, and a deck with looping
    motion failed DS-218 until someone moved `Motion` back out; the reversal removed the second
    form, so migrating now lands a deck in its final shape rather than in a shape a gate objects to.
    """
    for old, new, _why in MIGRATIONS:
        if "%s" in new:
            new = new % CHROME_TAIL
        if old in html:
            html = html.replace(old, new, 1)
    return html



def sync(html):
    """The deck, with the **installed** shell under its own regions (T-124).

    `cut` gives the deck's parts and throws its shell away; filling `shell/shell.html` with those
    parts is the same operation in the other direction, and that is the whole upgrade. The script
    nests, so its three per-deck declarations are cut out and put back into the shipped `deck.js`.

    **Why this needs to exist.** `check` compares three regions byte for byte, which is what makes
    the shared half trustworthy (T-085) - and the other edge of it is that any release touching
    `shell/` makes every deck already in the world fail, through no fault of its author. Until this
    command there was nothing to run: `new` builds an empty deck, and pointing it at a deck with
    slides in it is not an upgrade path. Three releases in a row could not name a smallest edit.
    """
    html = migrate(html)
    _skeleton, parts = cut(html)
    _script_skeleton, script_parts = cut(parts["SCRIPT"], SCRIPT_SLOTS)
    parts["SCRIPT"] = fill(read(DECK_JS), script_parts)
    parts["COMPONENTS"] = read(COMPONENTS)
    return fill(read(SHELL_HTML), parts)


def kept(html):
    """Every per-deck part, flattened - the ten top-level regions that are not the component block,
    with the script replaced by the three declarations nested inside it.

    This is what a sync must not touch, and comparing it before and after is the whole guarantee."""
    _skeleton, parts = cut(html)
    _script_skeleton, script_parts = cut(parts["SCRIPT"], SCRIPT_SLOTS)
    out = dict((k, v) for k, v in parts.items() if k not in ("COMPONENTS", "SCRIPT"))
    out.update(script_parts)
    return out


def changes(before, after):
    """`[(region, note)]` - what a sync moved, region by region.

    An adopter is being asked to accept a rewrite of a 250 KB file they cannot read, so the command
    that does it owes them a statement of where. Line counts plus the first difference is enough to
    tell a shell that moved from an edit of their own being reverted, which is the distinction no
    program here can make for them."""
    rows = []
    for name, old, new_ in (("SKELETON", cut(before)[0], cut(after)[0]),
                            ("COMPONENTS", cut(before)[1]["COMPONENTS"],
                             cut(after)[1]["COMPONENTS"]),
                            ("SCRIPT", cut(cut(before)[1]["SCRIPT"], SCRIPT_SLOTS)[0],
                             cut(cut(after)[1]["SCRIPT"], SCRIPT_SLOTS)[0])):
        if old == new_:
            continue
        rows.append((name, "%d lines -> %d lines%s"
                     % (old.count("\n") + 1, new_.count("\n") + 1, first_difference(old, new_))))
    return rows


# ------------------------------------------------------------------------------- tokens


# **The gap `sync` structurally cannot close** (T-166). A release may add a token to the shared
# block; the block is shell and gets installed, the declaration is a theme value and lives in the
# deck's own THEME region - which `sync` must not touch, and asserts it did not. So the upgrade
# reports success, `shell.py check` passes, and the next gate fails DS-013 on a token the adopter
# never had a chance to declare. Measured on the first real adopter upgrade this repository ever
# performed: `--qv-measure`, added by T-106, on a deck built at 0.2.2.
#
# `sync` is the one command that holds both halves - the shell it is installing and the deck it is
# installing into - so it is the one that can see this. It reports; it does not write, because
# writing here would cost the guarantee that makes `sync` safe to run on a 250 KB file nobody can
# read. `tokens --write` is the separate, narrower promise: it only ever ADDS what is missing.
TOKEN_MARK = "/* declared by `shell.py tokens`:"
TOKEN_BLOCK = ("\n\n" + TOKEN_MARK + " the shipped shell reads these and this deck\n"
               "   carried no declaration of its own. The values are the shipped theme's - change\n"
               "   them if this deck wants a different look. Nothing already declared was touched,\n"
               "   and re-running adds to this block rather than making a second one. */\n"
               ":root{\n%s}\n")

# The dark band's own marked block (T-177). Appended after the deck's own bands, where the higher
# specificity of `:root[data-theme="dark"]` over `:root` is what makes the dark value win in dark
# mode rather than the light one written a few lines above it.
TOKEN_MARK_DARK = "/* declared by `shell.py tokens`, dark band:"
TOKEN_BLOCK_DARK = ("\n\n" + TOKEN_MARK_DARK + " the same tokens at the shipped\n"
                    "   theme's DARK values. A separate block because they are separate values -\n"
                    "   carrying one of the two into both bands is the defect this replaced. */\n"
                    ':root[data-theme="dark"]{\n%s}\n')

_CACHE = {}


def contract_tokens():
    """The contract's token table, parsed once. `check` runs this on every fixture."""
    if "tokens" not in _CACHE:
        _CACHE["tokens"] = theme_mod.load()[0]
    return _CACHE["tokens"]


def shipped_values(theme_css=DEFAULT_THEME):
    """`{--name: value}` as the shipped theme declares them, flattened - what a value IS.

    Flattened is right for reading and wrong for carrying; `shipped_bands` is the other question.
    """
    if theme_css not in _CACHE:
        _CACHE[theme_css] = theme_mod.declarations(read(theme_css))
    return _CACHE[theme_css]


def shipped_bands(theme_css=DEFAULT_THEME):
    """`{band: {--name: value}}` for the shipped theme - what a value is IN EACH BAND (T-177)."""
    key = ("bands", theme_css)
    if key not in _CACHE:
        _CACHE[key] = theme_mod.bands(read(theme_css))
    return _CACHE[key]


def undeclared_tokens(html, theme_css=DEFAULT_THEME):
    """`[(token, {band: the shipped theme's value})]` - every token the contract requires that this
    deck's theme region does not declare, with a value per band the shipped theme declares it in.

    Read the same way DS-013 reads it - `theme.extract` then `theme.declarations`, against
    `theme.load` - so what this reports and what the gate fails on cannot drift apart. A deck with
    no theme region at all is DS-013's own verdict and not this; it returns nothing rather than
    naming all 117.

    **The value is a map rather than a string since T-177.** A colour is declared in both bands and
    the two are different values; returning one of them was how the dark value reached a light
    band. An empty map means the shipped theme has no value at all, which is a different answer
    from *one value* and is reported differently.
    """
    region = theme_mod.extract(html)
    if region is None:
        return []
    here = theme_mod.declarations(region)
    bands = shipped_bands(theme_css)
    out = []
    toks = contract_tokens()
    for name in sorted(toks):
        # An `optional` token is not one the contract *requires* (T-264), so a deck that declares
        # none of them is not short of anything and must not be told to run `tokens --write`.
        if name in here or toks[name].kind == "optional":
            continue
        out.append((name, {b: v[name] for b, v in bands.items() if name in v}))
    return out


def declare_tokens(html, theme_css=DEFAULT_THEME):
    """`(html, added, refused)` - the deck with every missing declaration added **in each band the
    shipped theme declares it in**, what was added as `[(token, band, value)]`, and what was
    declined as `[(token, why)]`.

    **Only ever additive.** A token already declared is a value someone chose, and a version gap is
    indistinguishable from a deliberate edit (the same reason `sync` reports first) - so nothing
    already present is read, let alone rewritten. A token the shipped theme has no value for is
    left for a person: there is nothing to copy and inventing one is how a band gets a number that
    fits one deck (**L-38**).

    **Carry both bands, and refuse rather than guess (T-177).** A token the shipped theme declares
    twice is written twice, into this deck's own light and dark bands. Where the deck has no band
    to receive one of them, the token is **declined with the reason** instead of being written at
    whichever value happened to be read last - which is the defect this function was fixed for. A
    wrong value is silent; a declined one is a sentence an adopter can act on.
    """
    missing = undeclared_tokens(html, theme_css)
    region = theme_mod.extract(html)
    if region is None:
        return html, [], []
    deck_bands = theme_mod.bands(region)

    plan, added, refused = {}, [], []
    for name, vals in missing:
        if not vals:
            continue                       # nothing to copy; the report already says so
        absent = sorted(b for b in vals if b not in deck_bands)
        if absent:
            refused.append((name, "the shipped theme gives it a %s value and this deck has no %s "
                                  "band to put %s in"
                            % (" and a ".join(sorted(vals)), " or ".join(absent),
                               "it" if len(absent) == 1 else "them")))
            continue
        for band in sorted(vals):
            plan.setdefault(band, []).append((name, vals[band]))
            added.append((name, band, vals[band]))
    if not plan:
        return html, [], refused

    for band, mark, block in (("light", TOKEN_MARK, TOKEN_BLOCK),
                              ("dark", TOKEN_MARK_DARK, TOKEN_BLOCK_DARK)):
        rows = plan.get(band)
        if not rows:
            continue
        lines = "".join("  %s:%s;\n" % (name, value.strip()) for name, value in rows)
        if mark in region:
            close = region.index("}", region.index(mark))
            region = region[:close] + lines + region[close:]
        else:
            region = region.rstrip("\n") + block % lines
    return theme_mod.swap(html, region), added, refused


def token_report(missing):
    """The lines `sync` and `check` both owe an adopter. Names the token and a value, never a
    count: a count sends them back to the tool, and the value is what they have to type.

    A dual-band token prints both values, because both are what has to be typed and printing one
    is the shape of the defect T-177 fixed.
    """
    out = []
    for name, vals in missing:
        if not vals:
            said = "no value in the shipped theme - see THEME-CONTRACT.md"
        else:
            said = "shipped theme declares " + ", ".join(
                "%s %s" % (band, vals[band].strip()) for band in sorted(vals))
        out.append("    %-18s %s" % (name, said))
    return out


def refusal_report(refused):
    """What `--write` declined and why, in the shape `token_report` uses. Empty when nothing was.

    Separate from `token_report` because they answer different questions - *what is missing* and
    *what this tool will not do about it* - and an adopter reading the first should not have to
    infer the second from a count that came up short.
    """
    return ["    %-18s DECLINED - %s" % (name, why) for name, why in refused]


# ------------------------------------------------------------------------------- check


def check(html, path="the deck"):
    """`[problem]` - where this deck and the shipped shell disagree."""
    problems = []
    try:
        skeleton, parts = cut(html)
    except NotAShell as exc:
        return ["NOT A SHELL   %s: %s" % (path, exc)]

    expected = read(SHELL_HTML)
    if skeleton != expected:
        problems.append("SKELETON      %s: the markup outside the %d regions differs from "
                        "shell/shell.html%s"
                        % (path, len(SLOTS), first_difference(skeleton, expected)))

    if parts["COMPONENTS"] != read(COMPONENTS):
        problems.append("COMPONENTS    %s: differs from shell/components.css%s"
                        % (path, first_difference(parts["COMPONENTS"], read(COMPONENTS))))

    # The script nests: three per-deck declarations inside it are the deck's, and everything
    # around them is the shell's.
    try:
        script_skeleton, _script_parts = cut(parts["SCRIPT"], SCRIPT_SLOTS)
    except NotAShell as exc:
        problems.append("SCRIPT        %s: %s" % (path, exc))
    else:
        if script_skeleton != read(DECK_JS):
            problems.append("SCRIPT        %s: differs from shell/deck.js%s"
                            % (path, first_difference(script_skeleton, read(DECK_JS))))
        # `STAGES` and `STAGE_ICON` are subscripted by the same `data-stage`, so they are one
        # table written as two and a deck is wrong the moment they differ in length. `new()`
        # builds them together and cannot get this wrong; a deck edited by hand can, and one
        # was - the reference deck carried eight stages against seven icons, so its colophon's
        # contents box drew `<use href="#undefined">` and printed with no mark (T-108).
        counts = [(name, len(re.findall(r"'[^']*'|\"[^\"]*\"", body)))
                  for name, body in ((n, b) for n, b in _script_parts.items()
                                     if n in ("STAGES", "STAGE_ICON"))]
        if len(counts) == 2 and counts[0][1] != counts[1][1]:
            problems.append("STAGE TABLE   %s: %s has %d entries and %s has %d - they are one "
                            "table subscripted by one `data-stage`, so a slide in the longer one "
                            "reads `undefined` out of the shorter"
                            % ((path,) + counts[0] + counts[1]))

    # DS-009: the preflight holds exactly the rows this deck has a subject for. Same shape as the
    # sprite check below, and the same failure it prevents - a region that was right when it was
    # written and stopped being right when the deck grew a feature.
    if parts["PREFLIGHT"] != preflight_mod.block(html):
        problems.append("PREFLIGHT     %s: the preflight is not the rows this deck needs - run "
                        "`shell.py preflight` (DS-009)" % path)

    # DS-113 and DS-112 in one: the sprite holds exactly the icons used, and each says which
    # Lucide glyph it is - a claim `icons --check` can settle against the shipped library.
    lib = library()
    mapping = declared(html)
    for concept, glyph in sorted(mapping.items()):
        if glyph is None:
            problems.append("NO PROVENANCE %s: <symbol id=\"i-%s\"> does not say which Lucide "
                            "glyph it is (DS-112)" % (path, concept))
    try:
        want_sprite = sprite(deck_icons(html), dict((k, v) for k, v in mapping.items() if v), lib)
    except NotAShell as exc:
        problems.append("ICONS         %s: %s" % (path, exc))
    else:
        if parts["ICONS"] != want_sprite:
            problems.append("ICONS         %s: the sprite is not the icons this deck uses - "
                            "run `shell.py icons` (DS-113)" % path)

    # The token gap, on a deck that has already been synced (T-166). `sync` names it at the moment
    # of upgrade; this names it every time afterwards, because an adopter who synced before this
    # existed got no warning and the deck is still short.
    missing = undeclared_tokens(html)
    if missing:
        problems.append("TOKENS        %s: %d token(s) THEME-CONTRACT.md requires are not declared "
                        "in this deck's theme, so DS-013 fails - run `shell.py tokens <deck> "
                        "--write`\n%s" % (path, len(missing), "\n".join(token_report(missing))))
    return problems


def first_difference(got, want):
    """Where two texts part company, as a line number and both sides. Silent when they do not."""
    if got == want:
        return ""
    for i, (a, b) in enumerate(zip(got, want)):
        if a != b:
            line = got.count("\n", 0, i) + 1
            return ("\n              first at line %d: %r\n              shipped:        %r"
                    % (line, got[i:i + 48], want[i:i + 48]))
    shorter, longer = (got, want) if len(got) < len(want) else (want, got)
    line = shorter.count("\n") + 1
    return "\n              identical to line %d, then one side continues" % line


# ------------------------------------------------------------------------------- self-test


def self_test():
    """Fixtures whose answers are known, one per failure this tool claims to catch (**L-04**)."""
    failures, ran = [], []

    def ok(label, condition, detail=""):
        print("  %-4s %-52s %s" % ("ok" if condition else "FAIL", label, "" if condition else detail))
        ran.append(label)
        if not condition:
            failures.append(label)

    def not_a_shell(fn):
        """True when `fn` refuses rather than returning something plausible."""
        try:
            fn()
        except NotAShell:
            return True
        return False

    # 1. The cut is lossless, and what it leaves is the shell. Everything else rests on this.
    #
    # Both assertions are made against a deck this function BUILDS, and that is the whole of T-176.
    # They used to be made against the tracked reference deck, where the second one - `what is left
    # is shell/shell.html` - is a statement about the repository rather than about this tool: it
    # goes false the moment anyone edits `shell/shell.html`, which is the one moment `sync` exists
    # for. `main()` runs this before every subcommand, so the tool locked the door on the command
    # behind it, and the message said `anything below means nothing` while nothing was wrong.
    #
    # Drift between a deck and the shell is not un-checked by this: `check()` reports it by name as
    # SKELETON, the fixture for that is below, and `sync` repairs it. The defect was restating a
    # serviceable finding somewhere it could only be fatal (**L-77** is the same file's other case).
    built = new("Fixture", "Subtitle")
    skeleton, parts = cut(built)
    ok("the cut round-trips", fill(skeleton, parts) == built)
    ok("and what it leaves is shell/shell.html", skeleton == read(SHELL_HTML),
       first_difference(skeleton, read(SHELL_HTML))[:90])

    # And on a real deck, which is the input the two above cannot stand in for: 270 KB of authored
    # slides, three embedded faces and a sprite. Losslessness only, because everything this deck
    # can say about `shell/shell.html` is the repository's business and `check` already says it.
    reference = os.path.join(ROOT, "examples", "reference-deck.html")
    if os.path.exists(reference):
        # `migrate` first, and this is **T-176 in a new shape**: the deck on disk is whatever
        # the last release left, so a self-test that reads it as current blocks `sync` - the one
        # command that makes it current. What is under test is losslessness of the cut on a real
        # 270 KB deck, which is a property of `cut` rather than a claim about the repository.
        original = migrate(read(reference))
        real_skeleton, real_parts = cut(original)
        ok("and it round-trips on a real deck", fill(real_skeleton, real_parts) == original)

    # 2. A deck built by `new` is a deck this tool recognises.
    fresh = new("Title", "Subtitle")
    ok("a fresh skeleton passes check", check(fresh) == [], "; ".join(check(fresh))[:70])

    # 3. Each region, broken on purpose. A check that has only ever passed is not evidence.
    broken = fresh.replace("\n<style>", "\n<style>\n.injected{color:red}", 1)
    ok("an edited component block is caught",
       any(p.startswith("COMPONENTS") for p in check(broken)))

    broken = fresh.replace("<script>", "<script>\nvoid 0;", 1)
    ok("an edited script is caught", any(p.startswith("SCRIPT") for p in check(broken)))

    # The defect this check was added for, seeded: one more stage than there are icons. Both
    # directions, because a table that is short at either end subscripts to `undefined` (T-108).
    longer = fresh.replace("var STAGES = ['Claim'];", "var STAGES = ['Claim','Extra'];", 1)
    ok("a stage with no icon is caught", any(p.startswith("STAGE TABLE") for p in check(longer)))
    shorter = fresh.replace("var STAGE_ICON = ['i-info'];", "var STAGE_ICON = [];", 1)
    ok("an icon table shorter than the stages is caught",
       any(p.startswith("STAGE TABLE") for p in check(shorter)))

    # The pager's label, and it MOVED here in T-114. `Read` was the seeded defect until the chrome
    # row's tail became a slot, at which point editing it stopped being a skeleton change and
    # became a per-deck one - so the fixture passed by testing nothing. The seed has to sit in
    # markup the byte comparison still owns, and the navigation container is where that now is.
    # T-112 added `.is-back` to the Previous pager, so the seed carries it: the defect being
    # seeded is an edited chrome row, and a seed that no longer matches tests nothing at all - which
    # is the state this fixture was already found in once, above.
    broken = fresh.replace(
        '<button class="btn btn--pager is-back" id="prev" aria-label="Previous slide">',
        '<button class="btn" id="prev" aria-label="Back">', 1)
    ok("edited chrome is caught", any(p.startswith("SKELETON") for p in check(broken)))

    # The other edge of the same move, asserted rather than assumed: what went into the slot is
    # now the DECK's, and `check` must not report it. What guards those labels instead is
    # `component.py` against COMPONENT-CONTRACT.md 3.4, which is where the cost of the one-slot
    # design is paid (T-114 step 7a).
    retitled = fresh.replace('<button class="btn" id="toDoc">Read</button>',
                             '<button class="btn" id="toDoc">Document</button>', 1)
    ok("and the tail is the deck's, so a relabelled menu item is not",
       not any(p.startswith("SKELETON") for p in check(retitled)))

    broken = fresh.replace('<main class="stage" id="stage" aria-label="Presentation">', "<main>", 1)
    ok("a file without the shell's structure is caught",
       any(p.startswith("NOT A SHELL") for p in check(broken)))

    # 3a. `sync` (T-124), against the three regions `check` compares. Each fixture is a deck one
    # release behind in exactly one of them, which is the shape an adopter actually meets.
    stale_parts = {
        "COMPONENTS": fresh.replace("\n<style>", "\n<style>\n.from-an-older-release{color:red}", 1),
        "SCRIPT": fresh.replace("<script>", "<script>\nvoid 0;  /* an older release */", 1),
        "SKELETON": fresh.replace('<button class="btn btn--pager is-back" id="prev" aria-label="Previous slide">',
                                  '<button class="btn" id="prev" aria-label="Back">', 1),
    }
    for region, stale in sorted(stale_parts.items()):
        ok("a deck behind in %s fails check" % region, check(stale) != [])
        synced = sync(stale)
        ok("and sync brings it back", check(synced) == [], "; ".join(check(synced))[:70])
        ok("and says %s is what moved" % region,
           [r[0] for r in changes(stale, synced)] == [region],
           "reported %r" % ([r[0] for r in changes(stale, synced)],))

    # 3b. The gap sync structurally cannot close (T-166), seeded: a deck one release behind in a
    # token, which is the shape of the real adopter upgrade that found it. The fixture is the
    # point - every assertion below reads FAIL if the reporting is removed, and the defect it
    # stands for shipped precisely because both commands an adopter runs said yes (**L-05**).
    older = fresh.replace("  --qv-measure:80rem;\n", "", 1)
    ok("a deck missing a token the shell reads is a different file",
       older != fresh, "the token line was not where this fixture expects it")
    ok("and theme.py fails it, which is the defect being reported",
       any("--qv-measure not declared" in m
           for _r, m in theme_mod.validate(theme_mod.extract(older))))
    ok("check names the token", any(p.startswith("TOKENS") and "--qv-measure" in p
                                    for p in check(older)))
    ok("and syncing the shell does not close it",
       [n for n, _v in undeclared_tokens(sync(older))] == ["--qv-measure"],
       "sync silently changed the theme region, which it must never do")

    declared_deck, added, refused = declare_tokens(older)
    ok("`tokens --write` declares it at the shipped theme's value",
       added == [("--qv-measure", "light", "80rem")], "added %r" % (added,))
    ok("and a single-band token is written once, not into both",
       [b for _n, b, _v in added] == ["light"], "bands %r" % ([b for _n, b, _v in added],))
    ok("and nothing was refused, because this deck has the band it needed",
       refused == [], "refused %r" % (refused,))

    # ---------------------------------------------------------------- T-177
    # **The defect, seeded.** A colour is declared in BOTH bands at two different values, and the
    # flat `{name: value}` map the old code used kept whichever was read last - the dark one. The
    # deck then got a near-black border on paper and nothing at all in dark mode, and `theme.py`
    # passed it, because DS-013 asks whether a token is DECLARED and not whether it is declared at
    # the right value in the right band. Found by T-114, which added the first new dual-band token
    # since this command shipped; every older one was already in every deck, so the flattening had
    # never been asked to carry anything.
    lightv = shipped_bands()["light"]["--line"]
    darkv = shipped_bands()["dark"]["--line"]
    ok("the fixture's token really is declared twice, at two values", lightv != darkv,
       "--line is %r in both bands, so this fixture proves nothing" % lightv)

    both = fresh.replace("--line:%s;" % lightv, "", 1).replace("--line:%s;" % darkv, "", 1)
    ok("a deck missing a dual-band token is seen to be missing it",
       "--line" in [n for n, _v in undeclared_tokens(both)],
       "the fixture did not remove both declarations")
    ok("and both values are reported, not one",
       dict(undeclared_tokens(both))["--line"] == {"light": lightv, "dark": darkv},
       "reported %r" % (dict(undeclared_tokens(both)).get("--line"),))

    carried, added2, refused2 = declare_tokens(both)
    ok("`--write` carries a dual-band token into BOTH bands",
       sorted((b, v) for n, b, v in added2 if n == "--line")
       == sorted([("dark", darkv), ("light", lightv)]),
       "added %r" % ([r for r in added2 if r[0] == "--line"],))
    ok("and neither band gets the other's value",
       theme_mod.bands(theme_mod.extract(carried))["light"]["--line"] == lightv
       and theme_mod.bands(theme_mod.extract(carried))["dark"]["--line"] == darkv,
       "light %r dark %r" % (theme_mod.bands(theme_mod.extract(carried))["light"].get("--line"),
                             theme_mod.bands(theme_mod.extract(carried))["dark"].get("--line")))
    ok("the carried deck passes theme.py", not theme_mod.validate(theme_mod.extract(carried)))
    ok("and carrying is idempotent", declare_tokens(carried)[1] == [])

    # **The other half: refuse rather than guess.** A deck with no dark band has nowhere to put the
    # second value, and writing only the first is exactly the silent wrong answer this replaced.
    no_dark_region = "\n".join(
        ln for ln in theme_mod.extract(both).split("\n") if "--line:" not in ln)
    a = no_dark_region.index(':root[data-theme="dark"]{')
    b = no_dark_region.index("}", a) + 1
    bandless = theme_mod.swap(both, no_dark_region[:a] + no_dark_region[b:])
    _out, added3, refused3 = declare_tokens(bandless)
    ok("a deck with no dark band is REFUSED the dual-band token, not given half of it",
       "--line" in [n for n, _w in refused3] and "--line" not in [n for n, _b, _v in added3],
       "added %r refused %r" % (added3, refused3))
    ok("and the refusal says which band is missing and why",
       any("dark" in w and "no dark band" in w for n, w in refused3 if n == "--line"),
       "said %r" % ([w for n, w in refused3 if n == "--line"],))
    ok("a single-band token is still written to that same deck",
       "--qv-measure" not in [n for n, _w in refused3])

    ok("and the deck then passes both", check(declared_deck) == []
       and not theme_mod.validate(theme_mod.extract(declared_deck)),
       "; ".join(check(declared_deck))[:70])
    ok("declaring is idempotent", declare_tokens(declared_deck)[1] == [])
    moved = [k for k in kept(older) if kept(older)[k] != kept(declared_deck).get(k)]
    ok("and it moved the theme region and nothing else", moved == ["THEME"],
       "moved %r" % (moved,))
    ok("a token already declared is never rewritten",
       declare_tokens(fresh.replace("--qv-measure:80rem", "--qv-measure:60rem", 1))[1] == [])

    # The property the command asserts on the adopter's file, asserted here on a deck that has
    # something in every per-deck region - a fresh skeleton would pass this vacuously.
    # Compared against the MIGRATED deck, because `migrate` is the first thing `sync` does: a slot
    # a later release added has no value in an older deck, and installing it is the one region
    # sync is entitled to write. Comparing against the un-migrated file would assert that sync
    # never adds a region, which is the opposite of what the migration table is for.
    original = migrate(read(reference))
    ok("sync leaves every per-deck region of the reference deck untouched",
       kept(sync(original)) == kept(original),
       "moved: %r" % sorted(k for k in kept(original)
                            if kept(original)[k] != kept(sync(original)).get(k)))
    # A deck ALREADY IN STEP is not changed - asserted on a deck this line syncs itself, never on
    # the repository's copy. `sync(original) == original` was the fixture until 2026-08-13, and it
    # asserts the current contents of a tracked artifact rather than a property of the tool: one
    # edit to `shell/deck.js` fails it, the self-test refuses to report, and the command that exists
    # to carry that edit to the decks is the command it takes down (T-126). L-71's family, one step
    # over - there the reference ENVIRONMENT was taken for correct, here the reference STATE. What
    # the fixture was standing in for is a gate's job and already done: check_all.py runs
    # `shell.py check` over every tracked deck.
    ok("and syncing a deck that is already in step changes nothing",
       sync(sync(original)) == sync(original),
       first_difference(sync(sync(original)), sync(original))[:90])
    ok("sync is idempotent", sync(sync(stale_parts["COMPONENTS"]))
       == sync(stale_parts["COMPONENTS"]))
    ok("a deck with no anchors is refused rather than guessed at",
       not_a_shell(lambda: sync(broken)))

    # 4. The sprite. Three ways it goes wrong, each with its own verdict.
    lib = library()
    using = fresh.replace("<!-- slides go here", '<svg class="icon"><use href="#i-when"/></svg>\n'
                                                 "<!-- slides go here", 1)
    ok("an icon with no sprite entry is caught",
       any(p.startswith("ICONS") for p in check(using)))

    wired = apply_icons(using, {"when": "clock"})
    ok("and syncing the sprite settles it", check(wired) == [], "; ".join(check(wired))[:70])
    ok("the synced symbol records its glyph", 'data-icon="clock"' in wired)

    stale = wired.replace('<use href="#i-when"/>', "")
    ok("a symbol nobody uses is caught (DS-113)",
       any(p.startswith("ICONS") for p in check(stale)))

    # The failure this tool had on its first real run: four of the reference deck's nine icons
    # are named in a script array and never in markup, and a markup-only scan deleted them.
    scripted = stale.replace("var STAGE_ICON = [", "var STAGE_ICON = ['i-when',", 1)
    ok("an icon named only in the script still counts", "when" in deck_icons(scripted))
    ok("and a bare i-name inside a token is not a reference",
       "line" not in deck_icons(fresh.replace("<script>", "<script>\nvar x='--ui-line';", 1)))
    staged = new("Untitled", "s", stages=["One", "Two"],
                 stage_icons=[("first", "flag"), ("second", "target")])
    ok("the three per-deck declarations are the deck's, not the shell's",
       "Untitled" in staged and "'One','Two'" in staged and "'i-first','i-second'" in staged)
    ok("and a stage icon names a concept, not the glyph that draws it",
       'id="i-first" data-icon="flag"' in staged and check(staged) == [])

    nameless = wired.replace(' data-icon="clock"', "")
    ok("a symbol with no provenance is caught (DS-112)",
       any(p.startswith("NO PROVENANCE") for p in check(nameless)))

    # 4b. The preflight, the other derived region (T-019). Three ways it goes wrong, and the one
    # that matters is the middle one: a deck that GROWS a feature and keeps yesterday's block.
    ok("a fresh deck emits the rows its own shell needs",
       "CSS custom properties" in fresh and "CSS grid" in fresh)
    ok("and not the rows nothing in it reaches for",
       "WebGL" not in fresh and "dynamic import()" not in fresh)
    quick = fresh.replace("<!-- slides go here",
                          '<template class="qv-src" data-qv="s"><p>x</p></template>\n'
                          "<!-- slides go here", 1)
    ok("a deck that grows a <template> has a stale preflight",
       any(p.startswith("PREFLIGHT") for p in check(quick)))
    synced = apply_preflight(quick)
    ok("and syncing settles it, naming the new row", check(synced) == []
       and "<template> element" in synced, "; ".join(check(synced))[:70])
    ok("the preflight is idempotent", apply_preflight(synced) == synced)
    ok("a hand-edited preflight is caught",
       any(p.startswith("PREFLIGHT")
           for p in check(fresh.replace("var d=document.documentElement", "var d=0", 1))))
    ok("the marker ships ON, so the degraded state is what an unsupported browser paints",
       'data-preflight="pending"' in fresh and ":root[data-preflight] .slide" in fresh)
    ok("and the script stands down while it survives",
       "if (root.hasAttribute('data-preflight')) return;" in fresh)

    try:
        apply_icons(using, {"when": "not-a-lucide-icon"})
        ok("an unknown glyph is refused", False, "it was accepted")
    except NotAShell:
        ok("an unknown glyph is refused", True)

    # 5. The library itself.
    ok("every symbol in the library is unique and non-empty",
       len(lib) == len(SYMBOL.findall(read(ICONS))) and all(v.strip() for v in lib.values()))

    # 6. The argument shapes, because the documented one has to be the one that runs (T-091).
    ok("one comma-separated --set carries every pair",
       pairs(option(["deck.html", "--set", "when=clock,where=map"], "--set"))
       == [("when", "clock"), ("where", "map")])
    try:
        option(["deck.html", "--set", "when=clock", "--set", "where=map"], "--set")
        ok("a repeated --set is refused rather than half-read", False,
           "the second pair was dropped in silence, which is the T-091 defect")
    except SystemExit as exc:
        ok("a repeated --set is refused rather than half-read",
           "--set" in str(exc) and "comma-separated" in str(exc),
           "it exited without naming the argument: %s" % exc)

    # The usage list, the per-command help and the dispatch name the same commands.
    #
    # **T-208.** `preflight` was dispatched, named in `USAGE` and named in a DS-009 failure message,
    # and absent from the list a reader gets with no arguments. `tail` was named nowhere at all.
    # Both were discoverable only by reading the source of the error you were trying to fix, which
    # is a tool telling the truth in one place and not the other.
    #
    # **The comparison is the one a reader cannot make**, so the tool makes it. Both sets are read
    # out of this file rather than kept as a list beside it, so the next command added fails here
    # rather than in someone's terminal - the same reason `parts` derives its regions from `SLOTS`.
    src = read(os.path.abspath(__file__))
    dispatched = set(re.findall(r'if cmd == "([a-z]+)"', src))
    listed = set(re.findall(r"shell\.py ([a-z]+)", __doc__))
    ok("every dispatched command is in the usage list", dispatched <= listed,
       "missing: %s" % ", ".join(sorted(dispatched - listed)))
    ok("and every one has its own --help entry", dispatched <= set(USAGE),
       "missing: %s" % ", ".join(sorted(dispatched - set(USAGE))))
    ok("and the list names nothing the tool will not run", listed <= dispatched,
       "not dispatched: %s" % ", ".join(sorted(listed - dispatched)))

    print("\n%d of %d fixtures behaved as specified.\n" % (len(ran) - len(failures), len(ran)))
    return failures


# ------------------------------------------------------------------------------- cli


def parts_report():
    print("The deck shell - what a run assembles, and what it authors.\n")
    rows = [("shell/shell.html", os.path.getsize(SHELL_HTML), "structure, chrome, reading view"),
            ("shell/components.css", os.path.getsize(COMPONENTS), "the shared component block"),
            ("shell/deck.js", os.path.getsize(DECK_JS), "the deck script"),
            ("shell/icons.svg", os.path.getsize(ICONS), "%d Lucide glyphs to choose from"
             % len(library())),
            ("themes/quarto.css", os.path.getsize(DEFAULT_THEME), "the theme, faces resolved in")]
    for name, size, what in rows:
        print("  %-22s %7d bytes   %s" % (name, size, what))
    print("\nThe deck varies in %d regions, and nowhere else:\n" % len(SLOTS))
    for slot, _o, _c, what in SLOTS:
        print("  %-12s %s" % ("{{%s}}" % slot, what))


USAGE = {
    "new": "usage: shell.py new <out.html> --title T [--subtitle S] [--theme t.css]\n"
           "  Writes a deck skeleton carrying the shipped shell and no slides.",
    "icons": "usage: shell.py icons <deck> [--set concept=lucide,...] [--check]\n"
             "       shell.py icons --list\n"
             "       shell.py icons --sheet <out.svg>\n"
             "  Keeps the deck's sprite equal to the icons the deck uses (DS-113).\n"
             "  --list   prints the concept ids the library holds, one per line\n"
             "  --sheet  draws every glyph into one SVG to look at\n"
             "  --check  reports whether the sprite is already exactly the used set",
    "sync": "usage: shell.py sync <deck> [--write]\n"
            "  Puts the shipped shared block back into a deck that has fallen behind.",
    "tokens": "usage: shell.py tokens <deck> [--write]\n"
              "  Adds the theme tokens THEME-CONTRACT.md requires and this deck lacks.\n"
              "  Only ever adds: a token already declared is a value someone chose.",
    "check": "usage: shell.py check <deck>\n"
             "  Proves the deck still carries the shipped shell, byte for byte.",
    "preflight": "usage: shell.py preflight <deck> [--check]\n"
                 "  Writes the preflight rows this deck's own content needs (DS-009).\n"
                 "  --check  reports whether they are already exactly the needed set",
    "tail": "usage: shell.py tail <deck> [--write]\n"
            "  Puts the `Motion` control where DS-218 asks for it: inside the `More`\n"
            "  menu, whether or not the deck loops.",
    "parts": "usage: shell.py parts\n  Lists the regions the shell is cut into.",
}


def main(argv):
    if "--self-test" in argv:
        return 1 if self_test() else 0

    if not argv:
        print(__doc__.strip())
        return 2

    # **`--help` is answered before the self-test, and that is deliberate (T-192).** A help request
    # is not evidence and does not need any; running twenty fixtures first and then dying on
    # `FileNotFoundError: '--help'` - which is what `icons --help` did in 0.4.0, because the flag
    # was taken as the deck path - is the worst of both. Found by the first outside build, which
    # asked twice, got a traceback twice, and went and grepped `icons.svg` instead.
    if argv[0] in ("--help", "-h", "help") or "--help" in argv or "-h" in argv:
        print(USAGE.get(argv[0], __doc__.strip()))
        return 0

    print("Self-test first - a tool that has not been shown to fail is not evidence (L-04).\n")
    if self_test():
        print("SELF-TEST FAILED - the tool itself is wrong; anything below means nothing.")
        return 2

    cmd, rest = argv[0], argv[1:]

    if cmd == "parts":
        parts_report()
        return 0

    if cmd == "new":
        if not rest:
            sys.exit("usage: shell.py new <out.html> --title T [--subtitle S] [--theme t.css]")
        out = rest[0]
        title = option(rest, "--title") or "Untitled deck"
        subtitle = option(rest, "--subtitle") or ""
        theme_css = option(rest, "--theme") or DEFAULT_THEME
        stages = [s.strip() for s in (option(rest, "--stages") or "").split("|") if s.strip()]
        icons = pairs(option(rest, "--stage-icons"))
        if stages and icons and len(stages) != len(icons):
            sys.exit("--stages names %d stage(s) and --stage-icons %d icon(s); DS-134 marks each "
                     "stage, so they have to agree" % (len(stages), len(icons)))
        html = new(title, subtitle, theme_css=theme_css, stages=stages or None,
                   stage_icons=icons or None)
        write(out, html)
        print("wrote %s - %d bytes, no slides yet." % (out, len(html)))
        print("Next: author slides against docs/COMPONENT-CONTRACT.md 3.2, then\n"
              "  python tools/deck/shell.py icons %s --set <concept>=<lucide>\n"
              "  python tools/deck/check.py %s" % (out, out))
        return 0

    if cmd == "icons":
        # **The library, in the terminal (T-192).** `--sheet` answers *what do they look like* and
        # is the only answer 0.4.0 had, so an author who wanted *what may I name* had to open an
        # SVG or grep it. The first outside build grepped, with the wrong pattern first.
        if "--list" in rest:
            names = sorted(library())
            print("\n".join(names))
            print("\n%d concept(s). Use one as `--set <concept>=<lucide>`." % len(names),
                  file=sys.stderr)
            return 0
        target = option(rest, "--sheet")
        if target:
            write(target, sheet())
            print("wrote %s - %d glyphs. Open it and look at them." % (target, len(library())))
            return 0
        if not rest:
            sys.exit("usage: shell.py icons <deck> [--set c=lucide,...] [--check]")
        deck = rest[0]
        sets = dict(pairs(option(rest, "--set")))
        html = read(deck)
        try:
            wired = apply_icons(html, sets)
        except NotAShell as exc:
            sys.exit(str(exc))
        used = deck_icons(html)
        if "--check" in rest:
            if wired == html:
                print("OK - the sprite holds exactly the %d icon(s) this deck uses." % len(used))
                return 0
            print("STALE - the sprite is not the icons this deck uses (DS-113). "
                  "Run without --check.")
            return 1
        write(deck, wired)
        print("%s - sprite now holds %d icon(s): %s"
              % (deck, len(used), ", ".join("i-%s" % u for u in used) or "none"))
        return 0

    if cmd == "preflight":
        if not rest:
            sys.exit("usage: shell.py preflight <deck> [--check]")
        deck = rest[0]
        html = read(deck)
        wired = apply_preflight(html)
        rows = preflight_mod.emitted(html)
        if "--check" in rest:
            if wired == html:
                print("OK - the preflight holds exactly the %d row(s) this deck needs." % len(rows))
                return 0
            print("STALE - the preflight is not the rows this deck needs (DS-009). "
                  "Run without --check.")
            return 1
        write(deck, wired)
        print("%s - preflight now holds %d of %d row(s): %s"
              % (deck, len(rows), len(preflight_mod.ROWS),
                 ", ".join(r[0] for r in rows) or "none"))
        print("Why each row is a row: python tools/deck/preflight.py rows")
        return 0

    if cmd == "sync":
        if not rest:
            sys.exit("usage: shell.py sync <deck> [--write]")
        deck = rest[0]
        rel = paths.display_path(deck, ROOT).replace("\\", "/")
        html = read(deck)
        # A slot a later release ADDED has no anchor in this deck, and `sync` installs it (see
        # MIGRATIONS). Installing it here as well is not redundant: everything below compares this
        # deck with the synced one, and comparing the un-migrated file would read the newly
        # installed region as a per-deck region that went missing, and refuse the write. It is
        # announced rather than done quietly, because it is the one edit `sync` makes that is not
        # "the shell you already had, one release newer".
        for _old, _new, why in MIGRATIONS:
            if _old in html:
                print("MIGRATING     %s: %s" % (rel, why))
        html = migrate(html)
        try:
            fresh = sync(html)
        except NotAShell as exc:
            sys.exit("%s: %s\nRefusing to guess where the regions are." % (rel, exc))

        # The guarantee, asserted on the adopter's own file rather than on a fixture that passed
        # here once. If a single per-deck region moved, the sync is wrong and nothing is written.
        was, now = kept(html), kept(fresh)
        lost = sorted(k for k in was if was[k] != now.get(k))
        if lost:
            print("REFUSING - a sync must leave every per-deck region untouched and this one "
                  "changed %s." % ", ".join(lost))
            print("Nothing was written. This is a defect in shell.py, not in %s." % rel)
            return 2

        # What a sync cannot carry, and therefore has to say (T-166). Read off the SYNCED deck,
        # because the question is what the incoming shell needs, not what the old one did.
        missing = undeclared_tokens(fresh)

        rows = changes(html, fresh)
        if not rows and not missing:
            print("OK - %s already carries the installed shell. Nothing to sync." % rel)
            return 0
        for name, note in rows:
            print("  %-12s %s" % (name, note))
        if missing:
            print("  %-12s %d token(s) the installed shell reads and this deck does not declare."
                  % ("TOKENS", len(missing)))
            for line in token_report(missing):
                print(line)
            print("""    A sync must not touch the theme region - it is the deck's own - so this is
    reported and never written here. `shell.py tokens %s --write` adds exactly
    the missing declarations at the values above. Until then DS-013 fails.""" % rel)
        if not rows:
            print("\n%s already carries the installed shell; only the declarations above are "
                  "missing." % rel)
            return 1
        if "--write" not in rest:
            print("\n%d region(s) would change; %d per-deck region(s) untouched. Nothing written."
                  % (len(rows), len(was)))
            print("Review the above, then run again with --write.")
            print("""
A deck one release behind and a deck whose shell someone edited on purpose are the same
bytes - nothing in a deck records which release built it - so this reports before it
writes, every time. And if this file is GENERATED by something else, regenerate it
instead: a sync writes the shipped shell over whatever that generator added (L-77).""")
            return 0
        write(deck, fresh)
        print("\n%s - %d region(s) synced, %d per-deck region(s) untouched."
              % (rel, len(rows), len(was)))
        print("Next: python tools/deck/shell.py check %s" % rel)
        return 0

    if cmd == "tail":
        if not rest:
            sys.exit("usage: shell.py tail <deck> [--write]")
        deck = rest[0]
        rel = paths.display_path(deck, ROOT).replace("\\", "/")
        # `--loops` / `--still` selected between two tail forms until 2026-08-29. The forms
        # collapsed to one (T-277), so the flags are refused rather than ignored: a script still
        # passing one is asking for a placement this tool no longer decides, and silently doing
        # the right thing would leave it asking.
        for gone in ("--loops", "--still"):
            if gone in rest:
                sys.exit("%s: `%s` is gone. DS-218's placement clause was reversed on 2026-08-29 "
                         "(T-277) and there is one tail form now - `Motion` inside the menu, "
                         "looping or not. Run `tail %s [--write]`." % (rel, gone, rel))
        html = read(deck)
        fresh = tail(html)
        if fresh == html:
            print("OK - %s already carries `Motion` inside the menu." % rel)
            return 0
        if "--write" not in rest:
            print("%s - `Motion` would move inside the menu (DS-218)." % rel)
            print("Nothing written. Run again with --write.")
            return 1
        write(deck, fresh)
        print("%s - `Motion` now sits inside the menu." % rel)
        print("Next: python tools/deck/audit.py %s - the DS-218 row is what settles it." % rel)
        return 0

    if cmd == "tokens":
        if not rest:
            sys.exit("usage: shell.py tokens <deck> [--write]")
        deck = rest[0]
        rel = paths.display_path(deck, ROOT).replace("\\", "/")
        html = read(deck)
        missing = undeclared_tokens(html)
        if not missing:
            print("OK - %s declares every token THEME-CONTRACT.md requires." % rel)
            return 0
        print("%s - %d token(s) required by the contract and not declared here:" % (rel, len(missing)))
        for line in token_report(missing):
            print(line)
        if "--write" not in rest:
            print("\nNothing written. Run again with --write to add exactly these, at the values\n"
                  "above. A token already declared is a value someone chose and is never touched.")
            return 1
        written, added, refused = declare_tokens(html)
        if refused:
            print("")
            for line in refusal_report(refused):
                print(line)
        if not added:
            print("\nNothing written: there was no value to copy for any of them, or this deck has\n"
                  "no band to copy it into. Declare them by hand - THEME-CONTRACT.md gives each\n"
                  "a band.")
            return 1
        write(deck, written)
        bands = sorted(set(b for _n, b, _v in added))
        print("\n%s - %d declaration(s) added across the %s band(s): %s"
              % (rel, len(added), " and ".join(bands),
                 ", ".join(sorted(set(n for n, _b, _v in added)))))
        print("Next: python tools/deck/theme.py check %s" % rel)
        return 1 if refused else 0

    if cmd == "check":
        if not rest:
            sys.exit("usage: shell.py check <deck>")
        deck = rest[0]
        rel = paths.display_path(deck, ROOT).replace("\\", "/")
        problems = check(read(deck), rel)
        for problem in problems:
            print("  %s" % problem)
        if problems:
            print("\n%d problem(s)." % len(problems))
            return 1
        print("OK - %s carries the shipped shell unchanged, and its sprite is the icons it uses."
              % rel)
        print("""
This checks the **half nobody rewrites**, not the deck. It cannot tell you a slide says
anything - that is tools/deck/check.py, and the five dimensions past it (L-05).""")
        return 0

    sys.exit("unknown command %r - one of: new, icons, preflight, sync, tokens, check, parts"
             % cmd)


def pairs(raw):
    """`concept=lucide,concept=lucide` -> `[(concept, lucide)]`, order kept."""
    out = []
    for pair in (raw or "").split(","):
        if not pair.strip():
            continue
        if "=" not in pair:
            sys.exit("expected concept=lucide pairs, got %r" % pair)
        key, value = pair.split("=", 1)
        out.append((key.strip(), value.strip()))
    return out


def option(argv, name):
    """The value after `--name`, or None.

    **A repeated option is refused, and that is T-091.** This reads `argv.index`, so a second
    `--set` used to be dropped without a word: an author with three icons wrote what `build.md`
    showed - one pair per flag - got the first pair wired and the others silently discarded, and
    then read `icon 'i-analysis' is used and nothing says which Lucide glyph it is`. True, and two
    steps downstream of the cause. The message has to name the argument that lost the value, not
    the icon that went missing.
    """
    if argv.count(name) > 1:
        sys.exit("%s was given %d times and this parser reads the first only, so the rest would be "
                 "dropped in silence. It takes ONE comma-separated value:\n  %s a=x,b=y,c=z"
                 % (name, argv.count(name), name))
    if name in argv:
        i = argv.index(name)
        if i + 1 < len(argv):
            return argv[i + 1]
        sys.exit("%s needs a value" % name)
    return None


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
