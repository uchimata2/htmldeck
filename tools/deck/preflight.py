#!/usr/bin/env python3
"""The capability preflight: which rows a deck needs, the block that ships them, and proof it fails.

R6 §7 defined the deck's version floor as a **preflight rather than a number** - the floor is
whatever browser passes it - and that position is only real if something emits one. This is that
something.

**The block is derived, never declared.** Which checks a deck needs is a fact about the deck's own
bytes, exactly as which icons it uses is, so this reads the deck and writes the rows it finds a
subject for. A deck with no `<template>` does not test `<template>`; a deck with no canvas does not
test canvas. That is DS-009's second clause, and deriving it is what makes the clause true by
construction rather than by an author remembering.

**The degraded state ships ON.** `<html>` carries `data-preflight` from the moment it is parsed, and
a passing preflight takes it off. A blank page therefore cannot happen by a check running too late -
only by the fallback CSS being wrong - and the same marker covers the case no preflight can catch,
which is a browser that runs no script at all.

    python tools/deck/preflight.py rows                     # the table, and why each row is in it
    python tools/deck/preflight.py show <deck>              # what this deck would emit
    python tools/deck/preflight.py prove <deck>             # suppress a capability, in real Chrome

Emission and the staleness check live in `shell.py`, with the sprite, because they are the same
sentence about a different region. Pure standard library (**L-07**).
"""

import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths                                                        # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# The emitted block itself, so a scan of the deck never counts the preflight's own probe source as
# evidence that the deck uses the capability. Without this, the `import(` row justifies itself.
BLOCK = re.compile(r'<script id="preflight">.*?</script>', re.S)

# **Base64 cannot produce any of the characters these patterns turn on.** A deck is ~170 KB of
# embedded font payload, and the sprite scan has already been bitten once by a bare name matching
# inside a token (`--ui-line` for `i-line`). Every pattern below contains `<`, `:`, `(` or `-`,
# none of which is in the base64 alphabet, so no row can fire on font bytes.


def uses_tokens(html):
    return "var(--" in html


def uses_grid(html):
    return re.search(r"display\s*:\s*grid", html) is not None


# **An element row wants an ELEMENT, not the element's name.** `"<template" in html` looks right
# and is wrong: `components.css` and `deck.js` both explain the quick view in a comment that names
# the tag, both ship inside every deck, and so every deck emitted the `<template>` row - including
# the ones with no quick view at all. Caught by this tool's own fixture the first time it ran.
# Requiring a closing tag is what separates an element from prose about one, and it is exactly the
# `--ui-line`/`i-line` trap the sprite scan already has a comment about, one file along.
ELEMENT = "<%s[\\s>][^>]*>.*?</%s>"


def uses_template(html):
    return re.search(ELEMENT % ("template", "template"), html, re.S) is not None


def uses_canvas(html):
    return (re.search(ELEMENT % ("canvas", "canvas"), html, re.S) is not None
            or re.search(r"getContext\s*\(\s*['\"]2d", html) is not None)


def uses_webgl(html):
    return re.search(r"getContext\s*\(\s*['\"]webgl", html) is not None


def uses_esm(html):
    return re.search(r"\bimport\s*\(", html) is not None


