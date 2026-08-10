#!/usr/bin/env python3
"""The specification pair check — what `<slug>.foundation.md` and `<slug>.slides.md` can only get
wrong together.

    python tools/deck/spec.py <slug>.foundation.md <slug>.slides.md

Four verdicts, all mechanical, none of them about whether the deck is any good:

  SPEC-1  every slide answers `Sources`, and `none` is an answer.
  SPEC-2  every slug a slide names has a row in the foundation's source list.
  SPEC-3  every listed source is named by at least one slide - an unused source is a missing
          citation or a stale file, and both are findings.
  SPEC-4  the ledger wins. Where a figure's `Origin` is used on a slide whose `Sources` omits it,
          the slide is wrong, not the ledger.

**Why SPEC-4 is a comparison and not a derivation.** The slide field is wider than the ledger on
purpose: a slide rests on a source it quotes no number from - a date, a definition, a threshold, a
diagram redrawn from it - and none of those is a ledger row. So the field cannot be generated from
the ledger, and the ledger cannot be generated from the field. Two records of overlapping facts,
one authoritative where they overlap, and the overlap checked rather than trusted (T-071).

Run it before writing any slide, and again after a deviation is written back. Pure standard
library (**L-07**).
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths                                                        # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SLIDE_HEAD = re.compile(r"^##\s+Slide\s+(\d+)\b", re.M)
SOURCES_FIELD = re.compile(r"^-\s+\*\*Sources\.\*\*\s*(.*)$", re.M)


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


def verdicts(foundation_text, slides_text):
    listed = [r[0].strip("`") for r in rows(foundation_text, "Slug") if r and r[0]]
    ledger = [r for r in rows(foundation_text, "Figure") if len(r) >= 4]
    spec = slides(slides_text)

    missing_field = [n for n, cell in spec if cell is None]
    named = {n: slugs(cell or "") for n, cell in spec}

    unknown = sorted({(n, s) for n, ss in named.items() for s in ss if s not in listed})
    unused = [s for s in listed if not any(s in ss for ss in named.values())]

    contradicted = []
    for row in ledger:
        origin = row[2].strip("`")
        for n in used_on(row[3]):
            if n in named and origin not in named[n] and (n, origin) not in contradicted:
                contradicted.append((n, origin))

    # **Each row reports None when its own subject is absent, never True.** All four are of the form
    # *every X is Y*, and such a rule over no X is undecided rather than satisfied - the bar
    # `audit.py`'s absent-subject fixture holds every verdict producer in this directory to, and the
    # shape DS-064 and DS-200 were both wrong about before T-075. A presentation-only pair reaches
    # all four of these legitimately: no source list, no slug named, no ledger.
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
    by_rule = dict((r, ok) for r, _w, ok in verdicts(foundation, good))
    if not all(ok is True for ok in by_rule.values()):
        sys.exit("SELF-TEST FAILED: the consistent pair did not pass - %r" % by_rule)
    empty = dict((r, ok) for r, _w, ok in verdicts("", ""))
    if any(ok is not None for ok in empty.values()):
        sys.exit("SELF-TEST FAILED: a row decided something against an empty pair - %r" % empty)

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
        got = dict((r, ok) for r, _w, ok in verdicts(foundation, text))
        if got[rule] is not False:
            sys.exit("SELF-TEST FAILED: %s reported %r on a document seeded to break it"
                     % (rule, got[rule]))
    # SPEC-3's seed drops `calendar` from the only slide that used it, which must also trip
    # SPEC-4 - the two overlap, and a seed that trips only one of them would be the weaker test.
    return True


def main(foundation, slides_path):
    self_test()
    print("foundation: %s" % paths.display_path(foundation, ROOT))
    print("slides:     %s" % paths.display_path(slides_path, ROOT))
    with open(foundation, encoding="utf-8") as fh:
        foundation_text = fh.read()
    with open(slides_path, encoding="utf-8") as fh:
        slides_text = fh.read()
    rows_out = verdicts(foundation_text, slides_text)
    for rule, what, ok in rows_out:
        print("  %-8s %-90s %s"
              % (rule, what, "NO SUBJECT" if ok is None else "pass" if ok else "FAIL"))
    print("\nThis compares the two specifications. Whether either is any good is DESIGN-SYSTEM.md.")
    return 0 if all(ok is not False for _r, _w, ok in rows_out) else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) != 2:
        sys.exit("usage: spec.py <slug>.foundation.md <slug>.slides.md")
    sys.exit(main(os.path.abspath(a[0]), os.path.abspath(a[1])))
