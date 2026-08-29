#!/usr/bin/env python3
"""Rank a deck's content motions, so `--motion-density` selects the same ones every build.

    python tools/deck/density.py list  <deck>
    python tools/deck/density.py check <deck>
    python tools/deck/density.py write <deck> [-o out.html]

**Density is a budget and the budget has to be spent the same way twice** (T-112). A deck that
animated different elements each time it was built could not be reviewed, could not be diffed, and
would fail the byte-for-byte discipline this repository runs everywhere else. So the selection is
not drawn - it is **derived from the deck**, and this tool is the derivation.

**The rule, in one line.** Order every element carrying a content motion by `(tier, slide, document
order)`, then give the *i*th of *n* the rank `floor((i-1)/n*100)+1`; a content motion runs when
`--motion-density >= --m-rank`. The first element in the order therefore always carries rank 1 and
runs at any density above 0, and at 100 every one of them runs. Nothing here reads a clock or an
unseeded random, so `check` can recompute the whole set and say whether the deck's own numbers are
the ones the rule produces - which is a stronger claim than diffing two builds, because it holds
against a deck nobody rebuilt.

**Tier is what the motion is about, and it answers the question T-112 left open** - *what density 10
selects first when a slide has several eligible elements*. The argument's key figure before its
decoration: a pulse is DS-147's one emphasis on the number the slide is about, so it is tier 1 and
survives to the lowest density that runs anything at all.

**Affordance motion is not here.** It is not governed by density (DS-237), so it has no rank and a
rank written on one is a defect this tool reports.

Pure standard library (**L-07**).
"""

import io
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content                                                      # noqa: E402

import paths                                                        # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

RULE = "DS-239"

# **The tier table orders the content motions; it no longer decides which ones there are**
# (`PR-44`). It used to be both, and the denominator was therefore the list rather than the deck:
# [T-187](../../tasks/T-187-open-the-motion-vocabulary-into-a-style-guide.md) opened DS-140's
# vocabulary on 2026-08-21, so a conformant motion may now carry a name no table holds - it would
# get no rank, run at every density, and DS-239's row would still have read *0 of n*. What the
# deck contains is now read off the `--motion-kind` declarations, which is the idiom
# [T-214](../../tasks/T-214-ds-142s-checker-is-an-allow-list-of-one-class-name.md) restored twenty
# lines further down this same file for DS-237 and DS-238.
#
# A derived class the table does not name still ranks - after every class it does, because the
# table is an order and an unnamed motion has no place in it yet. Adding a row here moves it.
CONTENT_CLASSES = [
    ("pulse", 1, "DS-147's one emphasis pulse on the number the slide is about - the argument's "
                 "key figure, so it outranks everything decorative"),
    ("arrow-pop", 2, "the arrowheads of one figure, scaling out of their lines. About the diagram's "
                     "direction, which is the argument's shape rather than its headline number"),
    ("dot-pop", 3, "a matrix of marks arriving one at a time. The most decorative of the three, so "
                   "it is the first to go as density falls"),
]

# `AFFORDANCE_CLASSES` was here and was read by nothing in the tree - a second list of names, dead
# since it was written. Half of `PR-44`'s subject was therefore a deletion rather than a re-binding.

SLIDE = re.compile(r'<section[^>]*\bclass="[^"]*\bslide\b[^"]*"[^>]*>', re.I)
TAG = re.compile(r'<(\w+)([^>]*\bclass="([^"]*)"[^>]*)>')
RANK_ATTR = re.compile(r'--m-rank:\s*(\d+)')
DP_ATTR = re.compile(r'--dp:\s*(\d+)')
CIRCLE = re.compile(r'<circle\b[^>]*>')
# The slash that closes an SVG element, and the whitespace a formatter may have put before it. A
# tag ending `/>` has no attribute space at its last character, which is the assumption `set_var`
# used to make.
SELF_CLOSING = re.compile(r'\s*/\s*>$')
FIG_OPEN = re.compile(r'<svg\b[^>]*\bclass="[^"]*\bdot-pop\b[^"]*"[^>]*>')