# (id, what the recipient reads, the probe expression, `used(html)`, why it is load-bearing)
#
# **Ordered as they would bite**, which is R6 §7's phrase and a real ordering: a browser without
# custom properties has no type scale to lay a grid out in, so naming grid first would name a
# consequence.
#
# `s(q)` is bound in the emitted block and is `CSS.supports` with a false-on-anything fallback. A
# browser with no `CSS.supports` at all reports every CSS row missing, which is the safe direction:
# it is a browser old enough to fail them.
ROWS = (
    ("custom-properties", "CSS custom properties", "s('--a: 0')", uses_tokens,
     "The theme region is the deck's entire look expressed as custom properties, and every size "
     "inside the stage derives from `--du`. Without them there is no type scale, no colour and no "
     "spacing - and `.slide` stays at `opacity:0`, so the deck is blank rather than plain."),
    ("grid", "CSS grid", "s('display: grid')", uses_grid,
     "`.slide` is a four-row grid with its header, disclosure, body and bottom line placed "
     "explicitly (DS-040). In block flow the rows collapse into source order and the bottom line "
     "stops being anchored to the foot of the slide, which is DS-203's whole subject."),
    ("template", "the &lt;template&gt; element",
     "('content' in document.createElement('template'))", uses_template,
     "The quick view carries each cited source in a `<template class=\"qv-src\">` and clones it on "
     "demand (T-070). Where the element is not supported the parser does not treat its children as "
     "inert: the source's markup renders into the slide it was cited on."),
    ("canvas", "the 2D canvas", "!!(document.createElement('canvas').getContext)", uses_canvas,
     "A deck that draws into a canvas shows an empty box without one, and an empty box is "
     "indistinguishable from a figure that rendered nothing."),
    ("webgl", "WebGL", "('WebGLRenderingContext' in window)", uses_webgl,
     "3D is opt-in and rare, and a missing context is the one failure that renders as a black "
     "rectangle rather than as nothing at all."),
    # The probed URL is a `data:` one and not an empty string, which is T-093's doing and an
    # improvement rather than a concession: the form R6 §6 measured as working is the form worth
    # asking the browser about, and DS-005 reads the argument now.
    ("esm", "dynamic import()",
     "(function(){try{new Function('import(\"data:text/javascript,\")');return true}"
     "catch(e){return false}})()",
     uses_esm,
     "R6 §6: a deck that inlines an ESM library reaches it through `import()` of a blob, and the "
     "call site is a **parse** error where the syntax is unsupported - so the script carrying it "
     "never runs at all. Probed by parsing, not by importing, because the block runs before the "
     "first slide is parsed and cannot wait on a promise."),
)

# Considered and left out, each for the same stated reason: a row earns its place only where a real
# opening route makes it fail (the owner's rule, 2026-08-07, generalised from `isSecureContext`).
#
#   transform: scale()   - the stage's scaling. No browser has `display:grid` and not this; the
#                          grid row already covers every engine that would fail it.
#   Element.closest      - the delegated quick-view handler, and `Element.matches` in the keydown
#     / Element.matches    handler, which is unguarded. Same vintage as custom properties: there is
#                          no browser with one and not the other.
#   min()                - `.qv-sheet` sizes with `width:min(...)`, and it is the NEWEST feature in
#                          the shell. Left out anyway: an unsupported `min()` makes that one sheet
#                          auto-width, which is a worse quick view and not an unreadable deck.
#   text-wrap: balance   - DS-037, and `default`. Cosmetic by construction.
#   <use href>           - an engine wanting `xlink:href` drops the icons and keeps every word.
#
# The list is here rather than in the docs because it is the argument for the table's SIZE, and a
# reader's first question about a six-row table is what the seventh row would have been.


def emitted(html):
    """`[row]` - the rows this deck has a subject for, in the table's order."""
    body = BLOCK.sub("", html)
    return [r for r in ROWS if r[3](body)]


def block(html, indent=""):
    """The `<script id="preflight">` body for this deck. Never the surrounding tag."""
    rows = emitted(html)
    lines = [
        "",
        "/* Capability preflight (DS-009), emitted by tools/deck/preflight.py from what THIS deck",
        "   uses - R6 §7's floor, as a question the browser answers rather than a version number.",
        "   <html> ships carrying data-preflight, so the degraded state is what an unsupported",
        "   browser paints; this takes it off. Deliberately the most conservative script in the",
        "   file: it has to run on the browser it is judging. */",
        "(function(){",
        "var d=document.documentElement,m=[],",
        "    s=(window.CSS&&CSS.supports)?function(q){try{return CSS.supports(q)}"
        "catch(e){return false}}",
        "                               :function(){return false};",
    ]
    for _rid, name, probe, _used, _why in rows:
        lines.append("if(!%s)m.push('%s');" % (probe, name.replace("&lt;", "<").replace("&gt;", ">")))
    lines += [
        "if(!m.length){d.removeAttribute('data-preflight');return;}",
        "d.setAttribute('data-preflight','fail');",
        "var p=document.getElementById('preflightSay');",
        "if(p)p.textContent='This browser is missing '+m.join(', ')+\". The deck cannot present "
        "here, so every slide's content is below instead, in order.\";",
        "})();",
        "",
    ]
    return "\n".join(indent + ln if ln else ln for ln in lines)


# ------------------------------------------------------------------------------- reporting


