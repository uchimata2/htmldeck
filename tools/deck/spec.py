#!/usr/bin/env python3
"""The specification pair check — what `<slug>.foundation.md` and `<slug>.slides.md` can only get
wrong together, plus the one thing the built deck settles about the ledger.

    python tools/deck/spec.py <slug>.foundation.md <slug>.slides.md [<slug>.html]

Five verdicts, all mechanical, none of them about whether the deck is any good:

  SPEC-1  every slide answers `Sources`, and `none` is an answer.
  SPEC-2  every slug a slide names has a row in the foundation's source list.
  SPEC-3  every listed source is named by at least one slide - an unused source is a missing
          citation or a stale file, and both are findings.
  SPEC-4  the ledger wins. Where a figure's `Origin` is used on a slide whose `Sources` omits it,
          the slide is wrong, not the ledger.
  SPEC-5  and here the ledger loses. Where a row's `Used on` names a slide, that slide has to
          show the value. Needs the built deck, so it is undecided without one.

**Why SPEC-4 is a comparison and not a derivation.** The slide field is wider than the ledger on
purpose: a slide rests on a source it quotes no number from - a date, a definition, a threshold, a
diagram redrawn from it - and none of those is a ledger row. So the field cannot be generated from
the ledger, and the ledger cannot be generated from the field. Two records of overlapping facts,
one authoritative where they overlap, and the overlap checked rather than trusted (T-071).

**Why SPEC-5 exists, and why it is the only half of the ledger question that is checkable.** SPEC-4
trusts `Used on` to decide whether a slide's `Sources` is right, so a cell naming a slide the figure
never reached mis-calibrates the rule built on it - T-082's hand sweep found four such cells and this
found a fifth. The mirror question, whether the ledger is *complete*, needs something that can
enumerate every figure on a slide, and nothing here can: `content.py`'s figure pattern cannot see
`6 rounds`, `04:10` or `27 of 31`, and widening it to any digit makes every axis tick a figure. So
completeness stays DS-102's `judge` (T-082 §3, **L-62**), and this rule searches for a known string
on a known slide instead of deciding what a figure is.

**The deck argument is optional on purpose.** This tool is meant to run before a slide is written,
let alone built; a required deck would break its own instructions. With no deck SPEC-5 reports no
subject, exactly as the other four do when theirs is absent. **A deck that was supplied and parsed
to no slides is not that**, and since T-090 it is a FAIL naming the cause: the two arrived at one
verdict, and a rule that skips itself must not be able to say so in the words for *not applicable*.

Run it before writing any slide, and again after a deviation is written back. Pure standard
library (**L-07**).
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths                                                        # noqa: E402
import content                                                      # noqa: E402  - for `runs`

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SLIDE_HEAD = re.compile(r"^##\s+Slide\s+(\d+)\b", re.M)
SOURCES_FIELD = re.compile(r"^-\s+\*\*Sources\.\*\*\s*(.*)$", re.M)

# The deck already declares its own slide numbers, and `Used on` is written in them. Reading the
# number rather than counting sections means a deck that ships a colophon or any other section
# outside the run cannot silently shift every row by one.
SLIDE_SECTION = re.compile(r'<section[^>]*class="[^"]*\bslide\b[^"]*"[^>]*>(.*?)</section>',
                           re.S | re.I)
# **A number-bearing prefix, not the whole accessible name.** This closed on the quote until T-090,
# so it matched a label that is NOTHING BUT `Slide N` - the form both decks in this repository
# happen to ship. An adopter's deck labelled `Slide 1 of 12: <title>` parsed to no slides at all,
# and SPEC-5 then reported the same `NO SUBJECT` as a run with no deck: a whole gate skipped with
# nothing said. Neither DESIGN-SYSTEM.md nor COMPONENT-CONTRACT.md §3.2 constrains the wording, and
# the longer name is the better one, so the pattern was what needed widening.
SLIDE_NUMBER = re.compile(r'aria-label="Slide\s+(\d+)\b', re.I)

WORD_NUMBERS = "one two three four five six seven eight nine ten eleven twelve".split()
MONTHS = ("january february march april may june july august september october "
          "november december").split()


def rows(text, first_column):
    """Every data row of the one markdown table whose header starts with `first_column`.

    Returns a list of cell lists. The separator row and anything outside the table are dropped;
    a document with no such table gives `[]`, which is what a presentation-only run looks like.
    """
    out, inside = [], False
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            inside = False
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells and cells[0].lower() == first_column.lower():
            inside = True
            continue
        if not inside:
            continue
        if set("".join(cells)) <= set(":- "):
            continue
        out.append(cells)
    return out


def slugs(cell):
    """The slugs in one `Sources` answer. `none` is empty, and so is a blank."""
    cell = re.sub(r"[`*]", "", cell).strip().rstrip(".")
    if not cell or cell.lower() == "none":
        return []
    return [s.strip() for s in re.split(r"[,;]", cell) if s.strip()]


def slides(text):
    """`(number, sources-cell-or-None)` per slide, in document order."""
    heads = list(SLIDE_HEAD.finditer(text))
    out = []
    for i, head in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        body = text[head.end():end]
        field = SOURCES_FIELD.search(body)
        out.append((int(head.group(1)), field.group(1) if field else None))
    return out


def used_on(cell):
    """The slide numbers in a ledger row's `Used on` cell."""
    return [int(n) for n in re.findall(r"\d+", cell)]


