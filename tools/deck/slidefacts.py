#!/usr/bin/env python3
"""Print what a slide actually contains, so a specification and its deck stop drifting silently.

    python tools/deck/slidefacts.py examples/sort-window/sort-window.html 4
    python tools/deck/slidefacts.py examples/sort-window/sort-window.html --all
    python tools/deck/slidefacts.py --self-test

A deck is built from a specification pair and then **edited in place**, which is the supported way
to work once a slide carries anything the build cannot reproduce. From that moment the entry in
`<slug>.slides.md` is a claim about the deck, and nothing checks it. An adopter swept theirs on
2026-08-27 and found **twenty-three of twenty-five entries had drifted**, with `check.py` green
throughout - the gate reads the deck, and the drift is between the deck and a second document
(T-259, adopter report `026`).

**This makes no judgement, and that is the design.** It prints one slide's own answer for every
field an entry claims; a reader decides whether the entry matches. A differ would produce noise on
every intentional difference and there are many - the entry is prose about a slide, not a
serialisation of one. The adopter's own version made the same choice and named it as the reason
theirs was usable.

Three things here are not obvious:

- **A `<template>`'s text is inside its slide's `<section>`.** Each quick-view source document
  ships as `<template class="qv-src">` within the slide that cites it, so a printer reading the
  section whole answers for the slide with the documents it links to. Measured on slide 4 of
  `examples/sort-window/sort-window.html`: 9,826 bytes raw against 4,056 with templates removed,
  so **59% of that section is payload belonging to another document**. Templates are cut first,
  before any field is read (**L-149**).
- **The motion vocabulary is the deck's, never a list kept here.** Which class names animate is
  read from the deck's own `--motion-kind` declarations through `density.motion_rules`, the same
  idiom `DS-239` uses. A copied list is a second home for the vocabulary and goes stale the first
  time a theme adds a class.
- **A browser buys nothing here.** Report `026` proposed reusing `render.py`'s parse; that parse is
  a Chrome DOM read. Every field an entry claims is in the static markup, so this is standard
  library (**L-07**) and costs no launch.

Slides are located by `density.slide_bounds`, which reads the deck's own declared sections rather
than counting - a deck shipping a colophon outside the run cannot shift every answer by one.
"""

import html as html_lib
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import density                                                      # noqa: E402
import content                                                      # noqa: E402

TEMPLATE = re.compile(r"<template\b[^>]*>.*?</template>", re.S | re.I)
TAG = re.compile(r"<[^>]+>")
CLASS_ATTR = re.compile(r'\bclass="([^"]*)"')
OPEN_TAG = re.compile(r"<(\w+)(\s[^>]*)?>")
ATTR = re.compile(r'([\w:-]+)\s*=\s*(?:"([^"]*)"|\'([^\']*)\')')
# The elements HTML never closes, so none of them opens a depth.
VOID = frozenset(("area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
                  "param", "source", "track", "wbr"))
# The roles that make an element a control a reader operates (report `10`).
CONTROL_ROLES = ("button", "tab", "switch")


def unescape(text):
    """Every named and numeric HTML entity, through the standard library.

    This was a six-entry table until 2026-08-30 - `&amp;`, `&lt;`, `&gt;`, `&quot;`, `&#39;`,
    `&nbsp;` - on the reasoning that a deck writes no others. It writes plenty: the title slide of
    `examples/measure-first/measure-first.html` alone carries `&middot;` and `&rsquo;`, and both
    reached the printed output as literal text and were counted as words by
    [`readability.py`](readability.py). A hand-kept table of *the ones we use* is a second home for
    a list the standard library already owns.
    """
    return html_lib.unescape(text)


def flatten(fragment):
    """Visible text of `fragment`, tags removed, runs joined by single spaces."""
    return " ".join(unescape(TAG.sub(" ", fragment)).split())


def without_templates(section):
    """`section` with every `<template>` replaced by nothing.

    This is the first thing done to any slide markup here. See the module docstring: the quick-view
    payload is the majority of some sections, and it is another document's text.
    """
    return TEMPLATE.sub(" ", section)