def rows_report():
    print("The capability preflight - every row, and why it is a row.\n")
    print("A row is emitted only where the deck has a subject for it, and it earns its place in")
    print("this table only where a real opening route makes it fail. Both halves matter: the")
    print("first keeps the block small, the second keeps it honest.\n")
    for rid, name, probe, _used, why in ROWS:
        print("  %-18s %s" % (rid, name.replace("&lt;", "<").replace("&gt;", ">")))
        print("  %-18s probe: %s" % ("", probe))
        for line in wrap(why, 84):
            print("  %-18s %s" % ("", line))
        print("")


def wrap(text, width):
    out, line = [], ""
    for word in text.split():
        if len(line) + len(word) + 1 > width:
            out.append(line)
            line = word
        else:
            line = (line + " " + word).strip()
    if line:
        out.append(line)
    return out


def show(deck):
    html = read(deck)
    rows = emitted(html)
    rel = paths.display_path(deck, ROOT).replace("\\", "/")
    print("%s emits %d of %d row(s):\n" % (rel, len(rows), len(ROWS)))
    for rid, name, _p, _u, _w in rows:
        print("  %-18s %s" % (rid, name.replace("&lt;", "<").replace("&gt;", ">")))
    silent = [r for r in ROWS if r not in rows]
    if silent:
        print("\nnot emitted - this deck has no subject for them:\n")
        for rid, _n, _p, _u, _w in silent:
            print("  %s" % rid)
    body = block(html)
    print("\n%d bytes of preflight, %d of them the comment."
          % (len(body.encode("utf-8")), len(body.split("(function(){")[0].encode("utf-8"))))
    return 0


def read(path):
    import io
    return io.open(path, encoding="utf-8", newline="").read()


# ------------------------------------------------------------------------------- prove (L-04)


# Each entry suppresses one capability in a COPY of the deck and says how honestly it does it.
# **`template` is a real suppression**: deleting the prototype property removes the capability, not
# the answer about it, and the deck's own `tpl.content.cloneNode` breaks exactly as it would on a
# browser that never had it. The two CSS rows cannot be taken away from Chrome at all, so what they
# suppress is the detector - which proves the row's wiring and the degraded state, and does not
# prove the capability's absence. Saying which is which is the point (**L-05**).
SUPPRESSIONS = {
    "template": ("delete HTMLTemplateElement.prototype.content;",
                 "REAL - the capability is gone, not the answer about it"),
    "grid": ("var _s=CSS.supports.bind(CSS);CSS.supports=function(){"
             "var a=[].slice.call(arguments);"
             "if(/grid/.test(a.join(':')))return false;return _s.apply(null,a)};",
             "DETECTOR ONLY - Chrome cannot be made to lack CSS grid"),
    "custom-properties": ("var _s=CSS.supports.bind(CSS);CSS.supports=function(){"
                          "var a=[].slice.call(arguments);"
                          "if(/--a/.test(a.join(':')))return false;return _s.apply(null,a)};",
                          "DETECTOR ONLY - Chrome cannot be made to lack custom properties"),
}


def suppressed_copy(html, what):
    """The deck with `what` taken away, by a script that runs BEFORE the preflight does."""
    js, _how = SUPPRESSIONS[what]
    if '<script id="preflight">' not in html:
        sys.exit("this deck carries no preflight - run `shell.py preflight <deck>` first")
    return html.replace('<script id="preflight">',
                        "<script>/* T-019 suppression: %s */%s</script>\n"
                        '<script id="preflight">' % (what, js), 1)


def scriptless_copy(html):
    """The deck with every script removed - what a browser that runs none renders, reproducibly.

    Suppressing scripting in the engine instead was tried both ways Chrome offers and neither
    survives; the comment at the screenshot call says which failed how.
    """
    return re.sub(r"<script\b[^>]*>.*?</script>", "", html, flags=re.S)


# `<html ...>` as the PARSER sees it: the first tag in the document, never a mention of one.
#
# This read `<html[^>]*\bdata-preflight="..."` anywhere in the dump and reported the control as
# degraded - because `shell.html`'s own comment explains the marker by quoting the tag, and with
# the attribute correctly removed from the real element the search ran on and found the comment.
# A passing deck was reported as failing, by an instrument reading documentation about the thing it
# was measuring (**L-06**).
HTML_TAG = re.compile(r"(?s).*?<html([^>]*)>")
MARKER = re.compile(r'\bdata-preflight="([^"]*)"')


