#!/usr/bin/env python3
"""Report how hard a deck's copy is to read, and name the hardest lines. It never gates.

    python tools/deck/readability.py examples/measure-first/measure-first.html
    python tools/deck/readability.py examples/measure-first/measure-first.html --lines 15
    python tools/deck/readability.py --self-test

The gate has two rules over copy and neither measures difficulty. `DS-092` measures **length** and
`DS-106` measures a **banned list**; both were green on a deck whose own author called it hard, and
the difficulty was vocabulary, noun stacks and abstraction (T-258, adopter report `025`).

**It reports and must never gate, and that is a decision rather than a missing feature.** A
threshold on prose invites writing to the threshold, and this instrument cannot tell a hard sentence
from a precise one - a slide that has to say *depreciation* says it. The record that asked for this
measured **Flesch 64.6, which reads as plain English, on the copy its reader found difficult**: the
aggregate agreed with nobody. What it did do was locate the lines. So the ranking below is the
output and the aggregate is context, not the other way round, and every exit code here is 0.

**The subject is the deck's contracted prose, decided by measurement.** Report `025` asked for *the
deck's own text nodes*; scored both ways on the four tracked decks, the two readings differ by **8
Flesch points on `measure-first`** - a reading grade - and the sign is not even constant, so it is
not an offset to correct for. An axis tick and a legend key are terse noun phrases with no verb and
no sentence end, and scoring them measures label style rather than reading. The words left out are
**counted and named** rather than dropped in silence (**L-149**). T-258 §2 carries the table.

Lines come from `slidefacts.facts`, so *what text is on a slide* has one implementation here and
this tool inherits its two cuts: the `<template>` payload of a quick view is another document's
prose, and drawn labels are partitioned away from body copy (**L-08**, **L-149**).

**What the numbers are, and are not.** Flesch, Flesch-Kincaid and Fog are syllable-and-length
formulas from the 1940s-60s. They cannot see whether a sentence is ambiguous, whether a claim
attaches to its subject, or whether a noun stack hides an actor. They are counted here because they
are cheap, reproducible and they rank - not because a score is a verdict. Pure standard library
(**L-07**).
"""

import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content                                                      # noqa: E402
import density                                                      # noqa: E402
import slidefacts                                                   # noqa: E402

# The prose fields, in the order a reader meets them. `drawn labels`, `controls`, `motion classes`,
# `quick views` and `sources` are deliberately not here - see the docstring.
PROSE_FIELDS = ["eyebrow", "headline", "standfirst", "body copy", "bottom line"]
COUNTED_OUT = ["drawn labels", "sources"]

VOWELS = "aeiouy"
WORD = re.compile(r"[A-Za-z][A-Za-z'’-]*")
SENTENCE_END = re.compile(r"(?<=[.!?])\s+")

# Fog excludes a word made three syllables by an inflection. The classical rule also excludes proper
# nouns and familiar compounds; neither is done here, because both need a list and a list is a
# second home for a judgement (`DS-106` spent a task on exactly that). Stated rather than implied.
INFLECTION = ("es", "ed", "ing")

# A nominalisation turns a verb or an adjective into a noun, which is where an actor goes missing:
# *the reconciliation of the variance* against *we reconciled the variance*. Report `025` counted
# **129** of them in the copy its reader found hard, so they are counted here beside the formulas.
# Suffix matching over-counts - `attention`, `moment`, `city` are not nominalisations - so the
# number is reported as a rate to compare against, never as a defect count.
NOMINAL = ("tion", "sion", "ment", "ance", "ence", "ity", "ness", "ism", "ancy", "ency")
NOMINAL_MIN = 6


def syllables(word):
    """Vowel-group count, with a silent trailing `e` removed. At least 1 for any word with a letter.

    A heuristic, and every readability formula in this file rests on it. It is wrong on `queue` (1,
    counted 2) and on `poem` (2, counted 1). It is consistent, which is what a ranking needs.
    """
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    n, prev_vowel = 0, False
    for ch in w:
        is_vowel = ch in VOWELS
        if is_vowel and not prev_vowel:
            n += 1
        prev_vowel = is_vowel
    if w.endswith("e") and n > 1 and not w.endswith(("le", "ee")):
        n -= 1
    return max(n, 1)


def complex_word(word):
    """Fog's `complex`: three or more syllables, not counting one an inflection added."""
    if syllables(word) < 3:
        return False
    low = word.lower()
    for suffix in INFLECTION:
        if low.endswith(suffix) and syllables(low[:-len(suffix)]) < 3:
            return False
    return True


def nominalisation(word):
    """A noun built from a verb or an adjective, by suffix. Over-counts; see `NOMINAL`."""
    low = re.sub(r"[^a-z]", "", word.lower())
    return len(low) >= NOMINAL_MIN and low.endswith(NOMINAL)


