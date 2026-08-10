#!/usr/bin/env python3
"""The theme region: read it out of a deck, validate it against the contract, swap it.

A deck is one self-contained file, so a theme cannot be a stylesheet the browser loads. It is a
**region** — exactly one `<style id="theme">` holding every `@font-face` and every `:root` block —
and swapping a theme replaces that element's contents and touches nothing else.

`docs/THEME-CONTRACT.md` is the contract, and **this file parses it rather than restating it**
(**L-08**, **L-13**): adding a token to the document has to change what `validate` demands without
anyone editing this file. The same reason `ruleset.py` reads `DESIGN-SYSTEM.md`.

    python tools/deck/theme.py tokens                       # the contract, as data
    python tools/deck/theme.py validate themes/quarto.css   # a theme against it
    python tools/deck/theme.py swap <deck> themes/<name>.css [-o out.html]
    python tools/deck/theme.py check <deck>                 # the rows the gate asks for

Without `-o`, a swap writes to `.assets-cache/deck/themed/<deck>-<theme>.html` — where
`docs/THEME-CONTRACT.md` §1 says a themed copy belongs. **It never writes to the deck it was
given**, whatever `-o` says; that default cost a recovery once (**T-059**).

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

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONTRACT = os.path.join(ROOT, "docs", "THEME-CONTRACT.md")
FACES = os.path.join(ROOT, "themes", "faces")
OUT = os.path.join(ROOT, ".assets-cache", "deck", "themed")

AXES = ("colour", "type", "geometry", "shape", "motion")
KINDS = ("primitive", "derived", "fixed")

REGION_OPEN = '<style id="theme">'
REGION = re.compile(r'<style\s+id="theme"\s*>(.*?)</style>', re.S)
FACE_DIRECTIVE = re.compile(r"/\*\s*htmldeck-faces:\s*([^*]+?)\s*\*/")


# ---------------------------------------------------------------------------- the contract


class Token(object):
    __slots__ = ("name", "axis", "kind", "governs", "legal")

    def __init__(self, name, axis, kind, governs, legal):
        self.name, self.axis, self.kind = name, axis, kind
        self.governs, self.legal = governs, legal

    @property
    def rule(self):
        """The rule a range comes from, read out of the *Governs* cell.

        **A range with no rule behind it is a number invented to fit one deck** (**L-38**), and
        the self-test refuses one. Reading the citation rather than storing it in a column of its
        own means the sentence a person reads and the rule the gate cites cannot disagree.
        """
        cited = re.findall(r"DS-\d{3}", self.governs)
        return cited[-1] if cited else None

    def __repr__(self):
        return "<%s %s/%s>" % (self.name, self.axis, self.kind)


def parse_token_row(line):
    """One `| --name | axis | kind | governs | legal |` row, or None.

    Read from the left for the first three cells and from the right for the last, because
    *Governs* routinely contains a pipe inside a code span - the same trap `ruleset.py` records
    for the rule table, and the reason neither counts columns from one end only.
    """
    if not line.startswith("| `--"):
        return None
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) < 5:
        return None
    name = cells[0].strip("` ")
    axis, kind, legal = cells[1], cells[2], cells[-1].strip("` ")
    governs = "|".join(cells[3:-1]).strip()
    if axis not in AXES or kind not in KINDS:
        return None                     # a table that is not the token table
    return Token(name, axis, kind, governs, legal)


def parse_exemption_row(line):
    """One `| where | property | value | why |` row of §5, as `(where, props, magnitudes)`.

    `None` in a slot means *anything here*. `props` is otherwise `("not", {...})` — the form the
    composition row uses, because the properties a theme owns are a short list and everything
    else is one deck's composition. Both are read from the code spans in the cell, so the table a
    person reads and the list the check applies are the same characters.
    """
    if not line.startswith("| "):
        return None
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) != 4 or cells[0] in ("Where", ":---"):
        return None
    where = cells[0].strip("` ")
    if where != "any" and not where.startswith((".", "#")):
        return None                     # not an exemption row

    def spans(cell):
        return [s.strip() for s in re.findall(r"`([^`]+)`", cell)]

    props = None
    if cells[1].strip().lower() != "any":
        names = spans(cells[1])
        if not names:
            return None
        props = ("not", set(names)) if "not" in cells[1].lower() else ("only", set(names))

    mags = set()
    for s in spans(cells[2]):
        m = re.match(r"^(-?(?:\d+(?:\.\d+)?|\.\d+))(px|rem|em|ch|ms|s)?$", s)
        if m:
            mags.add(float(m.group(1)))
    return (where, props, mags or None)


def load(path=CONTRACT):
    """`(tokens, exemptions)` from the contract document."""
    tokens, exempt = {}, []
    section = ""
    for line in io.open(path, encoding="utf-8"):
        if line.startswith("#"):
            section = line.strip()
        t = parse_token_row(line)
        if t is not None:
            if t.name in tokens:
                sys.exit("CONTRACT: %s appears twice" % t.name)
            tokens[t.name] = t
            continue
        if "may still be a literal" in section or "still be a literal" in section:
            e = parse_exemption_row(line)
            if e is not None:
                exempt.append(e)
    if len(tokens) < 50:
        sys.exit("CONTRACT: parsed only %d tokens from %s - the format moved under the parser"
                 % (len(tokens), path))
    if not exempt:
        sys.exit("CONTRACT: no exemption parsed from %s. An empty list is not the same as none "
                 "declared, and the difference is every literal in the deck" % path)
    return tokens, exempt


# ---------------------------------------------------------------------------- values


def declarations(css_text):
    """`{--name: value}` for every custom property declared, last wins."""
    return dict(re.findall(r"(--[a-z0-9-]+)\s*:\s*([^;{}]+);", css_text))


def expand(value, decls, depth=8):
    for _ in range(depth):
        if "var(" not in value:
            break
        value = re.sub(r"var\(\s*(--[a-z0-9-]+)[^)]*\)",
                       lambda m: decls.get(m.group(1), "").strip(), value)
    return value


ARITH = re.compile(r"^[-+*/(). \d]+$")


def number(value, decls, unit="du"):
    """The value as a plain number in `unit`, or None if it does not reduce to one.

    `du` means design units, which are CSS pixels before the transform - so `--du` expands to
    `1px`, `px` drops out, and what is left is arithmetic. **The evaluation is guarded by a
    whitelist**: anything that is not digits and operators after the units are stripped returns
    None rather than being handed to `eval`.
    """
    v = expand(str(value), decls).strip()
    v = re.sub(r"/\*.*?\*/", "", v, flags=re.S).strip()
    if unit == "ms":
        v = re.sub(r"(\d(?:[\d.]*)?)\s*s\b", lambda m: "%s" % (float(m.group(1)) * 1000), v)
        v = v.replace("ms", "")
    else:
        for u in ("px", "rem", "em", "ch"):
            v = v.replace(u, "")
    v = re.sub(r"\bcalc\b", "", v)
    if not v or not ARITH.match(v):
        return None
    try:
        return float(eval(v, {"__builtins__": {}}, {}))       # noqa: S307 - guarded by ARITH
    except (SyntaxError, ZeroDivisionError, TypeError, NameError):
        return None


def check_legal(tok, decls):
    """`None` if the token's value satisfies its *Legal* cell, else what is wrong with it."""
    legal = tok.legal.strip()
    raw = decls.get(tok.name)
    if raw is None:
        return "not declared"
    if legal in ("", "—", "-"):
        return None
    if legal == "colour":
        return None if re.match(r"^\s*(#[0-9A-Fa-f]{3,8}|rgba?\(|hsla?\()", raw) \
            else "is %r, which is not a colour" % raw.strip()
    if legal == "1px":
        return None if raw.strip() == "1px" else "is %r; the design unit is fixed at 1px" % raw.strip()
    m = re.match(r"^(n|du|rem|ms)\s+(-?[\d.]+)-(-?[\d.]+)?$", legal)
    if not m:
        sys.exit("CONTRACT: %s has Legal %r, which is not a form this file knows" % (tok.name, legal))
    kind, lo = m.group(1), float(m.group(2))
    hi = float(m.group(3)) if m.group(3) else float("inf")
    got = number(raw, decls, "ms" if kind == "ms" else "du")
    if got is None:
        return "is %r, which does not reduce to a number" % raw.strip()
    if not (lo - 1e-9 <= got <= hi + 1e-9):
        return "is %.4g, outside the %s %g-%s %s allows"  \
            % (got, kind, lo, "" if hi == float("inf") else "%g" % hi, tok.rule or "the contract")
    return None