def marker_of(dom):
    """The value of `data-preflight` on the document element, or None if it was taken off."""
    tag = HTML_TAG.match(dom)
    if not tag:
        return None
    found = MARKER.search(tag.group(1))
    return found.group(1) if found else None


def unescape(text):
    return (text.replace("&lt;", "<").replace("&gt;", ">")
                .replace("&quot;", '"').replace("&#39;", "'").replace("&amp;", "&"))


def prove(deck, out=None):
    """Suppress each capability in turn, in real Chrome, offline, and read back what it said."""
    import render

    html = read(deck)
    dest = out or render.out_dir(deck)
    os.makedirs(dest, exist_ok=True)
    rel = paths.display_path(deck, ROOT).replace("\\", "/")
    print("deck:    %s\nbrowser: %s\nout:     %s\n" % (rel, render.CHROME, dest))

    cases = [(rid, SUPPRESSIONS[rid][1]) for rid, _n, _p, _u, _w in emitted(html)
             if rid in SUPPRESSIONS]
    cases.append(("no-script", "REAL - the script never runs, which no preflight can catch"))
    cases.insert(0, ("none", "the control: nothing suppressed, and it must NOT degrade"))

    results = []
    for case, how in cases:
        path = os.path.join(dest, "preflight-%s.html" % case)
        if case == "none":
            variant = html
        elif case == "no-script":
            variant = scriptless_copy(html)
        else:
            variant = suppressed_copy(html, case)
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(variant)
        dom, err = render.chrome_run(render.file_url(path), 1280, 900, ["--dump-dom"])
        if not dom:
            print("  %-18s NO DOM  %s" % (case, err[:120]))
            results.append((case, None, "", how))
            continue
        said = re.search(r'<p class="preflight-say" id="preflightSay">(.*?)</p>', dom, re.S)
        text = unescape(" ".join(said.group(1).split())) if said else ""
        results.append((case, marker_of(dom), text, how))
        # The shot is the point of the exercise (**L-01**).
        #
        # **Both of Chrome's ways to switch scripting off were tried here and neither can be used.**
        # `--blink-settings=scriptEnabled=false` really does disable it and then produces neither a
        # screenshot nor a `--dump-dom` payload - honest and useless. `--disable-javascript` writes
        # the screenshot and DOES NOT DISABLE ANYTHING: the deck presented normally under it, which
        # is a lie in the optimistic direction (**L-15**) and would have shipped a picture of a
        # working deck labelled as the no-script state. So the file carries the suppression instead:
        # a deck with its scripts removed renders exactly what a browser refusing to run them does,
        # and it renders it reproducibly.
        render.chrome_run(render.file_url(path), 1280, 900,
                          ["--screenshot=" + os.path.join(dest, "preflight-%s.png" % case)])

    print("  %-18s %-9s %s" % ("suppressed", "marker", "what the recipient reads"))
    for case, marker, text, _how in results:
        print("  %-18s %-9s %s" % (case, marker if marker is not None else "(removed)", text[:74]))
    print("")
    for case, _m, _t, how in results:
        print("  %-18s %s" % (case, how))

    rows = dict((r[0], r) for r in ROWS)
    control = [r for r in results if r[0] == "none"]
    clean = bool(control) and control[0][1] is None
    suppressed = [r for r in results if r[0] not in ("none", "no-script")]
    named = [r for r in suppressed
             if r[1] == "fail" and unescape(rows[r[0]][1]).lower() in r[2].lower()]
    nojs = [r for r in results if r[0] == "no-script" and r[1] == "pending"]
    print("\n  control does not degrade         %s"
          % ("yes" if clean else "NO - a working deck showed the warning"))
    print("  a suppressed row is NAMED        %d of %d" % (len(named), len(suppressed)))
    print("  no script still degrades         %s" % ("yes" if nojs else "NO"))
    print("\nShots are beside the copies. Open them - a preflight nobody looked at is not "
          "evidence (**L-01**).")
    return 0 if (clean and nojs and len(named) == len(suppressed)) else 1


# ------------------------------------------------------------------------------- self-test