def close_of(section, tag, start):
    """Where the `tag` element whose open tag ends at `start` closes, or the end of `section`.

    **At its own close tag, not at the first one** (T-303). This was `section.find("</div>")` until
    2026-09-14, so a `.body` whose first child is a `<div>` ended at that child, and every sibling
    after it was dropped with no marker (report `13`). Opens of the same tag are counted, and the
    close is the one where the depth returns to zero. A void element opens no depth.
    """
    if tag.lower() in VOID:
        return start
    depth = 1
    for m in re.compile(r"<(/?)%s(?=[\s/>])[^>]*>" % re.escape(tag), re.I).finditer(section, start):
        if m.group(1):
            depth -= 1
            if not depth:
                return m.start()
        elif not m.group(0).endswith("/>"):
            depth += 1
    return len(section)


def svg_spans(section):
    """`[(start, end)]` of every outermost `<svg>`, each closed at its own `</svg>`.

    `<svg\\b.*?</svg>` is the first-close defect in a second helper: it ended a figure at the first
    icon nested inside it, so the reference deck's sources slide printed a figure's labels as body
    copy and none as drawn labels. `readability.py`'s ledger found it on its first run (T-303).
    """
    out, pos = [], 0
    opener = re.compile(r"<svg(?=[\s/>])[^>]*>", re.I)
    while True:
        m = opener.search(section, pos)
        if not m:
            return out
        if m.group(0).endswith("/>"):
            end = m.end()
        else:
            close = close_of(section, "svg", m.end())
            end = section.find(">", close) + 1 if close < len(section) else len(section)
        out.append((m.start(), end))
        pos = end


def without_svg(section):
    """`section` with every `<svg>` replaced by a space."""
    parts, pos = [], 0
    for start, end in svg_spans(section):
        parts += [section[pos:start], " "]
        pos = end
    return "".join(parts) + section[pos:]


def attributes(fragment):
    """`{name: value}` for an open tag's attribute text, names lower-cased and values unescaped."""
    return {m.group(1).lower(): unescape(m.group(2) if m.group(2) is not None else m.group(3))
            for m in ATTR.finditer(fragment or "")}


def by_class(section, name):
    """Every element carrying class `name`, flattened, in document order.

    Matches the class as a whole token, so `.body` does not answer for `.bottom-line` and `.name`
    does not answer for `.sources-item`.
    """
    out = []
    token = re.compile(r"(?:^|\s)%s(?:\s|$)" % re.escape(name))
    for m in re.finditer(r"<(\w+)([^>]*\bclass=\"[^\"]*\"[^>]*)>", section):
        attrs = m.group(2)
        cls = CLASS_ATTR.search(attrs)
        if not cls or not token.search(cls.group(1)):
            continue
        text = flatten(section[m.end():close_of(section, m.group(1), m.end())])
        if text:
            out.append(text)
    return out


def drawn_labels(section):
    """Text drawn inside an `<svg>` - the labels a `Visuals` line describes.

    Kept separate from body copy because the two fail differently: prose drifts when somebody
    rewrites it, a drawn label drifts when the chart behind it is rebuilt.
    """
    out = []
    for start, end in svg_spans(section):
        for m in re.finditer(r"<text\b[^>]*>(.*?)</text>", section[start:end], re.S | re.I):
            text = flatten(m.group(1))
            if text:
                out.append(text)
    return out


def reachable(tabindex):
    """True for a `tabindex` a keyboard reaches. Below zero is focusable by script only."""
    try:
        return tabindex is not None and int(tabindex.strip()) >= 0
    except ValueError:
        return False


def accessible_name(section, m, attrs):
    """`aria-label`, else the element's own text, else `title`, else empty.

    `aria-labelledby` is not resolved: the id it names can sit on another slide, and a name read
    from the wrong element is worse than an empty one, which the report prints as missing.
    """
    if attrs.get("aria-label", "").strip():
        return attrs["aria-label"].strip()
    if not m.group(0).endswith("/>"):
        inner = section[m.end():close_of(section, m.group(1), m.end())]
        text = flatten(without_svg(inner))
        if text:
            return text
    return attrs.get("title", "").strip()


