#!/usr/bin/env python3
"""Carry a source document inside the deck, so a provenance mark can be opened rather than read.

    python tools/deck/quickview.py plan <deck> --source <title>=<path> [--source ...]
    python tools/deck/quickview.py add  <deck> --source <title>=<path> [--source ...] [-o out.html]
    python tools/deck/quickview.py list <deck>

**`plan` is the default posture and `add` is the exception**, because the failure this feature can
cause is not a broken deck - it is a client's internal document arriving in everyone's inbox
(T-070 §1). Embedding is opt-in per source, `plan` says exactly what would be carried and what it
costs, and nothing is written without `add`. `add` refuses a source `plan` would have refused.

**Admission is three tests, not a list of file types** (T-070, settled by the owner 2026-08-10):

  1. it embeds with **zero external references** (DS-001), or it is a link and DS-105 already
     handles it;
  2. it **executes no script** into the deck. A source is evidence; evidence that can rewrite the
     argument around it is not evidence;
  3. it keeps the deck inside the measured size bound.

A type that passes all three is in without a further decision. `.docx` and `.pdf` fail test 1 in
this repository's terms - they need a parser **L-07** will not let it acquire - and video is
linked-never-embedded, which makes it DS-105's external-URL case.

**DS-110 is narrowed by scope, not relaxed.** What the build *produces* stays vector always; what a
source *is* may be quoted in the form it exists in, raster included, and only inside
`<template class="qv-src">`. Where a source offers a vector form as well, this tool takes it and
refuses the raster by name.

Runs its own self-test first and refuses to report if it fails (**L-04**). Pure standard library
(**L-07**).
"""

import base64
import io
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths                                                        # noqa: E402
import shell as shell_mod                                           # noqa: E402

ROOT = shell_mod.ROOT

# **The bound is the deck, not the source.** R5 measured a full 12-slide deck at 192 KB and the two
# shipped here are 232 and 244 KB; a deck that has to be uploaded rather than emailed has lost the
# property the whole project is built on (CLAUDE.md rule 2). 5 MB is the smallest common attachment
# limit still in wide use, and half of it is the working bound so a deck stays comfortable rather
# than just legal.
SIZE_BOUND = 2 * 1024 * 1024

RASTER = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
          ".gif": "image/gif", ".webp": "image/webp"}
VECTOR_INSTEAD = (".svg", ".md", ".txt", ".html")

# Anything that can fetch, execute, or restyle the deck around it. Stripped rather than escaped,
# because a source is being *quoted*: what is dropped is not part of what it says.
# **Two alternatives, and the first one is why.** A single pattern ending at `</\1>|/?>` matches the
# shortest of the two, which is the opening tag's own `>` - so `<style>` vanished and its rules were
# left behind as text, with the closing tag after them. Caught by embedding a hostile source and
# reading what landed in the deck, not by reading the regex (**L-01**). Paired elements are removed
# with their contents; void ones are removed alone.
INERT = re.compile(r"<\s*(script|style|iframe|object|form|noscript)\b[^>]*>.*?</\s*\1\s*>"
                   r"|<\s*(?:script|style|link|meta|base|embed|iframe|object)\b[^>]*/?>",
                   re.S | re.I)
EVENT_ATTR = re.compile(r"\son[a-z]+\s*=\s*(\"[^\"]*\"|'[^']*'|[^\s>]+)", re.I)
# `javascript:` and `data:text/html` in an href are both script by another route.
BAD_URL = re.compile(r"(href|src|xlink:href)\s*=\s*(\"|')?\s*(javascript:|data:text/html)", re.I)
EXTERNAL = re.compile(r"(?:href|src)\s*=\s*[\"']?(https?:)?//", re.I)
ANCHOR = re.compile(r"<a\b[^>]*href\s*=\s*[\"']([^\"']*)[\"'][^>]*>(.*?)</a>", re.S | re.I)
ID_ATTR = re.compile(r"\sid\s*=\s*(\"[^\"]*\"|'[^']*')", re.I)


class Refused(Exception):
    """A source that fails an admission test, with which test it failed."""