def validate(source, tokens=None):
    """Every way a theme fails the contract, as `[(rule or None, message)]`.

    **The rule travels with the problem** so the gate cites what it measured (T-038): a duration
    outside its band is DS-140's defect and a body size outside 24-28 is DS-034's, neither is
    "the contract" in general. `None` is the contract's own — a token missing, undocumented, or
    pinned where it should derive.
    """
    tokens = tokens if tokens is not None else load()[0]
    decls = declarations(source)
    bad = []
    for name in sorted(tokens):
        tok = tokens[name]
        problem = check_legal(tok, decls)
        if problem:
            # A missing token is the contract's problem whatever the rule behind its range.
            bad.append((None if problem == "not declared" else tok.rule,
                        "%s %s" % (name, problem)))
            continue
        value = decls[name]
        # `var(--du)` does not count. A derived token rewritten as `calc(30*var(--du))` still
        # carries a var() and has still left the scale, which is exactly the defect this names.
        refs = set(re.findall(r"var\(\s*(--[a-z0-9-]+)", value)) - {"--du"}
        if tok.kind == "derived" and not refs:
            bad.append((None,
                        "%s is `derived` and references no dial - a derived token written as a "
                        "literal has left the scale, which is the defect the kind exists to name"
                        % name))
    for name in sorted(set(decls) - set(tokens)):
        bad.append((None, "%s is declared and the contract does not name it - add a row or drop "
                          "the token; an undocumented dial is one a generator cannot set" % name))
    return bad


