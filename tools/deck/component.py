#!/usr/bin/env python3
"""The markup contract: what a deck is made of, and whether this deck is made of it.

`docs/COMPONENT-CONTRACT.md` is the contract, and **this file parses it rather than restating it**
(**L-08**, **L-13**): adding a part to the document has to change what `check` demands without
anyone editing this file. The same reason `theme.py` reads `THEME-CONTRACT.md` and `ruleset.py`
reads `DESIGN-SYSTEM.md`.

Four claims, and the fourth is the one that keeps the document true:

- **structure** - every part is the element the contract names, sits inside the part it names, and
  carries the attributes it names;
- **place** - no element carries a contracted class somewhere the contract does not put it;
- **motion** - every rule the contract lists reads the motion tokens it lists, which is the
  positive half `theme.py`'s literal scan cannot state (it can say *no literal was written*, never
  *the token is read*);
- **completeness** - every class the shared style block styles has a row. A component nobody
  contracted is a component a generator cannot emit, and it is added by writing CSS, which is
  exactly when nobody remembers to write the row.

    python tools/deck/component.py parts                  # the contract, as data
    python tools/deck/component.py check <deck>

Runs its own self-test first and refuses to report if it fails (**L-04**). Pure standard
library (**L-07**).
"""

import io
import os
import re
import sys
from html.parser import HTMLParser

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONTRACT = os.path.join(ROOT, "docs", "COMPONENT-CONTRACT.md")

SOURCES = ("author", "script", "print", "vocabulary")

# Elements that never carry children. SVG's are here too: the deck's diagrams are inline SVG, and
# `<path/>` closes itself while `<path>` in a hand-written figure does not - treating them as
# containers reparents everything after the first one.
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param",
        "source", "track", "wbr",
        "path", "circle", "rect", "line", "polyline", "polygon", "ellipse", "stop", "use"}


# ---------------------------------------------------------------------------- the contract


class Part(object):
    __slots__ = ("name", "element", "within", "modifier", "lo", "hi", "attrs", "source")

    def __init__(self, name, element, within, modifier, lo, hi, attrs, source):
        self.name, self.element = name, element
        self.within, self.modifier = within, modifier
        self.lo, self.hi, self.attrs, self.source = lo, hi, attrs, source

    def __repr__(self):
        return "<%s %s in %s>" % (self.name, self.element or "-", self.within or "-")


COUNTS = {"1": (1, 1), "0-1": (0, 1), "1+": (1, None), "0+": (0, None)}


def _spans(cell):
    return [s.strip() for s in re.findall(r"`([^`]+)`", cell)]


def parse_part_row(line):
    """One `| .part | element | sits in | count | attributes | source |` row, or None.

    Read from the left, unlike `theme.py`'s token row: every cell here is a code span or a short
    keyword, so none of them can contain the pipe that forces that file to read from both ends.
    """
    if not line.startswith("| `."):
        return None
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) != 6:
        return None
    name = cells[0].strip("` ")
    if not name.startswith("."):
        return None
    source, count = cells[5].strip(), cells[3].strip("` ")
    if source not in SOURCES or count not in COUNTS:
        return None                       # a table that is not a part table
    element = cells[1].strip("` ") if cells[1].strip() not in ("—", "-") else None
    within, modifier = None, False
    w = cells[2].strip("` ")
    if w.startswith("on "):
        within, modifier = w[3:].strip().lstrip("."), True
    elif w not in ("—", "-"):
        within = w.lstrip(".")
    lo, hi = COUNTS[count]
    return Part(name.lstrip("."), element, within, modifier, lo, hi,
                _spans(cells[4]), source)


def parse_motion_row(line):
    """One `| rule | motion | tokens |` row of §3.8, as `(selector, [token])`."""
    if not line.startswith("| `"):
        return None
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) != 3:
        return None
    sel = cells[0].strip("` ")
    toks = [t for t in _spans(cells[2]) if t.startswith("--")]
    if not toks:
        return None
    return (sel, toks)