def sentences(text):
    """The sentences of `text`. A line with no terminator is one sentence, not zero - a headline
    ends without a full stop and still costs a reader one sentence's work."""
    parts = [s.strip() for s in SENTENCE_END.split(text) if s.strip()]
    return parts or ([text.strip()] if text.strip() else [])


def measure(text):
    """Flesch, Flesch-Kincaid, Fog, the three-syllable share and the nominalisation rate.

    `None` where there is nothing to measure, which is the answer rather than a zero: a slide with
    no prose has no reading difficulty, and `0.0` would sort it as the easiest copy in the deck.
    """
    words = WORD.findall(text)
    sents = sentences(text)
    if not words or not sents:
        return None
    syl = sum(syllables(w) for w in words)
    hard = sum(1 for w in words if complex_word(w))
    nominal = sum(1 for w in words if nominalisation(w))
    per_sentence = float(len(words)) / len(sents)
    per_word = float(syl) / len(words)
    return {
        "words": len(words),
        "sentences": len(sents),
        "flesch": 206.835 - 1.015 * per_sentence - 84.6 * per_word,
        "grade": 0.39 * per_sentence + 11.8 * per_word - 15.59,
        "fog": 0.4 * (per_sentence + 100.0 * hard / len(words)),
        "three_syllable": 100.0 * hard / len(words),
        "nominalisations": nominal,
        "nominal_rate": 100.0 * nominal / len(words),
    }


def lines_of(html):
    """`[(slide, field, text)]` - every prose line in the deck, in reading order.

    Through `slidefacts.facts`, so the `<template>` payload and the drawn labels are already
    handled there rather than a second time here.
    """
    out = []
    for i in range(1, len(density.slide_bounds(html)) + 1):
        facts = slidefacts.facts(html, i)
        for field in PROSE_FIELDS:
            for text in facts[field]:
                out.append((i, field, text))
    return out


def counted_out(html):
    """`(words, fields)` - the text this measurement does not read, so it is never silent about it."""
    words, fields = 0, {}
    for i in range(1, len(density.slide_bounds(html)) + 1):
        facts = slidefacts.facts(html, i)
        for field in COUNTED_OUT:
            n = sum(len(WORD.findall(t)) for t in facts[field])
            words += n
            fields[field] = fields.get(field, 0) + n
    return words, fields


# A line shorter than this is not ranked. Fog over four words is arithmetic on one sentence and puts
# a two-word eyebrow at the top of a list meant to name what to rewrite. Measured on the four
# tracked decks: at 8 the eyebrows leave the ranking and every entry is a sentence somebody wrote.
RANK_MIN_WORDS = 8


def hardest(lines, limit):
    """The `limit` hardest lines by Fog, longest first among ties. Short lines are not ranked."""
    scored = []
    for slide, field, text in lines:
        m = measure(text)
        if m and m["words"] >= RANK_MIN_WORDS:
            scored.append((m["fog"], m["words"], slide, field, text, m))
    scored.sort(key=lambda r: (-r[0], -r[1]))
    return scored[:limit]


def combined(lines):
    """One measurement over all the prose, as context for the ranking."""
    return measure(" ".join(text for _s, _f, text in lines))


def band(flesch):
    """The conventional Flesch band. A label, never a verdict - see the module docstring."""
    for edge, name in ((90, "very easy"), (80, "easy"), (70, "fairly easy"), (60, "plain"),
                       (50, "fairly hard"), (30, "hard")):
        if flesch >= edge:
            return name
    return "very hard"


def report(html, limit):
    """The whole account, as text."""
    lines = lines_of(html)
    whole = combined(lines)
    if not whole:
        return "No prose found. Nothing to measure, and that is not a pass.\n"

    out = ["Over %d line(s) of prose, %d word(s), %d sentence(s):"
           % (len(lines), whole["words"], whole["sentences"]), ""]
    out.append("  Flesch Reading Ease   %5.1f   (%s)" % (whole["flesch"], band(whole["flesch"])))
    out.append("  Flesch-Kincaid Grade  %5.1f" % whole["grade"])
    out.append("  Gunning Fog           %5.1f" % whole["fog"])
    out.append("  Three-syllable words  %5.1f%%" % whole["three_syllable"])
    out.append("  Nominalisations       %5d   (%.1f%% of words)"
               % (whole["nominalisations"], whole["nominal_rate"]))

    skipped, fields = counted_out(html)
    out += ["", "  Not read: %d word(s) - %s. A label is a noun phrase with no verb and no "
                "sentence end;" % (skipped, ", ".join("%s %d" % (f, n) for f, n in
                                                      sorted(fields.items()))),
            "  scoring one measures label style rather than reading (T-258 section 2)."]

    out += ["", "The hardest lines. This ranks them; it does not judge them - a slide that has to "
                "say", "`depreciation` says it.", ""]
    ranked = hardest(lines, limit)
    if not ranked:
        out.append("  (no line reaches %d words, the shortest this will rank)" % RANK_MIN_WORDS)
    for fog, words, slide, field, text, m in ranked:
        out.append("  Fog %4.1f  %2d words  %3.0f%% three-syllable   slide %d, %s"
                   % (fog, words, m["three_syllable"], slide, field))
        out.append("    %s" % (text if len(text) <= 150 else text[:147] + "..."))
    out += ["", "This measures syllables and length. It cannot see an ambiguous sentence, a claim "
                "that does not", "attach to its subject, or a noun stack hiding an actor. "
                "It never gates and its exit code is 0."]
    return "\n".join(out) + "\n"