def controls(section):
    """`[(kind, name, label)]` - every interactive control the slide carries, in document order.

    `data-disc` is the disclosure's own name and is what a specification entry quotes. **Every other
    control is read from the accessibility contract, not from a class name** (T-303): a `<button>`,
    an element whose `role` is `button`, `tab` or `switch`, and an element a keyboard reaches through
    `tabindex`, SVG included, each with its accessible name. This read `data-disc` alone until
    2026-09-14, so a slide's own buttons printed *the slide carries none* (report `10`).

    **Each control is printed once, under the field that names it.** The first control inside a
    `[data-disc]` element is that disclosure's trigger, and a control carrying `data-qv` is under
    `Quick views`.
    """
    out, spans, labels = [], [], by_class(section, "disc-label")
    for m in OPEN_TAG.finditer(section):
        tag, attrs = m.group(1).lower(), attributes(m.group(2))
        if "data-disc" in attrs:
            n = sum(1 for kind, _n, _l in out if kind == "disclosure")
            out.append(("disclosure", attrs["data-disc"], labels[n] if n < len(labels) else ""))
            spans.append([m.end(), close_of(section, m.group(1), m.end()), False])
            continue
        role = attrs.get("role", "").strip().lower()
        if tag == "button":
            kind = "button"
        elif role in CONTROL_ROLES:
            kind = "role=" + role
        elif reachable(attrs.get("tabindex")):
            kind = "tabindex"
        else:
            continue
        trigger = next((s for s in spans if s[0] <= m.start() < s[1] and not s[2]), None)
        if trigger:
            trigger[2] = True
            continue
        if "data-qv" in attrs:
            continue
        out.append((kind, accessible_name(section, m, attrs), ""))
    return out


def quick_views(section):
    """`[(title, file)]` - every quick view the slide opens, by its control rather than its
    payload. The payload is a `<template>` and has been cut by the time this runs."""
    out = []
    for m in re.finditer(r'<button[^>]*\bdata-qv="([^"]*)"[^>]*\bdata-file="([^"]*)"', section):
        out.append((unescape(m.group(1)), unescape(m.group(2))))
    return out


def motion_vocabulary(html):
    """`{class: kind}` - every class name this deck animates, and whether it is content or
    affordance motion. Read from the deck's `--motion-kind` declarations, never listed here."""
    out = {}
    for sel, _body, kind in density.motion_rules(html):
        for name in density.ranked_classes(sel):
            # A class declared both ways keeps the content reading: that is the one a slide's
            # pacing depends on, and the one an entry's `Animations` line is about.
            if out.get(name) != "content":
                out[name] = kind or "undeclared"
    return out


def motion_on(section, vocabulary):
    """`[(class, kind)]` - the animated classes actually present on this slide, in the order the
    deck declares them, deduplicated."""
    present, seen = [], set()
    for m in CLASS_ATTR.finditer(section):
        for name in density.classes(m.group(1)):
            if name in vocabulary and name not in seen:
                seen.add(name)
                present.append((name, vocabulary[name]))
    return present


def facts(html, index):
    """Every field an entry claims, answered from slide `index` (1-based) of `html`."""
    bounds = density.slide_bounds(html)
    if not 1 <= index <= len(bounds):
        raise IndexError("the deck has %d slide(s); asked for %d" % (len(bounds), index))
    start, end, name = bounds[index - 1]
    section = without_templates(html[start:end])
    # Body copy is read with the SVG removed, because `drawn labels` already answers for it and a
    # figure normally sits inside a `.body` wrapper. Measured on slide 4 of
    # `examples/sort-window/sort-window.html`: without this the eleven chart labels are printed
    # twice, once as prose, and a reader holding the entry's `Text.` line against the deck reads
    # axis ticks as a paragraph. The two fields partition the slide's text; they do not overlap.
    prose = without_svg(section)
    return {
        "slide": index,
        "name": name,
        "eyebrow": by_class(section, "eyebrow"),
        "headline": by_class(section, "headline"),
        "standfirst": by_class(section, "standfirst"),
        "bottom line": by_class(section, "bottom-line"),
        "body copy": by_class(prose, "body"),
        "drawn labels": drawn_labels(section),
        "controls": controls(section),
        "motion classes": motion_on(section, motion_vocabulary(html)),
        "quick views": quick_views(section),
        "sources": by_class(section, "sources-item"),
    }