def canonical(text):
    """One spelling for the two ways a deck legitimately writes the same figure.

    Both were measured on `sort-window` rather than anticipated, and between them they account for
    ten of the nineteen pairs a literal search could not decide:

    - **a small number spelled as a word.** The ledger says `6 people`; the slide says *Six people*
      in its headline and *six-person crew* in its body. One to twelve, which is where English
      stops spelling by default and where the corpus stops too.
    - **a month abbreviated.** The ledger says `4 September`; the timeline chip says *4 Sep*.

    Hyphens fold to spaces for the same reason - *six-person* has to reach `6 person`. Nothing here
    guesses at a figure's meaning; it normalises how the same string is written.
    """
    t = text.lower().replace("\u2019", "'")
    t = re.sub(r"[\u2010-\u2015\u2212]", "-", t).replace("-", " ")
    # nbsp, figure, thin, narrow-nbsp, en and em spaces - a deck sets figures with them.
    t = t.translate(dict.fromkeys(
        map(ord, "\u00a0\u2007\u2009\u202f\u2002\u2003"), " "))
    for month in MONTHS:
        t = re.sub(r"\b%s\.?\b" % month[:3], month, t)
    for i, word in enumerate(WORD_NUMBERS, 1):
        t = re.sub(r"\b%s\b" % word, str(i), t)
    return re.sub(r"\s+", " ", t)


def slide_text(deck_html):
    """`{slide number: canonical text}` for every slide the deck declares a number for.

    `content.runs` does the splitting, because reading a slide as one string merges an axis label
    into the figure beside it - the mistake it carries its own comment about.
    """
    out = {}
    for m in SLIDE_SECTION.finditer(content.strip_comments(deck_html)):
        number = SLIDE_NUMBER.search(m.group(0))
        if number:
            out[int(number.group(1))] = canonical(" ".join(content.runs(m.group(1))))
    return out


def shows(text, value):
    """Whether `text` carries `value` as a value rather than as part of a longer one.

    The two guards are the whole of it. `27` may not match inside `27,600`, and `9` may not match
    inside `95%` - but a value that ends in a symbol needs no closing guard at all, which is what
    lets `5%` match where the run splitter has left it flush against the next word.
    """
    v = canonical(value).strip()
    if not v:
        return False
    tail = r"(?!\w|,\d|\.\d)" if re.search(r"\w$", v) else ""
    return re.search(r"(?<![\w.,$])" + re.escape(v) + tail, text) is not None


def reaches(text, value):
    """Whether a ledger row's value reaches one slide, in any of the three forms it may take.

    1. **As written.** 80 of the 89 pairs on the worked example, and the only form a reader of the
       ledger would predict.
    2. **As one mark of a series.** `4.1 / 11.2 / 15.9 / 18.7%` is one row and four marks, and one
       mark is the bar this rule may ask for: the chart on slide 4 labels its maximum and prints
       *3.4% or under* for the four months below it, so demanding every mark would fail a deck that
       is right. The row still binds the series to the slide, which is what `Used on` claims.
    3. **As its leading quantity.** `6 people` reaches a slide that says *Six people*; the unit noun
       is the ledger's description of the figure, not the figure.
    """
    for part in ([p.strip() for p in value.split(" / ")] if " / " in value else [value]):
        if shows(text, part):
            return True
        quantity = re.search(r"\S*\d\S*", canonical(part))
        if quantity and quantity.group(0) != canonical(part).strip() \
                and shows(text, quantity.group(0)):
            return True
    return False