# ---------------------------------------------------------------------------- faces


def face_slugs(source):
    m = FACE_DIRECTIVE.search(source)
    return [s.strip() for s in m.group(1).split(",") if s.strip()] if m else []


def resolve(source, faces_dir=FACES):
    """A theme's source form -> the form that sits in a deck: faces inlined where the directive was.

    DS-001 is why this exists at all. The source form names its faces so that two themes sharing a
    face share one copy of a 30 KB payload in the repository; the resolved form carries the bytes,
    so the deck is still one file with zero external references.
    """
    slugs = face_slugs(source)
    if not slugs:
        return source
    parts = []
    for slug in slugs:
        path = os.path.join(faces_dir, slug + ".css")
        if not os.path.exists(path):
            sys.exit("theme names the face %r and %s does not exist"
                     % (slug, paths.display_path(path, ROOT)))
        parts.append(io.open(path, encoding="utf-8").read().rstrip("\n"))
    return FACE_DIRECTIVE.sub(lambda _m: "\n\n".join(parts), source, count=1)


# ---------------------------------------------------------------------------- the region


def extract(html):
    """The theme region's contents, or None if the deck has no region."""
    m = REGION.search(html)
    return m.group(1) if m else None


def swap(html, resolved):
    """`html` with its theme region replaced. Everything outside the region is untouched."""
    if not REGION.search(html):
        sys.exit("this deck has no <style id=\"theme\"> region to swap")
    return REGION.sub(lambda _m: '%s\n%s\n</style>' % (REGION_OPEN, resolved.strip("\n")),
                      html, count=1)


