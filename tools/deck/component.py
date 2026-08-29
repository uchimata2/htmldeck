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
    found = at_rule_span(css, media)
    if not found:
        return css
    return css[:found[0]] + css[found[2]:]


def at_rule_span(css, media):
    """`(start, inner_start, end)` of `@media <media>{...}`, or None.

    Matched to the block's own closing brace rather than to the next one, because the print block
    nests `@page` - the reason `drop_at_rule` exists in this shape, kept in one place now that the
    inside of the block is wanted as well as the outside (T-242).
    """
    found = re.search(r"@media\s+%s\s*\{" % re.escape(media), css)
    if not found:
        return None
    depth, i = 1, found.end()
    while i < len(css) and depth:
        depth += 1 if css[i] == "{" else -1 if css[i] == "}" else 0
        i += 1
    return (found.start(), found.end(), i)


def print_css(html):
    """The `@media print` block's own rules - what `shared_css` cuts out.

    Section 2.1 says a `print` row is checked for its rule existing, and the rule it means is one in
    this block. Nothing read it until T-242.
    """
    for attrs, body in re.findall(r"<style([^>]*)>(.*?)</style>", html, re.S):
        if "id=" in attrs:
            continue
        span = at_rule_span(body, "print")
        return "" if not span else CSS_COMMENT.sub("", body[span[1]:span[2] - 1])
    return ""


CSS_COMMENT = re.compile(r"/\*.*?\*/", re.S)


def rules(css):
    """`[(selector, declarations)]`, one per comma-separated selector, at-rules dropped.

    **Comments go first, because the text between one rule's `}` and the next rule's `{` includes
    any comment written there** - and everything below reads that text AS a selector. `density.py`
    carried the same defect in the same shape and it is fixed there in the same change.
    """
    css = CSS_COMMENT.sub(" ", css)
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