ORDER = ["eyebrow", "headline", "standfirst", "bottom line", "body copy", "drawn labels",
         "controls", "motion classes", "quick views", "sources"]

# The line printed where a slide carries nothing for a field. It says the slide was ASKED and
# answered nothing, which is the answer a reader needs when an entry claims the field: a blank
# would read as a printer that does not cover it.
ABSENT = "- (the slide carries none)"


def render_line(field, value):
    """One field's answer, as lines."""
    if field == "controls":
        return ["- %s %s%s" % (kind, repr(name) if name else "(no accessible name)",
                               (" - %r" % label) if label else "")
                for kind, name, label in value]
    if field == "motion classes":
        return ["- .%s (%s)" % (name, kind) for name, kind in value]
    if field == "quick views":
        return ["- %r -> %s" % (title, path) for title, path in value]
    return ["- %s" % v for v in value]


def report(html, index):
    """Slide `index`'s fact sheet, as text."""
    f = facts(html, index)
    out = ["Slide %d - %s" % (f["slide"], f["name"] or "(no data-name)"), ""]
    for field in ORDER:
        out.append("%s:" % field.capitalize() if field[0].islower() else "%s:" % field)
        lines = render_line(field, f[field])
        out.extend(["  " + line for line in (lines or [ABSENT])])
        out.append("")
    return "\n".join(out).rstrip() + "\n"


# --- the self-test --------------------------------------------------------------------------

# One slide carrying every field once, plus the trap: a `<template>` holding text that would answer
# for four different fields if it were not cut.
FIXTURE = (
    '<style>.rise{animation:rise 300ms;--motion-kind:affordance}'
    '.current{animation:draw 2s;--motion-kind:content}</style>'
    '<section class="slide" data-name="A seasonal failure">'
    '<p class="eyebrow rise">Winter against summer</p>'
    '<h2 class="headline rise">The failure is seasonal</h2>'
    '<p class="standfirst rise">The same depot, six months apart.</p>'
    '<div class="body figwrap">'
    '<svg viewBox="0 0 10 10"><path class="current"/>'
    '<text class="val">9.8%</text><text class="lab">Nov</text></svg></div>'
    '<div class="disc" data-disc="scope"><span class="disc-label">What this line includes</span>'
    '</div>'
    '<p class="bottom-line rise">Four months sit under 3.4%.</p>'
    '<span class="sources-item">Throughput model'
    '<button class="sources-open" data-qv="Throughput model" data-file="throughput-model.md">'
    'open</button>'
    '<template class="qv-src" data-qv="Throughput model">'
    '<p class="eyebrow">PAYLOAD EYEBROW</p><h2 class="headline">PAYLOAD HEADLINE</h2>'
    '<text>PAYLOAD LABEL</text><p class="bottom-line">PAYLOAD BOTTOM LINE</p>'
    '</template></span>'
    '</section>')