def destination(deck, theme, out=None):
    """Where a swap writes — and the one file it must never write.

    `out` is `-o` when it was given. Without it the destination is derived under `OUT`, which is
    where `THEME-CONTRACT.md` §1 says a themed copy belongs: *the demonstration deck is built, not
    committed*. **The default used to be `deck` itself**, and on 2026-08-09 that replaced the
    reference deck mid-task (T-059). It was noticed only because the byte count moved; a themed
    build of the same size would have passed every check in the repository, because the gate reads
    whatever deck it is pointed at and a themed reference deck is a valid deck.

    Raises `ValueError` when the destination resolves to the input — including `-o` naming it, and
    a second spelling of the same file. **Raising rather than exiting is deliberate**: the self-test
    has to be able to observe the refusal, and a function that ends the process can only be trusted,
    never asserted (**L-04**).
    """
    if out is None:
        stem = lambda p: os.path.splitext(os.path.basename(p))[0]                      # noqa: E731
        out = os.path.join(OUT, "%s-%s.html" % (stem(deck), stem(theme)))
    if os.path.realpath(out) == os.path.realpath(deck):
        raise ValueError("that would overwrite the deck it was given (%s). A swap reads one file "
                         "and writes another; pass -o with a different path, or omit -o and it "
                         "goes to %s" % (paths.display_path(deck, ROOT),
                                         paths.display_path(OUT, ROOT)))
    return out


def styles(html):
    """`[(attrs, body)]` for every `<style>` in the deck."""
    return re.findall(r"<style([^>]*)>(.*?)</style>", html, re.S)


def outside_region(html):
    """`[(scope, css)]` for every style block that is not the theme region.

    **The scope is the block's own id**, prefixed onto each selector below, so an exemption can
    name a whole block — which is what `#slides` is: rules that exist because one deck has a
    ledger with three columns, and that a generated deck would emit differently.

    `@media print` is dropped: paper is a different medium with no theme, and DS-226 requires a
    floor in POINTS there, which the stage's own rules forbid. `audit.screen_css` excludes it for
    the same reason.
    """
    out = []
    for attrs, body in styles(html):
        if 'id="theme"' in attrs:
            continue
        m = re.search(r'id="([^"]+)"', attrs)
        body = re.sub(r"url\(\s*data:[^)]*\)", "url(data:)", body, flags=re.S)
        body = re.split(r"@media\s+print\s*\{", body)[0]
        out.append(("#" + m.group(1) if m else "",
                    re.sub(r"/\*.*?\*/", "", body, flags=re.S)))
    return out


# `.6rem` is a length and `(?<![\w.-])` used to skip it, because the lookbehind rejected the
# number's own leading dot. Four `rem` gaps in the reading view went unseen that way.
NUM = r"(-?(?:\d+(?:\.\d+)?|\.\d+))"
LITERAL = re.compile(
    NUM + r"\s*\*\s*var\(\s*--du\s*\)"                     # a design-unit literal
    r"|(?<![\w#-])" + NUM + r"(px|rem|em|ch|ms|s)\b"       # a length or a duration
)


# An easing CURVE outside the region, which §5 admits no exception to. The keywords are the rules'
# own words - DS-141 says *ease-in-out*, and `linear` is the only easing a looping dash and a
# zero-duration step survive - so they are not scanned; a curve is a choice about how a motion
# feels and there is exactly one in this deck, `--rise-ease`, inside the region.
CURVE = re.compile(r"\b(cubic-bezier|steps)\s*\(")


def curves(html):
    """`[(selector, declaration)]` for every easing curve written outside the region.

    Restricted to `transition` and `animation` declarations on purpose: `cubic-bezier` is also the
    argument form of `offset-rotate` and of an `@keyframes` timing function, and a scan of every
    declaration would report the same defect from two directions."""
    found = []
    for scope, css_text in outside_region(html):
        for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css_text):
            sel = (scope + " " + " ".join(sel.split())).strip()
            for decl in body.split(";"):
                d = " ".join(decl.split())
                if ":" not in d or d.startswith("--"):
                    continue
                if not d.split(":")[0].strip().startswith(("transition", "animation")):
                    continue
                if CURVE.search(d):
                    found.append((sel, d))
    return found