# Values an `#ARRAY` attribute may hold that are not subscripts. Two: `data-stage="back"` and,
# since 2026-08-20, `data-stage="front"` - the lobby a deck may open on (T-200). Both name matter
# that is outside the argument, which is why neither indexes a stage.
# marks a slide as outside the argument, so it indexes nothing (T-108). Kept as a set rather than a
# literal because the contract states it as a vocabulary, and the next one must not need this
# branch rewritten.
NOT_AN_INDEX = frozenset(["back", "front"])


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
            # **A lobby rests on nothing, so it carries no provenance mark** (DS-242, T-200). This
            # is the one scoped exemption in the count check and it is stated rather than inferred:
            # `.provenance` says *what the argument rests on*, and front matter is not the argument
            # - the same shape as DS-225's *back matter carries no mark*, which the ruleset already
            # holds. It is narrow on purpose. DS-085 warns that a slide kind relaxing the contract
            # hands the next slide kind the same argument, so the exemption names one part and one
            # stage, and everything else on a lobby is the ordinary contract.
            if name == "provenance" and "front" in (h.attrs.get("data-stage", ""), ):
                continue
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
                    def indexes(v):
                        # `back` is the one non-positional value: it marks a slide as outside the
                        # argument, so it indexes nothing and must not be read as out of range
                        # (T-108, COMPONENT-CONTRACT.md).
                        return v in NOT_AN_INDEX or (v.isdigit() and int(v) < size)
                    wrong = sorted({v or "(empty)" for _e, v in held if not indexes(v)})
                    if wrong:
                        bad.append(".%s: %s is a zero-based index into %s (0-%d), or %s, and %d "
                                   "element(s) leave it: %s"
                                   % (name, attr, needs[1:], size - 1,
                                      " or ".join("`%s`" % v for v in sorted(NOT_AN_INDEX)),
                                      len([v for _e, v in held if not indexes(v)]),
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


# **The deck-local prefix** (T-266, adopter report `014`). A class under it is the deck's own, and
# DS-229 does not hold it to a contract it could never be in - the contract ships in the plugin, so
# *uncontracted* named a row a builder had nowhere to add.
#
# **It reserves a name; it does not hide a component.** A contracted class stays contracted however
# it is reached: `.d-x .slide{...}` puts `slide` in `styled`, where its row and every structural
# DS-229 check still decide it. What the prefix does buy a deck is an ancestor of its own to scope
# such a rule from - measured while this landed, `.d-x .headline{color:red}` passes where
# `.x .headline{color:red}` failed. **That is a smaller change than it looks**: `.slide .headline`
# scoped from a contracted ancestor has always passed, so the deck could already restyle a component
# and this only spares it borrowing a name. Restyling was never what this check decides; it decides
# whether a component nobody contracted has been invented, and that is unchanged.
#
# `d-` was the report's own proposal and nothing in the tree starts with it - checked against the
# contract and the shell's stylesheets when this landed. Short on purpose: it is typed on every
# figure-internal class a deck writes.
DECK_LOCAL = "d-"


def missing_rows(parts, styled):
    """Classes the shared block styles and the contract does not name.

    A class every one of whose rules sits under one of the ADAPTATIONS above is `#slides`' class
    reached from another rendering, and not a component. A class with even one unscoped rule is.

    A class under `DECK_LOCAL` is neither: it is the deck naming its own repeated treatment, which
    is what a class is for and which no component contract can anticipate.
    """
    out, local = [], []
    for c, sels in sorted(styled.items()):
        if c in parts or all(s.startswith(ADAPTATIONS) for s in sels):
            continue
        if c.startswith(DECK_LOCAL):
            local.append(c)
            continue
        out.append(c)
    return out, local


PSEUDO_FN = re.compile(r":(?:where|is|matches|any)\s*\(")
SIMPLE = re.compile(r"\[[^\]]*\]|\.[A-Za-z_][\w-]*|#[A-Za-z_][\w-]*|::?[A-Za-z-]+|[A-Za-z][\w-]*")


def compounds(selector):
    """`selector` as a list of compounds, each a set of its simple selectors.

    A functional pseudo-class is a bracket around part of the chain rather than a step in it, so
    `:where(...)` and `:is(...)` are flattened into it. Combinators are treated as descendant,
    which is deliberate: this decides *does this rule style that thing*, not *how tightly*.
    """
    flat = PSEUDO_FN.sub(" ", selector).replace(")", " ").replace(">", " ")
    flat = flat.replace("+", " ").replace("~", " ")
    return [set(SIMPLE.findall(c)) for c in flat.split() if c.strip()]


def selector_covers(contract_sel, css_sel):
    """Does the rule `css_sel` style what the contract row `contract_sel` names?

    True when the contract's compounds are the TAIL of the rule's, each a subset of the rule's
    compound in that place. `.pulse` is covered by `:where(.slide[data-played]) .pulse` and by
    `.slide[data-played] .pulse`, and is not covered by `.pulse-ring` or by `.pulse .label`.
    """
    want, got = compounds(contract_sel), compounds(css_sel)
    if not want or len(want) > len(got):
        return False
    tail = got[len(got) - len(want):]
    return all(w <= g for w, g in zip(want, tail))


def absent_tokens(toks, bodies):
    """The contract tokens none of `bodies` reads."""
    joined = "\n".join(bodies).replace(" ", "")
    return [t for t in toks if ("var(%s" % t) not in joined]


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
            bodies, by_scope = ([m.group(1)] if m else []), []
        else:
            # **Exact text first, then the compound** (the adopter's `020`). Keying the row on the
            # selector AS WRITTEN meant that scoping a motion to a state -
            # `:where(.slide[data-played]) .pulse`, the ordinary way to say *this plays on
            # arrival* - left the row with no rule to find. The tokens were declared, the motion
            # worked, and the gate reported the row unsatisfied: the natural construction failed
            # and the awkward one passed, which teaches the awkward one.
            #
            # **Scope is consulted whenever the tokens are still missing, not only when no rule
            # matched exactly.** A deck usually keeps several rules on one class - the density
            # gate, the reduced-motion collapse, the preflight - so `.pulse` matched exactly and
            # read none of the tokens, and a fallback guarded on *no exact match* never ran.
            #
            # The exact match is still tried first and still wins on its own, because matching on
            # the compound alone would let `.rise` be answered by `.slide[data-played] .rise` - a
            # different rule with different tokens. When scope is what completed the row, the row
            # says so rather than passing silently, which is the second half of what `020` asked.
            bodies, by_scope = by_sel.get(sel, []), []
            if absent_tokens(toks, bodies):
                for css_sel, css_bodies in by_sel.items():
                    if css_sel != sel and selector_covers(sel, css_sel):
                        by_scope.append(css_sel)
                        bodies = bodies + css_bodies
        if not bodies:
            bad.append("%s is in the contract and not in the deck's CSS" % sel)
            continue
        absent = absent_tokens(toks, bodies)
        if absent:
            bad.append("%s does not read %s" % (sel, " ".join(absent)))
    return bad


def unstyled_rows(parts, styled, printed):
    """`script` and `print` rows whose class no rule declares - section 2.1's stated check.

    **The document said this was checked and nothing checked it** (`PR-34`, T-242). `structure`
    opens by skipping both sources, and `missing_rows` runs the other way - it iterates the STYLED
    classes and asks which have a row - so a contracted class with no rule at all was examined by
    nobody. Section 2.1's own reason for the `vocabulary` source is this one: *declared and unused
    is otherwise unfalsifiable*, and `script` and `print` were declared-and-unverified in exactly
    that shape. Four rows carry the two sources and all four happen to be styled, which is why
    nothing surfaced.
    """
    bad = []
    for name in sorted(parts):
        source = parts[name].source
        if source == "script" and name not in styled:
            bad.append(".%s is `script` and no rule in the shared block styles it" % name)
        elif source == "print" and name not in printed:
            bad.append(".%s is `print` and no rule in the print block styles it" % name)
    return bad


MOTION_DECL = re.compile(r"(?:^|;)\s*(?:animation|transition)(?:-[a-z-]+)?\s*:\s*([^;]+)", re.I)


def unrowed_motions(css, motions):
    """CSS rules that start a motion on a token and have no row in §3.8 - the other direction.

    **`motion_gaps` iterates the CONTRACT and asks whether the CSS agrees; nothing iterated the
    CSS.** So a rule with no row at all was invisible to the table that calls itself *that sentence
    made checkable*, and `.arrow-pop marker path` and `.dot-pop circle` animated on `--scale-dur`
    with no row here - the same defect T-198 fixed once by hand, recurring because nothing looked
    this way round (`PR-35`, T-242). Section 1's parts table has had a completeness half from the
    start, for exactly this reason.

    **A motion is a declaration that starts one**: `animation` or `transition`, or one of their
    longhands, valued something other than `none` and reading at least one token. A rule switching
    motion off reads `none` and is not one, so the reduced-motion collapse, the preflight and the
    density gate stay quiet without being named here. **A rule the contract's selector covers is
    accounted for** - `:where(.slide[data-played]) .pulse` is `.pulse`'s row, which is the same
    scope rule `motion_gaps` reads in the other direction.
    """
    rowed = [sel for sel, _toks in motions]
    seen, out = set(), []
    for sel, body in rules(css):
        if sel in seen:
            continue
        for value in MOTION_DECL.findall(body):
            v = value.strip()
            if v.startswith("none") or "var(" not in v:
                continue
            if any(selector_covers(r, sel) for r in rowed):
                break
            seen.add(sel)
            out.append(sel)
            break
    return out


def scoped_rows(css, motions):
    """Contract rows that only their SCOPED form satisfies - `[(row, [selector])]`.

    Reported rather than left silent: a row satisfied by `:where(...) .pulse` is satisfied, and a
    reader who cannot see that the exact selector is absent has no way to tell this deck from one
    where the contract and the stylesheet actually agree.
    """
    by_sel = {}
    for sel, body in rules(css):
        by_sel.setdefault(sel, []).append(body)
    out = []
    for sel, toks in motions:
        if sel.startswith("@keyframes") or not absent_tokens(toks, by_sel.get(sel, [])):
            continue
        hits = [s2 for s2 in by_sel if s2 != sel and selector_covers(sel, s2)]
        if hits and not absent_tokens(toks, by_sel.get(sel, [])
                                      + [b for s2 in hits for b in by_sel[s2]]):
            out.append((sel, hits))
    return out


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
    missing, deck_local = missing_rows(parts, styled)
    gaps = motion_gaps(css, motions)
    scoped = scoped_rows(css, motions)
    unrowed = unrowed_motions(css, motions)
    unstyled = unstyled_rows(parts, styled, styled_classes(print_css(html)))

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
        # The scoped count travels in the text for the reason every denominator here does
        # (**L-36**): *0 gaps* over rules all matched exactly and *0 gaps* over a deck where three
        # rows were completed by a scoped rule are the same boolean and not the same fact.
        ("DS-229", "every rule the contract lists reads the motion tokens it lists: "
         "%d rule(s), %d gap(s)%s%s"
         % (len(motions), len(gaps), "" if not gaps else " - " + "; ".join(gaps[:3]),
            "" if not scoped else "; %d row(s) satisfied by a scoped rule rather than the "
            "contracted selector - %s" % (len(scoped),
                                          "; ".join("%s via %s" % (r, h[0]) for r, h in scoped[:2]))),
         not gaps),
        # **The completeness half of the motion table** (T-242, `PR-35`). Its own row rather than a
        # clause on the one above, because the two are different obligations: a row whose rule has
        # stopped reading its tokens, and a rule with no row at all. One number covering both would
        # have let the second hide inside the first, which is how it stayed invisible.
        ("DS-229", "every rule that starts a motion on a token has a row: %d unrowed%s"
         % (len(unrowed), "" if not unrowed else " - " + "; ".join(unrowed[:3])),
         not unrowed),
        # **The message names the remedy and not only the failure** (T-266, adopter report `014`).
        # *Uncontracted* was read as *not yet in the contract*; the contract ships in the plugin, so
        # the builder went looking for the row to add and the search ended nowhere. That cost one
        # full check cycle there and would have cost every deck the same one.
        #
        # The deck-local count travels for the reason every denominator here does (**L-36**):
        # *0 uncontracted* over a deck that names nothing of its own, and over one that names
        # eleven figure treatments, are the same boolean and not the same fact.
        ("DS-229", "every class the shared block styles has a row: %d styled, %d deck-local, "
         "%d uncontracted%s"
         % (len(styled), len(deck_local), len(missing),
            "" if not missing else " - ." + " .".join(missing[:6])
            + "; a deck may not add a contracted class - carry the properties as presentation "
              "attributes on the element, or name it `.%s...` if it is the deck's own repeated "
              "treatment" % DECK_LOCAL),
         not missing),
        # Section 2.1 states this check for its `script` and `print` sources and nothing ran it
        # (`PR-34`, T-242). The count of rows carrying those sources travels with the verdict, so
        # *0 problems* over four rows and *0 problems* over none are not the same fact (**L-36**).
        ("DS-229", "every `script` and `print` row's class is styled where its source says: "
         "%d row(s), %d problem(s)%s"
         % (len([p for p in parts.values() if p.source in ("script", "print")]),
            len(unstyled), "" if not unstyled else " - " + "; ".join(unstyled[:3])),
         not unstyled),
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
        # `back` indexes nothing and is legal (T-108). Asserted in BOTH directions, because a
        # vocabulary widened by one value is one step from a vocabulary that admits anything: the
        # word passes and a near-miss still fails.
        okd = parse(doc.replace('data-stage="0"', 'data-stage="back"'))
        if structure(okd, one, {}, stages):
            sys.exit("SELF-TEST FAILED: data-stage=\"back\" was reported: %s"
                     % structure(okd, one, {}, stages))
        for near in ('data-stage="backmatter"', 'data-stage="Back"', 'data-stage="back matter"'):
            broke = parse(doc.replace('data-stage="0"', near))
            if not any("index into STAGES" in m for m in structure(broke, one, {}, stages)):
                sys.exit("SELF-TEST FAILED: %s was accepted - the back-matter value is a word, "
                         "not a prefix" % near)
        # `data-stage="back "` is deliberately NOT in that list. Surrounding whitespace is stripped
        # here and `deck.js` trims the same attribute before reading it, so the two agree that it is
        # the same value - and a checker stricter than the runtime it guards reports defects that
        # are not there.
        # ...and with no array to index, the deck is missing the declaration rather than the value.
        if not any("declares no such array" in m for m in structure(parse(doc), one, {}, {})):
            sys.exit("SELF-TEST FAILED: a data-stage with no STAGES declared was not reported")
    if script_arrays("  var STAGES = ['a','b','c'];\n  var idx = 0;").get("STAGES") != 3:
        sys.exit("SELF-TEST FAILED: the deck's STAGES array was not counted")

    # The completeness check has to notice a component nobody contracted, or it is decoration.
    if not missing_rows({}, {"invented": [".invented"]})[0]:
        sys.exit("SELF-TEST FAILED: an uncontracted class was not reported")
    if missing_rows({}, {"ledger": [".doc .ledger"]})[0]:
        sys.exit("SELF-TEST FAILED: a reading-view adaptation was reported as a component")
    if missing_rows({}, {"figwrap": [":root[data-preflight] .figwrap"]})[0]:
        sys.exit("SELF-TEST FAILED: a degraded-state adaptation was reported as a component")
    # And the half that keeps the exemption narrow: one unscoped rule and it IS a component.
    if not missing_rows({}, {"preflight": [".preflight", ":root[data-preflight] .preflight"]})[0]:
        sys.exit("SELF-TEST FAILED: a class with an unscoped rule was exempted as an adaptation")

    # **The deck-local prefix, both directions** (T-266). The allowance and the thing it must not
    # become are asserted together, because a prefix that exempted anything NEAR it would give away
    # the rule the report explicitly did not ask to weaken.
    bad, local = missing_rows({}, {"d-ico": [".fig .d-ico"]})
    if bad or local != ["d-ico"]:
        sys.exit("SELF-TEST FAILED: a deck-local class was reported as uncontracted, so T-266's "
                 "prefix bought nothing - naming a repeated figure treatment once IS the request")
    if not missing_rows({}, {"ico": [".fig .ico"]})[0]:
        sys.exit("SELF-TEST FAILED: an unprefixed class was exempted. The prefix is opt-in on "
                 "purpose - a deck that has not asked for the escape does not get it")
    bad, local = missing_rows({}, {"drop": [".drop"], "d": [".d"]})
    if len(bad) != 2 or local:
        sys.exit("SELF-TEST FAILED: `.drop` or `.d` was taken for a deck-local class. The prefix "
                 "is `%s` and the hyphen is what makes it a prefix rather than a first letter"
                 % DECK_LOCAL)
    # The one thing the prefix must never do: take a contracted class out of the check because the
    # rule reaching it is deck-local. The class is what is decided, never the selector around it.
    if not missing_rows({}, {"slide": [".d-x .slide"]})[0]:
        sys.exit("SELF-TEST FAILED: a contracted class styled from a deck-local rule escaped the "
                 "contract. The prefix reserves a name; a component stays a component however it "
                 "is reached")
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

    # ---- T-242: the two directions the contracts stated and nothing decided ------------------
    #
    # **`unrowed_motions` is the completeness half of the motion table.** Both directions, because
    # a check that only ever reports is as useless as one that only ever passes (**L-125**).
    _rows = [(".pulse", ["--pulse-dur"])]
    if unrowed_motions(".gizmo{animation:spin var(--scale-dur) linear}", _rows) != [".gizmo"]:
        sys.exit("SELF-TEST FAILED: a rule animating on a token with no row in section 3.8 was not "
                 "reported - that is `.arrow-pop marker path` and two others, which animated "
                 "unrowed because nothing iterated the CSS (`PR-35`)")
    if unrowed_motions(".gizmo{animation:none}", _rows):
        sys.exit("SELF-TEST FAILED: a rule switching motion OFF was read as starting one. The "
                 "reduced-motion collapse, the preflight and the density gate are all that shape "
                 "and would each need a row they should not have")
    if unrowed_motions(".gizmo{animation:spin 300ms linear}", _rows):
        sys.exit("SELF-TEST FAILED: a rule animating on a LITERAL was reported here. That is "
                 "DS-010's defect and this table's positive claim is about tokens")
    if unrowed_motions(":where(.slide[data-played]) .pulse{transition:opacity var(--pulse-dur)}",
                       _rows):
        sys.exit("SELF-TEST FAILED: a rule the contract's own selector covers was reported as "
                 "unrowed - the scope rule `motion_gaps` reads has to hold in both directions")

    # **`unstyled_rows` is section 2.1's stated check**, and each source looks in its own block.
    _parts = {"disc-lead": Part("disc-lead", None, None, False, 0, None, (), "script"),
              "contents": Part("contents", None, None, False, 0, None, (), "print")}
    if unstyled_rows(_parts, {"disc-lead"}, {"contents"}):
        sys.exit("SELF-TEST FAILED: two rows styled exactly where their source says were reported")
    if len(unstyled_rows(_parts, set(), set())) != 2:
        sys.exit("SELF-TEST FAILED: a `script` and a `print` row with no rule anywhere were not "
                 "reported - section 2.1 states this check and nothing ran it (`PR-34`)")
    if not unstyled_rows(_parts, {"disc-lead", "contents"}, set()):
        sys.exit("SELF-TEST FAILED: a `print` row styled in the SHARED block passed. Its source "
                 "says the print block, and a rule in the wrong block is what the row claims about")
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