def verdicts(foundation_text, slides_text, deck_html=""):
    listed = [r[0].strip("`") for r in rows(foundation_text, "Slug") if r and r[0]]
    ledger = [r for r in rows(foundation_text, "Figure") if len(r) >= 4]
    spec = slides(slides_text)

    missing_field = [n for n, cell in spec if cell is None]
    named = {n: slugs(cell or "") for n, cell in spec}

    unknown = sorted({(n, s) for n, ss in named.items() for s in ss if s not in listed})
    unused = [s for s in listed if not any(s in ss for ss in named.values())]

    # **`Origin` is a list, and one entry of it is a reserved word** (T-194).
    #
    # It read `row[2].strip("`")` until 2026-08-20 - one slug, so a row citing two arrived as a
    # single slug named `` exercise`, `notes ``, matched nothing listed, and SPEC-4 failed. A deck
    # whose job is to cross-check two documents produces such rows **by construction**: the first
    # outside build was nine of them, and its author's only recourse was to pick one origin and put
    # the truth in prose - the ledger lying to keep the gate quiet, which is the opposite of what a
    # ledger is for. `slugs()` already splits and strips exactly this shape for the slide's own
    # `Sources` cell; the two cells now read the same way.
    #
    # **`derived` is the third kind, and it is a different claim from either source.** A figure a
    # deck works out by comparing two documents is stated in neither of them, so *both sources* and
    # *neither source* are not the same answer and the ledger has to be able to make each. It is
    # reserved rather than free text so the check can tell a claim from a typo, and it composes: a
    # row may read `` `exercise`, `notes`, derived `` - these two documents, and the number is ours.
    contradicted = []
    for row in ledger:
        for origin in [o for o in slugs(row[2]) if o.lower() != "derived"]:
            for n in used_on(row[3]):
                if n in named and origin not in named[n] and (n, origin) not in contradicted:
                    contradicted.append((n, origin))

    # **Each row reports None when its own subject is absent, never True.** All four are of the form
    # *every X is Y*, and such a rule over no X is undecided rather than satisfied - the bar
    # `audit.py`'s absent-subject fixture holds every verdict producer in this directory to, and the
    # shape DS-064 and DS-200 were both wrong about before T-075. A presentation-only pair reaches
    # all four of these legitimately: no source list, no slug named, no ledger.
    # SPEC-5's subject is a pair - a ledger row that names a slide, and a deck that has slides to
    # name. A `Used on` naming a slide the deck does not have is a FAIL and not an absent subject:
    # the cell is a claim about a deck, and a claim about a slide that does not exist is the
    # strongest form of the error this rule is for.
    # **A deck that was supplied and could not be read is its own verdict, and it is a FAIL.**
    # `absent` and `unparsed` used to arrive at the same `None`, and only one of the two is benign:
    # `NO SUBJECT` reads as *not applicable*, so the author of an unreadable deck was told nothing
    # (T-090). It stays inside the three verdict values rather than becoming a fourth, because
    # `audit.py`'s absent-subject fixture partitions every producer's rows on `True in oks` and
    # `False in oks` - a fourth value would fall in neither and put this family back outside the
    # fixture, which is the failure T-066 and T-075 exist to prevent.
    on_deck = slide_text(deck_html) if deck_html else {}
    unreadable = bool(deck_html) and not on_deck
    unbuilt, unshown, claimed = [], [], 0
    if on_deck:
        for row in ledger:
            for n in used_on(row[3]):
                claimed += 1
                if n not in on_deck:
                    unbuilt.append("slide %d does not exist (%s)" % (n, row[0]))
                elif not reaches(on_deck[n], row[1]):
                    unshown.append("slide %d does not show %s (%s)" % (n, row[0], row[1]))

    any_named = any(ss for ss in named.values())
    scored = [r for row in ledger for r in used_on(row[3]) if r in named]
    return [
        ("SPEC-1", "every slide answers Sources%s" % (
            "" if not missing_field else " - missing on %s" % _list(missing_field)),
         None if not spec else not missing_field),
        ("SPEC-2", "every named slug is listed%s" % (
            "" if not unknown else " - %s" % ", ".join(
                "slide %d cites %s" % (n, s) for n, s in unknown)),
         None if not any_named else not unknown),
        ("SPEC-3", "every listed source is used%s" % (
            "" if not unused else " - unused: %s" % ", ".join(unused)),
         None if not listed else not unused),
        ("SPEC-4", "slides agree with the ledger%s" % (
            "" if not contradicted else " - %s" % ", ".join(
                "slide %d omits %s" % (n, s) for n, s in contradicted)),
         None if not scored else not contradicted),
        ("SPEC-5", "every ledger row reaches the slides it names%s" % (
            " - DECK UNREADABLE: a deck was supplied and no slide parsed from it, so this rule "
            "did not run. Every slide needs aria-label=\"Slide N ...\"" if unreadable else
            "" if not (unbuilt + unshown) else " - %s" % "; ".join(unbuilt + unshown)),
         False if unreadable else None if not claimed else not (unbuilt or unshown)),
    ]