def literals(html):
    """`[(selector, declaration, magnitude, exempt-reason or None)]` outside the region.

    Every length and duration written outside the theme is a value a theme cannot reach. Colour is
    not scanned here - `audit.ds010_colours_tokenised` has owned that half since T-005, and two
    checks measuring one thing is how a count stops meaning anything.
    """
    _tokens, exemptions = load()
    found = []
    for scope, css_text in outside_region(html):
        for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css_text):
            sel = (scope + " " + " ".join(sel.split())).strip()
            if "@" in sel:
                continue                # an at-rule prelude: keyframe stops carry no selector
            for decl in body.split(";"):
                d = " ".join(decl.split())
                if not d or d.startswith("--") or ":" not in d:
                    continue            # a component-scoped custom property is its own defect
                prop = d.split(":")[0].strip()
                for m in LITERAL.finditer(d):
                    mag = float(m.group(1) or m.group(2))
                    found.append((sel, d, mag, _exempt(exemptions, sel, prop, mag)))
    return found


def _exempt(exemptions, sel, prop, mag):
    """The `Where` of the first exemption covering this literal, or None."""
    for where, props, mags in exemptions:
        if where != "any" and where not in sel:
            continue
        if props is not None:
            named = any(prop.startswith(p) for p in props[1])
            if (props[0] == "not") == named:
                continue                # `not` excludes the named ones; `only` admits them
        if mags is None or mag in mags:
            return where
    return None


# ---------------------------------------------------------------------------- verdicts


def verdicts(html):
    """`(rule, what, ok)` rows, in the shape every other stage returns.

    Counts travel in the verdict text on purpose: a scan that found no literal because it read no
    declarations reads exactly like a clean deck, and the count is what separates them (**L-36**).
    """
    tokens, _ = load()
    region = extract(html)
    regions = len([1 for attrs, _b in styles(html) if 'id="theme"' in attrs])

    # Every :root and every @font-face inside the region, or the region is not the theme.
    stray_roots, stray_faces = 0, 0
    for attrs, body in styles(html):
        if 'id="theme"' in attrs:
            continue
        stray_roots += len(re.findall(r":root(?:\s*\[[^\]]*\])?\s*\{", body))
        stray_faces += body.count("@font-face")

    lits = literals(html) if region else []
    offending = [l for l in lits if l[3] is None]
    bad = validate(region, tokens) if region else [(None, 'no <style id="theme"> region')]
    own = [m for rule, m in bad if rule is None]

    rows = [
        ("DS-011", "one theme region: %d declared, %d :root and %d @font-face outside it"
         % (regions, stray_roots, stray_faces),
         regions == 1 and not stray_roots and not stray_faces),
        ("DS-013", "every token THEME-CONTRACT.md names is declared and derives as it says: "
         "%d token(s) required, %d problem(s)%s"
         % (len(tokens), len(own), "" if not own else " - " + "; ".join(own[:3])),
         not own),
    ]
    # **One row per rule the contract cites, always** - not one per rule currently violated. A row
    # that appears only when something is wrong is a row the coverage account cannot count, and a
    # rule nothing says anything about is SILENT rather than passing (**L-36**). `colour` is not a
    # band and its rules are `contrast.py`'s; only the numeric ranges get a row here.
    banded = [t for t in tokens.values() if t.rule and t.legal not in ("—", "-", "", "colour")]
    for rule in sorted({t.rule for t in banded}):
        held = sorted(t.name for t in banded if t.rule == rule)
        broke = [m for r, m in bad if r == rule]
        rows.append((rule, "the band it states holds in the theme: %s%s"
                     % (" ".join(held), "" if not broke else " - " + "; ".join(broke[:2])),
                     not broke))
    curved = curves(html) if region else []
    rows.append(
        ("DS-010", "no theme-varying length or easing curve outside the region: %d literal(s) "
         "scanned, %d exempt, %d offending; %d curve(s)%s"
         % (len(lits), len(lits) - len(offending), len(offending), len(curved),
            "" if not (offending or curved) else " - " + "; ".join(
                ["%s {%s}" % (s, d) for s, d, _m, _w in offending[:2]]
                + ["%s {%s}" % (s, d) for s, d in curved[:2]])),
         not offending and not curved))
    return rows


