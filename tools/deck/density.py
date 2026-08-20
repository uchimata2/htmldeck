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

# **The content-motion vocabulary, with the tier that orders it.** Adding a content motion adds a
# row here, and the ordering rule does not change - which is the point of a table rather than a
# sort key spread through the code. Affordance motions are deliberately absent: they are not
# ranked, and `check` fails a rank found on one.
CONTENT_CLASSES = [
    ("pulse", 1, "DS-147's one emphasis pulse on the number the slide is about - the argument's "
                 "key figure, so it outranks everything decorative"),
    ("arrow-pop", 2, "the arrowheads of one figure, scaling out of their lines. About the diagram's "
                     "direction, which is the argument's shape rather than its headline number"),
    ("dot-pop", 3, "a matrix of marks arriving one at a time. The most decorative of the three, so "
                   "it is the first to go as density falls"),
]

AFFORDANCE_CLASSES = ["rise", "current", "opening"]

SLIDE = re.compile(r'<section[^>]*\bclass="[^"]*\bslide\b[^"]*"[^>]*>', re.I)
TAG = re.compile(r'<(\w+)([^>]*\bclass="([^"]*)"[^>]*)>')
RANK_ATTR = re.compile(r'--m-rank:\s*(\d+)')
DP_ATTR = re.compile(r'--dp:\s*(\d+)')
CIRCLE = re.compile(r'<circle\b[^>]*>')
FIG_OPEN = re.compile(r'<svg\b[^>]*\bclass="[^"]*\bdot-pop\b[^"]*"[^>]*>')

# **The scramble, and why a number rather than a shuffle.** A matrix whose dots arrive left
# to right reads as a progress bar; one that arrives in no order reads as arrival. `random()`
# is not a thing a deck may contain (DS-239), so the order is a permutation anyone can
# recompute: 7 is coprime with the counts a matrix comes in, so `(i * 7) % n` visits every
# position exactly once rather than most of them.
DOT_STEP = 7


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
    tiers = dict((c, t) for c, t, _why in CONTENT_CLASSES)
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
    """
    pat = re.compile(re.escape(name) + r":\s*[^;\"]*")
    if pat.search(tag):
        return pat.sub("%s:%s" % (name, value), tag, count=1)
    m = re.search(r'style="([^"]*)"', tag)
    if m:
        val = m.group(1).rstrip().rstrip(";")
        joined = ("%s;%s:%s" % (val, name, value)) if val else "%s:%s" % (name, value)
        return tag[:m.start(1)] + joined + tag[m.end(1):]
    return tag[:-1] + ' style="%s:%s"' % (name, value) + tag[-1]


def set_rank(tag, rank):
    """The tag with `--m-rank` set."""
    return set_var(tag, "--m-rank", rank)


def stray_ranks(html):
    """Ranks written on something that carries no content motion - a rank that governs nothing."""
    out = []
    for m in TAG.finditer(html):
        if not RANK_ATTR.search(m.group(0)):
            continue
        cls = classes(m.group(3))
        if not any(c in dict((c, t) for c, t, _w in CONTENT_CLASSES) for c in cls):
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
                            % (r[5] + 1, r[6][:30], "/".join(c for c in r[3] if c in
                                                             dict((c2, t) for c2, t, _w in CONTENT_CLASSES))))
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


def css_of(html):
    """Every `<style>` body in the document, joined. The deck carries its CSS inline."""
    return "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S | re.I))


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
        if all(v.strip().split()[0].rstrip("!important").strip() in ("none", "") for v in live if v.strip()):
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
    html = ('<section class="slide" data-name="one"><p class="rise">a</p></section>'
            '<section class="slide" data-name="two"><p class="stat-figure pulse">b</p></section>')
    rows = eligible(html)
    if len(rows) != 1 or rows[0][6] != "two":
        sys.exit("SELF-TEST FAILED: `eligible` did not find exactly the pulse on slide two - it "
                 "found %r. A rise is affordance motion and must not be ranked" % (rows,))
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
        problems, rows, _ = report(deck)
        for p in problems:
            print("  %s" % p)
        print("%s - %d content motion(s), %d wrong"
              % (paths.display_path(deck, ROOT), len(rows), len(problems)))
        return 1 if problems else 0
    if cmd == "write":
        html = io.open(deck, encoding="utf-8").read()
        ranks, rows = wanted(html)
        for r in sorted(rows, key=lambda x: -x[1]):
            tag = html[r[1]:r[2]]
            html = html[:r[1]] + set_rank(tag, ranks[r[1]]) + html[r[2]:]
        for _fs, _fe, circles in sorted(dot_figures(html), key=lambda f: -f[0]):
            n = len(circles)
            for i, (cs, ce) in reversed(list(enumerate(circles))):
                tag = html[cs:ce]
                html = html[:cs] + set_var(tag, "--dp", dot_place(i, n)) + html[ce:]
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