def _list(numbers):
    return ", ".join(str(n) for n in numbers)


def self_test():
    """One consistent pair, then the same pair with each defect seeded, one at a time.

    A checker is only worth its green run if its red one has been seen (**L-04**), and matching a
    tool's *command list* proves nothing about what it catches (**L-57**) - so every verdict is
    made to fail here on purpose.
    """
    foundation = ("## Sources and the figure ledger\n\n"
                  "| Slug | Source | What it carries |\n| :--- | :--- | :--- |\n"
                  "| cost-model | Cost model | money |\n| calendar | Calendar | dates |\n\n"
                  "| Figure | Value | Origin | Used on |\n| :--- | :--- | :--- | :--- |\n"
                  "| Capital | $1 | cost-model | 2 |\n")
    good = ("## Slide 1 - a\n\n- **Sources.** none\n\n"
            "## Slide 2 - b\n\n- **Sources.** cost-model, calendar\n")
    deck = ('<section class="slide" aria-label="Slide 1"><h2>a</h2></section>'
            '<section class="slide" aria-label="Slide 2"><p>The grant is <b>$1</b>.</p></section>')
    by_rule = dict((r, ok) for r, _w, ok in verdicts(foundation, good, deck))
    if not all(ok is True for ok in by_rule.values()):
        sys.exit("SELF-TEST FAILED: the consistent pair did not pass - %r" % by_rule)
    empty = dict((r, ok) for r, _w, ok in verdicts("", ""))
    if any(ok is not None for ok in empty.values()):
        sys.exit("SELF-TEST FAILED: a row decided something against an empty pair - %r" % empty)
    # **The two-argument run has to be exactly what it was**, because that is what makes the deck
    # optional rather than a breaking change: this tool's own instructions say to run it before a
    # slide is written, and a deck cannot exist then. Asserted rather than assumed - it is the whole
    # of the decision in T-086 §3 to put this rule here instead of in a file of its own.
    without = dict((r, ok) for r, _w, ok in verdicts(foundation, good))
    if [r for r, ok in without.items() if ok is not (None if r == "SPEC-5" else True)]:
        sys.exit("SELF-TEST FAILED: the run with no deck did not leave SPEC-1..4 alone and "
                 "SPEC-5 undecided - %r" % without)

    # **A two-source row, and a derived one** (T-194). Both are what a cross-check deck produces
    # and neither parsed before 2026-08-20: the first arrived as one slug named after both, the
    # second had no way to say *this number is in neither document*. Seeded failing first - with
    # `row[2].strip("`")` in place, the two-source pair reports SPEC-4 `False`.
    two = foundation.replace("| Capital | $1 | cost-model | 2 |",
                             "| Capital | $1 | `cost-model`, `calendar` | 2 |\n"
                             "| Gap | $2 | `cost-model`, `calendar`, derived | 2 |")
    got = dict((r, ok) for r, _w, ok in verdicts(two, good, deck))
    if got["SPEC-4"] is not True:
        sys.exit("SELF-TEST FAILED: a ledger row citing two sources, and one derived from them, "
                 "reported SPEC-4 %r against a slide whose Sources names both - %r"
                 % (got["SPEC-4"], got))
    # And the reserved word is not a way past the rule: an origin the slide does not name still fails.
    bad_two = foundation.replace("| Capital | $1 | cost-model | 2 |",
                                 "| Capital | $1 | `cost-model`, `nowhere` | 2 |")
    if dict((r, ok) for r, _w, ok in verdicts(bad_two, good, deck))["SPEC-4"] is not False:
        sys.exit("SELF-TEST FAILED: a second origin the slide does not cite was not reported")

    # **The label the adopter's deck carried, and the label this repository's two decks carry.**
    # Both parse, and the widened pattern is only worth having if the second still does - a fix
    # that trades one accepted form for another is not a widening (T-090).
    for label in ('aria-label="Slide 2 of 2: what the grant buys"',
                  'aria-label="Slide 2 - b"',
                  'aria-label="Slide 2"'):
        wide = deck.replace('aria-label="Slide 2"', label)
        got = dict((r, ok) for r, _w, ok in verdicts(foundation, good, wide))
        if got["SPEC-5"] is not True:
            sys.exit("SELF-TEST FAILED: SPEC-5 reported %r against a slide labelled %s. The rule "
                     "decides on any accessible name that names the slide's number; a name it "
                     "cannot read is the defect T-090 reported, not a deck at fault"
                     % (got["SPEC-5"], label))

    # **Absent and unparsed must not arrive at one verdict, and this is the assertion that says so.**
    # It is the whole of T-090: four rules passed on the adopter's deck, so it was plainly being
    # read, and SPEC-5 alone reported the words a two-argument run prints. A future widening of
    # SLIDE_NUMBER that re-collapses them fails here rather than in an adopter's build.
    unreadable_row = [(w, ok) for r, w, ok in
                      verdicts(foundation, good, "<section class='slide'><h2>a</h2></section>")
                      if r == "SPEC-5"]
    (what, ok), = unreadable_row
    if ok is not False:
        sys.exit("SELF-TEST FAILED: SPEC-5 reported %r for a deck that was supplied and parsed to "
                 "no slides. That is the state T-090 found collapsed into NO SUBJECT, and it has "
                 "to be its own" % ok)
    if "UNREADABLE" not in what or "supplied" not in what:
        sys.exit("SELF-TEST FAILED: the unparsed-deck verdict reads %r, which does not name the "
                 "cause. A reader has to be able to tell it from *not applicable*" % what)

    seeded = {
        "SPEC-1": ("## Slide 1 - a\n\n- **Archetype.** A-01\n\n"
                   "## Slide 2 - b\n\n- **Sources.** cost-model, calendar\n"),
        "SPEC-2": ("## Slide 1 - a\n\n- **Sources.** none\n\n"
                   "## Slide 2 - b\n\n- **Sources.** cost-model, calendar, ghost\n"),
        "SPEC-3": ("## Slide 1 - a\n\n- **Sources.** none\n\n"
                   "## Slide 2 - b\n\n- **Sources.** cost-model\n"),
        "SPEC-4": ("## Slide 1 - a\n\n- **Sources.** none\n\n"
                   "## Slide 2 - b\n\n- **Sources.** calendar\n"),
    }
    for rule, text in seeded.items():
        got = dict((r, ok) for r, _w, ok in verdicts(foundation, text, deck))
        if got[rule] is not False:
            sys.exit("SELF-TEST FAILED: %s reported %r on a document seeded to break it"
                     % (rule, got[rule]))
    # SPEC-3's seed drops `calendar` from the only slide that used it, which must also trip
    # SPEC-4 - the two overlap, and a seed that trips only one of them would be the weaker test.

    # SPEC-5 is seeded in the deck rather than in the slides, because the deck is its subject. Two
    # seeds, because the row has two ways to fail and the second was reachable by no other test:
    # a slide that shows a different value, and a `Used on` naming a slide nobody built.
    for what, seed in (("a slide that shows another value",
                        deck.replace("$1", "$2")),
                       ("a Used on naming a slide the deck does not have",
                        deck.replace('aria-label="Slide 2"', 'aria-label="Slide 3"'))):
        got = dict((r, ok) for r, _w, ok in verdicts(foundation, good, seed))
        if got["SPEC-5"] is not False:
            sys.exit("SELF-TEST FAILED: SPEC-5 reported %r against %s"
                     % (got["SPEC-5"], what))
    return True