# ---------------------------------------------------------------------------- self-test


def self_test():
    tokens, exemptions = load()
    for t in tokens.values():
        if t.legal in ("—", "-", "", "colour"):
            continue
        if t.kind == "derived":
            sys.exit("CONTRACT: %s is derived and carries a Legal range. A derived value is a "
                     "consequence of its dials, so the range belongs on the dial" % t.name)
        # **A range with no rule behind it is a number invented to fit one deck** (**L-38**), and
        # the gate would then cite the contract for a threshold the contract made up. Three were
        # written that way during T-007 and were dropped rather than justified after the fact.
        if not t.rule:
            sys.exit("CONTRACT: %s allows %r and its Governs cell cites no rule. A threshold "
                     "invented to fit one deck is worse than no threshold (L-38) - cite the rule "
                     "the number comes from, or write `—`" % (t.name, t.legal))
    if not [t for t in tokens.values() if t.kind == "derived"]:
        sys.exit("CONTRACT: no token is derived, so the primitive/derived split is decorative")

    row = parse_token_row("| `--fs-body` | type | derived | Body text (DS-034). | — |\n")
    if row is None or row.name != "--fs-body" or row.kind != "derived":
        sys.exit("SELF-TEST FAILED: a well-formed token row did not parse")
    if parse_token_row("| `--x` | type | derived | a `|` in a code span | — |\n") is None:
        sys.exit("SELF-TEST FAILED: a pipe inside the Governs cell lost the row's columns")
    if parse_token_row("| Token | Axis | Kind | Governs | Legal |\n") is not None:
        sys.exit("SELF-TEST FAILED: the header row parsed as a token")

    d = {"--du": "1px", "--fs-base": "26", "--type-ratio": "1.155",
         "--fs-body": "calc(var(--fs-base)*var(--du))",
         "--pulse-dur": "1.2s", "--rise-dur": "340ms"}
    if abs(number(d["--fs-body"], d) - 26.0) > 1e-9:
        sys.exit("SELF-TEST FAILED: a derived du value did not reduce - %r" % number(d["--fs-body"], d))
    if abs(number(d["--pulse-dur"], d, "ms") - 1200.0) > 1e-6:
        sys.exit("SELF-TEST FAILED: seconds did not convert to milliseconds")
    if number("var(--nothing)", d) is not None:
        sys.exit("SELF-TEST FAILED: an unresolvable value returned a number")

    # **A theme that breaks a band has to fail.** A validator only ever seen passing is one nobody
    # can tell from a validator that returns nothing (**L-36**, T-051).
    ok = io.open(os.path.join(ROOT, "themes", "quarto.css"), encoding="utf-8").read()
    if validate(ok, tokens):
        sys.exit("SELF-TEST FAILED: the shipping theme does not satisfy its own contract - %s"
                 % "; ".join(m for _r, m in validate(ok, tokens)[:3]))
    if not validate(ok.replace("--lh-body:1.55", "--lh-body:2.6"), tokens):
        sys.exit("SELF-TEST FAILED: a line height outside DS-034's band validated clean")
    if not validate(ok.replace("--fs-lead:calc(var(--fs-base)*var(--type-ratio)*var(--du))",
                               "--fs-lead:calc(30*var(--du))"), tokens):
        sys.exit("SELF-TEST FAILED: a derived token rewritten as a literal validated clean")

    # The exemption list is applied, not merely parsed: a literal it covers and one it does not
    # must be told apart, or every literal in the deck is exempt and the count means nothing.
    fake = ('<style id="theme">:root{--du:1px}</style>'
            '<style>.stage{width:calc(1920*var(--du))}'
            '.slide{font-size:calc(999*var(--du))}</style>')
    got = {mag: why for _s, _d, mag, why in literals(fake)}
    if got.get(1920.0) is None or got.get(999.0) is not None:
        sys.exit("SELF-TEST FAILED: the exemption list does not separate 1920 from 999 - %r" % got)

    # Easing: the keyword is the rule's word and the curve is the theme's choice, so the scan has
    # to tell them apart in both directions or §5's line is one nobody is held to.
    keyworded = '<style id="theme">:root{--du:1px}</style><style>.a{transition:all 1ms ease-in-out}</style>'
    if curves(keyworded):
        sys.exit("SELF-TEST FAILED: an easing keyword was reported as a curve")
    if not curves(keyworded.replace("ease-in-out", "cubic-bezier(.4,0,.2,1)")):
        sys.exit("SELF-TEST FAILED: a cubic-bezier outside the region was not reported")
    if curves('<style id="theme">:root{--e:cubic-bezier(.22,1,.36,1)}</style>'):
        sys.exit("SELF-TEST FAILED: the theme's own curve was scanned as a component's")

    # **Composition versus look is the whole of the two scoped rows**, and getting it backwards
    # exempts the type scale while policing a grid track - the opposite of what the contract says.
    scoped = ('<style id="theme">:root{--du:1px}</style>'
              '<style id="slides">.stat{grid-template-columns:calc(680*var(--du)) 1fr;'
              'font-size:calc(84*var(--du))}</style>'
              '<style>.icon{width:calc(40*var(--du))}</style>')
    by_mag = {mag: why for _s, _d, mag, why in literals(scoped)}
    if by_mag.get(680.0) is None:
        sys.exit("SELF-TEST FAILED: a grid track inside #slides is composition and was policed")
    if by_mag.get(84.0) is not None:
        sys.exit("SELF-TEST FAILED: a font-size inside #slides was exempted - a slide that can "
                 "set its own type scale is a slide a theme cannot reach")
    if by_mag.get(40.0) is not None:
        sys.exit("SELF-TEST FAILED: a shared component's size was exempted as composition. The "
                 "composition rows are scoped to #slides and .ruler; outside them a width is a "
                 "value a denser theme has to be able to shrink")

    # **The destination is the one thing here that can destroy work**, so it is asserted rather
    # than exercised (T-059). The deck used below need not exist: `destination` decides a path and
    # reads nothing, which is what lets the input case be constructed on any machine.
    deck = os.path.join(ROOT, "examples", "reference-deck.html")
    # Caught rather than compared. Restoring the old `out = deck` default makes this call *raise*,
    # so a comparison on the return value is a line that can never run - it read like an assertion
    # and was dead code. The failure has to be diagnosed here or it surfaces as a traceback.
    try:
        default = destination(deck, os.path.join(ROOT, "themes", "lattice.css"))
    except ValueError:
        sys.exit("SELF-TEST FAILED: the default destination is the input deck. That is the defect "
                 "T-059 exists for, and it cost a recovery the one time it fired")
    if os.path.dirname(os.path.realpath(default)) != os.path.realpath(OUT):
        sys.exit("SELF-TEST FAILED: the default destination is not under %s, where "
                 "THEME-CONTRACT.md §1 says a themed copy belongs - %r"
                 % (paths.display_path(OUT, ROOT), default))
    # Both spellings of "the deck itself" have to be refused, or the guard only catches the
    # spelling somebody happened to try (**L-36**: a refusal never seen refusing is not a refusal).
    for named in (deck, os.path.join(ROOT, "examples", "..", "examples", "reference-deck.html")):
        try:
            destination(deck, "themes/lattice.css", named)
            sys.exit("SELF-TEST FAILED: -o naming the input deck was accepted as %r" % named)
        except ValueError:
            pass
    # ...and an ordinary -o must still go through, or the guard is refusing everything and the
    # command is simply broken in a way that looks like safety.
    elsewhere = os.path.join(OUT, "elsewhere.html")
    if destination(deck, "themes/lattice.css", elsewhere) != elsewhere:
        sys.exit("SELF-TEST FAILED: an -o that is not the input deck was not honoured")
    return True


