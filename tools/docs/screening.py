#!/usr/bin/env python3
"""Check that the screening partition still counts the catalogue it claims to partition.

    python tools/docs/screening.py

`docs/CONTEXT-AUDIT.md` §4 states *"the three verdicts partition the catalogue: 12 adopted, 10
rejected, 13 deferred, summing to 35"*, over a table it contains, about a catalogue in
`docs/research/R8-context-economy-for-coding-agents.md` §7.2 that it does not.

**Why this is a tool and not an `ACCOUNTS` entry in `figures.py`.** That binding was the obvious
route and it cannot serve, for the reason the claim exists to guard against. `figures.py` binds a
prose numeral by finding a field whose **value** matches and whose label the sentence names - so a
figure that has drifted matches no field, binds to nothing, and lands in `unanchored` with four
hundred numerals that are not figures at all. It would report `compared` for exactly as long as the
number was already right. That is **L-97**, *a check anchored on the value that drifts goes blind
exactly when it is needed*, and §1 of T-156 names it. A partition has to be asserted the other way
round: **count the rows, then require the page to say that number** (**L-104**).

**The sum was never the check anyone thought it was.** It summed correctly at 19 while two techniques
were missing, and again at 21 while fourteen were - the arithmetic was self-consistent and the
catalogue was short both times (**L-84**). So the id sets are compared across the two documents as
well, which is the only half that can see a technique nobody screened.

Runs its own self-test first and refuses to report if it fails (**L-04**). Pure standard library
(**L-07**).
"""

import io
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

AUDIT = "docs/CONTEXT-AUDIT.md"
CATALOGUE = "docs/research/R8-context-economy-for-coding-agents.md"

VERDICTS = ("adopted", "rejected", "deferred")

# The claim, bound on its own vocabulary and its own order. **It must match or the run fails**: a
# reworded sentence is a claim this tool can no longer read, and covering nothing quietly is the
# failure mode every hand-kept declaration here is written against (`figures.py`'s ARTIFACTS).
PARTITION = re.compile(r"(\d+)\s+adopted,\s+(\d+)\s+rejected,\s+(\d+)\s+deferred,\s+"
                       r"summing\s+to\s+(\d+)")

# A catalogue row in either document: a table row whose first cell is a technique id. Both tables
# use it, and nothing else in either document does.
ROW = re.compile(r"^\|\s*(T\d+)\s*\|")

# A verdict cell is bolded in the screening table and nowhere else on the row.
VERDICT_CELL = re.compile(r"\*\*(%s)\*\*" % "|".join(VERDICTS))


def read(rel):
    return io.open(os.path.join(ROOT, rel.replace("/", os.sep)), encoding="utf-8").read()


def section(text, heading):
    """The lines of `text` from `heading` up to the next heading of the same or higher level.

    Anchored on the heading rather than on a line number, so an edit above it cannot silently move
    what this tool counts.
    """
    depth = len(heading) - len(heading.lstrip("#"))
    out, inside = [], False
    for line in text.split("\n"):
        if line.startswith(heading):
            inside = True
            continue
        if inside and line.startswith("#"):
            here = len(line) - len(line.lstrip("#"))
            if here <= depth:
                break
        if inside:
            out.append(line)
    return out


def screened(text):
    """`{id: verdict}` for every row of the screening table, and `None` for a row carrying none."""
    out = {}
    for line in section(text, "## 4."):
        m = ROW.match(line)
        if m:
            v = VERDICT_CELL.search(line)
            out[m.group(1)] = v.group(1) if v else None
    return out


def catalogued(text):
    """The set of technique ids the catalogue itself lists."""
    return set(m.group(1) for m in (ROW.match(l) for l in section(text, "### 7.2")) if m)


def stated(text):
    """`(adopted, rejected, deferred, total)` as the page writes them, or `None`."""
    m = PARTITION.search(text)
    return tuple(int(g) for g in m.groups()) if m else None