def load(path=CONTRACT):
    """`(parts, motions)` from the contract document."""
    parts, motions = {}, []
    for line in io.open(path, encoding="utf-8"):
        p = parse_part_row(line)
        if p is not None:
            if p.name in parts:
                sys.exit("CONTRACT: .%s appears twice" % p.name)
            parts[p.name] = p
            continue
        m = parse_motion_row(line)
        if m is not None:
            motions.append(m)
    if len(parts) < 40:
        sys.exit("CONTRACT: parsed only %d parts from %s - the format moved under the parser"
                 % (len(parts), path))
    if not motions:
        sys.exit("CONTRACT: no motion row parsed from %s. An empty list is not the same as none "
                 "declared, and the difference is every duration in the deck" % path)
    return parts, motions


# ---------------------------------------------------------------------------- the markup


class Node(object):
    __slots__ = ("tag", "attrs", "children", "parent")

    def __init__(self, tag, attrs, parent):
        self.tag, self.attrs, self.parent, self.children = tag, attrs, parent, []

    @property
    def classes(self):
        return (self.attrs.get("class") or "").split()


class Tree(HTMLParser):
    """A tolerant element tree. `html.parser` is standard library, which is the whole reason.

    An unmatched close tag walks up to the nearest open element of that name rather than popping
    blindly, so one stray `</div>` in a hand-written figure cannot reparent the rest of the deck.
    """

    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.root = Node("#root", {}, None)
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        n = Node(tag, {k: (v if v is not None else "") for k, v in attrs}, self.cur)
        self.cur.children.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(
            Node(tag, {k: (v if v is not None else "") for k, v in attrs}, self.cur))

    def handle_endtag(self, tag):
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is not self.root:
            self.cur = n.parent


def parse(html):
    body = html[html.index("<body>"):] if "<body>" in html else html
    t = Tree()
    t.feed(body)
    return t.root


def walk(n):
    yield n
    for c in n.children:
        for x in walk(c):
            yield x


def ancestor(node, cls):
    p = node.parent
    while p is not None:
        if cls in p.classes:
            return p
        p = p.parent
    return None


# ---------------------------------------------------------------------------- the shared block


def shared_css(html):
    """The unnamed `<style>` block, comments and `@media print` removed.

    The theme region and `#slides` are both excluded by having an id: one owns the values a second
    theme changes, the other owns one deck's composition, and neither owns a component.

    **The print block is cut out, not truncated at.** This split on `@media print {` and kept the
    first half, so any rule written after the print block was invisible here - and the completeness
    verdict below reported *0 uncontracted* while two new classes were styled. A check that stops
    reading at a marker keeps reporting the coverage it had on the day that marker went last, and
    says nothing about anything added past it (found by T-019, **L-36**).
    """
    for attrs, body in re.findall(r"<style([^>]*)>(.*?)</style>", html, re.S):
        if "id=" in attrs:
            continue
        return re.sub(r"/\*.*?\*/", "", drop_at_rule(body, "print"), flags=re.S)
    return ""


def drop_at_rule(css, media):
    """`css` with `@media <media>{...}` removed, matched to its own closing brace."""
    found = re.search(r"@media\s+%s\s*\{" % re.escape(media), css)
    if not found:
        return css
    depth, i = 1, found.end()
    while i < len(css) and depth:
        depth += 1 if css[i] == "{" else -1 if css[i] == "}" else 0
        i += 1
    return css[:found.start()] + css[i:]


def rules(css):
    """`[(selector, declarations)]`, one per comma-separated selector, at-rules dropped."""
    out = []
    for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        s = " ".join(sel.split())
        if "@" in s or "%" in s or s in ("from", "to"):
            continue
        for one in s.split(","):
            out.append((one.strip(), body))
    return out


def styled_classes(css):
    """`{class: [selector]}` for every class the shared block styles."""
    out = {}
    for sel, _body in rules(css):
        for c in re.findall(r"\.([A-Za-z][\w-]*)", sel):
            out.setdefault(c, []).append(sel)
    return out


def is_scoped(part, styled):
    """Is the class meaningless outside the part it sits in?

    **Derived from the CSS, never declared**, because the answer is already written there. `.pos`
    is styled only as `.fig .pos`, so a `<b class="pos">` in a ledger is a different class that
    `#slides` owns - flagging it as a misplaced figure mark would be the check inventing a defect.
    `.disc-panel` is styled bare, so it means the same thing wherever it appears and one outside a
    `.disc` is exactly the wiring mistake this check is for.
    """
    if not part.within or part.modifier:
        return False
    sels = styled.get(part.name)
    if not sels:
        return False                      # an unstyled hook the script selects; place still binds
    return all("." + part.within in s.split("." + part.name)[0] for s in sels)