# ---------------------------------------------------------------------------- commands


def print_tokens():
    tokens, exemptions = load()
    print("%s\n" % paths.display_path(CONTRACT, ROOT))
    for axis in AXES:
        rows = sorted((t for t in tokens.values() if t.axis == axis), key=lambda t: t.name)
        prim = len([t for t in rows if t.kind == "primitive"])
        der = len([t for t in rows if t.kind == "derived"])
        fix = len([t for t in rows if t.kind == "fixed"])
        print("  %-9s %3d  (%d primitive, %d derived, %d fixed)" % (axis, len(rows), prim, der, fix))
    print("  %-9s %3d" % ("total", len(tokens)))
    print("\n  exemptions: %d entr(ies)" % len(exemptions))
    for where, props, mags in exemptions:
        print("    %-8s %-38s %s"
              % (where,
                 "any property" if props is None
                 else "%s %s" % (props[0], " ".join(sorted(props[1]))),
                 "any value" if mags is None else " ".join("%g" % m for m in sorted(mags))))
    return 0


def print_check(deck):
    html = io.open(deck, encoding="utf-8").read()
    print("theme region - %s" % os.path.basename(deck))
    fails = 0
    for rule, what, ok in verdicts(html):
        print("  %-8s %-4s %s" % (rule, "pass" if ok else "FAIL", what))
        fails += 0 if ok else 1
    lits = literals(html)
    print("\n  %d literal(s) outside the region, %d exempt"
          % (len(lits), len([l for l in lits if l[3]])))
    for sel, decl, _m, why in lits:
        if why is None:
            print("    %-40s %s" % (sel[:40], decl[:70]))
    return 1 if fails else 0