# --- the self-test --------------------------------------------------------------------------

# Two slides, one deliberately hard and one deliberately plain, saying the same thing. The hard one
# is built from the faults report `025` names: nominalisation, noun stacks and abstraction.
HARD = ("The implementation of the reconciliation methodology necessitates the identification of "
        "the discrepancies prior to the finalisation of the consolidation activity.")
PLAIN = ("We reconcile the accounts. Find the gaps first, then close the books.")

FIXTURE = (
    '<section class="slide" data-name="hard">'
    '<p class="eyebrow">Reconciliation</p>'
    '<h2 class="headline">Close the books</h2>'
    '<p class="body">%s</p></section>'
    '<section class="slide" data-name="plain">'
    '<p class="eyebrow">Reconciliation</p>'
    '<h2 class="headline">Close the books</h2>'
    '<p class="body">%s</p>'
    '<svg viewBox="0 0 10 10"><text class="lab">Jan</text>'
    '<text class="lab">Feb</text></svg></section>') % (HARD, PLAIN)


def self_test():
    """Prove the instrument in **both** directions (**L-125**): hard copy scores hard on every
    measure, and plain copy is not reported as hard. One direction alone passes for an instrument
    that returns a constant."""
    hard, plain = measure(HARD), measure(PLAIN)
    for name, worse, better in (("flesch", plain, hard),
                                ("grade", hard, plain),
                                ("fog", hard, plain),
                                ("three_syllable", hard, plain),
                                ("nominalisations", hard, plain)):
        if not worse[name] > better[name]:
            sys.exit("SELF-TEST FAILED: %s did not separate the two fixtures - hard %r, plain %r. "
                     "An instrument that cannot rank deliberately hard copy above deliberately "
                     "plain copy cannot rank a deck's" % (name, hard[name], plain[name]))
    if band(hard["flesch"]) == band(plain["flesch"]):
        sys.exit("SELF-TEST FAILED: both fixtures landed in the %r band" % band(hard["flesch"]))

    # the ranking names the hard line and does not name the plain one
    lines = lines_of(FIXTURE)
    ranked = hardest(lines, 1)
    if not ranked:
        sys.exit("SELF-TEST FAILED: nothing ranked, over %d line(s)" % len(lines))
    if ranked[0][4] != HARD:
        sys.exit("SELF-TEST FAILED: the hardest line came out as %r" % (ranked[0][4],))
    if any(text == PLAIN for _f, _w, _s, _fi, text, _m in hardest(lines, 1)):
        sys.exit("SELF-TEST FAILED: the plain line was ranked hardest")

    # a short line is not ranked, or the list names eyebrows instead of sentences
    if any(len(WORD.findall(text)) < RANK_MIN_WORDS
           for _f, _w, _s, _fi, text, _m in hardest(lines, 20)):
        sys.exit("SELF-TEST FAILED: a line under %d words was ranked" % RANK_MIN_WORDS)

    # the drawn labels are counted out rather than dropped in silence (L-149)
    skipped, fields = counted_out(FIXTURE)
    if skipped != 2 or fields.get("drawn labels") != 2:
        sys.exit("SELF-TEST FAILED: the fixture's two drawn labels were counted as %r, %r - text "
                 "this does not read has to be counted, or the report is silent about it"
                 % (skipped, fields))
    for _s, _f, text in lines:
        if text in ("Jan", "Feb"):
            sys.exit("SELF-TEST FAILED: a drawn label reached the prose subject")

    # an empty subject answers `None`, not zero - a deck with no prose is not the easiest deck
    if measure("") is not None or measure("   ") is not None:
        sys.exit("SELF-TEST FAILED: empty copy was measured rather than refused")


def main(argv):
    self_test()
    if argv and argv[0] == "--self-test":
        print("self-test passed - hard copy ranks above plain on every measure, the ranking names "
              "the hard line, short lines and drawn labels stay out of it, and empty copy is "
              "refused rather than scored")
        return 0
    if not argv or argv[0] in ("-h", "--help"):
        print("python tools/deck/readability.py <deck> [--lines N]\n"
              "Reports how hard the copy is and names the hardest lines. It never gates.")
        return 0 if argv else 2

    limit = 10
    if "--lines" in argv:
        limit = int(argv[argv.index("--lines") + 1])
    deck = argv[0]
    html = content.strip_comments(open(deck, encoding="utf-8").read())
    print("%s - a measurement, not a verdict.\n" % deck)
    print(report(html, limit))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