def self_test():
    """Prove the printer in **both** directions (**L-125**): a field the slide carries is printed,
    and a field it does not carry says so. A printer only ever checked against a full slide cannot
    distinguish *the deck answers this* from *the printer never looks*."""
    f = facts(FIXTURE, 1)

    # --- direction one: what is there is printed, and attributed to the right field
    expected = {
        "eyebrow": ["Winter against summer"],
        "headline": ["The failure is seasonal"],
        "standfirst": ["The same depot, six months apart."],
        "bottom line": ["Four months sit under 3.4%."],
        "drawn labels": ["9.8%", "Nov"],
        "quick views": [("Throughput model", "throughput-model.md")],
        "controls": [("disclosure", "scope", "What this line includes")],
    }
    for field, want in expected.items():
        if f[field] != want:
            sys.exit("SELF-TEST FAILED: %s came out as %r, expected %r" % (field, f[field], want))
    if f["name"] != "A seasonal failure":
        sys.exit("SELF-TEST FAILED: the slide name came out as %r" % (f["name"],))
    if ("current", "content") not in f["motion classes"]:
        sys.exit("SELF-TEST FAILED: `.current` is declared content motion in the fixture's own CSS "
                 "and the slide carries it; the printer reported %r" % (f["motion classes"],))
    if ("rise", "affordance") not in f["motion classes"]:
        sys.exit("SELF-TEST FAILED: `.rise` is declared affordance motion and the slide carries "
                 "it; the printer reported %r" % (f["motion classes"],))

    # --- an entity is text, and every entity is, not a table of the ones somebody remembered
    entities = ('<section class="slide" data-name="e">'
                '<p class="body">Priya &middot; Partners&rsquo; meeting &amp; review</p></section>')
    got = facts(entities, 1)["body copy"]
    if got != ["Priya · Partners’ meeting & review"]:
        sys.exit("SELF-TEST FAILED: entities came out as %r. `&middot;` and `&rsquo;` are on the "
                 "title slide of a tracked deck, and an undecoded one is printed as literal text "
                 "and counted as a word by readability.py" % (got,))

    # --- an element closes at its OWN close tag (T-303, report `13`)
    nested = '<div class="body"><div class="a">FIRST</div><p>SECOND</p><p>THIRD</p></div>'
    if by_class(nested, "body") != ["FIRST SECOND THIRD"]:
        sys.exit("SELF-TEST FAILED: a `.body` whose first child is a <div> read as %r. It closed "
                 "at that child's tag, so every sibling after it went missing" %
                 (by_class(nested, "body"),))
    # The failing direction (**L-125**): the arithmetic this replaced, so the case is seen to
    # reproduce the defect rather than merely to pass.
    if flatten(nested[len('<div class="body">'):nested.find("</div>")]) != "FIRST":
        sys.exit("SELF-TEST FAILED: the nested fixture no longer reproduces the first-close defect, "
                 "so the assertion above proves nothing about it")
    if by_class('<p class="body">a<br>b<img src="x">c</p><p>d</p>', "body") != ["a b c"]:
        sys.exit("SELF-TEST FAILED: a void element inside a field opened a depth, so the field "
                 "ran past its own close")

    # --- an <svg> closes at its own </svg>, not at an icon nested inside it (T-303)
    iconed = ('<section class="slide" data-name="i"><div class="body"><svg class="fig">'
              '<svg class="icon"><use href="#i"/></svg><text class="name">After the icon</text>'
              '</svg><p>Prose.</p></div></section>')
    got = facts(iconed, 1)
    if got["drawn labels"] != ["After the icon"] or got["body copy"] != ["Prose."]:
        sys.exit("SELF-TEST FAILED: a figure holding an icon <svg> read as drawn labels %r and body "
                 "copy %r. It closed at the icon's </svg>, so its labels became prose"
                 % (got["drawn labels"], got["body copy"]))
    if "After the icon" not in flatten(re.sub(r"<svg\b.*?</svg>", " ", iconed, flags=re.S | re.I)):
        sys.exit("SELF-TEST FAILED: the icon fixture no longer reproduces the first-close defect, "
                 "so the assertion above proves nothing about it")

    # --- every control, once, under the field that names it (T-303, report `10`)
    ctl = ('<section class="slide" data-name="c">'
           '<div class="disc" data-disc="scope"><button class="disc-btn">Open</button>'
           '<span class="disc-label">What it covers</span></div>'
           '<button class="walkbtn" type="button">Next step</button>'
           '<svg viewBox="0 0 9 9"><rect tabindex="0" role="button" aria-label="Exact, 47 of 91"/>'
           '</svg><div role="tab">Winter</div><p tabindex="0" title="A focusable note"></p>'
           '<span tabindex="0"></span><h2 tabindex="-1">Not a control</h2>'
           '<button class="sources-open" data-qv="Model" data-file="m.md">open</button>'
           '</section>')
    want = [("disclosure", "scope", "What it covers"), ("button", "Next step", ""),
            ("role=button", "Exact, 47 of 91", ""), ("role=tab", "Winter", ""),
            ("tabindex", "A focusable note", ""), ("tabindex", "", "")]
    if facts(ctl, 1)["controls"] != want:
        sys.exit("SELF-TEST FAILED: the controls came out as %r, expected %r"
                 % (facts(ctl, 1)["controls"], want))
    if "(no accessible name)" not in report(ctl, 1):
        sys.exit("SELF-TEST FAILED: a control with no accessible name printed an empty quote "
                 "rather than saying it has none")
    if facts('<section class="slide" data-name="q"><p class="body">Prose.</p></section>',
             1)["controls"] != []:
        sys.exit("SELF-TEST FAILED: a slide with no control reported one")

    # --- the two text fields partition the slide, they do not overlap
    for label in f["drawn labels"]:
        for para in f["body copy"]:
            if label in para:
                sys.exit("SELF-TEST FAILED: the drawn label %r was also printed as body copy - "
                         "%r. A figure sits inside a `.body` wrapper, so the prose read must have "
                         "the SVG removed or every chart label is printed twice" % (label, para))

    # --- the trap: no field may be answered by the `<template>` payload
    for field in ORDER:
        flat = repr(f[field])
        if "PAYLOAD" in flat:
            sys.exit("SELF-TEST FAILED: %s was answered by the <template> payload - %r. A quick "
                     "view's source document sits inside the slide that cites it and must be cut "
                     "before any field is read" % (field, f[field]))

    # --- direction two: a field the slide does NOT carry says so, rather than going quiet
    stripped = FIXTURE.replace('<p class="standfirst rise">The same depot, six months apart.</p>',
                               "")
    g = facts(stripped, 1)
    if g["standfirst"] != []:
        sys.exit("SELF-TEST FAILED: the standfirst was removed from the fixture and the printer "
                 "still reported %r" % (g["standfirst"],))
    if ABSENT not in report(stripped, 1):
        sys.exit("SELF-TEST FAILED: a slide carrying no standfirst printed no %r line, so a reader "
                 "cannot tell an absent field from an unread one" % (ABSENT,))
    # and removing it must not disturb the fields around it
    if g["headline"] != f["headline"] or g["bottom line"] != f["bottom line"]:
        sys.exit("SELF-TEST FAILED: removing the standfirst changed a neighbouring field - "
                 "headline %r, bottom line %r" % (g["headline"], g["bottom line"]))

    # --- the section boundary: a second slide must not answer for the first
    two = FIXTURE + ('<section class="slide" data-name="second">'
                     '<h2 class="headline">SECOND HEADLINE</h2></section>')
    if facts(two, 1)["headline"] != ["The failure is seasonal"]:
        sys.exit("SELF-TEST FAILED: slide 1 answered with slide 2's headline")
    if facts(two, 2)["headline"] != ["SECOND HEADLINE"]:
        sys.exit("SELF-TEST FAILED: slide 2 came out as %r" % (facts(two, 2)["headline"],))


def main(argv):
    self_test()
    if not argv or argv[0] in ("--self-test", "-h", "--help"):
        if argv and argv[0] == "--self-test":
            print("self-test passed - the printer answers a present field, says so for an absent "
                  "one, and no field is answered by a <template> payload")
            return 0
        print(__doc__.strip().split("\n\n")[1].strip())
        return 0 if argv else 2

    deck = argv[0]
    html = content.strip_comments(open(deck, encoding="utf-8").read())
    total = len(density.slide_bounds(html))
    if len(argv) > 1 and argv[1] == "--all":
        wanted = range(1, total + 1)
    elif len(argv) > 1:
        wanted = [int(argv[1])]
    else:
        print("%s carries %d slide(s). Name one, or --all." % (deck, total))
        return 2

    print("%s - what the deck itself says. This makes no judgement: hold it against "
          "<slug>.slides.md yourself.\n" % deck)
    for i in wanted:
        print(report(html, i))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