def esc(text):
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def inline(text):
    """Emphasis, code and links inside one line of Markdown.

    A source's own link becomes **text plus its target in mono**, which is the whole of this tool's
    answer to DS-105 and DS-001 at once: nothing here is a link, so nothing here can be dead or
    reach the network, and the reader still sees where the source pointed.
    """
    out = esc(text)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    out = re.sub(r"\[([^\]]+)\]\(([^)\s]+)[^)]*\)",
                 r'\1 <span class="qv-href">\2</span>', out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", out)
    out = re.sub(r"(?<![*\w])\*([^*]+)\*(?!\w)", r"<i>\1</i>", out)
    return out


def front_matter(lines):
    """`(rows, rest)` - a leading YAML block as key/value pairs, or `([], lines)`.

    **130 of 355 corpus source documents open with one**, and without this branch the block renders
    as a paragraph of `key: value` runs between two rules. Rendered as a table rather than dropped:
    dropping content out of a quoted source is the one thing a provenance surface must not do, and
    the quick view carries a fidelity claim on its own face (T-070).
    """
    if not lines or lines[0].strip() != "---":
        return [], lines
    for i in range(1, len(lines)):
        if lines[i].strip() in ("---", "..."):
            rows = []
            for ln in lines[1:i]:
                if not ln.strip() or ln.startswith((" ", "\t", "-")):
                    # nested or list-valued YAML: kept as its own row rather than parsed. This
                    # renders metadata, it does not implement YAML.
                    if rows:
                        rows[-1][1] = (rows[-1][1] + " " + ln.strip()).strip()
                    continue
                key, sep, val = ln.partition(":")
                rows.append([key.strip(), val.strip()] if sep else [ln.strip(), ""])
            return rows, lines[i + 1:]
    return [], lines


def markdown(text):
    """Enough Markdown to read a source document, and nothing that needs a dependency (**L-07**).

    Front matter, headings, paragraphs, ordered and unordered lists, thematic breaks, tables,
    quotes and fences - the shapes source documents are actually written in, audited against the
    355-document corpus by T-107 rather than assumed. Anything unrecognised stays as its own
    paragraph, which is the safe direction: a source renders as plainer than it was, never as
    something it is not.

    **Two constructs are known to be missing and are counted rather than forgotten**: a nested list
    is flattened to one level (995 lines in 125 corpus documents) and an indented code block becomes
    paragraphs (958 lines in 124). Both change how the renderer holds state rather than adding a
    branch to it, so both are T-121. Setext headings are not missing: the corpus uses `===` zero
    times and `---`-under-text once in 355 documents, so `---` is read as a thematic break with no
    ambiguity worth resolving.
    """
    lines = text.split("\n")
    fm, lines = front_matter(lines)
    text = "\n".join(lines)
    out, para, rows, lst, fence = [], [], [], None, None
    if fm:
        out.append("<table>%s</table>"
                   % "".join("<tr><th>%s</th><td>%s</td></tr>" % (inline(k), inline(v))
                             for k, v in fm))
    def flush_para():
        if para:
            out.append("<p>%s</p>" % inline(" ".join(para)))
            del para[:]
    def flush_rows():
        if rows:
            body = []
            for i, cells in enumerate(rows):
                tag = "th" if i == 0 else "td"
                body.append("<tr>%s</tr>" % "".join("<%s>%s</%s>" % (tag, inline(c), tag)
                                                    for c in cells))
            out.append("<table>%s</table>" % "".join(body))
            del rows[:]
    # `ol` or `ul`. A one-element list rather than `nonlocal`, matching how `para` and `rows` are
    # already held. An ordered list rendered as `<ul>` loses the numbering a source used to order
    # its steps - 1994 lines in 161 corpus documents were losing it.
    kind = ["ul"]
    def flush_list():
        if lst is not None and lst:
            out.append("<%s>%s</%s>" % (kind[0],
                                        "".join("<li>%s</li>" % inline(i) for i in lst),
                                        kind[0]))

    for raw in text.split("\n"):
        line = raw.rstrip()
        if fence is not None:
            if line.strip().startswith("```"):
                out.append("<pre>%s</pre>" % esc("\n".join(fence)))
                fence = None
            else:
                fence.append(line)
            continue
        if line.strip().startswith("```"):
            flush_para(); flush_rows()
            if lst: flush_list()
            lst = None
            fence = []
            continue
        if not line.strip():
            flush_para(); flush_rows()
            if lst: flush_list()
            lst = None
            continue
        head = re.match(r"(#{1,6})\s+(.*)", line)
        if head:
            flush_para(); flush_rows()
            if lst: flush_list()
            lst = None
            level = min(3, len(head.group(1)))
            out.append("<h%d>%s</h%d>" % (level, inline(head.group(2)), level))
            continue
        if line.lstrip().startswith("|") and line.rstrip().endswith("|"):
            flush_para()
            if lst: flush_list()
            lst = None
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if not all(re.match(r"^:?-{2,}:?$", c) for c in cells):
                rows.append(cells)
            continue
        # A thematic break, before the list branch: `- - -` is not a list item, and `---` under a
        # line of text is a setext heading exactly once in 355 corpus documents (T-107).
        if re.match(r"^(?:-{3,}|\*{3,}|_{3,}|(?:[-*_] ){2,}[-*_])\s*$", line.strip()):
            flush_para(); flush_rows()
            if lst: flush_list()
            lst = None
            out.append("<hr>")
            continue
        item = re.match(r"\s*(?:[-*+]|(\d+)[.)])\s+(.*)", line)
        if item:
            flush_para(); flush_rows()
            if lst is None:
                lst = []
                kind[0] = "ol" if item.group(1) else "ul"
            lst.append(item.group(2))
            continue
        if line.lstrip().startswith(">"):
            flush_para(); flush_rows()
            if lst: flush_list()
            lst = None
            out.append("<blockquote>%s</blockquote>" % inline(line.lstrip().lstrip(">").strip()))
            continue
        if lst is not None:
            flush_list()
            lst = None
        rows and flush_rows()
        para.append(line.strip())
    flush_para(); flush_rows()
    if lst: flush_list()
    return "".join(out)


def make_inert(html):
    """Markup a source brought, with everything that could act on the deck removed.

    Test 2 is structural in *where the result sits* - a `<template>` runs nothing whatever it holds
    - and this is the second half: what is cloned out of that template must not be able to restyle
    or rewrite the deck either. Ids go because they would collide with the deck's own; `<style>`
    goes because a source's stylesheet is not scoped to the source.
    """
    removed = []
    def count(pat, text, what):
        n = len(pat.findall(text))
        if n:
            removed.append("%d %s" % (n, what))
        return pat.sub("", text)

    out = count(INERT, html, "element(s) that can act on the deck (script, style, iframe, form)")
    out = count(EVENT_ATTR, out, "event handler(s)")
    out = count(ID_ATTR, out, "id(s), which would collide with the deck's own")
    links = len(ANCHOR.findall(out))
    if links:
        removed.append("%d link(s), shown as their target in text" % links)
    out = ANCHOR.sub(lambda m: '%s <span class="qv-href">%s</span>'
                     % (m.group(2), esc(m.group(1))), out)
    return out, removed


def admit(path, body):
    """Run the three tests over a rendered body, or raise `Refused` naming the one it failed."""
    if EXTERNAL.search(body):
        raise Refused("test 1 (zero external references, DS-001): %s renders a reference to another "
                      "host. A source that needs the network is a link, and DS-105 handles those"
                      % os.path.basename(path))
    if re.search(r"<\s*script\b", body, re.I) or BAD_URL.search(body):
        raise Refused("test 2 (executes no script): %s renders script into the deck. A source is "
                      "evidence; evidence that can rewrite the argument around it is not evidence"
                      % os.path.basename(path))
    return body


def render(path):
    """`(body, kind, removed)` - a source as inert markup, admitted, and what was taken out of it.

    **What was removed is reported rather than absorbed.** A quoted source that quietly lost three
    elements is a rendering that misrepresents its original, which is DS-102's problem wearing a
    quick view (T-070 §1) - the author has to be able to see that the quote is shorter than the
    source before deciding to carry it.
    """
    ext = os.path.splitext(path)[1].lower()
    if ext in RASTER:
        # DS-110 as narrowed: a raster is the LAST resort, and a vector form of the same source
        # wins wherever there is one. Refused by name rather than silently preferred, so the
        # builder is told what it has rather than given something else.
        stem = os.path.splitext(path)[0]
        for other in VECTOR_INSTEAD:
            if os.path.exists(stem + other):
                raise Refused("DS-110: %s exists beside it, and where a source offers a vector form "
                              "the builder takes it. Raster is the last resort, not a parallel "
                              "option" % os.path.basename(stem + other))
        with open(path, "rb") as fh:
            data = base64.b64encode(fh.read()).decode("ascii")
        return ('<img src="data:%s;base64,%s" alt="%s">'
                % (RASTER[ext], data, esc(os.path.basename(path))), "raster", [])
    text = io.open(path, encoding="utf-8", errors="replace").read()
    if ext in (".svg", ".html", ".htm"):
        body, removed = make_inert(text)
        return admit(path, body), ("svg" if ext == ".svg" else "html"), removed
    if ext == ".md":
        return admit(path, markdown(text)), "markdown", []
    return admit(path, "<pre>%s</pre>" % esc(text)), "text", []


# What may sit in front of the title inside a `.sources-item`, and be carried through unchanged:
# the short identifier and the kind glyph (T-109). Both are the component's, not the route's, so
# wiring a quick view must preserve them rather than rebuild them - a `D1` this tool dropped would
# be a defect in the mark that only shows up on the slides a source happens to be wired into.
ITEM_HEAD = (r'(?:<span class="sources-id">[^<]*</span>)?'
             r'(?:<svg class="sources-icon"[^>]*>.*?</svg>)?')


def item_pattern(title):
    return re.compile(r'<span class="sources-item">(%s)%s</span>' % (ITEM_HEAD, re.escape(title)),
                      re.S)


def carried(html):
    """`[(title, bytes)]` - the quick views a deck already carries, one row per source."""
    return [(m.group(1), len(m.group(2).encode("utf-8")))
            for m in re.finditer(r'<template class="qv-src" data-qv="([^"]*)">(.*?)</template>',
                                 html, re.S)]


def wire(html, title, body, file=""):
    """The deck with a control on **every** mark citing `title`, and **one** copy of the rendering.

    A source cited by six slides is one document, not six. The control goes on all six because a
    reader opens the source from the slide they are looking at; the `<template>` goes on the first,
    and the script finds it by `data-qv` rather than by position - six copies of one document would
    be the size cost this feature has to justify, spent on nothing.

    `file` is the source's **base name and nothing above it** (T-109). The quick view names it so a
    reader can find the original outside the deck, and a directory would describe the author's
    machine rather than the document - which the handoff rules and DS-105's reasoning both refuse.
    """
    pat = item_pattern(title)
    hits = len(pat.findall(html))
    if not hits:
        raise Refused("no provenance item reads %r in this deck. A quick view is attached to a "
                      "source a slide already cites - if the slide does not cite it, that is a "
                      "specification question and not this tool's (T-069)" % title)
    control = ('<span class="sources-item">%%s<button class="sources-open" type="button" '
               'data-qv="%s" data-file="%s">%s</button>%%s</span>'
               % (esc(title), esc(os.path.basename(file)), title))
    first = [True]

    def swap(m):
        head = m.group(1) or ""
        if first[0]:
            first[0] = False
            return control % (head, '<template class="qv-src" data-qv="%s">%s</template>'
                                    % (esc(title), body))
        return control % (head, "")

    return pat.sub(swap, html)


def plan(deck, sources, write=False, out=None):
    html = shell_mod.read(deck)
    before = len(html.encode("utf-8"))
    print("deck: %s - %d bytes, %d quick view(s) already carried"
          % (paths.display_path(deck, ROOT), before, len(carried(html))))
    print("\n**What this would put inside the deck.** Every recipient of the file gets every line "
          "of it.\n")
    refused, added = [], 0
    for title, path in sources:
        try:
            body, kind, removed = render(path)
            html = wire(html, title, body, path)
        except Refused as exc:
            refused.append((title, str(exc)))
            print("  REFUSED  %-28s %s" % (title, exc))
            continue
        cost = len(body.encode("utf-8"))
        added += cost
        print("  %-8s %-28s %s -> %d bytes"
              % (kind, title, paths.display_path(path, ROOT), cost))
        for what in removed:
            print("           neutralised %s" % what)
    after = len(html.encode("utf-8"))
    print("\n  deck %d -> %d bytes (+%d), bound %d" % (before, after, added, SIZE_BOUND))
    if after > SIZE_BOUND:
        print("\nREFUSED test 3 (size): the deck would be %d bytes, past the %d bound. Nothing "
              "written." % (after, SIZE_BOUND))
        return 1
    if refused and write:
        print("\nNothing written: %d source(s) were refused, and a partial write would leave a deck "
              "whose provenance says less than the run reported." % len(refused))
        return 1
    if not write:
        print("\nNothing written. Re-run with `add` to embed exactly what is listed above.")
        return 1 if refused else 0
    target = out or deck
    shell_mod.write(target, html)
    print("\nwrote %s - %d bytes" % (paths.display_path(target, ROOT), after))
    return 0


def self_test():
    """One fixture per refusal this tool claims to make, and one for the shape it produces."""
    # **One fixture per construct the corpus uses**, not per construct someone remembered. T-107
    # counted them across 355 source documents, and the gap that reached a shipped deck - 7
    # `<p>---</p>` and 0 `<hr>` - was a construct in 119 of them that no fixture named. A self-test
    # narrower than the input is what makes L-04's guarantee narrower than it reads.
    md = markdown("---\ntitle: A source\n---\n\n# Title\n\nA line with **bold** and `code`.\n\n"
                  "- one\n- two\n\n1. first\n2. second\n\n---\n\n> quoted\n\n```\nfenced\n```\n\n"
                  "| a | b |\n| :-- | :-- |\n| 1 | 2 |\n")
    for want, construct in (("<th>title</th>", "front matter, in 130 of 355 corpus documents"),
                            ("<h1>Title</h1>", "an ATX heading"),
                            ("<b>bold</b>", "bold"),
                            ("<code>code</code>", "inline code"),
                            ("<ul><li>one</li>", "an unordered list"),
                            ("<ol><li>first</li>", "an ordered list, as <ol> and not <ul>"),
                            ("<hr>", "a thematic break, in 119 of 355 corpus documents"),
                            ("<blockquote>quoted</blockquote>", "a quote"),
                            ("<pre>fenced</pre>", "a fence"),
                            ("<th>a</th>", "a table heading"),
                            ("<td>1</td>", "a table cell")):
        if want not in md:
            sys.exit("SELF-TEST FAILED: the Markdown renderer dropped %s - wanted %r, got %r"
                     % (construct, want, md))
    if "<p>---</p>" in md:
        sys.exit("SELF-TEST FAILED: a thematic break shipped as a paragraph of hyphens, which is "
                 "the T-107 defect exactly: 7 of them reached a presented deck")

    hostile = ('<p>real content</p><script>document.body.innerHTML="";</script>'
               '<style>.slide{display:none}</style><div id="stage" onclick="go(99)">x</div>'
               '<a href="javascript:alert(1)">link</a>')
    inert, removed = make_inert(hostile)
    if not removed:
        sys.exit("SELF-TEST FAILED: a hostile source was neutralised and the run said nothing was "
                 "taken out. A quote shorter than its source, reported as whole, is the fidelity "
                 "claim T-070 exists to keep honest")
    if "real content" not in inert:
        sys.exit("SELF-TEST FAILED: making a source inert dropped the source")
    # **The bodies go with the tags.** A pattern that removed `<style>` and left its rules as text
    # passed every tag-shaped assertion below; what caught it was reading the template that landed
    # in a real deck. Asserted here in the terms that failed.
    for leftover in (".slide{display:none}", "document.querySelector"):
        if leftover in inert:
            sys.exit("SELF-TEST FAILED: %r survived into the quick view. The element was removed "
                     "and its contents were not, which is a source's stylesheet rendered as prose "
                     "and, one parser bug away, as a stylesheet" % leftover)
    for bad, what in (("<script", "a script tag"), ("<style", "a stylesheet"),
                      ("onclick", "an event handler"), ('id="stage"', "an id colliding with the "
                                                                     "deck's own"),
                      ("<a ", "a link, which is a target this deck cannot promise is live"),
                      ("href=", "an href of any kind")):
        if bad in inert:
            sys.exit("SELF-TEST FAILED: %s survived into the quick view. A source that can act on "
                     "the deck around it is not a source, it is a second script (T-070 test 2)"
                     % what)
    # **The `javascript:` URL survives as text and that is the right answer**, not a miss: it is
    # rendered as the target the source pointed at, escaped, in a `<span>`. Asserted so nobody
    # "fixes" it into a strip - what would be lost is the reader's view of where the source led.
    if "javascript:alert(1)" not in inert:
        sys.exit("SELF-TEST FAILED: the link's target was dropped rather than shown as text. The "
                 "reader is meant to see where the source pointed, without being able to follow it")
    # An attribute `make_inert` does not rewrite - SVG's `xlink:href` - still has to be refused.
    try:
        admit("x.svg", '<svg><a xlink:href="javascript:alert(1)"><rect/></a></svg>')
        sys.exit("SELF-TEST FAILED: a javascript: url in an attribute this tool does not rewrite "
                 "was admitted")
    except Refused as exc:
        if "test 2" not in str(exc):
            sys.exit("SELF-TEST FAILED: a javascript: url was refused by the wrong test: %s" % exc)

    # The tests refuse rather than sanitising away, where the defect is what the source IS.
    try:
        admit("x.html", '<img src="https://example.com/a.png">')
        sys.exit("SELF-TEST FAILED: a source referencing another host was admitted - DS-001 is the "
                 "one rule the whole project rests on")
    except Refused as exc:
        if "test 1" not in str(exc):
            sys.exit("SELF-TEST FAILED: an external reference was refused by the wrong test: %s" % exc)
    try:
        admit("x.html", '<div><script src="a.js"></script></div>')
        sys.exit("SELF-TEST FAILED: a source carrying script was admitted")
    except Refused as exc:
        if "test 2" not in str(exc):
            sys.exit("SELF-TEST FAILED: script was refused by the wrong test: %s" % exc)

    # Wiring, and the refusal that keeps it honest.
    deck = '<span class="sources-box"><span class="sources-item">Cost model</span></span>'
    wired = wire(deck, "Cost model", "<p>x</p>")
    if 'class="sources-open"' not in wired or '<template class="qv-src"' not in wired:
        sys.exit("SELF-TEST FAILED: wiring produced neither a control nor a template - %r" % wired)
    if carried(wired) != [("Cost model", len("<p>x</p>"))]:
        sys.exit("SELF-TEST FAILED: a wired deck does not report the quick view it carries - %r"
                 % carried(wired))
    try:
        wire(deck, "Nobody cites this", "<p>x</p>")
        sys.exit("SELF-TEST FAILED: a quick view was attached to a source no slide cites")
    except Refused:
        pass

    # T-109. The identifier and the kind glyph belong to the component, not to the route, so wiring
    # carries them through untouched; the file name is a base name, because a directory would
    # describe the author's machine. Both are asserted by breaking them, like everything above.
    typed = ('<span class="sources-box"><span class="sources-item">'
             '<span class="sources-id">D1</span>'
             '<svg class="sources-icon" aria-hidden="true"><use href="#i-src-doc"/></svg>'
             'Cost model</span></span>')
    wired = wire(typed, "Cost model", "<p>x</p>", os.path.join("some", "where", "cost-model.md"))
    if 'class="sources-id">D1<' not in wired:
        sys.exit("SELF-TEST FAILED: wiring dropped the source's identifier - %r" % wired)
    if 'class="sources-icon"' not in wired:
        sys.exit("SELF-TEST FAILED: wiring dropped the source's kind glyph - %r" % wired)
    if 'data-file="cost-model.md"' not in wired:
        sys.exit("SELF-TEST FAILED: the quick view control names no file, or names a path rather "
                 "than a base name - %r" % wired)
    return True


def main(argv):
    if not argv:
        print(__doc__.strip())
        return 2
    self_test()
    cmd, rest = argv[0], argv[1:]
    if cmd == "list":
        if not rest:
            sys.exit("usage: quickview.py list <deck>")
        html = shell_mod.read(rest[0])
        rows = carried(html)
        print("%s - %d quick view(s), %d bytes of deck"
              % (paths.display_path(rest[0], ROOT), len(rows),
                 len(html.encode("utf-8"))))
        for title, cost in rows:
            print("  %-30s %d bytes" % (title, cost))
        if not rows:
            print("  none. `quickview.py plan <deck> --source <title>=<path>` says what one costs.")
        return 0
    if cmd not in ("plan", "add"):
        sys.exit("usage: quickview.py plan|add|list <deck> [--source <title>=<path>]")
    if not rest:
        sys.exit("usage: quickview.py %s <deck> --source <title>=<path>" % cmd)
    deck = rest[0]
    sources = []
    for i, a in enumerate(rest):
        if a == "--source" and i + 1 < len(rest):
            spec = rest[i + 1]
            if "=" not in spec:
                sys.exit("--source takes <title>=<path>, got %r" % spec)
            title, path = spec.split("=", 1)
            sources.append((title.strip(), path.strip()))
    if not sources:
        sys.exit("no --source given; there is nothing to plan")
    out = None
    if "-o" in rest:
        out = rest[rest.index("-o") + 1]
    return plan(deck, sources, write=(cmd == "add"), out=out)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