# **The scramble, and why a number rather than a shuffle.** A matrix whose dots arrive left
# to right reads as a progress bar; one that arrives in no order reads as arrival. `random()`
# is not a thing a deck may contain (DS-239), so the order is a permutation anyone can
# recompute: 7 is coprime with the counts a matrix comes in, so `(i * 7) % n` visits every
# position exactly once rather than most of them.
DOT_STEP = 7


# The class a motion rule ranks: the RIGHTMOST compound that bears a class. `.pulse` gives `pulse`,
# `.arrow-pop marker path` gives `arrow-pop` and `.dot-pop circle` gives `dot-pop` - in both of the
# last two the animation runs on an inner ELEMENT and the ranked thing is the figure that carries
# the class. It reads a scoped rule the same way: `:where(.slide[data-played]) .pulse` is still
# `pulse`, which is the construction the adopter's `020` asked DS-229 to accept.
CLASS_TOKEN = re.compile(r"\.([A-Za-z_][\w-]*)")
PSEUDO_FN = re.compile(r":(?:where|is|matches|any)\s*\(")


def ranked_classes(selector):
    """The class names the rightmost class-bearing compound of `selector` carries."""
    out = []
    for branch in selector.split(","):
        # A functional pseudo-class is a bracket around part of the chain, not a step in it.
        flat = PSEUDO_FN.sub(" ", branch).replace(")", " ")
        for compound in reversed(flat.split()):
            names = CLASS_TOKEN.findall(compound)
            if names:
                out.extend(names)
                break
    return out


def content_classes(html):
    """`{class: tier}` - the content-motion vocabulary THIS deck declares.

    The denominator is the deck (`PR-44`). `CONTENT_CLASSES` supplies the order for the classes it
    names and nothing else; a declared class it does not name sorts after all of them.
    """
    named = dict((c, t) for c, t, _why in CONTENT_CLASSES)
    unnamed_tier = len(CONTENT_CLASSES) + 1
    out = {}
    for sel, _body, kind in motion_rules(html):
        if kind != "content":
            continue
        for c in ranked_classes(sel):
            out[c] = named.get(c, unnamed_tier)
    return out


def slide_bounds(html):
    """`[(start, end, name)]` for every slide section, in document order."""
    out = []
    # Comments blanked, not deleted: the bounds below are offsets into the string the CALLER holds
    # (T-191, and see `content.strip_comments`).
    for m in SLIDE.finditer(content.strip_comments(html, keep_length=True)):
        end = html.find("</section>", m.end())
        name = re.search(r'data-name="([^"]*)"', m.group(0))
        out.append((m.start(), end if end > 0 else len(html), name.group(1) if name else ""))
    return out


def classes(attr_class):
    return attr_class.split()


def eligible(html):
    """Every element carrying a content motion, in ranking order.

    Returns `[(pos, tag_start, tag_end, classes, tier, slide_index, slide_name)]`. `pos` is the
    element's place in the ranking order, 1-based.
    """
    tiers = content_classes(html)
    bounds = slide_bounds(html)
    found = []
    for m in TAG.finditer(html):
        cls = classes(m.group(3))
        hit = [c for c in cls if c in tiers]
        if not hit:
            continue
        tier = min(tiers[c] for c in hit)
        idx, name = None, ""
        for i, (a, b, nm) in enumerate(bounds):
            if a <= m.start() < b:
                idx, name = i, nm
                break
        if idx is None:
            # Outside every slide: the chrome and the reading view. A content motion there is not
            # part of the argument, so it is not ranked and `check` says so rather than ranking it.
            continue
        found.append([0, m.start(), m.end(), cls, tier, idx, name])
    found.sort(key=lambda r: (r[4], r[5], r[1]))
    for i, row in enumerate(found, start=1):
        row[0] = i
    return found


def dot_place(i, n):
    """Where the `i`th dot of `n` sits in the arrival order. 0-based both ends."""
    return (i * DOT_STEP) % n if n else 0