# ---------------------------------------------------------------------------- the checks


SCRIPT_ARRAY = re.compile(r"var\s+([A-Z][A-Z_]*)\s*=\s*\[(.*?)\]\s*;", re.S)


def script_arrays(html):
    """`{NAME: length}` for every `var NAME = [...]` the deck's script declares.

    **The deck is the only place these lengths are written** (T-102). `data-stage` is an index into
    `STAGES`, and `STAGES` is a per-deck line the shell fills in — so the contract can say *an index
    into the deck's own array* but can never list the values, and a check that wants to decide the
    attribute has to read the file it is checking.
    """
    out = {}
    for name, body in SCRIPT_ARRAY.findall(html):
        quoted = re.findall(r"'[^']*'|\"[^\"]*\"", body)
        out[name] = len(quoted) if quoted else len([s for s in body.split(",") if s.strip()])
    return out


def structure(root, parts, styled, arrays=None):
    """Every way the markup departs from the contract, as `[message]`."""
    bad = []
    arrays = arrays or {}
    nodes = list(walk(root))
    for name in sorted(parts):
        p = parts[name]
        els = [n for n in nodes if name in n.classes]
        if p.source in ("script", "print"):
            continue
        if p.source == "vocabulary":
            inside = [n for n in els if not p.within or ancestor(n, p.within)]
            if inside:
                bad.append(".%s is `vocabulary` and this deck has %d of it - the row is misfiled, "
                           "not the deck" % (name, len(inside)))
            continue
        if p.modifier:
            stray = [n for n in els if p.within not in n.classes]
            if stray:
                bad.append(".%s is a modifier on .%s and %d element(s) carry it alone"
                           % (name, p.within, len(stray)))
            continue

        scoped = is_scoped(p, styled)
        if p.within:
            placed = [n for n in els if ancestor(n, p.within)]
            orphans = [n for n in els if n not in placed]
            if orphans and not scoped:
                bad.append(".%s: %d element(s) sit outside .%s (%s)"
                           % (name, len(orphans), p.within,
                              " ".join(sorted({n.tag for n in orphans}))))
            els = placed
            hosts = [n for n in nodes if p.within in n.classes]
        else:
            hosts = [root]

        for h in hosts:
            n = len([e for e in els if ancestor(e, p.within) is h]) if p.within else len(els)
            if n < p.lo or (p.hi is not None and n > p.hi):
                bad.append(".%s: %d per %s, outside %s"
                           % (name, n, ("." + p.within) if p.within else "deck",
                              "%d-%s" % (p.lo, p.hi if p.hi is not None else "")))
                break                     # one message per part; the first host says it

        if p.element:
            wrong = sorted({e.tag for e in els if e.tag != p.element})
            if wrong:
                bad.append(".%s must be <%s>; found %s" % (name, p.element, " ".join(wrong)))
        for spec in p.attrs:
            attr, _, needs = spec.partition(":")
            missing = [e for e in els if attr.lower() not in e.attrs]
            if missing:
                bad.append(".%s: %d of %d carry no %s" % (name, len(missing), len(els), attr))
            elif "/" in needs:
                # A closed set. `data-disc` is the only one, and the check is closure alone: that
                # the value is one of DS-230's four kinds, never that it is the RIGHT one - which
                # is why DS-230 is `judge` and this row cites DS-229 with the rest of the markup.
                allowed = needs.split("/")
                wrong = sorted({(e.attrs.get(attr.lower()) or "").strip() or "(empty)"
                                for e in els if (e.attrs.get(attr.lower()) or "").strip()
                                not in allowed})
                if wrong:
                    bad.append(".%s: %s is a closed set (%s) and %d element(s) leave it: %s"
                               % (name, attr, " ".join(allowed),
                                  len([e for e in els
                                       if (e.attrs.get(attr.lower()) or "").strip()
                                       not in allowed]), " ".join(wrong)))
            elif needs.startswith("#"):
                # An index into one of the deck's own script arrays, which is a range no contract
                # can enumerate: `STAGES` has as many entries as the deck has stages. A deck that
                # writes the stage's *name* here opens, renders and passes four gates, and loses
                # its ruler and its arrow keys, because `deck.js` subscripts the array with it
                # (T-102). The failure names the attribute, not the navigation it breaks.
                size = arrays.get(needs[1:])
                held = [(e, (e.attrs.get(attr.lower()) or "").strip()) for e in els]
                if size is None:
                    if held:
                        bad.append(".%s: %s is an index into %s and this deck declares no such "
                                   "array" % (name, attr, needs[1:]))
                else:
                    wrong = sorted({v or "(empty)" for _e, v in held
                                    if not (v.isdigit() and int(v) < size)})
                    if wrong:
                        bad.append(".%s: %s is a zero-based index into %s (0-%d) and %d "
                                   "element(s) leave it: %s"
                                   % (name, attr, needs[1:], size - 1,
                                      len([v for _e, v in held
                                           if not (v.isdigit() and int(v) < size)]),
                                      " ".join(wrong)))
            elif needs:
                empty = [e for e in els if needs not in (e.attrs.get(attr.lower()) or "")]
                if empty:
                    bad.append(".%s: %d of %d have a %s that does not set %s"
                               % (name, len(empty), len(els), attr, needs))
    return bad