def counted(rows):
    """`(adopted, rejected, deferred, total)` as the table actually is."""
    return tuple([sum(1 for v in rows.values() if v == name) for name in VERDICTS]
                 + [len(rows)])


def problems(audit_text, cat_text):
    """`[complaint]` - every disagreement between the sentence, its table, and the catalogue."""
    out = []
    rows = screened(audit_text)
    said = stated(audit_text)
    got = counted(rows)

    if said is None:
        out.append("%s states no partition this tool can read. The sentence is matched on its own "
                   "words - `N adopted, M rejected, K deferred, summing to S` - and a rewording "
                   "leaves the claim unchecked, which is the state T-156 was raised from" % AUDIT)
    elif said != got:
        for i, name in enumerate(VERDICTS):
            if said[i] != got[i]:
                out.append("%s says %d %s and its own table holds %d"
                           % (AUDIT, said[i], name, got[i]))
        if said[3] != got[3]:
            out.append("%s says the catalogue sums to %d and its own table holds %d rows"
                       % (AUDIT, said[3], got[3]))

    blank = sorted(k for k, v in rows.items() if v is None)
    if blank:
        out.append("%s screens %s without a verdict, so the row is in the total and in no part"
                   % (AUDIT, ", ".join(blank)))

    # **The half the sum can never see.** A technique added to the catalogue and never screened
    # leaves the partition self-consistent and the coverage short - twice, measured.
    cat = catalogued(cat_text)
    if not cat:
        out.append("%s lists no catalogue rows, so the cross-document check covers nothing" % CATALOGUE)
    unscreened = sorted(cat - set(rows), key=lambda t: int(t[1:]))
    ghosts = sorted(set(rows) - cat, key=lambda t: int(t[1:]))
    if unscreened:
        out.append("%s catalogues %s and %s screens none of them - the partition sums correctly "
                   "and the coverage is short, which is what it did at 19 and at 21"
                   % (CATALOGUE, ", ".join(unscreened), AUDIT))
    if ghosts:
        out.append("%s screens %s and %s catalogues no such technique"
                   % (AUDIT, ", ".join(ghosts), CATALOGUE))
    return out


