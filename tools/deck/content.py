#!/usr/bin/env python3
"""The content half — the figure ledger, and the three reconciliations over it.

**A deck can pass every presentation check and still put a wrong number in front of a board.** The
evidence is in `docs/BRIEF.md`: a five-document set where every document passed its own review, and
the figure that reached the board's decision cell was wrong in eight places. Nothing on the
presentation list would have caught it, and nothing here would have caught the rest.

**These checks do not cite DS-102, and the reason matters.** DS-102 — *no fabricated metrics; every
figure sourced* — is `judge`, and it is judge because deciding whether a figure is fabricated needs
someone to read the source and think. What a program can do is narrower and worth having: compare
the numbers on the slides against the numbers in the files they came from, and against each other.
So these carry their own IDs, `FIG-1` to `FIG-3`, the way §7's criteria do. Citing DS-102 for them
would be the defect T-038 spent a whole task sweeping out of `audit.py`.

**The matching is a heuristic and says so.** A figure is recognised by shape, and a label by the
words around it, so a source that phrases a quantity differently from the slide will read as
unsourced. That direction is the safe one: it over-reports rather than passing a wrong number.

    python tools/deck/content.py examples/reference-deck.html examples/sources

Pure standard library (**L-07**).
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

# A figure is a quantity a reader would repeat: money, a count, a percentage, a duration. A bare
# small integer is not - "3 corridors" is a figure and "3" inside `translate(0,3)` is geometry, so
# the number has to carry a currency mark, a separator, a decimal, a magnitude or a unit word.
#
# **A time word may also come BEFORE its numeral, and only a time word** (T-169). `Month 4`,
# `week 2`, `day 30` is how a plan states a date, and it is ordinary copy on a slide and in the
# documents a deck is built from - but the pattern read numeral-then-unit and nothing else, so a
# whole class of figure was never offered for binding, on EITHER side. The measured case: five
# source documents state a stop-or-go gate at month 4 three times over, and carried not one figure
# of kind `month` between them. That is a silent under-report, which is the direction the docstring
# above says these checks do not fail in.
#
# It is the time words alone because they are the only ones that stay a QUANTITY when reversed.
# `Route 3` and `Phase 1` name a thing rather than measure one, and admitting them fills every
# ledger with identifiers a reader would never repeat as a number.
TIME_UNITS = r"minutes?|mins?|hours?|days?|weeks?|months?|years?"

# **The unit vocabulary is two things and used to be one** (`PR-45`). The shape-based half below
# is domain-free - a proportion, a duration, an SI length - and belongs to every deck. The other
# half was the reference deck's transit domain written out as nouns: *stations, routes, riders,
# trips, people, buses, corridors, stops*. `examples/sort-window/` states *9 miles*, *14 miles*,
# *6 miles* and *14 nights* on its slides and none of them was a figure, because `miles` and
# `nights` are not in that list - and its `FIG-1` row read *figures on a slide that appear in no
# source: 0 of 73*. A silent under-report, which is the direction this module's own docstring says
# these checks do not fail in.
#
# **Enlarging the list is the answer this argues against**: a list of nouns is one deck's domain
# however long it grows, and the next adopter's domain is not in it. So the domain half is DERIVED
# from the pair being compared - any word the SOURCES use beside a numeral is a unit word for this
# deck - which is the shape the pattern already used for currency and separators.
SHAPE_UNITS = r"%|per cent|percent|" + TIME_UNITS + r"|km|m\b"

# The transit nouns are kept as the vocabulary of LAST resort - what `FIGURE` reads when there are
# no sources to derive from, which is every reader outside the ledger (DS-231 compares a bottom
# line against the slide faces, and both sides are the deck). They no longer decide the ledger's
# denominator, which is what `PR-45` is about.
FALLBACK_UNITS = r"stations?|routes?|riders?|trips?|people|buses|corridors?|stops?"
UNITS = SHAPE_UNITS + r"|" + FALLBACK_UNITS


def figure_pattern(units):
    """The figure pattern over `units`, an alternation of unit words."""
    return re.compile(FIGURE_SHAPE % {"time": TIME_UNITS, "units": units}, re.I)


# **The numeral may not END in a comma**, or the deriver reads a list separator as part of the
# number and takes the next word as its unit. `18, against 22` minted `against` as a unit word
# for the whole run, and `380 against` and `430 against` then became figures the reference deck
# does not state - reported as unsourced, which sends a reader to look for something nobody
# wrote. `38,000` is unaffected: its commas sit between digits.
NUMERAL_THEN_WORD = re.compile(
    r"(?<![\w.$:])\d(?:[\d,]*\d)?(?:\.\d+)?\s?([A-Za-z][A-Za-z-]{1,19})\b")


def units_from(text):
    """Every word `text` uses immediately after a numeral, as an alternation - or `""`.

    **The vocabulary comes from the documents being compared, not from a table** (`PR-45`). A word
    a source writes beside a number is a unit word for this pair by demonstration, which is the
    same evidence the reader on the slide would use. Stop words are excluded because *4 and*,
    *2 of* and *30 per* are grammar rather than measurement, and the hyphen is allowed because
    *9 miles-per-hour* is one word to a reader.
    """
    words = set()
    for m in NUMERAL_THEN_WORD.finditer(text):
        w = m.group(1).lower().rstrip("-")
        if w and w not in STOP and w not in FUNCTION_WORDS and not w.isdigit():
            words.add(w)
    return "|".join(re.escape(w) for w in sorted(words, key=lambda x: (-len(x), x)))


FIGURE_SHAPE = (
    r"(?<![\w.$:])((?:%(time)s)[\s-]\d+(?:,\d{3})*(?:\.\d+)?|"  # month 4, Month 4, month-4
    r"\$\s?\d[\d,]*(?:\.\d+)?\s?[MKB]?|"                      # $5.6M, $1.5M
    r"\d[\d,]*\.\d+\s?[MKB]?|"                                # 6.8, 4.1M
    r"\d{1,3}(?:,\d{3})+|"                                    # 38,000
    r"\d+\s?[MKB]\b|"                                         # 5M
    # **The unit word must not run on into a hyphenated compound.** Without the guard,
    # `month-4 stop-or-go gate` bound the numeral to `stop` out of the compound and minted
    # `4 stop` - a figure the slide does not state, reported as unsourced rather than as not a
    # figure, sending a reader to look for something nobody wrote (T-169).
    #
    # **A word character and not just a hyphen** (T-171). This was first written `(?![-\w])`,
    # narrowed to `(?!-)` because it cost a real figure, and restored once the thing it was paying
    # for was fixed: `runs()` used to DELETE an inline tag, so `<span>The other 5%</span><span>The
    # 02:30 ...` arrived as `5%The` and the wider guard correctly read that as a compound. It now
    # arrives as `5% The`. The narrow form let `4 stopover` mint `4 stop` - the same shape of
    # phantom the compound guard exists to stop, one character to the left.
    r"\d+\s?(?:%(units)s)(?![-\w]))")

# The default pattern: the shape forms plus the fallback nouns. Every reader that has no sources to
# derive from uses this - `audit.py`'s DS-231 among them, where both sides of the comparison are
# the deck.
FIGURE = figure_pattern(UNITS)

STOP = set(("the a an of in on for and or to is are was with by at from that this it its as "
            "be but not no than then so under over into per one two").split())

# **The open class is derived; the closed class is listed - and that is the whole distinction**
# (`PR-45`). Unit nouns are an OPEN class: *stations*, *riders*, *miles*, *nights*, and the next
# adopter's word is not in any list however long it grows, which is why `units_from` reads them off
# the sources instead. English function words are a CLOSED class - finite, domain-free, and the
# same set for every deck - so listing them is not the failure that listing nouns is.
#
# The words below are the ones that can stand immediately after a numeral without measuring it.
# The measured cases: `Phase 2 cannot start early` minted `cannot` as a unit and then `5 cannot`
# as a figure the deck does not state; `18, against 22` did the same with `against`. The module's
# own comment above already states the principle for the numeral's other side - *`Route 3` and
# `Phase 1` name a thing rather than measure one* - and this is that principle one word to the
# right.
FUNCTION_WORDS = set((
    "cannot can will would should could must may might shall need dare "
    "does do did done has have had having "
    "more most less least fewer other others another each every both all any some none "
    "further again also only just even still yet already almost about "
    "out up down off before after during while because since until unless although though "
    "against across within without between through above below near along around beyond behind "
    "toward towards onto upon via plus minus times who which what when where why how "
    "we they he she you i us them him her our their your my its his hers "
    "new old same such these those there here").split())


# **The reversed form is turned round in one place, and every reader of a figure uses it** (T-169).
# `normalise` needs it to key the ledger; `audit.magnitude` needs it to reduce a cited figure to its
# number, and without it `month 18` reduced to the whole string, matched no number on the slide
# face, and DS-231 reported the reference deck citing a figure it shows three times. Two copies of
# this is the failure the `QUICK_VIEW` comment below describes, in the place where it is hardest to
# see: the second reader is in another module and fails on a different rule.
REVERSED = re.compile(r"^(" + TIME_UNITS + r")[\s-]+(\d.*)$", re.I)


def unreverse(value):
    """`month-4` and `Month 4` become `4 month`. Anything else is returned unchanged."""
    m = REVERSED.match(value.strip())
    return (m.group(2) + " " + m.group(1)) if m else value


def normalise(value):
    """`$5.6M`, `$5.6 M` and `5.6M` are one figure. Case, spacing and the currency mark are
    presentation; the magnitude is the figure.

    **Word order is presentation too** (T-169): `month 4`, `Month 4`, `month-4` and `4 months` are
    one figure, so the reversed form is turned round before anything else. Without this the two
    orderings normalise to two different values and never meet - and `kind` returns `""` for one of
    them, so `build_ledger` would filter the pair out before a label was ever compared.
    """
    v = unreverse(value).lower().replace(",", "").replace("$", "").replace(" ", "")
    m = re.match(r"^([\d.]+)([mkb])?(.*)$", v)
    if not m:
        return v
    num, mag, rest = m.group(1), m.group(2) or "", m.group(3) or ""
    num = num.rstrip(".")
    if "." in num:
        num = num.rstrip("0").rstrip(".")
    rest = re.sub(r"s$", "", rest)                    # months / month
    rest = {"min": "minute", "mins": "minute", "yr": "year"}.get(rest, rest)
    return num + mag + rest


def label_of(context, value):
    """The words a figure is about, taken from its own sentence with the figure removed. Kept as a
    SET of significant words rather than a phrase, because a source rarely repeats a slide's word
    order and comparing phrases would report every match as a miss."""
    text = context.replace(value, " ")
    words = [w for w in re.findall(r"[A-Za-z][A-Za-z-]+", text.lower())
             if w not in STOP and len(w) > 2]
    return words[:12]


# Inline tags carry emphasis inside one run of prose; everything else starts a new one. The split
# matters more than it looks: `<b>$5.6M</b> · the whole grant` is one figure with a label, and
# `<text class="lab">2,000</text>` beside `<text class="lab">4,000</text>` is a scale. Reading the
# whole slide as one string merged the second into the first and produced axis gridlines with
# borrowed labels - and `Route 3` next to `Route 7` came back as the figure "3 Route".
INLINE = re.compile(r"</?(?:b|strong|i|em|span|small|sup|sub|a|code|u|mark|tspan)\b[^>]*>", re.I)

# **The quick view is where a quoted source lives** (T-070). The distinction is between what a deck
# MAKES and what it QUOTES, and it is decidable by position rather than by intent: a raster inside
# `template.qv-src` or `.qv-body` is a source, and a raster anywhere else is a rasterised diagram -
# as much a defect after the amendment as before it. Cut narrowly and by container, in the shape
# DS-001's provenance exemption was cut in T-069: the exemption goes exactly as far as the container
# that earns it.
#
# **It lives here rather than in `audit.py`, which is where it was written**, because T-167 gave it
# a second caller and `audit.py` already imports this module - so this is the one direction that
# holds one definition. Two copies of this regex is the failure the shell exists to prevent, in a
# smaller place.
QUICK_VIEW = re.compile(r'<template class="qv-src"[^>]*>.*?</template>'
                        r'|<div class="qv-body"[^>]*>.*?</div>', re.S | re.I)


def strip_comments(html, keep_length=False):
    """The document with every HTML comment removed, and it is run **before** slides are split.

    **A comment can open a phantom slide, and the shell's own scaffold comment did** (T-191). Four
    tools here split a deck with a regex over `<section ... class="slide" ...>`, and
    `shell.py new` wrote

        <!-- slides go here, one <section class="slide"> each (COMPONENT-CONTRACT.md 3.2) -->

    at the insertion point. The pattern matched the tag **inside the comment**, so the comment
    became a slide running to the first real `</section>` - and `runs()` below, which does strip
    comments, could not help: it sees the fragment *after* the split, by which point the opening
    `<!--` has been consumed and there is nothing left to strip. What came out was `3.2` reported
    under `FIG-1` as a figure on slide 1 appearing in no source, **on a string the shell wrote**.

    So the order is the fix, not the regex: comments stop being markup before anything looks for
    markup. The four callers keep their own patterns, which genuinely differ - `density.py` wants
    the opening tag alone - and share this one fact about what a comment is.

    **`keep_length` blanks each comment instead of deleting it**, so every offset after it is the
    offset it was. `density.py` returns `(start, end)` pairs its callers slice the ORIGINAL string
    with; deleting bytes there would leave the slide bounds pointing a little further left with
    every comment passed, which is a worse defect than the one being fixed and a silent one.
    """
    if keep_length:
        return re.sub(r"<!--.*?-->", lambda m: " " * len(m.group(0)), html, flags=re.S)
    return re.sub(r"<!--.*?-->", " ", html, flags=re.S)


def runs(fragment):
    """The text runs of a fragment, split at every non-inline tag.

    **An inline tag becomes a space, not nothing** (T-171). Deleting it glued the last word of one
    inline element to the first word of the next, which is exactly how a deck's key/value rows are
    written: `<span class="k">If it fails</span><span>Service holds ...` arrived as
    `failsService holds`, and `label_of` keyed it under `failsservice`. A label is a set of
    significant words and a glued word matches nothing, so two documents describing one figure in
    the same words failed to bind - invisibly, because a label full of `getnothing` looks like the
    approximate matching this module documents. The reverse risk is a figure written across a tag,
    `$<b>5.6M</b>` and `<b>5.6</b>M`; both patterns already allow one `\\s?` and `self_test` holds
    them to it.
    """
    frag = re.sub(r"<!--.*?-->", " ", fragment, flags=re.S)
    frag = re.sub(r"<(script|style)\b.*?</\1>", " ", frag, flags=re.S | re.I)
    frag = INLINE.sub(" ", frag)
    out = []
    for part in re.split(r"<[^>]+>", frag):
        t = re.sub(r"\s+", " ", part).replace("&nbsp;", " ").replace("&amp;", "&").strip()
        if t:
            out.append(t)
    return out


def deck_figures(deck, figure=None):
    """Every figure on a slide, with the slide it is on and the words around it.

    Read per `<section class="slide">` so *Used on* is a real answer rather than a guess.

    **A number alone in its own run is a mark on a scale, not a figure**, and it is dropped: an
    axis tick is not something a reader repeats or a board decides on, and requiring a source for
    one would make every chart unsourceable.

    **A figure inside a quick view is not a figure on the slide** (T-167). The quoted sources sit
    in the provenance mark, which is inside the `<section class="slide">` this reads, so they came
    in with it: on the first deck here whose sources were written elsewhere, **122 of the 152
    figures this returned were quotations**, and FIG-3 duly reported the deck contradicting itself
    every time a source's own table disagreed with the slide citing it. The source half of the
    ledger already reads those documents; counting them here as well compares a document with
    itself.
    """
    html = strip_comments(io.open(deck, encoding="utf-8").read())
    out = []
    for m in re.finditer(r'<section[^>]*class="[^"]*\bslide\b[^"]*"[^>]*>(.*?)</section>',
                         html, re.S | re.I):
        block = m.group(0)
        name = re.search(r'data-name="([^"]*)"', block)
        name = name.group(1) if name else "?"
        for run in runs(QUICK_VIEW.sub(" ", m.group(1))):
            for f in (figure or FIGURE).finditer(run):
                label = label_of(run, f.group(1))
                if not label:
                    continue
                out.append({"value": f.group(1).strip(), "norm": normalise(f.group(1)),
                            "slide": name, "label": label, "context": run[:110]})
    return out


def source_units(text):
    """A source read as units of meaning rather than as lines.

    **Line by line was wrong and quietly so.** A prose source wraps, so `16` and `stations` land on
    different lines and the figure is not there at all — the reference deck's `16 stations` read as
    unsourced against a file that says it. Paragraphs are joined; a markdown table row stays its
    own unit, because a whole table collapsed into one string gives every figure in it the same
    label and makes the disagreement check meaningless.
    """
    units = []
    for para in re.split(r"\n\s*\n", text):
        for unit in re.split(r"\n(?=\s*\|)", para):
            u = re.sub(r"\s+", " ", unit).strip()
            if u:
                units.append(u)
    return units


def source_figures(paths, figure=None):
    """Every figure in the supplied sources, with its unit as context. Text files are read as
    text; a source that is not one is reported rather than silently skipped."""
    out, files, skipped = [], [], []
    for path in paths:
        if os.path.splitext(path)[1].lower() not in (".md", ".txt", ".csv", ".markdown"):
            skipped.append(path)
            continue
        files.append(path)
        for unit in source_units(io.open(path, encoding="utf-8").read()):
            for f in (figure or FIGURE).finditer(unit):
                out.append({"value": f.group(1).strip(), "norm": normalise(f.group(1)),
                            "origin": os.path.basename(path),
                            "label": label_of(unit, f.group(1)), "context": unit[:110]})
    return out, files, skipped


def collect(sources):
    if os.path.isfile(sources):
        return [sources]
    found = []
    for base, _dirs, names in os.walk(sources):
        for n in sorted(names):
            found.append(os.path.join(base, n))
    return found


def overlap(a, b):
    """How many significant words two labels share."""
    return len(set(a) & set(b))


def similarity(a, b):
    """Jaccard over the two label sets. Overlap alone says two figures are discussed together;
    similarity says they are about **the same thing**, which is what a contradiction needs."""
    sa, sb = set(a), set(b)
    return len(sa & sb) / float(len(sa | sb)) if (sa or sb) else 0.0


def kind(norm):
    """The unit a figure is in, stripped of its magnitude. Two numbers in different units are not
    two answers to one question - `0 minutes` and `14,800 trips` were being compared."""
    return re.sub(r"^[\d.]+", "", norm)


def build_ledger(deck, sources):
    """The **Figure · Value · Origin · Used on** table `artifacts.md` specifies, emitted rather
    than kept internal — [T-004] prioritises what this one counts."""
    # **The vocabulary is derived from the sources, then both sides are read with it** (`PR-45`).
    # A word the sources use beside a numeral is a unit word for this pair, so the ledger's
    # denominator is what the documents state rather than what a table of nouns admits. The
    # fallback nouns stay in the alternation: dropping them would narrow a deck whose sources
    # happen not to spell one out, and this change is about widening.
    paths = collect(sources)
    derived = units_from("\n".join(
        io.open(f, encoding="utf-8", errors="replace").read() for f in paths
        if os.path.splitext(f)[1].lower() in (".md", ".txt", ".csv", ".markdown")))
    figure = figure_pattern(UNITS + ("|" + derived if derived else ""))
    figs = deck_figures(deck, figure)
    src, files, skipped = source_figures(paths, figure)
    by_norm = {}
    for s in src:
        by_norm.setdefault(s["norm"], []).append(s)

    rows, unsourced, disagreeing = [], [], []
    for f in figs:
        matches = by_norm.get(f["norm"], [])
        origin = matches[0]["origin"] if matches else None
        if not matches:
            # Does a source talk about this SUBJECT with a different number? That is the more
            # dangerous case and it is reported as a disagreement, not merely as unsourced.
            # **Same unit, or it is not a rival**: `0 minutes` and `14,800 trips` are not two
            # answers to one question, and matching on words alone said they were.
            rival = None
            for s in src:
                if kind(s["norm"]) != kind(f["norm"]):
                    continue
                if overlap(f["label"], s["label"]) >= 3:
                    rival = s
                    break
            if rival:
                disagreeing.append((f["slide"], f["value"], rival["value"], rival["origin"],
                                    rival["context"]))
            else:
                unsourced.append((f["slide"], f["value"], f["context"]))
        rows.append({"figure": " ".join(f["label"][:4]) or f["value"], "value": f["value"],
                     "origin": origin or "-", "usedOn": f["slide"]})

    # The same figure twice in the deck with different values, which is the failure that put a
    # wrong number in a board's decision cell. Three conditions, each of which had to be added
    # after the version without it fired on a conforming deck:
    #
    #  - **different slides.** A-07 draws the same diagram twice with one edge changed, so a
    #    before/after slide IS one subject with two values, by design. The cost: a contradiction
    #    inside one slide is not reported, and that is the trade taken.
    #  - **different runs**, so a sentence listing three quantities is not three contradictions.
    #  - **the same unit and a similar label**, not merely a shared word: `$4.1M of the grant` and
    #    `$6.8M a year from the general fund` share *general*, *fund* and *year* and are two facts.
    contradictions = []
    for i, a in enumerate(figs):
        for b in figs[i + 1:]:
            if a["norm"] == b["norm"] or a["slide"] == b["slide"]:
                continue
            if a["context"] == b["context"] or kind(a["norm"]) != kind(b["norm"]):
                continue
            if similarity(a["label"], b["label"]) >= 0.6:
                contradictions.append((a["slide"], a["value"], b["slide"], b["value"],
                                       " ".join(sorted(set(a["label"]) & set(b["label"])))))
    return {"rows": rows, "unsourced": unsourced, "disagreeing": disagreeing,
            "contradictions": contradictions, "sourceConflicts": source_conflicts(src),
            "sourceCount": len(files),
            "sourceFiles": [os.path.basename(f) for f in files],
            "skipped": [os.path.basename(s) for s in skipped],
            "deckFigures": len(figs), "sourceFigureCount": len(src)}


# How many significant words two source labels must share before the pair is worth reading. Three
# is what FIG-2 uses to find a rival; four is what this needs, and **the second corpus is why the
# number is not trusted further than that** (**L-45**).
#
# Measured at four, over both source sets in this repository and one deliberately contradicted copy:
#
#   examples/sort-window/sources   0 candidates   (clean, and it reports clean)
#   examples/sources               10 candidates  (clean, and all ten are false)
#   the contradicted copy          1 candidate    (the planted one, and only it)
#
# Ten false candidates on a clean corpus is the honest result, not a tuning failure: the reference
# deck's cost model writes denser prose, so more pairs share four words. No threshold removed them
# without also losing the true case, because what separates the two is semantics. That is the
# measurement behind this being a reading list rather than a verdict.
SUBJECT_WORDS = 4


def source_conflicts(src):
    """Two sources answering one question with two numbers - **before any deck exists.**

    The other three rows all need a deck: FIG-1 and FIG-2 compare a slide with its sources, FIG-3
    compares a slide with another slide. Nothing compared **two sources with each other**, and a
    deck inherits its material's disagreements whether or not it quotes both sides. The corpus case
    is not two files disagreeing but *a summary contradicting the table above it*, so a conflict
    inside one document counts and the pair need not span files.

    **These are candidates for a person, not a gate row, and that is a finding rather than a
    convenience.** Three thresholds were tried against two real pairs - a restatement that IS a
    contradiction (*busiest single day* at 31,900 in a table, 30,400 in a summary) and a pair that
    is NOT (*mean round utilisation, off-peak* at 71% against *peak* at 88%). Set equality of the
    labels misses the first, because a restatement rephrases. Jaccard at 0.6 misses it too, at 0.5.
    Every threshold loose enough to catch the true pair also catches the false one, because what
    separates them is that *peak* and *off-peak* are contrastive - which is semantics, not counting.

    So the deterministic half stops here: **same unit, three significant words in common, different
    values.** Whether the two phrasings are one question is the reading pass's call, and that is the
    2026-08-07 ruling applied rather than worked around - counting gates, judgement explains. Over-
    reporting is the safe direction when a person is the consumer (**L-48**); it would be the wrong
    direction for a row that blocks a build, which is exactly why this is not one.
    """
    out = []
    for i, a in enumerate(src):
        for b in src[i + 1:]:
            if a["norm"] == b["norm"] or a["context"] == b["context"]:
                continue
            if kind(a["norm"]) != kind(b["norm"]):
                continue
            if overlap(a["label"], b["label"]) >= SUBJECT_WORDS:
                out.append((a["origin"], a["value"], b["origin"], b["value"],
                            " ".join(sorted(set(a["label"]) & set(b["label"])))))
    return out


def audit(deck, sources):
    """`(ledger, rows)` in the shape every other stage returns."""
    L = build_ledger(deck, sources)
    # **Which figures, not how many** (T-169). A count says something failed and gives no way to
    # judge it without re-running the tool and reading the ledger. The one time that mattered, a
    # real defect in this module sat unraised for a session because `1 of 30` looked exactly like
    # the approximate matching the docstring above documents. The values cost one line and make the
    # next one decidable on sight; the cap keeps a badly-sourced deck from printing a page.
    named = "; ".join("%s [%s]" % (v, s) for s, v, _c in L["unsourced"][:6])
    if len(L["unsourced"]) > 6:
        named += "; +%d more" % (len(L["unsourced"]) - 6)
    rows = [
        ("FIG-1", "figures on a slide that appear in no source: %d of %d%s"
         % (len(L["unsourced"]), L["deckFigures"], (" - " + named) if named else ""),
         not L["unsourced"] and L["deckFigures"] > 0),
        ("FIG-2", "figures disagreeing with the source they came from: %d"
         % len(L["disagreeing"]), not L["disagreeing"]),
        ("FIG-3", "figures appearing twice in the deck with different values: %d"
         % len(L["contradictions"]), not L["contradictions"]),
    ]
    # FIG-4 is deliberately absent from this list. `source_conflicts` explains why: no threshold
    # separates a restatement that contradicts from a qualified pair that does not, so the pairs
    # are candidates a reviewer confirms and never a verdict that blocks a build.
    if L["skipped"]:
        rows.append(("FIG-0", "source files this reader cannot open: %d (%s)"
                     % (len(L["skipped"]), ", ".join(L["skipped"])), False))
    return L, rows


def self_test():
    """Known answers, on strings rather than files (**L-04**)."""
    if normalise("$5.6M") != normalise("5.6 m"):
        sys.exit("SELF-TEST FAILED: the currency mark and spacing changed a figure's identity")
    if normalise("38,000") != "38000":
        sys.exit("SELF-TEST FAILED: a thousands separator survived normalisation")
    if normalise("14 months") != normalise("14 month"):
        sys.exit("SELF-TEST FAILED: a plural changed a figure's identity")
    if normalise("4.10") != "4.1":
        sys.exit("SELF-TEST FAILED: a trailing zero changed a figure's identity")
    found = [m.group(1) for m in FIGURE.finditer("the $5.6M grant reaches 38,000 riders in "
                                                 "14 months, at 12 min headway")]
    if len(found) != 4:
        sys.exit("SELF-TEST FAILED: the figure pattern found %d of 4 in a known line: %s"
                 % (len(found), found))
    if FIGURE.search("translate(0,18)"):
        sys.exit("SELF-TEST FAILED: an SVG coordinate parsed as a figure")
    if overlap(label_of("the grant is $5.6M in total", "$5.6M"),
               label_of("a grant of $5.6M", "$5.6M")) < 1:
        sys.exit("SELF-TEST FAILED: two labels about one subject shared no significant word")

    # T-169, both halves in one line: the reversed figure is found, and the unit word inside the
    # compound beside it does not mint a second one. Before the fix this returned `['4 stop']`.
    if [m.group(1) for m in FIGURE.finditer("the month-4 stop-or-go gate")] != ["month-4"]:
        sys.exit("SELF-TEST FAILED: a hyphenated compound minted a figure, or a time word before "
                 "its numeral was not one")
    if [m.group(1) for m in FIGURE.finditer("| Set the gate | Month 4 |")] != ["Month 4"]:
        sys.exit("SELF-TEST FAILED: a time word before its numeral in a table cell is not a figure")
    if not FIGURE.search("4 stops on the route"):
        sys.exit("SELF-TEST FAILED: the compound guard rejected a unit word that ends the match")
    for form in ("month-4", "Month 4", "month 4"):
        if normalise(form) != normalise("4 months"):
            sys.exit("SELF-TEST FAILED: %r and '4 months' are not one figure" % form)
    if kind(normalise("Month 4")) != "month":
        sys.exit("SELF-TEST FAILED: a reversed figure carries no unit, so nothing can rival it")

    # T-171, both directions, on the two shapes the change trades between. Butting inline elements
    # must leave a word boundary; a figure written ACROSS an inline tag must survive the space that
    # boundary costs. The second is the risk the first creates, and it is asserted in both the
    # currency-first and the magnitude-last form.
    glued = runs('<span class="k">If it fails</span><span>Service holds the slot</span>')
    if glued != ["If it fails Service holds the slot"]:
        sys.exit("SELF-TEST FAILED: butting inline elements did not leave a word boundary: %s"
                 % glued)
    words = label_of(glued[0], "no-such-figure")
    if "service" not in words or "fails" not in words:
        sys.exit("SELF-TEST FAILED: a glued pair survived into a label: %s" % words)
    for markup, want in (('<p>$<b>5.6M</b> of the grant</p>', "5.6m"),
                         ('<p>the grant is <b>5.6</b>M in total</p>', "5.6m")):
        got = [normalise(m.group(1)) for r in runs(markup) for m in FIGURE.finditer(r)]
        if want not in got:
            sys.exit("SELF-TEST FAILED: a figure written across an inline tag was lost: %s -> %s"
                     % (markup, got))
    if FIGURE.search("4 stopover services"):
        sys.exit("SELF-TEST FAILED: a unit word running on into a longer word minted a figure")

    # FIG-4, both directions. The quoted figure is the case it exists for; the qualified pair is
    # the false positive that set its strictness, and it is a real row out of a real source file.
    def src_fig(origin, context, value):
        return {"origin": origin, "context": context, "value": value,
                "norm": normalise(value), "label": label_of(context, value)}

    restated = [src_fig("model.md", "busiest single day, 5 December, observed maximum", "31,900"),
                src_fig("pack.md", "the busiest single day, 5 December, reached 30,400 parcels",
                        "30,400")]
    if len(source_conflicts(restated)) != 1:
        sys.exit("SELF-TEST FAILED: FIG-4 missed a figure restated with a different value")

    units = [src_fig("model.md", "the notice window runs 8 weeks", "8 weeks"),
             src_fig("model.md", "the notice window runs 8 miles", "8 miles")]
    if source_conflicts(units):
        sys.exit("SELF-TEST FAILED: FIG-4 compared two different units")

    apart = [src_fig("model.md", "capital for nine vans", "$522k"),
             src_fig("model.md", "annual crew cost", "$170k")]
    if source_conflicts(apart):
        sys.exit("SELF-TEST FAILED: FIG-4 paired two figures about different subjects")
    return True


def main(deck, sources):
    self_test()
    L, rows = audit(deck, sources)
    print("deck:    %s" % paths.display_path(deck, ROOT))
    print("sources: %d file(s) - %s" % (L["sourceCount"], ", ".join(L["sourceFiles"]) or "none"))
    print("\n| Figure | Value | Origin | Used on |")
    print("| :--- | :--- | :--- | :--- |")
    for r in L["rows"]:
        print("| %s | %s | %s | %s |" % (r["figure"], r["value"], r["origin"], r["usedOn"]))
    print("\n%d figures on the slides, %d in the sources" % (L["deckFigures"],
                                                             L["sourceFigureCount"]))
    for rule, what, ok in rows:
        print("  %-6s %-62s %s" % (rule, what, "pass" if ok else "FAIL"))
    for slide, value, ctx in L["unsourced"][:12]:
        print("      unsourced  %-34s %-10s %s" % (slide[:34], value, ctx[:50]))
    for slide, value, was, origin, ctx in L["disagreeing"][:12]:
        print("      disagrees  %-34s %s vs %s in %s" % (slide[:34], value, was, origin))
    for sa, va, sb, vb, shared in L["contradictions"][:12]:
        print("      two values %s=%s / %s=%s  (%s)" % (sa[:20], va, sb[:20], vb, shared))
    if L["sourceConflicts"]:
        print("\n  FIG-4  source pairs to read - candidates, not verdicts: %d"
              % len(L["sourceConflicts"]))
        for oa, va, ob, vb, shared in L["sourceConflicts"][:12]:
            print("      %s=%s / %s=%s  (%s)" % (oa[:24], va, ob[:24], vb, shared))
    return 0 if all(ok for _r, _w, ok in rows) else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    sys.exit(main(os.path.abspath(a[0]), os.path.abspath(a[1])))