# The scopes under which the shared block is undoing one deck's composition rather than declaring a
# component of its own. `.doc .ledger` reflows a ledger for the reading view; `:root[data-preflight]
# .figwrap` does the same thing for the degraded state (DS-009). Both are renderings reaching into
# `#slides`' classes, and neither makes the class a component.
ADAPTATIONS = (".doc ", ":root[data-preflight] ")


def missing_rows(parts, styled):
    """Classes the shared block styles and the contract does not name.

    A class every one of whose rules sits under one of the ADAPTATIONS above is `#slides`' class
    reached from another rendering, and not a component. A class with even one unscoped rule is.
    """
    out = []
    for c, sels in sorted(styled.items()):
        if c in parts or all(s.startswith(ADAPTATIONS) for s in sels):
            continue
        out.append(c)
    return out


def motion_gaps(css, motions):
    """Motion rows whose rule does not read the tokens the contract says it reads."""
    bad = []
    text = css
    by_sel = {}
    for sel, body in rules(css):
        by_sel.setdefault(sel, []).append(body)
    for sel, toks in motions:
        if sel.startswith("@keyframes"):
            m = re.search(r"@keyframes\s+" + re.escape(sel.split()[-1]) + r"\s*\{(.*?)\}\s*\}",
                          text, re.S)
            bodies = [m.group(1)] if m else []
        else:
            bodies = by_sel.get(sel, [])
        if not bodies:
            bad.append("%s is in the contract and not in the deck's CSS" % sel)
            continue
        joined = "\n".join(bodies)
        absent = [t for t in toks if ("var(%s" % t) not in joined.replace(" ", "")]
        if absent:
            bad.append("%s does not read %s" % (sel, " ".join(absent)))
    return bad


# ---------------------------------------------------------------------------- verdicts


def verdicts(html):
    """`(rule, what, ok)` rows, in the shape every other stage returns.

    **Five rows, always** - not one per problem found. A row that appears only when something is
    wrong is a row the coverage account cannot count, and a rule nothing says anything about is
    SILENT rather than passing (**L-36**). All five cite DS-229, which is the mechanical instance
    of DS-136 and points at this contract by name.
    """
    parts, motions = load()
    root = parse(html)
    css = shared_css(html)
    styled = styled_classes(css)

    authored = [p for p in parts.values() if p.source == "author"]
    vocab = [p for p in parts.values() if p.source == "vocabulary"]
    bad = structure(root, parts, styled, script_arrays(html))
    missing = missing_rows(parts, styled)
    gaps = motion_gaps(css, motions)

    place = [m for m in bad if "sit outside" in m or "carry it alone" in m]
    vocabbad = [m for m in bad if "is `vocabulary`" in m]
    rest = [m for m in bad if m not in place and m not in vocabbad]

    return [
        ("DS-229", "every authored part is the element, place and count the contract names: "
         "%d part(s) required, %d problem(s)%s"
         % (len(authored), len(rest), "" if not rest else " - " + "; ".join(rest[:3])),
         not rest),
        ("DS-229", "no contracted class sits where the contract does not put it: %d problem(s)%s"
         % (len(place), "" if not place else " - " + "; ".join(place[:3])),
         not place),
        ("DS-229", "every rule the contract lists reads the motion tokens it lists: "
         "%d rule(s), %d gap(s)%s"
         % (len(motions), len(gaps), "" if not gaps else " - " + "; ".join(gaps[:3])),
         not gaps),
        ("DS-229", "every class the shared block styles has a row: %d styled, %d uncontracted%s"
         % (len(styled), len(missing), "" if not missing else " - ." + " .".join(missing[:6])),
         not missing),
        ("DS-229", "every `vocabulary` row is still unused: %d declared, %d now in the deck%s"
         % (len(vocab), len(vocabbad), "" if not vocabbad else " - " + "; ".join(vocabbad[:3])),
         not vocabbad),
    ]