def self_test():
    """Fixtures whose answers are known, one per row and one per way the scan can lie (**L-04**)."""
    failures, ran = [], []

    def ok(label, condition, detail=""):
        print("  %-4s %-58s %s" % ("ok" if condition else "FAIL", label, "" if condition else detail))
        ran.append(label)
        if not condition:
            failures.append(label)

    ids = [r[0] for r in ROWS]
    ok("every row id is unique", len(set(ids)) == len(ids))
    ok("every row states why it is load-bearing", all(len(r[4]) > 60 for r in ROWS))

    # Each row fires on its own subject and on nothing else's. A table where two rows share a
    # trigger is a table that cannot emit one without the other.
    subjects = {
        "custom-properties": "<style>a{color:var(--ink)}</style>",
        "grid": "<style>.slide{display:grid}</style>",
        "template": '<template class="qv-src"><p>x</p></template>',
        "canvas": '<canvas id="c"></canvas>',
        "webgl": "<script>c.getContext('webgl2')</script>",
        "esm": "<script>import('data:text/javascript,')</script>",
    }
    ok("the table and the fixtures name the same rows", set(subjects) == set(ids))
    for rid, fixture in sorted(subjects.items()):
        fired = [r[0] for r in emitted(fixture)]
        ok("%s fires on its own subject" % rid, fired == [rid],
           "fired %s" % (fired or "nothing"))

    ok("an empty file emits nothing", emitted("") == [])

    # The failure the sprite scan actually had, one file along: font payload is ~170 KB of base64
    # and a loose pattern reads words out of it.
    payload = "data:font/woff2;base64," + ("gridcanvastemplateimportwebgl" * 400)
    ok("base64 font payload fires no row", emitted(payload) == [])

    # And the failure THIS scan actually had, found by this fixture on the first run: the shared
    # component block and the deck script each explain the quick view in a comment that names the
    # tag, so every deck ever built emitted the `<template>` row, quick view or no quick view.
    prose = ("/* cloned from the cited slide's own <template class=\"qv-src\"> */\n"
             "<!-- an unsupported <template> is an unknown element -->\n"
             "<style>a{color:#000}</style>")
    ok("a comment naming an element is not that element", emitted(prose) == [],
       "fired %s" % [r[0] for r in emitted(prose)])

    # And the one this scan would have had: its own probe source mentions every capability it
    # tests, so a deck carrying a preflight must not be read as using them.
    seeded = '<script id="preflight">%s</script>' % block(subjects["canvas"])
    ok("a deck's own preflight is not evidence about the deck", emitted(seeded) == [])

    # The emitted block. It must be ES5, and it must not carry a row it was not asked for.
    one = block(subjects["grid"])
    ok("the block names the row it emitted", "CSS grid" in one)
    ok("and carries no row the deck has no subject for",
       "WebGL" not in one and "canvas" not in one)
    ok("the block is ES5 - it runs on the browser it judges",
       "=>" not in one and "const " not in one and "let " not in one and "`" not in one)
    ok("the block takes the marker off when every row passes",
       "removeAttribute('data-preflight')" in one)
    ok("and puts a reason in it when one does not",
       "setAttribute('data-preflight','fail')" in one)
    ok("nothing in the block can close the script element",
       "</script" not in block("".join(subjects.values())))

    all_rows = block("".join(subjects.values()))
    ok("a deck using everything emits every row",
       all(name.replace("&lt;", "<").replace("&gt;", ">") in all_rows for _i, name, _p, _u, _w in ROWS))
    ok("and a deck using nothing still emits the block that clears the marker",
       "removeAttribute('data-preflight')" in block(""))

    print("\n%d of %d fixtures behaved as specified.\n" % (len(ran) - len(failures), len(ran)))
    return failures


# ------------------------------------------------------------------------------- cli


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
    if cmd == "rows":
        rows_report()
        return 0
    if cmd == "show":
        if not rest:
            sys.exit("usage: preflight.py show <deck>")
        return show(os.path.abspath(rest[0]))
    if cmd == "prove":
        if not rest:
            sys.exit("usage: preflight.py prove <deck> [--out <dir>]")
        out = None
        if "--out" in rest:
            i = rest.index("--out")
            if i + 1 >= len(rest):
                sys.exit("--out needs a directory")
            out = os.path.abspath(rest[i + 1])
        return prove(os.path.abspath(rest[0]), out)
    sys.exit("unknown command %r - one of: rows, show, prove" % cmd)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