def dot_figures(html):
    """`[(fig_start, fig_end, [(circle_start, circle_end)])]` for every `dot-pop` figure."""
    out = []
    for m in FIG_OPEN.finditer(html):
        end = html.find("</svg>", m.end())
        if end < 0:
            continue
        body = html[m.end():end]
        circles = [(m.end() + c.start(), m.end() + c.end()) for c in CIRCLE.finditer(body)]
        out.append((m.start(), end, circles))
    return out


def rank_for(pos, total):
    """The rank of the `pos`th of `total`. The first is always 1, so a deck's leading moment runs
    at any density above 0; the last is at most 100, so density 100 runs everything."""
    if total <= 0:
        return None
    return int((pos - 1) * 100 // total) + 1


def wanted(html):
    """`{tag_start: rank}` - what the rule says this deck's ranks are."""
    rows = eligible(html)
    n = len(rows)
    return dict((r[1], rank_for(r[0], n)) for r in rows), rows


def declared(html, start, end):
    m = RANK_ATTR.search(html[start:end])
    return int(m.group(1)) if m else None


def set_var(tag, name, value):
    """The tag with one custom property set, merged into an existing `style=` or added as a new one.

    Merging rather than replacing is the whole of it: a risen element already carries `--i`, its
    stagger index, and a writer that replaced the attribute would drop it - silently, because the
    element still animates and only its timing is wrong.

    **The new attribute goes before the tag's closing punctuation, which is not always one
    character** (T-254). `<circle ... />` closes on `/>`, and inserting before the final `>` alone
    put the attribute outside the element: `<circle ... /  style="--dp:0">`. The browser reparents
    the broken subtree, and what the gate then reports is `DS-035` failing three untouched labels
    at `0.0 du` - a rule that names neither this tool nor the tag it damaged.
    """
    pat = re.compile(re.escape(name) + r":\s*[^;\"]*")
    if pat.search(tag):
        return pat.sub("%s:%s" % (name, value), tag, count=1)
    m = re.search(r'style="([^"]*)"', tag)
    if m:
        val = m.group(1).rstrip().rstrip(";")
        joined = ("%s;%s:%s" % (val, name, value)) if val else "%s:%s" % (name, value)
        return tag[:m.start(1)] + joined + tag[m.end(1):]
    close = SELF_CLOSING.search(tag)
    cut = close.start() if close else len(tag) - 1
    return tag[:cut].rstrip() + ' style="%s:%s"' % (name, value) + tag[cut:]


def written_ok(before, after, name):
    """`set_var`'s post-condition, or the reason it was broken - what `write` refuses to save on.

    Stated as what must still be true of the tag rather than as the shape of the one defect T-254
    found: a guard that recognises only the bug it was written for reports green on the next one.
    An edit here changes an attribute's text and nothing else, so the element, the way it closes
    and the fact that it is a single tag all survive it.
    """
    b, a = re.match(r"<(\w+)", before), re.match(r"<(\w+)", after)
    if not a or not b or a.group(1) != b.group(1):
        return "the element name changed"
    if bool(SELF_CLOSING.search(before)) != bool(SELF_CLOSING.search(after)):
        return "the tag stopped closing the way it did - the attribute landed outside the element"
    if not after.endswith(">") or "<" in after[1:] or ">" in after[:-1]:
        return "the edit produced something that is not one tag"
    if after.count('"') % 2:
        return "an unbalanced quote"
    if not re.search(re.escape(name) + r":\s*[^;\"]", after):
        return "%s is not in the tag that was written" % name
    return None


def set_rank(tag, rank):
    """The tag with `--m-rank` set."""
    return set_var(tag, "--m-rank", rank)


def stray_ranks(html):
    """Ranks written on something that carries no content motion - a rank that governs nothing."""
    out, tiers = [], content_classes(html)
    for m in TAG.finditer(html):
        if not RANK_ATTR.search(m.group(0)):
            continue
        cls = classes(m.group(3))
        if not any(c in tiers for c in cls):
            out.append((m.group(1), " ".join(cls)[:48]))
    return out


def report(deck):
    """`(problems, rows, ranks)` - everything wrong with this deck's ranking."""
    html = io.open(deck, encoding="utf-8").read()
    ranks, rows = wanted(html)
    problems = []
    for r in rows:
        want = ranks[r[1]]
        got = declared(html, r[1], r[2])
        if got is None:
            problems.append("slide %d %s: carries %s and no --m-rank, so it is ranked 101 by the "
                            "root default and never runs at any density"
                            % (r[5] + 1, r[6][:30],
                               "/".join(c for c in r[3] if c in content_classes(html))))
        elif got != want:
            problems.append("slide %d %s: --m-rank is %d, the rule gives %d"
                            % (r[5] + 1, r[6][:30], got, want))
    for _fs, _fe, circles in dot_figures(html):
        n = len(circles)
        for i, (cs, ce) in enumerate(circles):
            want = dot_place(i, n)
            m = DP_ATTR.search(html[cs:ce])
            got = int(m.group(1)) if m else None
            if got != want:
                problems.append("a dot-pop dot carries --dp %s where the derivation gives %d; the "
                                "arrival order is not reproducible" % (got, want))
                break
    for tag, cls in stray_ranks(html):
        problems.append("<%s class=\"%s\"> carries --m-rank and no content motion, so the rank "
                        "governs nothing" % (tag, cls))
    return problems, rows, ranks


def verdicts(deck):
    """`DS-239`'s row - `[(rule, what, ok)]`, the shape `check.py` gathers.

    **A prohibition, and the denominator is what makes it one.** *No content motion is ranked
    against the rule* has the deck's content motions as its subject, so a deck with none passes
    honestly - and *0 wrong of 0* and *0 wrong of 8* are the same boolean and not the same fact
    (**L-36**), so the count travels in the text.
    """
    if not deck:
        return [(RULE, "no deck to read - the density ranking gate has no subject", False)]
    try:
        problems, rows, _ranks = report(deck)
    except (OSError, UnicodeDecodeError) as exc:
        return [(RULE, "could not read the deck: %s" % exc, False)]
    detail = "" if not problems else " - " + "; ".join(problems[:3])
    return [(RULE, "content motions whose --m-rank is not what the rule derives: %d of %d%s"
             % (len(problems), len(rows), detail), not problems)]


# ---------------------------------------------------------------- DS-237 and DS-238, statically
# **A rule that starts a motion is one that names an animation or a transition property.** A rule
# that *stops* one - `animation:none`, `transition:none` - is not starting anything and owes no
# declaration; requiring one there would put `--motion-kind` on every reduced-motion and print
# collapse in the stylesheet, where it would say nothing.
CSS_RULE = re.compile(r"([^{}/][^{}]*)\{([^{}]*)\}", re.S)
STARTS = re.compile(r"(?:^|;|\s)(animation|animation-name|transition|transition-property)\s*:", re.M)
KIND = re.compile(r"--motion-kind\s*:\s*(content|affordance)\b")


# A CSS comment is not part of a selector, and `CSS_RULE` cannot tell the difference: the text
# between one rule's `}` and the next rule's `{` includes any comment written there, so a commented
# rule arrived with the comment glued to the head of its selector. **7 of the reference deck's 14
# motion rules were affected**, two of the three content ones among them. Nothing had failed,
# because DS-237 and DS-238 only ask whether a KIND is declared - but a vocabulary derived from
# those selectors would have been derived from prose, and DS-237's diagnostic was printing 44
# characters of comment where it means to name a selector.
CSS_COMMENT = re.compile(r"/\*.*?\*/", re.S)


def css_of(html):
    """Every `<style>` body in the document, joined, with CSS comments removed.

    The deck carries its CSS inline. Comments go because everything downstream reads the text
    between braces AS a selector.
    """
    return CSS_COMMENT.sub(" ", "\n".join(
        re.findall(r"<style[^>]*>(.*?)</style>", html, re.S | re.I)))


BANG_IMPORTANT = "!important"


def switched_off(value):
    """`animation:` / `transition:` value that starts nothing.

    **`rstrip` takes a character SET, not a suffix**, and this test used to read
    `.rstrip("!important")`. `"pop"` is three characters all of which are in `"!important"`, so it
    stripped to the empty string, `"" in ("none", "")` was true, and a rule reading
    `animation:pop 1s` was classified as one switching motion OFF - dropped from the motion set
    entirely, taking its `--motion-kind` declaration with it. Nothing in the tree animates a name
    that spells out of those nine letters today, which is why it had never fired; found while
    deriving DS-239's vocabulary from this function, where a dropped rule is a dropped class.
    """
    first = value.strip().split()[0]
    if first.endswith(BANG_IMPORTANT):
        first = first[:-len(BANG_IMPORTANT)]
    return first.strip() in ("none", "")


def motion_rules(html):
    """`[(selector, body, kind)]` for every rule that starts a motion. `kind` may be `None`."""
    out = []
    for m in CSS_RULE.finditer(css_of(html)):
        sel, body = m.group(1).strip(), m.group(2)
        if sel.startswith("@") or not STARTS.search(body):
            continue
        # a rule whose every motion declaration is `none` is switching motion off, not starting it
        live = re.findall(r"(?:animation|animation-name|transition|transition-property)\s*:\s*([^;]*)",
                          body)
        if all(switched_off(v) for v in live if v.strip()):
            continue
        k = KIND.search(body)
        out.append((sel, body, k.group(1) if k else None))
    return out


def kind_verdicts(html):
    """DS-237 and DS-238's rows, from the markup alone.

    **Two claims, two rows, and each prints its own denominator** (**L-36**): *0 undeclared of 0*
    and *0 undeclared of 8* are the same boolean and not the same fact, and a document with no
    stylesheet must not read as one whose motions were classified.
    """
    rules = motion_rules(html)
    missing = [sel for sel, _b, k in rules if k is None]
    rows = [("DS-237", "motion rules declaring neither content nor affordance: %d of %d%s"
             % (len(missing), len(rules),
                "" if not missing else " - " + "; ".join(s[:44] for s in missing[:3])),
             not missing)]

    # DS-238: a content motion is gated on `--m-on`; an affordance motion never is. Static, because
    # the gate is visible in the rule that carries it and a render would only say the same thing
    # more slowly.
    wrong = []
    for sel, body, k in rules:
        gated = "--m-on" in body
        if k == "content" and not gated:
            wrong.append("%s is content and its duration is not gated on --m-on" % sel[:40])
        elif k == "affordance" and gated:
            wrong.append("%s is affordance and density reaches it" % sel[:40])
    rows.append(("DS-238", "motions governed by the wrong half of the split: %d of %d%s"
                 % (len(wrong), len(rules),
                    "" if not wrong else " - " + "; ".join(wrong[:3])),
                 not wrong))
    return rows


def self_test():
    """The arithmetic, and the two ways of reading it wrongly (**L-04**)."""
    if rank_for(1, 1) != 1:
        sys.exit("SELF-TEST FAILED: the only content motion in a deck must rank 1. A deck with one "
                 "moment and a default density has to show it")
    if rank_for(1, 10) != 1 or rank_for(10, 10) != 91:
        sys.exit("SELF-TEST FAILED: ten motions must span 1..91, so density 100 runs all of them "
                 "and density 10 runs the first")
    if rank_for(2, 10) <= 10:
        sys.exit("SELF-TEST FAILED: the second of ten ranked inside the default density. Density 10 "
                 "is meant to be a small number of moments, not most of them")
    if rank_for(1, 0) is not None:
        sys.exit("SELF-TEST FAILED: a deck with no content motion produced a rank")
    # **Order is tier first, then the slide, then the document** - and the fixture asserts it in a
    # deck where document order and tier order disagree, which is the only case that can catch it.
    # **The fixture carries the stylesheet, because the vocabulary comes from it** (`PR-44`). The
    # markup alone used to be enough: three class names were compiled in, so a `<p class="pulse">`
    # was a content motion by spelling. It is one here because a rule says so, and the same fixture
    # now asserts the derivation as well as the order.
    STYLE = ('<style>.pulse{animation:pulse 900ms ease both;--motion-kind:content}'
             '.slide[data-played] .rise{animation:rise 300ms ease both;--motion-kind:affordance}'
             '</style>')
    html = (STYLE
            + '<section class="slide" data-name="one"><p class="rise">a</p></section>'
            '<section class="slide" data-name="two"><p class="stat-figure pulse">b</p></section>')
    rows = eligible(html)
    if len(rows) != 1 or rows[0][6] != "two":
        sys.exit("SELF-TEST FAILED: `eligible` did not find exactly the pulse on slide two - it "
                 "found %r. A rise is affordance motion and must not be ranked" % (rows,))
    if content_classes(html) != {"pulse": 1}:
        sys.exit("SELF-TEST FAILED: the vocabulary was not derived from the deck's declarations - "
                 "it came out as %r. `rise` is declared `affordance` and must not be in it"
                 % (content_classes(html),))

    # **A content motion the tier table does not name is still ranked** - the failure `PR-44`
    # predicts, and the one a compiled-in list cannot pass. It sorts after every named tier.
    opened = (STYLE.replace("</style>", '.swell{animation:swell 400ms ease both;'
                                        '--motion-kind:content}</style>')
              + '<section class="slide" data-name="one"><p class="swell">a</p>'
              '<p class="pulse">b</p></section>')
    voc = content_classes(opened)
    if "swell" not in voc or voc["swell"] <= voc["pulse"]:
        sys.exit("SELF-TEST FAILED: a declared content motion the tier table does not name was "
                 "dropped or out-ranked a named one - the vocabulary came out as %r. T-187 opened "
                 "DS-140's names, so a conformant motion may carry one no table holds" % (voc,))
    got = [r[3] for r in eligible(opened)]
    if len(got) != 2 or "pulse" not in got[0][0:] and "pulse" not in got[0]:
        sys.exit("SELF-TEST FAILED: the opened vocabulary did not rank both motions - %r" % (got,))

    # `css_of` strips comments, or a commented rule arrives with the comment as its selector.
    commented = "<style>/* a note about .pulse */\n.dot-pop circle{animation:pop 1s;" \
                "--motion-kind:content}</style>"
    if sorted(content_classes(commented)) != ["dot-pop"]:
        sys.exit("SELF-TEST FAILED: a comment above a rule reached the selector - the vocabulary "
                 "came out as %r" % (sorted(content_classes(commented)),))
    tag = '<p class="stat-figure pulse">'
    if set_rank(tag, 7) != '<p class="stat-figure pulse" style="--m-rank:7">':
        sys.exit("SELF-TEST FAILED: a rank was not added to a tag with no style attribute")
    tag = '<p class="safeguard rise pulse" style="--i:1">'
    if set_rank(tag, 51) != '<p class="safeguard rise pulse" style="--i:1;--m-rank:51">':
        sys.exit("SELF-TEST FAILED: a rank did not merge into an existing style attribute - it "
                 "replaced it, which would drop the stagger index beside it")
    if set_rank('<p class="pulse" style="--m-rank:3">', 9) != '<p class="pulse" style="--m-rank:3">'.replace("3", "9"):
        sys.exit("SELF-TEST FAILED: an existing rank was not replaced in place")

    # ---- DS-237 and DS-238's fixtures ---------------------------------------------------------
    css = ("<style>"
           ".a{animation:rise 300ms ease both;--motion-kind:affordance}"
           ".b{animation:pulse 900ms ease 1 both;--m-on:1;animation-duration:calc(var(--m-on)*1s);"
           "--motion-kind:content}"
           ".c{transition:transform 200ms ease}"
           ".d{animation:none;transition:none}"
           "</style>")
    rules = motion_rules(css)
    sels = sorted(s for s, _b, _k in rules)
    if sels != [".a", ".b", ".c"]:
        sys.exit("SELF-TEST FAILED: the motion rules found were %r. `.d` switches motion OFF and "
                 "owes no declaration; requiring one there would put a kind on every reduced-motion "
                 "collapse in the stylesheet" % (sels,))
    got = dict((r[0], (r[1], r[2])) for r in kind_verdicts(css))
    if got["DS-237"][1] or "1 of 3" not in got["DS-237"][0]:
        sys.exit("SELF-TEST FAILED: an undeclared motion rule passed DS-237, or the row lost its "
                 "denominator: %r" % (got["DS-237"],))
    if not got["DS-238"][1]:
        sys.exit("SELF-TEST FAILED: DS-238 failed a fixture where content is gated and affordance "
                 "is not: %r" % (got["DS-238"],))
    bad = css.replace(".a{animation:rise 300ms ease both;--motion-kind:affordance}",
                      ".a{animation:rise 300ms ease both;animation-duration:calc(var(--m-on)*1s);"
                      "--motion-kind:affordance}")
    got = dict((r[0], (r[1], r[2])) for r in kind_verdicts(bad))
    if got["DS-238"][1]:
        sys.exit("SELF-TEST FAILED: an affordance motion gated on --m-on passed DS-238. Density "
                 "reaching an affordance motion is the one thing the split exists to prevent")
    # **A `rstrip` that took a character set rather than a suffix.** `animation:pop` classified as
    # `animation:none`, so the rule left the motion set and its `--motion-kind` left with it.
    if switched_off("pop 1s") or switched_off("swell 400ms ease both"):
        sys.exit("SELF-TEST FAILED: a live animation was read as one switching motion off. Its "
                 "rule would leave the motion set and take its --motion-kind declaration with it")
    if not switched_off("none") or not switched_off("none!important"):
        sys.exit("SELF-TEST FAILED: `animation:none` was not recognised as switching motion off")
    if kind_verdicts("")[0][2] is not True or "of 0" not in kind_verdicts("")[0][1]:
        sys.exit("SELF-TEST FAILED: a document with no stylesheet either failed DS-237 or reported "
                 "no denominator - and *0 of 0* must not read like *0 of 8* (**L-36**)")

    # ---- the dot order --------------------------------------------------------------------------
    places = sorted(dot_place(i, 36) for i in range(36))
    if places != list(range(36)):
        sys.exit("SELF-TEST FAILED: the dot order is not a permutation of 36 - it visits %d of them. "
                 "A step that shares a factor with the count lands twice on some dots and never on "
                 "others, and the matrix would arrive with holes in it" % len(set(places)))
    if dot_place(1, 36) == 1:
        sys.exit("SELF-TEST FAILED: dot 1 arrives first, so the matrix sweeps in document order and "
                 "reads as a progress bar rather than as arrival")
    if set_var('<circle class="quiet-s" cx="1">', "--dp", 4) != '<circle class="quiet-s" cx="1" style="--dp:4">':
        sys.exit("SELF-TEST FAILED: --dp was not added to a circle with no style attribute")
    if set_var('<p style="--i:1;--m-rank:3">', "--m-rank", 9) != '<p style="--i:1;--m-rank:9">':
        sys.exit("SELF-TEST FAILED: setting one custom property disturbed another beside it")

    # ---- the self-closing tag (T-254) -----------------------------------------------------------
    # Every circle in a `dot-pop` figure is one, so this is the ordinary case rather than an edge.
    for tag, want in [('<circle class="quiet-s" cx="1"/>',
                       '<circle class="quiet-s" cx="1" style="--dp:4"/>'),
                      ('<circle class="quiet-s" cx="1" />',
                       '<circle class="quiet-s" cx="1" style="--dp:4" />'),
                      ('<circle class="quiet-s" style="--i:1" r="2"/>',
                       '<circle class="quiet-s" style="--i:1;--dp:4" r="2"/>')]:
        got = set_var(tag, "--dp", 4)
        if got != want:
            sys.exit("SELF-TEST FAILED: --dp was written outside the element. %r became %r, wanted "
                     "%r. The attribute lands after the closing slash, the browser reparents the "
                     "subtree, and DS-035 reports the damage on text nobody touched" %
                     (tag, got, want))
        if written_ok(tag, got, "--dp") is not None:
            sys.exit("SELF-TEST FAILED: `written_ok` refused a correct edit of %r" % (tag,))
    # The other direction (**L-125**): the insertion this task replaced must be caught, not merely
    # absent. `write` refuses to save on exactly this verdict.
    broke = '<circle class="quiet-s" cx="1"/ style="--dp:4">'
    if written_ok('<circle class="quiet-s" cx="1"/>', broke, "--dp") is None:
        sys.exit("SELF-TEST FAILED: `written_ok` passed a tag whose attribute is outside the "
                 "element - %r. A guard that cannot fail cannot protect the deliverable" % broke)
    if written_ok('<p class="pulse">', '<p class="pulse" style="--i:1">', "--dp") is None:
        sys.exit("SELF-TEST FAILED: `written_ok` passed an edit that did not set the property it "
                 "was asked for")
    return True


def main(argv):
    if len(argv) < 2:
        print(__doc__.strip())
        return 2
    self_test()
    cmd, deck = argv[0], argv[1]
    if cmd == "list":
        problems, rows, ranks = report(deck)
        print("%s - %d content motion(s)" % (paths.display_path(deck, ROOT), len(rows)))
        html = io.open(deck, encoding="utf-8").read()
        for r in rows:
            print("  rank %3d  tier %d  slide %2d  %-34s %s"
                  % (ranks[r[1]], r[4], r[5] + 1, r[6][:34],
                     " ".join(c for c in r[3])[:40]))
        if not rows:
            print("  none. Every motion in this deck is affordance motion, which density does not "
                  "govern (DS-237).")
        return 0
    if cmd == "check":
        problems, rows, ranks = report(deck)
        # **Print the rank the rule derives, per motion.** The gate already knows it, and the
        # adopter's `021` is what printing it costs when it does not: `--m-rank` is derived from
        # the SET, so removing two of five content motions leaves the other three wrong with
        # nothing in the edit touching them. Read as a list of ranks that is one line; read by
        # bisection it was an afternoon.
        for r in rows:
            print("  slide %2d  %-30s %-22s rank %3d derived%s"
                  % (r[5] + 1, r[6][:30], " ".join(r[3])[:22], ranks[r[1]],
                     "" if declared(io.open(deck, encoding="utf-8").read(), r[1], r[2])
                     == ranks[r[1]] else "  <- the deck does not carry this"))
        for p in problems:
            print("  %s" % p)
        print("%s - %d content motion(s), %d wrong"
              % (paths.display_path(deck, ROOT), len(rows), len(problems)))
        return 1 if problems else 0
    if cmd == "write":
        html = io.open(deck, encoding="utf-8").read()
        ranks, rows = wanted(html)
        bad = []

        def kept(tag, new, name):
            """One edit, held to `set_var`'s post-condition before it goes into the document."""
            why = written_ok(tag, new, name)
            if why:
                bad.append((why, tag, new))
            return new

        for r in sorted(rows, key=lambda x: -x[1]):
            tag = html[r[1]:r[2]]
            html = html[:r[1]] + kept(tag, set_rank(tag, ranks[r[1]]), "--m-rank") + html[r[2]:]
        for _fs, _fe, circles in sorted(dot_figures(html), key=lambda f: -f[0]):
            n = len(circles)
            for i, (cs, ce) in reversed(list(enumerate(circles))):
                tag = html[cs:ce]
                html = html[:cs] + kept(tag, set_var(tag, "--dp", dot_place(i, n)), "--dp") + html[ce:]
        # **Nothing is saved until every tag this run wrote still parses as the tag it was.** The
        # defect T-254 fixed wrote invalid markup into the deliverable and the gate then reported
        # it under an unrelated rule, so the run that caused the damage is the only cheap place to
        # catch it (adopter record 015, item 2).
        if bad:
            print("REFUSED to write %s - %d tag(s) came out malformed"
                  % (paths.display_path(deck, ROOT), len(bad)))
            for why, before, after in bad:
                print("  %s\n      was  %s\n      now  %s" % (why, before[:96], after[:96]))
            return 1
        out = deck
        if "-o" in argv:
            out = argv[argv.index("-o") + 1]
        with io.open(out, "w", encoding="utf-8", newline="") as fh:
            fh.write(html)
        print("wrote %s - %d content motion(s) ranked"
              % (paths.display_path(out, ROOT), len(rows)))
        return 0
    sys.exit("usage: density.py list|check|write <deck>")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