def main(foundation, slides_path, deck_path=None):
    self_test()
    print("foundation: %s" % paths.display_path(foundation, ROOT))
    print("slides:     %s" % paths.display_path(slides_path, ROOT))
    print("deck:       %s" % (paths.display_path(deck_path, ROOT) if deck_path
                              else "not given - SPEC-5 has no subject"))
    with open(foundation, encoding="utf-8") as fh:
        foundation_text = fh.read()
    with open(slides_path, encoding="utf-8") as fh:
        slides_text = fh.read()
    deck_html = ""
    if deck_path:
        with open(deck_path, encoding="utf-8") as fh:
            deck_html = fh.read()
    rows_out = verdicts(foundation_text, slides_text, deck_html)
    for rule, what, ok in rows_out:
        print("  %-8s %-90s %s"
              % (rule, what, "NO SUBJECT" if ok is None else "pass" if ok else "FAIL"))
    print("\nThis compares the two specifications. Whether either is any good is DESIGN-SYSTEM.md.")
    return 0 if all(ok is not False for _r, _w, ok in rows_out) else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) not in (2, 3):
        sys.exit("usage: spec.py <slug>.foundation.md <slug>.slides.md [<slug>.html]")
    sys.exit(main(os.path.abspath(a[0]), os.path.abspath(a[1]),
                  os.path.abspath(a[2]) if len(a) == 3 else None))
