#!/usr/bin/env python3
"""Carry a source document inside the deck, so a provenance mark can be opened rather than read.

    python tools/deck/quickview.py plan    <deck> --source <title>=<path> [--source ...]
    python tools/deck/quickview.py add     <deck> --source <title>=<path> [--source ...] [-o out.html]
    python tools/deck/quickview.py refresh <deck> --source <title>=<path> [--write] [-o out.html]
    python tools/deck/quickview.py check   <deck> --source <title>=<path> [--source ...]
    python tools/deck/quickview.py list    <deck>

**`plan` is the default posture and `add` is the exception**, because the failure this feature can
cause is not a broken deck - it is a client's internal document arriving in everyone's inbox
(T-070 §1). Embedding is opt-in per source, `plan` says exactly what would be carried and what it
costs, and nothing is written without `add`. `add` refuses a source `plan` would have refused.

**`refresh` re-renders what a deck already carries** (T-179). It is a third verb rather than a flag
because it answers a different question from `add`, and refuses on different grounds: `add` asks
whether a slide cites the source at all, `refresh` asks whether the deck already carries a quick
view for it. It exists because a renderer fix cannot otherwise reach a deck that has already
shipped - once wired, the item `add` looks for is gone. Same posture as `plan`: it writes nothing
without `--write`.

**`check` is the half a refresh verb cannot cover** (T-181). `refresh` made the drift
*reachable*; nothing made it *detectable*, so the three corrections T-179 found stranded inside
one deck had sat there through every green gate this repository runs. `check` asks `refresh`'s
question, writes nothing under any flag, and exits non-zero when a rendering has moved. What it
prints separates the two causes: a **tag histogram difference** is a renderer that changed, a
**differing word** is a source document that was edited, and a byte count is neither (**L-118**).

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


def unesc(text):
    """`esc` undone, for reading a title back out of the markup it was written into.

    **The raw title is this tool's currency** (`PR-59`). It is what an author types after
    `--source`, so it is the form every comparison uses; the escaped form exists only inside
    markup, and is produced at the boundary and undone at it. Before that ruling the tool escaped
    the title in three places and not in two, and a source titled with an ampersand was matched
    against markup that must carry the entity - no item was found, and `wire()` blamed the
    specification for a citation that was there.
    """
    return (text.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&"))


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

    Front matter, headings, paragraphs, ordered and unordered lists to any depth, indented and
    fenced code, thematic breaks, tables and quotes - the shapes source documents are actually
    written in, audited against the source corpus by T-107 rather than assumed. Anything
    unrecognised stays as its own paragraph, which is the safe direction: a source renders as
    plainer than it was, never as something it is not.

    **An indented line is not evidence of code, and the corpus is what says so.** T-107 counted an
    upper bound and labelled it one; T-121 split it over the same tree, reading 357 documents where
    T-107 read 355. Of 810 lines matching the indented pattern, 146 sit inside a fence, and of the
    664 left, **229 - 34% - are wrapped continuations of a list item rather than code**. So the
    branch is guarded by how deep the line sits inside the open item, not by the indent alone: a fix
    that rendered every indented line as `<pre>` would have been wrong about a third of the
    population it was written for. Nesting is held on a stack for the same kind of reason - the
    corpus nests four levels deep, and two levels used to render as one.

    Setext headings are still not missing: the corpus uses `===` zero times and `---`-under-text
    once, so `---` is read as a thematic break with no ambiguity worth resolving.
    """
    lines = text.split("\n")
    fm, lines = front_matter(lines)
    text = "\n".join(lines)
    out, para, rows, fence, code, pending = [], [], [], None, [], False
    if fm:
        out.append("<table>%s</table>"
                   % "".join("<tr><th>%s</th><td>%s</td></tr>" % (inline(k), inline(v))
                             for k, v in fm))
    # One frame per open list level: [marker indent, content indent, tag, [item html, ...]]. A
    # stack rather than the single flat list this held until T-121, which rendered two levels as
    # one in 125 of 355 corpus documents. `code` is empty, or [dedent column, line, ...]; both are
    # held as lists rather than rebound, matching how `para` and `rows` already avoid `nonlocal`.
    stack = []

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

    def settle(frame):
        """Convert the item's open text run, if one is open, and close it.

        **A wrapped line is part of the run, not a run of its own** (T-269, adopter report `007`).
        A list item used to convert each of its lines the moment it read one, so `**four CRITICAL
        and` / `eight HIGH**` met the inline pass as two halves and neither matched - the reader saw
        the asterisks. `flush_para` never had the fault because it joins first and converts once;
        this is that same order, applied where an item accumulates instead of a paragraph.
        """
        if frame[4]:
            frame[3][-1] = frame[4][0] + inline(" ".join(frame[4][1:]))
            del frame[4][:]

    def open_run(frame, raw):
        """Start (or extend) the item's text run with one raw line."""
        if frame[4]:
            frame[4].append(raw)
        else:
            frame[4].extend([frame[3][-1], raw])

    def emit(html):
        """Into the innermost open list item, or into the document when no list is open."""
        if stack:
            settle(stack[-1])
            stack[-1][3][-1] += html
        else:
            out.append(html)

    def close_lists(depth=0):
        """Close open levels until `depth` remain, nesting each into the item that contains it."""
        while len(stack) > depth:
            settle(stack[-1])
            frame = stack.pop()
            tag, items = frame[2], frame[3]
            emit("<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % i for i in items), tag))

    def flush_code():
        if code:
            body = code[1:]
            # Blank lines inside an indented block are part of it; the ones at the end belong to
            # whatever comes next, and a block that is only blank lines was never a block.
            while body and not body[-1].strip():
                body.pop()
            if body:
                emit("<pre>%s</pre>" % esc("\n".join(body)))
            del code[:]

    for raw in text.split("\n"):
        line = raw.rstrip()
        lead = line[:len(line) - len(line.lstrip())]
        indent = len(lead.expandtabs(4))
        if fence is not None:
            if line.strip().startswith("```"):
                out.append("<pre>%s</pre>" % esc("\n".join(fence)))
                fence = None
            else:
                fence.append(line)
            continue
        if code:
            if not line.strip():
                code.append("")
                continue
            if indent >= code[0]:
                code.append(line.expandtabs(4)[code[0]:])
                continue
            flush_code()
        if pending:
            # **A blank line does not end a list - the line after it does.** Closing on the blank
            # itself put indented code inside a list item out of reach, because the item it belonged
            # to was already shut by the time the code arrived; it also split every loose list into
            # one `<ul>` per item. Deferring the close is also what makes the docstring's 34% a
            # statement about this renderer rather than about the script that counted it.
            pending = False
            if not (stack and (indent >= stack[-1][1]
                               or re.match(r"\s*(?:[-*+]|\d+[.)])\s+", line))):
                close_lists()
        if line.strip().startswith("```"):
            flush_para(); flush_rows(); close_lists()
            fence = []
            continue
        if not line.strip():
            flush_para(); flush_rows()
            pending = True
            continue
        head = re.match(r"(#{1,6})\s+(.*)", line)
        if head:
            flush_para(); flush_rows(); close_lists()
            level = min(3, len(head.group(1)))
            out.append("<h%d>%s</h%d>" % (level, inline(head.group(2)), level))
            continue
        if line.lstrip().startswith("|") and line.rstrip().endswith("|"):
            flush_para(); close_lists()
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if not all(re.match(r"^:?-{2,}:?$", c) for c in cells):
                rows.append(cells)
            continue
        # A thematic break, before the list branch: `- - -` is not a list item, and `---` under a
        # line of text is a setext heading exactly once in 355 corpus documents (T-107).
        if re.match(r"^(?:-{3,}|\*{3,}|_{3,}|(?:[-*_] ){2,}[-*_])\s*$", line.strip()):
            flush_para(); flush_rows(); close_lists()
            out.append("<hr>")
            continue
        item = re.match(r"(\s*)((?:[-*+]|\d+[.)])\s+)(.*)", line)
        if item:
            flush_para(); flush_rows()
            mark = indent
            content = mark + len(item.group(2).expandtabs(4))
            tag = "ol" if item.group(2)[0].isdigit() else "ul"
            while len(stack) > 1 and mark < stack[-1][0]:
                close_lists(len(stack) - 1)
            if stack and mark > stack[-1][0]:
                stack.append([mark, content, tag, [], []])
            elif stack and stack[-1][2] != tag:
                # A changed marker at the same level starts a new list rather than continuing one.
                close_lists(len(stack) - 1)
                stack.append([mark, content, tag, [], []])
            elif not stack:
                stack.append([mark, content, tag, [], []])
            else:
                stack[-1][0], stack[-1][1] = mark, content
            settle(stack[-1])
            stack[-1][3].append("")
            open_run(stack[-1], item.group(3))
            continue
        if line.lstrip().startswith(">"):
            flush_para(); flush_rows(); close_lists()
            out.append("<blockquote>%s</blockquote>" % inline(line.lstrip().lstrip(">").strip()))
            continue
        # An indented line that is not an item: a code block, or the wrapped rest of the item above
        # it. Depth decides, not the indent - the docstring carries the count that made that the
        # rule. Code needs a clean start, so a line indented under an open paragraph continues it.
        if indent >= 4 or stack:
            base = (stack[-1][1] + 4) if stack else 4
            if indent >= base and not para:
                flush_rows()
                code.extend([base, line.expandtabs(4)[base:]])
                continue
            if stack and indent:
                flush_rows()
                open_run(stack[-1], line.strip())
                continue
        close_lists()
        rows and flush_rows()
        para.append(line.strip())
    flush_code(); flush_para(); flush_rows(); close_lists()
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
    # The markup carries the escaped title, so the pattern must too (`PR-59`). This matched the
    # raw one while `data-qv`, `data-file` and `wired_pattern` all escaped, so a title with an
    # ampersand matched nothing and the author was sent to fix a correct specification.
    return re.compile(r'<span class="sources-item">(%s)%s</span>'
                      % (ITEM_HEAD, re.escape(esc(title))), re.S)


# **One sentence, two callers.** `wire` refuses a source no slide cites; so does `refresh`, and
# T-179 required the wording to be unchanged between them. Written once so that is mechanical
# rather than careful - a copy would have drifted the first time either was edited.
UNCITED = ("no provenance item reads %r in this deck. A quick view is attached to a "
           "source a slide already cites - if the slide does not cite it, that is a "
           "specification question and not this tool's (T-069)")


def wired_pattern(title):
    """Matches the `<template>` an already-wired quick view carries: open tag, body, close tag.

    This is the swap target for `refresh`, and it is deliberately **not** `item_pattern`. The
    template is what `carried()` already locates and what the script finds by `data-qv`, so
    replacing its body reaches the rendering and nothing else - the control beside it, and the
    identifier and kind glyph `ITEM_HEAD` carries through, are never inside the substitution.
    """
    return re.compile(r'(<template class="qv-src" data-qv="%s">)(.*?)(</template>)'
                      % re.escape(esc(title)), re.S)


def rewire(html, title, body):
    """`(html, old_body, copies)` - the deck with this rendering replaced, what it was, and how
    many templates carried it.

    **Every copy, not the first** (T-233). This substituted with `count=1` until a shipped deck was
    found carrying eleven templates for one source: `deck.js` builds `qvSrc[data-qv] = tpl` while
    walking them in document order, so the **last** wins and the repair went into the first - the
    verb reported a successful refresh and the deck went on rendering the stale copy. On a
    conformant deck the two are the same template and this changes nothing; on a drifted one it is
    the difference between a repair and a report of one. `check` now fails a deck carrying more
    than one, so this is the belt to that brace rather than a licence to carry duplicates.

    Pure, and separated from `refresh` for the reason `wire` is separate from `plan`: the two
    refusals below are the whole of this verb's guard, and a branch reachable only through a file
    on disk is a branch the self-test cannot watch fail (**L-04**).
    """
    pat = wired_pattern(title)
    match = pat.search(html)
    if not match:
        # **Which refusal applies is the deck's answer, not the caller's.** A title the deck cites
        # but has not wired is an `add` job and says so; a title no slide cites at all is the
        # T-069 guard, in T-069's words - `refresh` relaxes nothing.
        if item_pattern(title).search(html):
            raise Refused("this deck cites %r but carries no quick view for it. `add` attaches "
                          "one; `refresh` re-renders one that is already there" % title)
        raise Refused(UNCITED % title)
    # A function, not a string: a rendered source carries backslashes, and `sub` would read them
    # as group escapes.
    out, copies = pat.subn(lambda m: m.group(1) + body + m.group(3), html)
    return out, match.group(2), copies


def carried(html):
    """`[(title, bytes)]` - the quick views a deck already carries, one row per source."""
    # Read back as the raw title (`PR-59`), because that is the form `--source` names and every
    # comparison here uses. `data-qv` holds the escaped one; unescaping at this boundary is what
    # stops `check` reporting a carried view as MISSING because its title has an ampersand in it.
    return [(unesc(m.group(1)), len(m.group(2).encode("utf-8")))
            for m in re.finditer(r'<template class="qv-src" data-qv="([^"]*)">(.*?)</template>',
                                 html, re.S)]


LEAKS = (
    ("**", re.compile(r"\*\*[^*]{1,120}\*\*")),
    ("__", re.compile(r"(?<![_\w])__[^_]{1,120}__(?!\w)")),
    ("#", re.compile(r"^\s*#{1,6}\s+\S")),
)


def leaked(body):
    """`[(construct, sample)]` - Markdown the renderer left on screen, in one rendered body.

    **A reader of a quick view sees raw asterisks, and no gate said so** (T-269, adopter report
    `007`). Three occurrences shipped in one deck, in two passages, and `check.py`, `component.py`,
    `theme.py` and `spec.py` all passed on it: the renderer's output is HTML, so nothing that reads
    HTML has a reason to look for Markdown in it.

    This is the general form of that fault rather than a test for the one construct that caused it.
    The renderer will keep meeting shapes it does not handle - it implements enough Markdown to
    read a source document and says so - and the point of a gate here is that the next one costs a
    minute instead of a shipped deck.

    **Scanned over text runs, not over the body** - the tags are split out first. Written against
    the body, the `**` pattern fired on `data-t="a**b**c"`: a leak is what a reader sees, and an
    attribute is not that. The first draft's docstring claimed it could not happen, and the seeded
    fixture said otherwise, which is why the claim is a split rather than a sentence. A heading is
    matched at the start of a run, where a converted one would never be.
    """
    runs = [t for t in re.split(r"<[^>]*>", body) if t.strip()]
    hits = []
    for name, pattern in LEAKS:
        for run in runs:
            m = pattern.search(run)
            if m:
                hits.append((name, " ".join(m.group(0).split())[:60]))
                break
    return hits


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
        raise Refused(UNCITED % title)
    control = ('<span class="sources-item">%%s<button class="sources-open" type="button" '
               'data-qv="%s" data-file="%s">%s</button>%%s</span>'
               # The label was the one raw use left (`PR-59`): a title carrying an angle bracket
               # went into the deck as markup rather than as text.
               % (esc(title), esc(os.path.basename(file)), esc(title)))
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


def refresh(deck, sources, write=False, out=None):
    """Re-render the quick views a deck already carries, from the sources named, in place.

    **The verb exists because `add` cannot answer this question** (T-179). Once wired, a
    `.sources-item` holds a control and a template, so `item_pattern` no longer matches it and
    `add` refuses - correctly, for its own question, which is whether a slide cites the source at
    all. Refreshing is a different question, and until this verb there was no way to put a fixed
    renderer's output into a deck that had already shipped: T-121 fixed `markdown()` and could not
    reach the two decks carrying the defect it fixed.

    Writes nothing without `--write`, and reports bytes per source either way, because a refresh
    silently rewriting a shipped deck is this feature's failure mode rather than a broken deck.
    """
    html = shell_mod.read(deck)
    before = len(html.encode("utf-8"))
    print("deck: %s - %d bytes, %d quick view(s) already carried"
          % (paths.display_path(deck, ROOT), before, len(carried(html))))
    print("\n**What this would replace inside the deck.** Every recipient of the file gets every "
          "line of it.\n")
    refused, moved, same = [], 0, 0
    for title, path in sources:
        try:
            body, kind, removed = render(path)
            html, was, copies = rewire(html, title, body)
        except Refused as exc:
            refused.append((title, str(exc)))
            print("  REFUSED  %-28s %s" % (title, exc))
            continue
        old_bytes = len(was.encode("utf-8"))
        new_bytes = len(body.encode("utf-8"))
        if body == was:
            same += 1
            print("  %-8s %-28s %s -> %d bytes, unchanged"
                  % (kind, title, paths.display_path(path, ROOT), new_bytes))
        else:
            moved += 1
            print("  %-8s %-28s %s -> %d bytes (was %d, %+d)"
                  % (kind, title, paths.display_path(path, ROOT), new_bytes, old_bytes,
                     new_bytes - old_bytes))
        if copies > 1:
            # Repaired, and said out loud: the deck is malformed, and a verb that quietly fixed
            # eleven copies would hide the finding that produced this line (T-233).
            print("           %d templates carried this title - all %d replaced. A deck should "
                  "carry one; `quickview.py check` fails this" % (copies, copies))
        for what in removed:
            print("           neutralised %s" % what)
    after = len(html.encode("utf-8"))
    print("\n  deck %d -> %d bytes (%+d), bound %d; %d changed, %d unchanged"
          % (before, after, after - before, SIZE_BOUND, moved, same))
    if after > SIZE_BOUND:
        print("\nREFUSED test 3 (size): the deck would be %d bytes, past the %d bound. Nothing "
              "written." % (after, SIZE_BOUND))
        return 1
    if refused and write:
        print("\nNothing written: %d source(s) were refused, and a partial write would leave a "
              "deck whose provenance says less than the run reported." % len(refused))
        return 1
    if not write:
        print("\nNothing written. Re-run with `--write` to replace exactly what is listed above.")
        return 1 if refused else 0
    target = out or deck
    shell_mod.write(target, html)
    print("\nwrote %s - %d bytes" % (paths.display_path(target, ROOT), after))
    return 0


def profile(html):
    """`(tag counts, the text with every tag stripped)` - the two axes a drift moves along."""
    tags = {}
    for name in re.findall(r"<(\w+)", html):
        tags[name] = tags.get(name, 0) + 1
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip()
    return tags, text


def differences(was, now):
    """What changed between two renderings, in the terms that name the CAUSE.

    **A byte count cannot tell a reader which repair is owed** (T-181), and the three drifts T-179
    found in one deck were two of one kind and one of the other:

      * a **tag count that moved** is the renderer - `<p> 42 -> 0` and `<ol> 0 -> 7` are exactly
        T-107's thematic break and T-121's list continuation, and the repair is `refresh --write`;
      * a **word that differs** is the source document, edited since the deck captured it, and the
        repair is a decision about whether the deck should carry the new text at all.

    Both can be true at once, so both are reported. Where the tags and the text are identical and
    the strings are not, the difference is in attributes or whitespace and the row says so - a
    comparison that failed must never print nothing.
    """
    out = []
    tw, xw = profile(was)
    tn, xn = profile(now)
    for name in sorted(set(tw) | set(tn)):
        a, b = tw.get(name, 0), tn.get(name, 0)
        if a != b:
            out.append("<%s> %d -> %d" % (name, a, b))
    if xw != xn:
        a, b = xw.split(" "), xn.split(" ")
        n = 0
        while n < min(len(a), len(b)) and a[n] == b[n]:
            n += 1
        out.append("text differs at word %d: %r -> %r"
                   % (n + 1, " ".join(a[n:n + 7])[:70], " ".join(b[n:n + 7])[:70]))
    if not out:
        out.append("same tags and same text - the difference is attributes or whitespace")
    return out


def check(deck, sources):
    """Report whether each quick view still matches a fresh render of its source. Writes nothing.

    Returns a shell exit code: non-zero if any named source drifted, was refused, or is not carried
    by this deck at all.

    **The denominator is in the line** (**L-36**). A deck holds *n* quick views and a run names *m*
    sources; *compared 2 of 5* and *compared 5 of 5* are the same verdict and not the same fact, and
    a partial run reading as clean would be this check's own version of the failure it exists to
    find. Anything carried and not named is printed by name.
    """
    html = shell_mod.read(deck)
    held = [title for title, _cost in carried(html)]
    print("deck: %s - %d quick view(s) carried, %d named here"
          % (paths.display_path(deck, ROOT), len(held), len(sources)))
    # **A title carried twice is named, never absorbed into the denominator** (T-233).
    # `portfolio-review.html` shipped eleven templates for one source and every line here read
    # cleanly: the count above said 12, the comparison below reads whichever copy `search` finds
    # first, and `uncompared` excludes the title because `--source` did name it. So ten dead
    # payloads - 84,750 bytes, 20.8% of that deck - were invisible to the check that reads them.
    dupes = sorted({t for t in held if held.count(t) > 1})
    for tit in dupes:
        n = held.count(tit)
        print("  DUPLICATE %-31s %d templates carry this title. `deck.js` keys on `data-qv`, so "
              "one is read and the other %d are bytes nobody can open"
              % (tit[:31], n, n - 1))
    drifted = refused = missing = same = 0
    named = set()
    for title, path in sources:
        named.add(title)
        if title not in held:
            missing += 1
            print("  MISSING  %-32s this deck carries no quick view for that title" % title[:32])
            continue
        try:
            body, _kind, _removed = render(path)
        except Refused as exc:
            refused += 1
            print("  REFUSED  %-32s %s" % (title[:32], exc))
            continue
        was = wired_pattern(title).search(html).group(2)
        if body == was:
            same += 1
            print("  match    %-32s %s" % (title[:32], paths.display_path(path, ROOT)))
        else:
            drifted += 1
            print("  DRIFTED  %-32s %s" % (title[:32], paths.display_path(path, ROOT)))
            for line in differences(was, body):
                print("             %s" % line)
    uncompared = [tit for tit in held if tit not in named]
    print("")
    print("  compared %d of %d carried: %d match, %d drifted, %d refused, %d not carried"
          % (same + drifted, len(held), same, drifted, refused, missing))
    for tit in uncompared:
        print("  NOT COMPARED  %-32s no --source named it, so nothing here checked it" % tit[:32])
    # **Every carried view, not only the compared ones.** A leak is a property of the rendering the
    # deck holds, so it needs no source file and must not inherit the drift check's denominator -
    # the views `--source` did not name are exactly the ones nothing else here reads.
    leaks = 0
    for m in re.finditer(r'<template class="qv-src" data-qv="([^"]*)">(.*?)</template>',
                         html, re.S):
        for name, sample in leaked(m.group(2)):
            leaks += 1
            print("  MARKDOWN %-32s unconverted %s on screen: %s"
                  % (unesc(m.group(1))[:32], name, sample))
    if leaks:
        print("")
        print("A quick view showing raw Markdown is a renderer gap, not a source defect: fix the "
              "renderer, then `quickview.py refresh <deck> --source ... --write`.")
    if dupes:
        print("")
        print("A duplicated quick view is removed by hand - the copies are byte-identical, so "
              "keeping the first is a deletion. `wire` writes one; a deck with more got them some "
              "other way (T-233).")
    if drifted or refused or missing or leaks or dupes:
        print("")
        print("A drifted quick view is repaired by `quickview.py refresh <deck> --source ... "
              "--write` where the renderer moved, and by a decision where the source document did.")
        return 1
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

    # T-121's two constructs, in one fixture each, and each written so that removing its branch
    # fails here rather than degrading quietly. The pair that has to be tested *together* is code
    # and continuation: they match the same pattern, and the corpus says a third of the matches are
    # continuations, so a fixture holding only code would pass a renderer that got them all wrong.
    nested = markdown("- one\n    - a\n        - deep\n    - b\n- two\n\n1. first\n    1. inner\n")
    for want, construct in (
            ("<ul><li>one<ul><li>a<ul><li>deep</li></ul></li><li>b</li></ul></li><li>two</li></ul>",
             "a three-level unordered list, which the corpus nests four deep"),
            ("<ol><li>first<ol><li>inner</li></ol></li></ol>",
             "an ordered list nested in an ordered list")):
        if want not in nested:
            sys.exit("SELF-TEST FAILED: the Markdown renderer flattened %s - wanted %r, got %r. "
                     "Two levels rendering as one is the T-121 defect, in 125 of 355 corpus "
                     "documents" % (construct, want, nested))

    # T-269's construct, and the gate that would have named it. A list item used to convert each
    # line as it read it, so emphasis opening on one and closing on the next met the inline pass in
    # halves and neither half matched - three occurrences reached a presented deck. The renderer
    # and the gate are tested together on purpose: either alone passes a deck the pair would fail.
    wrapped = markdown("- residual risk is inherent risk: **four CRITICAL and\n"
                       "  eight HIGH** (`D1`).\n\nA paragraph with *emphasis that\nwraps* too.\n")
    if "<b>four CRITICAL and eight HIGH</b>" not in wrapped:
        sys.exit("SELF-TEST FAILED: emphasis spanning a wrapped list item stayed literal - got %r. "
                 "That is the T-269 defect, three occurrences in one shipped deck" % wrapped)
    if "<i>emphasis that wraps</i>" not in wrapped:
        sys.exit("SELF-TEST FAILED: emphasis spanning a wrapped paragraph stayed literal - got %r"
                 % wrapped)
    if leaked(wrapped):
        sys.exit("SELF-TEST FAILED: the leak gate fired on correctly rendered output - %r"
                 % (leaked(wrapped),))
    # Both directions (**L-125**). A gate that never fires and a gate that always fires read the
    # same from a green run, so the seeded body is checked beside the clean one.
    for body, want, construct in (
            ("<li>risk is: **four CRITICAL and eight HIGH** (<code>D1</code>).</li>", "**",
             "the exact body the renderer produced before T-269"),
            ("<p>__also strong__ here</p>", "__", "underscore emphasis"),
            ("<p>## A heading that never converted</p>", "#", "an unconverted ATX heading")):
        if want not in [name for name, _sample in leaked(body)]:
            sys.exit("SELF-TEST FAILED: the leak gate missed %s in %r" % (construct, body))
    for body, construct in (
            ('<a class="x" data-t="a**b**c">t</a>', "an attribute, which no reader sees"),
            ("<p>a variable named my__name is not emphasis</p>", "a snake_case identifier"),
            ("<p>see issue #42 and #43 here</p>", "a # that is not a heading"),
            ("<p>a <b>b</b> and <code>x**y</code></p>", "a lone asterisk pair inside code")):
        if leaked(body):
            sys.exit("SELF-TEST FAILED: the leak gate fired on %s - %r would be a false alarm on "
                     "every deck carrying one" % (construct, body))

    # `PR-59` - the title's two forms, and the one boundary between them. The fixture carries an
    # ampersand because that is the character a correct deck must write as an entity, so a tool
    # that matches the raw title against correct markup finds nothing and blames the specification.
    amp = "Fleet & cost model"
    cited = ('<span class="sources-item"><span class="sources-id">D1</span>'
             '<svg class="sources-icon"></svg>%s</span>' % esc(amp))
    if not item_pattern(amp).search(cited):
        sys.exit("SELF-TEST FAILED: a source titled %r does not match the markup a correct deck "
                 "carries for it. That is `PR-59`: the author is sent to fix a citation that is "
                 "already right" % amp)
    wired = wire(cited, amp, "<p>body</p>", file="d1.md")
    if [t for t, _c in carried(wired)] != [amp]:
        sys.exit("SELF-TEST FAILED: %r did not read back as itself - got %r. The raw title is this "
                 "tool's currency and `check` compares against it"
                 % (amp, [t for t, _c in carried(wired)]))
    if ">%s<" % amp in wired:
        sys.exit("SELF-TEST FAILED: the control's label went into the deck raw, so a title with an "
                 "angle bracket would ship as markup")
    if unesc(esc(amp)) != amp:
        sys.exit("SELF-TEST FAILED: esc/unesc does not round-trip on %r" % amp)

    blocks = markdown("intro\n\n    code one\n    code two\n\n- an item that wraps\n"
                      "    onto the next line\n- an item with code\n\n      indented under it\n")
    if "<pre>code one\ncode two</pre>" not in blocks:
        sys.exit("SELF-TEST FAILED: an indented code block rendered as prose, which is the other "
                 "half of T-121 - 435 lines in 81 corpus documents. Got %r" % blocks)
    if "<li>an item that wraps onto the next line</li>" not in blocks:
        sys.exit("SELF-TEST FAILED: a wrapped list continuation was not joined to its item. If it "
                 "became a <pre> the indented-code branch is unguarded, and the corpus says that "
                 "is wrong 229 times in 27 documents - 34%% of everything the pattern matches. "
                 "Got %r" % blocks)
    if "<li>an item with code<pre>indented under it</pre></li>" not in blocks:
        sys.exit("SELF-TEST FAILED: code indented inside a list item did not stay inside it. A "
                 "blank line must not end the item, or the block it introduces has nowhere to go. "
                 "Got %r" % blocks)

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

    # **T-233: a deck carrying two templates for one title.** The fault is silent - the old
    # `count=1` repaired the first while `deck.js` reads the last, so `refresh` reported a
    # successful write over a deck that still rendered the stale copy. Built by duplicating a
    # wired template rather than by hand, so the fixture cannot drift away from what `wire` emits.
    _one = ('<span class="sources-box"><span class="sources-item">Cost model</span></span>')
    _wired1 = wire(_one, "Cost model", "<p>old</p>", "cost-model.md")
    _tpl = '<template class="qv-src" data-qv="Cost model"><p>old</p></template>'
    if _wired1.count(_tpl) != 1:
        sys.exit("SELF-TEST FAILED: the duplicate fixture could not be built - `wire` no longer "
                 "emits %r" % _tpl)
    _dupe = _wired1.replace(_tpl, _tpl + _tpl, 1)
    _fixed, _was, _copies = rewire(_dupe, "Cost model", "<p>new</p>")
    if _copies != 2:
        sys.exit("SELF-TEST FAILED: rewire saw %d copies in a deck carrying 2" % _copies)
    if "<p>old</p>" in _fixed:
        sys.exit("SELF-TEST FAILED: refreshing a deck with two templates left one stale. That is "
                 "the T-233 fault exactly, and it reports success while doing it - %r" % _fixed)

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

    # T-179. Refreshing, and its two refusals. `wired` above is a deck that already carries a quick
    # view for "Cost model" - which is exactly the state `add` cannot act on, so it is the right
    # fixture for the verb that can.
    again, was, copies = rewire(wired, "Cost model", "<p>y</p>")
    if copies != 1:
        sys.exit("SELF-TEST FAILED: refreshing a deck with one template reported %d copies"
                 % copies)
    if was != "<p>x</p>":
        sys.exit("SELF-TEST FAILED: refreshing did not report what the quick view held before - "
                 "%r. The byte delta is the only thing standing between this verb and a shipped "
                 "deck rewritten silently" % was)
    if carried(again) != [("Cost model", len("<p>y</p>"))]:
        sys.exit("SELF-TEST FAILED: refreshing did not replace the rendering - %r" % carried(again))
    if "<p>x</p>" in again:
        sys.exit("SELF-TEST FAILED: refreshing left the old rendering in the deck beside the new "
                 "one - %r" % again)
    # The control, the identifier and the kind glyph are outside the substitution by construction.
    # Asserted anyway, because "by construction" is what T-109 was before it was a fixture.
    for keep, what in (('class="sources-open"', "the control"),
                       ('class="sources-id">D1<', "the source's identifier"),
                       ('class="sources-icon"', "the kind glyph"),
                       ('data-file="cost-model.md"', "the file name")):
        if keep not in again:
            sys.exit("SELF-TEST FAILED: refreshing dropped %s. Only the rendering inside the "
                     "<template> is this verb's to touch - %r" % (what, again))
    # **A refresh that agrees with what is embedded must be a no-op, byte for byte.** This is the
    # control case T-179 named: without it, "refreshed" and "rewritten" are indistinguishable.
    noop, _, _copies = rewire(again, "Cost model", "<p>y</p>")
    if noop != again:
        sys.exit("SELF-TEST FAILED: refreshing with an identical rendering changed the deck. A "
                 "no-op that writes bytes cannot be told from a defect")
    try:
        rewire(again, "Nobody cites this", "<p>x</p>")
        sys.exit("SELF-TEST FAILED: a quick view was refreshed for a source no slide cites")
    except Refused as exc:
        if "T-069" not in str(exc):
            sys.exit("SELF-TEST FAILED: an uncited source was refused by `refresh` in different "
                     "words from `add`. The guard is one guard: %s" % exc)
    # Cited, never wired: a different answer, and the one that must not read as the guard above.
    try:
        rewire(deck, "Cost model", "<p>x</p>")
        sys.exit("SELF-TEST FAILED: a source with no quick view at all was 'refreshed'")
    except Refused as exc:
        if "T-069" in str(exc) or "add" not in str(exc):
            sys.exit("SELF-TEST FAILED: a cited-but-unwired source was refused as though no slide "
                     "cited it. The reader is one `add` away and the message has to say so: %s"
                     % exc)

    # ---- `check`'s own fixtures (T-181) -------------------------------------------------------
    # **The row has to name the cause, not the fact.** A byte count says a rendering moved; it does
    # not say whether the repair is `refresh --write` or a decision about the source document, and
    # those were 2 and 1 of the three drifts T-179 found inside one deck.
    renderer = differences("<p>a</p><p>---</p>", "<p>a</p><hr>")
    if not any(d.startswith("<hr> 0 -> 1") for d in renderer):
        sys.exit("SELF-TEST FAILED: a renderer-shaped drift did not report the tag whose count "
                 "moved. `<p>---</p>` to `<hr>` is T-107 exactly, and the count is the evidence: %s"
                 % renderer)
    edited = differences("<p>hello there world</p>", "<p>hello brave world</p>")
    if len(edited) != 1 or "word 2" not in edited[0]:
        sys.exit("SELF-TEST FAILED: a source document edited under a stable renderer must report "
                 "the differing word and no tag movement at all: %s" % edited)
    if differences("<p>x</p>", "<p>x</p>") == []:
        sys.exit("SELF-TEST FAILED: `differences` returned nothing. It is only ever called on two "
                 "strings that are not equal, so an empty list is a comparison reporting silence")
    quiet = differences('<p a="1">x</p>', '<p a="2">x</p>')
    if len(quiet) != 1 or "attributes" not in quiet[0]:
        sys.exit("SELF-TEST FAILED: a difference in attributes alone reported %s. Same tags and "
                 "same text is a real drift and the row must say what is left" % quiet)
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
    if cmd not in ("plan", "add", "refresh", "check"):
        sys.exit("usage: quickview.py plan|add|refresh|check|list <deck> [--source <title>=<path>]")
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
    if cmd == "check":
        return check(deck, sources)
    if cmd == "refresh":
        return refresh(deck, sources, write=("--write" in rest), out=out)
    return plan(deck, sources, write=(cmd == "add"), out=out)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