def main(argv):
    self_test()
    cmd = argv[0] if argv else "tokens"
    if cmd == "tokens":
        return print_tokens()
    if cmd == "validate":
        src = io.open(argv[1], encoding="utf-8").read()
        bad = validate(src)
        print("%s - %s" % (paths.display_path(argv[1], ROOT),
                           "conforms" if not bad else "%d problem(s)" % len(bad)))
        for axis, msg in bad:
            print("  %-9s %s" % (axis or "-", msg))
        return 1 if bad else 0
    if cmd == "swap":
        deck, theme = argv[1], argv[2]
        try:
            out = destination(deck, theme, argv[argv.index("-o") + 1] if "-o" in argv else None)
        except ValueError as exc:
            sys.exit("refusing to swap: %s" % exc)
        html = io.open(deck, encoding="utf-8").read()
        src = io.open(theme, encoding="utf-8").read()
        bad = validate(src)
        if bad:
            sys.exit("%s does not satisfy the contract:\n  %s"
                     % (paths.display_path(theme, ROOT), "\n  ".join(bad)))
        new = swap(html, resolve(src))
        if os.path.dirname(out):
            os.makedirs(os.path.dirname(out), exist_ok=True)
        io.open(out, "w", encoding="utf-8", newline="\n").write(new)
        print("%s + %s -> %s (%d bytes)"
              % (os.path.basename(deck), os.path.basename(theme), paths.display_path(out, ROOT),
                 len(new.encode("utf-8"))))
        return 0
    if cmd == "check":
        return print_check(argv[1])
    sys.exit("usage: theme.py tokens | validate <theme.css> | swap <deck> <theme.css> [-o out] "
             "| check <deck>\n"
             "       swap without -o writes to %s/<deck>-<theme>.html"
             % paths.display_path(OUT, ROOT))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