# ---------------------------------------------------------------------------- self-test


def self_test():
    """The check must be able to tell a conforming deck from a broken one (**L-04**).

    Every assertion here is made by **breaking** something, because a checker that has never been
    seen to fail is a claim about the instrument (**L-36**) - the same discipline
    `static_variants.py` applies to the gate as a whole, applied to the parser this file is.
    """
    parts, motions = load()
    for name, p in parts.items():
        if p.source not in SOURCES:
            sys.exit("SELF-TEST FAILED: .%s has source %r" % (name, p.source))
        if p.modifier and not p.within:
            sys.exit("SELF-TEST FAILED: .%s is a modifier on nothing" % name)
        if p.within and p.within not in parts and p.within not in ("body",):
            sys.exit("SELF-TEST FAILED: .%s sits in .%s, which the contract does not name"
                     % (name, p.within))
    for sel, toks in motions:
        for t in toks:
            if not t.startswith("--"):
                sys.exit("SELF-TEST FAILED: %s lists %r, which is not a token" % (sel, t))

    doc = ('<body><div class="viewport" id="v"><main class="stage" id="s" aria-label="x">'
           '<section class="slide" data-name="a" data-stage="0" aria-label="Slide 1">'
           '<div class="disc" data-disc="scope"><button class="disc-btn" aria-expanded="false" '
           'aria-controls="p"><span class="disc-mark" aria-hidden="true"></span>'
           '<span class="disc-label">L</span></button>'
           '<div class="disc-panel" id="p" hidden><div class="row"><span class="k">K</span>'
           '</div></div></div></section></main></div></body>')
    root = parse(doc)
    if len([n for n in walk(root) if "disc-btn" in n.classes]) != 1:
        sys.exit("SELF-TEST FAILED: the tree lost the disclosure control")
    tiny = {k: parts[k] for k in ("disc", "disc-btn", "disc-mark", "disc-label", "disc-panel",
                                 "row", "k") if k in parts}
    if structure(root, tiny, {}):
        sys.exit("SELF-TEST FAILED: a conforming disclosure set was reported broken: %s"
                 % structure(root, tiny, {}))
    broken = parse(doc.replace(' aria-controls="p"', ""))
    if not any("aria-controls" in m for m in structure(broken, tiny, {})):
        sys.exit("SELF-TEST FAILED: a control with no aria-controls was not reported")
    moved = parse(doc.replace('<div class="disc" data-disc="scope">', "<div>"))
    if not any("sit outside" in m for m in structure(moved, tiny, {})):
        sys.exit("SELF-TEST FAILED: a panel outside its .disc was not reported")
    # The closed set has to be closed, or `data-disc` is back to carrying nothing (DS-230).
    outside = parse(doc.replace('data-disc="scope"', 'data-disc="appendix"'))
    if not any("closed set" in m for m in structure(outside, tiny, {})):
        sys.exit("SELF-TEST FAILED: a data-disc outside DS-230's four kinds was not reported")
    if not any("closed set" in m for m in structure(parse(doc.replace('="scope"', '')), tiny, {})):
        sys.exit("SELF-TEST FAILED: a valueless data-disc was not reported")

    # `data-stage` is an index into the deck's own `STAGES`, and the stage's *name* in that slot
    # passes every other check in this file while costing the deck its ruler and its arrow keys
    # (T-102). Three cases, because the two wrong ones fail differently: a name is not a number,
    # and a number can still be past the end.
    if "slide" in parts:
        one, stages = {"slide": parts["slide"]}, {"STAGES": 8}
        if structure(parse(doc), one, {}, stages):
            sys.exit("SELF-TEST FAILED: an in-range data-stage was reported: %s"
                     % structure(parse(doc), one, {}, stages))
        for bad_value in ('data-stage="Problem"', 'data-stage="8"', 'data-stage=""'):
            broke = parse(doc.replace('data-stage="0"', bad_value))
            if not any("index into STAGES" in m for m in structure(broke, one, {}, stages)):
                sys.exit("SELF-TEST FAILED: %s was not reported" % bad_value)
        # ...and with no array to index, the deck is missing the declaration rather than the value.
        if not any("declares no such array" in m for m in structure(parse(doc), one, {}, {})):
            sys.exit("SELF-TEST FAILED: a data-stage with no STAGES declared was not reported")
    if script_arrays("  var STAGES = ['a','b','c'];\n  var idx = 0;").get("STAGES") != 3:
        sys.exit("SELF-TEST FAILED: the deck's STAGES array was not counted")

    # The completeness check has to notice a component nobody contracted, or it is decoration.
    if not missing_rows({}, {"invented": [".invented"]}):
        sys.exit("SELF-TEST FAILED: an uncontracted class was not reported")
    if missing_rows({}, {"ledger": [".doc .ledger"]}):
        sys.exit("SELF-TEST FAILED: a reading-view adaptation was reported as a component")
    if missing_rows({}, {"figwrap": [":root[data-preflight] .figwrap"]}):
        sys.exit("SELF-TEST FAILED: a degraded-state adaptation was reported as a component")
    # And the half that keeps the exemption narrow: one unscoped rule and it IS a component.
    if not missing_rows({}, {"preflight": [".preflight", ":root[data-preflight] .preflight"]}):
        sys.exit("SELF-TEST FAILED: a class with an unscoped rule was exempted as an adaptation")
    if not motion_gaps(".rise{opacity:0}", [(".rise", ["--rise-dist"])]):
        sys.exit("SELF-TEST FAILED: a rule that reads no motion token was not reported")

    # The print block is cut out rather than truncated at, so a rule AFTER it is still read. Nested
    # braces on purpose - `@page{}` and a media query both nest, and a naive first-`}` scan would
    # stop inside one and take the rest of the print rules for components.
    after = ("<style>.a{color:red}@media print{@page{margin:0}.b{color:blue}}"
             ".c{color:green}</style>")
    seen = styled_classes(shared_css(after))
    if "c" not in seen:
        sys.exit("SELF-TEST FAILED: a rule after @media print was not read - the block is being "
                 "truncated at rather than cut out")
    if "b" in seen:
        sys.exit("SELF-TEST FAILED: a print-only rule was counted as a component")
    return True


