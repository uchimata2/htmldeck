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
    python tools/deck/shell.py check <deck>
    python tools/deck/shell.py parts

**`check` is the reason the other commands are trustworthy.** It cuts the same ten regions out of
the deck and compares what is left with `shell/shell.html` byte for byte, so a batch edit that
strayed into the shared block is a red run rather than a discovery two decks later. The stale
fixture (**L-05**) is the same failure in a different file.

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

# The eleven regions a deck varies in. Everything else is the shell.
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
        "SLIDES": "\n<!-- slides go here, one <section class=\"slide\"> each "
                  "(COMPONENT-CONTRACT.md 3.2) -->\n",
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
        problems.append("SKELETON      %s: the markup outside the ten regions differs from "
                        "shell/shell.html%s" % (path, first_difference(skeleton, expected)))

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

    # 1. The cut is lossless. Everything else rests on this.
    reference = os.path.join(ROOT, "examples", "reference-deck.html")
    if os.path.exists(reference):
        original = read(reference)
        skeleton, parts = cut(original)
        ok("the cut round-trips on the reference deck", fill(skeleton, parts) == original)
        ok("and what is left is shell/shell.html", skeleton == read(SHELL_HTML),
           first_difference(skeleton, read(SHELL_HTML))[:90])
    else:
        ok("the reference deck exists to cut", False, "examples/reference-deck.html is missing")
        return failures

    # 2. A deck built by `new` is a deck this tool recognises.
    fresh = new("Title", "Subtitle")
    ok("a fresh skeleton passes check", check(fresh) == [], "; ".join(check(fresh))[:70])

    # 3. Each region, broken on purpose. A check that has only ever passed is not evidence.
    broken = fresh.replace("\n<style>", "\n<style>\n.injected{color:red}", 1)
    ok("an edited component block is caught",
       any(p.startswith("COMPONENTS") for p in check(broken)))

    broken = fresh.replace("<script>", "<script>\nvoid 0;", 1)
    ok("an edited script is caught", any(p.startswith("SCRIPT") for p in check(broken)))

    broken = fresh.replace('<button class="btn" id="toDoc">Read</button>',
                           '<button class="btn" id="toDoc">Document</button>', 1)
    ok("edited chrome is caught", any(p.startswith("SKELETON") for p in check(broken)))

    broken = fresh.replace('<main class="stage" id="stage" aria-label="Presentation">', "<main>", 1)
    ok("a file without the shell's structure is caught",
       any(p.startswith("NOT A SHELL") for p in check(broken)))

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
    print("\nThe deck varies in eleven regions, and nowhere else:\n")
    for slot, _o, _c, what in SLOTS:
        print("  %-12s %s" % ("{{%s}}" % slot, what))


def main(argv):
    if "--self-test" in argv:
        return 1 if self_test() else 0

    if not argv:
        print(__doc__.strip())
        return 2

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

    sys.exit("unknown command %r - one of: new, icons, preflight, check, parts" % cmd)


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