def self_test():
    """Seeded on a synthetic pair, never on the live documents (**L-78**, **L-85**) - the numbers
    here are the subject of the check, so a fixture quoting them asserts today and reddens tomorrow.
    Each case is judged by its **message**, because an assertion that cannot run still exits
    non-zero (**L-55**)."""
    def pages(said_a=2, said_r=1, said_d=1, said_s=4, rows=None, cat=None):
        rows = ["| T1 | one | **adopted** | why |", "| T2 | two | **adopted** | why |",
                "| T3 | three | **rejected** | why |",
                "| T4 | four | **deferred** | why |"] if rows is None else rows
        cat = ["| T1 | one |", "| T2 | two |", "| T3 | three |",
               "| T4 | four |"] if cat is None else cat
        audit = ("## 4. Screening\n\nThe three verdicts partition the catalogue: %d adopted, "
                 "%d rejected, %d deferred, summing to %d.\n\n| # | T | V | W |\n| :- | :- | :- | :- |\n"
                 % (said_a, said_r, said_d, said_s) + "\n".join(rows)
                 + "\n\n## 5. After\n\nnot counted: | T9 | stray |\n")
        return audit, "### 7.2 The catalogue\n\n| # | T |\n| :- | :- |\n" + "\n".join(cat) + "\n"

    audit, cat = pages()
    if problems(audit, cat):
        sys.exit("SELF-TEST FAILED: a partition that agrees with its table and its catalogue was "
                 "reported as broken (%r). A check that fires on the ordinary case is switched off "
                 "the week it lands" % problems(audit, cat))

    # **A wrong number in the sentence, one verdict at a time**, and the message must name the
    # document - criterion 2 asks for the failure to say *which*.
    for i, name in enumerate(VERDICTS):
        seed = [2, 1, 1, 4]
        seed[i] += 1
        bad = problems(*pages(seed[0], seed[1], seed[2], 4))
        if not [p for p in bad if name in p and AUDIT in p]:
            sys.exit("SELF-TEST FAILED: the sentence was seeded to overstate `%s` by one and the "
                     "run reported %r. A partition checked against itself is what has already been "
                     "wrong twice" % (name, bad))

    if not [p for p in problems(*pages(said_s=5)) if "sums to" in p]:
        sys.exit("SELF-TEST FAILED: a stated total the table does not reach passed. The total is the "
                 "half a reader trusts most, because the three parts are tedious to count by hand")

    # **A technique catalogued and never screened** - the case the partition cannot see by
    # construction, and the one this tool exists for (**L-84**).
    grew = ["| T1 | one |", "| T2 | two |", "| T3 | three |", "| T4 | four |", "| T5 | five |"]
    missed = problems(*pages(cat=grew))
    if not [p for p in missed if "T5" in p and CATALOGUE in p]:
        sys.exit("SELF-TEST FAILED: a row added to the catalogue and left unscreened raised nothing "
                 "(%r). The partition still sums - it summed at 19 with two missing and at 21 with "
                 "fourteen - so this is the only half of the check that can see it" % (missed, ))

    # The other direction: a screened id the catalogue does not carry. Silence here would let the
    # screening table drift into inventing techniques.
    if not [p for p in problems(*pages(cat=["| T1 | one |", "| T2 | two |", "| T3 | three |"]))
            if "T4" in p]:
        sys.exit("SELF-TEST FAILED: a screened technique absent from the catalogue raised nothing")

    # A row with no verdict is in the total and in no part, so the parts stop summing to it.
    no_verdict = ["| T1 | one | **adopted** | why |", "| T2 | two | **adopted** | why |",
                  "| T3 | three | **rejected** | why |", "| T4 | four | pending | why |"]
    if not [p for p in problems(*pages(rows=no_verdict)) if "without a verdict" in p]:
        sys.exit("SELF-TEST FAILED: a catalogue row carrying no verdict was counted into the total "
                 "and into no part, and nothing said so")

    # A sentence this tool cannot read must fail, not pass quietly - the ARTIFACTS condition.
    unreadable = pages()[0].replace("summing to 4", "and that is all of them")
    if not [p for p in problems(unreadable, cat) if "no partition" in p]:
        sys.exit("SELF-TEST FAILED: a page whose partition sentence was reworded beyond this tool's "
                 "reading passed. A declaration that comes to cover nothing has to say so")
    return True


def report():
    audit_text, cat_text = read(AUDIT), read(CATALOGUE)
    rows = screened(audit_text)
    got = counted(rows)
    said = stated(audit_text)

    print("Screening partition - %s section 4 against %s section 7.2\n" % (AUDIT, CATALOGUE))
    bad = problems(audit_text, cat_text)
    for p in bad:
        print("  MISMATCH   %s" % p)

    print("\n  counted from the screening table")
    for i, name in enumerate(VERDICTS):
        print("    %-12s %3d" % (name, got[i]))
    print("    %-12s %3d   = every row, so the three verdicts are a partition" % ("total", got[3]))
    print("\n  stated in the sentence")
    print("    %s" % ("%d adopted, %d rejected, %d deferred, summing to %d" % said
                      if said else "UNREADABLE - the sentence no longer matches the claim shape"))
    print("\n  the catalogue this partitions")
    print("    %-12s %3d   = rows in %s section 7.2" % ("techniques", len(catalogued(cat_text)),
                                                        CATALOGUE))

    print("\n%s" % ("%d disagreement(s) to fix" % len(bad) if bad else
                    "0 disagreements - the sentence, its table and the catalogue agree"))
    print("\nThis counts rows and compares ids. It cannot tell you a verdict is right, or that the\n"
          "catalogue is complete - R8 section 7.1's search record is what carries that.")
    return 1 if bad else 0


if __name__ == "__main__":
    self_test()
    sys.exit(report())