# ---------------------------------------------------------------------------- command


def main(argv):
    self_test()
    what = argv[0] if argv else "check"
    if what == "parts":
        parts, motions = load()
        print("%-22s %-9s %-16s %-6s %-11s %s"
              % ("PART", "ELEMENT", "SITS IN", "COUNT", "SOURCE", "ATTRIBUTES"))
        for name in sorted(parts):
            p = parts[name]
            band = "%d+" % p.lo if p.hi is None else \
                   ("%d" % p.lo if p.lo == p.hi else "%d-%d" % (p.lo, p.hi))
            print("%-22s %-9s %-16s %-6s %-11s %s"
                  % ("." + name, p.element or "-",
                     ("on ." if p.modifier else ".") + p.within if p.within else "-",
                     band, p.source, " ".join(p.attrs)))
        print("\n%d part(s), %d motion rule(s)" % (len(parts), len(motions)))
        return 0

    deck = os.path.abspath(argv[1]) if len(argv) > 1 else os.path.join(
        ROOT, "examples", "reference-deck.html")
    html = io.open(deck, encoding="utf-8").read()
    rows = verdicts(html)
    for rule, what, ok in rows:
        print("  %-8s %-88s %s" % (rule, what[:88], "pass" if ok else "FAIL"))
    return 0 if all(ok for _r, _w, ok in rows) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
